# Versionado y lanzamientos

## Dos versiones con funciones distintas

`format_version` es un entero que identifica el esquema de un documento JSON.
Permite decidir cómo leer sus campos. Se incrementa cuando cambia ese contrato;
no se incrementa por añadir evidencia que conserva el mismo esquema.

`release` identifica el corte integrado del proyecto, por ejemplo `R8` o `R9`.
Un lanzamiento puede conservar la misma versión de formato. Un archivo de
propuesta no acredita por sí mismo que ese lanzamiento ya esté instalado.

Esta convención se aplica a los nuevos paquetes que la declaran. Los documentos
históricos conservan sus formatos y campos originales; no se les añade una
versión retroactivamente.

## Evidencia y decisiones

Cada nueva integración fija sus archivos de evidencia mediante SHA-256 y un
manifiesto propio. La configuración de esa ronda fija el hash del manifiesto.
Las auditorías independientes identifican el material exacto que aceptaron.
Una corrección posterior produce otra versión de propuesta o una ronda nueva.

Los manifiestos y los informes de rondas cerradas se preservan. Los archivos
generados de uso corriente —cobertura, Turtle del portal y recibos de carga o
Studio— representan el estado actual y se respaldan antes de publicar el corte
siguiente. No deben confundirse con los snapshots de evidencia históricos.

## Unidades de conteo

Se informan por separado significados respaldados, conceptos, correspondencias
físicas, declaraciones de unidad, intervalos y relaciones jerárquicas. Añadir una
declaración de unidad a una definición existente no añade un significado ni
autoriza trasladar esa unidad a otros recursos, columnas o periodos.

El total de triples de la carga del portal y el total de Studio tienen ámbitos
distintos: Studio puede conservar ediciones ajenas al conjunto gestionado. La
sincronización verifica el delta y la conservación de esas ediciones.

## Publicación de un corte

1. Respaldar y comprobar los insumos y el estado anterior.
2. Congelar propuestas y obtener dos dictámenes independientes del material.
3. Aplicar únicamente lo aceptado con un solo escritor de archivos centrales.
4. Ejecutar la suite Python, generar RDF, validar sintaxis y SHACL y comprobar
   las consultas afectadas. La publicación de archivos y la suite se ejecutan
   en secuencia para evitar conflictos de lectura en Windows.
5. Respaldar Studio, sincronizar y verificar el grafo resultante y SHACL.
6. Publicar un informe nuevo con hashes, pruebas, delta y pendientes externos.

Una propuesta negativa también cierra un piloto: documenta qué evidencia falta
y qué permitiría reabrirlo. No produce datos ni relaciones por suposición.
