# Resultado — Agente 4, ronda 2: vigencia por periodo de las 16 referencias

## Entregables (en `propuestas/ronda-2/agente-4-vigencia/`)

- `matriz-vigencia.json` / `matriz-vigencia.md`: 16 filas V01–V16 con F1–F4 y clasificación.
- `propuestas.json`: 16 propuestas (no aplicadas) que registran `vigencia: no_acreditada` + facetas.
- `notas-busqueda.md`: método, URLs, hallazgos.
- `verificar.py`: reproducible (`uv run python propuestas/ronda-2/agente-4-vigencia/verificar.py`) → TODO OK.
- `evidencia/ckan/`: 11 `package_<id>.json` + `ckan_manifiesto.json` (consulta real 2026-10-23T09:46:08.727202+00:00).
- `evidencia/externa/cmpe2016_inegi.pdf` + `evidencia/extractos/cmpe2016_citas.json`.

## Correcciones del integrador (aplicadas, sin cambio de clasificación)

1. Fechas: consulta real CKAN citada desde manifiesto (`fecha_consulta_ckan_utc`);
   generación como campo separado (`fecha_generacion_utc`). F1 con fechas crudas completas
   (microsegundos) comparadas contra los package originales en `verificar.py`.
2. Redacción: `created` CKAN = registro en portal, no edición; F4 dice "fecha de edición y
   aplicación histórica no documentadas". Ausencia de documento = no localizada en el alcance.
3. CMPE 2016 con evidencia primaria fijada (PDF, sha, pp. 2 y 8); sin afirmar adopción/
   obligatoriedad/aplicabilidad a UTH. Ficha SNIEG queda como candidata no verificada.
4. Verificador endurecido: F1 completos, 6 SHAs únicos, identidad contra agente-1/
   territorio.json, facetas matriz↔propuestas, coherencia de fechas.

## Resultados

- Clasificación: **16/16 `no_acreditada`** (= falta de evidencia temporal, no invalidez).
  0 documentada/parcial. `des_mpo_res` fuera de matriz (sin resolver, P09).
- F1: 11 paquetes sin `extras` temporales; catálogos sin descripción; registro/modificación
  por referencia en el JSON.
- F2: periodos declarados por título/nota (cuatrimestres 2022–2026, anuales 2022–2025,
  décadas 1941–2024, anuales 2022–2024, 1990–2019+2020–2040 / 1990–2040, 2015–2025).
- F3: CMPE 2016 acreditada con evidencia primaria (V01–V04); resto sin edición determinada.
- F4: ausente en las 16.

## Limitaciones

- Recurso 1960–1969 sin URL; `AGZCH` (Chihuahua) en presas; `ea54…` compartido sin
  transferencia de vigencia; ficha SNIEG no verificada; sin contacto con publicadores.
- Sin comprobaciones de valores ni cotejo de localidades (agente 3).

## Pruebas

`verificar.py` → TODO OK (conteos, espejo matriz↔propuestas, 11 sha CKAN, F1 completos ×16,
6 sha únicos, identidad central, facetas, fechas, sha PDF).
