# Dictamen independiente — CLASIF (`.../67156807...%2F5`)

Veredicto: **rechazar** (`dictamen: rechazar` para automatización).
Entrega evaluada: `propuestas/investigacion-post-r6/diversos/entrega.json`
SHA-256 `4320e5fd18d27cf9b63da22ca210155bd3d24857c270a31ccd8143839079cbf3`
(previas `4e54958f…`, `9d6df76c…`, conservadas en `dictamen.json`).
Estado final aceptado: **sigue_pendiente** (motivo activo verificado
coherente: identidad documental + brecha abierta, C1-C4; cierre autor idle:
0 propuestas/5 pendientes; `staging/clasif.json` = RECHAZADA/NO_INTEGRAR,
traza histórica; propuesta original en `historial_propuesta_rechazada`).
Criterio: `propuestas/investigacion-post-r6/criterios-auditoria.md`.
No se leyó el dictamen de auditoria-otros. Criterio sin cambios;
sin promoción forzada.

## Por qué

- Ninguna afirmación primaria acredita "tipo de asentamiento":
  diccionario local = solo "Clasificación " (`data/portal/inspecciones/67156807...json`,
  `/definiciones/4`); diccionario nacional = solo "Clasificación "
  (espejo igualmente genérico dentro de `conapo-IMC_2020.zip`);
  CKAN declara base INEGI + Fuentes extras a nivel de **conjunto**, sin
  fila/huella; nota CONAPO solo acredita base a nivel colonia;
  DBF trae campo `CLASIF C(25)` sin semántica; INEGI `v_tip_asen`
  es otro instrumento (RNM, alojamientos de asistencia social) sin
  vínculo a IMC_2020, y sus códigos 1–43 no están adoptados.
- 38 valores = observados, no dominio cerrado: sin catálogo ni lista
  autorizada; `-` es nulo declarado; hay artefacto de codificación
  en `Ranchería`; DBF trae 74226 registros frente a 74227 filas XLSX.
- Igualdad recalculada por clave (ver `verificar_clasif.py` →
  `resultado.json`): 2129 claves locales = 2129 subset nacional
  Sonora (`CVE_ENT=26`), cabecera de 28 idéntica en datos,
  **0 diferencias** en los 28 campos (solo strip + `float==float`),
  misma distribución `1050/854/119/89/7/7/2/1`. Confirma identidad
  documental del extracto; no suple el significado ni autoriza
  joins, identidad de catálogos, códigos o vigencia.
- Nota SHA (resuelta, no abierta): la observación de SHA de 61 caracteres
  correspondía a versión previa; la entrega evaluada trae el SHA-256 de
  64 hex correcto `0eb78483…54e9466` en fuentes y decisiones, verificado
  contra el archivo.
- Cierre RAR/nota (ronda 2d, revisado): programa R extraído con `tar.exe`
  (`calculo-extraido/…txt`, 9031 B, no ejecutado): 0 `CLASIF`, 0
  asentamiento; carga `IMUC_2020` (rbind ambas hojas) y calcula DP2 sobre
  columnas 15:25 — arrastra `CLASIF` (col 5) sin definirla; remite a la
  nota metodológica. Nota técnica IMUC 2020 (18 pp.,
  `conapo-nota-tecnica-IMUC_2020.pdf` + `nota-tecnica-p4.txt` +
  `nota-tecnica-hits.json`): 1 mención útil en p4 nota 10
  ("clasificación de la colonia" como atributo de capa simplificada);
  0 `CLASIF` exacto, 0 "tipo de asentamiento". Conclusión firme:
  procedencia/contexto intactos, objeto sin resolver; rechazo original
  firme; pendiente final aceptado (C1-C4). 2129x28 no re-revisado:
  fuentes originales sin cambio de SHA.

## Mínimo acotado (constatación, no promoción)

> Valor textual consignado en la columna CLASIF (hoja IMC_2020,
> posición 5) del recurso 09ef2342 (2020); coincide con el
> subconjunto Sonora (2129 filas) del producto CONAPO IMC_2020
> ed. 2020 a nivel colonia; ambos diccionarios la describen
> únicamente como "Clasificación"; en Sonora se observan 7 valores
> más "-" como nulo declarado. Sin "tipo de asentamiento", sin
> dominio cerrado, sin códigos, sin joins, sin vigencia.

Límites: no reutilizar como tipo, dominio, código INEGI, join o vigencia.

## Fuentes (SHA + localizador) y código

Ver `dictamen.json` (15 fuentes con SHA-256 y localizador) y
`verificar_clasif.py` / `resultado.json` en esta misma carpeta.
Nota comparativa refrescada a SHA `9738fdfc…` (corrección 74226
válidas + 1 fila vacía, límites C1-C4).

Si los archivos del autor cambian, solicitar revisar hash final.
No se exige ninguna aprobación humana. Sin tests generales ni
contactos externos.
