# Cierre de brechas — significados-salud (85 IDs)

Tarea `significados-salud`. Fecha: 2026-10-24. 0 propuestas / 85 siguen pendientes.
Ningun cambio al nucleo; solo propuestas revisables en esta carpeta.

## Novedad real frente a post-R6 (no repetida)

1. DGIS Datos Abiertos DEFUN 2022: descriptor de 73 campos + 45 catalogos CSV,
   contrastados por ID contra las 32 columnas de defunciones.
2. Descriptor nacional SINAC 2020-2025 (vigencia explicita, 65 variables ID 1..64):
   31/53 variables de nacimientos con nombre exacto + descripcion + catalogo;
   22/53 sin contraparte (20 columnas D + ANOMALIACIE1/2).
3. Resultado: coherencias nuevas (2=IMSS, 3=Otro medico, 8/88 sentinelas, U071,
   sitio_ocur 1..12) e incoherencias nuevas ('4' fuera de 011..110, '997'/'9997'
   fuera de rangos, CLUES/JURISDICCION sin campo nacional). Nada promociona:
   falta la tabla del publicador columna<->campo y el codebook del recurso.

## Brecha exacta que subsiste (por grupo)

- Defunciones (32): nota del publicador que vincule el recurso 6f39fc5d con el
  campo nacional DEFUN 2022 citado por ID (tabla columna<->campo + codebook).
- Nacimientos con nombre exacto (31): nota del publicador que vincule el recurso
  46977217 con la variable IDnac citada (contenido del catalogo + tabla).
- Nacimientos sin contraparte (22): descripcion publicada de la columna D o nota
  equivalente del publicador.

## Archivos

- `entrega.json` — 85 decisiones + 9 fuentes con SHA verificado contra bytes.
- `evidencia/` — zips descargados, descriptores xlsx, catalogos csv, paginas DGIS,
  `peticiones-web.json` (al inicio) y este generador en `temporales/`.
- `listo.json` — conteos y SHAs.
