# Nota de método

Fecha: 2026-11-13 (fase 6). Esta nota junta en un solo lugar cómo se mide el acceso y en qué normas se apoya. Las decisiones detalladas están en `docs/decisiones.md` (D01–D63) y los chequeos en `docs/validacion.md`.

## 1. Qué se mide

- **Población**: Censo 2020 por cuadra (la más reciente a ese nivel). En lo rural, el ITER 2020 por localidad.
- **Servicios**: los vigentes en 2026 (Marco Geoestadístico EIC 2025, DENUE 05/2026, catálogo SEP consultado el 2026-10-22, CLUES de agosto de 2026).
- **Distancia**: en las 4 localidades urbanas, a pie por la red de calles desde cada cuadra al servicio más cercano. En lo rural, línea recta × 1.33 desde el punto de la localidad, porque no se pudo bajar una red de caminos (D26).
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

La medida "salud abierta" se calcula para toda la población y, aparte, para la población **sin afiliación a servicios de salud** (Censo 2020). La medida anterior se conserva para comparar.

## 5. Datos ocultos y lo que no se mide

- El INEGI oculta con "*" los datos de cuadras con pocas viviendas. Los grupos de población se estiman por AGEB (D10) y se reporta el mínimo visible al lado.
- La tienda básica y los consultorios privados no se miden en lo rural (D32, D35).
- "Vialidad primaria" no se puede medir: el Marco Geoestadístico solo dice el tipo de nombre de la calle (calle, avenida, carretera), no su jerarquía (D61).
