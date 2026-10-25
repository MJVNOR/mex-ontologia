# Q-unidades v003 â€” exclusiones (sin triple en el TTL)

## Q-U01 `Toneladas` (PRODTON, 94215f51) â€” variante local no acreditada

W v002 verifico `http://qudt.org/vocab/unit/TON_Metric` y dejo constancia de que el literal local no elige variante. El corpus usa `Toneladas` sin calificativo en 3 definiciones de 2 diccionarios (agricultura y pesca). Asignar TON_Metric seria decidir la unidad local desde la norma: no se hace.

Reapertura: evidencia local (documentacion del recurso o del publicador) que declare tonelada metrica para esa definicion.

## hm3 / `HectÃ³metros cÃºbicos` (1 fila) â€” busqueda agotada

HectoM3: 404 + ausente del indice QUDT 3.5.3 (sello W v003 de la ronda anterior). No se repite la busqueda y no se sustituye por M3 ni por factor alguno.

## Fuera de alcance de v003

- Los otros 49 filas con literal `Porcentaje` y las otras 2 con `Toneladas`: v003 solo publica los 5 casos con vinculo verificado; el inventario completo esta en `v002/inventario-unidades.json` (sellado).
- Compuestas, moneda, conteos, codigos y referencias indirectas: ver `v002/informe-exclusiones.md`.
