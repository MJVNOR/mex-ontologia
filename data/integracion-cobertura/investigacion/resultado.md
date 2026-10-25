# Investigación con Obscura (solo lectura web)

Pestaña propia (tab-2), cerrada al final. Insumos verificados 23/23 SHA OK
contra `fuentes/manifiesto.json`. Sin promociones ni cambios a diccionarios.

## Resultado

4 temas; ninguna fuente confirma variables locales (`vigencia_acreditada:false`
en todas: documentan catálogos, no el vínculo con la variable).

1. **Portal Sonora SEED**: solo Diccionario + Defunciones 2022; sin
   manual/catálogo para CERTIFICADOPOR/SITIODEFUNCION/FECHACERTIFICACION.
   Negativo.
2. **DGIS índice de catálogos** (NOM-024): confirma catálogos candidatos
   (Entidades, Diagnósticos, etc.). Neutro.
3. **CAT_LENGUAS_INDIGENAS** (origen INEGI, actualización 2018, página
   2021-07-01): pertinente a HABLALENGUAINDIGENA(D) y Grupo Indig. (Habla).
   Candidata sin confirmar.
4. **CAT_LOCALIDADES** (origen INEGI, actualización septiembre 2026, página
   2026-10-21): pertinente a LOCALIDADOCURRENCIA(D)/LOCALIDADCERTIFICA(D).
   Candidata sin confirmar.

## Negativos

`browser_search` sin resultados; Google con CAPTCHA; URL SESNSP adivinada 404
(instrumento de delitos no localizado); INEGI vitales sin formato localizado;
certificado de defunción SSA sin página localizada; semana epidemiológica,
SEP-911 y Marco Geoestadístico no consultados (presupuesto).

## Archivos

- `evidencia.json` — herramienta, URL, título, fecha, fragmento (≤25
  palabras), IRIs completas, versión acreditada o no, aplicabilidad/límite,
  conclusión por tema.
- `listo.json` — estado listo + SHA-256 de evidencia.json.
