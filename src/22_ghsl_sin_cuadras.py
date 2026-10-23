"""22 · Crecimiento que el Marco Geoestadístico no dibuja (fase 4c).

El GHSL ve ~67 ha nuevas construidas en la ciudad entre 2010 y 2020, pero las cuadras
nuevas del MG suman ~18 ha. Aquí se ubica la diferencia:

  1. Celdas GHS-BUILT-S (100 m = 1 ha, Mollweide) a <= 1 km de las 4 localidades urbanas
     (misma asignación que 20_ghsl_serie.py). Ganancia = m² construidos 2020 − 2010.
  2. Cada celda se cruza con las cuadras del MG más reciente (MG EIC 2025, todas las del
     municipio): fracción de la celda cubierta por cuadras. La ganancia se reparte en
     "dentro de cuadras" (ganancia × fracción) y "fuera" (el resto), sin umbral.
  3. Celda "sin cuadras" (D52, provisional): ganancia >= GANANCIA_MIN m² y < COBERTURA_MAX
     de su superficie en cuadras. Las celdas contiguas (vecindad de 8) forman una zona.

Salidas:
  data/processed/ghsl_cambio_2010_2020.gpkg   capas "celdas" (solo las que ganaron) y "zonas"
  data/processed/ghsl_zonas_sin_cuadras.csv   todas las zonas
  docs/zonas_ghsl_sin_cuadras.kml             contorno de las MAX_KML zonas más grandes
  docs/verificar_zonas_ghsl.csv               lista para revisar en Google Maps (conserva lo anotado)
  validacion_fase4b.json, clave "ghsl_sin_cuadras"
"""

import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from scipy import ndimage
from shapely.geometry import MultiPolygon, box

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
DOCS = RAIZ / "docs"


def modulo(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "src" / archivo)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


crec19 = modulo("crec19", "19_crecimiento.py")
ghsl20 = modulo("ghsl20", "20_ghsl_serie.py")
URBANAS = crec19.URBANAS

A0, A1 = 2010, 2020
GANANCIA_MIN = 500     # m² ganados por celda (5 % de la celda)
COBERTURA_MAX = 0.25   # fracción máxima de la celda dentro de cuadras para contar como "sin cuadras"
SENSIBILIDAD = [(200, 0.25), (1000, 0.25), (500, 0.10), (500, 0.50)]
MAX_KML = 20
SAT = "https://www.google.com/maps/@{lat:.6f},{lon:.6f},300m/data=!3m1!1e3"


def celdas_poligono():
    """Celdas como cuadrados en el CRS del ráster, con fila, columna y m² por año."""
    with rasterio.open(P / "ghsl" / f"ghsl_built_s_{A0}_acambaro.tif") as r:
        t, forma, crs = r.transform, r.shape, r.crs
    filas, cols = np.indices(forma)
    filas, cols = filas.ravel(), cols.ravel()
    x0, y0 = t * (cols, filas)
    x1, y1 = t * (cols + 1, filas + 1)
    g = gpd.GeoDataFrame({"fila": filas, "col": cols},
                         geometry=[box(a, b, c, d) for a, b, c, d in zip(x0, y1, x1, y0)], crs=crs)
    for a in (A0, A1):
        with rasterio.open(P / "ghsl" / f"ghsl_built_s_{a}_acambaro.tif") as r:
            v = r.read(1).ravel().astype(float)
            v[v == r.nodata] = np.nan
        g[a] = v
    return g, forma


def zonas(c, forma, sel):
    """Agrupa las celdas seleccionadas contiguas (vecindad de 8). Devuelve la etiqueta por celda."""
    m = np.zeros(forma, dtype=bool)
    m[c.fila[sel], c.col[sel]] = True
    et, _ = ndimage.label(m, structure=np.ones((3, 3)))
    return np.where(sel, et[c.fila, c.col], 0)


def kml(z):
    raiz = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(raiz, "Document")
    ET.SubElement(doc, "name").text = "Acámbaro: construcción 2010–2020 (GHSL) fuera de las cuadras del INEGI"
    ET.SubElement(doc, "description").text = (
        f"Celdas de 100 m del GHSL con al menos {GANANCIA_MIN} m² construidos nuevos entre {A0} y {A1} y menos "
        f"de {COBERTURA_MAX:.0%} de su superficie dentro de cuadras del Marco Geoestadístico (EIC 2025). "
        f"Las {MAX_KML} zonas más grandes. El GHSL es un modelo con celdas de 100 m y su capa 2020 combina "
        "imágenes de varios años: puede haber falsos positivos. Lista: docs/verificar_zonas_ghsl.csv.")
    st = ET.SubElement(doc, "Style", id="ghsl")
    ls = ET.SubElement(st, "LineStyle")
    ET.SubElement(ls, "color").text = "ffff00ff"
    ET.SubElement(ls, "width").text = "2"
    ET.SubElement(ET.SubElement(st, "PolyStyle"), "color").text = "44ff00ff"
    for _, f in z.iterrows():
        pm = ET.SubElement(doc, "Placemark")
        ET.SubElement(pm, "name").text = f.id
        ET.SubElement(pm, "description").text = (
            f"Zona {f.id}. Localidad: {f.localidad}. Superficie: {f.superficie_ha:.0f} ha ({f.celdas} celdas de 100 m). "
            f"Construcción ganada {A0}–{A1} según el GHSL: {f.m2_ganados:,.0f} m². "
            f"Dentro del polígono de la localidad: {f.dentro_poligono_localidad}."
            + (f" Localidades rurales del INEGI dentro: {f.localidades_rurales_en_zona}." if f.localidades_rurales_en_zona else ""))
        ET.SubElement(pm, "styleUrl").text = "#ghsl"
        geom = f.geometry
        partes = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
        padre = ET.SubElement(pm, "MultiGeometry") if len(partes) > 1 else pm
        for pol in partes:
            p = ET.SubElement(padre, "Polygon")
            for tag, anillo in [("outerBoundaryIs", pol.exterior)] + [("innerBoundaryIs", h) for h in pol.interiors]:
                ET.SubElement(ET.SubElement(ET.SubElement(p, tag), "LinearRing"), "coordinates").text = \
                    " ".join(f"{x:.6f},{y:.6f},0" for x, y in anillo.coords)
    ET.indent(raiz)
    ET.ElementTree(raiz).write(DOCS / "zonas_ghsl_sin_cuadras.kml", encoding="utf-8", xml_declaration=True)


def main():
    mun = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="municipio")
    crs = mun.crs
    c, forma = celdas_poligono()
    # Asignación a localidad: misma regla que 20 (centro de la celda a <= BUFFER m del polígono; la más cercana)
    cen_celda = c.geometry.centroid.to_crs(crs)
    loc = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="localidades_amanzanadas")
    loc_u = loc[loc.CVE_LOC.isin(URBANAS)].dissolve("CVE_LOC").reset_index()
    dist = np.column_stack([cen_celda.distance(p) for p in loc_u.geometry])
    c["cve_loc"] = np.where(dist.min(axis=1) <= ghsl20.BUFFER, loc_u.CVE_LOC.to_numpy()[dist.argmin(axis=1)], "")
    c = c.to_crs(crs)
    c["ganancia_m2"] = c[A1] - c[A0]
    dom = c[c.cve_loc != ""].copy()

    # Fracción de cada celda en cuadras del MG EIC 2025 y en polígonos de localidad amanzanada
    mz = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="manzanas")
    cu = gpd.read_file(P / "cuadras_antiguedad.gpkg", layer="cuadras")[["periodo", "geometry"]]

    def fraccion(capas):
        i = gpd.overlay(dom[["geometry"]].reset_index(), capas[["geometry"]], how="intersection", keep_geom_type=True)
        return (i.area.groupby(i["index"]).sum() / 1e4).reindex(dom.index, fill_value=0).clip(upper=1)

    dom["frac_cuadras"] = fraccion(mz.dissolve())
    dom["frac_poligono_loc"] = fraccion(loc.dissolve())
    for per, col in [(crec19.CONSOL, "frac_consolidada"), (crec19.N1020, "frac_nueva_1020"), (crec19.N20, "frac_nueva_post2020")]:
        dom[col] = fraccion(cu[cu.periodo == per].dissolve())

    v = {"celdas_dominio": len(dom), "celdas_sin_dato": int(dom[[A0, A1]].isna().any(axis=1).sum()),
         "celdas_con_perdida": int((dom.ganancia_m2 < 0).sum()),
         "perdida_m2": float(dom.ganancia_m2[dom.ganancia_m2 < 0].sum())}
    # Contabilidad sin umbral (ganancia positiva y neta)
    g = dom.ganancia_m2.fillna(0)
    gp = g.clip(lower=0)
    cont = []
    for cl in URBANAS:
        s = dom.cve_loc == cl
        cont.append({"cve_loc": cl, "localidad": URBANAS[cl], "celdas": int(s.sum()),
                     "construido_2010_ha": round(dom.loc[s, A0].sum() / 1e4, 1),
                     "construido_2020_ha": round(dom.loc[s, A1].sum() / 1e4, 1),
                     "ganancia_neta_ha": round(g[s].sum() / 1e4, 1),
                     "ganancia_positiva_ha": round(gp[s].sum() / 1e4, 1),
                     "dentro_cuadras_ha": round((gp * dom.frac_cuadras)[s].sum() / 1e4, 1),
                     "dentro_consolidadas_ha": round((gp * dom.frac_consolidada)[s].sum() / 1e4, 1),
                     "dentro_nuevas_1020_ha": round((gp * dom.frac_nueva_1020)[s].sum() / 1e4, 1),
                     "dentro_nuevas_post2020_ha": round((gp * dom.frac_nueva_post2020)[s].sum() / 1e4, 1),
                     "fuera_cuadras_ha": round((gp * (1 - dom.frac_cuadras))[s].sum() / 1e4, 1),
                     "fuera_poligono_localidad_ha": round((gp * (1 - dom.frac_poligono_loc))[s].sum() / 1e4, 1)})
    cont = pd.DataFrame(cont)
    v["contabilidad"] = cont.to_dict("records")
    # Distribución de la cobertura por cuadras en celdas urbanas ya construidas en 2010 (para justificar el corte)
    urb = dom[(dom[A0] >= 3000)]
    v["frac_cuadras_celdas_construidas_2010_percentiles"] = urb.frac_cuadras.quantile([.1, .25, .5, .75, .9]).round(2).to_dict()
    v["frac_cuadras_celdas_con_ganancia"] = {
        "<10%": int(((gp >= GANANCIA_MIN) & (dom.frac_cuadras < .10)).sum()),
        "10-25%": int(((gp >= GANANCIA_MIN) & dom.frac_cuadras.between(.10, .25, inclusive="left")).sum()),
        "25-50%": int(((gp >= GANANCIA_MIN) & dom.frac_cuadras.between(.25, .50, inclusive="left")).sum()),
        ">=50%": int(((gp >= GANANCIA_MIN) & (dom.frac_cuadras >= .50)).sum())}

    # Celdas "sin cuadras" y zonas
    def seleccion(gmin, cmax):
        return (gp >= gmin) & (dom.frac_cuadras < cmax)

    sens = []
    for gmin, cmax in [(GANANCIA_MIN, COBERTURA_MAX)] + SENSIBILIDAD:
        s = seleccion(gmin, cmax)
        et = zonas(dom, forma, s.to_numpy())
        for cl in URBANAS:
            k = s & (dom.cve_loc == cl)
            sens.append({"ganancia_min_m2": gmin, "cobertura_max": cmax, "localidad": URBANAS[cl],
                         "celdas": int(k.sum()), "zonas": len(np.unique(et[k.to_numpy()])),
                         "m2_ganados_ha": round(gp[k].sum() / 1e4, 1)})
    sens = pd.DataFrame(sens)
    v["sensibilidad"] = sens.to_dict("records")

    sel = seleccion(GANANCIA_MIN, COBERTURA_MAX)
    dom["sin_cuadras"] = sel
    dom["zona"] = zonas(dom, forma, sel.to_numpy())
    cen = crec19.centros(crs)
    zs = dom[dom.zona > 0].dissolve("zona", aggfunc={"cve_loc": "first", "ganancia_m2": "sum", A1: "sum",
                                                      "frac_poligono_loc": "mean", "fila": "count"})
    zs = zs.rename(columns={"fila": "celdas", "ganancia_m2": "m2_ganados", A1: "m2_construidos_2020"}).reset_index()
    # Una zona puede tocar dos localidades: se usa la de la mayoría de sus celdas
    moda = dom[dom.zona > 0].groupby("zona").cve_loc.agg(lambda x: x.mode().iloc[0])
    zs["cve_loc"] = zs.zona.map(moda)
    zs["localidad"] = zs.cve_loc.map(URBANAS)
    zs["superficie_ha"] = zs.area / 1e4
    zs["dentro_poligono_localidad"] = np.select([zs.frac_poligono_loc >= .5, zs.frac_poligono_loc > 0],
                                                ["sí (mayormente)", "en parte"], "no")
    # ¿El INEGI la registra de otra forma? Localidades rurales puntuales y caserío disperso dentro de la zona
    punt = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="localidades_puntuales_rurales")
    cas = gpd.read_file(P / "mg_eic2025_acambaro.gpkg", layer="caserio_disperso")
    zs["localidades_rurales_en_zona"] = ["; ".join(f"{r.NOMGEO} ({r.CVE_LOC})" for r in punt[punt.within(z)].itertuples())
                                         for z in zs.geometry]
    zs["caserio_disperso_en_zona"] = [int(cas.within(z).sum()) for z in zs.geometry]
    pt = zs.geometry.representative_point()
    zs["dist_centro_m"] = [round(p.distance(cen[l])) for p, l in zip(pt, zs.cve_loc)]
    ll = pt.to_crs(4326)
    zs["lat"], zs["lon"] = ll.y.round(6), ll.x.round(6)
    zs = zs.sort_values("m2_ganados", ascending=False).reset_index(drop=True)
    zs["id"] = [f"G-{i + 1:03d}" for i in range(len(zs))]
    zs["m2_ganados"] = zs.m2_ganados.round(0)
    zs["m2_construidos_2020"] = zs.m2_construidos_2020.round(0)
    zs["superficie_ha"] = zs.superficie_ha.round(1)
    zs["frac_poligono_loc"] = zs.frac_poligono_loc.round(2)
    dom["zona_id"] = dom.zona.map(dict(zip(zs.zona, zs.id))).fillna("")
    v["zonas"] = len(zs)
    v["zonas_por_localidad"] = zs.groupby("localidad").agg(zonas=("id", "size"), celdas=("celdas", "sum"),
                                                          m2_ganados=("m2_ganados", "sum")).to_dict("index")
    v["zonas_de_1_celda"] = int((zs.celdas == 1).sum())
    v["zonas_con_localidad_rural_o_caserio"] = int(((zs.localidades_rurales_en_zona != "") | (zs.caserio_disperso_en_zona > 0)).sum())
    v["celdas_dominio_fuera_del_municipio"] = int((~dom.geometry.centroid.within(mun.union_all())).sum())
    v["zonas_fuera_del_municipio"] = int((~zs.geometry.representative_point().within(mun.union_all())).sum())

    # Salidas
    cols_z = ["id", "cve_loc", "localidad", "celdas", "superficie_ha", "m2_ganados", "m2_construidos_2020",
              "frac_poligono_loc", "dentro_poligono_localidad", "localidades_rurales_en_zona", "caserio_disperso_en_zona",
              "dist_centro_m", "lat", "lon"]
    capa_c = dom[dom.ganancia_m2 > 0].drop(columns=["zona"]).rename(columns={A0: f"m2_{A0}", A1: f"m2_{A1}"})
    capa_c.to_file(P / "ghsl_cambio_2010_2020.gpkg", layer="celdas", driver="GPKG")
    zs[cols_z + ["geometry"]].to_file(P / "ghsl_cambio_2010_2020.gpkg", layer="zonas", driver="GPKG")
    zs[cols_z].to_csv(P / "ghsl_zonas_sin_cuadras.csv", index=False)
    cont.to_csv(P / "ghsl_dentro_fuera_cuadras.csv", index=False)
    sens.to_csv(P / "ghsl_sin_cuadras_sensibilidad.csv", index=False)
    kml(zs.head(MAX_KML).to_crs(4326))

    lista = zs[["id", "localidad", "superficie_ha", "m2_ganados", "celdas", "localidades_rurales_en_zona",
               "lat", "lon"]].copy()
    lista["en_kml"] = np.where(lista.index < MAX_KML, "sí", "no")
    lista["enlace_satelite"] = [SAT.format(lat=a, lon=b) for a, b in zip(lista.lat, lista.lon)]
    lista["que_verificar"] = (f"¿Hay casas, calles o naves nuevas que no estaban en la imagen de {A0}? "
                              "¿O es invernadero, bordo, suelo desnudo u otra cosa?")
    for col in ["existe_en_imagen", "que_se_ve", "notas"]:
        lista[col] = ""
    ruta = DOCS / "verificar_zonas_ghsl.csv"
    if ruta.exists():   # conserva lo que Alejandro ya anotó
        prev = pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8-sig").set_index("id")
        for col in ["existe_en_imagen", "que_se_ve", "notas"]:
            lista[col] = [prev[col].get(k, "") for k in lista.id]
    lista.to_csv(ruta, index=False, encoding="utf-8-sig")

    j = json.loads((P / "validacion_fase4b.json").read_text())
    j["ghsl_sin_cuadras"] = v
    (P / "validacion_fase4b.json").write_text(json.dumps(j, ensure_ascii=False, indent=1, default=str))
    print(cont.to_string())
    print(sens.to_string())
    print(zs[cols_z].head(25).to_string())
    print(json.dumps({k: v[k] for k in v if k not in ("contabilidad", "sensibilidad")}, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
