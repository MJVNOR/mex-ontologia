# Agente 5 ronda 2 — Evaluación de solo lectura del chat (grafo integrado MEX-Ontologi)

Solo lectura fuera de `propuestas/ronda-2/agente-5-evaluacion-chat/`. Sin cambios a prompts, código, configuración, credenciales, grafo, motor ni instalación. Sin reiniciar Studio ni borrar conversaciones. Sin consumir entregas de otros agentes de ronda 2. Sin relanzar preguntas ni duplicar costos de modelo (se reutilizan las 4 respuestas ya obtenidas; los 16 restantes quedan `no_ejecutado` con su error registrado).

## Alcance exacto (ver `alcance.json`)

- Canal evaluado: **prueba del pipeline fuente GraphRAG+QA+Gemini con grafo vivo**. NO es la UI de Studio.
- Evaluación UI de Studio: **no_ejecutada** en los 20 casos. Límite: sin automatización GUI en este entorno; no se altera instalación ni conversaciones.
- Identidad de backend: **NO demostrada**. Se importa `graphrag.ts` + `providers/openai.ts` desde el repositorio `C:/Users/marti/Documents/open-ontologies/` (hashes SHA-256 registrados), no necesariamente el sidecar instalado en uso por Studio (`.../sidecars/agent/dist/index.js`, hash registrado; fuente TS vs bundle JS sin prueba de build). No se afirma "mismo backend de Studio".
- Configuración: solo valores no secretos — proveedor `openai-compatible`, base URL `https://generativelanguage.googleapis.com/v1beta/openai`, modelo `gemini-3.5-flash`. La clave API nunca se registra ni se imprime. Coincidencia con la configuración efectiva de la UI: **NO comprobada** (`agent-env-path.txt` apunta al `.env` del proyecto, pero eso no prueba la carga efectiva del proceso UI en ejecución).
- Grafo: `http://127.0.0.1:8137/api/query` (POST JSON `{query: SPARQL}`, valores en RDF N3). Son verdades del grafo, no verdad externa.

## Base contrastada (verdades del grafo)

Fecha UTC: 2026-10-23. Consultas y respuestas brutas en `fuentes/sparql/`.

- `ConceptoCompartido`: 103
- `VariableDocumentada` por `estadoSemantico`: 232 respaldada, 23 candidata, 11 fuera del núcleo (= 266)
- `CorrespondenciaSemantica`: 162 documental_revisada, 792 candidata_por_nombre, 6 ambigua_por_nombre (= 960)
- `ReferenciaCatalogoDeclarada`: 16 recurso_identificado, 1 sin resolver (des_mpo_res)
- `LocalidadObservada` IML_2020: 1850, estado derivada_observada_sin_completitud_oficial
- `ComprobacionAplicacionTerritorial`: 16 compatible, 11 compatible_con_excepciones, 1 sin_columna_fisica (= 28)
- Detalles: 3 columnas ide_id / 6 vínculos ambiguos (Fiebre manchada 2022/2023/2024, sin elegir); 26998/26999 categoria_no_municipal; columna a–o (U+2013) Nacimientos 2024 con límite sin corrección ni transferencia de 2022; 2 variables CLUES pendientes distintas (Nacimientos vs Defunciones, "Pendiente de especificar"); CVEGEO municipal según GeoJSON del portal (`identifier-system/geojson-d20d36c4-6406-4054-845c-43308b380b95`, códigos 26001… con 26 de entidad + 3 de municipio) con esa composición comprobada en dicha referencia; lo no acreditado es que los códigos municipales de otros recursos correspondan al mismo sistema o su equivalencia con IML/Registro Civil (el límite guardado en IML_2020 deja composición y correspondencia con CVEGEO no resueltas para ese recurso); des_mpo_res sin resolver + filas 177/178 degeneradas conservadas.

Las afirmaciones de ausencia solo valen para el alcance de cada consulta COMPLETE (p. ej. conteos por variable o por estado); el vecindario general del chat es parcial por diseño y "no recuperado" no equivale a "no existe".

## Casos (20 únicos, 9 con resultado correcto "no acreditado")

`casos.json` con preguntas neutrales y constantes (piden evidencia/procedencia, nunca editar ni corregir).
No-acreditados: C03, C04, C08, C10, C11, C13, C16, C18, C19.

## Resultados del pipeline fuente (sin nuevos costos)

- Intentos con respuesta del modelo: 4 (C01, C02, C05, C06; texto completo en `respuestas_brutas/`). Intentos con error HTTP/cuota sin respuesta del modelo: 16 (errores `HTTP 503 UNAVAILABLE` / `HTTP 429 free-tier` conservados por caso; sin respuestas inventadas ni sustitución de modelo). La etiqueta `no_ejecutado_cuota_modelo` significa únicamente "intento registrado que no obtuvo respuesta por error HTTP/cuota", no un veredicto sobre el grafo.
- Aciertos: 2 (C01 año_matrimonio = "Año de registro" con mapping Matrimonios 2022; C02 año_defuncion = "Año en el que fallecio" con 10 revisadas confirmadas por SPARQL `c02_rev.json`).
- Fallos: 2 (C05, C06). Ambas son abstenciones honestas ("no se encuentran en la evidencia recuperada"), no alucinaciones.
- Clasificación respaldada por el contexto guardado de cada caso: **error de recuperación / parcialidad del contexto**, no error del modelo, solo para C05/C06 y según sus `.contexto.txt` (las preguntas amplias sin identificador `nombreVariableLocal` no activan `correspondenceContext`, así que los conteos COMPLETE no llegan al modelo; el modelo obedece al prompt QA y no inventa). No se generaliza a partir de 4 respuestas: no se concluye que el modelo nunca falle. SPARQL directo sí confirma 4 revisadas Matrimonios 2022 (`c05_mat2022.json`), pero esa consulta no es respuesta del chat y se registra como canal distinto.

## Límites explícitos

- UI real no evaluada por falta de driver GUI; el pipeline fuente comparte lógica de recuperación, prompt y modelo, pero su identidad con el bundle instalado no está demostrada.
- 16/20 sin respuesta del modelo por cuota 429/503; no se relanza para no duplicar costos.
- Verificación reproducible sin modelo: `verificar_entrega.py` (solo lectura: no llama a modelos ni modifica evidencias) comprueba 20 casos únicos, conteos ejecutados/no_ejecutados y existencia/consistencia de evidencias. Reejecutar SPARQL sin tocar originales: `verificar_base.py` por defecto consulta y compara en memoria; con `--refresh` guarda una nueva corrida fechada sin sobrescribir las evidencias originales, siempre dentro de esta carpeta.
- Esta entrega es un diagnóstico **PARCIAL** del pipeline fuente, no una evaluación completa ni una certificación de la UI.
- Sin propuestas de cambio al grafo ni al chat (evaluación de solo lectura).
