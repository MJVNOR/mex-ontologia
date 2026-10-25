# Tres análisis de pares posteriores a R9

Los tres análisis quedan bloqueados por la evidencia y validaciones disponibles. No se calcularon comparaciones de volúmenes, proporciones o distribuciones ni se ejecutaron joins. El [top 50](top50-oportunidades-r9.html) solo prioriza revisiones.

## Llamadas procedentes e improcedentes

**Pregunta:** ¿Se pueden comparar los volumenes clasificados como procedentes e improcedentes por municipio y mes? Solo calcular una proporcion si consta que las categorias forman una particion del mismo universo.

El Q1 etiquetado como improcedentes es un duplicado de procedentes; el Q2 de improcedentes carece de MUNICIPIO. Las muestras disponibles no permiten calcular la comparación municipal y mensual ni una proporción del universo.

| Comprobación | Estado en la ficha fuente |
| --- | --- |
| cardinalidad | no_acreditada |
| claves | no_acreditada |
| cobertura datos | parcial_y_asimetrica |
| grano | fila_evento_llamada_sin_agregacion_validada |
| periodo | nominal_2026_sin_verificar_contenido |
| poblacion | sin_particion_acreditada |
| unicidad | no_acreditada |
| unidades | conteo_de_llamadas_sin_unidad_fisica |

### Condiciones de reapertura

- Recurso correcto de improcedentes Q1 y esquema territorial aplicable a Q2.
- Archivos completos, periodos verificados y estrategia de agregación validada.
- Para proporciones, documento que acredite partición del mismo universo.

[Ficha y evidencia originales](../propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/resultados.json); SHA256 `8c8c3ea96f31e57aa25033f4b5d4b264e3ea5c672b3d44787a2ff19f6afab5f1`.

## Matrimonios y nacimientos registrados

**Pregunta:** Que volumenes de matrimonios y nacimientos se registran en un periodo y ambito territorial documentalmente comparables?

Los datos disponibles tienen distinto grano y las validaciones detectan totales incompatibles con hombres + mujeres y meses ausentes. Una comparación de agregados requiere validar su preparación y cobertura; la diferencia de grano por sí sola no la impide. No se interpretan tasas poblacionales ni causalidad.

| Comprobación | Estado en la ficha fuente |
| --- | --- |
| claves | no_acreditada |
| grano | distinto_bloquea_join |
| unicidad | no_acreditada |
| cardinalidad | no_acreditada |
| poblacion | distinta |
| periodo ambito | comparable_solo_en_registro_no_acreditado_para_join |
| unidades | no_homologables_sin_regla |
| cobertura | no_acreditada |

### Condiciones de reapertura

- Archivos completos y cobertura por municipio y mes.
- Aclaración o corrección de totales y meses ausentes.
- Regla documentada para agregar matrimonios y comparar periodos de registro.

[Ficha y evidencia originales](../propuestas/ampliacion-post-r9/ejecucion-20261024/A2-registro-civil/v002/resultados.json); SHA256 `c9ff005dad8e77524a8eb4f8525939c1436d951535cb8e4e6fbbd9012823edb8`.

## Internamiento y externamiento ITAMA

**Pregunta:** ¿Cómo se distribuyen los registros de internamiento y externamiento por sexo/escolaridad en un periodo común?

Faltan copias locales completas de los recursos ITAMA y respaldo del periodo observado y de escolaridad. Los trimestres son metadatos; las muestras de 29 y 16 registros no acreditan el universo completo. Comparar distribuciones agregadas será posible si se documentan grano, categorías, periodo y cobertura; aquí no se suman universos ni se vinculan personas.

| Comprobación | Estado en la ficha fuente |
| --- | --- |
| claves | sin_clave_documentada |
| grano | no_definido |
| unicidad | no_acreditada |
| cardinalidad | no_acreditada |
| poblacion | distinta_y_no_sumable |
| periodo | documental_2026_filas_no_verificado |
| unidades | no_declaradas |
| cobertura datos | insuficiente_para_distribucion |

### Condiciones de reapertura

- Copias completas de los recursos del par y alcance de cada hoja.
- Grano y periodo documentados; catálogo de sexo y definición de escolaridad aplicables.
- Comprobaciones de cobertura y recuentos reproducibles por población.

[Ficha y evidencia originales](../propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v002/resultados/analisis-a3-itama-v002.json); SHA256 `526ef2d52bbbfe0608811587b4d549b266644ec2ab93e5c954331a2cc555861d`.

## Límites

- No se ejecutaron joins ni se añadieron relaciones analíticas al grafo.
- Una muestra no demuestra unicidad ni cobertura integral; ausencia no equivale a cero.
- El ranking prioriza revisiones; no aprueba comparabilidad.

El JSON publicado conserva las ocho comprobaciones completas y su evidencia, junto con el vínculo y huella del original. Las conclusiones precisan el alcance del bloqueo sin modificar los originales.
