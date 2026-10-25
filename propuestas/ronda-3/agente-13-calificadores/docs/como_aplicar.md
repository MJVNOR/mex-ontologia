# Cómo aplicar el patch (solo el integrador, tras revisar)

Alcance: `shapes/semantica.ttl`, `tests/test_semantica.py`.
No toca reglas, conteos, `expectedrounds`, ni la integración 3.

## Estado del patch de script

`patch/consolidar_semantica.patch` está **vacío a propósito**: el central
`scripts/consolidar_semantica.py` ya integra el diseño aprobado
(`validar_calificador` con rechazo por `strip` y devolución verbatim,
materialización de `CalificadorDocumental`, `fuente_revision`, `limites`).
El staging es copia byte a byte del central; el verificador lo comprueba
(`construir_real_sin_calificador_identico`: grafos isomorfos, modelo igual).
No hay nada que aplicar en el script.

## Aplicación

Desde la raíz del proyecto, con el árbol limpio:

```powershell
git apply --check propuestas/ronda-3/agente-13-calificadores/patch/semantica_ttl.patch
git apply --check propuestas/ronda-3/agente-13-calificadores/patch/test_semantica.patch
git apply propuestas/ronda-3/agente-13-calificadores/patch/semantica_ttl.patch
git apply propuestas/ronda-3/agente-13-calificadores/patch/test_semantica.patch
```

Contenido residual:
- Shape: `sh:pattern "\\S"` en `dimensionCalificador`/`valorCalificador`
  (rechaza vacío y solo-blancos, espejo del validador) y `sh:nodeKind sh:IRI`
  en el enlace `tieneCalificadorDocumentado` (nodos estables).
- Tests: 4 tests nuevos (`CalificadorTest`) con 2 negativos solo-blancos y
  positivo `' San Luis R.C. '` verbatim.

No se necesita patch del loader: `scripts/ampliar_portal.py` ya carga
`shapes/semantica.ttl`. Verificado por el chequeo `loader_sin_cambio_necesario`.

## Verificación tras aplicar

```powershell
uv run python -m unittest tests.test_semantica
uv run python propuestas/ronda-3/agente-13-calificadores/scripts/verificar.py
```

El primer comando corre los tests centrales (20 vigentes + 4 propuestos).
El segundo corre las 11 verificaciones significativas contra el staging y el
núcleo real en memoria (nunca `generar()`, nunca escribe fuera de la carpeta 13).

## Equivalencia con el staging

`staging/` es el resultado esperado tras `git apply`. Los SHA esperados están
en `fuente/huellas.json` (sección `propios`, claves `staging/...`).
