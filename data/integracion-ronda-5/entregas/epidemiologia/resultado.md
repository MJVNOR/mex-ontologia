# Resultado — epidemiología (ronda 5)

Rol: epidemiologia. Conjunto: Vigilancia Epidemiológica (`dca16d84-dbf0-4501-b702-dc6372a480ea`), diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d`.

## Cuentas verificadas

- Asignados: 25 significados, 0 correspondencias actuales.
- Decisiones: 25 (pendiente 25, proponer 0, artefacto_documental 0).
- Reglas nuevas: 0. Conceptos nuevos: 0. Vínculos: 0. Decisiones de columnas: 0.
- Huellas de fila diccionario coincidentes con cobertura.json: 25/25; descripciones y estado `fuera_del_nucleo_actual` coincidentes 25/25.
- Catálogo declarado: vacío en las 59 filas del diccionario (verificado en captura fresca).
- Columnas físicas observadas en hoja SUIVE del xlsx 2022 para los 25 casos (posiciones 9, 11, 13, 23–44): presencia confirmada, significado no documentado.
- Base ronda 4 inmutable: huellas de `ontologia/semantica.json`, `data/semantica/cobertura.json`, `ontologia/revision-ronda-4.json` coinciden con `base.json`.
- Solicitudes a catalogos-web: 3 (`solicitudes_web.json`).

## Decisiones individuales

- `cve_cie10` ("Clave"): pendiente. Ejemplo con códigos CIE no acredita objeto ni catálogo; regla r3a6-005 prohíbe expandir CIE por ejemplo. Requiere SW-EPI-02.
- `acumulado` ("Acumulados"): pendiente. Sin objeto ni periodo de acumulación. Requiere SW-EPI-01.
- `de01_a_04` ("Total de personas en vigilancia entre 1 y 5 años"): pendiente. Contradicción nombre (01–04) vs descripción (1–5) más solape en edad 5 con `de05_a_09`; las reglas hermanas r3a6-007..016 conservan ese borde literal. Proponer exigiría elegir intervalo. Requiere SW-EPI-03.
- `se_ignoran` + 11 columnas con sufijo `f` + `se_ignoraf`: pendiente. Descripción "Pendiente de especificar"; el sufijo `f` no se interpreta por simetría ni por proximidad a `totalf`. Requieren SW-EPI-01.
- `ssa`, `imss_ord`, `issste`, `otras`, `imss_sol`, `d_if`, `pemex`, `sedena`, `sedemar`: pendiente. Siglas sin objeto contado declarado. Requieren SW-EPI-01.

## Búsqueda negativa documentada

Se revisaron: diccionario completo fresco vía API datastore (59/59 filas, 2026-10-23), fila completa con tipo/formato/ejemplo/catálogo en `contenido-inspeccion.json`, esquema físico hoja SUIVE, inventario, nota del conjunto en CKAN ("Repositorio Integral de Datos para la Supervisión y Análisis Epidemiológico", sin documentación por columna), reglas r3a6 del dictamen previo (lote-3) y cobertura. Ninguna fuente fija objeto, partición, periodo, catálogo o intervalo para los 25 casos. No se promete solución pública; las 3 solicitudes web dicen la evidencia exacta que desbloquearía cada caso.
