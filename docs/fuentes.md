# Fuentes de datos

Fecha de consulta y descarga de todo lo siguiente: **2026-10-22**. Las URLs directas están también en `src/01_descargar.py`, que las vuelve a bajar sin buscar nada. Tamaño y huella sha256 de cada archivo: `data/raw/manifiesto.csv`.

Prefijos usados abajo:
- `INEGI` = `https://www.inegi.org.mx/contenidos`
- `MG` = `https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia`

## Descargadas

| Dato | Versión / fecha | URL directa | Uso |
|---|---|---|---|
| Censo 2020, principales resultados por AGEB y manzana urbana, Guanajuato | Censo de Población y Vivienda 2020; archivo modificado 2021-07-26 (versión que completa las localidades urbanas < 2 500 hab.) | `INEGI/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_11_cpv2020_csv.zip` | Población y viviendas por manzana |
| ITER 2020, Guanajuato | Censo 2020; metadatos modificados 2022-05-19 | `INEGI/programas/ccpv/2020/datosabiertos/iter/iter_11_cpv2020_csv.zip` | Localidades: población y coordenadas |
| Censo 2010, principales resultados por AGEB y manzana urbana, Guanajuato | Censo 2010; modificado 2013-06-26 | `INEGI/programas/ccpv/2010/datosabiertos/ageb_y_manzana/resageburb_11_2010_csv.zip` | Comparación 2010 |
| ITER 2010, Guanajuato | Censo 2010; modificado 2013-06-26 | `INEGI/programas/ccpv/2010/datosabiertos/iter_11_2010_csv.zip` | Comparación 2010 |
| Cartografía geoestadística **urbana**, cierre del Censo 2010, Acámbaro | Producto 702825585853 (edición 2010) | `MG/urbana/SHP/Guanajuato/SHP/702825585853_s.zip` | Manzanas 2010 (3 localidades urbanas) |
| Cartografía geoestadística **rural**, cierre del Censo 2010, Acámbaro | Producto 702825561291 (edición 2010) | `MG/rural/SHP/Guanajuato/702825561291_s.zip` | Manzanas 2010 (78 localidades rurales amanzanadas) |
| Marco Geoestadístico, Censo de Población y Vivienda 2020, Guanajuato | Producto 889463807469; fecha de referencia 2019-09-13, insumos al 2020-11-30 | `MG/marcogeo/889463807469/11_guanajuato.zip` | Manzanas, localidades, AGEB, calles 2020 |
| Marco Geoestadístico 2025, Guanajuato | Producto 794551163061; edición 2025, referencia 2025-07-31 | `MG/marcogeo/794551163061/11_guanajuato.zip` | Respaldo / control (no es la más reciente) |
| **Marco Geoestadístico, Encuesta Intercensal 2025**, Guanajuato | Producto 794551196649; edición 2026, referencia 2025-11-14 (verificación de campo 8-sep a 14-nov-2025); metadatos 2026-08-25 | `MG/marcogeo/794551196649/11_guanajuato.zip` | **Versión más reciente**: manzanas posteriores a 2020 |
| Marco Geoestadístico, Encuesta Intercensal 2025, **Michoacán** (descargado 2026-10-22, fase 2) | Producto 794551196649; misma edición y referencia que el de Guanajuato | `MG/marcogeo/794551196649/16_michoacandeocampo.zip` (ojo: el nombre es `michoacandeocampo`; `16_michoacan.zip` devuelve una página HTML) | Escuelas, centros de salud y mercados de Michoacán a ≤ 10 km (capas `sip` y `sia`) |
| Encuesta Intercensal 2025, conjunto de datos abiertos "Principales resultados por localidad de 50 000 y más habitantes" (incluye total de cada municipio) | Levantamiento oct–nov 2025; publicado 2026-09-22 | `INEGI/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip` | Total municipal 2025 con error estándar e intervalo de confianza |
| DENUE Guanajuato | Corte 05_2026, modificado 2026-05-20 | `INEGI/masiva/denue/denue_11_csv.zip` | Abasto; escuelas y salud (con nombre y sector), junto con el MG |
| DENUE Michoacán | Corte 05_2026 | `INEGI/masiva/denue/denue_16_csv.zip` | Servicios del otro lado del límite estatal |
| DENUE Querétaro | Corte 05_2026 | `INEGI/masiva/denue/denue_22_csv.zip` | Ídem (resultó sin establecimientos a ≤ 10 km) |
| GHSL GHS-BUILT-S R2023A, 100 m, Mollweide, mosaico R7_C9, años 1975–2020 (cada 5) | Release R2023A, V1-0; archivos del servidor fechados 2025-01-27 | `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A/GHS_BUILT_S_E{AÑO}_GLOBE_R2023A_54009_100/V1-0/tiles/GHS_BUILT_S_E{AÑO}_GLOBE_R2023A_54009_100_V1_0_R7_C9.zip` | Serie histórica de superficie construida (solo observada) |

Páginas donde se localizaron (por si cambian las URLs):
- Censo 2020: https://www.inegi.org.mx/programas/ccpv/2020/ (pestaña Datos abiertos)
- Censo 2010: https://www.inegi.org.mx/programas/ccpv/2010/
- EIC 2025: https://www.inegi.org.mx/programas/eic/2025/
- Marco Geoestadístico: https://www.inegi.org.mx/temas/mg/ (Descargas) y fichas `https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=<producto>`
- DENUE: https://www.inegi.org.mx/app/descarga/ (DENUE, CSV por entidad)
- GHSL: https://human-settlement.emergency.copernicus.eu/download.php y el FTP del JRC

## Uso en la fase 2 (catálogo de servicios)
Escuelas, salud de primer nivel y mercados: capas de servicios del MG EIC 2025 (Gto. y Mich.) unidas con el DENUE 05/2026. Abarrotes, minisúper y supermercados: solo DENUE. Detalle en `docs/decisiones.md` (D14–D17).

## Fase 3 (descargadas el 2026-10-23)

| Dato | Versión / fecha | URL directa | Uso |
|---|---|---|---|
| CLUES, establecimientos de salud (nacional; hoja `CLUES_202608`) | Corte **agosto 2026** (DGIS, Secretaría de Salud). Subido por Alejandro al release | `https://github.com/AlexTheKing1/acambaro-acceso-servicios/releases/download/datos-crudos/ESTABLECIMIENTO_SALUD_202608.xlsx` | Confirmar unidades de salud, institución, estatus de operación, público/privado |
| Catálogo de centros de trabajo de la SEP, **Guanajuato** | Archivo `cct11.csv` (latin-1), 22 017 registros; sin fecha de corte ni ciclo escolar en el archivo; se cita la **fecha de consulta 2026-10-22** (D40, V35) | `.../releases/download/datos-crudos/cct11.csv` | Confirmar escuelas, nivel, sostenimiento, estatus y turnos |
| Catálogo de centros de trabajo de la SEP, **Michoacán** | Archivo `cct16.csv` (latin-1), 26 898 registros; misma observación (consulta 2026-10-22) | `.../releases/download/datos-crudos/cct16.csv` | Escuelas de Michoacán en la franja de 10 km |
| Catálogo de asentamientos humanos de Acámbaro (Catálogo Único de Claves Geoestadísticas, INEGI) | Servicio web v2; 147 asentamientos; campo `periodo` = **11/2021**; fuente declarada: Censo 2020. **Sin polígonos** | `https://gaia.inegi.org.mx/wscatgeo/v2/asentamientos/11/002` (JSON) | Nombres de colonia (D24) |

- Del catálogo SEP se quitan, al recortar, las columnas de contacto (nombre, CURP, RFC, teléfono y correo del director); de la CLUES, teléfonos y RFC. No se usan y no se versionan.
- Ninguna de estas fuentes trae matrícula o número de alumnos (D23).

### Intentadas sin éxito (fase 3)
| Dato | Qué se intentó | Resultado |
|---|---|---|
| Red Nacional de Caminos (RNC) 2024, INEGI | Ficha `https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551132173` y página `https://www.inegi.org.mx/programas/rnc/` (2 intentos) | Páginas dinámicas: no muestran el enlace de descarga sin navegador |
| OpenStreetMap vía Overpass | `https://overpass-api.de/api/interpreter`, recuadro municipio + 15 km (consulta en `src/01_descargar.py`) | Conexión cortada por el proxy del entorno ("tunnel closed"), 2 intentos; por un error de Claude se hicieron 2 intentos más al volver a correr la descarga (4 en total) |
| OpenStreetMap, extracto de México de Geofabrik | `https://download.geofabrik.de/north-america/mexico-latest.osm.pbf` | Conexión cortada por el proxy, 2 intentos (una consulta de encabezados y una descarga) |
| CONAPO, índices de marginación urbana 2020 | (fase 0) | No disponible; sustituido según D24 |

## Antes pendientes

- CLUES y catálogo SEP: no se podían bajar desde el entorno (dgis.salud.gob.mx no responde; datos.gob.mx 403; certificado incompleto en la API de SIGED). Alejandro los subió al release `datos-crudos` el 2026-10-23 (tabla de arriba).
- CONAPO, índice de marginación urbana 2020 por AGEB y por colonia (https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372): los enlaces `conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/...` redirigen a una página 404 y conapo.gob.mx no responde. **No disponible**: sustituido según D24 y declarado como limitación.
- `verificacion_servicios.csv`: subido el 2026-10-23 (fase 4, tabla de abajo). `verificacion_zonas.csv`: sigue pendiente (404); `01_descargar.py` lo baja cuando exista.

## Fase 4 (2026-10-23)

| Dato | Versión / fecha | URL directa | Uso |
|---|---|---|---|
| Verificación remota de servicios de Alejandro (Google Maps: satélite y Street View) | `verificacion_servicios.csv`, 134 filas, 68 revisadas; subido al release el 2026-10-23 | `.../releases/download/datos-crudos/verificacion_servicios.csv` | Marca `dudoso_remoto`, tasas de confirmación y lista de campo (D41, V37) |
| Verificación de rutas de Alejandro (Google Maps, a pie) | 5 rutas, 2026-10-23 (cifras dadas en la conversación) | — (anotadas en `docs/verificar_rutas.csv`) | V36 |
| Ubicación del CECyTE, ISSSTE, Secundaria Técnica 24 | Consulta de Alejandro en Google Maps y verificación local, 2026-10-23 | — | D36, D37, D39 |

### Intentadas sin éxito (fase 4)
| Dato | Qué se intentó | Resultado |
|---|---|---|
| OpenStreetMap vía Overpass (sesión nueva) | `https://overpass-api.de/api/interpreter`, misma consulta | "Connection reset by peer", 2 intentos |
| Texto del SNEU (SEDESOL), tomo Educación | 2 búsquedas web dirigidas | Solo fuentes secundarias; no se encontró el documento original (V31) |
