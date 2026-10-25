# Resultado — catalogos-web, ronda 5 (primera fase: 17 dictámenes + 21 solicitudes)

> Nota de alcance: este archivo documentó la primera fase (catálogos V01–V16 +
> des_mpo_res y las 21 solicitudes de defunciones, diversos, epidemiologia,
> presas y nacimientos). La segunda fase (13 entradas TIC/matrículas/presas-dup)
> está en `resultado-seguimiento.md` con `listo-seguimiento.json`. Ambos
> informes son consistentes: ningún catálogo aprobado sin F4.

17/17 referencias decididas (pendiente), 0 propuestas al núcleo, 0 vínculos.
Investigación web nueva con Obscura (2026-10-23, 9 piezas W01–W09) que amplía
sin duplicar la ronda 4. No se recibió ninguna `solicitudes_web.json` de los
seis especialistas ni de presas (verificado por glob el 2026-10-23).

## Cuentas verificadas

- Referencias revisadas: 17 (V01–V16 + des_mpo_res).
- Decisiones: 17 pendiente (4 con F3 acreditada + F4 ausente; 13 con F3+F4 ausentes).
- Reglas nuevas: 0. Conceptos nuevos: 0. Vínculos: 0. Columnas: 0.
- Fuentes web nuevas: 9 (5 negativas, 2 neutras, 3 parciales-contexto, ninguna acredita F4).
- Local re-verificado: 6 sha xlsx coinciden; 11 packages CKAN sin extras temporales.

## Hallazgos nuevos (no duplican ronda 4)

1. Portal UTH (V01/V02): publicador = Universidad Tecnológica de Hermosillo,
   fuente interna, sin mención a la CMPE (W01, W02). Búsqueda de adopción UTH
   negativa (W08); SNIEG solo acredita marco nacional (W09).
2. Hídricos (V05): el recurso 1960-1969 sigue listado sin descarga en vivo (W03).
3. Proyecciones (V09–V12, V15–V16): el publicador cita Fuentes extras CONAPO
   1990-2040 (W05, nuevo); el documento CONAPO es del 09-05-2024 y cubre
   1990-2020 + 2021-2040 — desfase de 1 año vs periodos locales y sin declarar
   edición del catalogo.xlsx (W06). No se atribuye vigencia.
4. Delictiva/Víctimas (V13–V14): origen SESNSP declarado en la nota de ambos
   conjuntos + Fuentes extras (W07); sin edición/corte del catálogo local.
5. Rickettsia (V06–V08, des_mpo_res): recursos publicados = Diccionario +
   Catalogo + datos 2022-2024; sin catálogo de municipios (W04).

## Seguimiento — solicitudes_web (2026-10-23, tarde)

21/21 atendidas con resolución web comprobable, sin aprobar catálogos sin F4:

- defunciones (5): SW-D1/D3/D5 negativos (portal SEED sin codebook; R01, R02 con
  fechas del diccionario 10-01-2024/01-11-2024); SW-D2 y SW-D4 parcial-contexto
  (CIE-10 Abr-2024 y CLUES Ago-2026 confirmados, R03/R04, sin vínculo local).
- diversos (4): SW-DIV-01 negativo; SW-DIV-02 parcial (CONAPO 2020 citado, R11);
  SW-DIV-03 negativo-portal (UUID corregido por búsqueda, R12);
  SW-DIV-04 negativo (sin fe de erratas, R13).
- epidemiologia (3): SW-EPI-01 parcial-documento (portal sin manual, R05;
  manual SUIVE auténtico preservado en `evidencia/manual_suive_32.pdf`, R06,
  contenido pendiente de OCR); SW-EPI-02 parcial (R03); SW-EPI-03 negativo.
- presas (1): negativo + constancia de que NO existe Historico_presas (R14).
- nacimientos (8): nac-web-01/08 negativos (R07); nac-web-02–07
  parcial-contexto (Manual Certificado 2015 auténtico + PDF preservado en
  `evidencia/CN_ManualLlenado_2015.pdf`, R08; rutas 404 corregidas, R09).

Regla aplicada: fuente nacional sugiere interpretación pero sin aplicabilidad
local queda pendiente. Descargas xlsx del portal no usadas como fuente. Solo
páginas públicas y documentos auténticos.

## Archivos (nuevos del seguimiento)

- `respuestas_web.json` — 21 respuestas, una por solicitud.
- `evidencia_web_solicitudes.json` — 15 piezas R01–R15 con URL, fecha,
  fragmento, localizador, sha256, conclusión.
- `evidencia/manual_suive_32.pdf` + `evidencia/CN_ManualLlenado_2015.pdf`.
- `solicitudes_web.json` — estado atendidas_21_de_21.
- `listo.json` — sha de entrega.json intacto (`f01b8284…`), estado
  completo-con-seguimiento.
- `evidencia_web.json` — 9 piezas con URL, fecha, fragmento, localizador, sha256, conclusión.
- `solicitudes_web.json` — sin solicitudes recibidas; cobertura de INV-R4C-01–06.
- `listo.json` — sha256 de entrega.json y conteos.
