# W-estandares v002 - respuestas QUDT 3.5.3

Fecha UTC: 2026-10-24T20:20:38.953908+00:00. Estado: propuesta para auditar.
Obscura via MCP nativo OpenCode; sin puentes CLI. Seis peticiones Q atendidas.

## Respuestas

| id | caso | literal local | sujeto RDF (http) | version | simbolo | etiqueta |
| --- | --- | --- | --- | --- | --- | --- |
| Q-W-01 | Q-U01 | Toneladas | http://qudt.org/vocab/unit/TON_Metric | 3.5.3 | t | Metric Ton (sin @es) |
| Q-W-02 | Q-U02 | Kilogramos | http://qudt.org/vocab/unit/KiloGM | 3.5.3 | kg | Kilogramo |
| Q-W-03 | Q-U03 | MW | http://qudt.org/vocab/unit/MegaW | 3.5.3 | MW | Megavatio |
| Q-W-04 | Q-U04 | GWh | http://qudt.org/vocab/unit/GigaW-HR | 3.5.3 | GW·h | Gigawatt Hour (sin @es) |
| Q-W-05 | Q-U05 | Porcentaje | http://qudt.org/vocab/unit/PERCENT | 3.5.3 | % | Percent (sin @es) |
| Q-W-06 | Q-U06 | Grados celcius | http://qudt.org/vocab/unit/DEG_C | 3.5.3 | °C | Grado Celsius |

Cada sujeto se capturo en su pagina oficial, con `rdfs:isDefinedBy`
`http://qudt.org/3.5.3/vocab/unit` y `Generated 2026-10-20T17:45:20.378+00:00`.

## Limites que no se normalizan

- TON_Metric, GigaW-HR y PERCENT no tienen etiqueta `@es` en QUDT; se conserva la etiqueta `@en`.
- GigaW-HR declara simbolo `GW·h`, no `GWh`; `ucumCode` es `GW.h` y `uneceCommonCode` `GWH`.
- El literal local `Grados celcius` (sic) no se corrige en esta capa.
- `Toneladas` no elige por si mismo entre variantes; la decision requiere evidencia local de Q.

Ningun alias, factor de conversion ni caso local se promueve desde estas fuentes.
Sellos SHA-256 en `congelada.json`, calculados por `scripts/generar_y_sellar.py`.
