# data/raw — datos crudos

Esta carpeta no se sube al repositorio. `python src/01_descargar.py` la llena sola con todo lo que tiene URL directa (lista completa en `docs/fuentes.md`) y escribe `manifiesto.csv` (tamaño y huella sha256 de cada archivo).

## Lo que está en el release `datos-crudos` (lo baja `01_descargar.py`)

| Archivo | Qué es | Subido |
|---|---|---|
| `ESTABLECIMIENTO_SALUD_202608.xlsx` | CLUES, corte agosto 2026 | 2026-10-23 |
| `cct11.csv`, `cct16.csv` | Catálogo de centros de trabajo SEP, Guanajuato y Michoacán | 2026-10-23 |
| `verificacion_zonas.csv`, `verificacion_servicios.csv` | (opcionales) revisión de las listas de verificación en Google Maps | pendiente |

CONAPO no está disponible y ya no se busca (D24).

La red de caminos de OpenStreetMap solo se intenta bajar si se pide: `python src/01_descargar.py --solo osm_caminos` (falló en el entorno de trabajo; ver `docs/fuentes.md`).

## Historial: instrucciones originales para subir CLUES, SEP y CONAPO

### Lo que Alejandro debía bajar y subir al release `datos-crudos`

Estos tres no se pueden bajar desde el entorno de trabajo (sitio bloqueado, caído o con certificado defectuoso). Súbelos como *assets* del release con etiqueta **`datos-crudos`** de este repositorio (GitHub → Releases → Draft a new release → tag `datos-crudos`), **con exactamente estos nombres**. El script los baja de ahí.

### 1. CLUES vigente → `clues.zip`
- Página: Secretaría de Salud, DGIS, "Catálogo de Clave Única de Establecimientos de Salud (CLUES)": http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html
- Qué bajar: el archivo más reciente de **establecimientos de salud** (se publica mensual, nombre tipo `ESTABLECIMIENTO_SALUD_AAAAMM.xlsx` o `.zip`). Nacional completo; no hace falta filtrar.
- Si la DGIS no abre: datos.gob.mx → buscar "CLUES" (conjunto "Establecimientos de salud").
- Subirlo comprimido como `clues.zip` (si ya viene en zip, solo renómbralo).
- Anota el mes del corte (aparece en el nombre del archivo).

### 2. Catálogo de escuelas SEP vigente → `sep_escuelas.zip`
- Opción A (preferida): datos.gob.mx → conjunto **"Catálogo de centros de trabajo"** de la SEP (`datos.gob.mx/dataset/catalogo_centros_trabajo_sep`), recursos de **Guanajuato** y **Michoacán** (Acámbaro colinda con Michoacán), el más reciente, con latitud y longitud.
- Opción B: SIGED, buscador de escuelas: https://www.siged.sep.gob.mx/SIGED/escuelas.html → Entidad *Guanajuato*, municipio *Acámbaro* → Buscar → botón de descarga a Excel. Repetir para los municipios vecinos: Jerécuaro, Salvatierra, Tarimoro, Tarandacuao (Gto.) y los de Michoacán que colindan.
- Debe incluir: clave de centro de trabajo (CCT), turno, nivel educativo (preescolar, primaria, secundaria, media superior), sostenimiento (público/privado), estatus (activo) y coordenadas.
- Meter todos los archivos en un solo `sep_escuelas.zip`. Anota la fecha o ciclo escolar del corte.

### 3. CONAPO, índice de marginación urbana 2020 → `conapo_imu2020_ageb.zip` y `conapo_imu2020_colonia.zip`
- Página: https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372
- Los enlaces de esa página apuntan a `conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/...` y hoy dan error 404 desde aquí. Si a ti te abren:
  - **Por AGEB**: `Marginacion/IMU_2020.zip` → subir como `conapo_imu2020_ageb.zip`.
  - **Por colonia**: `Colonia/IMC_2020.zip` (tabla) y `Colonia/imc2020_shp.zip` (mapa) → ambos dentro de `conapo_imu2020_colonia.zip`.
- Si tampoco te abren, avísame y lo marcamos como faltante (el análisis no depende de él; sirve para el contexto social y para tener los nombres y polígonos de colonias del explorador).

## Opcional (no bloquea nada)
- **EIC 2025, tabulados municipales de Guanajuato** (discapacidad, grupos de edad a nivel municipio con intervalo de confianza): https://www.inegi.org.mx/programas/eic/2025/ → pestaña *Tabulados* → Guanajuato. Subir como `eic2025_tabulados_gto.zip`. Ya tenemos de la EIC 2025 el conjunto de datos abiertos con el total municipal y los grupos quinquenales de edad.
