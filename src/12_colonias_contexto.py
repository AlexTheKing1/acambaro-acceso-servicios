"""12 · Nombres de colonia por cuadra y contexto social (fase 3, D24).

CONAPO no está disponible (D24). Se sustituye así:

1. Nombres de colonia. El Catálogo de asentamientos humanos del INEGI
   (data/raw/asentamientos/asentamientos_11_002.json) trae la lista oficial de
   colonias, fraccionamientos, barrios, etc. de Acámbaro (clave, nombre, tipo y
   localidad), pero NO trae polígonos. Para ubicar cada asentamiento se usan los
   registros que sí traen el nombre del asentamiento y coordenadas: DENUE
   (nomb_asent), catálogo SEP (INMUEBLE_C_NOM_ASEN) y CLUES (ASENTAMIENTO).
   Cada cuadra de las 4 localidades urbanas toma:
     a) el nombre más frecuente entre los registros que caen dentro de la cuadra; si no hay,
     b) el más frecuente entre los K_VECINOS registros más cercanos a <= DIST_VECINOS m;
     c) si tampoco, queda sin nombre.
   Solo se aceptan nombres que existen en el catálogo del INEGI de la misma
   localidad (comparación sin acentos ni mayúsculas); los demás se descartan.
   Es una aproximación: el límite entre dos colonias queda donde cambian los
   registros, no donde lo marca un plano oficial.

2. Contexto social: indicadores del Censo 2020 por AGEB urbana y por localidad,
   tal como los publica INEGI (sin construir un índice): grado promedio de
   escolaridad, % de 15 años y más analfabeta, % sin afiliación a servicios de
   salud, % de viviendas sin agua entubada dentro, sin drenaje, sin electricidad
   y sin automóvil o camioneta. Los "*" se dejan vacíos.

Salidas en data/processed/:
  colonias_cuadras.csv     CVEGEO, colonia, tipo, cómo se asignó, n de registros que votaron
  colonias_catalogo.csv    catálogo INEGI + cuántas cuadras quedaron con cada nombre
  contexto_ageb.csv, contexto_localidades.csv
  validacion_fase3_colonias.json
"""

import importlib.util
import json
import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
RAW = RAIZ / "data" / "raw"

spec = importlib.util.spec_from_file_location("base03", RAIZ / "src" / "03_base_geografica.py")
base03 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base03)
spec6 = importlib.util.spec_from_file_location("cat06", RAIZ / "src" / "06_catalogo_servicios.py")
cat06 = importlib.util.module_from_spec(spec6)
spec6.loader.exec_module(cat06)

URBANAS = {"0001": "Acámbaro", "0027": "Irámuco", "0047": "Parácuaro", "0017": "Chupícuaro (Nuevo Chupícuaro)"}
K_VECINOS = 5
DIST_VECINOS = 300   # m
TIPOS_ASEN = r"^(COLONIA|COL|FRACCIONAMIENTO|FRACC|BARRIO|UNIDAD HABITACIONAL|ZONA CENTRO|CENTRO|AMPLIACION|AMPL|RESIDENCIAL|CONJUNTO HABITACIONAL)\.?\s+"

VARS_CONTEXTO = ["POBTOT", "GRAPROES", "P15YM_AN", "P_15YMAS", "PSINDER", "VIVPAR_HAB", "VPH_AGUADV",
                 "VPH_NODREN", "VPH_S_ELEC", "VPH_AUTOM"]


def normal(n):
    n = cat06.sin_acentos(n) if isinstance(n, str) else ""
    n = re.sub(TIPOS_ASEN, "", n)
    return " ".join(re.sub(r"[^A-Z0-9 ]", " ", n).split()) or None


def puntos_con_asentamiento(crs):
    d = pd.read_csv(P / "denue_acambaro_buffer10km.csv", dtype=str)
    d = d[(d.en_acambaro == "True") & d.cve_loc.isin(URBANAS)]
    den = gpd.GeoDataFrame({"cve_loc": d.cve_loc, "asent": d.nomb_asent, "fuente": "DENUE"},
                           geometry=gpd.points_from_xy(d.longitud.astype(float), d.latitud.astype(float)), crs=4326)
    s = pd.read_csv(P / "sep_escuelas_buffer10km.csv", dtype=str)
    s = s[(s.INMUEBLE_CV_ENT == "11") & (s.INMUEBLE_CV_MUN == "002") & s.INMUEBLE_CV_LOC.isin(URBANAS)]
    sep = gpd.GeoDataFrame({"cve_loc": s.INMUEBLE_CV_LOC, "asent": s.INMUEBLE_C_NOM_ASEN, "fuente": "SEP"},
                           geometry=gpd.points_from_xy(s.INMUEBLE_LONGITUD.astype(float),
                                                       s.INMUEBLE_LATITUD.astype(float)), crs=4326)
    c = pd.read_csv(P / "clues_buffer10km.csv", dtype=str)
    c = c[(c["CLAVE DE LA ENTIDAD"] == "11") & (c["CLAVE DEL MUNICIPIO"] == "002")
          & c["CLAVE DE LA LOCALIDAD"].isin(URBANAS)]
    clu = gpd.GeoDataFrame({"cve_loc": c["CLAVE DE LA LOCALIDAD"], "asent": c.ASENTAMIENTO, "fuente": "CLUES"},
                           geometry=gpd.points_from_xy(c.LONGITUD.astype(float), c.LATITUD.astype(float)), crs=4326)
    return gpd.GeoDataFrame(pd.concat([den, sep, clu], ignore_index=True), crs=4326).to_crs(crs)


def mas_frecuente(nombres):
    vc = nombres.value_counts()
    if not len(vc):
        return None, 0, False
    return vc.index[0], int(vc.iloc[0]), bool(len(vc) > 1 and vc.iloc[0] == vc.iloc[1])


def colonias():
    cat = pd.DataFrame(json.loads((RAW / "asentamientos" / "asentamientos_11_002.json").read_text())["datos"])
    cat["clave_nombre"] = cat.nom_asen.map(normal)
    v = {"catalogo_asentamientos": len(cat), "catalogo_periodo": sorted(cat.periodo.unique()),
         "catalogo_por_localidad": cat.cve_loc.value_counts().to_dict(),
         "catalogo_por_tipo": cat.tipo_asen.value_counts().to_dict()}
    mza = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="manzanas")
    pts = puntos_con_asentamiento(mza.crs)
    pts["clave_nombre"] = pts.asent.map(normal)
    # Solo nombres que existen en el catálogo de la misma localidad
    validos = set(zip(cat.cve_loc, cat.clave_nombre))
    pts["en_catalogo"] = [(l, n) in validos for l, n in zip(pts.cve_loc, pts.clave_nombre)]
    v["registros_con_asentamiento"] = pts.groupby("fuente").size().to_dict()
    v["registros_con_nombre_en_catalogo"] = pts[pts.en_catalogo].groupby("fuente").size().to_dict()
    v["nombres_fuera_de_catalogo_mas_frecuentes"] = (pts[~pts.en_catalogo].asent.value_counts().head(15).to_dict())
    pts = pts[pts.en_catalogo]

    filas = []
    dentro = gpd.sjoin(pts, mza[["CVEGEO", "geometry"]], predicate="within")
    por_cuadra = dentro.groupby("CVEGEO").clave_nombre
    for _, m in mza.iterrows():
        loc_pts = pts[pts.cve_loc == m.CVE_LOC]
        if m.CVEGEO in por_cuadra.groups:
            nom, n, empate = mas_frecuente(por_cuadra.get_group(m.CVEGEO))
            como = "registros dentro de la cuadra"
        else:
            d = loc_pts.distance(m.geometry)
            cerca = loc_pts[d <= DIST_VECINOS].assign(d=d[d <= DIST_VECINOS]).nsmallest(K_VECINOS, "d")
            nom, n, empate = mas_frecuente(cerca.clave_nombre)
            como = f"{K_VECINOS} registros más cercanos (<= {DIST_VECINOS} m)" if nom else "sin registros cerca"
        filas.append({"CVEGEO": m.CVEGEO, "CVE_LOC": m.CVE_LOC, "clave_nombre": nom, "como": como,
                      "votos": n, "empate": empate})
    t = pd.DataFrame(filas)
    ref = cat.drop_duplicates(["cve_loc", "clave_nombre"]).set_index(["cve_loc", "clave_nombre"])
    t["colonia"] = [ref.nom_asen.get((l, n)) if n else None for l, n in zip(t.CVE_LOC, t.clave_nombre)]
    t["tipo_asentamiento"] = [ref.tipo_asen.get((l, n)) if n else None for l, n in zip(t.CVE_LOC, t.clave_nombre)]
    t["localidad"] = t.CVE_LOC.map(URBANAS)
    t = t.merge(mza[["CVEGEO", "POBTOT"]], on="CVEGEO")
    t.drop(columns="clave_nombre").to_csv(P / "colonias_cuadras.csv", index=False)

    usados = t.groupby(["CVE_LOC", "colonia"]).agg(cuadras=("CVEGEO", "size"), pob_2020=("POBTOT", "sum")).reset_index()
    cat_out = cat.merge(usados, left_on=["cve_loc", "nom_asen"], right_on=["CVE_LOC", "colonia"], how="left")
    cat_out[["cvegeo", "cve_loc", "cve_asen", "nom_asen", "tipo_asen", "periodo", "cuadras", "pob_2020"]].fillna(
        {"cuadras": 0, "pob_2020": 0}).to_csv(P / "colonias_catalogo.csv", index=False)

    v["cuadras_por_metodo"] = t.groupby(["localidad", "como"]).size().unstack(fill_value=0).to_dict("index")
    v["cuadras_con_nombre_pct"] = t.groupby("localidad").colonia.apply(lambda x: round(100 * x.notna().mean(), 1)).to_dict()
    v["poblacion_con_nombre_pct"] = t.groupby("localidad").apply(
        lambda g: round(100 * g.loc[g.colonia.notna(), "POBTOT"].sum() / g.POBTOT.sum(), 1)).to_dict()
    v["cuadras_con_empate"] = int(t.empate.sum())
    v["asentamientos_del_catalogo_sin_cuadra_urbana"] = int(
        (cat_out.cuadras.fillna(0) == 0)[cat_out.cve_loc.isin(URBANAS)].sum())
    v["asentamientos_del_catalogo_en_localidades_urbanas"] = int(cat_out.cve_loc.isin(URBANAS).sum())
    return v


def contexto():
    mza, ageb, loc, _ = base03.censo_manzanas("censo2020_mza_acambaro.csv", VARS_CONTEXTO)
    it = base03.numeros(pd.read_csv(P / "iter2020_acambaro.csv", dtype=str), VARS_CONTEXTO)
    it = it[~it.LOC.isin(["0000", "9998", "9999"])]

    def indicadores(t):
        out = pd.DataFrame({
            "poblacion_2020": t.POBTOT,
            "escolaridad_promedio_anios": t.GRAPROES,
            "pct_15ymas_analfabeta": 100 * t.P15YM_AN / t.P_15YMAS,
            "pct_sin_afiliacion_salud": 100 * t.PSINDER / t.POBTOT,
            "pct_viv_sin_agua_entubada_dentro": 100 * (1 - t.VPH_AGUADV / t.VIVPAR_HAB),
            "pct_viv_sin_drenaje": 100 * t.VPH_NODREN / t.VIVPAR_HAB,
            "pct_viv_sin_electricidad": 100 * t.VPH_S_ELEC / t.VIVPAR_HAB,
            "pct_viv_sin_automovil": 100 * (1 - t.VPH_AUTOM / t.VIVPAR_HAB),
        }).round(1)
        return out

    a = pd.concat([ageb[["LOC", "NOM_LOC", "AGEB"]].rename(columns={"LOC": "cve_loc", "NOM_LOC": "localidad",
                                                                     "AGEB": "cve_ageb"}),
                   indicadores(ageb)], axis=1)
    a["localidad"] = a.cve_loc.map(URBANAS)
    a.to_csv(P / "contexto_ageb.csv", index=False)
    l_ = pd.concat([it[["LOC", "NOM_LOC"]].rename(columns={"LOC": "cve_loc", "NOM_LOC": "localidad"}),
                    indicadores(it)], axis=1)
    l_["urbana"] = l_.cve_loc.isin(URBANAS)
    l_.to_csv(P / "contexto_localidades.csv", index=False)
    return {"agebs": len(a), "localidades": len(l_),
            "localidades_con_algun_indicador_oculto": int(l_.drop(columns=["cve_loc", "localidad", "urbana"])
                                                         .isna().any(axis=1).sum()),
            "agebs_con_algun_indicador_oculto": int(a.drop(columns=["cve_loc", "localidad", "cve_ageb"])
                                                    .isna().any(axis=1).sum())}


def main():
    v = {"colonias": colonias(), "contexto": contexto()}
    (P / "validacion_fase3_colonias.json").write_text(json.dumps(v, ensure_ascii=False, indent=1, default=str))
    print(json.dumps(v, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
