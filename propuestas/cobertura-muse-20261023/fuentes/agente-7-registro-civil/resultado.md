# Agente 7 ronda 3 — registro civil (Divorcios / Defunciones / Nacimientos / Matrimonios)

## Base verificada (real, recalculada)

- `data/semantica/cobertura.json` sha256 `38d0e7cb…` coincide con el declarado en la asignación: 103 conceptos, 232 respaldadas, 1308 fuera del núcleo, 23 candidatas, 836 revisadas, 118 candidatas, 6 ambiguas, 16 catálogos con recurso identificado.
- 163/163 huellas de fila recalculadas desde `data/portal/contenido-inspeccion.json` coinciden; mapeo definición-IRI→fila y nombre exactos; partición sin omitidos/duplicados ni solape con 6/8/9/10.
- Daño U+FFFD: 0 celdas en las 163 filas; literales y erratas originales conservados, sin normalizaciones.

## Totales reales

| Resultado | Cantidad |
| --- | ---: |
| Definiciones asignadas con lectura literal individual | 163 |
| Decisiones propuesta-significado | 75 |
| Decisiones pendiente | 88 (75 descripción pendiente/vacía, 10 identidad/etnia/lengua, 2 genérica, 1 contradicción código-texto) |
| Reglas propuestas (r3a7-) | 75 |
| Conceptos nuevos estrechos | 50 |
| Conceptos reutilizados exactos | 1 (sexo-difunto; EDAD del difunto usa concepto nuevo sin momento confirmado) |
| Correspondencias columna→variable | 0 (revisión posterior) |
| sameAs/exactMatch | 0 |
| Descargas de red | 0 (basta evidencia local) |

### Desglose excluyente (suma 163 exacto)

| Clase | Cantidad |
| --- | ---: |
| propuesta-significado | 75 |
| pendiente por descripción pendiente/vacía | 75 |
| pendiente por identidad/etnia/lengua | 10 |
| pendiente por descripción genérica | 2 |
| pendiente por contradicción código-texto | 1 |
| **Total** | **163** |

## Verificaciones (scripts/verificar.py → OK)

Positivos: las 75 reglas simulan `interpretacion()` en memoria (solo funciones puras centrales); robustez positiva: fila sin unidad sigue casando (la unidad es metadato, no clave). Negativos: solo-nombre, contexto-mutado, otra-IRI no casan; código-no-acreditado (0 catálogos, 0 sameAs/exactMatch).

## Archivos (solo carpeta asignada)

- `propuestas.json`, `fuente/inspeccion-extracto.json`, `scripts/construir.py`, `scripts/verificar.py`, `resultado.md`.

## Pendientes y límites

- 75 descripciones pendientes aunque el nombre sugiera contenido (APGAR, vacunas, CIECAUSABASICA, etc.).
- 10 identidad/etnia/lengua sin catálogo que defina valores; CLAVEEDAD/CLAVEEDADD genéricas.
- 1 contradicción código-texto (RESIDEEXTRANJEROD frente a RESIDEEXTRANJERO) pendiente con pregunta; no se unifican ni se deduce lugar.
- FECHANACIMIENTO/HORANACIMIENTO del nacido: sujeto del contexto del conjunto (límite en el concepto).
- Pesos/talla/edad-gestacional sin unidad; indicadores sí/no sin valores documentados.
