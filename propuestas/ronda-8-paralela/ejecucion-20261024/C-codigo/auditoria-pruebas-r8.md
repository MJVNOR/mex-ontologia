# Auditoría test R8 coordinador — dictamen: aceptar

Revisión acotada y estática. Sin modificar files, sin instalar R8. Sin Gemma/Obscura/externos. R8 aún no instalada en producción (`ontologia/revision-ronda-8.json` ausente → el test hace `skipUnless` por diseño); suite final la corre el coordinador tras instalar.

## Referencias (SHA-256 programáticos, hashlib sobre bytes en disco)

- Test coordinador `propuestas/ronda-8-paralela/ejecucion-20261024/codigo-coordinador/test_ronda_8.py` `db0ef74374d813d613a3f71b0c483e05200a2bdfe9f844c64496f08061ad2b7d` — 9 tests.
- API staging I3 `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/scripts/integrar_ronda_8.py` `65e631e35f4cf2c55003d8e69921af06919d965509ff670c1fe6ed0e17bae827` — coincide con entrada del sello.
- Sello I3 `propuestas/ronda-8-paralela/ejecucion-20261024/I-codigo/v003/congelada.json` `2d13a57cc212cf4e7b53b0a73ce320b4f7555cfb4269d0898951b286a042f41c` — 20/20 archivos OK; aceptadas `db3167f9…`; `entrega.json` `e36bae28…` la confirma.

## Verificado

- 9/9: delta exacto (extensión + adición no aprobada), manifiesto, IRI (`/definition/` vs `/documented-variable/`), descripción local, campo/variable/rowhash de otra fila, candidata ausente del universo, dictamen global, pin SHA.
- TMP+repin: `fixture()` copia árbol real a tmp (`copytree` + `copy2` revisión) y `repin()` refija SHAs + `manifiesto_sha256`; mutaciones solo en tmp; vivo solo leído (último negativo con `deepcopy`).
- API real: `cargar`/`validar_sobre_base`/`construir`; gates `UNIVERSO_28<=candset`, fila exacta, pin R7 4478/45/1423/16/124/1106/4523, 28 exactos, doble aprobación A/B con pin + dictamen global.
- Sin red/Gemma en el test.

## Siguiente (coordinador)

Instalar R8 y correr suite final con este test (esperado 9/9 tras instalación). No modificar test ni API en este pase.
