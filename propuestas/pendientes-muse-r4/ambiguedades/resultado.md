# Ronda 4 — Ambigüedades: resultado (cierre corregido)

Rol: resolver 6 columnas ambiguas (12 destinos) y 5 observaciones de `asignacion.json`.
Solo se escribe en `propuestas/pendientes-muse-r4/ambiguedades/`. Sin control de Obscura; sin cambios al núcleo.

## Decisiones por columna (6)

| Columna | Campo | Decisión | Destino / motivo |
| --- | --- | --- | --- |
| Fiebre 2023 `…/Hoja1/1` | ide_id | proponer* | → def `/1` por exclusión estructural de /177 y /178 (encabezado repetido como dato, campos desplazados); *condicionado a aprobación de r4-lote-1-001 |
| Fiebre 2022 `…/Hoja1/1` | ide_id | proponer* | idem; misma huella de esquema; *misma condición |
| Fiebre 2024 `…/Hoja1/1` | ide_id | proponer* | idem; *misma condición |
| Presas `…/cat_estatal/1` | Clave | pendiente | /1 (Histórico_presas) vs /4 (Catálogo_estatal); hoja física `cat_estatal` no iguala exactamente a ninguna (cat≠catálogo). No se fuerza |
| Plantas `…/Plantas…/9` | Unidad de Medida | proponer | → def `/9` unidad-capacidad (regla vigente r3a10-0286): pos 9/16 entre Capacidad (8) y Generación (10), mismo orden que el diccionario |
| Plantas `…/Plantas…/11` | Unidad de Medida | proponer | → def `/11` unidad-generación (regla vigente r3a10-0288): pos 11/16 entre Generación (10) y Energético (12) |

Las 12 correspondencias ambiguas previas quedan en evidencia histórica; para las 5 columnas
resueltas el generador elegirá el destino exacto de cada vínculo (columna física + `definicion_iri` +
huellas + descripción + criterio) y no mantendrá los otros destinos como ambiguos vigentes.
La columna Presas sigue sin resolver (pendiente). Detalle de fidelidad: la fila RAW /1 del
diccionario trae «Número de identificación » (espacio final) y su huella se conserva intacta;
el campo `descripcion` de los 3 vínculos fiebre usa el valor materializado exacto
(«Número de identificación», sin espacio), que es el que coteja el generador.

Dependencia literal: los 3 vínculos fiebre→/1 verifican solo si se aprueba
`propuestas/pendientes-muse-r4/lote-1/entrega.json` regla r4-lote-1-001
(concepto numero-identificacion-registro-rickettsia, lote-1 estado completo-segunda-revision);
sin esa aprobación quedan sin efecto. No se recurre a /177 ni /178 en ningún caso.

## Decisiones por observación (5, contra las 865 vigentes)

- **egresos-descripcion-urgencias**: pendiente vigente (sin vínculo para Total_Egresos). Pregunta: ¿la columna cuenta egresos o urgencias?
- **municipio-formato-ejemplo**: significado municipal resuelto (vínculo concepto municipio); pendiente solo composición del código nnn vs 26048. Pregunta: ¿CVE_MUN es municipal (3) o CVEGEO compuesta (5)?
- **fecha-ejemplo-numerico**: significado fecha-precipitacion resuelto; pendiente solo codificación DD/MM/AAAA vs 45658. Pregunta: ¿representación real de las fechas (serial Excel)?
- **anio-nacimientos-2024**: pendiente vigente (año sin vínculo en ese recurso). Pregunta: confirmar que el campo datastore `a–o` es año y equivale a la variable año del diccionario.
- **anio-divorcios-2023**: nota histórica conservada, NO pendiente: alias anio_registro→año_registro ya resuelto como documental_revisada. Sin petición nueva.

## Fe de erratas

La «discrepancia de huella /11» del informe anterior no existe: fue error de transcripción propio.
`data/semantica/cobertura.json` registra literalmente `d33c36c8…05dfe5d404…`, idéntico al valor
verificado desde la fila capturada. Retirado.

## Cuentas verificadas

- Columnas: 6 → proponer 5 (3 condicionados), pendiente 1, rechazar 0.
- Vínculos: 5, todos con `definicion_iri`. Reglas nuevas: 0. Conceptos nuevos: 0.
- Significados: 3 (/1 dependencia de lote-1; /177 y /178 artefactos pendientes de exclusión).
- Solicitudes: 7 (1 dependencia literal, 1 presas, 4 observaciones vigentes, 1 nota histórica).
