# Paquete W-web — pistas nuevas (2026-10-24, primera pasada)

Fecha de trabajo: 2026-10-24. Actualizacion real: 2026-10-24T07:26:59+00:00.
Horas no registradas con reloj figuran como `no_registrada`; no se inventa ninguna hora.
Todo via Obscura (MCP nativo) + curl.exe para 2 descargas concretas. Sin Gemma, sin contactos, sin login.

> Nada aqui cierra casos. Son pistas con identificador para verificacion por fila+huella.

## Respetos (no repetidos)

- Portada del portal, iframe DGIS (`Dat-ehosp-Descripcion_de_variables`) y pagina Diagnostico
  (cascaron JS + PowerBI): ya examinados en `web-obscura` (obs-dgis / obs-diagnostico). No re-examinados.
- RAR del programa de calculo CONAPO y nota tecnica de 18 pp.: ya examinados sin definir CLASIF. No re-examinados.
- Fallos HTTP no se afirman como fuente agotada (ver F-W01: sharepoint pendiente, no inexistente).

## Pistas nuevas

- `F-W01-SESNSP-DICC` — Pagina SESNSP datos abiertos: locator exacto del
  `Diccionario de datos incidencia delictiva metodologia (2015-2025)` (sharepoint `:x:`)
  + Manual RNID V1.0 descargado en `paquete/Manual_metodologico_RNID_V1.0.pdf`
  (731610 B, sha `ca00bfb7…`). Ataca V13/V14 (contexto F3 por verificar).
  Diccionario sharepoint pendiente de descarga (requiere interaccion).
- `F-W02-SINAC-CAT` (prioritaria, multi-ID) — Pagina DGIS nacimientos (DOM):
  `sinac_catalogos_2020_2023.zip?V=1.1`, `sinac_catalogos_2024.zip?V=2025.06.24`,
  `sinac_catalogos_2025.zip?V=2026.07.09`. Nunca citados en el expediente.
  Pueden contener SI_NO, TRIMESTRE_PRIMER_CONSULTA, etc. para S2 (53 IDs).
  No descargados (23–48 MB c/u, masividad). Reapertura en paquete-v002.
  Descriptor 2020-2025 `?V=2026.07.09` re-descargado (13347 B, sha `61be6ed4…`,
  identico al local): sin bytes nuevos.
- `F-W03-DEFUN-VER` — Pagina DGIS defunciones (DOM, 66 enlaces): versionado
  `CATALOGOS_DEFUN_2022.zip?v=2023.11.10` / `DESCRIPTOR_CAMPOS_DEFUN_2022.zip?v=2023.11.10`.
  Contexto de edicion nacional para S1; bytes ya locales.
- `F-W04-TIC-ATDT` — Dataset TIC 0ec245ba renderizado (ATDT, 23 vars, sin programacion,
  tags entorno-digital, download_all) + organizacion ATDT (16 conjuntos, 10 entorno-digital;
  Presas tambien es ATDT, util V05). Negativa renderizada: ningun cuestionario/codebook
  publicado en conjunto/organizacion. Los 24 IDs TIC siguen pendientes.

## Sin pista nueva en esta pasada

S3 (matriculas/UTH), S4 (SUIVE), S6 (Total_Egresos/CLASIF, respetos arriba),
V1 (adopcion UTH), V2 (Rickettsia/fe de erratas), V3 (COESPO/CONAPO).
Primera pasada acotada a los 10 roles y consultas disponibles; el coordinador
pedira adenda en paquete-v002 si hace falta.
