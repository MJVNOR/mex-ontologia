# Agente 11 ronda 3 — auditoría independiente (3/7/8/9/10; 6 excluido)

Rol: auditor (6 lo audita agente 12 e integra su revisión). No propone conceptos ni
reglas, no toca núcleo ni otras propuestas. Solo escribe en esta carpeta. Sin red,
sin consolidar/ampliar/sincronizar.

## Base verificada (real, recalculada)

103 conceptos núcleo, 232 respaldadas, 1308 fuera del núcleo, 23 candidatas agente 4,
836 revisadas, 118 candidatas, 3 ambiguas. Particiones exactas y disjuntas:
163 (A7) + 126 (A8) + 243 (A9) + 468 (A10) + 66 leídas A3 = 1308 sin solape.
Huellas antes=después dentro de la corrida → base estable.

| Propuesta auditada | SHA-256 auditado | Reglas |
| --- | --- | ---: |
| A7 registro civil | `c0523fc8…` | 75 |
| A3 cobertura | `92a7dcdd…` | 63 |
| A8 educación | `9672a4ba…` | 99 |
| A9 gobierno digital | `d730f00d…` | 121 |
| A10 territorio-economía | `10ee1791…` | 419 |

Versiones anteriores (NO auditoría final, ya cambiaron):
A7 `f075f884` (76 reglas) → `c0523fc8` (75);
A3 `29f1dadf` → `92a7dcdd` (63);
A10 `4ee4a145` (331) → `ddba32c2` (intermedio) → `10ee1791` (419).
Si vuelven a cambiar, re-auditar por SHA.

## Dictámenes por regla (777/777 literales revisados, no muestra)

Cada dictamen en `auditoria.json` identifica regla, IRI de definición, concepto,
representación, variable y descripción + motivos + chequeos: accionable sin revisar
el código del auditor.
IRI/fila/huella contra inspección actual, literales byte-exactos
(variable/descripción/unidad/tipo/ejemplo/catálogo), alcance simultáneo
conjunto/diccionario/definición/nombre/descripción, representación justificada,
sin unidades/años/MXN inventados, sin identidad/etnia/diagnóstico por abreviatura,
sin código↔nombre sin evidencia, sin colisiones con los 103 ni entre propuestas,
pipeline real (`consolidar_semantica.interpretacion`).

| Propuesta | Aceptar | Condicionado | Rechazar |
| --- | ---: | ---: | ---: |
| A7 (75 reglas, 50 nuevos + `sexo-difunto`) | 52 | 23 | 0 |
| A3 (63 reglas, 55 nuevos + `organizacion`) | 52 | 11 | 0 |
| A8 (99 reglas, 66 nuevos + `programa-educativo`) | 59 | 40 | 0 |
| A9 (121 reglas, 85 nuevos) | 116 | 5 | 0 |
| A10 (419 reglas, 398 nuevos + 5 reutilizados) | 317 | 102 | 0 |

Condicionados por categoría (significado neutro con límite, sin habilitar cruces):
- Calificadores (10 SHD + 20 sedes): NO aprobar perdiendo DDR/sede; condicionados a
  implementación central posterior (decisión del integrador, ya asumida).
- A7 DEVUELTO por integrador: `residencia-extranjero-madre` ≠ `residente extranjera`
  (par textual pendiente por contradicción); delimitar madre contextual; prueba de
  unidad como robustez, no como rechazo.
- Población inferida del contexto con límite explícito: nacido/madre (A7, con
  `(inferencia-contextual-publicada)` ya declarada por el agente), difunto implícito
  SEED, alumno/egresado (A8), beneficiado/externado/internado (A10).
- Contradicciones nombre/descripción sin deducir: NACIOEXTRANJERO (A7),
  PROGRAMADO vs binario (TIPOCESAREAD), ejemplo 99 en EDADPADRE.
- Ejemplos incoherentes con tipo: Platicas/No/Si numéricos (A9), "Bajo" (A10).
- Atributos sensibles/vulnerables: víctima/delito/internado/detenido/desaparecido,
  etnia/lengua/dialecto/grupo-indígena, discapacidad/enfermedad (A8/A10, neutros).
- Mismo concepto para literales distintos: verificar equivalencia (presa
  completa/común, clave presa, estado civil, especie/cuenca/región).
- Pares código/nombre o existencia/nombre del mismo objeto y reutilizaciones de
  mismo literal: aceptados con nota. Representación con ejemplo vacío: condicionado leve.

Correcciones de los agentes verificadas en archivo actual: edad sin afirmar años,
EDAD difunto sin momento, extranjería sin deducir lugar, `Medida: volumen` sin "o peso".

Negativos: A7/A8/A9 alimentan el validador central con entradas mutadas.
A10 usa `interpretacion()` local (matcher de tuplas, muestra de 40), no el pipeline:
señalado; esta auditoría re-ejecuta las 419 con el pipeline real (OK).

## Verificación propia (scripts read-only fuera de esta carpeta)

```powershell
uv run python -B propuestas/ronda-3/agente-11-auditoria/scripts/auditar.py
uv run python -B propuestas/ronda-3/agente-11-auditoria/scripts/verificar.py
```

OK: 777/777 positivos con pipeline real, 15 negativos con códigos esperados,
huellas estables, 0 colisiones, 0 U+FFFD, erratas y ñ preservadas, 0 sameAs/exactMatch
como predicado.

## Archivos (solo carpeta asignada)

`auditoria.json` (regla+IRI+concepto+motivos+chequeos), `propuestas.json`
(0 reglas/conceptos, SHA actual + versiones anteriores), `fuente/huellas.json`
(antes/después), `scripts/auditar.py`, `scripts/verificar.py`, `resultado.md`.

## Pendientes

1. Agente 6: fuera de esta auditoría (agente 12 + integrador). 2. Integrador: 181
condicionados (calificadores a implementación central; A7 devuelto; sensibles sin
cruces; equivalencias; ejemplos incoherentes). 3. Agente 2: candidatas (709 A3 +
pendientes A7/A8/A9/A10). 4. Suite central de 85 tests al integrador. 5. Si A7/A3/A10
vuelven a versionar, re-auditar por SHA (no es auditoría final de versiones viejas).
