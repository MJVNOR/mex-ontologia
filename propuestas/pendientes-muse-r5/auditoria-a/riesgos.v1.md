# Auditoría-a R5 v1 — informe de riesgos concretos (tic, nacimientos, matriculas, presas, catálogos-web)

Sin esperar a las entregas: casos que deben resolverse como pendiente salvo evidencia explícita. Modelo: Muse 1.3. Sin Obscura; solo lectura local.

## TIC (31 significados, 11 booleanos Si/No)

- **R-TIC-01 — conteo/procedimiento vs Booleano (rechazo casi seguro si se proponen como medida):** P36 (¿Cuántos proyectos…?), P40 (¿Cuántas personas…?), P39 (¿Cómo atiende incidencias…?) en dos diccionarios (af14… y a4e8…-familia). Precedente R4: 025/026/027 retiradas por contradicción real. Solo cabe existencia declarada, nunca conteo/procedimiento.
- **R-TIC-02 — P13 tipo-pruebas con ejemplo `Si`:** Texto sí puede portar tipos; exigir positivo de texto libre + límite no tabular (precedente R4-022 corregido y aceptado).
- **R-TIC-03 — P11 presupuestal Booleano con ejemplo textual `Tecnologia 1, tecnologia 2`:** contradicción tipo-vs-ejemplo; no tabular ni agregar.
- **R-TIC-04 — vagos sin clasificador:** P2 `Sector` ×5 encuestas (ej. `04 - SECRETARIA DE HACIENDA`): sin separar código/nombre, sin catálogo, sin equiparar entre encuestas (precedente R4-008 condicionado). P7 `¿Cómo se generan?` ×2 sin sujeto; P27/29/31/33 `¿Cuáles?` anafóricos ×4; P8 doble (metodología Y documentación); P10/P11 `Actividades principales`/`¿De qué área depende?` (área sin catálogo); P15 `Especifique el perfil` (ej. `Computologo`, lista abierta); P10/P16/P18 booleanos de existencia (solo existencia declarada, representación no_especificada).
- **R-TIC-05 — P13 recursos `5000, software`:** mezcla monto+especie sin unidad/moneda; solo lista declarada (precedente R4-16).

## Nacimientos (54: 53 vacías + 1 divergente)

- **R-NAC-01 — 53 descripciones `Pendiente de especificar`:** pares código+texto (X/XD: ATENCIONPRENATAL/D, TAMIZ/D, VACUNA/D, VITAMINA/D, AFILIACION/D, etc.). Riesgo: decodificar XD por simetría o por ejemplo (`SI`, `CESÁREA`, `NINGUNA APARENTE`). Prohibido: el ejemplo no es codebook. Solo pendiente salvo diccionario corregido o nota del publicador con codebook + vínculo + vigencia.
- **R-NAC-02 — RESIDEEXTRANJERO vs RESIDEEXTRANJEROD:** divergencia documentada (`recidente en el extranjero` vs `residente extranjera`); no fusionar ni elegir por nombre.
- **R-NAC-03 — CLUES (`SRSMP000314`), CODIGOCIEANOMALIA (`0000`), TIEMPOTRASLADO (Hora `hh:mm`):** sin catálogo local ni calendario; no promover DGIS/INEGI sin vínculo local + vigencia (precedente defunciones).

## Matrículas (30: 28 vacías + 2 parciales)

- **R-MAT-01 — 28 vacías** (inscripción, grupos, equivalencia, estímulos, Grupo Indig. ×4, promedios, bajas, titulación, fechas): no inferir escala de promedios (`8.2` sin escala declarada), ni calendario/vigencia de fechas (`dd/mm/aaaa`, ej. `30/11/2021`), ni identidad por `222 (Reing)` o listas de grupos.
- **R-MAT-02 — `Municipio` (`Municipio donde el alumno…`, ej. `HERMOSILLO`, descripción al parecer trunca):** sentido parcial; sin código ni catálogo declarado; como máximo concepto de texto declarado con límite, nunca clave geográfica.
- **R-MAT-03 — `Tipo de baja` (descripción = nombre):** genérico; sin tipología declarada.

## Presas (asignación: completo-condicionado)

- **R-PRE-01 — Clave de presas:** pendiente correcto si persiste la ambigüedad de hoja exacta/dominio; prohibido habilitar joins por compartir `Clave`. Verificar hoja exacta y huella antes de aceptar cualquier vínculo.

## Catálogos-web (17 referencias)

- **R-CAT-01 — vigencias:** exigir enlace documental edición–recurso–periodo por cada referencia; fecha de publicación/captura y similitud de valores NO bastan. Sin ese enlace: pendiente, 0 cambios al núcleo (postura correcta actual).

## Criterio transversal

Concepto limitado realmente acreditado = literal de fila (nombre+descripción+tipo/formato/ejemplo/catálogo) con sentido unívoco + ámbito exacto + límites. Todo lo demás es inferencia por nombre y va a pendiente con solicitud precisa. Las decisiones finales por ID (aceptar/corregir/rechazar) se emitirán sobre cada entrega final sin reabrir lo ya dictaminado.
