# A2 — Resultados (v002)

Veredicto: **BLOQUEADO** — no hay comparación de volúmenes ni join al grafo.
Idéntico a v001 en veredicto, causas y 8 ejes; v002 solo precisa el inventario
(H-02) y ancla las fuentes completas (H-04).

Causas (bloquean cualquier comparación/join):

1. Grano distinto: evento matrimonial vs agregado mensual de nacimientos.
2. Unicidad y cardinalidad no acreditadas: muestras n=100, alcance muestral explícito.
3. Inconsistencia interna en Nacimientos: `total ≠ hombres+mujeres` (2015, 2020–2023); meses faltantes (2016).
4. Ámbito solo de registro (sin residencia, sin catálogo de correspondencia acreditado).
5. Poblaciones distintas; prohibidas causalidad y tasas poblacionales.

Inventario (H-02): Matrimonios **10 recursos de datos + 1 diccionario = 11**
(2015–2024); Nacimientos **15 recursos de datos + 1 diccionario = 16** (2010–2024).

## Fuentes ancladas (H-04)

SHA256 de archivo completo, calculado por código en `scripts/analizar.py`:

| Fuente | Bytes | SHA256 |
|--------|-------|--------|
| `reports/catalogo-perfil.json` | 227576 | `aae23b2eb8f8e37cbee18d86c0cac7c73f0899f02fbd417bc90d01a8fd54fc43` |
| `data/portal/contenido-inspeccion.json` | 2652648 | `61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb` |
| `data/portal/oportunidades-cruce.json` | 9645149 | `40f107d5cf9c11ce937073ac2f7b5b0e3c9db8c342f7414cecb0f0744e0d0c14` |
| `data/portal/lote-cruces/validacion-lote.json` | 1478239 | `9031b875b1bf7873722f74847abbbce9b87201415f43788f60be1a75b50ede19` |

Detalle máquina: `resultados.json`. Sello: `sello.json` (+ sidecar `sello.sha256`),
generado por `scripts/sellar.py` sin autohash ni cachés.
