# Resultado documental — rol nacimientos (ronda 5)

Asignados: 54 significados + 5 correspondencias de columna (candidatas por nombre).

## Decisiones

- **Proponer: 1** — `RESIDEEXTRANJEROD` (%2F18, "Indicador textual de si la madre es residente extranjera").
  Regla `r5-nac-resideextranjerod-no_especificada`, concepto nuevo `residencia-extranjera-madre`
  (representación `no_especificada`). Revisa el dictamen previo
  (`r3a7-nac-resideextranjero-codigo`, que dejaba el par D pendiente por contradicción):
  no se unifica con `RESIDEEXTRANJERO` %2F17 (texto distinto, tipo distinto). 1 vínculo + 1 decisión de columna.
- **Pendiente: 53** — todas con descripción `Pendiente de especificar` en la fila del diccionario,
  verificada por recomputación de huella (54/54 OK). No se aprueba por nombre ni por ejemplo.
  Revisa dictamen previo r4-investigación (localización de las 53) y r4-lote-3 (prohibición de
  interpretar el nombre, candidatas sin promoción): se confirma, la fuente local no cambió.
- **Columnas: 5 pendientes** — se mantienen `candidata_por_nombre` (CLUES, MUNICIPIOCERTIFICA(D),
  LOCALIDADCERTIFICA(D)); núcleo: CLUES queda candidato, pista de nombre sin promoción.

## Verificación

- Huellas de fila recomputadas: 54/54 coincidentes con `asignacion.json`.
- Huella de esquema recomputada sobre `data/portal/inspecciones/46977217-...json#tablas[0]`: `9b46e1c0...` OK;
  posiciones 18/83/102–105 verificadas (106 campos, hoja `SINAC 2022 26-09-22`).
- Negativo CLI 2026-10-23: el portal responde página Web Application Firewall a la descarga del xlsx
  y al API datastore; archivo descartado. Derivado a `solicitudes_web.json` (8 solicitudes temáticas).

## Archivos

- `entrega.json` (54 decisiones de significado, 6 de columna, 1 vínculo, 1 regla, 1 concepto, fuentes, 53 pendientes precisos)
- `solicitudes_web.json` (8 solicitudes a catalogos-web)
- `listo.json` (sha256 + conteos, estado completo)
