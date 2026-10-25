# Interfaces minimas de integracion futura (R9, solo si la forma se aprueba)

1. `shapes/semantica.ttl`, `shape:VariableDocumentada`: anadir UNICAMENTE el
   bloque `sh:sparql` de `propuesta/shape-exclusion-significado.ttl`.
   No tocar `maxCount 1` de cada significado ni los `minCount` de PROV.
2. Versionado: subir `format_version` solo si cambia el esquema de entrega;
   `release` cambia solo con ronda aprobada. Anexar manifiesto nuevo; jamas
   reescribir manifiestos R1-R8.
3. Validacion: suite Python completa + SHACL central con alcance declarado
   (triples de carga vs total Studio) + replicas de estas 4 fixtures.
4. Esta entrega no integra nada: no modifica semantica, shapes centrales,
   manifiestos previos, grafo ni Studio.
