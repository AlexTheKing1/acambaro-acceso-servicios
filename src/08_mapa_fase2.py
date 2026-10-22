"""08 · Mapa de revisión de la fase 2 (docs/figuras/fase2_servicios.png).

Izquierda: municipio y franja de 10 km con escuelas y salud del catálogo,
coloreadas según la fuente que las registra (MG, DENUE o ambas).
Derecha: ciudad de Acámbaro con los mismos servicios más el abasto.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
FIG = RAIZ / "docs" / "figuras"

COLOR_FUENTE = {"MG+DENUE": "#1b7837", "MG": "#2166ac", "DENUE": "#d6604d"}
MARCA_TIPO = {"preescolar": "o", "primaria": "s", "secundaria": "^", "bachillerato": "D",
              "salud_primer_nivel": "P"}
NOMBRE_TIPO = {"preescolar": "Preescolar", "primaria": "Primaria", "secundaria": "Secundaria",
               "bachillerato": "Bachillerato", "salud_primer_nivel": "Salud de primer nivel"}


def puntos(ax, sedes, tam):
    for tipo, marca in MARCA_TIPO.items():
        for fuente, color in COLOR_FUENTE.items():
            s = sedes[(sedes.tipo == tipo) & (sedes.fuentes == fuente)]
            if len(s):
                s.plot(ax=ax, marker=marca, color=color, markersize=tam, edgecolor="white", lw=0.3, zorder=3)


def main():
    mun = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="municipio")
    mza = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="manzanas")
    sedes = gpd.read_file(P / "servicios.gpkg", layer="sedes")
    analizadas = sedes[sedes.analizado & (sedes.tipo != "abasto")]
    abasto = sedes[sedes.tipo == "abasto"]

    fig, (a, b) = plt.subplots(1, 2, figsize=(15, 7.5))
    franja = mun.buffer(10_000)
    gpd.GeoSeries(franja).plot(ax=a, color="#f7f7f7", edgecolor="#999", lw=0.6, ls="--")
    mun.plot(ax=a, color="#f4f1ea", edgecolor="#555", lw=0.8)
    mza.plot(ax=a, color="#bbb", lw=0)
    puntos(a, analizadas, 10)
    a.set_title("Escuelas y salud de primer nivel en el municipio y a 10 km\n"
                "(color = fuente que la registra)", fontsize=10)

    ciudad = mza[mza.CVE_LOC == "0001"]
    xmin, ymin, xmax, ymax = ciudad.total_bounds
    mza.plot(ax=b, color="#e5e5e5", edgecolor="white", lw=0.2)
    abasto[abasto.subtipo != "mercado"].plot(ax=b, color="#888", markersize=2, zorder=2)
    abasto[abasto.subtipo.str.contains("mercado")].plot(ax=b, color="#7b3294", marker="*", markersize=120,
                                                         edgecolor="white", zorder=4)
    puntos(b, analizadas, 30)
    b.set_xlim(xmin - 300, xmax + 300)
    b.set_ylim(ymin - 300, ymax + 300)
    b.set_title("Ciudad de Acámbaro: escuelas, salud y abasto", fontsize=10)

    leyenda = [Line2D([], [], marker="o", ls="", color=c, label=f"Fuente: {f}") for f, c in COLOR_FUENTE.items()]
    leyenda += [Line2D([], [], marker=m, ls="", color="#444", label=NOMBRE_TIPO[t]) for t, m in MARCA_TIPO.items()]
    leyenda += [Line2D([], [], marker="*", ls="", color="#7b3294", markersize=12, label="Mercado"),
                Line2D([], [], marker="o", ls="", color="#888", markersize=3, label="Abarrotes, minisúper, supermercado")]
    b.legend(handles=leyenda, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, frameon=False)
    for ax in (a, b):
        ax.set_axis_off()
    fig.text(0.5, 0.02, "Fuentes: INEGI, Marco Geoestadístico EIC 2025 (servicios) y DENUE 05/2026. "
             "Faltan CLUES (salud) y catálogo SEP (escuelas).", ha="center", fontsize=8, color="#555")
    fig.savefig(FIG / "fase2_servicios.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    main()
