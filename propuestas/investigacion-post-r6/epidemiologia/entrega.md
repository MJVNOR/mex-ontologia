# Investigación post-R6 — epidemiología (25 IDs)

Grupo: `epidemiologia`. Diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d`, conjunto
`dca16d84-dbf0-4501-b702-dc6372a480ea` (Vigilancia Epidemiológica).
IDs: filas 9 (`cve_cie10`), 11 (`acumulado`), 13 (`de01_a_04`), 23–44
(`se_ignoran`, serie `*f` 24–35, bloque institucional 36–44).

Resultado: **0 propuesta_respaldada, 25 sigue_pendiente**. Ningún ID satisface el
criterio de aceptación (documento del publicador que fije el sentido literal con
conjunto+diccionario+fila+huella y vincule edición-recurso-periodo, o
diccionario corregido/codebook aplicable a la fila). No se inventan
definiciones, vigencias ni equivalencias.

## Qué se investigó de nuevo frente a R6 (2026-10-24)

1. **Package fresco** (`evidencia/package_show_2026-10-24.json`): `version=null`,
   `fuentes_extras=""`, sin cambios vs R6. Fija la edición aplicable
   (recurso `1689b19c`, 2022-01-01/2022-12-31) y confirma que el publicador
   sigue sin publicar nota metodológica ni codebook.
2. **Diccionario live** (`evidencia/datastore_diccionario_2026-10-24.json`,
   59 filas): descripciones y catálogos vacíos sin cambios; 22 filas siguen en
   "Pendiente de especificar".
3. **Examen por ID del Manual SUIVE 32** (`evidencia/examen_manual_suive32_paginas.txt`,
   pp. 17, 18, 24, 26, 50 — R6 lo citó sólo como contexto):
   - p18: formato nacional de **30 columnas** vs **59** locales; tabulación por
     edad/sexo nacional sin convención de sufijo `f`.
   - p17: instituciones nacionales (SSA, IMSS, ISSSTE, Otras, IMSS-Prospera, DIF,
     PEMEX, SEDENA, SEMAR) — conjunto **distinto** de las 9 columnas locales
     (`imss_ord`/`imss_sol`/`d_if`/`sedemar` vs IMSS-Prospera/DIF/SEMAR).
   - p26: "acumulado" como concepto analítico semanal nacional, no regla de
     cómputo de la columna local pos 11.
   - p50: "Ign." de pantalla SUAVE nacional, no definición de `se_ignoran`.
   - CIE-10 mencionado sin versión/edición vinculada al recurso 2022.
4. **Re-descarga del manual desde URL oficial DGE**: byte-idéntico al preservado
   (mismo SHA-256), `Last-Modified 2021-08-10` anterior al periodo 2022 → sin
   vínculo edición-recurso-periodo.
5. **Negativas acotadas** (`evidencia/http_log.json`): sin edición 2022 del
   instrumento ni codebook del publicador; xlsx/csv/boletín Sonora SE 37
   bloqueados con 403 Cloudflare (sin evadir; se reutiliza inspección previa).

## Qué impide la promoción (por bloque)

- `cve_cie10`: falta objeto de la clave + versión CIE vinculada al recurso 2022.
- `acumulado`: falta objeto contado y periodo/regla de acumulación.
- `de01_a_04`: contradicción nombre (01–04) vs descripción (1–5 años) + solape
  edad 5 con `de05_a_09`; sólo una nota del publicador puede fijarlo.
- Serie `*f` (24–35): el sufijo no está documentado en ningún lado; inferirlo de
  `totalf` está prohibido.
- Bloque institucional (36–44): siglas sin objeto contado documentado y lista
  nacional no equivalente a la local.
- `se_ignoran`/`se_ignoraf`: "Pendiente de especificar" + fragmento nacional
  insuficiente.

## Archivos

- `entrega.json` (25 decisiones + 7 fuentes con SHA verificados desde bytes)
- `entrega.md` (este archivo)
- `listo.json` (hashes)
- `evidencia/`: package_show, datastore, http_log, examen por páginas
- `temporales/generar_entrega.py`: generador (hashes recomputados, no transcritos)
