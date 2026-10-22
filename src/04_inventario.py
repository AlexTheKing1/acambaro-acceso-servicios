"""04 · Inventario de datos.

Escribe docs/inventario.md a partir de data/raw/manifiesto.csv y de los
recortes de data/processed/: qué hay en cada archivo, columnas clave, sistema
de coordenadas y cuántos registros caen en Acámbaro. También resume la
superficie construida GHSL observada (1975–2020) dentro del municipio.
"""

import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyogrio
import rasterio
from rasterio.mask import mask

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
P = RAIZ / "data" / "processed"

CLAVE = ["CVEGEO", "CVE_LOC", "CVE_AGEB", "CVE_MZA", "LOC", "AGEB", "MZA", "AMBITO", "TIPOMZA",
         "POBTOT", "VIVTOT", "NOMGEO", "NOM_LOC", "LONGITUD", "LATITUD", "ESTIMADOR",
         "codigo_act", "nombre_act", "per_ocu", "latitud", "longitud", "fecha_alta", "NOMSERV", "TIPO"]


def crs_corto(crs):
    if crs is None:
        return "sin proyección declarada"
    return f"{crs.name}" + (f" (EPSG:{crs.to_epsg()})" if crs.to_epsg() else "")


def main():
    man = pd.read_csv(RAW / "manifiesto.csv")
    L = ["# Inventario de datos", "",
         "Generado por `src/04_inventario.py`. Versiones y fechas de publicación: `docs/fuentes.md`.", "",
         "## Archivos crudos (data/raw/, no versionados)", "",
         "| Fuente | Archivo | MB | Contenido del zip |", "|---|---|---|---|"]
    for _, r in man.iterrows():
        nombres = [n for n in zipfile.ZipFile(RAW / r.fuente / r.archivo).namelist() if not n.endswith("/")]
        datos = sorted((n.split("/")[-1] for n in nombres if n.lower().endswith((".csv", ".shp", ".tif"))),
                       key=lambda n: not n.lower().endswith((".shp", ".tif")))
        resumen = ", ".join(datos[:4]) + (f" … (+{len(datos) - 4})" if len(datos) > 4 else "")
        L.append(f"| {r.fuente} | {r.archivo} | {r.bytes / 1e6:.1f} | {len(nombres)} archivos; datos: {resumen} |")

    L += ["", "## Capas geográficas recortadas a Acámbaro (data/processed/*.gpkg)", "",
          "| Archivo | Capa | Registros | Geometría | Sistema de coordenadas | Columnas clave |",
          "|---|---|---|---|---|---|"]
    for gpkg in sorted(P.glob("*.gpkg")):
        for capa, geom in pyogrio.list_layers(gpkg):
            info = pyogrio.read_info(gpkg, layer=capa)
            g = gpd.read_file(gpkg, layer=capa, max_features=1)
            cols = [c for c in info["fields"] if c in CLAVE][:8]
            L.append(f"| {gpkg.name} | {capa} | {info['features']} | {geom} | {crs_corto(g.crs)} | {', '.join(cols)} |")

    L += ["", "## Tablas recortadas a Acámbaro (data/processed/*.csv)", "",
          "| Archivo | Filas | Columnas | Columnas clave |", "|---|---|---|---|"]
    for csv in sorted(P.glob("*.csv")):
        t = pd.read_csv(csv, dtype=str, nrows=None)
        cols = [c for c in t.columns if c in CLAVE][:10]
        L.append(f"| {csv.name} | {len(t)} | {len(t.columns)} | {', '.join(cols)} |")

    # GHSL: superficie construida observada dentro del municipio
    mun = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="municipio")
    L += ["", "## GHS-BUILT-S R2023A dentro del municipio (solo años observados)", "",
          "Mollweide (ESRI:54009), celdas de 100 m; valor = m² construidos por celda.", "",
          "| Año | Superficie construida (ha) | Celdas con algo construido |", "|---|---|---|"]
    for tif in sorted((P / "ghsl").glob("*.tif")):
        with rasterio.open(tif) as src:
            datos, _ = mask(src, list(mun.to_crs(src.crs).geometry), crop=True, nodata=65535)
            d = datos[0].astype("float64")
            d[d == 65535] = np.nan
        anio = tif.stem.split("_")[3]
        L.append(f"| {anio} | {np.nansum(d) / 1e4:,.0f} | {int(np.nansum(d > 0)):,} |")

    (RAIZ / "docs" / "inventario.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[-14:]))


if __name__ == "__main__":
    main()
