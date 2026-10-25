# Q-unidades v003 â€” 5 declaraciones integrables con vinculo QUDT

Valida el sello W v002 (12 archivos, 6 sujetos http, QUDT 3.5.3) y aplica vinculo solo donde las fuentes lo avalan.

| caso | variable | literal | sujeto QUDT | evidencia |
| --- | --- | --- | --- | --- |
| Q-U02 | `pesoprom` | `Kilogramos` | `http://qudt.org/vocab/unit/KiloGM` | `Q-W-02` |
| Q-U03 | `Unidad de Medida` | `MW` | `http://qudt.org/vocab/unit/MegaW` | `Q-W-03` |
| Q-U04 | `Unidad de Medida` | `GWh` | `http://qudt.org/vocab/unit/GigaW-HR` | `Q-W-04` |
| Q-U05 | `ANALF` | `Porcentaje` | `http://qudt.org/vocab/unit/PERCENT` | `Q-W-05` |
| Q-U06 | `temperatura` | `Grados celcius` | `http://qudt.org/vocab/unit/DEG_C` | `Q-W-06` |

**Excluidas:** Q-U01 `Toneladas` (W acredita TON_Metric pero el literal local no elige variante: requiere evidencia local) y hm3/Hectometros cubicos (busqueda agotada; sin M3 ni factor).

Integracion: `integracion.md`. Copias y hashes: `fuentes/indice-copias.json` y `validacion-w.json`.
