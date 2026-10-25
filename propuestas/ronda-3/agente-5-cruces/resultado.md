# Ronda 3 — Agente 5 (cruces): matriz TRIAJE + 3 fichas

Solo lectura fuera de `propuestas/ronda-3/agente-5-cruces/`; sin consolidar/ampliar/sincronizar,
sin descargas nuevas, sin contactos, sin cambios al grafo. Originales de proyecciones leídos
in situ desde copias fijadas (`data/integracion/fuentes/<sha>.xlsx`, SHAs verificados).

## Base verificada

103 conceptos, 232 respaldadas, 836 revisadas, 118 candidatas, 3/6 ambiguas/os,
23 significados, 16 vigencia no_acreditada, 32 dictámenes, 14 preguntas,
1850 IML vs 7300 ITER. Manifiestos r1/r2 con SHA coincidente.
Verificador: `scripts/verificar_base.py` → BASE OK (huellas en `fuente/huellas.json`).

## Matriz TRIAJE (no exhaustividad demostrada)

3916 pares. Decisiones por operación, no prohibiciones universales
(`scripts/construir_matriz.py` → `matriz-cruces.json`):

| Decisión | Pares | Alcance |
| --- | ---: | --- |
| pendiente | 3868 | sin evaluar (sentidos distintos, sin clave, dimensiones amplias) |
| exploratorio | 40 | clave compartida, falta estrategia de agregación |
| habilitable_con_condiciones | 2 | UES programa/sede, archivos completos; solo conteos |
| exploratorio_con_condiciones_pendientes | 2 | F1 (agregados RC, sin filas crudas ni catálogo), F2 (cruce 2020 nuevo, vigencia/serie pendientes) |
| no_validado | 2 | Matrimonios/Divorcios–Nacimientos: el lote no superó comprobaciones por error/fuente faltante; incompatibilidad no demostrada |
| no_comparable | 2 | Incidencia y Víctimas actual–anterior: no concatenar como misma serie (metodologías distintas); otras yuxtaposiciones no evaluadas |

Los 2 no_comparable son solo misma-familia actual–anterior (Incidencia, Víctimas),
acotados a no concatenar como misma serie. Defunciones vs Registro Civil: pendiente
con sentidos documentados (año_defunción ≠ año_registro); yuxtaposición por
variables comparables no evaluada, sin afirmar imposibilidad.

## Fichas

- **F1** Matrimonios–Divorcios 2022 → exploratorio_con_condiciones_pendientes
  (recomputo desde agregados por fuente: 67 códigos, 62 ambas, 13881/6064; unicidad,
  dominio, año obligatorio; 7 verificadas + 5 bloqueos, entre ellos SIN catálogo:
  ≤72 no identifica municipios ni equivale a INEGI; año de divorcios sin diccionario).
- **F2** Proyecciones Grandes grupos–Indicadores → exploratorio_con_condiciones_pendientes
  (VALIDACIÓN NUEVA sobre originales: headers reales, 7344 + 3672 filas, cobertura
  1990–2040 OBSERVADA en ambos; cruce NUEVO solo 2020 por (CLAVE,AÑO): 72/72 claves,
  nombres 72/72, POB coherente 72/72, detalle en `fichas/claves-2020.json`; bloquean
  vigencia no_acreditada y cruce año por año pendiente).
- **F3** UES Titulados–Egresados 2020-2021 (175/54, 1404/1947) + Nuevo–Reingreso 2021-2022
  (165/59, 3385/12271) → habilitable_con_condiciones (archivos completos con sha;
  límites: identidad por nombre con acentos, periodo de metadatos, fuente agregada,
  sin tasas ni cohortes).

SPARQL (rdflib, sin BD nueva): `queries/q1-q3` + `scripts/consultas_sparql.py` →
reproduce 3916 / 1191 / 2328 / 396 / 1 y familias entidad+municipio de Proyecciones.

## Límites (se mantienen)

Vigencia no_acreditada ≠ inválido; fecha CKAN ≠ edición. IML 1850 vs ITER 7300 es
cobertura observada (5295 con 1–9 hab), no equivalencia global; ITER 2020-03-15 vs
IML año 2020. Alias Magdalena acotado. 26998/26999 no municipales. Localidades no
asignadas a otros conjuntos. Textos originales y ceros preservados.

## Reproducir

```powershell
uv run python propuestas/ronda-3/agente-5-cruces/scripts/verificar_todo.py
```

→ TODO OK. Propuestas máquina: `propuestas.json`. No se propone sameAs/exactMatch
ni activar cruces.
