"""19 · Crecimiento urbano y acceso (fase 4b).

En las 4 localidades urbanas (D09), cada cuadra se clasifica por antigüedad con el
criterio de geometría de D12 (nueva = menos del 50 % de su superficie ya era manzana
en la edición anterior del MG):
  - consolidada: cuadra 2020 que ya existía en el MG 2010;
  - nueva 2010–2020: cuadra 2020 que no existía en 2010;
  - nueva posterior a 2020: cuadra del MG EIC 2025 que no existía en 2020 (sin población).
El caserío disperso (D04) queda aparte.

Luego compara, por localidad:
  1. el acceso (distancias de acceso_cuadras, 11_accesibilidad.py) de cada grupo, con
     los tres umbrales (D33); las cuadras posteriores a 2020 por número y superficie;
  2. lo mismo dentro de anillos de 500 m desde el centro de la localidad (punto del
     ITER 2020), para separar "periferia" de "zona nueva";
  3. viviendas deshabitadas y de uso temporal 2020 por grupo, por anillo y por AGEB,
     con lo que oculta el "*";
  4. el cambio 2010 → 2020 de población y viviendas por anillo y por AGEB 2020
     (cada manzana 2010 se asigna por su centroide). Las deshabitadas y de uso
     temporal de 2010 están ocultas en casi todas las manzanas, así que la década se
     compara con los totales publicados por AGEB, agrupados en "unidades comparables"
     (conjuntos de AGEB 2010 y 2020 que cubren el mismo suelo);
  5. una tipología de AGEB propuesta (criterios en CRITERIOS; los aprueba Alejandro).
Si data/raw/verificacion/verificacion_zonas.csv existe, repite 1 y 5 sin las cuadras
de las zonas marcadas "no"; si no, todo es provisional.

Salidas en data/processed/:
  cuadras_antiguedad.gpkg / .csv           una fila por cuadra (posición = acceso_cuadras)
  crecimiento_acceso.csv                   localidad × servicio × umbral × grupo
  crecimiento_acceso_por_anillo.csv        lo mismo por anillo de 500 m
  crecimiento_acceso_periferia.csv         nuevas contra consolidadas a igual distancia del centro
  crecimiento_viviendas.csv                viviendas 2020 por localidad / anillo / AGEB × grupo
  crecimiento_viviendas_2010_2020.csv      población y viviendas 2010 vs 2020 (anillo, unidad, localidad)
  tipologia_ageb.csv                       tipología propuesta por AGEB 2020
  tipologia_sensibilidad.csv               cuántas AGEB cambian de clase al mover cada umbral
  validacion_fase4b.json
"""

import importlib.util
import json
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
VERIF_ZONAS = RAIZ / "data" / "raw" / "verificacion" / "verificacion_zonas.csv"

spec = importlib.util.spec_from_file_location("acc11", RAIZ / "src" / "11_accesibilidad.py")
acc11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc11)
URBANAS = acc11.URBANAS
NIVELES = acc11.NIVELES

UMBRAL_NUEVA = 0.5   # D12
ANILLO = 500         # m, ancho de los anillos desde el centro
# Servicios que se comparan (los del resumen de la fase 4; escuelas todas, bachillerato público)
SERVICIOS = ["preescolar", "primaria", "secundaria", "bachillerato_publico", "salud_publica",
             "tienda_basica", "abasto_completo"]
CONSOL, N1020, N20 = "consolidada", "nueva 2010–2020", "nueva posterior a 2020"
GRUPOS = [CONSOL, N1020, N20]
SECTORES = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
# Tipología propuesta (D46): umbrales y alternativas para la sensibilidad
# - nueva: al menos frac_sup_nueva de la superficie de sus cuadras es nueva (2010–2020 o posterior);
# - desatendida: en al menos servicios_lejos de los 5 BASICOS, más de la mitad de su población
#   (o de su superficie, si no tiene población) está lejos con el umbral principal;
# - vaciándose: % de viviendas no habitadas (deshabitadas + uso temporal) en el percentil indicado
#   o más, dentro de su localidad (corte_por), con al menos min_viviendas, y población 2020 < 2010
#   en su unidad comparable.
CRITERIOS = {"frac_sup_nueva": 0.30, "servicios_lejos": 3, "percentil_no_habitadas": 0.75,
             "min_viviendas": 30, "corte_por": "localidad"}
ALTERNATIVAS = {"frac_sup_nueva": [0.25, 0.40], "servicios_lejos": [2, 4], "percentil_no_habitadas": [0.66, 0.90],
                "corte_por": ["4 localidades juntas"]}
BASICOS = ["preescolar", "primaria", "secundaria", "salud_publica", "abasto_completo"]


def num(s):
    return pd.to_numeric(s.replace("*", np.nan), errors="coerce")


def mediana_ponderada(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    ok = np.isfinite(x) & (w > 0)
    if not ok.any():
        return np.nan
    o = np.argsort(x[ok])
    c = np.cumsum(w[ok][o])
    return float(x[ok][o][np.searchsorted(c, c[-1] / 2)])


def centros(crs):
    l = pd.read_csv(P / "localidades2020.csv", dtype={"LOC": str})
    l = l[l.LOC.isin(URBANAS)]
    g = gpd.GeoDataFrame(l, geometry=gpd.points_from_xy(l.lon, l.lat), crs=4326).to_crs(crs)
    return dict(zip(g.LOC, g.geometry))


def sector(dx, dy):
    ang = (np.degrees(np.arctan2(dx, dy)) + 360 + 22.5) % 360   # 0 = norte, en sentido horario
    return np.array(SECTORES)[(ang // 45).astype(int)]


def censo(anio):
    c = pd.read_csv(P / f"censo{anio}_mza_acambaro.csv", dtype=str)
    c = c[c.LOC.isin(URBANAS)].copy()
    for k in ["POBTOT", "VIVTOT", "TVIVHAB", "VIVPAR_DES", "VIVPAR_UT"]:
        c[k] = num(c[k])
    c["CVEGEO"] = "11002" + c.LOC + c.AGEB + c.MZA
    return c


# --- 1. Antigüedad ----------------------------------------------------------------

def antiguedad():
    cu = gpd.read_file(P / "acceso_cuadras.gpkg", layer="cuadras")
    c20 = gpd.read_file(P / "manzanas_cambios.gpkg", layer="mg2020_vs_2010")
    frac = c20.set_index("CVEGEO").frac_ya_existia
    cart = c20.set_index("CVEGEO").localidad_ya_cartografiada
    n25 = gpd.read_file(P / "manzanas_cambios.gpkg", layer="eic2025_vs_2020")
    n25 = n25[n25.geometria_nueva & n25.CVE_LOC.isin(URBANAS)].set_index("CVEGEO")
    es20 = cu.origen == "cuadra 2020"
    es25 = cu.origen == "cuadra nueva posterior a 2020"
    # La clave de una cuadra posterior a 2020 puede repetir una de 2020: se une por (CVEGEO, origen)
    cu["frac_ya_existia"] = np.where(es20, cu.CVEGEO.map(frac), np.where(es25, cu.CVEGEO.map(n25.frac_ya_existia), np.nan))
    cu["localidad_ya_cartografiada_2010"] = np.where(es20, cu.CVEGEO.map(cart), np.nan)
    cu["periodo"] = np.select([es20 & (cu.frac_ya_existia >= UMBRAL_NUEVA), es20, es25],
                              [CONSOL, N1020, N20], default="caserío disperso")
    cu["superficie_m2"] = np.where(cu.geom_type == "Polygon", cu.area, 0.0)
    cen = centros(cu.crs)
    pt = cu.geometry.representative_point()
    cx = cu.CVE_LOC.map(lambda l: cen[l].x)
    cy = cu.CVE_LOC.map(lambda l: cen[l].y)
    cu["dist_centro_m"] = np.hypot(pt.x - cx, pt.y - cy).round(0)
    cu["anillo_m"] = (cu.dist_centro_m // ANILLO * ANILLO).astype(int)
    cu["sector"] = sector(pt.x - cx, pt.y - cy)
    # Viviendas 2020 (MG 2020 = misma edición que el censo: aquí sí se une por CVEGEO)
    viv = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="manzanas").set_index("CVEGEO")
    for k in ["VIVTOT", "TVIVHAB", "VIVPAR_DES", "VIVPAR_UT"]:
        cu[k] = np.where(es20, cu.CVEGEO.map(viv[k]), np.nan)
    return cu, cen


def zonas_no():
    """Cuadras de zonas marcadas "no" en la revisión de Alejandro, como pares (CVEGEO, periodo)."""
    if not VERIF_ZONAS.exists():
        return None
    z = pd.read_csv(VERIF_ZONAS, dtype=str)
    z = z[z.existe_en_imagen.fillna("").str.strip().str.lower() == "no"]
    per = {"2010-2020": N1020, "posterior a 2020": N20}
    return {(c, per.get(p, p)) for p, cs in zip(z.periodo, z.claves_cuadras) for c in str(cs).split()}


# --- 2. Acceso según antigüedad ---------------------------------------------------

def resumir(t, cat, u):
    d = t[f"d_{cat}"].to_numpy(float)
    w = t.POBTOT.fillna(0).to_numpy(float)
    a = t.superficie_m2.to_numpy(float)
    lejos = d > u
    pob = w.sum()
    return {"cuadras": len(t), "superficie_ha": round(a.sum() / 1e4, 1),
            "poblacion_2020": int(pob) if len(t) and t.periodo.iloc[0] != N20 else np.nan,
            "dist_mediana_pob_m": round(mediana_ponderada(d, w)) if pob else np.nan,
            "dist_mediana_cuadras_m": round(float(np.nanmedian(d))) if len(t) else np.nan,
            "pob_lejos": int(w[lejos].sum()) if pob else np.nan,
            "pct_pob_lejos": round(100 * w[lejos].sum() / pob, 1) if pob else np.nan,
            "pct_cuadras_lejos": round(100 * lejos.mean(), 1) if len(t) else np.nan,
            "pct_superficie_lejos": round(100 * a[lejos].sum() / a.sum(), 1) if a.sum() else np.nan,
            "dist_centro_mediana_m": round(float(t.dist_centro_m.median())) if len(t) else np.nan}


def acceso(cu, excluir=None):
    filas, anillos = [], []
    cu = cu[cu.periodo.isin(GRUPOS)]
    if excluir:
        cu = cu[[(c, p) not in excluir for c, p in zip(cu.CVEGEO, cu.periodo)]]
    for loc, nom in URBANAS.items():
        t = cu[cu.CVE_LOC == loc]
        for cat in SERVICIOS:
            for niv, u in zip(NIVELES, acc11.umbral(cat, acc11.UMBRALES_CIUDAD)):
                for g in GRUPOS:
                    tg = t[t.periodo == g]
                    filas.append({"cve_loc": loc, "localidad": nom, "servicio": cat, "umbral": niv,
                                  "umbral_m": u, "grupo": g, **resumir(tg, cat, u)})
                    for r, tr in tg.groupby("anillo_m"):
                        anillos.append({"cve_loc": loc, "localidad": nom, "servicio": cat, "umbral": niv,
                                        "umbral_m": u, "anillo_m": f"{r}–{r + ANILLO}", "anillo_ini": r,
                                        "grupo": g, **resumir(tr, cat, u)})
    return pd.DataFrame(filas), pd.DataFrame(anillos)


def periferia(an):
    """Nuevas contra consolidadas a igual distancia del centro: lo que se esperaría en las
    nuevas si en cada anillo tuvieran la tasa de las consolidadas del mismo anillo."""
    filas = []
    claves = ["cve_loc", "localidad", "servicio", "umbral"]
    tot = an.copy()
    tot["cve_loc"], tot["localidad"] = "4U", "Las 4 localidades (cada una con sus anillos)"
    for (k, t) in pd.concat([an, tot]).groupby(claves):
        c = t[t.grupo == CONSOL].groupby(["cve_loc", "anillo_ini"])
        cons_pct = c.apply(lambda x: (x.pct_pob_lejos * x.poblacion_2020).sum() / x.poblacion_2020.sum()
                           if x.poblacion_2020.sum() else np.nan, include_groups=False)
        cons_pct_cu = c.apply(lambda x: (x.pct_cuadras_lejos * x.cuadras).sum() / x.cuadras.sum(), include_groups=False)
        for g, peso, real, ref in [(N1020, "poblacion_2020", "pct_pob_lejos", cons_pct),
                                   (N1020, "cuadras", "pct_cuadras_lejos", cons_pct_cu),
                                   (N20, "cuadras", "pct_cuadras_lejos", cons_pct_cu)]:
            n = t[t.grupo == g].copy()
            n["ref"] = [ref.get((l, r), np.nan) for l, r in zip(n.cve_loc, n.anillo_ini)]
            sin_ref = n.ref.isna()
            m = n[~sin_ref]
            w = m[peso].sum()
            filas.append(dict(zip(claves, k)) | {
                "grupo": g, "medida": "% población lejos" if peso == "poblacion_2020" else "% cuadras lejos",
                "nuevas_real_pct": round((m[real] * m[peso]).sum() / w, 1) if w else np.nan,
                "consolidadas_mismo_anillo_pct": round((m.ref * m[peso]).sum() / w, 1) if w else np.nan,
                "consolidadas_todas_pct": round(float(
                    (t[t.grupo == CONSOL][real] * t[t.grupo == CONSOL][peso]).sum() / t[t.grupo == CONSOL][peso].sum()), 1),
                "peso_comparado": int(w), "peso_sin_consolidadas_en_su_anillo": int(n[sin_ref][peso].sum())})
    p = pd.DataFrame(filas)
    p["efecto_zona_nueva_pp"] = (p.nuevas_real_pct - p.consolidadas_mismo_anillo_pct).round(1)
    p["efecto_periferia_pp"] = (p.consolidadas_mismo_anillo_pct - p.consolidadas_todas_pct).round(1)
    return p


# --- 3. Viviendas 2020 ------------------------------------------------------------

def viviendas_2020(cu):
    c = censo(2020)
    ageb_pub = c[(c.MZA == "000") & (c.AGEB != "0000")].set_index(["LOC", "AGEB"])
    loc_pub = c[c.AGEB == "0000"].set_index("LOC")
    t = cu[cu.periodo.isin([CONSOL, N1020])].copy()
    t["no_habitadas"] = t.VIVTOT - t.TVIVHAB
    filas = []

    def fila(nivel, clave, g, x, pub=None):
        r = {"nivel": nivel, **clave, "grupo": g, "cuadras": len(x), "poblacion_2020": int(x.POBTOT.sum()),
             "viviendas_total": int(x.VIVTOT.sum()),
             "no_habitadas_visibles": int(x.no_habitadas.sum()),
             "cuadras_habitadas_oculto": int(x.TVIVHAB.isna().sum()),
             "deshabitadas_visibles": int(x.VIVPAR_DES.sum()),
             "cuadras_deshabitadas_oculto": int(x.VIVPAR_DES.isna().sum()),
             "viviendas_en_cuadras_deshabitadas_oculto": int(x.VIVTOT[x.VIVPAR_DES.isna()].sum()),
             "uso_temporal_visibles": int(x.VIVPAR_UT.sum()),
             "cuadras_uso_temporal_oculto": int(x.VIVPAR_UT.isna().sum())}
        vt = x.VIVTOT[x.TVIVHAB.notna()].sum()
        r["pct_no_habitadas_visible"] = round(100 * r["no_habitadas_visibles"] / vt, 1) if vt else np.nan
        vd = x.VIVTOT[x.VIVPAR_DES.notna()].sum()
        r["pct_deshabitadas_visible"] = round(100 * r["deshabitadas_visibles"] / vd, 1) if vd else np.nan
        vu = x.VIVTOT[x.VIVPAR_UT.notna()].sum()
        r["pct_uso_temporal_visible"] = round(100 * r["uso_temporal_visibles"] / vu, 1) if vu else np.nan
        if pub is not None:
            r |= {"deshabitadas_publicado": pub.VIVPAR_DES, "uso_temporal_publicado": pub.VIVPAR_UT,
                  "viviendas_publicado": pub.VIVTOT}
        return r

    for loc, nom in URBANAS.items():
        tl = t[t.CVE_LOC == loc]
        for g in [CONSOL, N1020, "todas"]:
            x = tl if g == "todas" else tl[tl.periodo == g]
            filas.append(fila("localidad", {"cve_loc": loc, "localidad": nom}, g, x,
                              loc_pub.loc[loc] if g == "todas" else None))
            for r, xr in x.groupby("anillo_m"):
                filas.append(fila("anillo", {"cve_loc": loc, "localidad": nom, "anillo_m": f"{r}–{r + ANILLO}",
                                             "anillo_ini": r}, g, xr))
        for ag, xa in tl.groupby("CVE_AGEB"):
            for g in [CONSOL, N1020, "todas"]:
                x = xa if g == "todas" else xa[xa.periodo == g]
                if len(x):
                    filas.append(fila("ageb", {"cve_loc": loc, "localidad": nom, "cve_ageb": ag}, g, x,
                                      ageb_pub.loc[(loc, ag)] if g == "todas" and (loc, ag) in ageb_pub.index else None))
    v = pd.DataFrame(filas)
    # Lo que el "*" oculta: total publicado − suma visible (solo donde el total está publicado)
    v["deshabitadas_ocultas"] = v.deshabitadas_publicado - v.deshabitadas_visibles
    v["uso_temporal_ocultas"] = v.uso_temporal_publicado - v.uso_temporal_visibles
    return v


# --- 4. Década 2010 → 2020 --------------------------------------------------------

def decada(cu, cen):
    """Asigna cada manzana 2010 a la AGEB 2020 y al anillo que contienen su centroide."""
    crs = cu.crs
    m10 = gpd.read_file(P / "mg2010_acambaro.gpkg", layer="manzanas").to_crs(crs)
    m10 = m10[m10.CVE_LOC.isin(URBANAS)]
    c10 = censo(2010)
    m10 = m10.merge(c10[["CVEGEO", "POBTOT", "VIVTOT", "TVIVHAB", "VIVPAR_DES", "VIVPAR_UT"]], on="CVEGEO", how="left")
    m10["AGEB10"] = m10.CVEGEO.str[9:13]
    pt = m10.geometry.representative_point()
    cx = m10.CVE_LOC.map(lambda l: cen[l].x)
    cy = m10.CVE_LOC.map(lambda l: cen[l].y)
    m10["anillo_ini"] = (np.hypot(pt.x - cx, pt.y - cy) // ANILLO * ANILLO).astype(int)
    a20 = cu[cu.periodo.isin([CONSOL, N1020])].dissolve(by=["CVE_LOC", "CVE_AGEB"]).reset_index()[
        ["CVE_LOC", "CVE_AGEB", "geometry"]]
    j = gpd.sjoin(gpd.GeoDataFrame(m10.drop(columns="geometry"), geometry=pt, crs=crs), a20, how="left",
                  predicate="within")
    j = j[~j.index.duplicated()]
    falta = j.CVE_AGEB.isna()
    if falta.any():   # fuera de toda AGEB 2020 (borde): la más cercana de su localidad
        near = gpd.sjoin_nearest(j[falta][["CVE_LOC_left", "geometry"]], a20, how="left")
        near = near[~near.index.duplicated()]
        j.loc[falta, "CVE_AGEB"] = near.CVE_AGEB
    m10["AGEB20"] = j.CVE_AGEB.values
    m10["fuera_ageb_2020"] = falta.values

    # Unidades comparables: componentes del grafo AGEB 2010 — AGEB 2020 (arista si ≥ 5 % de
    # las viviendas 2010 de la AGEB 2010 caen en esa AGEB 2020, o si una AGEB 2020 recibe
    # alguna manzana 2010). Dentro de una unidad, los totales publicados son comparables.
    G = nx.Graph()
    for loc in URBANAS:
        for ag in a20[a20.CVE_LOC == loc].CVE_AGEB:
            G.add_node(("20", loc, ag))
    reparto = m10.groupby(["CVE_LOC", "AGEB10", "AGEB20"]).VIVTOT.sum()
    tot10 = m10.groupby(["CVE_LOC", "AGEB10"]).VIVTOT.sum()
    for (loc, a10, a20_), viv in reparto.items():
        G.add_node(("10", loc, a10))
        if tot10[(loc, a10)] == 0 or viv / tot10[(loc, a10)] >= 0.05:
            G.add_edge(("10", loc, a10), ("20", loc, a20_))
    unidad = {}
    for i, comp in enumerate(sorted(nx.connected_components(G), key=lambda c: sorted(c))):
        for n in comp:
            unidad[n] = f"U{i + 1:03d}"

    pub = {}
    for anio in (2010, 2020):
        c = censo(anio)
        pub[anio] = c[(c.MZA == "000") & (c.AGEB != "0000")].set_index(["LOC", "AGEB"])
    t20 = cu[cu.periodo.isin([CONSOL, N1020])]
    filas = []
    # (a) por unidad comparable, con totales publicados por AGEB
    for u in sorted(set(unidad.values())):
        nodos = [n for n, x in unidad.items() if x == u]
        loc = nodos[0][1]
        r = {"nivel": "unidad", "cve_loc": loc, "localidad": URBANAS[loc], "unidad": u,
             "agebs_2010": " ".join(sorted(n[2] for n in nodos if n[0] == "10")),
             "agebs_2020": " ".join(sorted(n[2] for n in nodos if n[0] == "20"))}
        x20 = t20[(t20.CVE_LOC == loc) & t20.CVE_AGEB.isin(r["agebs_2020"].split())]
        w = x20.VIVTOT.sum()
        r["dist_centro_m"] = round(float((x20.dist_centro_m * x20.VIVTOT).sum() / w)) if w else np.nan
        r["anillo_ini"] = int(r["dist_centro_m"] // ANILLO * ANILLO) if w else np.nan
        r["frac_sup_nueva_2010_2020"] = round(x20.superficie_m2[x20.periodo == N1020].sum() / x20.superficie_m2.sum(), 3)
        for anio, key in [(2010, "10"), (2020, "20")]:
            ags = [n[2] for n in nodos if n[0] == key]
            p = pub[anio].reindex([(loc, a) for a in ags])
            for k in ["POBTOT", "VIVTOT", "VIVPAR_DES", "VIVPAR_UT"]:
                r[f"{k}_{anio}"] = p[k].sum(min_count=1) if p[k].notna().all() else np.nan
            r[f"agebs_con_oculto_{anio}"] = int(p[["VIVPAR_DES", "VIVPAR_UT"]].isna().any(axis=1).sum())
        filas.append(r)
    # (b) por anillo y (c) por AGEB 2020, con manzanas visibles (asignación por centroide)
    for nivel, k10, k20 in [("anillo", "anillo_ini", "anillo_m"), ("ageb_2020", "AGEB20", "CVE_AGEB")]:
        for loc, nom in URBANAS.items():
            a = m10[m10.CVE_LOC == loc].groupby(k10)
            b = t20[t20.CVE_LOC == loc].groupby(k20)
            for key in sorted(set(a.groups) | set(b.groups)):
                r = {"nivel": nivel, "cve_loc": loc, "localidad": nom}
                r["anillo_ini" if nivel == "anillo" else "cve_ageb"] = key
                if nivel == "anillo":
                    r["anillo_m"] = f"{key}–{key + ANILLO}"
                else:
                    r["unidad"] = unidad.get(("20", loc, key))
                for anio, g in [(2010, a), (2020, b)]:
                    x = g.get_group(key) if key in g.groups else pd.DataFrame(columns=["POBTOT", "VIVTOT", "VIVPAR_DES", "VIVPAR_UT"])
                    # min_count=1: Chupícuaro no tiene tabla por manzana en 2010 (vacío, no cero)
                    r[f"POBTOT_{anio}"] = x.POBTOT.sum(min_count=1)
                    r[f"VIVTOT_{anio}"] = x.VIVTOT.sum(min_count=1)
                    r[f"VIVPAR_DES_visibles_{anio}"] = x.VIVPAR_DES.sum(min_count=1)
                    r[f"VIVPAR_UT_visibles_{anio}"] = x.VIVPAR_UT.sum(min_count=1)
                    r[f"manzanas_{anio}"] = len(x)
                    r[f"manzanas_des_oculto_{anio}"] = int(x.VIVPAR_DES.isna().sum())
                filas.append(r)
    # (b') por anillo con los totales publicados de las unidades comparables que tienen
    # deshabitadas y uso temporal publicados en ambos años (anillo de la unidad = distancia
    # media al centro de sus cuadras 2020, ponderada por viviendas)
    un = pd.DataFrame([f for f in filas if f["nivel"] == "unidad"])
    cols = [f"{k}_{a}" for a in (2010, 2020) for k in ["POBTOT", "VIVTOT", "VIVPAR_DES", "VIVPAR_UT"]]
    ok = un[cols].notna().all(axis=1)
    for (loc, r_), x in un[ok].groupby(["cve_loc", "anillo_ini"]):
        viv_loc = t20[t20.CVE_LOC == loc].VIVTOT.sum()
        filas.append({"nivel": "anillo_unidades", "cve_loc": loc, "localidad": URBANAS[loc], "anillo_ini": r_,
                      "anillo_m": f"{int(r_)}–{int(r_) + ANILLO}", "unidades": len(x),
                      **x[cols].sum().to_dict(),
                      "cobertura_viviendas_2020_loc_pct": round(100 * x.VIVTOT_2020.sum() / viv_loc, 1)})
    # (d) por localidad, totales publicados (Chupícuaro 2010 no tiene tabla por manzana: ITER 2010)
    for loc, nom in URBANAS.items():
        r = {"nivel": "localidad", "cve_loc": loc, "localidad": nom}
        for anio in (2010, 2020):
            it = pd.read_csv(P / f"iter{anio}_acambaro.csv", dtype=str)
            it = it[it.LOC == loc].iloc[0]
            for k in ["POBTOT", "VIVTOT", "VIVPAR_DES", "VIVPAR_UT"]:
                r[f"{k}_{anio}"] = float(num(pd.Series([it[k]])).iloc[0])
        filas.append(r)
    d = pd.DataFrame(filas)
    for anio in (2010, 2020):
        vt = d[f"VIVTOT_{anio}"]
        d[f"pct_deshabitadas_{anio}"] = (100 * d.get(f"VIVPAR_DES_{anio}") / vt).round(1)
        d[f"pct_uso_temporal_{anio}"] = (100 * d.get(f"VIVPAR_UT_{anio}") / vt).round(1)
    d["cambio_pob"] = d.POBTOT_2020 - d.POBTOT_2010
    d["cambio_viviendas"] = d.VIVTOT_2020 - d.VIVTOT_2010
    d["cambio_deshabitadas"] = d.get("VIVPAR_DES_2020") - d.get("VIVPAR_DES_2010")
    return d, m10, unidad


# --- 5. Tipología -----------------------------------------------------------------

def tipologia(cu, viv, dec, unidad, crit=CRITERIOS, excluir=None):
    t = cu[cu.periodo.isin(GRUPOS)].copy()
    if excluir:
        t = t[[(c, p) not in excluir for c, p in zip(t.CVEGEO, t.periodo)]]
    filas = []
    for (loc, ag), x in t.groupby(["CVE_LOC", "CVE_AGEB"]):
        sup = x.superficie_m2.sum()
        pob = x.POBTOT.fillna(0).sum()
        r = {"cve_loc": loc, "localidad": URBANAS[loc], "cve_ageb": ag, "cuadras": len(x),
             "poblacion_2020": int(pob), "superficie_ha": round(sup / 1e4, 1),
             "frac_sup_nueva": round(x.superficie_m2[x.periodo != CONSOL].sum() / sup, 3),
             "frac_sup_nueva_post2020": round(x.superficie_m2[x.periodo == N20].sum() / sup, 3),
             "dist_centro_m": round(float(x.dist_centro_m.median()))}
        lejos = []
        for cat in BASICOS:
            u = acc11.umbral(cat, acc11.UMBRALES_CIUDAD)[1]
            l = x[f"d_{cat}"] > u
            frac = x.POBTOT[l].sum() / pob if pob else x.superficie_m2[l].sum() / sup
            r[f"frac_lejos_{cat}"] = round(float(frac), 3)
            lejos.append(frac > 0.5)
        r["servicios_lejos"] = int(sum(lejos))
        r["medida_lejania"] = "población" if pob else "superficie (sin población)"
        # Viviendas no habitadas = viviendas − habitadas, sumando las cuadras donde "habitadas" es
        # visible (solo 51 de 1 620 cuadras la ocultan; en la ciudad da 25.9 % contra 26.1 % del
        # total publicado de deshabitadas + uso temporal).
        a = viv[(viv.nivel == "ageb") & (viv.cve_loc == loc) & (viv.cve_ageb == ag) & (viv.grupo == "todas")]
        r["viviendas_2020"] = int(a.viviendas_total.iloc[0]) if len(a) else 0
        r["pct_no_habitadas"] = a.pct_no_habitadas_visible.iloc[0] if len(a) else np.nan
        u = unidad.get(("20", loc, ag))
        du = dec[(dec.nivel == "unidad") & (dec.unidad == u)]
        r["unidad_2010_2020"] = u
        r["cambio_pob_unidad"] = float(du.cambio_pob.iloc[0]) if len(du) else np.nan
        filas.append(r)
    t = pd.DataFrame(filas)
    nueva = t.frac_sup_nueva >= crit["frac_sup_nueva"]
    base = t[t.pct_no_habitadas.notna() & ~nueva & (t.viviendas_2020 >= crit["min_viviendas"])]
    if crit["corte_por"] == "localidad":
        corte = t.cve_loc.map(base.groupby("cve_loc").pct_no_habitadas.quantile(crit["percentil_no_habitadas"]))
    else:
        corte = pd.Series(base.pct_no_habitadas.quantile(crit["percentil_no_habitadas"]), index=t.index)
    t["corte_no_habitadas_pct"] = corte.round(1)
    desat = t.servicios_lejos >= crit["servicios_lejos"]
    vacia = (t.pct_no_habitadas >= corte) & (t.viviendas_2020 >= crit["min_viviendas"]) & (t.cambio_pob_unidad < 0)
    t["clase"] = np.select([nueva & desat, nueva, vacia, desat],
                           ["nueva y desatendida", "nueva y bien servida", "consolidada y vaciándose",
                            "consolidada desatendida"], default="consolidada estable")
    t["tambien_desatendida"] = vacia & ~nueva & desat
    return t


def main():
    cu, cen = antiguedad()
    v = {}
    v["cuadras_por_periodo"] = {f"{URBANAS[l]} | {p}": int(n) for (l, p), n in cu.groupby(["CVE_LOC", "periodo"]).size().items()}
    v["superficie_ha_por_periodo"] = {f"{URBANAS[l]} | {p}": round(float(s) / 1e4, 1)
                                      for (l, p), s in cu.groupby(["CVE_LOC", "periodo"]).superficie_m2.sum().items()}
    v["poblacion_por_periodo"] = {f"{URBANAS[l]} | {p}": int(s) for (l, p), s in cu.groupby(["CVE_LOC", "periodo"]).POBTOT.sum().items()}
    v["localidad_no_cartografiada_2010"] = int((cu.localidad_ya_cartografiada_2010 == 0).sum())
    v["dist_centro_mediana_m"] = {f"{URBANAS[l]} | {p}": float(s)
                                  for (l, p), s in cu.groupby(["CVE_LOC", "periodo"]).dist_centro_m.median().items()}
    # Chequeo: población de todas las cuadras = la que usó 11 (resumen por localidad)
    res = pd.read_csv(P / "acceso_resumen_por_localidad.csv")
    v["chequeo_poblacion"] = {URBANAS[l]: int(s) for l, s in cu.groupby("CVE_LOC").POBTOT.sum().items()}

    excl = zonas_no()
    v["verificacion_zonas"] = "no está en el release: resultados provisionales" if excl is None else \
        f"{len(excl)} cuadras en zonas marcadas 'no'"

    tab, an = acceso(cu)
    tab["provisional"] = excl is None
    per = periferia(an)
    if excl:
        t2, a2 = acceso(cu, excl)
        t2["sensibilidad"] = "sin zonas marcadas 'no'"
        tab = pd.concat([tab.assign(sensibilidad="todas"), t2], ignore_index=True)
    viv = viviendas_2020(cu)
    dec, m10, unidad = decada(cu, cen)
    v["manzanas_2010_fuera_de_ageb_2020"] = int(m10.fuera_ageb_2020.sum())
    v["manzanas_2010_sin_censo"] = int(m10.POBTOT.isna().sum())
    v["manzanas_2010_deshabitadas_oculto"] = f"{int(m10.VIVPAR_DES.isna().sum())} de {len(m10)}"
    v["unidades_comparables"] = int(dec[dec.nivel == "unidad"].shape[0])

    tip = tipologia(cu, viv, dec, unidad, excluir=excl)
    v["tipologia"] = tip.clase.value_counts().to_dict()
    v["tipologia_corte_no_habitadas_pct"] = tip.groupby("localidad").corte_no_habitadas_pct.first().to_dict()
    sens = []
    for k, alts in ALTERNATIVAS.items():
        for a in alts:
            t2 = tipologia(cu, viv, dec, unidad, CRITERIOS | {k: a}, excl)
            cambia = (t2.clase != tip.clase)
            sens.append({"criterio": k, "valor_base": CRITERIOS[k], "valor_alternativo": a,
                         "agebs_que_cambian": int(cambia.sum()),
                         "detalle": "; ".join(f"{l}-{g}: {x} → {y}" for l, g, x, y in zip(
                             tip.cve_loc[cambia], tip.cve_ageb[cambia], tip.clase[cambia], t2.clase[cambia])),
                         **{f"n_{c}": int((t2.clase == c).sum()) for c in sorted(set(tip.clase) | set(t2.clase))}})

    cols = ["CVEGEO", "CVE_LOC", "localidad", "CVE_AGEB", "origen", "periodo", "frac_ya_existia",
            "superficie_m2", "dist_centro_m", "anillo_m", "sector", "POBTOT", "VIVTOT", "TVIVHAB",
            "VIVPAR_DES", "VIVPAR_UT"] + [f"d_{c}" for c in SERVICIOS]
    out = cu[cols + ["geometry"]].copy()
    out["superficie_m2"] = out.superficie_m2.round(0)
    out.to_file(P / "cuadras_antiguedad.gpkg", layer="cuadras", driver="GPKG")
    out.drop(columns="geometry").to_csv(P / "cuadras_antiguedad.csv", index=False)
    tab.to_csv(P / "crecimiento_acceso.csv", index=False)
    an.to_csv(P / "crecimiento_acceso_por_anillo.csv", index=False)
    per.to_csv(P / "crecimiento_acceso_periferia.csv", index=False)
    viv.to_csv(P / "crecimiento_viviendas.csv", index=False)
    dec.to_csv(P / "crecimiento_viviendas_2010_2020.csv", index=False)
    tip.to_csv(P / "tipologia_ageb.csv", index=False)
    pd.DataFrame(sens).to_csv(P / "tipologia_sensibilidad.csv", index=False)
    v["chequeo_poblacion_resumen_11"] = {
        r.localidad: int(r.pob_total) for r in res[(res.categoria == "preescolar") & (res.umbral == "principal")
                                                   & (res.grupo == "Población total")].itertuples()
        if r.localidad in URBANAS.values()}
    (P / "validacion_fase4b.json").write_text(json.dumps(v, ensure_ascii=False, indent=1, default=str))
    print(json.dumps(v, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
