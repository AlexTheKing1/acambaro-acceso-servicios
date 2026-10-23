# Fase 4b — Crecimiento urbano y acceso: resumen para Alejandro

Fecha: 2026-10-23; actualizado en la fase 4c (tipología final y crecimiento no registrado). Detalle técnico en `docs/validacion.md` (V39–V47) y `docs/decisiones.md` (D42–D52).

> **Resultados provisionales.** `verificacion_zonas.csv` todavía no está en el release, así que las cuadras nuevas no se han revisado en imágenes. Cuando lo subas, `src/19_crecimiento.py` repite la comparación sin las zonas que marques "no".
>
> **Cómo se cuentan las cuadras nuevas en textos públicos (D49)**: con personas, cuadras y hectáreas, no con porcentajes, porque es un grupo pequeño. Los porcentajes de este documento son de trabajo. El hallazgo del preescolar se mantiene porque aparece con los tres umbrales.
>
> **Todo es descriptivo, no causal.** Que las cuadras nuevas estén más lejos de un servicio no dice por qué. Puede ser por dónde se construyó, por dónde se pusieron las escuelas o por otra razón.

## La respuesta corta

1. **La ciudad casi no creció en cuadras nuevas, pero sí construyó fuera de ellas.** Entre 2010 y 2020 aparecieron 53 cuadras nuevas en las 4 localidades urbanas: 29 ha, con 356 habitantes en 2020 (el 0.5 % de su población). Después de 2020 aparecieron 6 más (4.5 ha, sin población censada). La gran mayoría de la gente vive en cuadras que ya existían en 2010. En cambio, el GHSL ve unas 42 ha de construcción nueva en la ciudad **fuera** de las cuadras del INEGI (sección 6, provisional).
2. **Las cuadras nuevas 2010–2020 sí quedaron peor servidas, sobre todo por estar en la orilla.** Comparadas con cuadras viejas *a la misma distancia del centro*, la diferencia se reduce mucho. La excepción clara es el **preescolar**: en las cuadras nuevas, el 48 % de la gente está lejos de uno; en las cuadras viejas a la misma distancia del centro, el 13 %.
3. **La ciudad de Acámbaro sí se vació por dentro mientras crecía en suelo.** Entre 2010 y 2020 perdió 1 375 habitantes (de 57 972 a 56 597), pero ganó 2 508 viviendas (de 18 813 a 21 321). Las viviendas deshabitadas pasaron de 3 178 (17 %) a 4 606 (22 %). La pérdida de población se concentró en el primer kilómetro alrededor del centro (−2 093 personas, −12 %). Al mismo tiempo, la superficie construida (GHSL) creció 17 %.
4. **El vaciamiento no está solo en el centro.** El % de viviendas deshabitadas subió en todos los anillos de la ciudad, no solo en el centro. En 2020 el % de viviendas no habitadas es casi igual en el centro (26 %) que a 1–3 km (24–26 %), y un poco mayor en la orilla, a más de 3 km (31 %).

## 1. Cuántas cuadras son nuevas

Criterio D12: una cuadra es nueva si menos de la mitad de su superficie ya era cuadra en la edición anterior del Marco Geoestadístico.

| Localidad | Consolidadas (ya existían en 2010) | Nuevas 2010–2020 | Personas en las nuevas (2020) | Nuevas posteriores a 2020 |
|---|---:|---:|---:|---:|
| Ciudad de Acámbaro | 1 178 cuadras · 56 135 hab. | 30 cuadras · 18.3 ha | 254 | 4 cuadras · 2.5 ha |
| Irámuco | 137 · 6 228 hab. | 5 · 1.7 ha | 25 | 1 · 0.8 ha |
| Parácuaro | 127 · 3 987 hab. | 12 · 6.3 ha | 19 | 0 |
| Chupícuaro | 125 · 2 443 hab. | 6 · 3.0 ha | 58 | 1 · 1.2 ha |

(Más 32 puntos de caserío disperso con 464 personas, que quedan aparte.)

Las cuadras nuevas son pocas y chicas, y casi no tienen gente: en la ciudad son 30 cuadras con 82 viviendas. Por eso **los porcentajes de las cuadras nuevas se mueven mucho con pocas personas** y hay que leerlos con cuidado.

Las nuevas están más lejos del centro: en la ciudad, la mediana es de 3.2 km, contra 1.9 km de las consolidadas. Mapa: `docs/figuras/fase4b_antiguedad.png`.

**Ojo: el GHSL ve más crecimiento que el Marco Geoestadístico.** Entre 2010 y 2020 la superficie construida de la ciudad creció 67 ha, pero las cuadras nuevas suman solo 18 ha. Con el cruce celda por celda de la fase 4c (sección 6), de esas 67 ha, 25 caen dentro de cuadras (22 en cuadras que ya existían en 2010 y menos de 1 ha en las cuadras nuevas) y **42 ha fuera de toda cuadra**.

## 2. ¿Quedaron peor servidas las zonas nuevas?

### Las 4 localidades juntas, umbral principal (% de la población lejos)

Cada localidad se compara con sus propios anillos de 500 m desde su centro. El centro es el punto del ITER 2020.

| Servicio | Cuadras nuevas 2010–2020 (356 hab.) | Viejas a la misma distancia del centro | Todas las viejas | Lectura |
|---|---:|---:|---:|---|
| Preescolar | **48 %** | 13 % | 10 % | **efecto "zona nueva"** |
| Primaria | 43 % | 42 % | 37 % | sin diferencia |
| Secundaria | 54 % | 51 % | 30 % | efecto "periferia" |
| Bachillerato público | 45 % | 41 % | 36 % | casi sin diferencia |
| Salud pública | 38 % | 32 % | 24 % | sobre todo periferia |
| Mercado o supermercado | 69 % | 59 % | 39 % | sobre todo periferia, algo de zona nueva |
| Tienda básica | 6 % | 1 % | 1 % | casi nadie lejos en ningún caso |

Cómo se lee: en la secundaria, las cuadras nuevas (54 %) están casi igual que las viejas a la misma distancia del centro (51 %). Las dos están peor que el promedio de las viejas (30 %). Es decir, lo que pesa es estar en la orilla, no ser nueva. En el preescolar no pasa eso: las cuadras nuevas están mucho peor que las viejas que tienen al lado.

**Con los otros umbrales**, el preescolar sigue en el mismo sentido: con el estricto, 48 % contra 25 %; con el holgado, 16 % contra 5 %. En salud pública, la ventaja de las viejas aparece con el estricto (69 % contra 50 %) y se invierte con el holgado (17 % contra 23 %): ese resultado no es firme. Tabla completa: `data/processed/crecimiento_acceso_periferia.csv`.

### Por localidad (umbral principal)

- **Ciudad de Acámbaro** (254 hab. en cuadras nuevas): preescolar 37 % lejos, contra 16 % de las viejas a igual distancia; secundaria 63 % contra 62 %; mercado 57 % contra 62 %; primaria 25 % contra 43 % (aquí las nuevas están **mejor**); salud 22 % contra 39 % (también **mejor**).
- **Chupícuaro** (58 hab.): las 6 cuadras nuevas, al oriente, están lejos de preescolar, primaria, mercado y salud (86–100 %). Las viejas a la misma distancia del centro están en 35–95 %.
- **Parácuaro** (19 hab.) e **Irámuco** (25 hab.): muy pocas personas para sacar conclusiones.
- **Posteriores a 2020** (6 cuadras sin población): 5 de las 6 están lejos de un mercado o supermercado, y 4 de las 6 de un bachillerato público. Las 4 de la ciudad están a una mediana de 1.5 km del centro, más cerca que las nuevas de 2010–2020.

Tablas: `crecimiento_acceso.csv` (por localidad, servicio, umbral y grupo) y `crecimiento_acceso_por_anillo.csv`.

## 3. Viviendas deshabitadas y de uso temporal

### 2020, por localidad

"No habitadas" = deshabitadas + de uso temporal (casas de fin de semana o de quien vive fuera).

| Localidad | Viviendas | % no habitadas | % deshabitadas | % uso temporal | Viejas / nuevas: % no habitadas |
|---|---:|---:|---:|---:|---|
| Ciudad de Acámbaro | 21 321 | 26 % | 22 % | 4 % | 26 % / 30 % (82 viviendas nuevas) |
| Irámuco | 2 336 | 38 % | 28 % | 10 % | 38 % / 46 % (13) |
| Parácuaro | 2 040 | 42 % | 24 % | 18 % | 43 % / 20 % (16) |
| Chupícuaro | 1 335 | 46 % | 26 % | 20 % | 47 % / 26 % (23) |

(% deshabitadas y % uso temporal: totales publicados por localidad. Columna de viejas / nuevas: suma de las cuadras donde el dato es visible.)

En las tres localidades chicas, casi la mitad de las viviendas no está habitada. En Parácuaro y Chupícuaro pesa mucho el uso temporal (18–20 %). Probablemente son casas de familias que viven fuera (migración), pero eso no lo dice el censo. Mapa: `docs/figuras/fase4b_deshabitadas.png`.

### 2010 → 2020: ¿aumentó el vaciamiento?

**Sí, en las cuatro localidades aumentaron las viviendas deshabitadas** (totales publicados por localidad):

| Localidad | Población 2010 → 2020 | Viviendas 2010 → 2020 | % deshabitadas 2010 → 2020 | % uso temporal 2010 → 2020 |
|---|---|---|---|---|
| Ciudad de Acámbaro | 57 972 → 56 597 (**−1 375**) | 18 813 → 21 321 (+2 508) | 17 % → **22 %** | 6 % → 4 % |
| Irámuco | 5 954 → 6 275 | 1 839 → 2 336 | 19 % → **28 %** | 14 % → 10 % |
| Parácuaro | 4 058 → 4 159 | 1 926 → 2 040 | 23 % → 24 % | 17 % → 18 % |
| Chupícuaro | 2 273 → 2 583 | 1 226 → 1 335 | 18 % → **26 %** | 33 % → 20 % |

**Por distancia al centro, ciudad de Acámbaro.** La población y el total de viviendas están completos por cuadra en los dos censos:

| Distancia al centro | Población 2010 → 2020 | Viviendas 2010 → 2020 |
|---|---|---|
| 0–1 km | 18 090 → 15 997 (**−2 093**) | 6 236 → 6 518 (+282) |
| 1–2 km | 22 012 → 21 629 (−383) | 6 828 → 7 762 (+934) |
| 2–3 km | 12 456 → 12 678 (+222) | 3 878 → 4 672 (+794) |
| más de 3 km | 5 414 → 6 085 (+671) | 1 871 → 2 288 (+417) |

**Las deshabitadas por distancia** se compararon con los totales publicados por AGEB. En 2010, el INEGI ocultó el número de deshabitadas en 9 de cada 10 cuadras, así que no se puede contar por cuadra. Esto cubre el 92 % de las viviendas de la ciudad:

| Distancia al centro | % deshabitadas 2010 → 2020 | % uso temporal 2010 → 2020 |
|---|---|---|
| 0–1 km | 15 % → **22 %** | 8 % → 4 % |
| 1–2 km | 15 % → **21 %** | 6 % → 4 % |
| 2–3 km | 17 % → 21 % | 4 % → 5 % |
| más de 3 km | 26 % → 25 % | 5 % → 6 % |

**Lectura**: en el centro de la ciudad (primer kilómetro) se perdieron 2 093 habitantes, mientras el número de viviendas siguió creciendo y las deshabitadas subieron de 15 % a 22 %. La población crece solo a más de 2 km. Eso es lo que la pregunta llama "vaciarse por dentro". Pero el % de deshabitadas subió casi igual a 1–2 km: es un fenómeno de toda la ciudad, no solo del centro histórico. Una parte del aumento de deshabitadas en el centro coincide con la baja del uso temporal (8 % → 4 %). Puede ser que viviendas que en 2010 se contaron como de uso temporal en 2020 se contaran como deshabitadas. El censo no permite distinguirlo.

En Irámuco el centro (0–500 m) también perdió gente (−330), y en Parácuaro también (−245).

### Lo que oculta el "*" (efecto declarado)
- **2020**: el número de deshabitadas está oculto en 602 de 1 652 cuadras urbanas (incluye el caserío). Por localidad, lo oculto es la diferencia entre el total publicado y lo visible: 587 deshabitadas en la ciudad (13 % de 4 606), 73 en Irámuco, 74 en Parácuaro y 91 en Chupícuaro. Por eso se usó "viviendas − habitadas", que solo está oculto en 51 cuadras y da casi lo mismo que lo publicado: 25.9 % contra 26.1 % en la ciudad.
- **2010**: está oculto en 1 339 de 1 478 manzanas. La comparación de la década se hizo con los totales por localidad y por AGEB (agrupadas en "unidades comparables" cuando sus límites cambiaron). En 35 de las 110 AGEB de 2010 y en 41 de las 126 de 2020 también está oculto el total de la AGEB. Esas AGEB quedan fuera de la tabla por distancia. Chupícuaro no tiene datos por cuadra en 2010 (era rural); solo tiene el total de la localidad.

## 4. Expansión de largo plazo (GHSL 1975–2020)

| | 1975 | 1990 | 2000 | 2010 | 2020 | Crecimiento 1975–2020 |
|---|---:|---:|---:|---:|---:|---:|
| Municipio, superficie construida | 357 ha | 603 ha | 971 ha | 1 107 ha | 1 358 ha | ×3.8 |
| Ciudad de Acámbaro (+1 km) | 161 ha | 213 ha | 349 ha | 390 ha | 456 ha | ×2.8 |
| Irámuco | 31 ha | 48 ha | 63 ha | 67 ha | 71 ha | ×2.3 |
| Parácuaro | 20 ha | 32 ha | 56 ha | 63 ha | 73 ha | ×3.7 |
| Chupícuaro | 16 ha | 27 ha | 48 ha | 53 ha | 62 ha | ×3.9 |

**Superficie construida por habitante** (solo 2010 y 2020, que tienen población del mismo año):

| | 2010 | 2020 |
|---|---:|---:|
| Municipio | 102 m²/hab | **125 m²/hab** (+23 %) |
| Ciudad de Acámbaro | 67 m²/hab | **81 m²/hab** (+20 %) |
| Irámuco | 113 | 114 |
| Parácuaro | 155 | 175 |
| Chupícuaro | 233 | 242 |

El municipio construyó 23 % más superficie en la década con la misma población: 109 030 en 2010, 108 697 en 2020 y 108 140 según la EIC 2025 (intervalo 100 644–115 636). **Más suelo construido por persona: la ciudad se extiende sin ganar habitantes.**

**Hacia dónde creció la ciudad**: hacia el **sur y el suroeste** en todos los periodos: 24 % y 23 % de lo construido en 2010–2020; en 1990–2000, 34 % y 19 %. Le sigue el **oriente** (17 %). El norte creció poco en 2010–2020 (6 %). Las cuadras nuevas del MG 2010–2020 caen en el mismo sentido: sur 43 %, sureste 28 %, suroeste 21 %. El mayor salto fue en 1990–2000: la superficie construida de la ciudad pasó de 213 a 349 ha. Gráfica: `docs/figuras/fase4b_ghsl.png`.

**Limitación**: los ITER de 1990, 1995, 2000 y 2005 no tienen enlace directo de descarga (2 intentos). Por eso la superficie por habitante solo se calcula para 2010 y 2020. Si los subes al release, se completa la serie desde 1990.

## 5. Tipología de AGEB (criterios finales, D47)

Criterios aprobados por Alejandro: **nueva** = ≥ 30 % de su superficie es cuadra nueva; **desatendida** = en ≥ 3 de 5 servicios básicos (preescolar, primaria, secundaria, salud pública, mercado o supermercado) más de la mitad de su gente (o de su superficie, si no tiene gente) está lejos con el umbral principal; **vaciándose** = % de viviendas no habitadas en el cuarto más alto **de su propia localidad** (AGEB con ≥ 30 viviendas) y pérdida de población entre 2010 y 2020. Recalculada: los números no cambian respecto a la propuesta.

| Clase | AGEB | Habitantes 2020 | Con 2 de 5 (sensibilidad) |
|---|---:|---:|---:|
| Nueva y desatendida | 15 | 146 | 20 |
| Nueva y bien servida | 11 | 225 | 6 |
| Consolidada y vaciándose | 4 | 1 227 | 4 |
| Consolidada desatendida | 43 | 7 408 | 68 |
| Consolidada estable | 53 | 60 143 | 28 |

Por localidad: la ciudad tiene 39 AGEB estables (51 372 hab.), 24 desatendidas (3 434), las 4 que se vacían (1 227) y 18 nuevas (356 hab.; 10 de ellas desatendidas). Irámuco: 11 consolidadas desatendidas (3 777 hab.). Parácuaro: 8 desatendidas (197 hab.) y 7 nuevas casi sin gente. Chupícuaro: 3 estables.

Mapa: `docs/figuras/fase4b_tipologia.png`. Tabla: `data/processed/tipologia_ageb.csv`.

Qué tan firme es (`tipologia_sensibilidad.csv`):
- El umbral de "nueva" (25 % o 40 %) mueve 0–2 AGEB. **Firme.**
- **Con 2 de 5 servicios** cambian 30 AGEB: casi toda la orilla queda "desatendida" (68 consolidadas), porque el mercado, la primaria y la secundaria están lejos para la mitad de la gente en muchas AGEB. Con 4 de 5 cambian 26. Por eso el número de servicios es el criterio que más pesa, y el texto lo dirá.
- Las 4 AGEB que se vacían están en la **orilla oriente de la ciudad** (2.3–3.4 km del centro), no en el centro; 3 de ellas también son desatendidas. El centro perdió población, pero su % de no habitadas (26 %) no llega al cuarto más alto de la ciudad (≥ 32 %).

## 6. Crecimiento que el INEGI no dibuja (provisional hasta tu revisión)

El GHSL ve 67 ha nuevas construidas en la ciudad entre 2010 y 2020; las cuadras nuevas del Marco Geoestadístico suman 18 ha. Se cruzó cada celda de 100 m del GHSL con las cuadras del MG más reciente (EIC 2025):

| Localidad (+1 km) | Construcción nueva 2010–2020 | Dentro de cuadras | Fuera de cuadras | Zonas sin cuadras* |
|---|---:|---:|---:|---:|
| Ciudad de Acámbaro | 66.6 ha | 25.0 ha | **41.6 ha** | 52 zonas · 25.9 ha |
| Irámuco | 4.0 | 2.0 | 2.0 | 5 · 0.9 |
| Parácuaro | 10.0 | 4.6 | 5.5 | 10 · 2.8 |
| Chupícuaro | 9.5 | 4.0 | 5.5 | 11 · 2.6 |

\* Zona = celdas contiguas que ganaron ≥ 500 m² construidos y tienen menos de 25 % de su superficie en cuadras (D52). Con criterios más laxos o más estrictos, la ciudad queda entre 21 y 30 ha: el orden de magnitud es firme.

Lo que se encontró:
- **Casi nada de la construcción nueva cayó en las cuadras nuevas del MG** (0.6 ha de 18). Esas cuadras estaban trazadas pero casi vacías en 2020, lo que coincide con sus 82 viviendas.
- **La mayor parte de lo construido quedó fuera de la traza del INEGI**, en la orilla (mediana a 3.2 km del centro). La zona más grande (G-001, 29 ha de celdas, 3.9 ha construidas) está al sur de la ciudad, a 2.9 km del centro.
- **Parte de eso el INEGI sí lo registra, pero como localidad rural**: 18 de las 78 zonas contienen un punto de localidad rural o caserío (por ejemplo Las Malayas, Hacienda Real de Acámbaro). En la ciudad son 9.4 de las 25.9 ha. Ahí la gente se cuenta en el censo, pero no dentro de la ciudad ni con cuadras.
- Una zona se llama "Puente de Fierro [Invernadero]": probablemente es un invernadero que el GHSL leyó como construcción.

**Limitaciones**: el GHSL es un modelo con celdas de 100 m, no un dibujo de casas: una zona de una sola celda (33 de las 78) puede ser una nave, una bodega o un bordo. Su capa 2020 combina imágenes de varios años y puede confundir invernaderos, techos agrícolas o suelo desnudo con construcción. **Puede haber falsos positivos**, por eso hace falta tu revisión. Además, no se sabe cuánta gente vive ahí: el censo no la reporta por cuadra fuera de las cuadras, y **no se inventa población**.

Para revisar: `docs/zonas_ghsl_sin_cuadras.kml` (las 20 zonas más grandes, en Google Earth) y `docs/verificar_zonas_ghsl.csv` (las 78, con enlace a Google Maps satelital; llena `existe_en_imagen` con si / no / no se ve, `que_se_ve` y `notas`).

## Qué revisar
1. Los cuatro mapas `docs/figuras/fase4b_*.png`.
2. `docs/zonas_nuevas.kml` en Google Earth y subir `verificacion_zonas.csv`: con eso estos resultados dejan de ser provisionales.
3. `docs/zonas_ghsl_sin_cuadras.kml` y `docs/verificar_zonas_ghsl.csv` (sección 6): con eso la sección 6 deja de ser provisional.

## Decisiones tomadas (fase 4c, Alejandro)
1. Tipología: "desatendida" con 3 de 5; 2 de 5 como sensibilidad; "vaciándose" dentro de su localidad (D47).
2. Centro de cada localidad: el punto del ITER 2020 (D48).
3. Cuadras nuevas en textos públicos: conteos, no porcentajes; se mantiene el preescolar (D49).
4. ITER 1990–2005: no se buscan; queda como limitación (D50).
5. Título de trabajo: "¿Quién está lejos hoy? Acceso a servicios y vaciamiento urbano en Acámbaro" (D51).

## Decisión que necesito
- **Criterio de "zona sin cuadras" (D52)**: ≥ 500 m² ganados y < 25 % de la celda en cuadras. ¿Te parece bien, o lo ajustamos después de revisar las zonas?
