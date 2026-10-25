# Plan para ampliar la cobertura semántica con Muse 1.3

Fecha: 23 de octubre de 2026. Alcance: interpretar las definiciones pendientes con evidencia documental y preparar su integración revisada. Modelo comprobado en OpenCode: `opencode-go/muse-spark-1.3-contributor`.

## Base y objetivo

El núcleo vigente contiene 1,563 definiciones: 232 respaldadas, 23 candidatas y 1,308 fuera del núcleo. Hay 103 conceptos y 836 correspondencias columna–variable revisadas. Estos son conteos de entidades distintas; ampliar significados no revisa automáticamente las correspondencias.

El objetivo es que cada una de las 1,308 definiciones tenga una decisión trazable: significado respaldado, interpretación limitada o pendiente con motivo y evidencia faltante. Las 23 candidatas se revisan por separado. El éxito no exige confirmar lo que el publicador no documentó.

## Reparto de lectura por dominio

Se aprovechan las entregas de ronda 3, con partición comprobada sin solapes:

| Responsable | Dominio | Definiciones |
| --- | --- | ---: |
| Agente 3 | Agricultura, ganadería, pesca y trigo | 66 |
| Agente 6 | Salud y vigilancia | 242 |
| Agente 7 | Registro civil | 163 |
| Agente 8 | Educación | 126 |
| Agente 9 | Gobierno digital | 243 |
| Agente 10 | Territorio, economía y restantes | 468 |
| Total | Fuera del núcleo | 1,308 |

Los agentes 11 y 12 realizan revisión independiente. El integrador aplica los cambios centrales en secuencia. Cada agente escribe únicamente en su carpeta asignada.

## Secuencia de ejecución

1. **Fijar la versión de las entregas.** Recalcular conteos desde decisiones y reglas, comprobar IRIs y huellas de fuentes y guardar un manifiesto. Algunas propuestas cambiaron después de sus auditorías; una auditoría histórica no aprueba una versión nueva. Reconciliar también resúmenes y controles desactualizados.
2. **Revisar las propuestas existentes por dominio.** Exigir definición original, recurso/diccionario, IRI de la fila, nombre, descripción, concepto, representación, límites y huella. Auditar educación, gobierno digital y territorio/economía, y volver a revisar las modificaciones de salud y registro civil. Comparar conceptos entre dominios para evitar duplicados y falsas unificaciones.
3. **Investigar las lagunas con Obscura.** Un agente investigador usa el MCP de Obscura para buscar documentación oficial: primero Sonora y el organismo publicador; después INEGI o Salud cuando corresponda. Registra URL, título, consulta, versión/periodo, pasaje breve e IRI local afectada. Una norma o catálogo nacional solo respalda la variable local si se acredita su aplicación a esa publicación. Si falta ese vínculo, queda como evidencia contextual o pendiente.
4. **Conservar el contexto en el generador.** Resolver la pérdida de calificadores antes de integrar las reglas afectadas: actualmente diez reglas de trigo distinguen distrito y veinte de educación distinguen sede. Elegir una representación explícita, conservarla hasta RDF y comprobar mediante consultas que las distinciones sobreviven. Alternativamente, usar conceptos específicos cuando corresponda.
5. **Integrar por lotes auditados.** Respaldar el núcleo, fijar las entregas aceptadas y simular su aplicación. Conservar las 232 interpretaciones y los 836 vínculos previos, salvo correcciones justificadas explícitamente. Incorporar únicamente propuestas aceptadas; las condicionadas requieren cumplir su condición y revisar la nueva versión.
6. **Comprobar el resultado y actualizar cobertura.** Ejecutar pruebas centrales, SHACL y consultas semánticas; después regenerar los informes. Para publicar en Studio, usar el procedimiento de respaldo y sincronización existente y contrastar el grafo vivo. Reportar por separado propuestas, aceptaciones, pendientes y correspondencias revisadas.

## Pruebas que deciden la aceptación

- Una regla no se aplica a otra definición, diccionario, conjunto o descripción por coincidencia del nombre.
- Municipio de residencia, registro y ocurrencia permanecen distinguibles; también las poblaciones y eventos temporales.
- Dos distritos o sedes conservan sus valores distintos en el RDF generado y en las consultas.
- No se añaden unidades, monedas, escalas, códigos de nulos, diagnósticos o equivalencias que la fuente no documente.
- La evidencia externa conserva versión y alcance; una mención a CLUES o CIE no asigna automáticamente un catálogo a una variable local.
- La suma de estados cubre cada definición exactamente una vez; nuevas interpretaciones no se cuentan como correspondencias ya revisadas.

## Resultado de la preparación

Dos sesiones existentes de Muse 1.3 prepararon inventario y plan de validación en paralelo:

- `propuestas/plan-cobertura-muse/cobertura/`: base, partición, conteos por entrega y comprobador.
- `propuestas/plan-cobertura-muse/revision/`: requisitos de auditoría, lotes y pruebas.
- `propuestas/plan-cobertura-muse/investigacion-obscura/`: investigación piloto encargada por petición posterior del usuario; consultar su evidencia y estado antes de afirmar resultados.

La instantánea del inventario encontró 980 propuestas de significado y 328 pendientes entre las 1,308 definiciones. Son propuestas sin integrar. Los archivos de ronda 3 estaban evolucionando; esos números solo describen las huellas registradas en el inventario y deben recalcularse al fijar una versión.

La revisión identificó pérdida de calificadores y auditorías que describen versiones anteriores. Sus propios totales agregados requieren reconciliación con el inventario. Ninguno de estos informes constituye aprobación semántica de las propuestas actuales.

## Estado del trabajo

La preparación del plan y el inventario están terminados; la partición de 1,308 definiciones se comprobó también desde el integrador. El piloto de Obscura consultó documentación de CLUES, municipios y CIE-10. No encontró evidencia suficiente para confirmar su aplicación a las variables locales seleccionadas ni acreditó vigencia de sus catálogos. Las referencias quedan en su carpeta de evidencia para revisión.

El plan se ejecutó con ocho roles Muse 1.3: cinco especialistas, un investigador Obscura y dos auditores independientes. Se reutilizaron las sesiones y entregas; el auditor A se reemplazó para cerrar sobre las versiones finales sin mezclar la revisión histórica. Los archivos y recibos están en `propuestas/cobertura-muse-20261023/`.

Se integraron 980 significados aceptados: el núcleo pasa de 232 a 1,212 variables respaldadas (77.5% de 1,563), con 940 conceptos. Las 328 definiciones sin respaldo suficiente y las 23 candidatas permanecen sin confirmar. El generador conserva 149 variables con calificadores en el reporte y RDF, junto con límites y procedencia. Las 836 correspondencias revisadas se preservan; las 3,312 candidatas y 12 vínculos ambiguos actuales requieren su propia revisión.

La integración dispone de evidencia fijada por SHA-256 y respaldo, 99 pruebas aprobadas y SHACL conforme sobre el grafo completo. La sincronización y las consultas de comprobación se registran en `reports/cobertura-muse.md` y sus archivos de validación. Se conserva el léxico de los calificadores al comparar las formas equivalentes de cadenas RDF 1.1. El resto de las ampliaciones de correspondencias y cruces se coordina por separado con el otro chat.
