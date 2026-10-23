# ¿Quién está lejos hoy? Acceso a servicios y vaciamiento urbano en Acámbaro

(Título de trabajo.) Municipio de Acámbaro, Guanajuato (clave INEGI 11002), 2010–2026.

Medimos qué tan lejos —a pie en la ciudad y por carretera en el municipio— está cada manzana y cada localidad de la escuela (preescolar a bachillerato), el centro de salud de primer nivel y el abasto más cercanos, y cuánta población (niñas, niños, jóvenes, personas mayores y con discapacidad) vive lejos. También vemos dónde creció la mancha urbana desde 2010 y si las zonas nuevas quedaron lejos de los servicios.

## Estructura
```
src/             scripts numerados; se corren en orden (01_, 02_, …)
data/raw/        datos originales sin tocar (no se suben al repo; ver data/raw/LEEME.md)
data/processed/  recortes de Acámbaro y resultados intermedios (sí se suben)
docs/            fuentes, decisiones, validación, inventario y figuras
```

## Reproducir
```
pip install -r requirements.txt
python src/01_descargar.py
python src/02_recortar.py
python src/03_base_geografica.py
python src/04_inventario.py
python src/05_mapa_fase1.py
python src/06_catalogo_servicios.py
python src/07_listas_verificacion.py
python src/08_mapa_fase2.py
# … y así hasta src/22_ghsl_sin_cuadras.py; orden completo en CLAUDE.md
```

Fuentes y versiones: [docs/fuentes.md](docs/fuentes.md) · Decisiones: [docs/decisiones.md](docs/decisiones.md) · Chequeos: [docs/validacion.md](docs/validacion.md)

Límite principal: la población por manzana es la del Censo 2020 (no hay otra más reciente a ese nivel hasta el Censo 2030); la Encuesta Intercensal 2025 se usa solo para el total municipal.
