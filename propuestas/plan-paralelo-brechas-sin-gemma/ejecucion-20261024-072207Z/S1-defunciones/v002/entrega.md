# S1-defunciones v002 — reevaluación de precisión (sin material nuevo)

Rol: S1-defunciones. 32/32 IDs. **0 promociones; 32 brechas externas.** v001 congelada intacta.

## Reinterpretaciones explícitas para los dos auditores

1. **Ámbito general fijado solo para el bloque violenta/lesión** (/53, /54, /67, /68, /69): el manual ubica esas preguntas en el certificado de defunción y la página SEED-DGIS declara "muertes accidentales/violentas solo para Defunciones" (`http_log.json`, hallazgo verificado). Fija ámbito, no definición ni códigos. No se extiende a otros IDs.
2. **Ningún identificador local coincide exactamente con un mnemónico nacional** (37 pares locales vs `sem_gest`, `natviole`, `causa_def`, etc.): todo vínculo por nombre es alias.
3. **Recodificación local probada**: /30 ejemplo `4` de 1 dígito frente a códigos nacionales de 3 (`ocupacion.csv`, 57 filas); /72 `997` y /74 `9997` fuera de ambos rangos nacionales (ocurrencia y lesión). Esto invalida suponer la codificación nacional en cualquier columna del extracto por igualdad de valores.
4. **Diferencia concreta por ID** en el `motivo` de cada decisión de `entrega.json`: alias, desajuste de códigos, horquilla de sujeto/ámbito/campo, ausencia total en el instrumento, o desajuste de representación (/78: una Fecha local vs tres campos nacionales).

## Por qué cero promociones

La carga era sistema+edición+identificador exacto+representación+ámbito sin exigir mención de Sonora. Ningún ID la supera: el identificador exacto falla en los 32, la codificación local no está publicada en ninguno, y las horquillas (fallecido/madre, ocurrencia/lesión, triple campo de embarazo, doble certificado) no las resuelve el instrumento. La "tabla local" no fue la única objeción: cada brecha mantiene una diferencia formal concreta.

## Pares estructurales

Sin `documental_revisada` propuesta; los 5 IDs ligados a pares candidatos no cambian de estado. Petición S1-WEB-01 sigue pendiente (adenda del coordinador si aporta).
