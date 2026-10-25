# Plan de integración R7 — staging v002 (sin instalar)

Expediente `ejecucion-20261024-072207Z`, carpeta `integracion/v002/`.
Corrige v001 (congelada, no editada): ver
`trabajo/nota-correccion-v002.md`. Núcleo intacto. Sin Gemma, sin contactos
externos, sin tests.

## 1. Qué cubre

Adiciones exactas auditadas: reglas para el subconjunto de las 31
definiciones SINAC de `S2-nacimientos/v002/entrega.json` que las auditorías
A (documental) y B (técnica) aprueben, y solo las correspondencias de los 20
pares estructurales cuyo significado quede respaldado en el mismo lote
(S2 deja como máximo 3 promovibles: 83/102/104). Aprobación parcial o nula
admitida; nada se asume aprobado. Las columnas derivadas `...D` (103, 105 y
equivalentes) y los 15 pares de otros frentes siguen pendientes.

## 2. Código preparado (copias completas, no instaladas)

- `codigo/integrar_ronda_7.py` (nuevo, v002): universo cerrado de 31 IRIs,
  allowlist de 20 columnas, esquema cerrado de claves, un único nombre y una
  única descripción exactos por regla, conceptos existentes o nuevos sin
  sobrantes (broader verificado), vínculo con concepto idéntico al de su
  regla, orígenes con SHA pinnados por manifiesto, doble aprobación A+B por
  regla y por vínculo, base R6 exacta, unicidad y exactitud final.
  Sin filtro textual de contenido y sin NLP: el texto libre lo juzga la
  auditoría documental; los efectos prohibidos (equivalencias, identidad de
  catálogos, vigencias nuevas, fusiones) son estructuralmente imposibles por
  esta vía (`construir()` solo emite PROV + sha256).
- `codigo/integrar_ronda_6.py`: copia byte-idéntica a v001 (reorden con
  delegación a R7 antes de exactitud).
- `codigo/consolidar_semantica.py`: copia byte-idéntica a v001 (bloque fase 7).
- `sincronizar_studio_portal.py`: sin cambios; uso con respaldo y SHACL solo
  con cambio de grafo aprobado.

## 3. Base R6 (aclaración del defecto documental v001)

- Base de R7 = fichero congelado `data/integracion-ronda-6/base-semantica.json`,
  sha256 `0dd6f0f7…1407bd` (1276 reglas, 4474 vínculos, 1075 conceptos).
- `ontologia/semantica.json` (`a30a2842…fc68ca`) es el estado vivo =
  base R6 + vínculo de presas R6 (verificado por bytes); no es la base de R7.
- Al integrar, `data/integracion-ronda-7/base-semantica.json` se copia
  byte-idéntica del fichero real (`cp`, sin reescritura) y su SHA debe seguir
  siendo `0dd6f0f7…1407bd`. No mover estas fuentes.

## 4. Al aprobar A/B (no ahora)

1. Respaldar el estado a modificar.
2. Nuevo manifiesto `data/integracion-ronda-7/` con la copia byte-idéntica de
   la base, `aceptadas.json` (solo lo aprobado en A y B, según
   `esquema-aceptadas.json`), auditorías e insumos con SHA. No tocar
   manifiestos anteriores.
3. Instalar las tres copias + `ontologia/revision-ronda-7.json`.
4. Regenerar artefactos; el delta debe coincidir con lo aprobado.
5. Validaciones de datos y SHACL si cambia el RDF; Studio con respaldo solo
   con cambio de grafo aprobado.
6. Informe que separe resoluciones, vigencias y brechas externas.

## 5. Lo que no se entrega

Reglas definitivas inventadas: `trabajo/propuesta-transformacion-por-id.json`
es propuesta por ID para revisión, no aprobación. La investigación documental
adicional no requiere carta especial como único medio, pero el código solo
acepta IDs definitivamente aprobados.
