# Dictamen independiente — educación TIC (matrículas + TIC, 54 IDs)

Fecha UTC: 2026-10-24. Auditor independiente post-R6. Sin editar entregas ni fuentes; sin contactos externos; sin tests generales.

## Veredicto global: ACEPTAR (54/54)

0 promociones en ambos grupos: correcto y sostenible. No se fuerza ninguna promoción.

## Archivos revisados (SHA-256 exactos, refrescados al cierre)

| Archivo | SHA-256 | Bytes |
| --- | --- | --- |
| `propuestas/investigacion-post-r6/matriculas/entrega.json` | `e09df5f5e224067495fa354deca8cd2102950d49ce02b998423a44bf1a454e7e` | 91088 |
| `propuestas/investigacion-post-r6/matriculas/entrega.md` | `2eeeb85911bc1d3a706646095f9b5679b9a9b24560001d839899bcf2746f4e75` | 12719 |
| `propuestas/investigacion-post-r6/tic/entrega.json` | `afd6fb855255c089d53578e204572c18550aab0f34d20251d737774479b9087a` | 119908 |
| `propuestas/investigacion-post-r6/tic/entrega.md` | `9c61b2cae066c95e7a8efedd9a9c52d726438c19663d7f4ddd08c4c561bb0a10` | 91947 |

Versión TIC final congelada (autor confirma; `listo.json` coherente con estos SHAs). Cambios finales revisados: puntuación de citas históricas corregida, marcadas como heredadas, sin exclusividad; sin cambios materiales.

Matrículas `listo.json` existe (revisión final, no preliminar) y sus hashes coinciden con la entrega revisada. TIC `listo.json` coherente con la versión final congelada.

## Comprobaciones

- **Cobertura 30+24 exacta**: cada entrega cubre 1:1 los IDs de su `grupo_fuente` en `reports/pendientes-depurados.json` (variable, descripción original y huella coinciden; 0 duplicados; 0 faltantes/sobrantes).
- **Huellas/originales**: 30/30 y 24/24 huellas coinciden con inspecciones; SHAs de toda evidencia citada coinciden con bytes reales (12/12 matrículas, 29/29 TIC, 0 mismatches en evidencia por decisión).
- **Fuente primaria**: CKAN `datos.sonora.gob.mx` + `ues.sonora.gob.mx` / `www.sonora.gob.mx`; `.bin` crudos preservados; derivados rotulados como tales (no codebooks).
- **Novedad frente a R6**: real en ambos grupos (matriculas: package/datastore vivos + xlsx 58f2d5a6 + 5 normas UES + páginas/búsqueda; TIC: 8 package_show + 2 páginas + relectura 24/24 + barrido PDFs). R6 no contenía estas fuentes.
- **Localizadores/afirmaciones**: JSON-pointers verificados por muestreo; afirmaciones soportadas por bytes locales (instrumento CKAN, ediciones UES, ausencia de "no exigibilidad" salvo Mención Honorífica 2026).
- **Sin imposibilidad ni exclusividad sin prueba**: la frase histórica "Solo el publicador lo tiene" quedó marcada como cita R5/R6 heredada con conclusión acotada ("no se atribuye exclusividad"); negativas acotadas ("no es ausencia universal" / "no localizado en publicación primaria").
- **Enlaces públicos examinados**: normatividad/titulación + búsqueda (matriculas); programa especial/diagnóstico PowerBI (TIC), con localizador y fragmento, verificados en bytes locales.
- **Base intacta**: 12/12 SHAs de `base.json` coinciden.

## Por ID (detalle máquina en `dictamen.json`)

Todos: `sigue_pendiente`, `significado_propuesto: null`, veredicto **aceptar**, defectos "sin defectos; pendiente sostenible" (salvo nota en TIC P10/063058e6-10: cita histórica correctamente acotada), corrección mínima "ninguna".

Matrículas (30): filas 8, 11, 12, 13, 14, 17, 20, 25, 26, 27, 28, 29, 35, 47, 48, 49, 52, 53, 54, 58, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70 — aceptar.
TIC (24): 3851f1c3/8, /9, /13; bdbf043f/26, /28, /30, /32; f3ecd3d2/7; 8f8e3cfb/11; c65eb4e7/7; 063058e6/10, /11, /16, /18, /21; a4e8bee0/22, /36, /39, /40; af14d207/8, /13, /36, /39, /40 — aceptar.
