"""28 · Localidades de 2 500 habitantes o más y polos de desarrollo del Plan Municipal (fase 6; D59, D60).

Ajuste 3: la norma (SEDESOL 1999, tomo Salud) prevé un centro de salud rural por
localidad de 2 500 a 10 000 habitantes. Para cada localidad con >= 2 500 hab. en
2020: ¿tiene dentro un centro de salud abierto (27_salud_abierta.py)? ¿tiene
secundaria (incluye general, técnica y telesecundaria)?

Ajuste 9: el Plan Municipal de Desarrollo Acámbaro 2030 (p. 254–255) se fija como
meta que cada polo de desarrollo rural tenga escuelas de preescolar a media
superior, plaza de comercio y abasto, y centro de salud. Polos = los 8 "ejes de
desarrollo" (micro regiones) del plan (p. 53–83); sede = la localidad que da
nombre al eje (D60). Se evalúan los 7 rurales; la ciudad va como referencia.

"Dentro de la localidad" (D59): sede del catálogo de la fase 4 en el municipio,
con clave de localidad igual a la de la localidad y que no esté dada de baja.
Si no hay: distancia al más cercano desde el punto ITER 2020 de la localidad,
línea recta × 1.33 (como en lo rural, D26); para las 4 urbanas se añade la mediana
por persona de la distancia a pie por calles (acceso_cuadras.csv /
acceso_salud_abierta.csv).

Tianguis: ninguna fuente los registra (D35). Si no hay mercado registrado, la
casilla de abasto queda "no verificable", no "no".

Salidas: data/processed/localidades_2500.csv, data/processed/polos_desarrollo.csv,
clave "localidades_y_polos" en validacion_fase6.json.
"""

import importlib.util
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
spec = importlib.util.spec_from_file_location("acc11", RAIZ / "src" / "11_accesibilidad.py")
acc11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc11)
FACTOR = acc11.FACTOR_FIJO

# Polos (Plan Municipal, cap. 4: p. 53, 58, 63, 67, 72, 76, 79, 83)
POLOS = [
    ("4.1 Zona Urbana y Conurbana", "0001", 53, True),
    ("4.2 Irámuco", "0027", 58, False),
    ("4.3 Parácuaro", "0047", 63, False),
    ("4.4 Chupícuaro", "0017", 67, False),
    ("4.5 Chamácuaro", "0015", 72, False),
    ("4.6 San Mateo Tócuaro", "0092", 76, False),
    ("4.7 Arroyo de la Luna", "0006", 79, False),
    ("4.8 Inchamácuaro", "0026", 83, False),
]
SERVICIOS = {   # columna -> (filtro sobre las sedes, columna de distancia urbana en las tablas de acceso)
    "preescolar": (lambda s: s.tipo == "preescolar", "d_preescolar"),
    "primaria": (lambda s: s.tipo == "primaria", "d_primaria"),
    "secundaria": (lambda s: s.tipo == "secundaria", "d_secundaria"),
    "bachillerato": (lambda s: s.tipo == "bachillerato", "d_bachillerato"),
    "salud_abierta": (None, "d_salud_abierta"),
    "mercado": (lambda s: (s.tipo == "abasto") & (s.subtipo == "mercado"), None),
}


def mediana_ponderada(d, w):
    o = np.argsort(d)
    d, w = np.asarray(d)[o], np.asarray(w)[o]
    c = np.cumsum(w)
    return float(d[np.searchsorted(c, c[-1] / 2)]) if c[-1] else np.nan


def main():
    sedes = gpd.read_file(P / "servicios_fase4.gpkg", layer="sedes")
    crs = sedes.crs
    sedes = sedes[~sedes.estado_cruce.str.startswith(("baja", "descartada"))]
    abiertas = pd.read_csv(P / "salud_clasificacion_instituciones.csv", dtype=str)
    ids_abiertas = set(abiertas[abiertas.clase.isin(["abierta", "abierta_umr"])].id_sede)
    filtros = {k: (f if f else (lambda s: s.id_sede.isin(ids_abiertas))) for k, (f, _) in SERVICIOS.items()}

    loc = gpd.read_file(P / "localidades2020.gpkg").to_crs(crs)
    assert (loc.geometry.geom_type == "Point").all()
    cu = pd.read_csv(P / "acceso_cuadras.csv", dtype={"CVE_LOC": str})
    sa = pd.read_csv(P / "acceso_salud_abierta.csv", dtype={"CVE_LOC": str}, low_memory=False)
    sa = sa[sa.escala == "ciudad"].reset_index(drop=True)
    assert len(sa) == len(cu)
    cu["d_salud_abierta"] = sa.d_salud_abierta.to_numpy()
    cu = cu[cu.origen != "cuadra nueva posterior a 2020"]

    def evaluar(cve):
        fila = loc[loc.LOC == cve].iloc[0]
        r = {"cve_loc": cve, "localidad": fila.NOM_LOC, "pob_2020": int(fila.POBTOT)}
        for k, f in filtros.items():
            s = sedes[f(sedes)]
            dentro = s[s.en_acambaro & (s.cve_loc == cve)]
            r[f"{k}_dentro"] = "sí" if len(dentro) else "no"
            r[f"{k}_n"] = len(dentro)
            r[f"{k}_ids"] = ";".join(dentro.id_sede)
            if len(dentro):
                r[f"{k}_dist_m"] = 0
                continue
            d = s.geometry.distance(fila.geometry)
            j = d.idxmin()
            r[f"{k}_dist_m"] = round(float(d[j]) * FACTOR, -1)
            r[f"{k}_mas_cercano"] = f"{s.loc[j, 'nombre'] or s.loc[j, 'subtipo']} ({s.loc[j, 'localidad'] or s.loc[j, 'municipio']}; {s.loc[j, 'id_sede']})"
            col = SERVICIOS[k][1]
            if col and cve in acc11.URBANAS:
                c = cu[cu.CVE_LOC == cve]
                r[f"{k}_mediana_por_persona_a_pie_m"] = round(mediana_ponderada(c[col], c.POBTOT.fillna(0)), -1)
        return r

    # --- Ajuste 3 ------------------------------------------------------------------------
    grandes = loc[(loc.POBTOT >= 2500) & (loc.LOC != "0000")].sort_values("POBTOT", ascending=False)
    t3 = pd.DataFrame([evaluar(c) for c in grandes.LOC])
    cols3 = ["cve_loc", "localidad", "pob_2020", "salud_abierta_dentro", "salud_abierta_n", "salud_abierta_dist_m",
             "salud_abierta_mas_cercano", "secundaria_dentro", "secundaria_n", "secundaria_dist_m",
             "secundaria_mas_cercano", "secundaria_mediana_por_persona_a_pie_m", "salud_abierta_ids", "secundaria_ids"]
    t3 = t3.reindex(columns=cols3)
    t3["norma"] = np.where(t3.pob_2020 <= 10000, "SEDESOL 1999: 1 centro de salud rural por localidad de 2 500 a 10 000 hab.",
                           "más de 10 000 hab.: aplica el centro de salud urbano")
    t3.to_csv(P / "localidades_2500.csv", index=False)

    # --- Ajuste 9 ------------------------------------------------------------------------
    filas = []
    for eje, cve, pag, ref in POLOS:
        r = {"eje_de_desarrollo": eje, "pagina_plan": pag, "solo_referencia": ref, **evaluar(cve)}
        req = ["preescolar", "primaria", "secundaria", "bachillerato", "salud_abierta"]
        falta = [k for k in req if r[f"{k}_dentro"] == "no"]
        if r["mercado_dentro"] == "no":
            r["mercado_dentro"] = "no verificable (sin mercado registrado; puede haber tianguis)"
        if ref:
            r["cumple_meta_plan"] = "referencia (no se evalúa)"
        elif falta:
            r["cumple_meta_plan"] = "no (falta: " + ", ".join(falta) + ")"
        elif r["mercado_dentro"] != "sí":
            r["cumple_meta_plan"] = "no verificable (escuelas y salud sí; abasto sin registro)"
        else:
            r["cumple_meta_plan"] = "sí"
        filas.append(r)
    t9 = pd.DataFrame(filas)
    base = ["eje_de_desarrollo", "pagina_plan", "cve_loc", "localidad", "pob_2020", "solo_referencia"]
    serv = [c for k in SERVICIOS for c in (f"{k}_dentro", f"{k}_n", f"{k}_dist_m", f"{k}_mas_cercano")]
    t9 = t9.reindex(columns=base + serv + ["cumple_meta_plan"] + [f"{k}_ids" for k in SERVICIOS])
    t9.to_csv(P / "polos_desarrollo.csv", index=False)

    f = P / "validacion_fase6.json"
    todo = json.loads(f.read_text()) if f.exists() else {}
    todo["localidades_y_polos"] = {
        "localidades_2500": t3[["localidad", "pob_2020", "salud_abierta_dentro", "secundaria_dentro",
                                "secundaria_dist_m"]].to_dict("records"),
        "polos": t9[["localidad", "cumple_meta_plan"]].to_dict("records"),
        "control_cada_si_tiene_id": bool(all(((t9[f"{k}_n"] > 0) == t9[f"{k}_ids"].fillna("").ne("")).all() for k in SERVICIOS)),
    }
    f.write_text(json.dumps(todo, ensure_ascii=False, indent=1, default=str))
    pd.set_option("display.width", 250)
    print(t3.drop(columns=["salud_abierta_ids", "secundaria_ids", "norma"]).to_string())
    print(t9[base[2:5] + [f"{k}_dentro" for k in SERVICIOS] + ["cumple_meta_plan"]].to_string())
    print(t9[[c for c in t9.columns if c.endswith("_dist_m") or c.endswith("mas_cercano")]].to_string())


if __name__ == "__main__":
    main()
