# Resultado tic — ronda 5

Significados asignados: 31. proponer: 7. pendiente: 24. artefacto_documental: 0.
Reglas nuevas: 7 (r5-tic-001 a r5-tic-007). Conceptos nuevos: 2 (condiciones-innovacion-tic-declaradas, recursos-anuales-innovacion-declarados). Concepto vigente reutilizado: 1 (sector-dependencia-diagnostico).
Vinculos/decisiones de columnas: 0 (asignación sin correspondencias actuales; no se tocan columnas).
Solicitudes a catalogos-web: 7 (tic-web-01 a tic-web-07).

## Qué se resolvió y por qué

- Los 5 "Sector" (P2 en Política Digital, Información General, Planeación TIC, Presupuesto TIC y Mejora Regulatoria) se proponen con el concepto vigente sector-dependencia-diagnostico. La fila es byte-identica (huella 7e479222…) a la aceptada por auditoría-a (r4-lote-3-sector-dependencia-encuestada-8) con los mismos límites: texto declarado tal cual, sin separar código/nombre, sin catálogo, sin comparar entre encuestas. Esto revierte el pendiente r4 con evidencia nueva.
- P7 de Política Digital ("Enliste las condiciones…", descripción completa, Tipo Texto) se propone como lista textual declarada, sin catálogo ni conteo; precede el análogo r4-lote-5-006 (P9 prototipos).
- P13 de Política Digital ("Enliste los recursos anuales…", ejemplo "5000, software") se propone como consignación textual con límite explícito de unidad/moneda no declaradas; no cuantifica ni compara. Revierte el pendiente r4 con un concepto que renuncia a lo que el pendiente exigía inventar.

## Qué queda pendiente y por qué

- 5 descripciones truncadas en la celda fuente (P10/P16/P18/P21 Política Digital, P22 Desarrollo): verificadas contra la inspección local; el portal tiene descripciones de hasta 395 caracteres, así que no hay tope de captura. Re-descarga 2026-10-23 bloqueada por WAF (búsqueda negativa documentada).
- 8 anaforas sin referente declarado en la propia fila (P11 Política Digital→P10 truncada; P27/P29/P31/P33 Infraestructura→filtros no vinculados, P33 con marca "4" sin nota; P7 Gobernanza y P7 Fortalezas→P6; P11/P15 Información General→sujeto/referente): vecinas releídas, pero el diccionario no declara el vínculo; no se transfiere por proximidad (precedentes lote-4/lote-6 confirmados).
- 10 contradicciones tipo-vs-descripción/ejemplo conservadas como tales (P11 Presupuesto; P36/P39/P40 Desarrollo y Mejora; P8 doble y P13 Mejora): no se inventa significado alternativo.
- 1 tautología (P10 Información General: "Actividades principales:"/"Actividades Principales").

## Verificación

- Las 31 definiciones de asignacion.json tienen decisión individual; huellas y conjunto/diccionario de cada regla coinciden con la asignación.
- Fuentes con SHA-256 en entrega.json (9 inspecciones, cobertura, auditoría-a). Sin fuentes externas respaldando significados: la auditoría-a se usa solo como condición de aceptación, sin reemplazar la fuente.
- Búsqueda negativa y bloqueo registrado: el 2026-10-23 la descarga directa del diccionario (curl.exe, 56208 bytes) y del datastore devolvieron página HTML de firewall (magic `<!DOCTYPE html>`, título "Web Application Firewall"), no un xlsx; ambos archivos se eliminaron y no se citan como evidencia. Verificación de cabeceras sin descargar cuerpo el mismo día: `HTTP/1.1 403 Forbidden`, `Content-Type: text/html`, `Server: cloudflare`. Ninguna página HTML se convirtió en evidencia del diccionario: las 7 solicitudes concretas a catalogos-web están en solicitudes_web.json.
- Autenticidad de copias locales: la carpeta tic/ contiene solo asignacion.json, entrega.json, listo.json, resultado.md y solicitudes_web.json (magia JSON/`#` verificada, sin xlsx ni html). Las 9 inspecciones, cobertura.json, auditoría-a y semantica.json son JSON válido sin rastro HTML y los 9 hashes citados en entrega.json coinciden con los archivos; se usan las capturas originales fijadas, sin reemplazo por fuente nueva.
- No se tocó Obscura, chat, Studio, núcleos ni otras carpetas. Modelo: agentes Muse 1.3; preferencia Gemma del chat Studio intacta.
