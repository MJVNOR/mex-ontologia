# Localidades Sonora — agente-3 ronda-2 (referencia oficial INEGI)

Fecha: 2026-10-23. Escritura exclusiva en `propuestas/ronda-2/agente-3-localidades-inegi/`. Sin asignar localidades a otros conjuntos. Evidencia central usada: `data/integracion/fuentes/771cc…xlsx` y `data/integracion/manifiesto.json` (no la carpeta histórica del agente 2).

## 1. Fuente oficial: ITER Censo 2020, Sonora

- Descarga: `fuentes/iter_26_cpv2020_csv.zip` (799029 B, SHA-256 `4ad93805…96dee2`, consulta 2026-10-23) desde `https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_26_cpv2020_csv.zip`.
- Descriptor: `fuentes/fd_iter_cpv2020.pdf` (SHA-256 `1b7ea20f…1876525eb`). Metadatos en `inegi-fuente.json`.
- Fecha de referencia ITER: **2020-03-15** (levantamiento 2–27 mar 2020). IML declara año **2020 sin día/mes**: el año común acredita comparabilidad temporal, **no por sí solo idéntico corte**.
- Propósito ITER: publicar indicadores del cuestionario básico por localidad. No es el universo cartográfico (Marco Geoestadístico) ni el estudio de marginación: coberturas pueden diferir por diseño.
- Confidencialidad (LSNIEG): localidades de 1–2 viviendas agregadas en `LOC 9998/9999` por municipio y entidad; resto de indicadores con asterisco. Ver `inegi-fuente.json`.
- Formato verificado: UTF-8 con BOM, coma, `quotechar` comillas dobles estándar → 7500 filas, 286 columnas, 0 malformadas. Las comillas simples **no** son delimitador ni envoltura (usar `quotechar="'"` rompe 2 filas: líneas 1197 y 7495, `NOM_LOC` con comillas dobles literales). Los valores comparados son los literales del CSV, sin retiro de envolturas.

## 2. Separación previa (no se comparan agregados como localidades)

- ITER Sonora: 7500 registros = 75 agregados (`MUN 000` o `LOC 0000`: 1 total entidad + 2 acumulados entidad + 72 totales municipales) + 125 especiales confidenciales (`LOC 9998/9999` por municipio) + **7300 localidades censales publicadas**, claves únicas.
- IML_2020: 1850 filas, 1850 CVE únicos, 0 especiales (`0000/9998/9999`), 72 municipios. Códigos ya en TEXTO con ceros.
- Validación estricta: `zfill(2/3/4/9)` solo si el original textual cumple `^[0-9]+$` ASCII (`[0-9]` no incluye dígitos Unicode); `float`/decimales se rechazan sin truncar; cada padding quedaría registrado aparte. **0 transformaciones** (ninguna hizo falta).

## 3. Contraste (ver `contraste-localidades.json`; detalle solo-ITER en `solo-ITER-CVE.json`)

- Estatus: **contraste_completo**, definido como comparación completa de **estas dos fuentes publicadas** (IML_2020 vs ITER Sonora 2020). No significa catálogo cartográfico completo, ni idéntico universo, ni equivalencia institucional.
- Intersección: **1850/1850** claves IML presentes en ITER; **0** solo-IML.
- Nombres literales: **0** diferencias (y 0 normalizadas sin acentos/caso); **POBTOT** igual en **1850/1850**.
- Solo-ITER: 5450 localidades censales no incluidas en IML; 5295 con 1–9 hab. Ningún municipio con IML > ITER; los 72 municipios cubiertos en ambas.
- La coincidencia total en claves, nombres y población acredita la referencia, no identidad de universos. La causa metodológica de las 5450 exclusiones **no queda demostrada** sin documentación de selección de IML: se describe el perfil (localidades muy pequeñas), no se afirma el motivo.

## 4. Marco Geoestadístico 2020

No consultado: lo declarado es este cotejo de dos fuentes, y el MG no es obligatorio para ello. No se afirma que todas las diferencias de universo estén oficialmente explicadas.

## 5. Condiciones de uso

- Permitido: evaluar comparabilidad contra la derivada IML con huella `771cc22d…` usando correspondencias calificadas, citando hoja/fila y códigos originales.
- Prohibido: asignar localidades a registros, confirmar identidad por nombre, `owl:sameAs`/`skos:exactMatch` desde la derivada, homologar `9998/9999/0000`, o completar ceros silenciosamente.

## 6. Reproducción y verificación

- `uv run python propuestas/ronda-2/agente-3-localidades-inegi/descargar_iter.py` (falla si cambia un SHA)
- `uv run python propuestas/ronda-2/agente-3-localidades-inegi/contrastar.py` (recalcula y escribe)
- `uv run python propuestas/ronda-2/agente-3-localidades-inegi/contrastar.py --check` (solo lectura, no escribe; sale 1 ante SHA cambiado, claves inválidas/duplicadas, CSV malformado, composición inconsistente o conteos/listas que no coincidan). Ejecutado: OK 1850/0/5450. Prueba negativa ejecutada: conteo alterado → falla con exit 1.
