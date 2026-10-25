# Vigencias salud — V06/V07/V08 (Fiebre manchada Rickettsia) — 2026-10-24

## Decisión por ID

| ID | Hoja / campo | Estado | Brecha exacta que subsiste |
|---|---|---|---|
| V06 | Catalogo Servicios / servic_atencion | sigue_pendiente | F3+F4: sin declaración de edición/versión/fecha del catálogo ni vínculo con 2022-2024 |
| V07 | Catalogo rechazo / motiv_rech_ricket_sangre | sigue_pendiente | F3+F4: idem hoja Catalogo rechazo |
| V08 | Catalogo especie / ricket_especie (var. ricket_especie_rtpcr) | sigue_pendiente | F3+F4: idem hoja Catalogo especie |

Ningún ID se marca solucionado: el catálogo actual está verificado pero falta historia (edición aplicable al periodo).

## Qué se reverificó en vivo (nuevo 2026-10-24, no repetición ciega)

1. **API CKAN package_show**: `version=null`, `extras=[]`, `metadata_modified 2026-05-11` sin cambios — respuesta **byte-idéntica** a la captura previa (sha `e751fe48` en ambas).
2. **catalogo.xlsx en vivo**: conserva sha `3b8546ac` (size 12702 = API; sin re-subida). Interior por hoja: Servicios A1:B8, rechazo A1:B21, especie A1:B5; 37 sharedStrings sin versión ni periodo (`edici` solo aparece dentro de "Medicina interna"; `fecha` solo en valores de rechazo). core.xml: created 2026-04-15, modified 2026-04-29 — export posterior a los periodos, sin versión.
3. **Diccionario en vivo** (sha `2c8ce131`): filas 129/162/168 citan los catálogos por nombre sin edición; los 17 `2022` son fechas de ejemplo, no vigencia; fila `des_mpo_res` con catálogo de referencia vacío (sub-pista negativa).
4. **Pista nueva** salud.sonora.gob.mx (estrategia FMRR, hub Rickettsiosis, informes SE): la estrategia (sha `9c2aec12`) no menciona el catálogo CKAN ni sus campos — negativa documentada, no es la declaración requerida.
5. Cobertura `2022-01-01/2026-12-31` del recurso y fechas de carga **no acreditan edición** (criterio de aceptación).

## Evidencia local (verificada por SHA de bytes)

`evidencia/api_package_show_2026-10-24.json`, `evidencia/catalogo_xlsx_2026-10-24.xlsx`, `evidencia/diccionario_csv_2026-10-24.csv`, `evidencia/recurso_catalogo_pagina_2026-10-24.html`, `evidencia/estrategia_fmrr_salud_sonora.pdf`. Ver `entrega.json` (fuentes + localizadores).

## Límites

Sin joins ni identidad automática de catálogos; sin inferir vigencia del nombre del archivo; sin extender a otros conjuntos/periodos; sin contactar publicadores; navegador Obscura no manejado por este agente (peticiones en `peticiones-web.json`).
