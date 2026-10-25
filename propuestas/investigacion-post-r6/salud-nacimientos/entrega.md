# Investigación post-R6 — salud-nacimientos (53 IDs)

Grupo: `salud-nacimientos`. Conjunto Información Sobre Nacimientos (SINAC Sonora 2022,
recurso 46977217, 2022-01-01 a 2022-09-26). Diccionario 22202305-2d02-4c49-b216-cc98224357f0.
Fecha de investigación: 2026-10-24. Sin contactos al publicador; sólo evidencia primaria
pública y material local preservado. Históricos, manifiestos, semántica, cobertura,
Studio y chat intactos.

## Resultado

0 propuestas respaldadas / 53 siguen pendientes. Ninguna primaria examinada acredita el
vínculo fila-local ↔ edición/recurso/periodo exigido por el criterio de aceptación, por lo
que no hay insumos de staging (nada que promover sin modificar el núcleo).

## Qué se investigó (nuevo frente a R6)

1. Re-verificación local 2026-10-24: las 53 filas del diccionario 22202305 siguen con
   `Descripción='Pendiente de especificar'` y `Catálogo de referencia=''` (ver
   `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json`, `/definiciones`).
2. Manual de Instalación y Operación del SINAC, DGIS (NUEVO, HTTP 200, 7 710 525 B):
   también edición **Modelo 2015, SINAC Versión 2.0.1**; 0 menciones a 2022; sin
   diccionario de variables ni codebook.
3. `CN_ManualLlenado.pdf` servido hoy por gob.mx (NUEVO): bytes **idénticos** al
   preservado R5 (`a97b4ec4…`); portada Modelo 2015; 0 menciones a 2022. Examen por ID:
   preguntas 11, 12, 13, 14, 16, 22.1, 22.2, 23, 24, 25, 27, 28.2, 29, 32, 34-35, 37
   citadas por decisión en `entrega.json`; ninguna trae mapa a columnas locales,
   codebook publicado ni vigencia a 2022.
4. Página oficial SINAC re-verificada (HTTP 200): última modificación 2022-01-13;
   **único documento enlazado = metodología de calidad 2020** (descargada, HTTP 200,
   2 041 492 B, 17 pp.: índice cobertura/consistencia/oportunidad; 0 definiciones).
   Ningún manual de nacimiento enlazado.
5. Diccionario nacional INEGI RNM-530/SINAC2018 (NUEVO, HTTP 200): 62 variables V1–V62
   con etiqueta y pregunta del CN (datos 2017). Examinado por ID: p. ej. V18 orden_nac,
   V19 aten_pren, V35 apgarh, V48 clues, V54 cert_por. No acredita: otra edición,
   otro periodo (2017 vs 2022), 62 vars vs 106 columnas, nombres distintos
   (`orden_nac` vs `ORDENNACIMIENTO`), columnas `D` sin contraparte, sin tabla de
   equivalencias del publicador.
6. DOF Lineamientos CEN (código 5389287, HTTP 200): el rol Codificador usa CIE-10 y
   "catálogos contenidos en el eSINAC" (no publicados); Manual de Expedición del CN
   anunciado sin URL. Sin codebook ni vínculo a Sonora 2022.
7. SEED Modelo 2022 (R6): ámbito **defunciones y muerte fetal**, no nacimientos.
   Usarlo para SINAC sería cruce de subsistemas: se documenta y se descarta.

## Por qué no se promueve nada (regla aplicada por ID)

La homonimia con el manual nacional o el diccionario INEGI no acredita vínculo local.
Cada decisión en `entrega.json` cita la contraparte nacional exacta y la falla formal
(edición/periodo distintos, sin mapa pregunta↔columna, sin codebook, columnas `D` sin
correlato, o ausencia total de contraparte como `TIEMPOTRASLADO`).

## Hueco exacto que impide la promoción

Falta el vínculo del publicador entre cada fila (conjunto+diccionario+fila+huella) y el
recurso 46977217: diccionario corregido con descripciones, o nota con
descripción+codebook+tabla pregunta-manual↔columna-local y edición aplicable al periodo
2022-01-01 a 2022-09-26. En manos del publicador.

## Búsquedas negativas (limitadas a lo revisado, ver `evidencia/http-log.json`)

Página SINAC sin manual; manual DGIS-SINAC edición 2015; Modelo 2015 sin vigencia 2022;
INEGI 2017 sin equivalencias; DOF sin codebook publicado; SEED fuera de ámbito.
No ausencia universal.

## Archivos

- `entrega.json` — 53 decisiones + 12 fuentes con SHA verificados contra bytes.
- `evidencia/` — 2 PDF DGIS, 4 capturas HTML, `http-log.json` (7 consultas HTTP 200).
- `temporales/` — `generar_entrega.py`, extracciones de texto, verificación gob.mx↔R5.
