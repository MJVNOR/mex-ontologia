# B-tecnica — compatibilidad R7 (2026-10-24)

Dictamen staging compatibilidad-v002: **aceptar**. 3 defectos
documentados (D1/D2 resueltos en v001; D3 de v001 corregido en v002).

## Defectos concretos (scripts en arbol, pre-staging)

- D1 `scripts/integrar_entregas.py:312-326`: esperado solo-R6
  (conceptos 1075, respaldadas 1392, pendientes 19, revisadas 4475).
  Con R7 vivo (1106/1423/4478) levanta `ValueError`. El parche R6
  existente solo cubria revisadas=4475.
- D2 `scripts/integrar_ronda_2.py:306-316`: revisadas 4475→4478,
  candidatas 20→17. Mismo `ValueError`.

## Staging: aceptado (v002)

Rama R7 solo tras bloque R6, deriva de baseline R6 + `aceptadas.json`
auditado con lote exacto 31/3/31 y pines de doble via
(1106/1423/4478/140/17). Anclas historicas intactas; ningun observado
como esperado (el resumen vivo solo entra en invariante de
conservacion); sin `except` nuevos; SHAs verificados en congelada.
Reserva: el gate dual-aceptar vive en `integrar_ronda_7.construir`;
no relajar a corridas parciales del script suelto.

## D3 (v001, coordinador; corregido en v002, congelada v001 intacta)

Tupla `(n_reglas,n_vinc,n_con)` comparada contra `(31,31,3)` en ambos
archivos; lo correcto es `(31,3,31)` — con el lote real siempre
fallaba. v002 la corrige y reduce el bloque de entregas (cadena
historica `cargar()` primero; fidelidad por regla en `construir`
fase R7). Verificado ademas: `sources.update` valido (`sources` en
scope en ambas `construir`, cero `source_files`); R6cfg trae
`estados_variables_esperados` (1392/152/19, el codigo falla si falta);
delta v001→v002 solo tuple+mensaje+reduccion.

## Sin bloqueo (verificado)

Rondas 3/4/5/6 (base+delta exactos), cobertura y consolidar
(estructurales), ampliar/sincronizar (sin conteos).
`depurar_pendientes.py:145-147` hardcodea R6 pero es standalone
verificado (sin importadores): no bloquea, no tocar.
Tests solo R6-aware: fuera de alcance, pendiente CI.

Sin instalar, sin tests, sin alterar manifiestos ni Gemma.
Validacion historica y delta exacto mantenidos.
