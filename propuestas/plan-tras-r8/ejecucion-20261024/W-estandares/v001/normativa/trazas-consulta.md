# Trazas de consulta normativa (W-estandares, 2026-10-24)

Fecha UTC de los barridos: 2026-10-24 (ver `fecha_utc` en `v001/entrega.json`).
MCP: nativo OpenCode (`tools.obscura.*`), sin puentes CLI. Modelo: `opencode-go/muse-spark-1.3-contributor`.
Catálogo comprobado: 37 herramientas `tools.obscura.browser_*` (back, clear_cookies, click,
close, console_messages, count, detect_forms, evaluate, extract, fill, fill_form, forward,
get_attribute, get_cookies, interactive_elements, links, markdown, navigate, network_requests,
pdf, press_key, reload, screenshot, scroll, search, select_option, set_cookie, set_storage_state,
snapshot, storage_state, tab_close, tab_list, tab_new, tab_switch, type, wait_for, wait_for_text).

## 1. https://qudt.org/schema/qudt/ — OK (fuente primaria normativa, sólo exclusión/diseño)

- URL real verificada por `browser_evaluate(location.href)`: `https://qudt.org/schema/qudt/`
- Contenido leído: Turtle del esquema QUDT, `innerText.length = 99435`.
- Localizadores (vía `browser_search` sobre el texto renderizado):
  - `rdfs:label "QUDT Schema - Version 3.5.3"` (etiqueta de versión del esquema).
  - `qudt:QuantityValue a owl:Class; rdfs:label "Quantity value"`.
  - `qudt:quantityValue a owl:ObjectProperty; rdfs:range qudt:QuantityValue`
    (propiedad que relaciona cantidad con su valor).
  - `qudt:value a rdf:Property; dcterms:description "A property to relate an
    observable thing with a value expressed as a decimal"`.
  - `qudt:FactorUnit ... owl:onProperty qudt:hasUnit` (restricción de cardinalidad 1,
    contexto de unidades factoriales, no afirmación sobre variables locales).
- Fragmento mínimo copiado a `normativa/qudt-schema-fragmento.ttl` (sólo líneas necesarias,
  transcritas de los snippets de búsqueda Obscura; sin inventar URIs de unidad).
- Regla para P1: cuando P1 pida una URI de unidad concreta se usará la oficial
  `http://qudt.org/vocab/unit/...` verificada contra el vocabulario publicado;
  W no propone ninguna URI concreta en esta entrega (0 casos, 0 unidades afirmadas).

## 2. https://www.w3.org/TR/owl-time/ — NEGATIVO limitado (bloqueo bot, no evidencia)

- Barrido 1: `browser_navigate` + `browser_wait_for_text("Time Ontology", 30s)` → timeout.
  Página renderizada: `Title: Just a moment...`, cuerpo Cloudflare
  "Performing security verification ... Ray ID: a4f82702dfefdb69".
- Barrido 2 (razonable): `browser_reload` + espera 30s → segundo timeout idéntico.
- Conclusión: resultado negativo limitado a lo examinado (desafío Cloudflare en el
  navegador compartido). No demuestra inexistencia ni vigencia del estándar;
  no se usa como evidencia de periodo alguno. P2 continúa localmente.

## 3. https://www.w3.org/TR/shacl/ — NEGATIVO limitado (bloqueo bot, no evidencia)

- Barrido 1: `browser_navigate` + espera 30s de `"SHACL"` → timeout.
  Snapshot: `Just a moment... / Performing security verification / Ray ID: a4f828c5785cdb69`.
- Barrido 2 (razonable): `browser_reload` + espera 30s → segundo timeout
  (`Ray ID: a4f82994a936db69`).
- Conclusión: negativo limitado a lo examinado. P4 ya diseñó y validó su forma
  con motor real local (ver `P4-shacl-versionado/v001/entrega.json`); no necesita
  esta URL para su veredicto.

## Principio registrado

Fuentes normativas ≠ evidencia local de unidad/periodo/jerarquía.
Ningún caso se declara resuelto por estándar. QUDT/OWL-Time/SHACL sólo sirven
para excluir usos indebidos y acotar diseños (P1/P2/P4); la integración exige
fuente que declare unidad, límites temporales o agrupación para variable/recurso
concretos, con localizador preciso y SHA-256.
