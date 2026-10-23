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

## Fase 2 — Catálogo de servicios (2026-10-22)

Cifras generadas por `src/06_catalogo_servicios.py` en `data/processed/validacion_fase2.json`.

**V12 · Fuentes disponibles.** El release `datos-crudos` sigue vacío (404): **no hay CLUES ni catálogo SEP**. El catálogo se armó con el MG EIC 2025 (Guanajuato y Michoacán) y el DENUE 05/2026 (D14). Recorte de servicios del MG a la franja de 10 km: 1 897 puntos (621 en Acámbaro, igual que el recorte municipal de la fase 1) y 829 áreas (226 en Acámbaro).

**V13 · El DENUE registra pocas escuelas públicas y centros de salud.** Registros dentro de Acámbaro:

| Tipo | MG EIC 2025 | DENUE | Registros del DENUE con un registro del MG a ≤ 150 m | Registros del MG con uno del DENUE a ≤ 150 m |
|---|---:|---:|---:|---:|
| Preescolar | 90 | 29 | 27 | 25 |
| Primaria | 115 | 34 | 34 | 27 |
| Secundaria | 34 | 9 | 9 | 8 |
| Bachillerato | 6 | 10 | 4 | 4 |
| Salud de primer nivel | 26 | 9 | 6 | 6 |

- Casi todo lo que está en el DENUE también está en el MG (escuelas básicas: 70 de 72), pero el MG tiene unas 3 veces más escuelas. Las que solo están en el MG son sobre todo rurales (mapa `docs/figuras/fase2_servicios.png`): el DENUE casi no registra escuelas ni centros de salud de las localidades rurales.
- **Bachillerato es al revés**: el MG solo dibuja 6 en el municipio y le faltan, por ejemplo, el CBTIS 147 de Acámbaro y el CBTA 298 de Parácuaro, que sí están en el DENUE. Ninguna de las dos fuentes es completa; se usa la unión.
- Distancia mediana entre el MG y el DENUE cuando registran el mismo sitio: 23 m (preescolar), 23 m (primaria), 25 m (secundaria), 53 m (bachillerato), 21 m (salud).

**V14 · Sedes (un punto por sitio, D16).** Dentro de Acámbaro / en la franja de 10 km:

| Tipo | Acámbaro | Franja 10 km | Solo MG | Solo DENUE | Ambas | Sector conocido (Acámbaro) |
|---|---:|---:|---:|---:|---:|---|
| Preescolar | 92 | 204 | 65 | 2 | 25 | 24 públicas, 3 privadas, 65 sin dato |
| Primaria | 112 | 208 | 88 | 0 | 24 | 22 públicas, 2 privadas, 88 sin dato |
| Secundaria | 34 | 85 | 26 | 0 | 8 | 8 públicas, 26 sin dato |
| Bachillerato | 12 | 23 | 2 | 6 | 4 | 7 públicos, 3 privados, 2 sin dato |
| Salud de primer nivel | 29 | 67 | 20 | 3 | 6 | 9 públicas, 20 sin dato |
| Abasto | 824 | 1 447 | — | — | — | — |

- Abasto en Acámbaro: 792 abarrotes, 23 minisúper, 3 supermercados y 6 mercados (Miguel Hidalgo con 201 locales, 22 de Octubre, San Antonio y Sóstenes Rocha en la ciudad; los municipales de Parácuaro y Chupícuaro). Los 740 locales del DENUE en mercados públicos (todo el área) se juntaron en 12 mercados; 4 de los 6 de Acámbaro coinciden con un mercado del MG.
- Franja de 10 km por entidad: Michoacán aporta 89 preescolares, 92 primarias, 39 secundarias, 9 bachilleratos, 38 unidades de salud y 614 comercios de abasto.
- Excluidos del MG: 1 centro de salud "fuera de uso" y 1 preescolar "en construcción". Áreas del MG: 82, ninguna duplicada de un punto (son escuelas o centros de salud dibujados solo como polígono).
- **"Sin dato" de sector**: el MG no dice si es pública o privada. Solo la SEP y la CLUES lo resuelven.

**V15 · Reclasificación por nombre (D17).** 4 registros del DENUE pasaron a salud de primer nivel: UMAPS Loma Dorada y Unidad de Medicina Familiar del ISSSTE (Acámbaro, ambos codificados como hospital general 622112), "Centro de Salud" (Acámbaro, 621399) y Unidad Médica Rural IMSS-Bienestar (Mariano Escobedo, Cuitzeo, 622112). Los dos de Acámbaro coinciden con un centro de salud del MG a ≤ 150 m.

**V16 · Casos dudosos detectados (quedan en la muestra para revisar).**
- UMAPS Irámuco: el DENUE y el MG lo ubican a **291 m** de distancia; quedaron como dos sedes. Puede ser el mismo edificio mal ubicado en una de las dos fuentes.
- "Centro Médico la Soledad" (MG, centro de salud) por el nombre parece privado.
- "Preparatoria abierta" (DENUE, bachillerato público) es una modalidad no escolarizada: no es una escuela a la que se asista a diario (pregunta para Alejandro).
- "Consultorio médico civil" (DENUE, consultorio público en Acámbaro): no se sabe qué institución es.
- Hospitales en Acámbaro (no se miden): IMSS, Hospital Municipal, Centro Médico Guadalupano y dos privados del DENUE. No se sabe si el IMSS tiene ahí también consulta familiar: lo dirá la CLUES.

**V17 · Listas de verificación (D13, D19).**
- `docs/verificar_zonas_nuevas.csv`: **163 zonas**. 2010–2020: 150 zonas (323 cuadras, 247.7 ha); de ellas 114 zonas (174 cuadras, 120.5 ha) en localidades que ya estaban cartografiadas en 2010 y 36 zonas (149 cuadras, 127.2 ha) en localidades sin cartografía en 2010. Posterior a 2020: 13 zonas (17 cuadras, 12.8 ha). Las zonas 2010–2020 de las localidades urbanas tenían 356 habitantes en 2020 (254 en la ciudad de Acámbaro); las rurales no tienen dato por cuadra.
- Una zona posterior a 2020 está en "Los Caballos [Fraccionamiento]" (0481), localidad dibujada en el MG 2020 pero **sin fila en el ITER 2020** (sin población censada); otra (San José de la Peña) mide 0.01 ha: probablemente un ajuste de dibujo.
- `docs/verificar_servicios_muestra.csv`: **134 sedes** en 36 estratos (todas las de salud de primer nivel y bachillerato del municipio y los 12 mercados).
- Los enlaces satelitales siguen el formato pedido (`https://www.google.com/maps/@LAT,LON,300m/data=!3m1!1e3`); los de Street View, el formato oficial `map_action=pano`. No se abrieron desde aquí (no hay navegador con Google Maps en el entorno): se comprobó solo que las coordenadas caen dentro del municipio o la franja.

## Fase 3 — Accesibilidad (2026-10-23)

Cifras generadas por `src/09_catalogo_sep_clues.py` (`validacion_fase3_catalogo.json`), `src/10_redes.py` (`validacion_fase3_red.json`), `src/11_accesibilidad.py` (`validacion_fase3_acceso.json`) y `src/12_colonias_contexto.py` (`validacion_fase3_colonias.json`), todos en `data/processed/`.

**V18 · SEP y CLUES recortados.** Catálogo SEP (Gto. + Mich.): 1 620 registros en la franja de 10 km, 565 dentro del municipio; ninguno de Acámbaro sin coordenadas; 1 de Salvatierra cae dentro del límite de Acámbaro. De los centros tipo "escuela" de la franja, 429 están INACTIVOS. CLUES: 173 registros en la franja (124 en operación, 49 fuera de operación); 57 declarados en Acámbaro, de los cuales **5 no tienen coordenadas** (consultorios junto a farmacias: 4 Farmacias Similares en operación y 1 Benavides fuera de operación) y quedan fuera.
- **Salió mal y se corrigió**: la CLUES trae la institución "SERVICIOS DE SALUD IMSS BIENESTAR " con un espacio al final; en la primera corrida eso dejó fuera las 16 unidades de IMSS-Bienestar de Michoacán y 12 centros de salud de Michoacán aparecían "dados de baja" (eran el cambio de la Secretaría de Salud a IMSS-Bienestar en 2024, con nueva clave y mismas coordenadas). Ahora se limpian los espacios.

**V19 · Cruce del catálogo con SEP y CLUES (D29). Sedes dentro de Acámbaro:**

| Tipo | Fase 2 | Confirmadas | No confirmadas | Dadas de baja | Nuevas (solo SEP/CLUES) | Fase 3 (que se miden) |
|---|---:|---:|---:|---:|---:|---:|
| Preescolar | 92 | 83 | 3 | 6 | 15 | **101** |
| Primaria | 112 | 94 | 17 | 1 | 6 | **117** |
| Secundaria | 34 | 34 | 0 | 0 | 7 | **41** |
| Bachillerato (escolarizado) | 12 | 8 | 2 | 1 | 16 | **26** |
| Salud de primer nivel | 29 | 20 | 8 | 1 | 2 | 24 públicas (D30) |
| Consultorio privado (aparte) | 44 | 5 | 39 | 0 | 1 | 45 |

- **Cuántas cambiaron en Acámbaro**: 46 sedes nuevas (15 preescolares, 6 primarias, 7 secundarias, 16 bachilleratos, 2 de salud), 10 dadas de baja (incluido un hospital privado), 1 preparatoria abierta pasa a "bachillerato no escolarizado" y 1 videobachillerato del CERESO a "escuela en centro penitenciario"; además el sector (público/privado) se conoce ahora en casi todas: escuelas con sector desconocido pasan de 181 a 27.
- Registros que cruzaron: SEP 395 a ≤ 150 m y 201 como vecinos mutuos a ≤ 300 m; 271 sin sede (nuevos). CLUES 85 a ≤ 150 m, 7 vecinos mutuos, 28 nuevos. Distancia entre el registro oficial y la sede: SEP mediana 62 m (p90 215 m); CLUES mediana 24 m (p90 132 m).
- **Lo nuevo son sobre todo escuelas rurales pequeñas** que ni el MG ni el DENUE tenían: telebachilleratos comunitarios (Monte Prieto, La Ortiga, San Mateo Tócuaro, Andocutín, El Rodeo), videobachilleratos (Arroyo de la Luna, Loreto, Chamácuaro), telesecundarias (Santiaguillo, San José de las Pilas, San Luis de los Agustinos, Tres Marías) y preescolares y primarias comunitarias (CONAFE). En la ciudad: preparatorias privadas y el CONALEP 163 (en Jesús Ruiz Ruiz).
- **Dadas de baja**: 6 preescolares y 1 primaria rurales (El Sauz, San José de la Peña ×2, El Moral, San Ramón, Los Ángeles (El Carrizo), La Carpa), la Preparatoria Prof. Leopoldo Salgado (ciudad; ojo: su "plantel" sigue activo en la SEP, ver V27), la **UMAPS vieja de Irámuco** (la CLUES la sustituyó por la nueva, a unos 300 m; resuelve el caso dudoso de V16) y un hospital privado (Sanatorio del Refugio).
- 4 conflictos de sector entre DENUE y SEP (se usa la SEP): Secundaria Federal Lic. Rafael Carrillo y Bachillerato Bivalente Militarizado (DENUE: público; SEP: privado); Centro Educativo Gabriela Mistral y Preparatoria por Cooperación Melchor Ocampo (al revés).
- 1 cambio de tipo por la CLUES: "Clínica Los Ángeles" (franja) pasa de primer nivel a hospital.
- De las 30 sedes "no confirmadas" de Acámbaro (17 primarias, 8 de salud, 3 preescolares, 2 bachilleratos), 25 vienen solo del MG y 20 no tienen nombre; 14 tienen a ≤ 60 m un registro SEP de **otro nivel** (p. ej. el MG dice "primaria" donde la SEP tiene un preescolar o un videobachillerato): el MG pudo haber etiquetado mal el nivel. Columna `oficial_otro_tipo_cerca` en `servicios_sedes_fase3.csv`.

**V20 · Matrícula.** Ninguna fuente disponible (SEP, CLUES, DENUE, MG) trae matrícula o número de alumnos. No se puede decir cuántos estudian en la preparatoria abierta.

**V21 · Red de calles (D31).** 9 648 ejes del MG EIC 2025 → 24 969 tramos. Antes de unir: 164 pedazos sin conexión y 2 046 extremos sueltos. Se agregaron 455 uniones de calles "cortadas" (mediana 8.8 m, máximo 14.9 m) → 138 pedazos (la mayoría son localidades rurales distintas, que en el MG no están unidas por caminos). En las localidades urbanas quedan cuadras en pedazos aislados de la red principal: Acámbaro 8 cuadras (193 personas, un grupo de 6 cuadras con 159), Irámuco 6 (28), Parácuaro 1 (8), Chupícuaro 0. Esas cuadras se conectan a la red principal con su tramo de acceso en línea recta.
- Tramo de acceso de la cuadra a la calle: mediana 26–38 m según la localidad, p95 70–85 m; máximos de 450–700 m en puntos de caserío disperso (viviendas fuera de cuadra). 14 cuadras tienen acceso > 100 m.
- **Riesgo**: una unión de < 15 m puede cruzar un muro o un canal que en realidad no se puede cruzar. No se revisaron una por una (capa `uniones` en `red_peatonal.gpkg`).

**V22 · Red rural no disponible (D26).** RNC: sin enlace directo (2 intentos). Overpass: conexión cortada por el proxy ("tunnel closed after 8 s"), 2 intentos — y **2 más por un error de Claude** al volver a correr la descarga con esa fuente incluida (se corrigió: ahora solo se intenta con `--solo osm_caminos`). Geofabrik: conexión cortada, 2 intentos. Se usó línea recta × factor.

**V23 · Factor de rodeo y controles de la medición.**
- Factor = **1.33** (mediana de distancia por red / línea recta en 14 456 pares cuadra–servicio más cercano con recta ≥ 300 m; p25 1.23, p75 1.47).
- Distancia por red menor que la línea recta: **0 casos** (control de que la red no "atajó").
- Población en los orígenes por localidad = V01 (Acámbaro 56 596 —falta la persona de la AGEB 0111—, Irámuco 6 275, Parácuaro 4 159, Chupícuaro 2 583).
- Servicios medidos en línea recta × factor por estar fuera de la red de la localidad (a > 300 m de ella): en Parácuaro **todas** las cuadras para secundaria (no hay secundaria en la localidad, ver V25); en Irámuco todas para abasto completo; en Acámbaro 550 cuadras para bachillerato público (el CECyTE y el CONALEP están en la orilla o fuera de la red).

**V24 · El DENUE no cubre comercios rurales (D32).** De los 5 974 establecimientos del DENUE en Acámbaro, 5 932 están en las 4 localidades urbanas; los 42 restantes están dispersos en 28 localidades rurales y **ninguno es abarrotes, minisúper o supermercado**. La tienda básica y el consultorio privado no se pueden medir en lo rural.

**V25 · Casos raros (distancias extremas y sin ruta).**
- **Parácuaro no tiene secundaria** según la SEP, el MG y el DENUE: la más cercana es la Secundaria Técnica 24, en el campus agropecuario a ~4 km (5.4 km mediana estimada). Todas sus 4 159 personas quedan "lejos" con cualquier umbral. Vale la pena confirmarlo.
- **Irámuco no tiene mercado ni supermercado**: el más cercano está a 15–17.6 km (estimado en línea recta × factor).
- El Bachillerato SABES de Irámuco está ~2 km al oeste del pueblo: 57 % de Irámuco queda a más de 2.5 km.
- Máximos dentro de la ciudad de Acámbaro: preescolar y primaria ~2.8 km (puntos de caserío disperso de la orilla), secundaria 3.4 km, bachillerato 3.8 km, salud 3.6 km.
- Rurales: **Isla Cerro Grande (Isla Chanaco), 73 hab., es una isla**: no hay ruta por tierra; su distancia estimada (4.8 km a preescolar, 6.7 km a secundaria) no representa el viaje real. La Ortiga (1 107 hab.) queda a 7.3 km de una unidad pública de salud (su punto de salud del MG no está en la CLUES, D30). Gaytán del Refugio (536 hab.) y El Sauz (229 hab.) quedan a ~11 km de un bachillerato. Abasto completo: hasta 20.9 km (localidades de 1 a 19 habitantes).
- Ninguna localidad queda "sin ruta" en el cálculo porque la línea recta siempre existe; ese es justamente el límite del método (D26).

**V26 · Población por grupo (D10).** En 34 de 1 008 combinaciones ciudad × categoría × umbral × grupo, el mínimo visible (a) supera la estimación por AGEB (c) por 1 a 31 personas (sobre todo adultos mayores de Irámuco): ahí el supuesto de (c) falla y la cifra real es al menos (a). Columna `minimo_supera_estimado`. Población oculta en el ITER rural: 13 (3–5 años), 22 (6–11), 16 (12–14), 17 (15–17), 56 (60+), 26 (con discapacidad); la población total no tiene ocultos.

**V27 · Duplicados probables que quedan.**
- **CECyTE Acámbaro**: el MG y el DENUE lo ubican al sur de la ciudad (20.0135, −100.7402) y la SEP 4 km al norte (20.0451, −100.7158). Quedan los dos puntos; uno está mal. Afecta mucho al bachillerato público de la ciudad (es el más cercano para 548 cuadras).
- **CBTA 298**: el DENUE lo pone en Parácuaro y la SEP en el campus agropecuario a 4 km; el punto de Parácuaro coincide con el Videobachillerato de Parácuaro (SEP), así que ahí sí hay un bachillerato.
- **UMF del ISSSTE** (ciudad): el MG y el DENUE la tienen; la CLUES tiene una "UMF Acámbaro" del ISSSTE a 167 m **fuera de operación**, sin motivo ni fecha de baja. Se dejó como unidad que opera (el DENUE la registra en mayo de 2026); hay que confirmarlo.
- Preparatoria Prof. Leopoldo Salgado: la escuela está INACTIVA en la SEP pero su "plantel" sigue activo.

**V28 · Sensibilidad con solo sedes confirmadas (D28), umbral propuesto.** Quitar las 65 escuelas de preescolar, 66 primarias y 27 secundarias que solo dibuja el MG (en toda la franja) cambia poco: primaria en la ciudad de Acámbaro +1 381 personas lejos (de 31 392 a 32 773), Chupícuaro +275, localidades rurales +146 (preescolar), +210 (primaria), +234 (secundaria). Las demás categorías no cambian. Tabla completa: `data/processed/acceso_sensibilidad_confirmadas.csv`.

**V29 · Colonias (D24).** Catálogo INEGI: 147 asentamientos (141 en las 4 localidades urbanas), periodo 11/2021. Registros con nombre de asentamiento: DENUE 5 932, SEP 260, CLUES 13; de ellos coinciden con un nombre del catálogo 5 024, 85 y 9. Cuadras con nombre: **Acámbaro 99.8 %**, pero Irámuco 31 %, Chupícuaro 31 % y Parácuaro 24 %: en esas localidades casi todos los registros ponen como asentamiento el nombre del pueblo ("IRAMUCO", "PARACUARO"), no la colonia. 59 cuadras quedaron con empate entre dos nombres (se tomó el primero). 70 asentamientos del catálogo no quedaron en ninguna cuadra.
- Contexto social: 126 AGEB urbanas y 212 localidades; 96 AGEB y 68 localidades tienen al menos un indicador oculto ("*", valores de 1 o 2).

**V30 · Verificaciones de Alejandro.** `verificacion_zonas.csv` y `verificacion_servicios.csv` **no están** en el release: se incorporan en la siguiente fase. La muestra `docs/verificar_servicios_muestra.csv` no se regeneró; solo se le agregó la columna `confirmado_sep_clues` (resultado: de 103 escuelas y unidades de salud, 75 confirmadas por SEP (50) o CLUES (25), 25 no, 2 dadas de baja y 1 preparatoria abierta; 31 de abasto no aplican). Para comparar rutas: `docs/verificar_rutas.csv` (5 cuadras al azar, semilla 20261023).

## Fase 4 — Decisiones finales y verificaciones (2026-10-23)

Cifras generadas por `src/15_catalogo_fase4.py` (`validacion_fase4_catalogo.json`), `src/11_accesibilidad.py` (`validacion_fase4_acceso.json`), `src/17_zonas_kml.py` y `src/18_verificar_campo.py`.

**V31 · Texto del SNEU (D33).** Dos búsquedas web dirigidas al tomo de Educación del Sistema Normativo de Equipamiento Urbano (SEDESOL). Solo aparecieron fuentes secundarias (tesis y planes municipales) que usan el "radio de influencia" como círculo de cobertura. **No se encontró el texto original**, así que no se pudo confirmar si el "radio de servicio urbano recomendable" se define en línea recta. Tampoco se confirmaron los valores (750 / 500 / 1 000 m). Se aplicó × 1.33 como decidió Alejandro para este caso. **Pendiente: cotejar el documento original antes de publicar.**

**V32 · Red rural, nuevo intento (fase 4).** Overpass (`01_descargar.py --solo osm_caminos`), 2 intentos: "Connection reset by peer" en ambos, igual que en la fase 3. No se reintentó más. Lo rural se queda con línea recta × 1.33 (D26).

**V33 · Factor de rodeo con el catálogo de la fase 4.** Se usa el factor fijo de 1.33 (D33). Recalibrado con el nuevo catálogo da **1.349**, con 14 544 pares (p25 1.24, p75 1.50). El cambio viene casi todo del bachillerato público: con el CECyTE en el sur (D37), la mediana red / línea recta de esa categoría pasa de 1.29 a 1.51: los recorridos desde el norte de la ciudad son largos y con más rodeo. Las demás categorías no cambian (1.27–1.37).
- **Salió mal y se corrigió**: en la primera corrida el factor se recalibró solo (1.348) y movió entre 1 y 6 m distancias que no tenían por qué cambiar. Se fijó en 1.33. Además, la categoría del anexo (D34) quedó fuera de la calibración.
- **Control contra la fase 3** (mismas cuadras y localidades): cambia el servicio más cercano solo donde se esperaba. En salud pública cambian 45 cuadras (32 usaban el consultorio del CERESO). En bachillerato público cambian 852 cuadras (475 usaban el punto SEP del CECyTE). En bachillerato (todos) cambian 258. Las demás diferencias son de redondeo (≤ 6 m), porque la fase 3 usaba 1.3304 sin redondear.
- Población en los orígenes: igual que en la fase 3 (Acámbaro 56 596, Irámuco 6 275, Parácuaro 4 159, Chupícuaro 2 583). Distancia por red menor que la recta: 0 casos. En todas las filas, estricto ≥ principal ≥ holgado.
- 56 de 1 092 combinaciones ciudad × categoría × umbral × grupo tienen el mínimo visible por encima de la estimación por AGEB (por 1 a 39 personas). Ahí la cifra real es al menos el mínimo (columna `minimo_supera_estimado`).

**V34 · Parácuaro (D39).** Ninguna secundaria dentro de la localidad (SEP, MG, DENUE). Las más cercanas al centro del pueblo, en línea recta: la **Secundaria Técnica 24** (`secundaria-S0002`, SEP 11DST0024Y, campus de la Escuela Tecnológica Agropecuaria) a 4.2 km, y la Telesecundaria 847 de La Concepción (`secundaria-0015`) a 4.3 km, hacia el norte. Por camino estimado, la ST 24 es la más cercana para 72 de las 147 cuadras (3.3–6.3 km, mediana 5.5 km) y la Telesecundaria 847 para las otras 75 (mediana 5.3 km). Es la misma secundaria que calculó la fase 3: el "~4 km" era la línea recta.

**V35 · Fecha del catálogo SEP (D40).** `cct11.csv` y `cct16.csv` tienen 93 columnas. La única fecha es `F_FUNDACION` (fecha de fundación): llena en 4 278 de 22 017 registros (Gto.) y 8 749 de 26 898 (Mich.), con la más reciente en diciembre de 2017. No hay ciclo escolar ni fecha de corte. Se cita la fecha de consulta: 2026-10-22.

**V36 · Rutas contra Google Maps (verificación de Alejandro, `docs/verificar_rutas.csv`).**

| Cuadra (servicio) | Claude (m) | Google (m) | Diferencia |
|---|---:|---:|---:|
| 1100200010520045 (secundaria) | 1 586 | 1 500 | +86 m (+5.7 %) |
| 110020001054A026 (mercado o súper) | 1 392 | 1 400 | −8 m (−0.6 %) |
| 1100200270395060 (bachillerato) | 3 153 | 3 100 | +53 m (+1.7 %) |
| 1100200010234051 (tienda) | 148 | 110 | +38 m (+35 %) |
| 1100200010465087 (primaria) | 1 009 | 1 000 | +9 m (+0.9 %) |

- Diferencia absoluta mediana: **1.7 %**. Máxima en distancias de más de 1 km: **5.7 %**. La de 148 m difiere 38 m por el tramo de acceso (de la cuadra a la calle, 22 m en el cálculo). Google redondea a 10 o 100 m. En 4 de 5 rutas el cálculo sale algo más largo, así que la medida no subestima la distancia.
- Son 5 rutas (4 en la ciudad de Acámbaro y 1 en Irámuco): sirven como control de orden de magnitud, no como tasa de error.

**V37 · Verificación remota de servicios (D41).** `verificacion_servicios.csv` (release `datos-crudos`, subido el 2026-10-23) tiene 134 filas, 68 marcadas "revisado". Se unieron todas por `id` con el catálogo (0 sin pareja). 57 están dentro del municipio y 11 en la franja de 10 km.
- **Advertencia: no es una muestra al azar.** Se revisaron todos los bachilleratos y casos priorizados (sin nombre, sin confirmar, raros). Las tasas describen esos casos y **no** la confiabilidad general del catálogo.
- **Total**: 50 "sí", 11 "no" y 7 "no se ve" de 68 = **73.5 %** confirmados (82.0 % sin contar los "no se ve"). Dentro del municipio: 44 de 57 (77.2 %). En la franja: 6 de 11 (54.5 %).

  | Tipo | Revisados | Sí | No | No se ve | % sí | % sí sin "no se ve" |
  |---|---:|---:|---:|---:|---:|---:|
  | Abasto | 15 | 13 | 2 | 0 | 86.7 % | 86.7 % |
  | Bachillerato | 17 | 11 | 4 | 2 | 64.7 % | 73.3 % |
  | Bachillerato no escolarizado | 1 | 0 | 1 | 0 | 0 % | 0 % |
  | Preescolar | 4 | 3 | 0 | 1 | 75.0 % | 100 % |
  | Primaria | 5 | 4 | 1 | 0 | 80.0 % | 80.0 % |
  | Salud de primer nivel | 20 | 17 | 2 | 1 | 85.0 % | 89.5 % |
  | Salud en el CERESO (D38) | 1 | 0 | 1 | 0 | 0 % | 0 % |
  | Secundaria | 5 | 2 | 0 | 3 | 40.0 % | 100 % |

  | Fuente del catálogo | Revisados | Sí | No | No se ve | % sí | % sí sin "no se ve" |
  |---|---:|---:|---:|---:|---:|---:|
  | Solo MG | 21 | 12 | 5 | 4 | 57.1 % | 70.6 % |
  | Solo DENUE | 24 | 19 | 4 | 1 | 79.2 % | 82.6 % |
  | MG + DENUE | 23 | 19 | 2 | 2 | 82.6 % | 90.5 % |

- Por estado del cruce con SEP/CLUES: confirmadas 30 de 39 (76.9 %); no confirmadas 6 de 11 (54.5 %). La única "baja en SEP" revisada (Preparatoria Prof. Leopoldo Salgado) salió "no", lo que concuerda con la SEP. La UMAPS vieja de Irámuco ("baja en CLUES") salió "sí": se ve algo parecido a la nueva a una cuadra.
- `visto_en`: street view 20, no especificado 18, ambos 10, ninguno 6, satélite 4, vacío 10.
- **Los 11 "no" (`dudoso_remoto`)**: dentro del municipio hay 8. Son primaria-0030 (Monte Prieto; en el punto se ve la Telesecundaria 845, a 130 m, y la primaria sí está en la SEP), el mercado "22 de Octubre", la tienda "Abarrotes Juanita", la Preparatoria Prof. Leopoldo Salgado (ya dada de baja, no se usaba), la preparatoria abierta (no se mide), "Centro Médico la Soledad" y la unidad de La Presa de Santa Inés (ambas del anexo, D34), y el consultorio del CERESO (D38). En la franja hay 3, todos bachilleratos (Instituto Vasco de Quiroga en Salvatierra, Preparatoria Lázaro Cárdenas en Zinapécuaro y uno sin nombre).
- **Sensibilidad sin dudosos remotos** (umbral principal, `acceso_sensibilidad.csv`): solo cambian dos cifras. Localidades rurales, primaria: +1 116 personas lejos (de 695 a 1 811), casi todo Monte Prieto (1 068 hab.). Ciudad de Acámbaro, abasto completo: +978 (de 20 267 a 21 245), por el mercado 22 de Octubre. Ninguna otra categoría ni localidad cambia.
- **Sensibilidad solo confirmadas (D28)**, umbral principal: primaria en la ciudad +1 801 (de 17 853 a 19 654), Chupícuaro +403, rural +146 (preescolar), +210 (primaria), +234 (secundaria).

**V38 · Archivos para Alejandro.**
- `docs/zonas_nuevas.kml`: 28 zonas (las 13 posteriores a 2020 y las 15 más grandes de 2010–2020). Cada contorno es la unión de las cuadras nuevas de la zona, de la capa de su propio periodo. Se abrió con GDAL (LIBKML) sin errores. `docs/verificar_zonas_nuevas.csv` tiene ahora la columna `en_kml` (28 sí, 135 no).
- `docs/verificar_campo.csv`: 19 puntos en 5 salidas (agrupados por cercanía a ≤ 10 km de diámetro). Son 12 "no" o "no se ve" del municipio (se quitó el del CERESO, ya resuelto), las 2 UMAPS de Irámuco y 5 "sí" al azar (semilla 2026) para medir el error de la verificación remota.
- `verificacion_zonas.csv` sigue sin estar en el release (404).

## Fase 4b (2026-10-23) — crecimiento urbano y acceso

Todos los resultados son **provisionales**: `verificacion_zonas.csv` sigue sin estar en el release (`01_descargar.py --solo verificacion`, 2026-10-23: solo bajó `verificacion_servicios.csv`).

**V39 · Clasificación de cuadras (`cuadras_antiguedad.csv`).**
- 4 localidades: 1 567 consolidadas, 53 nuevas 2010–2020, 6 posteriores a 2020 y 32 puntos de caserío. Coinciden con `acceso_cuadras` (1 620 + 6 + 32).
- Cuadras nuevas 2010–2020 / posteriores a 2020: Acámbaro 30 / 4, Irámuco 5 / 1, Parácuaro 12 / 0, Chupícuaro 6 / 1. Superficie nueva 2010–2020: 29.3 ha. Población 2020 en cuadras nuevas: 356.
- 0 cuadras en localidades sin cartografía en 2010.
- Chequeo de población: la suma por localidad (56 596 / 6 275 / 4 159 / 2 583) es igual a la de `acceso_resumen_por_localidad.csv`.

**V40 · Comparación por anillos (`crecimiento_acceso_periferia.csv`).**
- En todos los anillos con cuadras nuevas hay consolidadas: la columna `peso_sin_consolidadas_en_su_anillo` es 0 en todas las filas.
- Las 4 localidades juntas, umbral principal, % de población lejos (nuevas / consolidadas del mismo anillo / todas las consolidadas): preescolar 48 / 13 / 10; primaria 43 / 42 / 37; secundaria 54 / 51 / 30; bachillerato público 45 / 41 / 36; salud 38 / 32 / 24; abasto completo 69 / 59 / 39; tienda 6 / 1 / 1.
- El preescolar mantiene el sentido con los tres umbrales. Salud se invierte con el holgado (17 contra 23).
- **Cuidado**: el grupo nuevo tiene 356 personas en total (Irámuco 25, Parácuaro 19). Los porcentajes por localidad de las nuevas son frágiles.

**V41 · GHSL contra el MG.**
- La superficie construida de la ciudad (+1 km) creció 66.6 ha entre 2010 y 2020. Las cuadras nuevas del MG en ese periodo suman 18.3 ha. El GHSL registra construcción dentro de cuadras que ya existían; el MG no la cuenta como crecimiento.
- Superficie construida 2020 de la ciudad (GHSL): 456 ha. Superficie de cuadras del MG 2020: 1 271 ha (las cuadras incluyen patios, huertas y lotes baldíos).
- Celdas sin dato dentro del municipio: 0.

**V42 · Viviendas y "*".**
- 2020, cuadras urbanas: deshabitadas ocultas en 602 de 1 652; uso temporal en 713; habitadas en 51.
- Ocultas por localidad (total publicado − suma visible): deshabitadas 587 / 73 / 74 / 91 y uso temporal 479 / 55 / 61 / 65 (Acámbaro / Irámuco / Parácuaro / Chupícuaro).
- "Viviendas − habitadas" en la ciudad: 25.9 %, contra 26.1 % publicado (deshabitadas + uso temporal).
- 2010: deshabitadas ocultas en 1 339 de 1 478 manzanas urbanas del MG. 127 manzanas del MG 2010 no tienen fila en el censo por manzana: son todas las de Chupícuaro, que en 2010 no tenía tabla por manzana. 28 manzanas 2010 cayeron fuera de toda AGEB 2020 y se asignaron a la más cercana de su localidad.
- AGEB con total oculto: 35 de 110 (2010) y 41 de 126 (2020).
- Se formaron 122 unidades comparables (103 con una sola AGEB 2010 y 4 con dos). Las unidades con dato completo en los dos años cubren el 92 % de las viviendas 2020 de la ciudad.
- Totales por localidad 2010 → 2020 (ITER): la ciudad pierde 1 375 habitantes y gana 2 508 viviendas; deshabitadas 3 178 → 4 606.

**V43 · ITER históricos.** Se probaron dos patrones de URL (`ccpv/{año}/datosabiertos/iter_11_{año}_csv.zip` y `.../iter/iter_11_{año}_csv.zip`) para 1990, 1995, 2000 y 2005. Los 8 devolvieron una página HTML (2 263 bytes), no un zip. No se buscó más: la superficie por habitante solo se calcula para 2010 y 2020.

**V44 · Tipología.** 126 AGEB: 53 consolidada estable (60 143 hab.), 43 consolidada desatendida (7 408), 4 consolidada y vaciándose (1 227; 3 también desatendidas), 11 nueva y bien servida (225), 15 nueva y desatendida (146). Corte de % no habitadas (percentil 75 dentro de la localidad): Acámbaro 31.6, Irámuco 39.1, Parácuaro 44.4, Chupícuaro 51.2.
