# Registro de decisiones metodológicas

Formato: fecha · decisión · opciones consideradas · quién decidió · por qué. Las marcadas **(provisional)** las tomó Claude por ser técnicas o para poder avanzar, y Alejandro puede cambiarlas.

---

### D01 · 2026-10-22 · Versión "más reciente" del Marco Geoestadístico
- **Decisión**: usar el *MG, Encuesta Intercensal 2025* (edición 2026, referencia 2025-11-14). El MG 2025 (referencia 2025-07-31) se baja solo como control.
- **Opciones**: MG 2025 · MG EIC 2025.
- **Quién**: Claude (provisional).
- **Por qué**: es la última publicada y la que se verificó en campo para la EIC (sep–nov 2025). Diferencia en Acámbaro: 3 520 vs 3 522 manzanas.

### D02 · 2026-10-22 · Cartografía 2010
- **Decisión**: usar la *cartografía geoestadística urbana y rural de cierre del Censo 2010* del municipio (productos 702825585853 y 702825561291), no el MG 2010 v5.0 nacional.
- **Opciones**: MG 2010 v4.3 / v5.0 / v5.0.A nacionales · cartografía de cierre del Censo 2010 por municipio.
- **Quién**: Claude (provisional).
- **Por qué**: es la cartografía con la que se publicaron los resultados por manzana 2010, así que las claves coinciden con la tabla censal 2010; incluye manzanas de 3 localidades urbanas y 78 rurales.
- **Consecuencia**: los shapefiles rurales no traen proyección; se les asignó la de los urbanos (Lambert ITRF92). Verificado en V07.

### D03 · 2026-10-22 · Qué cuenta como "manzana nueva"
- **Decisión**: una manzana de la edición posterior es **nueva** si menos del 50 % de su superficie ya era manzana en la edición anterior (criterio de geometría). Se reporta también el criterio por clave (CVEGEO que no existía) y se marca si la localidad ya estaba cartografiada antes.
- **Opciones**: solo clave · solo geometría · ambas.
- **Quién**: Claude (provisional; **el umbral de 50 % es de criterio**, ver pregunta 4 del resumen). **Confirmado por Alejandro el 2026-10-22 (D12).**
- **Por qué**: INEGI renumera manzanas que ya existían (subdivisiones, cambios de AGEB): 30 de las 38 claves nuevas 2020→2025 están sobre suelo que ya era manzana. Contar solo claves exageraría el crecimiento.

### D04 · 2026-10-22 · Caserío disperso urbano (clave de manzana 800)
- **Decisión**: incluir las 32 claves "800" de la tabla censal 2020 (464 personas) usando su geometría de puntos de la capa `caserio_disperso` del MG 2020.
- **Opciones**: descartarlas · incluirlas como puntos.
- **Quién**: Claude (provisional).
- **Por qué**: son viviendas reales fuera de manzana; descartarlas perdería 464 personas.

### D05 · 2026-10-22 · Datos ocultos por confidencialidad ("*")
- **Decisión**: el "*" se trata como dato ausente; **no se imputa**. En cada paso se reporta cuánta población queda oculta (total de la AGEB menos la suma visible de sus manzanas).
- **Opciones**: dejar vacío · repartir el faltante de cada AGEB entre sus manzanas con "*" · trabajar los grupos de edad a nivel AGEB.
- **Quién**: Claude (provisional). Alejandro decidió cómo tratarlo en los resultados por grupo: ver **D10**.
- **Por qué**: la regla del proyecto es no inventar datos.

### D06 · 2026-10-22 · Servicios fuera del municipio
- **Decisión**: conservar servicios del DENUE hasta 10 km fuera del límite municipal, incluidos los de Michoacán (y se revisó Querétaro).
- **Opciones**: solo dentro del municipio · franja de 5, 10 o más km.
- **Quién**: Claude (provisional). **Confirmado por Alejandro el 2026-10-22 (D11).**
- **Por qué**: 75 de los 274 km del contorno municipal son límite estatal; para localidades de borde, la escuela o tienda más cercana puede estar en otro municipio o estado.

### D07 · 2026-10-22 · GHSL
- **Decisión**: mosaico R7_C9 (100 m, Mollweide) de GHS-BUILT-S R2023A, años 1975–2020. No se bajan 2025 ni 2030.
- **Quién**: definido por Alejandro (solo serie observada); el mosaico y la resolución, Claude.
- **Por qué**: 2025 y 2030 son proyecciones del modelo, no observación.

### D08 · 2026-10-22 · Fuentes no descargables
- **Decisión**: CLUES, SEP y CONAPO las baja Alejandro y las sube al release `datos-crudos`.
- **Quién**: Alejandro.
- **Por qué**: no hay acceso desde el entorno de trabajo (ver `docs/fuentes.md`).

---

## Fase 2 — Catálogo de servicios

### D09 · 2026-10-22 · Qué es "la ciudad" y cómo se nombra
- **Decisión**: "la ciudad" es la cabecera, Acámbaro (localidad 0001). Irámuco (0027), Parácuaro (0047) y Chupícuaro / Nuevo Chupícuaro (0017) son localidades distintas, no parte de la ciudad. Dentro de cada una de las 4 localidades urbanas el análisis se hace por cuadra (manzana del INEGI) y cada localidad se reporta por separado. En los textos para el público se dice "cuadra" o "localidad", nunca "manzana".
- **Opciones**: solo la cabecera · cabecera más localidades conurbadas como una sola ciudad · 4 localidades urbanas por separado.
- **Quién**: Alejandro.
- **Por qué**: son poblaciones separadas físicamente y con identidad propia; juntarlas mezclaría realidades distintas.

### D10 · 2026-10-22 · Grupos de población ocultos por "*" (resuelve lo pendiente de D05)
- **Decisión**: opción **(c)**, los grupos de edad y de discapacidad se trabajan **por AGEB**, con la opción **(a)** como apoyo.
  - **(c)** Para cada AGEB se usa el total publicado de cada grupo (3–5, 6–11, 12–14, 15–17, 60+, con discapacidad), que no tiene ocultos. La parte de ese grupo que vive lejos de un servicio se calcula con la proporción de la población total de la AGEB que vive en cuadras lejanas.
  - **(a)** Como apoyo y control: la suma de lo que sí es visible por cuadra (sin rellenar los "*"). Es un **mínimo seguro**: la cifra real nunca es menor.
- **Supuesto explícito de (c)**: *dentro de cada AGEB, cada grupo de edad (y la población con discapacidad) está repartido entre las cuadras en la misma proporción que la población total.* Si, por ejemplo, el 30 % de la población de una AGEB vive en cuadras a más de 1 km de una primaria, se supone que también el 30 % de sus niñas y niños de 6 a 11 años. Ese supuesto falla si dentro de la AGEB los niños se concentran en un fraccionamiento nuevo de la orilla (subestimaría) o en el centro (sobreestimaría). Cada cifra por grupo se reportará con su mínimo visible (a) al lado, para que se vea el margen.
- **Opciones**: (a) dejar vacío · (b) repartir el faltante de cada AGEB entre sus cuadras con "*" · (c) grupos por AGEB.
- **Quién**: Alejandro.
- **Por qué**: (c) no inventa datos por cuadra y usa totales publicados completos; (a) muestra cuánto depende el resultado del supuesto. Fuera de las 4 localidades urbanas no aplica: allí se usa el ITER por localidad.

### D11 · 2026-10-22 · Servicios fuera del municipio (confirma D06)
- **Decisión**: se incluyen servicios hasta 10 km fuera del límite municipal, incluidos los de Michoacán. Las recomendaciones distinguirán lo que es competencia del municipio de lo que no.
- **Quién**: Alejandro.
- **Consecuencia técnica**: además del DENUE, se bajó el MG EIC 2025 de **Michoacán** para tener las escuelas y centros de salud dibujados por INEGI también del otro lado del límite (ver D14). Cada servicio del catálogo lleva su entidad, municipio y una columna de competencia (D18).

### D12 · 2026-10-22 · Umbral de "manzana nueva" (confirma D03)
- **Decisión**: una cuadra es nueva si menos del 50 % de su superficie ya era manzana en la edición anterior del MG.
- **Quién**: Alejandro (aceptó la propuesta de D03).

### D13 · 2026-10-22 · Validación sin trabajo de campo
- **Decisión**: la validación se hace con imágenes satelitales históricas (Google Earth) y Street View. Claude prepara dos listas en `docs/`: `verificar_zonas_nuevas.csv` (cada zona de crecimiento) y `verificar_servicios_muestra.csv` (muestra de servicios), con coordenadas, enlace a Google Maps en vista satelital y columnas vacías `existe_en_imagen` y `notas`.
- **Quién**: Alejandro (método); Claude (formato y muestra, D19).
- **Por qué**: Alejandro no tiene conocimiento local detallado ni hará visitas.

### D14 · 2026-10-22 · Fuentes del catálogo mientras faltan CLUES y SEP
- **Decisión**: el catálogo se arma con dos fuentes oficiales que se cruzan entre sí:
  1. **Marco Geoestadístico EIC 2025, capas de servicios** (puntos y áreas): escuelas por nivel, centros de salud, hospitales y mercados, verificados en campo por INEGI en sep–nov 2025. No traen sector (público/privado) y casi nunca nombre.
  2. **DENUE 05/2026**: nombre, actividad y sector, pero **registra muy pocas escuelas públicas y centros de salud rurales** (V13).
  La ubicación de una sede que aparece en ambas fuentes es la del MG.
- **Opciones**: solo DENUE · solo MG · ambas · esperar CLUES y SEP.
- **Quién**: Claude (provisional, técnica). Cuando lleguen CLUES y SEP se contrastan con este catálogo y se decide si las reemplazan.
- **Por qué**: solo con el DENUE, Acámbaro tendría 29 preescolares en vez de 92; los resultados de distancia saldrían muy exagerados en lo rural.

### D15 · 2026-10-22 · Qué cuenta en cada tipo de servicio
- **Decisión** (provisional; las preguntas de criterio van en el resumen de la fase 2):
  - **Preescolar, primaria, secundaria, bachillerato**: escuelas del MG por nivel + DENUE (SCIAN 6111xx por nivel, públicas y privadas). Secundaria incluye general y técnica; bachillerato incluye media superior y media técnica terminal.
  - **Salud de primer nivel**: "Centro de Salud" del MG + DENUE públicos 621112 (consultorio de medicina general) y 621116 (clínica de consultorios), más los que se reclasifican por nombre (D17).
  - **Abasto**: mercados públicos (MG + locales del DENUE agrupados por mercado), supermercados (462111), minisúper (462112) y abarrotes (461110).
  - **Se guardan pero no se miden** (columna `analizado` = falso): escuelas que combinan varios niveles (no se sabe cuáles: colegios privados, Centro de Atención Múltiple, INAEBA), consultorios privados (621111, 621115) y hospitales.
- **Quién**: Claude (provisional). **Pendiente de Alejandro**: consultorios privados, escuelas privadas, qué tiendas cuentan como abasto y la preparatoria abierta (preguntas del resumen).

### D16 · 2026-10-22 · Un punto por sitio ("sede")
- **Decisión**: los registros del mismo tipo a menos de **60 m** se juntan en una sede (una escuela con dos turnos viene dos veces en el DENUE). Un registro que solo está en el DENUE se une a la sede del MG del mismo tipo más cercana si está a **150 m** o menos (las dos fuentes ubican el mismo edificio con una diferencia mediana de 20–25 m, y en algunos casos de más de 60 m: V14). Las tiendas no se juntan entre sí (dos abarrotes vecinos son dos comercios). Un área del MG con un punto del mismo tipo a 50 m o menos sería duplicado (resultó no haber ninguno: las 82 áreas son sitios distintos).
- **Quién**: Claude (provisional, técnica).
- **Por qué**: para medir la distancia al servicio más cercano basta un punto por sitio; los umbrales mueven la ubicación menos de una cuadra.

### D17 · 2026-10-22 · Reclasificación por nombre de unidades de primer nivel
- **Decisión**: los registros del DENUE de salud (621, 622) cuyo nombre contiene UMAPS, "Unidad Médica/de Medicina Familiar", "Unidad Médica Rural" o "Centro de Salud" se cuentan como salud de primer nivel aunque su código diga hospital u "otros consultorios". Son 4: UMAPS Loma Dorada y la UMF del ISSSTE en Acámbaro (codificadas como hospital general), un "Centro de Salud" de Acámbaro (otros consultorios) y la Unidad Médica Rural IMSS-Bienestar de Mariano Escobedo, Cuitzeo.
- **Quién**: Claude (provisional, técnica). CLUES lo confirmará.
- **Por qué**: el MG los dibuja como centro de salud y el nombre lo dice; contarlos como hospital los sacaría del análisis.

### D18 · 2026-10-22 · Columna de competencia (propuesta)
- **Decisión**: cada sede lleva quién tiene la competencia, para separar después las recomendaciones: **mercados → municipal** (art. 115 constitucional, fracción III); escuelas → estatal/federal (educación); salud → estatal/federal (salud); tiendas → privado.
- **Quién**: Claude (propuesta). Alejandro puede afinarla (p. ej. si el municipio participa en construcción de aulas o en casas de salud).

### D19 · 2026-10-22 · Cómo se arman las listas de verificación
- **Zonas nuevas**: las cuadras nuevas (D12) de la misma localidad y periodo, pegadas o a menos de 30 m, forman una zona; así un fraccionamiento se revisa una vez y no cuadra por cuadra. Se incluyen también las de localidades que no tenían cartografía en 2010, marcadas, porque la imagen de 2010 es justamente lo que dice si ya había casas.
- **Muestra de servicios**: aleatoria (semilla fija 20261022) por estratos de tipo × fuente (solo MG, solo DENUE, ambas) × dentro/fuera del municipio: 5 sedes por estrato dentro del municipio y 2 en la franja; **todas** las sedes de salud de primer nivel y bachillerato del municipio y todos los mercados. Abasto se estratifica por tipo de comercio. Además del enlace satelital se añade uno a Street View.
- **Quién**: Claude (provisional).

---

## Fase 3 — Accesibilidad

### D20 · 2026-10-23 · Salud: qué cuenta en la medida principal
- **Decisión**: el resultado principal usa **unidades públicas de primer nivel** (centros de salud y UMAPS de la Secretaría de Salud, IMSS, ISSSTE, IMSS-Bienestar). Los **consultorios privados** se miden y se reportan **como dato aparte**.
- **Quién**: Alejandro (responde la pregunta de la fase 2).
- **Cómo se aplicó** (Claude): una sede cuenta si su tipo es salud de primer nivel, su sector es público (según CLUES o DENUE) y la CLUES no la da de baja. Se incluye el Hospital General de Subzona con Medicina Familiar 13 del IMSS porque da consulta familiar. Nota: IMSS e ISSSTE atienden solo a sus derechohabientes; el reporte lo dirá.

### D21 · 2026-10-23 · Escuelas: todas y solo públicas
- **Decisión**: cada nivel se mide dos veces: con **todas** las escuelas y con **solo públicas** (sostenimiento según el catálogo SEP; si la SEP no la tiene, según el DENUE).
- **Quién**: Alejandro.
- **Consecuencia**: las escuelas que solo dibuja el MG y que la SEP no confirma (sector desconocido) entran en "todas" pero no en "públicas".

### D22 · 2026-10-23 · Abasto: dos medidas
- **Decisión**: **tienda básica** = abarrotes, minisúper, supermercado o mercado; **abasto completo** = mercado o supermercado.
- **Quién**: Alejandro.

### D23 · 2026-10-23 · Preparatoria abierta
- **Decisión**: no cuenta para la distancia a bachillerato (no es escolarizada). Se registra como categoría aparte, **"bachillerato no escolarizado"**, aparece en el mapa de bachillerato y en los conteos por localidad. Matrícula: incluirla si alguna fuente la trae.
- **Quién**: Alejandro.
- **Resultado**: hay 1 en el municipio (DENUE, "Preparatoria abierta", ciudad de Acámbaro); la SEP no la registra como escuela del municipio. **Ninguna fuente trae matrícula ni número de alumnos** (el catálogo de centros de trabajo de la SEP no tiene esa columna): queda como limitación y pregunta pendiente (V20).
- Por la misma regla, Claude separó también un "Videobachillerato CERESO Acámbaro" (dentro del penal: no está abierto a la población) como "escuela en centro penitenciario" (provisional).

### D24 · 2026-10-23 · Sustitución de CONAPO
- **Decisión**: CONAPO no está disponible (sus enlaces dan error): se registra como limitación. En su lugar:
  - **Nombres de colonia**: Catálogo de asentamientos humanos del INEGI (servicio web del Catálogo Único de Claves Geoestadísticas). **No trae polígonos** (ni la fecha 2025: su periodo es 11/2021, el del Censo 2020), así que los nombres se asignan por cercanía con el método de abajo.
  - **Contexto social**: indicadores del Censo 2020 por AGEB y por localidad, sin índice propio.
- **Quién**: Alejandro (sustitución); Claude (método de asignación, provisional).
- **Método de nombres** (`src/12_colonias_contexto.py`): los registros del DENUE, la SEP y la CLUES traen el nombre del asentamiento y coordenadas. Cada cuadra toma el nombre más frecuente entre los registros que caen dentro de ella; si no hay, entre los 5 más cercanos a ≤ 300 m. Solo se aceptan nombres que existen en el catálogo del INEGI para esa localidad. Es aproximado: el límite entre colonias queda donde cambian los registros, no donde lo dibuja un plano.
- **Indicadores**: escolaridad promedio, % de 15+ analfabeta, % sin afiliación a servicios de salud, % de viviendas sin agua entubada dentro, sin drenaje, sin electricidad y **sin automóvil** (este último lo agregó Claude: dice quién depende de caminar o del transporte público).

### D25 · 2026-10-23 · Umbrales de "lejos" (cerrada: los definitivos están en D33)
- **Decisión**: se calculan tres umbrales por categoría; **Alejandro elige el definitivo después de ver los resultados.**
- **Ciudad, a pie por calles (m)** — estricto / **propuesto** / holgado:

  | Categoría | Estricto | Propuesto | Holgado | Fuente o razón |
  |---|---:|---:|---:|---|
  | Preescolar | 500 | **750** | 1 000 | SNEU (SEDESOL), tomo Educación: radio de servicio urbano recomendable del jardín de niños, 750 m |
  | Primaria | 400 | **500** | 1 000 | SNEU: primaria, 500 m; holgado = 15 min a paso infantil |
  | Secundaria | 750 | **1 000** | 1 500 | SNEU: secundaria general, 1 000 m |
  | Bachillerato | 1 500 | **2 500** | 5 000 | SNEU: bachillerato/preparatoria, 2–5 km (se propone el medio) |
  | Salud pública de primer nivel | 750 | **1 000** | 1 500 | SNEU, tomo Salud: centro de salud urbano, 1 km |
  | Tienda básica | 300 | **500** | 800 | Proximidad cotidiana: ~5–7 min a pie (no hay norma SNEU para abarrotes) |
  | Abasto completo (mercado o súper) | 750 | **1 200** | 2 000 | SNEU, tomo Comercio y Abasto: mercado público, 750 m; propuesto = 15 min a pie (ciudad de 15 minutos, Moreno et al. 2021) |

- **Localidades rurales, por camino (m)**: preescolar y primaria 1 000 / **2 000** / 3 000 (2 km ≈ 30 min a pie de un niño); secundaria 3 000 / **5 000** / 10 000; bachillerato 5 000 / **10 000** / 15 000; salud 3 000 / **5 000** / 10 000; abasto completo 5 000 / **10 000** / 15 000. Para lo rural no hay una norma comparable: son propuesta de Claude basada en tiempos de traslado a pie o en transporte, y deben leerse como sensibilidad.
- **Quién**: Claude propone; Alejandro decide.
- **Ojo**: los valores del SNEU se citan de las tablas de "radio de servicio urbano recomendable" del Sistema Normativo de Equipamiento Urbano (SEDESOL, 1999). El documento no se volvió a abrir en esta sesión (no está en el repositorio); conviene cotejarlos antes de publicarlos.

### D26 · 2026-10-23 · Red de caminos para lo rural
- **Decisión** (Alejandro): cascada RNC del INEGI → OpenStreetMap (primero Overpass, luego Geofabrik) → línea recta × factor de rodeo calibrado con la red de la ciudad, declarado como limitación. Sin detenerse.
- **Qué pasó**: la RNC no tiene URL directa localizable (2 intentos a páginas del INEGI, dinámicas); Overpass y Geofabrik cortaron la conexión en el proxy del entorno (ver V22). Se usó **línea recta × 1.33** (mediana de red/recta en la ciudad).
- **Limitación**: la línea recta no ve ríos, cerros, presas ni el lago de Cuitzeo; el factor de la ciudad (cuadrícula) probablemente **subestima** los rodeos de los caminos rurales. Las distancias rurales son aproximadas y es probable que sean algo mayores en realidad.

### D27 · 2026-10-23 · Casas de salud
- **Decisión**: se reportan como dato aparte y **no cuentan** como unidad de salud de primer nivel en la medida principal (suelen no tener médico permanente).
- **Quién**: Alejandro.
- **Resultado**: la CLUES de agosto de 2026 no registra ninguna "casa de salud" en el municipio ni en la franja de 10 km. Por la misma razón, Claude dejó también aparte la **unidad móvil** (ESI 29 Cútaro, sin sede fija) (provisional).
- **Cerrada** (fase 4): ya no es un pendiente.

### D28 · 2026-10-23 · Sensibilidad: solo sedes confirmadas
- **Decisión**: además de los tres umbrales, el resultado con el umbral propuesto se recalcula usando **solo sedes confirmadas** por SEP, CLUES o DENUE (se quitan las que solo dibuja el MG sin confirmación). Tabla comparativa en `data/processed/acceso_sensibilidad_confirmadas.csv` (desde la fase 4: `acceso_sensibilidad.csv`, que agrega la sensibilidad sin dudosos remotos, D41).
- **Quién**: Alejandro.

### D29 · 2026-10-23 · Cómo se cruzan SEP y CLUES con el catálogo de la fase 2
- **Decisión**: registros de SEP/CLUES del mismo tipo a ≤ 60 m forman un grupo (varios turnos o claves en el mismo edificio). Un grupo **confirma** a la sede de la fase 2 del mismo tipo si está a ≤ 150 m, o si son vecinos más cercanos mutuos a ≤ 300 m (la SEP ubica a veces la escuela a media cuadra: mediana 62 m, percentil 90 215 m). Un grupo sin sede es **sede nueva**. Una sede de la fase 2 sin confirmación se conserva marcada como "no confirmada" (el MG 2025 se verificó en campo); si en cambio tiene a ≤ 150 m un registro **dado de baja** del mismo tipo, se marca "baja" y **no se usa** (el registro oficial es más reciente). La ubicación de una sede confirmada sigue siendo la del MG o el DENUE.
- **Quién**: Claude (provisional, técnica).
- **Escuela "que opera"**: estatus ACTIVO en la SEP y al menos un turno sin la marca "(INACTIVO)". **Unidad que opera**: "EN OPERACION" en la CLUES.

### D30 · 2026-10-23 · Unidades de salud del MG sin registro en la CLUES
- **Decisión** (provisional): las 6 sedes de salud del municipio que solo dibuja el MG y que la CLUES no registra (sector desconocido: Solís, La Ortiga, La Encarnación, San Luis de los Agustinos, La Presa de Santa Inés y "Centro Médico la Soledad" en la ciudad) **no entran** en "salud pública", porque no hay evidencia de que sean unidades públicas con médico. Pueden ser casas de salud (D27) o consultorios. Quedan en el catálogo para revisión.
- **Quién**: Claude (provisional). **Cerrada en D34** (Alejandro: fuera de la medida principal, en un anexo).

### D31 · 2026-10-23 · Detalles técnicos de la medición a pie
- **Red**: ejes viales del MG EIC 2025 (todos los tipos, incluidos andadores y peatonales), sin sentido de circulación. Extremos sueltos a < 15 m de otro tramo se unen (455 uniones, V21).
- **Origen**: un punto interior de cada cuadra (no el centroide, que puede caer fuera en cuadras con forma de "L") y los puntos de caserío disperso. Cada origen y cada servicio se conectan en línea recta al tramo más cercano de la red de su localidad; esa recta se suma a la distancia.
- **Servicios lejos de la red de la localidad** (a más de 300 m, p. ej. en otra localidad o en un campus aislado): se miden en línea recta × 1.33 y se toma el menor de los dos caminos; cada distancia dice cuál se usó (`via_<categoría>`).
- **Velocidad para convertir a minutos**: 4 km/h (paso de niños y adultos mayores; un adulto camina ~4.8 km/h).
- **Quién**: Claude (provisional, técnica).

### D32 · 2026-10-23 · Tiendas y consultorios privados en lo rural: no medibles
- **Decisión**: en las localidades rurales **no se mide** la distancia a tienda básica ni a consultorio privado.
- **Por qué**: el DENUE solo registra comercios y consultorios de las localidades urbanas: de los 5 974 establecimientos del municipio, 5 932 están en las 4 urbanas y **ninguna tienda de abarrotes, minisúper o supermercado** está fuera de ellas (V24). Medir contra las tiendas de la ciudad haría parecer que 96 % de la población rural vive lejos de una tienda, lo cual es un efecto de la fuente, no un hecho.
- **Quién**: Claude (provisional). **Confirmada por Alejandro en D35** para la tienda básica; el abasto completo rural sí se mide.

## Fase 4 — Decisiones finales (2026-10-23)

### D33 · 2026-10-23 · Umbrales definitivos (cierra D25)
- **Decisión**: el "radio de servicio urbano recomendable" del Sistema Normativo de Equipamiento Urbano (SNEU, SEDESOL) se interpreta como un radio **en línea recta**. Nuestra medida es por calle, así que el umbral principal por calle = radio SNEU × **1.33** (factor de rodeo calibrado en la fase 3, V23). Estricto = radio SNEU sin convertir; holgado = principal × 1.5. La tienda básica (500 m) y el abasto completo (1 000 m = 15 min a pie a 4 km/h) no vienen del SNEU: se les aplica la misma proporción.

  | Ciudad, a pie por calles (m) | Estricto | **Principal** | Holgado |
  |---|---:|---:|---:|
  | Preescolar (SNEU 750 m) | 750 | **1 000** | 1 500 |
  | Primaria (SNEU 500 m) | 500 | **670** | 1 000 |
  | Secundaria (SNEU 1 000 m) | 1 000 | **1 330** | 2 000 |
  | Bachillerato (SNEU 2 500 m) | 2 500 | **3 330** | 5 000 |
  | Salud pública de primer nivel (SNEU 1 000 m) | 1 000 | **1 330** | 2 000 |
  | Tienda básica | 380 | **500** | 750 |
  | Abasto completo (mercado o supermercado) | 750 | **1 000** | 1 500 |

- **Rural**: sin cambios respecto a D25 (preescolar y primaria 2 km, secundaria 5 km, bachillerato 10 km, salud 5 km, abasto completo 10 km; estricto y holgado igual que en la fase 3).
- **Factor fijo**: el factor queda fijo en 1.33 (`FACTOR_FIJO` en `11_accesibilidad.py`). Recalibrado con el catálogo de la fase 4 sale 1.349, porque al reubicar el CECyTE (D37) los recorridos al bachillerato público cruzan la ciudad (V33). Cambiarlo movería los umbrales que se derivan de él.
- **Verificación del SNEU**: Alejandro pidió verificar en el texto que el radio es en línea recta. No se pudo abrir el texto original (V31). Alejandro decidió de antemano que, si el texto no lo dice explícitamente, se aplica × 1.33 y se avisa. **Si el SNEU definiera el radio como distancia recorrida, el umbral correcto sería el estricto.**
- **Cómo se reporta**: el principal es la cifra del reporte. Si un hallazgo solo aparece con uno de los tres umbrales, se dice.
- **Quién**: Alejandro (2026-10-23), con el ajuste de estricto y holgado.

### D34 · 2026-10-23 · Unidades de salud sin CLUES: anexo (cierra D30)
- **Decisión**: los 6 puntos de salud que solo dibuja el INEGI y que no están en la CLUES (Solís, La Ortiga, La Encarnación, San Luis de los Agustinos, La Presa de Santa Inés y "Centro Médico la Soledad" en la ciudad) quedan **fuera de la medida principal**. En un anexo se muestra qué pasaría si contaran (categoría `salud_publica_con_anexo`).
- **Quién**: Alejandro.

### D35 · 2026-10-23 · Tiendas y mercados en lo rural
- **Decisión**: la **tienda básica** en lo rural es "no medible": el DENUE no registra los negocios de las localidades rurales pequeñas (D32). El **abasto completo** (mercado o supermercado) rural **sí se mide**, porque esos están en localidades que el DENUE cubre. Se anota que **ninguna fuente registra tianguis**.
- **Redacción para Irámuco**: "no hay mercado ni supermercado registrado; puede existir un tianguis que ninguna fuente captura".
- **Quién**: Alejandro (corrigió la propuesta inicial de declarar también el abasto rural como no medible).

### D36 · 2026-10-23 · Clínica del ISSSTE
- **Decisión**: la UMF del ISSSTE en la ciudad (`salud_primer_nivel-0011`) está **en operación** y cuenta en salud pública. Alejandro la verificó localmente, y Google Maps no la marca como cerrada. Se declara la discrepancia: la CLUES de agosto de 2026 la registra "fuera de operación", sin motivo.
- **Quién**: Alejandro.

### D37 · 2026-10-23 · Ubicación del CECyTE Acámbaro
- **Decisión**: Google Maps lo ubica como "CECYTEG Plantel Acámbaro", en Av. San Pablo 8, col. Valle de Acámbaro. El DENUE trae el mismo número (8) y la misma colonia (Valle de Acámbaro) en el punto del sur de la ciudad, que es también el del MG (`bachillerato-0022`, a 680 m de las cuadras de esa colonia). Se **conserva** ese punto, que queda confirmado con la clave SEP 11ETC0037Z. Se **descarta** el punto de la SEP (calle Loma Bonita, col. Loma Bonita, 4.3 km al norte; `bachillerato-S0004`).
- El MG no trae ninguna calle llamada "San Pablo", así que no se pudo cotejar la calle.
- **Quién**: Alejandro (ubicación); Claude (cuál punto coincide).

### D38 · 2026-10-23 · Consultorio del CERESO
- **Decisión**: el "CONSULTORIO MEDICO CIVIL" del DENUE (`salud_primer_nivel-0093`) está dentro del CERESO y no es un servicio abierto a la población. Sale de salud pública (tipo `salud_centro_penitenciario`). Es el mismo criterio que se usó con las escuelas del penal en la fase 3.
- **Quién**: Alejandro.

### D39 · 2026-10-23 · Parácuaro: secundaria
- **Decisión**: la secundaria que atiende a Parácuaro es la **Escuela Secundaria Técnica Núm. 24** (clave 11DST0024Y), en la carretera Acámbaro–Parácuaro km 9, fuera del pueblo. Redacción: "no hay secundaria dentro de la localidad".
- **Comprobación** (V34): es la misma que calculó la fase 3. Está a 4.2 km en línea recta del centro de Parácuaro (5.5 km estimados por camino, mediana). Para la mitad norte del pueblo, la Telesecundaria 847 de La Concepción queda a una distancia casi igual.
- **Quién**: Alejandro.

### D40 · 2026-10-23 · Fecha del catálogo SEP
- **Decisión**: el catálogo de centros de trabajo de la SEP (`cct11.csv`, `cct16.csv`) se cita con **fecha de consulta 2026-10-22**. El archivo no trae columna de fecha de corte ni de ciclo escolar. La única fecha es `F_FUNDACION`, llena solo en 19–33 % de los registros, y la más reciente es de diciembre de 2017, así que no sirve como fecha de corte (V35).
- **Quién**: Alejandro.

### D41 · 2026-10-23 · Verificación remota de servicios: "dudoso_remoto"
- **Decisión**: la verificación de Alejandro en Google Maps (satélite y Street View, 68 servicios revisados) es **preliminar**. Un "no" **no borra** el servicio: se marca `dudoso_remoto` y se calcula una sensibilidad sin esos servicios. Los "no" y los "no se ve" del municipio pasan a la lista de campo (`docs/verificar_campo.csv`).
- **No es muestra al azar**: se revisaron todos los bachilleratos y casos priorizados. Las tasas se reportan por tipo y por fuente, y la total con esa advertencia. No describen la confiabilidad general del catálogo.
- **Excepción**: el consultorio del CERESO (D38).
- **Casas de salud (D27)**: decididas; ya no son un pendiente.
- **Quién**: Alejandro.


---

## Fase 4b — Crecimiento urbano y acceso

### D42 · 2026-10-23 · Antigüedad de las cuadras
- **Decisión**: en las 4 localidades urbanas, cada cuadra 2020 es **consolidada** si al menos la mitad de su superficie ya era manzana en el MG 2010, y **nueva 2010–2020** si no (D12, `manzanas_cambios.gpkg`, capa `mg2020_vs_2010`). Las cuadras del MG EIC 2025 con menos de la mitad de su superficie en manzanas 2020 son **nuevas posteriores a 2020** (sin población). El caserío disperso queda aparte. Las cuadras posteriores a 2020 se unen por la pareja (clave, periodo), nunca solo por clave.
- **Quién**: Alejandro (criterio, D12); Claude (aplicación).
- **Por qué**: es el criterio ya aprobado. Las 4 localidades estaban cartografiadas en 2010, así que ninguna cuadra es "nueva" solo porque su localidad no tenía cartografía (V39).

### D43 · 2026-10-23 · Centro de cada localidad y anillos (propuesta)
- **Decisión**: el centro es la coordenada de la localidad en el ITER 2020 (el INEGI la ubica en la plaza o el centro). La distancia al centro es en línea recta desde un punto interior de cada cuadra. Para separar "periferia" de "zona nueva", cada cuadra nueva se compara con las consolidadas de su mismo anillo de 500 m: % esperado = tasa de las consolidadas del anillo, ponderada por la población (o por las cuadras) de las nuevas.
- **Opciones**: punto del ITER · presidencia o plaza digitalizada a mano · centroide de la localidad · anillos de 250, 500 o 1 000 m.
- **Quién**: Claude (provisional; **pendiente de Alejandro**).
- **Por qué**: es un punto oficial y reproducible. 500 m es el ancho que deja cuadras consolidadas en todos los anillos donde hay cuadras nuevas (V40).

### D44 · 2026-10-23 · Viviendas no habitadas y el "*"
- **Decisión**: (a) **2020 por cuadra**: % no habitadas = (viviendas − habitadas) / viviendas, sumando solo cuadras con dato visible. Se usa porque "habitadas" solo está oculta en 51 cuadras, contra 602 de "deshabitadas". (b) **2010 → 2020**: "deshabitadas" y "uso temporal" de 2010 están ocultas en 1 339 de 1 478 manzanas. Por eso la década se compara con totales publicados por localidad y por AGEB. Las AGEB 2010 y 2020 se agrupan en **unidades comparables**: cada manzana 2010 se asigna, por su centroide, a la AGEB 2020 que la contiene, y se unen las AGEB que comparten ≥ 5 % de viviendas. Población y viviendas totales (sin ocultos) se comparan además por cuadra y anillo. (c) Lo oculto se reporta en cifras (total publicado − suma visible).
- **Opciones**: deshabitadas visibles por cuadra · viviendas − habitadas · repartir el oculto (descartado: regla 3).
- **Quién**: Claude (método); Alejandro pidió la comparación 2010–2020 por anillo y por AGEB.
- **Por qué**: no se imputa nada y se usa la medida con menos ocultos. En la ciudad, viviendas − habitadas da 25.9 % contra 26.1 % de deshabitadas + uso temporal publicadas (V42).

### D45 · 2026-10-23 · GHSL: zonas, sectores y población
- **Decisión**: superficie construida (GHS-BUILT-S, 1975–2020) por celdas cuyo centro está en el municipio, o a ≤ 1 km del polígono de cada localidad urbana (MG EIC 2025; si una celda queda cerca de dos, va a la más cercana). Direcciones: 8 sectores y anillos de 1 km desde el centro de la ciudad (D43). La superficie por habitante solo se calcula con población del mismo año (2010 y 2020). La EIC 2025 se muestra sin superficie. Los ITER 1990–2005 no se pudieron bajar (V43).
- **Quién**: Claude (provisional).
- **Por qué**: D07 (solo serie observada) y regla 3 (no se interpola población entre censos).

### D46 · 2026-10-23 · Tipología de AGEB (propuesta, **pendiente de Alejandro**)
- **Propuesta**: nueva = ≥ 30 % de la superficie de sus cuadras es nueva (2010–2020 o posterior). Desatendida = en ≥ 3 de 5 servicios básicos (preescolar, primaria, secundaria, salud pública, abasto completo), más de la mitad de su población (o de su superficie, si no tiene población) está lejos con el umbral principal. Vaciándose = % no habitadas ≥ percentil 75 de las AGEB consolidadas de su localidad con ≥ 30 viviendas, **y** población 2020 menor que la de 2010 en su unidad comparable. Clases: nueva y desatendida · nueva y bien servida · consolidada y vaciándose (prioridad sobre desatendida; se marca si también lo es) · consolidada desatendida · consolidada estable.
- **Sensibilidad** (`tipologia_sensibilidad.csv`): nueva 25/40 % (0–2 AGEB cambian); servicios 2 o 4 (30 y 26 cambian); percentil 66/90 (1–2); percentil de las 4 localidades juntas (5).
- **Quién**: Claude propone; Alejandro decide después de ver los resultados.

---

## Fase 4c — Decisiones de la 4b y crecimiento no registrado

### D47 · 2026-10-23 · Tipología de AGEB: criterios finales (cierra D46)
- **Decisión**: "desatendida" = en ≥ 3 de 5 servicios básicos (preescolar, primaria, secundaria, salud pública, abasto completo) más de la mitad de la población (o de la superficie, si no tiene población) está lejos con el umbral principal. Con 2 de 5 se reporta como sensibilidad. "Vaciándose" se compara con las AGEB de su propia localidad (percentil 75 de % no habitadas entre las consolidadas con ≥ 30 viviendas), y sigue pidiendo pérdida de población 2010–2020 en su unidad comparable. Nueva = ≥ 30 % de su superficie es cuadra nueva, como se propuso.
- **Quién**: Alejandro.
- **Por qué**: 3 de 5 separa la orilla más alejada sin marcar como desatendida casi toda la periferia (con 2 de 5 cambian 30 AGEB). Cada localidad tiene su propio nivel de viviendas no habitadas.

### D48 · 2026-10-23 · Centro de cada localidad (cierra D43)
- **Decisión**: el centro es el punto de la localidad en el ITER 2020. Se mantienen los anillos de 500 m.
- **Quién**: Alejandro.

### D49 · 2026-10-23 · Cómo se presentan las cuadras nuevas
- **Decisión**: en los textos públicos, las cuadras nuevas se presentan con conteos (personas, cuadras, hectáreas), no con porcentajes, porque son un grupo pequeño (356 personas en 2010–2020). El hallazgo del preescolar se mantiene porque aparece con los tres umbrales. En los documentos de trabajo se conservan los porcentajes.
- **Quién**: Alejandro.

### D50 · 2026-10-23 · Población 1990–2005
- **Decisión**: los ITER 1990–2005 no se buscan por ahora. La superficie construida por habitante se queda en 2010 y 2020, y se declara como limitación.
- **Quién**: Alejandro.

### D51 · 2026-10-23 · Título de trabajo
- **Decisión**: "¿Quién está lejos hoy? Acceso a servicios y vaciamiento urbano en Acámbaro". Puede cambiar al redactar.
- **Quién**: Alejandro.

### D52 · 2026-10-23 · Construcción del GHSL fuera de las cuadras del INEGI (provisional)
- **Decisión**: (a) **Contabilidad sin umbral**: se usan las celdas GHS-BUILT-S de 100 m a ≤ 1 km de las 4 localidades urbanas, con la misma asignación que D45. Para cada celda, los m² ganados entre 2010 y 2020 se reparten según qué fracción de la celda está cubierta por cuadras del MG más reciente (MG EIC 2025, todas las del municipio): esa parte cuenta "dentro de cuadras" y el resto "fuera". (b) Una **celda "sin cuadras"** ganó ≥ 500 m² (5 % de la celda) y tiene < 25 % de su superficie en cuadras. (c) Las celdas sin cuadras que se tocan (también por la esquina) forman una **zona**. Las zonas se ordenan por m² ganados; el KML lleva las 20 más grandes.
- **Opciones**: corte de cobertura en 10, 25 o 50 %; ganancia mínima de 200, 500 o 1 000 m²; usar el polígono de la localidad en lugar de las cuadras (incluye calles); contar solo celdas sin ninguna cuadra.
- **Quién**: Claude (provisional, **pendiente de la revisión de Alejandro** con `docs/verificar_zonas_ghsl.csv`).
- **Por qué**: una celda urbana ya construida en 2010 tiene normalmente 69–90 % de su superficie en cuadras (percentiles 10–90), porque las calles no son cuadra. Con menos de 25 %, la celda está claramente fuera de la traza del INEGI. 500 m² equivale a unas 4–5 casas y evita contar como crecimiento las variaciones pequeñas del modelo. Los resultados se mueven poco con los cortes alternativos (V46).
