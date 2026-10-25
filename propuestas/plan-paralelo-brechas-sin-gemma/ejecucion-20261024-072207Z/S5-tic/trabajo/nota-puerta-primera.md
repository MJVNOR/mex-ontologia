# S5-tic — nota de primera puerta (2026-10-24)

## Método (sin repetir búsquedas agotadas)

1. Lectura íntegra de `asignacion.json` (24 casos) + antecedentes por ID.
2. Lectura íntegra de `propuestas/cierre-brechas-post-r6/significados-tic-diversos/evidencia/nueva-tic-sonora-2026-10-24.md`
   (búsqueda nueva del día: página `sonora.gob.mx/datos/diagnostico-entorno-digital`, fetch nav-only negativo).
3. Lectura íntegra de `propuestas/cierre-brechas-post-r6/web-obscura/obs-diagnostico-2026-10-24.json`
   (Obscura con DOM renderizado, 2026-10-24T06:51:28Z, sobre la misma URL: cascarón JS confirmado,
   1 iframe PowerBI, sin cuestionario/codebook/tabla extraíble).
4. Verificación SHA-256 de los 19 archivos de evidencia previa: todos OK (bytes idénticos).
5. Barrido local de archivos `*cuestionario* *diagnostico* *codebook* *diccionario*`: sin instrumento
   inédito del Diagnóstico del Entorno Digital (solo material ya examinado o de otros temas).
6. Cabecera del `.bin` preservado del Diagnóstico: HTML cascarón JS, material ya examinado.

## Resultado de puerta

- 24/24 IDs: `sin_pista_nueva` → `brecha_externa`. Cero `pista_nueva`, cero `cambio_de_fuente_por_comprobar`.
- La única URL candidata del día ya fue examinada por dos métodos independientes el mismo día.
- No se emitió `peticiones-web.json`: Obscura ya cubrió la página interactiva hoy 06:51Z y reinspeccionar
  la misma página sin pista está prohibido. Paquete W-web ausente al cierre local; si W aporta el
  instrumento, el coordinador hará adenda (v002 solo si se pide).

## Límites

- Búsquedas negativas acotadas a lo revisado; no es ausencia universal.
- Nada del PowerBI se afirma (requiere interacción).
- No se propone ningún significado: derivarlo del nombre violaría el criterio.
