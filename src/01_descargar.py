"""01 · Descarga de datos crudos.

Baja de nuevo, sin buscar nada, todos los archivos cuya URL directa ya se
verificó (ver docs/fuentes.md). Guarda cada archivo en data/raw/<id>/ y
escribe data/raw/manifiesto.csv con tamaño, sha256 y fecha de descarga.

Las fuentes sin URL directa verificada (CLUES, SEP, CONAPO) no se descargan
aquí: Alejandro las sube al release "datos-crudos" del repo (ver
data/raw/LEEME.md) y este script las baja de ese release si ya existen.

Uso:
    python src/01_descargar.py            # baja lo que falte
    python src/01_descargar.py --forzar   # vuelve a bajar todo
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
    "clues": ["clues.zip"],
    "sep_escuelas": ["sep_escuelas.zip"],
    "conapo_imu2020": ["conapo_imu2020_ageb.zip", "conapo_imu2020_colonia.zip"],
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
            with open(destino, "rb") as f:
                if f.read(2) != b"PK":
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true")
    args = ap.parse_args()

    pendientes = {k: [(f"{RELEASE}/{n}", n) for n in v] for k, v in DEL_RELEASE.items()}
    filas, fallas = [], []
    for fuente, archivos in {**FUENTES, **pendientes}.items():
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
                filas.append({
                    "fuente": fuente, "archivo": nombre, "url": url,
                    "bytes": destino.stat().st_size, "sha256": sha256(destino),
                    "descargado_utc": datetime.fromtimestamp(
                        destino.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
                })
            else:
                fallas.append((fuente, nombre, estado))
        if not any(carpeta.iterdir()):
            carpeta.rmdir()

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
