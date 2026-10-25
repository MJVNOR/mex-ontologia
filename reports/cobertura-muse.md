# Cobertura semántica ampliada con Muse 1.3

Se revisaron las 1,308 definiciones fuera del núcleo y se integraron 980 significados respaldados. Las variables respaldadas pasan de 232 (14.8%) a 1,212 (77.5%) de 1,563 definiciones. Las 328 restantes y las 23 candidatas conservan su incertidumbre.

## Resultado de esta fase

| Medida | Antes | Después |
| --- | ---: | ---: |
| Variables respaldadas | 232 | 1212 |
| Definiciones fuera del núcleo | 1308 | 328 |
| Significados candidatos | 23 | 23 |
| Conceptos | 103 | 940 |
| Correspondencias revisadas | 836 | 836 |
| Correspondencias candidatas por nombre | 118 | 3312 |
| Vínculos ambiguos | 6 | 12 |

El aumento de candidatas es efecto de materializar las nuevas variables: no acredita sus vínculos físicos ni autoriza cruces. Los 12 vínculos ambiguos afectan seis columnas; las cinco observaciones previas y las revisiones existentes se conservan.

## Revisión por dominio

| Dominio | Definiciones revisadas | Significados aceptados | Pendientes |
| --- | ---: | ---: | ---: |
| salud | 242 | 203 | 39 |
| registro-civil | 163 | 75 | 88 |
| educacion | 126 | 99 | 27 |
| gobierno-digital | 243 | 121 | 122 |
| territorio-economia | 534 | 482 | 52 |

Ocho roles: cinco especialistas, un investigador con Obscura y dos auditores independientes. Se reutilizaron sesiones y entregas. El auditor A se reemplazó para cerrar sobre las versiones finales sin duplicar las 63 definiciones agro incluidas en territorio/economía. Las auditorías se fijaron por SHA-256 de cada entrega final; la aplicación central fue secuencial.

## Cambios que preservan significado

- 149 variables conservan calificadores documentales; su consulta devuelve 195 pares dimensión/valor. Incluyen distrito, sede, instrumento y contexto, sin convertirlos en identidades oficiales.
- Los límites y las fuentes de revisión llegan al RDF. Cada significado nuevo referencia su entrega y auditoría fijadas.
- Se distinguen índice de marginación e índice normalizado. Población reconstruida/ajustada no se homologa con proyección.
- Se neutralizaron sujetos no documentados en salud y educación, sin añadir poblaciones o unidades por costumbre.

## Investigación y pendientes

El agente investigador utilizó el MCP de Obscura en fuentes oficiales de Sonora y DGIS. La existencia de un catálogo nacional no acredita su uso por una variable local: no se promovieron significados ni se afirmó vigencia con esa evidencia contextual. Las fuentes, consultas y límites están en `data/integracion-cobertura/investigacion/`.

Los pendientes incluyen descripciones vacías o genéricas, contradicciones y códigos sin catálogo acreditado. La referencia `des_mpo_res` y la vigencia histórica de catálogos siguen sin resolver. Las decisiones individuales y sus motivos están en `data/integracion-cobertura/aceptadas.json` y los archivos `pendientes.json` por dominio. No se contactó a publicadores.

## Validación y reproducción

99 pruebas aprobadas, sin omisiones. Cubren preservación de las interpretaciones anteriores y de los 836 vínculos, alcance de reglas, calificadores en el generador real y rechazo de fuentes o manifiestos alterados. SHACL conforme, cero infracciones, sobre el grafo completo de esta fase. Studio se sincronizó con respaldo, conservación de ediciones ajenas y comprobación de isomorfismo. Se corrigió la comparación de cadenas RDF 1.1: el motor exporta xsd:string como literal simple equivalente; la recuperación verificó los recibos y conservó la propiedad de los triples ya insertados, sin repetir mutaciones. Las consultas al motor vivo comprobaron 1,212 variables respaldadas, 940 conceptos, 836 correspondencias revisadas y 149 variables calificadas.

```powershell
uv run python -m unittest discover -s tests -q
uv run python scripts/ampliar_portal.py --load
uv run python scripts/sincronizar_studio_portal.py
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_calificadores.rq
```

La generación verifica la evidencia fijada, no consulta modelos ni vuelve a navegar. Los conteos de este informe son la instantánea semántica anterior a la ampliación de correspondencias y cruces coordinada con el otro chat.

Archivos: `reports/cobertura-muse.json`, `reports/cobertura-muse-studio.json`, `ontologia/revision-cobertura.json`, `data/integracion-cobertura/manifiesto.json`. Respaldo previo: `data/backups/cobertura-antes-20261023.zip`.
