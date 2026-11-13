# Contraste con los planes oficiales

Fecha: 2026-11-13 (fase 6). Este documento compara lo que decían dos planes oficiales con lo que muestran los datos de este estudio. **No evalúa a ninguna administración**: habla de diagnósticos que ya existían y de metas que, con el paso del tiempo, no se cumplieron o no se pueden verificar.

Cada cita se verificó en el PDF de forma automática (`src/30_planes.py` → `docs/verificar_citas_planes.csv`: 34 de 34 citas encontradas en la página indicada). Páginas: en el Plan Municipal, la página del PDF coincide con la impresa; en el PROT se cita la **página impresa** (la del PDF es una más).

---

## 1. Fichas

| | Plan Municipal de Desarrollo Acámbaro 2030 | Programa Regional de Ordenamiento Territorial, Subregión 10 (PROT) |
|---|---|---|
| Quién | COPLADEM Acámbaro (Comité de Planeación para el Desarrollo Municipal) | SEDATU e IPLANEG (Instituto de Planeación, Estadística y Geografía de Guanajuato) |
| Cuándo | Administración 2003–2006; usa cifras de 2006 | 2014 (cita datos hasta 2015) |
| Horizonte | 2030 | 2030 (escenarios) |
| Cobertura | Municipio de Acámbaro, dividido en 8 "ejes de desarrollo" o micro regiones ("polos de desarrollo", p. 6) | Subregión 10 "Sierra de los Agustinos": Acámbaro, Coroneo, Jerécuaro y Tarandacuao |
| Archivo | `plan_municipal_desarrollo_2030.pdf` (256 p.), release `datos-crudos` | `prot_subregion10_2014.pdf` (124 p.), release `datos-crudos` |

---

## 2. Lo que decía el plan y lo que muestran los datos

| Tema | Lo que decía el plan | Lo que muestran los datos |
|---|---|---|
| **Población** | El Plan Municipal da 115 121 habitantes en 2006 (p. 18), con fuente "Proyección de Población del CONAPO 2000-2030" (p. 34); no publica la serie hacia 2030. El PROT proyectaba, con datos del CONAPO, que la subregión crecería 3.14 % a 2016, **5.07 % a 2020** y 8.9 % a 2030 respecto a 2010 (p. 59), y daba 112 076 habitantes para Acámbaro y 189 535 para la subregión en 2014 (cuadro 3, p. 38). El propio PROT advertía que las tendencias de migración "no parecen contempladas en esta proyección" (p. 47). | El municipio tenía 110 718 habitantes en 2000, 101 762 en 2005, 109 030 en 2010, 108 697 en 2020 y unos 108 140 en 2025 (EIC; intervalo de 90 %: 100 654–115 626). **Nunca llegó a 112 000.** La subregión pasó de 183 194 (2010) a 180 601 (2020): **−1.4 %, contra +5.07 % proyectado**, unas 11 900 personas menos de lo esperado. Figura: `docs/figuras/fase6_proyeccion.png`. |
| **La ciudad** | El PROT esperaba que la ciudad de Acámbaro tuviera **51 613 habitantes en 2030** (estimación CONAPO 2010, p. 42), es decir, que perdiera población. | La cifra es comparable: el PROT da a la ciudad el 31.64 % de los 183 194 habitantes de 2010 (p. 30), unos 57 960, igual a la localidad 0001 del censo 2010 (57 972). La ciudad bajó a **56 597 en 2020** (−2.4 %) y la EIC 2025 da 56 771 (sin cambio distinguible de cero). Para llegar a 51 613 en 2030 tendría que perder casi 5 000 personas en diez años, más del triple que en 2010–2020. **La ciudad quedó por encima de lo proyectado, mientras el municipio y la subregión quedaron por debajo**: se concentró población en la ciudad y se perdió en el resto. |
| **Vivienda** | El Plan Municipal se proponía "disminuir el déficit habitacional" (p. 214), adquirir reservas de terreno para vivienda nueva (p. 215) y "mantener estricto control de los fraccionamientos" (p. 216). | Entre 2010 y 2020 el municipio ganó **6 348 viviendas** (de 39 391 a 45 739, +16 %) sin ganar población. Las **viviendas deshabitadas** pasaron de 7 492 (19 %) a **11 130 (24 %)**. En la ciudad, de 3 178 a 4 606. El problema de hoy no es la falta de casas sino las casas vacías y la ciudad que ocupa más suelo con menos gente (superficie construida +17 % según el GHSL, población −2.4 %). |
| **Migración** | El Plan Municipal dice que Acámbaro es "uno de los tres [municipios] en el estado, considerado como de muy alta migración" (p. 18) y que se cerraban turnos escolares por "emigración y la baja población que existe en edad escolar" (p. 31). El PROT: "El 20% de las viviendas de la Subregión reciben remesas" (p. 31, con datos de IPLANEG 2014). | El diagnóstico sigue vigente. En 2025, **el 14.9 % de los hogares de Acámbaro recibe dinero de alguien que vive en otro país** (EIC 2025; intervalo de 90 %: 13.8–16.1 %), contra 8.6 % en Guanajuato. No es la misma medida que la del PROT (hogares contra viviendas; municipio contra subregión), así que no se puede decir si subió o bajó. |
| **Irámuco** | El Plan Municipal: "Irámuco se constituirá como el principal concentrador de población micro regional y el segundo en el ámbito municipal" (p. 61). El PROT, al describir la situación de 2014 en su escenario tendencial: en Irámuco "es una interacción con Michoacán la que ha propiciado que **actualmente haya un fuerte crecimiento poblacional y de desarrollo habitacional** en la zona" (p. 59). Es una descripción de 2014, no una proyección. | Irámuco sí es la segunda localidad del municipio. Pero **antes de 2014 venía perdiendo población**: 6 232 (2000), 6 141 (2005), 5 954 (2010). Entre 2010 y 2020: **población +5 % (5 954 → 6 275), viviendas +27 % (1 839 → 2 336) y viviendas deshabitadas casi el doble (356 → 658; de 19 % a 28 %)**. Hubo crecimiento habitacional, pero una parte grande quedó vacía; la población apenas volvió a su nivel de 2000. La EIC 2025 no publica localidades de este tamaño. Hoy Irámuco **no tiene mercado ni supermercado registrado** (el más cercano, a 13–18 km en Santa Ana Maya) y el 80 % de su gente vive lejos de una primaria. Tabla: `data/processed/iramuco_serie.csv`. |
| **Parácuaro** | "En esta zona se cuenta con una secundaria técnica localizada en la carretera Parácuaro- El Jaral, y ésta también presta servicio a otras localidades" (Plan Municipal, p. 64; en p. 31 la llama "secundaria técnica agropecuaria"). | El diagnóstico se mantiene: **no hay secundaria dentro de Parácuaro** (D39). La que lo atiende, la Secundaria Técnica 24 (11DST0024Y), queda fuera del pueblo; la más cercana al centro es la Telesecundaria 847 de La Concepción, a unos 5.6 km por camino estimado. **Hay una diferencia de ubicación**: el Plan la pone en la carretera Parácuaro–El Jaral, y D39 en la carretera Acámbaro–Parácuaro km 9. No se asume cuál es correcta: puede ser otra escuela o una reubicación. Queda como punto de verificación en campo (`docs/verificar_campo_fase6.csv`). |
| **Equipamiento educativo** | El cuadro 3 del PROT (p. 38) calcula para **la subregión en total** un superávit de aulas: preescolar +279, primaria +1 048, bachillerato +56 (secundaria sin cálculo). | Un superávit sumado para toda la subregión no dice dónde están las aulas. Por distancia, en la ciudad 32 % de la gente vive lejos de una primaria y 43 % de un bachillerato público; en Irámuco, 80 % lejos de una primaria; Parácuaro no tiene secundaria. Sobrar aulas en total y faltar escuelas cerca pueden ser ciertos a la vez. |
| **Crecimiento** | El PROT: "En Acámbaro, el crecimiento urbano ocurre en la periferia de la cabecera municipal y en otras localidades como Irámuco" (p. 59). | Se confirma en la forma: la ciudad ganó 2 508 viviendas y 30 cuadras nuevas en la orilla entre 2010 y 2020, y su superficie construida creció 17 %. Pero lo hizo **perdiendo 1 375 habitantes**. La mayoría de las "cuadras nuevas" del resto del municipio son pueblos que ya existían y que el INEGI empezó a dibujar (D54). |
| **Ordenamiento** | "Elaborar y publicar el plan de ordenamiento territorial en un plazo no mayor a 6 meses a partir de la publicación de este plan de desarrollo" (p. 241), y uno para cada polo de desarrollo (p. 241 y 255). | No se localizó ningún plan municipal de ordenamiento publicado (no se buscó a fondo: queda **pendiente para Alejandro**). Lo que muestran los datos es lo que un plan así buscaba evitar: vivienda nueva sin gente nueva, casas vacías en todos los anillos de la ciudad y crecimiento disperso en la orilla. |

---

## 3. Metas por polo de desarrollo (Plan Municipal, p. 254–255)

El plan se fija como meta que **cada polo de desarrollo rural** tenga "infraestructura educativa desde el nivel pre-escolar hasta el nivel medio superior al 100%" (p. 254), "plazas públicas para el comercio y abasto" y "centros comunitarios de salud" (p. 255). Polos = los 8 ejes de desarrollo del plan; sede = la localidad que da nombre al eje (D60). Se evalúan los 7 rurales; la ciudad aparece como referencia. "Tiene" = hay al menos una sede del catálogo dentro de la localidad (D59). Salud = salud abierta (D58). Distancia al más cercano (línea recta × 1.33 desde el centro de la localidad) cuando no tiene.

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

- **Escuelas y salud**: 5 de los 7 polos tienen todo. Faltan la secundaria en Parácuaro y el bachillerato y la unidad de salud en Inchamácuaro.
- **Abasto**: solo Parácuaro y Chupícuaro tienen mercado registrado. En los otros 5 no se puede afirmar que falte, porque ningún registro capta tianguis; por eso quedan "no verificable" y no "no".
- **Solo Chupícuaro cumple la meta completa** con lo que registran las fuentes.
- Bachillerato cuenta todas las escuelas de media superior, incluidos videobachilleratos (la preparatoria abierta no cuenta, D23).
- Tabla completa con claves de cada sede: `data/processed/polos_desarrollo.csv`.

### Localidades de 2 500 habitantes o más (norma SEDESOL 1999: un centro de salud rural por localidad de 2 500 a 10 000 hab.)

| Localidad | Pob. 2020 | Centro de salud abierto dentro | Secundaria o telesecundaria dentro |
|---|---:|---|---|
| Acámbaro (ciudad; más de 10 000 hab.) | 56 597 | sí (4) | sí (10) |
| Irámuco | 6 275 | sí | sí |
| Parácuaro | 4 159 | sí | **no**: la más cercana, a 5.6 km desde el centro (mediana por persona, 5.4 km) |
| Chupícuaro (Nuevo Chupícuaro) | 2 583 | sí | sí |

Las 3 localidades de 2 500 a 10 000 habitantes cumplen la norma del centro de salud. Tabla: `data/processed/localidades_2500.csv`.

---

## 4. Lo que no se pudo contrastar

- **Serie CONAPO del Plan Municipal**: el plan cita la proyección CONAPO 2000–2030 como fuente (p. 34), pero solo publica la cifra de 2006. Las imágenes del PDF son la marca de agua, no gráficas.
- **Gráfica del PROT (2.2.2.3, p. 47)**: el texto describe una tendencia "exponencial", pero la página no trae gráfica ni cifras. Las cifras proyectadas del PROT que se usan son las de p. 38 (2014), p. 42 (ciudad 2030) y p. 59 (porcentajes sobre 2010).
- **Coherencia interna del PROT**: su cifra de 2014 para la subregión (189 535, +3.5 % sobre 2010) es mayor que la que da para 2016 (+3.14 %). Se reportan las dos como aparecen.
- **2005** es el II Conteo de Población y Vivienda, que dio cifras más bajas que los censos de 2000 y 2010 en toda la subregión. La cifra del Plan Municipal para 2006 (115 121) es 13 % mayor que la del Conteo 2005 (101 762).

## 5. Pendiente para Alejandro

1. Confirmar si existe un **plan municipal de desarrollo más reciente** o un **PMDUOET** (Programa Municipal de Desarrollo Urbano y Ordenamiento Ecológico Territorial) publicado para Acámbaro. Si existe, conviene contrastarlo también: este documento compara con planes de 2003–2006 y de 2014.
2. Verificar en campo la ubicación de la secundaria técnica de Parácuaro (`docs/verificar_campo_fase6.csv`).
