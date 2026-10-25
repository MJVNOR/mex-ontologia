# Compatibilidad R7 — nota para revisión B, v003 (staging, no instalado)

Hallazgo real de generación: 31 promociones = 28 desde fuera + 3 desde
candidatas (83/102/104); 28 coincidencias automáticas nuevas que se declaran
candidatas visibles (listas en `listas-derivadas.json`), sin ocultar ni
aprobar. `delta.json` (materialización v002, congelada intacta) predecía 17:
se corrige aquí a 45 = 17 anteriores + 28 nuevas, con la diferencia declarada
en `delta-corregido.json`. Los 3 links aceptados no cambian.

Derivación en código (bloques R7 de `integrar_entregas.py` e
`integrar_ronda_2.py`): cadena R6→R7 con SHA, lote (31,3,31), partición
(3,28) desde cobertura R6 congelada (SHA de respaldo-previo) + accepted,
viejas 17 = pre−promovidos, nuevas 28 = vivo−pre con legitimidad verificada
(variable de coincidencia respaldada por R7), revisadas 4478, candidatas
45 = 20−3+28, columnas 4495+28 = 4523, fuera 124, pendientes 140 con
conservación 1423+124+16 = 1563. Sin defaults, sin observados, sin NLP.
B audita sin editar al autor.

## Cierre v003 (revisión coordinador durante escritura)

- Eliminado el bloque viejo v002 en ambos files (sobrescribía candidatas
  16→19 y guard 140 erróneo): un solo `if r7cfg.exists():` por file.
- `sha()` confirmada en `integrar_ronda_2.py` (línea 18); `sources` existe en
  ambas funciones, sin `source_files`.
- Sin dependencia mutable sin pin: `manifiesto-respaldo.json` pinnado por
  hash literal `ea354f8a…0d5cd` antes de leer la cobertura R6.
