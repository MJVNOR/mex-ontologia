# Trazas v002 (W-estandares, 2026-10-24) — preserva v001, no la edita

MCP nativo OpenCode (`tools.obscura.*`), sin puentes CLI/proxy ni terceros. Sin CAPTCHA.

## P1: unidades QUDT (peticiones P1-W-01..03)

- https://qudt.org/vocab/unit/MilliM → OK. Título `http://qudt.org/vocab/unit/MilliM`;
  tipos DerivedUnit+Unit; symbol `mm`; label `Millimetro`@es; scalingOf unit:M. (P1-W-01 VERIFICADO)
- https://qudt.org/vocab/unit/HA → OK. Título `http://qudt.org/vocab/unit/HA`;
  symbol `ha`; label `Hectare`@en; Area; x10000. (P1-W-03 VERIFICADO)
- https://qudt.org/vocab/unit/HectoHA → 404 Not Found. (HectoHA de P1 v1 RECHAZADO, alias por parecido)
- https://qudt.org/vocab/unit/HectoM3 → 404 Not Found. Índice https://qudt.org/vocab/unit/:
  `HectoM3`/`HectoM2`/`CubicHectoM` sin matches; solo existe unit:HectoM (longitud).
  Análogos sí existentes: DecaM3, MilliM3, CentiM3. (P1-W-02 NEGATIVO normativo)
- https://qudt.org/vocab/unit/M3 → OK (alternativa normativa: symbol `m³`, FactorUnit exponente 3 sobre unit:M).
- Regla http vs https: sujetos RDF reales en `http://qudt.org/vocab/...` (isDefinedBy
  `http://qudt.org/3.5.3/vocab/unit`); la URL navegable https no impone la URI RDF.

## P2: OWL-Time (petición P2-WEB-01)

- https://www.w3.org/TR/2020/REC-owl-time-20200326/ → 2 barridos 30s (navigate+wait, reload+wait):
  desafío Cloudflare `Just a moment...`, Ray IDs a4f83afcdae0f09d / a4f83bca3e0af09d. Negativo limitado.
- Repo oficial w3c/sdw (rama gh-pages, dir time/): solo stub `index.html` con meta-refresh a
  `https://w3c.github.io/sdw-time/` + abstract; sin términos (innerText 673 cars, 0 matches).
- Repo oficial vigente w3c/sdw-time (gh-pages): namespace doc `time.html` (namespace
  `http://www.w3.org/2006/time#`, fecha 2021-02-01) con alternates `./rdf/time.ttl|.rdf|.jsonld|.nt`.
- Ontología https://raw.githubusercontent.com/w3c/sdw-time/gh-pages/rdf/time.ttl → OK:
  82194 caracteres; ProperInterval x38; hasBeginning x2; fragmentos en `owl-time-evidencia.txt`.
  Hallazgo: `:inXSDDateTime` está DEPRECADA (`owl:deprecated true`, usar `:inXSDDateTimeStamp`).

## SHACL fechado (sondeo opcional)

- https://www.w3.org/TR/2017/REC-shacl-20170720/ → 2 barridos 30s: Cloudflare,
  Ray IDs a4f8407c5db71002 / a4f8414b6b991002. Negativo limitado; P4 no lo necesita
  (forma validada con motor real local en P4 v001).

## Principio

Puente término↔QUDT/OWL-Time exclusivamente normativo y por id de petición.
Ningún caso local promovido desde URIs; `HectoHA`/`HectoM3` no se aceptan por parecido.
