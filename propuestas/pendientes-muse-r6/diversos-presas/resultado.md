# Resultado diversos-presas, ronda 6

7 significados asignados + 1 columna presas. Decisiones: 0 proponer, 5 pendiente (significados) + 1 pendiente (columna), 2 artefacto_documental. Reglas 0, conceptos nuevos 0, vinculos 0. Sin cambios al nucleo. Las 5 columnas resueltas del contexto (3 fiebre condicionadas, 2 plantas directas) no se tocan.

## Diversos (7)

- Fiebre manchada 177/178 (huellas 4b17625c..., b5dbcdf5...): artefacto_documental. Filas repiten encabezados como valores. Matiz nuevo R6: la fila 7 genuina `des_mpo_res` es texto libre ("Municipio donde reside el caso", ejemplo "Hermosillo"), por lo que el supuesto catalogo ni siquiera aportaria dominio de codigos. Requiere fe de erratas del publicador.
- TRIMESTRE Denuncias (799f924f...): pendiente. Re-descarga del xlsx bloqueada por WAF (2026-10-23); sin valores. Requiere metodologia PROAES que defina "estrato".
- CLASIF marginacion colonia (c16feb71...): pendiente. Documento autentico nuevo: CONAPO IMU 2020 (PDF, sha 21b5e823...) documenta el atributo INEGI "clasificacion de la colonia" (Anexo B, notas 98-99, 109) como pista concreta; sin vinculo al recurso local. Requiere metodologia COESPO o verificacion web (SW6-DIV-01).
- CVOTRAS (7b439083...) / DOTRAS (738de032...): pendiente. Catalogo local re-verificado por bytes (sha 08d345e0... identico a R5): 4 hojas, sin "otras". Requiere diccionario corregido o metodologia SAGARHPA (SW6-DIV-03).
- Total_Egresos (98c73e56...): pendiente. Documento autentico nuevo: guia DGIS GIIS-B002 v5.9 (ZIP, sha eaea651e...) separa egresos de urgencias (GIIS-B014; motivoEgreso 1-7) pero es edicion 2026, fuera de la epoca local 2018-2022: agudiza la contradiccion sin curarla. Requiere aclaracion del publicador (SW6-DIV-02 como alternativa web).

## Presas (1 columna)

- `.../cat_estatal/1` Clave: pendiente. Linea nueva R6: el Inventario Nacional de Presas (CONAGUA 2015, via CENAPRED ArcGIS REST, HTTP 200) no tiene campo Clave CCCCC; sus claves son numericas (NUM/ID_CT: p. ej. Lazaro Cardenas 2983, El Novillo 3001, Oviachic 2928) en 203 registros Sonora. Tipo incompatible y sin documento que vincule NUM/ID_CT con la Clave local: aprobar por nombre o por clave nacional seria aprobar por nombre. Re-descarga del xlsx autentico bloqueada por WAF (403, 2026-10-23). Requiere nota del publicador sobre hoja y dominio (SW6-PRESAS-01 como alternativa web).

## Fe de erratas original

Revisada (`data/integracion-ronda-4/entregas/ambiguedades/resultado.md`): la "discrepancia de huella /11" fue error de transcripcion propio; cobertura registra el valor verificado. Confirmado 2026-10-23 (huella d33c36c8... presente, cobertura sha intacto vs base). No se reabre.

## Archivos

- `entrega.json` (7 significados + 1 columna, 6 fuentes, 6 pendientes DIV-P-01..05 + PRESAS-P-01)
- `solicitudes-web.json` (4 solicitudes: SW6-PRESAS-01, SW6-DIV-01/02/03)
- `evidencia/`: CONAPO_IMU_2020_urbana.pdf, DGIS_GIIS-B002-05-09_egresos-v5.9.zip, CENAPRED_inventario-presas-2015_layer43.json, ..._sonora.json
- Evidencia negativa: re-descargas portal bloqueadas por WAF (403 text/html cloudflare) 2026-10-23; HTML no conservados.
