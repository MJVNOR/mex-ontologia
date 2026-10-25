# Entrega R8 v003 (staging, no produccion)

Solo 28 vinculos SINAC con significado ya respaldado en R7; 0 reglas, 0 conceptos.
Endurece v002: guarda `UNIVERSO_28 <= candidatas`; fila coteja definicion/variable/campo/descripcion local; auditoria exige dictamen global `aceptar`.
Evidencia aceptadas = material final v003 (`db3167f9...`); rechaza URI-wrong M2 v001 y descriptor amplio v002.

## Archivos

- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/aceptadas.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/auditorias/auditoria-a.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/auditorias/auditoria-b.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/base-semantica.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/cobertura-r7.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/fuentes/M1-sinac-entrega.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/fuentes/M2-sinac-entrega.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/fuentes/aceptadas-r7.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/fuentes/cobertura-r7.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/fuentes/inspeccion-contenido.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/data/integracion-ronda-8/manifiesto.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/ontologia/revision-ronda-8.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/scripts/consolidar_semantica.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/scripts/integrar_entregas.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/scripts/integrar_ronda_2.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/scripts/integrar_ronda_7.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/scripts/integrar_ronda_8.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/scripts/r8_proyeccion.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/tests/test_cargar_r8.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/tests/test_proyeccion_r8.py`

## SHAs

- aceptadas: `db3167f98a308cc4219202cfa5ce8587923dd05bc4664d30d83375872309f0d9`
- congelada: `2d13a57cc212cf4e7b53b0a73ce320b4f7555cfb4269d0898951b286a042f41c`
- manifiesto R8: `f0729af791895c8c5a3037282ab374a81a9e3c4298294571271844204fdfdb20`

## Gates

- SHA manifiesto + SHAs de evidencia
- aceptadas dual A/B con pin + dictamen global aceptar
- IRI definition exacta + UNIVERSO_28 contenido en candidatas
- fila exacta: definicion/variable/campo/descripcion local + huella + scope SINAC
- igualdad base R7
- expected = base + 28 vinculos exactos
- proyeccion 28 revisadas->candidatas solo si existe config R8; sin config, R7 intacto

Verificacion: `py_compile` OK (8), `test_proyeccion_r8` 4/4 OK, `test_cargar_r8` 9/9 OK, gates reales valid/invalid OK. Sin instalar, sin red.
