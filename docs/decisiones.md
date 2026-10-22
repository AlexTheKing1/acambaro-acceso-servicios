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
