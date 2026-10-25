# Parches para R7 (resueltos en copias completas de `codigo/`, NO instalados)

> Staging: `codigo/integrar_ronda_6.py` y `codigo/consolidar_semantica.py` son
> copias completas modificadas, verificadas contra los originales con
> `git diff --no-index` (solo los hunks descritos abajo). `R5` no necesita cambios.

## 1. `scripts/integrar_ronda_6.py` — mismo cuidado que el fallo R5 corregido

Estado actual (`validar_sobre_base`, líneas ~39-57): compara `rules != expected`
**antes** de validar duplicados/aprobaciones y no delega. Parche: validar los
invariantes propios primero y delegar a R7 antes de comparar, espejo de R5
(`scripts/integrar_ronda_5.py` líneas 47-62):

```python
  for field, key in [('reglas_descripcion_exacta', 'id'), ('vinculos_documentales_revisados', 'columna')]:
      ids = [r[key] for r in rules[field]]
      if len(ids) != len(set(ids)):
          raise ValueError('Reglas o columnas duplicadas en ronda 6')
  for audit_name, category, key in [('auditoria-a', 'reglas', 'id'), ('auditoria-b', 'vinculos', 'columna')]:
      audit = json.loads((folder / 'auditorias' / f'{audit_name}.json').read_text(encoding='utf-8'))
      approvals = {x['id'] for x in audit['dictamenes'] if x['tipo'] == category and x['dictamen'] == 'aceptar'}
      for row in accepted[category]:
          if row[key] not in approvals:
              raise ValueError('Ronda 6 sin aprobación independiente: ' + row[key])
  if (root / 'ontologia/revision-ronda-7.json').exists():
      import sys as _sys
      _here = str(Path(__file__).resolve().parent)
      if _here not in _sys.path:
          _sys.path.insert(0, _here)
      from integrar_ronda_7 import validar_sobre_base as validar_ronda_7
      return validar_ronda_7(rules, expected, root)
  if rules != expected:
      raise ValueError('Ronda 6 permite solo la base y la adenda-diversos auditada exacta')
  return config, folder, baseline, accepted, sources
```

Es decir: mover el `if rules != expected` debajo de las dos validaciones y de la
delegación (actualmente está encima). Sin este reorden, R7 heredaría el defecto
de orden que R5 ya corrigió.

## 2. `scripts/integrar_ronda_5.py` — sin cambios de lógica

Su delegación (`if revision-ronda-6.json existe: delegar a R6`) ya propaga a R7
una vez aplicado el parche 1. No tocar.

## 3. `scripts/consolidar_semantica.py:generar()` — bloque R7 espejo del R6

Aplicado en `codigo/consolidar_semantica.py` (copia completa). Hunk añadido
después del bloque R6, sin alterar los anteriores:

```python
    if (ROOT / 'ontologia/revision-ronda-7.json').exists():
        from integrar_ronda_7 import construir as integrar_ronda_7
        r7_data, r7_report, r7_sources = integrar_ronda_7(report, rules, base)
        data += r7_data
        report['integracion_ronda_7'] = r7_report
        sources.update(r7_sources)
```

## 4. `scripts/ampliar_portal.py` — sin cambios previstos

R4/R5/R6 no tienen shapes propios (solo ronda-2/3 añaden `.ttl`, líneas ~214-218);
R7, al ser solo 1 regla sin correspondencias, tampoco necesita shape nuevo.

## 5. Archivos que solo existirán al integrar (no crear ahora)

- `ontologia/revision-ronda-7.json` (`evidencia` + `manifiesto_sha256`).
- `data/integracion-ronda-7/{manifiesto.json, base-semantica.json (= estado R6),
  aceptadas.json (1 regla / 0 vínculos / 1 concepto), auditorias/auditoria-a.json,
  auditorias/b.json}`.
