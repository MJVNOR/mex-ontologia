# Diseño R7 (adiciones exactas auditadas) — propuesta, sin instalar

## Alcance

- Reglas: subconjunto (parcial o vacío, nunca supuesto) de las 31 definiciones
  SINAC en `universo-31.json`, solo las que A y B aprueben con `aceptar`.
- Vínculos: solo columnas del allowlist de 20 pares (`pares-20.json`) cuya
  `definicion_iri` quede respaldada por una regla de la misma `aceptadas.json`.
  Las `...D` (103,105 y equivalentes) siguen pendientes: el código las rechaza
  por falta de respaldo, no por lista manual.
- Conceptos nuevos: solo si ningún concepto de la base R6 representa
  exactamente el sentido. Cada concepto nuevo trae alcance + representación y
  límites; nada de códigos equivalentes, identidad de catálogos ni vigencias.
- Base congelada: `base-semantica.json` debe ser byte-idéntica al estado R6
  validado (`data/integracion-ronda-6/base-semantica.json`,
  sha256 `0dd6f0f7dfdb057a57c47d5dbec690b41f564f07690c7551e3f1a6c4421407bd`).
  Ronda 7 no reescribe historia: R4/R5/R6 intactos.

## Reglas de integridad (implementadas en `codigo/integrar_ronda_7.py`)

1. Manifiesto nuevo fija todo: `base-semantica.json`, `aceptadas.json`,
   `auditorias/auditoria-a.json`, `auditorias/auditoria-b.json` + insumos.
   `cargar()` verifica SHA de cada archivo e insumo; rechaza manifiesto
   incompleto, evidencia fuera de carpeta, versión cambiada.
2. Aporte no aprobado → rechazo: cada regla (`id`) y cada vínculo (`columna`)
   exige `aceptar` en AMBOS dictámenes (A y B). Aprobación parcial = solo el
   subconjunto aprobado viaja en `aceptadas.json`; aprobación nula = listas
   vacías (el código lo admite: cero adiciones, cadena intacta).
3. ID duplicado → rechazo: ids de regla, definiciones y columnas únicos en
   `aceptadas.json` y en `rules` final.
4. Universo cerrado: cada regla usa exactamente 1 definición del universo de
   31, con diccionario `22202305-…`, conjunto `940de7d8-…` y huella de fila
   obligatoria; cada vínculo usa 1 columna del allowlist de 20 y su
   `definicion_iri` debe estar respaldada en el mismo lote.
5. Conceptos sin silencios: clave nueva obligatoria (si existe en base → error,
   reutilizar en su lugar); valor `[etiqueta, definición, broader-o-null]` con
   broader existente; sin sobrescritura ni deduplicación silenciosa.
6. Sin alcance extra: barrido de `join/vigencia/equivalen/homolog/sameas/
   exactmatch/unifica/fusiona/identidad.*catalogo` sobre campos libres de
   reglas y vínculos; límites escritos obligatorios; representación y criterio
   obligatorios.
7. Contrato del núcleo intacto: `construir()` exige variable materializada con
   `estado == respaldada_por_definicion` + regla/concepto/huella fieles, y
   vínculo con `revision` fiel; emite solo triples PROV con sha256 de la
   evidencia fijada. No toca `consolidar_semantica.py:construir` ni relaja
   `respaldada_por_definicion`.

## Archivos que se instalarían (copias completas en `v001/codigo/`)

- `integrar_ronda_7.py` (nuevo).
- `integrar_ronda_6.py` (copia del instalado + reorden: invariantes propios y
  delegación a R7 antes de comparar exactitud contra R6).
- `consolidar_semantica.py` (copia del instalado + bloque fase 7 en `generar()`).
- Al integrar (no ahora): `ontologia/revision-ronda-7.json` +
  `data/integracion-ronda-7/{manifiesto.json, base-semantica.json,
  aceptadas.json, auditorias/auditoria-a.json, auditorias/b.json}`.
- `sincronizar_studio_portal.py`: sin cambios (se usa tal cual, con respaldo,
  solo si hay cambio de grafo aprobado).

## Lo que NO se prepara ahora

Reglas definitivas inventadas. `propuesta-transformacion-por-id.json` es una
propuesta de transformación por ID para revisión (origen: afirmaciones v002),
no una aprobación. `esquema-aceptadas.json` fija el contrato vacío que el
manifiesto nuevo llenará solo con lo que A/B aprueben.
