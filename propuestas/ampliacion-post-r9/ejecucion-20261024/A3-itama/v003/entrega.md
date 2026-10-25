# A3 — ITAMA Internamiento/Externamiento (v003 consolidado, 2026-10-25)

**Decisión: BLOQUEADO. Sin distribución computable.** v003 no recalcula ni
inventa resultados: consolida v002 (intacta) en snapshots byte-exactos y
re-sella todo según el dictamen D-analisis
(`reanudacion-muse/D-analisis/v001/dictamen-A3-itama.json`:
`ACEPTADA_EN_FONDO_CON_OBSERVACIONES_DE_FORMA`).

Pregunta: ¿cómo se distribuyen los registros de internamiento y externamiento
por sexo/escolaridad en un periodo común? Par `27a5c80c…--4d27a1c4…`
(`requiere_transformacion_o_catalogo`).

## 1. Fondo (verbatim de v002, raw intacto)

Raw analítico `originales-v002/resultados/analisis-a3-itama-v002.json`,
SHA-256 `526ef2d5…61d` sin cambios. Cifras: 138 XLSX y 96 CSV en repo (otros
conjuntos), **0 copias ITAMA** (0 de 8 IDs por nombre, contenido XML y
SHA-256); 6 recursos XLSX; periodo documental 2026-01-01/09-30 (metadatos, no
observable fila a fila: 0 columnas de fecha en POBLACION); muestras n=29/n=16
que no validan el universo; ESCOLARIDAD 29/29 nulo en A por ausencia de
columna (0 conceptos ITAMA, fuera de diccionarios; solo hoja heredada FEBRERO
2016); SEXO con 2 conceptos IRI y 2 diccionarios, insuficiente sin archivos
completos; poblaciones distinta_y_no_sumable. Ficha 8 ejes: claves
sin_clave_detectada, grano indefinido, unicidad/cardinalidad no acreditadas,
periodo común solo metadatos, unidades no declaradas, cobertura insuficiente.

## 2. Snapshots (`originales-v002/`, 9 archivos byte-exactos de v002)

resultados/analisis-a3-itama-v002.json, ejecucion-analisis.out,
ejecucion-pruebas.out, inventario-archivos-repo.json, evidencia-busqueda.json,
nucleo.ttl, scripts/analisis_a3_itama_v002.py,
scripts/registrar_busqueda_itama.py, pruebas/test_a3_itama_v002.py.
Equivalencias SHA-256 con sus fuentes v002 en `entrega.json` y `sello.json`.
Version/modelo originales se preservan dentro de los snapshots como
antecedente (cabeceras v002, deepseek).

## 3. Excluidos (documentados en `entrega.json`, no copiados)

`tests/test_a3_itama_v002.py` (duplicado obsoleto, 3F+1E),
`scripts/__pycache__/` (cachés), `scripts/sellar_v002.py`, `congelada.json`,
`entrega.json/md` de v002 (sealers/manifiestos viejos desfasados).

## 4. Pruebas canónicas

`pruebas/test_a3_itama_v002.py` **9/9 OK** (D-verificadas; re-ejecutadas en
solo-lectura el 2026-10-25 contra v002 intacta, sin escribir fuentes).

## 5. Reproducibilidad (evidencia original, no refactor portable)

Para reproducir: validar el SHA del snapshot contra `sello.json` y ejecutar
el canónico original; no usar el duplicado obsoleto de `tests/`.

## 6. Sello y límites

`sello.json` cubre los 11 archivos (entrega + 9 snapshots) con SHA-256 por
archivo, sin autohash; `sello.sha256` es el SHA-256 real de `sello.json`.
Límites: sin person matching, sin sumar universos, sin completar
periodos/sujetos, muestras no validan archivo entero, sin joins/promociones,
sin Gemma/contactos/web, sin tocar base IRI, R1–R9, núcleo ni centrales. Solo
escribe `A3-itama/v003`. R10 síncope pendiente.
