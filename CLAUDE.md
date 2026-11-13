# CLAUDE.md — contexto y reglas del proyecto

## Proyecto
**"¿Quién está lejos hoy? Acceso a servicios y vaciamiento urbano en Acámbaro"** (título de trabajo, D51; puede cambiar al redactar). Municipio de Acámbaro, Guanajuato (clave 11002), 2010–2026.

Roles: Alejandro define preguntas, umbrales, interpretaciones y conclusiones. Claude hace el trabajo técnico, propone opciones con pros y contras y pide decisión cuando algo es de criterio y no técnico. Alejandro no programa: los resultados se le explican en lenguaje llano, con cifras y mapas, no con código.

- **Servicios**: versiones más recientes disponibles (DENUE vigente, CLUES vigente, catálogo de escuelas SEP vigente). El análisis describe el acceso **actual**.
- **Población**: Censo 2020 por manzana (la fuente más reciente a ese nivel; no habrá otra hasta el Censo 2030). Encuesta Intercensal (EIC) 2025 a nivel municipal solo como contexto y para ajustar totales. Esta limitación se declara en el reporte.
- **Escala ciudad**: distancia a pie por la red de calles desde cada manzana urbana al servicio más cercano de cada tipo: preescolar, primaria, secundaria, bachillerato, salud de primer nivel, abasto (mercados, abarrotes, supermercados). Población afectada total y por grupo: 3–5, 6–11, 12–14, 15–17, 60+, con discapacidad.
- **Escala municipio**: distancia por carretera desde cada localidad (ITER 2020) a esos servicios.
- **Crecimiento**: comparar Marco Geoestadístico (MG) 2010, 2020 y el más reciente (MG EIC 2025, edición 2026) para identificar manzanas creadas en 2010–2020 y después de 2020. Las posteriores a 2020 no tienen población censada: se analizan por ubicación y distancia, **sin inventar población**. GHSL GHS-BUILT-S solo para la serie observada hasta 2020 (2025–2030 son modelados, no se usan como evidencia). Viviendas deshabitadas y de uso temporal por manzana (Censo 2020).
- **Entregable final**: sitio estático en GitHub Pages (historia guiada con mapa que cambia por sección + explorador con filtros por colonia/localidad y tipo de servicio, conectado al mismo mapa) y un reporte PDF generado del mismo contenido. Todo en español.

## Reglas de trabajo
1. Mantener este archivo al día.
2. Todo reproducible: scripts numerados en `src/` (`01_...`, `02_...`), datos originales intactos en `data/raw/`, intermedios en `data/processed/`. Python con geopandas; librerías estables fijadas en `requirements.txt`.
3. Nunca inventar ni completar datos. Si algo falta o no cuadra, decirlo.
4. `docs/decisiones.md`: cada decisión metodológica con fecha, opciones, quién decidió y por qué.
5. `docs/validacion.md`: cada chequeo con resultado en cifras, incluido lo que salió mal.
6. INEGI oculta datos ("*") en manzanas con pocas viviendas y en valores de 1 y 2: cuantificar la población perdida en cada paso.
7. `docs/fuentes.md`: versión, fecha y URL de cada dato usado.
8. Trabajar por fases y detenerse al final de cada una con un resumen para Alejandro: qué se hizo, qué se encontró, qué validar, qué decisión se necesita.
9. Los crudos pesados nunca se suben: `data/raw/` está en `.gitignore` (salvo `LEEME.md`). Solo se versionan los recortes de Acámbaro en `data/processed/` y los scripts que los generan.

## Cómo se reproduce
```
pip install -r requirements.txt
python src/01_descargar.py      # baja crudos a data/raw/ (y del release "datos-crudos" lo que no es descargable)
python src/02_recortar.py       # recortes de Acámbaro -> data/processed/
python src/03_base_geografica.py  # población 2020 por manzana, localidades, manzanas nuevas, chequeos
python src/04_inventario.py     # docs/inventario.md
python src/05_mapa_fase1.py     # docs/figuras/fase1_base.png
python src/06_catalogo_servicios.py   # catálogo: data/processed/servicios.gpkg, servicios_sedes.csv
python src/07_listas_verificacion.py  # docs/verificar_zonas_nuevas.csv, docs/verificar_servicios_muestra.csv
python src/08_mapa_fase2.py     # docs/figuras/fase2_servicios.png
python src/09_catalogo_sep_clues.py   # catálogo con SEP y CLUES: servicios_fase3.gpkg, servicios_sedes_fase3.csv (+ columna en la muestra)
python src/10_redes.py          # red de calles para caminar: red_peatonal.gpkg
python src/15_catalogo_fase4.py # decisiones finales + verificación remota: servicios_fase4.gpkg, servicios_sedes_fase4.csv
python src/11_accesibilidad.py  # distancias y población lejana (umbrales definitivos): acceso_*.csv/gpkg, conteo_servicios_por_localidad.csv
python src/12_colonias_contexto.py  # colonias_cuadras.csv, contexto_ageb.csv, contexto_localidades.csv
python src/13_mapas_fase3.py    # docs/figuras/fase4_<categoría>.png (las fase3_*.png quedan como registro)
python src/14_verificar_rutas.py  # docs/verificar_rutas.csv (conserva lo anotado por Alejandro)
python src/17_zonas_kml.py      # docs/zonas_nuevas.kml + columna en_kml en verificar_zonas_nuevas.csv
python src/18_verificar_campo.py  # docs/verificar_campo.csv
python src/19_crecimiento.py    # fase 4b: cuadras_antiguedad, crecimiento_*.csv, tipologia_ageb.csv
python src/20_ghsl_serie.py     # ghsl_serie.csv, ghsl_sectores.csv
python src/21_mapas_fase4b.py   # docs/figuras/fase4b_*.png
python src/22_ghsl_sin_cuadras.py  # fase 4c: construcción GHSL fuera de cuadras -> ghsl_*.csv/gpkg, docs/zonas_ghsl_sin_cuadras.kml, docs/verificar_zonas_ghsl.csv
python src/23_verificacion_zonas.py   # fase 5: revisión de zonas INEGI y GHSL, cambio de cartografía (D54)
python src/24_comparacion_regional.py # comparacion_regional.csv, docs/figuras/fase5_regional.png
python src/25_vaciamiento_correlatos.py  # vaciamiento_*.csv
python src/26_nse_aproximado.py       # nse_*.csv, docs/figuras/fase5_nse.png
python src/27_salud_abierta.py        # fase 6: salud_clasificacion_instituciones.csv, acceso_salud_abierta.csv, salud_abierta_resumen.csv
python src/28_localidades_y_polos.py  # localidades_2500.csv, polos_desarrollo.csv (necesita 27)
python src/29_vialidades.py           # servicios_junto_carretera.csv (no interpretable, D61)
python src/30_planes.py               # docs/verificar_citas_planes.csv, iramuco_serie.csv, proyecciones_vs_censo.csv, docs/figuras/fase6_proyeccion.png, docs/verificar_campo_fase6.csv
```
La fase 5 necesita `01_descargar.py --solo verificacion iter2010 iter2020 iter_nacional eic2025 censo2020_ageb_mza`. Todas escriben su parte en `validacion_fase5.json`.
La fase 6 (27–30) necesita `01_descargar.py --solo planes iter2000 iter2005 iter2010 iter2020` (27–29 solo usan `data/processed/`). Escriben en `validacion_fase6.json`. `30` usa `pdftotext` (poppler-utils).
`15` necesita `data/raw/verificacion/verificacion_servicios.csv` (`01_descargar.py --solo verificacion`). No hay `16` (reservado para la red rural si algún día se baja).
`01_descargar.py --solo <fuentes>` baja solo esas fuentes (p. ej. `clues sep_escuelas asentamientos`); la red de OpenStreetMap solo se intenta con `--solo osm_caminos`.
`02_recortar.py --solo <pasos>` corre solo algunos pasos (mg, mg2010, tablas, denue, servicios_mg, ghsl, sep, clues).

## Notas técnicas para Claude
- Red: inegi.org.mx, gob.mx y jrc.ec.europa.eu responden; **datos.gob.mx responde 403** (bloqueado por el proxy), dgis.salud.gob.mx y conapo.gob.mx no responden, y la API de SIGED (SEP) tiene una cadena de certificados incompleta (no desactivar la verificación TLS). Por eso CLUES y SEP vienen del release `datos-crudos` (ver `data/raw/LEEME.md`); CONAPO no está disponible (D24). gaia.inegi.org.mx (servicios web del Catálogo Único) sí responde: claves con formato `/asentamientos/11/002`.
- Las páginas de INEGI son dinámicas; las URLs directas ya están en `src/01_descargar.py` y `docs/fuentes.md`, no hace falta volver a buscarlas.
- Leer zips sin descomprimir con `/vsizip/` (pyogrio/rasterio). Los CSV 2010 vienen en UTF-8 con BOM; el DENUE y la EIC en latin-1.
- Sistema de coordenadas de trabajo: el del MG (Cónica Conforme de Lambert, ITRF2008, metros). Los shapefiles rurales de 2010 no traen `.prj`; se les asigna la proyección de los urbanos (verificado: mediana de desplazamiento 0 m).
- Clave de manzana `800` = caserío disperso (puntos en la capa `caserio_disperso`, no polígonos).
- El MG de Michoacán se llama `16_michoacandeocampo.zip` (no `16_michoacan.zip`).
- Decisiones de Alejandro vigentes: "la ciudad" = cabecera (0001); Irámuco, Parácuaro y Chupícuaro son localidades aparte; las 4 urbanas se analizan por cuadra y se reportan por separado (D09). En textos públicos: "cuadra" o "localidad", no "manzana". Grupos ocultos por "*": por AGEB con el mínimo visible de apoyo (D10). Servicios hasta 10 km fuera, incluido Michoacán (D11). Cuadra nueva: < 50 % ya era manzana (D12). Validación con imágenes satelitales y Street View, no campo (D13).
- El DENUE registra pocas escuelas y centros de salud rurales: el catálogo usa MG EIC 2025 + DENUE (D14), contrastado con SEP y CLUES en la fase 3 (D29): sedes confirmadas, no confirmadas (se conservan), nuevas y dadas de baja (no se usan).
- El DENUE prácticamente no registra comercios ni consultorios fuera de las 4 localidades urbanas: tienda básica y consultorio privado no se miden en lo rural (D32).
- Decisiones de fase 3 vigentes: salud principal = públicas de primer nivel (D20; consultorios privados, casas de salud y unidad móvil aparte, D27); escuelas todas y solo públicas (D21); tienda básica / abasto completo (D22); preparatoria abierta = "bachillerato no escolarizado", no cuenta (D23); CONAPO sustituido (D24); red rural = línea recta × 1.33 porque no hubo red descargable (D26; Overpass volvió a fallar en la fase 4); sensibilidad con solo confirmadas (D28).
- Decisiones de fase 4 (Alejandro): umbral principal en ciudad = radio SNEU × 1.33 (preescolar 1 000, primaria 670, secundaria 1 330, bachillerato 3 330, salud 1 330, tienda 500, abasto 1 000 m); estricto = radio sin convertir, holgado = principal × 1.5; rural igual que en la fase 3; factor fijo 1.33 (D33). Salud sin CLUES (6) solo en anexo (D34). Tienda rural no medible; abasto completo rural sí se mide, sin tianguis (D35). ISSSTE en operación (D36). CECyTE = punto MG/DENUE de Valle de Acámbaro; punto SEP descartado (D37). Consultorio del CERESO fuera (D38). Parácuaro: "no hay secundaria dentro de la localidad", la atiende la ST 24 (D39). SEP fechado por consulta 2026-10-22 (D40). Verificación remota: "no" = `dudoso_remoto`, nunca se borra; sensibilidad sin ellos; las tasas no son muestra al azar (D41).
- Red y proxy: overpass-api.de y download.geofabrik.de cortan la conexión en el proxy (2026-10-23) aunque Alejandro los agregó; la RNC del INEGI no tiene URL directa localizable. No reintentar más de dos veces por fuente.
- La CLUES trae espacios al final en algunos campos (p. ej. "SERVICIOS DE SALUD IMSS BIENESTAR "): limpiar antes de comparar. El catálogo SEP trae datos personales del director (CONTACTO_*): se quitan al recortar.
- Fase 4b: las deshabitadas y de uso temporal de 2010 están ocultas en 9 de cada 10 manzanas; la década se compara con totales por localidad y por "unidades comparables" de AGEB (D44). En 2020 se usa viviendas − habitadas (pocos ocultos). Los ITER 1990–2005 no tienen URL directa (V43): no reintentar.
- La clave de una cuadra nueva posterior a 2020 puede repetir la de una cuadra 2020 renumerada: no unir tablas por CVEGEO entre ediciones; usar posición o la pareja (CVEGEO, origen).
- Decisiones de fase 4c (Alejandro): tipología final con desatendida = 3 de 5 (2 de 5 como sensibilidad) y vaciándose dentro de su localidad (D47); centro = punto ITER 2020 (D48); cuadras nuevas en textos públicos con conteos, no porcentajes, y se mantiene el preescolar (D49); ITER 1990–2005 no se buscan (D50); título de trabajo (D51). Zona GHSL sin cuadras = ≥ 500 m² ganados 2010–2020 y < 25 % de la celda en cuadras del MG EIC 2025 (D52, provisional).
- `19_crecimiento.py` reescribe `validacion_fase4b.json` sin las claves de `20` y `22`: correr `20` y `22` después de `19`.
- Claves de los municipios vecinos (Gto.): Coroneo 010, Jerécuaro **019**, Salvatierra 028, Santiago Maravatío **036**, Tarandacuao 038, Tarimoro 039 (018 y 031 son otros municipios). El ITER nacional 2010 trae encabezados en minúsculas. En la EIC 2025, PCN_HOG_OPAIS = hogares que **reciben remesas**.
- Planes (fase 6): en el PROT se cita la **página impresa** (= página del PDF − 1); en el Plan Municipal coinciden. Cada cita del contraste se verifica en `30_planes.py` (lista `CITAS`): si se agrega una cita a `docs/contraste_planes.md`, agregarla ahí. Los "polos de desarrollo" del Plan Municipal son sus 8 "ejes de desarrollo" (micro regiones). SEDESOL 1999, SEDATU–GIZ 2024 y NOM-002 no están en el repositorio: se citan con las páginas de Alejandro, sin cotejar.
- ITER 2000 (`cgpv2000_iter_11_csv.zip`) y 2005 (`cpv2005_iter_11_csv.zip`, columnas `p_total`, `t_vivhab`) sí tienen URL directa (fase 6). No traen viviendas deshabitadas.
- Decisiones de fase 6: salud abierta = SSG + IMSS-Bienestar + UMR del IMSS (con sensibilidad sin UMR); solo derechohabientes = IMSS ordinario (UMF, HGSMF, UMFH) e ISSSTE; SMP fuera; DIF solo si da consulta (D58). "Dentro de la localidad" = misma clave de localidad; distancia desde el punto ITER × 1.33 (D59). Polos: 7 rurales evaluados, ciudad como referencia; sin mercado = "no verificable" (D60). Vialidad primaria no realizable; carretera no interpretable (D61). Cifras de los planes con página y cuadro, sin aproximadas (D62). ITER 2000/2005 solo para la gráfica e Irámuco (D63).
- Decisiones de fase 5: D52 aceptado como detección de construcción, no de vivienda (Alejandro). Z20-010 excluida por error de dibujo (D53, `EXCLUIR_ZONAS` en `19`). Zona 2010–2020 en localidad con población en el ITER 2010 = cambio de cartografía, salvo en las 4 urbanas = crecimiento (D54, confirmado por Alejandro); las 28 zonas urbanas 2010–2020 no verificadas en imágenes se declaran como limitación. Comparación regional sobre VIVTOT, EIC 2025 con IC 90 % (D55). Índice socioeconómico aproximado, z dentro de cada conjunto, urbano y rural nunca se comparan, sin piso de tierra (D56, aprobado; el cruce rural índice–acceso es un indicio, no un hallazgo). Cruces con ≥ 30 viviendas (D57).

## Estado
- Fase 0 y 1 (inventario y base geográfica): terminadas y revisadas por Alejandro el 2026-10-22 (decisiones D09–D12).
- Fase 2 (catálogo de servicios): terminada el 2026-10-22; preguntas de criterio respondidas por Alejandro el 2026-10-23 (D20–D24). Alejandro está revisando `docs/verificar_servicios_muestra.csv` (no regenerarla).
- Fase 3 (accesibilidad): terminada el 2026-10-23. Resumen en `docs/resumen_fase3.md`; sus pendientes se cerraron en la fase 4.
- Fase 4 (decisiones finales y números definitivos): terminada el 2026-10-23. Resumen en `docs/resumen_fase4.md`. Pendiente de Alejandro: cotejar el texto original del SNEU (no se pudo abrir), salidas de campo con `docs/verificar_campo.csv`, revisar zonas con `docs/zonas_nuevas.kml` y subir `verificacion_zonas.csv`, red de caminos (RNC al release). Siguiente: sitio web y reporte PDF.
- Fase 4b (crecimiento urbano y acceso): terminada el 2026-10-23, **provisional** hasta que llegue `verificacion_zonas.csv`. Resumen en `docs/resumen_fase4b.md`.
- Fase 4c (decisiones de la 4b y crecimiento no registrado): terminada el 2026-10-23; la parte provisional se cerró en la fase 5. Decisiones D47–D51 registradas; tipología final sin cambios en cifras. El GHSL ve 41.6 de 66.6 ha nuevas de la ciudad fuera de cuadras (sección 6 del resumen de la 4b, **provisional**). Pendiente de Alejandro: revisar `docs/zonas_ghsl_sin_cuadras.kml` / `docs/verificar_zonas_ghsl.csv` y aprobar el criterio D52. Siguiente: sitio web y reporte PDF.
- Fase 6 (ajustes, normas y contraste con los planes): terminada el 2026-11-13. Salud abierta (en la ciudad, lejos 22 % → 58 %), localidades de 2 500 o más, polos del Plan Municipal, Irámuco 2000–2020, proyección contra censo, `docs/metodo.md` y `docs/contraste_planes.md`. `docs/resumen_final.md` actualizado (sección 8: qué cambió). Pendiente de Alejandro: qué medida de salud va como principal, plan municipal reciente o PMDUOET, campo (Parácuaro en `docs/verificar_campo_fase6.csv`). Siguiente: sitio web y reporte PDF.
- Fase 5 (cierre del análisis): terminada el 2026-11-13. Verificaciones de zonas incorporadas (4b y 4c ya no son provisionales; cifras urbanas sin cambio), comparación regional, correlatos del vaciamiento, índice socioeconómico aproximado. **Resumen base para redactar: `docs/resumen_final.md`.** D54 y D56 confirmadas por Alejandro el 2026-11-13. Pendiente de Alejandro: el SNEU, el campo y la RNC. Siguiente: sitio web y reporte PDF.
