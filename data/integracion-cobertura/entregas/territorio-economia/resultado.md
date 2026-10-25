# territorio-economia — cobertura-muse-20261023

Decisiones: 534 (proponer 482, pendiente 52). Reglas: 482. Conceptos nuevos: 458.

Base: 103 conceptos, 232 respaldadas, 23 candidatas iniciales, 836 revisadas, 118 candidatas: preservadas (sin correspondencias nuevas).

## Revision manual vs automatizacion

Manual: lectura literal de cada regla y definicion; 5 conceptos IMN separados de IM;
6 representaciones a no_especificada; limites de reconstruida-vs-proyeccion, conjunto-poblacion,
ejemplo incoherente y contradicciones nombre-descripcion; 10 calificadores DDR conservados.

Automatico: huellas manifiesto, particion 468+66 sin solapes, literales, filas por IRI,
interpretacion() con positivos y negativos, respaldo de unidades/objetos, padres validos.

## Pendientes

Quedan 52 pendientes (49 heredados A10 + 3 A3) para aclaracion del publicador.

## Devolucion integrador + auditor A11 (cambios precisos)

1. Huella a nivel regla: las 482 reglas traen `huella_fila_diccionario` top-level,
   igual a evidencia anidada, decision y cobertura (verificado 482/482; sin re-hasheos).
2. Renombre proyeccion: 24 conceptos `poblacion-proyectada-edad-*` y
   `poblacion-total-proyectada-*` pasan a `poblacion-reconstruida-ajustada-edad-*`,
   `poblacion-total-reconstruida-ajustada-quinquenios`,
   `poblacion-total-edad-*-grandes` y `suma-poblacion-total-grandes-grupos`;
   etiquetas con literal ('Poblacion reconstruida y ajustada...' o literal exacto
   del conjunto). Reglas y decisiones actualizadas; sin colisiones ni padres rotos.
3. Limite explicito en 48 reglas de proyecciones: no se homologa
   reconstruida/ajustada con proyeccion; la mencion viene solo del titulo del conjunto.
4. IM vs IMN ya separados en 5 niveles (verificado por test); año 2020 solo con
   respaldo literal o de conjunto (colonia IM/GM/IMN sin año; prueba dedicada).
5. Clave presa: broader comun sin identidad interfuente; 4 representaciones
   nombre->no_especificada; peso/moneda solo con respaldo.
Particion 534 y 10 calificadores DDR intactos.
