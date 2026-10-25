# W-estándares v003 — corrección de metadatos (evidencia inmutable en v002)

Estado: **propuesta_para_auditar**. 0 casos, 0 promovidos. Sin navegación nueva
(no era necesaria: todo lo verificable ya está sellado en v002).

## Qué corrige

`v002/entrega.json` citaba para `P2-owl-time/peticiones-web.json` un hash truncado
de 41 caracteres (no SHA-256). Revisión completa por código de los 11 hashes citados
en v002: solo ese difería del archivo. v003 lo corrige con el valor real de 64
verificado por código (detalle en `verificacion-hashes.json`, generado por código).

## Evidencia

Inmutable en v002, preservada sin edición: P1-W-01/03 verificados
(MilliM, HA), P1-W-02 negativo (HectoM3/HectoHA inexistentes), P2-WEB-01 atendida
(ontología oficial w3c/sdw-time), trazas con Ray IDs. v003 no duplica evidencias.

## Aclaración M3 (alcance)

`http://qudt.org/vocab/unit/M3` acredita solo esa IRI. **No** autoriza sustituir
hm³ por M3 en ningún caso local ni aplicar factor de conversión alguno sin evidencia
local que declare unidad, escala y valores para esa variable/recurso.
P1-Q2 sigue pendiente de evidencia local.

## Sello

`congelada.json` cubre todos los archivos de `W-estandares/` excepto a sí mismo;
hashes calculados por código. Correcciones futuras en v004.
