"""03 · Base geográfica 2020 de Acámbaro y chequeos de la fase 1.

Entradas: recortes de data/processed/ generados por 02_recortar.py.
Salidas en data/processed/:
  manzanas2020_poblacion.gpkg   manzanas urbanas MG 2020 + población Censo 2020
  localidades2020.gpkg          localidades ITER 2020 (puntos) con población
  manzanas_cambios.gpkg         manzanas nuevas 2010→2020 y 2020→EIC 2025
  validacion_fase1.json         todas las cifras de los chequeos

Regla de confidencialidad observada en los datos 2020: INEGI pone "*" en lugar
de los valores 1 y 2 y en todas las variables (salvo POBTOT y VIVTOT) de las
manzanas con menos de 3 viviendas habitadas. Aquí "*" se deja como vacío; nunca
se imputa. La población "perdida" de cada variable se mide como la diferencia
entre el total publicado de cada AGEB y la suma de lo visible en sus manzanas.
"""

import json
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
PREFIJO = "11002"

GRUPOS = {
    "POBTOT": "Población total",
    "P_3A5": "3 a 5 años",
    "P_6A11": "6 a 11 años",
    "P_12A14": "12 a 14 años",
    "P_15A17": "15 a 17 años",
    "P_60YMAS": "60 años y más",
    "PCON_DISC": "Con discapacidad",
}
VIVIENDA = ["VIVTOT", "TVIVHAB", "TVIVPAR", "VIVPAR_HAB", "VIVPAR_DES", "VIVPAR_UT"]
UMBRAL_NUEVA = 0.5  # una manzana es "nueva" si menos de la mitad de su área ya era manzana


def numeros(df, columnas):
    out = df.copy()
    for c in columnas:
        out[c] = pd.to_numeric(out[c].replace({"*": None, "N/D": None}), errors="coerce")
    return out


def censo_manzanas(archivo, columnas):
    t = pd.read_csv(P / archivo, dtype=str)
    t = numeros(t, [c for c in columnas if c in t.columns])
    t["CVEGEO"] = PREFIJO + t.LOC + t.AGEB + t.MZA
    mza = t[(t.MZA != "000") & (t.AGEB != "0000")].copy()
    ageb = t[(t.MZA == "000") & (t.AGEB != "0000")].copy()
    loc = t[(t.AGEB == "0000") & (t.LOC != "0000")].copy()
    mun = t[t.LOC == "0000"].copy()
    return mza, ageb, loc, mun


def dms_a_decimal(texto):
    if not isinstance(texto, str):
        return None
    g, m, s, h = re.match(r"(\d+)°(\d+)'([\d.]+)\"\s*([NSEW])", texto).groups()
    v = int(g) + int(m) / 60 + float(s) / 3600
    return -v if h in "SW" else v


def perdida_por_confidencialidad(mza, ageb):
    filas = []
    for var, nombre in GRUPOS.items():
        visible = mza.groupby(["LOC", "AGEB"])[var].sum(min_count=1)
        total = ageb.set_index(["LOC", "AGEB"])[var]
        oculta = (total - visible.reindex(total.index).fillna(0)).clip(lower=0)
        filas.append({
            "variable": var, "grupo": nombre,
            "total_publicado_agebs": int(total.sum()),
            "suma_visible_manzanas": int(mza[var].sum()),
            "oculta": int(oculta.sum()),
            "pct_oculta": round(100 * oculta.sum() / total.sum(), 2) if total.sum() else None,
            "manzanas_con_asterisco": int(mza[var].isna().sum()),
        })
    return filas


def manzanas_nuevas(nuevas, previas):
    """Clasifica cada manzana de `nuevas` según su clave y su traslape con `previas`."""
    previas = previas.to_crs(nuevas.crs)
    union = previas.union_all()
    n = nuevas[["CVEGEO", "CVE_LOC", "CVE_AGEB", "AMBITO", "geometry"]].copy()
    area = n.geometry.area
    n["frac_ya_existia"] = (n.geometry.intersection(union).area / area).round(3)
    n["clave_nueva"] = ~n.CVEGEO.isin(previas.CVEGEO)
    n["geometria_nueva"] = n.frac_ya_existia < UMBRAL_NUEVA
    n["area_m2"] = area.round(0)
    # Si la localidad no tenía cartografía en la edición previa, su manzana no es
    # necesariamente crecimiento: puede ser solo que antes no se había dibujado.
    n["localidad_ya_cartografiada"] = n.CVE_LOC.isin(previas.CVE_LOC)
    return n


def main():
    v = {}

    # --- Población 2020 por manzana -------------------------------------------
    cols = list(GRUPOS) + VIVIENDA
    mza, ageb, loc, mun = censo_manzanas("censo2020_mza_acambaro.csv", cols)
    iter20 = pd.read_csv(P / "iter2020_acambaro.csv", dtype=str)
    iter20 = numeros(iter20, ["POBTOT", "VIVTOT", "TVIVHAB"])
    iter20["CVEGEO"] = PREFIJO + iter20.LOC
    iter_loc = iter20[~iter20.LOC.isin(["0000", "9998", "9999"])].copy()
    pob_mun_iter = int(iter20.loc[iter20.LOC == "0000", "POBTOT"].iloc[0])

    cuadre = []
    for _, r in loc.iterrows():
        cuadre.append({
            "LOC": r.LOC,
            "localidad": iter_loc.loc[iter_loc.LOC == r.LOC, "NOM_LOC"].iloc[0],
            "iter_pobtot": int(iter_loc.loc[iter_loc.LOC == r.LOC, "POBTOT"].iloc[0]),
            "total_localidad_en_tabla_mza": int(r.POBTOT),
            "suma_agebs": int(ageb.loc[ageb.LOC == r.LOC, "POBTOT"].sum()),
            "suma_manzanas": int(mza.loc[mza.LOC == r.LOC, "POBTOT"].sum()),
            "manzanas": int((mza.LOC == r.LOC).sum()),
        })
    for c in cuadre:
        c["dif_manzanas_vs_iter"] = c["suma_manzanas"] - c["iter_pobtot"]
    v["cuadre_poblacion_por_localidad"] = cuadre
    pob_urbana = sum(c["iter_pobtot"] for c in cuadre)
    v["cobertura_manzanas"] = {
        "pob_municipio_iter": pob_mun_iter,
        "pob_localidades_con_datos_por_manzana": pob_urbana,
        "pct_municipio_con_datos_por_manzana": round(100 * pob_urbana / pob_mun_iter, 2),
        "pob_sin_datos_por_manzana": pob_mun_iter - pob_urbana,
    }
    v["perdida_confidencialidad_2020"] = perdida_por_confidencialidad(mza, ageb)
    v["manzanas_menos_de_3_viviendas_habitadas"] = {
        "manzanas": int(mza.TVIVHAB.isna().sum()),
        "poblacion": int(mza.loc[mza.TVIVHAB.isna(), "POBTOT"].sum()),
    }

    # --- Unión a la geometría MG 2020 -----------------------------------------
    g20 = gpd.read_file(P / "mg2020_acambaro.gpkg", layer="manzanas")
    sel = mza[["CVEGEO", "NOM_LOC"] + cols]
    unidas = g20.merge(sel, on="CVEGEO", how="inner")
    sin_geom = sel[~sel.CVEGEO.isin(g20.CVEGEO)]
    v["union_censo_mg2020"] = {
        "manzanas_tabla_censal": len(sel),
        "manzanas_mg2020_municipio": len(g20),
        "manzanas_mg2020_urbanas": int((g20.AMBITO == "Urbana").sum()),
        "unidas": len(unidas),
        "tabla_sin_geometria": len(sin_geom),
        "pob_tabla_sin_geometria": int(sin_geom.POBTOT.sum()),
        "mg2020_urbanas_sin_dato_censal": int(((g20.AMBITO == "Urbana") & ~g20.CVEGEO.isin(sel.CVEGEO)).sum()),
        "pob_unida": int(unidas.POBTOT.sum()),
    }
    # Clave de manzana 800 = caserío disperso: viviendas fuera de manzana que el
    # MG representa como puntos (capa caserio_disperso), no como polígonos.
    cd = gpd.read_file(P / "mg2020_acambaro.gpkg", layer="caserio_disperso")
    cd_unidos = cd.merge(sel, on="CVEGEO", how="inner")
    v["union_censo_mg2020"]["caserio_disperso_unido_a_puntos"] = len(cd_unidos)
    v["union_censo_mg2020"]["pob_caserio_disperso"] = int(cd_unidos.POBTOT.sum())
    v["union_censo_mg2020"]["tabla_sin_ninguna_geometria"] = int(
        (~sel.CVEGEO.isin(set(g20.CVEGEO) | set(cd.CVEGEO))).sum())
    out = P / "manzanas2020_poblacion.gpkg"
    out.unlink(missing_ok=True)
    unidas.to_file(out, layer="manzanas", driver="GPKG")
    cd_unidos.to_file(out, layer="caserio_disperso", driver="GPKG")

    # --- Localidades ITER 2020 -------------------------------------------------
    iter_loc["lon"] = iter_loc.LONGITUD.map(dms_a_decimal)
    iter_loc["lat"] = iter_loc.LATITUD.map(dms_a_decimal)
    l20 = gpd.read_file(P / "mg2020_acambaro.gpkg", layer="localidades_amanzanadas")
    lpr = gpd.read_file(P / "mg2020_acambaro.gpkg", layer="localidades_puntuales_rurales")
    iter_loc["en_mg2020"] = iter_loc.CVEGEO.isin(set(l20.CVEGEO) | set(lpr.CVEGEO.str[:9]))
    iter_loc["tipo_mg2020"] = iter_loc.CVEGEO.map(
        lambda c: "amanzanada" if c in set(l20.CVEGEO) else ("puntual" if c in set(lpr.CVEGEO.str[:9]) else "no está"))
    gl = gpd.GeoDataFrame(
        iter_loc[["CVEGEO", "LOC", "NOM_LOC", "POBTOT", "VIVTOT", "TVIVHAB", "lon", "lat", "tipo_mg2020"]],
        geometry=gpd.points_from_xy(iter_loc.lon, iter_loc.lat), crs="EPSG:4326")
    out = P / "localidades2020.gpkg"
    out.unlink(missing_ok=True)
    gl.to_file(out, layer="localidades", driver="GPKG")
    gl.drop(columns="geometry").to_csv(P / "localidades2020.csv", index=False)
    v["localidades_iter2020"] = {
        "localidades": len(iter_loc),
        "suma_pobtot": int(iter_loc.POBTOT.sum()),
        "total_municipal_iter": pob_mun_iter,
        "dif_suma_vs_total": int(iter_loc.POBTOT.sum()) - pob_mun_iter,
        "filas_9998_9999": iter20.loc[iter20.LOC.isin(["9998", "9999"]), ["LOC", "NOM_LOC", "POBTOT"]]
            .fillna("").astype(str).to_dict("records"),
        "sin_coordenadas": int(iter_loc.lon.isna().sum()),
        "por_tipo_mg2020": iter_loc.tipo_mg2020.value_counts().to_dict(),
        "pob_por_tipo_mg2020": iter_loc.groupby("tipo_mg2020").POBTOT.sum().astype(int).to_dict(),
        "por_tamano": pd.cut(iter_loc.POBTOT, [-1, 0, 49, 249, 499, 999, 2499, 1e7],
                             labels=["0", "1-49", "50-249", "250-499", "500-999", "1000-2499", "2500+"])
            .value_counts().sort_index().astype(int).to_dict(),
    }

    # --- Cambios en manzanas ---------------------------------------------------
    g25 = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="manzanas")
    g10 = gpd.read_file(P / "mg2010_acambaro.gpkg", layer="manzanas")
    g10["CVEGEO"] = g10.CVEGEO.astype(str)
    # La cartografía 2010 solo incluye manzanas; se descartan polígonos sin clave.
    v["mg2010_manzanas_sin_clave"] = int(g10.CVEGEO.isin(["None", "nan", ""]).sum())
    n25 = manzanas_nuevas(g25, g20)
    n20 = manzanas_nuevas(g20, g10)

    # Comprobación de que la proyección asignada a 2010 coincide con 2020.
    g10p = g10.to_crs(g20.crs)
    par = g20[["CVEGEO", "geometry"]].merge(
        g10p[["CVEGEO", "AMBITO", "geometry"]], on="CVEGEO", suffixes=("_20", "_10"))
    d = gpd.GeoSeries(par.geometry_20).centroid.distance(gpd.GeoSeries(par.geometry_10, crs=g20.crs).centroid)
    v["alineacion_2010_2020"] = {
        amb: {"pares_misma_clave": int((par.AMBITO == amb).sum()),
              "mediana_distancia_centroides_m": round(float(d[par.AMBITO == amb].median()), 1),
              "p95_distancia_m": round(float(d[par.AMBITO == amb].quantile(0.95)), 1)}
        for amb in ["Urbana", "Rural"]
    }

    def resumen(n, etiqueta):
        return {
            "manzanas_edicion_nueva": len(n),
            "clave_nueva": int(n.clave_nueva.sum()),
            "geometria_nueva": int(n.geometria_nueva.sum()),
            "clave_y_geometria_nuevas": int((n.clave_nueva & n.geometria_nueva).sum()),
            "clave_nueva_pero_ya_existia_el_suelo": int((n.clave_nueva & ~n.geometria_nueva).sum()),
            "area_nueva_ha": round(float(n.loc[n.geometria_nueva, "area_m2"].sum()) / 1e4, 1),
            "geometria_nueva_en_localidad_ya_cartografiada": int((n.geometria_nueva & n.localidad_ya_cartografiada).sum()),
            "geometria_nueva_en_localidad_sin_cartografia_previa": int((n.geometria_nueva & ~n.localidad_ya_cartografiada).sum()),
            "area_nueva_ha_localidad_ya_cartografiada": round(float(
                n.loc[n.geometria_nueva & n.localidad_ya_cartografiada, "area_m2"].sum()) / 1e4, 1),
            "geometria_nueva_por_localidad": n[n.geometria_nueva].CVE_LOC.value_counts().to_dict(),
            "etiqueta": etiqueta,
        }

    v["manzanas_nuevas_2020_a_eic2025"] = resumen(n25, "MG EIC 2025 vs MG 2020")
    v["manzanas_nuevas_2010_a_2020"] = resumen(n20, "MG 2020 vs cierre Censo 2010")
    v["manzanas_2020_que_ya_no_estan_en_eic2025"] = int((~g20.CVEGEO.isin(g25.CVEGEO)).sum())
    out = P / "manzanas_cambios.gpkg"
    out.unlink(missing_ok=True)
    n25.to_file(out, layer="eic2025_vs_2020", driver="GPKG")
    n20.to_file(out, layer="mg2020_vs_2010", driver="GPKG")

    # --- Contexto EIC 2025 -------------------------------------------------------
    eic = pd.read_csv(P / "eic2025_acambaro.csv", dtype=str)
    est = eic[eic.CVE_LOC == "0000"].set_index("ESTIMADOR")
    v["eic2025_municipio"] = {k: est.loc[k, "POBTOT"] for k in est.index}
    v["eic2025_vs_censo2020"] = round(100 * (float(est.iloc[0]["POBTOT"]) / pob_mun_iter - 1), 2)

    with open(P / "validacion_fase1.json", "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2, default=str)
    print(json.dumps(v, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
