# Compatibilidad R7 — nota para revisión B (staging, no instalado)

Fallo: `consolidar_semantica` → `integrar_entregas.py:312` (`Resultado
inesperado conceptos 1106`) y el mismo patrón en `integrar_ronda_2.py:306`.
Causa: ambos comparan el reporte ya regenerado (con R7 materializado) contra
esperados históricos solo-R6. Históricos intactos; faltaba la rama R7.

## Parche (solo inserciones tras el bloque R6 existente)

- `integrar_entregas.py` (+49): con `revision-ronda-7.json` exige base R6,
  carga la cadena R7 (`cargar`: manifiesto + SHAs + aceptadas + auditorías),
  registra sus fuentes, exige lote exacto 31/31/3 y deriva:
  conceptos 1075+31=1106, respaldadas 1392+31=1423, candidatas 19,
  revisadas 4475+3=4478, fuera+candidatas=140 con conservación del examinado
  (1423+121+19=1563), y materialización fiel regla por regla. Toda ausencia
  falla; ningún observado se usa como esperado.
- `integrar_ronda_2.py` (+19): revisadas 4475+3=4478, candidatas 20−3=17,
  mismo lote exacto y fuentes registradas.
- Anclas históricas (`esperado`, `esperado_actual`, bloques R6) sin tocar.
  `depurar_pendientes.py` hardcodea conteos R6 pero NO está en la cadena de
  regeneración (vista standalone): no bloquea, no se toca.
- Sin manifiestos editados, sin tests, sin NLP.

## SHAs (staging)

- `integrar_entregas.py`: ver `congelada.json`
- `integrar_ronda_2.py`: ver `congelada.json`
