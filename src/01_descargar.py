"""01 · Descarga de datos crudos.

Baja de nuevo, sin buscar nada, todos los archivos cuya URL directa ya se
verificó (ver docs/fuentes.md). Guarda cada archivo en data/raw/<id>/ y
escribe data/raw/manifiesto.csv con tamaño, sha256 y fecha de descarga.

Las fuentes sin URL directa verificada (CLUES, SEP) no se descargan aquí:
Alejandro las sube al release "datos-crudos" del repo (ver data/raw/LEEME.md)
y este script las baja de ese release. CONAPO no está disponible (D24).

Uso:
    python src/01_descargar.py                    # baja lo que falte
    python src/01_descargar.py --forzar           # vuelve a bajar todo
    python src/01_descargar.py --solo clues sep_escuelas   # solo esas fuentes
"""

import argparse
import csv
import hashlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"

INEGI = "https://www.inegi.org.mx/contenidos"
MG = f"{INEGI}/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia"
GHSL = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A"
RELEASE = "https://github.com/AlexTheKing1/acambaro-acceso-servicios/releases/download/datos-crudos"

# id -> lista de (url, nombre de archivo)
FUENTES = {
    "censo2020_ageb_mza": [
        (f"{INEGI}/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_11_cpv2020_csv.zip",
         "ageb_mza_urbana_11_cpv2020_csv.zip"),
    ],
    "iter2020": [
        (f"{INEGI}/programas/ccpv/2020/datosabiertos/iter/iter_11_cpv2020_csv.zip",
         "iter_11_cpv2020_csv.zip"),
    ],
    "censo2010_ageb_mza": [
        (f"{INEGI}/programas/ccpv/2010/datosabiertos/ageb_y_manzana/resageburb_11_2010_csv.zip",
         "resageburb_11_2010_csv.zip"),
    ],
    "iter2010": [
        (f"{INEGI}/programas/ccpv/2010/datosabiertos/iter_11_2010_csv.zip",
         "iter_11_2010_csv.zip"),
    ],
    # Cartografía de cierre del Censo 2010, municipio de Acámbaro (urbana y rural).
    # Se usa la presentación en shapefile (_s); la _d es DWG de AutoCAD.
    "mg2010_acambaro": [
        (f"{MG}/urbana/SHP/Guanajuato/SHP/702825585853_s.zip", "702825585853_s.zip"),
        (f"{MG}/rural/SHP/Guanajuato/702825561291_s.zip", "702825561291_s.zip"),
    ],
    "mg2020": [
        (f"{MG}/marcogeo/889463807469/11_guanajuato.zip", "11_guanajuato.zip"),
    ],
    "mg2025": [
        (f"{MG}/marcogeo/794551163061/11_guanajuato.zip", "11_guanajuato.zip"),
    ],
    "mg_eic2025": [
        (f"{MG}/marcogeo/794551196649/11_guanajuato.zip", "11_guanajuato.zip"),
        # Michoacán: solo para escuelas y centros de salud a <= 10 km del límite (fase 2).
        (f"{MG}/marcogeo/794551196649/16_michoacandeocampo.zip", "16_michoacandeocampo.zip"),
    ],
    "eic2025": [
        (f"{INEGI}/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip",
         "conjunto_de_datos_eic2025_105_csv.zip"),
    ],
    # Guanajuato más Michoacán y Querétaro: el municipio colinda con Michoacán y
    # los servicios cercanos pueden quedar del otro lado del límite estatal.
    "denue": [
        (f"{INEGI}/masiva/denue/denue_{e}_csv.zip", f"denue_{e}_csv.zip") for e in ("11", "16", "22")
    ],
    # Catálogo de asentamientos humanos (colonias, fraccionamientos...) de Acámbaro,
    # servicio web del Catálogo Único de Claves Geoestadísticas del INEGI. Trae
    # clave, nombre y tipo, sin polígonos (D24). Respuesta JSON.
    "asentamientos": [
        ("https://gaia.inegi.org.mx/wscatgeo/v2/asentamientos/11/002", "asentamientos_11_002.json"),
    ],
    # GHSL: mosaico R7_C9 (Mollweide, 100 m) cubre todo el municipio.
    # Solo años observados (1975–2020); 2025 y 2030 son proyecciones y no se usan.
    "ghsl_built_s": [
        (f"{GHSL}/GHS_BUILT_S_E{a}_GLOBE_R2023A_54009_100/V1-0/tiles/"
         f"GHS_BUILT_S_E{a}_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip",
         f"GHS_BUILT_S_E{a}_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip")
        for a in range(1975, 2021, 5)
    ],
}

# Fuentes que Alejandro sube al release "datos-crudos" (nombres esperados en LEEME.md).
DEL_RELEASE = {
    # CLUES, corte agosto 2026 (DGIS, Secretaría de Salud), nacional
    "clues": ["ESTABLECIMIENTO_SALUD_202608.xlsx"],
    # Catálogo de centros de trabajo de la SEP: Guanajuato (11) y Michoacán (16)
    "sep_escuelas": ["cct11.csv", "cct16.csv"],
}
# Red de caminos para la escala municipio (D26). La Red Nacional de Caminos del
# INEGI no tiene URL directa localizable (sus páginas son dinámicas; 2 intentos
# fallidos el 2026-10-23), así que se usa OpenStreetMap vía Overpass, acotado al
# recuadro del municipio + 15 km (EPSG:4326). Solo vías transitables en vehículo,
# incluidas brechas y caminos de terracería (track).
OVERPASS = "https://overpass-api.de/api/interpreter"
BBOX_CAMINOS = (19.7768, -101.1485, 20.3649, -100.3379)   # sur, oeste, norte, este
CONSULTA_CAMINOS = (
    "[out:json][timeout:300];"
    'way["highway"~"^(motorway|trunk|primary|secondary|tertiary|unclassified|residential|'
    'motorway_link|trunk_link|primary_link|secondary_link|tertiary_link|living_street|service|track|road)$"]'
    "({},{},{},{});out geom;"
).format(*BBOX_CAMINOS)
OSM = {"osm_caminos": "overpass_caminos.json"}

# Opcionales: revisión de Alejandro en Google Maps (no es error que falten)
OPCIONALES = {
    "verificacion": ["verificacion_zonas.csv", "verificacion_servicios.csv"],
}


def bajar(url, destino, intentos=4):
    for i in range(intentos):
        try:
            with requests.get(url, stream=True, timeout=120) as r:
                if r.status_code == 404:
                    return "no existe (404)"
                r.raise_for_status()
                tmp = destino.with_suffix(destino.suffix + ".part")
                with open(tmp, "wb") as f:
                    for bloque in r.iter_content(1 << 20):
                        f.write(bloque)
                tmp.rename(destino)
            # INEGI responde 200 con una página HTML cuando un archivo no existe.
            # (Los CSV del release no son ZIP: solo se revisa la firma de .zip y .xlsx.)
            with open(destino, "rb") as f:
                if destino.suffix in (".zip", ".xlsx") and f.read(2) != b"PK":
                    destino.unlink()
                    return "la respuesta no es un ZIP"
            return "ok"
        except requests.RequestException as e:
            if i == intentos - 1:
                return f"error: {e}"
            time.sleep(2 ** (i + 1))


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def bajar_overpass(destino, intentos=2):
    """Consulta Overpass (POST). Máximo 2 intentos (regla de gasto de la fase 3)."""
    for i in range(intentos):
        try:
            r = requests.post(OVERPASS, data={"data": CONSULTA_CAMINOS}, timeout=400)
            r.raise_for_status()
            if not r.content.lstrip().startswith(b"{"):
                raise requests.RequestException("la respuesta no es JSON")
            destino.write_bytes(r.content)
            return "ok"
        except requests.RequestException as e:
            if i == intentos - 1:
                return f"error: {e}"
            time.sleep(30)


def fila_manifiesto(fuente, nombre, url, destino):
    return {
        "fuente": fuente, "archivo": nombre, "url": url,
        "bytes": destino.stat().st_size, "sha256": sha256(destino),
        "descargado_utc": datetime.fromtimestamp(
            destino.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--solo", nargs="+", help="ids de fuente a bajar (las demás se dejan como estén)")
    args = ap.parse_args()

    release = {k: [(f"{RELEASE}/{n}", n) for n in v] for k, v in {**DEL_RELEASE, **OPCIONALES}.items()}
    filas, fallas = [], []
    for fuente, archivos in {**FUENTES, **release}.items():
        if args.solo and fuente not in args.solo:
            # Se conservan en el manifiesto los archivos que ya estaban.
            for url, nombre in archivos:
                destino = RAW / fuente / nombre
                if destino.exists():
                    filas.append(fila_manifiesto(fuente, nombre, url, destino))
            continue
        carpeta = RAW / fuente
        carpeta.mkdir(parents=True, exist_ok=True)
        for url, nombre in archivos:
            destino = carpeta / nombre
            if destino.exists() and not args.forzar:
                estado = "ya estaba"
            else:
                print(f"bajando {fuente}/{nombre} ...", flush=True)
                estado = bajar(url, destino)
            if destino.exists():
                filas.append(fila_manifiesto(fuente, nombre, url, destino))
            elif fuente not in OPCIONALES:
                fallas.append((fuente, nombre, estado))
        if not any(carpeta.iterdir()):
            carpeta.rmdir()

    # Overpass falló 4 veces el 2026-10-23 (el proxy corta la conexión): solo se
    # intenta si se pide de forma explícita (--solo osm_caminos), para no gastar.
    for fuente, nombre in OSM.items():
        destino = RAW / fuente / nombre
        if not args.solo or fuente not in args.solo:
            if destino.exists():
                filas.append(fila_manifiesto(fuente, nombre, OVERPASS, destino))
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        estado = "ya estaba" if destino.exists() and not args.forzar else bajar_overpass(destino)
        if destino.exists():
            filas.append(fila_manifiesto(fuente, nombre, OVERPASS, destino))
        else:
            fallas.append((fuente, nombre, estado))

    with open(RAW / "manifiesto.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print(f"\n{len(filas)} archivos presentes; manifiesto en data/raw/manifiesto.csv")
    if fallas:
        print("Faltan (ver data/raw/LEEME.md):")
        for fuente, nombre, estado in fallas:
            print(f"  - {fuente}/{nombre}: {estado}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
