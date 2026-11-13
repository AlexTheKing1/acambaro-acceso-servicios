# Contraste con los planes oficiales

Fecha: 2026-11-13 (fase 6, ampliada a cuatro documentos). Este documento compara lo que decían cuatro planes oficiales, de 2006 a 2025, con lo que muestran los datos de este estudio. **No evalúa a ninguna administración**: habla de diagnósticos que ya existían y de metas que, con el tiempo, no se cumplieron o no se pueden verificar.

**El hilo**: de 2006 a 2025, los cuatro documentos repiten los mismos diagnósticos (migración, localidades con poco equipamiento, Irámuco y Parácuaro como casos aparte) y la misma promesa de un instrumento de ordenamiento territorial. Ninguno mide el equipamiento por distancia ni menciona la vivienda deshabitada.

**Cómo se verificaron las citas**: todas de forma automática (`src/30_planes.py` → `docs/verificar_citas_planes.csv`): **64 de 64 citas encontradas en la página indicada**. Se cita siempre la **página impresa**. En el Plan 2006 coincide con la del PDF; en el PROT, la del PDF es una más. Los dos documentos de 2015 y 2025 son escaneos: se verificaron sobre el texto OCR que subió Alejandro, con la página del encabezado del Periódico Oficial, y las dudosas se revisaron en la imagen.

Nombres cortos: **Plan 2006** = Plan Municipal de Desarrollo Acámbaro 2030; **PROT 2014**; **Plan 2040** = Plan Municipal de Desarrollo 2040 (2015); **Programa 2025** = Programa de Gobierno Municipal 2024–2027.

---

## 1. Fichas

| | Plan 2006 | PROT 2014 | Plan 2040 (2015) | Programa 2025 |
|---|---|---|---|---|
| Nombre | Plan Municipal de Desarrollo Acámbaro 2030 | Programa Regional de Ordenamiento Territorial de la Subregión 10 | Plan Municipal de Desarrollo 2040 de Acámbaro | Programa de Gobierno Municipal 2024–2027 |
| Quién | COPLADEM Acámbaro (Comité de Planeación para el Desarrollo Municipal) | SEDATU e IPLANEG (Instituto de Planeación, Estadística y Geografía de Guanajuato) | Ayuntamiento de Acámbaro | Ayuntamiento de Acámbaro |
| Cuándo | Administración 2003–2006; usa cifras de 2006 | 2014 (cita datos hasta 2015) | Aprobado el 25/03/2015; Periódico Oficial núm. 118, 2.ª parte, 24/07/2015, p. 106–186 | Aprobado el 23/07/2025; Periódico Oficial núm. 173, 2.ª parte, 29/08/2025, p. 18–97 |
| Horizonte | 2030 | 2030 (escenarios) | 2040 (dice "Plan Municipal 2012-2040") | 2024–2027 |
| Cobertura | Municipio, en 8 "ejes de desarrollo" o micro regiones ("polos de desarrollo", p. 6), con metas por polo | Subregión 10: Acámbaro, Coroneo, Jerécuaro y Tarandacuao | Municipio; objetivos generales, **sin polos ni metas por localidad, sin proyecciones de población** | Municipio; diagnóstico y acciones por dependencia. Menciona "11 polos de desarrollo rural" (p. 55), sin enumerarlos ni fijarles metas |
| Archivo (release `datos-crudos`) | `plan_municipal_desarrollo_2030.pdf` | `prot_subregion10_2014.pdf` | `plan_municipal_desarrollo_2040.pdf` (escaneo) + `_ocr.txt` | `programa_gobierno_2024_2027.pdf` (escaneo; página impresa = página del PDF + 15) + `_ocr.txt` |

---

## 2. Síntesis por tema

| Tema | Plan 2006 | PROT 2014 | Plan 2040 (2015) | Programa 2025 | Lo que muestran los datos |
|---|---|---|---|---|---|
| **Irámuco y Parácuaro** | Irámuco "se constituirá como el principal concentrador de población micro regional" (p. 61). Parácuaro: secundaria técnica "en la carretera Parácuaro- El Jaral" (p. 64) | Irámuco: "actualmente haya un fuerte crecimiento poblacional y de desarrollo habitacional" (p. 59, situación de 2014) | No los trata por separado | "presentan problemáticas particulares como la baja cobertura de servicios públicos y equipamiento, debido a condiciones de dispersión y baja accesibilidad" (p. 55) | Irámuco: sin mercado ni supermercado registrado, 80 % lejos de una primaria; población +5 %, viviendas +27 %, deshabitadas casi el doble en 2010–2020. Parácuaro: sin secundaria dentro |
| **Ordenamiento** | Publicar el plan de ordenamiento "en un plazo no mayor a 6 meses" (p. 241) y uno por polo (p. 255) | Es en sí un programa regional de ordenamiento | "Contar con un instrumento técnico normativo en materia ambiental y territorial" (p. 172); Programa de Desarrollo Urbano y Ordenamiento Ecológico Territorial e Instituto Municipal de Planeación como "Proyecto Nuevo" (p. 166 y 174); observatorio ciudadano (p. 176) | El PMDUOET "se encuentra en elaboración por un grupo de especialistas" (p. 60); acción 1.3.1.1 "Concluir" el PMDUOET y 1.3.1.2 actualizar el Plan 2040 (p. 68) | 19 años después del primer compromiso, el instrumento municipal sigue sin publicarse. Mientras tanto: vivienda nueva sin gente nueva, casas vacías en todos los anillos de la ciudad, crecimiento disperso en la orilla |
| **Cómo se mide el equipamiento** | Conteo de escuelas y unidades por micro región (p. 60, 64) | Unidades básicas de servicio de toda la subregión: **superávit** de aulas (cuadro 3, p. 38) | Escuelas por habitante del municipio: **déficit**, "menor número de [...] escuelas en primarias, en secundaria y en bachillerato por habitante" (p. 158; también p. 143) | Conteo de unidades de salud del municipio (p. 45) | Ninguno mide por distancia ni ubicación. Medido así: en la ciudad 32 % lejos de una primaria y 43 % de un bachillerato público; Irámuco 80 % lejos de una primaria; Parácuaro sin secundaria |
| **Vivienda deshabitada** | Habla de "déficit habitacional" (p. 214) y reservas de suelo (p. 215) | No la menciona | No la menciona | Cuenta 30 171 viviendas habitadas (p. 49); no menciona las deshabitadas | 11 130 viviendas deshabitadas en 2020 (24 % del total), +3 638 desde 2010 |

---

## 3. Lo que decían los planes y lo que muestran los datos

| Tema | Lo que decían los planes | Lo que muestran los datos |
|---|---|---|
| **Población** | Plan 2006: 115 121 habitantes en 2006 (p. 18), con fuente "Proyección de Población del CONAPO 2000-2030" (p. 34); no publica la serie hacia 2030. PROT 2014: la subregión crecería 3.14 % a 2016, **5.07 % a 2020** y 8.9 % a 2030 respecto a 2010 (p. 59); 112 076 habitantes para Acámbaro y 189 535 para la subregión en 2014 (cuadro 3, p. 38); advertía que las tendencias de migración "no parecen contempladas en esta proyección" (p. 47). Plan 2040: sin proyecciones. Programa 2025: 109 030 (2010), 112 125 (Intercensal 2015) y 108 697 (2020), y reconoce que "la población tuvo paulatina disminución" (p. 41–42). | El municipio tenía 110 718 habitantes en 2000, 101 762 en 2005, 109 030 en 2010, 108 697 en 2020 y unos 108 140 en 2025 (EIC; intervalo de 90 %: 100 654–115 626). **Nunca llegó a 112 000 en un censo.** La subregión pasó de 183 194 (2010) a 180 601 (2020): **−1.4 %, contra +5.07 % proyectado**, unas 11 900 personas menos de lo esperado. El Programa 2025 es el primero de los cuatro documentos que reconoce la disminución. Figura: `docs/figuras/fase6_proyeccion.png`. |
| **La ciudad** | PROT 2014: la ciudad de Acámbaro tendría **51 613 habitantes en 2030** (estimación CONAPO 2010, p. 42), es decir, perdería población. | La cifra es comparable: el PROT da a la ciudad el 31.64 % de los 183 194 habitantes de 2010 (p. 30), unos 57 960, igual a la localidad 0001 del censo 2010 (57 972). La ciudad bajó a **56 597 en 2020** (−2.4 %), y la EIC 2025 da 56 771, sin cambio distinguible de cero. Para llegar a 51 613 en 2030 tendría que perder casi 5 000 personas en diez años, más del triple que en 2010–2020. **La ciudad quedó por encima de lo proyectado, mientras el municipio y la subregión quedaron por debajo**: se concentró población en la ciudad y se perdió en el resto. |
| **Salud** | Plan 2006: en 2006, 19.01 % con seguridad social (p. 34). Plan 2040: 23 unidades en 2010, "1 IMSS, 1 ISSTE y 21 de SSG" (p. 127); 24.6 % con carencia por acceso a servicios de salud (p. 138); objetivo: "Garantizar el acceso a servicios de salud en localidades rurales y urbanas" (p. 162). Programa 2025: 20.72 % sin afiliación (p. 44); 26 unidades, 1 IMSS, 1 ISSSTE y "24 unidades a la Secretaría de Salud del Estado de Guanajuato" (p. 45). | Ningún documento separa las unidades por a quién atienden ni mide la distancia. **En la ciudad, 7 039 de las 11 479 personas sin afiliación (61 %) viven lejos de una unidad que las atienda** (salud abierta, umbral principal de 1 330 m a pie; 75 / 61 / 30 % con los tres umbrales). La ciudad tiene 6 unidades públicas, pero 2 (el Hospital General de Subzona 13 del IMSS y la clínica del ISSSTE) solo atienden a sus derechohabientes. Como comparación: con las 4 abiertas, 58 % de toda la población vive lejos; con las 6 públicas, 22 %. La diferencia es real solo para quien no tiene afiliación, porque los afiliados al IMSS o al ISSSTE sí pueden usar esas clínicas. Parte de la población sin afiliación se atiende en **consultorios de farmacia**: no se cuentan como salud pública (son privados) y no están en esta medida. En lo rural y en Irámuco, Parácuaro y Chupícuaro, separar las unidades no cambia nada. |
| **Vivienda** | Plan 2006: "disminuir el déficit habitacional" (p. 214), adquirir reservas de terreno para vivienda nueva (p. 215) y "mantener estricto control de los fraccionamientos" (p. 216). Plan 2040 y Programa 2025: no mencionan la vivienda deshabitada; el Programa cuenta "30,171 viviendas habitadas" (p. 49). | Entre 2010 y 2020 el municipio ganó **6 348 viviendas** (de 39 391 a 45 739, +16 %) sin ganar población. Las **viviendas deshabitadas** pasaron de 7 492 (19 %) a **11 130 (24 %)**; en la ciudad, de 3 178 a 4 606. El problema de hoy no es la falta de casas, sino las casas vacías y una ciudad que ocupa más suelo con menos gente (superficie construida +17 % según el GHSL, población −2.4 %). |
| **Migración** | Plan 2006: "uno de los tres [municipios] en el estado, considerado como de muy alta migración" (p. 18); turnos escolares cerrados por "emigración y la baja población que existe en edad escolar" (p. 31). PROT 2014: "El 20% de las viviendas de la Subregión reciben remesas" (p. 31). Plan 2040: intensidad migratoria "clasificado como alto" (p. 138) y la migración entre las principales amenazas (p. 142). Programa 2025: remesas por "un total de 68 millones de dólares" en 2022 (p. 43). | El diagnóstico sigue vigente en los cuatro documentos. En 2025, **el 14.9 % de los hogares de Acámbaro recibe dinero de alguien que vive en otro país** (EIC 2025; intervalo de 90 %: 13.8–16.1 %), contra 8.6 % en Guanajuato. Las medidas no son iguales (hogares contra viviendas, municipio contra subregión, dólares), así que no se puede decir si subió o bajó. |
| **Irámuco** | Plan 2006: "Irámuco se constituirá como el principal concentrador de población micro regional y el segundo en el ámbito municipal" (p. 61). PROT 2014, al describir la situación de 2014 en su escenario tendencial: en Irámuco "es una interacción con Michoacán la que ha propiciado que **actualmente haya un fuerte crecimiento poblacional y de desarrollo habitacional** en la zona" (p. 59). Es una descripción de 2014, no una proyección. Programa 2025: "baja cobertura de servicios públicos y equipamiento" (p. 55). | Irámuco sí es la segunda localidad del municipio. Pero **antes de 2014 venía perdiendo población**: 6 232 (2000), 6 141 (2005), 5 954 (2010). Entre 2010 y 2020: **población +5 % (5 954 → 6 275), viviendas +27 % (1 839 → 2 336) y deshabitadas casi el doble (356 → 658; de 19 % a 28 %)**. Hubo crecimiento habitacional, pero buena parte quedó vacía, y la población apenas volvió a su nivel de 2000. Hoy **no tiene mercado ni supermercado registrado** (el más cercano, a 13–18 km en Santa Ana Maya) y el 80 % de su gente vive lejos de una primaria. Errata del Programa 2025: en p. 55 dice que Irámuco tiene "6,725" habitantes (revisado en la imagen); en p. 43 el mismo documento da 6 275, igual que el censo. Tabla: `data/processed/iramuco_serie.csv`. |
| **Parácuaro** | Plan 2006: "En esta zona se cuenta con una secundaria técnica localizada en la carretera Parácuaro- El Jaral, y ésta también presta servicio a otras localidades" (p. 64; en p. 31 la llama "secundaria técnica agropecuaria"). Programa 2025: la misma "baja cobertura de servicios públicos y equipamiento" que Irámuco (p. 55). | El diagnóstico se mantiene: **no hay secundaria dentro de Parácuaro** (D39). La que lo atiende, la Secundaria Técnica 24 (11DST0024Y), queda fuera del pueblo; la más cercana al centro es la Telesecundaria 847 de La Concepción, a unos 5.6 km por camino estimado. **Hay una diferencia de ubicación**: el Plan 2006 pone la secundaria técnica en la carretera Parácuaro–El Jaral, y D39 en la carretera Acámbaro–Parácuaro km 9. No se asume cuál es correcta: puede ser otra escuela o una reubicación. Queda como punto de verificación en campo (`docs/verificar_campo_fase6.csv`). |
| **Equipamiento educativo** | PROT 2014, cuadro 3 (p. 38): **superávit** de aulas en la subregión en total (preescolar +279, primaria +1 048, bachillerato +56; secundaria sin cálculo). Plan 2040: **déficit**, "menor número de bibliotecas públicas, escuelas en primarias, en secundaria y en bachillerato por habitante de todo el estado" (p. 158) y "Proporción de equipamiento educativo [...] por número de habitantes inferior a la proporción estatal" (p. 143); objetivo: "Impulsar el equipamiento urbano de educación, salud, vialidad y deporte acorde a las necesidades de todo el municipio" (p. 169). | Uno ve superávit y otro déficit porque **los dos miden en total, sin ubicación**: el PROT suma aulas contra la población de la subregión; el Plan 2040 compara escuelas por habitante con el estado. Ninguno dice dónde faltan. Por distancia: en la ciudad 32 % vive lejos de una primaria y 43 % de un bachillerato público; en Irámuco, 80 % lejos de una primaria; Parácuaro no tiene secundaria. Sobrar aulas en total y faltar escuelas cerca pueden ser ciertos a la vez. |
| **Crecimiento** | PROT 2014: "En Acámbaro, el crecimiento urbano ocurre en la periferia de la cabecera municipal y en otras localidades como Irámuco" (p. 59). | Se confirma en la forma: la ciudad ganó 2 508 viviendas y 30 cuadras nuevas en la orilla entre 2010 y 2020, y su superficie construida creció 17 %. Pero lo hizo **perdiendo 1 375 habitantes**. La mayoría de las "cuadras nuevas" del resto del municipio son pueblos que ya existían y que el INEGI empezó a dibujar (D54). |
| **Ordenamiento** | Plan 2006: publicar el plan de ordenamiento territorial "en un plazo no mayor a 6 meses a partir de la publicación de este plan" (p. 241). Plan 2040: "Contar con un instrumento técnico normativo en materia ambiental y territorial dentro del Municipio" (p. 172), el "Programa de Desarrollo Urbano y Ordenamiento Ecológico Territorial del Municipio" y la "Creación de Instituto Municipal de Planeación" como proyectos nuevos (p. 174; Instituto de Planeación también en p. 166), y "la creación de un observatorio ciudadano local" para dar seguimiento al plan (p. 176). Programa 2025: el PMDUOET "se encuentra en elaboración por un grupo de especialistas" (p. 60); acciones 1.3.1.1 "Concluir el Programa Municipal de Desarrollo Urbano y Ordenamiento ecológico Territorial" y 1.3.1.2 "Actualizar el Plan de Desarrollo Municipal visión 2040" (p. 68). | La misma promesa aparece en 2006, 2015 y 2025. Dato **no verificado** (no se afirma): el PMDUOET podría estar en revisión del IPLANEG. Lo que muestran los datos es lo que un instrumento así busca evitar: vivienda nueva sin gente nueva, casas vacías y crecimiento disperso en la orilla. |
| **Acciones en las localidades (Programa 2025)** | En salud, campañas en las comunidades "llevando la Unidad médica" del DIF municipal (p. 73); en abasto, un "proyecto integral de los 4 mercados" municipales de la ciudad (p. 83). | Se revisó todo el apartado de estrategias y acciones (p. 61–89). Hay obras de agua, canchas, calles, panteones (Irámuco, Chamácuaro, Chupícuaro, Desmontes), electrificación rural, mercados de la ciudad y espacios del DIF. **No hay acciones para construir unidades de salud, escuelas o mercados en las localidades.** Las carencias que este estudio encuentra (secundaria en Parácuaro; mercado en Irámuco; bachillerato y salud en Inchamácuaro) no tienen una acción que las atienda. La educación y la salud son sobre todo competencia estatal y federal (D18); el mercado es municipal. |

---

## 4. Metas por polo de desarrollo (Plan 2006, p. 254–255)

La evaluación por polos usa el **Plan 2006** porque es el único que define los polos con su sede y les fija metas. El Plan 2040 abandonó ese enfoque: no tiene polos, metas por localidad ni proyecciones. El Programa 2025 dice que "el municipio cuenta con 11 polos de desarrollo rural" (p. 55), una clasificación de las localidades por "ubicación, accesibilidad, vocación natural y productiva", pero no los enumera ni les fija metas de servicios. No se pueden evaluar.

El Plan 2006 se fija como meta que **cada polo de desarrollo rural** tenga "infraestructura educativa desde el nivel pre-escolar hasta el nivel medio superior al 100%" (p. 254), "plazas públicas para el comercio y abasto" y "centros comunitarios de salud" (p. 255).
- Polos = los 8 ejes de desarrollo del plan; sede = la localidad que da nombre al eje (D60).
- Se evalúan los 7 rurales; la ciudad aparece como referencia.
- "Tiene" = hay al menos una sede del catálogo dentro de la localidad (D59). Salud = salud abierta (D58).
- Si no tiene, se da la distancia al más cercano (línea recta × 1.33 desde el centro de la localidad).

| Polo (sede) | Pob. 2020 | Preescolar | Primaria | Secundaria | Bachillerato | Salud abierta | Mercado o tianguis | Cumple la meta |
|---|---:|---|---|---|---|---|---|---|
| Irámuco | 6 275 | sí | sí | sí | sí | sí | sin mercado registrado (15.2 km); tianguis no verificable | **no verificable** |
| Parácuaro | 4 159 | sí | sí | **no** (5.6 km) | sí | sí | sí | **no** |
| Chupícuaro (Nuevo Chupícuaro) | 2 583 | sí | sí | sí | sí | sí | sí | **sí** |
| San Mateo Tócuaro | 1 685 | sí | sí | sí | sí | sí | sin mercado registrado (5.9 km) | **no verificable** |
| Chamácuaro | 1 197 | sí | sí | sí | sí | sí | sin mercado registrado (10.9 km) | **no verificable** |
| Inchamácuaro (Chamacuarillo) | 641 | sí | sí | sí | **no** (3.3 km) | **no** (3.7 km) | sin mercado registrado (13.2 km) | **no** |
| Arroyo de la Luna | 469 | sí | sí | sí | sí | sí | sin mercado registrado (10.9 km) | **no verificable** |
| *Acámbaro (referencia)* | 56 597 | sí | sí | sí | sí | sí | sí | — |

- **Escuelas y salud**: 5 de los 7 polos tienen todo. Faltan la secundaria en Parácuaro, y el bachillerato y la unidad de salud en Inchamácuaro.
- **Abasto**: solo Parácuaro y Chupícuaro tienen mercado registrado. En los otros 5 no se puede afirmar que falte, porque ningún registro capta tianguis; por eso quedan "no verificable" y no "no".
- **Solo Chupícuaro cumple la meta completa** con lo que registran las fuentes.
- El bachillerato cuenta todas las escuelas de media superior, incluidos los videobachilleratos (la preparatoria abierta no cuenta, D23).
- Tabla completa, con las claves de cada sede: `data/processed/polos_desarrollo.csv`.

### Localidades de 2 500 habitantes o más (norma SEDESOL 1999: un centro de salud rural por localidad de 2 500 a 10 000 hab.)

| Localidad | Pob. 2020 | Centro de salud abierto dentro | Secundaria o telesecundaria dentro |
|---|---:|---|---|
| Acámbaro (ciudad; más de 10 000 hab.) | 56 597 | sí (4) | sí (10) |
| Irámuco | 6 275 | sí | sí |
| Parácuaro | 4 159 | sí | **no**: la más cercana, a 5.6 km desde el centro (mediana por persona, 5.4 km) |
| Chupícuaro (Nuevo Chupícuaro) | 2 583 | sí | sí |

Las 3 localidades de 2 500 a 10 000 habitantes cumplen la norma del centro de salud. Tabla: `data/processed/localidades_2500.csv`.

---

## 5. Lo que no se pudo contrastar o no cuadra

- **Serie CONAPO del Plan 2006**: el plan cita la proyección CONAPO 2000–2030 como fuente (p. 34), pero solo publica la cifra de 2006. Las imágenes del PDF son la marca de agua, no gráficas.
- **Gráfica del PROT (2.2.2.3, p. 47)**: el texto describe una tendencia "exponencial", pero la página no trae gráfica ni cifras. Se usan las cifras proyectadas de p. 38 (2014), p. 42 (ciudad 2030) y p. 59 (porcentajes sobre 2010).
- **Coherencia interna del PROT**: su cifra de 2014 para la subregión (189 535, +3.5 % sobre 2010) es mayor que la que da para 2016 (+3.14 %). Se reportan las dos como aparecen.
- **2005** es el II Conteo de Población y Vivienda, que dio cifras más bajas que los censos de 2000 y 2010 en toda la subregión. La cifra del Plan 2006 para 2006 (115 121) es 13 % mayor que la del Conteo 2005 (101 762).
- **Plan 2040, unidades de salud**: dice "23 unidades [...] 1 IMSS, 1 ISSTE y 21 de SSG" y luego divide las de la SSG en 1 hospital general, 1 unidad móvil, 1 centro de salud urbano y 21 rurales, que suman 24 (p. 127). Se cita como aparece.
- **Programa 2025, polos**: atribuye su imagen de polos al Plan 2040 (p. 55), pero el texto del Plan 2040 no menciona polos. Su mapa 4 (p. 175) no tiene leyenda legible en el escaneo.

## 6. Pendientes para Alejandro

1. **Resuelto**: el plan municipal más reciente es el Plan 2040 (2015), y el Programa 2025 dice que el PMDUOET está en elaboración. Queda como dato no verificado que podría estar en revisión del IPLANEG.
2. Verificar en campo la ubicación de la secundaria técnica de Parácuaro y que las 4 unidades de salud abierta de la ciudad funcionen y atiendan a cualquier persona (`docs/verificar_campo_fase6.csv`).
