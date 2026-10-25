# Integración de chat, correspondencias y cruces — ronda 3

La etapa quedó integrada y sincronizada con Studio el 23 de octubre de 2026. Se respetó el reparto autorizado: «Revisar errores de la antología» integró la semántica y este chat terminó el chat, las correspondencias y la evidencia de cruces después de recibir su relevo explícito.

| Resultado comprobado | Cantidad |
| --- | ---: |
| Correspondencias documentales añadidas | 29 |
| Revisadas totales, preservando las 836 previas | 865 |
| Candidatas por nombre después de la ampliación semántica | 3,283 |
| Vínculos ambiguos | 12 |
| Fichas de cruces incorporadas | 3 |
| Comparaciones nuevas de proyecciones, solo 2020 | 72 |
| Evidencias separadas por fuente para esas comparaciones | 144 |
| Triples comprobados en Studio | 284,810 |

Las reglas, conceptos, observaciones y condiciones del núcleo semántico recibido se conservaron exactamente. Continúan 1,212 significados respaldados, 940 conceptos, 328 definiciones fuera del núcleo y 23 candidatas. La ampliación y sus auditorías se documentan en [cobertura-muse.md](cobertura-muse.md); no se sustituyó su evidencia fijada.

## Qué se puede consultar

- F1: conteos de matrimonios y divorcios de 2022, recomputados desde agregados históricos por fuente. Conserva ausencias y limitaciones: no acredita tasas, cohortes, identidades ni equivalencia INEGI.
- F2: 72 comparaciones de 2020 entre grandes grupos e indicadores de proyecciones. Dos archivos originales fijados sustentan valores, medidas, nombres, SHA-256, hoja y filas de cada fuente. La suma de hombres y mujeres precede a la unión. La igualdad numérica no demuestra identidad de medidas. No se extendió el cruce a toda la cobertura observada 1990–2040.
- F3: comparaciones educativas UES por programa y sede, recomputadas desde listas agregadas históricas. Conserva periodos declarados, variantes de nombres y límites; no produce tasas ni cohortes.

La consulta [cruces_ronda_3.rq](../queries/portal/cruces_ronda_3.rq) devuelve las 72 comparaciones y ambas evidencias por clave. El triaje de 3916 pares permanece informativo y no constituye una aprobación de todos los cruces. Uso y preguntas sugeridas: [guía](../docs/correspondencias-y-cruces-ronda-3.md).

## Validación y chat

Pasaron 108 pruebas centrales y 45 pruebas del sidecar. SHACL confirmó el grafo completo y el estado final de Studio con cero infracciones y sin restricciones omitidas. Se probaron además casos inválidos en el motor nativo para rechazar falta de huella, periodo distinto y mezcla de filas entre fuentes. La sincronización conservó las ediciones ajenas al conjunto gestionado.

La corrección del chat está compilada e instalada con respaldo. Se repitieron seis casos de recuperación contra el motor HTTP vivo, incluyendo totales y preguntas por recurso; todos pasan con los conteos actuales. Las pruebas no llamaron al modelo. La respuesta del modelo desde la interfaz continúa sin evaluar: la guarda de actividad del usuario y la ventana minimizada impidieron completar esa prueba durante la instalación. No se cambió el modelo configurado en Studio.

Durante la integración se corrigió el índice de variables para conservar las siete filas sin nombre sin tratarlas como destinos con IRI. También se sustituyó el guardado directo de Turtle por publicación de un temporal completo y reemplazo después de errores de escritura al truncar archivos existentes; las pruebas comprueban que una serialización fallida conserva el archivo anterior. Los ajustes y las huellas del código instalado están registrados en el informe JSON.

## Reproducción y comprobantes

```powershell
uv run python -B scripts/ampliar_portal.py --load
uv run python -B -m unittest discover -s tests
uv run python -B scripts/sincronizar_studio_portal.py
```

La generación no vuelve a consultar fuentes ni ejecuta llamadas al modelo. La sincronización requiere Studio abierto, respalda su estado y comprueba que no cambie durante la operación. No se debe repetir el aplicador inicial sobre una ronda ya instalada.

La guardia de cobertura permite exclusivamente las 836 correspondencias anteriores y las 29 adiciones fijadas, sin permitir otros cambios de vínculos. Las expectativas actuales de las rondas anteriores se actualizaron conservando sus conteos históricos.

- Evidencia fijada: `data/integracion-ronda-3/manifiesto.json`, SHA-256 `c926c28467a499ff72ed626da8014cc6c642c31f7760ca25cffa4ad1d6782dff`.
- Respaldo central previo: `data/backups/antes-ronda-3-20261023T113720Z.zip`.
- Respaldo previo a sincronización: `data/backups/studio-antes-portal-20261023T114604995444Z.ttl`.
- Resultado completo: [integracion-ronda-3.json](integracion-ronda-3.json).
- Controles vivos: `propuestas/ronda-3/integrador/control-studio-final.json`.
- Aplicación y copia del código instalado: `propuestas/ronda-3/integrador/aplicacion.json` y `codigo-instalado/`.
- Reparto entre chats y sesiones Muse: [orquestación](../docs/orquestacion-ronda-3.md).
