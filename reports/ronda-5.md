# Ronda 5: investigación e integración verificadas

Se investigaron los 179 significados con **10 agentes OpenCode/Muse 1.3**, búsquedas con MCP Obscura y dos revisiones independientes. Se integraron **8 significados, 3 conceptos y 8 correspondencias**. El núcleo queda en **1392 significados respaldados, 1075 conceptos y 4474 correspondencias revisadas**. Toda la base anterior se conservó.

Las **130 pruebas pasan**. SHACL nativo del grafo completo y del estado previsto de Studio termina sin violaciones; las consultas SELECT del Studio vivo confirman el resultado. Studio conserva 321209 triples, incluidas sus ediciones ajenas a la ampliación. Las tres fichas de cruce, 72 comparaciones de 2020 y 144 evidencias se mantienen.

## Resultado documental

| Grupo | Investigados | Resueltos | Pendientes |
|---|---:|---:|---:|
| Nacimientos | 54 | 1 | 53 |
| Defunciones | 32 | 0 | 32 |
| Matrículas | 30 | 0 | 30 |
| Vigilancia epidemiológica | 25 | 0 | 25 |
| TIC | 31 | 7 | 24 |
| Diversos | 7 | 0 | 7 |
| Total | 179 | 8 | 171 |

Se respaldó el indicador textual de residencia extranjera de la madre y siete campos de encuestas TIC: cinco declaraciones de sector, una lista de condiciones para innovación y la consignación textual de recursos anuales para innovación. Las reglas conservan los límites documentales: no acreditan moneda, cantidades, catálogos, identidad de medidas ni comparabilidad entre encuestas.

Se retiraron 15 propuestas iniciales de matrículas al comprobar que no tenían respaldo más allá de nombres, ejemplos o descripciones incompletas. Los reglamentos UES de 2019/2022 y la guía de titulación de 2023 aportan contexto, pero no resuelven las definiciones y códigos del recurso local de 2022. La adenda documenta además que el reglamento previo sí contiene equivalentes numéricos; eso no define los promedios ni su método.

La búsqueda ampliada atendió **33 solicitudes únicas** (34 respuestas, una repetida de presas) y preservó cinco PDF oficiales. No se localizó evidencia suficiente para acreditar la hoja de destino de `cat_estatal/Clave`, la vigencia histórica de los 16 catálogos identificados ni el catálogo aplicable a `des_mpo_res`. No se afirma ausencia universal de documentación; se registra lo revisado y la brecha exacta.

## Evidencia y siguiente dependencia

- `pendientes-ronda-5.json`: 171 definiciones con dictamen y evidencia faltante, más presas y catálogos.
- `solicitudes-publicador-ronda-5.md` y `.json`: borradores locales con los ocho casos resueltos excluidos; no se contactó a nadie.
- `data/integracion-ronda-5/`: adiciones, base y auditorías fijadas por manifiesto.
- `data/integracion-ronda-5-web/`: investigación ampliada, documentos y adenda.
- `data/integracion-ronda-5-compatibilidad/`: ajustes de pruebas históricas y manejo del archivo abierto en Windows, auditados por separado. Los manifiestos anteriores no se reescribieron.

Para resolver los 171 casos restantes se requieren definiciones completas, correcciones del publicador o vínculos documentales al recurso y periodo. Más agentes no sustituyen esa evidencia.

Gemma 4 31B permanece configurado y su ajuste está instalado. Una prueba real de F2 respondió; otras consultas recibieron HTTP500 del proveedor. El control de Studio emitió una señal de parada y se detuvieron las acciones de interfaz: **no se confirmó la activación del nuevo sidecar ni se certifica todo el chat**.
