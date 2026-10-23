"""11 · Distancia al servicio más cercano y población lejana (fase 3; umbrales definitivos en la fase 4).

Escala ciudad (las 4 localidades urbanas, D09): distancia a pie por la red de
calles (data/processed/red_peatonal.gpkg, 10_redes.py) desde cada cuadra al
servicio más cercano de cada categoría.
  - Origen: un punto dentro de cada cuadra (MG 2020, con población 2020) y los
    puntos de caserío disperso (D04). Las cuadras nuevas posteriores a 2020 (MG EIC
    2025, D12) se miden igual pero no tienen población: se cuentan, no se inventa
    gente (regla 3).
  - El origen se conecta en línea recta al tramo más cercano del componente
    principal de su localidad; el servicio, al tramo más cercano de ese mismo
    componente si está a <= SNAP_MAX m. La distancia es: tramo de acceso del
    origen + recorrido por la red + tramo de acceso del servicio.
  - Servicios que no quedan sobre la red de la localidad (otra localidad, otro
    municipio): línea recta × FACTOR de rodeo calibrado con la propia red. Se
    toma el menor de los dos y se dice cuál fue.
Escala municipio (localidades rurales, ITER 2020): no fue posible bajar una red
de caminos (D26; nuevo intento fallido con Overpass el 2026-10-23, fase 4), así que la distancia es línea recta × FACTOR desde el punto
de la localidad.

Población lejana:
  - Ciudad (D10): método (c) por AGEB = total publicado del grupo en la AGEB ×
    proporción de la población total de la AGEB que vive en cuadras lejanas; y
    (a) mínimo visible = suma de lo publicado por cuadra (sin rellenar "*").
  - Rural: ITER por localidad; se suma lo visible y se reporta lo oculto.

Salidas en data/processed/:
  acceso_cuadras.gpkg / .csv       una fila por cuadra: d_<cat>, id_<cat>, via_<cat>
  acceso_localidades.csv           una fila por localidad rural
  acceso_resumen_por_localidad.csv población lejana por localidad × categoría × umbral × grupo
  acceso_sensibilidad.csv          umbral principal: todas las sedes vs. solo confirmadas (D28) y vs.
                                   sin las marcadas "no" en la verificación remota (D41)
  conteo_servicios_por_localidad.csv   sedes de cada tipo por localidad (incluye las "aparte")
  validacion_fase3_acceso.json
"""

import importlib.util
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
import shapely
from shapely import STRtree

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"

spec = importlib.util.spec_from_file_location("base03", RAIZ / "src" / "03_base_geografica.py")
base03 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base03)
GRUPOS = base03.GRUPOS

URBANAS = {"0001": "Acámbaro", "0027": "Irámuco", "0047": "Parácuaro", "0017": "Chupícuaro (Nuevo Chupícuaro)"}
SNAP_MAX = 300           # m: servicio a más de esto de la red de la localidad no se conecta a ella
VEL_PIE = 4.0            # km/h, para traducir metros a minutos (adultos mayores y niños, D31)

# Categorías que se miden (D20–D22). filtro(sedes) -> sedes que cuentan.
def _no_baja(s):
    """Sin las dadas de baja (SEP/CLUES) ni las descartadas por ubicación errónea (D37)."""
    return ~s.estado_cruce.str.startswith(("baja", "descartada"))


CATEGORIAS = {
    "preescolar": lambda s: (s.tipo == "preescolar") & _no_baja(s),
    "primaria": lambda s: (s.tipo == "primaria") & _no_baja(s),
    "secundaria": lambda s: (s.tipo == "secundaria") & _no_baja(s),
    "bachillerato": lambda s: (s.tipo == "bachillerato") & _no_baja(s),
    "preescolar_publica": lambda s: (s.tipo == "preescolar") & (s.sector == "público") & _no_baja(s),
    "primaria_publica": lambda s: (s.tipo == "primaria") & (s.sector == "público") & _no_baja(s),
    "secundaria_publica": lambda s: (s.tipo == "secundaria") & (s.sector == "público") & _no_baja(s),
    "bachillerato_publico": lambda s: (s.tipo == "bachillerato") & (s.sector == "público") & _no_baja(s),
    "salud_publica": lambda s: (s.tipo == "salud_primer_nivel") & (s.sector == "público") & _no_baja(s),
    "tienda_basica": lambda s: s.tipo == "abasto",
    "abasto_completo": lambda s: (s.tipo == "abasto") & s.subtipo.str.contains("mercado|supermercado"),
    # Datos aparte: no entran al resultado principal
    # D34: salud pública + las unidades que solo dibuja el INEGI (anexo)
    "salud_publica_con_anexo": lambda s: (s.tipo == "salud_primer_nivel")
    & ((s.sector == "público") | s.anexo_salud_sin_clues.fillna(False).astype(bool)) & _no_baja(s),
    "consultorio_privado": lambda s: (s.tipo == "consultorio_privado") & _no_baja(s),
}
NOMBRES = {
    "preescolar": "Preescolar (todas)", "primaria": "Primaria (todas)", "secundaria": "Secundaria (todas)",
    "bachillerato": "Bachillerato (todos)", "preescolar_publica": "Preescolar pública",
    "primaria_publica": "Primaria pública", "secundaria_publica": "Secundaria pública",
    "bachillerato_publico": "Bachillerato público", "salud_publica": "Salud pública de primer nivel",
    "tienda_basica": "Tienda básica", "abasto_completo": "Abasto completo (mercado o supermercado)",
    "salud_publica_con_anexo": "Salud pública + unidades sin CLUES (anexo)",
    "consultorio_privado": "Consultorio privado (dato aparte)",
}

# Umbrales de "lejos" (D25 definitivo, D33): (estricto, principal, holgado), en metros.
# Ciudad: el radio de servicio urbano recomendable del SNEU (SEDESOL) se interpreta
# como línea recta; la medida es por calle, así que principal = radio × 1.33 (factor
# de rodeo calibrado en la fase 3), estricto = radio sin convertir y holgado =
# principal × 1.5 (redondeo a 10 m). Tienda (500 m) y abasto completo (1 000 m = 15 min
# a 4 km/h) no vienen del SNEU: misma proporción a partir de su principal.
UMBRALES_CIUDAD = {
    "preescolar": (750, 1000, 1500), "primaria": (500, 670, 1000), "secundaria": (1000, 1330, 2000),
    "bachillerato": (2500, 3330, 5000), "salud_publica": (1000, 1330, 2000),
    "tienda_basica": (380, 500, 750), "abasto_completo": (750, 1000, 1500),
    "salud_publica_con_anexo": (1000, 1330, 2000), "consultorio_privado": (1000, 1330, 2000),
}
UMBRALES_RURAL = {
    "preescolar": (1000, 2000, 3000), "primaria": (1000, 2000, 3000), "secundaria": (3000, 5000, 10000),
    "bachillerato": (5000, 10000, 15000), "salud_publica": (3000, 5000, 10000),
    "tienda_basica": (500, 1000, 2000), "abasto_completo": (5000, 10000, 15000),
    "salud_publica_con_anexo": (3000, 5000, 10000), "consultorio_privado": (3000, 5000, 10000),
}
NIVELES = ["estricto", "principal", "holgado"]
CALIBRACION_EXCLUYE = {"salud_publica_con_anexo"}
# Factor de rodeo (red / línea recta). Calibrado en la fase 3 (1.33, V22) y fijo desde
# la fase 4 (D33): los umbrales definitivos se derivan de él. Se sigue recalibrando
# como chequeo; con el catálogo de la fase 4 sale 1.349 por la reubicación del CECyTE.
FACTOR_FIJO = 1.33
# El DENUE solo registra comercios y consultorios de las localidades urbanas (en
# Acámbaro, 5 932 de sus 5 974 establecimientos están en las 4 urbanas; ninguna
# tienda de abarrotes rural). En lo rural estas categorías no se pueden medir:
# no hay fuente, y medir contra las tiendas de la ciudad inventaría lejanía (V24).
NO_MEDIBLE_RURAL = {"tienda_basica": "el DENUE no registra tiendas en localidades rurales",
                    "consultorio_privado": "el DENUE no registra consultorios en localidades rurales"}
# El abasto completo rural sí se mide (mercados y supermercados están en localidades
# que el DENUE cubre), pero ninguna fuente registra tianguis (D35).
NOTA_RURAL = {"abasto_completo": "no incluye tianguis: ninguna fuente los registra"}


def umbral(cat, tabla):
    if cat in tabla:
        return tabla[cat]
    return tabla[cat.replace("_publica", "").replace("_publico", "")]


def confirmada(s):
    """D28: sede respaldada por un registro con nombre (SEP, CLUES o DENUE)."""
    return (s.confirmado_por.fillna("") != "") | s.fuentes.fillna("").str.contains("DENUE") \
        | s.estado_cruce.str.startswith("nueva")


def no_dudosa(s):
    """D41: sin las sedes marcadas "no" en la verificación remota de Alejandro."""
    return ~s.dudoso_remoto.fillna(False).astype(bool)


SENSIBILIDADES = {"solo confirmadas (D28)": confirmada, "sin dudosos remotos (D41)": no_dudosa}


# --- Red -------------------------------------------------------------------------
class Red:
    def __init__(self, tramos):
        self.t = tramos.reset_index(drop=True)
        self.n = int(max(self.t.u.max(), self.t.v.max())) + 1
        self.L = self.t.longitud.to_numpy()

    def componente(self, comp):
        sel = self.t[self.t.componente == comp]
        return sel, STRtree(sel.geometry.values)

    def anclar(self, puntos, sel, arbol):
        """Para cada punto: tramo más cercano de 'sel', posición a lo largo y distancia de acceso."""
        pts = puntos.geometry.representative_point().values   # el caserío viene como multipunto
        idx = arbol.nearest(pts)
        geo = sel.geometry.values[idx]
        acc = shapely.distance(geo, pts)
        pos = shapely.line_locate_point(geo, pts)
        return pd.DataFrame({"tramo": sel.index.values[idx], "pos": pos, "acceso": acc}, index=puntos.index)

    def distancias(self, orig, dest):
        """orig y dest: DataFrames de anclar(). Devuelve distancia y etiqueta del destino más cercano."""
        u, v, L = self.t.u.to_numpy(), self.t.v.to_numpy(), self.L
        nd = len(dest)
        # nodos de destino: n .. n+nd-1, unidos a los extremos de su tramo
        filas = [u, v]
        cols = [v, u]
        pesos = [L, L]
        di = np.arange(self.n, self.n + nd)
        tr = dest.tramo.to_numpy()
        filas += [di, di]
        cols += [u[tr], v[tr]]
        pesos += [dest.pos.to_numpy() + dest.acceso.to_numpy(), L[tr] - dest.pos.to_numpy() + dest.acceso.to_numpy()]
        filas += [u[tr], v[tr]]
        cols += [di, di]
        pesos += [dest.pos.to_numpy() + dest.acceso.to_numpy(), L[tr] - dest.pos.to_numpy() + dest.acceso.to_numpy()]
        m = coo_matrix((np.concatenate(pesos) + 1e-6, (np.concatenate(filas), np.concatenate(cols))),
                       shape=(self.n + nd, self.n + nd)).tocsr()
        D, _, fuente = dijkstra(m, directed=False, indices=di, min_only=True, return_predecessors=True)
        to = orig.tramo.to_numpy()
        du = D[u[to]] + orig.pos.to_numpy()
        dv = D[v[to]] + (L[to] - orig.pos.to_numpy())
        d = np.minimum(du, dv) + orig.acceso.to_numpy()
        f = np.where(du <= dv, fuente[u[to]], fuente[v[to]])
        # Origen y destino sobre el mismo tramo: distancia directa a lo largo del tramo
        por_tramo = dest.reset_index(drop=True).groupby("tramo")
        for k, (t_o, p_o, a_o) in enumerate(zip(to, orig.pos.to_numpy(), orig.acceso.to_numpy())):
            if t_o in por_tramo.groups:
                g = dest.iloc[por_tramo.groups[t_o]]
                alt = np.abs(g.pos.to_numpy() - p_o) + g.acceso.to_numpy() + a_o
                j = alt.argmin()
                if alt[j] < d[k]:
                    d[k], f[k] = alt[j], self.n + por_tramo.groups[t_o][j]
        etiqueta = np.where(f >= self.n, f - self.n, -1)
        d[etiqueta < 0] = np.inf
        return d, etiqueta


# --- Población ---------------------------------------------------------------------
def poblacion_lejos_ciudad(cu, lejos, ageb_tot):
    """D10. cu: cuadras con población (CVE_AGEB, POBTOT y grupos). lejos: bool por cuadra."""
    out = {}
    pob = cu.POBTOT.fillna(0)
    pob_ageb = pob.groupby(cu.CVE_AGEB).sum()
    lej_ageb = pob[lejos].groupby(cu.CVE_AGEB[lejos]).sum().reindex(pob_ageb.index, fill_value=0)
    prop = (lej_ageb / pob_ageb.replace(0, np.nan)).fillna(0)
    for var in GRUPOS:
        tot = ageb_tot[var].reindex(prop.index)
        est = float((tot * prop).sum())
        visible = float(cu.loc[lejos, var].sum(min_count=1)) if lejos.any() else 0.0
        out[var] = {"estimado_c": est if var != "POBTOT" else float(pob[lejos].sum()),
                    "minimo_visible_a": visible if not np.isnan(visible) else 0.0,
                    "total": float(tot.sum()) if var != "POBTOT" else float(pob.sum())}
    return out


def main():
    sedes = gpd.read_file(P / "servicios_fase4.gpkg", layer="sedes")
    tramos = gpd.read_file(P / "red_peatonal.gpkg", layer="tramos")
    red = Red(tramos)
    crs = tramos.crs
    sedes = sedes.to_crs(crs)
    v = {"parametros": {"SNAP_MAX_m": SNAP_MAX, "velocidad_km_h": VEL_PIE,
                        "umbrales_ciudad_m": UMBRALES_CIUDAD, "umbrales_rural_m": UMBRALES_RURAL}}

    # Orígenes de la ciudad: cuadras 2020 con población + caserío + cuadras nuevas posteriores a 2020
    mza = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="manzanas")
    cas = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="caserio_disperso")
    # (La clave de una cuadra nueva puede repetir la de una cuadra 2020 renumerada:
    # por eso todo se une por posición, no por CVEGEO.)
    cu = pd.concat([mza.assign(poligono=mza.geometry, geometry=mza.representative_point(), origen="cuadra 2020"),
                    cas.assign(poligono=cas.geometry, geometry=cas.representative_point(), origen="caserío disperso 2020")], ignore_index=True)
    nuevas = gpd.read_file(P / "manzanas_cambios.gpkg", layer="eic2025_vs_2020").to_crs(crs)
    nuevas = nuevas[nuevas.geometria_nueva & nuevas.CVE_LOC.isin(URBANAS)]
    cu = pd.concat([cu, nuevas[["CVEGEO", "CVE_LOC", "CVE_AGEB"]].assign(
        poligono=nuevas.geometry, geometry=nuevas.representative_point(),
        origen="cuadra nueva posterior a 2020")], ignore_index=True)
    cu = gpd.GeoDataFrame(cu, geometry="geometry", crs=crs)
    cu["localidad"] = cu.CVE_LOC.map(URBANAS)
    v["origenes_ciudad"] = {f"{a} | {b}": n for (a, b), n in cu.groupby(["localidad", "origen"]).size().items()}

    # Componente principal de cada localidad: el que tiene más tramos dentro de sus cuadras
    comp_loc = {}
    for loc in URBANAS:
        j = gpd.sjoin_nearest(cu[cu.CVE_LOC == loc][["geometry"]], tramos[["componente", "geometry"]], how="left")
        comp_loc[loc] = int(j.componente.mode().iloc[0])

    cats = list(CATEGORIAS)
    resultados = {}
    pares_factor = []
    anclas = {}
    for loc in URBANAS:
        sel, arbol = red.componente(comp_loc[loc])
        o = cu[cu.CVE_LOC == loc]
        anclas[loc] = (red.anclar(o, sel, arbol), sel, arbol)
    # Primera pasada: solo red, para calibrar el factor de rodeo. Solo con las
    # categorías de la fase 3: agregar una categoría aparte (anexo) cambiaría el
    # factor, y los umbrales definitivos (D33) se derivan del factor 1.33.
    for loc in URBANAS:
        ao, sel, arbol = anclas[loc]
        o = cu.loc[ao.index]
        for cat in [c for c in cats if c not in CALIBRACION_EXCLUYE]:
            s = sedes[CATEGORIAS[cat](sedes)]
            ad = red.anclar(s, sel, arbol)
            ad = ad[ad.acceso <= SNAP_MAX]
            if not len(ad):
                continue
            d, k = red.distancias(ao, ad)
            ok = np.isfinite(d)
            dest = s.loc[ad.index[k[ok]]]
            recta = o[ok].geometry.distance(dest.geometry, align=False).to_numpy()
            pares_factor.append(pd.DataFrame({"red": d[ok], "recta": recta, "cat": cat, "loc": loc}))
    pf = pd.concat(pares_factor)
    pf = pf[pf.recta >= 300]
    calibrado = float((pf.red / pf.recta).median())
    FACTOR = FACTOR_FIJO
    v["factor_rodeo"] = {"valor_usado": FACTOR, "calibrado_con_este_catalogo": round(calibrado, 3),
                         "mediana_por_categoria": (pf.red / pf.recta).groupby(pf.cat).median().round(3).to_dict(),
                         "pares_usados": len(pf),
                         "p25": round(float((pf.red / pf.recta).quantile(0.25)), 3),
                         "p75": round(float((pf.red / pf.recta).quantile(0.75)), 3),
                         "nota": "mediana de distancia por red / línea recta, pares cuadra–servicio más cercano con recta >= 300 m"}
    v["red_menor_que_recta"] = int((pf.red < pf.recta - 1).sum())

    # Segunda pasada: red + respaldo en línea recta × factor
    tabla = cu[["CVEGEO", "CVE_LOC", "localidad", "CVE_AGEB", "origen"]].copy()
    for loc in URBANAS:
        ao, sel, arbol = anclas[loc]
        o = cu.loc[ao.index]
        tabla.loc[ao.index, "acceso_red_m"] = ao.acceso.round(1)
        for cat in cats:
            s = sedes[CATEGORIAS[cat](sedes)]
            ad = red.anclar(s, sel, arbol)
            en_red = ad[ad.acceso <= SNAP_MAX]
            d_red = np.full(len(o), np.inf)
            id_red = np.array([None] * len(o), dtype=object)
            if len(en_red):
                d, k = red.distancias(ao, en_red)
                ok = k >= 0
                d_red[ok] = d[ok]
                id_red[ok] = s.loc[en_red.index[k[ok]], "id_sede"].to_numpy()
            fuera = s.loc[s.index.difference(en_red.index)]
            d_rec = np.full(len(o), np.inf)
            id_rec = np.array([None] * len(o), dtype=object)
            if len(fuera):
                j = gpd.sjoin_nearest(o[["geometry"]], fuera[["id_sede", "geometry"]], how="left", distance_col="dr")
                j = j[~j.index.duplicated()]
                d_rec = j.dr.to_numpy() * FACTOR
                id_rec = j.id_sede.to_numpy()
            usar_red = d_red <= d_rec
            tabla.loc[o.index, f"d_{cat}"] = np.round(np.where(usar_red, d_red, d_rec), 0)
            tabla.loc[o.index, f"id_{cat}"] = np.where(usar_red, id_red, id_rec)
            tabla.loc[o.index, f"via_{cat}"] = np.where(usar_red, "red", "recta×factor")
    resultados["ciudad"] = tabla

    # --- Rural: línea recta × factor desde el punto ITER de cada localidad -----------
    loc = gpd.read_file(P / "localidades2020.gpkg")
    iter20 = pd.read_csv(P / "iter2020_acambaro.csv", dtype=str)
    iter20 = base03.numeros(iter20, list(GRUPOS))
    rur = loc[~loc.LOC.isin(URBANAS)].copy()
    rur = rur.merge(iter20[["LOC"] + [g for g in GRUPOS if g != "POBTOT"]], on="LOC", how="left")
    rur = rur.to_crs(crs)
    tr = rur[["CVEGEO", "LOC", "NOM_LOC", "tipo_mg2020"] + list(GRUPOS)].copy()
    for cat in cats:
        s = sedes[CATEGORIAS[cat](sedes)]
        j = gpd.sjoin_nearest(rur[["geometry"]], s[["id_sede", "cve_loc", "en_acambaro", "geometry"]],
                              how="left", distance_col="dr")
        j = j[~j.index.duplicated()]
        tr[f"d_{cat}"] = (j.dr * FACTOR).round(0).to_numpy() if cat not in NO_MEDIBLE_RURAL else np.nan
        tr[f"id_{cat}"] = j.id_sede.to_numpy()
        tr[f"en_la_localidad_{cat}"] = (j.en_acambaro.astype(bool) & (j.cve_loc == rur.LOC)).to_numpy()
    resultados["rural"] = tr

    # --- Población lejana ---------------------------------------------------------------
    _, ageb, loc_tab, mun = base03.censo_manzanas("censo2020_mza_acambaro.csv", list(GRUPOS))
    ageb["CVE_AGEB"] = ageb.AGEB
    tc = tabla.join(cu[list(GRUPOS)])
    filas = []
    for cat in cats:
        for nivel, (uc, ur) in zip(NIVELES, zip(umbral(cat, UMBRALES_CIUDAD), umbral(cat, UMBRALES_RURAL))):
            for cl, nombre in URBANAS.items():
                c = tc[(tc.CVE_LOC == cl) & (tc.origen != "cuadra nueva posterior a 2020")]
                at = ageb[ageb.LOC == cl].set_index("CVE_AGEB")
                lejos = (c[f"d_{cat}"] > uc).to_numpy()
                res = poblacion_lejos_ciudad(c.set_index(c.index), pd.Series(lejos, index=c.index), at)
                nuevas_lejos = int(((tc.CVE_LOC == cl) & (tc.origen == "cuadra nueva posterior a 2020")
                                    & (tc[f"d_{cat}"] > uc)).sum())
                for var, r in res.items():
                    filas.append({"localidad": nombre, "escala": "ciudad (a pie, por calles)", "categoria": cat,
                                  "umbral": nivel, "umbral_m": uc, "grupo": GRUPOS[var], "variable": var,
                                  "pob_lejos": round(r["estimado_c"]), "pob_lejos_minimo_visible": round(r["minimo_visible_a"]),
                                  "pob_total": round(r["total"]),
                                  "pct_lejos": round(100 * r["estimado_c"] / r["total"], 1) if r["total"] else None,
                                  "cuadras_lejos": int(lejos.sum()), "cuadras": len(c),
                                  "cuadras_nuevas_post2020_lejos": nuevas_lejos})
            lejos_r = tr[f"d_{cat}"] > ur
            medible = cat not in NO_MEDIBLE_RURAL
            for var in GRUPOS:
                vis = float(tr.loc[lejos_r, var].sum())
                tot_vis = float(tr[var].sum())
                filas.append({"localidad": "Localidades rurales (208)", "escala": "municipio (línea recta × factor)",
                              "categoria": cat, "umbral": nivel, "umbral_m": ur, "grupo": GRUPOS[var], "variable": var,
                              "pob_lejos": round(vis) if medible else None,
                              "pob_lejos_minimo_visible": round(vis) if medible else None,
                              "pob_total": round(tot_vis),
                              "pct_lejos": round(100 * vis / tot_vis, 1) if tot_vis and medible else None,
                              "cuadras_lejos": None, "cuadras": None, "cuadras_nuevas_post2020_lejos": None,
                              "localidades_lejos": int(lejos_r.sum()) if medible else None,
                              "nota": NO_MEDIBLE_RURAL.get(cat, NOTA_RURAL.get(cat, ""))})
    resumen = pd.DataFrame(filas)
    # Si el mínimo visible (a) supera la estimación (c), el supuesto de (c) falla en
    # esa localidad (los lejanos tienen más de ese grupo que el promedio de su AGEB):
    # la cifra real es al menos (a). Se marca para no reportar (c) solo.
    resumen["minimo_supera_estimado"] = resumen.pob_lejos_minimo_visible > resumen.pob_lejos

    # Población oculta en el ITER rural, por grupo (lo que no se ve en ninguna localidad)
    mun_tot = mun.iloc[0]
    v["iter_rural_oculto"] = {GRUPOS[g]: {
        "total_municipal": float(mun_tot[g]),
        "visible_urbanas": float(loc_tab[loc_tab.LOC.isin(URBANAS)][g].sum()),
        "visible_rurales": float(tr[g].sum()),
        "oculto_en_rurales": float(mun_tot[g] - loc_tab[loc_tab.LOC.isin(URBANAS)][g].sum() - tr[g].sum())}
        for g in GRUPOS}

    # --- Sensibilidades, umbral principal: solo confirmadas (D28), sin dudosos remotos (D41)
    sens = []
    for variante, filtro in SENSIBILIDADES.items():
        conf = sedes[filtro(sedes)]
        for cat in cats:
            s_all = sedes[CATEGORIAS[cat](sedes)]
            s_conf = conf[CATEGORIAS[cat](conf)]
            quitadas = len(s_all) - len(s_conf)
            uc, ur = umbral(cat, UMBRALES_CIUDAD)[1], umbral(cat, UMBRALES_RURAL)[1]
            for cl, nombre in URBANAS.items():
                c = tc[(tc.CVE_LOC == cl) & (tc.origen != "cuadra nueva posterior a 2020")]
                ao, sel, arbol = anclas[cl]
                ao = ao.loc[c.index]
                o = cu.loc[c.index]
                ad = red.anclar(s_conf, sel, arbol)
                en_red = ad[ad.acceso <= SNAP_MAX]
                d_red = red.distancias(ao, en_red)[0] if len(en_red) else np.full(len(o), np.inf)
                fuera = s_conf.loc[s_conf.index.difference(en_red.index)]
                d_rec = np.full(len(o), np.inf)
                if len(fuera):
                    j = gpd.sjoin_nearest(o[["geometry"]], fuera[["geometry"]], how="left", distance_col="dr")
                    d_rec = j[~j.index.duplicated()].dr.to_numpy() * FACTOR
                d2 = np.round(np.minimum(d_red, d_rec), 0)   # igual que en la tabla principal
                p1 = float(c.loc[c[f"d_{cat}"] > uc, "POBTOT"].sum())
                p2 = float(c.loc[d2 > uc, "POBTOT"].sum())
                sens.append({"variante": variante, "localidad": nombre, "categoria": cat, "umbral_principal_m": uc,
                             "pob_lejos_todas": round(p1), "pob_lejos_variante": round(p2),
                             "diferencia": round(p2 - p1), "sedes_quitadas_en_toda_la_zona": quitadas})
            if cat in NO_MEDIBLE_RURAL:
                continue
            j = gpd.sjoin_nearest(rur[["geometry"]], s_conf[["geometry"]], how="left", distance_col="dr")
            d2 = np.round(j[~j.index.duplicated()].dr.to_numpy() * FACTOR, 0)
            p1 = float(tr.loc[tr[f"d_{cat}"] > ur, "POBTOT"].sum())
            p2 = float(tr.loc[d2 > ur, "POBTOT"].sum())
            sens.append({"variante": variante, "localidad": "Localidades rurales (208)", "categoria": cat,
                         "umbral_principal_m": ur, "pob_lejos_todas": round(p1), "pob_lejos_variante": round(p2),
                         "diferencia": round(p2 - p1), "sedes_quitadas_en_toda_la_zona": quitadas})
    sens = pd.DataFrame(sens)

    # --- Conteo de sedes por localidad (incluye las que se registran aparte) ------------
    s_mun = sedes[sedes.en_acambaro].copy()
    s_mun["cve_loc"] = s_mun.cve_loc.fillna("")
    nombres_loc = dict(zip(loc.LOC, loc.NOM_LOC))
    s_mun["NOM_LOC"] = s_mun.cve_loc.map(nombres_loc).fillna(s_mun.localidad)
    s_mun["tipo_conteo"] = np.where(s_mun.estado_cruce.str.startswith("baja"), s_mun.tipo + " (dada de baja)", s_mun.tipo)
    conteo = s_mun.groupby(["cve_loc", "NOM_LOC", "tipo_conteo"]).size().unstack(fill_value=0).reset_index()

    # --- Salidas -----------------------------------------------------------------------
    geo = gpd.GeoDataFrame(tc, geometry=cu.geometry.values, crs=crs)
    salida = P / "acceso_cuadras.gpkg"
    salida.unlink(missing_ok=True)
    gpd.GeoDataFrame(tc, geometry=gpd.GeoSeries(cu.poligono.values, crs=crs), crs=crs).to_file(
        salida, layer="cuadras", driver="GPKG")
    ll = geo.to_crs("EPSG:4326")
    geo.drop(columns="geometry").assign(lat=ll.geometry.y.round(6), lon=ll.geometry.x.round(6)).to_csv(
        P / "acceso_cuadras.csv", index=False)
    rr = rur.to_crs("EPSG:4326")
    tr.assign(lat=rr.geometry.y.round(6).values, lon=rr.geometry.x.round(6).values).to_csv(
        P / "acceso_localidades.csv", index=False)
    resumen.to_csv(P / "acceso_resumen_por_localidad.csv", index=False)
    sens.to_csv(P / "acceso_sensibilidad.csv", index=False)
    conteo.to_csv(P / "conteo_servicios_por_localidad.csv", index=False)

    # --- Chequeos -----------------------------------------------------------------------
    v["componente_por_localidad"] = comp_loc
    v["filas_con_minimo_visible_mayor_que_estimado"] = int(resumen.minimo_supera_estimado.sum())
    v["filas_ciudad"] = int((resumen.escala.str.startswith("ciudad")).sum())
    v["acceso_red_m"] = tabla.groupby("localidad").acceso_red_m.describe(percentiles=[.5, .95]).round(1).to_dict("index")
    v["cuadras_acceso_mayor_100m"] = (tabla[tabla.acceso_red_m > 100][["CVEGEO", "localidad", "origen", "acceso_red_m"]]
                                      .to_dict("records"))
    v["via_recta_factor"] = {cat: tabla.groupby("localidad")[f"via_{cat}"].apply(
        lambda x: int((x != "red").sum())).to_dict() for cat in cats}
    v["distancias_ciudad_m"] = {cat: tabla.groupby("localidad")[f"d_{cat}"].describe(
        percentiles=[.5, .9]).round(0)[["50%", "90%", "max"]].to_dict("index") for cat in cats}
    v["distancias_rural_m"] = {cat: tr[f"d_{cat}"].describe(percentiles=[.5, .9]).round(0)[["50%", "90%", "max"]].to_dict()
                               for cat in cats}
    v["rural_mas_lejanas"] = {cat: tr.nlargest(3, f"d_{cat}")[["NOM_LOC", "POBTOT", f"d_{cat}"]].to_dict("records")
                              for cat in cats if cat not in NO_MEDIBLE_RURAL}
    den = pd.read_csv(P / "denue_acambaro_buffer10km.csv", dtype=str)
    den = den[den.en_acambaro == "True"]
    v["denue_establecimientos_acambaro_por_localidad"] = {
        "4 localidades urbanas": int(den.cve_loc.isin(URBANAS).sum()), "resto": int((~den.cve_loc.isin(URBANAS)).sum()),
        "localidades_rurales_con_algun_registro": int(den[~den.cve_loc.isin(URBANAS)].cve_loc.nunique()),
        "abarrotes_minisuper_super_fuera_de_las_urbanas": int(
            (~den.cve_loc.isin(URBANAS) & den.codigo_act.isin(["461110", "462111", "462112"])).sum())}
    v["ciudad_mas_lejanas"] = {cat: tabla.nlargest(3, f"d_{cat}")[["CVEGEO", "localidad", f"d_{cat}", f"via_{cat}"]]
                               .to_dict("records") for cat in cats}
    # Control: población total en orígenes = V01
    v["poblacion_en_origenes"] = tc.groupby("localidad").POBTOT.sum().to_dict()
    # Control: distancia por red nunca menor que la recta (ver red_menor_que_recta)
    (P / "validacion_fase4_acceso.json").write_text(json.dumps(v, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: v[k] for k in ["factor_rodeo", "red_menor_que_recta", "poblacion_en_origenes",
                                        "componente_por_localidad", "acceso_red_m", "via_recta_factor"]},
                     ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
