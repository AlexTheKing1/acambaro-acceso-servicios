# Inventario de datos

Generado por `src/04_inventario.py`. Versiones y fechas de publicación: `docs/fuentes.md`.

## Archivos crudos (data/raw/, no versionados)

| Fuente | Archivo | MB | Contenido del zip |
|---|---|---|---|
| censo2020_ageb_mza | ageb_mza_urbana_11_cpv2020_csv.zip | 10.4 | 3 archivos; datos: conjunto_de_datos_ageb_urbana_11_cpv2020.csv, diccionario_datos_ageb_urbana_11_cpv2020.csv |
| iter2020 | iter_11_cpv2020_csv.zip | 1.9 | 4 archivos; datos: tam_loc.csv.csv, conjunto_de_datos_iter_11CSV20.csv, diccionario_datos_iter_11CSV20.csv |
| censo2010_ageb_mza | resageburb_11_2010_csv.zip | 6.5 | 3 archivos; datos: resultados_ageb_urbana_11_cpv2010.csv, fd_resultados_ageb_urbana_cpv2010.csv |
| iter2010 | iter_11_2010_csv.zip | 1.3 | 4 archivos; datos: tam_loc.csv, iter_11_cpv2010.csv, fd_iter_cpv2010.csv |
| mg2010_acambaro | 702825585853_s.zip | 0.7 | 108 archivos; datos: 110020027A.shp, 110020027CA.shp, 110020027E.shp, 110020027L.shp … (+23) |
| mg2010_acambaro | 702825561291_s.zip | 1.4 | 1401 archivos; datos: 110020176E.shp, 110020176L.shp, 110020176M.shp, 110020176SIA.shp … (+463) |
| mg2020 | 11_guanajuato.zip | 133.2 | 96 archivos; datos: 11a.shp, 11ar.shp, 11cd.shp, 11e.shp … (+18) |
| mg2025 | 11_guanajuato.zip | 126.1 | 96 archivos; datos: 11a.shp, 11ar.shp, 11cd.shp, 11e.shp … (+18) |
| mg_eic2025 | 11_guanajuato.zip | 126.4 | 101 archivos; datos: 11a.shp, 11ar.shp, 11cd.shp, 11e.shp … (+18) |
| eic2025 | conjunto_de_datos_eic2025_105_csv.zip | 8.3 | 3 archivos; datos: conjunto_datos_eic2025_105.csv, diccionario_datos_eic2025_105.csv |
| denue | denue_11_csv.zip | 28.0 | 3 archivos; datos: denue_diccionario_de_datos.csv, denue_inegi_11_.csv |
| denue | denue_16_csv.zip | 26.9 | 3 archivos; datos: denue_diccionario_de_datos.csv, denue_inegi_16_.csv |
| denue | denue_22_csv.zip | 10.4 | 3 archivos; datos: denue_diccionario_de_datos.csv, denue_inegi_22_.csv |
| ghsl_built_s | GHS_BUILT_S_E1975_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 7.5 | 2 archivos; datos: GHS_BUILT_S_E1975_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E1980_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 8.3 | 2 archivos; datos: GHS_BUILT_S_E1980_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E1985_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 9.0 | 2 archivos; datos: GHS_BUILT_S_E1985_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E1990_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 9.7 | 2 archivos; datos: GHS_BUILT_S_E1990_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E1995_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 10.2 | 2 archivos; datos: GHS_BUILT_S_E1995_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E2000_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 10.7 | 2 archivos; datos: GHS_BUILT_S_E2000_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E2005_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 11.5 | 2 archivos; datos: GHS_BUILT_S_E2005_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E2010_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 12.4 | 2 archivos; datos: GHS_BUILT_S_E2010_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E2015_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 13.8 | 2 archivos; datos: GHS_BUILT_S_E2015_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |
| ghsl_built_s | GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip | 14.9 | 2 archivos; datos: GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100_V1_0_R7_C9.tif |

## Capas geográficas recortadas a Acámbaro (data/processed/*.gpkg)

| Archivo | Capa | Registros | Geometría | Sistema de coordenadas | Columnas clave |
|---|---|---|---|---|---|
| localidades2020.gpkg | localidades | 212 | Point | WGS 84 (EPSG:4326) | CVEGEO, LOC, NOM_LOC, POBTOT, VIVTOT |
| manzanas2020_poblacion.gpkg | manzanas | 1620 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, AMBITO, TIPOMZA, NOM_LOC, POBTOT |
| manzanas2020_poblacion.gpkg | caserio_disperso | 32 | MultiPoint | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, TIPOMZA, AMBITO, NOM_LOC, POBTOT |
| manzanas_cambios.gpkg | eic2025_vs_2020 | 3522 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, AMBITO |
| manzanas_cambios.gpkg | mg2020_vs_2010 | 3505 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, AMBITO |
| mg2010_acambaro.gpkg | manzanas | 3159 | MultiPolygon | North_America_Lambert_Conformal_Conic_ITRF_1992 | CVEGEO, CVE_LOC, AMBITO |
| mg2010_acambaro.gpkg | localidades_amanzanadas | 81 | Polygon | North_America_Lambert_Conformal_Conic_ITRF_1992 | CVEGEO, CVE_LOC, AMBITO |
| mg2010_acambaro.gpkg | ageb_urbanas | 110 | Polygon | North_America_Lambert_Conformal_Conic_ITRF_1992 | CVEGEO, CVE_LOC, AMBITO |
| mg2010_acambaro.gpkg | vialidades | 6098 | LineString | North_America_Lambert_Conformal_Conic_ITRF_1992 | CVE_LOC, AMBITO, CVEGEO |
| mg2010_acambaro.gpkg | servicios_puntos | 593 | Point | North_America_Lambert_Conformal_Conic_ITRF_1992 | TIPO, CVE_LOC, AMBITO, CVEGEO |
| mg2010_acambaro.gpkg | servicios_areas | 112 | Polygon | North_America_Lambert_Conformal_Conic_ITRF_1992 | TIPO, CVE_LOC, AMBITO, CVEGEO |
| mg2010_acambaro.gpkg | servicios_lineas | 1029 | LineString | North_America_Lambert_Conformal_Conic_ITRF_1992 | TIPO, CVE_LOC, AMBITO, CVEGEO |
| mg2020_acambaro.gpkg | municipio | 1 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, NOMGEO |
| mg2020_acambaro.gpkg | localidades_amanzanadas | 105 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMGEO, AMBITO |
| mg2020_acambaro.gpkg | localidades_puntuales_rurales | 282 | Point | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, NOMGEO |
| mg2020_acambaro.gpkg | ageb_urbanas | 126 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB |
| mg2020_acambaro.gpkg | ageb_rurales | 13 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_AGEB |
| mg2020_acambaro.gpkg | manzanas | 3505 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, AMBITO, TIPOMZA |
| mg2020_acambaro.gpkg | vialidades | 9561 | LineString | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, AMBITO |
| mg2020_acambaro.gpkg | caserio_disperso | 142 | MultiPoint | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, TIPOMZA, AMBITO |
| mg2020_acambaro.gpkg | poligonos_externos | 121 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC |
| mg2020_acambaro.gpkg | poligonos_externos_manzana | 32 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA |
| mg2020_acambaro.gpkg | servicios_puntos | 581 | Point | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, NOMSERV, TIPO, AMBITO |
| mg2020_acambaro.gpkg | servicios_areas | 150 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMSERV, TIPO, AMBITO |
| mg2020_acambaro.gpkg | servicios_lineas | 989 | LineString | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMSERV, TIPO, AMBITO |
| mg2025_acambaro.gpkg | municipio | 1 | Polygon | Mexico ITRF2008 / LCC (EPSG:6372) | CVEGEO, NOMGEO |
| mg2025_acambaro.gpkg | localidades_amanzanadas | 105 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMGEO, AMBITO |
| mg2025_acambaro.gpkg | localidades_puntuales_rurales | 282 | Point | Mexico ITRF2008 / LCC (EPSG:6372) | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, NOMGEO |
| mg2025_acambaro.gpkg | ageb_urbanas | 124 | Polygon | MEXICO_ITRF_2008_LCC | CVE_LOC, CVE_AGEB, CVEGEO |
| mg2025_acambaro.gpkg | ageb_rurales | 13 | Polygon | Mexico ITRF2008 / LCC (EPSG:6372) | CVEGEO, CVE_AGEB |
| mg2025_acambaro.gpkg | manzanas | 3520 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, AMBITO, TIPOMZA |
| mg2025_acambaro.gpkg | vialidades | 9643 | LineString | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, AMBITO |
| mg2025_acambaro.gpkg | caserio_disperso | 156 | MultiPoint | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, TIPOMZA, AMBITO |
| mg2025_acambaro.gpkg | poligonos_externos | 115 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC |
| mg2025_acambaro.gpkg | poligonos_externos_manzana | 41 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA |
| mg2025_acambaro.gpkg | servicios_puntos | 621 | Point | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, NOMSERV, TIPO, AMBITO |
| mg2025_acambaro.gpkg | servicios_areas | 226 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMSERV, TIPO, AMBITO |
| mg2025_acambaro.gpkg | servicios_lineas | 1413 | LineString | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMSERV, TIPO, AMBITO |
| mg_eic2025_acambaro.gpkg | municipio | 1 | Polygon | Mexico ITRF2008 / LCC (EPSG:6372) | CVEGEO, NOMGEO |
| mg_eic2025_acambaro.gpkg | localidades_amanzanadas | 105 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMGEO, AMBITO |
| mg_eic2025_acambaro.gpkg | localidades_puntuales_rurales | 282 | Point | Mexico ITRF2008 / LCC (EPSG:6372) | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, NOMGEO |
| mg_eic2025_acambaro.gpkg | ageb_urbanas | 124 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB |
| mg_eic2025_acambaro.gpkg | ageb_rurales | 13 | Polygon | Mexico ITRF2008 / LCC (EPSG:6372) | CVEGEO, CVE_AGEB |
| mg_eic2025_acambaro.gpkg | manzanas | 3522 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, AMBITO, TIPOMZA |
| mg_eic2025_acambaro.gpkg | vialidades | 9648 | LineString | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, AMBITO |
| mg_eic2025_acambaro.gpkg | caserio_disperso | 156 | MultiPoint | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, TIPOMZA, AMBITO |
| mg_eic2025_acambaro.gpkg | poligonos_externos | 115 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC |
| mg_eic2025_acambaro.gpkg | poligonos_externos_manzana | 41 | MultiPolygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA |
| mg_eic2025_acambaro.gpkg | servicios_puntos | 621 | Point | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, CVE_AGEB, CVE_MZA, NOMSERV, TIPO, AMBITO |
| mg_eic2025_acambaro.gpkg | servicios_areas | 226 | Polygon | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMSERV, TIPO, AMBITO |
| mg_eic2025_acambaro.gpkg | servicios_lineas | 1413 | LineString | MEXICO_ITRF_2008_LCC | CVEGEO, CVE_LOC, NOMSERV, TIPO, AMBITO |

## Tablas recortadas a Acámbaro (data/processed/*.csv)

| Archivo | Filas | Columnas | Columnas clave |
|---|---|---|---|
| censo2010_mza_acambaro.csv | 1465 | 198 | LOC, NOM_LOC, AGEB, MZA, POBTOT, VIVTOT |
| censo2020_mza_acambaro.csv | 1783 | 230 | LOC, NOM_LOC, AGEB, MZA, POBTOT, VIVTOT |
| denue_acambaro_buffer10km.csv | 16142 | 43 | codigo_act, nombre_act, per_ocu, latitud, longitud, fecha_alta |
| eic2025_acambaro.csv | 10 | 349 | CVEGEO, CVE_LOC, NOM_LOC, ESTIMADOR, POBTOT |
| iter2010_acambaro.csv | 217 | 200 | LOC, NOM_LOC, LONGITUD, LATITUD, POBTOT, VIVTOT |
| iter2020_acambaro.csv | 215 | 286 | LOC, NOM_LOC, LONGITUD, LATITUD, POBTOT, VIVTOT |
| localidades2020.csv | 212 | 9 | CVEGEO, LOC, NOM_LOC, POBTOT, VIVTOT |

## GHS-BUILT-S R2023A dentro del municipio (solo años observados)

Mollweide (ESRI:54009), celdas de 100 m; valor = m² construidos por celda.

| Año | Superficie construida (ha) | Celdas con algo construido |
|---|---|---|
| 1975 | 357 | 3,575 |
| 1980 | 421 | 4,327 |
| 1985 | 503 | 4,989 |
| 1990 | 603 | 5,702 |
| 1995 | 763 | 6,507 |
| 2000 | 971 | 7,247 |
| 2005 | 1,031 | 7,813 |
| 2010 | 1,107 | 8,429 |
| 2015 | 1,203 | 9,533 |
| 2020 | 1,358 | 10,370 |
