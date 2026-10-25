# Plan de integración R7 — staging v001 (sin instalar)

Expediente `ejecucion-20261024-072207Z`, carpeta `integracion/v001/`.
Trabajo previo en `integracion/trabajo/` (análisis de cadena, diseño,
universo-31, pares-20, propuesta de transformación por ID para revisión).
Núcleo intacto. Sin Gemma, sin contactos externos, sin tests.

## 1. Qué cubre

Adiciones exactas auditadas: reglas para el subconjunto de las 31
definiciones SINAC de `S2-nacimientos/v002/entrega.json` que las auditorías
A (documental) y B (técnica) aprueben, y solo las correspondencias de los 20
pares estructurales cuyo significado quede respaldado en el mismo lote.
Aprobación parcial o nula admitida; nada se asume aprobado.
Las columnas derivadas `...D` (103, 105 y equivalentes) siguen pendientes:
el código rechaza cualquier vínculo sin significado respaldado en el lote.

## 2. Código preparado (copias completas, no instaladas)

- `codigo/integrar_ronda_7.py` (nuevo): universo cerrado de 31 IRIs SINAC,
  allowlist de 20 columnas, conceptos estrictamente nuevos, doble aprobación
  A+B por regla y por vínculo, orígenes con SHA fijados por manifiesto,
  base exacta R6, rechazo de ID duplicado / versión cambiada / aporte no
  aprobado / alcance extra (equivalencias, identidad de catálogos, vigencias
  nuevas, fusiones). `construir()` exige materialización fiel con estado
  `respaldada_por_definicion` y emite solo triples PROV con sha256.
- `codigo/integrar_ronda_6.py`: copia del instalado con el reorden ya
  corregido en R5: valida duplicados y aprobaciones propias y delega a R7
  antes de comparar exactitud contra R6. Sin este orden R7 heredaría el
  defecto que R5 ya corrigió.
- `codigo/consolidar_semantica.py`: copia del instalado + bloque fase 7 en
  `generar()` (espejo del bloque R6). Sin tocar `construir` ni el contrato
  de estados.
- `sincronizar_studio_portal.py`: sin cambios; se usa tal cual con respaldo
  y SHACL, solo si hay cambio de grafo aprobado.

## 3. Al aprobar A/B (no ahora)

1. Respaldar el estado a modificar.
2. Nuevo manifiesto `data/integracion-ronda-7/`: `base-semantica.json`
   (= base R6 byte-idéntica, sha `0dd6f0f7…1407bd`), `aceptadas.json`
   (solo lo aprobado en A y B, según `esquema-aceptadas.json`),
   `auditorias/auditoria-a.json` y `b.json`, insumos con SHA.
   No tocar manifiestos anteriores.
3. Instalar las tres copias + `ontologia/revision-ronda-7.json`.
4. Regenerar artefactos; el delta debe coincidir con lo aprobado:
   `respaldada_por_definicion` +N reglas, `documental_revisada` +M vínculos.
5. Validaciones de datos y SHACL si cambia el RDF; sincronizar Studio con
   respaldo solo con cambio de grafo aprobado.
6. Cerrar con informe que separe resoluciones, vigencias y brechas externas
   sin sumar categorías solapadas.

## 4. Lo que no se entrega

Reglas definitivas inventadas: `trabajo/propuesta-transformacion-por-id.json`
es propuesta por ID para revisión, no aprobación. La investigación documental
adicional no requiere carta especial como único medio, pero el código solo
acepta IDs definitivamente aprobados.
