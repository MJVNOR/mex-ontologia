# Agente 12 — Auditoría agente-6-salud (outcome actual: v2, 203 reglas)

## Versiones

- **v1 histórica:** `auditoria-v1-204.json` + `scripts/verificar_auditoria_v1.py`
  (204 aceptar-197/condicionado-7; 5 espacios finales recortados). Registro de
  versión, ya no es el outcome.
- **v2 actual (esta auditoría):** `auditoria.json` (203 dictámenes por IRI) +
  `scripts/verificar_auditoria.py` → **2076 comprobaciones OK**.
  SHA propuestas auditada:
  `2b12af0c61044ef5c059be0db1d0a641b64a72121b4254e37034bb685b4bcc73`.

## Cambios verificados en v2 (por IRI, no por ID renumerado)

- 203 proponer / 39 pendientes / 178 conceptos; partición 242 intacta.
- `de01_a_04` (...%2F13) pasó a pendiente `rango_contradictorio_nombre_descripcion`;
  sin regla; slug `de-1-a-4-anos` eliminado. RESUELTO.
- `lcr` conserva aspecto agua de roca en etiqueta y definición. RESUELTO.
- Inmuno: límite explícito NO equivale a positivo/negativo. RESUELTO.
- Servicios: catálogo identificado sin vigencia/valores, sin afirmar validado
  (verificado contra fila de inspección). RESUELTO con límite.
- `normalizado`: presente en literal de la fila (publicador). RESUELTO.
- CIE: límite sin expandir por formato/ejemplo/campo ×2. RESUELTO.
- 7 `descripcion_raw_literal` byte-exactos vs inspección; huellas intactas.
  RESUELTO (incluye 2 pendientes con raw: `ide_id`, `otros_especifique`).

## Dictámenes v2: aceptar 203, condicionado 0, rechazar 0

Negativos reales: solo-nombre, contexto mutado, otra IRI y `de01_a_04`
promovido no respaldan. 39 pendientes con razón.

## Límites

Sin red; sin cambios fuera de esta carpeta. No se aplica integración;
outcome actual 203 listo para integrador.
