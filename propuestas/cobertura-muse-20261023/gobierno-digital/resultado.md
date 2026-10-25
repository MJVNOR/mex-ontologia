# Gobierno digital — entrega cobertura-muse-20261023

Especialista (243 definiciones del agente 9, Diagnóstico del Entorno Digital, APE Sonora).
Insumos verificados contra `fuentes/manifiesto.json`: 17/17 copias congeladas y 6/6
insumos centrales por SHA-256. Base: copia congelada `fuentes/agente-9-gobierno-digital/`.

## Conteos (recalculados desde contenido)

243 decisiones (121 proponer, 122 pendiente), 121 reglas `r3a9-001…r3a9-121`,
86 conceptos nuevos, 0 reutilizados. 70 reglas con calificador formal
`{"instrumento": <tema de encuesta>}` (conceptos compartidos entre instrumentos pares);
51 reglas sin clave `calificador` (devolución del integrador: la clave solo existe con dict no vacío str->str; verificado con validar_calificador real). 0 correspondencias columna-variable, 0 sameAs/exactMatch.

## Verificación propia

`scripts/verificar_entrega.py` (TODO OK): partición exacta 243/243, huellas e IRIs
recalculadas, 121/121 positivos y 5/5 negativos con `interpretacion()` (funciones puras),
sin colisión con las 116 reglas centrales (se preservan 103 conceptos, 232 respaldadas,
23 candidatas, 836/118 correspondencias), unidades con respaldo literal, nombres neutros,
fusión existencia+nombre en `unidad-coordinadora-tic`, acotación completa por definición,
`pendientes.json` consistente (122) y disjunción con hermanos congelados.

## Correcciones integrador+auditor aplicadas

- Revertida la fusión P8/P9: `existencia-unidad-coordinadora-tic` (P8, Si/No) y
  `nombre-unidad-coordinadora-tic` (P9, nombre) son conceptos estrechos distintos;
  la existencia es medida de atributo, no identificador nominal. Sin fusiones
  existencia/conteo/nombre por compartir objeto (verificador lo bloquea: un concepto,
  una representación).
- 3 contradicciones tipo<->ejemplo (P11/P12 infra, P7 presupuesto) con representación
  `no_especificada`, atributo solo-literal y límite técnico explícito; tipo+ejemplo
  capturados en evidencia sin afirmar valores/montos.

## Correcciones sobre el trabajo previo

Dos etiquetas ajustadas al literal ("Acciones o estrategias…", "Comité o cuerpo colegiado…");
límites de alcance del "etc." en 4 reglas; calificador de instrumento donde procede;
esquema `entrega.json` con `huella_fila_diccionario` y `limites` por regla.

## Revisión manual vs automatización

Manual: lectura literal individual de cada definición; veredictos, motivos, conceptos y
calificadores decididos por persona (nada deducido por regex de nombres).
Automático: generador determinista + verificador que recalcula y simula; no propone nada.

## Archivos

`entrega.json`, `pendientes.json` (122 con motivo y faltante), `resultado.md`,
`scripts/generar_entrega.py`, `scripts/verificar_entrega.py`, `listo.json`.
No se tocó nada fuera de esta carpeta; no se ejecutó la suite central.
