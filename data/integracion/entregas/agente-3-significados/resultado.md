# Agente-3 — Revisión de 47 interpretaciones candidatas

Aislamiento: solo se leyó `data/semantica/cobertura.json`, `ontologia/semantica.json` y `docs/nucleo-semantico.md`.
Todas las escrituras están en `propuestas/agente-3-significados/`. No se modificó el motor, no se sincronizó Studio, no se usaron propuestas de otros agentes.
Unidad de trabajo: variable documentada y su definición. No se declaran correspondencias con columnas físicas. No se amplía a las 1,308 fuera del núcleo.
Propuestas no aplicadas al vocabulario central.

Total: 47 = proponer 24 + mantener pendiente 23.
Motivos pendiente: pendiente explícita 17, genérica insuficiente 5, truncada 1.
Verificación: `uv run python propuestas/agente-3-significados/scripts/verificar.py`.

## Criterio aplicado
- «Pendiente de especificar» o vacía → siempre pendiente, sin deducir por el nombre.
- Genérica/truncada/ambigua (`Clave geográfica`, `perido…`, `Trimestre del estrato`, `Registro cronológico…`, `Fecha del registro.`, `Municipio donde el alumno`) → pendiente; el texto no precisa evento, papel, unidad o representación.
- Propuesta solo si la descripción + contexto respaldan evento/objeto; si la población no está declarada se conserva la limitación en la definición del concepto.
- Clínica: toma/recepción/resultado separan muestra (suero/sangre), prueba (ser1/RT-PCR) y secuencia (primera); inicio/fin tratamiento e ingreso son eventos distintos e intercambiables entre sí queda prohibido.

## Decisiones por variable
### Atenciones brindadas — `Mes`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `mes-atencion` — Meses en que se brindó la atención según Atenciones brindadas; conserva evento atención. Población no precisada en la definición (contexto: personas atendidas); requiere año como contexto y no equivale a registro o captura.
- Regla propuesta: `mes-atencion` (representación `mes`)
- Evidencia: descripción literal 'meses en que se brindó la atención', def `https://example.org/mex-ontologi/definition/e2b59a36-0fe1-4106-9756-ed9aca7dd9d0%2F1`, diccionario `e2b59a36-0fe1-4106-9756-ed9aca7dd9d0`, conjunto `a723a8e4-b944-405e-b897-bd27f8c67cf9`, huella `d9fa87c5f2ed61f03727aa03991a64828dafe8b744e3b2a4f47cb446fa022351`, catálogo declarado ''
- Alcance: Solo la variable documentada Mes del diccionario e2b59a36-0fe1-4106-9756-ed9aca7dd9d0 (Atenciones brindadas), definición https://example.org/mex-ontologi/definition/e2b59a36-0fe1-4106-9756-ed9aca7dd9d0%2F1. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: requiere año como contexto y no equivale a registro o captura.
- Documentado vs inferencia: Documentado: 'meses en que se brindó la atención'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: meses en que se brindó la atención; contraejemplo: Año de captura (evento distinto)

### Cuerpos de Agua en el Estado de Sonora: Ubicación de las Presas — `Fecha`
- Decisión: **mantener_pendiente** (descripcion_generica_insuficiente: Descripción genérica o ambigua: no precisa evento, papel, unidad o representación para respaldar concepto/regla.)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Fecha del registro.', def `https://example.org/mex-ontologi/definition/bfb8788b-8ce3-475e-8bbd-dd1c5154c877%2F2`, diccionario `bfb8788b-8ce3-475e-8bbd-dd1c5154c877`, conjunto `8c1f452e-7967-4c6b-a7b5-f2279360ad6c`, huella `2186c3ca8317f63c694219598478b0d6bbb92fa403d90b1cd3185f7d8cd97e45`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha del diccionario bfb8788b-8ce3-475e-8bbd-dd1c5154c877 (Cuerpos de Agua en el Estado de Sonora: Ubicación de las Presas). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Fecha del registro.'. Inferencia separada: ninguna; mantener pendiente.

### Denuncias Ambientales — `FECHA RECEPCION`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-denuncia` — Fecha de la denuncia según Denuncias Ambientales; conserva evento denuncia. El nombre de la variable menciona recepción pero la descripción no la confirma; no se asume recepción ni fecha de ocurrencia de los hechos.
- Regla propuesta: `fecha-denuncia` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de la denuncia', def `https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F4`, diccionario `3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99`, conjunto `c589afac-79f1-4aac-9ade-e949301bcca3`, huella `a36c2deed414ebc1b03397deaeda60f7b7881371a9514b48a378a5ddcb75544b`, catálogo declarado ''
- Alcance: Solo la variable documentada FECHA RECEPCION del diccionario 3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99 (Denuncias Ambientales), definición https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F4. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: no se asume recepción ni fecha de ocurrencia de los hechos.
- Documentado vs inferencia: Documentado: 'Fecha de la denuncia'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de la denuncia en Denuncias Ambientales; contraejemplo: TRIMESTRE del estrato (granularidad y evento distintos)

### Denuncias Ambientales — `TRIMESTRE`
- Decisión: **mantener_pendiente** (descripcion_generica_insuficiente: Descripción genérica o ambigua: no precisa evento, papel, unidad o representación para respaldar concepto/regla.)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Trimestre del estrato', def `https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2`, diccionario `3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99`, conjunto `c589afac-79f1-4aac-9ade-e949301bcca3`, huella `799f924f8f10e3831cebdb4fbbc233cb6965caae8902f799881277d12f24320d`, catálogo declarado ''
- Alcance: Solo la variable documentada TRIMESTRE del diccionario 3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99 (Denuncias Ambientales). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Trimestre del estrato'. Inferencia separada: ninguna; mantener pendiente.

### Donaciones de Órganos y Tejidos — `Institucion`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `unidad-hospitalaria-donacion` — Unidad hospitalaria donde se realizó la donación; conserva objeto hospitalario y evento donación. No acredita pertenencia a catálogo CLUES ni distingue publicadora/capturadora.
- Regla propuesta: `unidad-hospitalaria-donacion` (representación `no_especificada`)
- Evidencia: descripción literal 'Unidad Hospitalaria donde se realizo la donacion', def `https://example.org/mex-ontologi/definition/52fbcaaa-765b-4c92-8418-ccebc3fcfdcd%2F4`, diccionario `52fbcaaa-765b-4c92-8418-ccebc3fcfdcd`, conjunto `e863b72e-7a08-4bc7-bdab-c26ee116a383`, huella `80d1ee444e0856c21a7763b491074204954652980ab497fd74ea52fb73e84532`, catálogo declarado ''
- Alcance: Solo la variable documentada Institucion del diccionario 52fbcaaa-765b-4c92-8418-ccebc3fcfdcd (Donaciones de Órganos y Tejidos), definición https://example.org/mex-ontologi/definition/52fbcaaa-765b-4c92-8418-ccebc3fcfdcd%2F4. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva objeto hospitalario y evento donación. No acredita pertenencia a catálogo CLUES ni distingue publicadora/capturadora.
- Documentado vs inferencia: Documentado: 'Unidad Hospitalaria donde se realizo la donacion'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Unidad Hospitalaria donde se realizo la donacion; contraejemplo: CLUES con descripción pendiente (sin respaldo)

### Fiebre manchada (Rickettsia) — `fecha_fin_trat_ricket`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-fin-tratamiento-rickettsia` — Fecha de término de tratamiento para rickettsiosis; conserva evento término y enfermedad. Población paciente solo contextual.
- Regla propuesta: `fecha-fin-tratamiento-rickettsia` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de termino de tratamiento para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F171`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `71114fe3000c34648951eb44c3b03a660501e52a1c7a86c463bd02fc3462d17f`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_fin_trat_ricket del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F171. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva evento término y enfermedad. Población paciente solo contextual.
- Documentado vs inferencia: Documentado: 'Fecha de termino de tratamiento para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de termino de tratamiento para rickettsiosis; contraejemplo: Fecha de inicio (evento distinto)

### Fiebre manchada (Rickettsia) — `fecha_ingreso`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-ingreso-paciente` — Fecha de ingreso del paciente según su diccionario; no especifica servicio ni institución de ingreso.
- Regla propuesta: `fecha-ingreso-paciente` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de ingreso del paciente', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F122`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `c44f56eb6597d3aea8e9a1895bd3a4e87c1889fe39737fe9a78492fe6d6926d7`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_ingreso del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F122. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: no especifica servicio ni institución de ingreso.
- Documentado vs inferencia: Documentado: 'Fecha de ingreso del paciente'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de ingreso del paciente = 2024-05-01; contraejemplo: Fecha de egreso del paciente (no es ingreso)

### Fiebre manchada (Rickettsia) — `fecha_ini_trat_ricket`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-inicio-tratamiento-rickettsia` — Fecha de inicio de tratamiento para rickettsiosis; conserva evento inicio y enfermedad. Población paciente implícita por contexto, no declarada en la definición.
- Regla propuesta: `fecha-inicio-tratamiento-rickettsia` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de inicio de tratamiento para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F170`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `03ace0fe6eb4b31f68cc7b1bd21020a1917915323a6d85b8562b2ce82ad8d9ba`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_ini_trat_ricket del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F170. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva evento inicio y enfermedad. Población paciente implícita por contexto, no declarada en la definición.
- Documentado vs inferencia: Documentado: 'Fecha de inicio de tratamiento para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de inicio de tratamiento para rickettsiosis; contraejemplo: Fecha de término (evento distinto)

### Fiebre manchada (Rickettsia) — `fecha_recep_rickett_sangre`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-recepcion-sangre-rickettsia` — Fecha de recepción de la primera muestra de sangre para rickettsiosis; conserva muestra sangre y secuencia primera. No equivale a toma ni a resultado.
- Regla propuesta: `fecha-recepcion-sangre-rickettsia` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de recepción de primera muestra de sangre para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F160`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `acac085686e81639dd8302d22bf5c550b4c63457b63285b72df81d23ae4f3025`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_recep_rickett_sangre del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F160. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva muestra sangre y secuencia primera. No equivale a toma ni a resultado.
- Documentado vs inferencia: Documentado: 'Fecha de recepción de primera muestra de sangre para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de recepción de primera muestra de sangre para rickettsiosis; contraejemplo: Fecha de recepción de suero (muestra distinta)

### Fiebre manchada (Rickettsia) — `fecha_recep_rickett_ser1`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-recepcion-suero-rickettsia-ser1` — Fecha de recepción de la primera muestra de suero para rickettsiosis según su definición; conserva «primera muestra de suero». «ser1» es identificador de la variable, no prueba tipificada. No equivale a toma ni a resultado.
- Regla propuesta: `fecha-recepcion-suero-rickettsia-ser1` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de recepción de primera muestra de suero para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F156`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `7acfcf13545a39b97dd6bb1f86ee7cb3ebca25225c9980b477d294759751d18d`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_recep_rickett_ser1 del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F156. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva «primera muestra de suero». «ser1» es identificador de la variable, no prueba tipificada. No equivale a toma ni a resultado.
- Documentado vs inferencia: Documentado: 'Fecha de recepción de primera muestra de suero para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de recepción de primera muestra de suero para rickettsiosis; contraejemplo: Fecha de toma (evento distinto)

### Fiebre manchada (Rickettsia) — `fecha_resultado_rickett_rtpcr`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-resultado-pcr-tiempo-real-rickettsia` — Fecha de resultado «PCR tiempo real» para rickettsiosis según su definición; conserva la expresión documentada sin tipificar ensayo. No equivale a toma, recepción ni a resultado de suero.
- Regla propuesta: `fecha-resultado-pcr-tiempo-real-rickettsia` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de resultado PCR tiempo real para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F167`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `5e50a9e078eb066f98cc57a44a4e85c34084a73f6932993285f18ccd45cc4e5f`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_resultado_rickett_rtpcr del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F167. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva la expresión documentada sin tipificar ensayo. No equivale a toma, recepción ni a resultado de suero.
- Documentado vs inferencia: Documentado: 'Fecha de resultado PCR tiempo real para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de resultado PCR tiempo real para rickettsiosis; contraejemplo: Fecha de resultado de primera muestra de suero (muestra/expresión distinta)

### Fiebre manchada (Rickettsia) — `fecha_resultado_rickett_ser1`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-resultado-suero-rickettsia-ser1` — Fecha de resultado de la primera muestra de suero para rickettsiosis según su definición (texto original «suer»); conserva «primera muestra de suero». «ser1» es identificador de la variable sin deducir prueba. No equivale a toma, recepción ni a «PCR tiempo real».
- Regla propuesta: `fecha-resultado-suero-rickettsia-ser1` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de resultado de la primera muestra de suer para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F157`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `e1e372021336d839cf3bc0165da66355938e7ce845e74920f95cd6c85d52f164`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_resultado_rickett_ser1 del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F157. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva «primera muestra de suero». «ser1» es identificador de la variable sin deducir prueba. No equivale a toma, recepción ni a «PCR tiempo real».
- Documentado vs inferencia: Documentado: 'Fecha de resultado de la primera muestra de suer para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de resultado de la primera muestra de suero para rickettsiosis; contraejemplo: Fecha de resultado «PCR tiempo real» (expresión distinta)

### Fiebre manchada (Rickettsia) — `fecha_toma_rickett_sangre`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-toma-sangre-rickettsia` — Fecha de toma de muestra de sangre para rickettsiosis; conserva muestra sangre. La definición no precisa secuencia ni prueba posterior.
- Regla propuesta: `fecha-toma-sangre-rickettsia` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de toma muestra de sangre para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F159`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `d7c7d8a271ed777f712b45f809bf981eaa4efa782aad9ae7d0c440f7942c135a`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_toma_rickett_sangre del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F159. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva muestra sangre. La definición no precisa secuencia ni prueba posterior.
- Documentado vs inferencia: Documentado: 'Fecha de toma muestra de sangre para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de toma muestra de sangre para rickettsiosis; contraejemplo: Fecha de toma de suero (muestra distinta)

### Fiebre manchada (Rickettsia) — `fecha_toma_rickett_ser1`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-toma-suero-rickettsia-ser1` — Fecha en la que se toma la primera muestra de suero para rickettsiosis según su definición; conserva la expresión documentada «primera muestra de suero». «ser1» se conserva como identificador de la variable sin deducir tipo de prueba serológica. No equivale a recepción ni a resultado.
- Regla propuesta: `fecha-toma-suero-rickettsia-ser1` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que se toma la primera muestra de suero para rickettsiosis', def `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F155`, diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto `5494daa1-09ca-4750-aeac-2558553700e1`, huella `c7f25229e7f3978b89732a1edbadbf2c0593c2629449180e0576eb7634e4b28f`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_toma_rickett_ser1 del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada (Rickettsia)), definición https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F155. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva la expresión documentada «primera muestra de suero». «ser1» se conserva como identificador de la variable sin deducir tipo de prueba serológica. No equivale a recepción ni a resultado.
- Documentado vs inferencia: Documentado: 'Fecha en la que se toma la primera muestra de suero para rickettsiosis'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que se toma la primera muestra de suero para rickettsiosis; contraejemplo: Fecha de recepción de esa muestra (evento distinto)

### Indice de marginación por localidad — `CVE_LOC`
- Decisión: **mantener_pendiente** (descripcion_generica_insuficiente: Descripción genérica o ambigua: no precisa evento, papel, unidad o representación para respaldar concepto/regla.)
- Concepto/regla: ninguno (pista previa `localidad` no promocionada)
- Evidencia: descripción literal 'Clave geográfica', def `https://example.org/mex-ontologi/definition/251309e5-0309-46ed-9711-77a1dd408eeb%2F1`, diccionario `251309e5-0309-46ed-9711-77a1dd408eeb`, conjunto `b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f`, huella `e94b7111521507993b7fdc300e1f645d879d4b3433e915de0c0ed5b86bd31578`, catálogo declarado ''
- Alcance: Solo la variable documentada CVE_LOC del diccionario 251309e5-0309-46ed-9711-77a1dd408eeb (Indice de marginación por localidad). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Clave geográfica'. Inferencia separada: ninguna; mantener pendiente.

### Información Sobre Nacimientos — `CLUES`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `unidad-salud` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F83`, diccionario `22202305-2d02-4c49-b216-cc98224357f0`, conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd`, huella `8acb1135cdd9dbc95750049533a5dacc41a05b4da37d6fe4ea9d19ea5b059a1d`, catálogo declarado ''
- Alcance: Solo la variable documentada CLUES del diccionario 22202305-2d02-4c49-b216-cc98224357f0 (Información Sobre Nacimientos). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Información Sobre Nacimientos — `LOCALIDADCERTIFICA`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `localidad` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F104`, diccionario `22202305-2d02-4c49-b216-cc98224357f0`, conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd`, huella `bda091e282317f0b810033ac9f31188dcecfe6208940a47fae73f4fb6ca85499`, catálogo declarado ''
- Alcance: Solo la variable documentada LOCALIDADCERTIFICA del diccionario 22202305-2d02-4c49-b216-cc98224357f0 (Información Sobre Nacimientos). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Información Sobre Nacimientos — `LOCALIDADCERTIFICAD`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `localidad` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F105`, diccionario `22202305-2d02-4c49-b216-cc98224357f0`, conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd`, huella `c77a7050ed8af0bf7ab37ca07a830539d720a02adb9c4722d417fcdcdabd4146`, catálogo declarado ''
- Alcance: Solo la variable documentada LOCALIDADCERTIFICAD del diccionario 22202305-2d02-4c49-b216-cc98224357f0 (Información Sobre Nacimientos). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Información Sobre Nacimientos — `MUNICIPIOCERTIFICA`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `municipio` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F102`, diccionario `22202305-2d02-4c49-b216-cc98224357f0`, conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd`, huella `21c7fce4e834b211e513fcdc8b55a757dc5afc3da9e2b846db7aba776cfbfdf5`, catálogo declarado ''
- Alcance: Solo la variable documentada MUNICIPIOCERTIFICA del diccionario 22202305-2d02-4c49-b216-cc98224357f0 (Información Sobre Nacimientos). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Información Sobre Nacimientos — `MUNICIPIOCERTIFICAD`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `municipio` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F103`, diccionario `22202305-2d02-4c49-b216-cc98224357f0`, conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd`, huella `305e3ccb01619f50cab0ded3a82e6211d21b4dcbebecd506e6911f6b489cf8f3`, catálogo declarado ''
- Alcance: Solo la variable documentada MUNICIPIOCERTIFICAD del diccionario 22202305-2d02-4c49-b216-cc98224357f0 (Información Sobre Nacimientos). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Fecha de alternativa de titulación de examen prof.`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F66`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `e7e0a6b9c15be989bb0faca42c9b29e55a557cd16b0d417fbb4ba533330970d2`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de alternativa de titulación de examen prof. del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Fecha de alternativa de titulación de no exigibilidad`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F64`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `6759b8b1157290027ece3602d7dff3c8609984dfbbf14c5408e656de0fe1b612`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de alternativa de titulación de no exigibilidad del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Fecha de baja`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-baja-alumno` — Fecha de baja del alumno; conserva población y evento baja. Distinta de inscripción y reinscripción.
- Regla propuesta: `fecha-baja-alumno` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el alumno se dio de baja', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F59`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `3d15c35ec09f95e97e04b0f65c32d93d2836218220c19d484ee1c98264334889`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de baja del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes), definición https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F59. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población y evento baja. Distinta de inscripción y reinscripción.
- Documentado vs inferencia: Documentado: 'Fecha en la que el alumno se dio de baja'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el alumno se dio de baja; contraejemplo: Fecha de reinscripción (evento distinto)

### Matrículas de Estudiantes — `Fecha de impresión del título profesional`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F68`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `0475086a02e3cd9f2d50ded42b978d782edb3e1ea742601c0c0b40fec2e43d58`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de impresión del título profesional del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Fecha de la convalidación`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F69`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `a0792669fb9fb33d8e517cc98ef71161b90ee12f10a620cfa84b647522a5c6c1`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de la convalidación del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Fecha de la equivalencia`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F70`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `1fe84a93ab498ab4d7dc47f0a54b4ad5278e0d9194e5cc00c06c3028927ff3b3`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de la equivalencia del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Fecha de titulación del título profesional`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F67`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `de5cd0cf3209d047b3dbc8b3a76992f8a52c6e1f6d5b20ca452b762f6b10e993`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de titulación del título profesional del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Fecha inscripción ciclo escolar actual`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-inscripcion-alumno` — Fecha de inscripción del alumno al ciclo escolar actual; conserva población alumno y evento inscripción. Ciclo referenciado sin resolver periodo.
- Regla propuesta: `fecha-inscripcion-alumno` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el alumno se inscribio al ciclo escolar actual', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F10`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `e39791526022d18b25ecc242b67f91e162b7bf11f9789e435473ca88e032d166`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha inscripción ciclo escolar actual del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes), definición https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F10. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población alumno y evento inscripción. Ciclo referenciado sin resolver periodo.
- Documentado vs inferencia: Documentado: 'Fecha en la que el alumno se inscribio al ciclo escolar actual'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el alumno se inscribio al ciclo escolar actual; contraejemplo: Fecha de reinscripción (evento distinto)

### Matrículas de Estudiantes — `Fecha inscripción en ciclo escolar  señalado`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F14`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `940c1f77837c39791ee0904bbe8123c69948da90bfc9965f38db9aacf6e680ec`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha inscripción en ciclo escolar  señalado del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `Municipio`
- Decisión: **mantener_pendiente** (descripcion_truncada: Descripción truncada/incompleta: «Municipio donde el alumno» sin verbo ni papel territorial; no se infiere residencia, escuela ni nacimiento.)
- Concepto/regla: ninguno (pista previa `municipio` no promocionada)
- Evidencia: descripción literal 'Municipio donde el alumno', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F20`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `ad458441825d75edce0abc7e0082d73b2e3fbc9ec36dbb1687451d73ff9d3eba`, catálogo declarado ''
- Alcance: Solo la variable documentada Municipio del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Municipio donde el alumno'. Inferencia separada: ninguna; mantener pendiente.

### Matrículas de Estudiantes — `fecha de reinscripción`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-reinscripcion-alumno` — Fecha de reinscripción del alumno; conserva población y evento reinscripción. Distinta de inscripción inicial y de baja.
- Regla propuesta: `fecha-reinscripcion-alumno` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que se reinscribió el alumno', def `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F38`, diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d`, conjunto `e819466c-7282-46c5-84e9-65917dd8cc85`, huella `62d7d4ba78b8fb437cc3d4ce7cbdfe9a2805d7cdb4b4068e52b0f2b8271ce193`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha de reinscripción del diccionario 8c0e76ff-3a86-4b1d-beee-b04bebe7df8d (Matrículas de Estudiantes), definición https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F38. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población y evento reinscripción. Distinta de inscripción inicial y de baja.
- Documentado vs inferencia: Documentado: 'Fecha en la que se reinscribió el alumno'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que se reinscribió el alumno; contraejemplo: Fecha de inscripción inicial (evento distinto)

### Personas desaparecidas en Sonora — `fecha_nac_vic`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-nacimiento-victima` — Fecha de nacimiento de la víctima; conserva población víctima y evento nacimiento. Distinta de nacimiento de titulado o alumno.
- Regla propuesta: `fecha-nacimiento-victima` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de nacimiento de la víctima', def `https://example.org/mex-ontologi/definition/5e430f3c-09d9-4402-9f75-4cae840d5421%2F2`, diccionario `5e430f3c-09d9-4402-9f75-4cae840d5421`, conjunto `4c1084b7-b038-4084-83b2-5fe042b09ffb`, huella `ef5dde019318d8de934d2f01837d852fcea23369b627bf8f22efb22048f041a5`, catálogo declarado ''
- Alcance: Solo la variable documentada fecha_nac_vic del diccionario 5e430f3c-09d9-4402-9f75-4cae840d5421 (Personas desaparecidas en Sonora), definición https://example.org/mex-ontologi/definition/5e430f3c-09d9-4402-9f75-4cae840d5421%2F2. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población víctima y evento nacimiento. Distinta de nacimiento de titulado o alumno.
- Documentado vs inferencia: Documentado: 'Fecha de nacimiento de la víctima'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de nacimiento de la víctima; contraejemplo: Fecha del reporte de la víctima (evento distinto)

### Poblacion Ceresos — `periodo`
- Decisión: **mantener_pendiente** (descripcion_generica_insuficiente: Descripción genérica o ambigua: no precisa evento, papel, unidad o representación para respaldar concepto/regla.)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'perido del cual se informa la numero de poblacion', def `https://example.org/mex-ontologi/definition/2fc2fbc6-e918-4d5d-b907-1191e266b131%2F5`, diccionario `2fc2fbc6-e918-4d5d-b907-1191e266b131`, conjunto `5f2e31dd-83e8-4445-b132-cd0925045941`, huella `4a69626fb56cbe2f69696a21ea48a6eb10b6042fd2af693aae1dd333436a1fa2`, catálogo declarado ''
- Alcance: Solo la variable documentada periodo del diccionario 2fc2fbc6-e918-4d5d-b907-1191e266b131 (Poblacion Ceresos). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'perido del cual se informa la numero de poblacion'. Inferencia separada: ninguna; mantener pendiente.

### Producción minera  — `Mes`
- Decisión: **mantener_pendiente** (descripcion_generica_insuficiente: Descripción genérica o ambigua: no precisa evento, papel, unidad o representación para respaldar concepto/regla.)
- Concepto/regla: ninguno (pista previa `tiempo` no promocionada)
- Evidencia: descripción literal 'Registro cronológico de la produción del metal extraido', def `https://example.org/mex-ontologi/definition/587a3ccd-a814-4190-8e6f-dfb20ccf44c4%2F1`, diccionario `587a3ccd-a814-4190-8e6f-dfb20ccf44c4`, conjunto `7e97d026-d773-47b1-a0ec-078cce93fd13`, huella `ec8c0b4b563119912bb74e809f9b97b7c99d6d2ac10dcb5b7ca988fbd585e1b8`, catálogo declarado ''
- Alcance: Solo la variable documentada Mes del diccionario 587a3ccd-a814-4190-8e6f-dfb20ccf44c4 (Producción minera ). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Registro cronológico de la produción del metal extraido'. Inferencia separada: ninguna; mantener pendiente.

### Relación de Titulados - Licenciatura — `Fecha de Titulación`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-titulacion-titulado` — Fecha en que el titulado se tituló; distinta de ingreso y egreso. Conserva población titulado.
- Regla propuesta: `fecha-titulacion-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el titulado se tituló', def `https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F7`, diccionario `5b587fca-6317-43a2-bdb3-6b3b046a0e76`, conjunto `ccec926d-f2c7-4a12-8ca1-0738afd35b2c`, huella `f1f1e2d28ef0c9014eac2808fd0369de52ca309de153b100836eda6ff341241b`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de Titulación del diccionario 5b587fca-6317-43a2-bdb3-6b3b046a0e76 (Relación de Titulados - Licenciatura), definición https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F7. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: distinta de ingreso y egreso. Conserva población titulado.
- Documentado vs inferencia: Documentado: 'Fecha en la que el titulado se tituló'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el titulado se tituló; contraejemplo: Fecha de egreso (evento distinto)

### Relación de Titulados - Licenciatura — `Fecha de egreso`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-egreso-institucion-titulado` — Fecha de egreso del titulado de la institución; conserva población y evento egreso. Institución no identificada en la definición.
- Regla propuesta: `fecha-egreso-institucion-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el titulado egreso de la institucion', def `https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F6`, diccionario `5b587fca-6317-43a2-bdb3-6b3b046a0e76`, conjunto `ccec926d-f2c7-4a12-8ca1-0738afd35b2c`, huella `6b5e888e586cb44bf27c9e79c9139017f88e778a0083f1fa61d487e2dfc29a9c`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de egreso del diccionario 5b587fca-6317-43a2-bdb3-6b3b046a0e76 (Relación de Titulados - Licenciatura), definición https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F6. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población y evento egreso. Institución no identificada en la definición.
- Documentado vs inferencia: Documentado: 'Fecha en la que el titulado egreso de la institucion'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el titulado egreso de la institucion; contraejemplo: Fecha de ingreso (evento distinto)

### Relación de Titulados - Licenciatura — `Fecha de ingreso`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-ingreso-institucion-titulado` — Fecha de ingreso del titulado a la institución; conserva población y evento ingreso. La definición no identifica institución concreta.
- Regla propuesta: `fecha-ingreso-institucion-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el titulado ingreso a la institucion', def `https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F5`, diccionario `5b587fca-6317-43a2-bdb3-6b3b046a0e76`, conjunto `ccec926d-f2c7-4a12-8ca1-0738afd35b2c`, huella `f28d4fcb558cfaca1f9bc675800a63763f37c7c15c9f7b6b34809f0e6b4e52be`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de ingreso del diccionario 5b587fca-6317-43a2-bdb3-6b3b046a0e76 (Relación de Titulados - Licenciatura), definición https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F5. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población y evento ingreso. La definición no identifica institución concreta.
- Documentado vs inferencia: Documentado: 'Fecha en la que el titulado ingreso a la institucion'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el titulado ingreso a la institucion; contraejemplo: Fecha de egreso (evento distinto)

### Relación de Titulados - Licenciatura — `Fecha de nacimiento`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-nacimiento-titulado` — Fecha de nacimiento del titulado; conserva población titulado y evento nacimiento. No precisa lugar.
- Regla propuesta: `fecha-nacimiento-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de nacimiento del titulado', def `https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F2`, diccionario `5b587fca-6317-43a2-bdb3-6b3b046a0e76`, conjunto `ccec926d-f2c7-4a12-8ca1-0738afd35b2c`, huella `9949b5c82a2ecf85259978f7f5f36877091bd1aa02d2daf4bf6db8cdb8a2d8bc`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de nacimiento del diccionario 5b587fca-6317-43a2-bdb3-6b3b046a0e76 (Relación de Titulados - Licenciatura), definición https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F2. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población titulado y evento nacimiento. No precisa lugar.
- Documentado vs inferencia: Documentado: 'Fecha de nacimiento del titulado'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de nacimiento del titulado; contraejemplo: Fecha de nacimiento de la víctima (población distinta)

### Relación de Titulados - Posgrado — `Fecha de Titulación`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-titulacion-titulado` — Fecha en que el titulado se tituló; distinta de ingreso y egreso. Conserva población titulado.
- Regla propuesta: `fecha-titulacion-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el titulado se tituló', def `https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F7`, diccionario `3f4a7c9e-78ed-4f0d-93b1-595c07e4059f`, conjunto `598143a6-6ab1-464c-a9fd-8f4ff49d6223`, huella `f1f1e2d28ef0c9014eac2808fd0369de52ca309de153b100836eda6ff341241b`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de Titulación del diccionario 3f4a7c9e-78ed-4f0d-93b1-595c07e4059f (Relación de Titulados - Posgrado), definición https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F7. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: distinta de ingreso y egreso. Conserva población titulado.
- Documentado vs inferencia: Documentado: 'Fecha en la que el titulado se tituló'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el titulado se tituló; contraejemplo: Fecha de egreso (evento distinto)

### Relación de Titulados - Posgrado — `Fecha de egreso`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-egreso-institucion-titulado` — Fecha de egreso del titulado de la institución; conserva población y evento egreso. Institución no identificada en la definición.
- Regla propuesta: `fecha-egreso-institucion-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el titulado egreso de la institucion', def `https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F6`, diccionario `3f4a7c9e-78ed-4f0d-93b1-595c07e4059f`, conjunto `598143a6-6ab1-464c-a9fd-8f4ff49d6223`, huella `6b5e888e586cb44bf27c9e79c9139017f88e778a0083f1fa61d487e2dfc29a9c`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de egreso del diccionario 3f4a7c9e-78ed-4f0d-93b1-595c07e4059f (Relación de Titulados - Posgrado), definición https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F6. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población y evento egreso. Institución no identificada en la definición.
- Documentado vs inferencia: Documentado: 'Fecha en la que el titulado egreso de la institucion'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el titulado egreso de la institucion; contraejemplo: Fecha de ingreso (evento distinto)

### Relación de Titulados - Posgrado — `Fecha de ingreso`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-ingreso-institucion-titulado` — Fecha de ingreso del titulado a la institución; conserva población y evento ingreso. La definición no identifica institución concreta.
- Regla propuesta: `fecha-ingreso-institucion-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha en la que el titulado ingreso a la institucion', def `https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F5`, diccionario `3f4a7c9e-78ed-4f0d-93b1-595c07e4059f`, conjunto `598143a6-6ab1-464c-a9fd-8f4ff49d6223`, huella `f28d4fcb558cfaca1f9bc675800a63763f37c7c15c9f7b6b34809f0e6b4e52be`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de ingreso del diccionario 3f4a7c9e-78ed-4f0d-93b1-595c07e4059f (Relación de Titulados - Posgrado), definición https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F5. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población y evento ingreso. La definición no identifica institución concreta.
- Documentado vs inferencia: Documentado: 'Fecha en la que el titulado ingreso a la institucion'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha en la que el titulado ingreso a la institucion; contraejemplo: Fecha de egreso (evento distinto)

### Relación de Titulados - Posgrado — `Fecha de nacimiento`
- Decisión: **proponer**
- Concepto propuesto (nuevo): `fecha-nacimiento-titulado` — Fecha de nacimiento del titulado; conserva población titulado y evento nacimiento. No precisa lugar.
- Regla propuesta: `fecha-nacimiento-titulado` (representación `fecha`)
- Evidencia: descripción literal 'Fecha de nacimiento del titulado', def `https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F2`, diccionario `3f4a7c9e-78ed-4f0d-93b1-595c07e4059f`, conjunto `598143a6-6ab1-464c-a9fd-8f4ff49d6223`, huella `9949b5c82a2ecf85259978f7f5f36877091bd1aa02d2daf4bf6db8cdb8a2d8bc`, catálogo declarado ''
- Alcance: Solo la variable documentada Fecha de nacimiento del diccionario 3f4a7c9e-78ed-4f0d-93b1-595c07e4059f (Relación de Titulados - Posgrado), definición https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F2. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.
- Limitaciones: conserva población titulado y evento nacimiento. No precisa lugar.
- Documentado vs inferencia: Documentado: 'Fecha de nacimiento del titulado'. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.
- Ejemplo positivo: Fecha de nacimiento del titulado; contraejemplo: Fecha de nacimiento de la víctima (población distinta)

### Sistema Epidemiológico y Estadístico de Defunciones — `CLUES`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `unidad-salud` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F38`, diccionario `12f684e9-f4d5-4714-933d-aa153a812174`, conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c`, huella `1b32ad8dbecd8c74b4f0bfd3497c88a32c8b2f8590a4a9f42f2b10717804423b`, catálogo declarado ''
- Alcance: Solo la variable documentada CLUES del diccionario 12f684e9-f4d5-4714-933d-aa153a812174 (Sistema Epidemiológico y Estadístico de Defunciones). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Sistema Epidemiológico y Estadístico de Defunciones — `LOCALIDADOCURRENCIA`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `localidad` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F74`, diccionario `12f684e9-f4d5-4714-933d-aa153a812174`, conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c`, huella `0485c56408609aa3a1cab7e67e8e7b1f0b4ee7cd6607fbe8c97de194423cac9d`, catálogo declarado ''
- Alcance: Solo la variable documentada LOCALIDADOCURRENCIA del diccionario 12f684e9-f4d5-4714-933d-aa153a812174 (Sistema Epidemiológico y Estadístico de Defunciones). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Sistema Epidemiológico y Estadístico de Defunciones — `LOCALIDADOCURRENCIAD`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `localidad` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F75`, diccionario `12f684e9-f4d5-4714-933d-aa153a812174`, conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c`, huella `6f76513d06bf1de37df4a91e3103ac0e3782913df200633ca0673e907e345bd4`, catálogo declarado ''
- Alcance: Solo la variable documentada LOCALIDADOCURRENCIAD del diccionario 12f684e9-f4d5-4714-933d-aa153a812174 (Sistema Epidemiológico y Estadístico de Defunciones). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Sistema Epidemiológico y Estadístico de Defunciones — `MUNICIPIOOCURRENCIA`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `municipio` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F72`, diccionario `12f684e9-f4d5-4714-933d-aa153a812174`, conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c`, huella `da9a0fcd2979fbcca215523a090a0332d76bfb531c9f92fecae3bd347819febf`, catálogo declarado ''
- Alcance: Solo la variable documentada MUNICIPIOOCURRENCIA del diccionario 12f684e9-f4d5-4714-933d-aa153a812174 (Sistema Epidemiológico y Estadístico de Defunciones). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

### Sistema Epidemiológico y Estadístico de Defunciones — `MUNICIPIOOCURRENCIAD`
- Decisión: **mantener_pendiente** (descripcion_pendiente_explicita: Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).)
- Concepto/regla: ninguno (pista previa `municipio` no promocionada)
- Evidencia: descripción literal 'Pendiente de especificar', def `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F73`, diccionario `12f684e9-f4d5-4714-933d-aa153a812174`, conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c`, huella `45f58439a5c544c88713e5f5ba62c1a0ddf40f9aa6181a506e30f6d50a6e1b85`, catálogo declarado ''
- Alcance: Solo la variable documentada MUNICIPIOOCURRENCIAD del diccionario 12f684e9-f4d5-4714-933d-aa153a812174 (Sistema Epidemiológico y Estadístico de Defunciones). Permanece candidata; no se propone concepto ni regla.
- Limitaciones: Sin respaldo suficiente en la definición; no deducir por el nombre de la variable.
- Documentado vs inferencia: Documentado: 'Pendiente de especificar'. Inferencia separada: ninguna; mantener pendiente.

## Reglas nuevas (20) — ejemplos y contraejemplos
- `fecha-baja-alumno` (fecha): +Fecha en la que el alumno se dio de baja / −Fecha de reinscripción (evento distinto)
- `fecha-denuncia` (fecha): +Fecha de la denuncia en Denuncias Ambientales / −TRIMESTRE del estrato (granularidad y evento distintos)
- `fecha-egreso-institucion-titulado` (fecha): +Fecha en la que el titulado egreso de la institucion / −Fecha de ingreso (evento distinto)
- `fecha-fin-tratamiento-rickettsia` (fecha): +Fecha de termino de tratamiento para rickettsiosis / −Fecha de inicio (evento distinto)
- `fecha-ingreso-institucion-titulado` (fecha): +Fecha en la que el titulado ingreso a la institucion / −Fecha de egreso (evento distinto)
- `fecha-ingreso-paciente` (fecha): +Fecha de ingreso del paciente = 2024-05-01 / −Fecha de egreso del paciente (no es ingreso)
- `fecha-inicio-tratamiento-rickettsia` (fecha): +Fecha de inicio de tratamiento para rickettsiosis / −Fecha de término (evento distinto)
- `fecha-inscripcion-alumno` (fecha): +Fecha en la que el alumno se inscribio al ciclo escolar actual / −Fecha de reinscripción (evento distinto)
- `fecha-nacimiento-titulado` (fecha): +Fecha de nacimiento del titulado / −Fecha de nacimiento de la víctima (población distinta)
- `fecha-nacimiento-victima` (fecha): +Fecha de nacimiento de la víctima / −Fecha del reporte de la víctima (evento distinto)
- `fecha-recepcion-sangre-rickettsia` (fecha): +Fecha de recepción de primera muestra de sangre para rickettsiosis / −Fecha de recepción de suero (muestra distinta)
- `fecha-recepcion-suero-rickettsia-ser1` (fecha): +Fecha de recepción de primera muestra de suero para rickettsiosis / −Fecha de toma (evento distinto)
- `fecha-reinscripcion-alumno` (fecha): +Fecha en la que se reinscribió el alumno / −Fecha de inscripción inicial (evento distinto)
- `fecha-resultado-pcr-tiempo-real-rickettsia` (fecha): +Fecha de resultado PCR tiempo real para rickettsiosis / −Fecha de resultado de primera muestra de suero (muestra/expresión distinta)
- `fecha-resultado-suero-rickettsia-ser1` (fecha): +Fecha de resultado de la primera muestra de suero para rickettsiosis / −Fecha de resultado «PCR tiempo real» (expresión distinta)
- `fecha-titulacion-titulado` (fecha): +Fecha en la que el titulado se tituló / −Fecha de egreso (evento distinto)
- `fecha-toma-sangre-rickettsia` (fecha): +Fecha de toma muestra de sangre para rickettsiosis / −Fecha de toma de suero (muestra distinta)
- `fecha-toma-suero-rickettsia-ser1` (fecha): +Fecha en la que se toma la primera muestra de suero para rickettsiosis / −Fecha de recepción de esa muestra (evento distinto)
- `mes-atencion` (mes): +meses en que se brindó la atención / −Año de captura (evento distinto)
- `unidad-hospitalaria-donacion` (no_especificada): +Unidad Hospitalaria donde se realizo la donacion / −CLUES con descripción pendiente (sin respaldo)

No aplicado a `ontologia/semantica.json` ni a `data/semantica/*`.