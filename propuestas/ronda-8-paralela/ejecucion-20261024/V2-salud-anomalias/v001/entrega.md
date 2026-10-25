# V2-salud-anomalias — entrega v001 (2026-10-24)

Rol: vigencias del catálogo Rickettsia (Fiebre manchada, conjunto 5494daa1).
Modelo: opencode-go/muse-spark-1.3-contributor. Sin Gemma, sin contactos, sin navegador (solo W).

## Decisiones

| ID | Hoja / campo | Estado | Puerta |
|----|--------------|--------|--------|
| V06 | Catalogo Servicios / servic_atencion | brecha_externa | sin_pista_nueva |
| V07 | Catalogo rechazo / motiv_rech_ricket_sangre | brecha_externa | sin_pista_nueva |
| V08 | Catalogo especie / ricket_especie | brecha_externa | sin_pista_nueva |

Afirmación acotada común (las 3): F3+F4 ausentes — el portal/API no declara
edición, versión ni fecha del catálogo (sha
`3b8546ac…293db9c`, recurso `08d3b1a7`) ni su aplicación a 2022, 2023 y 2024.
Las fechas visibles (cobertura API 2022-01-01/2026-12-31, carga 28/29-04-2026,
core.xlsx 2026-04-15/29) no acreditan edición. Prueba verificable por caso en
`entrega.json`: 5 evidencias con SHA-256 calculado por código.

## Revisión hecha (sin repetir búsquedas agotadas)

- SHA-256 por código de las 5 evidencias: byte-idénticos a R7.
- Contenido re-verificado por código: API (`version=null`,
  `fuentes_extras=""`, 5 recursos, Catálogo 12702 B 2022-01-01/2026-12-31);
  CSV 179 filas (fila 7 `des_mpo_res` sin catálogo; filas 129/162/168 citan
  catálogos por nombre sin edición); xlsx 3 hojas (A1:B8 / A1:B21 / A1:B5,
  37 sharedStrings sin versión, core 2026-04-15/29); HTML (creado 28-04-2026,
  formato XLSX, sin versión); PDF FMRR byte-idéntico al de la negativa R7.
- Expediente W-web v001..v004 + `nota-primera-puerta.md` + web-obscura R6
  revisados completos: v001 declara "Sin pista nueva" para V2; v002–v004 sin
  mención a V06–V08/Rickettsia; F-CKAN-RICK es reconfirmación ya incluida.
- `peticiones-web.json`: no emitido — sin pista primaria nueva concreta;
  pedir búsquedas genéricas repetiría lo agotado.

## Reapertura

Por caso en `entrega.json` (`condicion_reapertura` + `evidencia_faltante`):
fe de erratas, diccionario corregido o declaración de edición del publicador
que cite la hoja y la vincule con 2022–2024; entonces re-verificar
correspondencia formal campo/recurso/edición/periodo.
