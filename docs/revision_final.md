# Revisión final independiente (fase 7)

Fecha: 2026-11-14. Revisión externa antes de publicar el sitio y el PDF. **No se corrigió nada**: ni scripts, ni datos, ni textos. Este documento solo reporta.

**Cómo se hizo**
- Todo se volvió a correr en una **copia fuera del repositorio**. En el repositorio el único archivo nuevo es este.
- Las cifras se recalcularon con código propio del revisor, leyendo las tablas de `data/processed/` y, donde se pudo, los archivos originales del INEGI recién bajados (ITER 2000, 2005, 2010 y 2020, Censo 2020 por manzana). No se usaron las funciones de los scripts revisados para comprobarlos.
- Los crudos se bajaron de nuevo: INEGI y JRC con `01_descargar.py`; el release `datos-crudos` (12 archivos) con la API autenticada de GitHub.
- Orden pedido por Alejandro: primero cifras, consistencia, hallazgos, lenguaje y citas; después reproducibilidad.

**Estado de las secciones**

| Sección | Estado |
|---|---|
| 1. Resumen en lenguaje sencillo | pendiente (se escribe al final) |
| 2. Reproducibilidad | en curso |
| 3. Tabla de cifras | **terminada** |
| 4. Consistencia | pendiente |
| 5. Los seis hallazgos | pendiente |
| 6. Límites que el reporte debe declarar | pendiente |
| 7. Lenguaje | pendiente |
| 8. Citas de los planes | **terminada** |
| 9. Observaciones clasificadas | pendiente |

---

## 3. Tabla de cifras

Se rastrearon las cifras de `resumen_final.md` (R), `contraste_planes.md` (C) y `metodo.md` (M) hasta el archivo del que salen. "Recalculado" = el revisor volvió a obtener el número con su propio código.

**Resultado general**: de 118 cifras revisadas, **110 coinciden**, 5 coinciden con un matiz que el texto no dice, y **3 no coinciden o no se sostienen** (marcadas **NO**). Ninguna cifra de los seis hallazgos está mal copiada; los problemas están en cómo se interpretan dos de ellas (secciones 5 y 9).

### 3.1 Acceso en la ciudad

| Cifra | Doc. | Archivo fuente | Coincide |
|---|---|---|---|
| Ciudad: 56 596 habitantes | R | `acceso_cuadras.csv` (suma de cuadras) | sí. El ITER da 56 597; ver 4.1 |
| Sin afiliación lejos de salud abierta: 7 039 | R, C | `salud_abierta_resumen.csv` (principal, PSINDER) | sí. Es una **estimación**; el mínimo contado cuadra por cuadra es 6 908 (recalculado) |
| …de 11 479 sin afiliación | R, C | suma de AGEB con dato, Censo 2020 | sí, con matiz: el total de la localidad en el ITER es **11 515**. Faltan 36 personas de 19 AGEB ocultas |
| 61 % | R, C | 7 039 / 11 479 = 61.3 % | sí (61.1 % sobre 11 515; 60.2 % con el mínimo) |
| 75 / 61 / 30 % con los tres umbrales | R, C | `salud_abierta_resumen.csv` | sí (75.2 / 61.3 / 29.8) |
| Salud abierta, toda la población: 32 660 (58 %); 72 / 58 / 26 | R, C | `acceso_salud_abierta.csv` | sí (recalculado: 40 695 / 32 660 / 14 964) |
| Cualquier unidad pública: 12 205 (22 %) | R, C | `acceso_resumen_por_localidad.csv` | sí (21.6 %) |
| Sin afiliación con la medida anterior: 2 380 | R | `salud_abierta_resumen.csv` | sí |
| 4 unidades abiertas y 2 solo derechohabientes | R, C | `salud_clasificacion_instituciones.csv` | sí (4 de la SSG; HGSMF 13 del IMSS; UMF del ISSSTE) |
| Distancia mediana por persona: 1 470 m y 950 m | R | `acceso_salud_abierta.csv` | sí (recalculado: 1 467 y 948) |
| Mercado o supermercado: 20 267 (36 %); 62 / 36 / 18 | R | `acceso_resumen_por_localidad.csv` | sí |
| Primaria: 17 853 (32 %); 55 / 32 / 10 | R, C | ídem | sí (55.5 / 31.5 / 9.8) |
| Bachillerato público: 24 430 (43 %); holgado 1 % | R, C, M | ídem | sí (71.5 / 43.2 / 1.4) |
| Secundaria: 13 400 (24 %) | R | ídem | sí (42.8 / 23.7 / 6.0) |
| Preescolar: 4 636 (8 %) | R | ídem | sí |
| Tienda básica: 556 (1 %) | R | ídem | sí |
| 1 700 de 5 139 niños de 6–11 lejos de primaria | R | ídem | sí. Mínimo visible 1 583. El ITER da 5 167 niños, no 5 139 |
| 1 730 de 8 748 de 60+ lejos de salud pública | R | ídem | sí, pero usa la medida **anterior** (cualquier unidad pública), no la abierta; ver 4.3 |
| 2 799 de 60+ y 1 157 con discapacidad lejos de mercado | R | ídem | sí |
| 5 rutas con Google Maps: diferencia mediana 2 % | R | `docs/verificar_rutas.csv` | sí (1.7 %) |
| 74 % de 68 servicios revisados se ven | R | `servicios_sedes_fase4.csv` | sí (50 de 68 = 73.5 %) |

### 3.2 Irámuco, Parácuaro, Chupícuaro y lo rural

| Cifra | Doc. | Archivo fuente | Coincide |
|---|---|---|---|
| Irámuco 6 275, Parácuaro 4 159, Chupícuaro 2 583 | R, C | ITER 2020 (recalculado del crudo) | sí |
| Irámuco, mercado: 100 % lejos | R | `acceso_resumen_por_localidad.csv` | sí (con los tres umbrales) |
| Mercado más cercano a Irámuco: 13–18 km | R, C | `acceso_cuadras.csv` | sí (12.9 a 17.6 km según la cuadra; todas en línea recta × 1.33) |
| …15.2 km | C (polos) | `polos_desarrollo.csv` | sí (desde el punto ITER). Son dos medidas del mismo dato; ver 4.1 |
| Irámuco, primaria: 80 %; 88 / 80 / 56 | R, C | `acceso_resumen_por_localidad.csv` | sí (88.1 / 80.5 / 56.3) |
| Irámuco, salud pública: 64 % | R | ídem | sí |
| Parácuaro: ST 24 "a unos 5.5 km" | R | `acceso_cuadras.csv` | sí como mediana de las 72 cuadras que la tienen más cerca. **No** es la más cercana desde el centro; ver 4.1 |
| Parácuaro: la más cercana a 5.6 km; mediana por persona 5.4 km | C | `localidades_2500.csv`, `polos_desarrollo.csv` | sí (5 620 m a la Telesecundaria 847; 5 380 m) |
| Chupícuaro: preescolar 31 %, primaria 39 % | R | `acceso_resumen_por_localidad.csv` | sí (30.6 y 38.5) |
| Rural: 208 localidades, 39 083 habitantes | R | `acceso_localidades.csv` | sí |
| Rural, mercado: 15 733 (40 %); 86 / 40 / 11 | R | `acceso_resumen_por_localidad.csv` | sí |
| Rural, salud: 6 635 (17 %); con anexo 2 992; holgado 0 | R | ídem | sí |
| Rural, sin afiliación lejos: 1 152 (14 %); sin UMR +2 | R | `salud_abierta_resumen.csv` | sí |
| Rural, escuelas 2–3 %; estricto 24–27 % | R | `acceso_resumen_por_localidad.csv` | sí (1.8 a 3.0; 23.6 y 27.0) |
| Polos: población y distancias de la tabla (5.9, 10.9, 13.2, 10.9, 3.3, 3.7 km) | C | `polos_desarrollo.csv` | sí, las 7 filas |
| Localidades de 2 500 o más: 4 y 10 sedes en la ciudad | C | `localidades_2500.csv` | sí |

### 3.3 Vivienda y población

| Cifra | Doc. | Archivo fuente | Coincide |
|---|---|---|---|
| Ciudad: 57 972 → 56 597 (−1 375, −2.4 %) | R, C | ITER 2010 y 2020 (crudo) | sí |
| Ciudad: 18 813 → 21 321 viviendas (+2 508) | R, C | ídem | sí |
| Ciudad: deshabitadas 3 178 (17 %) → 4 606 (22 %) | R, C | ídem | sí (16.9 y 21.6) |
| Primer kilómetro: −2 093 personas, −12 % | R | `crecimiento_viviendas_2010_2020.csv` | sí (−11.6 %). Matiz: el anillo 0–500 m **ganó** 97; la pérdida es de 500 a 1 500 m; ver 7 |
| "El % de deshabitadas subió en todos los anillos" | R | ídem, filas `anillo_unidades` | **NO**: en el anillo de 3.5–4 km bajó (30.0 → 19.4 %), y de 3 a 4 km junto bajó de 26.2 a 24.7 % |
| No habitadas 2020: centro 26 %, 1–3 km 24–26 %, orilla 31 % | R | `crecimiento_viviendas.csv` | sí (25.9; 24.2 y 26.3; 30.5) |
| 4 AGEB que se vacían, 1 227 habitantes | R | `tipologia_ageb.csv` | sí. "Orilla oriente": no comprobado (la tabla no trae coordenadas) |
| Irámuco: 5 954 → 6 275 (+5 %) | R, C | ITER (crudo) | sí (+5.4 %) |
| Irámuco: viviendas 1 839 → 2 336 (+27 %) | R, C | ídem | sí |
| Irámuco: deshabitadas 356 → 658; 19 % → 28 % | R, C | ídem | sí (19.4 y 28.2) |
| Irámuco: 6 232 (2000), 6 141 (2005) | R, C | ITER 2000 y 2005 (crudo) | sí |
| No habitadas: Irámuco 38 %, Parácuaro 42 %, Chupícuaro 46 %; uso temporal 18–20 % | R | ITER 2020 (crudo) | sí (38.2, 42.2, 46.3; 18.1 y 20.4) |
| Municipio: 39 391 → 45 739 viviendas (+6 348, +16 %) | R, C | ITER (crudo) | sí |
| Municipio: deshabitadas 7 492 (19 %) → 11 130 (24 %), +3 638 | R, C | ídem | sí (19.0 y 24.3, sobre el total de viviendas) |
| Correlaciones rurales: 0.48, −0.57, −0.27; 93 localidades | R | `vaciamiento_correlaciones.csv` | sí |
| Cuartil más vacío 50–78 %, 24 % de 60+; menos vacío 13 % | R | `vaciamiento_cuartiles.csv` | sí |
| Correlaciones de la ciudad: −0.07, 0.08, 0.41, −0.36, 0.38; 42 AGEB | R | `vaciamiento_correlaciones.csv` | sí |
| Remesas: 14.9 % (13.8–16.1); Guanajuato 8.6 % | R, C | `vaciamiento_eic2025.csv` | sí |
| 0.44 % vivía en EE. UU. (0.35 %); 1.15 % en otro estado (1.43 %) | R | ídem | sí |

### 3.4 Crecimiento

| Cifra | Doc. | Archivo fuente | Coincide |
|---|---|---|---|
| 53 cuadras nuevas, 356 habitantes; ciudad 30 y 254; 6 posteriores a 2020 | R | `cuadras_antiguedad.csv` | sí |
| 29.2 ha | R | `zonas_2010_2020_clase.csv` | sí (`validacion.md` V39 dice 29.3) |
| Preescolar: 48 % contra 13 % | R | `crecimiento_acceso_periferia.csv` | sí. Matiz fuerte en "aparece con los tres umbrales"; ver 9 (b) |
| 150 zonas: 118 / 28 / 4; 199.6, 29.2 y 19.0 ha | R | `zonas_2010_2020_clase.csv` | sí |
| 67 localidades: 26 991 → 27 075 (+84) | R | ídem | sí |
| 191 habitantes en localidades nuevas | R | ídem | sí (137 + 30 + 24) |
| GHSL ciudad: 67 ha; 25 dentro y 42 fuera | R | `ghsl_dentro_fuera_cuadras.csv` | sí (66.6, 25.0, 41.6) |
| Revisión de 20 zonas: 8 / 6 / 2 / 4; m² y porcentajes | R | `verificacion_ghsl_resultado.csv` | sí, las 4 filas; 70.5 % de los m² |
| Vivienda: 5.7 ha, 3.7 en la ciudad | R | ídem | sí |
| Superficie construida +17 % | R, C | `ghsl_serie.csv` | sí (389.8 → 456.4 ha) |

### 3.5 Comparación regional e índice socioeconómico

| Cifra | Doc. | Archivo fuente | Coincide |
|---|---|---|---|
| Tabla regional: 9 filas × 5 columnas | R | `comparacion_regional.csv` | sí, todas las celdas |
| Acámbaro 3.º de 7 en población y 2.º en viviendas | R | ídem | sí |
| % deshabitadas más bajo de los 7 (24.3; otros 24.4–30.9) | R | ídem | sí. Matiz: Salvatierra tiene 24.4; es un empate |
| Cabecera 21.6 %; otras 22.4–29.5 | R | ídem | sí |
| EIC 2025: municipio 108 140 (100 654–115 626); ciudad 56 771 | R, C | ídem | sí |
| Índice: 53 AGEB, 67 922 de 69 614; 93 localidades, 37 696 de 39 083 | R | `nse_ageb.csv`, `nse_localidades.csv` | sí |
| Ejemplos por quintil (7.2 años, 33 %, 16 %…) | R | `validacion_fase5.json` | sí, pero son **medianas** entre AGEB, y el texto dice "promedio" |
| Servicios lejos por quintil (tabla) | R | `nse_acceso.csv` | sí, las 15 celdas |
| 65 % y 66 %; 27 % y 34 %; bachillerato 63, 43 y 4 %; rural 66 % | R | ídem | sí |
| "El índice no se relaciona con la distancia al centro de la ciudad (−0.03)" | R | `nse_ageb.csv` | **NO**: −0.03 sale de juntar las 53 AGEB de las 4 localidades. Solo en la ciudad (40 AGEB) la correlación es **−0.58**: a más distancia del centro, índice más bajo |
| Q1 urbano: 5 AGEB de Irámuco, 2 de Parácuaro, 1 de Chupícuaro, 3 de la ciudad | R | ídem | sí |
| Índices alternativos: Q1 3.0, Q5 0.8–0.9; rural Q2 1.0 y Q1 0.8 | R | `nse_acceso.csv` | sí (2.97; 0.78–0.82) |

### 3.6 Planes y proyecciones

| Cifra | Doc. | Archivo fuente | Coincide |
|---|---|---|---|
| Municipio: 110 718 (2000), 101 762 (2005), 109 030 (2010), 108 697 (2020) | R, C | ITER (crudo) | sí |
| Subregión: 183 194 → 180 601 (−1.4 %) | R, C | ITER de los 4 municipios (crudo) | sí |
| +5.07 % proyectado; "unas 11 900 menos" | R, C | PROT p. 59; 183 194 × 1.0507 − 180 601 | sí (11 881) |
| PROT: 112 076 y 189 535 en 2014 | R, C | PROT, cuadro 3, p. 38 (leído en el PDF) | sí |
| "El municipio nunca pasó de 110 718" | R | ITER | **NO** como está escrito: es cierto solo para los censos. La Encuesta Intercensal 2015 dio **112 125**, cifra que el propio contraste cita (Programa 2025, p. 41). Ver 9 (a) |
| Ciudad: 51 613 en 2030 | R, C | PROT p. 42 (leído en el PDF) | sí |
| 31.64 % de 183 194 ≈ 57 960; censo 57 972 | C | PROT p. 30; ITER 2010 | sí |
| "Casi 5 000 en diez años, más del triple" | C | 56 597 − 51 613 = 4 984; 4 984 / 1 375 = 3.6 | sí |
| Plan 2006: 115 121; 13 % más que el Conteo 2005 | C | Plan 2006 p. 18; ITER 2005 | sí |
| 64 citas verificadas | R, C | `docs/verificar_citas_planes.csv` | sí (sección 8) |
| Cuadro 3 del PROT: +279, +1 048, +56 | C | PROT p. 38 (leído en el PDF) | sí. Es de la **subregión** completa, no de la ciudad ni del municipio |
| "19 años después" | C | 2006 → 2025 | sí |

### 3.7 Nota de método

| Cifra | Doc. | Archivo fuente | Coincide |
|---|---|---|---|
| Tabla de los tres umbrales de la ciudad | M | `UMBRALES_CIUDAD` en `11_accesibilidad.py`; D33 | sí, las 7 filas |
| Umbrales rurales (2, 2, 5, 10, 5, 10 km) | R | `UMBRALES_RURAL` | sí |
| Radios de la norma de 1999 (750, 500, 1 000 m…), páginas de SEDATU 2024 y NOM-002 | M | documentos que no están en el repositorio | **no cotejable** (el propio texto lo declara) |
| DENUE 05/2026, CLUES agosto 2026, SEP consultado el 2026-10-22 | M | `docs/fuentes.md`; nombres y fechas de los archivos del release | sí |

---

## 8. Citas de los planes

**Verificación automática, vuelta a correr.** `src/30_planes.py` corrió sin errores en la copia, con los cuatro documentos bajados de nuevo del release. Sus salidas son **idénticas byte por byte** a las versionadas: `docs/verificar_citas_planes.csv` (**64 de 64** citas en su página), `iramuco_serie.csv`, `proyecciones_vs_censo.csv`, `verificar_campo_fase6.csv`, `validacion_fase6.json` y la figura.

**Qué prueba y qué no prueba esa verificación.** Busca la frase exacta en la página indicada. Es estricta: no acepta frases parecidas. Pero solo comprueba que la frase **está**; no comprueba que el texto que la rodea diga lo que el contraste le hace decir.

**Segunda verificación, del revisor.** Con un programa aparte se buscaron las 53 frases entre comillas de `contraste_planes.md` y las de la sección 7 del resumen en los cuatro documentos. Resultado:

- **47 aparecen tal cual** en la página citada.
- **3 no son literales**, aunque van entre comillas:
  - "Proyección de Población del CONAPO 2000-2030" (Plan 2006, p. 34). El original dice "Proyección de Población del Consejo Nacional de Población (CONAPO) 2000-2030".
  - "…y el segundo en el ámbito municipal" (Plan 2006, p. 61). El original dice "en **al** ámbito municipal" (errata del plan, corregida sin avisar).
  - "es una interacción con Michoacán" (PROT, p. 59). El original dice "es **un** interacción" (ídem).
- **1 página no corresponde**: la síntesis dice que el Plan 2040 presenta el instituto de planeación como "Proyecto Nuevo" en p. 166 y 174. La etiqueta "Proyecto Nuevo" solo está en p. 174. En p. 166 el instituto aparece en una lista de objetivos ("Contar con el Instituto de Planeación…"), sin esa etiqueta. La tabla de la sección 3 del contraste sí lo dice bien.
- Las demás (2) son expresiones propias del estudio entre comillas, no citas.

**Frases del contraste que no están en la lista `CITAS`** (no las cubre la verificación automática; el revisor las encontró a mano y están en su página): "En Acámbaro, el crecimiento urbano ocurre en la periferia de la cabecera municipal y en otras localidades como Irámuco" (PROT, p. 59); "secundaria técnica agropecuaria" (Plan 2006, p. 31); "Plan Municipal 2012-2040" (Plan 2040, p. 106 y 109); los valores +279, +1 048 y +56 del cuadro 3 del PROT (p. 38).

**Afirmaciones de ausencia** ("ninguno menciona…"). El revisor buscó en los cuatro textos:

| Afirmación | Qué se encontró | Se sostiene |
|---|---|---|
| Ninguno menciona la vivienda deshabitada | Programa 2025, Plan 2040 y PROT: nada. **Plan 2006, p. 171**: la ficha de la comunidad Arroyo Colorado dice "Tabique 120 (79 sin habitar)" | Con matiz: ninguno la trata como tema ni la mide para el municipio, pero el Plan 2006 sí la anota en una ficha de comunidad |
| Ninguno mide el equipamiento por distancia | El **PROT (p. 51)** tiene un "grado de accesibilidad a carretera pavimentada" (Acámbaro 94.75 %). No es distancia a escuelas ni a clínicas | Sí, con matiz: el PROT mide accesibilidad a carretera, no a servicios |
| El Programa 2025 es el primero que reconoce la disminución de la población | El **PROT (p. 30)** ya hablaba de "un decremento en sus tasas poblacionales" y proyectaba que la ciudad bajaría a 51 613 (p. 42) | Con matiz: es el primero que reconoce una baja **del municipio en cifras absolutas**; el PROT ya esperaba menos gente en la ciudad |
| Plan 2040: sin "polo", "deshabitad" ni "proyecci" | Confirmado en el OCR | Sí (sobre OCR) |

**Límite de fondo**: las afirmaciones de ausencia en el Plan 2040 y el Programa 2025 descansan en un texto OCR. Que una palabra no aparezca en el OCR no prueba que no esté en el documento (tablas, mapas e imágenes no se leen). El Mapa 4 del Plan 2040 ya se declara ilegible; lo mismo vale, en menor grado, para todo lo demás.
