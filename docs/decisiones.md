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
- **Quién**: Claude (provisional; **el umbral de 50 % es de criterio**, ver pregunta 4 del resumen).
- **Por qué**: INEGI renumera manzanas que ya existían (subdivisiones, cambios de AGEB): 30 de las 38 claves nuevas 2020→2025 están sobre suelo que ya era manzana. Contar solo claves exageraría el crecimiento.

### D04 · 2026-10-22 · Caserío disperso urbano (clave de manzana 800)
- **Decisión**: incluir las 32 claves "800" de la tabla censal 2020 (464 personas) usando su geometría de puntos de la capa `caserio_disperso` del MG 2020.
- **Opciones**: descartarlas · incluirlas como puntos.
- **Quién**: Claude (provisional).
- **Por qué**: son viviendas reales fuera de manzana; descartarlas perdería 464 personas.

### D05 · 2026-10-22 · Datos ocultos por confidencialidad ("*")
- **Decisión**: el "*" se trata como dato ausente; **no se imputa**. En cada paso se reporta cuánta población queda oculta (total de la AGEB menos la suma visible de sus manzanas).
- **Opciones**: dejar vacío · repartir el faltante de cada AGEB entre sus manzanas con "*" · trabajar los grupos de edad a nivel AGEB.
- **Quién**: Claude (provisional). **Pendiente de Alejandro** cómo tratarlo en los resultados por grupo (pregunta 2 del resumen).
- **Por qué**: la regla del proyecto es no inventar datos.

### D06 · 2026-10-22 · Servicios fuera del municipio
- **Decisión**: conservar servicios del DENUE hasta 10 km fuera del límite municipal, incluidos los de Michoacán (y se revisó Querétaro).
- **Opciones**: solo dentro del municipio · franja de 5, 10 o más km.
- **Quién**: Claude (provisional). **Pendiente de Alejandro** (pregunta 3).
- **Por qué**: 75 de los 274 km del contorno municipal son límite estatal; para localidades de borde, la escuela o tienda más cercana puede estar en otro municipio o estado.

### D07 · 2026-10-22 · GHSL
- **Decisión**: mosaico R7_C9 (100 m, Mollweide) de GHS-BUILT-S R2023A, años 1975–2020. No se bajan 2025 ni 2030.
- **Quién**: definido por Alejandro (solo serie observada); el mosaico y la resolución, Claude.
- **Por qué**: 2025 y 2030 son proyecciones del modelo, no observación.

### D08 · 2026-10-22 · Fuentes no descargables
- **Decisión**: CLUES, SEP y CONAPO las baja Alejandro y las sube al release `datos-crudos`.
- **Quién**: Alejandro.
- **Por qué**: no hay acceso desde el entorno de trabajo (ver `docs/fuentes.md`).
