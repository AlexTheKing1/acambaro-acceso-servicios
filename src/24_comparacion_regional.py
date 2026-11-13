"""24 · Comparación regional (fase 5).

Acámbaro frente a sus vecinos de Guanajuato (Coroneo, Jerécuaro, Salvatierra,
Santiago Maravatío, Tarandacuao, Tarimoro), el total de Guanajuato y el nacional,
con el ITER 2010 y 2020 (censos completos) y la EIC 2025 (encuesta, solo población,
con intervalo de confianza de 90 %).

Para cada municipio, a nivel municipio (LOC 0000) y cabecera (LOC 0001):
  población, viviendas totales, cambio 2010→2020 (%),
  % deshabitadas = VIVPAR_DES / VIVTOT, % uso temporal = VIVPAR_UT / VIVTOT (D55:
  mismo denominador que la fase 4b; las colectivas son < 0.1 % de VIVTOT).

Salidas: data/processed/comparacion_regional.csv, docs/figuras/fase5_regional.png,
validacion_fase5.json (clave "regional").
"""

import importlib.util
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
P = RAIZ / "data" / "processed"
FIG = RAIZ / "docs" / "figuras"

spec = importlib.util.spec_from_file_location("v23", RAIZ / "src" / "23_verificacion_zonas.py")
v23 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v23)

MUNICIPIOS = {"002": "Acámbaro", "010": "Coroneo", "019": "Jerécuaro", "028": "Salvatierra",
              "036": "Santiago Maravatío", "038": "Tarandacuao", "039": "Tarimoro"}
COLS = ["POBTOT", "VIVTOT", "TVIVHAB", "VIVPAR_DES", "VIVPAR_UT"]
Z90 = 1.645


def leer(zip_, interno, **kw):
    with zipfile.ZipFile(RAW / zip_) as z, z.open(interno) as f:
        t = pd.read_csv(f, dtype=str, **kw)
    t.columns = [c.upper() for c in t.columns]
    return t


def filas_iter(t, anio):
    t = t.rename(columns={"ENTIDAD": "ENT"})
    out = []
    for mun, nom in MUNICIPIOS.items():
        for loc, nivel in [("0000", "municipio"), ("0001", "cabecera")]:
            r = t[(t.ENT == "11") & (t.MUN == mun) & (t.LOC == loc)]
            out.append({"cve_mun": mun, "unidad": nom, "nivel": nivel, "nombre_loc": r.NOM_LOC.iloc[0], "anio": anio,
                        **{c: pd.to_numeric(r[c].iloc[0], errors="coerce") for c in COLS}})
    return out


def total(t, ent, nombre, anio):
    t = t.rename(columns={"ENTIDAD": "ENT"})
    r = t[(t.ENT == ent) & (t.MUN == "000") & (t.LOC == "0000")]
    return {"cve_mun": "000", "unidad": nombre, "nivel": "municipio", "nombre_loc": r.NOM_LOC.iloc[0], "anio": anio,
            **{c: pd.to_numeric(r[c].iloc[0], errors="coerce") for c in COLS}}


def main():
    v = {}
    g10 = leer("iter2010/iter_11_2010_csv.zip", "iter_11_cpv2010/conjunto_de_datos/iter_11_cpv2010.csv", encoding="utf-8-sig")
    g20 = leer("iter2020/iter_11_cpv2020_csv.zip", "iter_11_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_11CSV20.csv")
    n10 = leer("iter_nacional/iter_nal_2010_csv.zip", "iter_00_cpv2010/conjunto_de_datos/iter_00_cpv2010.csv",
               encoding="utf-8-sig", usecols=lambda c: c.upper() in {"ENTIDAD", "MUN", "LOC", "NOM_LOC", *COLS})
    n20 = leer("iter_nacional/iter_00_cpv2020_csv.zip", "iter_00_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_00CSV20.csv",
               usecols=lambda c: c.upper() in {"ENTIDAD", "MUN", "LOC", "NOM_LOC", *COLS})
    f = filas_iter(g10, 2010) + filas_iter(g20, 2020)
    f += [total(g10, "11", "Guanajuato", 2010), total(g20, "11", "Guanajuato", 2020),
          total(n10, "00", "Nacional", 2010), total(n20, "00", "Nacional", 2020)]
    d = pd.DataFrame(f)
    d["pct_deshabitadas"] = (100 * d.VIVPAR_DES / d.VIVTOT).round(1)
    d["pct_uso_temporal"] = (100 * d.VIVPAR_UT / d.VIVTOT).round(1)
    d["pct_no_habitadas"] = (100 * (d.VIVTOT - d.TVIVHAB) / d.VIVTOT).round(1)

    # Chequeos: Acámbaro igual a lo ya usado; nacional 2020 = suma de los 32 estados del mismo archivo
    a = d[(d.cve_mun == "002") & (d.nivel == "municipio")].set_index("anio").POBTOT
    v["chequeo_acambaro"] = {"2010": int(a[2010]), "2020": int(a[2020]), "esperado": "109030 / 108697",
                             "ok": bool(a[2010] == 109030 and a[2020] == 108697)}
    n20e = n20.rename(columns={"ENTIDAD": "ENT"})
    est = n20e[(n20e.MUN == "000") & (n20e.LOC == "0000") & (n20e.ENT != "00")]
    v["chequeo_nacional_2020_suma_estados"] = {"estados": len(est), "suma": int(pd.to_numeric(est.POBTOT).sum()),
                                               "total": int(d[(d.unidad == "Nacional") & (d.anio == 2020)].POBTOT.iloc[0])}
    v["chequeo_valores_faltantes"] = int(d[COLS].isna().sum().sum())

    # Ancho: una fila por unidad y nivel
    w = d.pivot_table(index=["cve_mun", "unidad", "nivel"], columns="anio",
                      values=COLS + ["pct_deshabitadas", "pct_uso_temporal", "pct_no_habitadas"]).reset_index()
    w.columns = [f"{a}_{b}" if b != "" else a for a, b in w.columns]
    w["cambio_pob_pct_2010_2020"] = (100 * (w.POBTOT_2020 / w.POBTOT_2010 - 1)).round(1)
    w["cambio_viv_pct_2010_2020"] = (100 * (w.VIVTOT_2020 / w.VIVTOT_2010 - 1)).round(1)
    w["cambio_hab_pct_2010_2020"] = (100 * (w.TVIVHAB_2020 / w.TVIVHAB_2010 - 1)).round(1)

    # EIC 2025: población con intervalo de 90 % (valor ± 1.645 × error estándar)
    with zipfile.ZipFile(RAW / "eic2025" / "conjunto_de_datos_eic2025_105_csv.zip") as z, \
            z.open("conjunto_de_datos/conjunto_datos_eic2025_105.csv") as fh:
        e = pd.read_csv(fh, dtype=str, encoding="latin1", usecols=["CVE_ENT", "CVE_MUN", "CVE_LOC", "ESTIMADOR", "POBTOT"])
    e["POBTOT"] = pd.to_numeric(e.POBTOT, errors="coerce")
    eic = []
    for _, r in w.iterrows():
        ent = "00" if r.unidad == "Nacional" else "11"
        loc = "0000" if r.nivel == "municipio" else "0001"
        s = e[(e.CVE_ENT == ent) & (e.CVE_MUN == r.cve_mun) & (e.CVE_LOC == loc)].set_index("ESTIMADOR").POBTOT
        if "Valor" in s:
            val, ee = s["Valor"], s["Error estándar"]
            eic.append({"pob_eic2025": val, "pob_eic2025_li90": round(val - Z90 * ee), "pob_eic2025_ls90": round(val + Z90 * ee),
                        "cambio_pob_pct_2020_2025": round(100 * (val / r.POBTOT_2020 - 1), 1),
                        "cambio_pct_2020_2025_li90": round(100 * ((val - Z90 * ee) / r.POBTOT_2020 - 1), 1),
                        "cambio_pct_2020_2025_ls90": round(100 * ((val + Z90 * ee) / r.POBTOT_2020 - 1), 1)})
        else:
            eic.append({})
    w = pd.concat([w, pd.DataFrame(eic, index=w.index)], axis=1)
    v["eic2025_sin_dato"] = [f"{u} ({n})" for u, n, x in zip(w.unidad, w.nivel, w.get("pob_eic2025")) if pd.isna(x)]
    orden = ["Acámbaro"] + [m for m in MUNICIPIOS.values() if m != "Acámbaro"] + ["Guanajuato", "Nacional"]
    w["orden"] = w.unidad.map({u: i for i, u in enumerate(orden)})
    w = w.sort_values(["nivel", "orden"], ascending=[False, True]).drop(columns="orden")
    w.to_csv(P / "comparacion_regional.csv", index=False, encoding="utf-8-sig")

    # ¿Destaca Acámbaro? Rango entre los 7 municipios y diferencia con la mediana de los otros 6
    comp = {}
    for nivel in ["municipio", "cabecera"]:
        m = w[(w.nivel == nivel) & (w.cve_mun != "000")].set_index("unidad")
        for c in ["cambio_pob_pct_2010_2020", "cambio_viv_pct_2010_2020", "pct_deshabitadas_2010", "pct_deshabitadas_2020",
                  "pct_uso_temporal_2010", "pct_uso_temporal_2020", "pct_no_habitadas_2020", "cambio_pob_pct_2020_2025"]:
            if c not in m or m[c].isna().all():
                continue
            x = m[c].dropna()
            if "Acámbaro" not in x:
                continue
            comp[f"{nivel} | {c}"] = {"acambaro": float(x["Acámbaro"]),
                                      "rango_de_mayor_a_menor": int(x.rank(ascending=False, method="min")["Acámbaro"]),
                                      "de": len(x), "mediana_otros": float(x.drop("Acámbaro").median()),
                                      "min_otros": float(x.drop("Acámbaro").min()), "max_otros": float(x.drop("Acámbaro").max())}
    v["acambaro_frente_a_vecinos"] = comp
    v23.guardar_validacion("regional", v)

    figura(w)
    pd.set_option("display.width", 250)
    print(w[["unidad", "nivel", "POBTOT_2010", "POBTOT_2020", "cambio_pob_pct_2010_2020", "cambio_viv_pct_2010_2020",
             "pct_deshabitadas_2010", "pct_deshabitadas_2020", "pct_uso_temporal_2010", "pct_uso_temporal_2020",
             "pob_eic2025", "cambio_pob_pct_2020_2025", "cambio_pct_2020_2025_li90", "cambio_pct_2020_2025_ls90"]].to_string())
    print(v["chequeo_acambaro"], v["chequeo_nacional_2020_suma_estados"], v["eic2025_sin_dato"])


def figura(w):
    """Tres paneles con eje propio: % deshabitadas, % uso temporal (2010 → 2020) y cambio de población."""
    AZUL, GRIS, GRIS_CLARO, TINTA, TINTA2 = "#2a78d6", "#8c8b86", "#c9c8c2", "#0b0b0b", "#52514e"
    m = w[w.nivel == "municipio"].iloc[::-1]
    y = np.arange(len(m))
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.8), sharey=True)
    paneles = [("pct_deshabitadas", "Viviendas deshabitadas (%)"), ("pct_uso_temporal", "Viviendas de uso temporal (%)")]
    for ax, (c, tit) in zip(axs, paneles):
        for i, (_, r) in enumerate(m.iterrows()):
            col = AZUL if r.unidad == "Acámbaro" else GRIS
            ax.plot([r[f"{c}_2010"], r[f"{c}_2020"]], [i, i], color=GRIS_CLARO, lw=2, zorder=1)
            ax.scatter(r[f"{c}_2010"], i, s=50, facecolor="white", edgecolor=col, lw=2, zorder=2)
            ax.scatter(r[f"{c}_2020"], i, s=60, color=col, zorder=3, edgecolor="white", lw=1.5)
        ax.set_title(tit, loc="left", fontsize=11, color=TINTA)
    ax = axs[2]
    for i, (_, r) in enumerate(m.iterrows()):
        col = AZUL if r.unidad == "Acámbaro" else GRIS
        ax.barh(i, r.cambio_pob_pct_2010_2020, color=col, height=0.55)
        ax.text(r.cambio_pob_pct_2010_2020 + (0.4 if r.cambio_pob_pct_2010_2020 >= 0 else -0.4), i,
                f"{r.cambio_pob_pct_2010_2020:+.1f}", va="center", fontsize=9, color=TINTA2,
                ha="left" if r.cambio_pob_pct_2010_2020 >= 0 else "right")
    ax.axvline(0, color=TINTA2, lw=0.8)
    ax.set_title("Cambio de población 2010–2020 (%)", loc="left", fontsize=11, color=TINTA)
    lo, hi = m.cambio_pob_pct_2010_2020.min(), m.cambio_pob_pct_2010_2020.max()
    ax.set_xlim(min(lo, 0) - 4, hi + 4)
    axs[0].set_yticks(y, m.unidad)
    for a in axs:
        a.grid(axis="x", color="#e6e5e0", lw=0.8)
        a.set_axisbelow(True)
        for s in ["top", "right", "left"]:
            a.spines[s].set_visible(False)
        a.tick_params(colors=TINTA2, labelsize=9)
    for lbl in axs[0].get_yticklabels():
        if lbl.get_text() == "Acámbaro":
            lbl.set_fontweight("bold")
    axs[0].scatter([], [], s=50, facecolor="white", edgecolor=GRIS, lw=2, label="2010")
    axs[0].scatter([], [], s=60, color=GRIS, label="2020")
    axs[0].legend(loc="lower right", frameon=False, fontsize=9)
    fig.suptitle("Acámbaro frente a sus vecinos, Guanajuato y el país (municipio completo)", x=0.01, ha="left",
                 fontsize=13, color=TINTA)
    fig.text(0.01, 0.01, "Fuente: INEGI, Censos de Población y Vivienda 2010 y 2020 (ITER). % sobre el total de viviendas.",
             fontsize=8, color=TINTA2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(FIG / "fase5_regional.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
