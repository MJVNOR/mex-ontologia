# Investigación documental posterior a R6

Se investigaron **169 significados** con seis agentes OpenCode en paralelo (`opencode-go/muse-spark-1.3-contributor`). Siguen pendientes 169; propuestas activas: 0. No se integraron promociones.

| Fuente | IDs examinados | Informe |
| --- | ---: | --- |
| diversos | 5 | [Evidencia y dictámenes](../propuestas/investigacion-post-r6/diversos/entrega.md) |
| epidemiologia | 25 | [Evidencia y dictámenes](../propuestas/investigacion-post-r6/epidemiologia/entrega.md) |
| matriculas | 30 | [Evidencia y dictámenes](../propuestas/investigacion-post-r6/matriculas/entrega.md) |
| salud-defunciones | 32 | [Evidencia y dictámenes](../propuestas/investigacion-post-r6/salud-defunciones/entrega.md) |
| salud-nacimientos | 53 | [Evidencia y dictámenes](../propuestas/investigacion-post-r6/salud-nacimientos/entrega.md) |
| tic | 24 | [Evidencia y dictámenes](../propuestas/investigacion-post-r6/tic/entrega.md) |

Cada dictamen conserva el texto original, la evidencia examinada, su vínculo con el recurso local y el obstáculo concreto para la promoción. Las búsquedas negativas se limitan a las fuentes consultadas; no prueban que la documentación no exista.

## Revisión independiente

- [auditoria-salud](../propuestas/investigacion-post-r6/auditoria-salud/dictamen.json)
- [auditoria-otros](../propuestas/investigacion-post-r6/auditoria-otros/dictamen.json)
- [auditoria-educacion-tic](../propuestas/investigacion-post-r6/auditoria-educacion-tic/dictamen.json)
- [auditoria-clasif](../propuestas/investigacion-post-r6/auditoria-clasif/dictamen.json)

## Resultados y límites

- **Defunciones:** examen por ID de las 32 variables contra el manual SEED Modelo 2022, con pregunta y página. Se distinguen certificados generales y fetales; persisten obstáculos de correspondencia formal, códigos o ámbito por variable.
- **Nacimientos:** contraste de las 53 variables con documentación SINAC y fuentes primarias preservadas; la documentación examinada no acredita la definición o edición aplicable a cada campo local.
- **Matrículas:** revisión del archivo 2022-2, sus distribuciones y documentación UES adicional. Los valores observados y normas de otras ediciones no acreditan por sí solos el significado y representación de los 30 campos.
- **Epidemiología y TIC:** se conservan fuentes e intentos nuevos de consulta, junto con el documento o vínculo concreto que aún falta por campo.
- **CLASIF:** se confirmó que las 2129 filas del archivo local coinciden por clave y en sus 28 campos con el extracto Sonora del producto CONAPO 2020. Esa evidencia acredita procedencia; los diccionarios local y nacional siguen diciendo únicamente «Clasificación». Se rechazó la glosa «tipo de asentamiento» por falta de fuente explícita. Los 38 valores nacionales son observados, no un catálogo cerrado. No se promovió un concepto tautológico ni se autorizaron cruces.
- **Vías limitadas:** se registran fallos HTTP y documentos que no pudieron examinarse. El RAR de cálculo CONAPO pudo extraerse con tar.exe de Windows y su programa se examinó como texto, sin ejecutarlo; no aportó una definición de CLASIF.

## Estado preservado

Se mantienen 1392 significados respaldados, 1075 conceptos, 4475 correspondencias revisadas, 20 candidatas y cero ambiguas. Las 16 brechas de vigencia y la anomalía heredada `des_mpo_res` siguen en su matriz previa. Se conservan los dos encabezados corruptos fuera de esta vista de investigación.

Se cotejaron 122 referencias locales con SHA-256, los originales de los 169 registros y los 12 archivos base. No se contactó a publicadores ni se modificó Studio o el chat. El código preparado para una eventual R7 permanece en staging, marcado para no aplicar.

[Detalle completo, decisiones y hashes](investigacion-post-r6.json).
