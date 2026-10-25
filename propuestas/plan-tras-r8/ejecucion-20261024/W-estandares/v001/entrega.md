# W-estándares v001 — paquete normativo de exclusión + atención de peticiones

Fecha UTC: 2026-10-24. Modelo: `opencode-go/muse-spark-1.3-contributor`. MCP nativo OpenCode, sin puentes.
Estado: **propuesta_para_auditar** (referencia de exclusión/diseño para P1/P2/P4).
Casos asignados: 0. Casos resueltos por estándar: **0** — las fuentes normativas no
resuelven ninguna unidad, periodo ni jerarquía local.

## Qué se hizo

1. Catálogo Obscura comprobado en sesión: 37 herramientas `tools.obscura.browser_*`
   (listado en `normativa/trazas-consulta.md`).
2. QUDT `https://qudt.org/schema/qudt/` verificado: esquema v3.5.3,
   `QuantityValue`, `quantityValue`, `value`. Fragmento mínimo en
   `normativa/qudt-schema-fragmento.ttl`. Ninguna URI `qudt.org/vocab/unit/...`
   afirmada ni inventada.
3. OWL-Time y SHACL (`w3.org/TR/...`): 2 barridos de 30s cada una, ambas bloqueadas
   por desafío Cloudflare (`Just a moment...`, Ray IDs en trazas). Negativos limitados
   a lo examinado; no prueban nada sobre los estándares.
4. Peticiones de roles: 2 barridos (globs `propuestas/**` y `ejecucion-20261024/**`).
   `P3-jerarquia-clinica/peticiones-web.json` y `C4-referencias/v001/peticiones-web.json`
   declaran cero peticiones. Detalle en `peticiones/atencion-peticiones.json`. Sin navegación adicional.

## Principio

Fuentes normativas ≠ evidencia local. QUDT/OWL-Time/SHACL sólo excluyen usos indebidos
y acotan diseños; la integración exige fuente que declare unidad, límites o agrupación
para variable/recurso concretos. C1/C4/P3 cubren sus casos (17/19/101); W no los duplica.

## Límites

Escritura exclusiva en `W-estandares/`; sin producción, semántica/shapes centrales,
manifiestos previos, grafo ni Studio. Gemma excluido, sin contactos externos, sin mensajes
a publicadores. Sin navegación genérica R8 ni trabajo documental repetido.

## Aceptación

El paquete vale como referencia auditable si: se usa sólo para diseño/exclusión;
los negativos se entienden limitados; QUDT se aplica sólo con unidad declarada;
OWL-Time sólo con límites documentados; SHACL permite ninguno e impide ambos;
PROV minCount 2 intacto. Correcciones futuras en v002 sin editar lo congelado.
