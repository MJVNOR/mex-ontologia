# Integración central — ronda 2 (antecedente histórico)

Los conteos de las tablas describen el cierre original de ronda 2. La cobertura vigente se registra en reports/consolidacion-semantica.md y data/semantica/cobertura.json.

Las cinco entregas se conservan como copias fijadas por SHA-256. Las carpetas originales no se modifican. La generación es sin red ni modelos.

| Resultado | Cantidad |
| --- | ---: |
| Nuevas correspondencias documentales | 674 |
| Correspondencias revisadas totales | 836 |
| Correspondencias candidatas restantes | 118 |
| Columnas ambiguas / vínculos | 3 / 6 |
| Conceptos / variables respaldadas / significados candidatos | 103 / 232 / 23 |
| Dictámenes de pendientes / preguntas sin enviar | 32 / 14 |
| Coincidencias IML con ITER 2020: clave, nombre y población | 1850 |
| Localidades publicadas solo en ITER | 5450 |
| Revisiones de vigencia no acreditada | 16 |

## Alcance por entrega

- Agente 1: se conservan las 162 revisiones anteriores y se añaden 674. Las 21 diferencias por acento agudo se documentan por recurso. Año/ano permanece pendiente; no se crean alias globales ni conceptos nuevos. La revisión documental no valida valores ni vigencia.
- Agente 2: 32 dictámenes calificados (23 requieren aclaración, 8 documentados con límite y un caso ya resuelto). Las 14 preguntas están preparadas, sin contactar al publicador. Los significados candidatos y las observaciones originales permanecen; los dictámenes no son promociones.
- Agente 3: contraste completo de dos fuentes publicadas. Se separan 75 agregados y 125 especiales de 7300 localidades ITER; las 1850 claves IML tienen nombres y población idénticos, sin transformaciones. Se integra una comprobación por localidad, no identidad oficial ni asignación a otros conjuntos. ITER declara 2020-03-15; IML declara año 2020. El motivo de las 5450 exclusiones no queda acreditado y no se cotejó el Marco Geoestadístico.
- Agente 4: 16 revisiones de aplicabilidad temporal no acreditada, con fechas CKAN, periodos declarados, edición y aplicabilidad separados. Se conserva la evidencia primaria CMPE 2016 sin atribuir adopción por periodo ni vigencia a UTH. No_acreditada no significa inválida.
- Agente 5: diagnóstico histórico PARCIAL del pipeline fuente contra el grafo vivo previo a esta integración: 20 intentos, 4 respuestas (2 aciertos y 2 fallos de recuperación), 16 intentos con error HTTP/cuota. UI no evaluada; identidad con el backend instalado no demostrada. No se relanzaron modelos ni se corrigió el chat. Las expectativas y consultas guardadas conservan los conteos anteriores 162/792; son evidencia histórica, no los conteos actuales.

## Reproducción y pendientes

ontologia/revision-ronda-2.json fija data/integracion-ronda-2/manifiesto.json. scripts/ampliar_portal.py --load regenera y valida el grafo; scripts/sincronizar_studio_portal.py respalda y conserva las ediciones ajenas a la ampliación.

Al cerrar esta ronda quedaron 23 significados candidatos, 118 correspondencias candidatas, 3 columnas ambiguas/6 vínculos, des_mpo_res sin resolver, vigencia histórica no acreditada y pruebas pendientes de UI/16 preguntas sin respuesta. Entonces 1308 definiciones estaban fuera del núcleo; las ampliaciones posteriores se documentan en la cobertura vigente. Esta ronda no ejecutó nuevos cruces ni creó owl:sameAs/skos:exactMatch.

Respaldo central previo: data\backups\integracion-ronda-2-20261023T100302Z.zip
