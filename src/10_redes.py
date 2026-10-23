"""10 · Red de calles para caminar (fase 3, paso 2).

Arma una red con los ejes viales del Marco Geoestadístico EIC 2025 (capa
"vialidades" del municipio; incluye calles, andadores, privadas, peatonales y
tramos de carretera dentro de las localidades) y revisa que esté conectada.

Cómo se arma:
  - Cada eje se parte en tramos entre vértices consecutivos; los vértices que
    coinciden (redondeados a 0.5 m) son el mismo nodo. Se ignora el sentido de
    circulación: a pie se puede ir en ambos sentidos.
  - Calles "cortadas" por el dibujo: un extremo suelto (nodo de grado 1) que queda
    a menos de TOL_CORTE m de otro tramo que no es el suyo se une a ese tramo con
    un segmento recto (el tramo se parte en el punto más cercano). Pasa cuando una
    calle termina en "T" sobre otra pero el dibujo no tiene ahí un vértice, o
    cuando le faltan unos metros para tocarla.
  - Después se cuentan los componentes (pedazos de red sin conexión entre sí) y,
    para las 4 localidades urbanas, cuántas cuadras y personas quedan en cada uno.

Salidas:
  data/processed/red_peatonal.gpkg   capa "tramos" (u, v, longitud, componente,
                                      es_union) y capa "uniones" (los segmentos agregados)
  data/processed/validacion_fase3_red.json
"""

import json
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
from shapely import STRtree
from shapely.geometry import LineString, Point

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"

REDONDEO = 0.5     # m: vértices a menos de esto son el mismo nodo
TOL_CORTE = 15     # m: un extremo suelto a menos de esto de otro tramo se une a él
URBANAS = {"0001": "Acámbaro", "0027": "Irámuco", "0047": "Parácuaro", "0017": "Chupícuaro (Nuevo Chupícuaro)"}


def clave(x, y):
    return (round(x / REDONDEO) * REDONDEO, round(y / REDONDEO) * REDONDEO)


def tramos_de(vial):
    """Tramos entre vértices consecutivos. Devuelve DataFrame u, v, x/y y eje de origen."""
    filas = []
    for i, geom in zip(vial.index, vial.geometry.explode(index_parts=False).groupby(level=0).agg(list)):
        for linea in geom:
            c = np.asarray(linea.coords)[:, :2]
            for (x1, y1), (x2, y2) in zip(c[:-1], c[1:]):
                a, b = clave(x1, y1), clave(x2, y2)
                if a != b:
                    filas.append((a, b, i))
    t = pd.DataFrame(filas, columns=["a", "b", "eje"])
    # Un mismo tramo dibujado dos veces cuenta una sola
    t["par"] = [tuple(sorted(p)) for p in zip(t.a, t.b)]
    return t.drop_duplicates("par").drop(columns="par").reset_index(drop=True)


def unir_cortes(t):
    """Une extremos sueltos a menos de TOL_CORTE m de otro tramo. Devuelve tramos y uniones."""
    grado = pd.concat([t.a, t.b]).value_counts()
    sueltos = [n for n, g in grado.items() if g == 1]
    geoms = [LineString([a, b]) for a, b in zip(t.a, t.b)]
    arbol = STRtree(geoms)
    nuevos, uniones, partir = [], [], {}
    for n in sueltos:
        p = Point(n)
        cand = arbol.query(p.buffer(TOL_CORTE))
        mejor = None
        for j in cand:
            if n in (t.a[j], t.b[j]):
                continue
            d = geoms[j].distance(p)
            if d <= TOL_CORTE and (mejor is None or d < mejor[1]):
                mejor = (j, d)
        if mejor is None:
            continue
        j, d = mejor
        s = geoms[j].project(p)
        q = geoms[j].interpolate(s)
        destino = clave(q.x, q.y)
        if destino in (t.a[j], t.b[j]) or s <= REDONDEO or s >= geoms[j].length - REDONDEO:
            destino = t.a[j] if Point(t.a[j]).distance(q) < Point(t.b[j]).distance(q) else t.b[j]
        else:
            partir.setdefault(j, set()).add(destino)
        if destino != n:
            uniones.append((n, destino, d))
    # Partir los tramos que reciben una unión a media cuadra
    quitar = []
    for j, puntos in partir.items():
        a, b = t.a[j], t.b[j]
        orden = sorted(puntos, key=lambda q: Point(a).distance(Point(q)))
        cadena = [a] + orden + [b]
        for x, y in zip(cadena[:-1], cadena[1:]):
            nuevos.append((x, y, t.eje[j]))
        quitar.append(j)
    t2 = pd.concat([t.drop(index=quitar), pd.DataFrame(nuevos, columns=["a", "b", "eje"])], ignore_index=True)
    u = pd.DataFrame(uniones, columns=["a", "b", "dist_m"])
    return t2, u


def main():
    vial = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="vialidades")
    crs = vial.crs
    t = tramos_de(vial)
    v = {"ejes_viales": len(vial), "tramos_iniciales": len(t),
         "ejes_por_tipo": vial.TIPOVIAL.value_counts().to_dict()}

    g0 = nx.Graph()
    g0.add_edges_from(zip(t.a, t.b))
    comp0 = list(nx.connected_components(g0))
    v["componentes_antes_de_unir"] = len(comp0)
    v["extremos_sueltos"] = int(sum(1 for _, d in g0.degree() if d == 1))

    t, uniones = unir_cortes(t)
    v["uniones_agregadas"] = len(uniones)
    v["uniones_longitud_m"] = {"mediana": round(float(uniones.dist_m.median()), 1),
                               "max": round(float(uniones.dist_m.max()), 1)} if len(uniones) else None
    t["es_union"] = False
    todo = pd.concat([t, uniones[["a", "b"]].assign(eje=-1, es_union=True)], ignore_index=True)
    todo["longitud"] = [Point(a).distance(Point(b)) for a, b in zip(todo.a, todo.b)]

    g = nx.Graph()
    g.add_edges_from(zip(todo.a, todo.b))
    comps = sorted(nx.connected_components(g), key=len, reverse=True)
    comp_de = {n: k for k, c in enumerate(comps) for n in c}
    todo["componente"] = todo.a.map(comp_de)
    v["componentes_despues_de_unir"] = len(comps)

    # Nodos numerados para la red (los usa 11_accesibilidad.py)
    nodos = pd.Index(pd.unique(pd.concat([todo.a, todo.b])))
    todo["u"] = nodos.get_indexer(todo.a)
    todo["v"] = nodos.get_indexer(todo.b)
    tramos = gpd.GeoDataFrame(
        todo[["u", "v", "longitud", "componente", "es_union", "eje"]],
        geometry=[LineString([a, b]) for a, b in zip(todo.a, todo.b)], crs=crs)
    tramos["CVE_LOC"] = tramos.eje.map(vial.CVE_LOC).fillna("")
    tramos["TIPOVIAL"] = tramos.eje.map(vial.TIPOVIAL).fillna("unión agregada")

    # Componentes por localidad urbana: cuadras y personas cuyo tramo más cercano cae en cada uno
    mza = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="manzanas")
    cas = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="caserio_disperso")
    orig = pd.concat([mza.assign(geometry=mza.representative_point()), cas], ignore_index=True)
    orig = gpd.GeoDataFrame(orig, crs=mza.crs)
    j = gpd.sjoin_nearest(orig[["CVEGEO", "CVE_LOC", "POBTOT", "geometry"]], tramos[["componente", "geometry"]],
                          how="left", distance_col="dist_acceso_m")
    j = j[~j.index.duplicated()]
    por = {}
    for loc, nombre in URBANAS.items():
        s = j[j.CVE_LOC == loc]
        k = s.groupby("componente").agg(cuadras=("CVEGEO", "size"), pob=("POBTOT", "sum"))
        principal = int(k.cuadras.idxmax())
        aisl = s[s.componente != principal]
        por[nombre] = {
            "componente_principal": principal,
            "cuadras": len(s), "cuadras_en_otro_componente": len(aisl),
            "pob_en_otro_componente": int(aisl.POBTOT.fillna(0).sum()),
            "detalle_otros": aisl.groupby("componente").agg(cuadras=("CVEGEO", "size"),
                                                            pob=("POBTOT", "sum")).reset_index().to_dict("records"),
            "acceso_m_mediana": round(float(s.dist_acceso_m.median()), 1),
            "acceso_m_p95": round(float(s.dist_acceso_m.quantile(0.95)), 1),
            "acceso_m_max": round(float(s.dist_acceso_m.max()), 1),
        }
    v["localidades_urbanas"] = por
    tam = tramos.groupby("componente").longitud.sum().sort_values(ascending=False)
    v["componentes_longitud_km_top10"] = (tam.head(10) / 1000).round(2).to_dict()
    v["componentes_menores_a_200m"] = int((tam < 200).sum())

    salida = P / "red_peatonal.gpkg"
    salida.unlink(missing_ok=True)
    tramos.to_file(salida, layer="tramos", driver="GPKG")
    if len(uniones):
        gpd.GeoDataFrame(uniones[["dist_m"]], geometry=[LineString([a, b]) for a, b in zip(uniones.a, uniones.b)],
                         crs=crs).to_file(salida, layer="uniones", driver="GPKG")
    (P / "validacion_fase3_red.json").write_text(json.dumps(v, ensure_ascii=False, indent=1, default=str))
    print(json.dumps(v, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
