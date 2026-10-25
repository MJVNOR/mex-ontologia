# V3-coespo v001 — entrega (2026-10-24)

Rol V3-coespo, IDs V09–V12, V15–V16 (vigencias de catálogo COESPO).
0 propuestas acreditadas; 6 brechas externas.

## Primera puerta

Pista nueva investigada por ID: interior del recurso Diccionario del mismo
conjunto CKAN (documento concreto nunca examinado en R5/R6/post-R6).
Resultado negativo para el documento exacto en los 6 casos: los diccionarios
solo remiten CLAVE/CLAVE_ENT a "Municipios"/"Estados" y a la clasificación
INEGI (procedencia, no vigencia); sin edición/versión/fecha de
catalogo.xlsx, sin recurso de catálogo, sin periodos.
Cambio_de_fuente_por_comprobar: API `package_show` de los 3 conjuntos
re-verificada el 2026-10-24 sin cambio (version=null, Catalogo 83769).
`package_revision_list` deshabilitado (HTTP 400): sin historial accesible,
sin inferir inexistencia. No se repitieron búsquedas genéricas agotadas.

## Decisiones

| ID | Puerta | Estado | Motivo resumido |
|----|--------|--------|-----------------|
| V09 | pista_nueva (dicc. 03a33e71, negativo) | brecha_externa | F3+F4 ausentes; falta declaración de edición de catalogo.xlsx (rec. de5c06c7) y vínculo con 1990-2019/2020-2040 |
| V10 | pista_nueva (dicc. 03a33e71, negativo) | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |
| V11 | pista_nueva (dicc. 1b6d0817, negativo) | brecha_externa | Igual, conj. 943d0723 rec. d7c4b8b2 |
| V12 | pista_nueva (dicc. 1b6d0817, negativo) | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |
| V15 | pista_nueva (dicc. f1bbd13b, negativo) | brecha_externa | Igual, conj. 960ef0a9 rec. e0d2acc2, periodo 1990-2040 |
| V16 | pista_nueva (dicc. f1bbd13b, negativo) | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |

Evidencia previa conservada (5 extractos post-R6 por decisión, SHA
recomputados OK) + 2 evidencias nuevas por decisión (diccionario y API
de su conjunto) + verificación del xlsx local (ea54aad3).
Condición de reapertura: declaración del publicador con edición/versión/
fecha del catálogo + recurso + periodos + aclaración del desfase vs
CONAPO 09-05-2024; opcionalmente anexos COESPO si W-web los recupera.

## Límites

Sin petición a W-web: el navegador compartido no era necesario; las pistas
al alcance se agotaron con herramientas independientes. Paquete W-web
pendiente al cierre local, sin dependencia bloqueante (adenda posible si
W encuentra evidencia resolutiva). Sin propuesta documental_revisada:
los 20 pares estructurales siguen con significado pendiente.
Detalle del método: `trabajo/nota-puerta.md`.
Fuentes nuevas: `trabajo/fuentes/` (3 diccionarios xlsx + 3 API JSON).
