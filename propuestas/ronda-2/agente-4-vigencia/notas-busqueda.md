# Notas de búsqueda (agente 4, ronda 2)

Solo lectura fuera de `propuestas/ronda-2/agente-4-vigencia/`. Sin contacto con publicadores.
No se consumieron propuestas de otros agentes de ronda 2.

## 1. CKAN (fuente primaria, descargada 2026-10-23T09:46:08.727202+00:00)

Método: `GET https://datos.sonora.gob.mx/api/3/action/package_show?id=<dataset>` para los 11
conjuntos. Cuerpos exactos en `evidencia/ckan/package_<id>.json`; sha256/bytes/fecha UTC
en `evidencia/ckan/ckan_manifiesto.json`. Campos inspeccionados: `title`, `notes`,
`extras` (= null en los 11), `metadata_created`, `metadata_modified`; por recurso: `name`,
`url`, `created`, `last_modified`, `metadata_modified`, `description` (vacía en catálogos).
`created`/`last_modified` son registro en el portal, no edición del catálogo.

Hallazgos:
- Ningún paquete declara edición del catálogo ni cobertura temporal en extras.
- Rangos declarados (título/nota, no cobertura observada): Hídricos ("1941 a la actualidad");
  proyecciones ("1990 a 2019" + "2020 a 2040" / "1990 a 2040"); Rickettsia ("Registro anual");
  delictiva/víctimas (procedencia SESNSP; 2015–2025 solo por títulos); educativas
  (periodo a consultar/reportar, sin rango explícito; periodos solo por títulos).
- Recurso `Datos hídricos 1960-1969` con `url` vacía: periodo declarado sin evidencia descargable.

## 2. Interiores de catálogos (fuentes centrales, solo lectura)

- `53bd…` (Hoja1, 10 entradas), `612b…` (3 hojas), `3b85…` (3 hojas), `ea54…`
  (Catalogo_Estado 32 + Catalogo_Municipios 2475; mismo sha en 3 paquetes),
  `84bb…` (cat_municipio), `96776…` (cat_entidad): ninguno declara edición, versión o fecha.
  Alcance: notas/extras CKAN + interior del xlsx.

## 3. Evidencia primaria externa (solo familia con edición nacional nombrada)

- Descargado `evidencia/externa/cmpe2016_inegi.pdf` (202 pp.,
  sha256 `66ba2fd24aa01d82684df52677b792e17fe55d38273d6325ff4f6f66a3ef714b`,
  2026-10-23T09:55:04.085665+00:00) desde las dos URLs (mismo bytes/sha).
  Citas en `evidencia/extractos/cmpe2016_citas.json`: p.2 catalogación
  (título, INEGI c2016, vii+206 p., ISBN 978-607-739-984-1); p.8 segunda edición,
  estructura de 8 a 10 campos. Acredita la EDICIÓN (F3); no aplicabilidad a periodos
  UTH, ni adopción u obligatoriedad para estos conjuntos (sin evidencia directa).
- Referencia candidata no verificada (no descargada): ficha técnica del acuerdo SNIEG
  sobre la CMPE (`snieg.mx/.../FT_Acuerdo_CMProgEstudio.pdf`). No se afirma su contenido.
- Presas/Rickettsia/territoriales: snapshots sin edición nombrada; la ausencia de
  documento de edición es solo "no localizada en el alcance descrito", no inexistencia
  absoluta. No se amplió la búsqueda externa por no haber edición nombrada que verificar.

## 4. Reglas aplicadas

- Título-año y fecha CKAN no acreditan edición ni vigencia. Coetaneidad de carga ≠ vigencia.
- Periodos por nombre de recurso = declarados por título, no cobertura observada.
- Muestras de filas antiguas no usadas como prueba de cobertura.
- Lo desconocido queda explícitamente `no_acreditada` (= falta de evidencia temporal,
  no prueba de invalidez).
