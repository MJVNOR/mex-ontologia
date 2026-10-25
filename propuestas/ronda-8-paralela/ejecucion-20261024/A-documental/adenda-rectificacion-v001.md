# A-documental — adenda y rectificación v001 (defecto definicion_iri M2)

Dictamen rectificado: **no_ejecutable_v001**. Material v001 SHA `555c3569…` se conserva histórico, sin aplicar.

## Error propio

`auditoria-material.json/md` afirmó “M1 forma `definition/`, M2 forma `documented-variable/`, ambas válidas”. Falso: el campo exige IRI de capa definición (`/definition/NN`); el IRI de variable (`/documented-variable/NN`) es otra capa. No equivalentes.

## Defecto

14 vínculos M2 (/65,/67,/69,/71,/72,/74,/76,/77,/79,/84,/87,/89,/97,/99) traen `definicion_iri` en capa variable. 14 vínculos M1 correctos en capa definición, pero el payload conjunto v001 sigue no ejecutable.

La evidencia subyacente de los 28 (nombre/ordinal/huellas/R7) puede ser válida; la aprobación del payload v001, no.

## R7 vs R8

R7 aprobada y congelada; lo pendiente era solo la auditoría R8. Sin re-auditar ni ampliar definiciones.

## Pendiente

M2 prepara v002 con 14 refs `/definition` exactas. Se auditará el nuevo material v002 cuando se avise hash. No se edita M2, núcleo, material v001 ni la auditoría histórica.

Detalle: `adenda-rectificacion-v001.json`.
