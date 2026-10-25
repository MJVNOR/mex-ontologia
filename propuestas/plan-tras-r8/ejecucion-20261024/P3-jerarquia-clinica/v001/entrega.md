# P3 — Jerarquía clínica (v001): propuesta negativa

**Estado:** `sin_evidencia_para_integrar` · 2026-10-24 · 101/101 casos cubiertos.

## Inventario broader

| Fuente | broader |
| --- | ---: |
| `ontologia/semantica.json` (todo el archivo) | 0 |
| `ontologia/revision-ronda-8.json` | 0 |
| `data/portal/portal-completo.ttl` (conceptos `caso-con-*`) | 0 |

Tercer elemento de cada concepto en `semantica.json`: `None` en los 101.

## Contexto fuente (igual para los 101)

Conjunto Fiebre manchada (Rickettsia) `5494daa1…`, diccionario `33d0a99e…`
(`data/portal/inspecciones/33d0a99e….json`, 178 definiciones, plano: sin
columna de agrupación; `Unidad de medida` vacía en las 101 variables).
Cada variable 1=Sí/2=No conserva población, manifestación y codificación.

## Decisión

Sin justificación jerárquica en fuentes primarias → **no integrar**.
Matriz de 101 con evidencia y brechas en `v001/entrega.json`; `agrupaciones_propuestas: []`.
Preserva cada manifestación y calificadores. Propuesta negativa válida
(plan tras R8, fase 3, fila P3).

## Consultas

- `consultas/grupo-caso-con.rq` — 101 filas, `?broader` sin vincular.
- `consultas/detalle-caso-con.rq` — detalle por concepto + variables.
- `consultas/fixtures/resultado-grupo-esperado.json` — resultado esperado.

Web: `peticiones-web.json` con 0 peticiones (sin pista primaria nueva).
Hashes: `congelada.json` (SHA-256 por código).
