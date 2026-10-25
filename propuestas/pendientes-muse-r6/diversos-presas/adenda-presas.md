# Adenda presas: vinculo Clave -> /4 (Catalogo_estatal)

Una columna resuelta con archivo autentico. No toca `entrega.json`, `listo.json` ni el nucleo.

## Decision

`.../cat_estatal/1` Clave -> `.../definition/bfb8788b...%2F4` (Catalogo_estatal): **proponer** (vinculo documental).

## Por que /4 y no /1 (estructura, no nombre)

- Bytes identicos: `web/evidencia/cat_estatal_1.xlsx` (11981 B, PK, SHA `b7a398a0...`) = `sha256_fragmento_o_archivo` de la inspeccion historica. Sin sustitucion; la captura original rige. (Mi HEAD CLI dio 403 WAF ese dia; la descarga web fue 200 normal: bytes identicos mandan.)
- Hoja `cat_estatal`: 10 filas (cabecera + 9 presas), 17 columnas en el mismo orden inspeccionado. Clave = 9 str unicos de 5 chars (LCDSO, PECSO, AOBSO, AGZCH, ARCSO, PMOSO, ARLSO, CHTSO, IRASO).
- Objeto Historico_presas = serie (Clave + Fecha AAAA/MM/DD + Almacenamiento Float) segun diccionario; la hoja fisica integra el objeto de atributos por presa (13 columnas hermanas ya `documental_revisada` a Catalogo_estatal) y la ausencia de columnas de fecha/almacenamiento lo corrobora sin ser por si sola la prueba. /1 excluido por incompatibilidad de objeto.
- Objeto Catalogo_estatal = atributos por presa: 13 columnas fisicas ya `documental_revisada` en cobertura a filas de esa hoja (/7,/20,/8,/9,/10,/11,/12,/13,/15,/16,/17,/18,/22; cobertura registra 15 correspondencias del recurso = 13 + 2 ambiguas de Clave; el conteo previo de 14 era incorrecto). Clave pos 1 es la llave de fila del mismo objeto; /4 (Texto/CCCCC, "Contiene la clave identificadora de cada presa") coincide en objeto, tipo, formato y posicion.
- Huellas calculadas por script con `scripts/consolidar_semantica.huella` sobre inspeccion `tablas[0]` y diccionario `definiciones[3]`, asignadas directamente al vinculo (validacion len-64 + hex). La cita R5 de la fila /4 omitia caracteres; rige el valor recomputado en `adenda-presas.json`.

## Limites (alcance documental)

Denota la clave declarada; sin catalogo publicado identificado en las fuentes consultadas que la valide. Sin joins por Clave (ni con /1). Sin identidad de dominios entre hojas. Sin edicion/vigencia (recurso creado 19-01-2024, periodo 2023-01-01: metadato citado, no acreditacion). La hoja fisica no es espejo de Catalogo_estatal (omite Comision/Subdireccion/Rio; pos 3/15/16 sin correspondencia). Significados /1 y /4 sin cambio.

## Archivos

- `adenda-presas.json` (decision + vinculo exacto + huellas + fuentes)
- `adenda-presas.sha.json` (marker SHA desde bytes, separado; no toca `listo.json`)
