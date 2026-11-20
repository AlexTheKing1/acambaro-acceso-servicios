# Resumen final del análisis

**"¿Quién está lejos hoy? Acceso a servicios y vaciamiento urbano en Acámbaro"** (título de trabajo, D51)

Fecha: 2026-11-20, actualizado en la fase 8 con la revisión final independiente (`docs/revision_final.md`). Este documento junta las cifras definitivas y es la base para redactar el sitio y el PDF. El detalle está en `docs/resumen_fase4.md` (acceso), `docs/resumen_fase4b.md` (crecimiento y vaciamiento), `docs/metodo.md` (método, normas y límites), `docs/contraste_planes.md` (planes oficiales), `docs/validacion.md` (V1–V63) y `docs/decisiones.md` (D01–D69). Lo que cambió en la fase 8 está en la sección 9.

**Cómo leer las cifras**
- La población es la del **Censo 2020**, la más reciente por cuadra. No habrá otra hasta 2030. Los servicios son los vigentes en 2026. Es decir, se mide **quién vive lejos hoy de los servicios de hoy, con la gente de 2020**.
- "Lejos" = más allá del **umbral principal** (D33). En la ciudad se mide a pie por las calles. En lo rural, con línea recta × 1.33, porque no se pudo bajar la red de caminos. Las cifras rurales que dependen de ese factor se dan como rango (factor de 1.0 a 1.5, `sensibilidad_factor_rural.csv`).
- Todo es **descriptivo**. Que dos cosas vayan juntas no dice que una cause la otra.
- Confiabilidad: **firme** = se sostiene con los tres umbrales o con todas las variantes probadas; **moderada** = depende de un criterio razonable o de pocos casos; **frágil** = cambia con el criterio o descansa en muy pocas personas.
- Cuando una cifra es una estimación por AGEB (D10), se da también el **piso seguro**: lo que se cuenta cuadra por cuadra con los datos visibles.

---

## Los seis hallazgos

1. **Salud.** En la ciudad de Acámbaro, unas **20 100 de las 34 900 personas que dependen de las unidades de salud abiertas a toda la población** (58 %; al menos 19 879) viven a más de 1.3 km a pie de una de las cuatro unidades que atienden a cualquier persona. Ese grupo son las personas sin ninguna afiliación y las afiliadas al INSABI / Seguro Popular o al IMSS-Bienestar, según la clasificación del Censo 2020: no pueden usar las clínicas del IMSS ni del ISSSTE. Entre ellas, **7 039 personas sin ninguna afiliación** (61 %; al menos 6 908). Con los tres umbrales: 72 / 58 / 27 %. **Firme en el sentido.**
2. **Localidades.** De las cuatro localidades urbanas, **Irámuco es la peor servida**: 8 de cada 10 habitantes viven a más de 670 m a pie de una primaria (88 / 80 / 56 %) y no hay mercado ni supermercado registrado (puede existir un tianguis que ninguna fuente captura). **Parácuaro no tiene secundaria dentro del pueblo.** Las dos más cercanas, la Secundaria Técnica 24 (junto a Jaral del Refugio) y la Telesecundaria 847 de La Concepción, están a unos 4.3 km en línea recta. La ST 24 está a unos 4.9 km por carretera (verificado en Google Maps). De los 7 polos rurales del plan de 2006, **Chupícuaro tiene todo lo que el plan pedía; a Parácuaro y a Inchamácuaro les falta algo, y en los otros 4 no se puede saber** porque no hay registro de tianguis. **Firme con matiz.**
3. **Ciudad.** Una de cada tres personas de la ciudad (**32 %**, 17 853) vive a más de 670 m a pie de una primaria; contando solo primarias públicas, **38 %** (21 460). Con los tres umbrales: 55 / 32 / 10 % (públicas, 62 / 38 / 11 %). Entre ellas hay unas 1 700 niñas y niños de 6 a 11 años (al menos 1 583). Indicio, no causa: dentro de la ciudad, las AGEB de índice socioeconómico más bajo tienden a estar más lejos del centro (correlación −0.58, 40 AGEB). **Firme** (la primaria); **indicio** (el índice).
4. **Vivienda.** En 2020, el **24 % de las viviendas del municipio estaba deshabitado** (11 130 de 45 739). Es el porcentaje más bajo de los 7 municipios de la región, empatado con Salvatierra (24.4 %), y muy por encima de Guanajuato (15.7 %). En **Irámuco**, entre 2010 y 2020, la población creció 5 % (5 954 → 6 275), las viviendas 27 % (1 839 → 2 336) y las deshabitadas pasaron de 356 a 658. **Firme** (censos completos).
5. **Se planeó para un municipio que crecería, y no creció.** El programa regional de 2014 esperaba que la subregión creciera 5.07 % entre 2010 y 2020; **bajó 1.4 %** (unas 11 900 personas menos de lo previsto). El municipio tenía **110 718 habitantes en el censo de 2000 y 108 697 en el de 2020**; en medio, la Encuesta Intercensal 2015 había estimado 112 125. Entre 2010 y 2020, **la ciudad perdió 1 375 habitantes y el resto del municipio ganó 1 042**. **Firme.**
6. **Planes.** De 2006 a 2025, los cuatro documentos señalan la migración, y tres prometen un instrumento municipal de ordenamiento territorial (2006, 2015 y 2025). En julio de 2025 el Programa de Gobierno decía que seguía en elaboración (p. 60), y no aparece en la ficha municipal del IPLANEG (consultada el 12 de noviembre de 2026). **Ninguno mide a qué distancia vive la gente de las escuelas, las clínicas o los mercados**: miden en total. El programa regional de 2014 calculó que en la subregión sobraban aulas de primaria (1 499 existentes contra 451 necesarias); contar aulas en total no dice si están cerca de donde vive la gente. **Firme con matiz** (las afirmaciones de ausencia en los dos planes escaneados descansan en un OCR).

---

## 1. Acceso a servicios

### Umbrales
| Servicio | Ciudad (a pie) | Rural (línea recta × 1.33) |
|---|---:|---:|
| Preescolar | 1 000 m | 2 km |
| Primaria | 670 m | 2 km |
| Secundaria | 1 330 m | 5 km |
| Bachillerato | 3 330 m | 10 km |
| Salud de primer nivel (abierta, D58, y cualquier unidad pública) | 1 330 m | 5 km |
| Tienda básica | 500 m | no medible |
| Mercado o supermercado | 1 000 m | 10 km |

### Ciudad de Acámbaro (56 597 habitantes)

La población de la ciudad es 56 597 en el ITER 2020. La suma por cuadra da 56 596: el censo por manzana tiene una persona menos. Las cifras de acceso usan la suma por cuadra.

**Salud: quién depende de las unidades abiertas (D69)**

La ciudad tiene 4 unidades que atienden a cualquier persona (Secretaría de Salud de Guanajuato) y 2 que solo atienden a sus derechohabientes (el Hospital General de Subzona 13 del IMSS y la clínica del ISSSTE). El Censo 2020 clasifica a la población por su afiliación. Dependen de las 4 unidades abiertas:

| Grupo (Censo 2020, ciudad) | Personas | Lejos de salud abierta (principal) | Piso seguro | Estricto / principal / holgado |
|---|---:|---:|---:|---|
| **Dependen de las unidades abiertas** (las tres filas siguientes) | **34 889** | **20 147 (58 %)** | 19 879 | 72 / 58 / 27 % |
| Sin ninguna afiliación | 11 479 | 7 039 (61 %) | 6 908 | 75 / 61 / 30 % |
| Afiliadas al INSABI / Seguro Popular | 23 267 | 13 041 (56 %) | 12 926 | 71 / 56 / 26 % |
| Afiliadas al IMSS-Bienestar | 143 | — | — | — |

- Los totales son las sumas de las AGEB con dato. Los totales publicados para la localidad son un poco mayores: 11 515 sin afiliación, 23 295 en el INSABI / Seguro Popular y 152 en el IMSS-Bienestar (34 962 en total, el 62 % de la ciudad). La diferencia son AGEB con datos ocultos ("*").
- **Clasificación del censo, no de hoy.** El INSABI ya no existe; quien estaba afiliado sigue atendiéndose en las mismas unidades abiertas.
- **Afiliaciones repetidas.** El censo permite declarar más de una afiliación: en la ciudad, al menos 830 personas tienen dos o más. Algunas personas del INSABI pueden tener también IMSS o ISSSTE, así que el grupo es un poco mayor que el número de personas que en verdad dependen solo de las unidades abiertas.
- **Comparaciones**: toda la población lejos de una unidad abierta, 32 660 (58 %; 72 / 58 / 26 %); toda la población lejos de **cualquier unidad pública** (medida anterior, D20), 12 205 (22 %). La distancia mediana por persona es de 1 470 m a una unidad abierta y de 950 m a cualquier unidad pública.
- **Nota**: parte de la población sin afiliación se atiende en **consultorios de farmacia** (registrados en la CLUES como servicios médicos privados). No se cuentan como salud pública y no están en esta medida.
- **Cada unidad no tiene la misma capacidad**: el Centro de Salud Acámbaro tiene 11 núcleos básicos; otras dos, 2. La medida dice dónde está la unidad, no cuánta gente puede atender.

**Los demás servicios**

| Servicio | Personas lejos | % | Confiabilidad |
|---|---:|---:|---|
| Mercado o supermercado | 20 267 | 36 % | **firme** (62 / 36 / 18 % con los tres umbrales) |
| Primaria (todas) | 17 853 | 32 % | **firme** (55 / 32 / 10 %) |
| Primaria (solo públicas) | 21 460 | 38 % | **firme** (62 / 38 / 11 %) |
| Bachillerato público | 24 430 | 43 % | **frágil**: con el umbral holgado, 1 %. Contando todos los bachilleratos, 2 % |
| Secundaria (todas) | 13 400 | 24 % | moderada (solo públicas, 37 %) |
| Preescolar (todos) | 4 636 | 8 % | moderada |
| Tienda básica | 556 | 1 % | firme (casi nadie lejos) |

La tabla cuenta todas las escuelas salvo en bachillerato, donde cuenta solo las públicas.

Grupos de edad (los totales son sumas de AGEB con dato; los del ITER están entre paréntesis): 1 700 niñas y niños de 6–11 años lejos de una primaria (de 5 139; ITER 5 167; piso 1 583); 2 799 personas de 60 y más y 1 157 con discapacidad lejos de un mercado o supermercado. Lejos de salud, por grupo de edad, solo se calculó con la medida anterior (cualquier unidad pública): 1 730 personas de 60 y más (de 8 748; ITER 8 773).

### Las otras localidades urbanas
- **Irámuco (6 275 hab.)**: es la peor servida de las 4 localidades urbanas: en promedio de los 5 servicios básicos (66 % lejos, contra 36 % en Parácuaro, la siguiente) y en 3 de ellos (mercado, primaria y salud). En secundaria la peor es Parácuaro y en preescolar, Chupícuaro. **No hay mercado ni supermercado registrado; puede existir un tianguis que ninguna fuente captura.** El registrado más cercano es el Mercado Revolución de Santa Ana Maya (Michoacán), a 11.4 km en línea recta del centro. Primaria: 80 % lejos (88 / 80 / 56 %); sus 2 primarias están confirmadas por la SEP. Salud: 64 %. Irámuco "tiene" primaria, secundaria, bachillerato y salud dentro del pueblo (tabla de polos); a la vez, la mayoría de su gente vive lejos de ellas. Las dos cosas son ciertas: "tiene" quiere decir que hay al menos una sede dentro del pueblo. **Firme.**
- **Irámuco, salud**: el grupo que depende de las unidades abiertas es casi todo el pueblo (5 841 de 6 275, 93 %). Lejos de su UMAPS: 3 761 de 5 822 (65 %; piso 3 699; 82 / 65 / 19 %).
- **Parácuaro (4 159 hab.)**: no tiene secundaria dentro del pueblo. Las dos más cercanas, la Secundaria Técnica 24 (junto a Jaral del Refugio) y la Telesecundaria 847 de La Concepción, están a unos 4.3 km en línea recta. La ST 24 está a unos 4.9 km por carretera (verificado en Google Maps, D68). **Firme.** Es la única de las 4 localidades de 2 500 o más sin secundaria. Las 3 de 2 500 a 10 000 habitantes tienen centro de salud abierto, como pide la norma de 1999. Salud: el grupo que depende de las unidades abiertas son 3 332 personas (80 %); lejos, 338 (10 %; piso 287; 30 / 10 / 0 %).
- **Chupícuaro (2 583 hab.)**: preescolar 31 %, primaria 39 %; lo demás, bajo. Salud: el grupo son 2 147 personas (83 %); lejos, 112 (5 %; piso 78; 16 / 5 / 2 %).
- En Irámuco, Parácuaro, Chupícuaro y lo rural, separar la salud abierta **no cambia** las cifras (todas sus unidades cercanas son de la Secretaría de Salud).

### Localidades rurales (208 localidades, 39 083 habitantes)

Todas las cifras rurales dependen del factor de rodeo. Se da la cifra con 1.33 y, entre paréntesis, el rango con factores de 1.0 a 1.5.

- Mercado o supermercado: 15 733 personas lejos, 40 % (de 17 a 49 % según el factor). Con los tres umbrales y el factor 1.33: 86 / 40 / 11 %. **Firme en el sentido**, sin tianguis porque ninguna fuente los registra.
- Salud: 6 635 lejos, 17 % (de 6 a 28 % según el factor). **Moderada**: si contaran 6 unidades sin CLUES, bajaría a 2 992; con el umbral holgado, 0. El grupo que depende de las unidades abiertas: 5 947 de 32 797 lejos (18 %); sin afiliación, 1 152 (14 %). Sin las Unidades Médicas Rurales del IMSS, +2 personas.
- Escuelas: 2–3 % lejos con el umbral principal (de 0 a 9 % según el factor). **Frágil** hacia arriba: con el umbral estricto, 24–27 % para secundaria y bachillerato.
- Tienda básica: **no medible** (el DENUE no registra tiendas rurales).

### Limitaciones del acceso
- Lo rural es aproximado: no ve ríos, cerros ni presas. El único recorrido rural verificado (Parácuaro–ST 24) salió **más corto** que la estimación: 4.9 km por carretera contra 5.7 km estimados (factor real 1.15). Un solo caso no dice hacia dónde se equivoca el factor en general.
- 5 rutas de la ciudad comparadas con Google Maps: diferencia mediana de 2 %. Sirve para saber que el orden de magnitud está bien, no como margen de error.
- La revisión remota de servicios no fue al azar: se revisaron 68 sedes; 74 % se ven en la imagen. Pendientes de campo: Monte Prieto (primaria), el Mercado 22 de Octubre y las 4 unidades de salud abierta de la ciudad.
- La norma (SEDESOL 1999, que SEDATU 2024 reconoce como vigente) no dice si el radio es en línea recta: por eso se reportan tres umbrales (`docs/metodo.md`). Si fuera distancia recorrida, el umbral correcto sería el estricto y todas las cifras de la ciudad subirían (primaria 55 %; salud abierta del grupo dependiente 72 %).
- Bachillerato: la norma da de 2 a 5 km para la preparatoria general; los 2.5 / 3.33 / 5 km del estudio caen dentro de ese rango, y por eso la cifra es frágil.
- La lista completa de límites está en `docs/metodo.md`, sección 6.

---

## 2. Vaciamiento

"**Deshabitada**" es la vivienda sin habitantes el día del censo que no es de uso temporal. "**No habitada**" = deshabitada + de uso temporal (vacacional o de fin de semana). Los porcentajes son sobre el total de viviendas.

### Lo que pasó en la ciudad entre 2010 y 2020
- **Perdió 1 375 habitantes** (de 57 972 a 56 597, −2.4 %) **y ganó 2 508 viviendas** (de 18 813 a 21 321). **Firme** (censos completos).
- Las **viviendas deshabitadas** pasaron de 3 178 (17 %) a 4 606 (22 %). **Firme.**
- La pérdida de población estuvo entre **500 m y 1.5 km del centro** (−2 190 y −1 280 personas por anillo); el anillo de 0 a 500 m ganó 97. **Firme.**
- El % de deshabitadas subió en 7 de los 8 anillos de 500 m hasta 4 km. En el último (3.5–4 km, 227 viviendas) bajó de 30 % a 19 %. En 2020 el % de no habitadas es casi igual en el centro (26 %) que a 1–3 km (24–26 %), y un poco mayor en la orilla (31 %).
- 4 AGEB "se vacían" (alto % de no habitadas y pierden población), con 1 227 habitantes. Están en la **orilla oriente**, de 2.3 a 3.4 km del centro (D47). **Moderada**: depende de cortes de la tipología, que además usa la medida de salud anterior (sección 6).
- **Irámuco 2010–2020**: población +5 % (5 954 → 6 275), viviendas +27 % (1 839 → 2 336) y viviendas deshabitadas de 356 a 658. Las viviendas aumentaron en 497 y las deshabitadas en 302; el censo no dice si las deshabitadas son las nuevas. Venía de perder población desde 2000 (6 232 en 2000; 6 141 en el Conteo de 2005). El PROT (2014, p. 59) describía "actualmente" un "fuerte crecimiento poblacional y de desarrollo habitacional". **Firme** (censos completos).
- Las otras localidades urbanas tienen más viviendas no habitadas que la ciudad: Irámuco 38 %, Parácuaro 42 %, Chupícuaro 46 %. Ahí pesa mucho el uso temporal (18–20 % en Parácuaro y Chupícuaro).

### Con qué va junto el vaciamiento (correlaciones entre áreas, no causas)
Se compararon AGEB urbanas y localidades rurales con al menos 30 viviendas. La medida es una correlación de rangos: 0 = nada, ±0.3 = moderada, ±0.5 = fuerte. Se probaron 54 correlaciones; con pocos casos, alguna puede salir "moderada" por azar.

- **En las localidades rurales** (93), hay más viviendas no habitadas donde hay **más gente de 60 años y más** (0.48) y **menos ocupantes por vivienda** (−0.57), y donde la población bajó entre 2010 y 2020 (−0.27). El cuarto más vacío (50–78 % de no habitadas) tiene 24 % de personas mayores; el menos vacío, 13 %. **Moderada.**
- **En la ciudad** (42 AGEB), el patrón es otro. El % de no habitadas **no** va con la edad (−0.07) ni con la pérdida de población (0.08). Sí va con más **gente nacida en otro estado** (0.41) y con AGEB más chicas (menos hogares, −0.36). El uso temporal es mayor donde la población **creció** (0.38). **Moderada**, con pocos casos.
- **Migración (EIC 2025, municipio)**: el **14.9 % de los hogares de Acámbaro recibe dinero de alguien que vive en otro país** (intervalo de 90 %: 13.8–16.1 %), contra 8.6 % en Guanajuato. Solo 0.44 % de la gente de 5 años y más vivía en EE. UU. en 2020 (Guanajuato 0.35 %) y 1.15 % en otro estado (Guanajuato 1.43 %). **Firme** para las remesas; la migración reciente es tan pequeña que el intervalo es grande en proporción.
- El censo por AGEB no publica quién vivía en otro país en 2015, así que la migración internacional no se puede cruzar a esa escala.

---

## 3. Crecimiento

### Cuadras nuevas del INEGI
- **Las 4 localidades urbanas**: 53 cuadras nuevas entre 2010 y 2020 (29.2 ha) con **356 habitantes en 2020**. En la ciudad son 30 cuadras (18.3 ha), 254 personas y 82 viviendas. Después de 2020: 6 cuadras (4.5 ha) sin población censada. **Firme** en el conteo. En los textos públicos van con conteos, no porcentajes (D49).
- **Acceso de las cuadras nuevas**: la diferencia con las viejas casi desaparece al compararlas con cuadras viejas a la misma distancia del centro. La excepción es el **preescolar**: 172 de sus 356 habitantes (48 %) viven lejos de uno, contra 13 % en las cuadras viejas del mismo anillo. **Moderada**: con el umbral holgado, la diferencia la dan las 58 personas de las 6 cuadras nuevas de Chupícuaro; en la ciudad se invierte.

### Revisión visual de Alejandro (fase 5)
- **Zonas INEGI**: 27 de las 28 revisadas tienen construcción. Casi siempre es poca: pocas casas con mucho terreno o cultivo. **Z20-010 se excluyó** por ser un tramo de calle mal dibujado (D53). No cambia ninguna cifra urbana.
- **La mayoría de las cuadras "nuevas" del municipio no son crecimiento, sino cambio de cartografía** (D54). De las 150 zonas de 2010–2020:

| Clase | Zonas | Hectáreas | Personas |
|---|---:|---:|---|
| Cambio de cartografía: pueblo que ya existía en 2010 y el INEGI empezó a dibujar en cuadras | 118 | 199.6 | 67 localidades con 26 991 hab. en 2010 y 27 075 en 2020 |
| Ampliación de las 4 localidades urbanas | 28 | 29.2 | 356 en las cuadras nuevas |
| Crecimiento nuevo: localidad que no existía en 2010 | 4 | 19.0 | 191 en 2020 (Colonia San Isidro, Juan Pablo II, La Providencia; Los Caballos sin dato) |

  Que esas 67 localidades no ganaran población (+84 personas en 10 años) mientras aparecían 200 ha de cuadras concuerda con lo que se ve en las imágenes: La Mesa de San José, Loretito de las Casas y Tres Marías son pueblos completos que ya estaban. **Firme** en el sentido (regla confirmada por Alejandro, D54). **Limitación**: las 28 zonas de las 4 localidades urbanas (29.2 ha, 356 personas) no se revisaron en imágenes. Su existencia descansa en el Marco Geoestadístico; el GHSL solo ve 0.6 ha de construcción en ellas.

### Construcción fuera de las cuadras (GHSL)
- El GHSL ve **67 ha** de construcción nueva en la ciudad entre 2010 y 2020: 25 dentro de cuadras y **42 fuera**. Es un modelo satelital de 100 m, no un dibujo de casas.
- **La revisión de las 20 zonas más grandes** (70 % de los m² sin cuadras) muestra que **la mayor parte no es vivienda**:

| Lo que se ve | Zonas | m² ganados | % de lo revisado |
|---|---:|---:|---:|
| Invernadero o nave | 8 | 99 739 | 44 % |
| Vivienda (casas dispersas o pocas casas) | 6 | 56 913 | 25 % |
| Terreno baldío | 2 | 43 719 | 19 % |
| Otros (casa con bodega, panteón, dudosa) | 4 | 26 598 | 12 % |

- Por eso (D52) **las 42 ha no se presentan como crecimiento residencial**. Lo que se puede decir es que hay algo de vivienda dispersa fuera de la traza del INEGI (unas 5.7 ha en 6 zonas revisadas, 3.7 de ellas en la ciudad), y que el crecimiento de casas fuera de las cuadras es menor de lo que sugería el GHSL. **Moderada.** No se extrapola a las 58 zonas no revisadas.
- La superficie construida de la ciudad creció 17 % (GHSL) mientras la población bajó 2.4 %: la ciudad **ocupa más suelo con menos gente**. **Firme en el sentido**, aproximada en la cifra.

---

## 4. Comparación regional: ¿Acámbaro destaca?

**Respuesta corta: no. Acámbaro sigue el patrón de su región, y en viviendas deshabitadas está empatado con el municipio más bajo de sus vecinos.** La región, Acámbaro incluido, perdió o casi no ganó población mientras Guanajuato y el país crecían.

| Municipio completo | Población 2010 → 2020 | Viviendas 2010 → 2020 | % deshabitadas 2010 → 2020 | % uso temporal 2010 → 2020 | Población 2025 (EIC, cambio desde 2020 e intervalo 90 %) |
|---|---:|---:|---:|---:|---|
| **Acámbaro** | **−0.3 %** | **+16.1 %** | **19.0 → 24.3** | **10.9 → 9.7** | **108 140 (−0.5 %; −7.4 a +6.4)** |
| Coroneo | −5.2 % | +17.4 % | 19.5 → 26.4 | 9.1 → 11.8 | 12 174 (+9.8 %; −8.4 a +28.1) |
| Jerécuaro | −2.6 % | +14.2 % | 22.9 → 26.0 | 10.0 → 10.8 | 51 157 (+3.3 %; −5.7 a +12.3) |
| Salvatierra | −3.0 % | +13.7 % | 18.8 → 24.4 | 7.5 → 8.0 | 95 228 (+1.2 %; −6.0 a +8.3) |
| Santiago Maravatío | +0.7 % | +12.6 % | 27.7 → 30.9 | 11.7 → 9.9 | 5 951 (−11.4 %; −21.7 a −1.0) |
| Tarandacuao | −2.9 % | +14.2 % | 20.7 → 26.1 | 13.6 → 12.5 | 11 322 (+0.2 %; −9.3 a +9.6) |
| Tarimoro | +0.9 % | +11.2 % | 25.7 → 27.0 | 9.7 → 8.9 | 35 135 (−2.1 %; −11.2 a +6.9) |
| Guanajuato | +12.4 % | +25.2 % | 15.2 → 15.7 | 4.6 → 4.6 | 6 423 384 (+4.2 %; +1.9 a +6.4) |
| Nacional | +12.2 % | +23.2 % | 14.0 → 14.0 | 5.6 → 5.7 | 130 393 389 (+3.5 %; +2.8 a +4.1) |

(% sobre el total de viviendas.)

- **Toda la región perdió o casi no ganó población** entre 2010 y 2020 (de −5.2 % a +0.9 %), mientras Guanajuato y el país crecieron 12 %. Acámbaro (−0.3 %) está entre los que menos perdieron (3.º de 7).
- **En toda la región las viviendas crecieron 11–17 % sin que creciera la población**, y el % de deshabitadas subió en los 7 municipios. Acámbaro construyó un poco más (+16.1 %, 2.º de 7).
- **En 2020 Acámbaro tiene el % de deshabitadas más bajo de los 7** (24.3 %), prácticamente empatado con Salvatierra (24.4 %); los otros, 26.0–30.9 %. Está muy por encima de Guanajuato (15.7 %) y del país (14.0 %). Su cabecera también tiene el más bajo de las 7 cabeceras (21.6 %; las otras, 22.4–29.5 %).
- **Cabeceras**: la de Acámbaro perdió 2.4 % de población (4.ª de 7); Tarandacuao (−6.7 %) y Salvatierra (−4.8 %) perdieron más.
- **2020–2025**: la EIC es una encuesta y sus intervalos son anchos. Para Acámbaro y casi todos los vecinos **no se puede distinguir un cambio de cero**. La excepción es Santiago Maravatío, que sí bajó. Guanajuato y el país siguieron creciendo. La EIC solo trae la cabecera de Acámbaro (56 771; +0.3 %, de −10.3 a +10.9 %).

**Confiabilidad**: **firme** para 2010 y 2020 (censos completos). 2025, **moderada**: sirve para decir que no hay evidencia de un cambio grande, no para dar una cifra.

Figura: `docs/figuras/fase5_regional.png`. Tabla: `data/processed/comparacion_regional.csv`.

---

## 5. Nivel socioeconómico aproximado

### Qué es y qué no es
Es un índice construido con el Censo 2020 (D56), **inspirado en la regla AMAI, pero no es el NSE oficial**: la AMAI clasifica hogar por hogar con su propio cuestionario, y aquí se usan promedios por área. **Tampoco mide ingreso.** Fórmula:

> índice = 0.5 × (escolaridad promedio, estandarizada) + 0.5 × (promedio estandarizado de: % de viviendas con automóvil, internet, computadora, refrigerador, lavadora, horno de microondas y 2 dormitorios o más)

"Estandarizada" significa que cada variable se mide en desviaciones respecto al promedio **de su propio conjunto**: AGEB urbanas por un lado y localidades rurales por otro. Por eso **los quintiles urbanos y los rurales no se comparan entre sí**: el Q1 urbano no es "igual de pobre" que el Q1 rural. Cada conjunto se reporta y se cruza por separado.

Cobertura: 53 AGEB urbanas (67 922 de 69 614 personas) y 93 localidades rurales (37 696 de 39 083). El piso de tierra quedó fuera porque el INEGI lo oculta en 16 AGEB (10 060 personas).

Ejemplo de lo que separa (medianas entre AGEB o localidades): en lo urbano, el quintil más bajo tiene 7.2 años de escolaridad, 33 % de viviendas con internet y 16 % con computadora; el más alto, 10.3 años, 57 % y 44 %. En lo rural: 5.4 años, 4 % y 4 %, contra 7.8 años, 20 % y 18 %.

### ¿Las zonas de menor nivel están más lejos?
Promedio de servicios básicos lejos por persona (de 5: preescolar, primaria, secundaria, salud pública, mercado o supermercado). Este cruce usa la medida de salud anterior (cualquier unidad pública); con salud abierta no se ha recalculado (pendiente de la versión 1.1).

| Quintil | Urbano (4 localidades) | Solo ciudad de Acámbaro | Rural |
|---|---:|---:|---:|
| Q1 (más bajo) | **2.6** (9 542 personas) | 3.2 (solo 358 personas) | **1.3** (4 843) |
| Q2 | 1.5 | 1.5 | 0.5 |
| Q3 | 1.9 | 1.9 | 0.7 |
| Q4 | 1.0 | 0.9 | 0.5 |
| Q5 (más alto) | **0.8** (22 824) | 0.8 | **0.5** (6 664) |

- **En general las zonas de menor nivel están más lejos, pero no en una escalera pareja.** En lo urbano, el quintil más bajo tiene más del triple de servicios lejos que el más alto. Buena parte de esa diferencia viene de Irámuco: sus 5 AGEB caen en el quintil más bajo, y es la localidad urbana peor servida. Solo en la ciudad, la diferencia entre Q2 y Q5 es de 1.5 a 0.8, y Q3 (1.9) rompe el orden.
- Por servicio, en lo urbano: del quintil más bajo, 65 % está lejos de una primaria y 66 % de un mercado o supermercado; del más alto, 27 % y 34 %. **La excepción es el bachillerato público**: los quintiles altos están más lejos (Q4 63 %, Q5 43 %) que el más bajo (4 %).
- En lo rural, la diferencia es sobre todo **salud pública**: 66 % del quintil más bajo está a más de 5 km de una unidad, contra 5–14 % en los demás.
- **Distancia al centro**: **dentro de la ciudad**, las AGEB de índice más bajo tienden a estar más lejos del centro (correlación −0.58, 40 AGEB). Es un indicio, no una causa. Juntando las 4 localidades urbanas, cada una medida desde su propio centro, la relación no aparece (−0.03, 53 AGEB); esa cifra no describe a la ciudad.
- Tipología: 5 de las 11 AGEB del quintil urbano más bajo son "consolidadas desatendidas" (3 de Irámuco y 2 de la orilla de la ciudad); en los otros quintiles, 1 o 2. El quintil más bajo reúne Irámuco (6 000 personas), 2 AGEB de Parácuaro, 1 de Chupícuaro y solo 3 AGEB pequeñas de la ciudad.

**Confiabilidad**: urbano **moderada**. Con pesos iguales o con componentes principales, el Q1 sigue en 3.0 y el Q5 en 0.8–0.9, pero el resultado depende mucho de Irámuco. Rural **frágil, y se presenta como indicio, no como hallazgo** (D56): con los índices alternativos, el quintil con más servicios lejos pasa a ser Q2 (1.0) y el Q1 baja a 0.8, y solo 45 % de las localidades quedan en el mismo quintil.

Figura: `docs/figuras/fase5_nse.png`. Tablas: `nse_ageb.csv`, `nse_localidades.csv`, `nse_acceso.csv`.

---

## 6. Limitaciones generales

La lista completa, con los límites agregados en la fase 8, está en `docs/metodo.md`, sección 6. Las principales:

1. **Población de 2020 con servicios de 2026.** Quien llegó después de 2020 no está contado, y no se inventa población para las cuadras nuevas. El catálogo SEP no tiene fecha de corte (se cita la consulta del 2026-10-22).
2. **El "*" del INEGI** oculta datos de cuadras y AGEB con pocas viviendas. Los grupos son estimaciones por AGEB (D10), con el piso seguro al lado. Los totales de grupo son sumas de AGEB con dato, un poco menores que los del ITER.
3. **Lo rural se mide con línea recta × 1.33**, no por caminos reales. Las cifras rurales cambian mucho con el factor (rangos en la sección 1).
4. **Tiendas y consultorios rurales no se pueden medir** (el DENUE no los registra). Los tianguis no están en ninguna fuente.
5. **La distancia no mide capacidad ni calidad**: ni cupo en la escuela, ni consultorios o médicos en la unidad.
6. **El GHSL detecta construcción, no vivienda**: confunde invernaderos y suelo desnudo.
7. **No hay población por localidad de 1990–1995** (D50); 2000 y 2005 solo para la gráfica de proyección y para Irámuco. 2005 es un conteo, no un censo.
8. **Todo es descriptivo.** Las correlaciones son entre áreas, no entre personas: que las AGEB con más gente de otro estado tengan más casas vacías no dice que esas personas dejen casas vacías.
9. **El índice socioeconómico es una aproximación por área**, no el NSE AMAI ni ingreso. La tipología y el cruce con el índice usan la medida de salud anterior.
10. **Las verificaciones fueron remotas** (Google Earth y Maps, D13) y no al azar. Las salidas de campo siguen pendientes. Las 28 zonas de cuadras nuevas 2010–2020 de las 4 localidades urbanas no se revisaron en imágenes.
11. **Las normas no se cotejaron** con el documento original (SEDESOL 1999, SEDATU 2024, NOM-002).
12. **Las citas del Plan 2040 y del Programa 2025 se verificaron sobre un OCR.** Las citas positivas están en su página; lo que "no se encontró" en esos dos documentos puede estar en una tabla o un mapa que el OCR no lee.

## 7. Los planes oficiales

Detalle en `docs/contraste_planes.md`: cuatro documentos, el Plan Municipal 2030 (2006), el PROT Subregión 10 (2014), el Plan Municipal de Desarrollo 2040 (2015) y el Programa de Gobierno 2024–2027 (2025). Figura: `docs/figuras/fase6_proyeccion.png`.

- **El hilo**: los cuatro documentos señalan la migración; tres tratan aparte a Irámuco (dos de ellos, también a Parácuaro) y dos hablan de poco equipamiento en las localidades. Tres prometen un instrumento municipal de ordenamiento territorial: se promete en 2006 (plazo de 6 meses, p. 241) y en 2015 (p. 172 y 174); en julio de 2025 el Programa de Gobierno decía que "se encuentra en elaboración" (p. 60) y fija como acción "Concluir" el PMDUOET (p. 68). No aparece en la ficha municipal del IPLANEG (consultada el 12 de noviembre de 2026). **Ninguno mide a qué distancia vive la gente de los servicios**, y ninguno trata la vivienda deshabitada como tema (el Plan 2006 la anota en una ficha de comunidad: "79 sin habitar" en Arroyo Colorado, p. 171).
- **Medir en total**: el PROT ve superávit de aulas en la subregión (cuadro 3, p. 38: primaria, 1 499 aulas existentes contra 451 necesarias) y el Plan 2040 ve un municipio con menos escuelas por habitante que el estado (p. 143 y 158). Los dos miden en total, sin ubicación; las distancias muestran dónde falta. El PROT sí mide la accesibilidad a carretera pavimentada (p. 51), que no es distancia a los servicios.
- **Salud**: el Programa 2025 cuenta 26 unidades y 20.72 % sin afiliación (p. 44–45), sin distinguir a quién atiende cada unidad ni dónde están. Sus acciones en salud son campañas con la unidad médica del DIF (p. 73). En todo el apartado de acciones **no se encontraron acciones para construir unidades de salud, escuelas o mercados en las localidades.**
- **Irámuco**: el Programa 2025 reconoce su "baja cobertura de servicios públicos y equipamiento" junto con Parácuaro (p. 55). En esa página da 6 725 habitantes (errata del documento; el censo y su p. 43 dan 6 275).
- **Se planeó para un municipio que crecería**: el PROT (2014) proyectaba +5.07 % para la subregión entre 2010 y 2020; el censo dio **−1.4 %** (unas 11 900 personas menos de lo proyectado). Para Acámbaro daba 112 076 en 2014. Los censos dieron 110 718 (2000), 109 030 (2010) y 108 697 (2020); la Encuesta Intercensal 2015 estimó 112 125 (cifra citada en el Programa 2025, p. 41). Para la ciudad, el PROT esperaba una baja a 51 613 habitantes en 2030; entre 2010 y 2020 la ciudad perdió 1 375 habitantes y el resto del municipio ganó 1 042. **Firme.**
- **Diagnósticos que ya existían**: la "muy alta migración" (Plan Municipal, p. 18; "alta" en el Plan 2040, p. 138; 68 millones de dólares en remesas en 2022 según el Programa 2025, p. 43) sigue: 14.9 % de los hogares recibe remesas en 2025. La falta de secundaria dentro de Parácuaro sigue. El Programa 2025 es el primer documento que reconoce una baja de la población del municipio en cifras (p. 41–42); el PROT ya hablaba de "un decremento en sus tasas poblacionales" (p. 30) y proyectaba menos gente en la ciudad (p. 42).
- **Metas por polo** (plan de 2006, el único que nombra sedes y fija metas por polo; el Plan 2040 no enumera polos ni fija metas por localidad en su texto, y el Programa 2025 menciona 11 polos sin enumerarlos ni fijarles metas): de los 7 polos de desarrollo rural, **Chupícuaro** tiene todo lo que pedía el plan; **Parácuaro** no tiene secundaria e **Inchamácuaro** no tiene bachillerato ni unidad de salud; en los otros **4** el abasto **no se puede verificar** (sin mercado registrado; puede haber tianguis). En 3 polos (San Mateo Tócuaro, Chamácuaro y Arroyo de la Luna) el bachillerato es un telebachillerato o videobachillerato que solo registra la SEP.
- **Vivienda**: el Plan Municipal hablaba de "déficit habitacional" (p. 214); entre 2010 y 2020 el municipio ganó 6 348 viviendas sin que creciera su población, y en 2020 había 11 130 deshabitadas (24 %).

## 8. Decisiones pendientes para Alejandro

1. Cotejar el SNEU original (las páginas de SEDESOL, SEDATU y la NOM se citan como las diste; Claude no tiene esos documentos).
2. Salidas de campo (`docs/verificar_campo.csv` y `docs/verificar_campo_fase6.csv`): que la ST 24 funcione y las 4 unidades de salud abierta de la ciudad.
3. Red de caminos rural (RNC al release).
4. La dirección de la ficha municipal del IPLANEG, para citarla en `docs/fuentes.md`.
5. Siguiente fase: sitio web y reporte PDF. Los pendientes de la versión 1.1 están en `CLAUDE.md`.

## 9. Qué cambió en la fase 8 (2026-11-20)

Se aplicó la revisión final independiente (`docs/revision_final.md`) con las decisiones de Alejandro.

| # | Antes | Ahora |
|---|---|---|
| 1 | 7 039 de 11 479 personas sin afiliación (61 %) lejos de una unidad abierta | Unas 20 100 de 34 900 personas que dependen de las unidades abiertas (58 %; piso 19 879; 72 / 58 / 27 %). Las 7 039 sin afiliación quedan como subgrupo (D69) |
| 2 | Irámuco "la peor servida"; Parácuaro, secundaria "a unos 5.5 km" (o 5.6); "solo Chupícuaro cumple" | "La peor de las 4 urbanas", con la frase completa del tianguis; Parácuaro con la frase única, las dos escuelas a 4.3 km en línea recta y la ST 24 a 4.9 km por carretera (D68); polos: 1 cumple, 2 no, 4 no se pueden evaluar |
| 3 | "Hay aulas suficientes en total, pero el 32 % vive lejos de una primaria" | 32 % (38 % solo públicas), con los tres umbrales; el superávit de aulas (subregión) pasa al hallazgo 6; indicio del índice dentro de la ciudad (−0.58) |
| 4 | 24 % deshabitadas; Irámuco | Sin cambio de cifras; "en 2020" y el empate con Salvatierra |
| 5 | "La ciudad superó en 2020 lo proyectado para 2030": concentración en la ciudad | "Se planeó para un municipio que crecería, y no creció": subregión, municipio (con la Intercensal 2015) y ciudad contra resto del municipio. Sin "concentración" |
| 6 | "Tres prometen un ordenamiento que no se ha publicado" | "En julio de 2025 seguía en elaboración (p. 60) y no aparece en la ficha municipal del IPLANEG" |

Además:
- Las 9 correcciones (a) y los 18 matices (b) de la revisión, en este documento, en `contraste_planes.md` y en `metodo.md` (detalle en el PR de la fase 8).
- Cifras rurales con rango según el factor (`src/31_sensibilidad_factor.py`, V61).
- `src/27_salud_abierta.py` calcula el grupo que depende de las unidades abiertas (V60); `src/26_nse_aproximado.py` da la correlación dentro de la ciudad; `src/04_inventario.py` vuelve a correr (V62).
- 11 citas nuevas en la verificación automática: 75 de 75 en su página (V63).
- Los límites que faltaban, en `docs/metodo.md`, sección 6.
