# Auditoría código R8 v003 — B-tecnica (aceptar)

- Auditado (solo lectura): `I-codigo/v003` con `congelada.json` (apareció
  durante la espera; v002 congelada no se aplica).
- Dictamen: **aceptar**. 28/28 verificaciones por código en
  `auditoria-codigo-v003.json` (SHAs calculados, no copiados). Sin instalar.
  Sin Gemma.

## Correcciones exigidas, verificadas

- (a) `if not UNIVERSO_28 <= candset` (sin `<` estricto) + test
  `test_invalid_falta_candidata`.
- (b) IRI tipo `definition` exacta (`PREFIX_DEFINICION` + respaldo R7 por
  clave exacta, sin alias), mapping col→`variable`==`iri` local, campo y
  descripción == local original exactas, huella de fila, scope SINAC
  pinnado, payload 0/28/0. Negativas: campo, descripción, variable-mapping,
  definición sin respaldo.
- (c) Ambas auditorías: dictamen global `aceptar` + `aceptadas_sha256`
  pinnado + 28 ids aprobados (negativas: global, falta de aprobación, SHA
  tras pin).
- (d) Sin config R8: no-op (imports y bloques tras `exists()`); con config:
  proyección 28 revisadas→candidatas con igualdad fuera del delta y sin
  weakening de invariantes (pins 4478/45/1423/16/124/1106/4523); R7 delega a
  R8 **antes** de la igualdad final manteniendo sus checks (`cargar()` corre
  primero); R1/R2 con import condicional.
- (e) Fixtures fake solo en `tmp` de staging; `sys.path` con staging primero;
  ninguna escritura fuera de `tmp`.

## Ejecución

- `test_cargar_r8.py` 9/9 OK, `test_proyeccion_r8.py` 4/4 OK (staging).
- Suite R7 producción 154 OK tras T2 (145 directos + 9 con `PYTHONPATH=scripts`:
  dictamen 3, selección 4, guardar 2).
- Sello: 19/19 SHAs de `congelada.json` verificados por código;
  aceptadas `db3167f9…` idéntica a material v003.

## Aplicables (al instalar)

6 scripts → `scripts/`: `consolidar_semantica.py`, `integrar_entregas.py`,
`integrar_ronda_2.py`, `integrar_ronda_7.py`, `integrar_ronda_8.py` (alta),
`r8_proyeccion.py` (alta); tests `test_cargar_r8.py`, `test_proyeccion_r8.py`
(staging, fixtures fake). Referencias y SHAs en el JSON.
