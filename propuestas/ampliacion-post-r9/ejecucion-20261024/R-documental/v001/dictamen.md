# R — Dictamen semantico/documental (v001)

Fecha UTC: 2026-10-24T20:22:02+00:00. Objeto: T-top50/v001 y A2-registro-civil/v001.
Lectura directa de fuentes locales; sin red, sin grafo, sin Studio. Ningun join ni rate aprobado por el ranking.

## Veredicto

**FAVORABLE CON OBSERVACIONES**

| Entrega | Veredicto | Checks | Sellos | Hallazgos |
| --- | --- | --- | --- | --- |
| T-top50/v001 | FAVORABLE CON OBSERVACIONES | 16/16 | verificados (7/7 archivos, bytes y SHA256) | H-01 |
| A2-registro-civil/v001 | FAVORABLE CON OBSERVACIONES | 15/15 | verificados (5/5 archivos y sidecar) | H-02, H-03, H-04 |
| A1-911 / A3-itama / Q-unidades / S | NO EVALUADO | 0/0 | no aplica | — |

## T — Top 50

Recomputo propio (sin importar el codigo de T): 3916 pares; 2328 sin clave, 1191 candidatas, 396 solo dimensiones, 1 exploratorio. 1191/1191 ids unicos y scores iguales a la matriz; 50/50 rangos, ids, scores y orden (score desc, id asc) iguales al CSV.
Top1 ITAMA: pesos 13.0 + penalizaciones -8.0 = 5.0. A1/A2/A3 en rangos 2/4/1 por ID exacto. 50 filas del staging fieles al mapa y todas en `NO_JOIN_APROBADO`. Cobertura R9 declarada (1423/1106/138/16/17) coincide con el reporte.

## A2 — Registro civil

`resultados.json` se reproduce integramente desde las fuentes con la logica declarada: BLOQUEADO, sin comparacion de volumenes ni join. Los 8 ejes se sostienen:

- Claves: par `candidata_por_validar`; `municipio` coincide solo como nombre de campo, sin catalogo/unicidad acreditados (pendientes del mapa).
- Grano: Matrimonios fila-evento (dia, edad/sexo de contrayentes) vs Nacimientos agregado municipio-anio-mes (hombres/mujeres/total).
- Unicidad/cobertura: muestras n=100 declaran no demostrar unicidad ni cobertura; no equivalen al universo.
- Cardinalidad: 6 pruebas; 5 con total != hombres+mujeres (2015, 2020-2023) y 1 con meses faltantes (2016); decision `fallo_validacion_integral`.
- Poblacion: actos con dos contrayentes vs conteos de nacidos; sin id de persona.
- Periodo/ambito: solape 2015-2024 solo por nombres; municipio/anio/mes de registro, sin residencia ni correspondencia de codigos acreditada.
- Unidades: fila-evento vs fila-agregado; pendiente de unidades; sin tasas.

## Hallazgos

| ID | Entrega | Severidad | Hallazgo | Accion |
| --- | --- | --- | --- | --- |
| H-01 | T-top50/v001 | menor | Huella declarada del plan no corresponde al archivo actual | Al congelar el plan, re-declarar su huella en T v002 (o registrar la version usada). |
| H-02 | A2-registro-civil/v001 | menor | Conteo de recursos distinto entre resultados.md y resultados.json | Precisar en v002: '10 recursos de datos + 1 diccionario' y '15 + 1'. |
| H-03 | A2-registro-civil/v001 | menor | La frase 'sin catalogo de correspondencia' es mas amplia que la evidencia | Reformular: 'sin correspondencia acreditada para estos recursos'. |
| H-04 | A2-registro-civil/v001 | menor | Fuentes locales sin huella SHA256 de archivo completo | Anadir huellas completas de las cuatro fuentes en A2 v002. |

Ningun hallazgo es bloqueante ni altera cifras o veredictos; los cuatro son de trazabilidad o redaccion y se corrigen en v002 sin reescribir lo sellado.

## Checks y limites

32/32 comprobaciones OK. La unica desviacion de un criterio es la huella del plan en T (H-01), explicada por edicion posterior al sellado. El detalle maquina, con hashes exactos calculados por codigo, esta en `dictamen.json`; el sello en `sello.json` (+ `sello.sha256`).

No se evaluan A1-911, A3-itama, Q-unidades ni S (en elaboracion): no se aprueba trabajo futuro. Base IRI/example.org intacta y fuera de alcance. Snapshots antes/despues prueban que no se modifico ningun byte sellado.
