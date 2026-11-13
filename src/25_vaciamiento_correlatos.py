"""25 · ¿Con qué va junto el vaciamiento? (fase 5). Descriptivo, no causal.

Unidades (D57):
  - AGEB urbanas 2020 de las 4 localidades urbanas (fila de total de AGEB del censo
    por manzana), con >= 30 viviendas (mismo mínimo que la tipología, D47);
  - localidades rurales del ITER 2020 con >= 30 viviendas.
Variable de vaciamiento: % deshabitadas, % uso temporal y % no habitadas (sobre VIVTOT).
Variables de contexto (Censo 2020): % de 60 y más, % nacida en otra entidad (PNACOE /
POBTOT), % que en 2015 vivía en otra entidad (PRESOE15 / P_5YMAS), hogares (TOTHOG),
promedio de ocupantes por vivienda (PROM_OCUP) y cambio de población 2010–2020 (AGEB:
el de su "unidad comparable" de la fase 4b; rural: ITER 2010 vs 2020).
El censo por AGEB no publica a quién vivía en otro país en 2015: no se usa.
Medida: correlación de rangos de Spearman y promedios por cuartil de % no habitadas.
Son correlaciones entre áreas: no dicen nada de personas ni de causas.

EIC 2025 (municipal, con intervalo de 90 %): % que en 2020 vivía en otra entidad, en
EE. UU. o en otro país (personas de 5 años y más), y % de hogares que reciben dinero de
alguien que vive en otro país (remesas); Acámbaro y Guanajuato.

Salidas: data/processed/vaciamiento_unidades.csv, vaciamiento_correlaciones.csv,
vaciamiento_cuartiles.csv, vaciamiento_eic2025.csv; validacion_fase5.json ("vaciamiento").
"""

import importlib.util
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
RAW = RAIZ / "data" / "raw"

spec = importlib.util.spec_from_file_location("v23", RAIZ / "src" / "23_verificacion_zonas.py")
v23 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v23)
URBANAS = v23.URBANAS

warnings.filterwarnings("ignore", category=RuntimeWarning)
MIN_VIV = 30
Z90 = 1.645
Y = {"pct_deshabitadas": "% deshabitadas", "pct_uso_temporal": "% uso temporal", "pct_no_habitadas": "% no habitadas"}
X = {"pct_60ymas": "% de 60 años y más", "pct_nacida_otra_entidad": "% nacida en otra entidad",
     "pct_vivia_otra_entidad_2015": "% que en 2015 vivía en otra entidad", "hogares": "hogares",
     "prom_ocupantes": "promedio de ocupantes por vivienda", "cambio_pob_pct_2010_2020": "cambio de población 2010–2020 (%)"}
NUM = ["POBTOT", "VIVTOT", "TVIVHAB", "VIVPAR_DES", "VIVPAR_UT", "P_60YMAS", "PNACOE", "PRESOE15", "P_5YMAS",
       "TOTHOG", "PROM_OCUP"]


def indicadores(t):
    t = t.copy()
    for c in NUM:
        t[c] = pd.to_numeric(t[c], errors="coerce")   # "*" -> NaN
    t["pct_deshabitadas"] = 100 * t.VIVPAR_DES / t.VIVTOT
    t["pct_uso_temporal"] = 100 * t.VIVPAR_UT / t.VIVTOT
    t["pct_no_habitadas"] = 100 * (t.VIVTOT - t.TVIVHAB) / t.VIVTOT
    t["pct_60ymas"] = 100 * t.P_60YMAS / t.POBTOT
    t["pct_nacida_otra_entidad"] = 100 * t.PNACOE / t.POBTOT
    t["pct_vivia_otra_entidad_2015"] = 100 * t.PRESOE15 / t.P_5YMAS
    t["hogares"] = t.TOTHOG
    t["prom_ocupantes"] = t.PROM_OCUP
    return t


def unidades():
    c = pd.read_csv(P / "censo2020_mza_acambaro.csv", dtype=str)
    a = c[(c.MZA == "000") & (c.AGEB != "0000") & c.LOC.isin(URBANAS)].copy()
    a = indicadores(a)
    a["conjunto"] = "urbano (AGEB)"
    a["clave"] = a.LOC + "-" + a.AGEB
    a["localidad"] = a.LOC.map(URBANAS)
    tip = pd.read_csv(P / "tipologia_ageb.csv", dtype={"cve_loc": str, "cve_ageb": str})
    dec = pd.read_csv(P / "crecimiento_viviendas_2010_2020.csv", dtype={"cve_loc": str})
    dec = dec[dec.nivel == "unidad"].set_index(["cve_loc", "unidad"])
    tip["cambio_pob_pct_2010_2020"] = [100 * dec.cambio_pob.get((l, u), np.nan) / dec.POBTOT_2010.get((l, u), np.nan)
                                       for l, u in zip(tip.cve_loc, tip.unidad_2010_2020)]
    tip["cambio_pob_pct_2010_2020"] = tip.cambio_pob_pct_2010_2020.replace([np.inf, -np.inf], np.nan)  # unidad sin gente en 2010
    tip["clave"] = tip.cve_loc + "-" + tip.cve_ageb
    a = a.merge(tip[["clave", "cambio_pob_pct_2010_2020", "clase"]], on="clave", how="left")

    i20 = pd.read_csv(P / "iter2020_acambaro.csv", dtype={"LOC": str})
    i10 = pd.read_csv(P / "iter2010_acambaro.csv", dtype={"LOC": str}, usecols=["LOC", "POBTOT"])
    r = i20[~i20.LOC.isin(list(URBANAS) + ["0000", "9998", "9999"])].copy()
    r = indicadores(r)
    r["conjunto"] = "rural (localidad)"
    r["clave"] = r.LOC
    r["localidad"] = r.NOM_LOC
    p10 = pd.to_numeric(i10.set_index("LOC").POBTOT, errors="coerce")
    r["cambio_pob_pct_2010_2020"] = 100 * (r.POBTOT / r.LOC.map(p10) - 1)
    cols = ["conjunto", "clave", "localidad", "POBTOT", "VIVTOT"] + list(Y) + list(X) + ["clase"]
    return pd.concat([a.reindex(columns=cols), r.reindex(columns=cols)], ignore_index=True)


def main():
    v = {}
    u = unidades()
    u["con_minimo"] = u.VIVTOT >= MIN_VIV
    u["completa"] = u[list(Y) + list(X)].notna().all(axis=1)
    u.round(2).to_csv(P / "vaciamiento_unidades.csv", index=False, encoding="utf-8-sig")
    for k, s in u.groupby("conjunto"):
        m = s[s.con_minimo]
        v[k] = {"unidades": len(s), "con_minimo_30_viv": len(m), "pob_bajo_minimo": int(s.POBTOT[~s.con_minimo].sum()),
                "completas": int(m.completa.sum()), "pob_en_unidades_con_oculto": int(m.POBTOT[~m.completa].sum()),
                "pob_total": int(s.POBTOT.sum()),
                "oculto_por_variable": {c: int(m[c].isna().sum()) for c in list(Y) + list(X) if m[c].isna().any()}}

    filas = []
    grupos = [("urbano (AGEB)", "4 localidades urbanas", None), ("urbano (AGEB)", "Acámbaro (ciudad)", "Acámbaro"),
              ("rural (localidad)", "localidades rurales", None)]
    for conj, etiqueta, loc in grupos:
        m = u[(u.conjunto == conj) & u.con_minimo]
        if loc:
            m = m[m.localidad == loc]
        for y in Y:
            for x in X:
                s = m[[x, y]].dropna()
                rho, p = spearmanr(s[x], s[y]) if len(s) > 5 else (np.nan, np.nan)
                filas.append({"conjunto": etiqueta, "vaciamiento": Y[y], "variable": X[x], "n": len(s),
                              "rho_spearman": round(rho, 2), "p_valor": round(p, 4),
                              "lectura": ("fuerte" if abs(rho) >= 0.5 else "moderada" if abs(rho) >= 0.3 else "débil")
                              + (" (positiva)" if rho > 0 else " (negativa)")})
    cor = pd.DataFrame(filas)
    cor.to_csv(P / "vaciamiento_correlaciones.csv", index=False, encoding="utf-8-sig")

    # Promedios por cuartil de % no habitadas (dentro de cada conjunto)
    cu = []
    for conj, etiqueta, loc in grupos:
        m = u[(u.conjunto == conj) & u.con_minimo & u.pct_no_habitadas.notna()].copy()
        if loc:
            m = m[m.localidad == loc]
        m["cuartil"] = pd.qcut(m.pct_no_habitadas, 4, labels=["Q1 (menos vacío)", "Q2", "Q3", "Q4 (más vacío)"])
        g = m.groupby("cuartil", observed=True).agg(unidades=("clave", "size"), poblacion=("POBTOT", "sum"),
                                                    no_habitadas_min=("pct_no_habitadas", "min"),
                                                    no_habitadas_max=("pct_no_habitadas", "max"),
                                                    **{x: (x, "median") for x in X}).round(1).reset_index()
        g.insert(0, "conjunto", etiqueta)
        cu.append(g)
    cu = pd.concat(cu)
    cu.to_csv(P / "vaciamiento_cuartiles.csv", index=False, encoding="utf-8-sig")

    # EIC 2025: migración municipal y estatal con IC 90 %
    var = {"PCN_PRESOE20": "% que en 2020 vivía en otra entidad", "PCN_PRESEUA20": "% que en 2020 vivía en EE. UU.",
           "PCN_PRESOP20": "% que en 2020 vivía en otro país (no EE. UU.)",
           "PCN_HOG_OPAIS": "% de hogares que reciben dinero de alguien que vive en otro país (remesas)"}
    with zipfile.ZipFile(RAW / "eic2025" / "conjunto_de_datos_eic2025_105_csv.zip") as z, \
            z.open("conjunto_de_datos/conjunto_datos_eic2025_105.csv") as fh:
        e = pd.read_csv(fh, dtype=str, encoding="latin1", usecols=["CVEGEO", "ESTIMADOR", *var])
    eic = []
    for cve, nom in [("110020000", "Acámbaro"), ("110000000", "Guanajuato")]:
        s = e[e.CVEGEO == cve].set_index("ESTIMADOR")
        for k, d in var.items():
            val, ee = pd.to_numeric(s.loc["Valor", k], errors="coerce"), pd.to_numeric(s.loc["Error estándar", k], errors="coerce")
            eic.append({"unidad": nom, "variable": d, "clave": k, "valor": val, "error_estandar": ee,
                        "li90": round(val - Z90 * ee, 2), "ls90": round(val + Z90 * ee, 2)})
    eic = pd.DataFrame(eic)
    eic.to_csv(P / "vaciamiento_eic2025.csv", index=False, encoding="utf-8-sig")
    v["eic2025"] = eic.to_dict("records")
    v23.guardar_validacion("vaciamiento", v)

    pd.set_option("display.width", 250)
    print(cor[cor.vaciamiento == "% no habitadas"].to_string())
    print(cor[(cor.vaciamiento != "% no habitadas") & (cor.rho_spearman.abs() >= 0.3)].to_string())
    print(cu.to_string())
    print(eic.to_string())
    print({k: v[k] for k in v if k != "eic2025"})


if __name__ == "__main__":
    main()
