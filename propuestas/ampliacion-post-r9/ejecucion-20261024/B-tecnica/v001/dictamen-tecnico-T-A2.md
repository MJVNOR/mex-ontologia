# Dictamen tecnico independiente T-top50 v001 y A2-registro-civil v001

Rol B-tecnica v001 - 2026-10-24T20:29:06+00:00.

Metodo: recomputo propio desde fuentes, verificacion de sellos, reproduccion en sandbox temporal con rutas redirigidas, ejecucion de pruebas selladas y comprobacion de no-escritura; solo stdlib.

Resumen: **53 PASS / 3 OBS / 0 FAIL**.

## Dictamen

| Carril | Veredicto | Base de la decision |
| --- | --- | --- |
| T-top50 | **ACEPTADO_CON_OBSERVACIONES** | 1191 scores recomputados; top50 = prefijo exacto del orden (-score, id); mapa 3916/1191 inmutable; MD/HTML coinciden fila a fila con el JSON |
| A2-registro-civil | **ACEPTADO_CON_OBSERVACIONES** | BLOQUEADO con 8 ejes; evidencia cruzada contra fuentes locales; muestra n=100 declarada como no universal; sin volumen ni join |

## Sellos auditados (SHA256 por archivo)

### T-top50/v001

Digest del manifiesto: `f52fce533bbf8a593b2b4853ee99334cde4e5593146e93c12853be6737a4f826`

| Archivo | SHA256 | Bytes |
| --- | --- | --- |
| `congelada.json` | `1ad806bcc41b014817d10f9e56467927c213de61d155913ccc3e90e4c658e116` | 1678 |
| `entrega.json` | `a8e88771cb796388b43199c82421ab986658473bbab7a251ba992100c0514230` | 6170 |
| `entrega.md` | `a5459e0f7630cf02eadc625b82f64846f38b869a59cfcac7a4c43fb2fc32592f` | 2328 |
| `scripts/reproducir_top50_r9.py` | `1a88b779b3ad5253ab3423c094226e369e21ac057fd3f29ca95e4d60b37102b2` | 7846 |
| `tests/test_top50_r9.py` | `b7be5301aa52d732de498a286a5bc1a22d71c2a975b4901766b6c45ef34a818a` | 3395 |
| `top50-oportunidades-r9.json` | `a8a2134b5d3de4f63b61802e7c54ae9c3cc175dc0ecb548cc1e5a99bc118f375` | 60154 |
| `top50-oportunidades-r9.md` | `22d9504bec57fe8f7d03eb3a7990f55f3ed064ec47eae32f1e2d0c1fc6b847d0` | 31005 |
| `vista-top50-r9.html` | `6e954950c4f271085e8d35bac1a7a9c324aa32ea3709da2e22b73bec69502287` | 35024 |

### A2-registro-civil/v001

Digest del manifiesto: `2c331abc9ce786bc506d41426bf489fb252e4bd413addd61e5e025c22dcc08a3`

| Archivo | SHA256 | Bytes |
| --- | --- | --- |
| `A2-pregunta-ficha.md` | `0ae5190cb341512f8a14b6d663e2e69219dc1fc83ed38a0d41655141765cae81` | 2288 |
| `congelada.json` | `25d899977ffe0a7b0c1173ff1b08264ad033ada777544c3453a35b79b5b3cce7` | 601 |
| `congelada.sha256` | `a45bb8049e70fe105bb96075e8c2d4c5dcad428725389287c87390bd19c75960` | 82 |
| `resultados.json` | `b724656745008ee8612c2e60e3ab0e79fa3764a586110414d038a7fda9df6e52` | 4640 |
| `resultados.md` | `7c8ac97f756e8347c4b234e4a1484f7f80d8a9cf8ffb8abba2ddc7e2e30b3d96` | 1002 |
| `scripts/analizar.py` | `53d60a063a6ea468a971b07fb14a5be04fcdbec0238df6e6be120939e530bd35` | 7315 |
| `tests/test_bloqueo.py` | `97ba05fcfeadd0526855dc99b1702a6bdb10cf9f276fa3a535b4b84dc38c8795` | 1256 |

## Fuentes clave verificadas

| Fuente | SHA256 |
| --- | --- |
| `data/portal/oportunidades-cruce.json` | `40f107d5cf9c11ce937073ac2f7b5b0e3c9db8c342f7414cecb0f0744e0d0c14` |
| `propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/criterio.json` | `2296486dc646b7b2fce1e5fafe56e81e34a290bbd341a771b9404d5583111306` |
| `propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/prioridades_top50.csv` | `db1182cda8be4686b4335ed443f3bf22480f04dccaa62f9b71358994c5d6174a` |
| `propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/matriz_pares_relevantes.csv` | `2f5fec408edf6dd216f93abcdd962f4163e4b7e070761f7ea57dd5dc5203db58` |
| `reports/cobertura-operativa-r9.json` | `fd64a9aeb622255f98c3bdcd2ebf311757113982ac9ff62770615a73a4175ab8` |
| `data/portal/lote-cruces/validacion-lote.json` | `9031b875b1bf7873722f74847abbbce9b87201415f43788f60be1a75b50ede19` |
| `data/portal/contenido-inspeccion.json` | `61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb` |
| `reports/catalogo-perfil.json` | `aae23b2eb8f8e37cbee18d86c0cac7c73f0899f02fbd417bc90d01a8fd54fc43` |
| `config.toml` | `0fa293d24094e70d81be6df257c4081627e1d571f9fc44dabb5e7bd21b1ff0c4` |

## Comprobaciones

| ID | Carril | Comprobacion | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| T-SELLO-1 | T | congelada.json v001: 7 archivos con SHA256 y bytes exactos | PASS | malos=[]; n=7 |
| T-SELLO-2 | T | congelada cubre todos los archivos de v001 salvo si misma | PASS | sin_cubrir=[]; cubiertos=7 |
| A2-SELLO-1 | A2 | congelada.json: 5 entregables con SHA256 exactos | PASS | malos=[]; n=5 |
| A2-SELLO-2 | A2 | sidecar congelada.sha256 sella congelada.json (sin autohash) | PASS | '25d899977ffe0a7b0c1173ff1b08264ad033ada777544c3453a35b79b5b3cce7  congelada.json' |
| A2-SELLO-3 | A2 | congelada cubre todos los archivos de v001 salvo sellos | PASS | sin_cubrir=[] |
| T-01 | T | Mapa: 3916 pares y 1191 candidatas_por_validar | PASS | pares=3916; candidatas=1191; estados={'sin_clave_detectada': 2328, 'candidata_por_validar': 1191, 'solo_dimensiones_amplias_o_tiempo': 396, 'exploratorio_ejecutado': 1} |
| T-02 | T | 1191 ids de candidata unicos | PASS |  |
| T-03 | T | 1191/1191 scores de matriz recomputados iguales (formula del criterio) | PASS | filas=1191; discrepancias=0 |
| T-04 | T | Matriz y mapa cubren el mismo conjunto de 1191 candidatas | PASS | mat=1191; mapa=1191 |
| T-05 | T | Orden completo de 1191 respeta (-score, id) | PASS | matriz ya ordenada como el recomputo |
| T-06 | T | Top50 = prefijo exacto del orden recomputado (50/50 ids en orden) | PASS | top=50 |
| T-07 | T | Rangos 1..50 unicos y en orden | PASS |  |
| T-08 | T | 50/50 scores del CSV iguales al recomputo | PASS |  |
| T-09 | T | Top50: 50 ids unicos; max 5.0 y min 1.0 como declara la entrega | PASS | max=5.0; min=1.0 |
| T-10 | T | Staging JSON: 50 filas coherentes con el mapa original (titulos, familias, bloqueadores, conjuntos) | PASS | filas=50 |
| T-11 | T | Todas las filas NO_JOIN_APROBADO; carril analitico solo en los 3 pares A1-A3 | PASS |  |
| T-12 | T | A1/A2/A3 por ID exacto, rangos 2/4/1 y scores 3.0/3.0/5.0 | PASS |  |
| T-13 | T | MD: 50 filas, en el mismo orden y con los mismos campos que el JSON | PASS | filas_md=50 |
| T-14 | T | HTML: 50 filas, mismo orden/campos/estado que el JSON (sin contradiccion) | PASS | filas_html=50 |
| T-15 | T | Cabeceras MD/HTML y meta del staging coinciden con mapa y cobertura R9 | PASS |  |
| T-16 | T | entrega.json: las 6 fuentes de datos/criterio con SHA256 exactos | PASS | n_fuentes=7; discrepancias_datos=[] |
| T-16b | T | Fuente documental del plan: el SHA citado ya no coincide con el archivo actual | OBS | deriva=[('docs/plan-paralelo-ampliacion-post-r9.md', '807a05e4473597ced2e1d708fb2069884d9a669cc0ec823d6a1aca316a680e9c', 'f43214a0d38ff2cb1fcdfb213d9aa0fba67415dc21b2033ac305a3a70eda0ce8')]; el plan citado se actualizo despues del sello (nota de continuidad DeepSeek); no afecta mapa, criterio, CSVs, cobertura ni seguimiento. Corregir con nota/delta en v002. |
| T-17 | T | Meta del staging sella mapa, criterio y cobertura con los SHA reales | PASS | mapa=40f107d5cf9c11ce937073ac2f7b5b0e3c9db8c342f7414cecb0f0744e0d0c14 |
| T-18 | T | Cifras de cobertura R9 declaradas (1423/1106/138/16/17) iguales a la fuente | PASS | significados=1423; conceptos=1106; vigencias=16; candidatas=17 |
| T-19 | T | Mapa original inmutable: SHA declarado, git limpio, mtime previo a base.json | PASS | sha=40f107d5cf9c11ce937073ac2f7b5b0e3c9db8c342f7414cecb0f0744e0d0c14; git=''; mtime=2026-10-23T06:47:52.640943+00:00; generado_interno=2026-10-23T06:47:52.505004+00:00; base=2026-10-24T20:08:00.503830+00:00 |
| T-20 | T | Sin join automatico: ningun JOIN_APROBADO ni campo join en T | PASS |  |
| T-21 | T | Reproductor real: solo stdlib, sin red y escribe unicamente dentro de V001 | PASS | imports=['csv', 'hashlib', 'html', 'json', 'pathlib']; escrituras=['(V001 / "top50-oportunidades-r9.json").write_text(', '(V001 / "top50-oportunidades-r9.md").write_text("\\n".jo', '(V001 / "vista-top50-r9.html").write_text(', '(V001 / "congelada.json").write_text('] |
| T-22 | T | Ninguna salida de T/A2 invoca Gemma ni contactos a publicadores | PASS |  |
| A2-01 | A2 | Par correcto, 8 ejes del plan, veredicto BLOQUEADO sin volumen ni join | PASS | ejes=['claves', 'grano', 'unicidad', 'cardinalidad', 'poblacion', 'periodo_ambito', 'unidades', 'cobertura']; causas=5 |
| A2-02 | A2 | Eje claves: par candidata_por_validar, familia municipio y pendientes de catalogo | PASS | estado=candidata_por_validar |
| A2-03 | A2 | Eje grano: variables citadas = diccionarios locales; evento vs agregado | PASS |  |
| A2-04 | A2 | Eje unicidad: limites de muestra declarados (n=100, sin universalidad) | PASS | limites=[100, 100]; alcance_verbatim_ok=True |
| A2-05 | A2 | Eje cardinalidad: 6 pruebas, 5 fallos total!=hombres+mujeres y 1 de meses faltantes | PASS | pruebas=6; total!=suma=5; meses=1 |
| A2-06 | A2 | Eje poblacion: actos con 2 contrayentes vs conteos agregados; sin id de persona | PASS |  |
| A2-07 | A2 | Eje periodo/ambito: interseccion real 2015-2024, solo registro, sin residencia | PASS | anios_mat=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]; anios_nac=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]; interseccion=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024] |
| A2-08 | A2 | Eje unidades: fila-evento vs fila-agregado; pendiente de homologacion citado | PASS |  |
| A2-09 | A2 | Eje cobertura: ausencia != cero y muestras de recursos/anios distintos | PASS | total_declarado={'Matrimonios 2023': 14685, 'Nacimientos 2024': 627} |
| A2-10 | A2 | Muestra != universo: la entrega no presenta la muestra como cobertura completa | PASS |  |
| A2-11 | A2 | Cita textual de unicidad: la fuente dice 'Diagnostico' con acento | OBS | La fuente dice 'Diagnóstico de muestra; ...'; resultados.json cita 'Diagnostico de muestra; ...' (sin tilde). El sentido se mantiene; la cita no es literal. |
| A2-12 | A2 | Cita de periodo: 'Anio-Mes de registro' no existe como variable unica | OBS | Los diccionarios tienen variables separadas 'Año de registro' y 'Mes de registro' (mas 'Dia de registro' en Matrimonios); la evidencia las parafrasea como 'Anio-Mes de registro'. No altera el veredicto. |
| A2-13 | A2 | Fuentes locales declaradas: conteos y SHA de diccionarios reales | PASS |  |
| A2-14 | A2 | Script reproducible real: solo stdlib, sin red y escribe unicamente en OUT | PASS | imports=['hashlib', 'json', 'pathlib']; escrituras=['with open(OUT / "resultados.json", "w", encoding="utf-8") as', 'with open(OUT / "congelada.json", "w", encoding="utf-8") as ', 'with open(OUT / "congelada.sha256", "w", encoding="utf-8") a'] |
| T-REPRO-1 | T | El reproductor sellado corre en staging simulado (asserts internos incluidos) | PASS | rc=0; stdout='OK 3916/1191/50 verificados; A1-A3 en top50; R9 cobertura_operativa_validada_sin_cambios_al_grafo; 4 archivos congelados' |
| T-REPRO-2 | T | Salidas regeneradas byte-identicas a las selladas (3/3) | PASS | iguales=['top50-oportunidades-r9.json', 'top50-oportunidades-r9.md', 'vista-top50-r9.html']; distintas=[] |
| A2-REPRO-1 | A2 | El analisis sellado corre en sandbox y concluye BLOQUEADO | PASS | rc=0; stdout='BLOQUEADO: grano distinto (evento vs agregado) impide join fila a fila; unicidad/cardinalidad no acreditadas: muestras n=100 declaran no demostrar unicidad ni cobertura; inconsistencia interna en Naci' |
| A2-REPRO-2 | A2 | resultados.json regenerado byte-identico al sellado | PASS | sha_sandbox=b724656745008ee8612c2e60e3ab0e79fa3764a586110414d038a7fda9df6e52 |
| A2-REPRO-3 | A2 | cadena de sello regenerada: 4/5 hashes iguales (script redirigido) y sidecar valido | PASS | El unico hash distinto es scripts/analizar.py, cuya copia solo cambia las 2 lineas de ruta (REPO/OUT) para escribir en el sandbox; el resto reproduce byte a byte. |
| T-TEST | T | Pruebas selladas T ejecutadas y en verde | PASS | rc=0; '.....\n----------------------------------------------------------------------\nRan 5 tests in 0.092s\n\nOK' |
| A2-TEST | A2 | Pruebas selladas A2 ejecutadas y en verde | PASS | rc=0; '..\n----------------------------------------------------------------------\nRan 2 tests in 0.001s\n\nOK' |
| X-01 | X | Base congelada intacta: 130/130 archivos de base.json con SHA exacto | PASS | n=130; malos=[] |
| X-02 | X | IRI fuera de alcance: config.toml con SHA declarado y sin cambios | PASS | sha=0fa293d24094e70d81be6df257c4081627e1d571f9fc44dabb5e7bd21b1ff0c4; base_iri=https://example.org/mex-ontologi/ |
| X-03 | X | Sin escrituras en T/A2 durante la auditoria (manifiestos identicos) | PASS |  |
| X-04 | X | La auditoria no modifica ningun archivo rastreado (git: modificaciones estables) | PASS | modificados_antes=33; ahora=33 |
| X-04b | X | Altas nuevas en el arbol corresponden a carriles concurrentes, no a B-tecnica | PASS | altas_durante_auditoria=0 fuera_de_B-tecnica; ejemplo=[]; otros carriles escriben v002 en paralelo |
| X-05 | X | Ningun carril produce RDF/TTL ni toca el grafo o Studio | PASS |  |
| X-06 | X | Manifiestos R1-R9 intactos y con SHA exacto | PASS | R1-R9=9 intactos; manifiestos adicionales intactos=6 |

## Reproduccion (comandos y resultado)

- `T-reproducir` rc=0 (cwd `C:\Users\marti\Documents\MEX-Ontologi\propuestas\ampliacion-post-r9\ejecucion-20261024\B-tecnica\v001\_sim\T-top50`): `C:\Users\marti\Documents\MEX-Ontologi\propuestas\ampliacion-post-r9\ejecucion-20261024\B-tecnica\v001\_sim\T-top50\v001\scripts\reproducir_top50_r9.py`
- `A2-analizar` rc=0 (cwd `C:\Users\marti\AppData\Local\Temp\b-tecnica-a2-vbd8zkoh`): `C:\Users\marti\AppData\Local\Temp\b-tecnica-a2-vbd8zkoh\v001\scripts\analizar.py`
- `T-tests` rc=0 (cwd `C:\Users\marti\Documents\MEX-Ontologi\propuestas\ampliacion-post-r9\ejecucion-20261024\T-top50\v001`): `C:\Users\marti\Documents\MEX-Ontologi\propuestas\ampliacion-post-r9\ejecucion-20261024\T-top50\v001\tests\test_top50_r9.py`
- `A2-tests` rc=0 (cwd `C:\Users\marti\Documents\MEX-Ontologi\propuestas\ampliacion-post-r9\ejecucion-20261024\A2-registro-civil\v001`): `C:\Users\marti\Documents\MEX-Ontologi\propuestas\ampliacion-post-r9\ejecucion-20261024\A2-registro-civil\v001\tests\test_bloqueo.py`

Sandbox: `C:\Users\marti\Documents\MEX-Ontologi\propuestas\ampliacion-post-r9\ejecucion-20261024\B-tecnica\v001\_sim\T-top50\v001` (eliminado al terminar) y `C:\Users\marti\AppData\Local\Temp\b-tecnica-a2-vbd8zkoh` (solo se redirigen las lineas de ruta de salida); nada se escribe en los v001 sellados.

## Pendiente (no auditado, no aceptado)

- **A1-911**: PENDIENTE: no se acepta ni se adelanta dictamen
- **A3-itama**: PENDIENTE: no se acepta ni se adelanta dictamen
- **Q-unidades**: PENDIENTE: no se acepta ni se adelanta dictamen
- **S-shacl**: PENDIENTE: no se acepta ni se adelanta dictamen
- **integracion_final**: PENDIENTE: se audita despues, sin instalar

v002 observados fuera de alcance: A1-911, A2-registro-civil, A3-itama, Q-unidades, R-documental, T-top50, W-estandares. Solo se dictamina sobre v001 sellado; sus bytes no cambiaron durante la auditoria.

## Limites

- IRI definitiva / example.org fuera de alcance: config.toml solo se verifica, no se toca.
- Sin Gemma, sin contactos a publicadores, sin busquedas agotadas, sin manifiestos R1-R9.
- Sin joins automaticos, sin instalar, sin Studio, sin tocar escritores centrales.
- Escritura limitada a propuestas/ampliacion-post-r9/ejecucion-20261024/B-tecnica/v001/.
