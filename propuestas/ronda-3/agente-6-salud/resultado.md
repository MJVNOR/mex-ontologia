# Agente 6 Salud — ronda 3

Partición exclusiva: 242 definiciones fuera del núcleo actual (Vigilancia Epidemiológica 56, Fiebre manchada 166, Atencion de Urgencias 6, Donaciones 5, Consulta Externa 3, Egresos Hospitalarios 6).

## Totales

- Decisiones: 242 (partición completa, sin omitidos ni duplicados).
- Proponer significado: 203.
- Pendientes con razón: 39.
- Reglas nuevas restringidas (conjunto+diccionario+definición+nombre+descripción+representación+huella): 203.
- Conceptos nuevos estrechos: 178. Conceptos vigentes reutilizados: 6 (entidad, municipio-residencia, municipio-ubicacion, organizacion, sexo-declarado, unidad-salud).

## Pendientes por razón

- abreviatura_sin_texto_publicado: 3.
- codigo_sin_catalogo_acreditado: 2.
- descripcion_generica_sin_objeto: 1.
- descripcion_pendiente_en_fuente: 22.
- fila_diccionario_danada: 2.
- identificador_sin_significado: 2.
- objeto_indeterminado_texto_libre: 3.
- objeto_no_especificado: 1.
- observacion_vigente_contradiccion: 1.
- periodo_sin_evento_acreditado: 1.
- rango_contradictorio_nombre_descripcion: 1.

## Verificación

- Huellas de fila de diccionario recalculadas desde inspección central: 242/242.
- Cobertura/asignación/semántica verificadas en lectura (103 conceptos, 232 respaldadas, 836 revisadas, 118 candidatas, 116 reglas).
- Sin colisiones con reglas vigentes. Verificador propio: scripts/verificar.py (positivos para las 242 + 9 negativos).

## Revisión manual vs automatización

- Manual: lectura literal individual de las 242 definiciones (descripción, tipo, formato, unidad, ejemplo, catálogo, detalle de catálogo) desde la inspección central; cada decisión quedó codificada en tablas explícitas por (diccionario, índice) en scripts/paso2_generar.py (PEND2, REUSE2, FIJOS, FECHAS, LABS, JURISD, MESES/EDADES) o en la plantilla de descripción de bandera de síntoma.
- Manual: 22 pendientes por descripción 'Pendiente de especificar' sin inferir por nombre (incluye aparentes instituciones y sufijos f); identificadores, indeterminados, abreviaturas SNC/CQ, CIE sin versión, filas 177/178 dañadas y Total_Egresos con observación vigente.
- Manual: contradicciones nombre vs descripción preservadas sin resolver (p. ej. de01_a_04 dice 'entre 1 y 5 años'; typos vigilanciade/incio/sonmnolencia/hipercusia/transtornos/inmunoflourecencia/ricketsiosis/romaña/metrorrragia).
- Automatizado: aplicación mecánica de esas tablas, generación de reglas/conceptos, recálculo de huellas, simulación de interpretacion() en memoria y negativos. Ninguna regla deduce significado desde regex de nombre: toda propuesta exige descripción exacta + conjunto + diccionario + definición.
- Criterio de unidades: sin unidades añadidas por costumbre (edad conserva 'en años' literal; temperatura conserva 'Grados celcius' sin homologar; conteos conservan objeto literal; sin porcentajes ni monetarios en la partición).

## Límites

- Sin nuevas correspondencias columna-variable; no se acredita vigencia, identidad, catálogos ni equivalencias.
- Fila 177/178 de fiebre manchada dañada (desplazada); se preserva literal y queda pendiente.
- 'SNC' y 'CQ' sin expansión en texto: pendientes, no se reconocen abreviaturas.
- Códigos CIE sin versión/vigencia: pendientes, no se promueven a catálogo.
- Total_Egresos mantiene observación vigente de contradicción: pendiente.
