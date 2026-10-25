# Cierre R7 — borrador S1 (no integrado; métricas/Studio las completa el coordinador)

Expediente: `propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/`.
Selección vigente: `seleccion-v002.json` (2026-10-24T07:51:38Z; reemplaza a `seleccion.json`
para incorporar V4 v004 final con W-v003). Lote auditado: `lote-2.json`
(S2-nacimientos v002 + V3-coespo v002; S6 y V4 van en adenda según A/B).
Dictámenes globales A y B: **aceptar**, 31 propuestas aceptadas cada uno
(`A-documental/dictamen.json`, `B-tecnica/dictamen.json`, misma `seleccion_sha256`).

## 1. Lo aprobado (auditoría doble A+B, sin afirmar integración)

- **31 nuevos significados SINAC** (S2-nacimientos v002, tiers A1–A5; 9 aceptar +
  22 aceptar_con_texto_acotado en A; 27 aceptar + 4 acotados en B; 0 rechazos).
  Base: descriptor SINAC 2020-2025 + codebook SINAC 2020-2023 (zip de 20 xlsx,
  contenido no examinado antes), prueba por ID código local en catálogo +
  etiqueta D idéntica. Universo fijado en `integracion/trabajo/universo-31.json` (31).
- **3 mappings promovibles**: pares estructurales 83, 102 y 104 (S2) dentro del
  universo 31 (`integracion/trabajo/pares-20.json`: 3/20 `en_universo_31`).
  Delta esperado (plan, no hecho): `documental_revisada` 4478, `candidata_por_nombre` 17
  (`integracion/materializacion/v001|v002/delta.json`: reglas 31, vínculos 3,
  conceptos 31; `respaldada_por_definicion` 1423).
- **Distinción 31 reglas vs 20 pares**: las 31 reglas nuevas (una por significado
  aceptado, alcance mínimo por ID) no son los 20 pares estructurales previos; solo
  3 de esos 20 pares entran al universo y se promueven; 17 quedan candidatos
  (15 de otros frentes + D103/D105 de S2).

## 2. Pendientes reales: 138 significados (169 − 31), todos brecha externa salvo V13/V14

| Frente | Estado | Reapertura (condición exacta) |
|---|---|---|
| S1-defunciones (32) | 32 brecha (v002) | Nota del publicador con tabla columna↔campo + codebook/edición por fila; S1-WEB-01 (dashboard, ámbito fetal) pendiente, solo adenda |
| S2-nacimientos (22) | 22 brecha (D-derivadas + ANOMALIACIE) | Variable nacional o regla de decodificación publicada para el par D |
| S3-matrículas (30) | 30 brecha | Diccionario del sistema escolar / nota UES aplicable a 2022-2 con vínculo campo/recurso/edición; WEB-MAT-02 pendiente de W |
| S4-epidemiología (25) | 25 brecha | Instrumento SUIVE edición 2022 que fije objeto de cve_cie10 y versión CIE vinculada al recurso; WEB-S4-01 pendiente, solo adenda |
| S5-TIC (24) | 24 brecha | Cuestionario/instrumento del Diagnóstico del Entorno Digital o muestra de valores vinculada a fila/recurso/edición |
| S6-diversos (5) | 5 brecha (v002, W sin_hallazgo) | Documento primario que fije objeto de cada campo (egresos/urgencias, periodo denuncias, pesca, `CLASIF`) |

## 3. Vigencias: 16 (V13/V14 en acceso_no_resuelto, resto brecha)

- V1 (V01–V05, UTH/Presas): brecha; falta adopción institucional CMPE y edición del catálogo de Presas para los periodos.
- V2 (V06–V08, Rickettsia): brecha; falta declaración de edición/versión/fecha del catálogo (sha `3b8546ac`) con vínculo 2022-2024.
- V3 (V09–V12, V15–V16, COESPO): brecha con novedad corregida (rev. auditoría A); falta declaración COESPO con edición/versión/fecha de `catalogo.xlsx` (sha `ea54aad3`) + periodos.
- V4 (V13/V14, SESNSP): **acceso_no_resuelto** (v004 final): descarga del Diccionario 2015-2025 agotada por estas vías (HTML/login, token 302, rejilla sin descarga); falta declaración del publicador (DEP-CAT-R6-05) con edición/corte + contenido legible del diccionario. Reapertura fuera de las vías agotadas.

## 4. Anomalía V2: des_mpo_res + encabezados 177/178 (3 registros, no 3 significados)

CSV vivo con 178 filas; las 2 últimas repiten la cabecera como valores (artefacto confirmado sin cambios); `des_mpo_res` fila 7 en texto libre sin catálogo de municipios de residencia en el inventario API cerrado. Falta: fe de erratas o diccionario corregido del publicador (conjunto `5494daa1`, recurso `33d0a99e`) + URL del catálogo si existe. Se conserva sin curar; no acredita nada.

## 5. Fuentes W congeladas (3 paquetes pinnados en seleccion-v002)

- `W-web/paquete/congelada.json` (`ae1b75c7…`): Manual metodológico RNID V1.0 (pdf, sha `ca00bfb7…`) + `sinac_descriptores_2020_2025_V2026-07-09.zip` + página SESNSP.
- `W-web/paquete-v002/congelada-v002.json` (`9abd3885…`): diccionario vigilancia epidemiológica 2026-10-24 (csv) + PROAES indicador-3 2021-2027 (pdf); P-S6-01/P-S6-02 sin_hallazgo con examen real.
- `W-web/paquete-v003/congelada-v003.json` (`c2e3142b…`): SESNSP negativo definitivo (F-V003-01-SP-DL; sin copias binarias, HTML rechazado como XLSX); cierra la rama "si W trae XLSX".
- Peticiones aún pendientes (adenda, no bloquean): S1-WEB-01, WEB-MAT-02, WEB-S4-01.

## 6. Lo que este borrador NO afirma (campos del coordinador)

- [ ] Integración R7 aplicada (código v003 no instalado; v001/v002 intactas).
- [ ] Métricas finales del núcleo (reglas / conceptos / correspondencias / significados).
- [ ] Sincronización Studio (respaldo previo existente en `integracion/respaldo-studio-previo.ttl`; sincronizar solo con cambio de grafo aprobado).
- [ ] Dictamen global final con adenda S6/V4 y `seleccion.json`.
- [ ] Validaciones de datos/SHACL y regeneración de artefactos tras integración.
