"""20 · Expansión de largo plazo con GHSL (fase 4b).

GHS-BUILT-S R2023A (D07): m² construidos por celda de 100 m, 1975–2020 cada 5 años
(solo la serie observada). Se suma por:
  - municipio (celdas cuyo centro cae dentro del límite municipal, MG EIC 2025);
  - cada localidad urbana: celdas a <= BUFFER m de su polígono (MG EIC 2025); si una
    celda queda cerca de dos, va a la más cercana;
  - para la ciudad, por sector (8 direcciones) y por anillo de 1 km desde su centro (ITER 2020).
Población del mismo año para la superficie por habitante: solo 2010 y 2020 (Censo e
ITER). La EIC 2025 municipal se reporta sin superficie (el GHSL observado termina en
2020). Los ITER de 1990–2005 no tienen URL directa (2 intentos, 2026-10-23): no hay
población para los años anteriores.

Salidas en data/processed/:
  ghsl_serie.csv      zona × año: superficie construida, población, m² por habitante
  ghsl_sectores.csv   ciudad: m² ganados por sector y anillo en cada periodo, más la
                      superficie de cuadras nuevas del MG (2010–2020, posterior a 2020) por sector
"""

import importlib.util
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"

spec = importlib.util.spec_from_file_location("crec19", RAIZ / "src" / "19_crecimiento.py")
crec19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crec19)
URBANAS = crec19.URBANAS

ANIOS = list(range(1975, 2021, 5))
BUFFER = 1000         # m alrededor del polígono de cada localidad urbana
ANILLO_KM = 1000      # m
PERIODOS = [(1975, 1990), (1990, 2000), (2000, 2010), (2010, 2020)]


def celdas():
    """Centros de celda (en el CRS del MG) y m² construidos por año."""
    with rasterio.open(P / "ghsl" / f"ghsl_built_s_{ANIOS[0]}_acambaro.tif") as r:
        filas, cols = np.indices(r.shape)
        xs, ys = rasterio.transform.xy(r.transform, filas.ravel(), cols.ravel())
        crs = r.crs
    g = gpd.GeoDataFrame(geometry=gpd.points_from_xy(xs, ys), crs=crs)
    for a in ANIOS:
        with rasterio.open(P / "ghsl" / f"ghsl_built_s_{a}_acambaro.tif") as r:
            v = r.read(1).ravel().astype(float)
            v[v == r.nodata] = np.nan
        g[a] = v
    return g


def main():
    mun = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="municipio")
    crs = mun.crs
    g = celdas().to_crs(crs)
    v = {"celdas": len(g), "celdas_sin_dato": {a: int(g[a].isna().sum()) for a in ANIOS}}
    g["municipio"] = g.within(mun.union_all())
    loc = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="localidades_amanzanadas")
    loc = loc[loc.CVE_LOC.isin(URBANAS)].dissolve("CVE_LOC").reset_index()
    dist = np.column_stack([g.distance(p) for p in loc.geometry])
    g["zona"] = np.where(dist.min(axis=1) <= BUFFER, loc.CVE_LOC.to_numpy()[dist.argmin(axis=1)], "")

    # Población
    it = {a: pd.read_csv(P / f"iter{a}_acambaro.csv", dtype=str).set_index("LOC") for a in (2010, 2020)}
    eic = pd.read_csv(P / "eic2025_acambaro.csv", dtype=str, encoding="utf-8")
    eic = eic[eic.CVE_LOC == "0000"].set_index("ESTIMADOR").POBTOT.astype(float)

    filas = []
    zonas = [("municipio", "Municipio de Acámbaro", g.municipio, "0000")] + \
            [(f"loc_{c}", f"{n} (+{BUFFER} m)", g.zona == c, c) for c, n in URBANAS.items()]
    for clave, nombre, sel, cl in zonas:
        for a in ANIOS:
            m2 = float(np.nansum(g.loc[sel, a]))
            pob = float(it[a].loc[cl, "POBTOT"]) if a in it else np.nan
            filas.append({"zona": clave, "nombre": nombre, "anio": a, "construido_ha": round(m2 / 1e4, 1),
                          "celdas": int(sel.sum()), "poblacion": pob,
                          "m2_construidos_por_hab": round(m2 / pob, 1) if pob == pob else np.nan,
                          "fuente_poblacion": ("Censo 2020 (ITER)" if a == 2020 else "Censo 2010 (ITER)") if a in it else ""})
        if clave == "municipio":
            filas.append({"zona": clave, "nombre": nombre, "anio": 2025, "construido_ha": np.nan, "celdas": int(sel.sum()),
                          "poblacion": eic["Valor"], "poblacion_li": eic["Límite inferior de confianza"],
                          "poblacion_ls": eic["Límite superior de confianza"], "m2_construidos_por_hab": np.nan,
                          "fuente_poblacion": "EIC 2025 (estimación con intervalo de 90 %); GHSL observado termina en 2020"})
    serie = pd.DataFrame(filas)
    base = serie[serie.anio == 1975].set_index("zona").construido_ha
    serie["indice_1975_100"] = (100 * serie.construido_ha / serie.zona.map(base)).round(0)

    # Ciudad: sectores y anillos desde el centro (ITER 2020)
    cen = crec19.centros(crs)["0001"]
    c = g[g.zona == "0001"].copy()
    dx, dy = c.geometry.x - cen.x, c.geometry.y - cen.y
    c["sector"] = crec19.sector(dx.to_numpy(), dy.to_numpy())
    c["anillo_km"] = (np.hypot(dx, dy) // ANILLO_KM).astype(int)
    sec = []
    for (a0, a1) in PERIODOS:
        gan = (c[a1] - c[a0])
        for tipo, col, orden in [("sector", "sector", crec19.SECTORES), ("anillo_km", "anillo_km", sorted(c.anillo_km.unique()))]:
            agg = gan.groupby(c[col]).sum()
            tot = gan.sum()
            for k in orden:
                sec.append({"tipo": tipo, "clave": f"{k}–{k + 1} km" if tipo == "anillo_km" else k,
                            "periodo": f"{a0}–{a1}", "ganado_ha": round(float(agg.get(k, 0)) / 1e4, 1),
                            "pct_del_periodo": round(100 * float(agg.get(k, 0)) / tot, 1) if tot else np.nan,
                            f"construido_{a1}_ha": round(float(c.loc[c[col] == k, a1].sum()) / 1e4, 1)})
    cu = pd.read_csv(P / "cuadras_antiguedad.csv", dtype={"CVE_LOC": str})
    cu = cu[cu.CVE_LOC == "0001"]
    for per in [crec19.N1020, crec19.N20]:
        x = cu[cu.periodo == per].groupby("sector").superficie_m2.sum()
        for k in crec19.SECTORES:
            sec.append({"tipo": "sector (cuadras nuevas MG)", "clave": k, "periodo": per,
                        "ganado_ha": round(float(x.get(k, 0)) / 1e4, 1),
                        "pct_del_periodo": round(100 * float(x.get(k, 0)) / x.sum(), 1) if x.sum() else np.nan})
    sec = pd.DataFrame(sec)

    serie.to_csv(P / "ghsl_serie.csv", index=False)
    sec.to_csv(P / "ghsl_sectores.csv", index=False)
    # Chequeo: superficie construida GHSL 2020 en la ciudad contra superficie de cuadras del MG 2020
    v["ciudad_construido_2020_ha"] = float(serie[(serie.zona == "loc_0001") & (serie.anio == 2020)].construido_ha.iloc[0])
    v["ciudad_cuadras_mg2020_ha"] = round(float(cu[cu.periodo.isin([crec19.CONSOL, crec19.N1020])].superficie_m2.sum()) / 1e4, 1)
    j = json.loads((P / "validacion_fase4b.json").read_text())
    j["ghsl"] = v
    (P / "validacion_fase4b.json").write_text(json.dumps(j, ensure_ascii=False, indent=1, default=str))
    print(serie.to_string())
    print(sec[sec.tipo != "anillo_km"].pivot_table(index="clave", columns="periodo", values="pct_del_periodo"))
    print(sec[sec.tipo == "anillo_km"].pivot_table(index="clave", columns="periodo", values="ganado_ha"))
    print(v)


if __name__ == "__main__":
    main()
