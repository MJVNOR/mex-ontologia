# Auditoría material v003 — B-tecnica (aceptar)

- Payload: `materializacion/v003/aceptadas.json`, SHA `db3167f98a308cc4219202cfa5ce8587923dd05bc4664d30d83375872309f0d9` (calculado por código, coincide con `congelada.json`).
- Composición: 0 reglas, 0 conceptos, **28 vínculos** (M1 v001 14 + M2 v003 14).
- Dictamen: **aceptar** 28/28. Detalle máquina en `auditoria-material-v003.json` (SHAs por código). Auditorías viejas (v001 observada) intactas como antecedente.

## Verificación exacta por vínculo (sin normalización ni alias)

Por cada uno: `definicion_iri` == IRI `/definition/...%2F<ord>` exacto
(regex, sin `/documented-variable/`); concepto == variable R7; descripción ==
literal local exacto `Pendiente de especificar` (fila y vínculo); diccionario
y recurso exactos; `huella_fila` recomputada == declarada; nombre == campo y
ordinal == posición; correspondencia R7 `candidata_por_nombre`; criterio solo
físico (sin `0000`/CIE-10/catálogos/valores; se excluyó el nombre del campo
del barrido para no falsear con `CODIGOCIE*`).

## Defectos M2 fuera del payload

IRI `/documented-variable/` (v001) y descriptor nacional + afirmación
`0000`/CIE-10 (v002): 0/28 presentes en v003 (barridos a cero por código).
M2 v003 trae IRI `/definition/` exacto y literal local (verificado contra
asignación y md v003 corregida).

## Físico/semántico y SHA roots

`congelada.json`: 13/13 SHAs verificados por código; `aceptadas_sha256`
coincide. Fuentes copiadas idénticas (aceptadas-r7, cobertura-r7,
inspección, M1/M2, manifiesto-r7, recibo-r7).

## Notas

R7 YA auditada; comentarios md heredados de autores sobre pendientes son
inexactos y no cambian este dictamen. Solo v003 auditada aquí; nada editado
fuera de `B-tecnica/`; IDs exactos, sin alias.
