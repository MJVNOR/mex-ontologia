# S2-nacimientos v001 (ronda-8-paralela/ejecucion-20261024)

22 IDs asignados, puerta `sin_pista_nueva` en los 22. Resultado: 0 propuesta_para_auditar, 22 brecha_externa.
Revision exclusivamente local (sin navegador; reservado a W). Dobles negativas verificadas por codigo:
descriptor SINAC 2020-2025 0/22 y codebook 2020-2023 (20 xlsx) 0/22 en nombres y celdas.
Expediente R7 revisado (S2 v001/v002, notas primera-puerta/w-web, W-web paquetes v001..v004 y cierres):
sin pista primaria nueva para estos IDs; no se repiten busquedas genericas agotadas.
Sin peticiones-web.json: ninguna pista nueva concreta requiere al navegador compartido.

| fila | variable | ejemplo | estado |
| --- | --- | --- | --- |
| 33 | ATENCIONPRENATALD | SI | brecha_externa |
| 35 | TRIMESTREPRIMERCONSULTAD | PRIMER TRIMESTRE | brecha_externa |
| 38 | SOBREVIVIOPARTOD | SI | brecha_externa |
| 40 | AFILIACIOND | NINGUNA | brecha_externa |
| 44 | INTERRUMPIOESTUDIOSD | NO | brecha_externa |
| 46 | CLAVEOCUPACIONHABITUALD | NO REMUNERADO, AMA DE CASA | brecha_externa |
| 60 | TAMIZAUDITIVOD | NO | brecha_externa |
| 62 | VACUNA_BCGD | SI | brecha_externa |
| 64 | VACUNAHEPATITIS_BD | SI | brecha_externa |
| 66 | VITAMINA_AD | NO ESPECIFICADO | brecha_externa |
| 68 | VITAMINA_KD | SI | brecha_externa |
| 70 | PRODUCTOEMBARAZOD | ÚNICO | brecha_externa |
| 73 | ANOMALIACIE1 | NINGUNA APARENTE | brecha_externa |
| 75 | ANOMALIACIE2 | NINGUNA APARENTE | brecha_externa |
| 78 | RESOLUCIONEMBARAZOD | CESÁREA | brecha_externa |
| 80 | UTILIZOFORCEPSD | NO APLICA | brecha_externa |
| 88 | PERSONALATENDIOD | MÉDICO | brecha_externa |
| 90 | TIPOMEDICOATENDIOD | MÉDICO GINECO OBSTETRA | brecha_externa |
| 98 | CERTIFICADOPORD | MÉDICO GINECO-OBSTETRA | brecha_externa |
| 101 | ENTIDADFEDERATIVACERTIFICAD | SONORA | brecha_externa |
| 103 | MUNICIPIOCERTIFICAD | SAN LUIS RÍO COLORADO | brecha_externa |
| 105 | LOCALIDADCERTIFICAD | SAN LUIS RIO COLORADO | brecha_externa |

## Pruebas verificables (por codigo, 2026-10-24)
- Filas: 22/22 Texto con Descripcion 'Pendiente de especificar' (lectura directa del JSON).
- Descriptor: 0/22 coincidencias exactas (barrido de celdas con openpyxl).
- Codebook zip (20 xlsx): 0/22 en nombres de archivo y en celdas (barrido con openpyxl).
- Hashes: inspeccion `76fe6822...7513b`, zip `9c7dcd52...141cb4e`, descriptor `0af0b6be...7fd6ed4`
  (completos en entrega.json; calculados por codigo).
- R7/W: S2 v001 (53 brechas) y v002 (31 propuestas + 22 brechas) mas W v001..v004 revisados;
  F-W02-SINAC-CAT ya incorporado en v002; v003/v004 sin material S2. Sin hallazgo nuevo.

## Limites
- Negativas acotadas a lo revisado el 2026-10-24; no ausencia universal.
- Fuentes nacionales citadas no sustituyen la tabla del publicador para el recurso 46977217.
- Sin joins, sin identidad de catalogos, sin vigencias inferidas.
