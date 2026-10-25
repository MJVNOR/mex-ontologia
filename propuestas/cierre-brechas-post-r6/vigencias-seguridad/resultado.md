# Vigencias seguridad (V13, V14) — resultado 2026-10-24

Dos casos asignados, una decisión por ID. Ambas: **sigue_pendiente** (sin propuesta de resolución).

## V13 — cat_municipio, Incidencia delictiva municipal (2015–2025)

- Novedad real: se examinó por primera vez el interior del **Diccionario** del conjunto
  (recurso `5f46e4b8`, copia `evidencia/V13_diccionario.xlsx`, sha `2a80ac6b…`).
  Fila R3: `Cve. Municipio → Catálogo de referencia: catalogo_municipios`
  ("Relaciona la clave del municipio con su nombre", ejemplo 260001).
  Referencia **nominal**: sin edición, versión, fecha, corte SESNSP, sin id de recurso
  y sin vínculo con 2015–2025. Avance de contexto, no acredita F3+F4.
- Reverificación CKAN en vivo 2026-10-24 (`evidencia/api_93ca5e1c_2026-10-24.json`,
  sha `97bcc5d6…`): `version=null`; recurso Catálogo `36d3ac85` size 10194 = local,
  `start/end 1989-06-04` (placeholder), `publisher "-"`; los CSV 2015–2025 sí traen
  rango anual real. El portal distingue datos fechados de catálogo sin fechar.
- Catálogo local (`evidencia/V13_catalogo.xlsx`, sha `84bb6fcd…` = asignación):
  hoja `cat_municipio`, core `creator SESNSP / created 2015-06-05 / modified 2026-01-22`,
  sin versión/corte. Nota: el diccionario dice `catalogo_municipios` y la hoja se llama
  `cat_municipio` — ni siquiera hay identidad nominal exacta; sin joins automáticos.
- Brecha exacta que subsiste: falta declaración del publicador con edición/versión/fecha
  y corte SESNSP de cat_municipio vinculada a 2015–2025 (DEP-CAT-R6-05).

## V14 — cat_entidad, Víctimas del fuero común (2015–2025)

- Novedad real: interior del **Diccionario** (recurso `a8a09044`,
  copia `evidencia/V14_diccionario.xlsx`, sha `b3872e4b…`). Fila R3:
  `Clave_Ent → Catálogo de referencia: catalogo_entidades`
  ("Describe la entidad en donde se registraron las víctimas", ejemplo 26).
  Igual que V13: solo nombre, sin edición/versión/fecha/corte ni vínculo con 2015–2025.
- Reverificación CKAN en vivo 2026-10-24 (sha `3ac8a95d…`): `version=null`;
  Catálogo `7f3aca28` size 10999 = local, placeholder 1989-06-04, sin editor.
- Catálogo local (sha `96776ca8…`): hoja `cat_entidad` (32 entidades), core
  `creator Practicante2`, sin versión/corte. Mismo desajuste nominal
  (`catalogo_entidades` vs `cat_entidad`).
- Brecha exacta que subsiste: falta declaración del publicador con edición/versión/fecha
  y corte SESNSP de cat_entidad vinculada a 2015–2025 (DEP-CAT-R6-05).

## Límites y notas

- La página SESNSP (observada vía webfetch 2026-10-24: bloques 2015–2025 y diccionario
  de metodología, fecha 16-10-2026) es contexto general sin vínculo con los recursos
  locales; no se presenta como evidencia de vigencia. Descarga directa bloqueada por
  challenge anti-bots: sin copia primaria, no insistir por esa vía.
- `web-obscura/` revisada: solo `disponibilidad.json`, sin resultados para V13/V14;
  `peticiones-web.json` propia publicada. Navegador compartido no tocado.
- Sin joins por compartir Clave; sin identidad automática de catálogos; sin extender
  a otros conjuntos/periodos. Solo propuestas revisables; integra auditará.
