# Agente 1 — Revisión de las 9 referencias a catálogos sin resolver

Propuestas, no aplicadas al grafo ni a los archivos centrales. Escritura exclusiva en `propuestas/agente-1-catalogos/`.

Fecha: 2026-10-23. Fuente: portal `https://datos.sonora.gob.mx/` (CKAN). Aislamiento: solo lectura fuera de esta carpeta; sin motor, sin sincronizar Studio, sin propuestas de otros agentes. Los SHA-256 de las 12 descargas y las huellas de las filas documentales coinciden con la evidencia previa.

## Resultado

De 9 referencias en `solo_referencia_declarada_sin_resolver` (las 8 territoriales están excluidas, ver §8):

- **8 con recurso identificado** (P01–P08): 4 educativas (una por conjunto), 1 hídrica, 3 de Fiebre manchada.
- **1 sin resolver** (P09): `des_mpo_res` (filas 177 y 178 del diccionario de Fiebre manchada).

Identificar el catálogo **no** significa que todos los archivos de datos lo usen ni que su vigencia histórica esté comprobada. Hojas, encabezados, nombres, códigos y entradas se conservan literalmente desde los archivos publicados; cualquier normalización va solo en campos `normalizacion/*` de `propuestas.json`.

## Las 9 referencias (origen documental)

Los literales del grafo central presentan daño de codificación; los originales legibles se tomaron de las celdas de los diccionarios descargados (`nombre_catalogo_diccionario` en cada propuesta).

| P | Referencia | Nombre original (diccionario) | Conjunto | Variable diccionario | Fila dicc. |
|---|-----------|-------------------------------|----------|----------------------|-----------|
| P01 | `1eb8b1a5…` | Clasificación mexicana…superior (sin dos puntos) | Promedio Académico `403912fd…` | `CAMPO DE FORMACIÓN ACADÉMICA` | 5 (`ed82f8a6…/5`, huella `37bb7e…`) |
| P02 | `4c28a0a2…` | Clasificación mexicana…superior**:** (con dos puntos) | Matriculas `e5aad52d…` | `Campo de Formación Académica` | 6 (`dc87a5be…/6`, huella `f4c01a…`) |
| P03 | `4c67f244…` | Clasificación mexicana…superior (sin dos puntos) | Estudiantes Titulados `e7a3d62f…` | `Campo de Formación Académica` | 3 (`508da131…/3`, huella `9990bf…`) |
| P04 | `7c2e51a0…` | Clasificación mexicana…superior (descripción con "formación académica" separado) | Estudiantes egresados `85ee0e2b…` | `Campo de Formación Académica` | 3 (`598dbd86…/3`, huella `72585f…`) |
| P05 | `3b45c474…` | `Catálogo_estatal` | Recursos Hídricos `ee8f639f…` | `Clave` (Clave de la presa ) | 1 (`ca5574f0…/1`, huella `521c50…`) |
| P06 | `9ff643fe…` | `Catálogo servicios` | Fiebre manchada `5494daa1…` | `servic_atencion` | 129 (`33d0a99e…/129`, huella `1c023d…`) |
| P07 | `5b1ccbaa…` | `Motivos de rechazo` (+espacio final) | Fiebre manchada | `motiv_rech_ricket_sangre` | 162 (`…/162`, huella `3825b9…`) |
| P08 | `c8e9eb88…` | `Especie rickettsiosis` | Fiebre manchada | `ricket_especie_rtpcr` | 168 (`…/168`, huella `592dc7…`) |
| P09 | `a2902c1f…` | `des_mpo_res` | Fiebre manchada (las **dos** filas son de este diccionario; **no** de Vigilancia Epidemiológica) | `ide_id` / `ide_col` (filas degeneradas) | 177 (`…/177`, huella `4b1762…`) y 178 (`…/178`, huella `b5dbcd…`) |

Detalle de máquinas en `fase1_refs.json`, `exactos.json`, `conjuntos_objetivo.json`.

## Evidencia publicada verificada (descarga 2026-10-23)

Manifiesto: `manifiesto_descargas.json` (URL, status, content-type, fecha, SHA-256, bytes, archivo local en `fuentes/`). Los 12 archivos (6 catálogos + 6 diccionarios) devolvieron HTTP 200 y sus SHA coinciden con la inspección local previa, salvo el diccionario de Fiebre (CSV descargado `2c8ce1…`; la inspección anterior usó la API datastore).

| Conjunto | Recurso Catalogo | URL | SHA-256 | Hoja / campos literales | Contenido (revisión completa: catálogos pequeños) |
|----------|-----------------|-----|---------|-------------------------|---------------------------------------------------|
| Promedio Académico | `6d561451…` | `…/403912fd…/resource/6d561451…/download/catalogo.xlsx` | `53bd5e97…4259` | `Hoja1`: `Campo de Formación Académica, Clasificación` | 10 entradas `01–10` (Educación…Servicios), códigos únicos |
| Matriculas | `aaf0c6c1…` | `…/e5aad52d…/resource/aaf0c6c1…/download/catalogo.xlsx` | `53bd5e97…4259` (idéntico) | `Hoja1`: mismos campos | 10 entradas idénticas, códigos únicos |
| Estudiantes Titulados | `0e69d911…` | `…/e7a3d62f…/resource/0e69d911…/download/catalogo.xlsx` | `53bd5e97…4259` (idéntico) | `Hoja1`: mismos campos | 10 entradas idénticas, códigos únicos |
| Estudiantes egresados | `af7a9aba…` | `…/85ee0e2b…/resource/af7a9aba…/download/catalogo.xlsx` | `53bd5e97…4259` (idéntico) | `Hoja1`: mismos campos | 10 entradas idénticas, códigos únicos |
| Recursos Hídricos | `f5060479…` | `…/ee8f639f…/resource/f5060479…/download/catalogo.xlsx` | `612b2b11…aaf824` | `Catálogo_estatal`: `Clave, Comision, Subdireccion, Presa, Nombre_comun, Estado, Municipio, cap_name, cap_namo, vol_muerto, Río, Numero, Latitud, Longitud, Altitud, Identificador_cuenca_disponibilidad, Cuenca de disponibilidad, Numero_region_hidrologica, Region_hidrológica` (+ hojas `Municipios` 72 entradas y `Regiones` 10 entradas, no referenciadas) | 10 presas, claves únicas `LCDSO, PECSO, AOBSO, AGZCH, ARCSO, PMOSO, ARLSO, CHTSO, IRASO, BICSO` |
| Fiebre manchada | `08d3b1a7…` | `…/5494daa1…/resource/08d3b1a7…/download/catalogo.xlsx` | `3b8546ac…ba293d` | `Catalogo Servicios: servic_atencion, tipo de atencion` (7); `Catalogo rechazo: motiv_rech_ricket_sangre, Tipo de rechazo` (20); `Catalogo especie: ricket_especie, especie` (4) | 7+20+4 entradas, códigos únicos por hoja (revisión completa) |

Contenido volcado en `catalogos_contenido.json` (hoja, encabezado y filas literales celda por celda).

### Correspondencias de campos (ajuste 2: no basta el parecido)

- **P01**: diccionario `CAMPO DE FORMACIÓN ACADÉMICA` ↔ catálogo `Campo de Formación Académica` (difiere en mayúsculas/acentos; normalización registrada en `normalizacion/`) + ejemplo `07` = código `07`.
- **P02–P04**: correspondencia directa de campo; se conservan los dos puntos finales de P02 y la variante "formación académica" de P04. Cada propuesta queda separada por conjunto aunque el archivo sea idéntico.
- **P05**: `Clave`↔`Clave` + detalle "Identifica la clave de una presa junto a su descripción" + ejemplo `LCDSO` = primer código. No se usa el parecido del nombre del recurso ("Catalogo") sino hoja+campo+contenido.
- **P06**: `servic_atencion`↔`servic_atencion` + `Identificadores`/`Detalle` del diccionario + ejemplo `Urgencias médicas` = entrada 1.
- **P07**: `motiv_rech_ricket_sangre`↔igual + ejemplo `3` = entrada 3 (`Días de transito`).
- **P08**: **no literal y justificada**: variable `ricket_especie_rtpcr` ↔ columna `ricket_especie`, puenteada por `Detalle de relación con catálogos = ricket_especie` e `Identificadores = ricket_especie_rtpcr` + ejemplo `1` = `R. Rickettsii`. La diferencia queda registrada en `normalizacion/`; no se homologa.

### Muestra vs revisión completa (ajuste 3)

- Revisión **completa** de los catálogos (pequeños): 10+10+10+10, 10 presas, 7+20+4 — todos con códigos únicos (`catalogos_contenido.json`, verificado por `comprueba.py` contra los `.bin`).
- **Muestra** de datos (primeras filas, `muestras_datos.json`; apoya, no prueba cobertura):
  - 4 educativos (25 filas c/u, archivos 2022): valores `04,06,07,09,10…` dentro de `01–10`.
  - Hídrico 1980–1989 (25 filas): `LCDSO, PECSO, AOBSO, AGZCH, ARCSO, PMOSO, ARLSO, CHTSO, IRASO…` (BICSO no sale en la muestra).
  - Fiebre 2022 (n=50): `servic_atencion` = 1,2,3,5,7 + `0` (nulo documentado); `ricket_especie_rtpcr` = 14 unos + resto 0/vacío; `motiv…` = 45 ceros + 5 vacíos; `des_mpo_res` = texto libre (`HERMOSILLO, PUERTO PEÑASCO, CAJEME…`).

## P09 `des_mpo_res`: sin resolver (ajuste 1)

- Origen comprobado: filas **177 y 178** del diccionario `33d0a99e…` de **Fiebre manchada (Rickettsia)** — ambas con `Catálogo de referencia = des_mpo_res`. No asignar a Vigilancia Epidemiológica.
- Ambas filas se conservan como evidencias distintas (difieren en ejemplo `ide_cp` vs `id_cp` y en huella `4b1762…` vs `b5dbcd…`). Contenido de la fila: `nombrevar=ide_id, desc=ide_col, identificadores=des_jur_res, detalle=cve_loc_res`. Parecen fragmentos de encabezado desalineados al final del CSV (líneas 177–178 de 178).
- Búsqueda de texto completo negativa en el libro `catalogo.xlsx` de Fiebre (3 hojas): sin `des_mpo_res/ide_id/ide_col/des_jur_res/cve_loc_res`.
- La variable homónima `des_mpo_res` de la fila 7 (`Municipio donde reside el caso`, ejemplo `Hermosillo`) tiene catálogo vacío: **no** es el origen de la referencia aunque comparta el nombre. La columna de datos usa texto libre.
- Clasificación: **sin resolver** (documental: celdas que declaran el catálogo; inferencia: sin candidato publicado en el conjunto).

## §8 Referencias territoriales excluidas (8, ya identificadas)

`Municipios/Estados/catalogo_municipios/catalogo_entidades` en Proyecciones (3×2) + Incidencia delictiva (`cat_municipio`) + Víctimas (`cat_entidad`): resoluciones en `data/semantica/cobertura.json > territorio.resoluciones` y `reports/catalogos-territoriales.md`. No se reabren aquí.

## Archivos de esta entrega

- `propuestas.json` — 9 propuestas con referencia original, recurso, evidencia, justificación, alcance, limitaciones y cambios sugeridos; `no_aplicado: true`. Clasificaciones sin cambios (8 `recurso_identificado` + 1 `sin_resolver`).
- `exactos.json` — literales de diccionarios y catálogos leídos de los archivos descargados.
- `manifiesto_descargas.json`, `muestras_datos.json`, `catalogos_contenido.json`, `conjuntos_objetivo.json`, `fase1_refs.json`, `inspecciones_objetivo.txt`, `inspecciones_datos.txt`, `vars_*.txt`, `cola_fiebre.txt` — evidencia y trazabilidad.
- `fuentes/` — 12 archivos publicados + 6 muestras de datos (bytes originales `.bin`).
- `*.py` — scripts de extracción, descarga, inspección, construcción y comprobación (solo stdlib + openpyxl para lectura).

## Reproducción

```powershell
uv run python propuestas/agente-1-catalogos/descargar.py
uv run python propuestas/agente-1-catalogos/extrae_exactos.py
uv run python propuestas/agente-1-catalogos/inspeccionar_catalogos.py
uv run python propuestas/agente-1-catalogos/descargar_muestras.py
uv run python propuestas/agente-1-catalogos/construir_propuestas.py
uv run python propuestas/agente-1-catalogos/comprueba.py
```

`comprueba.py` recalcula los SHA-256 de los 12 `.bin`, verifica hojas, encabezados y entradas completas contra los archivos descargados y exige literales con acentos; no contiene atajos (`or True` eliminado).

## Limitaciones generales

- Vigencia histórica **no comprobada** en ningún caso (metadatos con fechas genéricas `1989-06-04`; catálogos sin versión/año).
- Las muestras no demuestran unicidad, cobertura ni ausencia de códigos contradictorios; la revisión completa cubre los catálogos, no los datos.
- El catálogo hídrico incluye una presa de Chihuahua (`AGZCH`) y hojas `Municipios`/`Regiones` no referenciadas: no es un catálogo exclusivo de Sonora.
- Los 4 `catalogo.xlsx` educativos son byte-idénticos: igualdad registrada por SHA; referencias separadas por conjunto.
- No se modificó nada fuera de esta carpeta; no se aplicó ningún cambio al grafo.
