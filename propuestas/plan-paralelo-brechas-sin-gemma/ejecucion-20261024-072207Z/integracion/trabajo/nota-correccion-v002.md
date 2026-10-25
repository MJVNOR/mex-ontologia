# Corrección v002: filtro textual sustituido por controles estructurales

## Defecto (v001, `codigo/integrar_ronda_7.py`)

`_prohibido()` serializaba la regla/vínculo/concepto completos a texto y
buscaba subcadenas (`homolog`, `equivalen`, `nueva vigencia`, …). Dos fallos:

1. **Falsos positivos sobre negaciones válidas**: rechaza límites como
   `sin homologación` o `no equivalencias`, que son descargos legítimos
   (v001 ya comprobó que las 31 propuestas no disparan el filtro, pero
   cualquier regla futura con esos descargos sería vetada).
2. **No prueba nada semánticamente**: la presencia/ausencia de una palabra
   no demuestra el efecto (una equivalencia real no necesita la palabra
   `equivalencia`; una negación la contiene).

## Sustitución (v002, sin NLP frágil)

El texto libre (`descripciones`, `limites`, `criterio`, `evidencia`) queda
**sujeto a auditoría documental A/B**, sin vetos de contenido en código.
El código controla estructura, que sí decide efectos:

- **Esquema cerrado**: claves permitidas fijas (`REGLA_KEYS`,
  `VINCULO_KEYS`); sin campos para equivalencias, vigencias, joins o
  identidad de catálogos — esos efectos no tienen dónde expresarse.
- **Alcance mínimo por regla**: `definiciones == [1 IRI del universo 31]`,
  `nombres` y `descripciones` listas de longitud exactamente 1 (un único
  nombre y descripción exactos, sin expandir a otras variables),
  `diccionarios`/`conjuntos` pinnados a SINAC, huella de fila obligatoria,
  `evidencia`/`criterio`/`alcance` no vacíos, límites escritos.
- **Conceptos**: toda regla/vínculo referencia un concepto existente en la
  base o nuevo del lote; todo concepto nuevo es referenciado por ≥1 regla
  (sin sobrantes); broader existe en base o lote; clave nueva obligatoria
  (reutilizar en su lugar si un concepto existente representa el sentido).
- **Vínculos**: columna del allowlist de 20, `definicion_iri` respaldada en
  el mismo lote y `concepto` idéntico al de su regla (el core ya lo exige en
  `consolidar_semantica.py:271`; v002 lo comprueba antes).
- **Procedencia y aprobación**: orígenes con SHA pinnados por manifiesto
  (manifiesto + cada archivo e insumo verificados por hash), doble `aceptar`
  A+B por regla y por vínculo, base R6 exacta, unicidad de ids/definiciones/
  columnas, exactitud final `rules == expected`.

## Por qué los efectos prohibidos son estructuralmente imposibles

`construir()` emite solo `PROV.wasDerivedFrom` + `mex.sha256Evidencia`
sobre nodos ya materializados por el core; ni R7 ni el core crean
`owl:sameAs`, `skos:exactMatch`, joins, vigencias o fusiones de catálogos a
partir de reglas/vínculos (el vocabulario de `consolidar_semantica.py` no
tiene esos predicados para esta vía). La correspondencia exacta al
manifiesto la garantiza el pin de hashes, no el texto.

## Base R6 aclarada (defecto documental v001)

- `0dd6f0f7…1407bd` = hash del **fichero congelado**
  `data/integracion-ronda-6/base-semantica.json` (1276 reglas, 4474
  vínculos, 1075 conceptos). Verificado 2026-10-24.
- `a30a2842…fc68ca` = hash del **estado vivo**
  `ontologia/semantica.json` = base R6 + vínculo de presas R6
  (1276 reglas, 4475 vínculos; `sem == base+aceptadas` comprobado por
  bytes). No es la base de R7.
- Al integrar, `data/integracion-ronda-7/base-semantica.json` se **copia
  byte-idéntica del fichero real** (`cp`, sin reescritura ni normalización)
  y su SHA debe seguir siendo `0dd6f0f7…1407bd`. No mover estas fuentes.
