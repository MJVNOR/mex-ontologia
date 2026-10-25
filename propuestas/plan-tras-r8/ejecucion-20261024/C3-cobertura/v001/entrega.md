# C3 Cobertura R8 - auditoria derivada v001

Estado: `auditoria_derivada` (sin evidencia para integrar, sin propuesta de cambio central).

## Reconciliacion (verificada por codigo)

- Columnas: 5523 = 4506 documental_revisada + 17 candidata_por_nombre + 833 sin_definicion_coincidente + 154 definicion_sin_interpretacion_compartida + 13 sin_diccionario_en_conjunto.
- Con correspondencia: 4523 = 4506 + 17 = len(cobertura.correspondencias).
- Definiciones con nombre: 1563 = 1423 respaldada + 124 fuera_del_nucleo + 16 candidata; + 7 filas sin nombre (unidad aparte).
- Materializadas (con `iri`): 1442 = 1423 + 16 + 3. Los 3 con `iri` pero `fuera_del_nucleo_actual` son: filas corruptas 177/178 (huellas 4b17625c/b5dbcdf5, des_mpo_res) y Total_Egresos (huella 98c73e56, observacion egresos-descripcion-urgencias). Sin `iri`: 121 = 124 - 3. La diferencia 1442 - (1423+16) = 3 se explica por regla de materializacion (`sum('iri' in v)`), no por significados nuevos.
- 154 columnas != 154 definiciones: 154 es estado a nivel columna; a nivel definicion hay 140 variables pendientes = 124 + 16 (motivos 104 descripcion vacia + 34 dominio/medida sin regla + 2 pista sin interpretacion) = 138 significados reales + 2 headers corruptos.

## Cinco observaciones (recurso/columna en totales-cruces-observaciones.json)

1. egresos-descripcion-urgencias - recurso ad6f77b8 / Total_Egresos (columna candidata_por_nombre; variable fuera_del_nucleo con iri).
2. municipio-formato-ejemplo - recurso 046c2f52 / CVE_MUN (documental_revisada; significado municipal documentado, composicion del codigo no resuelta).
3. fecha-ejemplo-numerico - recurso c07fe117 / Fecha (documental_revisada; codificacion de fecha no validada).
4. anio-nacimientos-2024 - recurso ffca84a8 / anio (sin_definicion_coincidente; no extender alias de 2022).
5. anio-divorcios-2023 - recurso f05dfd7e / anio_registro (documental_revisada; alias explicito pendiente para este recurso).

## Archivos

- `matriz-columnas-5523.csv`: 5523 filas (columna_iri, recurso, campo, estado, n_correspondencias, n_definiciones, fuente_esquema), sin repetir prosa.
- `totales-cruces-observaciones.json`: totales, cruces (1 des_mpo_res sin resolver, 16 con recurso, 6 condiciones, 389 recursos con revision explicita de 396) y las 5 observaciones con localizadores.
- `congelada.json`: SHA-256 calculados por codigo.

## Limites y aceptacion

Gemma excluido, sin contactos externos, sin promocion por nombre (Puerta 1), sin tocar nucleo/Studio, sin busquedas genericas repetidas. Aceptar si las igualdades 5523/4523/1442 verifican, 154 no se presenta como definiciones, y cada observacion trae recurso/columna/localizador.
