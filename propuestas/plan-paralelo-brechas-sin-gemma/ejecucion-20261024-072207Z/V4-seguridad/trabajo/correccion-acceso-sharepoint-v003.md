# Corrección acceso SharePoint (v003) — V13/V14

## Lo que v002 dijo mal

v002 (motivo) afirmó que el Diccionario SESNSP 2015-2025 en SharePoint
"requiere interacción/auth". Falso según W-v002 congelado
(F-V002-01-SP-DICC, `paquete-v002/fuentes-v002.json`, 2026-10-24):
apertura PÚBLICA sin login; redirige a `excel.officeapps.live.com`
(visor readonly, `DD_SESNSP_Metodologia_Actual`); rejilla en `Loading...`
en dos visitas, 0 tablas DOM, 0 iframes de contenido; sin bytes descargados
("el viewer no expone descarga directa sin sesión"). v002 no se edita;
la corrección vive en v003.

## Estado exacto del acceso (congelado W-v002)

- URL exacta invitada (guest, pública):
  `https://sspcgob-my.sharepoint.com/:x:/g/personal/cni_sspc_gob_mx/Eft_H-La80NInrfnyRu9PCkBfyIyy-yr9hl8imxAyeLXMg?e=xvI38U`
  → viewer `.../files/e21f7ffbf3da48439eb7e7c91bbd3c29, readonly=1`.
- Archivo existe con ese nombre; contenido tabular NO extraíble por DOM.
- Causa del no-acceso: representación/descarga no legible (viewer canvas
  en Loading), NO autenticación y NO inexistencia.

## Pendiente

W anunció último intento de descarga pública legible en `paquete-v003`.
Al corte de v003 ese paquete no existe: v003 documenta el estado con
W-v002 congelado y deja la condición de reapertura en dos ramas
(XLSX recuperado → examinar edición/corte/periodo; si no → sigue
acceso_no_resuelto por representación no legible). Si paquete-v003
trae XLSX, se examinará en v004.

## Aporte del manual, distinguido (no aplicado a 2015-2025)

Manual RNID V1.0 (feb 2026): contexto metodológico nacional, rige reporte
desde 2026; no declara edición/corte de los catálogos locales ni vínculo
con 2015–2025 (ver `trabajo/examen-manual-RNID-V13-V14.md`). No se usa
para acreditar vigencia 2015–2025.
