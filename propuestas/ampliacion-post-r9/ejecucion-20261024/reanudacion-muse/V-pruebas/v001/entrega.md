# V-pruebas v001 — Ronda 10 (reanudación Muse)

18/18 pruebas en verde. Sin instalaciones ni cambios fuera de esta carpeta.

## Material verificado (real, congelado)

- `aceptadas.json` SHA `df5705eaf…b9c2031c`: 5 unidades Q-U02…Q-U06, 6 formas.
- Cada unidad: fila (`canon` == huella), índice 1-based == `indice_definicion` Q-v003
  y posición en `definiciones` de la fuente, nombre + `Unidad de medida` exactos,
  normativa SHA + `3.5.3` + URI canónica, `normativa_uri == unidad_qdt`.
- Q-U06 Datastore (`api_diccionario`): sin campos `http`/`completo`; URL API https válida.
- `datos/unidades.ttl`: 60 triples exactos, sujetos == 5 declarados, whitelist K completa.
- `shapes/adicionales.ttl`: 6 NodeShapes == formas declaradas, con objetos PROV
  (`wasDerivedFrom` real admitido).
- Snapshot inmutable: resumen R9 exacto (1423/1106/4506/17/1442 y resto),
  `base-semantica` PIN `dba467e…`, viva == fijada, `config-iri-base.toml` byte a byte
  con `config.toml`. Sello previo cubre los 16 archivos del payload.

## Mutaciones rechazadas (7 vías)

Triple extra, objeto M3 prohibido, factor de conversión, literal con datatype
no-xsd en shapes, unidad M3, forma fantasma, unidad duplicada: todas `ValueError`.

## Contrato completo (raíz TEMP, copias exactas)

`cargar`, `construir` (recibo 5 declaraciones + 6 formas, grafo >60 con trazas
PROV) y `cargar_shapes` (6 NodeShapes) sobre copias exactas de config, semántica
y payload + auditorías **reales** A/B (aceptan, SHA exacto, 11/11 casos).
Manifiesto/config temporales generados solo de esas copias.
Rechazo verificado: retirar/cambiar cada auditoría, su SHA o su lista de casos
(2×5), y núcleo o IRI cambiados.

## Pendiente

Nada: las auditorías A/B llegaron durante la ejecución y el contrato se ejecutó
completo, sin skips. Re-ejecutable luego con `python test_ronda_10.py`; si las
auditorías faltaran, el contrato queda PENDIENTE declarado y los rechazos siguen
corriendo con andamio inválido (nunca acepta).
