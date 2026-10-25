# Q-unidades v002 — 6 casos (continuacion de v001)

| caso | variable | literal exacto | diccionario | huella (12) | estado |
| --- | --- | --- | --- | --- | --- |
| Q-U01 | `PRODTON` | `Toneladas` | `94215f51` | `4d79bbed1d9c` | `pendiente_ambiguedad_tonelada` |
| Q-U02 | `pesoprom` | `Kilogramos` | `a4eb0b8b` | `3ebcb68ece60` | `pendiente_verificacion_W` |
| Q-U03 | `Unidad de Medida` | `MW` | `a6cdb7ad` | `7d4b4ed61114` | `pendiente_verificacion_W` |
| Q-U04 | `Unidad de Medida` | `GWh` | `a6cdb7ad` | `d33c36c8f0d7` | `pendiente_verificacion_W` |
| Q-U05 | `ANALF` | `Porcentaje` | `251309e5` | `1931b14a42ac` | `pendiente_verificacion_W` |
| Q-U06 | `temperatura` | `Grados celcius` | `33d0a99e` | `ecf25e75c913` | `pendiente_verificacion_W` |

Cada caso tiene copia fuente byte a byte en `fuentes/<caso>/` (sha256 igual al origen) y su fila exacta en `fila.json`.

Q-U01 queda pendiente: el literal `Toneladas` no declara variante y el corpus lo repite en 3 definiciones de 2 diccionarios. La norma no decide la unidad local; no se asigna variante metrica.

Ninguna URI QUDT se afirma en v002: W no ha sellado Q-W-01..06.
