# Auditoria compatibilidad R7 v003 — aceptar

Solo lectura, sin instalar, sin Gemma, sin pruebas. Adaptadores R1/R2 para regeneracion; manifiestos R7 ya integrados.

- Unico bloque R7 por file (`if r7cfg.exists()` entregas L321, ronda_2 L315).
- `sha()` definida en ambos (entregas L20, ronda_2 L18).
- Backup cov pin real: literal `ea354f8a…0d5cd` + `sha(bkcov)==pin.get(...)`; particion 3+28, viejas 17, nuevas 28, 45, 4523, fuera 124, 1423+124+16.
- Fuentes inmutables: SHA + `is_relative_to` + reverificacion encabezado/filas/claves.
- Baseline accepted cadena exacta R6→R7: `r7base == r6base + r6accepted` + conceptos preservados; lote 31/3/31.
- No observados como expected: expected de base+accepted+pre_var+viejas/nuevas; resumen solo en `actual`.
- Expected real R7: 1423/1106/16/124 (140=138+2 headers); 4478/45 (17+28); 3/31/31.

Pins: congelada `b0c9774d…ed58bf`, entregas `b32380be…08685`, ronda_2 `97e2f845…aca90`.
