# A-documental — dictamen lote-1 (2026-10-24)

Alcance: 128 casos en 7 versiones congeladas fijadas en `lote-1.json`.
Lote-2 (S2, S6, V4; 60 casos) pendiente: sin dictamen sobre ellos y sin
dictamen global del lote completo, que se emitirá con `seleccion.json`.

## Dictámenes por versión

| Rol | Versión | Casos | Dictamen |
|-----|---------|-------|----------|
| S1-defunciones | v002 | 32 | aceptar |
| S3-matriculas | v001 | 30 | aceptar |
| S4-epidemiologia | v001 | 25 | aceptar |
| S5-tic | v001 | 24 | aceptar |
| V1-uth-presas | v001 | 5 | aceptar |
| V2-salud-anomalias | v001 | 6 | aceptar |
| V3-coespo | v001 | 6 | **requiere_correccion** |

- **S1 v002 — aceptar.** Reevaluación concreta por ID: alias sistemático
  (ningún identificador local coincide exactamente con un mnemónico nacional)
  y recodificación demostrada con valores fuera del dominio nacional
  (`'4'` en ocupación; `'88'` en ent_ocurr; `'997'`/`'9997'` en mun/loc).
  Coherencias de valor registradas sin inferir adopción. Ningún caso con
  campo/edición/ámbito formalmente inequívoco. 0 promociones.
- **S3, S4, S5, V1, V2 — aceptar.** Brechas externas justificadas por ID,
  0 promociones, sin inferencias por igualdad ni por nombre parecido.
- **V3 v001 — requiere_correccion (formal, no de fondo).** Las conclusiones
  F3+F4 ausentes están verificadas; el defecto está en puerta/novedades:
  (1) `pista_nueva` se sostiene en "interior nunca examinado en R5/R6/post-R6"
  y "examinados por primera vez" sin citar los inventarios que lo prueben
  (los recursos Diccionario 03a33e71/1b6d0817/f1bbd13b ya eran conocidos
  como variables estructurales); (2) el `package_show` re-verificado sin
  cambio se etiqueta "evidencia nueva" en vez de re-verificación.
  Corrección mínima en v002 nueva (no editar la congelada): demostrar con
  inventarios o acotar la formulación, y etiquetar el API como
  re-verificación. Estado brecha_externa y reapertura se conservan.

## Propuestas aceptadas

Ninguna: las 7 versiones traen 0 propuestas (128/128 brecha_externa).
`propuestas_aceptadas: []`. No se fuerza ninguna promoción.

## Referencias

22 rutas con SHA-256 calculado de bytes (ver `lote-1.json`): `lote-1.json`
+ entrega.json/entrega.md/congelada.json de cada versión. Los SHA de
entrega y congelada coinciden con los fijados en `lote-1.json`.
