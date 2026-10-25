# Gate R8: negativa IRI variable — B-tecnica

- Payload auditado: `materializacion/v001/aceptadas.json` (SHA `555c3569…`, **no aplicar**).
- Gate auditado: `T-pruebas/v002` scope R8 (reglas `[]`, conceptos `{}`, columnas ⊆ candidatas).

## Dictamen (código): el gate actual NO rechaza el defecto

Simulación por código contra el payload v001: el scope R8 **pasa** (`True`)
con los 14 `definicion_iri` defectuosos, porque solo mira columnas y
vaciado de reglas/conceptos. Nunca valida el namespace del IRI.

Negativa exigida (añadir al gate R8 y al futuro `integrar_ronda_8`):

```python
for v in aceptadas_r8['vinculos']:
    assert RE_DEFINICION_SINAC.match(v['definicion_iri']), v['columna']  # /definition/ exacto, nunca /documented-variable/
    var = variables_cobertura[v['definicion_iri']]  # KeyError = rechaza: entidad distinta, sin alias
    assert var['estado'] == 'respaldada_por_definicion' and var['concepto'] == v['concepto']
    assert v['huella_fila_diccionario'] == var['huella_fila_diccionario']
```

- Contra v001: **rechaza 14/28** (ordinales 65, 67, 69, 71, 72, 74, 76, 77,
  79, 84, 87, 89, 97, 99). `/documented-variable/` es el `iri` de variable,
  entidad distinta de `/definition/`; payload debe rechazar, no alias.
- Contra `M2-sinac/v002/entrega.json`: **acepta 14/14** (0 malas; coincide
  con `definicion_iri` de asignación). Material v002 se hará luego sobre v002.

## Corrección pedida al coordinador

1. No aplicar el payload 555c.
2. Material v002 solo sobre M2 v002 (IRI ya exactos).
3. Endurecer el gate con la negativa de arriba + validación de forma del
   vínculo (claves/huellas/concepto), pues hoy la extensión exacta suma filas
   R8 sin validar su forma.

## Otros defectos reales

- `M2-sinac/v002/entrega.md` cabecera dice "v001" (`construir_v002.py`
  `lineas[0]`); cosmético, datos intactos.
- Gate R8 no valida forma de vínculo al extender la base exacta; incluirlo
  junto con la negativa IRI.

## Conservación histórica

`auditoria-material.json/md` (v001: 14 aceptar / 14 rechazar) intactos;
este dictamen es adicional. Solo lectura fuera de `B-tecnica/`; staging
no editado. Detalle máquina en `gate-r8-iri-negativa.json` (SHAs por código).
