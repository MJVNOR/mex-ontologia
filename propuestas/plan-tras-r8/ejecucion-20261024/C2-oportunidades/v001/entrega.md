# C2-oportunidades — vista nueva de prioridad con overlay R8 (auditoría derivada)

Fecha UTC: ver `v001/entrega.json`. Estado: `auditoria_derivada`. Casos asignados: 0.

## 1. Qué se hizo

Recálculo local de prioridad sobre el mapa `data/portal/oportunidades-cruce.json` (2026-10-23, 3916 pares, 1191 candidatas), sin reescribir el original, aplicando cobertura R8 y las 6 condiciones de conexión. No se promueve ningún join.

## 2. Vigencia del mapa (por SHA, código)

4/4 insumos vigentes — SHA actual == `huellas_entrada` del mapa:

- `data/portal/inventario.json`
- `data/portal/contenido-inspeccion.json`
- `data/portal/cruce-registro-civil.json`
- `data/catalogo/catalogo.ttl`

Ver `entrega.json → resultados.vigencia_insumos_mapa` y `fuentes[]`. Conclusión: mapa estructuralmente vigente, pero semánticamente anterior a R8 (2026-10-23 vs cierre R8 2026-10-24). Requiere overlay R8, no regeneración.

## 3. Overlay R8 requerido

Vista semántica que el mapa no contiene:

- `ontologia/semantica.json`: 1106 conceptos, 1423 significados, 6 condiciones (catálogo, rol, periodo, contexto, grano, unidad).
- `data/semantica/cobertura.json` integración R8: 0 significados/conceptos nuevos, 28 vínculos SINAC locales (mismo conjunto), 4506 revisadas, 17 candidatas dependientes de significado.
- `reports/pendientes-semanticos.json`: 138 significados reales, 16 vigencias (V13/V14 sin acceso), `des_mpo_res`, 2 encabezados corruptos, 5 observaciones.

Efecto: toda fila sigue `candidata_por_validar` hasta tener significado respaldado + columna física específica + 6 condiciones (puerta 1 del plan).

## 4. Criterio reproducible

`v001/criterio.json`: `score = suma(pesos_familia) + suma(penalizaciones)`; orden `score desc, id asc`.

- Pesos: municipio 3, localidad 3, unidad_salud_clues 3, division_territorial 2, clasificacion_delito 2, producto_especie 2, programa_educativo 2, periodo/entidad/anio/mes 1, estratos 0.5.
- Penaliza: sentidos distintos −4, sentido parcial −2, código↔nombre −2, programa sin institución −2, localidad/municipio sin contexto −1, CLUES sin vigencia −2, etc.
- `publicador_comun` y `anios_en_nombres` NO suman (pistas débiles, solo informativas). Reproducir con `v001/consultas/reproducir.py`.

## 5. Grupos de datos y prerrequisitos

- G1 educación (programa+estrato): exige institución+plan+homologación; no mezclar nuevo ingreso/reingreso/titulado.
- G2 salud (CLUES+sexo+municipio): exige catálogo CLUES y vigencia; sexo declarado no identifica registros.
- G3 agro/territorial (municipio+división+periodo+producto): municipio exige entidad; DDR/cuenca no es catálogo oficial; producto exige taxonomía.
- G4 seguridad/911/ITAMA (municipio+localidad+división+periodo+delito): localidad exige entidad+municipio; metodologías anterior/actual no mezclables.
- G5 registro civil (anio+mes+municipio): distinguir registro/ocurrencia/residencia; único cruce ejecutado (matrimonios↔divorcios 2022) no autoriza otros.
- G6 marginación/demografía (entidad+municipio+localidad): niveles distintos no se suman.
- G7 solo-municipio (1093 pares `revisar`): prioridad más baja; compartir municipio no identifica filas.

Oportunidad ≠ join aprobado. No se comparan poblaciones/roles/unidades distintos solo por concepto.

## 6. Archivos

- `v001/entrega.json` (esta vista, estado auditoria_derivada)
- `v001/prioridades_top50.csv` (top 50, rango 1: ITAMA Internamiento↔Externamiento score 5.0, 8 familias)
- `v001/matriz_pares_relevantes.csv` (1191 pares, con score, pendientes, publicador_n, años)
- `v001/criterio.json`
- `v001/consultas/reproducir.py`, `v001/fixtures/par_ejemplo.json`
- `v001/congelada.json` (SHA256 por código de todos los archivos de la entrega)

## 7. Límites y aceptación

Sin web (no hay `peticiones-web.json`: sin pista primaria concreta), sin Gemma, sin contactos externos, sin tocar producción/semántica/shapes/manifiestos/grafo/Studio. Aceptar si: 4/4 SHA vigentes, SHA R8 == base.json, CSV reproducibles, ninguna fila declara join, fuentes verificables, congelada por código.
