# Paquete web-obscura — pistas nuevas de evidencia primaria (2026-10-24)

> Nota temporal: las horas `12:00 UTC` que figuraron en `fuentes.json`
> fueron aproximadas, no registradas originalmente con reloj; se corrigieron
> a `null`/`no_registrada_originalmente` (ver `disponibilidad.json`).
> Fecha de trabajo: 2026-10-24. Actualización real: 2026-10-24T06:54:21+00:00.

Obscura **sí disponible** en esta sesión (ver `disponibilidad.json`):
snapshot + pestaña aislada `tab-2` al portal oficial de Sonora (89 conjuntos,
31 organizaciones, 8 grupos). Sin tocar pestañas ajenas. Resto con
herramientas web nativas + API CKAN directa. **Nada aquí cierra casos.**
Son pistas con identificador para verificación por fila+huella.

Regla: búsqueda negativa acotada a lo revisado el 2026-10-24, no ausencia
universal. Sin descargas masivas (SHA `null` = solo lectura web/API).

## Correspondencias (20) — todas siguen candidatas por nombre

- `F-CLUES-01` — Catálogo CLUES DGIS (CAT_CLUES, estatus Definido, caracteres
  1–5 = institución, actualización agosto 2026).
  Ataca: CLUES SINAC/SEED (corr-a 5 casos, corr-b `68f8868f`).
  Falta: tabla pregunta↔columna + codebook del publicador.
- `F-INEGI-MG` — Marco Geoestadístico INEGI (AGEM 3 dígitos, localidad
  4 dígitos, catálogo único con corte y equivalencias).
  Ataca: columnas municipio/localidad (corr-a/b) y `cat_municipio`/`cat_entidad`
  (V13/V14). No autoriza joins.
- `F-SUIVE-01` — Manual SUIVE-32 + formato SUIVE-1 2021 (EPI clave, CIE-10 por
  enfermedad, grupos `<1a,1-4,...,65+,Ign.`, CLUES/SUAVE) + boletín oficial
  (NOM-017-SSA2-2012). Ataca: `cve_cie10`, `acumulado`, `de01_a_04`,
  `se_ignoran`, `menores_1f`, `deXXf`.
- `F-CIE-U071` — U07.1 COVID-19 emergencia OMS (efectivo 2020-04-01, CDC/OPS).
  Ataca: `CIECAUSABASIC`/`CIECAUSABASICD`. Data el código, no fija edición 2022.
- `F-DGIS-EGR` (ya en expediente, re-citada) — Cubos DGIS + guía B014 confirman
  egresos ≠ urgencias. Ataca: `Total_Egresos` (`e1e53ced`). Sigue pendiente.

## Vigencias CMPE / UTH (V01–V04) + Presas (V05)

- `F-CKAN-V01` — `package_show` Promedio Académico en vivo: `version=null`,
  `fuentes_extras=''`, catálogo 10433 bytes = sha local, placeholder
  1989-06-04, 13 datos cuatrimestrales 2022–2026. F4 ausente (verificado,
  no repetido de R6: hay recurso 2026 nuevo).
- `F-CMPE-01` — SEP/SNIEG: CMPE como estándar nacional (página expone ed. 2011;
  la aplicable es 2016, pdf local). Sin mención UTH. Contexto, no cierre.
- V05: sin novedad web oltre R6 (recurso 1960-1969 `4d1bb645` con url vacía).

## Vigencias CONAPO / COESPO (V09–V12, V15–V16)

- `F-CKAN-V09` — `package_show` 0b5f5e16 en vivo: `fuentes_extras` = URL CONAPO
  1990-2040, notes reconstrucción 1990–2019 + proyecciones 2020–2040.
- `F-CONAPO-01` — CONAPO 09-05-2024: 2475 municipios, **1990–2020 + 2021–2040**,
  "escenario hipotético", cita SGCONAPO 31-05-2024. **Desfase de 1 año**
  vs corte local documentado; no transfiere vigencia al xlsx.

## Vigencias SESNSP (V13–V14)

- `F-SESNSP-01` — Datos abiertos SESNSP (16-10-2026): metodologías
  1997–2017 / 2015–2025 / 2026–, diccionario 2015–2025 + manual RNID.
  Ruta documental nueva; F3+F4 locales siguen ausentes.

## Corrección fiebre (V06–V08, des_mpo_res, EXC-177/178)

- `F-CKAN-RICK` — `package_show` 5494daa1 en vivo (2026-10-24): 5 recursos,
  Diccionario CSV `datastore_active=true` 2022–2026, Catálogo 12702 bytes
  2022-01-01/2026-12-31, `version=null`. Inventario reconfirmado **sin**
  recurso de municipios de residencia. Fe de erratas pendiente; cobertura API
  ≠ edición.

## Significados salud / educación-epidemiología / tic-diversos

- Salud: `F-CLUES-01` + `F-CIE-U071` + manual SEED del expediente; todo
  `sigue_pendiente` sin tabla pregunta↔columna.
- Educación-epidemiología: `F-SUIVE-01` por fila + `F-INEGI-MG`; sin edición
  aplicable 2022 ni diccionario corregido (EPI-R6-01/02/03).
- TIC-diversos: CLASIF/CVOTRAS/TRIMESTRE/Total_Egresos/P10-P29 sin documento
  nuevo oltre R6; `F-CKAN-V01/V09` sirven como plantilla de verificación
  en vivo para los agentes hermanos.
