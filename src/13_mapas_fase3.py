"""13 · Mapas de accesibilidad por categoría (docs/figuras/fase4_<categoria>.png).

(En la fase 3 este script generó docs/figuras/fase3_*.png con los umbrales
provisionales; esas figuras se conservan como registro.)

Cada mapa tiene: la ciudad de Acámbaro (grande), Irámuco, Parácuaro y
Chupícuaro (pequeños) con cada cuadra coloreada según la distancia a pie al
servicio más cercano, en 4 clases definidas por los 3 umbrales (estricto,
principal = definitivo, holgado; D33); y el municipio con cada localidad rural como un punto del
mismo color (tamaño = población 2020). Los servicios van en negro.

Paleta: una sola tonalidad de azul, de claro (cerca) a oscuro (lejos); validada
con el validador de paletas ordinales (pasa todos los chequeos sobre fondo claro).
"""

import importlib.util
from pathlib import Path

import geopandas as gpd
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
FIG = RAIZ / "docs" / "figuras"

spec = importlib.util.spec_from_file_location("acc11", RAIZ / "src" / "11_accesibilidad.py")
acc11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc11)

CLASES = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]   # cerca -> lejos
SIN_DATO = "#d9d9d6"
MAPAS = ["preescolar", "primaria", "secundaria", "bachillerato", "salud_publica", "tienda_basica",
         "abasto_completo", "consultorio_privado"]
APARTE = {"bachillerato": ["bachillerato_no_escolarizado"],
          "salud_publica": ["consultorio_privado", "unidad_movil", "casa_de_salud"]}
LOCALIDADES = [("0001", "Ciudad de Acámbaro"), ("0027", "Irámuco"), ("0047", "Parácuaro"),
               ("0017", "Chupícuaro (Nuevo Chupícuaro)")]


def clase(d, u):
    return np.select([d <= u[0], d <= u[1], d <= u[2], d > u[2]], [0, 1, 2, 3], default=-1)


def etiquetas(u, unidad):
    f = (lambda x: f"{x / 1000:g} km") if unidad == "km" else (lambda x: f"{x:,.0f} m".replace(",", " "))
    return [f"hasta {f(u[0])} (estricto)", f"{f(u[0])} a {f(u[1])} (principal)",
            f"{f(u[1])} a {f(u[2])} (holgado)", f"más de {f(u[2])}"]


def main():
    cu = gpd.read_file(P / "acceso_cuadras.gpkg", layer="cuadras")
    loc = pd.read_csv(P / "acceso_localidades.csv", dtype={"LOC": str})
    rur = gpd.GeoDataFrame(loc, geometry=gpd.points_from_xy(loc.lon, loc.lat), crs=4326).to_crs(cu.crs)
    sedes = gpd.read_file(P / "servicios_fase4.gpkg", layer="sedes").to_crs(cu.crs)
    mun = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="municipio").to_crs(cu.crs)
    mza25 = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="manzanas").to_crs(cu.crs)

    for cat in MAPAS:
        uc = acc11.umbral(cat, acc11.UMBRALES_CIUDAD)
        ur = acc11.umbral(cat, acc11.UMBRALES_RURAL)
        s = sedes[acc11.CATEGORIAS[cat](sedes)]
        aparte = sedes[(sedes.tipo.isin(APARTE.get(cat, []))
                        | ((cat == "salud_publica") & sedes.anexo_salud_sin_clues.fillna(False).astype(bool)))
                       & ~sedes.estado_cruce.str.startswith(("baja", "descartada"))]
        cu["k"] = clase(cu[f"d_{cat}"].to_numpy(), uc)

        fig = plt.figure(figsize=(16, 10.5))
        gs = fig.add_gridspec(3, 4, width_ratios=[1, 1, 0.8, 1.15], wspace=0.05, hspace=0.12)
        ejes = [fig.add_subplot(gs[:, :2]), fig.add_subplot(gs[0, 2]), fig.add_subplot(gs[1, 2]),
                fig.add_subplot(gs[2, 2])]
        for ax, (cl, nombre) in zip(ejes, LOCALIDADES):
            c = cu[cu.CVE_LOC == cl]
            for k in range(4):
                c[c.k == k].plot(ax=ax, color=CLASES[k], edgecolor="white", lw=0.25, markersize=10)  # caserío: puntos
            xmin, ymin, xmax, ymax = c.total_bounds
            pad = 150 if cl != "0001" else 250
            caja = (xmin - pad, ymin - pad, xmax + pad, ymax + pad)
            visibles = s.cx[caja[0]:caja[2], caja[1]:caja[3]]
            tam = 7 if cat == "tienda_basica" else 26
            visibles.plot(ax=ax, color="#111", markersize=tam if cl == "0001" else tam * 0.7,
                          marker="o", edgecolor="white", lw=0.4, zorder=4)
            if len(aparte):
                aparte.cx[caja[0]:caja[2], caja[1]:caja[3]].plot(
                    ax=ax, facecolor="none", edgecolor="#111", marker="D", markersize=30, lw=0.9, zorder=5)
            ax.set_xlim(caja[0], caja[2])
            ax.set_ylim(caja[1], caja[3])
            ax.set_axis_off()
            ax.set_title(nombre, fontsize=10 if cl != "0001" else 12, loc="left")

        ax = fig.add_subplot(gs[:, 3])
        mun.plot(ax=ax, color="#f4f3f0", edgecolor="#777", lw=0.7)
        mza25.plot(ax=ax, color="#cfcfcb", lw=0)
        medible = cat not in acc11.NO_MEDIBLE_RURAL
        if medible:
            rur["k"] = clase(rur[f"d_{cat}"].to_numpy(), ur)
            for k in range(4):
                r = rur[rur.k == k]
                r.plot(ax=ax, color=CLASES[k], markersize=6 + np.sqrt(r.POBTOT.fillna(0)) * 1.6,
                       edgecolor="white", lw=0.4, zorder=3)
            sm = s.cx[mun.total_bounds[0] - 3000:mun.total_bounds[2] + 3000,
                      mun.total_bounds[1] - 3000:mun.total_bounds[3] + 3000]
            sm.plot(ax=ax, color="#333", markersize=1.5, marker="o", zorder=4)
            titulo = ("Localidades rurales (tamaño = población 2020)\n"
                      "distancia estimada: línea recta × 1.33")
            if cat in acc11.NOTA_RURAL:
                titulo += "\n(" + acc11.NOTA_RURAL[cat] + ")"
        else:
            rur.plot(ax=ax, color=SIN_DATO, markersize=8, zorder=3)
            titulo = "Localidades rurales: no se puede medir\n(" + acc11.NO_MEDIBLE_RURAL[cat] + ")"
        xmin, ymin, xmax, ymax = mun.total_bounds
        ax.set_xlim(xmin - 2500, xmax + 2500)
        ax.set_ylim(ymin - 2500, ymax + 2500)
        ax.set_axis_off()
        ax.set_title(titulo, fontsize=10, loc="left")

        h = [Patch(color=CLASES[k], label=t) for k, t in enumerate(etiquetas(uc, "m"))]
        h.append(Line2D([], [], marker="o", ls="", color="#111", label=acc11.NOMBRES[cat]))
        if len(aparte):
            nom = {"bachillerato_no_escolarizado": "bachillerato no escolarizado (no cuenta)",
                   "consultorio_privado": "consultorio privado, unidad móvil, casa de salud o\nunidad sin CLUES (anexo; no cuentan)"}
            h.append(Line2D([], [], marker="D", ls="", markerfacecolor="none", color="#111",
                            label=nom.get(APARTE[cat][0], "registrado aparte")))
        fig.legend(handles=h, title="Distancia a pie por calles (cuadras)", loc="lower left",
                   bbox_to_anchor=(0.03, 0.02), fontsize=9, title_fontsize=9, frameon=False)
        if medible:
            hr = [Patch(color=CLASES[k], label=t) for k, t in enumerate(etiquetas(ur, "km"))]
            fig.legend(handles=hr, title="Localidades rurales", loc="lower right",
                       bbox_to_anchor=(0.99, 0.02), fontsize=9, title_fontsize=9, frameon=False)
        fig.suptitle(f"{acc11.NOMBRES[cat]}: distancia al servicio más cercano", x=0.03, ha="left",
                     fontsize=14, y=0.97)
        fig.text(0.03, 0.935, "Lejos = más allá del umbral principal (radio SNEU × 1.33); estricto y holgado son sensibilidad. "
                 "Población: Censo 2020. "
                 "Servicios: MG EIC 2025, DENUE 05/2026, SEP, CLUES 08/2026.", fontsize=9, color="#555")
        fig.savefig(FIG / f"fase4_{cat}.png", dpi=130, bbox_inches="tight")
        plt.close(fig)
        print("mapa", cat)


if __name__ == "__main__":
    main()
