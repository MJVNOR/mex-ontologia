# Resultado salud (ronda 6)

Asignados: 85 (53 nacimientos SINAC + 32 defunciones SEED). Decisiones: 0 proponer, 85 pendiente, 0 artefacto_documental.
Reglas nuevas: 0. Conceptos nuevos: 0. Vinculos: 0. Columnas: 0.
Solicitudes web: 4 (SAL-R6-01 a SAL-R6-04, IDs nuevos; no se reutilizan nac-web-*/SW-D*).

## Novedad R6 respecto de R5 (linea nueva, negativa acotada)

- R5 dejo 53+32 pendientes por descripcion 'Pendiente de especificar' y sin vinculo local; nada de ello se repite como hallazgo: huellas 85/85 recomputadas y datastore live 2026-10-23 confirman que las filas siguen sin descripcion.
- R6 verifico por CLI el vinculo local declarado (package_show CKAN 2026-10-23): nacimientos declara 'Subsistema de Informacion sobre Nacimientos' con periodo 2022-01-01 a 2022-09-26; defunciones declara titulo SEED con periodo 2022-01-01 a 2022-09-22. Ambos con version=null, url=null, fuentes_extras='': sistema+periodo si, edicion no (F4 ausente).
- R6 descargo el Manual SEED Modelo 2022 DGIS (HTTP 200, URL final identica, Content-Type application/pdf, magia %PDF-, 11717771 B, sha256 698ee48a...29b74f4, listado en la pagina oficial SEED-DGIS): cubre SITIO/CLUES/parentesco-del-informante/edad-gestacional-fetal y menciona CIE-10 una vez, pero nombra 'Sonora' cero veces y el publicador no lo vincula a los recursos 2022; no acredita codigo local ni vigencia. No se propone por nombre (parentesco-informante != PARENTESCOAGRESORD).
- SINAC: la pagina DGIS (ago-2023) no enlaza manual de nacimiento alguno; el Manual Modelo 2015 ya revisado en R5 sigue sin vinculo de vigencia a 2022 y la Guia Modelo 2025 es post-periodo. Manual 2015 y CLUES/CIE vigentes no se reutilizan (fuera de periodo).
- 85 pendientes confirmados con documento exacto necesario, todo en manos del publicador (ver entrega.json -> pendientes). No se aprueba por nombre; no se inventa definicion.

## Verificacion

- Huellas de fila recomputadas con huella() de scripts/consolidar_semantica.py: 85/85 OK.
- Fuentes con SHA recomputado desde bytes en este script (no transcritos).
- Reglas, conceptos y vinculos: 0 (sin colisiones que verificar).

## Archivos

- entrega.json, solicitudes-web.json, resultado.md, listo.json, construir.py, evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf, evidencia/package_nacimientos.json, evidencia/package_defunciones.json
- sha256(entrega.json) = c598972e85c3ef9a94c24c528e6c45c45fd005c87d6c73275755130251f89687

