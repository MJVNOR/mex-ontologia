# D-analisis v001 — revisión independiente (Muse 1.3, 2026-10-24)

Tres análisis separados. Ninguno aprueba joins; ninguna muestra se presenta como universo.

## T-top50 v002 — ACEPTADA

Ranking reproducido: 3916 pares (assert interno), 1191 candidatas, top50 con 50 IDs
únicos, orden score desc + id asc, top1 ITAMA `27a5c80c…--4d27a1c4…` 5.0, carriles
A3=1, A1=2, A2=4 por ID exacto. Publicador `generar(root,outdir)` con guardas
(fuentes, selladas incl. v001, solo 3 artefactos en outdir); tests 10/10 OK.
Sello: 10/10 archivos coinciden. Uso solo como priorización candidata.

## A1-911 v002 — ACEPTADA, resultado BLOQUEADO válido

Bloqueo con fuentes reales: duplicado Q1 (`54285a13` == `6ce17dd1`, sha
`9d710cb…`, hoja y URL de procedentes); Q2 improcedentes `0df8592f` sin MUNICIPIO;
muestra A sale del duplicado (cero observaciones de improcedentes); sin partición
acreditada. Sello 6/6 OK, tests OK. Sin proporción, sin join.

## A2-registro-civil v002 — ACEPTADA, resultado BLOQUEADO válido

Grano distinto no basta por sí solo para impedir comparar agregados; el bloqueo
actual se sostiene en falta de cobertura/validación: total≠suma, meses faltantes,
unicidad/cardinalidad no acreditadas, ámbito solo de registro. H-02/H-04/B-A2-11/
B-A2-12 verificadas. Sello 8/8 OK, tests 5/5 OK. Sin comparación, sin join.

## A3-itama v002 — ACEPTADA EN FONDO, observaciones de forma

Bloqueo válido: 0 copias ITAMA (138 XLSX/96 CSV ajenos, búsqueda acotada por
ID/nombre/contenido/SHA), escolaridad ausente de hojas y diccionarios, periodo
solo documental, poblaciones no sumables. Pruebas canónicas 9/9 OK.
Forma (solo MD, corrige coordinador en nueva versión sin tocar autores): sello
desactualizado — entrega.json/md y sellar difieren del manifiesto; faltan en el
manifiesto nucleo.ttl, evidencia-busqueda.json, registrar script y tests/
duplicado (ese extra falla 3F+1E); falta sidecar congelada.sha256.

## Archivos

`dictamen-T-top50.json`, `dictamen-A1-911.json`, `dictamen-A2-registro-civil.json`,
`dictamen-A3-itama.json` (SHA exactos dentro), `sello.json`.
Solo se escribió esta carpeta; entregas selladas intactas.
