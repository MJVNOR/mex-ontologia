# Dictamen de auditoría semántica — v001 (2026-10-24)

Alcance: C1, C2, C3, C4, P2, P3. Excluidos: P1, P4 (en curso, no revisados).
Método: read-only, re-hash SHA-256 por código, conteos independientes. Sin Gemma, sin web general, sin contactos. Sin cambios en producción.
Nota: AGENTS.md buscado en raíz y `propuestas/**`: no encontrado; se aplicaron los límites de cada asignación.

## Decisiones

- **C1-candidatas: APROBADA.** 17/17 casos (5 recursos, 5 conjuntos, 5 diccionarios; 16 candidata_sin_definicion + 1 fuera_del_núcleo). Ninguna cumple Puerta 1; 0 promociones, 0 cambios, 0 consultas. Hashes: entrega.json `e664d16c…`, entrega.md `cf4da50e…`. Menor: resto de plantilla en motivo del caso 6.
- **C2-oportunidades: APROBADA.** Heurística, sin joins (reproducir.py solo filtra, assert 1191). Oportunidad ≠ join declarado. Mapa 3916 = 2328+1191+396+1; overlay R8 desfasado declarado, no regenerado. Hashes: `386aaea0…` / `81790c3c…`. Menores: reproducir verifica, no regenera; default `pesos.get(f,1)`; formato 3.0 vs 3.
- **C3-cobertura: APROBADA.** 5523 filas lógicas, 5523 IRI distintos (16 filas con salto interno; `wc -l` sobrecuenta). Estados 4506+17+833+154+13 = 5523; con_correspondencia 4523. 5 observaciones. Distingue columnas de significados (138+2 corruptas). Hashes: entrega `04a3fc2b…`, matriz `b6082557…`, totales `cb5d5110…`. Menor: entrega dice 7 campos, cabecera real 9.
- **C4-referencias: APROBADA.** 19/19 = 16 vigencias + 3 anomalías. 0 propuestas; 104 evidencias con sha+ruta+localizador. 138 significados / 16 vigencias / des_mpo_res / V13-V14 consistentes. 7 preguntas sin envío, 0 peticiones web. Hashes: `88a20430…` / `9edadb0d…`.
- **P2-owl-time: APROBADA COMO NEGATIVA.** Nada que integrar. Inventario 4/4 sin bordes; piloto 0 triples ProperInterval; prohibido inventar UTC/calendario. Fixture 0 filas. Hashes: `fca5a923…` / `e276d093…` / piloto `7ca61813…`. Estructural: consultas/congelada/peticiones viven en `P2-owl-time/`, no en `v001/`.
- **P3-jerarquía-clínica: APROBADA COMO NEGATIVA.** 101/101 casos 1:1 con asignación. 0 broader en las 3 fuentes; 0 agrupaciones; sin fusión por parecido léxico. No habilita jerarquía inventada. Hashes: `99f106c9…` / `5d44066e…`. "138 significados" no pertenece a P3 (aquí: 1106 conceptos / 1423 respaldados).

## Reglas transversales verificadas

P2/P3 negativos no habilitan datos inventados. C2 oportunidad ≠ join validado.
