# Correspondencias y cruces de la ronda 3

Estado: integrado y sincronizado con Studio después del relevo semántico. El comprobante de aplicación está en `propuestas/ronda-3/integrador/aplicacion.json`; la sincronización se comprueba en `reports/studio-portal-sync.json`. Informe final: `reports/integracion-ronda-3.md`.

## Qué añade el paquete

Las 29 correspondencias relacionan columnas físicas concretas con definiciones documentales ya respaldadas. Conservan las 836 revisiones anteriores: el total comprobado es 865. Cada adición conserva recurso, columna, diccionario, descripción literal y las dos huellas. Revisar la correspondencia no equivale a validar todos los valores del archivo.

La ampliación semántica pertenece al chat «Revisar errores de la antología». Sus nuevas coincidencias por nombre permanecen candidatas hasta revisión individual. Por eso, las 89 pendientes del subconjunto revisado por el agente 2 no representan el total de candidatas de todo el portal después de esa ampliación.

## Qué permiten consultar los tres casos

| Caso | Evidencia | Interpretación permitida y límites |
| --- | --- | --- |
| F1, matrimonios y divorcios de 2022 | Recomputación desde agregados históricos por fuente; 67 códigos observados y 62 compartidos | Comparar conteos de cada fuente conservando ausencias. No calcula una tasa de divorcio, una cohorte ni identidades de personas. Los códigos no se convierten en INEGI. |
| F2, proyecciones en 2020 | Lectura de dos archivos originales fijados; 72 claves coinciden, con nombres y valores numéricos iguales | Consultar ambos valores, medidas, nombres, archivos y filas. Se sumaron hombres y mujeres antes de unir. La igualdad numérica no demuestra identidad de las medidas. Solo se cruzó 2020; la cobertura observada 1990–2040 no extiende el resultado a otros años. |
| F3, pares educativos UES | Recomputación de listas agregadas históricas por programa y sede | Comparar conteos independientes en cada periodo declarado. No calcula tasas, trayectorias o cohortes; conserva variantes de nombres y acentos sin fusionarlas. |

El triaje de 3916 pares es un inventario de revisión. No afirma que todos los pares sean comparables ni ejecuta esos cruces. La vigencia de catálogos continúa sin acreditar.

## Cómo comprobarlo

La consulta `queries/portal/cruces_ronda_3.rq`, instalada junto con el paquete, devuelve las 72 comparaciones de 2020 con dos evidencias por clave: valor, medida, nombre, SHA-256, hoja y filas. Puede filtrarse una clave manteniéndola como texto, por ejemplo `26001`.

En el chat de Studio se puede preguntar:

- «¿Cuántas correspondencias documentales revisadas hay? Distingue revisadas, candidatas y ambiguas».
- «Explica la evidencia F2 de proyecciones en 2020 y sus condiciones pendientes. No extrapoles a otros años».
- «¿Qué demuestra la igualdad de los dos valores de 2020 y qué queda sin demostrar?».

La recuperación del chat se corrigió y se instaló con respaldo. Se comprobaron las pruebas del sidecar y se repitieron seis casos de recuperación por API contra el grafo final; todavía no se verificó una respuesta del modelo desde la interfaz. No se hicieron llamadas al modelo en estas pruebas. Una respuesta debe citar las fuentes y conservar los límites del grafo.

## Trazabilidad

El paquete está fijado por SHA-256 en `data/integracion-ronda-3/manifiesto.json` una vez aplicado. La preparación aislada se conserva en `propuestas/ronda-3/integrador/paquete/`. La guardia de integración permite exactamente las 836 revisiones previas y las 29 adiciones aprobadas. No cambia conceptos, reglas, observaciones ni condiciones del núcleo semántico.

Las restricciones de cruces se comprobaron con el motor nativo: evidencia válida conforme, y rechazos por falta de huella, periodo distinto y mezcla de filas entre papeles de fuente. No se utilizan restricciones que el motor omita.
