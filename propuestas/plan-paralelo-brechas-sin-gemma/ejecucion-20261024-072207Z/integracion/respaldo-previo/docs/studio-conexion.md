# Comprobación del motor para Open Ontologies Studio

**Actualización:** Studio ya fue compilado, instalado y abierto con el catálogo. La incompatibilidad del lector descrita abajo se corrigió en la copia local de Studio. Ver [estado de instalación y ajustes](studio-instalacion.md). El resto de este documento conserva el diagnóstico inicial contra el lector original del repositorio.

Se probó el ejecutable descargado contra los puntos de conexión usados por el código actual de Studio. Esta es una prueba de integración del motor, no una confirmación de que se haya instalado o abierto la interfaz Tauri.

## Resultado

- El servidor nativo inicia en `127.0.0.1:8137`.
- `/api/load` carga el modelo y los datos desde los archivos locales.
- `/api/stats` devuelve 8,231 triples.
- `/api/query` permite comprobar los 89 conjuntos y 486 recursos.
- `/mcp` acepta inicialización, lista herramientas y permite una consulta con `onto_query`.
- Hay incompatibilidad entre la respuesta REST del ejecutable probado y el lector de resultados del Studio actual.

Respuesta observada en el motor:

```json
{"results": [{"n": "\"89\"^^<http://www.w3.org/2001/XMLSchema#integer>"}], "variables": ["n"]}
```

El lector `rows()` de `studio/src/lib/live-source.ts` espera la estructura SPARQL JSON `results.bindings`, con `value` dentro de cada término. Al recibir el formato anterior, devuelve una lista vacía; por tanto una conexión HTTP exitosa no garantiza que Studio muestre el catálogo.

## Alcance de la vista nativa

La consulta de clases de Studio encuentra una sola clase propia distinta (`mex:RecursoCatalogado`), repetida por las dos ramas de su UNION. Encuentra una relación de subclase hacia `rdfs:Resource`. Sus consultas actuales no seleccionan las instancias de conjuntos, organizaciones ni recursos.

Por tanto, aun resolviendo el formato de respuesta, esa proyección de la vista no mostraría automáticamente las relaciones entre las entidades del catálogo. No deben reclasificarse los conjuntos como clases OWL solo para hacerlos aparecer.

## Próximo trabajo para usar Studio

1. Preparar la aplicación nativa de Studio en Windows.
2. Alinear el lector de respuestas con el formato que devuelve la versión del motor, o elegir versiones cuya compatibilidad esté comprobada.
3. Configurar una proyección de entidades y relaciones del catálogo en el Studio si se requiere ver sus instancias.
4. Cargar los archivos del proyecto y comprobar la interfaz real. El motor de Studio inicia su propio proceso; el almacén del proyecto no queda conectado automáticamente.

No se modificó código de Studio, no se instaló la interfaz y no se dejó un servidor en segundo plano. La comprobación usa un proceso propio y almacenamiento en memoria; lo cierra al terminar.

## Repetir la prueba

```powershell
uv run python scripts/comprobar_studio.py
```

El puerto 8137 debe estar libre; el script no termina procesos ajenos para liberarlo. Las respuestas se guardan en `reports/studio-conexion.json` y el registro del motor en `reports/studio-motor.log`.

## Código oficial revisado

- https://github.com/fabio-rovai/open-ontologies/blob/main/studio/src/lib/live-source.ts
- https://github.com/fabio-rovai/open-ontologies/blob/main/studio/src/lib/mcp-client.ts
- https://github.com/fabio-rovai/open-ontologies/blob/main/studio/src-tauri/src/engine.rs
- https://github.com/fabio-rovai/open-ontologies/blob/main/docs/windows.md
