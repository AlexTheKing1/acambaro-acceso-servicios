# CLAUDE.md — contexto y reglas del proyecto

## Proyecto
**"¿Quién está lejos hoy? Acceso a servicios básicos y expansión urbana en el municipio de Acámbaro, Guanajuato (clave 11002), 2010–2026."**

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
```
`02_recortar.py --solo <pasos>` corre solo algunos pasos (mg, mg2010, tablas, denue, servicios_mg, ghsl).

## Notas técnicas para Claude
- Red: inegi.org.mx, gob.mx y jrc.ec.europa.eu responden; **datos.gob.mx responde 403** (bloqueado por el proxy), dgis.salud.gob.mx y conapo.gob.mx no responden, y la API de SIGED (SEP) tiene una cadena de certificados incompleta (no desactivar la verificación TLS). Por eso CLUES, SEP y CONAPO vienen del release `datos-crudos` (ver `data/raw/LEEME.md`).
- Las páginas de INEGI son dinámicas; las URLs directas ya están en `src/01_descargar.py` y `docs/fuentes.md`, no hace falta volver a buscarlas.
- Leer zips sin descomprimir con `/vsizip/` (pyogrio/rasterio). Los CSV 2010 vienen en UTF-8 con BOM; el DENUE y la EIC en latin-1.
- Sistema de coordenadas de trabajo: el del MG (Cónica Conforme de Lambert, ITRF2008, metros). Los shapefiles rurales de 2010 no traen `.prj`; se les asigna la proyección de los urbanos (verificado: mediana de desplazamiento 0 m).
- Clave de manzana `800` = caserío disperso (puntos en la capa `caserio_disperso`, no polígonos).
- El MG de Michoacán se llama `16_michoacandeocampo.zip` (no `16_michoacan.zip`).
- Decisiones de Alejandro vigentes: "la ciudad" = cabecera (0001); Irámuco, Parácuaro y Chupícuaro son localidades aparte; las 4 urbanas se analizan por cuadra y se reportan por separado (D09). En textos públicos: "cuadra" o "localidad", no "manzana". Grupos ocultos por "*": por AGEB con el mínimo visible de apoyo (D10). Servicios hasta 10 km fuera, incluido Michoacán (D11). Cuadra nueva: < 50 % ya era manzana (D12). Validación con imágenes satelitales y Street View, no campo (D13).
- El DENUE registra pocas escuelas y centros de salud rurales: el catálogo usa MG EIC 2025 + DENUE (D14). Al llegar CLUES y SEP, contrastar y decidir.

## Estado
- Fase 0 y 1 (inventario y base geográfica): terminadas y revisadas por Alejandro el 2026-10-22 (decisiones D09–D12).
- Fase 2 (catálogo de servicios): versión con MG EIC 2025 + DENUE terminada el 2026-10-22. Pendiente: que Alejandro revise las listas de verificación y responda las preguntas de criterio (consultorios privados, escuelas privadas, qué tiendas cuentan como abasto, preparatoria abierta). Siguen faltando CLUES, SEP y CONAPO (release `datos-crudos` vacío).
