# Registro de validación

Cada chequeo con su resultado en cifras, incluido lo que salió mal. Las cifras de la fase 1 las genera `src/03_base_geografica.py` en `data/processed/validacion_fase1.json`.

## Fase 0 — Descargas (2026-10-22)

**V00 · Descargas.** 23 archivos bajados de INEGI y JRC; todos verificados como ZIP válidos (INEGI responde con una página HTML cuando un archivo no existe, por eso se revisa la firma del archivo). Faltan 3 fuentes (CLUES, SEP, CONAPO): no accesibles desde el entorno (ver `docs/fuentes.md`). El release `datos-crudos` del repo todavía no tiene archivos (404).
- **Salió mal**: datos.gob.mx bloqueado (403) aunque se esperaba permitido; los enlaces de datos abiertos de CONAPO en gob.mx están rotos (404); la API de escuelas de la SEP tiene un certificado incompleto.

## Fase 1 — Base geográfica (2026-10-22)

**V01 · Población por manzana vs. ITER, por localidad urbana (Censo 2020).**

| Localidad | ITER 2020 | Suma de manzanas | Diferencia | Manzanas |
|---|---:|---:|---:|---:|
| Acámbaro (0001) | 56 597 | 56 596 | **−1** | 1 224 |
| Irámuco (0027) | 6 275 | 6 275 | 0 | 147 |
| Parácuaro (0047) | 4 159 | 4 159 | 0 | 147 |
| Chupícuaro / Nuevo Chupícuaro (0017) | 2 583 | 2 583 | 0 | 134 |
| **Total** | **69 614** | **69 613** | **−1** | 1 652 |

La persona faltante está en la AGEB 0111 de Acámbaro: el total publicado de la AGEB es 1 mayor que la suma de sus manzanas. Es una inconsistencia de la publicación de INEGI; no se corrige. ("Manzanas" incluye 32 claves 800 de caserío disperso.)

**V02 · Cobertura de los datos por manzana.** Solo las 4 localidades urbanas tienen datos por manzana: 69 614 personas = **64.0 %** del municipio (108 697). Las otras **39 083 personas (36.0 %)** viven en 208 localidades rurales y solo tienen dato a nivel localidad (ITER). De ellas, 37 976 viven en 100 localidades rurales que sí tienen manzanas dibujadas en el MG, pero sin población por manzana.

**V03 · Unión tabla censal ↔ polígonos MG 2020.** 1 620 de 1 620 manzanas urbanas del MG 2020 tienen dato censal (100 %). 32 filas de la tabla (464 personas) no tienen polígono: son la clave de manzana 800 (caserío disperso); las 32 sí se encuentran en la capa de puntos `caserio_disperso` y se incorporaron así (D04). Población con geometría: 69 149 en polígonos + 464 en puntos = 69 613. Filas sin ninguna geometría: 0.

**V04 · Población oculta por confidencialidad (Censo 2020, 4 localidades urbanas).** En los datos no aparece ningún valor 1 ni 2: INEGI los sustituye por "*". Población oculta = total publicado por AGEB − suma visible por manzana.

| Grupo | Total publicado (AGEB) | Visible en manzanas | Oculta | % oculto | Manzanas con "*" |
|---|---:|---:|---:|---:|---:|
| Población total | 69 614 | 69 613 | 1 | 0.0 % | 0 |
| 3 a 5 años | 3 463 | 2 705 | 758 | **21.9 %** | 729 |
| 6 a 11 años | 6 452 | 5 856 | 596 | 9.2 % | 571 |
| 12 a 14 años | 3 377 | 2 647 | 730 | **21.6 %** | 697 |
| 15 a 17 años | 3 544 | 2 830 | 714 | **20.1 %** | 701 |
| 60 años y más | 11 146 | 10 629 | 517 | 4.6 % | 487 |
| Con discapacidad | 4 329 | 3 690 | 639 | 14.8 % | 636 |

- 51 manzanas tienen menos de 3 viviendas habitadas (todas sus variables con "*" salvo POBTOT y VIVTOT); su población total publicada es 0, así que no esconden personas en el total.
- Viviendas: VIVTOT no tiene ocultos (27 032). Viviendas particulares deshabitadas: 6 036 en el total de AGEB, 5 306 visibles por manzana (**730 ocultas, 12.1 %**). De uso temporal: 1 795 en AGEB, 1 168 visibles (**627 ocultas, 34.9 %**).

**V05 · Localidades ITER 2020.** 212 localidades; suma de su población = 108 697 = total municipal (diferencia 0). Las filas 9998 "localidades de una vivienda" (141 hab.) y 9999 "de dos viviendas" (137 hab.) son agregados de localidades que ya aparecen una por una (hay 67 localidades con ≤ 2 viviendas habitadas); no se suman de nuevo. Todas tienen coordenadas. En el MG 2020: 104 son localidades amanzanadas (107 590 hab.) y 108 son puntuales (1 107 hab.); ninguna falta.

**V06 · EIC 2025 vs. Censo 2020.** Municipio: 108 140 en 2025 (error estándar 4 551; intervalo de confianza 100 644 – 115 636; CV 4.2 %) vs. 108 697 en 2020: **−0.5 %, dentro del margen de error**. Ciudad de Acámbaro: 56 771 (IC 50 768 – 62 774) vs. 56 597. Conclusión: no hay evidencia de cambio de población 2020–2025; la EIC no permite afirmar que creció ni que bajó.
- Contexto 2010: municipio 109 030; ciudad 57 972 (−2.4 % en 2020).

**V07 · Proyección asignada a la cartografía rural 2010.** 411 shapefiles rurales de 2010 sin archivo de proyección. Tras asignarles la de los urbanos y comparar manzanas con la misma clave en 2020: mediana de desplazamiento de centroides **0 m** (rurales, 1 514 pares; urbanas, 1 306 pares); percentil 95: 46 m rurales, 34 m urbanas (manzanas redibujadas). La asignación es correcta.

**V08 · Manzanas nuevas después de 2020 (MG EIC 2025 vs. MG 2020).**
- Manzanas en el municipio: 3 505 (2020) → 3 522 (EIC 2025).
- Por clave: 38 claves nuevas, pero 30 de ellas están sobre suelo que ya era manzana en 2020 (renumeraciones o subdivisiones).
- Por geometría (D03): **17 manzanas nuevas, 12.8 ha**, todas en localidades ya cartografiadas: 4 en la ciudad de Acámbaro, 3 en la localidad 0087, 3 en la 0481 y 1 en cada una de 0017, 0027, 0005, 0071, 0043, 0378, 0072.
- 21 claves de 2020 ya no existen en 2025.
- **Ojo**: 12.8 ha en 5 años es muy poco frente a 2010–2020 (abajo). Puede ser real o que INEGI no haya actualizado toda la periferia. No hay otra fuente oficial observada posterior a 2020 para contrastarlo (GHSL 2025 es modelado).

**V09 · Manzanas nuevas 2010 → 2020 (MG 2020 vs. cierre Censo 2010).** 685 claves nuevas; por geometría, 323 manzanas nuevas (247.8 ha). De ellas, 149 están en localidades que no tenían cartografía en 2010 (no es necesariamente crecimiento, solo que antes no se había dibujado); **174 manzanas / 120.6 ha** son crecimiento en localidades ya cartografiadas (30 en la ciudad de Acámbaro).

**V10 · GHSL, superficie construida observada en el municipio.** 1 107 ha (2010) → 1 358 ha (2020): **+23 %**, mientras la población bajó 0.3 %. Serie completa en `docs/inventario.md`.

**V11 · DENUE.** Corte 05_2026. 5 974 establecimientos en Acámbaro; 16 142 en la franja de 10 km (12 018 de Guanajuato, 4 124 de Michoacán, 0 de Querétaro).
