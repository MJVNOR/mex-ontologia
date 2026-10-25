# Hook minimo propuesto para el motor (aplica el integrador una vez liberado)

Precondiciones: entrega aprobada SHA
`cd77771d358cd7720710fee44ff70a6e6b184f56c95289160a706794e1d382e9` verificada,
staging/`resumen-cruces-r3.json` generado, shapes extendidas con
`RevisionCruceRonda3`, `ComparacionMunicipal2020` y `EvidenciaFuenteComparacion`.

```python
# scripts/consolidar_semantica.py, junto a integrar_ronda_2 / integrar_cobertura:
from integrar_cruces_r3 import construir as integrar_cruces_r3
cruces_data, cruces_report, cruces_sources = integrar_cruces_r3(base)
data += cruces_data
report["integracion_cruces_r3"] = cruces_report
sources.update(cruces_sources)
```

(Copiar `staging/integrar_cruces_r3.py` a `scripts/`; alli `ROOT`/`PROV` se importan
de `construir_catalogo` y `AG` se resuelve desde la config del integrador.)

El TTL es solo evidencia calificada (3 fichas + 72 yuxtaposiciones 2020 con
evidencia separada por fuente): no habilita cruces, no crea sameAs/exactMatch,
no afirma vigencia ni equivalencia INEGI.
