# Agente 9 — Gobierno digital (ronda 3)

Partición exclusiva: 243 definiciones `fuera_del_nucleo_actual` de 10 diccionarios del
Diagnóstico del Entorno Digital (Administración Pública Estatal de Sonora), verificadas
una por una con lectura literal + inspección completa (descripción, tipo, unidad, ejemplo,
catálogo) + contexto publicado del conjunto (tema y notas de metadatos).

## Totales reales

| Métrica | Valor |
|---|---:|
| Decisiones (cobertura de asignación) | 243 / 243, sin omitidos ni duplicados |
| Reglas propuestas (`r3a9-001`…`r3a9-121`) | 121 |
| Conceptos nuevos estrechos | 85 |
| Conceptos reutilizados de los 103 vigentes | 0 (ninguno exacto; ver nota) |
| Pendientes con motivo | 122 |
| Nuevas correspondencias columna→variable | 0 (no solicitadas) |
| sameAs / exactMatch | 0 |

Pendientes por motivo: metadato-captura 40 · respuesta-abierta 48 · genérica-fragmento 13 ·
truncada-en-fuente 10 · contradicción-tipo-descripción 6 · contexto-dependiente 5.

## Verificación

`scripts/verificar_r3a9.py` (reproducible, `PYTHONDONTWRITEBYTECODE=1`) recalcula desde la
inspección local: 243 huellas de fila, 243 IRIs posicionales y 243 literales; simula
`interpretacion()` importada de `scripts/consolidar_semantica.py` (solo funciones puras):
121/121 positivos resuelven a su regla sin colisiones con las 116 centrales, 5/5 negativos
reales (solo-nombre, contexto mutado, otra IRI, pendiente que no resuelve, descripción
extendida) no resuelven. Sin U+FFFD en la partición (verificado en las 243 filas);
acentos, `¿`, NBSP y elipsis preservados byte a byte. Detalle en
`fuente/verificacion-r3a9.json`.

## Archivos

- `propuestas.json` — decisiones (243), reglas (121), conceptos_nuevos (85), huellas de entrada, alcance y límites.
- `scripts/generar_r3a9.py` — generador determinista desde evidencia local.
- `scripts/verificar_r3a9.py` — verificador propio.
- `fuente/verificacion-r3a9.json` — resumen de la verificación.
- `fuente/huellas-entrada.json` — copiado abajo desde `propuestas.json` para lectura directa (mismo contenido).

## Huellas de entrada

Ver `propuestas.json → huellas_entrada` (SHA-256 del archivo de asignaciones, huellas de
cobertura/inspección/inventario/reglas de ronda 2 y SHA-256 de los 10 archivos de
inspección usados). Sin red, sin microdatos, sin contacto con publicadores.

## Revisión manual vs automatización

- **Manual (criterio)**: lectura literal individual de las 243 definiciones con inspección
  completa y contexto del conjunto; cada veredicto, motivo y concepto nuevo lo decidió una
  persona. Nada se deduce por regex de nombres: los nombres son códigos `P\d+`/`ID` neutros
  y el significado sale solo del literal (verificado: todos los nombres cumplen `^P\d+$|^ID$`).
- **Automático (verificación)**: el generador aplica la tabla manual y el verificador
  recalcula huellas/IRIs/literales, simula `interpretacion()` (121 positivos, 5 negativos) y
  comprueba criterios de integración (unidades con respaldo literal, fusión existencia+nombre
  en un concepto, acotación por definición). La automatización no propone nada; confirma que
  lo manual quedó bien registrado.

## Criterios de integración aplicados

- Sin unidades por costumbre: personas/años/GB/CPUs/montos solo donde el literal los trae;
  montos sin moneda (nunca MXN), sin porcentajes, sin edades.
- Contradicciones nombre↔descripción conservadas como pendiente (P36/P40/P39 por duplicado).
- Existencia (`P8`) y nombre (`P9`) de la unidad coordinadora comparten el concepto
  `unidad-coordinadora-tic` con representación distinta; medidas distintas (existencia vs
  conteo, sector vs dependencia) van en conceptos separados.
- Las 121 reglas exigen definición+diccionario+conjunto+nombre exactos con huella real.

## Pendientes y límites

1. 40 metadatos de captura (ID, Sector genérico, 3 horas) — no denotan objeto de dominio.
2. 48 respuestas abiertas (Enliste/Mencione/Comente/¿Cuáles?/¿Cómo?/¿Qué tipo?/Detalle) — sin referente cerrado.
3. 10 truncadas en el diccionario publicado (corte a 199 caracteres o a media palabra).
4. 6 contradicciones tipo↔literal ("¿cuántos/cuántas…?" con tipo Booleano; "¿cómo…?" con tipo Booleano).
5. 5 contexto-dependientes ("este/la consolidación/la pregunta anterior/perfil/área" sin antecedente en el literal).
6. Sin U+FFFD en la partición (verificado fila por fila); acentos, apertura de
   interrogación, NBSP (3 descripciones) y elipsis preservados sin normalizar; tampoco ñ→n.
7. Conceptos compartidos entre instrumentos pares (desarrollo/mejora, gobernanza/fortalezas,
   política/gobernanza-datos) denotan la misma pregunta; no se afirma equivalencia de instrumentos.
8. Si/No = existencia declarada, no verificación; conteos declarados; catálogo vacío en las 243.
9. Nota de reutilización: `anio` genérico no cubre años de compra/encargo; `organizacion` no cubre
   el fragmento `Sector`; ningún código se promueve a catálogo, identidad, etnia ni diagnóstico.

## Bloqueos

Ninguno bloqueante. No se ejecutó consolidar/ampliar/sincronizar ni la suite central (prohibido
generar fuera de la carpeta); pendiente la revisión del integrador.
