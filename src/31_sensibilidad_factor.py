"""31 · Sensibilidad del factor de rodeo rural (fase 8; revisión final, observación c3).

Lo rural se mide en línea recta × 1.33 (D26, D33). Este script recalcula la
población rural lejos con otros factores (1.0, 1.2, 1.33, 1.5) para que los
textos den un rango en lugar de una sola cifra. No cambia ninguna salida
anterior: parte de las distancias ya calculadas (distancia ÷ 1.33 = línea recta).

También deja el caso de Parácuaro, el único con una distancia por carretera
verificada (D68): la Secundaria Técnica 24, 4.9 km por carretera según Google
Maps (Alejandro, fase 8), contra la estimación línea recta × 1.33.

Entradas: acceso_localidades.csv (11), acceso_salud_abierta.csv (27),
          polos_desarrollo.csv (28), servicios_sedes_fase4.csv, localidades2020.csv
Salidas:  data/processed/sensibilidad_factor_rural.csv
          data/processed/validacion_fase8.json, clave "factor_rural"
"""

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"


def _modulo(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "src" / archivo)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


acc11 = _modulo("acc11", "11_accesibilidad.py")
FACTOR = acc11.FACTOR_FIJO
FACTORES = [1.0, 1.2, 1.33, 1.5]
CATEGORIAS = ["preescolar", "primaria", "secundaria", "bachillerato", "salud_abierta", "abasto_completo"]
ST24_CARRETERA_M = 4900          # Google Maps, Alejandro (fase 8, D68)
ST24_RECTA_GMAPS_M = 4340        # herramienta "Medir distancia", Alejandro


def distancia_m(lat1, lon1, lat2, lon2):
    """Gran círculo (m). Solo para el control de Parácuaro."""
    a = np.sin(np.radians(lat2 - lat1) / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) \
        * np.sin(np.radians(lon2 - lon1) / 2) ** 2
    return 6371000 * 2 * np.arcsin(np.sqrt(a))


def main():
    loc = pd.read_csv(P / "acceso_localidades.csv", dtype={"LOC": str})
    sa = pd.read_csv(P / "acceso_salud_abierta.csv", dtype={"CVE_LOC": str})
    sa = sa[sa.escala == "rural"].set_index("CVE_LOC").d_salud_abierta
    loc["d_salud_abierta"] = loc.LOC.map(sa)
    assert loc.d_salud_abierta.notna().all()
    pob_total = loc.POBTOT.sum()
    cat_umbral = {c: acc11.UMBRALES_RURAL["salud_publica" if c == "salud_abierta" else c] for c in CATEGORIAS}

    filas = []
    for cat in CATEGORIAS:
        recta = loc[f"d_{cat}"] / FACTOR
        for nivel, umbral in zip(acc11.NIVELES, cat_umbral[cat]):
            for f in FACTORES:
                lejos = recta * f > umbral
                filas.append({"categoria": cat, "umbral": nivel, "umbral_m": umbral, "factor": f,
                              "pob_lejos": int(loc.POBTOT[lejos].sum()), "pob_total": int(pob_total),
                              "pct_lejos": round(100 * loc.POBTOT[lejos].sum() / pob_total, 1),
                              "localidades_lejos": int(lejos.sum())})
    t = pd.DataFrame(filas)
    # Control: con 1.33 debe dar lo mismo que 11 / 27 (umbral principal)
    ref = pd.read_csv(P / "acceso_resumen_por_localidad.csv")
    ref = ref[(ref.localidad == "Localidades rurales (208)") & (ref.variable == "POBTOT")]
    for cat in CATEGORIAS:
        if cat == "salud_abierta":
            continue
        for nivel in acc11.NIVELES:
            mio = t[(t.categoria == cat) & (t.umbral == nivel) & (t.factor == FACTOR)].pob_lejos.iloc[0]
            r = ref[(ref.categoria == cat) & (ref.umbral == nivel)].pob_lejos.iloc[0]
            assert abs(mio - r) < 1, (cat, nivel, mio, r)
    t.to_csv(P / "sensibilidad_factor_rural.csv", index=False)

    # Parácuaro: estimación del método contra lo verificado
    sedes = pd.read_csv(P / "servicios_sedes_fase4.csv", dtype=str)
    st24 = sedes[sedes.id_sede == "secundaria-S0002"].iloc[0]
    tv847 = sedes[sedes.id_sede == "secundaria-0015"].iloc[0]
    l20 = pd.read_csv(P / "localidades2020.csv", dtype=str)
    par = l20[l20.LOC == "0047"].iloc[0]
    rec = lambda s: float(distancia_m(float(par.lat), float(par.lon), float(s.lat), float(s.lon)))
    r24, r847 = rec(st24), rec(tv847)
    v = {"factores": FACTORES,
         "principal": {cat: {str(f): [int(x.pob_lejos), float(x.pct_lejos)]
                             for f, x in t[(t.categoria == cat) & (t.umbral == "principal")].set_index("factor").iterrows()}
                       for cat in CATEGORIAS},
         "paracuaro": {"st24_clave": st24.claves_sep_clues, "st24_lat_lon_catalogo": [float(st24.lat), float(st24.lon)],
                       "st24_lat_lon_google_maps": [20.116199, -100.734521],
                       "st24_distancia_entre_puntos_m": round(distancia_m(float(st24.lat), float(st24.lon), 20.116199, -100.734521)),
                       "recta_centro_st24_m": round(r24), "recta_centro_tv847_m": round(r847),
                       "recta_google_maps_m": ST24_RECTA_GMAPS_M,
                       "estimado_st24_m": round(r24 * FACTOR), "carretera_google_maps_m": ST24_CARRETERA_M,
                       "factor_real": round(ST24_CARRETERA_M / r24, 2),
                       "sobreestimacion_m": round(r24 * FACTOR - ST24_CARRETERA_M),
                       "sobreestimacion_pct": round(100 * (r24 * FACTOR / ST24_CARRETERA_M - 1), 1)}}
    f = P / "validacion_fase8.json"
    todo = json.loads(f.read_text()) if f.exists() else {}
    todo["factor_rural"] = v
    f.write_text(json.dumps(todo, ensure_ascii=False, indent=1))
    print(t[t.umbral == "principal"].pivot_table(index="categoria", columns="factor", values="pct_lejos").to_string())
    print(json.dumps(v["paracuaro"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
