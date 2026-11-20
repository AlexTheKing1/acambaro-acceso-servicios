# Nota de método

Fecha: 2026-11-13 (fase 6); actualizada el 2026-11-20 (fase 8: grupo que depende de las unidades abiertas y sección 6, límites). Esta nota junta en un solo lugar cómo se mide el acceso y en qué normas se apoya. Las decisiones detalladas están en `docs/decisiones.md` (D01–D69) y los chequeos en `docs/validacion.md` (V1–V63).

## 1. Qué se mide

- **Población**: Censo 2020 por cuadra (la más reciente a ese nivel). En lo rural, el ITER 2020 por localidad.
- **Servicios**: los vigentes en 2026 (Marco Geoestadístico EIC 2025, DENUE 05/2026, catálogo SEP consultado el 2026-10-22, CLUES de agosto de 2026).
- **Distancia**: en las 4 localidades urbanas, a pie por la red de calles desde cada cuadra al servicio más cercano. En lo rural, línea recta × 1.33 desde el punto de la localidad, porque no se pudo bajar una red de caminos (D26). Las cifras rurales se reportan con el rango que dan factores de 1.0 a 1.5 (`src/31_sensibilidad_factor.py`).
- **"Lejos"**: más allá de un umbral. Se reportan tres (estricto, principal y holgado, D33). El principal es la cifra del reporte.

## 2. Referencias normativas

| Documento | Qué dice que nos sirve | Qué no dice |
|---|---|---|
| SEDESOL (1999), *Sistema Normativo de Equipamiento Urbano*, tomo I (Educación y cultura), tomo II (Salud y asistencia social) y tomo III (Comercio y abasto) | El "radio de servicio urbano recomendable" de cada elemento: jardín de niños 750 m; primaria 500 m; secundaria general 1 000 m; preparatoria general y Colegio de Bachilleres 2 a 5 km; CBTIS y CONALEP 5 a 10 km; centro de salud urbano 1 km; un centro de salud rural por localidad de 2 500 a 10 000 habitantes; mercado público 750 m; tianguis o mercado sobre ruedas 750 a 1 000 m | Ningún tomo tiene glosario ni dice si el radio es en línea recta o por calles |
| SEDATU–GIZ (2024), *Lineamientos de equipamiento* | p. 19: no sustituyen al "Sistema Normativo vigente", aunque lo critican por rígido. p. 26–27: marco de accesibilidad. p. 80: "radio caminable de 800 metros" | No fija nuevos radios por tipo de servicio que sustituyan a los de 1999 |
| NOM-002-SEDATU-2022 | Clasifica el equipamiento (sistemas y subsistemas) | No fija distancias |

Las tres referencias y sus páginas son las que dio Alejandro. Los documentos no están en el release del proyecto: **Claude no los cotejó** (ver `docs/fuentes.md`).

**Redacción acordada para el sitio y el PDF:**

> Usamos los radios del Sistema Normativo de 1999, que SEDATU (2024) reconoce como vigente. La norma no define si el radio es en línea recta; por eso reportamos tres umbrales.

## 3. Los tres umbrales

Como la norma no dice si el radio es en línea recta, se reportan tres umbrales (D33): **estricto** = el radio de la norma medido por calles; **principal** = el radio convertido a distancia por calles (× 1.33, el rodeo típico de la red de la ciudad); **holgado** = principal × 1.5. Si un hallazgo solo aparece con uno de los tres, se dice.

| Servicio, ciudad (a pie) | Estricto | Principal | Holgado |
|---|---:|---:|---:|
| Preescolar | 750 m | 1 000 m | 1 500 m |
| Primaria | 500 m | 670 m | 1 000 m |
| Secundaria | 1 000 m | 1 330 m | 2 000 m |
| Bachillerato | 2 500 m | 3 330 m | 5 000 m |
| Salud de primer nivel | 1 000 m | 1 330 m | 2 000 m |
| Tienda básica | 380 m | 500 m | 750 m |
| Mercado o supermercado | 750 m | 1 000 m | 1 500 m |

### Bachillerato
La norma de SEDESOL (1999) da un rango, no un valor: **preparatoria general y Colegio de Bachilleres, de 2 a 5 km; CBTIS y CONALEP, de 5 a 10 km**. Nuestros umbrales de la ciudad (**2.5 / 3.33 / 5 km**) caen dentro del rango de la preparatoria general. Por eso el resultado del bachillerato es frágil: con el umbral holgado (5 km, el tope del rango) casi nadie queda lejos; con el principal, 43 % de la ciudad. No usamos el rango de CBTIS y CONALEP porque la medida cuenta todos los bachilleratos, no solo los tecnológicos.

### Mercados y tianguis
La norma (tomo III) da para el **mercado público un radio de 750 m** y para el **tianguis o mercado sobre ruedas, de 750 a 1 000 m**. Nuestro umbral principal de abasto completo (1 000 m) queda en el tope del rango del tianguis. Pero **ninguna fuente registra tianguis** (D35): donde no hay mercado registrado, no se puede decir que no haya abasto. Puede haber un tianguis que ninguna fuente captura. En lo rural (umbral de 10 km) la norma no tiene un valor comparable.

## 4. Salud: pública y abierta

Desde la fase 3, "salud pública de primer nivel" (D20) contaba toda unidad pública, incluidas las que **solo atienden a sus derechohabientes**. En la fase 6 se separa (D58):

- **Salud abierta** (atiende a cualquier persona): Secretaría de Salud de Guanajuato (centros de salud y UMAPS), IMSS-Bienestar y Unidades Médicas Rurales del IMSS.
- **Solo derechohabientes**: IMSS ordinario (UMF, HGSMF, UMFH) e ISSSTE.

La medida "salud abierta" se calcula para toda la población y para el **grupo que depende de las unidades abiertas** (D69): las personas sin afiliación a servicios de salud, las afiliadas al INSABI / Seguro Popular y las afiliadas al IMSS-Bienestar, según la clasificación del Censo 2020. Ninguna de ellas puede usar las clínicas del IMSS ordinario ni del ISSSTE. Cada componente se estima por AGEB (D10) con su propio "*"; el grupo es la suma de las tres estimaciones, con el piso seguro (lo visible cuadra por cuadra) al lado. La población sin afiliación se reporta como subgrupo. La medida anterior (cualquier unidad pública) se conserva para comparar.

Dos cuidados: (1) es la clasificación de 2020; el INSABI ya no existe y sus afiliados siguen atendiéndose en las mismas unidades; (2) el censo permite varias afiliaciones (en la ciudad, al menos 830 personas tienen más de una), así que algunas personas del grupo pueden tener también IMSS o ISSSTE.

## 5. Datos ocultos y lo que no se mide

- El INEGI oculta con "*" los datos de cuadras con pocas viviendas. Los grupos de población se estiman por AGEB (D10) y se reporta el mínimo visible al lado.
- La tienda básica y los consultorios privados no se miden en lo rural (D32, D35).
- "Vialidad primaria" no se puede medir: el Marco Geoestadístico solo dice el tipo de nombre de la calle (calle, avenida, carretera), no su jerarquía (D61).

## 6. Límites

Lo que el sitio y el PDF deben declarar. Los seis primeros ya estaban en los documentos; del 7 al 20 se agregaron en la fase 8, a partir de la revisión final (`docs/revision_final.md`, sección 6).

1. **Lo rural se mide en línea recta × 1.33.** El factor se calibró con las calles de la ciudad, no con caminos rurales. Las cifras rurales cambian mucho con él: con factores de 1.0 a 1.5, la población rural lejos de salud va de 6 % a 28 %, y la lejos de un mercado o supermercado, de 17 % a 49 % (`sensibilidad_factor_rural.csv`).
2. **La verificación de los servicios fue remota, no en campo, y no al azar.** Se revisaron en Google Maps 68 sedes; 1 de cada 4 no se vio. Las primarias y secundarias casi no se revisaron en imagen y descansan en el catálogo de la SEP.
3. **Fechas distintas.** La población es del Censo 2020; los servicios, de 2026: DENUE de mayo de 2026, CLUES de agosto de 2026 y catálogo SEP sin fecha de corte (consultado el 2026-10-22, D40). La CLUES da como fuera de operación la clínica del ISSSTE que el estudio cuenta como abierta (D36).
4. **Ninguna fuente registra tianguis.** Donde no hay mercado registrado no se puede decir que no haya abasto.
5. **Las normas no se cotejaron** con el documento original (sección 2).
6. **Las citas del Plan 2040 y del Programa 2025 se verificaron sobre un OCR.** Las citas positivas están en su página; lo que "no se encontró" en esos dos documentos puede estar en una tabla o un mapa que el OCR no lee.
7. **El grupo que depende de las unidades abiertas es la clasificación del Censo 2020** (sección 4), con afiliaciones que pueden repetirse.
8. **La distancia no mide capacidad ni calidad.** Una escuela cerca puede no tener cupo; una unidad de salud puede tener 2 núcleos básicos u 11, o no tener médico ese día. El estudio mide dónde está el servicio.
9. **El umbral principal lleva un supuesto**: que el radio de la norma es en línea recta. Si fuera distancia recorrida, todas las cifras de la ciudad serían las del umbral estricto (primaria 55 % en vez de 32 %; del grupo que depende de las unidades abiertas, 72 % en vez de 58 % viviría lejos).
10. **"Lejos" es a pie.** En la ciudad no se considera transporte público, bicicleta ni automóvil.
11. **Cinco rutas de control.** La comparación con Google Maps son 5 rutas elegidas, 4 en la ciudad. En lo rural solo hay un recorrido verificado (límite 20).
12. **Muchas correlaciones, pocos casos.** En el vaciamiento se probaron 54 correlaciones; con 42 AGEB en la ciudad, alguna saldría "moderada" por azar. No se corrigieron por eso.
13. **"Deshabitada" es una foto del día del censo** (marzo de 2020). No distingue casa abandonada, en venta, en renta o de migrante que vuelve.
14. **Las AGEB de 2010 y 2020 no son las mismas.** La comparación por anillos y AGEB usa "unidades comparables" del estudio (D44), que cubren el 92 % de las viviendas de la ciudad.
15. **Las proyecciones del PROT son de CONAPO** sobre el Censo 2010. Compararlas con el censo de 2020 dice que la proyección no se cumplió, no por qué.
16. **La Encuesta Intercensal 2015 es una encuesta.** Su cifra para el municipio (112 125, tabulado del INEGI; la misma que cita el Programa de Gobierno 2025, p. 41) es la población en viviendas particulares habitadas, con un intervalo de 90 % de 103 624 a 120 626, que incluye las cifras de los censos de 2000 y 2020. No está en la serie ni en la gráfica de proyección (pendiente de la versión 1.1).
17. **Cada polo se evalúa en su localidad sede**, que el plan de 2006 no nombra (D60). "Tiene" quiere decir que hay al menos una sede dentro, aunque sea un telebachillerato.
18. **El estado del ordenamiento municipal** se conoce por el Programa de Gobierno (julio de 2025) y por la ficha municipal del IPLANEG (consultada el 12 de noviembre de 2026; la dirección ya no estaba disponible el 19 de noviembre). No se revisó el Periódico Oficial después de agosto de 2025.
19. **2005 es un conteo**, no un censo, y dio cifras bajas en toda la región.
20. **En el único recorrido rural verificado, el factor 1.33 sobreestimó la distancia.** De Parácuaro a la Secundaria Técnica 24: 4.3 km en línea recta, 5.7 km estimados, 4.9 km por carretera según Google Maps (factor real 1.15; D68). Es un solo caso: no dice hacia dónde se equivoca el factor en general, que en caminos con ríos, cerros o presas puede quedarse corto.
