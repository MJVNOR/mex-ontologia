# Validación y ejecución por lotes

El primer lote procesa exactamente los 98 pares con prioridad `revisar_primero` del mapa existente. Los clasifica sin modificar su estado original de oportunidad: la nueva decisión se registra en `mex:ValidacionLote`. Esto conserva la distinción entre detectar, diagnosticar y ejecutar un cruce.

## Resultado de esta ejecución

| Decisión | Pares |
| --- | ---: |
| Ejecución parcial exploratoria | 2 |
| Requiere transformación o catálogo | 53 |
| Requiere revisión | 41 |
| Falló alguna condición de la estrategia integral, sin ejecución | 2 |

El diagnóstico muestral cubre un recurso con claves observables de cada uno de los 51 conjuntos involucrados. Seleccionar un recurso no valida sus otros recursos o años. Se lee hasta 100 filas por API o hasta 30 filas de una hoja; se conservan estadísticas y valores de claves/estratos, sin filas personales. Las comparaciones de muestra indican coincidencias textuales y ausencias, no equivalencias, unicidad global o incompatibilidad definitiva.

La validación integral se intentó en 20 recursos del Registro Civil y cuatro archivos educativos completos. Doce recursos del Registro Civil y los cuatro educativos superaron sus condiciones. Los ocho recursos de Nacimientos no las superaron: seis presentan casos donde `total` no coincide con `hombres + mujeres`; dos carecen de alguno de los 12 meses por municipio. Eso exige revisar el contenido o su definición; no autoriza corregir la fuente ni interpretar ausencias como cero.

Ejemplo registrado: Nacimientos 2022, fila `_id=34`, municipio local 3, mes 12, hombres=10, mujeres=10 y total=21. No se infiere la causa de la diferencia. Estos recursos no producen agregados anuales en esta estrategia. Defunciones no se cruza automáticamente usando su año de fallecimiento como si fuera año de registro.

## Comparaciones educativas ejecutadas

- Titulados–Egresados UES: periodo **declarado** 2020–2021, 175 claves programa/sede y 54 con valores numéricos en ambas fuentes.
- Nuevo ingreso–Reingreso UES: periodo **declarado** 2021–2022, 165 claves programa/sede y 59 con valores numéricos en ambas fuentes.

En total se conservan 340 claves; 113 tienen valores numéricos en ambos indicadores. Las demás incluyen programas sin correspondencia textual o celdas sin valor publicado. Un cero explícito se conserva como cero. Las claves se comparan dentro de la misma institución, normalizando solo espacios y mayúsculas; diferencias de acentos, abreviaturas o palabras quedan sin homologar.

Los cuatro archivos se leyeron completos con límites de bytes/filas. Se exigieron encabezados y definiciones de número de estudiantes por sede, programas únicos tras normalización, valores enteros no negativos y, si existe, concordancia de la fila de totales. Se transformó la matriz de sedes en registros de programa/sede antes de unir, con grano único. No se multiplican filas ni se rellenan ausencias.

El periodo procede de metadatos coincidentes de los recursos; no está verificado con fechas de registros. Se comparan indicadores independientes: no se identifican estudiantes, cohortes ni tasas de titulación, permanencia o egreso. Los totales resumen valores conocidos, sin completar vacíos. Los promedios académicos no se suman ni se promedian sin ponderadores.

Resultados: [resultados-lote-educacion.md](../reports/resultados-lote-educacion.md). Decisiones de los 98 pares: [validacion-lote-cruces.md](../reports/validacion-lote-cruces.md).

## Catálogos y correspondencias

Se extrajeron 72 referencias municipales del GeoJSON del portal. Se verificó internamente que `CVEGEO = CVE_ENT + CVE_MUN`, entidad 26, códigos municipales 1–72 y consistencia de los nombres por código. Esta es una referencia publicada en el portal; no es una validación independiente del catálogo ni prueba que los códigos de otros conjuntos tengan el mismo significado.

No se asignan nombres de esa referencia a códigos locales del Registro Civil por mera coincidencia numérica. Las correspondencias de localidades, CLUES, programas y clasificaciones sectoriales siguen explícitamente pendientes donde no hay evidencia suficiente. Las 53 decisiones de transformación/catálogo y las otras 41 de revisión no están aprobadas para ejecución automática.

## Reproducir y actualizar

```powershell
uv run python scripts/validar_lote_cruces.py
uv run python scripts/ampliar_portal.py --load
uv run python scripts/sincronizar_studio_portal.py
uv run python scripts/consultar_catalogo.py --portal queries/portal/lote_resumen.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/lote_educacion.rq
```

Ejecutar el siguiente paso solo si el anterior termina correctamente. El mapa debe corresponder al inventario e inspección actuales. `--refresh` vuelve a consultar muestras, agregados y referencia municipal; `--retry-errors` reintenta fallos integrales de API. Sin esos indicadores se reutiliza evidencia fechada. No hay consultas programadas ni monitor.

Después de regenerar el mapa de oportunidades se regenera también el lote, aunque sus muestras puedan reutilizarse. La ampliación comprueba sus huellas y se detiene si el lote está desactualizado. El almacén generado es nuevo y la sincronización de Studio respalda el estado previo y conserva ediciones ajenas.

Evidencia completa en `data/portal/lote-cruces/validacion-lote.json`, `muestras/`, `agregados/` y `catalogo-municipal-portal.json`. Las URLs, fechas, errores y huellas de los campos procesados quedan registradas; no se guardan archivos fuente completos ni microdatos personales.

## Validación del software y del grafo

43 pruebas verifican, entre otras cosas, que se sumen nacimientos en lugar de contar filas, que falle la estrategia ante totales inconsistentes o meses ausentes, que no se unan agregados fallidos, que no se multipliquen filas por grano duplicado y que los vacíos no se conviertan en cero. Las pruebas también impiden mezclar periodos educativos distintos.

SHACL valida decisiones, ejecuciones, resultados educativos y referencias municipales, además del modelo anterior. La regla de resultados municipales del lote puede aparecer sin entidades objetivo: no se ejecutaron nuevos cruces municipales al fallar las condiciones de Nacimientos. Eso es una regla sin casos aplicables, no una infracción ni una aprobación de esos recursos.
