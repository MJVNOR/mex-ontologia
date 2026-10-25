# Dictamen A-auditoría v001 — aceptar

Auditor: a. Payload `payload/v001`, aceptadas SHA `df5705eaf6e0b8d8dcb0257a54a258264cda3e8adfe8655f87dfda90b9c2031c` (recalculado, coincide). 16/16 archivos del sello previo OK. 11/11 IDs aceptados (5 unidades + 6 formas).

## Unidades (verificación con código, no declaraciones)

- Q-U02..U06: `Q-unidades/v002/fuentes/<id>/fila.json` con `indice_definicion` 1-based verificado contra `definiciones[idx-1]` de la inspección original (`Nombre variable` + `Unidad de medida` exactos); `payload/v001/filas/<id>.json` idéntico a `fila.json`.
- Cobertura-R9: las 5 definiciones existen con estado `respaldada_por_definicion` y misma huella.
- Normativa W/v002 QUDT 3.5.3 exacta: KiloGM/MegaW/GigaW-HR/PERCENT/DEG_C como IRI `http://qudt.org/vocab/unit/...`; `payload/v001/normativa/<id>.txt` con SHA idéntico al de aceptadas; versión y sujeto verificados en el texto de evidencia.
- TTL `datos/unidades.ttl`: 5 sujetos r10/Q-U02..06, literales exactos (`Kilogramos`, `MW`, `GWh`, `Porcentaje`, `Grados celcius`); Q-U03/U04 comparten nombre `Unidad de Medida` pero son definiciones distintas (filas 9 y 11) sin transferencia a otras columnas; sin `QuantityValue`, sin triples de factor/conversión (solo la palabra en `rdfs:comment` de límite); Q-U01/TON y hm³ ausentes.
- Q-U06 viene de API Datastore (`metodo: api_diccionario`) y no presenta campos `http`/`completo` de ficheros: excepción admitida, su URL API es la fuente.

## Formas (6 NodeShapes reales en `S-shacl/v001/shapes.ttl` sha `0f342433...`, idéntico a `payload/v001/shapes/adicionales.ttl`)

IDs aceptados = locales NodeShape con `sh:targetClass` real; sin `sh:closed` global (solo mención en comentarios); `sh:path prov:wasDerivedFrom` presente (R6e). Motor real `open-ontologies.exe`: `negativo.ttl` 15/15 violaciones (`conforms false`), `positivo.ttl`, `portal-322405` y `studio-323014` conformes con 0 violaciones, `restricciones_ignoradas: []`.

## Código K (`K-codigo/v001/scripts`, integrador sha `05e834fd...` coincide)

`integrar_ronda_10.py` impone whitelist estructural exacta, exige auditorías `a`+`b` con SHA exacto de aceptadas y cobertura de los 11 IDs, prohíbe predicados/objetos de cantidad-conversión y excluye Toneladas/hm³ ambiguos (`_politica_literal`); hooks reales: `ampliar_portal.py` importa `cargar_shapes_r10`, `consolidar_semantica.py` invoca `integrar_ronda_10`. Coherente con lo auditado.

## Observación no bloqueante

`S-shacl/v001/sello.json` actual (`7ed238db...`) difiere del fijado en `payload-origenes.json` (`f1576589...`); el artefacto instalable `shapes.ttl` está intacto y es byte-idéntico al del payload. No afecta al dictamen.
