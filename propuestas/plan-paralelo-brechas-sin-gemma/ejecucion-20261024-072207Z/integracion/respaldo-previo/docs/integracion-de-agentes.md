# Integración de entregas de agentes

Esta guía documenta el procedimiento aplicado en las rondas 1 y 2. Python prepara el RDF y sus evidencias; Open Ontologies valida, consulta y presenta el grafo. Los archivos centrales se integran desde este chat después de revisar las entregas aisladas.

## 1. Recepción y revisión

Cada agente escribe solo en su carpeta de `propuestas/`. El integrador lee el resultado, las propuestas, las fuentes y los verificadores antes de aprobar una entrega.

La revisión comprueba:

- Identidad de conjuntos, recursos, hojas, columnas y definiciones mediante sus IRIs exactas.
- Literales originales, SHA-256 de archivos, huella del esquema completo y huella de la fila del diccionario.
- Cobertura de los ítems asignados, sin duplicados, omisiones ni solapes.
- Evidencia del significado y evidencia del vínculo entre columna y definición, registradas por separado.
- Alcance de nombres normalizados, alias, periodos, poblaciones, códigos y referencias.
- Diferencia entre comprobación completa, muestra, propuesta, incertidumbre y resultado ya integrado.

Los verificadores de los agentes se inspeccionan antes de ejecutarlos. Se contrastan también los resultados de forma independiente. Las correcciones se devuelven al agente dentro de su carpeta. Una prueba que pasa no sustituye la revisión de lo que esa prueba realmente verifica.

## 2. Respaldo y congelación de evidencia

Antes de cambiar el núcleo se guarda un ZIP de los archivos centrales pertinentes: vocabulario, scripts, shapes, pruebas, documentación, informes y grafos generados. La sincronización posterior guarda además un respaldo independiente del grafo vivo de Studio.

Se copian las entregas aprobadas y sus fuentes a carpetas centrales. Un manifiesto registra el origen y SHA-256 de cada archivo. Las carpetas originales se conservan.

| Ronda | Evidencia fijada | Configuración de integración |
| --- | --- | --- |
| 1 | `data/integracion/` | `ontologia/revision-agentes.json` |
| 2 | `data/integracion-ronda-2/` | `ontologia/revision-ronda-2.json` |

La configuración fija la huella del manifiesto y los conteos esperados. La generación comprueba las copias fijadas; no lee las carpetas originales de los agentes. Si cambia una evidencia fijada, la generación falla para exigir revisión.

## 3. Incorporación al modelo central

La aceptación y aplicación de propuestas es una etapa explícita del integrador. Los comandos de regeneración del apartado 5 no aceptan automáticamente propuestas nuevas.

- **Reglas y conceptos:** se incorporan a `ontologia/semantica.json` cuando están aprobados. Las reglas nuevas de ronda 1 quedaron restringidas por definición, diccionario, conjunto, nombre y descripción.
- **Correspondencias:** se añaden a `vinculos_documentales_revisados` con IRI física, recurso, campo, variable, diccionario, concepto, descripción, ambas huellas, criterio y procedencia de revisión. Las revisiones previas se conservan íntegramente.
- **Otras revisiones:** se generan como afirmaciones calificadas, con clases y estados propios. Un dictamen de pendiente no promueve una variable. Una comprobación de códigos no asigna automáticamente un sistema de identificadores.

El orden de generación es: núcleo semántico y correspondencias, referencias territoriales, integración de ronda 1 y después integración de ronda 2. `scripts/consolidar_semantica.py` coordina esas capas mediante `integrar_territorio.py`, `integrar_entregas.py` e `integrar_ronda_2.py`.

En ronda 2 se preservaron las 162 revisiones anteriores y se añadieron 674: 836 revisadas y 118 candidatas. Se incorporaron 32 dictámenes, 1850 comprobaciones IML/ITER y 16 revisiones de vigencia. El diagnóstico del pipeline de consulta se conservó como evaluación histórica parcial, ligada al grafo anterior; sus expectativas 162/792 no representan el estado actual 836/118.

## 4. Validación y sincronización

`scripts/ampliar_portal.py --load` regenera las capas desde las fuentes locales fijadas, las une al catálogo base, genera las shapes combinadas y carga un almacén nuevo con fecha. Valida sintaxis y SHACL y ejecuta las consultas de `queries/portal/`. Un incumplimiento de SHACL detiene esta etapa.

`scripts/sincronizar_studio_portal.py` realiza el despliegue en Studio:

1. Guarda el grafo vivo en `data/backups/studio-antes-portal-<sello>.ttl`.
2. Calcula las diferencias respecto a `data/portal/studio-managed.ttl`, que registra los triples gestionados por la sincronización anterior.
3. Prepara el grafo previsto conservando las ediciones ajenas a la ampliación y lo valida con SHACL.
4. Comprueba que Studio no haya cambiado durante la preparación; si cambió, se detiene antes de aplicar diferencias.
5. Retira los triples gestionados que quedaron obsoletos e inserta los nuevos.
6. Vuelve a guardar el grafo y comprueba que sea isomorfo al estado previsto.
7. Guarda `data/catalogo/studio-live.ttl` y actualiza el registro de triples gestionados.

Después de sincronizar se ejecutan consultas contra el motor HTTP vivo para contrastar los conteos esperados. También se verifica que las entregas originales conserven sus huellas. Las pruebas de Python comprueban, entre otras condiciones, la preservación de revisiones, el rechazo de códigos inválidos y la distinción entre diagnóstico parcial y evaluación de UI.

## 5. Regenerar el estado ya integrado

Desde la raíz del proyecto, usando el entorno Python 3.12 existente:

```powershell
uv run python -m unittest discover -s tests -q
```

Si las pruebas pasan, generar y validar el grafo completo:

```powershell
uv run python scripts/ampliar_portal.py --load
```

Si esa validación pasa, con Studio abierto y su motor disponible:

```powershell
uv run python scripts/sincronizar_studio_portal.py
```

Se ejecutan por etapas: hay que detenerse si una etapa falla. La regeneración no descarga fuentes externas ni llama a modelos. La sincronización utiliza el motor local de Studio en `http://127.0.0.1:8137/api`.

Para generar solo el módulo semántico local, sin cargar un almacén ni modificar Studio:

```powershell
uv run python scripts/consolidar_semantica.py
```

Este último comando sí actualiza los RDF e informes locales generados. La validación integral requiere el grafo completo del paso anterior.

## 6. Incorporar una ronda futura

Una nueva ronda requiere repetir la revisión y el respaldo, crear nuevas copias y manifiesto, aplicar únicamente las propuestas aprobadas, actualizar los conteos esperados y añadir o adaptar generadores, shapes y consultas cuando corresponda. Se mantienen las evidencias históricas con su alcance original.

No se debe editar una copia fijada y recalcular su huella para eludir un fallo de evidencia. Un cambio de fuente requiere revisar qué afirmaciones quedan afectadas. Los verificadores históricos de agentes pueden depender del estado central anterior; para el estado integrado se usan las pruebas centrales y las consultas vigentes.

## 7. Informes de comprobación

- `reports/integracion-agentes.md`: decisiones y alcance de ronda 1.
- `reports/integracion-ronda-2.md`: decisiones y alcance de ronda 2.
- `reports/portal-carga.json`: carga más reciente, sintaxis, SHACL, consultas y estadísticas.
- `reports/studio-portal-sync.json`: último respaldo vivo, diferencias aplicadas y validación.
- `reports/integracion-ronda-2-studio.json`: comprobaciones del estado vivo tras ronda 2, con 85 pruebas de Python aprobadas y originales conservados.
- `reports/pendientes-semanticos.md` y `.json`: cobertura y pendientes actuales.

SHACL valida la estructura del grafo. Las revisiones documentales y los contrastes de valores conservan sus propios límites: no acreditan por sí solos vigencia histórica, identidad institucional ni autorización para cruzar poblaciones.
