# Nueva pista DGIS 2026-10-24 — Total_Egresos (f89137ba…/15)

Fecha consulta: 2026-10-24. Proveedor/herramienta: webfetch nativa (opencode).
URL primaria: http://www.dgis.salud.gob.mx/contenidos/basesdedatos/bdc_egresoshosp_gobmx.html
Resultado: la página lista el enlace "Descripción de variables" en
http://sinba08.salud.gob.mx/cubos/Metadatos/Dat-ehosp-Descripcion_de_variables.html
(tabla SECRETARÍA DE SALUD, fila 1) y declara "Última modificación: Martes 21 de
abril de 2026". Texto extraído íntegro abajo.

Contraste con ronda 2c (línea agotada, no repetida como nueva): el archivo de
variables sigue sin ser recuperable por estas vías:
- GET http://sinba08.salud.gob.mx/cubos/Metadatos/Dat-ehosp-Descripcion_de_variables.html
  → marco vacío (solo imagen principal.jpg, sin tabla).
- GET https://sinba08.salud.gob.mx/cubos/Metadatos/Dat-ehosp-Descripcion_de_variables.html
  → error de transporte (sin contenido).
Conclusión: pista nueva concreta (enlace directo sinba08 no intentado en 2c)
examinada y agotada el 2026-10-24; no fija qué cuenta Total_Egresos
(egresos vs urgencias). Brecha exacta subsistente: sin cambio. Error HTTP/timeout
NO se interpreta como inexistencia del documento.

--- TEXTO EXTRAÍDO (bdc_egresoshosp_gobmx.html) ---
Egresos Hospitalarios Cubos dinámicos. La información sobre egresos
hospitalarios permite conocer la demanda de atención de los servicios de
hospitalización (morbilidad: todos los casos atendidos en hospitalización;
mortalidad 2000-2017: motivo del egreso = defunción). SSA 2000-2023 cifras
definitivas; 2024 OPD IMSS Bienestar definitivas; 2025 definitivas; 2026
preliminares. Sector Salud 2004-2024 definitivas, 2025-2026 preliminares.
"Las variables que incluye el cubo, así como su descripción y las categorías
correspondientes se pueden consultar en el archivo 'Descripción de variables'."
Tabla: [Metadatos](http://sinba08.salud.gob.mx/cubos/Metadatos/Dat-ehosp-Fuentes_de_informacion.html)
[Descripción de variables](http://sinba08.salud.gob.mx/cubos/Metadatos/Dat-ehosp-Descripcion_de_variables.html).
