# Ronda 4 — Auditoría-b (vínculos): resultado (revalidación final)

Alcance: vínculos de lote-1..6 reentregados (incluidas 336 adicionales) + 5
propuestas de ambigüedades, y código de integración (`integrador/codigo` +
`comprobar.py`, `fijar_aceptaciones.py`, `instalar.py`,
`verificar_studio.py`). Solo se escribe en `auditoria-b`; controles solo
leídos, sin editar ni instalar.

## Verificación por vínculo (3601/3601 aceptar, 0 rechazar, 0 condicionado)

Por cada vínculo: IRI física en inventario+inspección, recurso/campo/hoja/
posición y `huella_esquema`, diccionario del mismo conjunto, contexto de
publicación, descripción + `huella_fila_diccionario` recomputada desde la fila
RAW, concepto respaldado en núcleo o con regla nueva literal exacta
(nombres/descripciones/conjuntos/diccionarios/definición única/huella),
veredicto vigente de auditoría-a sobre la regla de soporte, ausencia de
aliases globales, no solape con la base 865, criterio presente.

- Cambios revalidados por IDs exactos (no por conteo): lote-2/3/6 con
  conceptos/representaciones/límites corregidos; lote-4 con reglas
  025/026/027 retiradas y sus 3 vínculos (P36/P39/P40) pasados a pendientes
  —dictámenes de retirados eliminados—; lote-6 con límites.
- Dependencia semántica resuelta contra auditoría-a actual (172 aceptar,
  `estado completo-reentregas-finales`, SHAs coincidentes): `r4-lote-1-001`
  aceptada (3 vínculos fiebre `ide_id → /1` sin condición pendiente;
  exclusión estructural de `/177` y `/178` verificada en RAW);
  `tiempo-9/10/11` corregidas y aceptadas; 025/026/027 retiradas sin exigir
  su inclusión. Ninguna propuesta rechazada sigue vigente.
- 5 columnas ambiguas resueltas producen 5 vínculos revisados (2 plantas con
  reglas vigentes `r3a10-0286`/`0288` + 3 fiebre con dependencia resuelta).
  Las 7 filas alternativas previas (177/178 ×3 + Clave /4) quedan solo como
  evidencia histórica; no son vínculos revisados. Presas sigue pendiente.
- Duplicados de nombre en conjunto: solo esos 5 vínculos, todos con
  `definicion_iri` propio. Resto con nombre único.
- Muestreo semántico por lote coherente; `clave-especie-pecuaria` compartido
  con límite explícito en regla.

## Observaciones (5 recalculadas contra base 865/1212)

- `egresos-descripcion-urgencias`: pendiente vigente.
- `municipio-formato-ejemplo`: significado resuelto; pendiente solo
  composición `nnn` vs `26048`.
- `fecha-ejemplo-numerico`: significado resuelto; pendiente solo
  codificación `DD/MM/AAAA` vs `45658`.
- `anio-nacimientos-2024`: pendiente vigente (campo datastore sin vínculo).
- `anio-divorcios-2023`: nota histórica; alias ya `documental_revisada`;
  sin petición nueva.

## Código (SHA actual, sellado tras los 2 cambios finales)

- `fijar_aceptaciones.py` (`44acd4a3`): whitelist de `chat` con
  `ensayo-gemma4` y `ensayo-gemini31` además de `antes-cambio-modelo` (14
  nombres públicos). Exclusión total de secretos verificada por barrido
  (`chat/` sin `.env`/claves/tokens/pem; los 3 directorios solo traen
  `evaluacion.json` y `respuestas-saneadas.json`). Nota: el `ignore` por
  nombre deja esos subdirectorios copiados vacíos; conservador, no arrastra
  secretos ni rompe manifiesto. Guardas de bloqueo/cobertura exacta/de
  código intactas.
- `instalar.py` (`f6cd37e0`): `sys.path.insert(0, codigo/scripts)` tras
  `root/scripts` → `construir` resuelve al generador PREPARADO (PIN
  `definition_pin` presente en staged, ausente en live que lo rechaza; la
  simulación necesita el nuevo ANTES de instalarlo). `construir_catalogo`
  solo existe en `scripts/` (sin sombreado) y
  `ROOT=Path(__file__).parents[1]` absoluto: ROOT real preservado,
  verificado por importación con el mismo orden. Línea 79 duplica el insert
  (idempotente). Núcleo y evidencia fijada intactos (no instalado).
- Resto sin cambios (`consolidar 14af513c`, `ronda_3 94b00456`,
  `ronda_4 4a6fa72a`, tests y `comprobar`/`verificar` idénticos).
- Tests: 10/10 OK (`test_ronda_4` 6 + `test_seleccion_documental` 4).

## Bloqueos

Ninguno. Dependencia externa resuelta: auditoría-a reemitida y coincidente.

## Cuentas

- Vínculos: 3601 (746+708+344+669+530+599+5) → aceptar 3601.
- `sha_entregas` finales y `sha_codigo` actual en `entrega.json`.
