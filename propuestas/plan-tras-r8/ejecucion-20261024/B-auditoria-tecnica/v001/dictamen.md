# B — Dictamen de auditoría técnica v001 (C1–C4, P2/P3 sellados)

Fecha UTC: 2026-10-24T10:22:53.687076+00:00 · Alcance: sellados bajo `propuestas/plan-tras-r8/ejecucion-20261024/`.
P1/P4 no dictaminados. Sin producción, sin Gemma, sin Studio, sin contactos externos.

Nota de método: no existe `AGENTS.md` en el repo (búsqueda `**/AGENTS.md` sin resultados);
se aplicaron las restricciones de la asignación (solo escritura en `B-auditoria-tecnica/v001`,
verificación SHA-256 por código con stdlib vía `uv`, sin sustituir MCP por CLI).

## Decisión global

**CONFORME** en los 6 roles auditados. Sellos SHA íntegros, FuenteR8 inmutable,
reproducibilidad y conteos verificados por código. Detalle máquina en `dictamen.json`.

| Rol | Sello | Decisión |
|---|---|---|
| C1-candidatas | `C1-candidatas/v001/congelada.json` íntegro (3/3) | CONFORME — 17/17, 0 promociones |
| C2-oportunidades | `C2-oportunidades/v001/congelada.json` íntegro (7/7) | CONFORME — 1191/50/3916 reproducibles |
| C3-cobertura | `C3-cobertura/v001/congelada.json` íntegro (5/5) | CONFORME — 5523 y partición verificadas |
| C4-referencias | `C4-referencias/v001/congelada.json` íntegro (5/5) | CONFORME — 19/19, 104/104 evidencias |
| P2-owl-time | `P2-owl-time/congelada.json` (raíz del rol, ref. v001) íntegro (6/6) | CONFORME negativa — 0 intervalos |
| P3-jerarquía-clínica | `P3-jerarquia-clinica/congelada.json` (raíz del rol, ref. v001) íntegro (6/6) | CONFORME negativa — 101 exactas |

## Verificaciones (código, stdlib)

- **FuenteR8 inmutable:** todas las rutas de `base.json` (`b3ac1894…`) coinciden byte a byte.
  Resumen congelado: 1563 definiciones, 1442 materializadas, 5523 columnas, 4523 con
  correspondencia, 1106 conceptos, `des_mpo_res` sin resolver, 6 condiciones.
- **C1:** 17 casos con IRI columna; 16 sobre significado candidata + 1 Total_Egresos
  fuera_del_núcleo; Puerta 1 impide promoción; sin artefactos de integración (declarado).
- **C2:** mapa `oportunidades-cruce.json` 3916 pares = 2328+1191+396+1; matriz 1191 filas
  únicas = 100% `candidata_por_validar`; top50 50 filas; recálculo
  `score=suma(pesos)+suma(penalizaciones)`, orden score desc/id asc, coincide fila a fila
  con CSV y con `top50_resumen` (0 discrepancias); mapa no reescrito.
- **C3:** `matriz-columnas-5523.csv` 5523 filas, `columna_iri` única 5523/5523;
  partición 4506+17+833+154+13=5523 verificada en CSV; 4523=4506+17;
  1563 variables en `cobertura.json`, 1442 con iri =1423+16+3 (3 fuera_con_iri por huella);
  154 columnas ≠ definiciones; 140=138+2 headers; 5 observaciones con localizador.
- **C4:** 19/19 casos (16 vigencias + 2 encabezados corruptos + `des_mpo_res`);
  104/104 evidencias SHA-256 coinciden; 0 propuestas; conserva 138/16/`des_mpo_res`/17;
  V13/V14 acceso no resuelto declarado.
- **P2:** 4/4 familias inventariadas, bordes inicio/fin `null`, 0 `ProperInterval`;
  `consultas/intervalos-periodos.rq` espera 0 filas + fixture `bindings: 0`;
  plantilla `piloto-owl-time.ttl` sin instanciar; 11 fuentes con SHA (base.json coincide).
- **P3:** 101/101 casos, `set(entrega)==set(asignacion)`; 0 `broader` en `semantica.json`
  y `revision-ronda-8`; diccionario `33d0a99e` plano (Unidad vacía en las 101);
  `grupo-caso-con.rq` → 101 filas 0 broader + `detalle-caso-con.rq` + fixture.
- **Roles:** `roles.json` SHA de las 6 asignaciones coinciden; `propuestas/plan-tras-r8/`
  es árbol untracked nuevo (no modifica tracked de producción).

## SHA de entregas (re-verificados por código)

- C1 entrega.json `e664d16c…116f72` (68136) · entrega.md `cf4da50e…3747a` (43791)
- C2 entrega.json `386aaea0…05481` (28321) · entrega.md `81790c3c…d7870` (4090) ·
  matriz `2f5fec40…03db58` (682244) · top50 `db1182cd…6174a` (9660) ·
  criterio `2296486d…311306` (1800) · reproducir.py `b1ad47ea…762a44` (1038) ·
  fixture `f8ec2140…0957e` (647)
- C3 entrega.json `04a3fc2b…7573cb13` (4618) · entrega.md `2fd78215…4c3c3c` (2694) ·
  csv `b6082557…28e17ac` (2168469) · totales `cb5d5110…8790e` (169266)
- C4 entrega.json `88a20430…68f61` (91306) · entrega.md `9edadb0d…e9138` (4673) ·
  matriz-preguntas `e505b161…f0efb1` (8151) · peticiones `03a264ad…35aec` (265)
- P2 entrega.json `fca5a923…d0433` (11679) · entrega.md `e276d093…3cd0c` (1212) ·
  piloto `7ca61813…0c807` (777) · rq `6f8a7efe…bcf223` (402) · fixture `889a791a…ca983` (124) ·
  peticiones `e2f19882…ca14e` (824)
- P3 entrega.json `99f106c9…0a2ac` (98658) · entrega.md `5d44066e…bea66` (1464) ·
  grupo.rq `c5db2018…bae598` (600) · detalle.rq `8edfb1ff…835bd` (875) ·
  fixture `e5a46cf9…9150a86` (258) · peticiones `13c73dec…0aabc` (293)

SHAs completos y bytes en `dictamen.json` (§`sha_entregas`).
