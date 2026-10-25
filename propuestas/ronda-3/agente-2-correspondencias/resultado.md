# Agente 2 (ronda 3) — Correspondencias: 118 candidatas + 3 ambiguas

Unidad: vínculo columna física → variable documentada del mismo conjunto.
Solo conceptos y reglas vigentes (`ontologia/semantica.json`); sin conceptos
nuevos, sin alias. Las 836 revisadas se conservan exactas, sin tocarlas.

Traducción explícita al formato integrador: cada propuesta trae la clave
`descripcion` con la descripción literal original del diccionario; la clave
`definicion` repite el mismo literal (compatibilidad con ronda 2).

## Base verificada (estado actual, no histórico)

103 conceptos, 232 variables respaldadas, 836 revisadas, 118 candidatas
(1 correspondencia cada una), 3 ambiguas / 6 vínculos. El conteo 792 fue el
alcance de preselección de ronda 2, no el estado actual; no se reutiliza.

## Decisiones (118 = 29 + 89; 3 ambiguas conservadas)

Promovidas (29, nombre exacto, diccionario único del conjunto, unicidad en
diccionario y esquema de ese recurso/hoja, huellas recalculadas exactas,
sin alias, recurso/hoja de observaciones —no catálogo—):

| N | Concepto / regla | Evidencia distintiva |
| ---: | --- | --- |
| 10 | entidad-registro / entidad-captura (`Clave_Ent`) | «Identificador del estado de captura» + catálogo declarado `catalogo_entidades`; captura=registro según definición del concepto |
| 9 | fecha-matrimonio-previo (`fecha_matrimonio`, Divorcios 2015–2024) | «Fecha en la que los divorciados contrajeron matrimonio»: evento + población + representación; previo = matrimonio anterior al divorcio según definición del concepto |
| 9 | toma/recepción/resultado suero rickettsia ser1 (2022–2024) | Descripciones literales completas; `ser1` = identificador según definición del concepto; `suer` = errata documentada en el concepto |
| 1 | programa-educativo / programa-nombre | «Programa de estudios», descripción aceptada por la regla vigente |

El diccionario único del conjunto es condición necesaria pero no
suficiente: no transfiere el vínculo a todas sus hojas. Cada propuesta
exige además columna única en el esquema de ese recurso/hoja, nombre
exacto y descripción distintiva, y se excluyen hojas de catálogo.

Caso retirado (devolución del integrador): `Clave_Ent` en hoja
`cat_entidad` del recurso `Catalogo` (7f3aca28, Víctimas) → pendiente con
motivo `catalogo_no_observacion`. Una entrada del catálogo no es un estado
de captura: mismo nombre/representación/conjunto no demuestra mismo papel.
Solo una evidencia publicada explícita de aplicación del campo a esa hoja
y papel lo promovería. Es el único catálogo entre las preseleccionadas;
otras columnas en recursos titulados «Catalogo» (servic_atencion,
motiv_rech_ricket_sangre, Campo de Formación Académica, Clave) ya quedan
pendientes en preselección por variable sin respaldo.

Pendientes (89): 60 `variable_sin_respaldo:fuera_del_nucleo_actual`
(Campo de Formación Académica 39, Clave 9, servic_atencion 4,
motiv_rech_ricket_sangre 4, ricket_especie_rtpcr 3, Total_Egresos 1);
24 `variable_sin_respaldo:candidata_sin_definicion_suficiente` (PERIODO,
CLUES, MUNICIPIO/LOCALIDAD CERTIFICA(D)/OCURRENCIA(D), Mes, TRIMESTRE,
7 fechas de titulación/inscripción, Municipio, CVE_LOC);
3 `descripcion_solo_reconfirma_nombre` (AÑO×2, SEXO×1: la descripción es
solo el nombre, insuficiente por sí sola);
1 `nombre_difiere` (Año→ano, Temporada 2019: ñ→n no equivale, sin alias);
1 `catalogo_no_observacion` (Clave_Ent en cat_entidad, ver arriba).

Ambiguas (3, `ide_id` en Fiebre manchada 2022–2024): sin promoción.
Filas 177/178 degeneradas («ide_col», fuera del núcleo). Se conservan ambas
alternativas + pregunta al publicador en `propuestas.json` (qué significa
`ide_id` y qué fila 1/177/178 la documenta).

## Verificación

```powershell
uv run python propuestas/ronda-3/agente-2-correspondencias/revisar.py
uv run python propuestas/ronda-3/agente-2-correspondencias/verificar.py
```

20 pruebas OK: SHAs de entrada, base 103/232/836/118/3-6, partición sin
solapes ni intersección con las 836, 836 IRIs intactas en los tres stores,
huellas de esquema y fila recalculadas para las 29 (coinciden con central),
conceptos/reglas vigentes sin nuevos, formato integrador completo
(`descripcion` literal presente e igual a `definicion`), y negativas
(solo-nombre×3 pendientes, Año→ano pendiente + enie sintética
rechazada y exacta/acentos aceptadas, catálogo×1 pendiente + puerta
sintética catálogo frente a tabla de observaciones, 177/178 ausentes en
propuestas, alcance solo con diccionario único, cero alias/normalizaciones).
`revisar.py` regenera `propuestas.json` bit a bit salvo `generado_en_utc`.

## Archivos (solo escritura en esta carpeta)

- `propuestas.json`: 29 propuestas + 89 pendientes + 3 ambiguas + 24 fichas
  de grupo (G-019 documenta el caso catálogo degradado a pendiente) +
  huellas SHA-256 de las 6 fuentes centrales + nota de traducción de formato.
- `revisar.py`, `verificar.py`: generador y verificador reproducibles.
- `resultado.md`: este informe.

## Límites y bloqueos

- Cero descargas: toda la evidencia usada (diccionarios, esquemas, huellas)
  está fijada en `data/portal/`; no se encontró evidencia suficiente en
  fuentes revisadas para los casos pendientes (descripciones vacías o
  genéricas, papel de catálogo). No se afirma imposibilidad sobre fuentes
  no examinadas.
- No se validan valores, unidades, codificaciones ni pertenencia a
  catálogos; alcance documental (p. ej. `catalogo_entidades` se registra
  como declarado, no como acreditado).
- Las 29 promociones cubren 1 columna cada una; no se generalizan a otros
  recursos/años.
- Pregunta abierta (ambiguas `ide_id`): sin respuesta del publicador no hay
  vínculo. Las 24 variables `candidata_sin_definicion_suficiente` dependen
  de agente 3 / aclaración del publicador, fuera de este alcance.
