# B — Revisión I v003: código provisional NO APTO (bloqueantes demostrados)

I-código/v001 sin sellar (provisional). v001/v002 de B preservados; autor y
producción sin modificar (lectura + ejecución en tmp). Suite staging real:
16/17, `test_valido` en ERROR. SHAs exactos y detalle en `revision-i.json`.

## Bloqueantes (ejecutados, no hipotéticos)

- **D1** `integrar_ronda_9.py:152-154` — PROHIBIDO por substring rechaza su
  propio `datos/propuesta-qudt.ttl`: `QuantityValue` (L7, comentario) y
  `https://qudt.org/vocab/unit` (evidenciaNormativa L18/L31). El test
  `test_conversion_colada` solo pasa con TTL sintético sin comentarios.
- **D2** `:226-229` — lo mismo rechaza su propio `vocabulario-minimo.ttl`
  (L10: comment con `qudt:QuantityValue`). La prohibición por token rompe el
  vocab que dice `SinQuantityValue`.
- **D3** `:250` — `txt.count("sh:sparql")!=1` rechaza el shape P4 v001 real
  pinnado por SHA (comentario L9 + predicado L12 = 2). Pin y conteo se
  contradicen en el mismo archivo.
- **D4** — happy path roto (`test_valido` ERROR). Fe de errata: se descartó
  hipótesis de código muerto en `make_root` por relectura byte-exacta.

## Cobertura (demostrado en RAM / lectura)

- **D5** `:210-231` — bypass PASA con sus reglas: predicado extra +
  triple en IRI variable + 3er sujeto de otra clase + `unidadLiteral="OTRA"`.
  De 26 triples/12 predicados solo se verifican sujetos tipados y `unidadQudt`.
  Exigido: whitelist estructural total + literal exacto por predicado.
- **D6** `:193-195` — presencia por substring en texto: literal erróneo en el
  triple pasa si figura en un comentario.
- **D7** `:95-99` `_clave` — iguala `Milimetros==Milímetros`,
  `Hectareas==Hectáreas`; pin v002 ASCII vs P1 v003 exacto (sujetos y tildes).
  Exigido: literales EXACTOS, sin `_clave`.
- **D8** `materializar.py:66-68` — chequeo por bloques-substring pinnado a v002.
- **D9** — 15/17 tests sintéticos en tmp; `fixtures/declaraciones-ejemplo.json`
  sin ningún test que lo cargue; nada ejecuta `cargar()` sobre staging real.
- **D10** — `BASE` absoluta de máquina en `build_v003.py:7`/`verify_v003.py:7`.

Contraste: P1 v003 (sello 22/22 OK) ya aplica exactitud estructural en su
ámbito; el integrador no lo adoptó. Desbloqueo en `revision-i.json`.
