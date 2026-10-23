"""17 · Zonas de crecimiento en KML para Google Earth (fase 4).

Escribe docs/zonas_nuevas.kml con el contorno exacto de cada zona de
docs/verificar_zonas_nuevas.csv (07_listas_verificacion.py): todas las
posteriores a 2020 y las 15 de mayor superficie de 2010–2020. El contorno es la
unión de las cuadras nuevas de la zona (columna claves_cuadras), tomadas de la
capa de manzanas_cambios.gpkg de su periodo (las claves no se cruzan entre
ediciones). Agrega a la lista la columna en_kml (sí / no) sin tocar las demás.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon

RAIZ = Path(__file__).resolve().parents[1]
P = RAIZ / "data" / "processed"
DOCS = RAIZ / "docs"
LISTA = DOCS / "verificar_zonas_nuevas.csv"

CAPA = {"2010-2020": "mg2020_vs_2010", "posterior a 2020": "eic2025_vs_2020"}
MAS_GRANDES_2010_2020 = 15
# Colores KML (aabbggrr): naranja para 2010–2020, rojo para posterior a 2020
ESTILO = {"2010-2020": ("ff1e90ff", "551e90ff"), "posterior a 2020": ("ff0000e6", "660000e6")}


def anillo(coords):
    return " ".join(f"{x:.6f},{y:.6f},0" for x, y in coords)


def poligono_kml(padre, pol):
    p = ET.SubElement(padre, "Polygon")
    ET.SubElement(ET.SubElement(ET.SubElement(p, "outerBoundaryIs"), "LinearRing"), "coordinates").text = \
        anillo(pol.exterior.coords)
    for hueco in pol.interiors:
        ET.SubElement(ET.SubElement(ET.SubElement(p, "innerBoundaryIs"), "LinearRing"), "coordinates").text = \
            anillo(hueco.coords)


def main():
    z = pd.read_csv(LISTA, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    z["sup"] = z.superficie_ha.astype(float)
    elegidas = pd.concat([z[z.periodo == "posterior a 2020"],
                          z[z.periodo == "2010-2020"].nlargest(MAS_GRANDES_2010_2020, "sup")])

    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(kml, "Document")
    ET.SubElement(doc, "name").text = "Acámbaro: zonas de crecimiento urbano"
    ET.SubElement(doc, "description").text = (
        "Contorno de las cuadras nuevas de cada zona (Marco Geoestadístico del INEGI). "
        "Rojo: posteriores a 2020 (MG EIC 2025 vs. MG 2020). Naranja: las 15 más grandes de 2010–2020. "
        "Lista completa: docs/verificar_zonas_nuevas.csv.")
    for periodo, (linea, relleno) in ESTILO.items():
        st = ET.SubElement(doc, "Style", id=periodo.replace(" ", "_"))
        ls = ET.SubElement(st, "LineStyle")
        ET.SubElement(ls, "color").text = linea
        ET.SubElement(ls, "width").text = "2"
        ET.SubElement(ET.SubElement(st, "PolyStyle"), "color").text = relleno

    n = 0
    for periodo in ["posterior a 2020", "2010-2020"]:
        m = gpd.read_file(P / "manzanas_cambios.gpkg", layer=CAPA[periodo])
        m = m[m.geometria_nueva].set_index("CVEGEO")
        assert m.index.is_unique
        carpeta = ET.SubElement(doc, "Folder")
        ET.SubElement(carpeta, "name").text = ("Posteriores a 2020 (todas)" if periodo != "2010-2020"
                                               else f"2010–2020 (las {MAS_GRANDES_2010_2020} más grandes)")
        for _, f in elegidas[elegidas.periodo == periodo].iterrows():
            claves = f.claves_cuadras.split()
            forma = gpd.GeoSeries([m.loc[claves].geometry.union_all()], crs=m.crs).to_crs("EPSG:4326").iloc[0]
            pm = ET.SubElement(carpeta, "Placemark")
            ET.SubElement(pm, "name").text = f.id
            pob = f"; población 2020: {f.pob_2020}" if f.pob_2020 else "; sin población censada (posterior al Censo 2020)" \
                if periodo != "2010-2020" else ""
            ET.SubElement(pm, "description").text = (
                f"Zona {f.id}. Periodo: {periodo}. Localidad: {f.localidad}. Superficie: {f.superficie_ha} ha. "
                f"Cuadras: {f.n_cuadras}{pob}.")
            ET.SubElement(pm, "styleUrl").text = "#" + periodo.replace(" ", "_")
            partes = list(forma.geoms) if isinstance(forma, MultiPolygon) else [forma]
            assert all(isinstance(p, Polygon) for p in partes)
            padre = ET.SubElement(pm, "MultiGeometry") if len(partes) > 1 else pm
            for p in partes:
                poligono_kml(padre, p)
            n += 1

    ET.indent(kml)
    ET.ElementTree(kml).write(DOCS / "zonas_nuevas.kml", encoding="utf-8", xml_declaration=True)
    z["en_kml"] = z.id.isin(elegidas.id).map({True: "sí", False: "no"})
    z.drop(columns="sup").to_csv(LISTA, index=False, encoding="utf-8-sig")
    print(f"{n} zonas en docs/zonas_nuevas.kml;", z.groupby("periodo").en_kml.value_counts().to_dict())


if __name__ == "__main__":
    main()
