"""05 · Mapa de revisión de la fase 1 (docs/figuras/fase1_base.png).

Izquierda: municipio con localidades del ITER 2020 por tamaño.
Derecha: ciudad de Acámbaro con población 2020 por manzana, manzanas que
aparecen en el MG 2020 y no en 2010, y las que aparecen en el MG EIC 2025 y no
en 2020 (criterio de geometría de 03_base_geografica.py).
"""

from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
FIG = RAIZ / "docs" / "figuras"


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    mun = gpd.read_file(P / "mg2020_acambaro.gpkg", layer="municipio")
    locs = gpd.read_file(P / "localidades2020.gpkg").to_crs(mun.crs)
    todas = gpd.read_file(P / "mg2020_acambaro.gpkg", layer="manzanas")
    pob = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="manzanas")
    n25 = gpd.read_file(P / "manzanas_cambios.gpkg", layer="eic2025_vs_2020")
    n20 = gpd.read_file(P / "manzanas_cambios.gpkg", layer="mg2020_vs_2010")
    n25, n20 = n25[n25.geometria_nueva], n20[n20.geometria_nueva & n20.localidad_ya_cartografiada]

    fig, (a, b) = plt.subplots(1, 2, figsize=(15, 7.5))
    mun.plot(ax=a, color="#f4f1ea", edgecolor="#555", lw=0.8)
    todas.plot(ax=a, color="#bbb", lw=0)
    locs.sort_values("POBTOT", ascending=False).plot(
        ax=a, markersize=(locs.POBTOT.clip(lower=1) ** 0.5) * 1.2, color="#1f5f8b", alpha=0.6)
    for _, r in locs.nlargest(6, "POBTOT").iterrows():
        a.annotate(f"{r.NOM_LOC.split(' (')[0]}\n{int(r.POBTOT):,}", (r.geometry.x, r.geometry.y),
                   fontsize=7, xytext=(4, 4), textcoords="offset points")
    a.set_title("Municipio de Acámbaro: 212 localidades (ITER 2020)\ntamaño del círculo ∝ población", fontsize=10)

    ciudad = pob[pob.CVE_LOC == "0001"]
    xmin, ymin, xmax, ymax = ciudad.total_bounds
    pob.plot(ax=b, column="POBTOT", cmap="YlGnBu", scheme=None, vmin=0, vmax=300, lw=0.1, edgecolor="white")
    n20.plot(ax=b, color="none", edgecolor="#e08a00", lw=1.2)
    n25.plot(ax=b, color="#d7301f", edgecolor="#d7301f", lw=1.5)
    b.set_xlim(xmin - 300, xmax + 300)
    b.set_ylim(ymin - 300, ymax + 300)
    b.set_title("Ciudad de Acámbaro: población por manzana (Censo 2020)", fontsize=10)
    b.legend(handles=[
        Patch(facecolor="#2c7fb8", label="Más población por manzana (0–300+)"),
        Line2D([], [], color="#e08a00", lw=2, label="Manzana nueva 2010→2020"),
        Patch(facecolor="#d7301f", label="Manzana nueva después de 2020 (sin población censada)"),
    ], loc="lower left", fontsize=8)
    for ax in (a, b):
        ax.set_axis_off()
    fig.text(0.5, 0.02, "Fuentes: INEGI, Censo 2020 (ITER y AGEB-manzana), Marco Geoestadístico 2010, 2020 y EIC 2025.",
             ha="center", fontsize=8, color="#555")
    fig.savefig(FIG / "fase1_base.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    main()
