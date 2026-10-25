# Revisión técnica independiente inicial — B-tecnica

Expediente: `propuestas/ronda-8-paralela/ejecucion-20261024`.
Solo lectura de producción. Escritura exclusiva en `B-tecnica/`.
Sin Gemma, sin mensajes externos, sin puentes CLI. Modelo Muse 1.3.

## 1. Producción R7: intacta

- `base.json` pins: **0 mismatches**. Vivo == base == `reports/ronda-7.json`:
  `respaldada 1423 / fuera 124 / candidata 16 / revisadas 4478 / candidatas 45`.
- Cadena `integrar_ronda_4 <- R5 <- R6 <- R7` delega (no reemplaza); `validar(rules)` OK.
- Sin duplicados: 1307 reglas, 4478 vínculos, ids/columnas/definiciones únicos.
- R7: 31 reglas + 3 vínculos + 31 conceptos; doble `aceptar` A+B con
  `aceptadas_sha256=0d58255d…` pinnado en ambas auditorías (34 dictámenes c/u).
  `manifiesto.json` insumos `{}` (vacío de origen, consta).

## 2. Suite inicial: 142 tests, 6 fallos — deuda de tests, no corrupción

`propuestas/suite-r7-inicial.log`: los 6 fallos son una sola causa raíz —
los tests viejos desconocen el delta R7 y esperan `1392/4475/836`:

- `test_cobertura_integrada` x3 (conteos, preservados, condicionados).
- `test_integracion_agentes` x1, `test_ronda_2` x1, `test_ronda_3_integrada` x1
  (`4478 != 4475`: falta sumar `+r7n`).

## 3. Staging T-pruebas v001: corrección correcta, sin congelar

- Patrón correcto: deriva R6/R7 de `aceptadas.json` de sus manifiestos
  (`promoted_ids`, `r7n`, base-cobertura R5); no hardcodea 1423/4478.
  Literales restantes (`1308/1563/836/865`) son invariantes históricos admitidos.
- Nuevo `test_ronda_7.py` (12 tests): manifiesto, doble aprobación SHA,
  extensión exacta sobre base R6, deltas cruzados, materialización+RDF,
  scope cerrado, pendientes conservados, negativas, hook R8. Sólido.
- Ejecución directa `uv run python <archivo>`: cobertura (4) OK,
  integración OK, ronda-2 OK, ronda-3 OK, ronda-7 (12) OK.
- **Defectos menores / a declarar**: `fijar-raiz.py` no toca
  `test_dictamen_historico.py` ni `test_seleccion_documental.py`
  (sin `ROOT`/`sys.path`; dependen de `PYTHONPATH=scripts` del corredor —
  igual que en producción, donde también fallan en directo).
  `test_ronda_7.py` cambió durante esta revisión
  (`assertTrue(insumos)` → `assertIsInstance(insumos, dict)`): staging vivo,
  sin `entrega.json/md` ni `congelada.json` (correcto por ahora).

## 4. Integrador R8: pendiente

Sin carpeta/entrega I-*; solo `seguimiento-chat.json` con session/job
del integrador. Nada que dictaminar hasta que exista entrega.

## 5. Auditoría pedida

- Conservación histórica / huellas / aprobaciones: OK (arriba).
- R8 delegación antes que igualdad R7: la cadena actual delega;
  el hook `test_r8_hook_por_deltas_aprobados` ya exige sumar el delta
  aprobado de R8 cuando exista, nunca el vivo contra sí mismo.
- Compatibilidad R1/R2 sin bloques duplicados: OK, 0 duplicados.
- Sin usar observados como expected: OK en staging (solo invariantes históricos).

## 6. Correcciones pedidas al coordinador (no edito autor)

1. **T-pruebas**: congelar versión (fijar hash de `v001/codigo/tests/`)
   antes del dictamen final; la evolución durante la revisión invalida el pin.
2. **T-pruebas**: declarar corredor oficial (¿`PYTHONPATH=scripts`?) o cubrir
   `test_dictamen_historico.py` y `test_seleccion_documental.py` en
   `fijar-raiz.py`; hoy solo fallan fuera del corredor, igual que producción.
3. **T-pruebas**: aportar log de suite staging completa (142 + nuevos R7)
   con el corredor oficial; mi verificación directa es parcial por archivo.
4. **T-pruebas**: aclarar si `insumos: {}` vacío en manifiesto R7 es
   esperado o debe documentarse; el test actual solo exige `dict`.
5. **Coordinador**: avisar cuando exista entrega del integrador R8
   (carpeta I-*/`entrega.json` + `congelada.json`) para revisarla;
   mientras tanto no hay dictamen R8.
6. **Coordinador**: el dictamen exacto por vínculo/propuesta con SHA
   aceptadas queda para después del cierre, como está previsto;
   este informe no congela ni integra nada.

## Veredicto inicial

Producción R7 íntegra y aprobada; 6 fallos = tests viejos sin hook R7.
Staging T v001 va por el patrón correcto y su test R7 nuevo es sólido;
falta congelar + declarar corredor. R8 sin entrega. No se editó
producción ni ningún otro folder.
