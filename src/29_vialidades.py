"""29 · Escuelas y unidades de salud junto a carreteras (fase 6, ajuste 6; D61).

Se usan los ejes viales del MG EIC 2025 que ya forman la red caminable
(red_peatonal.gpkg). Su atributo TIPOVIAL es el tipo de nombre de la vialidad
(Calle, Avenida, Carretera, Boulevard...), no una jerarquía funcional: por eso
"vialidad primaria" NO se puede medir con estos datos y no se inventa. Lo que sí:
  - junto a carretera: la sede está a <= 50 m (sensibilidad 25 y 100 m) de un
    tramo con TIPOVIAL = "Carretera".
  - junto a avenida o bulevar: igual con TIPOVIAL en {"Avenida", "Boulevard"},
    como dato aparte ("vialidad con nombre de avenida").
Limitación: los ejes del MG solo cubren el interior de las localidades; los tramos
de carretera entre localidades no están, así que una escuela rural sobre la
carretera pero fuera del polígono de su localidad no se detecta.

Sedes: las que cuentan en las medidas del análisis, dentro del municipio:
escuelas de los 4 niveles (todas) y salud pública de primer nivel (con su clase
de 27_salud_abierta.py).

Salida: data/processed/servicios_junto_carretera.csv; clave "vialidades" en
validacion_fase6.json.
"""

import importlib.util
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
spec = importlib.util.spec_from_file_location("acc11", RAIZ / "src" / "11_accesibilidad.py")
acc11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc11)

DIST = (25, 50, 100)
PRINCIPAL = 50
CATS = ["preescolar", "primaria", "secundaria", "bachillerato", "salud_publica"]


def main():
    sedes = gpd.read_file(P / "servicios_fase4.gpkg", layer="sedes")
    tramos = gpd.read_file(P / "red_peatonal.gpkg", layer="tramos")
    sedes = sedes.to_crs(tramos.crs)
    clase = pd.read_csv(P / "salud_clasificacion_instituciones.csv", dtype=str).set_index("id_sede").clase
    partes = []
    for cat in CATS:
        s = sedes[acc11.CATEGORIAS[cat](sedes) & sedes.en_acambaro].copy()
        s["categoria"] = cat
        partes.append(s)
    s = pd.concat(partes, ignore_index=True)
    s["clase_salud"] = s.id_sede.map(clase)
    s["urbana"] = s.cve_loc.isin(acc11.URBANAS)
    for nombre, tipos in {"carretera": {"Carretera"}, "avenida_bulevar": {"Avenida", "Boulevard"}}.items():
        t = tramos[tramos.TIPOVIAL.isin(tipos)]
        j = gpd.sjoin_nearest(s[["geometry"]], t[["TIPOVIAL", "geometry"]], how="left", distance_col="d")
        j = j[~j.index.duplicated()]
        s[f"d_{nombre}_m"] = j.d.round(0)
        for d in DIST:
            s[f"{nombre}_{d}m"] = s[f"d_{nombre}_m"] <= d
    ll = s.to_crs("EPSG:4326")
    cols = ["id_sede", "categoria", "nombre", "localidad", "cve_loc", "urbana", "clase_salud",
            "d_carretera_m", "d_avenida_bulevar_m"] + [f"{n}_{d}m" for n in ("carretera", "avenida_bulevar") for d in DIST]
    s[cols].assign(lat=ll.geometry.y.round(6), lon=ll.geometry.x.round(6)).to_csv(P / "servicios_junto_carretera.csv", index=False)

    resumen = {}
    for cat in CATS:
        c = s[s.categoria == cat]
        resumen[cat] = {"sedes": len(c), **{f"carretera_{d}m": int(c[f"carretera_{d}m"].sum()) for d in DIST},
                        "carretera_50m_urbanas": int(c[c.urbana].carretera_50m.sum()),
                        "carretera_50m_rurales": int(c[~c.urbana].carretera_50m.sum()),
                        "avenida_bulevar_50m": int(c.avenida_bulevar_50m.sum())}
    v = {"tramos_por_tipo_km": (tramos.groupby("TIPOVIAL").longitud.sum() / 1000).round(1).to_dict(),
         "localidades_con_tramos_de_carretera": int(tramos[tramos.TIPOVIAL == "Carretera"].CVE_LOC.nunique()),
         "resumen": resumen,
         "junto_carretera_50m": s[s.carretera_50m][["categoria", "nombre", "localidad", "d_carretera_m"]].to_dict("records"),
         "no_realizable": "vialidad primaria: el MG no trae jerarquía funcional; tramos de carretera fuera de las localidades no están en la red"}
    f = P / "validacion_fase6.json"
    todo = json.loads(f.read_text()) if f.exists() else {}
    todo["vialidades"] = v
    f.write_text(json.dumps(todo, ensure_ascii=False, indent=1, default=str))
    print(json.dumps(v, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
