# A-documental — revision inicial R8 (2026-10-24)

Solo lectura. Sin Gemma, sin mensajes externos, sin CLI puentes, sin Obscura. Escritura exclusiva en A-documental/. No edita fuentes ni entregas.

Ids auditados: 136 (M1 14 propuestas + 122 cierres motivados).
Dictamenes: 14 aceptar_propuesta_para_auditoria_AB, 122 aceptar_cierre_motivado_no_resolucion, 0 rechazos.

## Por rol (v001 congelada)

- M1-sinac: 14 ids, entrega daee9beb38cf..., marcador 5f8970264026...
- M3-anteriores: 17 ids, entrega 1be978aa6396..., marcador 4d1799a9923...
- S1-defunciones: 32 ids, entrega faef1ddf60c0..., marcador 25195b23ee1a...
- S4-epidemiologia: 25 ids, entrega 3ea6f5211d1a..., marcador 47dc9f01e4fb...
- S5-tic: 24 ids, entrega c5d934f89e23..., marcador 915ad838f484...
- S6-diversos: 5 ids, entrega 4c87d416867e..., marcador 819fce8bb579...
- V1-uth-presas: 5 ids, entrega bf684ec69e7d..., marcador 3e0bd590a8a7...
- V2-salud-anomalias: 3 ids, entrega fdbe2056205c..., marcador a88988f090bc...
- V3-coespo: 6 ids, entrega d466783413a64..., marcador 055df5651ded...
- V4-seguridad: 2 ids, entrega b49cae689e6f..., marcador 818a140dd2b9...
- X-anomalias: 3 ids, entrega 147c22f61180..., marcador 0ac9116857cf...
- W-web v001: 0 casos; disponibilidad sin navegacion nueva; nada que dictaminar por id.

## Pendientes (no auditados, no son rechazos)

- M2-sinac: sin entrega v001 al corte
- S2-nacimientos: solo trabajo/generar_v001.py, sin entrega ni congelada
- S3-matriculas: entrega v001 sin congelada.json (no auditable hasta congelar)
- T-pruebas: solo codigo v001, sin entrega ni congelada

## Herramienta comprobar.py (solo lectura)

- ids_incorrectos M1: falso positivo. La herramienta espera columna pero M1 entrega id=iri del vinculo semantico, correcto para su alcance fisico->significado. Verificacion manual: 14/14 iri coinciden con asignacion.
- M3 usa id=file-column, coherente con no-promover-sin-significado.
- Sin sha_no_coincide, sin brecha_sin_condicion, sin estado_incorrecto en lo congelado.

## Criterio por id

- Alcance: solo recurso+fila+huella o definicion local; limites niegan globalidad, joins, catalogo total, vigencias.
- Fuentes primarias: SHA-256 recalculadas por codigo, todas coinciden.
- No falsas novedades: DGIS/SINAC/DEFUN como contraste nacional con matiz explicito, no como definicion local. S1 lo declara por id. M1 no invoca DGIS como vinculo.
- Cierre motivado != resolucion. Propuesta M1 != aceptacion material (depende de S2 A/B).

## Aceptacion material

NO EMITIDA. Pendiente aceptadas.json exacto y aviso del coordinador.

Detalle por id, razon y SHAs: revision-inicial.json.
