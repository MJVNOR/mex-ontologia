# Agente 11 ronda 3 — auditoría independiente (agentes 3 y 7)

Rol: auditor. No propone conceptos ni reglas, no toca núcleo ni otras propuestas.
Solo escribe en `propuestas/ronda-3/agente-11-auditoria/`. Sin red, sin consolidar/ampliar/sincronizar.

## Base verificada (real, recalculada)

103 conceptos núcleo, 232 respaldadas, 1308 fuera del núcleo, 23 candidatas agente 4,
836 revisadas, 118 candidatas, 3 ambiguas — coincide con ronda 2 y con
`asignaciones-semanticas.json` (1242 = 1308 − 66 leídas por agente 3).
Huellas antes/después idénticas → fuentes estables, sin versión inestable.

| Archivo | SHA-256 |
| --- | --- |
| agente-7 `propuestas.json` | `f075f884…` (225732 B) |
| agente-3 `propuestas.json` | `29f1dadf…` (133579 B) |
| `cobertura.json` | `38d0e7cb…` |
| `semantica.json` | `b36ea6c6…` |
| `contenido-inspeccion.json` | `61861aab…` |
| `inventario.json` | `783f1255…` |
| `pendientes-semanticos.json` | `9294f997…` |
| `asignaciones-semanticas.json` | `360cb7f7…` |

## Dictámenes por regla

Se auditó el 100% de literales y conceptos (76 + 63), no una muestra:
IRI/fila/huella contra inspección actual, literales byte-exactos
(variable/descripción/unidad/tipo/ejemplo/catálogo), alcance simultáneo
conjunto/diccionario/definición/nombre/descripción, representación justificada
por literal, sin unidades/años/MXN inventados, sin identidad/etnia/diagnóstico
por abreviatura, sin código↔nombre sin evidencia, sin colisiones con los 103
vigentes ni entre propuestas, pipeline real (`interpretacion()`/`validar_propuestas`).

| Propuesta | Aceptar | Condicionado | Rechazar |
| --- | ---: | ---: | ---: |
| Agente 7 registro civil (76 reglas, 50 nuevos + `sexo-difunto`) | 61 | 15 | 0 |
| Agente 3 cobertura (63 reglas, 55 nuevos + `organizacion`) | 52 | 11 | 0 |

Detalle por regla en `auditoria.json` (`dictamenes_agente_7/3`: motivo + chequeos).

Condicionados A7 (significado neutro documentado con límite, sin habilitar cruces):
sujeto `nacido` inferido fuera del literal (FECHANACIMIENTO/HORANACIMIENTO);
`madre` añadida por contexto (HIJOS*, CONDICION/VIVE hijo anterior);
ejemplo `99` en EDADPADRE sugiere nulo no documentado;
`PROGRAMADO` vs binario en TIPOCESAREAD;
contradicción nombre/descripción NACIOEXTRANJERO* (neutral, sin deducir lugar);
matiz `recidente` vs `residente extranjera` en RESIDEEXTRANJERO* (confirmar o separar).

Condicionados A3: 10 SHD comparten `superficie-sembrada-trigo-ddr` con calificador
formal que `interpretacion()` no propaga — bloqueante hasta propagar el calificador
o crear 10 conceptos estrechos; `organizacion` para FUENTE (papel generadora vs
publicadora no distinguido, solo con límite).

Aceptados destacables: `edad-difunto-sin-momento-confirmado` (no adopta momento de
`edad-fallecimiento`, nomenclatura separada correcta); `sexo-difunto` reutilizado
exacto; pares código/nombre sin mapeo inventado (ORIGEN/CVORIGEN, DDR "139 CABORCA"
sin partir); PMR/rendimiento/peso-vivo con fórmula/metodología citada sin verificar
y sin homologar; TVAR con catálogo declarado ausente; 709 candidatas marcadas no revisadas.

Negativos: ambos verificadores alimentan el validador real con entradas mutadas
(códigos LITERAL_DIFERENTE, FRONTERA_AGENTE4, solo-nombre, contexto-mutado, otra-IRI);
ninguno usa funciones que se auto-lanzan ValueError. Nota: el chequeo
"unidad-faltante" de A7 es robustez (reafirma el positivo), no rechazo real.

## Concurrentes 6/8/9/10

Sin `propuestas.json` ni `resultado.md` a esta fecha (solo scripts/fuentes parciales):
6-salud (paso1/2), 8-educación (fuente+volcar), 9-gobierno-digital (vacío),
10-territorio-economía (construir). Pendiente auditar cuando entreguen.

## Verificación propia (scripts reproducibles, read-only fuera de esta carpeta)

```powershell
uv run python -B propuestas/ronda-3/agente-11-auditoria/scripts/auditar.py
uv run python -B propuestas/ronda-3/agente-11-auditoria/scripts/verificar.py
```

Ambos OK: 139/139 positivos disparan en pipeline, negativos con códigos esperados,
huellas estables, 0 colisiones duras, 0 U+FFFD, erratas y ñ preservadas, 0 sameAs/exactMatch
como predicado. Suite central de 85 tests no re-ejecutada (la cita de A3 queda al integrador).

## Archivos (solo carpeta asignada)

`auditoria.json`, `propuestas.json` (0 reglas, 0 conceptos), `fuente/huellas.json`
(antes/después), `scripts/auditar.py`, `scripts/verificar.py`, `resultado.md`.

## Pendientes

1. Auditar 6/8/9/10 cuando publiquen propuestas. 2. Integrador: 26 condicionados
(SHD bloqueante, 99/PROGRAMADO/nulos, RESIDE*/sujetos inferidos, FUENTE). 3. Agente 2:
709 candidatas A3 + pendientes A7. 4. Central: re-ejecutar suite de 85 tests.
