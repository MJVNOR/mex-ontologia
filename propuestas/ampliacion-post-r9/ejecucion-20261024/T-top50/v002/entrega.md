# T-top50 v002 — publicación reproducible y huella del plan actualizada

Fecha UTC: 2026-10-24. Estado: `reconciliacion_verificada_sin_join`.
Modelo: `opencode/deepseek-v4.1-flash-free`. Continúa el carril tras el cambio de
modelo; no reanuda ninguna sesión anterior.

## 0. Motivo de la versión (H-01)

R-documental v001 verificó T-top50 v001 y detectó **H-01**: la huella declarada
de `docs/plan-paralelo-ampliacion-post-r9.md` no coincidía con el archivo
actual. No es error de autoría: el plan se editó **después** del sellado de v001
(mtime del plan 2026-10-24T20:15:39Z, sello de T 2026-10-24T20:09:42Z), al
registrarse el cambio de modelo. v001 queda intacta y sellada.

Esta v002 re-declara la huella vigente y deja constancia del cambio:

| Dato | Valor |
| --- | --- |
| Huella declarada en v001 | `807a05e4473597ced2e1d708fb2069884d9a669cc0ec823d6a1aca316a680e9c` |
| Huella actual del plan | `f43214a0d38ff2cb1fcdfb213d9aa0fba67415dc21b2033ac305a3a70eda0ce8` |
| Bytes actuales | 5672 |
| Causa | edición posterior al sellado (cambio Muse → DeepSeek Free), no error del carril |

Ninguna cifra depende de ese archivo: 3916/1191/50 se recomputan desde el mapa,
el criterio y los CSV.

## 1. Script publicable

`scripts/publicar_top50_r9.py` (solo stdlib) sustituye al reproductor interno:

- API `generar(root, outdir)` y CLI con `--root` y `--out-dir`.
- Instalado en `scripts/`: sin `--out-dir` escribe en `reports/`.
- Carpeta de versión: **exige** `--out-dir`; esta entrega invoca siempre
  `--out-dir propuestas/.../T-top50/v002` (nunca usa el valor por defecto).
- Guardas de destino: rechaza escribir dentro de las fuentes (mapa, criterio,
  CSV top50/matriz, cobertura, seguimiento, plan) y dentro de cualquier carpeta
  sellada (detectada por `congelada.json`). Nunca escribe en v001.
- Salidas: `top50-oportunidades-r9.json`, `.md` y `.html` (nombre de destino
  publicable del HTML; ya no `vista-top50-r9.html`).

## 2. Verificación por código

- 3916 pares: 2328 sin clave, 1191 candidatas, 396 solo dimensiones, 1 exploratorio.
- 1191/1191 scores recomputados iguales a `matriz_pares_relevantes.csv`; ids únicos.
- 50/50 ids, rangos, scores y orden (score desc, id asc) iguales al CSV.
- Top1 ITAMA Internamiento<>Externamiento: 13.0 − 8.0 = 5.0.
- Carriles por ID exacto: A1-911 rango **2** (3.0), A2 rango **4** (3.0),
  A3-itama rango **1** (5.0).
- Las 50 filas en `NO_JOIN_APROBADO`; bloqueadores completos por fila.
- Cobertura R9: `cobertura_operativa_validada_sin_cambios_al_grafo`
  (1423 significados, 1106 conceptos).
- 7 fuentes con SHA256 completo vigente en `meta.fuentes` (incluido el plan).
- 10 pruebas: instalación/destino temporal, no escritura en fuentes ni v001,
  50 filas idénticas, carriles, contenido publicado y sello.

## 3. Salidas

- `top50-oportunidades-r9.json` — meta (fuentes, fórmula, cobertura, carriles) +
  50 filas con títulos, score, familias, bloqueadores, conjuntos fuente, estado
  y carril.
- `top50-oportunidades-r9.md` — tabla legible de las 50 filas.
- `top50-oportunidades-r9.html` — vista legible autocontenida (una tabla, CSS
  mínimo, sin scripts).
- `scripts/publicar_top50_r9.py`, `scripts/sellar_v002.py`,
  `tests/test_publicar_top50_r9.py`, `resultados/publicacion.out`,
  `resultados/pruebas.out`.
- `congelada.json` — sello calculado por código sobre los bytes de esta carpeta
  (excluye el propio sello, `__pycache__` y `*.pyc`); `sello_sha256` sobre JSON
  canónico. Sin autohash ni hashes transcritos.

## 4. Publicación

Los tres artefactos son el contenido publicable para `reports/`. La publicación
la realiza el único integrador central (instalando el script y ejecutándolo sin
`--out-dir`, o copiando los tres archivos). Esta entrega no escribe en `reports/`
ni instala nada.

## 5. Límites

Base IRI/`example.org` fuera de alcance; sin cambios en `config.toml`, Gemma,
manifiestos R1–R9 ni escritores centrales. Sin joins, sin rates, sin promoción
de candidatas. `v001` no se modifica. Las rutas de fuentes C2 conservan la
versión de su origen (`C2-oportunidades/v001/...`) por trazabilidad; son rutas
de lectura, no destinos de escritura. Oportunidad ≠ join aprobado.

## 6. Auditoría

Pendiente: R-documental y B-técnica revisarán estos bytes. Esta entrega no emite
dictamen ni anticipa veredicto.
