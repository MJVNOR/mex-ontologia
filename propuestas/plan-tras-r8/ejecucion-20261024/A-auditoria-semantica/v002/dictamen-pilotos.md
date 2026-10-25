# Dictamen pilotos — v002 (2026-10-24)

v001 preservado intacto (`9b93863b…`, no modificado). Read-only, sin Gemma, sin producción.

## P1-qudt/v002: OBSERVADA — no aprobada para integrar
Q1 MilliM (`http://qudt.org/vocab/unit/MilliM`) y Q3 HA (`http://qudt.org/vocab/unit/HA`) verificados, IRIs/diccionarios/huellas exactos; RDFS mínimo (1 clase + 8 props, sin QuantityValue/conversiones). estadoPropuesta en grafo: 0 (resuelto). Bloqueante: Q2 negativa trae nodo `declaracion-volumen-agua-hm3-negativa` en `propuesta-qudt.ttl` — viola "ni siquiera nodo negativo". Pendiente v003: Q2 solo en entrega.json + sello contra W corregido. Hashes: entrega `d8a05a0a…`, propuesta `fc804fa2…`, vocab `9dcff942…`.

## P4-shacl-versionado/v002: APROBADA como propuesta
Forma exacta v001 `fc301d85…` = disco = congelada v001; v001 intacta. Snapshot: conforms true, 1442 focos, 0 violaciones (1423+16+3=1442, ambos 0); fixtures 3 true + 1 false. No re-ejecutado con motor aquí (declarado-con-script). Hashes: entrega `991ad6d5…`, generar `0df65147…`.

## W-estandares/v002: OBSERVADA — no aprobada
Normas sólidas (MilliM/HA verif, HectoM3 negativo 404/ausente, OWL-Time primaria). Bloqueante: `entrega.json` fuente P2 con hash truncado 41 chars `e2f19882…ca14e`; real 64 chars `e2f19882…ca14e` (faltan 23 intermedios). Corregir en v003 sin tocar v002 congelada. Hashes: entrega `6ad442b2…`, congelada `d0c188b6…` (íntegra).

Regla: sin integración antes de los cambios pendientes reales.
