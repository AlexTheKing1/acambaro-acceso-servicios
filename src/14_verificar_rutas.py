"""14 · Rutas para comparar con Google Maps (docs/verificar_rutas.csv).

Elige al azar (semilla fija) 5 cuadras habitadas de las 4 localidades urbanas y,
para cada una, una categoría de servicio al azar. Escribe la distancia a pie
calculada por la red de calles hasta el servicio más cercano de esa categoría y
un enlace de Google Maps con la ruta a pie (origen y destino por coordenadas)
para que se compare a mano. Columnas "distancia_google_m" y "notas": vacías la
primera vez; si el archivo ya existe se conserva lo anotado.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
DOCS = RAIZ / "docs"
SEMILLA = 20261023
N = 5
CATEGORIAS = ["preescolar", "primaria", "secundaria", "bachillerato", "salud_publica", "tienda_basica",
              "abasto_completo"]
RUTA = ("https://www.google.com/maps/dir/?api=1&origin={la1:.6f},{lo1:.6f}"
        "&destination={la2:.6f},{lo2:.6f}&travelmode=walking")


def main():
    cu = pd.read_csv(P / "acceso_cuadras.csv", dtype={"CVEGEO": str})
    sedes = pd.read_csv(P / "servicios_sedes_fase4.csv").set_index("id_sede")
    hab = cu[(cu.origen == "cuadra 2020") & (cu.POBTOT > 0)]
    rng = np.random.default_rng(SEMILLA)
    elegidas = hab.iloc[rng.choice(len(hab), N, replace=False)]
    cats = rng.choice(CATEGORIAS, N, replace=False)
    filas = []
    for (_, c), cat in zip(elegidas.iterrows(), cats):
        s = sedes.loc[c[f"id_{cat}"]]
        filas.append({
            "cuadra": c.CVEGEO, "localidad": c.localidad, "categoria": cat,
            "servicio": s.nombre if isinstance(s.nombre, str) else f"({s.subtipo}, sin nombre)",
            "id_servicio": c[f"id_{cat}"],
            "distancia_calculada_m": int(c[f"d_{cat}"]), "como_se_calculo": c[f"via_{cat}"],
            "tramo_de_acceso_m": c.acceso_red_m,
            "origen_lat": c.lat, "origen_lon": c.lon, "destino_lat": s.lat, "destino_lon": s.lon,
            "enlace_ruta_a_pie": RUTA.format(la1=c.lat, lo1=c.lon, la2=s.lat, lo2=s.lon),
            "distancia_google_m": "", "notas": "",
        })
    t = pd.DataFrame(filas)
    # Conserva lo que Alejandro ya anotó (fase 4: distancias de Google Maps)
    ruta = DOCS / "verificar_rutas.csv"
    if ruta.exists():
        prev = pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8-sig")
        prev = prev.set_index(["cuadra", "categoria"])[["distancia_google_m", "notas"]]
        llave = list(zip(t.cuadra, t.categoria))
        for col in ["distancia_google_m", "notas"]:
            t[col] = [prev[col].get(k, "") for k in llave]
    t.to_csv(DOCS / "verificar_rutas.csv", index=False, encoding="utf-8-sig")
    print(t.drop(columns="enlace_ruta_a_pie").to_string())


if __name__ == "__main__":
    main()
