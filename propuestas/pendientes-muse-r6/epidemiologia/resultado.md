# Resultado epidemiología (ronda 6)

Asignados: 25. Decisiones: 0 proponer, 25 pendiente, 0 artefacto_documental.
Reglas nuevas: 0. Conceptos nuevos: 0. Vínculos: 0. Columnas: 0.
Solicitudes web: 3 (EPI-R6-01 a EPI-R6-03, IDs nuevos; no reutilizan SW-EPI-*).

## Novedad R6 respecto de R5 (línea nueva, sin repetir negativos)

- Metadatos frescos 2026-10-23 del package (evidencia/metadatos_r6.json): sin cambios vs R5. Fijan la edición aplicable: recurso 'Vigilancia Epidemiológica - 2022' (2022-01-01/2022-12-31, 3475599 B, Inteligencia de Datos, Caborca/Cajeme/Hermosillo/Navojoa/Santa Ana); diccionario CSV 2024-10-31; fuentes_extras vacío, sin nota metodológica.
- Estructura física SUIVE (59 campos, posiciones verificadas): serie edad 12+12 en espejo exacto (pos12-23 sin sufijo / pos24-35 con sufijo f, salvo de65_y_mas→de65_y_maf); bloque institucional pos36-44 (ssa, imss_ord, issste, otras, imss_sol, d_if, pemex, sedena, sedemar); bloque mensual pos45-56 + periodo/totalm/totalf pos57-59. totalm/totalf ('Total acumulado de Hombres/Mujeres') es el único 'acumulado' con objeto+partición; no define acumulado pos11 ni el sufijo f.
- Manual SUIVE 32 solo contexto + corrección: SHA correcto desde bytes f35746a0353c902b03d8ae01f703d1dfafdf3ad4bbf01777b648353d1b833757 (64 hex); el citado en R06 tenía 62 y era errata. Last-Modified 2021-08-10 precede al periodo 2022 y no hay vínculo edición-recurso-periodo: no acredita ninguna columna local.
- Reintento CLI directo del xlsx 2026-10-23 → HTTP 403 Cloudflare; sin evadir WAF. Se reutiliza la inspección previa 2026-10-23 como contexto, no como descarga nueva.
- Huellas de fila recomputadas con huella() de scripts/consolidar_semantica.py: 25/25 OK; base R6 intacta (cobertura.json coincide con base.json).
- 25 pendientes confirmados con documento exacto necesario, todo en manos del publicador (ver entrega.json → pendientes). No se aprueba por nombre; no se inventa definición.

## Verificación

- Fuentes con SHA recomputado desde bytes en este script (no transcritos).
- Reglas, conceptos y vínculos: 0 (sin colisiones que verificar).

## Archivos

- entrega.json, solicitudes-web.json, resultado.md, listo.json, construir.py, evidencia/metadatos_r6.json
- sha256(entrega.json) = c105170dc193f44edf9e648b8f9dbc85251f8509ab1a9644e92adf3f719c7bed

