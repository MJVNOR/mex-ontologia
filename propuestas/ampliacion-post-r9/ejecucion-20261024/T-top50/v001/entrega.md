# T-top50 — reconciliacion del ranking C2 v001 contra mapa y cobertura R9

Fecha UTC: ver `entrega.json`. Estado: `reconciliacion_verificada_sin_join`.

## 1. Que se hizo

Reconciliacion reproducible del ranking C2 v001 (`prioridades_top50.csv`,
`matriz_pares_relevantes.csv`) contra `data/portal/oportunidades-cruce.json`
(3916 pares), el criterio de pesos/penalizaciones y la cobertura R9.
Mapa original no modificado; solo lectura. Ningun join ni rate se deriva del ranking.

## 2. Verificacion por codigo

`scripts/reproducir_top50_r9.py` (solo stdlib) recomputa
`score = suma(pesos_familia) + suma(penalizaciones)` sobre las 1191 candidatas:

- 3916 pares; 2328 sin clave, 1191 candidatas, 396 solo-dimensiones, 1 exploratorio.
- 1191/1191 scores de matriz iguales al CSV; 1191 ids unicos.
- 50/50 ids, scores y rangos del top50 iguales al CSV (orden score desc, id asc).
- Top1 ITAMA Internamiento<>Externamiento: pesos 13.0 + penalizaciones −8.0 = 5.0.
- Pares A1–A3 del plan por ID exacto: A1 911 rango 2
  (`19e5036d-...--923b485b-...`), A2 matrimonios/nacimientos rango 4
  (`1cf9c8e2-...--df2d60f5-...`), A3 ITAMA rango 1 (`27a5c80c-...--4d27a1c4-...`).
- Cobertura R9: `cobertura_operativa_validada_sin_cambios_al_grafo`
  (1423 significados, 1106 conceptos); toda fila sigue `candidata_por_validar`.

## 3. Salidas en staging (este v001)

- `top50-oportunidades-r9.json` — contenido previsto para `reports/`: meta con
  fuentes/hashes + 50 filas (rango, id, titulos, score, familias, bloqueadores,
  conjuntos fuente, estado `NO_JOIN_APROBADO`, carril A1–A3 cuando aplica).
- `top50-oportunidades-r9.md` — tabla legible de las 50 filas.
- `vista-top50-r9.html` — vista simple accesible (una tabla, sin framework).
- `tests/test_top50_r9.py` — 5 pruebas: 3916/1191, matriz 1191 unicos+scores,
  top50 orden+scores, A1–A3 por ID, salidas y congelada.
- `congelada.json` — SHA256 por codigo de todos los archivos (no se incluye).

## 4. Publicacion pendiente (coordinador / carril I)

Copiar `top50-oportunidades-r9.json/.md` a `reports/` y la vista a staging
con el unico escritor central. Esta entrega no escribe fuera de su v001.

## 5. Limites

Base IRI/example.org fuera de alcance. Sin Gemma, sin contactos, sin busquedas
agotadas. Manifiestos R1–R9 intactos. Oportunidad != join aprobado.
