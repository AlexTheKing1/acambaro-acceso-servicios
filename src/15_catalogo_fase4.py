"""15 · Catálogo de servicios de la fase 4: decisiones finales y verificación remota.

Parte de data/processed/servicios_fase3.gpkg (09_catalogo_sep_clues.py; no se
modifica) y aplica las decisiones de Alejandro del 2026-10-23 (D33–D41):

  - CERESO (D38): el "CONSULTORIO MEDICO CIVIL" del DENUE está dentro del
    centro penitenciario; no es un servicio abierto a la población. Pasa al tipo
    "salud_centro_penitenciario" (fuera de salud pública).
  - CECyTE Acámbaro (D37): Google Maps lo ubica en Av. San Pablo 8, col. Valle de
    Acámbaro; el DENUE trae el mismo número y colonia. Se conserva el punto del
    MG/DENUE y se descarta el de la SEP (calle Loma Bonita, ~4 km al norte); la sede
    conservada queda confirmada con la clave SEP.
  - ISSSTE (D36): en operación (verificación local); la CLUES dice "fuera de
    operación". Se conserva y se anota la discrepancia.
  - Unidades de salud que solo dibuja el INEGI (D34): no entran en salud pública
    (ya no entraban: sector desconocido); se marcan para el anexo.
  - Verificación remota de Alejandro (D41, data/raw/verificacion/
    verificacion_servicios.csv): se une por id. Un "no" no borra el servicio: se
    marca dudoso_remoto y se usa en una sensibilidad (11_accesibilidad.py).

Salidas en data/processed/:
  servicios_fase4.gpkg           capa "sedes"
  servicios_sedes_fase4.csv      la misma capa en tabla, con latitud y longitud
  validacion_fase4_catalogo.json tasas de confirmación y cambios aplicados
"""

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
VERIF = RAIZ / "data" / "raw" / "verificacion" / "verificacion_servicios.csv"

CERESO = "salud_primer_nivel-0093"
CECYTE_CONSERVA, CECYTE_DESCARTA = "bachillerato-0022", "bachillerato-S0004"
ISSSTE = "salud_primer_nivel-0011"
SALUD_SOLO_INEGI = ["salud_primer_nivel-0007", "salud_primer_nivel-0008", "salud_primer_nivel-0014",
                    "salud_primer_nivel-0019", "salud_primer_nivel-0080", "salud_primer_nivel-0081"]
NOTAS = {
    ISSSTE: "En operación según verificación local de Alejandro (2026-10-23); la CLUES de agosto 2026 la "
            "registra fuera de operación sin motivo (D36).",
    CECYTE_CONSERVA: "Ubicación confirmada: Av. San Pablo 8, col. Valle de Acámbaro (Google Maps y DENUE). "
                     "La SEP la ubica en calle Loma Bonita, ~4 km al norte: punto SEP descartado (D37).",
    CECYTE_DESCARTA: "Punto SEP del CECyTE Acámbaro descartado: ubicación errónea (D37).",
    CERESO: "Está dentro del CERESO: no es un servicio abierto a la población (D38).",
    "primaria-0030": "En Street View, en el punto aparece la Telesecundaria No. 845 (secundaria-0007, a ~130 m); "
                     "la primaria está confirmada por la SEP. Se conserva; va a la verificación de campo.",
}


def tasas(t, por=None):
    """Tasa de confirmación: 'si' entre revisados, con y sin los 'no se ve'."""
    def fila(g):
        n_si, n_no, n_nv = (g.existe_en_imagen == "si").sum(), (g.existe_en_imagen == "no").sum(), \
            (g.existe_en_imagen == "no se ve").sum()
        return pd.Series({"revisados": len(g), "si": n_si, "no": n_no, "no_se_ve": n_nv,
                          "pct_si_de_revisados": round(100 * n_si / len(g), 1),
                          "pct_si_sin_contar_no_se_ve": round(100 * n_si / (n_si + n_no), 1) if n_si + n_no else None})
    if por is None:
        return fila(t).to_dict()
    return {k: fila(g).to_dict() for k, g in t.groupby(por)}


def main():
    s = gpd.read_file(P / "servicios_fase3.gpkg", layer="sedes")
    v = {}
    s["tipo_fase3"] = s.tipo
    s["nota_fase4"] = s.id_sede.map(NOTAS)

    # D38: CERESO
    s.loc[s.id_sede == CERESO, "tipo"] = "salud_centro_penitenciario"
    s.loc[s.id_sede == CERESO, "analizado"] = False

    # D37: CECyTE
    sep = s.loc[s.id_sede == CECYTE_DESCARTA].iloc[0]
    i = s.index[s.id_sede == CECYTE_CONSERVA][0]
    v["cecyte"] = {"conservada": CECYTE_CONSERVA, "descartada": CECYTE_DESCARTA,
                   "distancia_entre_puntos_m": round(float(s.geometry[i].distance(sep.geometry)), 0),
                   "estado_antes": s.loc[i, "estado_cruce"]}
    s.loc[i, ["confirmado_por", "claves_sep_clues", "estado_cruce", "institucion", "subtipo_oficial", "turnos"]] = [
        "SEP", sep.claves_sep_clues, "confirmada", sep.institucion, sep.subtipo_oficial, sep.turnos]
    s.loc[s.id_sede == CECYTE_DESCARTA, "estado_cruce"] = "descartada (ubicación errónea, D37)"

    # D34: anexo de salud
    s["anexo_salud_sin_clues"] = s.id_sede.isin(SALUD_SOLO_INEGI)
    for k in SALUD_SOLO_INEGI:
        s.loc[s.id_sede == k, "nota_fase4"] = ("Solo en el dibujo del INEGI, sin registro en la CLUES: fuera de la "
                                              "medida principal, en el anexo (D34).")
    v["anexo_salud_sin_clues"] = s.loc[s.anexo_salud_sin_clues, ["id_sede", "nombre", "localidad", "sector"]].to_dict("records")

    # D41: verificación remota
    ver = pd.read_csv(VERIF, dtype=str)
    ver = ver[ver.prioridad == "revisado"].rename(columns={"notas": "notas_verificacion"})
    s = s.merge(ver[["id", "existe_en_imagen", "visto_en", "notas_verificacion"]], left_on="id_sede",
                right_on="id", how="left").drop(columns="id")
    s["dudoso_remoto"] = s.existe_en_imagen == "no"
    s = gpd.GeoDataFrame(s, geometry="geometry", crs=s.crs)

    t = s[s.existe_en_imagen.notna()].copy()
    t["fuente_catalogo"] = t.fuentes
    t["donde"] = np.where(t.en_acambaro, "dentro del municipio", "fuera (hasta 10 km)")
    v["verificacion_remota"] = {
        "advertencia": ("No es una muestra al azar: se revisaron todos los bachilleratos y casos priorizados. "
                        "Las tasas describen esos casos, no la confiabilidad general del catálogo."),
        "filas_en_archivo": int(len(pd.read_csv(VERIF, dtype=str))), "revisados": int(len(t)),
        "total": tasas(t), "por_tipo": tasas(t, "tipo"), "por_fuente": tasas(t, "fuente_catalogo"),
        "por_donde": tasas(t, "donde"), "por_estado_cruce": tasas(t, "estado_cruce"),
        "visto_en": t.visto_en.fillna("(vacío)").value_counts().to_dict(),
        "dudosos_remotos": t[t.dudoso_remoto][["id_sede", "tipo", "nombre", "localidad", "fuentes", "en_acambaro",
                                               "estado_cruce", "notas_verificacion"]].to_dict("records"),
    }
    v["conteo_por_tipo_estado"] = {f"{a} | {b}": int(n) for (a, b), n in
                                   s[s.en_acambaro].groupby(["tipo", "estado_cruce"]).size().items()}

    salida = P / "servicios_fase4.gpkg"
    salida.unlink(missing_ok=True)
    s.to_file(salida, layer="sedes", driver="GPKG")
    ll = s.to_crs("EPSG:4326")
    s.drop(columns="geometry").assign(lat=ll.geometry.y.round(6), lon=ll.geometry.x.round(6)).to_csv(
        P / "servicios_sedes_fase4.csv", index=False)
    (P / "validacion_fase4_catalogo.json").write_text(json.dumps(v, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: v["verificacion_remota"][k] for k in ["total", "por_tipo", "por_fuente"]},
                     ensure_ascii=False, indent=1, default=str))
    print(v["cecyte"])


if __name__ == "__main__":
    main()
