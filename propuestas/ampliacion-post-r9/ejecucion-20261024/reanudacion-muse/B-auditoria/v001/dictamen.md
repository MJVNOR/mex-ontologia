# Dictamen B — auditoría independiente payload + K-codigo (v001)

Fecha UTC: 2026-10-25. Carpeta: `reanudacion-muse/B-auditoria/v001`. Solo escribe esta carpeta.

## Veredicto

- Payload `payload/v001`: **aceptar** (`auditoria-b.json`, 11/11 casos).
- Código `K-codigo/v001`: **aceptar** (`dictamen-codigo.json`, 3/3 scripts).

## Payload (material congelado v001)

- 16/16 SHA iguales a `sello-payload-previo.json`; `aceptadas.json` = `df5705eaf6e0b8d8dcb0257a54a258264cda3e8adfe8655f87dfda90b9c2031c`.
- 5 filas: canon==huella, literal/nombre exactos, cobertura `respaldada_por_definicion` con variable/conjunto/diccionario/definicion_iri/iri/huella iguales; índice 1-based (11/11, 9/16, 11/16, 9/19, 27/178); copias locales+Qv003 iguales; Q-U06 API sin exigir http/completo.
- Normativa 5/5: SHA, `3.5.3` y URI canónica exacta; `unidad_qudt==normativa_uri`; QUDT http.
- `datos/unidades.ttl`: 60/60 triples exactos (5×12), 5 sujetos r10, 0 prohibidos (sin M3/QuantityValue/factores/conversiones); MW/GWh como filas `Unidad de Medida` sin transferencia; Toneladas/hm³ excluidos.
- `shapes/adicionales.ttl` = S `shapes.ttl` (`0f342433…`): 6/6 IDs iguales, sin `sh:closed`, targets en 3 clases, 3 `FILTER NOT EXISTS`, 5 `SPARQLConstraint`, controles min/max/nodeKind/class/datatype.
- S motor real: negativo 15, positivos/portal322405/studio323014 0 violaciones, 0 ignoradas.
- Base 130/130 intacta; config byte-a-byte; Qv003 23/23 y W 12/12 sellos ok.
- `payload-origenes.json`: 5/6 iguales; desvío solo en wrapper `S-shacl/v001/sello.json` (declarado `f1576589…`, real `7ed238db…`); sus 9 artefactos verifican y el `shapes.ttl` consumido está intacto, así que no afecta bytes instalables. Se deja constancia, no se rechaza por ello.
- No se inventan aprobaciones en payload: K `_auditorias` sobre `payload/v001` rechaza (sin `auditorias/`).

## Código K

- SHAs verificados: integrador `05e834fd…`, ampliar `9370e83e…`, consolidar `b1b32231…`.
- Loader: `cargar()` exige a+b con dictamen aceptar, SHA exacto y 11/11 IDs sin duplicados; `construir()` y `cargar_shapes()` pasan por `cargar()`.
- PROV: `allowed` incluye `PROV`; `_datos` emite `prov:wasDerivedFrom`×2 y R6e lo exige como `sh:path`; I antiguo fallaba aquí.
- IDs: K exige `actual==declared` sobre NodeShapes reales; I no lo comprobaba.
- `_datos`/`_shapes`/`_validar_aceptadas` pasan sobre material real (60 y 73 triples); I `_datos` falla por `lang='es'` y su `_shapes` por PROV.
- Hooks mínimos contra vivos (vivos sin R10): ampliar +3 líneas, consolidar +6 líneas, patrón ronda-9, sin otros cambios.

## Seguimiento

Prueba completa real se ejecutará con este dictamen + A. Revisión de código ya cerrada aquí; queda seguimiento tras V-tests.
