# Ronda 10 — cierre de ampliación posterior a R9

Fecha del cliente: **2026-10-24, America/Hermosillo**. Ejecución retomada con Muse 1.3 por el MCP nativo de OpenCode.

R10 incorpora **cinco declaraciones de unidad cualificadas** y **seis formas SHACL**. Conserva **1423 significados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas**. **233 pruebas pasan**; RDF y SHACL conformes. Portal: **322495 triples**. Studio: **323104**, con respaldo, 90 inserciones y cero retiradas.

## Integrado

| Variable en su definición local | Literal conservado | Término QUDT 3.5.3 |
| --- | --- | --- |
| pesoprom | Kilogramos | `http://qudt.org/vocab/unit/KiloGM` |
| Unidad de Medida | MW | `http://qudt.org/vocab/unit/MegaW` |
| Unidad de Medida | GWh | `http://qudt.org/vocab/unit/GigaW-HR` |
| ANALF | Porcentaje | `http://qudt.org/vocab/unit/PERCENT` |
| temperatura | Grados celcius | `http://qudt.org/vocab/unit/DEG_C` |

MW y GWh califican exclusivamente sus filas «Unidad de Medida». No se transfieren a otras columnas ni a valores observados; no hay factores ni conversiones. Hay siete declaraciones de unidad en total, incluidas las dos de R9.

Las seis formas controlan coherencia de estados/significados, correspondencias revisadas y el contrato de UnidadDeclarada. Admiten propiedades adicionales válidas; no hay `sh:closed` global.

## Análisis publicados

- [Top 50 legible](top50-oportunidades-r9.html): 50 filas reconciliadas sobre 1191 candidatas y 3916 pares; todas `NO_JOIN_APROBADO`.
- [Tres fichas, ocho comprobaciones por par](analisis-pares-post-r9.md): 911, Registro Civil e ITAMA. No se calcularon proporciones, comparaciones de volúmenes ni distribuciones.
- 911: Q1 mal etiquetado/duplicado y Q2 improcedentes sin MUNICIPIO.
- Registro Civil: agregación pendiente de validar, totales incompatibles y meses ausentes.
- ITAMA: faltan archivos completos y respaldo de periodo/escolaridad; expediente consolidado y sellado en [v003](../propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v003/entrega.md).

## Comprobaciones y respaldo

- Dos auditorías independientes aceptaron los once casos y los bytes exactos; integrador y pruebas revisados.
- 233 pruebas Python, cero omitidas; 30 consultas del portal ejecutadas.
- RDF: 322405 → 322495; delta exacto del integrador: +90/−0. SHACL conforme en portal y Studio, cero infracciones.
- Una forma histórica carece de instancias: ResultadoMunicipalLote; se registra sin fingir una comprobación con instancias.
- Studio: 323014 → 323104; sincronización única con respaldo y conservación de datos ajenos.
- [Respaldo de Studio](../data/backups/studio-antes-portal-20261025T024314810289Z.ttl); archivo base de 130 entradas en el expediente.
- 41 archivos históricos/configuraciones contrastados por SHA; semántica e IRI intactas.
- Recibos, dictámenes, huellas y detalle de las adendas en [ronda-10.json](ronda-10.json).

## Brechas externas conservadas

138 significados reales, 16 vigencias, 17 correspondencias candidatas, `des_mpo_res` y dos encabezados corruptos. V13/V14 mantienen el problema de acceso. Toneladas requiere acreditar la variante local; hm³ sigue sin un término exacto verificado. No se inventan definiciones, vigencias, equivalencias ni unidades. Gemma y la decisión de IRI quedaron fuera de alcance; no se contactó a publicadores.
