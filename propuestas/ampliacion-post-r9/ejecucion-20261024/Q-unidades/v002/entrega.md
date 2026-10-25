# Q-unidades v002 — 6 declaraciones cualificadas (no instalables)

Continua `v001` (sellada por su carril) sin modificarla: corrige el tratamiento de `Toneladas` y anade copias fuente y formato de integracion. Base R9.

| caso | variable | literal | diccionario | estado |
| --- | --- | --- | --- | --- |
| Q-U01 | `PRODTON` | `Toneladas` | `94215f51` | `pendiente_ambiguedad_tonelada` |
| Q-U02 | `pesoprom` | `Kilogramos` | `a4eb0b8b` | `pendiente_verificacion_W` |
| Q-U03 | `Unidad de Medida` | `MW` | `a6cdb7ad` | `pendiente_verificacion_W` |
| Q-U04 | `Unidad de Medida` | `GWh` | `a6cdb7ad` | `pendiente_verificacion_W` |
| Q-U05 | `ANALF` | `Porcentaje` | `251309e5` | `pendiente_verificacion_W` |
| Q-U06 | `temperatura` | `Grados celcius` | `33d0a99e` | `pendiente_verificacion_W` |

Inventario: 61 literales / 259 filas en 486 diccionarios.

Sin `mex:unidadQudt` (W no sello Q-W-01..06), sin QuantityValue, sin factores. Q-U01 (`Toneladas`) pendiente por ambiguedad local: la norma no decide la unidad local.

Integracion: `formato-integracion.md`. Exclusiones: `informe-exclusiones.md`. Copias fuente: `fuentes/<caso>/`.
