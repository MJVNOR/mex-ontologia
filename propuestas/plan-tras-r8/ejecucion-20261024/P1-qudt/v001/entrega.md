# P1-QUDT v001 — propuesta_para_auditar (NO integrada)

Inventario de unidades explícitas + propuesta mínima QUDT cualificada (3 casos).

## Casos propuestos (declaración de unidad por variable/recurso)

| Caso | Variable | Unidad literal (fuente) | Diccionario | QUDT |
| --- | --- | --- | --- | --- |
| P1-Q1 | Precipitacion_mm | Milimetros | 6713de4e | unit:MilliM SIN VERIFICAR (P1-W-01) |
| P1-Q2 | Almacenamiento(hm3) | Hectometros cubicos | ca5574f0 | unit:HectoM3 SIN VERIFICAR (P1-W-02) |
| P1-Q3 | SUPSEM | Hectareas | 94215f51 | unit:HectoHA SIN VERIFICAR (P1-W-03) |

## Lo que NO se hace

Valores observados, conversiones, `qudt:QuantityValue`, dominio QuantityValue
sobre VariableDocumentada, Altitud-Grados (literal inverosímil, excluida),
temperatura/TALLA/PESO sin unidad declarada, claves/códigos como unidades,
familia de marginación nacional como codificación adoptada.

## Verificación

- `propuesta-qudt.ttl` parsea (rdflib del proyecto); Q1/Q2 → 3 filas.
- `peticiones-web.json` pide a W los 3 URIs exactos + documento normativo.
- `congelada.json`: SHA256 por código. Autohash de congelada.json =
  sha256 del JSON canónico (sort_keys) sin su propia entrada; reproducir con
  `build_v001.py` / script de verificación del auditor.
- Condición de integración: verificación W + réplica de hashes. Sin eso, no integrar.
