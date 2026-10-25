# Agente 8 — Educación (ronda 3)

## Verificación de base

Conteos actuales confirmados contra `reports/pendientes-semanticos.json`,
`data/semantica/cobertura.json`, `ontologia/semantica.json`
(huellas SHA-256 fijadas en `fuente/huellas.json`):

| Estado | Cantidad |
| --- | ---: |
| Variables fuera del núcleo actual | 1308 |
| Asignadas al agente 8 (partición exclusiva) | 126 |
| Conceptos vigentes / reglas del núcleo (no modificados) | 103 / 116 |
| Correspondencias revisadas / candidatas / significados agente 4 (intactos) | 836 / 118 / 23 |

Las 126 IRIs asignadas coinciden exactamente con las 126 decisiones
(sin omitidos ni duplicados); las 126 constan `fuera_del_nucleo_actual`
y en pendientes. Huellas de fila recalculadas con la función central
`huella()` desde la inspección cruda: 126/126 coinciden.

## Lectura completa (15 diccionarios, 126 variables)

Leídas fila por fila con literal, tipo de dato, unidad, catálogo de
referencia, ejemplo y contexto del conjunto (notas, organización, frecuencia).
Sin red: evidencia local publicada; URLs de diccionarios registradas sin
descargar microdatos. Literales latinos preservados byte-exactos
(verificación `sin-ufffd`); ninguna normalización ñ→n.

| Bloque | Vars | Reglas | Conceptos nuevos |
| --- | ---: | ---: | --- |
| Conteos por sede (nuevo ingreso, egresados, reingreso, titulados × 5 sedes) | 20 | 20 | 4 + calificador `sede` por regla |
| Resúmenes anuales por programa y sexo (titulados, egresados, TSU, reingreso) | 12 | 12 | 8 (+1 nivel y +1 campo compartidos abajo) |
| Nivel / campo de formación (5 diccionarios) | 11 | 11 | 2 |
| Sexo (alumno ×3, titulado ×2) | 5 | 5 | 2 |
| Matrículas UES (registro por alumno) | 34 | 34 | 30 (+2 reutilizaciones, +2 compartidos) |
| Matrículas (registro por alumno, otro conjunto) | 8 | 8 | 6 (+1 reutilización, +1 compartido) |
| Matrícula cuatrimestral (registro por estudiante) | 9 | 9 | 6 (+3 compartidos) |
| Aprovechamiento por programa (rangos, evaluados, global) | 7 | 7 | 7 |
| Promedio cuatrimestral por sexo | 3 | 3 | 3 (+2 compartidos) |
| Pendientes (vacías/genéricas/confusas, con motivo) | 27 | 0 | 0 |

Total: 126 decisiones, 99 reglas (una por definición), 66 conceptos nuevos,
1 reutilización (`programa-educativo`), 27 pendientes con razón.

## Requisito de integración: calificador de sede (limitación del pipeline)

`interpretacion()/construir()` no propagan calificador a la variable
documentada ni al grafo (misma limitación documentada por el agente 3).
Las 20 reglas de conteos por sede comparten concepto con calificador formal
`{"sede": "..."}` distinto por regla. Requisito antes de aplicar: propagar el
calificador y validar sede distinta por regla. Alternativa: 20 conceptos
estrechos por sede. El verificador incluye esta aritmética y no afirma que el
pipeline ya preserve el calificador.

## Aritmética simulada en memoria (funciones reales, sin generar nada central)

| Estado | Simulado | Cálculo |
| --- | ---: | --- |
| respaldadas | 331 | 232 + 99 |
| fuera del núcleo | 1209 | 1308 − 99 |
| candidatas agente 4 | 23 | intactas |
| conceptos | 169 | 103 + 66 |
| revisadas | 836 | intactas |
| candidatas por columna | 118 | intactas (esta entrega no crea candidatas) |

Las 232 respaldadas vigentes resuelven idéntico con las 99 reglas añadidas
(no-regresión verificada, sin conflictos `ValueError`).

## Verificación

`scripts/verificar.py`: 485 comprobaciones PASS, 0 fallos, incluidos:

- Huellas de los 4 insumos contra archivos reales + 126 huellas de fila
  recalculadas con `huella()` central desde la inspección cruda.
- 126 literales (variable, descripción, tipo, unidad, catálogo, ejemplo)
  byte-exactos contra asignación e inspección.
- 99 positivos: cada definición dispara su regla con su concepto vía
  `interpretacion()` real.
- 8 negativos reales: N1 solo-nombre, N2 contexto-mutado, N3 otra-IRI,
  N4 diccionario-distinto, N5 códigos cruzados no equivalentes + claves sin
  identidad, N6 pendiente sin regla, N7 IRI de columna física, N8 23
  candidatas del agente 4 intactas.
- Forma: IDs `r3a8-` únicos, broadeners existentes, sin `sameAs`/`exactMatch`
  estructurales, sin IRIs de columna, unidades de evidencia iguales al
  literal (ninguna inventada), conceptos sin colisión con núcleo ni agente 3.

Reproducir (solo lee fuera de esta carpeta, sin red):

```powershell
uv run python propuestas/ronda-3/agente-8-educacion/scripts/construir.py
$env:PYTHONDONTWRITEBYTECODE='1'
uv run python propuestas/ronda-3/agente-8-educacion/scripts/verificar.py
```

## Revisión manual vs automatización

Manual (lectura fila por fila de las 126 definiciones, sin regex sobre
nombres): cada decisión propuesta/pendiente, cada concepto nuevo y cada
criterio/límite se fijó leyendo descripción, tipo, unidad, ejemplo, catálogo
y notas del conjunto. Casos nombre-vs-descripción resueltos a favor de la
descripción y registrados en el límite (`Unidad Académica`→municipio;
`Periodo/Ciclo/Baja/Plan`→código; `Estado civil` sin población→población del
conjunto). Egreso y titulación, y nacimiento y nacionalidad, quedan en
conceptos distintos sin cruces.

Automático (`verificar.py`, 485 PASS): partición exacta, huellas y literales
byte-exactos, 99 positivos y 8 negativos con `interpretacion()` real,
no-regresión de las 232 respaldadas, forma y límites estructurales. La
máquina no decide significados: solo comprueba que lo decidido a mano quedó
fielmente codificado y acotado (definición+diccionario+conjunto+huella).

## Cumplimiento del criterio de integración

- Sin unidades por costumbre: edad sin unidad declarada (enteros, sin
  afirmar años); conteos con objeto literal de la descripción; promedios sin
  rango afirmado; sin porcentajes ni monetarios. Evidencia con unidad igual
  al literal (verificado).
- Sin promoción por apariencia: 27 pendientes (vacías/genéricas/confusas);
  ejemplos nunca sustituyen descripciones; códigos sin catálogo declarado no
  acreditan sistemas; sin `sameAs`/`exactMatch`; sin correspondencias.
- Código/nombre del mismo registro comparten concepto con representación
  distinta (campo de formación); categorías y medidas distintas llevan
  concepto específico (sexos, rangos, periodos, poblaciones) o calificador
  formal (sede, pendiente de propagación).

## Archivos entregados

- `resultado.md`, `propuestas.json` (126 decisiones, 99 reglas, 66 conceptos),
  `fuente/inspeccion-126.json`, `fuente/huellas.json`,
  `scripts/construir.py`, `scripts/verificar.py`, `scripts/volcar.py`.

## Bloqueos y pendientes

1. 27 variables quedan pendientes con motivo (21 descripciones vacías
   `Pendiente de especificar`, 2 números de orden, 1 número consecutivo de
   fila, 1 descripción confusa, 1 `Numero del alumno` genérico, 1 `Tipo de
   baja` sin leyenda). Requieren aclaración del publicador; ningún ejemplo
   sustituye una descripción.
2. 20 reglas con calificador de sede pendientes de propagación por el
   pipeline (requisito explícito arriba).
3. Sin descargas ni contactos: ningún vínculo para columnas sin definición.
