# Código v003 (no instalado; v001/v002 intactas)

v002 no verificaba `audit.aceptadas_sha256 == sha(aceptadas.json)`: una
aprobación podría referirse a otro texto. v003 lo exige para AMBAS auditorías
antes de aceptar ningún ID (`validar_sobre_base`): sin pin coincidente no hay
aprobación posible. La aprobación ata así al texto exacto revisado
(`materializacion/v001/aceptadas.json`, SHA pinnado también en las plantillas
pendientes que A/B completarán tras su review).

Cambio único respecto a v002 (ver diff): docstring + 5 líneas en
`validar_sobre_base`. `integrar_ronda_6.py` y `consolidar_semantica.py`
byte-idénticos a v002. Sin NLP frágil; núcleo, semántica, RDF y Studio
intactos; sin tests.
