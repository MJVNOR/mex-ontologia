# P2 — Piloto OWL-Time (v001): propuesta negativa

**Estado:** `sin_evidencia_para_integrar` · 4/4 familias inventariadas · 0 intervalos.

## Inventario (limites documentados)

| Familia | Fuente | Por que no es intervalo |
| --- | --- | --- |
| Cuatrimestre UTH | CUATRIMESTRE (huella `8cf8b7c5`), ej. Enero - Abril | Bandas mensuales en texto, sin dia/anio en la variable ni calendario/precision |
| Matriculas 2022-2 | Hoja Estudiantes 2022-2, 15212 filas | Titulo/anio no define bordes; calendario 2022-2 no localizado (MAT-W-03) |
| Agricultura CICLO | CICLO (huella `91012fac`) | Descripcion generica, sin valores ni fechas |
| Trigo ANO/CICLO | ANO `0eb68281` / CICLO `257b589d` | Etiqueta 2022-2023 en titulo de recurso, sin inicio/fin |

Cobertura CKAN manual (`version=null`, start/end) no es vigencia ni intervalo lectivo.

## Diseno (sin instanciar)

- `v001/piloto-owl-time.ttl` — plantilla `time:ProperInterval` + `hasBeginning/hasEnd`; 0 intervalos.
- `consultas/intervalos-periodos.rq` — espera 0 filas (`fixtures/resultado-esperado.json`).

Web: `peticiones-web.json` con 1 peticion a W (especificacion W3C OWL Time).
Hashes: `congelada.json` (SHA-256 por codigo).
