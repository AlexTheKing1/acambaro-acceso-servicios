"""21 · Mapas y gráficas de la fase 4b (docs/figuras/fase4b_*.png).

  fase4b_antiguedad.png     cuadras por antigüedad (consolidada, nueva 2010–2020, posterior a 2020)
                            con anillos de 500 m desde el centro de cada localidad
  fase4b_deshabitadas.png   % de viviendas no habitadas (deshabitadas + uso temporal) por cuadra, 2020
  fase4b_tipologia.png      tipología propuesta por AGEB (D46, pendiente de aprobación)
  fase4b_ghsl.png           superficie construida 1975–2020 (GHSL), m² por habitante y direcciones

Paletas: categórica en el orden fijo de la paleta de referencia (validada: pasa CVD y
visión normal; contraste bajo en 3 tonos, por eso todo lleva leyenda y las tablas están
en data/processed/); secuencial: la rampa azul de 4 clases de las figuras de la fase 4.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
FIG = RAIZ / "docs" / "figuras"

LOCALIDADES = [("0001", "Ciudad de Acámbaro"), ("0027", "Irámuco"), ("0047", "Parácuaro"),
               ("0017", "Chupícuaro (Nuevo Chupícuaro)")]
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
SEQ = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
GRIS, FONDO, TINTA, TINTA2 = "#d9d9d6", "#fcfcfb", "#0b0b0b", "#52514e"
PERIODOS = {"consolidada": "#c9c8c3", "nueva 2010–2020": CAT[1], "nueva posterior a 2020": CAT[0]}
CLASES = {"consolidada estable": CAT[0], "consolidada desatendida": CAT[3], "consolidada y vaciándose": CAT[4],
          "nueva y bien servida": CAT[2], "nueva y desatendida": CAT[1]}
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRIS, "text.color": TINTA, "axes.labelcolor": TINTA2,
                     "xtick.color": TINTA2, "ytick.color": TINTA2, "figure.facecolor": FONDO, "axes.facecolor": FONDO})


def paneles(titulo):
    fig = plt.figure(figsize=(13, 9))
    ax = [fig.add_axes([0.01, 0.04, 0.58, 0.84])] + [fig.add_axes([0.61, 0.04 + i * 0.30, 0.38, 0.24]) for i in (2, 1, 0)]
    fig.suptitle(titulo, x=0.01, ha="left", fontsize=13, fontweight="bold")
    return fig, ax


def anillos(a, cen, rmax):
    for r in range(500, int(rmax) + 500, 500):
        a.add_patch(plt.Circle((cen.x, cen.y), r, fill=False, ls=(0, (2, 3)), lw=0.6, color=TINTA2))
    a.plot(cen.x, cen.y, marker="+", ms=10, mew=1.5, color=TINTA)


def encuadre(a, g, titulo):
    x0, y0, x1, y1 = g.total_bounds
    m = 150
    a.set_xlim(x0 - m, x1 + m)
    a.set_ylim(y0 - m, y1 + m)
    a.set_aspect("equal")
    a.set_axis_off()
    a.set_title(titulo, loc="left", fontsize=10)


def mapa_antiguedad(cu, cen):
    fig, ax = paneles("Antigüedad de las cuadras (criterio D12: nueva = menos de la mitad ya era cuadra)")
    for a, (loc, nom) in zip(ax, LOCALIDADES):
        g = cu[(cu.CVE_LOC == loc) & cu.periodo.isin(PERIODOS)]
        for per, col in PERIODOS.items():
            x = g[g.periodo == per]
            if len(x):
                x.plot(ax=a, color=col, edgecolor=FONDO if per == "consolidada" else TINTA,
                       linewidth=0.2 if per == "consolidada" else 0.8)
        d = np.hypot(g.geometry.centroid.x - cen[loc].x, g.geometry.centroid.y - cen[loc].y).max()
        anillos(a, cen[loc], d)
        n = g.periodo.value_counts()
        encuadre(a, g, f"{nom}\n{n.get('nueva 2010–2020', 0)} cuadras nuevas 2010–2020, "
                        f"{n.get('nueva posterior a 2020', 0)} posteriores a 2020")
    ax[0].legend(handles=[Patch(color=c, label=l) for l, c in PERIODOS.items()] +
                 [plt.Line2D([], [], ls=(0, (2, 3)), color=TINTA2, label="anillos de 500 m desde el centro (+)")],
                 loc="lower right", frameon=True, facecolor=FONDO, edgecolor=GRIS)
    fig.text(0.01, 0.01, "Fuente: Marco Geoestadístico 2010, 2020 y EIC 2025 (INEGI). Provisional: falta la revisión de zonas en imágenes.",
             color=TINTA2, fontsize=8)
    fig.savefig(FIG / "fase4b_antiguedad.png", dpi=150)
    plt.close(fig)


def mapa_deshabitadas(cu, cen):
    fig, ax = paneles("Viviendas no habitadas (deshabitadas + uso temporal), 2020")
    cortes = [20, 30, 40]
    etiquetas = ["menos de 20 %", "20 a 30 %", "30 a 40 %", "40 % o más"]
    g0 = cu[cu.periodo.isin(["consolidada", "nueva 2010–2020"])].copy()
    g0["pct"] = 100 * (g0.VIVTOT - g0.TVIVHAB) / g0.VIVTOT
    for a, (loc, nom) in zip(ax, LOCALIDADES):
        g = g0[g0.CVE_LOC == loc]
        sin = g.pct.isna()
        g[sin].plot(ax=a, color=GRIS, edgecolor=FONDO, linewidth=0.2)
        k = np.digitize(g[~sin].pct, cortes)
        g[~sin].plot(ax=a, color=[SEQ[i] for i in k], edgecolor=FONDO, linewidth=0.2)
        nuevas = g[g.periodo == "nueva 2010–2020"]
        if len(nuevas):
            nuevas.boundary.plot(ax=a, color=CAT[1], linewidth=1.2)
        d = np.hypot(g.geometry.centroid.x - cen[loc].x, g.geometry.centroid.y - cen[loc].y).max()
        anillos(a, cen[loc], d)
        pct = 100 * (g.VIVTOT - g.TVIVHAB).sum() / g.VIVTOT[~sin].sum()
        encuadre(a, g, f"{nom}\n{pct:.0f} % de las viviendas no habitadas")
    ax[0].legend(handles=[Patch(color=c, label=l) for c, l in zip(SEQ, etiquetas)] +
                 [Patch(color=GRIS, label="sin dato (oculto por \"*\" o sin viviendas)"),
                  Patch(facecolor="none", edgecolor=CAT[1], label="cuadra nueva 2010–2020")],
                 loc="lower right", frameon=True, facecolor=FONDO, edgecolor=GRIS)
    fig.text(0.01, 0.01, "Fuente: Censo 2020, resultados por manzana (INEGI). % = (viviendas − habitadas) / viviendas.",
             color=TINTA2, fontsize=8)
    fig.savefig(FIG / "fase4b_deshabitadas.png", dpi=150)
    plt.close(fig)


def mapa_tipologia(cu, cen, tip):
    fig, ax = paneles("Tipología de AGEB propuesta (criterios por aprobar, D46)")
    ag = cu[cu.periodo.isin(PERIODOS)].dissolve(by=["CVE_LOC", "CVE_AGEB"]).reset_index()
    ag = ag.merge(tip[["cve_loc", "cve_ageb", "clase"]], left_on=["CVE_LOC", "CVE_AGEB"], right_on=["cve_loc", "cve_ageb"])
    for a, (loc, nom) in zip(ax, LOCALIDADES):
        g = ag[ag.CVE_LOC == loc]
        g.plot(ax=a, color=g.clase.map(CLASES), edgecolor=FONDO, linewidth=0.8)
        a.plot(cen[loc].x, cen[loc].y, marker="+", ms=10, mew=1.5, color=TINTA)
        n = g.clase.value_counts()
        encuadre(a, g, f"{nom}\n{len(g)} AGEB")
    ax[0].legend(handles=[Patch(color=c, label=l) for l, c in CLASES.items()], loc="lower right", frameon=True, facecolor=FONDO, edgecolor=GRIS)
    fig.text(0.01, 0.01, "Nueva: ≥ 30 % de su superficie es cuadra nueva. Desatendida: ≥ 3 de 5 servicios básicos lejos para más de la mitad. "
             "Vaciándose: % no habitadas en el cuarto más alto de su localidad y menos población que en 2010.",
             color=TINTA2, fontsize=8)
    fig.savefig(FIG / "fase4b_tipologia.png", dpi=150)
    plt.close(fig)


def grafica_ghsl():
    s = pd.read_csv(P / "ghsl_serie.csv")
    sec = pd.read_csv(P / "ghsl_sectores.csv")
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.6), gridspec_kw={"width_ratios": [1.3, 1, 1]})
    fig.suptitle("Expansión de la superficie construida (GHSL 1975–2020)", x=0.01, ha="left", fontsize=13, fontweight="bold")
    # (a) índice 1975 = 100 por zona
    nombres = {"municipio": "Municipio", "loc_0001": "Ciudad de Acámbaro", "loc_0027": "Irámuco",
               "loc_0047": "Parácuaro", "loc_0017": "Chupícuaro"}
    a = ax[0]
    for (z, n), col in zip(nombres.items(), CAT):
        x = s[(s.zona == z) & s.construido_ha.notna()]
        a.plot(x.anio, x.indice_1975_100, color=col, lw=2, marker="o", ms=4, label=n)
        a.annotate(f"{x.indice_1975_100.iloc[-1]:.0f}", (2020, x.indice_1975_100.iloc[-1]), xytext=(4, 0),
                   textcoords="offset points", va="center", fontsize=8, color=TINTA2)
    a.set_title("(a) Superficie construida, índice 1975 = 100", loc="left", fontsize=10)
    a.grid(axis="y", color=GRIS, lw=0.5)
    a.spines[["top", "right"]].set_visible(False)
    a.legend(frameon=False, fontsize=8)
    # (b) m² construidos por habitante, 2010 y 2020
    a = ax[1]
    x = s[s.anio.isin([2010, 2020]) & s.m2_construidos_por_hab.notna()]
    zs = list(nombres)
    w = 0.38
    for i, (anio, col) in enumerate([(2010, "#86b6ef"), (2020, "#1c5cab")]):
        y = [x[(x.zona == z) & (x.anio == anio)].m2_construidos_por_hab.iloc[0] for z in zs]
        b = a.bar(np.arange(len(zs)) + (i - 0.5) * w, y, w - 0.04, color=col, label=str(anio))
        a.bar_label(b, fmt="%.0f", fontsize=7, color=TINTA2)
    a.set_xticks(range(len(zs)), [nombres[z].replace("Ciudad de ", "") for z in zs], fontsize=8)
    a.set_title("(b) m² construidos por habitante", loc="left", fontsize=10)
    a.spines[["top", "right", "left"]].set_visible(False)
    a.set_yticks([])
    a.legend(frameon=False, fontsize=8)
    # (c) dirección del crecimiento de la ciudad
    a = ax[2]
    orden = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    for i, (per, col) in enumerate([("1990–2000", "#86b6ef"), ("2010–2020", "#1c5cab")]):
        y = sec[(sec.tipo == "sector") & (sec.periodo == per)].set_index("clave").reindex(orden).pct_del_periodo
        a.barh(np.arange(8) + (i - 0.5) * w, y, w - 0.04, color=col, label=per)
    a.set_yticks(range(8), orden)
    a.invert_yaxis()
    a.set_xlabel("% de la superficie ganada en el periodo")
    a.set_title("(c) Ciudad: hacia dónde creció", loc="left", fontsize=10)
    a.spines[["top", "right"]].set_visible(False)
    a.legend(frameon=False, fontsize=8)
    fig.text(0.01, 0.01, "Fuente: GHS-BUILT-S R2023A (JRC), celdas de 100 m; población: Censo 2010 y 2020 (ITER). "
             "Localidades: su polígono + 1 km. 2025 y 2030 del GHSL son modelados y no se usan.", color=TINTA2, fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(FIG / "fase4b_ghsl.png", dpi=150)
    plt.close(fig)


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("crec19", RAIZ / "src" / "19_crecimiento.py")
    crec19 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(crec19)
    cu = gpd.read_file(P / "cuadras_antiguedad.gpkg", layer="cuadras")
    cu = cu[cu.geom_type.isin(["Polygon", "MultiPolygon"])]
    cen = crec19.centros(cu.crs)
    tip = pd.read_csv(P / "tipologia_ageb.csv", dtype={"cve_loc": str, "cve_ageb": str})
    mapa_antiguedad(cu, cen)
    mapa_deshabitadas(cu, cen)
    mapa_tipologia(cu, cen, tip)
    grafica_ghsl()


if __name__ == "__main__":
    main()
