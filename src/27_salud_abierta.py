"""27 · Salud abierta a toda la población (fase 6, ajuste 1; D58).

La medida "salud pública de primer nivel" (D20) cuenta toda unidad pública,
incluidas las que solo atienden a sus derechohabientes (IMSS ordinario, ISSSTE).
Aquí se separan:
  - abierta: atiende a cualquier persona (Secretaría de Salud de Guanajuato, con
    sus centros de salud y UMAPS; IMSS-Bienestar; Unidades Médicas Rurales del
    IMSS, que la CLUES pasó al inventario del IMSS ordinario por el decreto de
    julio de 2025 pero siguen atendiendo a población sin seguridad social).
  - solo derechohabientes: UMF / HGSMF / UMFH del IMSS ordinario, ISSSTE.
Se usa la misma red, los mismos orígenes y el mismo umbral de salud que
11_accesibilidad.py (no se cambia nada de lo anterior). Sensibilidad: sin UMR.

Población: total y sin afiliación a servicios de salud (PSINDER, Censo 2020).
Ciudad: método D10 por AGEB (total publicado de la AGEB × proporción de su
población en cuadras lejanas) con el mínimo visible por cuadra al lado. Rural:
ITER por localidad; lo oculto ("*") se cuantifica.

Salidas (data/processed/):
  salud_clasificacion_instituciones.csv   una fila por sede de salud pública, con la regla
  acceso_salud_abierta.csv                distancias por cuadra (ciudad) y por localidad (rural)
  salud_abierta_resumen.csv               población lejos: pública vs abierta vs abierta sin UMR
  validacion_fase6.json                   clave "salud_abierta"
"""

import importlib.util
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"


def _modulo(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "src" / archivo)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


base03 = _modulo("base03", "03_base_geografica.py")
acc11 = _modulo("acc11", "11_accesibilidad.py")
URBANAS, FACTOR, SNAP_MAX = acc11.URBANAS, acc11.FACTOR_FIJO, acc11.SNAP_MAX
UMB_C = acc11.UMBRALES_CIUDAD["salud_publica"]
UMB_R = acc11.UMBRALES_RURAL["salud_publica"]
NIVELES = acc11.NIVELES
GRUPOS = {"POBTOT": "Población total", "PSINDER": "Sin afiliación a servicios de salud"}


# --- Clasificación (D58) --------------------------------------------------------------
def clasificar(fila):
    """Devuelve (clase, regla). clase: abierta | abierta_umr | derechohabientes."""
    inst = fila.institucion if isinstance(fila.institucion, str) else ""
    sub = (fila.subtipo_oficial or "") if isinstance(fila.subtipo_oficial, str) else ""
    nom = (fila.nombre or "").upper() if isinstance(fila.nombre, str) else ""
    if "SSG" in inst:
        return "abierta", "CLUES: Secretaría de Salud de Guanajuato" + (" (comparte con ISSSTE)" if "ISSSTE" in inst else "")
    if "IMSS-Bienestar" in inst:
        return "abierta", "CLUES: Servicios de Salud IMSS-Bienestar"
    if inst == "IMSS":
        if "unidad médica rural" in sub:
            return "abierta_umr", "CLUES: Unidad Médica Rural del IMSS (régimen bienestar, decreto jul-2025)"
        return "derechohabientes", f"CLUES: IMSS ordinario ({sub})"
    if "ISSSTE" in inst:
        return "derechohabientes", "CLUES: ISSSTE"
    # Sin registro CLUES: por nombre (se marca)
    if any(k in nom for k in ("ISSTE", "ISSSTE", "SEGURIDAD SOCIAL", "SERVICIOS SOCIALES", "SEGURIDAD Y SERVICIOS")):
        return "derechohabientes", "por nombre: ISSSTE"
    if any(k in nom for k in ("CENTRO DE SALUD", "UMAPS")):
        return "abierta", "por nombre: centro de salud"
    return "sin_clasificar", "sin CLUES ni nombre reconocible"


def main():
    sedes = gpd.read_file(P / "servicios_fase4.gpkg", layer="sedes")
    tramos = gpd.read_file(P / "red_peatonal.gpkg", layer="tramos")
    red = acc11.Red(tramos)
    crs = tramos.crs
    sedes = sedes.to_crs(crs)
    v = {}

    pub = sedes[acc11.CATEGORIAS["salud_publica"](sedes)].copy()
    cl = pub.apply(clasificar, axis=1, result_type="expand")
    pub["clase"], pub["regla"] = cl[0], cl[1]
    pub["clasificado_por_nombre"] = pub.regla.str.startswith("por nombre")
    cols = ["id_sede", "nombre", "institucion", "subtipo_oficial", "claves_sep_clues", "municipio", "entidad",
            "en_acambaro", "cve_loc", "localidad", "estado_cruce", "clase", "regla", "clasificado_por_nombre"]
    ll = pub.to_crs("EPSG:4326")
    pub[cols].assign(lat=ll.geometry.y.round(6), lon=ll.geometry.x.round(6)).to_csv(
        P / "salud_clasificacion_instituciones.csv", index=False)
    v["clasificacion"] = {
        "sedes_salud_publica": len(pub),
        "por_clase": pub.clase.value_counts().to_dict(),
        "por_clase_en_acambaro": pub[pub.en_acambaro].clase.value_counts().to_dict(),
        "clasificadas_por_nombre": pub[pub.clasificado_por_nombre][["id_sede", "nombre", "clase"]].to_dict("records"),
        "derechohabientes_en_acambaro": pub[pub.en_acambaro & (pub.clase == "derechohabientes")][["id_sede", "nombre"]].to_dict("records"),
    }
    # Controles pedidos por Alejandro (nota 3): SMP y DIF
    clues = pd.read_csv(P / "clues_buffer10km.csv", dtype=str)
    claves = set(pub.claves_sep_clues.dropna().str.split(r"[;, ]+").explode())
    v["control_smp_dif"] = {
        "registros_clues_SMP": int((clues["CLAVE DE LA INSTITUCION"] == "SMP").sum()),
        "registros_clues_DIF": clues.loc[clues["CLAVE DE LA INSTITUCION"] == "DIF", ["NOMBRE DE LA UNIDAD", "NOMBRE TIPO ESTABLECIMIENTO", "NIVEL ATENCION"]].to_dict("records"),
        "sedes_salud_publica_con_clave_SMP_o_DIF": int(clues[clues["CLAVE DE LA INSTITUCION"].isin(["SMP", "DIF"])].CLUES.isin(claves).sum()),
    }
    assert v["control_smp_dif"]["sedes_salud_publica_con_clave_SMP_o_DIF"] == 0
    assert (pub.clase != "sin_clasificar").all(), pub[pub.clase == "sin_clasificar"]

    variantes = {
        "salud_publica": pub,
        "salud_abierta": pub[pub.clase.isin(["abierta", "abierta_umr"])],
        "salud_abierta_sin_umr": pub[pub.clase == "abierta"],
    }

    # --- Orígenes de la ciudad: los mismos que 11 (cuadras 2020 + caserío + nuevas) ----
    mza = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="manzanas")
    cas = gpd.read_file(P / "manzanas2020_poblacion.gpkg", layer="caserio_disperso")
    cu = pd.concat([mza.assign(geometry=mza.representative_point(), origen="cuadra 2020"),
                    cas.assign(geometry=cas.representative_point(), origen="caserío disperso 2020")], ignore_index=True)
    nuevas = gpd.read_file(P / "manzanas_cambios.gpkg", layer="eic2025_vs_2020").to_crs(crs)
    nuevas = nuevas[nuevas.geometria_nueva & nuevas.CVE_LOC.isin(URBANAS)]
    cu = pd.concat([cu, nuevas[["CVEGEO", "CVE_LOC", "CVE_AGEB"]].assign(
        geometry=nuevas.representative_point(), origen="cuadra nueva posterior a 2020")], ignore_index=True)
    cu = gpd.GeoDataFrame(cu, geometry="geometry", crs=crs)
    cu["localidad"] = cu.CVE_LOC.map(URBANAS)
    # PSINDER por cuadra (con "*"): solo para las cuadras 2020 y el caserío (CVEGEO único en 2020)
    mza_c, ageb_c, loc_c, mun_c = base03.censo_manzanas("censo2020_mza_acambaro.csv", list(GRUPOS))
    ps = mza_c.drop_duplicates("CVEGEO").set_index("CVEGEO").PSINDER
    es2020 = cu.origen != "cuadra nueva posterior a 2020"
    cu["PSINDER"] = np.where(es2020, cu.CVEGEO.map(ps), np.nan)

    comp_loc = {}
    for loc in URBANAS:
        j = gpd.sjoin_nearest(cu[cu.CVE_LOC == loc][["geometry"]], tramos[["componente", "geometry"]], how="left")
        comp_loc[loc] = int(j.componente.mode().iloc[0])

    tabla = cu[["CVEGEO", "CVE_LOC", "localidad", "CVE_AGEB", "origen"]].copy()
    for loc in URBANAS:
        sel, arbol = red.componente(comp_loc[loc])
        o = cu[cu.CVE_LOC == loc]
        ao = red.anclar(o, sel, arbol)
        for nom, s in variantes.items():
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
                d_rec, id_rec = j.dr.to_numpy() * FACTOR, j.id_sede.to_numpy()
            usar = d_red <= d_rec
            tabla.loc[o.index, f"d_{nom}"] = np.round(np.where(usar, d_red, d_rec), 0)
            tabla.loc[o.index, f"id_{nom}"] = np.where(usar, id_red, id_rec)

    # Control: d_salud_publica debe ser idéntica a la de 11 (acceso_cuadras.csv), fila por fila
    ref = pd.read_csv(P / "acceso_cuadras.csv", dtype={"CVEGEO": str, "CVE_LOC": str})
    assert len(ref) == len(tabla)
    dif = np.abs(ref.d_salud_publica.to_numpy() - tabla.d_salud_publica.to_numpy())
    v["control_igual_a_11_ciudad"] = {"cuadras": len(tabla), "max_diferencia_m": float(np.nanmax(dif))}
    assert np.nanmax(dif) < 1

    # --- Rural ------------------------------------------------------------------------
    loc = gpd.read_file(P / "localidades2020.gpkg")
    iter20 = base03.numeros(pd.read_csv(P / "iter2020_acambaro.csv", dtype=str), ["POBTOT", "PSINDER"])
    rur = loc[~loc.LOC.isin(URBANAS)].drop(columns="POBTOT").merge(iter20[["LOC", "POBTOT", "PSINDER"]], on="LOC", how="left").to_crs(crs)
    tr = rur[["CVEGEO", "LOC", "NOM_LOC", "POBTOT", "PSINDER"]].copy()
    for nom, s in variantes.items():
        j = gpd.sjoin_nearest(rur[["geometry"]], s[["id_sede", "geometry"]], how="left", distance_col="dr")
        j = j[~j.index.duplicated()]
        tr[f"d_{nom}"] = (j.dr * FACTOR).round(0).to_numpy()
        tr[f"id_{nom}"] = j.id_sede.to_numpy()
    ref_r = pd.read_csv(P / "acceso_localidades.csv", dtype={"LOC": str})
    assert (ref_r.set_index("LOC").d_salud_publica.reindex(tr.LOC).to_numpy() == tr.d_salud_publica.to_numpy()).all()

    # --- Población lejos ------------------------------------------------------------------
    ageb_c["CVE_AGEB"] = ageb_c.AGEB
    tc = tabla.join(cu[["POBTOT", "PSINDER"]])
    filas = []
    for nom in variantes:
        for nivel, uc, ur in zip(NIVELES, UMB_C, UMB_R):
            for clv, nombre in URBANAS.items():
                c = tc[(tc.CVE_LOC == clv) & (tc.origen != "cuadra nueva posterior a 2020")]
                lejos = c[f"d_{nom}"] > uc
                at = ageb_c[ageb_c.LOC == clv].set_index("CVE_AGEB")
                pob = c.POBTOT.fillna(0)
                pa = pob.groupby(c.CVE_AGEB).sum()
                pl = pob[lejos].groupby(c.CVE_AGEB[lejos]).sum().reindex(pa.index, fill_value=0)
                prop = (pl / pa.replace(0, np.nan)).fillna(0)
                for var, gnom in GRUPOS.items():
                    if var == "POBTOT":
                        est, tot, vis = float(pob[lejos].sum()), float(pob.sum()), float(pob[lejos].sum())
                    else:
                        t_ag = at[var].reindex(prop.index)
                        est, tot = float((t_ag * prop).sum()), float(t_ag.sum())
                        vis = float(c.loc[lejos, var].sum())
                    filas.append({"medida": nom, "umbral": nivel, "umbral_m": uc, "localidad": nombre,
                                  "escala": "ciudad (a pie, por calles)", "grupo": gnom, "variable": var,
                                  "pob_lejos": round(est), "pob_lejos_minimo_visible": round(vis), "pob_total": round(tot),
                                  "pct_lejos": round(100 * est / tot, 1) if tot else None})
            lejos_r = tr[f"d_{nom}"] > ur
            for var, gnom in GRUPOS.items():
                vis, tot = float(tr.loc[lejos_r, var].sum()), float(tr[var].sum())
                filas.append({"medida": nom, "umbral": nivel, "umbral_m": ur, "localidad": "Localidades rurales (208)",
                              "escala": "municipio (línea recta × factor)", "grupo": gnom, "variable": var,
                              "pob_lejos": round(vis), "pob_lejos_minimo_visible": round(vis), "pob_total": round(tot),
                              "pct_lejos": round(100 * vis / tot, 1) if tot else None,
                              "localidades_lejos": int(lejos_r.sum())})
    res = pd.DataFrame(filas)
    # Control: salud_publica / POBTOT igual que en acceso_resumen_por_localidad.csv
    ref_s = pd.read_csv(P / "acceso_resumen_por_localidad.csv")
    ref_s = ref_s[(ref_s.categoria == "salud_publica") & (ref_s.variable == "POBTOT")].set_index(["localidad", "umbral"]).pob_lejos
    mia = res[(res.medida == "salud_publica") & (res.variable == "POBTOT")].set_index(["localidad", "umbral"]).pob_lejos
    assert (ref_s.reindex(mia.index) == mia).all(), pd.concat([ref_s, mia], axis=1)

    # Cambio respecto a la medida pública
    base = res[res.medida == "salud_publica"].set_index(["umbral", "localidad", "variable"]).pob_lejos
    res["cambio_vs_salud_publica"] = res.apply(lambda r: r.pob_lejos - base[(r.umbral, r.localidad, r.variable)], axis=1)
    res.to_csv(P / "salud_abierta_resumen.csv", index=False)

    # Oculto de PSINDER
    v["psinder_oculto"] = {
        "municipio_total": float(mun_c.PSINDER.iloc[0]) if "PSINDER" in mun_c else None,
        "ciudad_agebs_publicado": {URBANAS[k]: float(ageb_c[ageb_c.LOC == k].PSINDER.sum()) for k in URBANAS},
        "ciudad_suma_visible_cuadras": {URBANAS[k]: float(tc[tc.CVE_LOC == k].PSINDER.sum()) for k in URBANAS},
        "cuadras_con_asterisco": int(tc[es2020].PSINDER.isna().sum()),
        "rural_visible": float(tr.PSINDER.sum()),
        "rural_localidades_con_asterisco": int(tr.PSINDER.isna().sum()),
        "rural_pob_en_localidades_con_asterisco": float(tr.loc[tr.PSINDER.isna(), "POBTOT"].sum()),
    }
    it_tot = iter20[iter20.LOC == "0000"].PSINDER.iloc[0]
    it_urb = iter20[iter20.LOC.isin(URBANAS)].PSINDER.sum()
    v["psinder_oculto"]["iter_municipio"] = float(it_tot)
    v["psinder_oculto"]["iter_urbanas"] = float(it_urb)
    v["psinder_oculto"]["rural_oculto"] = float(it_tot - it_urb - tr.PSINDER.sum())

    # Salidas por cuadra / localidad
    out = pd.concat([tc.assign(escala="ciudad"),
                     tr.rename(columns={"LOC": "CVE_LOC", "NOM_LOC": "localidad"}).assign(escala="rural", origen="localidad")],
                    ignore_index=True)
    out.to_csv(P / "acceso_salud_abierta.csv", index=False)

    pr = res[(res.umbral == "principal")]
    v["resumen_principal"] = {f"{r.localidad} | {r.variable} | {r.medida}": [r.pob_lejos, r.pct_lejos, r.cambio_vs_salud_publica]
                              for r in pr.itertuples()}
    # Qué sede más cercana cambió
    v["cuadras_que_cambian_de_sede"] = {URBANAS[k]: int((tabla[tabla.CVE_LOC == k].id_salud_publica != tabla[tabla.CVE_LOC == k].id_salud_abierta).sum())
                                        for k in URBANAS}
    v["localidades_rurales_que_cambian_de_sede"] = int((tr.id_salud_publica != tr.id_salud_abierta).sum())
    v["localidades_rurales_que_cambian_sin_umr"] = int((tr.id_salud_abierta != tr.id_salud_abierta_sin_umr).sum())

    f = P / "validacion_fase6.json"
    todo = json.loads(f.read_text()) if f.exists() else {}
    todo["salud_abierta"] = v
    f.write_text(json.dumps(todo, ensure_ascii=False, indent=1, default=str))
    print(json.dumps({k: v[k] for k in ["clasificacion", "control_smp_dif", "psinder_oculto",
                                        "cuadras_que_cambian_de_sede", "localidades_rurales_que_cambian_de_sede",
                                        "localidades_rurales_que_cambian_sin_umr"]}, ensure_ascii=False, indent=1, default=str))
    print(pr[["medida", "localidad", "variable", "pob_lejos", "pct_lejos", "cambio_vs_salud_publica"]].to_string())


if __name__ == "__main__":
    main()
