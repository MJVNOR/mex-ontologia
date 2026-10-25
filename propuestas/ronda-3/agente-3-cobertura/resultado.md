# Agente 3 — Cobertura fuera del núcleo (ronda 3, con corrección del integrador)

## Verificación de base

Conteos actuales confirmados contra `reports/pendientes-semanticos.json`,
`data/semantica/cobertura.json`, `ontologia/semantica.json`,
`data/portal/inventario.json` y `data/portal/contenido-inspeccion.json`
(huellas SHA-256 fijadas en `fuente/huellas.json`):

| Estado | Cantidad |
| --- | ---: |
| Columnas examinadas | 5523 |
| definicion_sin_interpretacion_compartida | 3720 |
| sin_definicion_coincidente | 833 |
| sin_diccionario_en_conjunto | 13 |
| documental_revisada (intacta) | 836 |
| candidata_por_nombre (intacta) | 118 |
| ambigua_por_nombre (intacta) | 3 |
| Variables fuera del núcleo actual | 1308 |
| Significados candidatos del agente 4 (intactos, no tocados) | 23 |
| Conceptos / reglas del núcleo (no modificados) | 103 / 116 |

## Lectura completa (4 familias, 66 variables)

Leídas fila por fila con literal, tipo de dato, unidad de medida, catálogo
de referencia, nulos y ejemplo. La unidad se toma solo de la fila; si falta,
no se deduce (consta "Sin unidad declarada").

| Familia | Diccionario | Vars | Reglas | Conceptos nuevos |
| --- | --- | --- | --- | --- |
| Censo Ganadero de Sonora | 045da7ba… | 18 | 18 | 19 (12 categorías + bovino + menor + productores + DDR + región + cuenca + agrupador) |
| Agricultura Sonora | 94215f51… | 18 | 18 | 18 (DDR/municipio/mes/cultivo/variedad × código-nombre, cierre-avance, 3 superficies + agrupador, producción, rendimiento, PMR, valor) |
| Pesca y Acuacultura | 863b9cc8… | 14 | 12 | 12 (DDR/municipio/oficina/especie/origen × código-nombre, 2 pesos, valor) |
| Permisos de Siembra de Trigo | a7591bc9… | 16 | 15 | 5 (variedad × clave-nombre-tipo, superficie por DDR, superficie total) + 1 reutilización (`organizacion` para FUENTE) |

Total: 63 reglas (una por definición) + 55 conceptos nuevos + 1 reutilización.
Cada familia queda documentada en `propuestas.json → familias_revisadas`.

## Requisito de integración: calificador SHD (limitación del pipeline)

`interpretacion()/construir()` **no propagan calificador** a la variable
documentada ni al grafo — verificado en esta base: los resultados solo
traen `estado/concepto/regla/representacion` (0 calificadores). No se declara
que el pipeline ya lo preserve.

- Las 10 reglas SHD llevan `calificador {"distrito_desarrollo_rural": "NNN"}`
  distinto + `requisito_integracion` explícito.
- Requisito antes de aplicar: propagar el calificador a variable
  documentada/grafo y validar DDR distinto por regla.
- Alternativa: 10 conceptos estrechos por DDR.
- `scripts/verificar.py` incluye un detector en base que pasa mientras la
  limitación exista y falla a propósito si el pipeline empieza a propagar
  (señal para revisar el requisito). Sin cambios al núcleo.

## Aritmética simulada con las 63 reglas (funciones reales del pipeline)

| Estado | Simulado | Cálculo |
| --- | --- | --- |
| respaldadas | 295 | 232 + 63 |
| fuera del núcleo | 1245 | 1308 − 63 |
| candidatas agente 4 | 23 | intactas |
| conceptos | 158 | 103 + 55 |
| revisadas | 836 | intactas |
| candidatas por columna | 827 | 118 + 709 nuevas **no revisadas** |

Las 709 se corroboraron con cómputo propio: 709 columnas físicas matchean
las 63 definiciones (todas `definicion_sin_interpretacion_compartida`, nombre
único, definición única hoy). Candidata no es revisada: requieren revisión
del agente 2; esta propuesta no crea correspondencias.

## Pendientes: 1245 ≠ 1242 (distinguidos)

- 1245 fuera del núcleo tras integrar (1308 − 63).
- 1242 sin lectura (1308 − 66).
- 3 leídas y clasificadas sin propuesta (CVOTRAS, DOTRAS, GRUPO).
- 1242 + 3 = 1245. Ambos conteos constan en el inventario y el verificador.

## Corrección aplicada (revisión del integrador)

- SUPSEM/SUPCOSE/SUPSINI: conceptos separados superficie
  sembrada/cosechada/siniestrada con broader `superficie-cultivo`.
- TOTAL_GANADO_BOVINO vs MENOR: conceptos con población explícita distinta.
- VACAS/TOROS/etc: un concepto estrecho por categoría (12), con broader
  `ganado-registrado-censo`; ninguna medida indistinguible.
- SHD139–SHD193: 10 reglas con concepto compartido
  `superficie-sembrada-trigo-ddr` + calificador formal
  `{"distrito_desarrollo_rural": "NNN"}` distinto por regla; SUMTOT con
  concepto propio (total por registro, suma no demostrada).
- NDDR agricultura y pesca: sin evidencia de nombre puro (tipo
  Numérico/Texto, ejemplo vacío) → representación `no_especificada` y
  conceptos `descripcion-ddr-registro-cultivo` /
  `descripcion-ddr-registro-pesquero` (contexto conservado); conflicto de
  tipo Numérico en agricultura registrado en el límite, sin deducir formato
  ni catálogo.
- Evidencia: cada regla trae `evidencia` byte-exacta de las fuentes
  (variable, descripción, IRI, unidad, tipo, ejemplo, catálogo). La prosa
  analítica (alcance, positivo, contraejemplo, límite, definiciones de
  conceptos nuevos) es redacción propia y nunca transcribe literales: solo
  cita identificadores e IRIs. Verificado automáticamente.

Sin propuesta tras lectura (3, con motivo): CVOTRAS/DOTRAS (sin referente),
GRUPO (sin leyenda publicada).

Ninguna propuesta crea correspondencia columna→variable ni uso automático en
cruces (agente 2). Los 23 candidatos del agente 4 no se tocan (verificado).

Nota: los calificadores los implementa el parche del integrador; esta
entrega no cambia el núcleo y mantiene el requisito documentado.

## Inventario total (`inventario-cobertura.json`)

- 3720 columnas en 83 grupos por conjunto; 833 sin definición en 89 grupos;
  13 sin diccionario listadas (conjunto f58a3196…, sin diccionarios en el
  conjunto: clasificadas, sin vínculo — el nombre no es evidencia).
- 1308 fuera del núcleo en 85 grupos (1190 dominio/medida, 118 vacías).
- Prioridades pendientes (top 5): Fiebre manchada (456 col/166 var),
  Información Sobre Nacimientos (90/90), SEED Defunciones (65/65),
  Matrículas (57/57), Vigilancia Epidemiológica (56/56).

Límite explícito: solo las 4 familias están leídas; el resto está agrupado,
no leído fila por fila. Prioridades por conteo × especificidad literal, sin
simular revisión.

## Verificación

`scripts/verificar.py`: comprobaciones PASS, 0 fallos, incluidos:

- Huellas de los 5 insumos contra archivos reales.
- 63 literales + unidades + tipos + ejemplos byte-exactos contra
  `cobertura.json` e inspección.
- Prosa sin transcribir ningún literal; calificadores distintos en
  conceptos compartidos; unidades de conceptos iguales a la evidencia.
- Simulación con `interpretacion()` del pipeline: las 63 definiciones
  disparan su regla con su concepto; aritmética 295/1245/23/158.
- 709 candidatas nuevas corroboradas (827 = 118 + 709, no revisadas);
  distinción 1245/1242/3; detector de la limitación del calificador.
- Validador compartido `scripts/validar.py → validar_propuestas(prop, fuentes,
  asignacion)`: el positivo pasa por él en construcción y verificación.
  7 negativos por deepcopy + mutación sobre la misma función, cada uno con su
  código: N1 borrar alcance → CAMPO_FALTANTE, N2 regla global →
  SIN_RESTRICCION, N3 IRI inexistente → IRI_DESCONOCIDA, N4 literal mutado →
  LITERAL_DIFERENTE, N5 candidato agente 4 → FRONTERA_AGENTE4, N6 IRI física
  → IRI_COLUMNA, N7 regla duplicada → ID_DUPLICADO.
- Inventario con particiones exactas (`==`, no `>=`): 3720, 833 y 1308
  identidades listadas por grupo, sin solapes verificados.

Reproducir (solo lee fuera de esta carpeta, sin red):

```powershell
uv run python propuestas/ronda-3/agente-3-cobertura/scripts/construir.py
uv run python propuestas/ronda-3/agente-3-cobertura/scripts/verificar.py
```

Suite central: 85 tests OK.

## Archivos entregados

- `resultado.md`, `propuestas.json` (63 reglas, 55 conceptos, 4 familias),
  `inventario-cobertura.json`, `fuente/huellas.json`,
  `scripts/construir.py`, `scripts/validar.py`, `scripts/verificar.py`.

## Bloqueos y pendientes

1. 1242 variables sin lectura completa; siguiente: Fiebre manchada (166 var,
   microdatos clínicos, lectura íntegra pendiente).
2. Sin descargas ni contactos: ningún vínculo para columnas sin
   definición/diccionario.
3. Literales con U+FFFD de origen preservados byte-exactos; la corrección en
   origen (huellas) queda al integrador.
