# Diagnóstico F2 — fallo real de recuperación (C2)

Pregunta: `Explica la evidencia F2 de proyecciones en 2020 y sus condiciones pendientes. No extrapoles a otros años.`
Respuesta observada (`chat/antes-cambio-modelo/evaluacion.json` C2, `falla_oraculo`): "no se encontró evidencia F2", aunque el grafo vivo tiene 72 comparaciones `ComparacionMunicipal2020`, 144 evidencias `EvidenciaFuenteComparacion` y la ficha `https://example.org/mex-ontologi/cruce-r3/F2` (20 triples: alcance, 6 verificadas, 4 pendientes, 4 límites, decisión, tipo, `wasDerivedFrom` a `fichas/F2.json`).

Reproducción contra motor 8137 con módulos reales (`retrieve`/`asContext`/`terms` de `graphrag.ts`) y solo SELECT, cero llamadas al modelo (`repro` en esta carpeta, `evidencia_C2.json`):
- Original C2: anchors 16, hechos 240, `menciona_F2=false`, sin `144`/`grandes_grupos`. C3 (igualdad) sí menciona F2 vía `comparacionDe` desde `cruce-r3-2020/26001…`.
- Motor intacto: 284810 triples antes/después.

## Causa raíz (en `retrieve`, no en el modelo)

1. `terms()` exige `[\p{L}\p{N}][\p{L}\p{N}_-]{2,}` (mínimo 3 caracteres): el alias `F2` nunca entra a `ts` (`["explica","proyecciones","2020","condiciones","pendientes","extrapoles","otros","años"]`).
2. El anclaje es solo `CONTAINS(LCASE(label))` con `LIMIT 16 ORDER BY score, STRLEN`: con 8 términos genéricos (`otros`, `2020`, `explica`…) la ficha (label `F2 — Proyecciones…`, score 0, no corta) queda expulsada por recursos `2020`, oportunidades y datasets. C2 ancla `2020`/TIC/proyecciones pero no F2; los hechos 240 son vecindario de esos anclajes.
3. Sin resolución por alias/local-name exacto ni ficha dedicada: aunque 72 comparaciones apuntan a F2 (`comparacionDe`), nada las alcanza si los anclajes fallan. Tampoco dispara `wantsCorrespondenceOverview` (`evidencia` no está en `OVERVIEW_HINTS`), así que no hay conteo 72/144.
4. C3 pasa por accidente topológico: sus términos (`igualdad`,`valores`,`2020`) anclan `cruce-r3-2020/26001…` y el hop 1 trae `comparacionDe → F2`. C2 no tiene esa suerte.

## Parche (solo aditivo, en esta carpeta)

`graphrag.f2.ts` + `graphrag.f2.patch` contra `graphrag.ts` SHA256 `b109930519122d8970cd8c3d739a7dfd5659a5aa37d07b03e665cd7c5aa440ef` (43936 bytes):
- `cruceAliases()`: `/\bF\s?(\d{1,3})\b/gi` (no colisiona con años de 4 dígitos).
- `cruceFichaContext()`: por alias existente, ficha COMPLETA por IRI exacto (`?s ?p ?o`), conteos nativos `COUNT(DISTINCT)` de comparaciones (`comparacionDe`) y evidencias (`evidenciaDeFuente`), muestra de 3 comparaciones + 6 evidencias (rol/medida/nombre/fuente/hoja/sha/valor), con cabeceras de alcance `SOLO-2020`, `NO identidad de medida`, `sin equivalencia INEGI`, `cruce 1990-2040 NO ejecutado`. Sin `LIMIT` interno (rebanado en TS para no emitir doble `LIMIT`).
- `retrieve()`: ejecuta la ficha junto al scoped existente, antepone su ancla y la publica como `cruceFichaContext`. Solo se activa con alias F; sin alias el contexto es byte-idéntico al original.
- `asContext()`: bloque `CRUCE FICHA (COMPLETE FOR THE NAMED FICHA ONLY)`. Sin cambios a `QA_SYSTEM_PROMPT`, `terms()`, correspondencias, recursos ni variables.

Límites respetados: no afirma cobertura cruzada 1990-2040 (declara `solo 2020 cruzado`), no asume identidad de medidas (`suma_grupos_edad_H_M` vs `poblacion_mitad_ano`, yuxtaposición por clave textual), no acredita INEGI/vigencias.

## Verificación (cero modelo, solo SELECT)

- `test_regresion.mjs` (6 casos corpus, original vs parcheado): C2 pasa a `f2=true`, `ficha=true`, `faltan=[]`, `algunoOk=true`, `prohibidos=[]`; C1/C3/C4/C5/C6 byte-idénticos al original (definiciones/totales protegidos). Resultado: `REGRESION OK`.
- `evidencia_C2.json`: original 16/240 sin F2/144; parcheado 17/240 con F2 + `72` + `144` + `grandes_grupos` + pendientes/verificadas + `F2.json`.
- Grafo sin cambios (284810). No se tocó repo, instalación, configuración ni grafo.

## Ampliación: presupuesto Gemma4 31B (429 TPM)

Contextos medidos con módulos reales (prompt 4453ch + pregunta + contexto, ×1.15):
C1 14889tok, C2 22499tok, C3 9607tok, C4 42976tok, C5 58696tok, C6 74155tok.

## Corrección 429 (evidencia dashboard del usuario)

Captura Google aportada por el usuario (Gemma4 31B): RPM 1/30, TPM
13.08K/16K, RPD 1/14.4K. Esto demuestra consumo por minuto casi agotado
con RPM y RPD holgados: las llamadas sucesivas agotan el TPM aunque cada
petición individual quepa (el harness anterior las disparaba con 2s entre
ellas). Corrección al párrafo anterior: NO queda probado que cada 429
fuera una petición individual >16K; solo C2 (22499tok estimados) supera
16K por sí solo. Y NO se afirma cuota diaria agotada: RPD 1/14.4K la
descarta; es límite por minuto. El presupuesto (minimizar input a ≤10000
tok con margen) sigue necesario: reduce cada petición y deja ventana
para la salida dentro de los 16K/min. El harness exige espaciado mínimo
65s entre llamadas reales y respeta RetryInfo (esperas >15min no se
duermen: caso pendiente_cuota con hora de reanudación).

Parche (misma copia, sin tocar repo): `budgetForModel()` (Gemma→10000
tokens entrada, otros→Infinity intactos; `ONTO_CTX_BUDGET_TOKENS` o
override por llamada lo configuran), `estimateInputTokens()` (prompt +
pregunta + contexto, ~4ch/token ×1.15), `fitRetrieved()` (recorte por
lineas completas: COMPLETE y ficha siempre integros; mapping pineado >
definicion pedida > resto pineado > prioridad > resto; repetidas fuera;
nota BUDGET TRIM honesta), `maybeFit()` en `retrieve(..., {model})`
(retrocompatible: sin modelo = bytes identicos), y `cruceCodigoContext()`
(detalle exacto por codigoTextual+periodoCruzado: la vecindad hop-1 nunca
traia las medidas de cada fuente; excluye evidencias que tambien llevan
el codigo). `GEMMA_PACING_MS=65000` (>=60s) para llamadas reales;
harness exige `--con-modelo` + `ONTO_ALLOW_MODEL_CALLS=1` (nosotros:
0 llamadas).

Verificado (`test_presupuesto.mjs`, solo SELECT): 6/6 en 9870-9903tok,
F2+72/144/condiciones/limites, totales exactos, definiciones
(364ffa5c, diccionario.csv, definicionOriginal), 26001 ambas fuentes
(medida/nombre/archivo/filas/sha/valor), sin prohibidos, sin lineas
truncadas, otros modelos intactos.

## Bloqueo: texto F2 hardcodeado para F1/F3 (corregido antes de entrega)

Revisión del primer patch: `cruceFichaContext` aceptaba F1/F2/F3 pero
inyectaba siempre el resumen F2 (solo-2020, grandes_grupos/indicadores,
1990-2040, dos fuentes). Falsa afirmación: F1 es Matrimonios-Divorcios
2022 y F3 Titulados-Egresados 2020-2021 + Nuevo-Reingreso 2021-2022, ambas
con 0 comparaciones municipales en RDF; sus periodos/medidas viven en sus
propios triples (verificados por SELECT: F1 20 triples, F3 17 triples).

Corrección (misma copia, sin tocar repo): el resumen de cada ficha se
deriva de su RDF real — conteos nativos, `periodoCruzado` distintos,
`fuenteRol`/`medidaOrigen` distintos observados; `ALCANCE` declara el/los
periodo(s) observado(s) o la ausencia de comparaciones; el ejemplo de
comparación usa su `periodoCruzado` real. Cero frases acreditativas
hardcodeadas fuera de su ficha: F2 conserva sus datos porque su RDF los
trae (72, 2020, ambos roles/medidas, F2.json, límites en sus triples).
El texto de cada ficha se emite como hechos citados (triples), nunca como
instrucciones: la fuente investigada puede contener prompt injection y
aquí solo vale como datos. `cruceCodigoContext` igual: su línea LIMITES
ya no afirma identidad/vigencia, remite a los `limiteInterpretativo` de
los triples. Presupuesto y pacing Gemma (>=65s + RetryInfo) intactos.

Verificado (`test_fichas_f1_f3.mjs`, solo SELECT): F1 con F1.json/2022/0
comparaciones y 10/10 líneas sin texto F2; F3 con F3.json/2020-2021/
2021-2022 y 10/10 sin texto F2; F9 inexistente devuelve vacío sin sección
ni IRI inventado; F2 mantiene 72/144/roles/medidas/alcance derivados.
C1-C6 re-verificados (`test_regresion` + `test_presupuesto` + harness:
todo OK, grafo 284810 intacto, 0 llamadas al modelo).
