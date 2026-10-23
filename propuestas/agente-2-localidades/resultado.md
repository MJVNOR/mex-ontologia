# Localidades Sonora — agente-2 (aislado)

Fecha: 2026-10-23. Escritura exclusiva en `propuestas/agente-2-localidades/`. Sin asignar localidades a registros ni confirmar identidades por nombre.

## 1. Corrección de alcance (aprobada)

- El recurso `0c1554d8-…/download/catalogo.xlsx` del conjunto marginación por localidad **sí se examinó**: contiene solo `Catalogo_Estado` (32 entidades) y `Catalogo_Municipios` (2475 municipios nacionales). **No es catálogo de localidades.**
- Lo nuevo es evaluar el **archivo de datos** `8e684391-…/indice-de-marginacion-localidades-2020.xlsx` (hoja `IML_2020`) como **referencia derivada observada** en ese archivo. No se presenta como catálogo oficial completo de localidades de Sonora.
- Se mantienen separados: (a) catálogo publicado, (b) referencia derivada IML_2020, (c) fuente oficial externa INEGI.

## 2. Fuentes examinadas

| # | Fuente | Versión declarada | Fecha consulta (UTC) | Archivo local | SHA-256 | Hoja / fila / celda |
|---|---|---|---|---|---|---|
| 1 | https://datos.sonora.gob.mx/dataset/b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f/resource/8e684391-9137-4359-b654-f19602911421/download/indice-de-marginacion-localidades-2020.xlsx | "2020" en título del recurso `Indice de marginación por localidad 2020` | 2026-10-23T08:58:50 | `fuentes/IML_2020_datos.xlsx` (323808 B, http 200) | `771cc22d44fcba3d70c8762d6c90aebfbe1dd738e5f94cf3119d80d3fc01773e` | `IML_2020`, encabezado fila 1 (`CVE_LOC,ENT,NOM_ENT,MUN,NOM_MUN,LOC,NOM_LOC,…`, 19 cols + 1 vacía); primera fila datos fila 2: A2=`260010001`, B2=`26`, D2=`001`, F2=`0001` |
| 2 | https://datos.sonora.gob.mx/dataset/b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f/resource/251309e5-0309-46ed-9711-77a1dd408eeb/download/diccionario.xlsx | Definiciones "De acuerdo a clasificación de INEGI", ej. `260010001` | 2026-10-23T08:58:49 | `fuentes/diccionario_localidad.xlsx` (10815 B, http 200) | `67eda17676ff37a1fe0d0564ec9ea5b8cdad4de6c0d331a1b6fed4a544c89f3f` | `marginacion_localidades`, encabezado fila 1; fila 2 `CVE_LOC` formato `nnnnnnnnn` ej. `260010001`; filas 3–8 `ENT nn` ej. `26`, `MUN nnn` ej. `001`, `LOC nnnn` ej. `0001` |
| 3 | https://datos.sonora.gob.mx/dataset/b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f/resource/0c1554d8-71e9-46af-87de-55de8ededc88/download/catalogo.xlsx | Recurso nombre "Catalogo" (sin versión) | 2026-10-23T08:58:49 | `fuentes/catalogo_mun_ent_solo.xlsx` (83769 B, http 200) | `ea54aad30b7342ce678d1d66157325a5cbaa492380ee4d807b20918198c5b0f5` | Hojas exhaustivas: `Catalogo_Estado` (33 filas = enc.+32) y `Catalogo_Municipios` (2476 filas = enc.+2475 nacionales). **Ninguna hoja de localidades** (evidencia de ausencia por lista completa de hojas) |
| 4 | https://datos.sonora.gob.mx/dataset/a3320cad-afd3-4840-8c3b-36236df26099/resource/67156807-2013-4117-9ca9-394aea647127/download/diccionario.xlsx (contraste colonias, hoja `marginacion_localidades` fila `CVE_LOC`: formato declarado `nnnn` pero ejemplo `260010001` de 9 dígitos; obligatoriedad "No", nulos "Vacío") | Diccionario colonias | 2026-10-23T08:58:51 | `fuentes/diccionario_colonias.xlsx` (11640 B, http 200) | `ceece0d28e850abff212ee4ff19fa3f26a71e6bef904e934608f26136dd4b936` | Ver `data/portal/contenido-inspeccion.json` recurso `67156807…`: `CVE_LOC`/`NOM_LOC` opcionales; datos `09ef2342…/IMC_2020` hoja `IMC_2020` con `CVE_ENT,NOM_ENT,CVE_MUN,NOM_MUN,CVE_LOC,NOM_LOC` |
| 5 | INEGI Marco Geoestadístico — Catálogo Único: https://www.inegi.org.mx/app/ageeml (consulta), https://www.inegi.org.mx/servicios/catalogounico.html (metadatos y endpoints), ejemplo vivo https://gaia.inegi.org.mx/wscatgeo/v2/localidades/260010001 | Base cartográfica diciembre 2023 (metadatos servicio); registro ej. `periodo: 2015-06-01`, `Fuente_informacion_estadistica: INEGI. Censo de Población y Vivienda, 2020` | 2026-10-23 (web) | Sin archivo local (solo consulta; no se descarga catálogo nacional) | N/A (respuesta JSON puntual, no archivo) | Registro `260010001`: `cve_ent 26, cve_mun 001, cve_loc 0001, nomgeo Aconchi, ambito URBANO, pob_total 1650` |

SHAs 1–3 coinciden con `data/portal/contenido-inspeccion.json` (mismos bytes), lo que confirma identidad con la evidencia previa del portal.

## 3. Referencia candidata: derivada IML_2020 (observada, no oficial)

- **Qué es**: pares código→nombre **extraídos del propio archivo de datos** IML_2020: 1850 filas, `CVE_LOC` únicos 1850/1850, `ENT` solo `26`, 72 pares `ENT|MUN` distintos, 891 `LOC` distintos. Ver `iml2020-verificacion.json` (generado por `analizar_iml.py` en esta carpeta).
- **Qué no es**: no es un catálogo publicado de localidades, no acredita completitud contra INEGI, no sustituye al Marco Geoestadístico.
- **Estructura de claves (comprobada en valores, no solo diccionario)**:
  - `CVE_LOC` (9, TEXTO con ceros: `260010001`) = `ENT` (2, `26`) + `MUN` (3, `001`) + `LOC` (4, `0001`). Composición verificada fila por fila: **1850/1850 OK, 0 fallas** (comparación como cadenas; celdas Excel ya llegan como texto `data_type s`, ej. fila 2: `CVE_LOC '260010001' s`, `MUN '001' s`, `LOC '0001' s`).
  - Códigos originales conservados como cadenas; **ninguna transformación aplicada a la derivada** (el padding 2/3/4/9 del script solo fue método de comprobación, no dato).
  - Unicidad: un `CVE_LOC` → un par `(NOM_MUN, NOM_LOC)` (0 CVE con >1 par de nombres).
  - Homonimia (mismo par municipio+localidad con >1 CVE): 23 pares, ej. `Caborca||La Primavera → 260170320, 260170779`. No se resuelve identidad por nombre.
- **Categorías especiales**: búsqueda específica `LOC ∈ {0000, 9998, 9999}` y `CVE_LOC` terminado en `9999` → **0 casos** en IML_2020. No hay categoría especial documentada en esta fuente. (Nota: el conteo "14 candidatos" de una heurística ingenua por contener `9/99/999` en `iml2020-verificacion.json` se descarta; eran `0009/0099/0999` ordinarios.) No se traslada `26998/26999` municipal ni se inventa equivalencia de localidad.
- **Ceros a la izquierda**: IML_2020 ya los trae (`001`, `0001`, `260010001` como texto). La necesidad de completar ceros aplica a **otras columnas** (Registro Civil ej. `MUN 55`, `LOC 1`), y cualquier `zfill` para esas columnas queda como **transformación propuesta separada**, no observada.

## 4. Fuente oficial externa (separada, solo acreditación)

- INEGI define `cvegeo` localidad = AGEE(2, `01–32`) + AGEM(3, `001–999`) + localidad(4, `0001–9999`), todo **TEXTO**; endpoints `…/wscatgeo/v2/localidades/{cvegeo9}`, `…/localidades/{ent}/{mun}`, equivalencias y `ageeml`.
- Prueba puntual 2026-10-23: `260010001` → Aconchi (`26/001/0001`), `pob_total 1650` — coincide con la fila 2 de IML_2020 en clave, nombre y población. **Un registro consistente no demuestra equivalencia total ni vigencia**: el registro INEGI trae `periodo 2015-06-01` y base dic-2023, mientras IML declara 2020. La cobertura/versión oficial de Sonora exige cotejo contra una edición INEGI con fecha de corte explícita (pendiente del integrador, §8).

## 5. Cobertura y versiones

- Derivada IML_2020: solo `ENT 26` (Sonora), 72 municipios, 1850 localidades, `LOC` distintos 891, sin nulos en `NOM_LOC`, sin categorías especiales observadas. Cobertura = "localidades incluidas en el estudio de marginación 2020 del portal", **no** "todas las localidades de Sonora".
- Catálogo `0c1554d8`: nacional municipal (2475), sin localidades.
- Versiones: portal "2020" (título); diccionario remite a "clasificación de INEGI" sin edición; INEGI vivo con `periodo`/base propios. Sin tabla de equivalencias 2020↔edición INEGI no hay acreditación de vigencia.

## 6. Condiciones de uso

- Uso permitido: evaluar si una columna objetivo **puede** compararse contra la derivada (clave compuesta completa, mismo grano, mismo periodo/ámbito), y detectar inconsistencias de formato.
- Prohibido: asignar localidades a registros, confirmar identidad por coincidencia de nombres, homologar `26998/26999` u otros especiales, completar ceros silenciosamente, o presentar la derivada como catálogo oficial.
- Colonias (`CVE_LOC` opcional, formato declarado `nnnn` vs ejemplo 9 dígitos) no es referencia de localidades; solo sirve como contraste de cómo el portal reutiliza `CVE_LOC`.

## 7. Aplicabilidad a columnas existentes (qué permitiría evaluar, sin asignar)

| Familia | Columnas | Clave disponible | Qué permitiría evaluar con la derivada |
|---|---|---|---|
| Marginación localidades (referencia, no objetivo) | `CVE_LOC,ENT,MUN,LOC,NOM_*` (IML_2020) | Compuesta completa 9=2+3+4 como texto | Definir la derivada misma |
| Marginación colonias | `CVE_ENT,CVE_MUN,CVE_LOC,NOM_*` (`09ef2342…/IMC_2020`) | Compuesta presente pero localidad opcional/nulleable | Solo filas con `CVE_LOC` de 9 completo; documentar formato `nnnn` vs ej. 9 dígitos antes de comparar |
| Registro Civil (residencia, defunción, ocurrencia, parto, certifica) | `ENTIDAD*,MUNICIPIO*,LOCALIDAD*` + `*D` nombres (diccs. defunciones/nacimientos/divorcios; ej. `LOCALIDADRESIDENCIA` numérico ej. `1`, `MUNICIPIO…` ej. `55`, `Catálogo de referencia: ""`) | Clave simple sin ceros, sin catálogo declarado | Solo evaluable si se propone transformación explícita `zfill(2/3/4)` + `ENT+MUN+LOC` por papel (residencia≠defunción≠ocurrencia…); la transformación debe versionarse por fuente, no global |
| Delitos / seguridad | `LOCALIDAD`, `LOCALIDAD DEL DELITO` (texto) | Solo nombre | No evaluable contra claves; como máximo detección de homonimia (23 pares en la derivada advierten del riesgo) |
| SEMujeres atenciones | `MUNICIPIO,LOCALIDAD` (texto) + `TIPO DE ATENCIÓN,TOTAL,SEXO` | Solo nombres | No evaluable contra claves |
| `loc_name` / `colonia` (1 recurso c/u en inventario) | Nombres | Solo nombre | No evaluable contra claves |

Papeles territoriales no se mezclan: residencia, defunción, ocurrencia, parto y certifica son variables locales distintas aunque compartan "localidad".

## 8. Pendientes y cambios sugeridos para el integrador

1. **No crear `owl:sameAs`/`skos:exactMatch`** desde la derivada; como máximo correspondencias calificadas `codigo_y_nombre_exactos_en_derivada_IML_2020` con huella `771cc22d…`, hoja/fila y códigos originales.
2. Para acreditar cobertura/versión: descargar **Catálogo Único INEGI con fecha de corte 2020** (o tabla de equivalencias del periodo) para Sonora y cotejar los 1850 `CVE_LOC` (conteo, faltantes/sobrantes, cambios de nombre, `estatus/periodo`). Un registro puntual no basta.
3. Si se quiere evaluar Registro Civil: proponer regla de normalización **por conjunto y papel** (`str(int(v)).zfill(n)` solo si `v` es dígito; nulos/inválidos a categoría pendiente, nunca a `9999`), con auditoría de cuántos registros quedan incomparables por falta de `ENT/MUN`.
4. Documentar la columna fantasma 20 (`'None'`) de IML_2020 como artefacto vacío, y la contradicción formato-vs-ejemplo de `CVE_LOC` en el diccionario de colonias, sin corregir los originales.
5. **Pendiente declarado (no sustituido)**: no existe catálogo oficial completo de localidades dentro del portal; la derivada IML_2020 es observada y parcial; la equivalencia con una edición INEGI concreta sigue sin acreditar.
