# Agente 13 — Calificadores (ronda 3): patch central revisable, sin aplicar

## Ajuste final (rebase)

El central `scripts/consolidar_semantica.py` integró el diseño aprobado entre la
entrega y este ajuste (`validar_calificador` con rechazo por `strip` y devolución
verbatim, nodos `CalificadorDocumental`, `fuente_revision`, `limites`). El staging
de script es ahora copia byte a byte del central y su patch queda vacío a propósito.
Residual real: shape (`sh:pattern "\\S"` + `sh:nodeKind sh:IRI` en el enlace) y
4 tests centrales (2 negativos solo-blancos, positivo `' San Luis R.C. '` verbatim).
Sin cambios a contadores ni semántica de dominios. Comentario «ponytail» eliminado
(el staging es el central, con su explicación simple).

## Base verificada (solo lectura, sin generar fuera de la carpeta)

- Núcleo vigente: 103 conceptos, 232 variables respaldadas, 23 candidatas, 1308 fuera del núcleo.
- Correspondencias: 836 revisadas, 118 candidatas, 6 vínculos ambiguos.
- Central con 0 reglas con calificador y 20 con `fuente_revision`; `construir()` real
  en memoria: staging isomorfo e igual al original (modelo idéntico).
- No se ejecutó `generar()`. Sin descargas externas, sin secretos.

## Fixtures: snapshot propio vs propuestas upstream (no confundir)

- Snapshot propio `fixture/reglas_calificadas.json`: SHA
  `7dcaa3d4bdcd0f5730c712954d782eb2db70c4ba32e128c5ee1e00011535960e` (30 reglas verbatim).
- Upstream agente 3: `92a7dcdd...` (cambió 2 reglas NDDR **no calificadas**; antes `29f1dadf...`).
- Upstream agente 8: `9672a4ba...` (sin cambios; Nacionalidad no calificada).
- Las 30 con calificador siguen verbatim: 0 faltan, 0 difieren. Detalle en `fuente/huellas.json`.

## Verificaciones (reales, con negativos)

`uv run python propuestas/ronda-3/agente-13-calificadores/scripts/verificar.py` → **11/11**.
Detalle en `fuente/verificacion-13.json`:

1. Staging importa del ROOT central original; `generar()` jamás se llama.
2. 8 reglas vigentes sin calificador: salida idéntica original vs staging.
3. `construir()` real: grafos isomorfos, records, resumen y modelo iguales; contadores intactos.
4. 30/30 records y nodos con sus valores (DDR 139–193; 20 sedes en 5 valores distintos).
5. Mismo concepto (`estudiantes-nuevo-ingreso-sede`), sedes San Luis R.C. vs Hermosillo: no mezcladas.
6. Copia sin mutar: mutar el retorno no toca la regla.
7. 16 calificadores inválidos rechazados (incluye `'   '` en key y en value) + verbatim
   `' San Luis R.C. '` con espacios laterales intactos.
8. IRIs estables entre construcciones y reconstruibles por diccionario/fila/key.
9. Candidatas/fuera no autopromueven ni inventan calificador.
10. Shape estructural: `minLength 1`, `pattern \S`, provenance doble, enlace con `nodeKind IRI`.
11. Loader sin cambio necesario.

Propuestos centrales: `scripts/correr_tests_staging.py` → **24/24 OK**
(20 vigentes + 4 nuevos, en estructura temporal dentro de la carpeta).
Centrales intactos: `tests.test_semantica` → 20/20 OK (sin modificar el núcleo).

## Archivos

- `patch/consolidar_semantica.patch` (vacío documentado), `patch/semantica_ttl.patch`,
  `patch/test_semantica.patch`
- `staging/` (resultado esperado), `shape/calificador.ttl` (fragmento),
  `fixture/reglas_calificadas.json`, `scripts/verificar.py`, `scripts/correr_tests_staging.py`,
  `scripts/gen_huellas.py`, `fuente/huellas.json`, `fuente/verificacion-13.json`,
  `docs/como_aplicar.md`, `docs/revertir.md`, `propuestas.json`
- Aplicar: `docs/como_aplicar.md`. Revertir: `docs/revertir.md`.

## Pendientes (fuera de mi alcance)

- El integrador aplica al terminar auditorías; no intervengo la integración 3 ni los conteos.
- Conceptos nuevos de agentes 3/8 y sus correspondencias columna-variable: no incluidos.
- SHACL extremo a extremo tras aplicar: lo corre el integrador con `ampliar_portal.py --load`.
