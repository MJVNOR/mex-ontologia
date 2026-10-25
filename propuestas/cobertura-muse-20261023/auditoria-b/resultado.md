# Auditoría-b FINAL — entregas actuales salud / registro-civil / educación

SHA verificados propios contra `listo.json`: salud `39dd2c3b…`,
registro-civil `0fdfdf09…` (estable), educación `3e2df431…`.
Verificadores: `scripts/verificar_final.py` (3599 checks) +
`scripts/verificar_calificadores.py` (141 checks: 69 reglas completas →
`interpretacion()` real + triples *replicados* del patrón construir;
construir REAL: evidencia independiente
`integrador/verificacion-generador.json`).

## Dictámenes (377 reglas)

| Dominio | Reglas | Aceptar | Condicionado | Rechazar |
| --- | ---: | ---: | ---: | ---: |
| salud | 203 | 203 | 0 | 0 |
| registro-civil | 75 | 75 | 0 | 0 |
| educación | 99 | 99 | 0 | 0 |

## Delta re-auditado (12 sujetos neutralizados, etiqueta + definición)

Salud (10): `localidad-residencia`, `fecha-inicio-fiebre`,
`muestra-lcr-aspecto-agua-roca`, `resultado-bilirrubina-directa/total`,
`resultado-dhl/alt/ast`, `indicador-defuncion`,
`tratamiento-rickettsiosis` — sujeto eliminado, "sin acreditar sujeto"
explícito, significado literal intacto. Educación (2): `modalidad-cursada`,
`grado-cuatrimestre-cursado` — 'estudiante/matriculado' eliminados, dominio
y tramo conservados. Ninguna pierde significado literal → aceptar las 12.
69 calificadores: propagación ya probada; 0 str/null.

## Archivos

`auditoria.json` (esquema pedido), `resultado.md`,
`scripts/verificar_final.py`, `scripts/verificar_calificadores.py`,
`reporte_calificadores.json`, `calificadores.ttl`. Histórico de versiones:
`auditoria-fase1.json`, `auditoria-base-fase1.json`.
Fase cerrada; sin cambios de dominio hasta nueva devolución.
