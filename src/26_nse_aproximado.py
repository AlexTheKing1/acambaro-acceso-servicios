"""26 · Nivel socioeconómico aproximado y acceso (fase 5).

Índice por AGEB urbana (4 localidades urbanas) y por localidad rural (ITER 2020), con
variables del Censo 2020 (D56). NO es el NSE oficial de la AMAI (que se calcula hogar
por hogar con su propio cuestionario: escolaridad del jefe, baños, autos, internet,
ocupados y dormitorios) y NO mide ingreso: es una aproximación inspirada en esa regla,
con lo que el censo publica por área.

Variables (proporción de viviendas particulares habitadas, TVIVPARHAB):
  escolaridad:  GRAPROES (grado promedio de escolaridad, 15 años y más)
  bienes:       VPH_AUTOM, VPH_INTER, VPH_PC, VPH_REFRI, VPH_LAVAD, VPH_HMICRO
  vivienda:     VPH_2YMASD (2 dormitorios o más)
  (Piso de tierra, VPH_PISOTI, queda fuera: el INEGI lo oculta con "*" en 16 de las 56 AGEB
  con >= 30 viviendas, 10 060 personas, y fuera de eso casi no varía: 96–100 % sin tierra.)
Fórmula: z(x) = (x − media) / desviación estándar, calculada DENTRO de cada conjunto
(urbano o rural); índice = 0.5 · z(escolaridad) + 0.5 · promedio de los 7 z de bienes y
vivienda. Quintiles del índice dentro de cada conjunto (Q1 = nivel más bajo).
Como los z son de cada conjunto, los quintiles urbanos y rurales NO se comparan entre sí.
Sensibilidad: pesos iguales para las 8 variables y primer componente principal.

Unidades: >= 30 viviendas (D57). Valores "*" -> sin dato; se cuenta la población perdida.
Cruce con el acceso (umbral principal, D33): % de la población lejos de cada servicio y
número promedio de servicios básicos lejos (preescolar, primaria, secundaria, salud
pública, mercado o supermercado), por quintil, por separado en cada conjunto.

Salidas: nse_ageb.csv, nse_localidades.csv, nse_acceso.csv, docs/figuras/fase5_nse.png,
validacion_fase5.json ("nse").
"""

import importlib.util
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
FIG = RAIZ / "docs" / "figuras"

spec = importlib.util.spec_from_file_location("v23", RAIZ / "src" / "23_verificacion_zonas.py")
v23 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v23)
URBANAS = v23.URBANAS
UC, UR = v23.acc11.UMBRALES_CIUDAD, v23.acc11.UMBRALES_RURAL
umbral = v23.acc11.umbral

MIN_VIV = 30
BIENES = ["VPH_AUTOM", "VPH_INTER", "VPH_PC", "VPH_REFRI", "VPH_LAVAD", "VPH_HMICRO", "VPH_2YMASD"]
NOMBRES = {"GRAPROES": "escolaridad promedio (años)", "VPH_AUTOM": "% con automóvil", "VPH_INTER": "% con internet",
           "VPH_PC": "% con computadora", "VPH_REFRI": "% con refrigerador", "VPH_LAVAD": "% con lavadora",
           "VPH_HMICRO": "% con horno de microondas", "VPH_2YMASD": "% con 2 dormitorios o más"}
SERV = ["preescolar", "primaria", "secundaria", "bachillerato_publico", "salud_publica", "tienda_basica", "abasto_completo"]
BASICOS = ["preescolar", "primaria", "secundaria", "salud_publica", "abasto_completo"]   # los 5 de la tipología (D47)
Q = ["Q1 (más bajo)", "Q2", "Q3", "Q4", "Q5 (más alto)"]


def preparar(t):
    t = t.copy()
    for c in ["POBTOT", "VIVTOT", "TVIVPARHAB", "GRAPROES"] + BIENES:
        t[c] = pd.to_numeric(t[c], errors="coerce")
    x = pd.DataFrame({"GRAPROES": t.GRAPROES}, index=t.index)
    for c in BIENES:
        x[c] = 100 * t[c] / t.TVIVPARHAB
    return t, x


def indice(x):
    z = (x - x.mean()) / x.std(ddof=0)
    base = 0.5 * z.GRAPROES + 0.5 * z[BIENES].mean(axis=1)
    iguales = z.mean(axis=1)
    u, s, vt = np.linalg.svd(z.to_numpy(), full_matrices=False)
    pc1 = pd.Series(u[:, 0] * s[0], index=z.index)
    if np.corrcoef(pc1, base)[0, 1] < 0:
        pc1, vt[0] = -pc1, -vt[0]
    cargas = dict(zip(z.columns, np.round(vt[0], 3)))
    varexp = float(round(s[0] ** 2 / (s ** 2).sum(), 3))
    return base, iguales, pc1, cargas, varexp


def construir(t, x, etiqueta):
    ok = (t.VIVTOT >= MIN_VIV) & x.notna().all(axis=1)
    base, ig, pc1, cargas, varexp = indice(x[ok])
    out = t.loc[ok].copy()
    out[list(x.columns)] = x[ok].round(2)
    out["indice"] = base.round(3)
    out["indice_pesos_iguales"] = ig.round(3)
    out["indice_pc1"] = pc1.round(3)
    out["quintil"] = pd.qcut(out.indice, 5, labels=Q)
    out["quintil_pesos_iguales"] = pd.qcut(out.indice_pesos_iguales, 5, labels=Q)
    out["quintil_pc1"] = pd.qcut(out.indice_pc1, 5, labels=Q)
    sens = {"rho_base_vs_pesos_iguales": round(spearmanr(out.indice, out.indice_pesos_iguales)[0], 3),
            "rho_base_vs_pc1": round(spearmanr(out.indice, out.indice_pc1)[0], 3),
            "mismo_quintil_pesos_iguales_pct": round(100 * (out.quintil == out.quintil_pesos_iguales).mean(), 1),
            "mismo_quintil_pc1_pct": round(100 * (out.quintil == out.quintil_pc1).mean(), 1),
            "pc1_cargas": cargas, "pc1_varianza_explicada": varexp}
    cob = {"unidades": len(t), "con_indice": int(ok.sum()),
           "bajo_minimo_30_viv": int((t.VIVTOT < MIN_VIV).sum()),
           "pob_bajo_minimo": int(t.POBTOT[t.VIVTOT < MIN_VIV].sum()),
           "con_oculto": int(((t.VIVTOT >= MIN_VIV) & ~x.notna().all(axis=1)).sum()),
           "pob_con_oculto": int(t.POBTOT[(t.VIVTOT >= MIN_VIV) & ~x.notna().all(axis=1)].sum()),
           "pob_con_indice": int(t.POBTOT[ok].sum()), "pob_total": int(t.POBTOT.sum())}
    perfil = out.groupby("quintil", observed=True)[list(x.columns)].median().round(1)
    perfil.insert(0, "unidades", out.groupby("quintil", observed=True).size())
    perfil.insert(1, "poblacion", out.groupby("quintil", observed=True).POBTOT.sum())
    return out, {"conjunto": etiqueta, "cobertura": cob, "sensibilidad": sens,
                 "perfil_por_quintil": perfil.reset_index().to_dict("records")}


def lejania(d, w, cats, tabla):
    """% de población lejos por servicio y número promedio de servicios básicos lejos."""
    r = {}
    nb = np.zeros(len(d))
    for c in cats:
        u = umbral(c.replace("_publico", ""), tabla)[1] if c != "bachillerato_publico" else tabla["bachillerato"][1]
        lejos = (d[f"d_{c}"] > u).to_numpy()
        r[f"pct_lejos_{c}"] = round(100 * w[lejos].sum() / w.sum(), 1)
        if c in BASICOS:
            nb += lejos
    r["servicios_basicos_lejos_prom"] = round(float((nb * w).sum() / w.sum()), 2)
    return r


def main():
    v = {}
    # --- Urbano: AGEB -----------------------------------------------------------------
    c = pd.read_csv(P / "censo2020_mza_acambaro.csv", dtype=str)
    a = c[(c.MZA == "000") & (c.AGEB != "0000") & c.LOC.isin(URBANAS)].copy()
    a["clave"] = a.LOC + "-" + a.AGEB
    a, xa = preparar(a)
    na, va = construir(a, xa, "urbano (AGEB)")
    tip = pd.read_csv(P / "tipologia_ageb.csv", dtype={"cve_loc": str, "cve_ageb": str})
    tip["clave"] = tip.cve_loc + "-" + tip.cve_ageb
    na = na.merge(tip[["clave", "clase", "servicios_lejos", "dist_centro_m"]], on="clave", how="left")
    na["localidad"] = na.LOC.map(URBANAS)
    cols = ["clave", "LOC", "localidad", "AGEB", "POBTOT", "VIVTOT", "TVIVPARHAB"] + list(NOMBRES) + \
        ["indice", "quintil", "indice_pesos_iguales", "quintil_pesos_iguales", "indice_pc1", "quintil_pc1",
         "clase", "servicios_lejos", "dist_centro_m"]
    na[cols].to_csv(P / "nse_ageb.csv", index=False, encoding="utf-8-sig")

    # --- Rural: localidades -----------------------------------------------------------
    i20 = pd.read_csv(P / "iter2020_acambaro.csv", dtype={"LOC": str})
    r = i20[~i20.LOC.isin(list(URBANAS) + ["0000", "9998", "9999"])].copy()
    r, xr = preparar(r)
    nr, vr = construir(r, xr, "rural (localidad)")
    nr[["LOC", "NOM_LOC", "POBTOT", "VIVTOT", "TVIVPARHAB"] + list(NOMBRES) +
       ["indice", "quintil", "indice_pesos_iguales", "quintil_pesos_iguales", "indice_pc1", "quintil_pc1"]].to_csv(
        P / "nse_localidades.csv", index=False, encoding="utf-8-sig")
    v["urbano"], v["rural"] = va, vr

    # --- Cruce con el acceso ------------------------------------------------------------
    filas = []
    acc = pd.read_csv(P / "acceso_cuadras.csv", dtype={"CVE_LOC": str, "CVE_AGEB": str})
    acc["clave"] = acc.CVE_LOC + "-" + acc.CVE_AGEB
    acc = acc.merge(na[["clave", "quintil", "quintil_pesos_iguales", "quintil_pc1"]], on="clave", how="left")
    acc["w"] = acc.POBTOT.fillna(0)
    v["urbano"]["pob_acceso_sin_quintil"] = int(acc.w[acc.quintil.isna()].sum())
    v["urbano"]["pob_acceso_total"] = int(acc.w.sum())
    rl = pd.read_csv(P / "acceso_localidades.csv", dtype={"LOC": str})
    rl = rl.merge(nr[["LOC", "quintil", "quintil_pesos_iguales", "quintil_pc1"]], on="LOC", how="left")
    rl["w"] = pd.to_numeric(rl.POBTOT, errors="coerce").fillna(0)
    v["rural"]["pob_acceso_sin_quintil"] = int(rl.w[rl.quintil.isna()].sum())
    v["rural"]["pob_acceso_total"] = int(rl.w.sum())
    # Irámuco cae casi entero en el quintil más bajo: se repite solo con la ciudad (mismos quintiles)
    for conj, d, cats, tabla in [("urbano (AGEB)", acc, SERV, UC),
                                 ("solo ciudad de Acámbaro (quintiles urbanos)", acc[acc.CVE_LOC == "0001"], SERV, UC),
                                 ("rural (localidad)", rl, [s for s in SERV if s != "tienda_basica"], UR)]:
        for var in ["quintil", "quintil_pesos_iguales", "quintil_pc1"]:
            for q, s in d[d[var].notna()].groupby(var, observed=True):
                filas.append({"conjunto": conj, "indice": {"quintil": "principal", "quintil_pesos_iguales": "pesos iguales",
                                                          "quintil_pc1": "componente principal"}[var],
                              "quintil": q, "unidades": s.clave.nunique() if "clave" in s else s.LOC.nunique(),
                              "poblacion": int(s.w.sum()), **lejania(s, s.w.to_numpy(), cats, tabla)})
    cr = pd.DataFrame(filas)
    cr.to_csv(P / "nse_acceso.csv", index=False, encoding="utf-8-sig")

    # Tipología (D47) por quintil, urbano
    v["urbano"]["tipologia_por_quintil"] = pd.crosstab(na.quintil, na.clase).to_dict("index")
    # Índice vs distancia al centro (urbano) y vs servicios lejos de la AGEB
    v["urbano"]["rho_indice_vs_dist_centro"] = round(spearmanr(na.indice, na.dist_centro_m, nan_policy="omit")[0], 3)
    v["urbano"]["rho_indice_vs_servicios_lejos"] = round(spearmanr(na.indice, na.servicios_lejos, nan_policy="omit")[0], 3)
    v["urbano"]["quintiles_por_localidad"] = pd.crosstab(na.localidad, na.quintil).to_dict("index")
    v23.guardar_validacion("nse", v)

    figura(cr)
    pd.set_option("display.width", 260)
    print(cr[cr.indice == "principal"].drop(columns=["indice"]).to_string())
    print(cr[cr.indice != "principal"][["conjunto", "indice", "quintil", "servicios_basicos_lejos_prom"]].to_string())
    for k in ["urbano", "rural"]:
        print(k, v[k]["cobertura"], v[k]["sensibilidad"], v[k].get("pob_acceso_sin_quintil"), v[k].get("pob_acceso_total"))
        print(pd.DataFrame(v[k]["perfil_por_quintil"]).to_string())
    print(v["urbano"]["tipologia_por_quintil"], v["urbano"]["rho_indice_vs_dist_centro"],
          v["urbano"]["rho_indice_vs_servicios_lejos"], v["urbano"]["quintiles_por_localidad"])


def figura(cr):
    """Dos paneles independientes (urbano y rural): no comparten escala de índice."""
    AZUL, TINTA, TINTA2 = "#2a78d6", "#0b0b0b", "#52514e"
    t = cr[cr.indice == "principal"]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
    titulos = {"urbano (AGEB)": "Ciudad y localidades urbanas (por AGEB)", "rural (localidad)": "Localidades rurales"}
    for ax, (conj, tit) in zip(axs, titulos.items()):
        s = t[t.conjunto == conj]
        x = np.arange(len(s))
        ax.bar(x, s.servicios_basicos_lejos_prom, color=AZUL, width=0.6)
        for i, val in zip(x, s.servicios_basicos_lejos_prom):
            ax.text(i, val + 0.05, f"{val:.1f}", ha="center", fontsize=9, color=TINTA2)
        ax.set_xticks(x, [q.replace(" (", "\n(") for q in s.quintil.astype(str)])
        ax.set_ylim(0, 5)
        ax.set_title(tit, loc="left", fontsize=11, color=TINTA)
        ax.grid(axis="y", color="#e6e5e0", lw=0.8)
        ax.set_axisbelow(True)
        for sp in ["top", "right", "left"]:
            ax.spines[sp].set_visible(False)
        ax.tick_params(colors=TINTA2, labelsize=9)
    axs[0].set_ylabel("Servicios básicos lejos (de 5), promedio por persona", fontsize=9, color=TINTA2)
    fig.suptitle("Nivel socioeconómico aproximado y lejanía a servicios básicos", x=0.01, ha="left", fontsize=13, color=TINTA)
    fig.text(0.01, 0.01, "Quintiles del índice dentro de cada panel; los dos paneles no se comparan entre sí. "
             "Índice aproximado (Censo 2020), no es el NSE de la AMAI ni ingreso. Umbral principal (D33).",
             fontsize=8, color=TINTA2)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(FIG / "fase5_nse.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
