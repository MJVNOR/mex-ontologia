# Gate core desc/IRI + segundo defecto M2 v002 — B-tecnica

Dictamen: **rechazado / observado, sin aceptar antes del payload v3**.
Material v001 (555c) **no aplicar** (dos defectos). Detalle máquina en
`gate-core-desc-iri.json` (SHAs por código). Historial anterior intacto;
staging no editado.

## Segundo defecto M2 v002 (14/14)

- `descripcion` del vínculo **no es el literal local** (`Pendiente de
  especificar`, M1 14/14 exacto) sino el **descriptor nacional**
  (p. ej. `Se le aplicó la vitamina A`). Verificado 14/14.
- 74/76 afirman `0000` = CIE-10 `NINGUNA APARENTE` con catálogo
  DIAGNOSTICOS: **vetado R7**. R7 solo acredita alcance físico
  columna↔fila; no valida valores ni confirma pertenencia a catálogos
  (criterio M1). M2 prepara v003; material v003 se hará luego.

## Gate core: tipos exactos, sin normalización-alias

- `integrar_ronda_7.py` (180-183): `descripcion` solo truthy, no igualdad
  exacta → el descriptor nacional pasa.
- `consolidar_semantica.interpretacion` compara con `clave()` =
  lower + NFD-sin-Mn + strip/colapsa → alias oculta errores de literal.
- `I-codigo/v002/scripts` son copias exactas (mismo SHA), heredan el hueco;
  no hay `integrar_ronda_8`. `T-v002` tampoco chequea descripción ni
  namespace IRI.
- Exigencia: comparación **byte-exacta** (`==`, sin lower/strip/NFD) para
  descripción, campo, `definicion_iri`, concepto y huellas; IRI con regex
  `^.../definition/...%2F\d+$`; rechazar `/documented-variable/` sin alias.

## Solicitud a I-codigo (vía coordinador): closed guard R8

`0 reglas, 0 conceptos, 28 vínculos backed R7`: 28 columnas = 14 M1 + 14 M2;
por vínculo campo exacto al ordinal, `definicion_iri` exacto con variable R7
respaldada + mismo concepto + misma huella, `descripcion` == literal local
exacto, huellas recomputadas, recurso/diccionario exactos, criterio solo
físico (sin valores/CIE/catálogos/vigencias/joins/identidad). Sin
normalización en la comparación.
