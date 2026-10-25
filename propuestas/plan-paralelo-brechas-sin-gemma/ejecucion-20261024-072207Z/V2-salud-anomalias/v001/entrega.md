# V2-salud-anomalias — entrega v001 (2026-10-24)

Rol: `V2-salud-anomalias`. IDs: V06, V07, V08, fila 177, fila 178, `des_mpo_res`.

## Resultado

Sin propuesta acreditada. Las 6 decisiones quedan como **brecha_externa**,
todas con puerta **sin_pista_nueva** y `pista: null`.

## Qué se hizo

- Se verificó la evidencia previa (18 archivos, SHA-256 calculados hoy: todos
  coinciden con lo registrado en antecedentes; no se re-descargó nada).
- 2 búsquedas acotadas nuevas con herramienta web independiente
  (fe de erratas / diccionario corregido / edición del catálogo Rickettsia):
  sólo páginas conocidas del conjunto y material clínico sin vínculo
  campo/recurso/edición/periodo. Negativas documentadas en
  `trabajo/nota-primera-puerta.md`.
- No se emitió `peticiones-web.json`: no hay pista concreta que requiera
  navegador; pedir búsquedas genéricas repetiría lo agotado.

## Documento exacto que falta (por ID)

- V06/V07/V08: declaración de edición/versión/fecha del catálogo Rickettsia
  (sha `3b8546ac`, recurso `08d3b1a7`) vinculada a 2022-2024 + fe de erratas o
  diccionario corregido.
- Filas 177/178: fe de erratas o diccionario corregido del publicador
  (huellas `4b17625c` / `b5dbcdf5`).
- `des_mpo_res`: lo anterior y, sólo si el publicador confirma que existe un
  catálogo aplicable, su URL con edición/fecha.

## Límites

- Paquete `W-web` pendiente al cierre local; si W aporta evidencia
  resolutiva, corresponderá adenda del coordinador (v002).
- Los 2 artefactos EXC-ENC-177/178 siguen excluidos sólo de vista accionable y
  no cuentan como significados nuevos.
- A partir de `congelada.json` no se edita v001.
