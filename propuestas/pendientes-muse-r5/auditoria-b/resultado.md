# Ronda 5 — Auditoría-b: resultado (entregas cerradas; catálogos-web en seguimiento)

Solo se escribe en `auditoria-b`. Sin tocar core/Studio/.env ni otras entregas.
Base R4 inmutable; cobertura/semántica live solo leídas.

## Entregas cerradas (SHA verificado contra listo y control)

- `nacimientos` `eec89c6c…` ✓ (54 decisiones, 1 regla + 1 vínculo).
- `defunciones` `4f58c543…` ✓ (32 pendientes, 0 propuestas: nada que dictaminar).
- `epidemiologia` contenido `5145bbe2…` ✓ pero `listo.json` usa clave
  `sha256_entrega_json` en vez de `sha256_entrega` → dictamen **corregir**
  (renombrar clave, sin tocar entrega). 25 pendientes, 0 propuestas.
- `diversos` `231f4d97…` ✓ (5 pendientes + 2 artefactos, 0 propuestas).
- `presas` `020dc960…` ✓ (reentregada tras el snapshot de control, que aún
  cita `914cf5…`: control desactualizado, no la entrega).
- `matriculas` `e8ce4f70…` ✓ (30 pendientes, 15 propuestas retiradas,
  0 reglas: sin dictamen). `tic` `d720e428…` ✓ (7 reglas proponer,
  0 vínculos; 7 columnas en `columnas-adicionales.json`, `adicionales.json`
  en revisión → links al cierre).
- Pendiente: `catalogos-web` (sigue buscando en Obscura; no se espera; su
  cierre se revisará después). Sin control Obscura.

## Propuesta nacimientos — columna 18 (aceptar regla + vínculo)

Verificación exacta, sin aprobar por nombre:

- Física: recurso `46977217`, hoja `SINAC 2022 26-09-22` (106 campos),
  pos 18 = `RESIDEEXTRANJEROD`; `huella_esquema=9b46e1c0…` recomputada ✓.
- Fila: diccionario `22202305`, fila 18 `RESIDEEXTRANJEROD`/Texto/
  `Indicador textual de si la madre es residente extranjera`/ejemplo `NO`;
  `huella_fila=3c0156d2…` recomputada de RAW ✓. Unicidad en conjunto
  `940de7d8` ✓, variable `fuera_del_nucleo_actual` (requiere regla) ✓, sin
  alias (campo == variable) ✓, sin solape con base ✓.
- Regla `r5-nac-resideextranjerod-no_especificada`: literal exacta
  (nombres/descripciones/conjuntos/diccionarios/definición única/huella),
  concepto nuevo `residencia-extranjera-madre` limitado a lo documentado
  (3 elementos, padre nulo), calificador completo.
- Provenance con contradicción de tipo: `/17 RESIDEEXTRANJERO` es
  Numérico entero (`…recidente…`, ejemplo `2`) vs `/18` Texto; no se
  unifican, con precedente `r3a7-nac-resideextranjero-codigo` vigente.
  Límites y criterio explícitos.

## Presas — columna Clave (aceptar pendiente, no forzar)

- Física re-verificada: hoja `cat_estatal` (17 campos), pos 1 `Clave`
  única, `huella_esquema=29af60e8…` ✓.
- Diccionario completo (22 filas): f1 `Histórico_presas`
  (`87295257…`) vs f4 `Catálogo_estatal` (`d1208344…`), ambas
  `respaldada_por_definicion` con el mismo concepto; columna con 2
  `ambigua_por_nombre` vigentes ✓.
- `cat_estatal` ≠ `catálogo`/`catalogo`; la hoja física difiere del
  catálogo (trae `Cuenca hidrologica` sin fila, omite `Comision`/
  `Subdireccion`/`Rio`; homónimos pos 15/16 = /19//21 sin correspondencia).
  Sin recurso Histórico_presas ni datastore, el dominio compartido no es
  verificable. Elegir /1 o /4 sería aprobar por nombre → pendiente correcto.

## Dictámenes (11: 10 aceptar, 1 corregir, 0 rechazar)

- aceptar `r5-nac-resideextranjerod-no_especificada` + aceptar vínculo
  columna 18 (evidencia supra).
- aceptar pendiente presas `…/cat_estatal/1` (no forzar).
- aceptar `r5-tic-001..007` (filas literales exactas, huellas RAW
  verificadas, fuera_del_nucleo, nombre único; `sector-…` reutiliza
  núcleo exacto; lecciones R4 como límites; vínculos aún no propuestos).
- corregir `epidemiologia/listo.json` (clave SHA).
- `matriculas`: 0 propuestas (15 retiradas) → sin dictamen; 30 pendientes.
- 7 links TIC (`columnas-adicionales.json`, `adicionales.json` ausente):
  auditoría al cierre, sin espera pasiva. Manifiesto se fija al terminar.
- Simulación esperada: 1384/4466 → 1392/4467 (+8 significados, +1 vínculo).

Cuentas: 23 checks OK + 7 reglas TIC verificadas, 0 fallos. Catálogos (17) y
`catalogos-web`: seguimiento al cierre, fuera de este dictamen.
