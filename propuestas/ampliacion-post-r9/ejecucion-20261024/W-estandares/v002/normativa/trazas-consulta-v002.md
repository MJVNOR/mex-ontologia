# Trazas de consulta v002 (W-estandares, ampliacion post-R9)

Fecha UTC de consulta: 2026-10-24. Unico navegador: Obscura via MCP nativo OpenCode
(`tools.obscura.browser_navigate`, `tools.obscura.browser_evaluate`). Sin puentes CLI,
sin proxy, sin contactos a publicadores. No se repitio ninguna busqueda agotada:
hm3/HectoM3 queda excluido por el sello W v003 del plan anterior y no se volvio a sondear.

## Peticiones atendidas (Q-unidades/peticiones-web.json)

| id | caso | URL navegable | resultado |
| --- | --- | --- | --- |
| Q-W-01 | Q-U01 | https://qudt.org/vocab/unit/TON_Metric | OK, IRI exacta http |
| Q-W-02 | Q-U02 | https://qudt.org/vocab/unit/KiloGM | OK, IRI exacta http |
| Q-W-03 | Q-U03 | https://qudt.org/vocab/unit/MegaW | OK, IRI exacta http |
| Q-W-04 | Q-U04 | https://qudt.org/vocab/unit/GigaW-HR | OK, IRI exacta http |
| Q-W-05 | Q-U05 | https://qudt.org/vocab/unit/PERCENT | OK, IRI exacta http |
| Q-W-06 | Q-U06 | https://qudt.org/vocab/unit/DEG_C | OK, IRI exacta http |

Ninguna URL candidata devolvio 404. Por eso no se uso el indice para proponer terminos
alternativos y no se creo ningun alias por parecido.

## Capas normativas observadas en las seis paginas

- Sujeto RDF: `http://qudt.org/vocab/unit/<TERMINO>` (http, no https). La URL navegable
  https no impone la IRI del sujeto.
- Version: `rdfs:isDefinedBy http://qudt.org/3.5.3/vocab/unit` en las seis paginas.
- Generacion del vocabulario: `Generated 2026-10-20T17:45:20.378+00:00`.
- Simbolo: predicado `qudt:symbol`.
- Etiqueta: `rdfs:label` (idiomas disponibles por termino; no todos tienen @es).
- Definicion: `dcterms:description` (y `qudt:plainTextDescription` cuando existe).

## Diferencias entre el literal local y el termino normativo (no se normalizan aqui)

- `Toneladas` -> TON_Metric: etiqueta QUDT solo `"Metric Ton"@en`; sin @es en la pagina.
  La eleccion de variante (metrica/corta/larga) corresponde a la evidencia local de Q.
- `Kilogramos` -> KiloGM: `"Kilogramo"@es`, simbolo `kg`.
- `MW` -> MegaW: `"Megavatio"@es`, simbolo `MW`.
- `GWh` -> GigaW-HR: simbolo QUDT `GW·h` (no `GWh`); `ucumCode "GW.h"`,
  `uneceCommonCode "GWH"`; etiqueta solo `"Gigawatt Hour"@en`, sin @es.
  La diferencia de simbolo se conserva; no se declara alias.
- `Porcentaje` -> PERCENT: etiqueta solo `"Percent"@en`, simbolo `%`.
- `Grados celcius` (sic) -> DEG_C: `"Grado Celsius"@es`, simbolo `°C`.

Estas observaciones son normativas. No promueven ningun caso local ni autorizan factores
de conversion: la asignacion literal->termino y cualquier calculo siguen siendo de Q con
evidencia local.
