# Ronda 7 — NO_APLICAR / SIN_PROPUESTA_APROBADA (staging cerrado sin efecto)

Decisión del integrador: **no habrá promoción CLASIF** — ninguna fuente explícita
fija el objeto de la clasificación; la coincidencia 2129×28 acredita procedencia
pero el significado genérico no resuelve la brecha. Código preparatorio en esta
carpeta, sin instalar, sin integrar, sin efecto sobre históricos/semántica/
manifiestos/Studio/tests. Historial de la tarea preservado aquí.

Solo prepara código en `propuestas/investigacion-post-r6/integracion-staging/`.
No instala, no integra, no edita históricos/manifiestos/semántica/Studio/tests.

## 1. Qué hay hoy (cadena R4→R5→R6)

- `scripts/integrar_ronda_4.py:validar()` construye expected-R4; si existe
  `ontologia/revision-ronda-5.json` delega a R5, si no compara exactitud.
- `scripts/integrar_ronda_5.py:validar_sobre_base()` (orden correcto, fallo R5 ya
  corregido): verifica `baseline == R4 validado`, construye expected, valida
  duplicados + aprobaciones + orígenes fijados por manifiesto, **luego delega a R6
  si existe su config, si no compara** `rules != expected`.
- `scripts/integrar_ronda_6.py:validar_sobre_base()` hace lo mismo pero en orden
  inverso: compara exactitud **antes** de validar duplicados/aprobaciones y no
  delega (no hay R7). Al extender, aplicarle el mismo cuidado que a R5.
- `scripts/consolidar_semantica.py:generar()` encadena construir R4/R5/R6 por
  separado; `scripts/ampliar_portal.py` lo incorpora. R4/R5/R6 no tienen shapes
  propios (solo ronda-2/3 tienen `.ttl`), así que no hay cambio de shapes previsto.
  Copias completas modificadas en `codigo/`: `integrar_ronda_6.py` (reorden +
  delegación) y `consolidar_semantica.py` (bloque R7); verificadas con
  `git diff --no-index` (solo los hunks previstos) y compilación OK. No instaladas.

## 2. Qué añade R7 (solo cuando/pisi se apruebe; ahora solo staging)

- Nuevo `integrar_ronda_7.py` en `codigo/`: `cargar()` +
  `validar_sobre_base(rules, base_r6)` + `construir()`. Regla fijada a la IRI CLASIF
  asignada (IRI + diccionario + conjunto + nombre + descripción normalizada + huella
  `c16feb…`); concepto estrictamente nuevo (rechaza clave existente aun si igual);
  **ambas auditorías deben aceptar la REGLA**; límites escritos obligatorios; campos
  extra solo sin alcance de join/vigencia/equivalencia/homologación/catálogo;
  orígenes subset del manifiesto (única evidencia admitida).
- Delegación: R5 sin cambios de lógica (su delegación a R6 ya propaga); R6 mueve su
  bloque de delegación a R7 **antes** de comparar exactitud, tras validar sus
  propios invariantes (copia completa en `codigo/integrar_ronda_6.py`, no instalada).
- `generar()` añade un bloque R7 espejo del R6 (copia completa en
  `codigo/consolidar_semantica.py`, no instalada).

## 3. Aceptación (diseño, sin fijar significado)

Propuesta en elaboración `…/67156807…%2F5` (CLASIF): **no aprobada, no se inventa
significado** — el texto lo fijará `aceptadas.json` solo si el integrador la acepta.
Criterio: 1 regla con alcance simultáneo conjunto+diccionario+definición+nombre+
descripción+huella (`a3320cad…/67156807…/…%2F5`, huella `c16feb…`); 1 concepto nuevo;
**0 correspondencias/joins/identidades de catálogos, 0 vigencia nueva**
(no fechar por nombre de hoja, no adoptar códigos INEGI 1–43, `-` = nulo declarado).
Auditorías independientes obligatorias: `auditoria-a` y `auditoria-b` aceptan
la REGLA con dictamen aceptar explícito (sin vía vacua por vínculos).

## 4. Si se rechaza

Borrar o dejar esta carpeta sin efecto; históricos, semántica, coverage,
manifiestos, Studio y tests quedan intactos. Pasos de integración real
(fijar evidencia/auditorías/manifiesto/config + tests) solo si el usuario lo pide después.
