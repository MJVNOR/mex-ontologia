# Agente-4 ronda-3 — aclaraciones: 23 significados, 5 observaciones, des_mpo_res

Revisión contra fuentes oficiales publicadas actuales (CKAN datos.sonora.gob.mx,
descargas 2026-10-23 UTC en `fuente/` con URL+fecha+SHA). Sin correspondencias
nuevas, sin conceptos nuevos, sin elegir vínculos, sin contactar al publicador.

## Verificación de base

103 conceptos, 232 respaldadas, 836 revisadas, 118 candidatas, 3 columnas/6 vínculos,
23 significados, 5 observaciones, 1 referencia, 32 dictámenes (23 requieren, 8 con
límite, 1 resuelto), 14 preguntas, 1850 IML/ITER: todos confirmados en
`data/semantica/cobertura.json` y `ontologia/semantica.json` antes de empezar.

## Método

1. Descarga de diccionarios vía datastore_search: 8/12 OK; 4 sin datastore
   (404: 251309e5, 587a3ccd, bfb8788b, 3395795d) cubiertos por su xlsx oficial.
   Más 2 datastore extra (recurso ffca84a8 y diccionario 6bcf5b63): 14 intentos,
   10 OK, 4 sin datastore. 14 package_show OK.
2. Comparación semántica actual vs cobertura: 25 descripciones datastore coinciden,
   0 difieren; catálogo Fiebre byte-idéntico a la fijada (sha 3b8546ac...);
   diccionario IML byte-idéntico (sha 67eda176...); sin recursos nuevos en los
   4 conjuntos principales.
3. 4 datastore 404 (251309e5, 587a3ccd, bfb8788b, 3395795d): evidencia por archivo
   xlsx oficial; contenido coincide con cobertura.

## Hallazgos por hueco

- 17 'Pendiente de especificar' (SEED 5, Nacimientos 5, Matrículas 7): sin cambios.
  CLUES (2 filas): catálogo/formato declarados vacíos; ejemplos observados
  (SRIMS000915, SRSMP000314) son valores, no significado; homonimia con el
  catálogo nacional u otros conjuntos no usada como evidencia. Requiere publicador.
- 6 documentado_con_limite (CVE_LOC, periodo, TRIMESTRE, Mes, Municipio-mat,
  Fecha-presas): descripciones idénticas; límites intactos. Sin promoción.
- O-egresos / O-fecha-num: idénticos (incluido 'Total de urgencias atendidas' y
  ejemplo 45658). O-mun-formato: formato nnn + ejemplo 26048 idénticos.
- O-anio-nac2024: traza de origen completa (comparativa.json#traza_a_o,
  scripts/probar_huella.py). Hechos: datastore CKAN declara 'a–o'
  (codepoints 0x61/0x2013/0x6F, bytes E2 80 93 en JSON crudo, sin C3 B1);
  inventario central conserva 'a–o'; huella e0437c5f... recalculada con 'a–o'
  coincide con la fijada, con 'año' difiere (9c5c13e5...); columna IRI
  .../a%E2%80%93o derivada fielmente. Archivo CSV trae latin-1 'año'
  (61 F1 6F) y diccionario 6bcf5b63 fila 2 'año' (U+00F1, 'Año de registro').
  El pipeline local es fiel (este recurso se inspeccionó por
  api_esquema_previo, sin lectura de archivo; tablas() habría dado 'año'):
  la divergencia archivo-vs-datastore está del lado del publicador
  (ingesta CKAN), no es artefacto local. Recomendación técnica: no aplicar
  corrección local; si el publicador corrige el datastore a 'año', la huella
  de esquema cambiará de e0437c5f... a 9c5c13e5... e invalidará las 5
  revisiones G-239 y esta observación (revisión obligatoria). Se mantiene
  requiere_aclaracion_publicador con evidencia precisa y pregunta mantenida.
  Sin alias ñ→n, sin correspondencia.
- O-anio-div2023: resuelto en integración, citado íntegro, sin generalizar.
- A-30b18862/A-4121cf57/A-cc6c566f: defecto documental común — filas 177/178 son
  un artefacto de tabla ancha transpuesta (cada celda un nombre de variable,
  172 columnas Unnamed, ejemplos ide_cp/id_cp); ambos vínculos igualmente
  degenerados; no se elige.
- R-des-mpo-res: catálogo byte-idéntico, 3 hojas, 0 ocurrencias de
  des_mpo_res/ide_id/ide_col/des_jur_res/cve_loc_res; fila 7 homónima es texto
  libre municipal sin catálogo (no origen); sin recursos nuevos. Sin resolver.

## Entregas

`propuestas.json` (32 decisiones 23/8/1, 14 preguntas trazables),
`preguntas-publicador.md` (14 originales + estado),
`comparativa.json`, `fuente/manifiesto-fuentes.json` + descargas,
`scripts/` (descargar_evidencia, analizar, generar_propuestas,
generar_preguntas, leer_xlsx), `verificar.py` en raíz,
`resultado.md`.

## Límites y pendientes

Ningún hueco aclarado por las fuentes consultadas; todo sigue requiere_publicador o
documentado_con_limite. Lo no encontrado en las fuentes consultadas no implica
imposibilidad global: pueden existir documentos oficiales no consultados (fuera
de CKAN o no descargados por pertinencia); se registra solo lo verificado.
Datastore 404 en 4 diccionarios (límite de acceso, no de contenido: cubierto por
xlsx). Sin UI ni cruces. Bloqueo: red CKAN devolvió 403
sin User-Agent (resuelto con cabecera estándar); Divorcios-2023 sin datastore
(recurso CSV, no necesario: caso resuelto citado).
