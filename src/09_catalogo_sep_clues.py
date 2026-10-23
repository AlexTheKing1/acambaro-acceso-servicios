"""09 · Catálogo de servicios con SEP y CLUES (fase 3, paso 1).

Contrasta el catálogo de la fase 2 (data/processed/servicios.gpkg, MG EIC 2025 +
DENUE; no se modifica) con los dos registros administrativos oficiales:

  - Catálogo de centros de trabajo de la SEP, Gto. y Mich.
    (data/processed/sep_escuelas_buffer10km.csv): nivel, sostenimiento
    (público/privado), estatus y turnos de cada escuela.
  - CLUES, corte agosto 2026 (data/processed/clues_buffer10km.csv): institución,
    tipología, nivel de atención y estatus de operación de cada establecimiento.

Para cada tipo de servicio:
  1. Los registros de SEP (o CLUES) del mismo tipo a menos de DIST_MISMA_SEDE m se
     juntan en un grupo (varios turnos o claves en el mismo edificio, D16).
  2. Un grupo confirma a la sede de la fase 2 del mismo tipo si está a
     <= DIST_CONFIRMA m, o si son vecinos más cercanos mutuos a <= DIST_MUTUO m
     (las coordenadas de la SEP a veces caen a media cuadra).
  3. Los grupos que no confirman a ninguna sede son sedes nuevas.
  4. Las sedes de la fase 2 sin registro que las confirme se conservan, marcadas
     como "no confirmada" (el MG 2025 se verificó en campo; no se borran sin
     evidencia). Se usan en la medida principal y se quitan en la sensibilidad D28.

Salidas en data/processed/:
  servicios_fase3.gpkg          capa "sedes" (una fila por sitio) y capa "registros_sep_clues"
  servicios_sedes_fase3.csv     la capa "sedes" en tabla, con latitud y longitud
  validacion_fase3_catalogo.json cifras para docs/validacion.md
Además agrega a docs/verificar_servicios_muestra.csv la columna
"confirmado_sep_clues" (sin regenerar la muestra).
"""

import importlib.util
import json
import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
DOCS = RAIZ / "docs"

spec = importlib.util.spec_from_file_location("cat06", RAIZ / "src" / "06_catalogo_servicios.py")
cat06 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cat06)
componentes, sin_acentos, competencia = cat06.componentes, cat06.sin_acentos, cat06.competencia

DIST_MISMA_SEDE = cat06.DIST_MISMA_SEDE   # 60 m
DIST_CONFIRMA = cat06.DIST_MG_DENUE       # 150 m
DIST_MUTUO = 300                          # m, vecinos más cercanos mutuos

NIVEL_SEP = {"PREESCOLAR": "preescolar", "PRIMARIA": "primaria", "SECUNDARIA": "secundaria",
             "MEDIA SUPERIOR": "bachillerato", "CAM": "escuela_varios_niveles"}
# Modalidad no escolarizada (D23): no se mide la distancia, se registra aparte.
NO_ESCOLARIZADO = r"PREPARATORIA ABIERTA|ENSENANZA ABIERTA|NO ESCOLARIZAD|A DISTANCIA|EN LINEA"
# Escuelas dentro de un centro penitenciario: no están abiertas a la población.
PENITENCIARIO = r"CERESO|CEFERESO|PENITENCIARI|READAPTACION"

# CLUES: instituciones públicas que dan consulta de primer nivel (D20)
PUBLICAS = ["SECRETARIA DE SALUD", "SERVICIOS DE SALUD IMSS BIENESTAR",
            "INSTITUTO MEXICANO DEL SEGURO SOCIAL", "INSTITUTO MEXICANO DEL SEGURO SOCIAL REGIMEN BIENESTAR",
            "INSTITUTO DE SEGURIDAD Y SERVICIOS SOCIALES DE LOS TRABAJADORES DEL ESTADO",
            "SERVICIOS MEDICOS ESTATALES", "SERVICIOS MEDICOS MUNICIPALES"]
SIGLAS = {"SECRETARIA DE SALUD": "SSG (Secretaría de Salud de Guanajuato)",
          "SERVICIOS DE SALUD IMSS BIENESTAR": "IMSS-Bienestar",
          "INSTITUTO MEXICANO DEL SEGURO SOCIAL": "IMSS",
          "INSTITUTO MEXICANO DEL SEGURO SOCIAL REGIMEN BIENESTAR": "IMSS-Bienestar (régimen)",
          "INSTITUTO DE SEGURIDAD Y SERVICIOS SOCIALES DE LOS TRABAJADORES DEL ESTADO": "ISSSTE",
          "SERVICIOS MEDICOS PRIVADOS": "privado"}
# Tipologías con médicos de base que dan consulta familiar aunque el CLUES las
# clasifique de segundo nivel (hospital de subzona con medicina familiar del IMSS).
CON_MEDICINA_FAMILIAR = r"MEDICINA FAMILIAR|ATENCION FAMILIAR"


def claves_texto(d):
    return {" | ".join(map(str, k)) if isinstance(k, tuple) else k: n for k, n in d.items()}


def puntos(t, lat, lon, crs):
    return gpd.GeoDataFrame(t, geometry=gpd.points_from_xy(t[lon].astype(float), t[lat].astype(float)),
                            crs="EPSG:4326").to_crs(crs)


# --- SEP ---------------------------------------------------------------------
def registros_sep(crs):
    s = pd.read_csv(P / "sep_escuelas_buffer10km.csv", dtype=str)
    s = s.apply(lambda col: col.str.strip())
    v = {"registros_en_franja": len(s),
         "por_estatus_y_tipo_de_centro": claves_texto(s.groupby(["C_ESTATUS", "C_TIPO"]).size().to_dict())}
    s = s[s.C_TIPO == "ESCUELA"].copy()
    turnos = s[["C_TUNO_1", "C_TUNO_2", "C_TUNO_3"]]
    # El catálogo marca turnos dados de baja con "(INACTIVO)". Si ningún turno opera, no opera.
    turno_activo = turnos.apply(lambda c: c.notna() & ~c.fillna("").str.contains("INACTIVO")).any(axis=1)
    v["escuelas_activas_sin_turno_activo"] = (
        s[(s.C_ESTATUS == "ACTIVO") & ~turno_activo]
        [["CV_CCT", "C_NOMBRE", "INMUEBLE_C_NOM_MUN", "INMUEBLE_C_NOM_LOC", "C_TUNO_1"]].to_dict("records"))
    s["opera"] = (s.C_ESTATUS == "ACTIVO") & turno_activo
    s["tipo"] = s.TIPONIVELSUB_C_SERVICION2.map(NIVEL_SEP)
    v["escuelas_de_otros_niveles_no_usadas"] = s[s.opera & s.tipo.isna()].TIPONIVELSUB_C_SERVICION2.value_counts().to_dict()
    s = s[s.tipo.notna()].copy()
    nombre = s.C_NOMBRE.map(sin_acentos)
    s.loc[nombre.str.contains(NO_ESCOLARIZADO), "tipo"] = "bachillerato_no_escolarizado"
    s.loc[nombre.str.contains(PENITENCIARIO), "tipo"] = "escuela_centro_penitenciario"
    s["sector"] = s.SOSTENIMIENTO_C_CONTROL.map({"PÚBLICO": "público", "PRIVADO": "privado"}).fillna("desconocido")
    s["subtipo_sep"] = s.TIPONIVELSUB_C_SERVICION3.str.lower()
    s["turnos"] = turnos.loc[s.index].apply(lambda f: "; ".join(x for x in f.dropna()), axis=1)
    g = puntos(s, "INMUEBLE_LATITUD", "INMUEBLE_LONGITUD", crs)
    g = g.rename(columns={"CV_CCT": "clave", "C_NOMBRE": "nombre", "INMUEBLE_CV_ENT": "cve_ent",
                          "INMUEBLE_CV_MUN": "cve_mun", "INMUEBLE_C_NOM_MUN": "municipio",
                          "INMUEBLE_CV_LOC": "cve_loc", "INMUEBLE_C_NOM_LOC": "localidad"})
    g["fuente"] = "SEP"
    g["institucion"] = g.SOSTENIMIENTO_C_SUBCONTROL
    g["en_acambaro"] = g.en_acambaro == "True"
    cols = ["clave", "nombre", "tipo", "subtipo_sep", "sector", "institucion", "turnos", "cve_ent", "cve_mun",
            "municipio", "cve_loc", "localidad", "en_acambaro", "fuente", "opera", "geometry"]
    v["escuelas_que_operan_por_tipo"] = (g[g.opera].groupby(["tipo", "en_acambaro"]).size().unstack()
                                         .fillna(0).astype(int).to_dict("index"))
    v["escuelas_sin_operar_por_tipo"] = (g[~g.opera].groupby(["tipo", "en_acambaro"]).size().unstack()
                                         .fillna(0).astype(int).to_dict("index"))
    v["sin_dato_de_matricula"] = ("El catálogo de centros de trabajo no trae matrícula ni número de alumnos "
                                  "(columnas revisadas: " + str(len(s.columns)) + ").")
    return g[cols].copy(), v


# --- CLUES -------------------------------------------------------------------
def tipo_clues(f):
    inst, tipol = f["NOMBRE DE LA INSTITUCION"], sin_acentos(f["NOMBRE DE TIPOLOGIA"])
    tipo_est, nivel = f["NOMBRE TIPO ESTABLECIMIENTO"], f["NIVEL ATENCION"]
    if "CASA DE SALUD" in tipol:
        return "casa_de_salud"          # D27: dato aparte, no cuenta en la medida principal
    if "UNIDAD MOVIL" in tipol:
        return "unidad_movil"           # no tiene sede fija (provisional, ver D29)
    if inst == "SERVICIOS MEDICOS PRIVADOS":
        if tipo_est == "DE HOSPITALIZACIÓN":
            return "hospital"
        return "consultorio_privado" if tipo_est == "DE CONSULTA EXTERNA" else None
    if inst not in PUBLICAS:
        return None                     # DIF, Cruz Roja, Defensa, etc.: no son consulta general a la población
    if re.search(CON_MEDICINA_FAMILIAR, tipol):
        return "salud_primer_nivel"
    if tipo_est == "DE CONSULTA EXTERNA" and nivel == "PRIMER NIVEL":
        return "salud_primer_nivel"
    if tipo_est == "DE HOSPITALIZACIÓN":
        return "hospital"
    return None                         # oficinas, almacenes, apoyo


def registros_clues(crs):
    c = pd.read_csv(P / "clues_buffer10km.csv", dtype=str)
    c = c.apply(lambda col: col.str.strip())  # p. ej. "SERVICIOS DE SALUD IMSS BIENESTAR " trae espacio final
    v = {"registros_en_franja": len(c), "por_estatus": c["ESTATUS DE OPERACION"].value_counts().to_dict()}
    c["opera"] = c["ESTATUS DE OPERACION"] == "EN OPERACION"
    c["tipo"] = c.apply(tipo_clues, axis=1)
    v["en_operacion_por_institucion_tipologia"] = claves_texto(
        c[c.opera].fillna({"tipo": "no se usa"}).groupby(["NOMBRE DE LA INSTITUCION", "NOMBRE DE TIPOLOGIA", "tipo"])
        .size().to_dict())
    c = c[c.tipo.notna()].copy()
    g = puntos(c, "LATITUD", "LONGITUD", crs)
    g = g.rename(columns={"CLUES": "clave", "NOMBRE DE LA UNIDAD": "nombre", "CLAVE DE LA ENTIDAD": "cve_ent",
                          "CLAVE DEL MUNICIPIO": "cve_mun", "MUNICIPIO": "municipio",
                          "CLAVE DE LA LOCALIDAD": "cve_loc", "LOCALIDAD": "localidad"})
    g["sector"] = np.where(g["NOMBRE DE LA INSTITUCION"] == "SERVICIOS MEDICOS PRIVADOS", "privado", "público")
    g["institucion"] = g["NOMBRE DE LA INSTITUCION"].map(SIGLAS).fillna(g["NOMBRE DE LA INSTITUCION"])
    g["subtipo_sep"] = g["NOMBRE DE TIPOLOGIA"].str.lower()
    g["turnos"] = None
    g["fuente"] = "CLUES"
    g["en_acambaro"] = g.en_acambaro == "True"
    cols = ["clave", "nombre", "tipo", "subtipo_sep", "sector", "institucion", "turnos", "cve_ent", "cve_mun",
            "municipio", "cve_loc", "localidad", "en_acambaro", "fuente", "opera", "geometry"]
    v["en_operacion_por_tipo"] = (g[g.opera].groupby(["tipo", "en_acambaro"]).size().unstack()
                                  .fillna(0).astype(int).to_dict("index"))
    v["fuera_de_operacion_por_tipo"] = (g[~g.opera].groupby(["tipo", "en_acambaro"]).size().unstack()
                                        .fillna(0).astype(int).to_dict("index"))
    return g[cols].copy(), v


# --- Cruce -------------------------------------------------------------------
def grupos_registros(reg):
    """Junta registros SEP/CLUES del mismo tipo a <= DIST_MISMA_SEDE m."""
    reg = reg.copy()
    reg["grupo"] = None
    for tipo in reg.tipo.unique():
        sel = reg[reg.tipo == tipo]
        reg.loc[sel.index, "grupo"] = [f"{tipo}|{k}" for k in componentes(sel, DIST_MISMA_SEDE)]
    return reg


def cruzar(sedes, reg, tipos_equivalentes):
    """Asigna cada grupo de registros a una sede de la fase 2 o lo marca como nuevo.
    tipos_equivalentes: tipo del registro -> tipos de sede que puede confirmar."""
    reg = grupos_registros(reg)
    centro = reg.dissolve("grupo").geometry.centroid
    tipo_g = reg.groupby("grupo").tipo.first()
    asign = {}
    como = {}
    for tipo in tipo_g.unique():
        gs = centro[tipo_g == tipo]
        cand = sedes[sedes.tipo.isin(tipos_equivalentes.get(tipo, [tipo]))]
        if not len(cand):
            continue
        # distancia de cada grupo a cada sede candidata
        d = np.array([cand.distance(p).to_numpy() for p in gs])
        mas_cerca_g = d.argmin(axis=1)
        mas_cerca_s = d.argmin(axis=0)
        for i, k in enumerate(gs.index):
            j = mas_cerca_g[i]
            if d[i, j] <= DIST_CONFIRMA:
                asign[k], como[k] = cand.index[j], f"<= {DIST_CONFIRMA} m"
            elif d[i, j] <= DIST_MUTUO and mas_cerca_s[j] == i:
                asign[k], como[k] = cand.index[j], f"vecinos mutuos <= {DIST_MUTUO} m"
    reg["sede_idx"] = reg.grupo.map(asign)
    reg["como_cruzo"] = reg.grupo.map(como)
    reg["dist_a_sede_m"] = [
        round(float(g.distance(sedes.geometry.loc[i])), 0) if pd.notna(i) else None
        for g, i in zip(reg.geometry, reg.sede_idx)]
    return reg


def main():
    sedes = gpd.read_file(P / "servicios.gpkg", layer="sedes")
    crs = sedes.crs
    sep, v_sep = registros_sep(crs)
    clues, v_clues = registros_clues(crs)
    v = {"sep": v_sep, "clues": v_clues}

    sedes["tipo_fase2"] = sedes.tipo
    # Preparatoria abierta del DENUE (D23) y escuelas en penales: fuera de la medida
    nom = sedes.nombre.fillna("").map(sin_acentos)
    sedes.loc[(sedes.tipo == "bachillerato") & nom.str.contains(NO_ESCOLARIZADO), "tipo"] = "bachillerato_no_escolarizado"
    sedes.loc[sedes.tipo.isin(cat06.TIPOS[:4]) & nom.str.contains(PENITENCIARIO), "tipo"] = "escuela_centro_penitenciario"

    equivalentes = {"salud_primer_nivel": ["salud_primer_nivel"],
                    "consultorio_privado": ["consultorio_privado", "salud_primer_nivel"],
                    "hospital": ["hospital", "salud_primer_nivel"]}
    baja = pd.concat([sep[~sep.opera], clues[~clues.opera]], ignore_index=True)
    r_sep = cruzar(sedes, sep[sep.opera], {})
    r_clues = cruzar(sedes, clues[clues.opera], equivalentes)
    reg = pd.concat([r_sep, r_clues], ignore_index=True)

    # --- Sedes de la fase 2 con lo que dicen SEP / CLUES ------------------------
    sedes["confirmado_por"] = ""
    sedes["claves_sep_clues"] = ""
    sedes["sector_fuente"] = np.where(sedes.sector.isin(["público", "privado", "mixto"]), "DENUE", "")
    sedes["institucion"] = None
    sedes["subtipo_oficial"] = None
    sedes["turnos"] = None
    cambios_tipo = []
    conflictos_sector = []
    for idx, s in reg[reg.sede_idx.notna()].groupby("sede_idx"):
        idx = int(idx)
        fuentes = sorted(set(s.fuente))
        sedes.loc[idx, "confirmado_por"] = "+".join(fuentes)
        sedes.loc[idx, "claves_sep_clues"] = " ".join(sorted(s.clave))
        sectores = set(s.sector) - {"desconocido"}
        nuevo = sectores.pop() if len(sectores) == 1 else ("mixto" if sectores else "desconocido")
        anterior = sedes.loc[idx, "sector"]
        if anterior in ("público", "privado") and nuevo in ("público", "privado") and anterior != nuevo:
            conflictos_sector.append({"id_sede": sedes.loc[idx, "id_sede"], "nombre": sedes.loc[idx, "nombre"],
                                      "denue": anterior, "oficial": nuevo})
        if nuevo != "desconocido":
            sedes.loc[idx, "sector"] = nuevo
            sedes.loc[idx, "sector_fuente"] = "+".join(fuentes)
        sedes.loc[idx, "institucion"] = "; ".join(sorted(set(s.institucion.dropna())))
        sedes.loc[idx, "subtipo_oficial"] = "; ".join(sorted(set(s.subtipo_sep.dropna())))
        sedes.loc[idx, "turnos"] = "; ".join(x for x in s.turnos.dropna() if x)
        if not sedes.loc[idx, "nombre"] or pd.isna(sedes.loc[idx, "nombre"]):
            sedes.loc[idx, "nombre"] = s.nombre.iloc[0]
        # La CLUES manda sobre el tipo de una sede de salud (consultorio privado, hospital)
        tipos = set(s.tipo)
        if len(tipos) == 1 and (t := tipos.pop()) != sedes.loc[idx, "tipo"]:
            cambios_tipo.append({"id_sede": sedes.loc[idx, "id_sede"], "nombre": sedes.loc[idx, "nombre"],
                                 "de": sedes.loc[idx, "tipo"], "a": t})
            sedes.loc[idx, "tipo"] = t
    sedes["estado_cruce"] = np.where(sedes.confirmado_por != "", "confirmada", "no confirmada")
    oficial = {"preescolar", "primaria", "secundaria", "bachillerato", "salud_primer_nivel",
               "consultorio_privado", "hospital", "escuela_varios_niveles"}
    sedes.loc[~sedes.tipo.isin(oficial), "estado_cruce"] = "no aplica"
    # Sedes sin registro que opere, pero con un registro dado de baja del mismo tipo
    # a <= DIST_CONFIRMA m: el registro oficial (más reciente que el MG y el DENUE)
    # dice que ya no opera. Se excluyen de la medida y se reportan.
    sedes["baja_oficial"] = ""
    for i in sedes.index[sedes.estado_cruce == "no confirmada"]:
        cand = baja[baja.tipo.isin({sedes.tipo[i]} | ({"salud_primer_nivel", "consultorio_privado", "hospital"}
                                                     if sedes.tipo[i] == "salud_primer_nivel" else set()))]
        if len(cand):
            d = cand.distance(sedes.geometry[i])
            if d.min() <= DIST_CONFIRMA:
                b = cand.loc[d.idxmin()]
                sedes.loc[i, "estado_cruce"] = f"baja en {b.fuente}"
                sedes.loc[i, "baja_oficial"] = f"{b.clave} {b.nombre} ({d.min():.0f} m)"
    # Registro oficial de OTRO nivel a <= 60 m de una sede no confirmada: puede ser
    # que el MG haya etiquetado mal el nivel de la escuela. Se marca para revisión.
    sedes["oficial_otro_tipo_cerca"] = ""
    for i in sedes.index[sedes.estado_cruce == "no confirmada"]:
        otros = reg[reg.tipo != sedes.tipo[i]]
        d = otros.distance(sedes.geometry[i])
        cerca = otros[d <= DIST_MISMA_SEDE]
        if len(cerca):
            sedes.loc[i, "oficial_otro_tipo_cerca"] = "; ".join(sorted(set(cerca.fuente + " " + cerca.tipo)))

    # --- Sedes nuevas: grupos SEP / CLUES sin sede de la fase 2 -----------------
    nuevos = reg[reg.sede_idx.isna()].copy()
    filas = []
    contador = {}
    for grupo, s in nuevos.groupby("grupo", sort=False):
        tipo = s.tipo.iloc[0]
        fuente = s.fuente.iloc[0]
        contador[(tipo, fuente)] = contador.get((tipo, fuente), 0) + 1
        sectores = set(s.sector) - {"desconocido"}
        filas.append({
            "id_sede": f"{tipo}-{fuente[0]}{contador[(tipo, fuente)]:04d}",
            "tipo": tipo, "tipo_fase2": None, "subtipo": tipo.replace("_", " "),
            "nombre": s.nombre.iloc[0],
            "sector": sectores.pop() if len(sectores) == 1 else ("mixto" if sectores else "desconocido"),
            "fuentes": fuente, "n_registros_mg": 0, "n_registros_denue": 0, "n_locales_mercado": None,
            "cve_ent": s.cve_ent.iloc[0], "entidad": cat06.ENTIDADES.get(s.cve_ent.iloc[0], s.cve_ent.iloc[0]),
            "cve_mun": s.cve_mun.iloc[0], "municipio": s.municipio.iloc[0].title() if pd.notna(s.municipio.iloc[0]) else None,
            "cve_loc": s.cve_loc.iloc[0], "localidad": s.localidad.iloc[0].title() if pd.notna(s.localidad.iloc[0]) else None,
            "en_acambaro": bool(s.en_acambaro.any()), "analizado": tipo in cat06.TIPOS,
            "confirmado_por": fuente, "claves_sep_clues": " ".join(sorted(s.clave)),
            "sector_fuente": fuente, "institucion": "; ".join(sorted(set(s.institucion.dropna()))),
            "subtipo_oficial": "; ".join(sorted(set(s.subtipo_sep.dropna()))),
            "turnos": "; ".join(x for x in s.turnos.dropna() if x),
            "estado_cruce": f"nueva ({fuente})",
            "geometry": s.geometry.union_all().centroid,
        })
    nuevas = gpd.GeoDataFrame(filas, crs=crs)
    todas = gpd.GeoDataFrame(pd.concat([sedes, nuevas], ignore_index=True), crs=crs)
    todas["analizado"] = todas.tipo.isin(cat06.TIPOS)
    todas["competencia"] = [competencia(t, st, se) for t, st, se in zip(todas.tipo, todas.subtipo, todas.sector)]
    todas.loc[todas.tipo.isin(["bachillerato_no_escolarizado", "escuela_centro_penitenciario"]),
              "competencia"] = "estatal/federal (educación)"
    todas.loc[todas.tipo.isin(["casa_de_salud", "unidad_movil"]), "competencia"] = "estatal/federal (salud)"
    municipio = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="municipio")
    todas["dist_fuera_mun_m"] = todas.distance(municipio.geometry.iloc[0]).round(0)
    # Nombre de localidad de las sedes del municipio sin nombre
    todas = cat06.nombres_localidad(todas)

    salida = P / "servicios_fase3.gpkg"
    salida.unlink(missing_ok=True)
    todas.to_file(salida, layer="sedes", driver="GPKG")
    reg.drop(columns=["sede_idx"]).assign(
        id_sede=[todas.id_sede.iloc[int(i)] if pd.notna(i) else None for i in reg.sede_idx]
    ).to_file(salida, layer="registros_sep_clues", driver="GPKG")
    ll = todas.to_crs("EPSG:4326")
    todas.drop(columns="geometry").assign(lat=ll.geometry.y.round(6), lon=ll.geometry.x.round(6)).to_csv(
        P / "servicios_sedes_fase3.csv", index=False)

    # --- Cifras -------------------------------------------------------------------
    t = todas.assign(donde=np.where(todas.en_acambaro, "Acámbaro", "franja 10 km"))
    v["sedes_por_tipo_y_estado"] = {
        d: t[t.donde == d].groupby(["tipo", "estado_cruce"]).size().unstack().fillna(0).astype(int).to_dict("index")
        for d in ["Acámbaro", "franja 10 km"]}
    v["sedes_por_tipo_y_sector_acambaro"] = (t[t.en_acambaro].groupby(["tipo", "sector"]).size()
                                             .unstack().fillna(0).astype(int).to_dict("index"))
    v["sedes_fase2_por_tipo"] = sedes.assign(donde=np.where(sedes.en_acambaro, "Acámbaro", "franja 10 km")) \
        .groupby(["tipo_fase2", "donde"]).size().unstack().fillna(0).astype(int).to_dict("index")
    v["como_cruzaron_registros"] = claves_texto(
        reg.como_cruzo.fillna("sin sede (nueva)").groupby(reg.fuente).value_counts().to_dict())
    v["distancia_registro_a_sede_m"] = {
        f: {"mediana": float(reg[(reg.fuente == f) & reg.dist_a_sede_m.notna()].dist_a_sede_m.median()),
            "p90": float(reg[(reg.fuente == f) & reg.dist_a_sede_m.notna()].dist_a_sede_m.quantile(0.9))}
        for f in ["SEP", "CLUES"]}
    v["cambios_de_tipo"] = cambios_tipo
    v["conflictos_sector_denue_vs_oficial"] = conflictos_sector
    v["no_confirmadas_acambaro"] = (t[t.en_acambaro & (t.estado_cruce == "no confirmada") & t.analizado]
                                    [["id_sede", "tipo", "nombre", "fuentes", "localidad", "oficial_otro_tipo_cerca"]]
                                    .to_dict("records"))
    v["bajas_oficiales"] = (t[t.estado_cruce.str.startswith("baja")]
                            [["id_sede", "tipo", "nombre", "fuentes", "localidad", "en_acambaro", "baja_oficial"]]
                            .to_dict("records"))
    v["nuevas_acambaro"] = (t[t.en_acambaro & t.estado_cruce.str.startswith("nueva")]
                            [["id_sede", "tipo", "nombre", "sector", "subtipo_oficial", "localidad"]].to_dict("records"))
    v["aparte_acambaro"] = (t[t.en_acambaro & t.tipo.isin(["bachillerato_no_escolarizado", "escuela_centro_penitenciario",
                                                           "casa_de_salud", "unidad_movil"])]
                            [["id_sede", "tipo", "nombre", "localidad"]].to_dict("records"))
    v["parametros"] = {"DIST_MISMA_SEDE_m": DIST_MISMA_SEDE, "DIST_CONFIRMA_m": DIST_CONFIRMA, "DIST_MUTUO_m": DIST_MUTUO}

    # --- Columna nueva en la muestra de verificación (sin regenerarla) ----------
    ruta = DOCS / "verificar_servicios_muestra.csv"
    m = pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    conf = dict(zip(sedes.id_sede, sedes.confirmado_por))
    estado = dict(zip(sedes.id_sede, sedes.estado_cruce))

    def marca(i, tipo):
        if tipo == "abasto":
            return "no aplica (abasto: no está en SEP ni CLUES)"
        if str(estado.get(i, "")).startswith("baja"):
            return estado[i] + " (dada de baja)"
        if estado.get(i) == "no aplica":
            return "no aplica (" + sedes.loc[sedes.id_sede == i, "tipo"].iloc[0].replace("_", " ") + ")"
        return conf.get(i) or "no"

    m["confirmado_sep_clues"] = [marca(i, tp) for i, tp in zip(m["id"], m["tipo"])]
    m.to_csv(ruta, index=False, encoding="utf-8-sig")
    v["muestra_confirmado_sep_clues"] = claves_texto(m.groupby(["tipo", "confirmado_sep_clues"]).size().to_dict())

    (P / "validacion_fase3_catalogo.json").write_text(
        json.dumps(v, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: v[k] for k in ["sedes_por_tipo_y_estado", "como_cruzaron_registros", "cambios_de_tipo",
                                        "conflictos_sector_denue_vs_oficial", "muestra_confirmado_sep_clues"]},
                     ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
