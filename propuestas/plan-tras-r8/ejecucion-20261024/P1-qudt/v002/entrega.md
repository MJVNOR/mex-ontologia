# P1-QUDT v002 — propuesta_para_auditar (Q1/Q3) + Q2 negativa

v001 preservada. Q1→`http://qudt.org/vocab/unit/MilliM`, Q3→`http://qudt.org/vocab/unit/HA` (HTTP canónico verificado por W v002). Q2 sin vínculo (HectoM3 404/ausente índice; sin M3 ni factor).

Modelo mínimo en `vocabulario.ttl` (términos nuevos, sin rename): UnidadDeclarada, variableDocumentada, definicionFuente, conjuntoFuente=datasetUUID, diccionarioFuente=resourceUUID, unidadLiteral, unidadQudt, estadoPropuesta, motivoNegativo, evidenciaNormativa.

Consultas: Q1=2, Q2=1, Q3=5 filas (rdflib existente). Sello W v002 pendiente: SHAs normativos registrados como observados; hash final se fija contra sello W.
