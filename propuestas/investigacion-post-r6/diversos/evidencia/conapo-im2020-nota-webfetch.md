# Nota de observación web — CONAPO Índices de marginación 2020 (2026-10-24)

URL: https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372
Fecha de consulta (UTC): 2026-10-24
Método: lectura web directa (render). La descarga cruda por CLI el mismo día
devolvió página de reto de seguridad (preservada en `conapo-im2020.html`,
sha256 be2600c1835b908b…, 1829 bytes); el contenido real descrito abajo se
observó vía render y coincide con el enlace de Fuentes extras declarado por el
publicador en CKAN (`ckan-marginacion.json`).

Fragmentos observados (transcripción breve):
- Título: "Índices de marginación 2020" — Consejo Nacional de Población,
  04 de octubre de 2021.
- "En cada caso, se ofrece la publicación que contiene el apartado conceptual
  de la marginación… así como los anexos estadísticos, cartográficos y
  metodológicos… En cada caso… y por primera ocasión, una estimación a nivel
  de colonias."
- "Índice de marginación urbana 2020 / Base de datos a nivel colonia 2020" →
  https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Colonia/IMC_2020.zip
- "Cartografía digital (shp) del índice de marginación urbana por colonia 2020" →
  https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Colonia/imc2020_shp.zip
- "Programa de cálculo a nivel colonia 2020" →
  https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Marginacion/Indice_de_marginacion_urbana_por_colonia_2020.rar
- Documentos: "Índice de marginación urbana 2020 [Descargar documento]
  /cms/uploads/attachment/file/828844/urbana.pdf" (mismo objeto que la
  evidencia R6 `CONAPO_IMU_2020_urbana.pdf`, sha256 21b5e823…).

Alcance: la página acredita que existe base de datos y cartografía CONAPO a
nivel colonia (sigla IMC_2020, igual que la hoja local `IMC_2020` del recurso
09ef2342). NO acredita el sentido de la variable local CLASIF ni su dominio
de 7 valores: no se descargaron ni examinaron IMC_2020.zip / shp (fuera del
mínimo necesario; el vínculo publicador↔CONAPO/CONAPO↔columna local sigue
ausente). Línea futura acotada: comparar campos de IMC_2020.zip/shp contra la
columna física CLASIF (pos 5, hoja IMC_2020) y la lista de 7 valores.
