# Estado de coordinación (trabajo en curso)

Se está ejecutando `docs/plan-paralelo-ampliacion-post-r9.md` por instrucción
delegada del chat `01a16c87-06d0-7541-83bb-6023e23bb0c9` y autorización del usuario.
El usuario pidió después cambiar Muse por **DeepSeek V4.1 Flash Free** por cuota.
Se abortaron las nueve sesiones Muse y la prueba nativa confirmó exactamente
`opencode/deepseek-v4.1-flash-free`. Las continuaciones son sesiones NUEVAS.
No reanudar sesiones Muse: V2 conserva su modelo original.

## Límites

- Base IRI definitiva excluida: no cambiar `config.toml` ni decidir otra base.
- Gemma excluido; no contactos a publicadores ni búsquedas agotadas.
- No joins al grafo ni promoción de candidatas; R1–R9 manifiestos inmutables.
- Un solo integrador central (coordinador); todos los autores solo staging.
- Usuario pidió avisar al otro chat al terminar; autorización persistente para
  enviar resumen a `01a16c87-06d0-7541-83bb-6023e23bb0c9` después del cierre.

## Base

R9: 1423 significados, 1106 conceptos, 4506 revisadas, 17 candidatas, 0 ambiguas;
portal 322405, Studio 323014. Seguimiento operativo posterior: 213 pruebas OK.
138 significados/16 vigencias/des_mpo_res/2 headers/5 observaciones siguen abiertos.
`base.json` fija 130 archivos; ZIP previo verificado.
`iri-fuera-de-alcance.json` y `config-iri-base.toml` fijan adicionalmente config.

## Entregas

- T-top50/v001 (Muse, sellada): ranking reconciliado 50/1191/3916; vista MD/JSON/HTML.
- A2-registro-civil/v001 (Muse, sellada): `resultados.json/md`, ficha, script/tests.
  Resultado bloqueado (evento matrimonial vs agregado mensual, muestras, inconsistencias).
- A1-911/v002 (Free): continúa v001 incompleta; duplicado entre conjuntos y Q2 sin MUNICIPIO;
  ocho ejes y análisis separado, sin proporción no acreditada.
- A3-itama/v002 (Free): corrige v001 que afirmaba erróneamente cero XLSX en todo repo;
  debe limitar búsqueda a recursos ITAMA. Resultado bloqueado por documentación/datos.
- Q-unidades/v001 (Muse): seis candidatos y peticiones web, no instalable; continúa Free v002.
  Q-U01 Toneladas (PRODTON) podría no acreditar variante métrica: no forzar.
  Q-U02 Kilogramos, Q-U03 MW, Q-U04 GWh, Q-U05 Porcentaje, Q-U06 literal exacto
  `Grados celcius`. Los seis tienen estado respaldado en cobertura actual (comprobado).
  U03/U04 son variables llamadas Unidad de Medida: no transferir a otras columnas.
- W-estandares/v002 (Free): único navegador Obscura; seis páginas QUDT 3.5.3 ya capturadas
  en normativa/. Debe terminar sello/respuestas. HectoM3/hm³ agotado, no repetir ni usar M3.
- S-shacl/v001 (Free): autoría pendiente de formas y fixtures. Muse no entregó;
  su prototipo raíz `proto_q.py` se archivó en `S-shacl/antecedentes-muse/` (sin tocar código central).
- R-documental/v001 y B-tecnica/v001 (Free): revisan T/A2 ahora; necesitan continuar
  con A1/A3/Q/W/S finales y después payload exacto.
- I-codigo/v001 (Free): prepara scripts/integra_ronda_10, hooks y tests SOLO staging;
  contrato/material todavía pendiente. No aceptar código solo con tests sintéticos:
  ejecutar contra material real. No dictámenes falsos, solo mocks en TEMP.

## Pasos restantes

1. Terminar/verificar sellos de autores, corregir defectos en versiones nuevas.
2. Q final tras W; preparar payload de unidades realmente aceptables y SHACL precisas.
3. Dos auditorías independientes de los bytes exactos; revisar también código con material real.
4. Publicar top50 y tres análisis separados; integrar únicamente deltas aceptados con evidencia
   nueva R10 si corresponde. No tocar manifiestos antiguos ni config IRI.
5. Suite completa, RDF/SHACL, consultas, respaldo y sincronización Studio si hay delta RDF.
6. Informes y archivos modificados, dejar bloqueos externos explícitos; avisar al chat origen.

Usar `.venv/Scripts/python.exe`, PowerShell `login:false`. No CLI OpenCode ni puentes.
No ejecutar suite simultáneamente con publicación de TTL (bloqueos Windows previos).

## Actualización de revisión

R-documental/v001 rechaza por trazabilidad (cifras/bloqueos reproducidos):
T/v001 cita hash del plan anterior al cambio de modelo; A2/v001 no distingue
recursos de datos de diccionario en MD y no fija SHA de cuatro fuentes completas.
Se lanzaron sesiones Free nuevas para T/v002 y A2/v002 (no modificar v001):

- T: `ses_e906c0fabffemxT7gjALUYJNix`, job `job_bd14619788c148b0a2d150691124964d`.
  Además refactoriza script a generar(root,outdir) publicable con salida reports/,
  sin rutas staging hardcoded; MD/JSON/HTML top50 idéntico con fuentes actuales.
- A2: `ses_e906c0ea4ffeeurbkwoDRsFvFX`, job `job_ddeac924be034f7a86fc12c0376cd970`.
- W/v002 ya sellada: seis sujetos oficiales verificados en QUDT 3.5.3. La norma
  TON_Metric NO acredita que el literal local Toneladas elija variante métrica.
- R-documental recibió seguimiento para aclarar T-07 falso sin hallazgo y revisar
  las versiones nuevas cuando estén selladas. No instalar aún nada.

## Continuidad Free y pruebas de base

- Todos los carriles activos usan proveedor `opencode`, modelo `deepseek-v4.1-flash-free`; regla vigente registrada también en AGENTS.md.
- Suite base R9: 213 pruebas, 58.295 s, OK (`suite-base-r9.log`).
- S-shacl/v001 sellada: usar shapes.ttl SHA 0f342433c003d20cdda74fd8190cb746c8f7c665875b0584e5b5759dcf205566. NO usar propuesta/shapes-adicionales.ttl (antecedente distinto). Motor real: negativos15, positivos0, portal/Studio conformes,0ignoradas.
- R/v003 revisa T/A1/A2/A3/W; B/v002 revisa T/A3/W y recibió seguimiento para A1/A2/S en nueva versión.
- Q/v003 debe consumir W/v002 sellada:5vínculos U02..06; Toneladas excluida por variante local no acreditada.
- I-codigo/v001 empezó a escribir copias de hooks; pendiente integrador/contrato/tests reales.
- No se instaló ni sincronizó nada de esta ampliación todavía.


## INTERRUPCIÓN POR CUOTA FREE — estado vigente

El proveedor devolvió HTTP429 provider.quota / FreeUsageLimitError. Se interrumpieron las sesiones Free pendientes y no se reintenta automáticamente. No cambiar a modelo de pago sin instrucción.

Base: 130 archivos comprobados; cambiados: []. config.toml intacto. R10 NO instalada ni sincronizada. Payload16archivos intactos, aceptadasSHA df5705eaf6e0b8d8dcb0257a54a258264cda3e8adfe8655f87dfda90b9c2031c.

I-codigo/v001 se sustituyó por K-codigo/v001: copia corregida de 3 scripts, sello.json; PROV permitido y IDs NodeShape exactos. K pendiente auditoría; NO instalar aún. IntegradorSHA05e834fd28499f413a93e1210fbf7fdf65d1687a5fcd24298d80b4091b23811b.

Q-unidades/v003 entregó5vínculos con W/v002; verificar sello antes de usar. A-payload/v001 y B-payload/v001 dejaron scripts parciales sin dictamen. C-codigo y V-pruebas fallaron por cuota, sin entrega. R/B originales tienen seguimientos incompletos. No confundir sus salidas con aprobaciones finales.

Detalles y siguientes pasos: interrupcion-cuota-free.json. No se avisó al otro chat como terminado.


## Reanudación Muse autorizada (vigente)

Usuario indicó continuar con Muse1.3. Nuevas4sesiones en reanudacion-muse/agentes.json; sin reanudar Free. Base130 ypayload16 intactos al retomar. A/B aceptaron11casos yKcode exacto; V18tests unittest pasan sin skips conauditsreales; Bv002aceptótests. Preflight90triples/73formas. R10INSTALADA:manifiesto f28c5915e043b5081c44b824b9a9bd92f51e97218c2e42aeac98aed2b6aaa890. Regeneración con--load en curso, SIN sincronizaciónStudio todavía.

D aceptótop50 y3fichasbloqueadas, ademáspublicacióncurada. CLI originaltop50fallóalpublicarporprohibirreports; correcciónenK-publicador/v001,2testsrealesCLIinstalado pasan,sinmutarfuentes. Dv003revisando antesdecopiarcentrales. TestR10ya instalado.


## CIERRE R10 COMPLETO

reports/ronda-10.md/json yREADME/PLANactualizados.233testsOK,portal322495 yStudio323104SHACLconformes0violaciones.90agregados/0retirados,deltaexacto;7declaracionesunidad(5nuevas),6formasnuevas.41historicosconfigscerradosintactos,semantica/IRIintactas. SinGemma ni contactos. Top50y3analisisbloqueadospublicados.

ITAMAv003consolidado:Dv004aceptado. PublicadorK-publicadorv001corregido conCLIinstaladorealTEMP,2testsensus233,Dv003aceptado/adendafechaDv004. S-wrapperadendatrazabilidad.

Chat origen notificado tras cierre (notificacion-origen.json) para revisar ydevolverplanR10.No confundir pendientes externos con trabajo local inconcluso.


Chat origen completó revisión:71hashescoinciden+3checksmanifiesto/config/core;devuelve docs/plan-actualizado-tras-r10.md/json. Sin tareas semánticas locales justificadas con evidencia actual: siguiente ronda solo con fuente o pregunta concreta. Coordinador actualizó modelo devuelto(obsoletoFree) aMuse1.3porinstruccióndirectadelusuario y mantuvoGemmaexcluido. Registro plan-devuelto.json.
