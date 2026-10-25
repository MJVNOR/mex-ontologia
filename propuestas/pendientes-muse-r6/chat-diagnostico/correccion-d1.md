# Corrección D1 con datos reales R6 (refuta causa env-ausente)

Dato R6 (integrador, bundle instalado): handshake `_Connected: ... Model:
gemma-4-31b-it`, C1 respondió 4474/20/2 correcto, **C2 HTTP500** — todo bajo
entorno Gemma explícito y budget 6500 activo.

Consecuencia: el trim SÍ aplicaba y C2 falló igual. La hipótesis D1
(`EFFECTIVE_MODEL=''` → sin recorte → 500 por tamaño) queda REFUTADA como
explicación de estos 500 observados. `parche-propuesto.patch` (D1) pasa a
**robustez para otra configuración** (arranque sin env), no causa demostrada;
no atribuir el 500 del gateway a eso.

Lo que la evidencia sí sostiene y el nuevo parche atiende:
1. C1 (pequeño, con conteos COMPLETE) pasa; C2 (ficha F2 + 72/144) 500 con el
   MISMO schema y MISMO presupuesto → el 500 no es tamaño global del prompt
   en este régimen; es respuesta del servidor ante ese contenido/carga.
2. Si la primera respuesta llega vacía (thought-only recortado, recitación…),
   el código actual cae a `runTurn(context)` CON las 114 tools (132 KB) y con
   herramientas de MUTACIÓN disponibles (`onto_apply`, `onto_ingest`, …):
   riesgo de escritura desde un camino degradado. El parche lo cierra: error
   claro, sin mutación, sin cachear vacío.
3. Reintento: 1 solo (2 intentos), solo 500/502/503 y 429, solo en completion
   ANTES de ejecutar herramientas, misma Gemma, 500 vs 429 clasificados
   distinto, espera RetryInfo con piso 65s, cada resultado consumido 1 vez.
