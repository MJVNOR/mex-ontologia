# A2 — Resultados (v001)

Veredicto: **BLOQUEADO** — no hay comparación de volúmenes ni join al grafo.

Causas (bloquean cualquier comparación/join):

1. Grano distinto: evento matrimonial vs agregado mensual de nacimientos.
2. Unicidad y cardinalidad no acreditadas: muestras n=100, alcance muestral explícito.
3. Inconsistencia interna en Nacimientos: `total ≠ hombres+mujeres` (2015, 2020–2023); meses faltantes (2016).
4. Ámbito solo de registro (sin residencia, sin catálogo de códigos municipales).
5. Poblaciones distintas; prohibidas causalidad y tasas poblacionales.

Detalle máquina: `resultados.json`. Hashes: `congelada.json` (+ sidecar `congelada.sha256`).
Fuentes: `reports/catalogo-perfil.json` (inventario: 10 recursos Matrimonios 2015–2024,
15 recursos Nacimientos 2010–2024), `data/portal/contenido-inspeccion.json`
(diccionarios), `data/portal/oportunidades-cruce.json` (par candidata),
`data/portal/lote-cruces/validacion-lote.json` (fallo_validacion_integral).
