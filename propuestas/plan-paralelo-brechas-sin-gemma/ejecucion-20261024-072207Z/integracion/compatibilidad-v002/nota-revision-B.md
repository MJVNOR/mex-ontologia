# Compatibilidad R7 — v002 (staging, no instalado)

Delta unico respecto a v001 (congelada intacta):

- Tupla de lote corregida `(31, 3, 31)` en ambos archivos
  (v001 comparaba `(31, 31, 3)` y siempre fallaba).
- `integrar_entregas.py`: bloque reducido; la cadena historica
  (`cargar`, pines de manifiesto) corre antes de los deltas y la
  fidelidad exacta por regla queda en `integrar_ronda_7.construir`
  (fase R7, gate dual A+B), sin duplicarla aqui.

SHAs en `congelada.json`.
