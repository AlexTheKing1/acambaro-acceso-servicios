# Fase 3 — Accesibilidad: resumen para Alejandro

Fecha: 2026-10-23. Detalle técnico en `docs/validacion.md` (V18–V30) y `docs/decisiones.md` (D20–D32).

## Qué se hizo

1. **Catálogo de servicios actualizado con SEP y CLUES.** Se cruzó cada escuela y unidad de salud del catálogo de la fase 2 con el catálogo de escuelas de la SEP y la CLUES (agosto 2026): cuáles operan, cuáles son públicas o privadas, cuáles faltaban y cuáles ya cerraron.
2. **Distancia a pie por calles** desde cada cuadra de Acámbaro, Irámuco, Parácuaro y Chupícuaro al servicio más cercano de cada tipo, usando las calles del Marco Geoestadístico del INEGI.
3. **Distancia aproximada por camino** desde cada una de las 208 localidades rurales. No se pudo bajar ninguna red de caminos (ni la del INEGI ni OpenStreetMap), así que se usó la distancia en línea recta multiplicada por 1.33, que es cuánto más largo es en promedio el camino real que la línea recta dentro de la ciudad.
4. **Población lejos de cada servicio**, total y por grupo, con tres umbrales (estricto, propuesto y holgado) para que elijas.
5. Nombres de colonia por cuadra, indicadores sociales del Censo 2020, mapas y listas para verificar.

## Cambios en el catálogo (dentro del municipio)

- **46 servicios nuevos** que no estaban: sobre todo escuelas rurales pequeñas (telebachilleratos, videobachilleratos, telesecundarias, preescolares y primarias comunitarias del CONAFE), preparatorias privadas de la ciudad, el CONALEP 163, la clínica del IMSS (HGSMF 13, que da medicina familiar) y la UMAPS de San Juan Jaripeo.
- **10 ya no operan** según SEP o CLUES: 6 preescolares y 1 primaria rurales, una preparatoria privada de la ciudad, la UMAPS vieja de Irámuco (se cambió a un edificio nuevo, a unos 300 m) y un sanatorio privado.
- Ahora se sabe si son públicas o privadas casi todas las escuelas (antes faltaba el dato en 181; ahora en 27).
- Quedan en el municipio: 101 preescolares, 117 primarias, 41 secundarias, 26 bachilleratos, 24 unidades públicas de salud de primer nivel, 9 mercados o supermercados y 824 tiendas.
- Hay **1 bachillerato no escolarizado** (preparatoria abierta, en la ciudad). Ninguna fuente trae cuántos alumnos tiene.

## Cifras clave (umbral propuesto)

"Lejos" = más allá del umbral propuesto: a pie en las localidades urbanas; por camino estimado en las rurales.

### Ciudad de Acámbaro (56 596 habitantes)

| Servicio | Lejos si está a más de | Personas lejos | % | Del grupo que más lo usa |
|---|---:|---:|---:|---|
| Preescolar | 750 m | 12 518 | 22 % | 673 niñas y niños de 3–5 años (de 2 835) |
| Primaria | 500 m | 31 392 | 56 % | 2 915 de 6–11 años (de 5 139) |
| Secundaria | 1 km | 24 237 | 43 % | 1 170 de 12–14 años (de 2 688) |
| Bachillerato (todos) | 2.5 km | 3 139 | 6 % | 196 de 15–17 años |
| Bachillerato público | 2.5 km | 20 281 | 36 % | 1 072 de 15–17 años (de 2 886) |
| Salud pública de primer nivel | 1 km | 25 479 | 45 % | 4 048 de 60 años y más; 1 605 con discapacidad |
| Tienda básica | 500 m | 556 | 1 % | — |
| Mercado o supermercado | 1.2 km | 15 125 | 27 % | 2 017 de 60 años y más; 848 con discapacidad |

### Las otras tres localidades urbanas

| Servicio | Irámuco (6 275) | Parácuaro (4 159) | Chupícuaro (2 583) |
|---|---|---|---|
| Preescolar (750 m) | 47 % — 145 de 3–5 años | 40 % — 71 | 53 % — 63 |
| Primaria (500 m) | 88 % — 618 de 6–11 años | 72 % — 254 | 64 % — 163 |
| Secundaria (1 km) | 78 % — 282 de 12–14 años | **100 % — no hay secundaria en Parácuaro** | 26 % — 35 |
| Bachillerato (2.5 km) | 57 % — 193 de 15–17 años | 0 % | 0 % |
| Salud pública (1 km) | **82 %** — 869 de 60+ | 31 % — 252 de 60+ | 16 % — 80 de 60+ |
| Mercado o súper (1.2 km) | **100 % — no hay; el más cercano a ~15 km** | 6 % | 8 % |
| Tienda básica (500 m) | 2 % | 4 % | 1 % |

### Localidades rurales (208 localidades, 39 083 habitantes)

| Servicio | Lejos si está a más de | Personas lejos | % |
|---|---:|---:|---:|
| Preescolar | 2 km | 1 158 | 3 % |
| Primaria | 2 km | 695 | 2 % |
| Secundaria | 5 km | 1 040 | 3 % |
| Bachillerato | 10 km | 1 107 | 3 % |
| Salud pública de primer nivel | 5 km | 6 635 | 17 % (903 de 60+, 457 con discapacidad) |
| Mercado o supermercado | 10 km | 15 733 | 40 % |
| Tienda básica | — | no se puede medir | el DENUE no registra tiendas rurales |

### Qué tanto depende del umbral

Mucho. Por ejemplo, en la ciudad de Acámbaro:

| Servicio | Estricto | Propuesto | Holgado |
|---|---|---|---|
| Primaria | 40 706 (400 m) | 31 392 (500 m) | 5 553 (1 km) |
| Salud pública | 38 421 (750 m) | 25 479 (1 km) | 6 410 (1.5 km) |
| Secundaria | 35 514 (750 m) | 24 237 (1 km) | 9 711 (1.5 km) |
| Mercado o súper | 34 986 (750 m) | 15 125 (1.2 km) | 5 756 (2 km) |

Con el umbral holgado casi nadie queda lejos de una escuela en la ciudad; con el estricto, la mayoría. Por eso la elección del umbral es la decisión más importante de esta fase. Todas las combinaciones están en `data/processed/acceso_resumen_por_localidad.csv`.

### Si las escuelas no confirmadas no existieran

Quitar las escuelas que solo aparecen en el dibujo del INEGI (sin SEP ni DENUE que las confirmen) cambia poco: en la ciudad, +1 381 personas lejos de una primaria (de 31 392 a 32 773); en Chupícuaro +275 (primaria); en lo rural, +146 (preescolar), +210 (primaria) y +234 (secundaria). Salud, bachillerato y abasto no cambian.

## Lo que hay que saber de estas cifras

- **Las cifras por grupo de edad son estimaciones** (método acordado por AGEB, D10). Junto a cada una está el mínimo que se ve directamente en los datos publicados; la cifra real nunca es menor. En 34 de 1 008 casos el mínimo visible es mayor que la estimación (por 1 a 31 personas, sobre todo adultos mayores de Irámuco): ahí vale el mínimo.
- **La población es la del Censo 2020.** Las 6 cuadras nuevas posteriores a 2020 de las 4 localidades se midieron, pero no tienen población: se cuentan aparte, no se les inventa gente.
- **Lo rural es aproximado**: la línea recta × 1.33 no ve ríos, cerros, presas ni el lago. Lo más probable es que las distancias reales sean algo mayores. La Isla Cerro Grande (73 habitantes) es una isla: su distancia no tiene sentido por tierra.
- **IMSS e ISSSTE solo atienden a sus derechohabientes.** La medida de salud pública los incluye; quien no tiene esa afiliación depende de los centros de salud.
- **CONAPO no está disponible**; en su lugar hay indicadores del Censo 2020 por AGEB y por localidad (`contexto_ageb.csv`, `contexto_localidades.csv`), incluido el % de viviendas sin automóvil.
- **Nombres de colonia**: casi todas las cuadras de la ciudad tienen nombre; en Irámuco, Parácuaro y Chupícuaro solo un 25–31 %, porque los registros usan el nombre del pueblo en vez de la colonia.

## Qué validar

1. **`docs/verificar_rutas.csv`**: 5 cuadras al azar con la distancia calculada y un enlace de Google Maps con la ruta a pie. Anota en `distancia_google_m` lo que dice Google.
2. **`docs/verificar_servicios_muestra.csv`** (la que ya revisas): tiene una columna nueva, `confirmado_sep_clues`. De 103 escuelas y unidades de salud, 75 están confirmadas por SEP o CLUES; 25 no; 2 están dadas de baja.
3. Los mapas `docs/figuras/fase3_*.png` (uno por servicio).
4. Tus archivos `verificacion_zonas.csv` y `verificacion_servicios.csv` no estaban en el release; los incorporo en la siguiente fase.

## Decisiones que necesito

1. **Umbral definitivo de cada servicio** (la más importante). Propuesta: preescolar 750 m, primaria 500 m, secundaria 1 km, bachillerato 2.5 km, salud 1 km, tienda 500 m, mercado o súper 1.2 km; en lo rural 2 / 2 / 5 / 10 / 5 km y 10 km. Los de la ciudad salen del Sistema Normativo de Equipamiento Urbano de SEDESOL (conviene cotejar el texto antes de publicar); los rurales son propuesta mía (no hay norma comparable). La primaria a 500 m deja a más de la mitad de la ciudad "lejos"; si prefieres 750 m o 1 km, dime.
2. **6 unidades de salud que el INEGI dibuja pero la CLUES no registra** (Solís, La Ortiga, La Encarnación, San Luis de los Agustinos, La Presa de Santa Inés y "Centro Médico la Soledad" en la ciudad). Hoy no cuentan como salud pública (pueden ser casas de salud o consultorios). ¿Las dejamos fuera?
3. **Clínica del ISSSTE en la ciudad**: el DENUE (mayo 2026) la tiene; la CLUES (agosto 2026) dice "fuera de operación" sin motivo. Hoy cuenta como operando. ¿Puedes confirmarlo (Street View o una llamada)?
4. **CECyTE Acámbaro**: el INEGI lo ubica al sur de la ciudad y la SEP 4 km al norte. Uno está mal y cambia el resultado de bachillerato público para unas 550 cuadras. ¿Puedes ver en Google Maps dónde está?
5. **Parácuaro sin secundaria**: ninguna fuente registra una secundaria en Parácuaro (la más cercana es la Secundaria Técnica 24 en el campus agropecuario, a ~4 km). ¿Te parece correcto?
6. **Tiendas en lo rural**: no hay fuente. ¿Lo dejamos como "no medible" o lo verificamos con imágenes en una muestra de localidades?
7. **Red de caminos rural**: el entorno sigue sin poder conectarse a OpenStreetMap aunque agregaste los dominios (el proxy corta la conexión; puede que el cambio de configuración necesite una sesión nueva). Si puedes bajar la Red Nacional de Caminos del INEGI (https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=794551132173) y subirla al release, rehago lo rural con caminos reales.
8. **Fecha de corte del catálogo SEP** (`cct11.csv`, `cct16.csv`): el archivo no la trae; ¿de qué fecha o ciclo escolar es?

## Algo que salió mal

- Al volver a correr la descarga, Overpass se intentó 2 veces más de las acordadas (4 en total) por un error mío. Ya corregí el script para que solo lo intente si se pide expresamente.
- La CLUES trae un espacio de más en el nombre "IMSS Bienestar"; en la primera corrida eso hizo parecer cerrados 12 centros de salud de Michoacán. Se detectó y corrigió antes de calcular las distancias.
