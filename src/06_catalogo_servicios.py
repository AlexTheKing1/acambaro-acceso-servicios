"""06 · Catálogo de servicios (fase 2).

Junta en un solo catálogo los servicios que se van a medir, a partir de las dos
fuentes oficiales que sí están disponibles hoy:

  - DENUE, corte 05_2026 (data/processed/denue_acambaro_buffer10km.csv):
    establecimientos con nombre, actividad (SCIAN) y sector público/privado.
  - Marco Geoestadístico EIC 2025, capas de servicios (puntos y áreas)
    (data/processed/mg_eic2025_servicios_buffer10km.gpkg): escuelas, centros
    de salud y mercados dibujados y verificados en campo por INEGI en 2025,
    sin sector y casi siempre sin nombre.

CLUES (salud) y el catálogo de escuelas de la SEP todavía no están (release
"datos-crudos" vacío). Cuando lleguen, este catálogo se contrasta con ellos; por
ahora es la mejor versión posible con lo oficial disponible y se marca así.

Ambas fuentes se cubren en el municipio y en la franja de 10 km (Gto. y Mich.).

Salidas en data/processed/:
  servicios.gpkg            capa "registros": cada registro original clasificado
                            capa "sedes": un punto por sitio y tipo (para distancias)
  servicios_sedes.csv       la capa "sedes" en tabla, con latitud y longitud
  validacion_fase2.json     cifras de los chequeos (docs/validacion.md)

Un mismo sitio aparece varias veces: una escuela con dos turnos tiene dos
registros en el DENUE, y una escuela del MG puede venir como punto y como área.
Para medir distancias basta un punto por sitio: los registros del mismo tipo a
menos de DIST_MISMA_SEDE metros se agrupan en una "sede".
"""

import json
import unicodedata
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"

DIST_MISMA_SEDE = 60     # m: registros del mismo tipo más cerca que esto son el mismo sitio
DIST_AREA_PUNTO = 50     # m: un área del MG con un punto del mismo tipo a esta distancia es duplicado
DIST_MG_DENUE = 150      # m: un registro solo del DENUE se une a la sede del MG del mismo tipo más cercana

# El DENUE codifica algunas unidades de primer nivel como hospital (622112) u
# "otros consultorios" (621399). Por su nombre son primer nivel: centros de
# salud, UMAPS (Unión Multidisciplinaria de Atención Primaria para la Salud),
# unidades de medicina familiar y unidades médicas rurales. Se reclasifican.
PRIMER_NIVEL_POR_NOMBRE = r"UMAPS|MEDICA FAMILIAR|MEDICINA FAMILIAR|UNIDAD MEDICA RURAL|CENTRO DE SALUD"

# Tipos que se analizan (D15) y su orden en los reportes
TIPOS = ["preescolar", "primaria", "secundaria", "bachillerato", "salud_primer_nivel", "abasto"]
# Tipos que se guardan como contexto pero no entran al cálculo de distancias
CONTEXTO = ["escuela_varios_niveles", "consultorio_privado", "hospital"]

# DENUE: código SCIAN -> (tipo, subtipo, sector)
SCIAN = {
    "611111": ("preescolar", "preescolar", "privado"),
    "611112": ("preescolar", "preescolar", "público"),
    "611121": ("primaria", "primaria", "privado"),
    "611122": ("primaria", "primaria", "público"),
    "611131": ("secundaria", "secundaria general", "privado"),
    "611132": ("secundaria", "secundaria general", "público"),
    "611141": ("secundaria", "secundaria técnica", "privado"),
    "611142": ("secundaria", "secundaria técnica", "público"),
    "611151": ("bachillerato", "media técnica terminal", "privado"),
    "611152": ("bachillerato", "media técnica terminal", "público"),
    "611161": ("bachillerato", "media superior", "privado"),
    "611162": ("bachillerato", "media superior", "público"),
    "611171": ("escuela_varios_niveles", "varios niveles", "privado"),
    "611172": ("escuela_varios_niveles", "varios niveles", "público"),
    "621112": ("salud_primer_nivel", "consultorio de medicina general", "público"),
    "621116": ("salud_primer_nivel", "clínica de consultorios", "público"),
    "621111": ("consultorio_privado", "consultorio de medicina general", "privado"),
    "621115": ("consultorio_privado", "clínica de consultorios", "privado"),
    "622111": ("hospital", "hospital general", "privado"),
    "622112": ("hospital", "hospital general", "público"),
    "622311": ("hospital", "hospital de especialidades", "privado"),
    "622312": ("hospital", "hospital de especialidades", "público"),
    "462111": ("abasto", "supermercado", "privado"),
    "462112": ("abasto", "minisúper", "privado"),
    "461110": ("abasto", "abarrotes", "privado"),
}

# MG: (GEOGRAFICO, TIPO) -> (tipo, subtipo). "Medio Superior" es la grafía del MG 2020.
MG_TIPOS = {
    ("Escuela", "Preescolar"): ("preescolar", "preescolar"),
    ("Escuela", "Primaria"): ("primaria", "primaria"),
    ("Escuela", "Secundaria"): ("secundaria", "secundaria"),
    ("Escuela", "Media Superior"): ("bachillerato", "media superior"),
    ("Escuela", "Medio Superior"): ("bachillerato", "media superior"),
    ("Escuela", "Mixto"): ("escuela_varios_niveles", "varios niveles"),
    ("Centro de Asistencia Médica", "Centro de Salud"): ("salud_primer_nivel", "centro de salud"),
    ("Centro de Asistencia Médica", "Hospital"): ("hospital", "hospital"),
    ("Mercado", None): ("abasto", "mercado"),
}

# Quién tiene la competencia (D17, propuesta): sirve para separar recomendaciones.
COMPETENCIA = {
    "preescolar": "estatal/federal (educación)",
    "primaria": "estatal/federal (educación)",
    "secundaria": "estatal/federal (educación)",
    "bachillerato": "estatal/federal (educación)",
    "salud_primer_nivel": "estatal/federal (salud)",
    "hospital": "estatal/federal (salud)",
    "escuela_varios_niveles": "estatal/federal (educación)",
    "consultorio_privado": "privado",
}
ENTIDADES = {"11": "Guanajuato", "16": "Michoacán", "22": "Querétaro"}


def sin_acentos(texto):
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return " ".join(t.upper().split())


def competencia(tipo, subtipo, sector):
    if subtipo == "mercado":
        return "municipal (mercados, art. 115 constitucional)"
    if tipo == "abasto":
        return "privado"
    if sector == "privado":
        return "privado (supervisión estatal/federal)"
    return COMPETENCIA.get(tipo, "")


def registros_denue(crs):
    d = pd.read_csv(P / "denue_acambaro_buffer10km.csv", dtype=str)
    d = d.apply(lambda c: c.str.strip())  # el DENUE rellena nombres con espacios
    g = gpd.GeoDataFrame(d, geometry=gpd.points_from_xy(d.longitud.astype(float), d.latitud.astype(float)),
                         crs="EPSG:4326").to_crs(crs)
    g["en_acambaro"] = g.en_acambaro == "True"
    cl = g[g.codigo_act.isin(SCIAN)].copy()
    cl[["tipo", "subtipo", "sector"]] = cl.codigo_act.map(SCIAN).apply(pd.Series).to_numpy()
    cl["reclasificado"] = False
    salud = g[g.codigo_act.str[:3].isin(["621", "622"])
              & g.nom_estab.map(sin_acentos).str.contains(PRIMER_NIVEL_POR_NOMBRE)].copy()
    salud = salud[~salud.codigo_act.isin(["621112", "621116"])]  # ya son primer nivel
    salud[["tipo", "subtipo", "sector"]] = ["salud_primer_nivel", "primer nivel (por nombre)", "público"]
    salud["reclasificado"] = True
    cl = pd.concat([cl[~cl.id.isin(salud.id)], salud])

    # Mercados públicos: el DENUE registra cada local; se agrupan por mercado
    # (mismo nombre de centro comercial en la misma localidad) en un solo punto.
    m = g[g.tipoCenCom == "MERCADO PUBLICO"].copy()
    m["clave_mercado"] = m.cve_ent + m.cve_mun + m.cve_loc + "|" + m.nom_CenCom.map(sin_acentos)
    mercados = (m.groupby("clave_mercado")
                .agg(nom_estab=("nom_CenCom", "first"), cve_ent=("cve_ent", "first"),
                     cve_mun=("cve_mun", "first"), municipio=("municipio", "first"),
                     cve_loc=("cve_loc", "first"), localidad=("localidad", "first"),
                     en_acambaro=("en_acambaro", "first"), n_locales=("id", "size"),
                     x=("geometry", lambda s: float(np.median(s.x))),
                     y=("geometry", lambda s: float(np.median(s.y))))
                .reset_index())
    mercados = gpd.GeoDataFrame(mercados, geometry=gpd.points_from_xy(mercados.x, mercados.y), crs=crs)
    mercados["id"] = "mercado:" + mercados.clave_mercado
    mercados[["tipo", "subtipo", "sector"]] = ["abasto", "mercado", "público"]
    mercados["codigo_act"] = "mercado público (locales agrupados)"

    cols = ["id", "nom_estab", "codigo_act", "tipo", "subtipo", "sector", "cve_ent", "cve_mun",
            "municipio", "cve_loc", "localidad", "en_acambaro", "geometry"]
    mercados["reclasificado"] = False
    r = pd.concat([cl[cols + ["reclasificado"]], mercados[cols + ["reclasificado", "n_locales"]]], ignore_index=True)
    r = r.rename(columns={"id": "id_origen", "nom_estab": "nombre"})
    r["fuente"] = "DENUE"
    return gpd.GeoDataFrame(r, crs=crs), len(m)


def registros_mg(crs):
    capas = []
    excluidos = {}
    for capa in ["puntos", "areas"]:
        g = gpd.read_file(P / "mg_eic2025_servicios_buffer10km.gpkg", layer=capa).to_crs(crs)
        g["capa_mg"] = capa
        if capa == "areas":
            g["geometry_area"] = g.geometry
            g["geometry"] = g.geometry.representative_point()
        capas.append(g)
    g = gpd.GeoDataFrame(pd.concat(capas, ignore_index=True), crs=crs)
    clave = list(zip(g.GEOGRAFICO, g.TIPO))
    g["tipo_subtipo"] = [MG_TIPOS.get(k, MG_TIPOS.get((k[0], None))) for k in clave]
    g = g[g.tipo_subtipo.notna()].copy()
    g["tipo"] = g.tipo_subtipo.str[0]
    g["subtipo"] = g.tipo_subtipo.str[1]

    no_operan = g[g.CONDICION.isin(["Fuera de Uso", "En Construcción"])]
    excluidos["fuera_de_uso_o_en_construccion"] = no_operan[["tipo", "CONDICION", "capa_mg"]].astype(str).to_dict("records")
    g = g[~g.index.isin(no_operan.index)].copy()

    # Un área del MG con un punto del mismo tipo encima (o a <= 50 m) es el mismo sitio.
    pts, areas = g[g.capa_mg == "puntos"], g[g.capa_mg == "areas"]
    dup = []
    for i, a in areas.iterrows():
        mismos = pts[pts.tipo == a.tipo]
        if len(mismos) and mismos.distance(a.geometry_area).min() <= DIST_AREA_PUNTO:
            dup.append(i)
    excluidos["areas_duplicadas_de_un_punto"] = len(dup)
    excluidos["areas_sin_punto"] = int(len(areas) - len(dup))
    g = g.drop(index=dup)

    nombre = g.NOMSERV.where(~g.NOMSERV.isin(["Ninguno", "No Aplica"]))
    r = gpd.GeoDataFrame({
        "id_origen": "MG:" + g.capa_mg + ":" + g.CVEGEO + ":" + g.TIPO + ":" + g.index.astype(str),
        "nombre": nombre, "codigo_act": g.GEOGRAFICO + " / " + g.TIPO,
        "tipo": g.tipo, "subtipo": g.subtipo, "sector": "desconocido",
        "cve_ent": g.CVE_ENT, "cve_mun": g.CVE_MUN, "municipio": None, "cve_loc": g.CVE_LOC,
        "localidad": None, "en_acambaro": g.en_acambaro.astype(bool), "fuente": "MG",
        "capa_mg": g.capa_mg,
    }, geometry=g.geometry.values, crs=crs)
    return r, excluidos


def agrupar_sedes(reg):
    """Agrupa en una sede los registros del mismo tipo a menos de DIST_MISMA_SEDE m."""
    reg = reg.copy()
    reg["id_sede"] = None
    for tipo in reg.tipo.unique():
        sel = reg[reg.tipo == tipo]
        if tipo == "abasto":
            # Tiendas: cada registro es un comercio distinto aunque estén juntos;
            # solo se agrupa el mercado del DENUE con el del MG.
            grupos = pd.Series(range(len(sel)), index=sel.index)
            merc = sel[sel.subtipo == "mercado"]
            if len(merc):
                comp = componentes(merc, DIST_MISMA_SEDE * 2)
                grupos.loc[merc.index] = comp + len(sel)
        else:
            grupos = componentes(sel, DIST_MISMA_SEDE)
            # Coordenadas de una fuente y otra pueden diferir más que DIST_MISMA_SEDE:
            # un grupo solo del DENUE se une al grupo con MG más cercano a <= DIST_MG_DENUE.
            con_mg = set(grupos[sel.fuente == "MG"])
            mg = sel[sel.fuente == "MG"]
            for k in set(grupos) - con_mg:
                miembros = sel[grupos == k]
                if not len(mg):
                    break
                dist = mg.distance(miembros.geometry.union_all())
                if dist.min() <= DIST_MG_DENUE:
                    grupos[grupos == k] = grupos[dist.idxmin()]
        reg.loc[sel.index, "id_sede"] = [f"{tipo}-{int(k):05d}" for k in grupos]

    # Renumerar consecutivo por tipo
    for tipo in reg.tipo.unique():
        sel = reg.tipo == tipo
        codigos = {k: f"{tipo}-{n + 1:04d}" for n, k in enumerate(pd.unique(reg.loc[sel, "id_sede"]))}
        reg.loc[sel, "id_sede"] = reg.loc[sel, "id_sede"].map(codigos)

    def primero(s):
        s = s.dropna()
        return s.iloc[0] if len(s) else None

    filas = []
    for id_sede, s in reg.groupby("id_sede", sort=False):
        mg = s[s.fuente == "MG"]
        den = s[s.fuente == "DENUE"]
        # Ubicación: la del MG si existe (verificada en campo en 2025), si no la del DENUE.
        base = mg if len(mg) else den
        geom = base.geometry.iloc[0] if len(base) == 1 else base.geometry.union_all().centroid
        sectores = set(den.sector) - {"desconocido"}
        sector = sectores.pop() if len(sectores) == 1 else ("mixto" if sectores else "desconocido")
        subtipos = sorted(set(s.subtipo))
        filas.append({
            "id_sede": id_sede, "tipo": s.tipo.iloc[0], "subtipo": "; ".join(subtipos),
            "nombre": primero(den.nombre) or primero(mg.nombre),
            "sector": sector,
            "fuentes": "+".join(sorted(set(s.fuente), reverse=True)),
            "n_registros_mg": len(mg), "n_registros_denue": len(den),
            "n_locales_mercado": int(den.n_locales.sum()) if "n_locales" in den and den.n_locales.notna().any() else None,
            "cve_ent": s.cve_ent.iloc[0], "entidad": ENTIDADES.get(s.cve_ent.iloc[0], s.cve_ent.iloc[0]),
            "cve_mun": s.cve_mun.iloc[0], "municipio": primero(s.municipio),
            "cve_loc": s.cve_loc.iloc[0], "localidad": primero(s.localidad),
            "en_acambaro": bool(s.en_acambaro.any()),
            "analizado": s.tipo.iloc[0] in TIPOS,
            "geometry": geom,
        })
    sedes = gpd.GeoDataFrame(filas, crs=reg.crs)
    sedes["competencia"] = [competencia(t, st, se) for t, st, se in zip(sedes.tipo, sedes.subtipo, sedes.sector)]
    return reg, sedes


def componentes(g, dist):
    """Etiqueta de grupo: puntos unidos por cadenas de vecinos a <= dist m."""
    zonas = gpd.GeoDataFrame(geometry=[g.buffer(dist / 2).union_all()], crs=g.crs).explode(ignore_index=True)
    j = gpd.sjoin(g[["geometry"]], zonas, predicate="intersects", how="left")
    j = j[~j.index.duplicated()]
    return j.index_right.astype(int)


def nombres_localidad(sedes):
    """Completa municipio y localidad de las sedes que solo vienen del MG."""
    loc = gpd.read_file(P / "localidades2020.gpkg")[["LOC", "NOM_LOC"]]
    nombres = dict(zip("11002" + loc.LOC, loc.NOM_LOC))
    falta = sedes.localidad.isna() & sedes.en_acambaro
    sedes.loc[falta, "localidad"] = (sedes.cve_ent + sedes.cve_mun + sedes.cve_loc)[falta].map(nombres)
    # Municipios vecinos: nombre tomado del propio DENUE (misma clave de municipio)
    con_nombre = sedes.dropna(subset=["municipio"])
    municipios = dict(zip(con_nombre.cve_ent + con_nombre.cve_mun, con_nombre.municipio))
    sedes["municipio"] = sedes.municipio.fillna((sedes.cve_ent + sedes.cve_mun).map(municipios))
    return sedes


def coincidencia_mg_denue(reg, tipo, dist):
    """Para el tipo dado y dentro de Acámbaro: cuántos registros de cada fuente
    tienen uno de la otra fuente a <= dist m."""
    sel = reg[(reg.tipo == tipo) & reg.en_acambaro]
    mg, den = sel[sel.fuente == "MG"], sel[sel.fuente == "DENUE"]
    if not len(mg) or not len(den):
        return {"mg": len(mg), "denue": len(den)}
    d_mg = mg.geometry.apply(lambda p: den.distance(p).min())
    d_den = den.geometry.apply(lambda p: mg.distance(p).min())
    return {
        "mg": len(mg), "denue": len(den),
        "mg_con_denue_cerca": int((d_mg <= dist).sum()),
        "denue_con_mg_cerca": int((d_den <= dist).sum()),
        "mediana_m_mg_a_denue_si_coinciden": round(float(d_mg[d_mg <= dist].median()), 1)
        if (d_mg <= dist).any() else None,
    }


def main():
    municipio = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="municipio")
    crs = municipio.crs
    den, locales_mercado = registros_denue(crs)
    mg, excluidos = registros_mg(crs)
    reg = gpd.GeoDataFrame(pd.concat([mg, den], ignore_index=True), crs=crs)
    reg, sedes = agrupar_sedes(reg)
    sedes = nombres_localidad(sedes)
    reg["dist_limite_mun_m"] = reg.distance(municipio.geometry.iloc[0].boundary).round(0)
    reg.loc[reg.en_acambaro, "dist_limite_mun_m"] = 0
    sedes["dist_fuera_mun_m"] = sedes.distance(municipio.geometry.iloc[0]).round(0)

    salida = P / "servicios.gpkg"
    salida.unlink(missing_ok=True)
    reg.drop(columns=[c for c in ["n_locales"] if c in reg]).to_file(salida, layer="registros", driver="GPKG")
    sedes.to_file(salida, layer="sedes", driver="GPKG")
    ll = sedes.to_crs("EPSG:4326")
    tabla = sedes.drop(columns="geometry").assign(lat=ll.geometry.y.round(6), lon=ll.geometry.x.round(6))
    tabla.to_csv(P / "servicios_sedes.csv", index=False)

    # --- Cifras para docs/validacion.md ----------------------------------------
    v = {"excluidos_mg": {k: (len(x) if isinstance(x, list) else x) for k, x in excluidos.items()},
         "excluidos_mg_detalle": excluidos["fuera_de_uso_o_en_construccion"],
         "locales_denue_en_mercados_publicos": locales_mercado}
    v["registros_por_tipo_fuente"] = (reg.assign(donde=np.where(reg.en_acambaro, "Acámbaro", "franja 10 km"))
                                      .assign(col=lambda r: r.fuente + " " + r.donde)
                                      .groupby(["tipo", "col"]).size().unstack()
                                      .fillna(0).astype(int).to_dict("index"))
    t = sedes.assign(donde=np.where(sedes.en_acambaro, "Acámbaro", "franja 10 km"))
    v["sedes_por_tipo"] = t.groupby(["tipo", "donde"]).size().unstack().fillna(0).astype(int).to_dict("index")
    v["sedes_por_tipo_y_fuentes_acambaro"] = (t[t.en_acambaro].groupby(["tipo", "fuentes"]).size()
                                              .unstack().fillna(0).astype(int).to_dict("index"))
    v["sedes_por_tipo_y_sector_acambaro"] = (t[t.en_acambaro].groupby(["tipo", "sector"]).size()
                                             .unstack().fillna(0).astype(int).to_dict("index"))
    v["sedes_abasto_por_subtipo"] = (t[t.tipo == "abasto"].groupby(["subtipo", "donde"]).size()
                                     .unstack().fillna(0).astype(int).to_dict("index"))
    v["sedes_franja_por_entidad"] = (t[~t.en_acambaro].groupby(["tipo", "entidad"]).size()
                                     .unstack().fillna(0).astype(int).to_dict("index"))
    v["coincidencia_mg_denue_150m"] = {tp: coincidencia_mg_denue(reg, tp, 150) for tp in
                                       ["preescolar", "primaria", "secundaria", "bachillerato",
                                        "salud_primer_nivel", "hospital", "escuela_varios_niveles"]}
    v["denue_reclasificados_primer_nivel"] = (reg[reg.reclasificado.fillna(False).astype(bool)]
                                              [["nombre", "codigo_act", "municipio", "localidad"]].to_dict("records"))
    v["parametros"] = {"DIST_MISMA_SEDE_m": DIST_MISMA_SEDE, "DIST_AREA_PUNTO_m": DIST_AREA_PUNTO,
                       "DIST_MG_DENUE_m": DIST_MG_DENUE}
    (P / "validacion_fase2.json").write_text(json.dumps(v, ensure_ascii=False, indent=1, default=str))
    print(json.dumps(v, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
