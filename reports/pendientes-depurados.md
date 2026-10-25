# Pendientes documentales depurados tras R6

**171 registros históricos = 169 significados pendientes reales + 2 encabezados corruptos.**

Se excluyen los encabezados de la vista accionable y se conservan sus celdas, identificadores y procedencia. No se cuentan como significados resueltos ni se cambian los denominadores históricos.

El estado semántico conserva 1392 significados respaldados, 1075 conceptos, 4475 correspondencias revisadas, 20 candidatas y 0 ambiguas.

## Significados pendientes por fuente

| Grupo | Pendientes |
| --- | ---: |
| diversos | 5 |
| epidemiologia | 25 |
| matriculas | 30 |
| salud-defunciones | 32 |
| salud-nacimientos | 53 |
| tic | 24 |

Los 169 registros están enumerados en [el detalle por fuente](../propuestas/depuracion-post-r6/significados/pendientes.md) y en [el JSON consolidado](pendientes-depurados.json). Cada registro conserva el texto original, la evidencia faltante y el criterio de aceptación; sus localizadores cotejados distinguen índice JSON desde cero de fila lógica desde uno.

## Encabezados excluidos de la vista

| Registro | Diccionario / fila lógica | Texto original |
| --- | --- | --- |
| EXC-ENC-177 | 33d0a99e-c721-496f-a05e-07646e9ae42a / 177 | ide_id / ide_col |
| EXC-ENC-178 | 33d0a99e-c721-496f-a05e-07646e9ae42a / 178 | ide_id / ide_col |

[Celdas originales, motivos y huellas de las exclusiones](../propuestas/depuracion-post-r6/encabezados/exclusiones.md). Se requiere aclaración o fe de erratas para corregir el diccionario original.

## Documentos faltantes de catálogos y referencia heredada

Se mantienen 16 brechas de vigencia (V01–V16) y un caso de anomalía de referencia (`des_mpo_res`). Este último remite a las mismas dos filas corruptas: no acredita la existencia de un catálogo ni agrega dos significados pendientes nuevos.

| ID | Conjunto | Documento requerido |
| --- | --- | --- |
| V01 | Promedio Académico | Nota de adopcion UTH de la CMPE 2016 con rango de aplicacion por cuatrimestres/anuales 2022-2026 (oficio, lineamiento o nota de version del conjunto). Pendiente exacto: Acreditar F4: documento del publicador (UTH) que vincule la CMPE 2016 con los periodos 2022 cuatrimestres 1-3, 2023 cuatrimestres 1-3, 2024 cuatrimestres 1-3, 2025 cuatrimestres 1-3, 2026 cuatrimestre 1. |
| V02 | Matriculas | Nota de adopcion UTH de la CMPE 2016 con rango de aplicacion por cuatrimestres/anuales 2022-2026 (oficio, lineamiento o nota de version del conjunto). Pendiente exacto: Acreditar F4: documento del publicador (UTH) que vincule la CMPE 2016 con los periodos 2022 cuatrimestres 1-3, 2023 cuatrimestres 1-3, 2024 cuatrimestres 1-3, 2025 cuatrimestres 1-3, 2026 cuatrimestres 1-2. |
| V03 | Estudiantes Titulados | Nota de adopcion UTH de la CMPE 2016 con rango de aplicacion por cuatrimestres/anuales 2022-2026 (oficio, lineamiento o nota de version del conjunto). Pendiente exacto: Acreditar F4: documento del publicador (UTH) que vincule la CMPE 2016 con los periodos 2022 anual, 2023 anual, 2024 anual, 2025 anual. |
| V04 | Estudiantes egresados | Nota de adopcion UTH de la CMPE 2016 con rango de aplicacion por cuatrimestres/anuales 2022-2026 (oficio, lineamiento o nota de version del conjunto). Pendiente exacto: Acreditar F4: documento del publicador (UTH) que vincule la CMPE 2016 con los periodos 2022 anual, 2023 anual, 2024 anual, 2025 anual. |
| V05 | Recursos Hídricos | Declaracion de edicion/version/fecha del Catalogo_estatal (sha 612b2b11) con rango 1941-2024 + URL de descarga del recurso 1960-1969 (id 4d1bb645, hoy con url vacia en API). Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catálogo_estatal/Clave, sha 612b2b11) y documento que la vincule con 1941-1949, 1950-1959, 1960-1969, 1970-1979, 1980-1989, 1990-1999, 2000-2009, 2010-2019, 2020-2024; constancia del recurso 1960-1969. |
| V06 | Fiebre manchada (Rickettsia) | Declaracion de edicion/version/fecha del catalogo Rickettsia (sha 3b8546ac) con vinculo 2022-2024 + fe de erratas o diccionario corregido y URL del catalogo de des_mpo_res si existe. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo Servicios/servic_atencion, sha 3b8546ac) y documento que la vincule con 2022, 2023, 2024. |
| V07 | Fiebre manchada (Rickettsia) | Declaracion de edicion/version/fecha del catalogo Rickettsia (sha 3b8546ac) con vinculo 2022-2024 + fe de erratas o diccionario corregido y URL del catalogo de des_mpo_res si existe. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo rechazo/motiv_rech_ricket_sangre, sha 3b8546ac) y documento que la vincule con 2022, 2023, 2024. |
| V08 | Fiebre manchada (Rickettsia) | Declaracion de edicion/version/fecha del catalogo Rickettsia (sha 3b8546ac) con vinculo 2022-2024 + fe de erratas o diccionario corregido y URL del catalogo de des_mpo_res si existe. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo especie/ricket_especie, sha 3b8546ac) y documento que la vincule con 2022, 2023, 2024. |
| V09 | Proyecciones de población - Grupos quinquenales de edad | Declaracion de edicion/version/fecha de catalogo.xlsx (sha ea54aad3) con vinculo a reconstruccion 1990-2019 y proyecciones 2020-2040 + aclaracion del desfase de corte vs CONAPO 09-05-2024. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo_Municipios/CLAVE, sha ea54aad3) y documento que la vincule con reconstrucción 1990-2019 y proyecciones 2020-2040; aclarar desfase de corte vs CONAPO 2024. |
| V10 | Proyecciones de población - Grupos quinquenales de edad | Declaracion de edicion/version/fecha de catalogo.xlsx (sha ea54aad3) con vinculo a reconstruccion 1990-2019 y proyecciones 2020-2040 + aclaracion del desfase de corte vs CONAPO 09-05-2024. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo_Estado/CLAVE_ENT, sha ea54aad3) y documento que la vincule con reconstrucción 1990-2019 y proyecciones 2020-2040. |
| V11 | Proyecciones de población - Grandes grupos de edad | Declaracion de edicion/version/fecha de catalogo.xlsx (sha ea54aad3) con vinculo a reconstruccion 1990-2019 y proyecciones 2020-2040 + aclaracion del desfase de corte vs CONAPO 09-05-2024. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo_Municipios/CLAVE, sha ea54aad3) y documento que la vincule con reconstrucción 1990-2019 y proyecciones 2020-2040 (conjunto 943d0723). |
| V12 | Proyecciones de población - Grandes grupos de edad | Declaracion de edicion/version/fecha de catalogo.xlsx (sha ea54aad3) con vinculo a reconstruccion 1990-2019 y proyecciones 2020-2040 + aclaracion del desfase de corte vs CONAPO 09-05-2024. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo_Estado/CLAVE_ENT, sha ea54aad3) y documento que la vincule con reconstrucción 1990-2019 y proyecciones 2020-2040 (conjunto 943d0723). |
| V13 | Incidencia delictiva municipal | Declaracion de edicion/version/fecha y corte SESNSP de cat_municipio (sha 84bb6fcd) y cat_entidad (sha 96776ca8) con vinculo 2015-2025. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha y corte SESNSP del catálogo (cat_municipio/Cve. Municipio, sha 84bb6fcd) y documento que la vincule con 2015-2025. |
| V14 | Víctimas del fuero común en el estado | Declaracion de edicion/version/fecha y corte SESNSP de cat_municipio (sha 84bb6fcd) y cat_entidad (sha 96776ca8) con vinculo 2015-2025. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha y corte SESNSP del catálogo (cat_entidad/Clave_Ent, sha 96776ca8) y documento que la vincule con 2015-2025. |
| V15 | Proyecciones de población - Indicadores demográficos | Declaracion de edicion/version/fecha de catalogo.xlsx (sha ea54aad3) con vinculo a reconstruccion 1990-2019 y proyecciones 2020-2040 + aclaracion del desfase de corte vs CONAPO 09-05-2024. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo_Municipios/CLAVE, sha ea54aad3) y documento que la vincule con 1990-2040 (conjunto 960ef0a9). |
| V16 | Proyecciones de población - Indicadores demográficos | Declaracion de edicion/version/fecha de catalogo.xlsx (sha ea54aad3) con vinculo a reconstruccion 1990-2019 y proyecciones 2020-2040 + aclaracion del desfase de corte vs CONAPO 09-05-2024. Pendiente exacto: Acreditar F3+F4: declaración de edición/versión/fecha del catálogo (Catalogo_Estado/CLAVE_ENT, sha ea54aad3) y documento que la vincule con 1990-2040 (conjunto 960ef0a9). |
| des_mpo_res | Fiebre manchada (Rickettsia) | Fe de erratas o diccionario corregido del publicador que aclare que significan las filas 177/178 (huellas 4b17625c / b5dbcdf5); URL del recurso catalogo SOLO si el publicador confirma que existe un catalogo aplicable a des_mpo_res 2022-2024. Si confirma que no existe, basta la fe de erratas. |

[Matriz completa con evidencia, campos mínimos y criterios de aceptación](../propuestas/depuracion-post-r6/catalogos/brechas.md). Los periodos citados delimitan lo que debe acreditarse; no son vigencias demostradas. La resolución de Presas en R6 acredita el vínculo de columna con la definición /4 y mantiene abierta su vigencia V05.

## Validación y regeneración

- 171 identificadores únicos particionados sin pérdidas ni solapamiento; 171 huellas de filas cotejadas en 17 diccionarios.
- 33 fuentes locales cotejadas por SHA-256 y fuentes históricas de [la orquestación](../propuestas/depuracion-post-r6/orquestacion.json) conservadas.
- Cero definiciones o vigencias nuevas; cero contactos externos; sin cambios de grafo ni del chat.
- La revisión por ID del manual SEED 2022 ya preservado puede continuar como investigación documental; no promueve automáticamente significados.

Regenerar únicamente esta vista:

```powershell
uv run python scripts/depurar_pendientes.py
```
