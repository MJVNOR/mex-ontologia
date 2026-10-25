# Agente 1 ronda 3 — Corrección de recuperación del chat, v3 (revisable, sin desplegar)

Solo escritura dentro de `propuestas/ronda-3/agente-1-chat/`. Núcleo, Studio vivo,
configuración e instalación intactos. Sin consolidar/ampliar/sincronizar, sin modelos,
sin red externa, sin secretos.

## 1. Devoluciones atendidas (v2 + v3)

La v1 resolvía "recursos" por subcadena de etiqueta sobre cualquier `rdfs:label`
(falso cero ante paráfrasis, mezcla con no-columnas). La v2 resolvió recursos reales
pero con año-subcadena y agregación por etiqueta. La v3 corrige ambos:
- **Año delimitado + periodo declarado prioritario**: la etiqueta usa regex
  `(^|[^0-9])YYYY` ("20220" nunca casa 2022); con periodo interpretable
  (`inicioDeclarado`/`finDeclarado`) el año debe estar en el rango y la etiqueta es
  solo respaldo acotado; contradicción etiqueta≠periodo se documenta y el periodo
  prevalece; intervalos (1990–2040) casan por solape de rango declarado, nunca como
  cobertura observada de un año interior.
- **Agregación por IRI**: `GROUP BY ?resource ?status` (no por etiqueta),
  `VALUES ?resource` restringido a resueltos en conteos, etiquetas, detalle y gran
  total; gran total con `COUNT(DISTINCT ?mapping)` global en consulta propia, no suma
  de parciales. COMPLETE refiere al conjunto triangulado (columnas observadas vía
  recurso→esquema→columna), no al contenido exhaustivo del archivo original; sin
  esquema ⇒ PARTIAL ("columnas no observadas"), nunca cero de columnas fuente.

## 2. Diagnóstico y base

C05/C06 fallaban porque `correspondenceContext` exigía `nombreVariableLocal`; sin él
no había consulta COMPLETE y el modelo solo veía el vecindario parcial. Motor vivo
`http://127.0.0.1:8137/api/query` (solo SELECT, 2026-10-23): 103 conceptos; variables
232/23/11; correspondencias 836/118/6 (total 960). El grafo vivo ya integra ronda 2
(162/792 histórico). Matrimonios 2022: 9 columnas vía esquema, 4 mapeos revisados.
Evidencia: `evidencia/resumen_base.json`, `evaluacion_C05_C06.json`, sondeos de
topología en `scripts/sondear_topologia*.py`.

## 3. Corrección

`parche/graphrag.ts.patch` (+374/−2) e `index.ts.patch` (+1/−1), con archivos
completos en `parche/`:
- `correspondenceStatusOverview`: GROUP BY nativo con DISTINCT, COMPLETE + total.
- `resourceCorrespondenceContext` v3: `resourceKeywords` (sin verbos de instrucción
  ni estados), `questionYears`, `questionRange`, `keywordVariants` (singular/plural);
  pre-filtro SPARQL acotado + decisión estricta en TS (`strictYearVerdict`: periodo
  declarado primero, etiqueta delimitada como respaldo, contradicciones
  documentadas, rangos por solape sin afirmar cobertura observada). Resolución AND y
  respaldo OR multi-recurso con desglose; vocabulario descubierto por sufijo;
  agregación por IRI con gran total DISTINCT global; UNRESOLVED/PARTIAL sin
  afirmaciones de cero.
- `variableStatusOverview`, intentos deterministas, `retrieve` en paralelo,
  secciones COMPLETE en `asContext`, reglas global/recurso/variable en el prompt.
- `index.ts`: la rama de vacío exige además ausencia de los tres contextos.

## 4. Verificación

- Offline: 32+9 pasan; `tsc --strict` limpio. Cubren >200 registros con revisado
  tras offset 200, paráfrasis naturales, orden distinto, plural/singular, 2 recursos
  y 2 años, año-filtro no substring, negativos 20220/periodo-contradictorio, misma
  etiqueta en 2 IRIs, columna compartida (gran total 1), etiquetas idioma
  duplicadas, estados variable vs correspondencia, error→rechazo, UNRESOLVED sin cero.
- E2E con el `retrieve()`/`asContext()` **reales parchados** sobre HTTP 8137
  (`trabajo/recuperacion-e2e.test.ts`, adaptador onto_query, sin modelo; 6 casos en
  `evidencia/e2e_recuperacion.json` con pregunta+contexto+resumen): C06 6/118/836
  total 960; C05 y ambas paráfrasis resuelven Matrimonios 2022 con sus 4 revisadas
  (incluye mapping `c92aecbb…`); 2 años resuelven 2022+2024; variables 232/23/11.
- `scripts/verificar_entrega.py` (offline y `--live`): todo OK, incluido el e2e y la
  correspondencia parche↔archivos. Logs en `evidencia/`.
- Modelos: 0 peticiones. Cuota falló en ronda 2; la recuperación es determinista.

## 5. Identidad e instalación

Fuente intacta desde ronda 2 (`graphrag.ts` ae43065f…); bundle instalado igual al de
ronda 2 (50a560cc…, 528313 B). Rebuild local no lo reproduce: al instalar,
recompilar con deps fijadas y comparar hashes. Plan y reversión en
`propuestas.json`. UI no probada. Sin despliegue desde aquí.

## 6. Archivos y pendientes

`fuente/` (+`huellas.json`), `trabajo/`, `parche/`, `scripts/`,
`evidencia/` (base, C05/C06, e2e 6 casos, logs, build-identidad), `propuestas.json`.
Pendiente del integrador: revisar, aplicar, recompilar, instalar, comprobar C05/C06
en Studio y decidir si las pruebas entran al repo upstream.
