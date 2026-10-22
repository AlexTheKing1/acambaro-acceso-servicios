"""02 · Recortes de Acámbaro (municipio 11002).

Lee los archivos de data/raw/ sin descomprimirlos ni modificarlos y escribe en
data/processed/ solo la parte de Acámbaro:

  mg{2010,2020,2025,eic2025}_acambaro.gpkg   capas del Marco Geoestadístico
  censo2020_mza_acambaro.csv                 resultados por AGEB y manzana 2020
  censo2010_mza_acambaro.csv                 resultados por AGEB y manzana 2010
  iter2020_acambaro.csv, iter2010_acambaro.csv
  eic2025_acambaro.csv                       filas de Acámbaro en la EIC 2025
  denue_acambaro_buffer10km.csv              DENUE (Gto., Mich., Qro.) en el municipio + 10 km
  mg_eic2025_servicios_buffer10km.gpkg       servicios del MG EIC 2025 (Gto. y Mich.) en el municipio + 10 km
  ghsl/ghsl_built_s_{año}_acambaro.tif       GHS-BUILT-S 1975–2020 (observado)

Las tablas censales se guardan tal cual (texto), incluidos los asteriscos de
confidencialidad; la conversión a números ocurre en 03_base_geografica.py.
"""

import argparse
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
import rasterio
from rasterio.mask import mask

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "data" / "processed"
CVE_ENT, CVE_MUN = "11", "002"
CVEGEO_MUN = CVE_ENT + CVE_MUN
BUFFER_DENUE_M = 10_000
BUFFER_GHSL_M = 2_000

# Capas del Marco Geoestadístico 2020 en adelante (nombre en el zip -> capa de salida)
CAPAS_MG = {
    "mun": "municipio",
    "l": "localidades_amanzanadas",
    "lpr": "localidades_puntuales_rurales",
    "a": "ageb_urbanas",
    "ar": "ageb_rurales",
    "m": "manzanas",
    "e": "vialidades",
    "cd": "caserio_disperso",
    "pe": "poligonos_externos",
    "pem": "poligonos_externos_manzana",
    "sip": "servicios_puntos",
    "sia": "servicios_areas",
    "sil": "servicios_lineas",
}

# Capas de la cartografía de cierre del Censo 2010 (sufijo del shapefile -> capa)
CAPAS_2010 = {
    "M": "manzanas", "L": "localidades_amanzanadas", "A": "ageb_urbanas",
    "E": "vialidades", "SIP": "servicios_puntos", "SIA": "servicios_areas",
    "SIL": "servicios_lineas",
}


def recortar_mg(edicion):
    zip_ = RAW / edicion / "11_guanajuato.zip"
    salida = OUT / f"{edicion}_acambaro.gpkg"
    salida.unlink(missing_ok=True)
    for corto, capa in CAPAS_MG.items():
        ruta = f"/vsizip/{zip_}/conjunto_de_datos/11{corto}.shp"
        g = gpd.read_file(ruta, where=f"CVE_MUN = '{CVE_MUN}'")
        g.to_file(salida, layer=capa, driver="GPKG")
        print(f"  {edicion}/{capa}: {len(g)}")


def recortar_mg2010():
    """Une las carpetas por localidad (urbana y rural) en una capa por tipo."""
    crs_ref = None
    partes = {capa: [] for capa in CAPAS_2010.values()}
    sin_crs = 0
    for nombre_zip, ambito in [("702825585853_s.zip", "Urbana"), ("702825561291_s.zip", "Rural")]:
        zip_ = RAW / "mg2010_acambaro" / nombre_zip
        for n in zipfile.ZipFile(zip_).namelist():
            if not n.lower().endswith(".shp"):
                continue
            archivo = n.split("/")[-1][:-4]
            sufijo = archivo[9:].upper()
            if sufijo not in CAPAS_2010:
                continue
            g = gpd.read_file(f"/vsizip/{zip_}/{n}")
            if g.crs is None:
                sin_crs += 1
            elif crs_ref is None:
                crs_ref = g.crs
            g["CVE_LOC"] = archivo[5:9]
            g["AMBITO"] = ambito
            partes[CAPAS_2010[sufijo]].append(g)
    # Los shapefiles rurales de 2010 no traen .prj. Sus coordenadas están en el
    # mismo rango que los urbanos (Cónica Conforme de Lambert ITRF92), así que se
    # les asigna esa proyección; la coincidencia se comprueba en docs/validacion.md.
    salida = OUT / "mg2010_acambaro.gpkg"
    salida.unlink(missing_ok=True)
    for capa, lista in partes.items():
        lista = [g.set_crs(crs_ref, allow_override=True) if g.crs is None else g for g in lista]
        g = gpd.GeoDataFrame(pd.concat(lista, ignore_index=True), crs=crs_ref)
        g.to_file(salida, layer=capa, driver="GPKG")
        print(f"  mg2010/{capa}: {len(g)}")
    print(f"  shapefiles 2010 sin proyección (se les asignó la urbana): {sin_crs}")


def leer_csv_zip(zip_, interno, **kw):
    with zipfile.ZipFile(zip_) as z:
        with z.open(interno) as f:
            return pd.read_csv(f, dtype=str, **kw)


def recortar_tablas():
    t = leer_csv_zip(RAW / "censo2020_ageb_mza" / "ageb_mza_urbana_11_cpv2020_csv.zip",
                     "ageb_mza_urbana_11_cpv2020/conjunto_de_datos/conjunto_de_datos_ageb_urbana_11_cpv2020.csv")
    t[t.MUN == CVE_MUN].to_csv(OUT / "censo2020_mza_acambaro.csv", index=False)

    t = leer_csv_zip(RAW / "censo2010_ageb_mza" / "resageburb_11_2010_csv.zip",
                     "resultados_ageb_urbana_11_cpv2010/conjunto_de_datos/resultados_ageb_urbana_11_cpv2010.csv",
                     encoding="utf-8-sig")
    t.columns = [c.upper() for c in t.columns]
    t[t.MUN == CVE_MUN].to_csv(OUT / "censo2010_mza_acambaro.csv", index=False)

    t = leer_csv_zip(RAW / "iter2020" / "iter_11_cpv2020_csv.zip",
                     "iter_11_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_11CSV20.csv")
    t[t.MUN == CVE_MUN].to_csv(OUT / "iter2020_acambaro.csv", index=False)

    t = leer_csv_zip(RAW / "iter2010" / "iter_11_2010_csv.zip",
                     "iter_11_cpv2010/conjunto_de_datos/iter_11_cpv2010.csv", encoding="utf-8-sig")
    t.columns = [c.upper() for c in t.columns]
    t[t.MUN == CVE_MUN].to_csv(OUT / "iter2010_acambaro.csv", index=False)

    t = leer_csv_zip(RAW / "eic2025" / "conjunto_de_datos_eic2025_105_csv.zip",
                     "conjunto_de_datos/conjunto_datos_eic2025_105.csv", encoding="latin1")
    t[t.CVEGEO.str.startswith(CVEGEO_MUN)].to_csv(OUT / "eic2025_acambaro.csv", index=False)


def recortar_denue(municipio):
    t = pd.concat([leer_csv_zip(z, next(n for n in zipfile.ZipFile(z).namelist()
                                        if n.startswith("conjunto_de_datos/") and n.endswith(".csv")),
                                encoding="latin1")
                   for z in sorted((RAW / "denue").glob("denue_*_csv.zip"))], ignore_index=True)
    pts = gpd.GeoDataFrame(t, geometry=gpd.points_from_xy(t.longitud.astype(float), t.latitud.astype(float)),
                           crs="EPSG:4326").to_crs(municipio.crs)
    zona = municipio.buffer(BUFFER_DENUE_M).union_all()
    dentro = pts[pts.within(zona)].copy()
    dentro["en_acambaro"] = (dentro.cve_ent == CVE_ENT) & (dentro.cve_mun == CVE_MUN)
    dentro.drop(columns="geometry").to_csv(OUT / "denue_acambaro_buffer10km.csv", index=False)
    print(f"  DENUE: {len(dentro)} establecimientos ({int(dentro.en_acambaro.sum())} en Acámbaro); "
          f"por entidad: {dentro.cve_ent.value_counts().to_dict()}")


def recortar_servicios_mg(municipio):
    """Puntos y áreas de servicios (escuelas, salud, mercados...) del MG EIC 2025
    en el municipio y la franja de 10 km, de Guanajuato y Michoacán."""
    zona = municipio.buffer(BUFFER_DENUE_M).union_all()
    salida = OUT / "mg_eic2025_servicios_buffer10km.gpkg"
    salida.unlink(missing_ok=True)
    for corto, capa in [("sip", "puntos"), ("sia", "areas")]:
        partes = []
        for zip_ in sorted((RAW / "mg_eic2025").glob("*.zip")):
            ent = zip_.name[:2]
            g = gpd.read_file(f"/vsizip/{zip_}/conjunto_de_datos/{ent}{corto}.shp", bbox=zona.bounds)
            partes.append(g.to_crs(municipio.crs))
        g = gpd.GeoDataFrame(pd.concat(partes, ignore_index=True), crs=municipio.crs)
        g = g[g.intersects(zona)].copy()
        g["en_acambaro"] = (g.CVE_ENT == CVE_ENT) & (g.CVE_MUN == CVE_MUN)
        g.to_file(salida, layer=capa, driver="GPKG")
        print(f"  servicios MG {capa}: {len(g)} ({int(g.en_acambaro.sum())} en Acámbaro); "
              f"por entidad: {g.CVE_ENT.value_counts().to_dict()}")


def recortar_ghsl(municipio):
    (OUT / "ghsl").mkdir(exist_ok=True)
    for zip_ in sorted((RAW / "ghsl_built_s").glob("*.zip")):
        tif = zip_.name.replace(".zip", ".tif")
        anio = tif.split("_E")[1][:4]
        with rasterio.open(f"/vsizip/{zip_}/{tif}") as src:
            zona = municipio.to_crs(src.crs).buffer(BUFFER_GHSL_M).union_all()
            datos, transform = mask(src, [zona.envelope], crop=True)
            perfil = src.profile | {"height": datos.shape[1], "width": datos.shape[2],
                                    "transform": transform, "compress": "deflate"}
        with rasterio.open(OUT / "ghsl" / f"ghsl_built_s_{anio}_acambaro.tif", "w", **perfil) as dst:
            dst.write(datos)
    print("  GHSL recortado")


PASOS = ["mg", "mg2010", "tablas", "denue", "servicios_mg", "ghsl"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", nargs="+", choices=PASOS, default=PASOS,
                    help="correr solo estos pasos (por omisión, todos)")
    pasos = ap.parse_args().solo
    OUT.mkdir(parents=True, exist_ok=True)
    if "mg" in pasos:
        for edicion in ["mg2020", "mg2025", "mg_eic2025"]:
            recortar_mg(edicion)
    if "mg2010" in pasos:
        recortar_mg2010()
    if "tablas" in pasos:
        recortar_tablas()
    municipio = gpd.read_file(OUT / "mg_eic2025_acambaro.gpkg", layer="municipio")
    if "denue" in pasos:
        recortar_denue(municipio)
    if "servicios_mg" in pasos:
        recortar_servicios_mg(municipio)
    if "ghsl" in pasos:
        recortar_ghsl(municipio)


if __name__ == "__main__":
    main()
