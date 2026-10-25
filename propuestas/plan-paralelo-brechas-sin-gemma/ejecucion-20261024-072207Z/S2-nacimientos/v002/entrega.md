# S2-nacimientos v002 — reinterpretación explícita para auditores A/B (v001 intacta)

v001 cerró 53 brechas externas por falta de tabla local del publicador.
v002 reevalúa con UNA pista nueva real: el contenido del codebook nacional
SINAC 2020-2023 (zip DGIS, sha 9c7dcd52…, primera descarga del expediente;
rondas previas solo conocían nombres de catálogos, no su contenido).

Prueba por tiers (separables: el auditor puede aceptar A1 y rechazar el resto):
- A1 (17 IDs): el código entero local está en el catálogo nacional y la
  etiqueta D del mismo renglón es idéntica (normalizada) a la descripción
  nacional. Coincidencia textual conjunta en 10 catálogos independientes →
  el extracto se decodificó con ESTE codebook. La tabla local queda determinada.
- A2 (6 IDs, sin catálogo nacional): identificador exacto + sistema + edición
  + tipo compatible, en la misma hoja ya probada por A1.
- A3 (5 IDs, geo/CLUES): código local verificado existente/vigente en el
  catálogo fechado (26=SONORA; 26/055 SLRC VIGENTE; 26/055/0001 SLRC;
  SRSMP000314 EN OPERACION). CLUESCERTIFICA sin ejemplo local (límite).
- A4 (2 IDs): descriptor + CIE-10 (columna de catálogo + DOF CEN) + 0000
  corroborado por la columna hermana. DIAGNOSTICOS sin archivo en el zip (límite).
- A5 (1 ID, TIEMPOTRASLADO): significado del descriptor; duración codificada
  como Hora, formato no especificado (límite, no bloquea el significado).

Resultado: 31 propuesta_para_auditar, 22 brecha_externa.
Las 22 mantienen desajuste estructural concreto, no solo falta de tabla:
20 columnas `*D` derivadas sin variable nacional y sin regla de decodificación
publicada; 2 ANOMALIACIE* inexistentes en el instrumento (el modelo nacional
codifica con CODIGOCIEANOMALIA/0000).

Diferencias declaradas (no ocultan nada): entero local vs texto nacional con
cero inicial ('01' vs 1, mapeo biyectivo); edición por título/rango DGIS sin
acta separada; DIAGNOSTICOS ausente del zip; sin mención Sonora exigida —
ámbito probado por consistencia. Igualdad de valores sola no se usa como prueba.
