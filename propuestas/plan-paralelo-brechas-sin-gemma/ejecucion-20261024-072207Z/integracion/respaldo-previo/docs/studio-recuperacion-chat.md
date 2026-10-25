# Correspondencias semánticas en el chat de Studio

El chat recuperaba un vecindario de 16 anclas y hasta 120 relaciones por recorrido. Las correspondencias calificadas apuntan hacia la variable mediante `variableDestino`; encontrar la variable o su definición no garantizaba recuperar todos esos nodos ni sus estados. El modelo había afirmado que no existía ninguna correspondencia revisada, aunque sí estaban cargadas.

## Corrección local

En `../open-ontologies/studio/src-tauri/sidecars/agent/graphrag.ts`, la recuperación identifica las variables por `nombreVariableLocal` y consulta explícitamente sus correspondencias entrantes. Descubre el espacio de nombres del vocabulario a partir del grafo.

La consulta lee todas las páginas, de 200 filas cada una. El tamaño de página no limita el número total de correspondencias recuperadas. Cuenta por variable los estados distintos y sus nodos de correspondencia, sin deducir el estado por un enlace antiguo `definicionCandidata`.

Para controlar el contexto enviado al modelo, muestra hasta 80 registros por vocabulario, priorizando los revisados. Si hay más registros, declara que los ejemplos son parciales; los conteos siguen incluyendo todas las páginas. Adjunta definiciones originales, fuentes y evidencia de las columnas y de los mapeos revisados mostrados. El vecindario general conserva sus límites y se identifica expresamente como parcial.

El prompt distingue `estadoSemantico` de la variable y `estadoCorrespondencia` del enlace columna/variable. Prohíbe interpretar «no recuperado» como «no existe». Una afirmación de ausencia requiere una consulta marcada completa para ese alcance. El caché existente incorpora contexto y prompt, por lo que la nueva evidencia invalida las respuestas anteriores.

El componente JavaScript se compila con `npm run build` en `studio/src-tauri/sidecars/agent` y se instala en el `sidecars/agent/dist/index.js` de la instalación local. Se respalda la versión anterior y se reinicia Studio; no requiere cambiar la ontología ni recompilar el ejecutable nativo.

## Comprobación reproducible

Con Studio abierto y su motor en el puerto 8137:

```powershell
node --experimental-strip-types scripts/comprobar_recuperacion_chat.mjs
```

Para comprobar también la respuesta del modelo configurado en Studio (realiza una petición a ese proveedor):

```powershell
node --experimental-strip-types scripts/comprobar_recuperacion_chat.mjs --model
```

La prueba lee las credenciales desde la configuración existente sin imprimirlas. Los resultados quedan en `reports/chat-recuperacion.json`, el contexto en `reports/chat-recuperacion-contexto.txt` y la respuesta en `reports/chat-respuesta-comprobada.md`.

La comprobación sobre el grafo activo encuentra 10 correspondencias para cada variable: nueve `candidata_por_nombre` y una `documental_revisada`. Las revisadas corresponden a Matrimonios 2022 y Defunciones 2022. Verifica también las descripciones originales «Año de registro» y «Año en el que fallecio» y las URL de sus diccionarios.

Las pruebas automatizadas del componente incluyen 202 registros, con el único revisado en la segunda página; comprueban que el conteo sea completo y que aparezca entre los ejemplos. También comprueban que un error de consulta no se convierta en evidencia vacía.

Este cambio corrige la recuperación de las correspondencias de variables nombradas. No convierte la recuperación general del chat en una consulta exhaustiva de todo el grafo ni garantiza todas las respuestas futuras del modelo.
