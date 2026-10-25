# D-auditoría FINAL — A/B-v002-sellada/C post-R9 (2026-10-24)

**Dictamen: ACEPTAR como staging. Instalación NO aprobada** (requiere dictamen de instalación del coordinador). Solo D-auditoría/.

## Hallazgos del coordinador → estado en v002 sellada (`6ca0f2ec…`)
- 138/17/5 faltantes → **corregido**: 26 frentes con condición + referencia exacta.
- `cob.resumen` no cotejado → **corregido**: igualdad íntegra + test drift.
- CSV solo filas → **corregido**: DictReader, IRIs únicas, Counter exacto.
- 104 SHA no verificado → **corregido**: SHA físico en runtime, 104/104.
- Default staging / NoInstalado → **corregido parcial**: sin metadato, `--out-dir` explícito en staging; `reports/` libre verificado.

## Veredictos (bytes pinned en `entrega.json`)
- **A-presas ACEPTADA** (re-revisada, 16/16 SHA): Clave→/4 R6, V05 sin novedad.
- **B-v002 APROBADA sellada**: 9/9 tests, regen==sellada==congelada, staging.
- **C-preguntas ACEPTADA** (re-revisada): byte-idéntica, 7+7 no enviadas.
- v001: antecedente verificado (6/6), superado por v002. Primer dictamen preservado.
- Grafos portal/Studio: conforms, 0 violaciones, 0 mutaciones (solo lectura, `validacion/grafos.json`).
