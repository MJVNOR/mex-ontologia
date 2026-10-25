# S1-defunciones v001 — revisión local R8 (sin material nuevo)

Rol: S1-defunciones. 32/32 IDs. **0 propuestas; 32 brechas externas.**

## Método

- Revisión exclusivamente local 2026-10-24, sin Obscura (reservado a W-web), sin búsquedas genéricas repetidas.
- Expediente R7 revisado: S1 v001/v002 (entrega, trabajo/registro-primera-puerta.json, registro-reevaluacion-v002.json, peticiones-web.json S1-WEB-01); W-web paquete + v002 + v003 + v004 (fuentes/disponibilidad/congeladas) y cierres (cierre.json, cierre-r7.md).
- S1-WEB-01 ya atendida sin hallazgo (F-V002-05: página datos/defunciones cascarón + PowerBI, sin ámbito/fuente/periodo). Sin pista primaria nueva concreta: no se emite peticiones-web.json.
- Evidencia citada ya examinada en R7; se re-verifica por lectura/SHA local, no se presenta como hallazgo nuevo.

## Por qué cero promociones (criterio correspondencia formal suficiente)

1. Ningún identificador local coincide exactamente con un mnemónico nacional (alias universal: EDADGESTACIONAL vs sem_gest, AFILIACION vs derechohab, etc.). La coherencia interna de valores (2<->IMSS en /34-/35, 2=No, 8=No aplica) no es vínculo formal: se exige tabla columna<->campo del publicador o fuente primaria que acredite el vínculo al recurso 6f39fc5d.
2. Recodificación local probada invalida suponer la codificación nacional: /30 ejemplo 4 (1 dígito) fuera de ocupacion.csv nacional (57 filas, 3 dígitos); /72 997 fuera de mun_ocurr/mun_ocules; /74 9997 fuera de loc_ocurr/loc_ocules.
3. Horquillas no resueltas por el instrumento: fallecido vs madre (/32-/35), defunción vs lesión/expulsión (/36-/37, /70-/75), triple campo de embarazo (/63-/64), doble certificado (/76-/77), representación 1 Fecha local vs 3 campos nacionales (/78), ausencia total nacional (/38 sin campo, /79-/80 sin campo ni pregunta).
4. Sin codebook/tabla/edición del publicador para el recurso 6f39fc5d (2022-01-01 a 2022-09-22). package_show sin cambios y s_clues.html negativo ya constatados en R7; no se repiten.

## Pares estructurales

Sin propuesta documental; los IDs ligados a pares candidatos permanecen par_estructural_revisado_significado_pendiente.

## Archivos

- v001/entrega.json (32 decisiones, SHA por código)
- v001/entrega.md (este archivo)
- v001/congelada.json (SHA de los dos anteriores)
