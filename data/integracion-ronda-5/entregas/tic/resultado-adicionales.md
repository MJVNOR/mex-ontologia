# Resultado adicional tic — 7 columnas condicionadas (ronda 5)

Simulación revisada: 7/7 candidatas de `columnas-adicionales.json` acreditadas como `proponer` en `adicionales.json` (7 decisiones_columnas + 7 vinculos, formato núcleo exacto, sin claves extra). Pendientes: 0. No se crean reglas nuevas: cada decisión cita dependencia explícita y condicionada a su regla r5-tic-00X.

## Verificación por columna (todas contra fuentes, sin aprobación automática)

- `1e5e326f…/Hoja1/2` P2 ↔ 3851…/2 Sector (r5-tic-002): recurso del conjunto 0ec245ba (inventario, Información General), pos 2 única, hoja ok, huella_esquema 43eb2558…, huella_fila 7e479222….
- `1f7476be…/Hoja1/2` P2 ↔ 3b31…/2 Sector (r5-tic-003): conjunto d227c85d (Planeación TIC), pos 2 única, huellas 485b0085…/7e479222….
- `3d8d9ae1…/Hoja1/2` P2 ↔ 0630…/2 Sector (r5-tic-001): conjunto aa353273 (Política Digital), pos 2 única, huellas 7e26bdce…/7e479222….
- `3d8d9ae1…/Hoja1/7` P7 ↔ 0630…/7 condiciones (r5-tic-006): mismo recurso/conjunto, pos 7 única, descripción completa, huellas 7e26bdce…/fefc6b0d….
- `3d8d9ae1…/Hoja1/13` P13 ↔ 0630…/13 recursos (r5-tic-007): pos 13 única, huellas 7e26bdce…/fed72d1b…. Corrección precisa auditor B aplicada: la descripción RAW termina en NBSP U+00A0 y el valor materializado lo recorta; hash RAW intacto, sentido correcto, sin efecto semántico (nota explícita en evidencia y criterio).
- `b444876c…/Hoja1/2` P2 ↔ af14…/2 Sector (r5-tic-005): conjunto d175b134 (Mejora Regulatoria), pos 2 única, huellas 409464b6…/7e479222….
- `c6d42e45…/Hoja1/2` P2 ↔ 8f8e…/2 Sector (r5-tic-004): conjunto 9208a313 (Presupuesto TIC), pos 2 única, huellas 05688c29…/7e479222….

Controles aplicados a las 7: columna física (hoja Hoja1, posición exacta, nombre único, `metodo_encabezado=heuristica_requiere_revision` como rutina que no bloquea), recurso→conjunto (inventario), fila de diccionario exacta (nombre, tipo, ejemplo, catálogo vacío), IRI de columna/variable/definición cruzadas con la simulación, y concepto+descripción+representación de la regla citada. Alcance documental en todos los vínculos: sin validar valores, catálogos ni cruces.

## Cierre

- `entrega.json`/`listo.json` no modificados (siguen cerrados con su SHA).
- `adicionales.json` SHA-256 `4ffe85a0…ffc107b` registrado en `listo-adicionales.json`, estado completo-condicionado.
- Foco 7 TIC cumplido; el vínculo de Nacimientos queda fuera de esta entrega (ya propuesto por su rol).
