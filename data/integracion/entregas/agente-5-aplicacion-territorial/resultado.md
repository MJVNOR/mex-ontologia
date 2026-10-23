# Aplicacion de catalogos territoriales a archivos de datos

Fecha de comprobacion (UTC): 2026-10-23T09:11:14Z

Ocho variables documentadas con recurso de catalogo ya identificado (ontologia/territorio.json). No se reidentifica ni se propone ningun catalogo nuevo.

## Alcance y metodo

- Solo se leyeron columnas de clave, periodo (AÑO/Año) y nombre (NOM_MUN/NOM_ENT cuando existe). No se descargaron ni conservaron filas de personas; solo controles y conjuntos de claves.
- Codigo original conservado; comparacion con `strip`. Transformacion propuesta: `strip` al comparar. Sin relleno (`zfill`) ni prefijos: las ocho referencias usan sus propias claves (la transformacion `26 + municipio a tres digitos` pertenece a otros casos y no se aplica aqui).
- Cobertura (`completa`/`muestral`) y resultado (`compatible`/`compatible_con_excepciones`/`no_compatible`/`sin_columna_fisica`) se registran por separado.
- Repetir un codigo en distintas filas (formato largo) no es por si solo un error.
- Alias `Magdalena de Kino / Magdalena` (id `magdalena-sonora`, ontologia/territorio.json) vigilado solo en las entradas registradas; en los datos aparece `Magdalena`, sin activar el alias.
- Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

## Resumen por variable documentada

| Var | Variable | Conjunto | Recursos de datos | Periodos | Cobertura | Resultado |
| --- | --- | --- | ---: | --- | --- | --- |
| V1 | CLAVE | Proyecciones de poblacion - Grupos quinquenal | 1 | 1990-2040 (columna AÑO) | completa | compatible |
| V2 | CLAVE_ENT | Proyecciones de poblacion - Grupos quinquenal | 1 | 1990-2040 (columna AÑO) | completa | compatible |
| V3 | CLAVE | Proyecciones de poblacion - Grandes grupos de | 1 | 1990-2040 (columna AÑO) | completa | compatible |
| V4 | CLAVE_ENT | Proyecciones de poblacion - Grandes grupos de | 1 | 1990-2040 (columna AÑO) | completa | compatible |
| V5 | Cve. Municipio | Incidencia delictiva municipal | 11 | 2015–2025 | completa | compatible_con_excepciones |
| V6 | Clave_Ent | Victimas del fuero comun en el estado | 10 | 2016–2025 | completa | compatible |
| V7 | CLAVE | Proyecciones de poblacion - Indicadores demog | 1 | 1990-2040 (columna AÑO) | completa | compatible |
| V8 | CLAVE_ENT | Proyecciones de poblacion - Indicadores demog | 1 | 1990-2040 (columna AÑO) | completa | compatible |

Nota: V6 (Clave_Ent, victimas) no tiene columna fisica en el recurso 2015 (`4c1f984e…`), que trae `Cve. Municipio` sin respaldo en el diccionario `a8a09044…`; ese recurso queda `sin_columna_fisica` para V6.

## Detalle por recurso, columna y periodo

### V1 · CLAVE · recurso `81513319…` · periodo 1990-2040 (columna AÑO)

- Comprobacion: valores distintos de la columna fisica `CLAVE` contra `de5c06c7…/Catalogo_Municipios` (72 entradas).
- Ubicacion fisica: hoja `Sheet 1`, columna `A` (posicion 1), encabezado `CLAVE`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7344 filas leidas, 72 claves distintas, periodos: 1990–2040 (51).
- Coincidencias: 72 de 72 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Coherencia compuesta CLAVE↔CLAVE_ENT (CLAVE(5 digitos) == CLAVE_ENT(2 digitos) + municipio(3 digitos); igualdad exacta): 72 pares distintos, incoherentes=ninguno.
- Nombres (NOM_MUN leido): sin contradicciones (un nombre por codigo); 26036 → ['Magdalena'].
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['numerico_a_texto'].
- Consulta: descarga publicada, lectura solo de columnas clave+anio+nombre — `descargas/81513319-6073-4239-84ab-4cfcc660819a.xlsx`, SHA-256 `09eb9e0c49151c86…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V2 · CLAVE_ENT · recurso `81513319…` · periodo 1990-2040 (columna AÑO)

- Comprobacion: valores distintos de la columna fisica `CLAVE_ENT` contra `de5c06c7…/Catalogo_Estado` (32 entradas).
- Ubicacion fisica: hoja `Sheet 1`, columna `B` (posicion 2), encabezado `CLAVE_ENT`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7344 filas leidas, 1 claves distintas, periodos: 1990–2040 (51).
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Coherencia compuesta CLAVE↔CLAVE_ENT (CLAVE(5 digitos) == CLAVE_ENT(2 digitos) + municipio(3 digitos); igualdad exacta): 72 pares distintos, incoherentes=ninguno.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['numerico_a_texto'].
- Consulta: descarga publicada, lectura solo de columnas clave+anio+nombre — `descargas/81513319-6073-4239-84ab-4cfcc660819a.xlsx`, SHA-256 `09eb9e0c49151c86…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V3 · CLAVE · recurso `775d76b5…` · periodo 1990-2040 (columna AÑO)

- Comprobacion: valores distintos de la columna fisica `CLAVE` contra `d7c4b8b2…/Catalogo_Municipios` (72 entradas).
- Ubicacion fisica: hoja `Sheet 1`, columna `A` (posicion 1), encabezado `CLAVE`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7344 filas leidas, 72 claves distintas, periodos: 1990–2040 (51).
- Coincidencias: 72 de 72 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Coherencia compuesta CLAVE↔CLAVE_ENT (CLAVE(5 digitos) == CLAVE_ENT(2 digitos) + municipio(3 digitos); igualdad exacta): 72 pares distintos, incoherentes=ninguno.
- Nombres (NOM_MUN leido): sin contradicciones (un nombre por codigo); 26036 → ['Magdalena'].
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['numerico_a_texto'].
- Consulta: descarga publicada, lectura solo de columnas clave+anio+nombre — `descargas/775d76b5-eabc-4342-9beb-741ec68c42ed.xlsx`, SHA-256 `24301617b6a5d89c…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V4 · CLAVE_ENT · recurso `775d76b5…` · periodo 1990-2040 (columna AÑO)

- Comprobacion: valores distintos de la columna fisica `CLAVE_ENT` contra `d7c4b8b2…/Catalogo_Estado` (32 entradas).
- Ubicacion fisica: hoja `Sheet 1`, columna `B` (posicion 2), encabezado `CLAVE_ENT`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7344 filas leidas, 1 claves distintas, periodos: 1990–2040 (51).
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Coherencia compuesta CLAVE↔CLAVE_ENT (CLAVE(5 digitos) == CLAVE_ENT(2 digitos) + municipio(3 digitos); igualdad exacta): 72 pares distintos, incoherentes=ninguno.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['numerico_a_texto'].
- Consulta: descarga publicada, lectura solo de columnas clave+anio+nombre — `descargas/775d76b5-eabc-4342-9beb-741ec68c42ed.xlsx`, SHA-256 `24301617b6a5d89c…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V7 · CLAVE · recurso `7e590f35…` · periodo 1990-2040 (columna AÑO)

- Comprobacion: valores distintos de la columna fisica `CLAVE` contra `e0d2acc2…/Catalogo_Municipios` (72 entradas).
- Ubicacion fisica: hoja `Sheet 1`, columna `A` (posicion 1), encabezado `CLAVE`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 3672 filas leidas, 72 claves distintas, periodos: 1990–2040 (51).
- Coincidencias: 72 de 72 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Coherencia compuesta CLAVE↔CLAVE_ENT (CLAVE(5 digitos) == CLAVE_ENT(2 digitos) + municipio(3 digitos); igualdad exacta): 72 pares distintos, incoherentes=ninguno.
- Nombres (NOM_MUN leido): sin contradicciones (un nombre por codigo); 26036 → ['Magdalena'].
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['numerico_a_texto'].
- Consulta: descarga publicada, lectura solo de columnas clave+anio+nombre — `descargas/7e590f35-f293-40e3-b3e1-4002f8c3fbfe.xlsx`, SHA-256 `e0e21aad3a84b405…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V8 · CLAVE_ENT · recurso `7e590f35…` · periodo 1990-2040 (columna AÑO)

- Comprobacion: valores distintos de la columna fisica `CLAVE_ENT` contra `e0d2acc2…/Catalogo_Estado` (32 entradas).
- Ubicacion fisica: hoja `Sheet 1`, columna `B` (posicion 2), encabezado `CLAVE_ENT`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 3672 filas leidas, 1 claves distintas, periodos: 1990–2040 (51).
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Coherencia compuesta CLAVE↔CLAVE_ENT (CLAVE(5 digitos) == CLAVE_ENT(2 digitos) + municipio(3 digitos); igualdad exacta): 72 pares distintos, incoherentes=ninguno.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['numerico_a_texto'].
- Consulta: descarga publicada, lectura solo de columnas clave+anio+nombre — `descargas/7e590f35-f293-40e3-b3e1-4002f8c3fbfe.xlsx`, SHA-256 `e0e21aad3a84b405…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `2513ec12…` · periodo 2015

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2015.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/2513ec12-4b23-4700-8eeb-9cfb634d5553.csv`, SHA-256 `2256fbe28c736251…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `147ead58…` · periodo 2016

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2016.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/147ead58-f894-4b0d-9881-ab06368e4cc9.csv`, SHA-256 `58ef1ffc31cd49ea…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `4e13a33e…` · periodo 2017

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2017.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/4e13a33e-4738-41ac-a0a4-3ac0afab9091.csv`, SHA-256 `4892972c65e66727…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `d18cac7c…` · periodo 2018

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2018.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/d18cac7c-60dd-45ce-8cba-d90dc9fb5a18.csv`, SHA-256 `3ccdadaa99759ef3…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `0794d04e…` · periodo 2019

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2019.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/0794d04e-7779-4fb6-b2ad-94a927e49a64.csv`, SHA-256 `ed5a5fa47d759b1c…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `70c0bfb7…` · periodo 2020

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2020.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/70c0bfb7-5378-42db-a20c-95da9ce1a4e4.csv`, SHA-256 `6dfade242af0bda9…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `22d74901…` · periodo 2021

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2021.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/22d74901-c3ab-4d80-9f4f-b9e7da051ba8.csv`, SHA-256 `09446ed0b18100e8…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `fc4a46ba…` · periodo 2022

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2022.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/fc4a46ba-5318-4cc9-aadc-aa578300af15.csv`, SHA-256 `5bb9d16dcd05cd31…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `18b58aaf…` · periodo 2023

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2023.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/18b58aaf-e382-478e-86d9-8f50a7b08e12.csv`, SHA-256 `82d91ffd2a2e96d4…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `fb66e0fa…` · periodo 2024

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2024.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/fb66e0fa-21e5-4c11-9d9d-7b4f701ee044.csv`, SHA-256 `4ebfde317c717535…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V5 · Cve. Municipio · recurso `befd1c5e…` · periodo 2025

- Comprobacion: valores distintos de la columna fisica `Cve. Municipio` contra `36d3ac85…/cat_municipio` (74 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Cve. Municipio`.
- Significado: municipio respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 7252 filas leidas, 74 claves distintas, año: 2025.
- Coincidencias: 74 de 74 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=['26998', '26999']; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/befd1c5e-1222-4795-a866-d46cf602637b.csv`, SHA-256 `db47cc48dd7c90e7…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible_con_excepciones**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `15650860…` · periodo 2016

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2016.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/15650860-3a0b-461f-becb-658422e3a597.csv`, SHA-256 `9013760a92dd7314…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `c7ab7527…` · periodo 2017

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2017.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/c7ab7527-c2f5-44f2-a33e-6a368574f992.csv`, SHA-256 `ba2791100c45a1fa…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `1d7c90a8…` · periodo 2018

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2018.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/1d7c90a8-d10b-4dbc-a16d-61e57164d80a.csv`, SHA-256 `ef6dfc962d3dacac…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `e26eafbe…` · periodo 2019

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2019.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/e26eafbe-5d74-4882-af64-89e5bddbb46e.csv`, SHA-256 `c2e0a616b95cc2c9…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `652ca41a…` · periodo 2020

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2020.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/652ca41a-5c9e-4d00-aa9a-f4d006b613fe.csv`, SHA-256 `ce5e87cf6f5fe25f…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `1ec37796…` · periodo 2021

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2021.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/1ec37796-0ad6-44b9-ba36-30bd4ae3d526.csv`, SHA-256 `0baf917083876076…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `8c2618f2…` · periodo 2022

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2022.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/8c2618f2-b317-41b0-b0d3-8020e735ffd7.csv`, SHA-256 `6b3c84ac6f8974a1…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `10d7cb8c…` · periodo 2023

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2023.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/10d7cb8c-4058-4b9c-85f5-c25819d0f66b.csv`, SHA-256 `7f42555266602998…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `8f959438…` · periodo 2024

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2024.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/8f959438-7c12-419a-be1b-e0e4a52b0a26.csv`, SHA-256 `c961edcdad293ff4…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `39ff0330…` · periodo 2025

- Comprobacion: valores distintos de la columna fisica `Clave_Ent` contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: hoja `CSV (hoja unica)`, columna `B` (posicion 2), encabezado `Clave_Ent`.
- Significado: entidad respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado.
- Cobertura: completa — 230 filas leidas, 1 claves distintas, año: 2025.
- Coincidencias: 1 de 1 claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—.
- Transformacion propuesta: strip al comparar; conservar original y ceros; sin relleno ni prefijo; observadas en lectura: ['ninguna'].
- Consulta: descarga publicada CSV, lectura solo de columnas clave+anio — `descargas/39ff0330-1959-4b92-914e-a48c691aff01.csv`, SHA-256 `0934ab8a6c22683f…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **compatible**. Limitaciones: Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre poblaciones, periodos o niveles de agregacion.

### V6 · Clave_Ent · recurso `4c1f984e…` · periodo 2015

- Comprobacion: valores distintos de la columna fisica — (ausente) contra `7f3aca28…/cat_entidad` (32 entradas).
- Ubicacion fisica: sin columna fisica en el recurso; encabezado extraido del archivo: ['Año', 'Cve. Municipio', 'Bien jurídico afectado', 'Tipo de delito', 'Subtipo de delito', 'Modalidad', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'].
- Significado: entidad-registro respaldada por definicion; SIN columna fisica en el recurso 2015.
- Cobertura: revision de encabezado **completa**; validacion de valores **no_aplicable**.
- Coincidencias: 0 de ? claves en el catalogo.
- Excepciones: nulos=0; especiales_no_municipales=—; sin_correspondencia=—; nota: El recurso 2015 trae 'Cve. Municipio' (nivel municipal) sin respaldo en el diccionario a8a09044; no se homologa con Clave_Ent..
- Transformacion propuesta: ninguna; columna fuera del alcance de las ocho variables; observadas en lectura: —.
- Consulta: descarga publicada; encabezado extraido del archivo, sin lectura de valores — `descargas/4c1f984e-a6be-412b-b274-5af2d4ff55b1.csv`, SHA-256 `2256fbe28c736251…`, 2026-10-23T09:11:14Z.
- Estado del resultado: **sin_columna_fisica**. Limitaciones: No se comprueba Clave_Ent en 2015 porque la columna no existe en ese recurso. Revision de encabezado completa; validacion de valores no aplicable.

## Casos especiales

- `26998` (No Especificado) y `26999` (Otros Municipios): pertenecen al catalogo `36d3ac85…/cat_municipio` y, simultaneamente, son categorias no municipales (aparecen en los 11 recursos anuales de incidencia 2015–2025).
- Victimas 2015 (`4c1f984e…`): 7252 filas con `Cve. Municipio` (74 claves 26001–26072 + 26998/26999); esa columna no tiene respaldo en el diccionario `a8a09044…`, por lo que no se homologa con `Clave_Ent` ni se evalua contra `cat_entidad`.
- Encabezados de periodo con `enye` (`AÑO` en XLSX, `Año` en CSV, UTF-8 con BOM en CSV); la lectura conserva el texto fisico y solo aplica `strip`.
- SHA-256 completos de cada archivo descargado y de cada catalogo en `propuestas.json`; conjuntos de claves (original + normalizado) en `claves/`.
