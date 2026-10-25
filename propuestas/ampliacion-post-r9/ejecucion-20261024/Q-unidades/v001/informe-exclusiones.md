# Q-unidades v001 — exclusiones (no propuestas)

- **Hectómetros cúbicos** (4 filas: `cap_name`, `cap_namo`, `vol_muerto`, `Almacenamiento(hm³)`, según el diccionario sellado `P1-qudt/presas_vars.json`; la inspección local `ca5574f0…` solo expone 3 definiciones): búsqueda agotada; HectoM3 404 + ausente del índice QUDT 3.5.3 (sello W v003). No se repite sin pista primaria distinta; nada de M3/factores.
- **Hectáreas fuera de R9** (14 filas: SUPSEM ya vinculada en R9; SUPCOSE, SUPSINI, SHD139…, SUMTOT fuera): mismo término R9 (HA) ya vinculado en otra definición; no se duplica.
- **Compuestas sin término exacto conocido**: `Pesos/kilogramo` (3), `Toneladas/hectáreas` (1), `Pesos por tonelada` (1). Sin petición:
  requieren término precoordinado que Q no puede acreditar localmente.
- **Grados** (2 filas visibles: Latitud, Longitud; una tercera, Altitud en Grados, consta en `P1-qudt/presas_vars.json`): literal ambiguo sin calificativo (existe también `Grados celcius`) y fila malrotulada; no se propone en v001.
- **Moneda/importe** (`Pesos MXN`, `Miles de pesos MXN`, `Pesos Mexicanos`, `Miles de litros; Toneladas`): escala o moneda, no magnitud física con término exacto local.
- **Referencia indirecta**: `La unidad de medida que se indica en la siguiente variable` (3), `Mantiene las unidades indicadas en UMED`, `Unidad según tipo de metal` (descripción, columna vacía): sin literal explícito propio.
- **Conteo**: `Cabezas` (15): conteo, sin término físico exacto local.
- **Códigos, títulos, clasificaciones y N/A** (resto del inventario): no son unidades (ver `inventario-unidades.json`).
