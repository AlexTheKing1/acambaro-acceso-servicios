# Fase 4 — Números definitivos: resumen para Alejandro

Fecha: 2026-10-23. Detalle técnico en `docs/validacion.md` (V31–V38) y `docs/decisiones.md` (D33–D41).

## Qué se hizo

1. **Se aplicaron tus decisiones.** Umbrales definitivos (radio SNEU × 1.33). Las 6 unidades de salud sin CLUES pasan a un anexo. La tienda básica en lo rural queda como "no medible". El ISSSTE cuenta como en operación. Se conservó el punto del CECyTE que coincide con Google Maps. El consultorio del CERESO salió de salud pública. La Secundaria Técnica 24 queda como la de Parácuaro. El catálogo SEP se fecha por la consulta.
2. **Se incorporaron tus verificaciones.** Las 5 rutas comparadas con Google y los 68 servicios revisados en imágenes. Ningún servicio se borró por un "no": quedaron marcados como dudosos y se calculó cuánto cambiaría el resultado sin ellos.
3. **Se recalcularon** todas las tablas y los mapas (`docs/figuras/fase4_*.png`).
4. **Archivos nuevos para ti**: `docs/zonas_nuevas.kml` (para Google Earth) y `docs/verificar_campo.csv` (para las salidas de campo).
5. **Red rural**: se intentó otra vez bajar los caminos de OpenStreetMap (2 intentos). El proxy volvió a cortar la conexión. Lo rural sigue con línea recta × 1.33.

## Los umbrales que se usan

"Lejos" = más allá del umbral principal. En la ciudad se mide a pie por calles; en lo rural, por camino estimado.

| Servicio | Ciudad (a pie) | Rural (por camino) |
|---|---:|---:|
| Preescolar | 1 000 m | 2 km |
| Primaria | 670 m | 2 km |
| Secundaria | 1 330 m | 5 km |
| Bachillerato | 3 330 m | 10 km |
| Salud pública de primer nivel | 1 330 m | 5 km |
| Tienda básica | 500 m | no medible |
| Mercado o supermercado | 1 000 m (15 min a pie) | 10 km |

## Cifras clave (umbral principal)

Población del Censo 2020. Las cifras por grupo de edad son estimaciones (D10). Cuando lo que se ve directamente en los datos publicados es mayor que la estimación, se pone esa cifra mayor (marcada "al menos").

### Ciudad de Acámbaro (56 596 habitantes)

| Servicio | Personas lejos | % | Del grupo que más lo usa |
|---|---:|---:|---|
| Preescolar | 4 636 | 8 % | 249 niñas y niños de 3–5 años (de 2 835) |
| Primaria | 17 853 | 32 % | 1 700 de 6–11 años (de 5 139) |
| Secundaria | 13 400 | 24 % | 673 de 12–14 años (de 2 688) |
| Bachillerato (todos) | 1 042 | 2 % | 55 de 15–17 años |
| Bachillerato público | 24 430 | 43 % | 1 230 de 15–17 años (de 2 886) |
| Salud pública de primer nivel | 12 205 | 22 % | 1 730 de 60 años y más (de 8 748); 724 con discapacidad |
| Tienda básica | 556 | 1 % | al menos 63 de 60 años y más |
| Mercado o supermercado | 20 267 | 36 % | 2 799 de 60 años y más; 1 157 con discapacidad |

### Las otras tres localidades urbanas

| Servicio | Irámuco (6 275) | Parácuaro (4 159) | Chupícuaro (2 583) |
|---|---|---|---|
| Preescolar | 25 % — 80 de 3–5 años (de 327) | 9 % — 14 (de 173) | 31 % — 35 (de 128) |
| Primaria | **80 %** — 564 de 6–11 años (de 703) | 44 % — 152 (de 354) | 39 % — 99 (de 256) |
| Secundaria | 61 % — 215 de 12–14 años (de 371) | **100 % — no hay secundaria dentro de la localidad** | 10 % — 13 (de 131) |
| Bachillerato | 9 % — 36 de 15–17 años | 0 % | 0 % |
| Salud pública | **64 %** — al menos 704 de 60+ (de 1 040) | 10 % — 68 de 60+ | 5 % — 25 de 60+ |
| Mercado o supermercado | **100 % — no hay mercado ni supermercado registrado; puede existir un tianguis que ninguna fuente captura** | 16 % | 20 % |
| Tienda básica | 2 % | 4 % | 1 % |

- **Parácuaro**: la secundaria que lo atiende es la Escuela Secundaria Técnica Núm. 24, en la carretera Acámbaro–Parácuaro km 9. Está a 4.2 km en línea recta del centro del pueblo, unos 5.5 km por camino. Es la misma que calculó la fase 3. Para la mitad norte del pueblo, la Telesecundaria 847 de La Concepción queda a una distancia casi igual.
- **Irámuco**: el mercado registrado más cercano es el Mercado Revolución de Santa Ana Maya (Michoacán), a 13–18 km.

### Localidades rurales (208 localidades, 39 083 habitantes)

| Servicio | Personas lejos | % | Grupo |
|---|---:|---:|---|
| Preescolar (2 km) | 1 158 | 3 % | 59 de 3–5 años |
| Primaria (2 km) | 695 | 2 % | 70 de 6–11 años |
| Secundaria (5 km) | 1 040 | 3 % | 41 de 12–14 años |
| Bachillerato (10 km) | 1 107 | 3 % | 44 de 15–17 años |
| Salud pública (5 km) | 6 635 | 17 % | 903 de 60+; 457 con discapacidad |
| Mercado o supermercado (10 km) | 15 733 | 40 % | 3 222 de 60+ (no incluye tianguis: ninguna fuente los registra) |
| Tienda básica | no medible | — | el DENUE no registra negocios de las localidades rurales pequeñas |

## Qué tanto depende del umbral

Personas lejos en la ciudad de Acámbaro con los tres umbrales:

| Servicio | Estricto (radio SNEU) | **Principal** | Holgado (× 1.5) |
|---|---:|---:|---:|
| Preescolar | 12 518 (750 m) | **4 636** (1 000 m) | 1 198 (1 500 m) |
| Primaria | 31 392 (500 m) | **17 853** (670 m) | 5 553 (1 000 m) |
| Secundaria | 24 237 (1 000 m) | **13 400** (1 330 m) | 3 424 (2 000 m) |
| Bachillerato público | 40 452 (2 500 m) | **24 430** (3 330 m) | 807 (5 000 m) |
| Salud pública | 25 857 (1 000 m) | **12 205** (1 330 m) | 2 665 (2 000 m) |
| Mercado o supermercado | 34 986 (750 m) | **20 267** (1 000 m) | 10 053 (1 500 m) |

**Hallazgos que se sostienen con los tres umbrales** (los más sólidos):
- Irámuco: no hay mercado ni supermercado (100 % lejos con cualquier umbral).
- Parácuaro: no hay secundaria dentro de la localidad (100 % con cualquier umbral).
- Irámuco, primaria: 88 % / 80 % / 56 %.
- Irámuco, salud pública: 82 % / 64 % / 19 %.
- Ciudad de Acámbaro: mercado o supermercado 62 % / 36 % / 18 %; primaria 55 % / 32 % / 10 %.
- Rural, mercado o supermercado: 86 % / 40 % / 11 %.

**Hallazgos que dependen del umbral:**
- Bachillerato público en la ciudad: 72 % y 43 % con el estricto y el principal, pero **1 %** con el holgado. Casi toda la ciudad está a menos de 5 km de uno.
- Preescolar en Irámuco (47 % / 25 % / 0 %) y en Parácuaro (40 % / 9 % / 0 %): con el holgado no queda nadie lejos.
- Rural, secundaria (24 % / 3 % / 0 %), bachillerato (27 % / 3 % / 0 %) y salud (50 % / 17 % / 0 %): con el holgado nadie queda lejos.
- Bachillerato (todos) en la ciudad: solo con el estricto aparece una cifra apreciable (9 %; 2 % con el principal, 0 % con el holgado).

Todas las combinaciones están en `data/processed/acceso_resumen_por_localidad.csv`.

## Anexo: si contaran las 6 unidades de salud sin CLUES

Son Solís, La Ortiga, La Encarnación, San Luis de los Agustinos, La Presa de Santa Inés y "Centro Médico la Soledad" en la ciudad. Si contaran como salud pública, con el umbral principal:
- **Rural: de 6 635 a 2 992 personas lejos** (−3 643): La Ortiga y sus vecinas (1 580 personas), La Encarnación (842), San Miguel, junto a Solís (847), y San Luis de los Agustinos y su vecina (374).
- Ciudad de Acámbaro: de 12 205 a 11 464 (−741).
- Irámuco, Parácuaro y Chupícuaro: sin cambio.

Ojo: en tu verificación, dos de ellas salieron "no" ("Centro Médico la Soledad" y La Presa de Santa Inés) y una "no se ve" (Solís). Están en la lista de campo.

## Qué tan confiables son los datos

### Distancias a pie
- **5 rutas contra Google Maps**: diferencia mediana de **2 %**; la mayor, en distancias de más de 1 km, fue de **6 %**. La ruta corta (148 m contra 110 m) difiere 38 m por el tramo de la cuadra a la calle. En 4 de 5 rutas el cálculo sale un poco más largo que Google, así que no subestima. Son pocas rutas: sirven para saber que el orden de magnitud está bien, no para dar un margen de error.
- **Lo rural es aproximado** (línea recta × 1.33). No ve ríos, cerros, presas ni el lago. Lo más probable es que las distancias reales sean algo mayores.

### Servicios (verificación remota, preliminar)
**Advertencia: no fue una muestra al azar.** Revisaste todos los bachilleratos y los casos priorizados (sin nombre, sin confirmar, raros). Estas tasas dicen qué tan bien salieron *esos* casos. **No** son la confiabilidad general del catálogo: los casos fáciles no se revisaron, así que la del catálogo completo puede ser distinta (probablemente mayor).

- **Total**: 50 de 68 revisados se ven en la imagen (**74 %**); 82 % si no se cuentan los "no se ve". Dentro del municipio: 44 de 57 (77 %).
- **Por tipo**: salud de primer nivel 17 de 20 (85 %); abasto 13 de 15 (87 %); bachillerato 11 de 17 (65 %); primaria 4 de 5; preescolar 3 de 4; secundaria 2 de 5 (los otros 3 "no se ven", ninguno "no").
- **Por fuente**: lo que está en el MG y en el DENUE a la vez se confirma más (19 de 23, **83 %**) que lo que solo está en el DENUE (19 de 24, 79 %) o solo en el MG (12 de 21, **57 %**).
- **Por cruce con SEP/CLUES**: confirmadas por SEP o CLUES 30 de 39 (77 %); no confirmadas 6 de 11 (55 %).
- **Qué pasa si los "no" no existieran**: casi nada cambia. Solo dos cifras se mueven:
  - **Monte Prieto** (1 068 habitantes) quedaría lejos de una primaria: en lo rural, de 695 a 1 811 personas lejos. En ese punto viste la Telesecundaria 845; la primaria Emiliano Zapata sí está registrada en la SEP. Hay que verla en campo.
  - **Mercado 22 de Octubre** (ciudad): sin él, de 20 267 a 21 245 personas lejos de un mercado o supermercado.
- **Si solo contaran las escuelas confirmadas por SEP o DENUE**: primaria en la ciudad +1 801 personas lejos; Chupícuaro +403; rural +146 (preescolar), +210 (primaria), +234 (secundaria).

### Otras limitaciones (sin cambio)
- La población es la del Censo 2020. Las cuadras nuevas posteriores a 2020 se midieron pero no tienen población, y no se les inventa.
- IMSS e ISSSTE solo atienden a sus derechohabientes; la medida de salud pública los incluye.
- La CLUES registra la clínica del ISSSTE como "fuera de operación". Tú confirmaste que opera, y se usa como en operación.
- La SEP ubicaba el CECyTE 4.3 km al norte, en calle Loma Bonita. Se usa el punto del sur, que coincide con Google Maps y con el DENUE (número 8, col. Valle de Acámbaro). Con eso, el bachillerato público queda más lejos para el norte de la ciudad que en la fase 3.

## Qué revisar

1. **`docs/zonas_nuevas.kml`**: ábrelo en Google Earth. Trae 28 zonas: en rojo las 13 posteriores a 2020 y en naranja las 15 más grandes de 2010–2020, cada una con su id, periodo y superficie. En `docs/verificar_zonas_nuevas.csv`, la columna `en_kml` dice cuáles están.
2. **`docs/verificar_campo.csv`**: 19 puntos en 5 salidas. La salida 1 es la ciudad (10 puntos). La 2 va a Chupícuaro, Solís y Las Cruces; la 3 a Monte Prieto y Parácuaro; la 4 a La Presa de Santa Inés, y la 5 a Irámuco. Incluye:
   - los 12 servicios del municipio que salieron "no" o "no se ve";
   - las dos UMAPS de Irámuco, para saber si son una o dos clínicas;
   - 5 "sí" elegidos al azar, para medir cuánto se equivoca la revisión con Google.

   Cada punto trae un enlace de Google Maps y columnas vacías para anotar: `existe_campo`, `fecha_visita`, `foto`, `notas`. La columna `se_usa_en_la_medida` te dice cuáles afectan el resultado.
3. Los mapas `docs/figuras/fase4_*.png`.

## Decisiones pendientes

1. **Texto del SNEU**: no se pudo abrir el documento original de SEDESOL (2 búsquedas). Se aplicó × 1.33 como decidiste. Si consigues el PDF del tomo de Educación (o el de Salud), conviene cotejar dos cosas antes de publicar: que el "radio de servicio urbano recomendable" sea en línea recta, y los valores 750 / 500 / 1 000 m. Si el SNEU lo define como distancia recorrida, el umbral correcto sería el estricto.
2. **Salidas de campo** con `docs/verificar_campo.csv`. Si confirmas en campo que la primaria de Monte Prieto no existe, cambia la cifra rural de primaria (de 695 a 1 811 personas lejos).
3. **`verificacion_zonas.csv`**: sigue sin estar en el release. Cuando revises las zonas (ahora con el KML), súbelo y lo incorporo.
4. **Red de caminos rural**: sigue sin poder bajarse desde aquí. Si subes la Red Nacional de Caminos del INEGI al release, rehago lo rural con caminos reales.
5. **Siguiente fase**: el sitio web y el reporte PDF.

## Algo que salió mal

- Al recalcular, el factor de rodeo se recalibró solo, a 1.349, y movió entre 1 y 6 m algunas distancias. La causa fue la reubicación del CECyTE: los recorridos desde el norte de la ciudad hacia el sur tienen más rodeo. Como tus umbrales se derivan de 1.33, el factor se dejó fijo en 1.33 y el 1.349 se reporta como chequeo.
- En la fase 3 escribí que la Secundaria Técnica 24 estaba "a ~4 km" de Parácuaro. Era la distancia en línea recta; por camino son unos 5.5 km.
