# Entrega S-shacl v001 — formas adicionales acotadas

Generado en UTC: `2026-10-24T20:32:31.318531+00:00`. Carril S, carpeta exclusiva `propuestas/ampliacion-post-r9/ejecucion-20261024/S-shacl/v001/`.

## Alcance

- Formas SHACL **adicionales** para coherencia estado/significado de `VariableDocumentada`, `CorrespondenciaSemantica` y contrato de `UnidadDeclarada`.
- No se modifica `shapes/` ni ninguna entrega sellada; no se usa `sh:closed` global; no se rechazan propiedades adicionales válidas.
- La base IRI se conserva tal como está en `config.toml` (`https://example.org/mex-ontologi/`, sha256 `0fa293d24094e70d81be6df257c4081627e1d571f9fc44dabb5e7bd21b1ff0c4`); no se decide ni sustituye.
- Sin Gemma, contactos, búsquedas agotadas, manifiestos R1–R9, escritores centrales ni Studio en ejecución.

## Motor

Motor real: `tools/open-ontologies.exe` sha256 `765803297dbaaeef6fce9bcb2b1794d0bd6683a21afa7981d504722ff611e1bf`, invocado por `scripts/construir_catalogo.py:motor` con `--no-connect` y un `--data-dir` temporal por prueba. `sh:sparql` se evaluó correctamente (sin restricciones ignoradas).

Nota de implementación: este motor no compila `sh:or` cuando algún miembro usa `sh:node` (lo declara en `skipped_constraints` y deja la conformidad indeterminada). Por eso las reglas condicionales se expresan con `sh:sparql`, que sí se evalúa; no se usó `sh:or` en las formas entregadas.

## Reglas y justificación

| Regla | Clase objetivo | Restriccion | Justificacion |
| --- | --- | --- | --- |
| CorrespondenciaRevisadaVariableRespaldada | https://example.org/mex-ontologi/vocab/CorrespondenciaSemantica | sh:sparql | R5: correspondencia documental_revisada sin variableDestino respaldada_por_definicion |
| UnidadDeclaradaContrato | https://example.org/mex-ontologi/vocab/UnidadDeclarada | path https://example.org/mex-ontologi/vocab/variableDocumentada; min 1; max 1; nodeKind http://www.w3.org/ns/shacl#IRI; class https://example.org/mex-ontologi/vocab/VariableDocumentada | R6a: UnidadDeclarada requiere exactamente un mex:variableDocumentada IRI de clase VariableDocumentada |
| UnidadDeclaradaContrato | https://example.org/mex-ontologi/vocab/UnidadDeclarada | path https://example.org/mex-ontologi/vocab/definicionFuente; min 1; max 1; nodeKind http://www.w3.org/ns/shacl#IRI; class https://example.org/mex-ontologi/vocab/DefinicionVariable | R6b: UnidadDeclarada requiere exactamente un mex:definicionFuente IRI de clase DefinicionVariable |
| UnidadDeclaradaContrato | https://example.org/mex-ontologi/vocab/UnidadDeclarada | path https://example.org/mex-ontologi/vocab/unidadLiteral; min 1; max 1; datatype http://www.w3.org/2001/XMLSchema#string | R6c: UnidadDeclarada requiere exactamente una unidad literal (xsd:string) sin sustituirla por el termino normalizado |
| UnidadDeclaradaContrato | https://example.org/mex-ontologi/vocab/UnidadDeclarada | path https://example.org/mex-ontologi/vocab/unidadQudt; max 1; nodeKind http://www.w3.org/ns/shacl#IRI | R6d: UnidadDeclarada admite como maximo un mex:unidadQudt y debe ser IRI; no se impone una lista cerrada de terminos |
| UnidadDeclaradaContrato | https://example.org/mex-ontologi/vocab/UnidadDeclarada | path http://www.w3.org/ns/prov#wasDerivedFrom; min 1; nodeKind http://www.w3.org/ns/shacl#IRI | R6e: UnidadDeclarada requiere procedencia prov:wasDerivedFrom IRI |
| VariableCandidataConSignificadoCandidato | https://example.org/mex-ontologi/vocab/VariableDocumentada | sh:sparql | R3: VariableDocumentada candidata_sin_definicion_suficiente sin mex:significadoCandidato |
| VariableCandidataSinSignificadoDocumentado | https://example.org/mex-ontologi/vocab/VariableDocumentada | sh:sparql | R4: VariableDocumentada candidata_sin_definicion_suficiente con mex:significadoDocumentado |
| VariableRespaldadaConSignificadoDocumentado | https://example.org/mex-ontologi/vocab/VariableDocumentada | sh:sparql | R1: VariableDocumentada respaldada_por_definicion sin mex:significadoDocumentado |
| VariableRespaldadaSinSignificadoCandidato | https://example.org/mex-ontologi/vocab/VariableDocumentada | sh:sparql | R2: VariableDocumentada respaldada_por_definicion con mex:significadoCandidato |

## Pruebas

| Prueba | Corpus (triples) | Esperado | Conforms | Violaciones | Ignoradas | Resultado |
| --- | --- | --- | --- | --- | --- | --- |
| negativo.ttl | propuestas/ampliacion-post-r9/ejecucion-20261024/S-shacl/v001/fixtures/negativo.ttl (75) | 15 violaciones | False | 15 | 0 | OK |
| positivo-instancias-r9.ttl | propuestas/ampliacion-post-r9/ejecucion-20261024/S-shacl/v001/fixtures/positivo-instancias-r9.ttl (358) | conforme | True | 0 | 0 | OK |
| positivo.ttl | propuestas/ampliacion-post-r9/ejecucion-20261024/S-shacl/v001/fixtures/positivo.ttl (45) | conforme | True | 0 | 0 | OK |
| portal-322405 | data/portal/portal-completo.ttl (322405) | conforme | True | 0 | 0 | OK |
| studio-323014 | data/portal/studio-verificacion.ttl (323014) | conforme | True | 0 | 0 | OK |

El fixture de instancias R9 contiene 3 variables con estado `fuera_del_nucleo_actual` y 17 correspondencias `candidata_por_nombre` (incluida la de Total_Egresos). Todas conforman: no se rechazan por estas formas.

### Focus nodes de las violaciones observadas

| Prueba | Forma | focus_node |
| --- | --- | --- |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6e |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6b |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6c |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6d |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6g |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6a |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6h |
| negativo.ttl | UnidadDeclaradaContrato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r6f |
| negativo.ttl | CorrespondenciaRevisadaVariableRespaldada | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r5a |
| negativo.ttl | CorrespondenciaRevisadaVariableRespaldada | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r5b |
| negativo.ttl | CorrespondenciaRevisadaVariableRespaldada | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r5c |
| negativo.ttl | VariableCandidataSinSignificadoDocumentado | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r4 |
| negativo.ttl | VariableCandidataConSignificadoCandidato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r3 |
| negativo.ttl | VariableRespaldadaSinSignificadoCandidato | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r2 |
| negativo.ttl | VariableRespaldadaConSignificadoDocumentado | https://example.org/mex-ontologi/prueba-s-shacl/v001/n-r1 |

## Restricciones ignoradas y formas sin instancias

- Restricciones ignoradas: **0**.
- Shapes sin instancias reportadas por el motor: **1**.

```json
[
  {
    "prueba": "positivo-instancias-r9.ttl",
    "shape": "https://example.org/mex-ontologi/shapes/UnidadDeclaradaContrato",
    "target": "https://example.org/mex-ontologi/vocab/UnidadDeclarada",
    "target_class": "https://example.org/mex-ontologi/vocab/UnidadDeclarada",
    "target_form": "class"
  }
]
```

## Archivos y SHA-256

- `shapes.ttl` `0f342433c003d20cdda74fd8190cb746c8f7c665875b0584e5b5759dcf205566`
- `fixtures/esperado.json` `ac71a867855731f29121b477bd520ab3d2cf09dffe6b0799c299d2c7d8a45741`
- `fixtures/negativo.ttl` `5b3e981e753b18abcc2fb69f02c465fabe436c1a6ef5e2adc77f183c1ce7f77d`
- `fixtures/positivo-instancias-r9.ttl` `263c563c58c7818096acf08136b643820e73d82f9eb931f5146b62d1614e493e`
- `fixtures/positivo.ttl` `1d9a4ff92ecc724647fdc021e5a037939ff774766e042d088e32c5474b9eb242`

Los SHA de esta entrega, de sus entradas y del motor están en `sello.json`, calculados por este mismo script sobre los bytes escritos.

Solo se sellan los artefactos enumerados explícitamente por `validar.py`; cualquier otro archivo presente en la carpeta no forma parte de esta entrega.

## Límites

- No se promueven candidatas, no se crean correspondencias y no se toca el grafo central.
- Las copias completas se cargaron en stores temporales aislados y se eliminaron al terminar; el JSON conserva ruta temporal, conteo de triples y SHA del corpus.
- Una violación en fixtures negativos es el resultado esperado; en las copias completas el resultado esperado es conformidad total con estas formas.
- La conformidad conjunta con las formas de producción no se prueba aquí: estas formas son adicionales y su combinación corresponde a la integración central.

Resultado global: **OK** (5/5 pruebas).
