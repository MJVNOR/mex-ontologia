# V3-coespo v002 — entrega (2026-10-24, corrección auditoría A lote-1)

Rol V3-coespo, IDs V09–V12, V15–V16 (vigencias de catálogo COESPO).
0 propuestas acreditadas; 6 brechas externas (estado y condición conservados
de v001; v001 no editada).

## Corrección aplicada

Se retira la etiqueta de novedad no demostrada ("nunca examinado",
"por primera vez"): el interior de los 3 Diccionarios CKAN se examinó en
esta revisión con resultado negativo para F3+F4, y no consta examen previo
del interior para vigencia en los antecedentes citados. Puerta re-etiquetada
a `sin_pista_nueva`, tipo_trabajo
`analisis_adicional_de_documento_conocido`. Las URL de los diccionarios se
conservan como soportes analizados, sin etiqueta nueva. El API
`package_show` queda etiquetado como re-verificación sin cambio
(version=null, Catalogo 83769), no como evidencia nueva.
`package_revision_list` deshabilitado (HTTP 400): sin historial accesible,
sin inferir inexistencia.

## Decisiones

| ID | Puerta | Estado | Motivo resumido |
|----|--------|--------|-----------------|
| V09 | sin_pista_nueva | brecha_externa | F3+F4 ausentes; falta declaración de edición de catalogo.xlsx (rec. de5c06c7) y vínculo con 1990-2019/2020-2040 |
| V10 | sin_pista_nueva | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |
| V11 | sin_pista_nueva | brecha_externa | Igual, conj. 943d0723 rec. d7c4b8b2 |
| V12 | sin_pista_nueva | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |
| V15 | sin_pista_nueva | brecha_externa | Igual, conj. 960ef0a9 rec. e0d2acc2, periodo 1990-2040 |
| V16 | sin_pista_nueva | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |

Evidencia previa conservada (5 extractos post-R6 por decisión) + soportes
analizados en esta revisión (diccionario y API de su conjunto, con
formulación acotada) + verificación del xlsx local (ea54aad3).
Condición de reapertura: declaración del publicador con edición/versión/
fecha del catálogo + recurso + periodos + aclaración del desfase vs
CONAPO 09-05-2024; opcionalmente anexos COESPO si W-web los recupera.

## Límites

Sin nuevas búsquedas para v002; sin otras carpetas. Paquete W-web pendiente
al cierre local, sin dependencia bloqueante (adenda posible si W encuentra
evidencia resolutiva). Sin propuesta documental_revisada: los 20 pares
estructurales siguen con significado pendiente.
Detalle del método: `trabajo/nota-puerta.md` (registro histórico de v001;
la formulación vigente es la acotada de este documento y de `entrega.json`).
Soportes: `trabajo/fuentes/` (3 diccionarios xlsx + 3 API JSON).
