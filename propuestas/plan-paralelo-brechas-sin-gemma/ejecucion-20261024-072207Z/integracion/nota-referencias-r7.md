# Referencias de catálogo en R7 — lectura del diagnóstico intermedio (no instalada)

Fuente: `integracion/diagnostico-conteos-r7.json:reporte_intermedio`
(antes-guards) vs cobertura R6 de `integracion/respaldo-previo`.
Comparación directa por bytes, sin aceptaciones nuevas ni conteos falseados.

## Variables y correspondencias (confirmado por diff directo)

| Indicador | R6 backup | Intermedio R7 | Delta |
| --- | ---: | ---: | --- |
| respaldada_por_definicion | 1392 | 1423 | +31 (28 fuera + 3 candidatas: 83/102/104) |
| fuera_del_nucleo_actual | 152 | 124 | −28 |
| candidata_sin_definicion_suficiente | 19 | 16 | −3 |
| conceptos | 1075 | 1106 | +31 nuevos `sinac-*` |
| documental_revisada | 4475 | 4478 | +3 links aceptados (83/102/104, sin cambio) |
| candidata_por_nombre | 20 | 45 | 17 anteriores + 28 nuevas |
| columnas_con_correspondencia | 4495 | 4523 | +28 |

28 nuevas = columnas sin correspondencia previa que ahora coinciden por nombre
exacto con una variable respaldada por R7 (verificadas una por una contra
`listas-derivadas.json` de compatibilidad-v003): visibles, NO aprobadas,
NO ocultas. 099 materializada fiel (`r7-s2-099`, `sinac-cluescertifica`).

## Referencias: 9 sin resolver (antes 1), 8 con recurso (antes 16)

Total declarado idéntico: 9+8 = 17 = 1+16. **Cero referencias nuevas**:
las 31 filas SINAC traen `Catálogo de referencia` vacío, luego el core no
crea ningún nodo de referencia para ellas; no hay identidad nueva de
catálogos en ningún punto (ni `CatalogoPublicado` SINAC ni equivalencias).

El 9 es un valor INTERMEDIO (antes-guards), no final: las 8 de diferencia son
las resoluciones propias de la fase agentes (`resoluciones_catalogos`), que en
la corrida fallida aún no se habían aplicado al grafo. En corrida completa y
exitosa vuelven a `sin_resolver = 1`, `con_recurso_identificado = 16`, como
en R6. **No afirmar "todas 1" desde el intermedio**: el valor final se lee
tras la corrida completa (el helper `cerrar_ronda_7.py` lo exige post-sync).

Congelados R7 (v001/v002, materialización, compatibilidad) intactos.
