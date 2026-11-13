"""23 · Verificación visual de zonas (fase 5).

Incorpora la revisión de Alejandro en Google Earth (release "datos-crudos"):
  - verificacion_zonas.csv       28 zonas de cuadras nuevas del INEGI (15 de 2010–2020, 13 posteriores)
  - verificacion_zonas_ghsl.csv  las 20 zonas GHSL "sin cuadras" más grandes (D52)

1. Zonas INEGI: resultado por zona; Z20-010 se excluye por error de dibujo (D53;
   la exclusión se aplica en 19_crecimiento.py).
2. Zonas 2010–2020 (las 150) y el ITER 2010 (D54, regla de Alejandro): si la localidad
   ya tenía población en el ITER 2010, la zona es "cambio de cartografía" (pueblo que
   existía y se empezó a dibujar en cuadras), no crecimiento nuevo. En las 4 localidades
   urbanas (D09), que ya estaban completas en cuadras en 2010, las cuadras nuevas son
   ampliación de la mancha: crecimiento. Sin población en 2010: crecimiento nuevo.
   Personas: las de la zona (cuadras 2020) solo existen en las 4 urbanas; en lo rural
   el censo por cuadra no se publica, así que se da la población de la localidad
   completa en el ITER 2010 y 2020 (no la de la zona).
3. Zonas GHSL: tipo de lo que se ve (vivienda / invernadero o nave / baldío / otros),
   en número de zonas y m² ganados 2010–2020. D52: detecta construcción, no vivienda.

Salidas en data/processed/:
  verificacion_zonas_resultado.csv, zonas_2010_2020_clase.csv,
  verificacion_ghsl_resultado.csv, validacion_fase5.json (clave "zonas")
"""

import importlib.util
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
V = RAIZ / "data" / "raw" / "verificacion"
DOCS = RAIZ / "docs"

spec = importlib.util.spec_from_file_location("acc11", RAIZ / "src" / "11_accesibilidad.py")
acc11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc11)
URBANAS = acc11.URBANAS

spec = importlib.util.spec_from_file_location("cre19", RAIZ / "src" / "19_crecimiento.py")
cre19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cre19)
EXCLUIR_ZONAS = cre19.EXCLUIR_ZONAS

# Tipo GHSL a partir de lo que Alejandro anotó en que_se_ve (se aplica en este orden).
# Revisado a mano zona por zona (docs/validacion.md, V49).
REGLAS_GHSL = [
    ("otros", ["casa aislada", "panteón", "o invernadero"]),   # casa con bodega, panteón, dudosa
    ("invernadero o nave", ["invernadero", "nave"]),
    ("baldío", ["baldío"]),
    ("vivienda", ["casas", "casa"]),
]


def tipo_ghsl(texto):
    t = str(texto).lower()
    for tipo, claves in REGLAS_GHSL:
        if any(c in t for c in claves):
            return tipo
    return "otros"


def guardar_validacion(clave, valor):
    ruta = P / "validacion_fase5.json"
    v = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    v[clave] = valor
    ruta.write_text(json.dumps(v, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


def main():
    v = {}
    # --- 1. Zonas INEGI -----------------------------------------------------------
    rev = pd.read_csv(V / "verificacion_zonas.csv", dtype=str)
    lista = pd.read_csv(DOCS / "verificar_zonas_nuevas.csv", dtype={"cve_loc": str})
    huerf = set(rev.id) - set(lista.id)
    r = lista.drop(columns=["existe_en_imagen", "notas"]).merge(
        rev[["id", "existe_en_imagen", "que_se_ve", "notas"]], on="id", how="inner")
    r["existe_en_imagen"] = r.existe_en_imagen.str.strip().str.lower()
    r["excluida"] = r.id.isin(EXCLUIR_ZONAS)
    r["motivo_exclusion"] = r.excluida.map({True: "error de dibujo (D53)", False: ""})
    r.drop(columns=["claves_cuadras", "enlace_satelite", "que_verificar"]).to_csv(
        P / "verificacion_zonas_resultado.csv", index=False, encoding="utf-8-sig")
    v["inegi_revisadas"] = len(r)
    v["inegi_sin_pareja_en_lista"] = sorted(huerf)
    v["inegi_existe_en_imagen"] = r.existe_en_imagen.value_counts().to_dict()
    v["inegi_por_periodo"] = r.groupby(["periodo", "existe_en_imagen"]).size().rename("zonas").reset_index().to_dict("records")
    v["inegi_excluidas"] = r[r.excluida][["id", "localidad", "n_cuadras", "superficie_ha"]].to_dict("records")
    z20 = lista[lista.periodo == "posterior a 2020"]
    v["posteriores_2020_sin_excluidas"] = {"zonas": int((~z20.id.isin(EXCLUIR_ZONAS)).sum()),
                                           "cuadras": int(z20[~z20.id.isin(EXCLUIR_ZONAS)].n_cuadras.sum()),
                                           "ha": round(float(z20[~z20.id.isin(EXCLUIR_ZONAS)].superficie_ha.sum()), 2),
                                           "antes": {"zonas": len(z20), "cuadras": int(z20.n_cuadras.sum()),
                                                     "ha": round(float(z20.superficie_ha.sum()), 2)}}

    # --- 2. Zonas 2010–2020 y el ITER 2010 ----------------------------------------
    i10 = pd.read_csv(P / "iter2010_acambaro.csv", dtype={"LOC": str}, usecols=["LOC", "NOM_LOC", "POBTOT", "VIVTOT"])
    i20 = pd.read_csv(P / "iter2020_acambaro.csv", dtype={"LOC": str}, usecols=["LOC", "NOM_LOC", "POBTOT", "VIVTOT"])
    i10 = i10[i10.LOC != "0000"].rename(columns={"NOM_LOC": "nombre_iter2010", "POBTOT": "pob_loc_2010", "VIVTOT": "viv_loc_2010"})
    i20 = i20[i20.LOC != "0000"].rename(columns={"NOM_LOC": "nombre_iter2020", "POBTOT": "pob_loc_2020", "VIVTOT": "viv_loc_2020"})
    z = lista[lista.periodo == "2010-2020"].merge(i10, left_on="cve_loc", right_on="LOC", how="left").drop(columns="LOC")
    z = z.merge(i20, left_on="cve_loc", right_on="LOC", how="left").drop(columns="LOC")
    for c in ["pob_loc_2010", "pob_loc_2020", "viv_loc_2010", "viv_loc_2020"]:
        z[c] = pd.to_numeric(z[c], errors="coerce")
    z["nombre_distinto_2010"] = z.nombre_iter2010.notna() & (z.nombre_iter2010.str.strip() != z.localidad.str.strip())
    tenia = z.pob_loc_2010.fillna(0) > 0
    urb = z.cve_loc.isin(URBANAS)
    z["clase"] = "crecimiento nuevo (localidad sin población en 2010)"
    z.loc[tenia & ~urb, "clase"] = "cambio de cartografía (pueblo que ya existía)"
    z.loc[urb, "clase"] = "crecimiento (ampliación de localidad urbana)"
    z["cuadras_en_mg2010"] = z.localidad_ya_cartografiada
    z = z.merge(rev[["id", "existe_en_imagen", "que_se_ve", "notas"]], on="id", how="left", suffixes=("_x", ""))
    z = z.drop(columns=[c for c in z.columns if c.endswith("_x")])
    cols = ["id", "cve_loc", "localidad", "nombre_iter2010", "nombre_distinto_2010", "clase", "cuadras_en_mg2010",
            "n_cuadras", "superficie_ha", "pob_2020", "pob_loc_2010", "pob_loc_2020", "viv_loc_2010", "viv_loc_2020",
            "en_kml", "existe_en_imagen", "que_se_ve", "notas", "lat", "lon"]
    z[cols].to_csv(P / "zonas_2010_2020_clase.csv", index=False, encoding="utf-8-sig")

    # Resumen por clase: personas de la zona solo en urbanas; localidades rurales sin duplicar
    filas = []
    for k, s in z.groupby("clase"):
        locs = s.drop_duplicates("cve_loc")
        filas.append({"clase": k, "zonas": len(s), "cuadras": int(s.n_cuadras.sum()),
                      "ha": round(float(s.superficie_ha.sum()), 1), "localidades": len(locs),
                      "personas_en_las_cuadras_2020": int(s.pob_2020.fillna(0).sum()) if k.startswith("crecimiento (") else None,
                      "pob_localidades_2010": int(locs.pob_loc_2010.fillna(0).sum()),
                      "pob_localidades_2020": int(locs.pob_loc_2020.fillna(0).sum()),
                      "viv_localidades_2010": int(locs.viv_loc_2010.fillna(0).sum()),
                      "viv_localidades_2020": int(locs.viv_loc_2020.fillna(0).sum()),
                      "zonas_revisadas": int(s.existe_en_imagen.notna().sum())})
    res = pd.DataFrame(filas)
    v["z10_por_clase"] = res.to_dict("records")
    # Sensibilidad: dentro de "cambio de cartografía", si la localidad ya tenía alguna cuadra en el MG 2010
    cc = z[z.clase.str.startswith("cambio")]
    v["z10_cartografia_por_cuadras_previas"] = cc.groupby("cuadras_en_mg2010").agg(
        zonas=("id", "size"), ha=("superficie_ha", "sum")).round(1).reset_index().to_dict("records")
    v["z10_nombre_distinto_2010"] = z[z.nombre_distinto_2010][["id", "localidad", "nombre_iter2010"]].to_dict("records")
    v["z10_sin_iter2010"] = z[z.pob_loc_2010.isna()][["id", "localidad", "cve_loc", "superficie_ha"]].to_dict("records")
    v["z10_revisadas_por_clase"] = z[z.existe_en_imagen.notna()].groupby("clase").id.apply(list).to_dict()
    nuevas = z[z.clase.str.startswith("crecimiento nuevo")]
    v["z10_crecimiento_nuevo_localidades"] = nuevas.groupby(["cve_loc", "localidad"]).agg(
        zonas=("id", "size"), ha=("superficie_ha", "sum"), pob_loc_2020=("pob_loc_2020", "first")).reset_index().to_dict("records")

    # --- 3. Zonas GHSL ----------------------------------------------------------------
    g = pd.read_csv(V / "verificacion_zonas_ghsl.csv", dtype={"id": str})
    todas = pd.read_csv(P / "ghsl_zonas_sin_cuadras.csv", dtype={"cve_loc": str})
    g["tipo"] = g.que_se_ve.map(tipo_ghsl)
    g["existe_en_imagen"] = g.existe_en_imagen.str.strip().str.lower()
    g = g.merge(todas[["id", "cve_loc", "dist_centro_m", "celdas"]], on="id", how="left")
    g[["id", "localidad", "cve_loc", "superficie_ha", "m2_ganados", "celdas", "dist_centro_m",
       "localidades_rurales_en_zona", "existe_en_imagen", "que_se_ve", "tipo", "notas"]].to_csv(
        P / "verificacion_ghsl_resultado.csv", index=False, encoding="utf-8-sig")
    t = g.groupby("tipo").agg(zonas=("id", "size"), m2_ganados=("m2_ganados", "sum"),
                              ids=("id", lambda s: " ".join(s))).reset_index()
    t["pct_m2_revisados"] = (100 * t.m2_ganados / t.m2_ganados.sum()).round(1)
    v["ghsl_por_tipo"] = t.to_dict("records")
    v["ghsl_por_tipo_y_localidad"] = g.groupby(["localidad", "tipo"]).agg(
        zonas=("id", "size"), m2=("m2_ganados", "sum")).reset_index().to_dict("records")
    v["ghsl_existe_en_imagen"] = g.existe_en_imagen.value_counts().to_dict()
    v["ghsl_m2_revisados_de_total"] = {"revisados": float(g.m2_ganados.sum()), "total_78": float(todas.m2_ganados.sum()),
                                       "pct": round(100 * g.m2_ganados.sum() / todas.m2_ganados.sum(), 1)}
    v["ghsl_sin_pareja"] = sorted(set(g.id) - set(todas.id))
    guardar_validacion("zonas", v)

    print(r.groupby(["periodo", "existe_en_imagen"]).size())
    print(res.to_string())
    print(t.to_string())
    print(json.dumps({k: v[k] for k in ["z10_cartografia_por_cuadras_previas", "z10_nombre_distinto_2010",
                                        "z10_sin_iter2010", "ghsl_m2_revisados_de_total", "posteriores_2020_sin_excluidas"]},
                     ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
