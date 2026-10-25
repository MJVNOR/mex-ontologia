# Análisis de cadena R4/R5/R6 + consolidar + studio (solo lectura, sin instalar)

Expediente: `propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z`
Fecha: 2026-10-24. Sin cambios al núcleo.

## Cadena de validación (estado instalado en `scripts/`)

- `integrar_ronda_4.py:validar(rules)`: base + adiciones R4; si existe
  `ontologia/revision-ronda-5.json` delega a R5 con la base esperada;
  si no, exige `rules == expected`. Doble chequeo: duplicados + cada
  adición con aprobación independiente (a=reglas, b=vínculos).
- `integrar_ronda_5.py:validar_sobre_base(rules, base_r4)`: exige
  `baseline == base_r4`; construye expected; valida duplicados (líneas 47-49)
  y aprobaciones (50-54); **después** delega a R6 si existe su config
  (55-60); solo si no existe R6 compara `rules != expected` (61).
  Orden correcto: invariantes propios + delegación antes de exactitud.
- `integrar_ronda_6.py` instalado (79 líneas): **sin delegación a R7** y con
  `if rules != expected` al final tras sus validaciones propias. El staging
  viejo (`propuestas/investigacion-post-r6/integracion-staging/codigo/`)
  ya trae la copia con delegación R6→R7, pero atada al caso CLASIF
  hardcoded (1 regla + 1 concepto + 0 vínculos, PIN CLASIF). No reutilizar.
- `consolidar_semantica.py:generar()` instalado (506 líneas): registra fases
  R2..R6 por existencia de `ontologia/revision-ronda-N.json`; **sin bloque R7**.
  El staging viejo añade el bloque R7 espejo del R6. Lógica de negocio
  (`construir`, línea 271) exige `respaldada_por_definicion` para vínculos
  revisados: no relajar.
- `sincronizar_studio_portal.py`: solo sincroniza triples de la ampliación
  con respaldo previo, validación SHACL del estado previsto y verificación
  de no-concurrencia. Sin cambios previstos para R7 (igual que R4/R5/R6 sin
  shapes propios salvo ronda-2/3). Solo se usa si hay cambio de grafo aprobado.

## Fallo R5 que no se repite

R5 ya corrigió el orden (invariantes + delegación antes de exactitud).
R6 instalado no delega; la nueva copia de R6 en `integracion/v001/codigo/`
aplica el mismo reorden con delegación a R7 antes de comparar exactitud
contra R6. Detalle en `notas-diseno-R7.md`.

## Universo S2 v002 (lectura)

- `S2-nacimientos/v002/entrega.json`: 53 decisiones, 31 `propuesta_para_auditar`
  (ver `universo-31.json`), 22 `brecha_externa` (todas columnas `...D`
  derivadas locales sin variable nacional: regla publicador→catálogo no
  declarada). Nada aprobado aún: auditorías A/B pendientes.
- `dependencias-correspondencias.json`: 20 pares estructurales, 5 de S2
  (filas 83,102,103,104,105). De ellos, 83/102/104 están entre las 31
  propuestas; 103/105 son `...D` (brecha) y siguen pendientes aunque se
  apruebe todo lo demás. Los otros 15 pares (S1/S3/S6) no tienen significado
  respaldado en este lote: no se promocionan automáticamente.
