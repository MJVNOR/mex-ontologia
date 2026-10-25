# A-presas — revisión READ-ONLY cierre R9 (2026-10-24)

**Decisión: NO REAPERTURA. No se integra nada.**

## 1. Qué se comparó (local, sin web nueva)

- `propuestas/pendientes-muse-r6/diversos-presas/adenda-presas.json` (SHA `18689699…`) + `adenda-presas.sha.json` (marker) + `adenda-presas.md`
- `propuestas/pendientes-muse-r6/auditoria-documental/dictamen-presas.json` (SHA `2b9098b1…`) + `listo-dictamen-presas.json` (cita `sha_adenda 18689699…`, `sha256 dictamen 2b9098b1…`)
- Auténtico: `propuestas/pendientes-muse-r6/web/evidencia/cat_estatal_1.xlsx` — 11981 B, SHA `b7a398a0…` = `sha256_fragmento` histórico citado en adenda. Corrobora, no es novedad.
- Snapshots: `reports/ronda-6.json` (`52b6abc5…`, presas RESUELTA con límites), `reports/ronda-8.json` (`5ac384bc…` = base de C4v002), `reports/ronda-9.json` (`5b35072f…`, 16 vigencias pendientes, sin evidencia nueva).
- Caso V05/C4v002: `C4-referencias/v002/entrega.json` (`32478e45…`) caso V05 `sin_evidencia_para_integrar / brecha_externa / sin_pista_nueva`; `matriz-preguntas.json` (`8c180f57…`) ND-02/PQ-02; `V1-uth-presas/v001/entrega.json` (`bf684ec6…`) igual.
- Evidencias V05 recalculadas: API V05 `2776b929…`, página recurso 1960-1969 `e2c474…`, `data/territorio/fuentes/f5060479…xlsx` `612b2b11…` — idénticas a las citadas en C4v002. Sin bytes nuevos.

## 2. Distinción obligatoria

- **Puntual YA integrada (R6):** `cat_estatal/Clave → definición /4` (clave-identificadora-presa). Pin documental solo-columna, con 13 hermanas a `Catalogo_estatal`, huellas `29af60e8…/d1208344…` recomputadas. Límites de adenda/dictamen: sin joins por Clave, sin identidad de dominios, sin vigencia/edición.
- **Vigencia histórica SIN acreditar (sigue abierta):** V05 F3+F4 ausentes (sin edición/versión/fecha del `Catalogo_estatal` ni vínculo 1941–2024; recurso 1960-1969 con `url=""`). C4v002 corrige organismo a `sagarhpa` y UUIDs completos — corrección documental, no evidencia primaria nueva.

## 3. Por qué no hay novedad

Todo lo localizable ya estaba citado e integrado o evaluado en R6–R9. R9 solo añade 2 declaraciones QUDT locales (Milímetros, Hectáreas) + regla SHACL; `hm³` explícitamente no enlazado. `docs/plan-actualizado-tras-r9.md` registra: 0 evidencia primaria nueva, 16 vigencias pendientes.

## 4. Límites respetados

No joins, no identidad de catálogos, no unidades/conversiones. Sin Gemma/contactos/browsing general. Sin modificar fuentes ni manifiestos R1–R9. `**/AGENTS.md` inexistente en el repo.

## 5. Única pista futura (solo para auditar, nunca producción)

Reutilizar sin cambios C4v002 ND-02/PQ-02: si aparece declaración `sagarhpa` + URL efectiva `4d1bb645…`, entonces auditar. Hoy `activa: false`. Ver `entrega.json` y `hashes.json`.
