# A1-911 v002 — Llamadas Improcedentes <> Procedentes 911: BLOQUEADO

Par `19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92`.

Pregunta: ¿Se pueden comparar los volumenes clasificados como procedentes e improcedentes por municipio y mes? Solo calcular una proporcion si consta que las categorias forman una particion del mismo universo.

Resultado: **bloqueado**. No se calculo proporcion ni se ejecuto join. Todo lo
de abajo lo produce `scripts/comprobar_a1_911.py` leyendo las fuentes locales.

## Ficha de ocho comprobaciones

| Eje | Estado | Evidencia |
| --- | --- | --- |
| claves | no_acreditada | Ninguno de los 6 recursos declara columna identificadora: las 7 variables del diccionario 1a95d734 (sha fcd73b159fdf, identico en ambos conjuntos) no aportan identificador (6 con 'Identificadores' vacio y 'hora' solo con texto residual). 6 de 6 esquemas usan metodo_encabezado=heuristica_requiere_revision. El cruce R9 exige clave compuesta entidad+municipio y entidad+municipio+localidad. |
| grano | fila_evento_llamada_sin_agregacion_validada | Los cuatro XLSX tienen grano de llamada individual (FECHA/HORA + atributos), sin columnas de total ni de resumen. El lote de cruces rechaza ejecutar por falta de estrategia de agregacion: Sin estrategia automática de agregación validada para las medidas y el grano de estos recursos. |
| unicidad | no_acreditada | Solo hay diagnosticos de muestra n=29 con alcance literal 'no demuestra unicidad ni cobertura integral'. Repeticiones en la muestra: MUNICIPIO 20/29 (Q1) y 20/29 (Q2); LOCALIDAD 18/29 y 10/29; COLONIA 1/29 y 4/29. Una muestra no acredita unicidad del recurso completo. |
| cardinalidad | no_acreditada | Sin clave primaria declarada no hay cardinalidad 1:1 ni N:M demostrable. El lote queda en 'requiere_revision' con ejecuciones=[] y pendiente 'comprobar_cardinalidad_y_evitar_multiplicacion_de_filas'. Ademas el recurso etiquetado como improcedentes Q1 comparte SHA con procedentes Q1, de modo que una union ingenua duplicaria filas y ningun total es fiable. |
| poblacion | sin_particion_acreditada | Procedentes e improcedentes viven en conjuntos separados y ningun recurso del par es un documento de particion: los 6 son XLSX/CSV de datos o diccionario, sin descripcion, y no aportan total del universo. El recurso de improcedentes Q1 (54285a13) contiene en realidad la hoja LLAMADAS PROCEDENTES 911 con sha 9d710cb868c3, identico a procedentes Q1 (6ce17dd1). Sin particion declarada no se calcula proporcion. |
| periodo | nominal_2026_sin_verificar_contenido | Trimestres solo en nombres/URL: Q1 y Q2 de 2026 en los cuatro XLSX; el cruce solo coincide en el anio y 'solo en nombres'. Las muestras n=29 pidieron ['COLONIA', 'LOCALIDAD', 'MUNICIPIO'] y no FECHA, asi que no hay ningun valor de fecha leido localmente. Un recurso de improcedentes Q1 no existe: ese lugar lo ocupa el duplicado de procedentes Q1. |
| unidades | conteo_de_llamadas_sin_unidad_fisica | Las 7 variables del diccionario tienen 'Unidad de medida' vacia. La medida implicita es conteo de filas (llamadas), no una magnitud con unidad; no hay termino QUDT aplicable ni peticion a W que hacer por este par. |
| cobertura_datos | parcial_y_asimetrica | Improcedentes reales: solo Q2 (0df8592f, 3 columnas FECHA/HORA/MOTIVO, sin MUNICIPIO). Procedentes: Q1 (6ce17dd1) y Q2 (943e2919), 7 columnas. El Q1 de improcedentes es un duplicado byte a byte de procedentes Q1. No hay conteos de filas: solo bytes leidos. Las dos muestras n=29 son de archivos procedentes (incluido el duplicado); no hay muestra de 0df8592f. |

## Hallazgos verificados

- **Duplicado entre conjuntos.** `54285a13-3a2a-4e47-b0af-e855861f5347` (conjunto A) es byte a byte
  `6ce17dd1-5716-44e9-bc5f-603c0925afe6` (conjunto B): sha `9d710cb868c3fb6304a4310259bf4c7e64d2af7cdc15cd253bdc8dd86c9c2109`, 8955252 bytes, hoja
  `LLAMADAS PROCEDENTES 911`. El "Q1 de improcedentes" del conjunto A es en
  realidad procedentes Q1; su URL tambien apunta al archivo de procedentes.
- **Diccionarios identicos** (`fcd73b159fdf46ce33a5d9c43f227b7a7b5e296cb197399a8eac6c6be57c5140`): 7 variables, `Unidad de medida` vacia en todas,
  sin identificador declarado (6 con `Identificadores` vacio; `hora` solo con texto residual),
  sin variable `motivo no procedente` (columna de improcedentes Q2 sin definicion).
- **Q2 improcedentes sin MUNICIPIO.** `0df8592f-bb3d-466c-aec3-6cbc91253be0` tiene solo
  FECHA, HORA, MOTIVO NO PROCEDENTE; no admite corte por municipio.
- **La muestra A del lote sale del duplicado.** `54285a13-3a2a-4e47-b0af-e855861f5347` vs `943e2919-6a8b-4776-ac4f-c3d6b02bb94e`:
  la comparacion muestral es procedentes Q1 contra procedentes Q2; no hay ninguna
  observacion de improcedentes.
- **Familias territoriales solo por el duplicado.** En el cruce, municipio, localidad y
  division territorial enlazan unicamente columnas de `54285a13-3a2a-4e47-b0af-e855861f5347`. Al excluir el
  duplicado, la unica familia compartida real es periodo (FECHA), con valores sin verificar.
- **Coincidencias muestrales de MUNICIPIO: 6** en n=29
  (CAJEME, GUAYMAS, HERMOSILLO, NOGALES, PUERTO PEÑASCO, SAN LUIS RIO COLORADO). El lote las califica:
  "Coincidencia textual muestral, sin equivalencia ni cobertura demostradas".
- **Sin particion del universo.** Ningun recurso del par declara total ni particion; los 6
  son XLSX/CSV de datos o diccionario, sin descripcion documental.
- **Sin copias locales de filas 911:** 0 archivos xlsx/xls/csv. Solo bytes y SHA de
  inspeccion, por lo que no hay numeradores ni denominadores.

## Comprobaciones

| Comprobacion | Estado | Detalle |
| --- | --- | --- |
| recursos_del_par | ok | 6 recursos en inventario (3 por conjunto): ['0df8592f-bb3d-466c-aec3-6cbc91253be0', '1a95d734-2f0e-4781-8831-77dcfcbe70f8', '54285a13-3a2a-4e47-b0af-e855861f5347', '6ce17dd1-5716-44e9-bc5f-603c0925afe6', '7922b8c8-db09-4172-ad7f-31b0ba0c68e3', '943e2919-6a8b-4776-ac4f-c3d6b02bb94e'] |
| duplicado_entre_conjuntos | ok | 54285a13-3a2a-4e47-b0af-e855861f5347 (conjunto A) == 6ce17dd1-5716-44e9-bc5f-603c0925afe6 (conjunto B), sha 9d710cb868c3fb6304a4310259bf4c7e64d2af7cdc15cd253bdc8dd86c9c2109, bytes 8955252, hoja LLAMADAS PROCEDENTES 911 |
| duplicado_no_se_repite_en_corpus | ok | el sha aparece exactamente en 2 inspecciones: ['54285a13-3a2a-4e47-b0af-e855861f5347', '6ce17dd1-5716-44e9-bc5f-603c0925afe6'] |
| diccionarios_identicos | ok | diccionarios de A y B con sha fcd73b159fdf46ce33a5d9c43f227b7a7b5e296cb197399a8eac6c6be57c5140; 7 variables; unidades vacias; sin variable 'motivo no procedente' |
| columnas_sin_diccionario | no_acreditado | columnas de improcedentes Q2 sin definicion en el diccionario: ['motivo no procedente'] |
| q2_improcedentes_sin_municipio | ok | 0df8592f solo tiene FECHA, HORA y MOTIVO NO PROCEDENTE; no permite corte por municipio |
| improcedentes_reales_solo_q2 | ok | unico XLSX con hoja de improcedentes: ['0df8592f-bb3d-466c-aec3-6cbc91253be0']; el Q1 del conjunto A es el duplicado de procedentes |
| muestra_a_desde_duplicado | ok | la muestra A del lote se tomo de 54285a13-3a2a-4e47-b0af-e855861f5347 (procedentes Q1), no de 0df8592f; la comparacion muestral es procedentes Q1 vs procedentes Q2 |
| familias_territoriales_solo_por_duplicado | ok | en el cruce, municipio/localidad/division_territorial_declarada solo enlazan columnas de 54285a13-3a2a-4e47-b0af-e855861f5347; sin el duplicado no hay familia territorial compartida |
| periodo_compartido_real | ok | FECHA existe en 0df8592f y en los procedentes; el periodo es la unica familia compartida con columna propia de improcedentes |
| coincidencias_municipio_muestrales | no_acreditado | 6 coincidencias textuales en muestra n=29 (CAJEME, GUAYMAS, HERMOSILLO, NOGALES, PUERTO PEÑASCO, SAN LUIS RIO COLORADO); interpretacion del lote: Coincidencia textual muestral, sin equivalencia ni cobertura demostradas |
| particion_no_declarada | bloqueado | ningun recurso del par declara particion del universo ni total; descripcion nula en los 6 |
| proporcion | bloqueado | no calculada: falta particion acreditada y, para improcedentes, falta MUNICIPIO |
| join | bloqueado | no ejecutado: lote requiere_revision, ejecuciones vacias, sin grano/clave/cardinalidad validados |
| filas_locales | no_acreditado | 0 copias locales de filas 911 (xlsx/xls/csv); solo bytes y SHA de inspeccion |
| concepto_municipio_improcedentes | no_acreditado | vinculos semanticos de MUNICIPIO solo en ['54285a13-3a2a-4e47-b0af-e855861f5347', '6ce17dd1-5716-44e9-bc5f-603c0925afe6', '943e2919-6a8b-4776-ac4f-c3d6b02bb94e']; 0df8592f no tiene |
| conflicto_semantico_duplicado | ok | el vinculo HORA de 54285a13-3a2a-4e47-b0af-e855861f5347 usa concepto 'hora-ingreso-llamada-911-improcedente' aunque el archivo es procedentes: la etiqueta improcedente del conjunto se propago al contenido |
| motivo_sin_definicion | no_acreditado | MOTIVO NO PROCEDENTE figura como 'sin_definicion_coincidente' en pendientes semanticos |

## Verificacion reproducible

```
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/comprobar_a1_911.py
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/tests/test_a1_911.py
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/sellar.py
```

Sin marcas de tiempo en la salida: dos ejecuciones producen bytes identicos.
`tests/test_a1_911.py` lo comprueba y ademas coteja los ficheros entregados con
la salida del script y el sello.

## Fuentes (SHA calculado al ejecutar)

| Fuente | sha256 | bytes |
| --- | --- | --- |
| data/portal/inventario.json | 783f12559b81e3c624e601c48d22733158135aa4229aad0feaea712824922faf | 716122 |
| data/portal/contenido-inspeccion.json | 61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb | 2652648 |
| data/portal/oportunidades-cruce.json | 40f107d5cf9c11ce937073ac2f7b5b0e3c9db8c342f7414cecb0f0744e0d0c14 | 9645149 |
| data/portal/lote-cruces/validacion-lote.json | 9031b875b1bf7873722f74847abbbce9b87201415f43788f60be1a75b50ede19 | 1478239 |
| ontologia/semantica.json | dba467b63286171bb68f5b1400a1ed51bfb99d5663e5b34a36f31fb94953cebd | 6961897 |
| reports/pendientes-semanticos.json | 42068c71f0d1578bcf4d8fe5b987d99bb90ec586eeab6bb1418b6a8918fb9adb | 4807159 |
| docs/plan-paralelo-ampliacion-post-r9.md | f43214a0d38ff2cb1fcdfb213d9aa0fba67415dc21b2033ac305a3a70eda0ce8 | 5672 |
| data/portal/inspecciones/0df8592f-bb3d-466c-aec3-6cbc91253be0.json | cf02b4e7f50db6563d3a6e0b4f5152140f2450db88fb6aa3673f1fa8f945e2a6 | 1195 |
| data/portal/inspecciones/54285a13-3a2a-4e47-b0af-e855861f5347.json | 65c2a3091926e0c4114b1293b7c6b1f6685924153e2f5c33322829b45c8379a9 | 1533 |
| data/portal/inspecciones/1a95d734-2f0e-4781-8831-77dcfcbe70f8.json | 029123d21949d8047dcd8600ca58caa444ad5daadcb777adc9f4fefefb3c3fc6 | 5127 |
| data/portal/inspecciones/6ce17dd1-5716-44e9-bc5f-603c0925afe6.json | 369fe04b9c08dbc9a478e0a6bb2c82d762b15f34f08490f2142aea907386166b | 1533 |
| data/portal/inspecciones/943e2919-6a8b-4776-ac4f-c3d6b02bb94e.json | a83567b73ce4eaf4e7e64264d9218ef963e49b2283995ae5e3057fd67c4af745 | 1536 |
| data/portal/inspecciones/7922b8c8-db09-4172-ad7f-31b0ba0c68e3.json | 8b78d45362080888ee3864d6c3d17a6468b39448fc18e41a58a5d1089e19d468 | 5127 |

## Reapertura

- Fe de erratas o diccionario del publicador que declare la particion procedentes/improcedentes del mismo universo con su total.
- Correccion del recurso 54285a13 (hoy duplicado de procedentes Q1) o sustituto real de improcedentes Q1.
- Esquema con MUNICIPIO para improcedentes Q2 (0df8592f) y catalogo de municipios con unicidad.
- Copias locales de filas para verificar periodo, conteos por municipio y mes, y unicidad.

## Limites

- No se calculo ninguna proporcion ni tasa; no se ejecuto join.
- No se infiere unicidad ni cardinalidad del universo a partir de muestras n=29.
- Las coincidencias textuales de MUNICIPIO en la muestra no acreditan equivalencia entre conjuntos.
- El duplicado Q1 se reporta como hallazgo; no se usa para agregar ni para sumar universos.
- No se toco v001, el grafo, la configuracion IRI ni Studio.
