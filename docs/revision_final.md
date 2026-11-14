# Revisión final independiente (fase 7)

Fecha: 2026-11-14. Revisión externa antes de publicar el sitio y el PDF. **No se corrigió nada**: ni scripts, ni datos, ni textos. Este documento solo reporta.

**Cómo se hizo**
- Todo se volvió a correr en una **copia fuera del repositorio**. En el repositorio el único archivo nuevo es este.
- Las cifras se recalcularon con código propio del revisor, leyendo las tablas de `data/processed/` y, donde se pudo, los archivos originales del INEGI recién bajados (ITER 2000, 2005, 2010 y 2020, Censo 2020 por manzana). No se usaron las funciones de los scripts revisados para comprobarlos.
- Los crudos se bajaron de nuevo: INEGI y JRC con `01_descargar.py`; el release `datos-crudos` (12 archivos) con la API autenticada de GitHub, como pidió Alejandro.
- Orden pedido por Alejandro: primero cifras, consistencia, hallazgos, lenguaje y citas; después reproducibilidad.

---

## 1. Resumen en lenguaje sencillo

**Qué se revisó.** Se volvió a correr todo el análisis desde los datos originales, se rastrearon las cifras de los tres documentos hasta su archivo (94 filas de comprobación; muchas traen varias cifras), se volvieron a verificar las citas de los cuatro planes y se puso a prueba cada uno de los seis hallazgos.

**Lo que está bien**

- **El análisis se reproduce.** De 28 scripts, 27 corrieron sin error con los datos bajados de nuevo, y **todas las tablas, mapas y figuras salieron iguales** a las que están guardadas. Solo falló el script del inventario, que no afecta a ninguna cifra.
- **Las cifras están bien copiadas.** De 94 comprobaciones, 84 coinciden con su archivo, 6 coinciden con un matiz que el texto no dice, 3 no se sostienen y 1 no se puede cotejar (las normas). Ninguna de las cifras de los seis hallazgos está mal.
- **Las citas de los planes están en su página.** 64 de 64, igual que antes. De las 53 frases entre comillas del contraste, 4 necesitan un ajuste pequeño.
- **Los límites principales ya están declarados**: lo rural medido en línea recta, la verificación remota, los tianguis, las normas sin cotejar.

**Lo que hay que corregir antes de publicar**

1. **"Concentración" no es lo que pasó.** Entre 2010 y 2020 la ciudad perdió 1 375 habitantes y el resto del municipio **ganó** 1 042. La ciudad pesa hoy menos que en 2010. Los números del hallazgo 5 están bien; la palabra "concentración" los contradice.
2. **El titular de salud se queda corto y su explicación tiene un hueco.** Las 7 039 personas sin afiliación están bien contadas (el piso seguro es 6 908). Pero el texto dice que solo ellas dependen de las 4 unidades abiertas. No es así: quien en 2020 estaba en el INSABI o el Seguro Popular (23 295 personas en la ciudad) tampoco puede usar el IMSS ni el ISSSTE. Al menos 12 926 de ellas también viven lejos. El grupo afectado es de unas 19 800 personas, no de 7 000.
3. **"Hay aulas suficientes" no es un dato de la ciudad.** Viene de un cuadro del programa regional de 2014 que suma las aulas de cuatro municipios. El estudio no tiene ningún dato de aulas de la ciudad. La otra mitad del hallazgo (32 % lejos de una primaria) sí es firme.
4. **Dos frases dicen lo contrario de los datos**: que el nivel socioeconómico "no se relaciona con la distancia al centro de la ciudad" (en la ciudad sí: baja al alejarse), y que las viviendas deshabitadas subieron "en todos los anillos" (en el de la orilla bajaron).
5. **"El municipio nunca pasó de 110 718 habitantes"** solo vale para los censos. La encuesta de 2015 dio 112 125, y el propio contraste la cita.
6. **Parácuaro**: los documentos dan tres distancias (5.4, 5.5 y 5.6 km) y nombran dos escuelas como "la más cercana". Lo único medido son 4.2 km en línea recta.
7. **"Un ordenamiento que no se ha publicado"** no está comprobado: lo último que se sabe es de julio de 2025.

**Veredicto de los seis hallazgos**

| # | Hallazgo | Veredicto |
|---|---|---|
| 1 | Salud: 7 039 de 11 479 sin afiliación, lejos de una unidad abierta | **Firme con matiz**: el número es sólido y es un piso |
| 2 | Irámuco, Parácuaro y los polos | **Firme con matiz**: "la peor" solo entre las 4 localidades urbanas; de 7 polos, 1 cumple, 2 no y 4 no se pueden evaluar |
| 3 | Aulas suficientes, pero 32 % lejos de una primaria | **Débil** la primera mitad; **firme** la segunda |
| 4 | 24 % de viviendas deshabitadas; Irámuco | **Firme** |
| 5 | La ciudad superó lo proyectado; la subregión bajó | **Firme** en las cifras; **débil** como "concentración" |
| 6 | Cuatro planes repiten, tres prometen, ninguno mide | **Firme con matiz**: falta comprobar que el ordenamiento sigue sin publicarse |

**Qué tan sensibles son los resultados**

- **A los tres umbrales**: los hallazgos 1, 2 y 3 mantienen el sentido con los tres. Las cifras cambian mucho (salud: 75, 61 o 30 %), y eso debe ir siempre junto al número.
- **A los datos ocultos del censo**: poco. En salud, entre 60 y 63 %. Los hallazgos 2 a 5 no dependen de datos ocultos.
- **Al factor 1.33 en lo rural**: los seis hallazgos casi no dependen de él (solo los "5.6 km" de Parácuaro y las distancias de los polos). Las cifras rurales del resumen sí, y mucho: la población rural lejos de salud va de 6 % a 28 % según el factor.
- **A lo no verificado en campo**: las 4 unidades de salud abiertas y los mercados de Chupícuaro y Parácuaro se ven en imágenes. Las primarias y secundarias casi no se revisaron en imagen; descansan en el catálogo de la SEP.

**Qué decide Alejandro**: cómo queda el titular de salud (punto 2), si el hallazgo 5 se sigue llamando "concentración" y si el hallazgo 3 conserva la frase de las aulas. La lista completa está en la sección 9.

---

## 2. Reproducibilidad

**Entorno.** Contenedor nuevo, Python 3.13, librerías de `requirements.txt` instaladas sin cambios de versión. Todo en una copia fuera del repositorio.

**Datos originales.** Se bajaron de nuevo los 41 archivos: 29 del INEGI y del JRC con `01_descargar.py` (sin fallas) y 12 del release `datos-crudos` con la API autenticada de GitHub. La dirección directa que usa el script también responde (se probó con un archivo); el error 401 de la primera prueba fue de una consulta de encabezados, no de la descarga. No se intentó la red de OpenStreetMap, como manda `CLAUDE.md`.

**Resultado.** 28 scripts; **27 corrieron sin error**; 1 falló.

| Script | Corrió | Salidas comparadas con las versionadas |
|---|---|---|
| `01_descargar.py` | sí (por fuentes) | 29 archivos bajados. El release se bajó con la API autenticada |
| `02_recortar.py` | sí | CSV idénticos; 5 GPKG con el mismo contenido |
| `03_base_geografica.py` | sí | idénticas; 3 GPKG con el mismo contenido |
| `04_inventario.py` | **no: falla** | Se detiene con "File is not a zip file". Intenta abrir como ZIP todos los archivos del manifiesto, y desde la fase 2 hay archivos que no lo son (JSON, CSV, PDF). `docs/inventario.md` no se puede regenerar; se quedó en la fase 1 |
| `05_mapa_fase1.py` | sí | figura idéntica |
| `06_catalogo_servicios.py` | sí | idénticas |
| `07_listas_verificacion.py` | sí | Regenera las dos listas sin una columna que añaden `09` y `17`. Después de correr esos dos, quedan idénticas |
| `08_mapa_fase2.py` | sí | figura idéntica |
| `09_catalogo_sep_clues.py` | sí | idénticas |
| `10_redes.py` | sí | mismo contenido |
| `15_catalogo_fase4.py` | sí | idénticas |
| `11_accesibilidad.py` | sí | CSV idénticos; `acceso_cuadras.gpkg` con el mismo contenido (1 658 cuadras, 0 valores distintos) |
| `12`, `13`, `14`, `17`, `18` | sí | idénticas (CSV, KML y 7 mapas) |
| `19_crecimiento.py` | sí | CSV idénticos. Borra dos claves de `validacion_fase4b.json`, que `20` y `22` reponen (ya está avisado en `CLAUDE.md`) |
| `20`, `21`, `22`, `23` | sí | idénticas |
| `24`, `25`, `26` | sí | idénticas |
| `27_salud_abierta.py` | sí | idénticas |
| `28_localidades_y_polos.py` | sí | idénticas |
| `29_vialidades.py` | sí | idénticas |
| `30_planes.py` | sí | idénticas, incluidas las 64 citas y la figura |

**Al terminar la cadena completa**: todos los CSV, JSON, KML, PNG y Markdown generados son **idénticos byte por byte** a los versionados. Los 15 archivos GPKG tienen bytes distintos y **el mismo contenido** (mismas capas, filas, valores y geometrías, comparados uno por uno): el formato guarda la fecha de escritura.

**Qué prueba esto.** Que las tablas guardadas salen de los scripts guardados y de los datos originales, sin pasos a mano, y que nada depende del azar ni del orden. **No prueba** que el método sea correcto; eso es lo que revisan las secciones 3 a 7.

**No corrido**

- `01_descargar.py --solo osm_caminos`: prohibido reintentar (`CLAUDE.md`).
- No existe el `16` (reservado para la red rural).

**Observaciones de reproducibilidad**

1. `04_inventario.py` no corre con los datos actuales (arriba).
2. `data/raw/manifiesto.csv` (tamaño y huella de cada archivo original) no se versiona. Sin él no se puede saber si un archivo bajado dentro de un año es el mismo. Esta vez lo fue, porque las salidas coinciden. La dirección del DENUE no lleva versión: cuando el INEGI publique el siguiente corte, `01` bajará otro archivo y las cifras de abasto cambiarán.
3. El orden importa en tres sitios (`07` antes de `09` y `17`; `19` antes de `20` y `22`; `15` antes de `11`). Está documentado; un solo script que corra todo en orden lo haría más seguro.
4. `07` reescribe `docs/verificar_servicios_muestra.csv`, que `CLAUDE.md` pide no regenerar. En la copia terminó idéntico, pero es un riesgo si alguien corre `07` solo.

---

## 3. Tabla de cifras

Se rastrearon las cifras de `resumen_final.md` (R), `contraste_planes.md` (C) y `metodo.md` (M) hasta el archivo del que salen. "Recalculado" = el revisor volvió a obtener el número con su propio código.

**Resultado general**: 94 filas de comprobación (muchas traen varias cifras). **84 coinciden**; 6 coinciden con un matiz que el texto no dice; **3 no coinciden o no se sostienen** (marcadas **NO**); 1 no se puede cotejar. Ninguna cifra de los seis hallazgos está mal copiada; los problemas están en cómo se interpretan dos de ellas (secciones 5 y 9).

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
| 4 AGEB que se vacían, 1 227 habitantes | R | `tipologia_ageb.csv` | sí. "Orilla oriente" comprobado con las coordenadas de sus cuadras: las 4 quedan de 2.3 a 3.4 km al oriente y suroriente del centro |
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

## 4. Consistencia

### 4.1 La misma cifra con valores distintos

| Qué | Dónde | Valores | Comentario |
|---|---|---|---|
| Población de la ciudad | resumen 1 / resumen 2 y contraste | **56 596** / **56 597** | 56 596 es la suma de cuadras; 56 597 es el ITER. Falta una persona en el censo por manzana. Hay que elegir una y decir por qué la otra difiere |
| Secundaria más cercana a Parácuaro | resumen 1 / contraste 3 y 4 | "la Secundaria Técnica 24, a unos **5.5 km**" / "la más cercana al centro es la Telesecundaria 847, a unos **5.6 km**" / mediana **5.4 km** | Tres cifras y dos escuelas para la misma idea. Las tres salen bien de las tablas, pero miden cosas distintas. El resumen dice además "por camino"; es línea recta × 1.33 |
| Mercado más cercano a Irámuco | resumen 1 y contraste 3 / contraste 4 | **13–18 km** / **15.2 km** | Rango por cuadra y valor desde el centro. Las dos son línea recta × 1.33 (11.4 km en línea recta desde el centro) |
| Sin afiliación en la ciudad | resumen y contraste / ITER | **11 479** / 11 515 | 11 479 es la suma de AGEB con dato. El texto lo presenta como "las personas sin afiliación" de la ciudad |
| Niños de 6 a 11 y personas de 60+ | resumen 1 / ITER | 5 139 y 8 748 / 5 167 y 8 773 | Misma causa: AGEB ocultas. La regla 6 del proyecto pide decir cuánta gente se pierde; aquí no se dice |
| Deshabitadas del municipio | lista de hallazgos / resumen 4 | 24 % / 24.3 % | Solo redondeo |
| Localidades que "cumplen la norma" del centro de salud | resumen 1 / contraste 4 | "las 4" / "las 3 de 2 500 a 10 000" | La norma citada aplica a 3; la ciudad tiene otra regla |
| Hectáreas de cuadras nuevas urbanas | `validacion.md` V39 / resto | 29.3 / 29.2 | Redondeo |
| Citas verificadas | `validacion.md` V58 / V59 | 34 / 64 | V58 quedó con la cifra de antes de la ampliación; V59 la corrige. No es error, pero confunde |

### 4.2 El mismo nombre para cosas distintas, o nombres distintos para lo mismo

- **"No habitadas" y "deshabitadas"** se usan con sentidos distintos (no habitadas = deshabitadas + uso temporal), pero el resumen **nunca define** "no habitadas". En la sección 2 aparecen 26 % de no habitadas y 22 % de deshabitadas para la misma ciudad sin explicación.
- **"Salud pública"** nombra dos cosas: la medida anterior (cualquier unidad pública) y, en la tabla de umbrales, también la abierta. Después de D64 conviene que "salud pública" solo nombre la medida de comparación.
- **"Por camino"**: en lo rural, el resumen escribe "por camino" y "por camino estimado" para lo mismo (línea recta × 1.33). Solo el segundo es correcto.
- **"Bachillerato"**: en la tabla de la ciudad es "bachillerato público" (43 %); primaria, secundaria y preescolar son "todas las escuelas" (con solo públicas serían 38 %, 37 % y 8 %). La tabla mezcla los dos criterios sin avisar. Con todos los bachilleratos, lejos queda 2 %.
- **"Promedio"** en los ejemplos del índice socioeconómico: son medianas entre AGEB.
- **"Manzana" y "AGEB"** aparecen en el resumen (limitación 2). Es documento de trabajo, pero la sección 6 se va a copiar al sitio: ahí debe decir "cuadra" (regla del proyecto).

### 4.3 Textos que no siguen una decisión vigente

| Decisión | Qué pide | Qué dice el texto |
|---|---|---|
| **D64** (la medida principal de salud es la abierta) | Que el titular y la medida principal sean salud abierta | Tres análisis siguen usando la medida anterior sin decirlo: los grupos de edad ("1 730 personas de 60 y más lejos de salud pública"), la **tipología** de AGEB (D47) y el cruce con el **índice socioeconómico**. En la ciudad la diferencia es de 22 % a 58 %, así que la tipología y el cruce cambiarían. El resumen dice "sin cambios" (sección 8.8), que es cierto, pero no dice que quedaron con la medida que ya no es la principal |
| **D35** (redacción de Irámuco) | "no hay mercado ni supermercado registrado; puede existir un tianguis que ninguna fuente captura" | El resumen (línea de Irámuco) y el contraste (fila de Irámuco y síntesis) dicen solo "no hay / no tiene mercado ni supermercado registrado", sin la segunda mitad. La tabla de polos sí la trae |
| **D39** (Parácuaro) | "no hay secundaria dentro de la localidad"; la atiende la ST 24 | El contraste dice que la más cercana al centro es la Telesecundaria 847. No contradice a D39, pero el lector ve dos escuelas "más cercanas" |
| **D49** (cuadras nuevas con conteos, no porcentajes) | En textos públicos, conteos | El resumen usa "48 % contra 13 %". Es documento de trabajo y D49 lo permite; al pasar al sitio hay que cambiarlo |
| **D62** (sin cifras aproximadas de los planes) | Cifras con página y cuadro | Se cumple. "Unos 57 960" y "unas 11 900" son cálculos del estudio, no cifras de los planes |
| **D66** (no decir que el Plan 2040 abandonó los polos) | — | Se cumple |
| **D56** (lo rural del índice como indicio) | — | Se cumple |
| **D52** (el GHSL no es vivienda) | — | Se cumple |
| Regla 6 de `CLAUDE.md` (decir cuánta población se pierde por el "*") | En cada paso | No se dice en los denominadores de 4.1 (11 479, 5 139, 8 748) |

### 4.4 Otros

- Los encabezados de `resumen_final.md` y `metodo.md` remiten a "D01–D63" y "V1–V58". Las decisiones llegan a D67 y las validaciones a V59.
- La síntesis del contraste pone "Proyecto Nuevo (p. 166 y 174)"; ver sección 8.
- La sensibilidad "solo confirmadas" (D28) da por confirmada toda sede que esté en el DENUE. Por eso **no pone a prueba la clínica del ISSSTE**, que el catálogo marca "no confirmada" y la CLUES "fuera de operación" (D36). No afecta al titular de salud; sí a la comparación del 22 %, que nadie recalculó sin esa clínica.

---

## 5. Los seis hallazgos

Veredictos: **firme** = se sostiene como está escrito; **firme con matiz** = el dato es sólido, pero la frase dice algo más de lo que el dato permite; **débil** = la frase, como está escrita, no se sostiene.

| # | Hallazgo | Veredicto |
|---|---|---|
| 1 | Salud | **Firme con matiz** (el número es sólido; se queda corto y falta decir a quién deja fuera) |
| 2 | Localidades | **Firme con matiz** |
| 3 | Ciudad: aulas y primaria | **Débil** en la primera mitad; **firme** en la segunda |
| 4 | Vivienda | **Firme** |
| 5 | Concentración | **Débil** como "concentración"; **firme** en las cifras |
| 6 | Planes | **Firme con matiz** |

### Hallazgo 1. Salud

> En la ciudad, 7 039 de las 11 479 personas sin afiliación (61 %) viven lejos de una unidad abierta a toda la población.

**Evidencia.** `acceso_salud_abierta.csv` y `salud_abierta_resumen.csv`. Recalculado por el revisor cuadra por cuadra: 32 660 personas a más de 1 330 m a pie de las 4 unidades de la Secretaría de Salud; de ellas, 6 908 sin afiliación contadas a la vista.

**Tres umbrales.** 75 / 61 / 30 %. El sentido se mantiene con los tres; la cifra cambia mucho (de 8 634 a 3 416 personas). A 100 m por debajo y por encima del umbral principal hay 584 y 471 personas sin afiliación: la cifra no está parada sobre un borde.

**Valores ocultos.** Poca dependencia. 7 039 es una estimación por AGEB (D10). El piso seguro es **6 908** (lo que se ve cuadra por cuadra). El techo es 7 281 (si las 373 personas ocultas vivieran todas lejos). En porcentaje: entre 60 y 63 %. El denominador 11 479 deja fuera 36 personas de AGEB ocultas (el ITER da 11 515).

**Factor 1.33 rural.** No interviene: es la ciudad, medida por calles. Sí interviene la otra aplicación del 1.33: el umbral principal (1 330 m) es el radio de la norma multiplicado por 1.33. Si la norma se refiriera a distancia recorrida, valdría el estricto (75 %).

**Unidades no verificadas.** Las 4 unidades abiertas están confirmadas por la CLUES y se ven en Street View o satélite. Lo que falta es de campo: que funcionen y que atiendan a cualquier persona (`verificar_campo_fase6.csv`). La clínica del ISSSTE, que la CLUES da como fuera de operación (D36), **no afecta** a este hallazgo, porque no cuenta como abierta; solo afecta a la comparación del 22 %.

**Lo que el texto no dice y debería (matiz principal).** El resumen y el contraste explican que "quien está afiliado al IMSS o al ISSSTE sí puede usar esas clínicas; quien no tiene afiliación, no", y que "la diferencia es real solo para quien no tiene afiliación". Eso deja fuera al grupo más grande. En el Censo 2020, la ciudad tiene:

| Afiliación (Censo 2020, localidad 0001) | Personas |
|---|---:|
| IMSS | 16 258 |
| ISSSTE (federal y estatal) | 5 370 |
| **INSABI / Seguro Popular** | **23 295** |
| IMSS-Bienestar | 152 |
| **Sin afiliación** | **11 515** |

Quien estaba afiliado al INSABI o al Seguro Popular **tampoco puede usar las clínicas del IMSS ni del ISSSTE**: se atiende en las mismas 4 unidades abiertas. El revisor contó, cuadra por cuadra, **12 926 afiliados al INSABI a más de 1 330 m de una unidad abierta** (57 % de los 22 811 visibles). Es decir: las personas que dependen de las unidades abiertas y viven lejos de una son, como mínimo, unas **19 800** (6 908 + 12 926), no 7 039. El titular no está mal; es el piso de un grupo casi tres veces mayor.

**Otros matices.** (a) "Unidad" no dice capacidad: una de las 4 tiene 11 consultorios y otras dos tienen 2. (b) Los consultorios de farmacia no cuentan; el texto ya lo dice. (c) El censo es de 2020 y el INSABI ya no existe; la gente sigue dependiendo de las mismas unidades.

**Redacción más fuerte que los datos permiten.**
> En la ciudad de Acámbaro, al menos 6 900 de las 11 500 personas sin ninguna afiliación (6 de cada 10) viven a más de 1.3 km a pie de las cuatro unidades de salud que atienden a cualquier persona. Lo mismo les pasa a unas 12 900 personas que en 2020 estaban afiliadas al INSABI o al Seguro Popular, que tampoco pueden usar las clínicas del IMSS ni del ISSSTE.

### Hallazgo 2. Localidades

> Irámuco es la peor servida (80 % lejos de una primaria, sin mercado registrado); Parácuaro no tiene secundaria (la más cercana a unos 5.6 km); de los 7 polos rurales del plan de 2006, solo Chupícuaro cumple la meta.

**Evidencia.** `acceso_resumen_por_localidad.csv`, `polos_desarrollo.csv`, `localidades_2500.csv`, `servicios_sedes_fase4.csv`.

**Irámuco.**
- Primaria: 88 / 80 / 56 % con los tres umbrales. Firme. Sus 2 primarias están confirmadas por la SEP; con solo confirmadas y con solo públicas la cifra no cambia. No depende de valores ocultos (la población total por cuadra no se oculta).
- Mercado: el catálogo trae 108 tiendas de abarrotes y ningún mercado ni supermercado. 100 % lejos con cualquier umbral y con cualquier factor (el más cercano está a 11.4 km en línea recta). Pero **"sin mercado registrado" no es "sin abasto"**: ninguna fuente registra tianguis (D35).
- "**La peor servida**": se sostiene **entre las 4 localidades urbanas**. Irámuco es la peor en 4 de los 5 servicios básicos (mercado 100 %, primaria 80 %, salud 64 %, preescolar 25 %); en secundaria la peor es Parácuaro. No se comparó con las 208 localidades rurales, que se miden de otra forma. Dicho sin ese límite, "la peor servida" es más de lo que los datos permiten.
- Hay una tensión que el reporte debe explicar: la tabla de polos dice que Irámuco "sí" tiene preescolar, primaria, secundaria, bachillerato y salud. Las dos cosas son ciertas: los servicios existen dentro del pueblo, pero la mayoría de su gente vive a más de 670 m de una primaria.

**Parácuaro.**
- "No tiene secundaria dentro de la localidad": firme. No hay ninguna en SEP, Marco Geoestadístico ni DENUE. No depende de umbrales ni del factor.
- "A unos 5.6 km": es **línea recta (4.2 km) × 1.33**. La distancia real por carretera no se midió. Con factor 1.2 serían 5.1 km; con 1.5, 6.3 km. Lo único medido es 4.2 km en línea recta.
- Los documentos dan tres cifras para lo mismo: 5.5 km (resumen, a la ST 24), 5.6 km (contraste, a la Telesecundaria 847 desde el centro) y 5.4 km (mediana por persona). Y nombran dos escuelas distintas como "la más cercana". Ver 4.1.
- Las dos secundarias cercanas están confirmadas por la SEP; ninguna se revisó en imagen. La ubicación de la ST 24 es justo lo que está pendiente de campo.

**Polos.**
- "Solo Chupícuaro cumple" es verdad **con lo que registran las fuentes**, pero el resultado completo es: 1 cumple, 2 no cumplen (Parácuaro e Inchamácuaro) y **4 no se pueden evaluar** por el abasto. Decir solo "de 7, 1 cumple" hace pensar que 6 fallan.
- Chupícuaro cumple con una sola sede de cada cosa: una telesecundaria, un bachillerato SABES, una UMAPS y un mercado de 6 locales. El mercado, el bachillerato y la UMAPS se ven en imagen; la telesecundaria solo está confirmada por la SEP.
- En 3 polos (San Mateo Tócuaro, Chamácuaro y Arroyo de la Luna) el "sí" de bachillerato es un **telebachillerato o videobachillerato** que solo registra la SEP, sin revisión en imagen. El plan de 2006 pedía "nivel medio superior", así que cuentan; conviene decirlo.
- Que Inchamácuaro "no tiene" bachillerato ni salud es firme (no hay sede dentro). Sus distancias (3.3 y 3.7 km) son línea recta × 1.33.
- La "sede" de cada polo es la localidad que da nombre al eje; el plan no lo dice (D60). Es un supuesto del estudio.

**Veredicto: firme con matiz.**

**Redacción más fuerte.**
> De las cuatro localidades urbanas, Irámuco es la peor servida: 8 de cada 10 habitantes viven a más de 670 m a pie de una primaria y no hay mercado ni supermercado registrado (puede haber un tianguis que ninguna fuente capta). Parácuaro no tiene secundaria dentro del pueblo; las dos más cercanas están a unos 4 km en línea recta. De los 7 polos rurales del plan de 2006, Chupícuaro tiene todo lo que el plan pedía; a Parácuaro y a Inchamácuaro les falta algo, y en los otros 4 no se puede saber porque no hay registro de tianguis.

### Hallazgo 3. Ciudad

> Hay aulas suficientes en total, pero el 32 % vive lejos de una primaria.

**Segunda mitad: firme.** 17 853 personas (31.5 %) a más de 670 m a pie de una primaria; 55 / 32 / 10 % con los tres umbrales. No depende de valores ocultos ni del factor rural. La cifra es más bien **conservadora**: cuenta todas las primarias, incluidas 5 privadas y 2 puntos sin confirmar que probablemente no son primarias ("UTL" y "Jardín de Niños Fray Pedro de Gante"). Con solo confirmadas, 35 % (19 654); con solo públicas, 38 % (21 460). Solo 2 de las 24 primarias de la ciudad se revisaron en imagen; 20 están confirmadas por la SEP.

**Primera mitad: débil.** "Aulas suficientes en total" sale del cuadro 3 del PROT (p. 38), que el revisor leyó en el PDF: 1 499 aulas de primaria existentes contra 451 necesarias. Ese cuadro es de **la subregión completa** (4 municipios, 189 535 habitantes), con datos de alrededor de 2014. No hay en el repositorio ningún dato de aulas, grupos ni matrícula **de la ciudad**, ni actual. El hallazgo junta una cifra de la subregión con una de la ciudad como si fueran del mismo lugar. Además, el Plan 2040 dice lo contrario para el municipio (menos escuelas por habitante que el estado, p. 158); el propio contraste lo reconoce.

**Otros matices.** Distancia no es cupo: el estudio mide dónde está la escuela, no si tiene lugar ni cuántos turnos. Y quien "vive lejos" es toda la población; niñas y niños de 6 a 11 años son 1 700 (mínimo visible 1 583).

**Redacción más fuerte.**
> En la ciudad, una de cada tres personas (32 %) vive a más de 670 m a pie de una primaria; entre ellas, unas 1 700 niñas y niños de 6 a 11 años. El programa regional de 2014 calculó que en la subregión sobraban aulas de primaria: contar aulas en total no dice si están cerca de donde vive la gente.

### Hallazgo 4. Vivienda

> 24 % de las viviendas del municipio está deshabitada; en Irámuco, 2010–2020, población +5 %, viviendas +27 %, deshabitadas de 356 a 658.

**Evidencia.** Recalculado de los ITER 2010 y 2020 bajados del INEGI. Municipio 2020: 11 130 deshabitadas de 45 739 viviendas = 24.3 %. Irámuco: 5 954 → 6 275 (+5.4 %); 1 839 → 2 336 viviendas (+27.0 %); 356 → 658 deshabitadas.

**Umbrales, ocultos, factor, verificación.** Nada de eso interviene: son totales de localidad publicados por el censo, sin "*". Las cifras de 2010 por manzana sí están ocultas en 9 de cada 10, pero este hallazgo no las usa.

**Matices.**
- "Deshabitada" es la definición del censo el día del levantamiento. No incluye las de uso temporal (otro 9.7 %). Con las dos, 34 % de las viviendas del municipio no están habitadas.
- Contexto que cambia la lectura: 24.3 % es **el más bajo de los 7 municipios de la región** (24.4 a 30.9 %), aunque muy por encima de Guanajuato (15.7 %).
- En Irámuco, las habitadas también crecieron (1 218 → 1 444). De 497 viviendas más, 302 son deshabitadas más. Los datos no dicen que las vacías sean las nuevas (ver 7).

**Veredicto: firme.** La frase ya es la más fuerte que los datos permiten. Solo convendría decir "en 2020".

### Hallazgo 5. Concentración

> La ciudad superó en 2020 lo proyectado para 2030 (56 597 contra 51 613); la subregión bajó 1.4 % frente a +5.07 % proyectado.

**Las cifras: firmes.** 56 597 y los totales de la subregión salen del ITER (recalculados). 51 613 y +5.07 % están en el PROT (p. 42 y 59, leídos en el PDF). La cifra de la ciudad es comparable (misma localidad).

**La palabra "concentración": no se sostiene.** El resumen dice: "Es concentración en la ciudad y pérdida en el resto". Los censos dicen otra cosa:

| | 2010 | 2020 | Cambio |
|---|---:|---:|---:|
| Ciudad | 57 972 | 56 597 | **−1 375** (−2.4 %) |
| Resto del municipio | 51 058 | 52 100 | **+1 042** (+2.0 %) |
| Parte de la ciudad en el municipio | 53.2 % | 52.1 % | baja |
| Parte de la ciudad en la subregión | 31.6 % | 31.3 % | baja |

Entre 2010 y 2020 **la ciudad perdió y el resto del municipio ganó**. La ciudad pesa hoy menos que en 2010, no más. La concentración solo aparece si se compara con 2000 (ciudad 55 516, 50.1 % del municipio), y todo ese cambio ocurrió antes de 2010. Quien perdió fueron los otros tres municipios de la subregión (−3.0 %).

**"Superó lo proyectado".** El PROT proyectaba que la ciudad **bajaría**. Estar en 2020 por encima de una meta de baja para 2030 es casi inevitable: en línea recta de 2010 a 2030, en 2020 le tocarían unos 54 800. Lo que sí se puede decir es que la ciudad bajó más despacio de lo proyectado (1 375 en diez años, contra unos 3 200 que pedía ese ritmo). El resumen ya lo califica de "moderada"; el hallazgo, tal como está en la lista, no.

**Subregión.** −1.4 % contra +5.07 %: firme. Dos avisos: el PROT se contradice (da más población para 2014 que para 2016; el contraste lo declara), y el resumen dice que el municipio "nunca pasó de 110 718", lo que solo vale para los censos: la Encuesta Intercensal 2015 dio 112 125, casi igual a lo que el PROT esperaba para 2014 (112 076). La caída se ve entre 2015 y 2020.

**Umbrales, ocultos, factor, verificación.** No intervienen. La EIC 2025 de la ciudad (56 771) tiene un intervalo de ±10 %: no sirve para decir si subió o bajó.

**Veredicto: débil como "concentración"; firme en las cifras.**

**Redacción más fuerte.**
> El programa regional de 2014 esperaba que la subregión creciera 5 % entre 2010 y 2020; bajó 1.4 %. Para la ciudad esperaba una baja hasta 51 613 habitantes en 2030; en 2020 tenía 56 597: perdió población, pero más despacio de lo previsto. Entre 2010 y 2020 la ciudad perdió 1 375 habitantes y el resto del municipio ganó 1 042.

### Hallazgo 6. Planes

> Cuatro documentos (2006–2025) repiten los diagnósticos; tres prometen un ordenamiento que no se ha publicado; ninguno mide dónde están los servicios.

**"Repiten los diagnósticos": con matiz.** No son los cuatro en cada tema. Migración: los cuatro (verificado). Irámuco y Parácuaro como casos aparte: tres (el Plan 2040 "no los trata por separado", según el propio contraste). Poco equipamiento en las localidades: explícito en 2006 y 2025.

**"Tres prometen un ordenamiento": firme.** 2006 (p. 241, plazo de 6 meses), 2015 (p. 172 y 174) y 2025 (p. 60 y 68). Las tres citas están en su página. El PROT es, él mismo, un programa de ordenamiento, pero regional.

**"Que no se ha publicado": no comprobado.** Lo único que hay es que el Programa de julio de 2025 dice que "se encuentra en elaboración". Nadie revisó el Periódico Oficial entre agosto de 2025 y hoy (noviembre de 2026). El propio contraste deja como "no verificado" que podría estar en revisión del IPLANEG. Además, el Plan 2006 (p. 241) habla de "actualizar y evaluar el Plan Director de Desarrollo Urbano": en 2006 ya existía un instrumento urbano anterior, que el contraste no menciona.

**"Ninguno mide dónde están los servicios": firme con matiz.** Ninguno mide distancia a escuelas, clínicas o mercados. Pero el Plan 2006 sí dice dónde están por micro región y por comunidad (fichas, p. 60, 64 y 171), y el PROT mide accesibilidad a carretera pavimentada (p. 51). Más exacto: "ninguno mide a qué distancia vive la gente de los servicios".

**Dependencia del OCR.** Todo lo del Plan 2040 y del Programa 2025 se leyó en un OCR. Las 30 citas positivas están en su página. Las afirmaciones de ausencia ("no menciona", "no hay acciones para construir…") son las más frágiles: una tabla o un mapa mal leído no aparece en la búsqueda.

**Veredicto: firme con matiz.**

**Redacción más fuerte.**
> Los cuatro documentos, de 2006 a 2025, señalan la migración; tres prometen un instrumento municipal de ordenamiento territorial (2006, 2015 y 2025), que en julio de 2025 seguía en elaboración según el propio Programa de Gobierno. Ninguno mide a qué distancia vive la gente de las escuelas, las clínicas o los mercados.

---

## 6. Límites que el reporte debe declarar

### Los que pidió revisar Alejandro

| Límite | ¿Está declarado? | Qué falta |
|---|---|---|
| Distancias rurales en línea recta × 1.33 | Sí (resumen 1 y 6; método 1; D26) | Decir **cuánto** pesa. Recalculado por el revisor, población rural lejos según el factor (1.0 / 1.2 / **1.33** / 1.5): salud 6 % / 12 % / **17 %** / 28 %; mercado 17 % / 34 % / **40 %** / 49 %; secundaria 0.2 % / 2 % / **3 %** / 9 %. Las cifras rurales se duplican o se reducen a la mitad con cambios razonables del factor. El 1.33 se calibró con las calles de la ciudad, no con caminos rurales |
| Verificación remota y no en campo | Sí (resumen 6.9; D13, D41) | Decir que solo se revisaron 68 de unas 300 sedes de escuelas y salud, que no fue al azar, y que entre las revisadas 1 de cada 4 no se vio |
| Fechas de los catálogos frente al Censo 2020 | Sí, en general (resumen 6.1; método 1) | Falta decir: (a) el catálogo SEP **no tiene fecha de corte** (D40); (b) la CLUES de agosto de 2026 da como fuera de operación la clínica del ISSSTE que el estudio cuenta (D36); (c) son 6 años entre la población y los servicios |
| Tianguis que ninguna fuente captura | Sí (resumen 1 y 6.4; método 3; D35) | Bien declarado. Mantenerlo pegado a cada frase sobre mercados, no solo en la lista de límites |
| Normas no cotejadas | Sí (método 2; resumen 9) | Bien declarado. Es el límite que más pesa en la ciudad: todos los umbrales salen de radios que nadie del proyecto ha visto en el documento original, y de un supuesto (que el radio es en línea recta) que la norma no dice |
| Citas sobre OCR | Sí (contraste, encabezado; D65) | Falta separar: las citas **positivas** están verificadas; las afirmaciones de **ausencia** sobre OCR no se pueden verificar del todo |

### Los que faltan

1. **"Sin afiliación" no es todo el que depende de las unidades abiertas.** En el Censo 2020, la afiliación al INSABI o al Seguro Popular cuenta como "con afiliación". En la ciudad son 23 295 personas, el doble de las que no tienen ninguna (hallazgo 1).
2. **La distancia no mide capacidad ni calidad.** Una escuela cerca puede no tener cupo; una unidad de salud puede tener 2 consultorios u 11, o no tener médico ese día. El estudio mide dónde está el servicio, nada más.
3. **El umbral principal lleva dentro un supuesto.** Multiplicar el radio de la norma por 1.33 da por hecho que la norma habla de línea recta. Si hablara de distancia recorrida, todas las cifras de la ciudad serían las del umbral estricto (primaria 55 % en vez de 32 %; salud abierta sin afiliación 75 % en vez de 61 %).
4. **"Lejos" es a pie.** En la ciudad no se considera transporte público, bicicleta ni automóvil. El bachillerato a 3.3 km a pie y la primaria a 670 m no son la misma clase de "lejos".
5. **Cinco rutas de control.** La comparación con Google Maps son 5 rutas elegidas, 4 en la ciudad. No hay ningún control de las distancias rurales.
6. **Muchas correlaciones, pocos casos.** En el vaciamiento se probaron 54 correlaciones; con 42 AGEB en la ciudad, algunas saldrían "moderadas" por azar. Las que se destacan (0.41, −0.36, 0.38) no se corrigieron por eso.
7. **Vivienda "deshabitada" es una foto del día del censo.** Marzo de 2020. No distingue casa abandonada de casa en venta o en renta, ni de casa de migrante que vuelve.
8. **Las AGEB de 2010 y 2020 no son las mismas.** La comparación por anillos y por AGEB usa "unidades comparables" armadas por el estudio (D44), que cubren 92 % de las viviendas de la ciudad.
9. **Las proyecciones del PROT son de CONAPO sobre el Censo 2010.** Compararlas con el censo de 2020 dice que la proyección no se cumplió, no por qué.
10. **La Encuesta Intercensal 2015 no está en el estudio.** Daba 112 125 habitantes al municipio. Sin ella, la serie parece plana entre 2010 y 2020; con ella, sube y luego cae.
11. **El polo se evalúa en su localidad sede**, que el plan de 2006 no nombra (D60). Y "tiene" significa "hay al menos una sede dentro", aunque sea un telebachillerato.
12. **El estado del ordenamiento municipal no se consultó** después de julio de 2025.
13. **El 2005 es un conteo**, no un censo, y dio cifras bajas en toda la región. El contraste lo dice; la gráfica debe decirlo también.

---

## 7. Lenguaje

### 7.1 Causa donde solo hay coincidencia

| Dónde | Frase | Por qué excede los datos | Alternativa |
|---|---|---|---|
| Resumen 2, rural | "Es el patrón de pueblos que envejecen y donde quedan casas vacías o de quien vive fuera" | Es una correlación de 2020 entre 93 localidades (más gente mayor, más casas no habitadas). No hay dato de que esos pueblos estén envejeciendo ni de quién son las casas | "Las localidades con más personas mayores tienen más viviendas no habitadas" |
| Resumen 2, ciudad | "Esto apunta a que, en la ciudad, la vivienda vacía está también en zonas de la orilla que crecieron" | Salta de una correlación con "gente nacida en otro estado" a una lectura espacial que esa correlación no muestra. Además son 42 AGEB y 54 correlaciones probadas | Dar el dato de los anillos (que sí lo muestra) y dejar la correlación como lo que es |
| Resumen 2, Irámuco; contraste, Irámuco | "buena parte de las casas nuevas quedó vacía"; "Hubo crecimiento habitacional, pero buena parte quedó vacía" | El censo dice que hay 497 viviendas más y 302 deshabitadas más. No dice que las vacías sean las nuevas | "Las viviendas aumentaron en 497 y las deshabitadas en 302" |
| Contraste, ordenamiento (dos veces) | "Lo que muestran los datos es lo que un instrumento así busca evitar"; "Mientras tanto: vivienda nueva sin gente nueva…" | Sugiere que la falta del instrumento explica el vaciamiento. No hay nada en el estudio que lo pruebe; y toda la región muestra lo mismo | Poner los dos hechos uno junto al otro sin unirlos |
| Contraste, vivienda | "El problema de hoy no es la falta de casas, sino las casas vacías" | Es una conclusión. Puede haber déficit y casas vacías a la vez (vivienda que no es de quien la necesita). El estudio no midió déficit | "En 2020 había 11 130 viviendas deshabitadas" |
| Resumen 7; contraste, la ciudad | "Es concentración en la ciudad y pérdida en el resto"; "se concentró población en la ciudad y se perdió en el resto" | Lo contradicen los censos de 2010 y 2020 (hallazgo 5) | Ver redacción del hallazgo 5 |
| Resumen 3 | "confirma lo que viste" | Que 67 localidades no ganaran población es compatible con la lectura de Alejandro; no la confirma por sí solo | "concuerda con lo que se ve en las imágenes" |
| Resumen 3 | "la diferencia con las viejas se explica sobre todo por estar en la orilla" | Es una comparación por anillos, no una explicación | "la diferencia casi desaparece al comparar con cuadras viejas a la misma distancia del centro" |
| Resumen 4 | "las viviendas crecieron 11–17 % sin gente nueva" | Correcto para el saldo; pero "sin gente nueva" no se sabe (puede haber llegado y salido gente) | "sin que creciera la población" |
| Contraste, educación | "Uno ve superávit y otro déficit **porque** los dos miden en total" | Además miden lugares distintos (subregión y municipio), en años distintos y contra referencias distintas. No es solo eso | Quitar el "porque" |
| Resumen 5 | "Pero buena parte se debe a Irámuco" | Aquí es aritmética (composición del quintil), no causa. Se sostiene | — |

### 7.2 Adjetivos y adverbios que los datos no sostienen

| Dónde | Frase | Observación |
|---|---|---|
| Resumen 1, título | "Las otras localidades urbanas: **lo más claro del estudio**" | Es una opinión. Lo más firme del estudio son los totales censales |
| Lista de hallazgos | "Irámuco es **la peor servida**" | Solo entre las 4 localidades urbanas (hallazgo 2) |
| Resumen 2 | "La pérdida de población **se concentró** en el primer kilómetro" | El anillo de 0 a 500 m ganó 97 personas. La pérdida está entre 500 m y 1.5 km (−2 190 y −1 280) |
| Resumen 2 | "subió en **todos** los anillos" | No en el de 3.5 a 4 km (sección 3.3) |
| Resumen 4 | "en viviendas vacías está **un poco mejor** que sus vecinos" | 24.3 contra 24.4 % de Salvatierra: empate. "Mejor" es además un juicio |
| Resumen 7 | "el municipio **nunca** pasó de 110 718" | Solo en censos (sección 3.6) |
| Contraste, Irámuco | "la población **apenas** volvió a su nivel de 2000" | 6 275 contra 6 232: volvió y lo pasó por 43. Sobra "apenas" |
| Resumen 3 | "**Firme** (aparece con los tres umbrales)" para el preescolar de las cuadras nuevas | Con el holgado, el efecto son las 58 personas de las 6 cuadras de Chupícuaro; en la ciudad se invierte (0 % contra 7 %) |
| Resumen 1 | "**Firme**" para "a unos 5.5 km por camino" | Lo firme es que no hay secundaria dentro. La distancia es una estimación |
| Resumen 5 | "no se relaciona con la distancia al centro" | Falso en la ciudad (sección 3.5) |
| Contraste, encabezado | "repiten **los mismos** diagnósticos" | No los cuatro en cada tema (hallazgo 6) |
| Contraste, acciones | "**No hay** acciones para construir unidades de salud, escuelas o mercados" | Afirmación de ausencia sobre OCR. Mejor: "no se encontraron" |

### 7.3 Lo que está bien

El resumen avisa al principio que todo es descriptivo, titula la sección como "correlaciones entre áreas, no causas", presenta lo rural del índice como indicio y no extrapola el GHSL. El contraste dice que no evalúa a ninguna administración y marca lo no verificado. El problema no es de tono general: son las frases sueltas de arriba.

---

## 8. Citas de los planes

**Verificación automática, vuelta a correr.** `src/30_planes.py` corrió sin errores en la copia, con los cuatro documentos bajados de nuevo del release. Sus salidas son **idénticas byte por byte** a las versionadas: `docs/verificar_citas_planes.csv` (**64 de 64** citas en su página), `iramuco_serie.csv`, `proyecciones_vs_censo.csv`, `verificar_campo_fase6.csv`, `validacion_fase6.json` y la figura.

**Qué prueba y qué no prueba esa verificación.** Busca la frase exacta en la página indicada. Es estricta: no acepta frases parecidas. Pero solo comprueba que la frase **está**; no comprueba que el texto que la rodea diga lo que el contraste le hace decir.

**Segunda verificación, del revisor.** Con un programa aparte se buscaron las 53 frases entre comillas de `contraste_planes.md` y las de la sección 7 del resumen en los cuatro documentos. Resultado:

- **47 aparecen tal cual** en la página citada (2 de ellas partidas por un corchete o por las columnas de una tabla).
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

---

## 9. Observaciones clasificadas

### (a) Errores que hay que corregir

1. **"Concentración" (hallazgo 5; resumen 7; contraste, fila "La ciudad").** Entre 2010 y 2020 la ciudad perdió 1 375 habitantes y el resto del municipio ganó 1 042; la ciudad pesa menos que en 2010. No hubo concentración en esa década. Las cifras del hallazgo están bien; la interpretación no.
2. **"El índice no se relaciona con la distancia al centro de la ciudad (−0.03)" (resumen 5).** El −0.03 mezcla las 4 localidades. En la ciudad sola es −0.58: el índice baja al alejarse del centro. La frase dice lo contrario de lo que muestran los datos de la ciudad.
3. **"El municipio nunca pasó de 110 718" (resumen 7).** La Encuesta Intercensal 2015 dio 112 125, y el propio contraste la cita. O se dice "en un censo" o se incluye 2015.
4. **"El % de deshabitadas subió en todos los anillos" (resumen 2; `resumen_fase4b.md`).** En el anillo exterior bajó.
5. **Hallazgo 3, "hay aulas suficientes en total".** El dato es de la subregión (PROT, cuadro 3), no de la ciudad. Como está escrito, afirma algo de la ciudad que ningún dato del estudio respalda.
6. **Explicación del titular de salud (resumen 1 y contraste).** "La diferencia es real solo para quien no tiene afiliación" no es correcto: 23 295 personas afiliadas al INSABI o al Seguro Popular dependen de las mismas 4 unidades, y al menos 12 926 de ellas viven lejos. El titular puede quedarse; la explicación y la magnitud deben corregirse.
7. **Parácuaro: dos escuelas y tres distancias** (4.1). Elegir una frase y usarla en todos lados. "Por camino" no es correcto.
8. **Cuatro citas que no son literales o no están en la página** (sección 8): CONAPO (p. 34), "en al ámbito" (p. 61), "un interacción" (p. 59) y "Proyecto Nuevo" (p. 166).
9. **"Que no se ha publicado" (hallazgo 6).** No está comprobado después de julio de 2025. O se comprueba en el Periódico Oficial, o se escribe "en julio de 2025 seguía en elaboración".

### (b) Matices de redacción

1. Dar el titular de salud con su piso: "al menos 6 908" o "unas 7 000 (entre 6 900 y 7 300)", y decir que 11 479 es el total con dato (11 515 en el ITER).
2. "La peor servida": añadir "de las 4 localidades urbanas".
3. Polos: decir 1 cumple, 2 no, 4 no se pueden evaluar; y que en 3 polos el bachillerato es un telebachillerato o videobachillerato.
4. Irámuco: usar siempre la redacción completa de D35 (con el tianguis).
5. Irámuco: explicar por qué "tiene" primaria en la tabla de polos y a la vez 80 % vive lejos de una.
6. Primaria en la ciudad: decir que 32 % cuenta todas las primarias; con solo públicas, 38 %.
7. Tabla de la ciudad: avisar que bachillerato es "público" y los demás niveles "todas".
8. Preescolar de las cuadras nuevas: no llamarlo "firme con los tres umbrales".
9. Definir "no habitadas" la primera vez.
10. "Ninguno menciona la vivienda deshabitada": el Plan 2006 tiene una ficha con "79 sin habitar" (p. 171). Mejor "ninguno la trata como tema".
11. "El Programa 2025 es el primero que reconoce la disminución": el PROT ya proyectaba la baja de la ciudad.
12. Pérdida de población "en el primer kilómetro": es de 500 m a 1.5 km.
13. Las frases de 7.1 y 7.2.
14. Deshabitadas: decir que 24.3 % es el más bajo de la región, empatado con Salvatierra.
15. Ejemplos del índice: son medianas.
16. Encabezados: D01–D67 y V1–V59. Unificar 56 596 y 56 597.
17. Al pasar a textos públicos: "cuadra" y no "manzana"; conteos y no porcentajes en las cuadras nuevas (D49).
18. Las afirmaciones de ausencia en los planes escaneados: "no se encontró" en lugar de "no hay".

### (c) Pendientes para la versión 1.1

1. **Población que depende de las unidades abiertas**: sumar sin afiliación, INSABI / Seguro Popular e IMSS-Bienestar, con el método D10, y reportarla junto al titular. Decisión de Alejandro.
2. **Tipología e índice socioeconómico con salud abierta** (hoy usan la medida anterior, 4.3).
3. **Sensibilidad del factor rural** en una tabla propia (1.0, 1.2, 1.33, 1.5), como la que se usó aquí en la sección 6.
4. **Red de caminos rural** (RNC), que sigue pendiente.
5. **Encuesta Intercensal 2015** en la serie de población y en la gráfica de proyección.
6. **Aulas, grupos o matrícula de la ciudad** (estadística 911 de la SEP), si se quiere sostener la primera mitad del hallazgo 3.
7. **Cotejo de las normas** (SEDESOL 1999, SEDATU 2024, NOM-002).
8. **Campo**: las 4 unidades abiertas, la ST 24, Monte Prieto, el Mercado 22 de Octubre, y los telebachilleratos de los polos.
9. **Estado del PMDUOET** en el Periódico Oficial.
10. **Sensibilidad sin la clínica del ISSSTE** para la comparación del 22 %.
11. **Agregar a `CITAS`** las frases del contraste que hoy no se verifican solas (sección 8).
12. **Superficie construida por habitante en 2000 y 2005** (D67, ya anotado).
13. **Correlaciones del vaciamiento**: reportar cuántas se probaron y no destacar las que no pasarían una corrección.
