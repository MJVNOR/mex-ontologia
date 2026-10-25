# A-documental — auditoria material R8 (28 vinculos)

Dictamen: **aceptar**. `aceptadas_sha256 = 555c35697c86fd026d84d09a4bc02cc549237c5170c70d93c94ed5056d913fdf` (calculado por codigo, coincide con `congelada.json`).

Exacto: 28 vinculos, 0 reglas, 0 conceptos. Alcance: solo 28 correspondencias fisicas SINAC con significado ya respaldado R7; sin codigos, vigencias, joins ni identidad de catalogos nuevos.

## Verificado por vinculo (no por nombre solo)

- Nombre exacto + ordinal /106 unico en esquema (inspeccion) y fila (diccionario 22202305), mismo conjunto 940de7d8.
- `huella_esquema 9b46e1c0…` + `huella_fila` coinciden con cobertura-r7 (variable `respaldada_por_definicion`, mismo concepto) y copia exacta de M1/M2 `vinculo_propuesto` en estado `propuesta_para_auditar`.
- Alcance por id: recurso 46977217 + diccionario/fila ordinal; `definicion_iri` con mismo ordinal (M1 forma `definition/`, M2 forma `documented-variable/`, ambas validas).
- Detalle por id + motivo en `auditoria-material.json` (28 dictamenes `aceptar`).

## Fuentes congeladas + primarias (SHAs recalculados, todos OK)

- 13/13 entradas de `congelada.json` coinciden (aceptadas, base-semantica, 11 fuentes).
- Copias idénticas a primarias vivas: cobertura-r7 = `E/cobertura-r7.json` (4627c2ba…), recibo-r7 = `reports/ronda-7.json` (19705497…), inspeccion = `data/portal/contenido-inspeccion.json` (61861aab…), M1/M2 entregas + congeladas = vivos.
- R7 manifiesto/auditorias estrictas intactos como entradas congeladas (aceptadas-r7 0d58255d, A 7daa6519…, B 524d2b37…).

## Aclaracion R7 vs R8

R7 YA aprobada y congelada. El “auditoria A/B pendiente” de `M1-sinac-entrega.md` es la auditoria R8 documental (esta), no R7. No se re-auditan ni amplian definiciones: el significado solo se cita como respaldado R7.

## Estado general

Comprobacion preliminar: 16/16 roles congelados, 202 casos (28 propuestas, 172 brechas, 2 accesos), sin discrepancias. Seleccion final queda a la auditoria de codigo posterior.

Metodo: solo lectura, sin instalar, sin editar material. Referencias ruta+SHA en el JSON.
