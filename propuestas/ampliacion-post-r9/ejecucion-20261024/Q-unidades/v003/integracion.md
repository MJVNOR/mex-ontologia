# Q-unidades v003 â€” integracion (carril I)

## Payload

`propuesta-q-unidades.ttl`: 5 `mex:UnidadDeclarada` con `mex:unidadQudt` y `mex:evidenciaNormativa`. Es el TTL integrable; no requiere cambios de vocabulario ni de shapes (todos los predicados ya existen en `data/portal/ampliacion.ttl`).

| caso | variable | literal | sujeto QUDT |
| --- | --- | --- | --- |
| Q-U02 | `pesoprom` | `Kilogramos` | `http://qudt.org/vocab/unit/KiloGM` |
| Q-U03 | `Unidad de Medida` | `MW` | `http://qudt.org/vocab/unit/MegaW` |
| Q-U04 | `Unidad de Medida` | `GWh` | `http://qudt.org/vocab/unit/GigaW-HR` |
| Q-U05 | `ANALF` | `Porcentaje` | `http://qudt.org/vocab/unit/PERCENT` |
| Q-U06 | `temperatura` | `Grados celcius` | `http://qudt.org/vocab/unit/DEG_C` |

## Pasos

1. Dos auditorias independientes sobre los bytes de v003 y del sello W v002 (`validacion-w.json` ya replica sus 12 hashes).
2. Integrar el TTL tal cual en el grafo del portal; una sola sincronizacion.
3. Ejecutar `consultas/q1..q3` y el SHACL del portal; comprobar que no se altera nada ajeno.
4. Respaldar Studio antes de sincronizar, como en R9.

## Prohibiciones

- No agregar Q-U01 (`Toneladas`) ni hm3: no estan en el TTL y no deben aparecer por convencion.
- No completar unidades de filas vecinas: cada declaracion alcanza solo su definicion. En U03/U04, solo la fila `Unidad de Medida`; no se transfiere a `Capacidad Autorizada` ni a `Generacion Estimada`.
- Sin `QuantityValue`, sin factores, sin conversiones, sin alias (`GWh` != simbolo QUDT `GW·h`; la diferencia se conserva).
