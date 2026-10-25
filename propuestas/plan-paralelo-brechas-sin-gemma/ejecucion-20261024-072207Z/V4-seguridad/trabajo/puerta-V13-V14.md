# Primera puerta V4-seguridad (V13, V14) — 2026-10-24

## Verificaciones realizadas (herramientas independientes; navegador Obscura no tocado)

1. Antecedentes leídos: asignación V4, `propuestas/cierre-brechas-post-r6/vigencias-seguridad/entrega.json`,
   `resultado.md`, `peticiones-web.json`; base/roles del plan.
2. SHAs de evidencia previa recalculados de los bytes (coinciden con lo citado):
   V13/V14 diccionarios, catálogos y api_*.json del 2026-10-24.
3. `W-web/paquete/` no existe en esta ejecución (glob vacío): sin resultados web pendientes de contrastar.
4. Re-verificación CKAN en vivo hoy 2026-10-24 vía webfetch (no Obscura):
   - 93ca5e1c: `version=null`, Catálogo 36d3ac85 size 10194, Diccionario 5f46e4b8 size 11436,
     ambos con start/end 1989-06-04 y publisher `-`; CSV 2015–2025 con rangos anuales reales.
   - caf587a5: `version=null`, Catálogo 7f3aca28 size 10999, Diccionario a8a09044 size 11540,
     mismos placeholders; CSV anuales fechados.
   Sin cambios frente a la evidencia api_*.json del 2026-10-24. No es pista nueva:
   es confirmación de ausencia de cambio (cambio_de_fuente comprobado, resultado negativo).
5. Descarga directa con curl de `package_show` devuelve página challenge anti-bots
   (HTML, no JSON): sin copia guardable; no se insiste (antecedente ya lo registró).
   Archivos inválidos eliminados, no se citan.

## Clasificación por ID

- V13 (cat_municipio, sha 84bb6fcd, recurso 36d3ac85): ninguna URL/documento/anexo
  no examinado aporta edición/versión/fecha/corte del catálogo ni vínculo con 2015–2025.
  Diccionario interior ya examinado: solo referencia nominal `catalogo_municipios`
  (ni siquiera coincide con el nombre de hoja `cat_municipio`). → **sin_pista_nueva**.
- V14 (cat_entidad, sha 96776ca8, recurso 7f3aca28): idem; diccionario interior solo
  referencia nominal `catalogo_entidades` (hoja `cat_entidad`). → **sin_pista_nueva**.

Página SESNSP datos-abiertos: ya observada en la pasada anterior (contexto general
de procedencia, bloques 2015–2025, sin vínculo con los recursos locales 36d3ac85/7f3aca28).
Re-observarla no es novedad. No se emiten peticiones-web (nada que pedir a W-web).

## Consecuencia

Ambos IDs → `brecha_externa` con documento exacto faltante y condición de reapertura.
Ninguna propuesta acreditada. Trabajo local cerrado; si W-web aportara evidencia
resolutiva, el coordinador hará adenda.
