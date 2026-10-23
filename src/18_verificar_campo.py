"""18 · Lista para verificación de campo (fase 4): docs/verificar_campo.csv.

Incluye, dentro del municipio:
  - los servicios que Alejandro marcó "no" o "no se ve" en la verificación remota
    (salvo el consultorio del CERESO, ya resuelto: D38);
  - las dos UMAPS de Irámuco (salud_primer_nivel-0096 del DENUE y -0021 del MG,
    probablemente la misma clínica: la vieja se cambió a un edificio nuevo);
  - 5 servicios marcados "si", elegidos al azar con semilla fija, para medir cuánto
    se equivoca la verificación con Google.
Se agrupan en salidas por cercanía (agrupamiento jerárquico, corte a DIST_SALIDA)
y dentro de cada salida se ordenan por vecino más cercano desde el centro de la
ciudad, para recorrerlos en pocas salidas.
"""

import importlib.util
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
DOCS = RAIZ / "docs"

spec = importlib.util.spec_from_file_location("acc11", RAIZ / "src" / "11_accesibilidad.py")
acc11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc11)

SEMILLA = 2026
N_CONTROL = 5
DIST_SALIDA = 10000          # m, corte del agrupamiento (enlace completo: diámetro máximo de una salida)
IRAMUCO = ["salud_primer_nivel-0096", "salud_primer_nivel-0021"]
RESUELTOS = {"salud_primer_nivel-0093": "CERESO (D38)"}
CENTRO = (20.031, -100.722)     # jardín principal de Acámbaro, aprox.
ENLACE = "https://www.google.com/maps/search/?api=1&query={lat:.6f},{lon:.6f}"
PRINCIPALES = ["preescolar", "primaria", "secundaria", "bachillerato", "salud_publica", "tienda_basica",
               "abasto_completo"]


def main():
    s = gpd.read_file(P / "servicios_fase4.gpkg", layer="sedes")
    mun = s[s.en_acambaro.astype(bool)].copy()
    usa = pd.Series(False, index=mun.index)
    for cat in PRINCIPALES:
        usa |= acc11.CATEGORIAS[cat](mun)

    dudosos = mun[mun.existe_en_imagen.isin(["no", "no se ve"]) & ~mun.id_sede.isin(RESUELTOS)].copy()
    dudosos["motivo"] = "verificación remota: " + dudosos.existe_en_imagen
    ira = mun[mun.id_sede.isin(IRAMUCO)].copy()
    ira["motivo"] = "UMAPS de Irámuco: ¿una o dos clínicas? (DENUE la registra; MG dibuja otra a ~300 m)"
    si = mun[(mun.existe_en_imagen == "si") & ~mun.id_sede.isin(IRAMUCO)]
    control = si.sample(N_CONTROL, random_state=SEMILLA).copy()
    control["motivo"] = "control: marcado 'si' en la verificación remota (al azar, semilla 2026)"
    t = pd.concat([dudosos, ira, control])
    assert t.id_sede.is_unique

    xy = np.c_[t.geometry.x, t.geometry.y]
    t["salida"] = fcluster(linkage(xy, method="complete"), DIST_SALIDA, criterion="distance")
    centro = gpd.GeoSeries(gpd.points_from_xy([CENTRO[1]], [CENTRO[0]]), crs=4326).to_crs(t.crs).iloc[0]
    # Salidas numeradas de la más cercana a la más lejana del centro
    dist_c = t.geometry.distance(centro).groupby(t.salida).min().sort_values()
    t["salida"] = t.salida.map({k: i + 1 for i, k in enumerate(dist_c.index)})
    orden = []
    for _, g in t.groupby("salida"):
        actual, quedan = centro, list(g.index)
        while quedan:
            j = min(quedan, key=lambda i: g.geometry[i].distance(actual))
            orden.append(j)
            actual = g.geometry[j]
            quedan.remove(j)
    t = t.loc[orden]
    t["orden"] = t.groupby("salida").cumcount() + 1

    ll = t.to_crs("EPSG:4326")
    out = pd.DataFrame({
        "salida": t.salida, "orden": t.orden, "id": t.id_sede, "tipo": t.tipo, "nombre": t.nombre,
        "localidad": t.localidad, "motivo": t.motivo,
        "se_usa_en_la_medida": usa.reindex(t.index).map({True: "sí", False: "no"}),
        "estado_sep_clues": t.estado_cruce, "remoto_existe": t.existe_en_imagen, "remoto_visto_en": t.visto_en,
        "remoto_notas": t.notas_verificacion,
        "lat": ll.geometry.y.round(6), "lon": ll.geometry.x.round(6),
        "enlace_google_maps": [ENLACE.format(lat=p.y, lon=p.x) for p in ll.geometry],
        "existe_campo": "", "fecha_visita": "", "foto": "", "notas": ""})
    out.to_csv(DOCS / "verificar_campo.csv", index=False, encoding="utf-8-sig")
    print(out.groupby("salida").agg(n=("id", "size"), localidades=("localidad", lambda x: ", ".join(sorted(set(x.dropna())))))
          .to_string())
    print(out.motivo.str.split(":").str[0].value_counts().to_string())


if __name__ == "__main__":
    main()
