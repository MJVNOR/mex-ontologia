# Investigación post-R6 — salud-defunciones (32/32)

Grupo: `salud-defunciones`. Prioridad ADV-SALUD-MANUAL ejecutada: examen POR ID del PDF
auténtico SEED Modelo 2022 ya preservado. Resultado: **0 propuestas, 32 siguen pendientes**.
Nada que estadificar; sin cambios al núcleo.

## 1. Autenticidad del manual (nuevo frente a R6)

- Re-descarga completa el 2026-10-24: HTTP 200, `11717771 B`, SHA256 idéntico al preservado
  (`698ee48a…29b74f4`), `Last-Modified: 2022-10-19`. Ver `evidencia/http_log.json`.
- Página oficial SEED-DGIS confirma vigente el enlace “Manual de Llenado del Certificado de
  Defunción y Certificado de Muerte Fetal Modelo 2022” (página modificada 2024-12-02).
- R6 había verificado el PDF pero lo examinó **0/85 por ID**; aquí se examina **32/32**.
- El manual trae DOS certificados: Defunción general (preguntas 1–45, pp24–61) y Muerte Fetal
  (preguntas 1–42, pp66–98). No confundirlos: 12 veredictos son ambiguos por esta causa.

## 2. Examen por ID (pregunta/página exacta; detalle en `evidencia/examen_por_id.json`)

| n | Variable | Pregunta manual (página) | Veredicto |
|---|----------|--------------------------|-----------|
| 1 | EDADGESTACIONAL | 2 fetal (p66) / 10.2 general (p30) | ambiguo: fetal exige semanas sin admitir desconocido; general solo <28 días y admite 99 |
| 2 | CLAVEOCUPACIONHABITUAL | 14 (p35) | incompatible: columna numérica con clave, manual en texto libre sin claves; ej 4 inmapeable |
| 3 | CLAVEOCUPACIONHABITUALD | 14 (p35) | compatible-temática: ejemplo en la familia del manual, sin catálogo cerrado |
| 4 | TRABAJAACTUALMENTE | 14.1 (p36) / 31.1 fetal madre (pp86–87) | ambiguo + ej 2 sin mapa |
| 5 | TRABAJAACTUALMENTED | 14.1 / 31.1 fetal | ambiguo (“NO” existe en ambas) |
| 6 | AFILIACION | 15 (p37) / 32 fetal madre (p87) | ambiguo + ej 2 sin mapa |
| 7 | AFILIACIOND | 15 / 32 fetal | ambiguo (“IMSS” en ambas, sin catálogo enumerado) |
| 8 | SITIODEFUNCION | 19 (p39) / 9 fetal (p70) | ambiguo + catálogo 1–9 ausente; ej 3 inmapeable |
| 9 | SITIODEFUNCIOND | 19 / 9 fetal | ambiguo; “IMSS” es institución, no sitio (posible captura cruzada) |
| 10 | CLUES | 19.2 (p39) / 9.2 fetal (p70) | ambiguo cuál CLUES; formato no validable |
| 11 | MUERTEACCIDENTALVIOLENTA | 24 (p45) | compatible-temática; ej 2 sin mapa (Sí/No sin códigos) |
| 12 | MUERTEACCIDENTALVIOLENTAD | 24 (p45) | compatible-temática (“NO”) |
| 13 | INTENCIONEVENTO | 25 (pp45–46) o 35 (p53), sin título literal | ambiguo; concepto “presunta intencionalidad” cubre bloque 31–36 (p22, 12.2.7.5.2 p12); ej 8 sin mapa |
| 14 | INTENCIONEVENTOD | 25 o 35 | compatible-temática (falta-vínculo: NO APLICA sin codebook; ausencia ≠ incompatibilidad) |
| 15 | CIECAUSABASICA | 26 (p47) / 30 (p51) | compatible-temática / ambiguo-edición: manual documenta blanco al certificante y cita ed. 1995, pero no documenta edición aplicable a 2022 ni vínculo para U071 |
| 16 | CIECAUSABASICAD | 26 / 30 | compatible-temática (falta-vínculo: literal de código de emergencia 2020; edición aplicable no declarada; sin posterioridad como prueba) |
| 17 | CAUSAPROPIAEMBARAZO | 28.2/28.3 (p49) | compatible-temática; ej 8 sin mapa |
| 18 | CAUSAPROPIAEMBARAZOD | 28.2/28.3 (pp49–50) | compatible-temática; “NO APLICA” no es literal |
| 19 | SITIOOCURRENCIALESION | 32 (p52, lesión ≠ defunción) | compatible-temática; ej 88 (sentinela indocumentado) |
| 20 | SITIOOCURRENCIALESIOND | 32 (p52) | compatible-temática; “NO APLICA” no es literal |
| 21 | PARENTESCOAGRESORD | 34 (p53; ≠ informante p38) | compatible-temática fuerte (única D sin par, texto libre) pero ej “NO APLICA” ≠ “ninguno”/“Se ignora” |
| 22 | ENTIDADOCURRENCIA | 36.10 (p56, lesión) | compatible-temática; ej 88 sin mapa; triple ambigüedad residual (36.10 vs 20.x vs 10.10 fetal) |
| 23 | ENTIDADOCURRENCIAD | 36.10 (p56) | compatible-temática |
| 24 | MUNICIPIOOCURRENCIA | 36.9 (p55) | compatible-temática; ej 997 sin mapa |
| 25 | MUNICIPIOOCURRENCIAD | 36.9 (p55) | compatible-temática |
| 26 | LOCALIDADOCURRENCIA | 36.8 (p55) | compatible-temática; ej 9997 sin mapa |
| 27 | LOCALIDADOCURRENCIAD | 36.8 (p55) | compatible-temática |
| 28 | CERTIFICADOPOR | 37 (p56) / 36 fetal (p92) | ambiguo + opciones 1–3 no enumeradas; ej 3 inmapeable |
| 29 | CERTIFICADOPORD | 37 / 36 fetal | ambiguo; “OTRO MÉDICO” no es literal |
| 30 | FECHACERTIFICACION | 42 (p60) / 42 fetal (p97) | ambiguo + formato: manual solo fecha DD/MM/AAAA, local trae hora (“0:00”) |
| 31 | JURISDICCION_CLUES | ninguna | sin-pregunta: “jurisdicción” solo administrativa (pp13–14,19); nombre sugiere derivación por catálogo CLUES; mismo ej 6 que JURISDICCIONDEFUNCION (join prohibido) |
| 32 | JURISDICCION_CLUESD | ninguna | sin-pregunta; coincide con JURISDICCIONDEFUNCIOND sin que ello acredite nada |

## 3. Por qué nada se promueve (vía alternativa sometida a prueba, no resuelta)

Corrección de auditoría: no se exige que el manual nacional mencione a Sonora. Se probó la vía
alternativa —mismo sistema+periodo y uso formal inequívoco por ID con códigos/posición, nunca
alias por nombre— y **falla en el segundo prong en 32/32** (detalle: `evidencia/revision_vinculo_formal.json`):

- Prong 1 (sistema+periodo), ACREDITADO como marco necesario no suficiente: SEED en dos
  certificados + Modelo 2022 vigente 2022–2026 (p17) cubriendo el recurso 2022-01-01–2022-09-22.
  Pero el manual cubre DOS certificados, así que esto solo no desambigua fetal vs general.
- Prong 2 (uso formal), FALLA: el manual marca con X o captura texto libre y **no publica
  codebook numérico** para estas variables (solo opciones 10/11/12/99, 1–5, 1–4, Sí/No sin
  números); su convención de desconocido es **serie-9** (99, 9999, nueves) frente a la
  **serie-8** local (8, 88, 997, 9997: 0 ocurrencias en el manual); no trae tabla
  pregunta↔columna; posiciones inconmensurables (filas 17–80 vs preguntas 2–42 en dos
  certificados de 45+42). Casos que siguen sin acreditarse por falta de vínculo: ocupación en texto libre sin claves (n=2, incompatible formal); edición CIE aplicable a 2022 no documentada (n=15/16, ambiguo-edición/falta-vínculo); literal NO APLICA sin codebook (n=14, compatible-temática/falta-vínculo); JURISDICCION_CLUES sin pregunta (n=31/32).
- Lo que falta es ahora más preciso: codebook del publicador (o nota de equivalencia
  formato↔columna) + edición aplicable por fila. El recurso de datos es un XLSX con
  `datastore_active=false` (sin mapeo físico verificable; `version=null`, `url=null`).

## 4. Búsquedas negativas (acotadas a lo revisado, ver `evidencia/http_log.json`)

- “Sonora” en el manual: 0 (búsqueda registrada; **ya no usada como criterio** tras la
  precisión de auditoría: el vínculo se prueba por sistema+periodo+códigos/posición).
- “88”/“997”/“9997” locales en el manual: 0 (incompatibilidad formal de sentinelas serie-8 vs serie-9).
- Pregunta titulada “intención del evento”: 0 (concepto sí existe, bloque 31–36).
- Codebook de claves numéricas locales: ausente. Tabla pregunta↔columna: ausente.
- No se repitió ninguna línea agotada de R6/R5 (package_show, datastore live, SINAC 2015/2025):
  la única línea nueva es el examen por ID + re-verificación de autenticidad.

## 5. Artefactos y verificación

`entrega.json` (32 decisiones `sigue_pendiente`, fuentes F1–F8, sección `revision_vinculo_formal`), `listo.json` (hashes),
`evidencia/` (examen por ID, revisión formal por ID, log HTTP, extracción paginada del manual),
`temporales/generadores/construir_entrega.py` (reproduce `entrega.json`+`listo.json`).
Cada fuente local existe y su SHA corresponde a bytes (verificado por el generador).
