# A-documental — dictamen GLOBAL 188 casos (2026-10-24)

Selección revisada: `seleccion-v002.json` (sha en `dictamen.json`), 10 versiones
+ 3 paquetes web. No modificada. Totales verificados por bytes:
**188 = 31 propuesta_para_auditar + 155 brecha_externa + 2 acceso_no_resuelto.**

- **128 casos lote-1 sin cambios**: los 8 SHA de selección coinciden con lo
  auditado (S1 v002, S3/S4/S5/V1/V2 v001, S2 v002, V3 v002). No repetidos.
- **S6 v002 (5)**: 0 propuestas; 5 brecha_externa (2 desde v001, 3 sostenidas
  tras W-web paquete-v002: PROAES y SAGARHPA sin_hallazgo, con SHA). Conforme.
- **V4 (2)**: 0 propuestas; V13/V14 en acceso_no_resuelto. Auditada v004
  (final, fijada en seleccion-v002): incorpora W-v003 congelado
  (F-V003-01-SP-DL, negativo definitivo por esas vías) y cierra la rama
  pendiente de v003. Mismos estados/conteos y misma evidencia faltante
  (declaración edición/corte 2015–2025). Delta v003→v004 verificado
  inmaterial para los totales.
- **31 propuestas S2**: aceptadas en significado mínimo acotado (9 tal cual,
  22 con texto exacto en `decisiones_propuestas`); excluidos tabla
  determinada, códigos no verificados, DIAGNOSTICOS=CIE-10, 0000, EN
  OPERACION y formatos. Cero promociones de correspondencias.
- **Defectos abiertos: 0.** Lote-1 (V3 novedad) y lote-2 cerrados.

Nota: las reglas R7 se materializan aparte; aquí no se afirma nada
instalado. Pendiente la revisión concreta de aceptadas.json + código con SHA.
