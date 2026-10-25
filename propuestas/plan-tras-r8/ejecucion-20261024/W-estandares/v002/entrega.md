# W-estándares v002 — respuesta a P1-W-01..03 y P2-WEB-01 (v001 intacta)

Estado: **propuesta_para_auditar**. 0 casos, 0 promovidos. Puente término↔norma únicamente.

## P1 — unidades

- **P1-W-01 Milímetros: VERIFICADO** → `http://qudt.org/vocab/unit/MilliM` (http),
  symbol `mm`, `Millimetro`@es.
- **P1-W-02 Hectómetros cúbicos: NEGATIVO normativo** → `HectoM3` da 404 y no existe
  en el índice QUDT 3.5.3 (sí existen DecaM3/MilliM3/CentiM3). Alternativa verificada:
  `http://qudt.org/vocab/unit/M3` (símbolo m³, exponente 3 sobre unit:M). Sin alias por parecido.
- **P1-W-03 Hectáreas: VERIFICADO** → `http://qudt.org/vocab/unit/HA` (http),
  symbol `ha`, `Hectare`@en. `HectoHA` (P1 v1) da 404: RECHAZADO.

## P2 — OWL-Time

- **P2-WEB-01 ATENDIDA** con ontología del repo oficial `w3c/sdw-time`
  (`rdf/time.ttl`, baseURI `http://www.w3.org/2006/time`, mod. 2026-10-06):
  `ProperInterval` ⊑ Interval, disjunta de Instant; `hasBeginning`/`hasEnd` rango Instant.
  Advertencia: `:inXSDDateTime` está DEPRECADA; usar `:inXSDDateTimeStamp`.
- `w3.org/TR/*` (incl. fechadas) bloqueado por Cloudflare: 2×30s cada una, Ray IDs en trazas.

## Límites

v001 sin editar; escritura solo en `W-estandares/v002/`; sin Gemma/contactos/CAPTCHA;
normativa ≠ evidencia local. Correcciones en v003.
