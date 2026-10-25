# Entrega — investigación post-R6, grupo `diversos` (5 IDs)

Fecha (UTC): 2026-10-24 (ronda 2 + decisión integrador el mismo día). Solo se
escribió en `propuestas/investigacion-post-r6/diversos/`.

## Decisiones (0 propuestas; 5 siguen pendientes)

| IRI (fila) | Variable | Estado | Fundamento / hueco |
|---|---|---|---|
| `…/67156807…%2F5` | CLASIF | sigue_pendiente | Decisión integrador tras 2 auditorías: NO promover. "Tipo de asentamiento" sin fuente explícita; la lectura mínima acredita procedencia pero no el objeto clasificado. Propuesta original conservada en `historial_propuesta_rechazada` (entrega.json). Avance documental intacto: subset Sonora 2129x28 idéntico, 38 valores OBSERVADOS sin catálogo, conteo nacional 74226 válidas + 1 fila vacía. Límites C1-C4 (objeto, observado-sin-catálogo, no-joins, vínculo a nivel conjunto). |
| `…/f89137ba…%2F15` | Total_Egresos | sigue_pendiente | Contradicción sin árbitro + tabla DGIS irrecuperable por las vías accesibles (NEG-DIV-05). Falta aclaración o fe de erratas. |
| `…/3f6942e3…%2F2` | TRIMESTRE | sigue_pendiente | "Estrato" sin definir. Falta metodología PROAES. |
| `…/863b9cc8…%2F7` | CVOTRAS | sigue_pendiente | Objeto de "otras" indeterminado. Falta diccionario/metodología SAGARHPA. |
| `…/863b9cc8…%2F8` | DOTRAS | sigue_pendiente | Gemela de CVOTRAS; mismo hueco. |

## Notas

- Ronda 2: base nacional IMC_2020 y shp examinados (nivel colonia, sin
  equiparar localidad/AGEB); pista DGIS agotada (NEG-DIV-05); RAR sin
  extractor (NEG-DIV-06); lenguaje de no-exclusividad aplicado a las 4
  pendientes (defecto auditor-otros).
- `staging/clasif.json` = **RECHAZADA/NO_INTEGRAR** (traza histórica, no
  aprobable). Sin insumos de staging para el núcleo.
- Cierre RAR/nota: `tar.exe` listó 1 entrada segura y extrajo el script en
  `evidencia/calculo-extraido/` (arrastra CLASIF sin definirla; remite a la
  nota técnica). Nota IMUC 2020 (18 pp.): 1 mención a "clasificación de la
  colonia" como atributo de capa (nota 10, p4); 0 a `CLASIF` y 0 a "tipo de
  asentamiento" — sin definición explícita, NO promover queda firme
  (NEG-DIV-06 superada, NEG-DIV-07).

Ver `entrega.json` (fuentes con URL/fecha/SHA/localizador; decisiones con
evidencia, vínculo local, evidencia faltante, motivo y límites) y `listo.json`
(hashes).
