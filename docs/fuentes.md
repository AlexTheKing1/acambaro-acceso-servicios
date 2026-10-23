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

## Pendientes (las sube Alejandro al release `datos-crudos`; ver `data/raw/LEEME.md`)

| Dato | Página | Por qué no se bajó |
|---|---|---|
| CLUES vigente | http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html | dgis.salud.gob.mx no responde desde el entorno (error 502 en el proxy); datos.gob.mx responde 403 |
| Catálogo de escuelas SEP vigente | datos.gob.mx (`catalogo_centros_trabajo_sep`) o https://www.siged.sep.gob.mx/SIGED/escuelas.html | datos.gob.mx 403; la API de SIGED (`api.siged.sep.gob.mx`) presenta un certificado TLS incompleto y no se desactivó la verificación |
| CONAPO, índice de marginación urbana 2020 por AGEB y por colonia | https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372 | Los enlaces (`conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Marginacion/IMU_2020.zip`, `.../Colonia/IMC_2020.zip`, `.../Colonia/imc2020_shp.zip`) redirigen a una página 404 de gob.mx; conapo.gob.mx no responde |
