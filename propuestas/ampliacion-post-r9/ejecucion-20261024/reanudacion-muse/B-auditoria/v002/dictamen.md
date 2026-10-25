# Dictamen B v002 — V-pruebas/v001 apta para tests/

Fecha UTC: 2026-10-25. Carpeta: `reanudacion-muse/B-auditoria/v002`. v001 sellada intacta, no se toca.

## Veredicto: aceptar

`test_ronda_10.py` SHA `41aec2892decaccd85313097d2979de7f18ac927e6faa40ed4fba164f4f086b1`
(sello V verificado: test + resultados + entrega coinciden).
Re-ejecutado por B: **18/18 OK, 0 skips**, con auditorías reales A+B.

## Portabilidad (apta para tests/ sin cambio)

- Localiza ROOT por `config.toml`+`scripts` en ancestros; `sys.path` a `scripts`.
- K: usa `scripts/integrar_ronda_10.py` si existe, si no el candidato K (fallback explícito).
- MAT: usa `data/integracion-ronda-10` si instalada, si no `payload/v001`.
- Solo stdlib `unittest` + `rdflib` (como el resto de tests/); sin red.
- Escrituras solo en `tempfile` (mutaciones y raíz TEMP); fuera de eso solo lee.

## Cobertura y aserciones

- Material (7): SHA+cabecera, sello 16/16, 5 filas (canon, 1-based, fuente, normativa
  3.5.3, `normativa_uri==unidad_qudt`), Q-U06 sin `http`/`completo`, 60 triples,
  6 formas+PROV, snapshot/PIN/config.
- Mutaciones (5 tests, 7 vías): triple extra, M3, conversionMultiplier, literal no-xsd,
  unidad M3, forma fantasma, unidad duplicada — todas exigen `ValueError`. Válidas.
- Contrato (6): estado auditorías, `cargar`, `construir` (5u/6f, grafo >60),
  `cargar_shapes` (6), rechazo 2×5 auditorías + núcleo/IRI. Sin skips con A+B reales;
  sin A+B quedaría PENDIENTE declarado y los rechazos igual corren. Sin aserciones
  inválidas detectadas (`next(fdir.iterdir())` asume 1 fichero por caso, cierto hoy;
  `>60` es cota débil pero el preflight fija el 90 exacto).

## Preflight del coordinador (solo lectura)

`M/preflight.json`: OK, 90 triples extensión, 73 formas, 5u/6f, base130 intacta,
integrador `05e834fd…`, no instalado. Coherente: 90 = 60 datos + 30 trazas PROV;
73 = `K._shapes` real (verificado en v001); helper `preparar_integracion.py` no está
en repo (solo su salida), nada que revisar en código. No se reaudita todo.
