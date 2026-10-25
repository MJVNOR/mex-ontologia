# Q-unidades v002 — formato de integracion

## Que entrega v002

`propuesta-q-unidades.ttl`: 6 `mex:UnidadDeclarada`, una por definicion, con
`mex:unidadLiteral` exacto y sin `mex:unidadQudt`. Nada mas se afirma.

Predicados usados, todos ya presentes en el vocabulario instalado
(`data/portal/ampliacion.ttl`, verificado por codigo):

| predicado | objeto | comprobacion |
| --- | --- | --- |
| `mex:variableDocumentada` | IRI `documented-variable/...%2F<n>` | coincide con `cobertura.json` |
| `mex:definicionFuente` | IRI `definition/...%2F<n>` | indice de fila exacto |
| `mex:conjuntoFuente` | literal uuid | `cobertura.json` |
| `mex:diccionarioFuente` | literal uuid | `cobertura.json` |
| `mex:unidadLiteral` | literal exacto de fila | sin normalizar |
| `prov:wasDerivedFrom` | URL del recurso | `fuente` de la inspeccion |

## Estado por caso

| caso | literal | estado | condicion para promover |
| --- | --- | --- | --- |
| Q-U01 | `Toneladas` | `pendiente_ambiguedad_tonelada` | evidencia **local** que declare tonelada metrica |
| Q-U02 | `Kilogramos` | `pendiente_verificacion_W` | sello W de Q-W-02 |
| Q-U03 | `MW` | `pendiente_verificacion_W` | sello W de Q-W-03 |
| Q-U04 | `GWh` | `pendiente_verificacion_W` | sello W de Q-W-04 |
| Q-U05 | `Porcentaje` | `pendiente_verificacion_W` | sello W de Q-W-05 |
| Q-U06 | `Grados celcius` | `pendiente_verificacion_W` | sello W de Q-W-06 |

v002 **no es integrable como esta**: falta el vinculo normativo. La version
integrable (v003 o posterior) se produce cuando W selle las peticiones, y solo
para los casos que ademas tengan respaldo local no ambiguo.

## Como se integra (carril I, escritor central unico)

1. Dos auditorias independientes sobre los bytes de v002 y del sello W.
2. Copiar la declaracion aceptada y anadir, **solo** en los casos promovidos:

   ```turtle
   mex:unidadQudt <http://qudt.org/vocab/unit/...> ;
   ```

   y `mex:evidenciaNormativa` con la ruta de la evidencia W, su `sha256` y el
   `sha256` del sello W. Mismo patron que R9
   (`P1-qudt/v003/propuesta-qudt.ttl`).
3. Q-U01 no se promueve por sello W: el estandar no decide la unidad local.
   Se queda como declaracion cualificada o fuera, segun dictamen.
4. Verificar con `consultas/q1..q3` mas SHACL del portal; comprobar que no se
   altera nada ajeno.

## Prohibiciones (aplican a Q y a I)

- Nada de `QuantityValue` global ni por variable.
- Sin factores, conversiones ni sustituciones (hm3 -> M3 incluido).
- Sin atribucion global de unidad a un diccionario o conjunto.
- Sin URIs QUDT no selladas por W; sin alias por parecido.
- No se editan R1–R9, manifiestos, `config.toml` ni Studio.
- v002 no instala, no regenera grafo y no escribe fuera de su carpeta.
