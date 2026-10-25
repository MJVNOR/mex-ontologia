# Investigación piloto con Obscura (solo lectura web)

MCP Obscura disponible y usado (pestaña exclusiva, cerrada al final).
3 temas en 14 llamadas; 0 promociones de significado.

## Resultado

Las 3 documentaciones oficiales consultadas existen, pero **ninguna
confirma la variable local** (`vigencia_acreditada:false` en las 3: página
sin edición fechada solo acredita documentación consultada).

1. **CLUES (DGIS):** documentado CAT_CLUES (NOM-024-SSA3-2012). NO resuelve
   `JURISDICCION_CLUES` (+`...D`) / `CLUESCERTIFICA` (descripción pendiente
   en fuente). Referencia candidata para agente-2.
2. **Municipios (DGIS, origen INEGI):** documentado CAT_MUNICIPIOS. NO
   confirma `des_mpo_res` (r3a6-036); referencia candidata sin equivalencia.
3. **CIE-10 (OPS/OMS):** documentado. NO acredita `Clave CIE` (sin versión
   ni catálogo declarado). Mantener pendiente.

## Archivos

- `evidencia.json` — herramienta, URL, título, fecha UTC, fragmento
  (≤25 palabras), array de IRIs completas, nombre publicado,
  `vigencia_acreditada:false`, por qué no aplica.
- Sin descargas, sin cambios a entregas/núcleo/Studio.
