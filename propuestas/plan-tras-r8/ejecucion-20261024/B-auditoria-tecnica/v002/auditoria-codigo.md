# B — Auditoría de código v002: PENDIENTE (I-código/v001 sin sellar)

Fecha UTC: 2026-10-24 (ver `auditoria-codigo.json`). Estado: **BLOQUEADO_pendiente_sello_I-codigo_v001**.
v001 preservado e intacto (`dictamen.json` 12481 B `0f43545b…`, `dictamen.md` 4798 B `ab8546cd…`).
No se integró código; sin producción, Gemma, Studio ni contactos externos.

## Lo verificado por código (sellado, íntegro)

- **P1-qudt v002** — sello 21/21 SHA OK (raíz P1 + v002; v001 histórica excluida y preservada).
  `estado=propuesta_para_auditar`: Q1 MilliM y Q3 HA para auditar (IRIs http),
  Q2 HectoM3 fuera (negativo W, sin conversión). Consultas Q1=2/Q2=1/Q3=5 filas + checks OK.
  Condición W pendiente de P1 **resuelta**: W v003 verifica los 4 SHAs normativos citados.
- **P4-shacl-versionado v002** — sello 3/3 OK. `propuesta_para_auditar`:
  forma v001 exacta (`fc301d85…`) conforma sobre snapshot aislado
  (`studio-live.ttl`, 322952 triples): conforms=true, 0 violaciones, 1442 focos
  (1423 doc + 16 cand + 0 ambos), fixtures 3×true + 1×false. Generador NO ejecutado.
- **W-estandares v003** — sello 20/20 SHA+bytes OK; v001/v002 intactas.
  Repara metadato truncado de 41 chars citado en v002 por el real de 64
  (`e2f19882…ca14e` → `e2f19882…67ca14e`); ningún otro hash difiere.
  Aclara M3: solo existencia de la IRI, no sustituciones ni factores; Q2 sigue pendiente.

## Lo bloqueado (I-código/v001 en elaboración)

Sin `congelada.json` ni `entrega.json`. Inventario exacto (no sello, 4 archivos):
`consolidar_semantica.py` (`2a2e79d1…`, 38772 B),
`ampliar_portal.py` (`58603b22…`, 16638 B),
`vocabulario-minimo.ttl` (= vocabulario P1 v002, `9dcff942…`),
`shape-exclusion-significado.ttl` (= forma v001 P4, `fc301d85…`).
`tests/` solo trae `fixtures/` vacío: staging **no ejecutable**;
invariantes R8 / manifiesto / A+B por caso y scope **no verificables** (sin sellar).

## Desbloqueo

I-código debe sellar `v001/congelada.json` + `entrega.json` (scripts, tests con
fixtures, manifiesto, auditorías A/B por caso, scope). Tras ello: correr tests
staging en aislado, verificar invariantes/manifiesto/A+B y emitir dictamen final.
Detalle máquina y SHAs en `auditoria-codigo.json`.
