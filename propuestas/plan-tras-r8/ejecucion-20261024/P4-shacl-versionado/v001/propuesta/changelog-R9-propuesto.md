# Propuesta de changelog (staging, no aplicar a docs/ sin aprobacion R9)

## Formato
- `format_version`: version del esquema de entrega (este piloto: `p4-v001` = formato 1).
- `release`: ronda aprobada (R8 vigente; R9 cuando se integre lo aprobado).

## Entrada propuesta (no integrada)
- `P4 v001`: regla de exclusion documentado/candidato (TTL separado) + 4 fixtures
  validados con motor real en stores aislados (3 conformes, 1 no conforme).
- Manifiestos R1-R8 intactos; el siguiente manifiesto se ANEXA (append/snapshot),
  no se reescribe historia.

## Regla
- No mutar manifiestos ni rondas aprobadas. Cada integracion anexa un manifiesto
  nuevo y, si el motor lo soporta, un snapshot (`version`/`history`).
