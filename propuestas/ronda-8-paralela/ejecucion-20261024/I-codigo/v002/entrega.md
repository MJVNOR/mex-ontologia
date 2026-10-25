# Entrega R8 v002 (staging, no produccion)

Solo 28 vinculos SINAC con significado ya respaldado en R7; 0 reglas, 0 conceptos.
Corrige v001: 14 IRI `documented-variable` -> `definition`; respaldo R7 por cobertura-r7 pinnada.

## Archivos

- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/aceptadas.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/auditorias/auditoria-a.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/auditorias/auditoria-b.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/base-semantica.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/cobertura-r7.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/fuentes/M1-sinac-entrega.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/fuentes/M2-sinac-entrega.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/fuentes/aceptadas-r7.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/fuentes/inspeccion-contenido.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/data/integracion-ronda-8/manifiesto.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/ontologia/revision-ronda-8.json`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/scripts/consolidar_semantica.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/scripts/integrar_entregas.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/scripts/integrar_ronda_2.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/scripts/integrar_ronda_7.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/scripts/integrar_ronda_8.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/scripts/r8_proyeccion.py`
- `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v002/tests/test_proyeccion_r8.py`

## SHAs

- aceptadas: `9cf983c44ed644981b999281aa97eec4c0b3b0692ab6295c6b14102b9bb632c8`
- congelada: `5644f58bd2973a8c55965f8760aabbab7e0e067ace77b2c5972913cd77ac4377`
- manifiesto R8: `b0dcfb3996e7469ccefc8f0e76c581490c426b7328d2ab0a875b86d004b7197e`

## Gates

- SHA manifiesto + SHAs de evidencia
- aceptadas dual A/B con pin
- IRI definition exacta + universo 28
- scope/huellas exactas SINAC
- igualdad base R7
- expected = base + 28 vinculos exactos
- proyeccion 28 revisadas->candidatas solo si existe config R8; sin config, R7 intacto

Verificacion: `py_compile` OK (7), `test_proyeccion_r8` 4/4 OK, gates sinteticos valid/invalid OK. Sin instalar, sin red.
