# Resumen — entrada de integración (29 correspondencias)

## Objeto

`entrada_integracion_29.json`: las 29 propuestas aprobadas en formato de
`vinculos_documentales_revisados` (`recurso, campo, columna, diccionario,
concepto, descripcion, huella_esquema, huella_fila_diccionario, criterio`),
con descripción literal, campos exactos y ambas huellas. Lista para que el
integrador la aplique tras regenerar cobertura.

## Archivos (solo esta carpeta)

- `preparar_integracion.py`: construye la entrada desde `propuestas.json`
  CONGELADA (SHA-256 `83593587…cc9508e1d2`; aborta si cambia) y valida
  contra el estado central. Solo escribe `entrada_integracion_29.json`.
- `test_entrada_integracion.py`: 12 pruebas (SHA congelado, formato,
  revalidación central, simulación 865 sin solapes, sin catálogos,
  conceptos vigentes, 6 mutaciones rechazadas).
- `entrada_integracion_29.json`: artefacto para el integrador.
- No se modificó la entrega aprobada (`propuestas.json`, SHA intacto) ni
  ninguna fuente central, motor o revisión de cobertura.

## Verificación

```powershell
uv run python propuestas/ronda-3/agente-2-correspondencias/preparar_integracion.py
uv run python propuestas/ronda-3/agente-2-correspondencias/test_entrada_integracion.py
```

12/12 OK. Simulación: 836 previas exactas (claves únicas) + 29 nuevas sin
solape = 865. No se asume ningún total de candidatas: la cobertura se está
regenerando en el chat integrador y los conteos posteriores pueden variar;
lo único fijado aquí es 836 + 29 disjuntos.

## Límites

- Cada entrada exige columna física existente, (recurso, campo, conjunto)
  iguales al esquema, huellas recalculadas, descripción literal que
  identifica una variable respaldada única, concepto vigente coincidente y
  recurso/hoja de observaciones (no catálogo).
- Cualquier huella, campo, columna o concepto alterado es rechazado
  (probado por mutación, incluido solape con una previa).
- Esta entrada no integra por sí sola: el integrador la aplica y regenera.
