# Selector de modelos de Studio

El chat incluye **Cambiar modelo**. **Actualizar** consulta el catálogo de la API configurada; **Comprobar acceso** envía una solicitud breve de texto sin datos de la ontología; **Usar modelo** cambia el proveedor de las próximas preguntas. **Volver a Gemma** restaura el predeterminado.

El predeterminado sigue siendo `gemma-4-31b-it`, tomado del `.env` existente. La selección solo dura mientras Studio está abierto: no modifica credenciales ni el `.env`. El cambio conserva la conversación visible y reinicia la historia interna del proveedor. El presupuesto de recuperación y la clave de caché usan el modelo seleccionado. No hay sustitución automática cuando un modelo falla.

Las operaciones se serializan con las preguntas del chat. El selector y el envío quedan bloqueados mientras se comprueba o cambia un modelo. Las credenciales permanecen en el proceso del agente; el frontend recibe identificadores y estados, nunca la clave. Una respuesta HTTP fallida conserva el modelo activo y no incorpora el cuerpo del error del proveedor al selector.

## Catálogo y comprobación de 2026-10-24

La API anunció 60 modelos. Se filtraron 19 candidatos de texto Gemma/Gemini; se excluyeron identificadores de imagen, audio, TTS, embeddings, live, robótica y otras modalidades incompatibles con este chat. El filtro identifica candidatos: la prueba confirma una respuesta breve de texto, no llamadas a herramientas ni disponibilidad futura.

Respondieron con texto (HTTP 200):

- `gemma-4-26b-a4b-it`
- `gemini-flash-lite-latest`
- `gemini-3-flash-preview`
- `gemini-3.1-flash-lite-preview`
- `gemini-3.1-flash-lite`
- `gemini-3.5-flash`
- `gemini-3.5-flash-lite`
- `gemini-3.6-flash`

El predeterminado `gemma-4-31b-it` devolvió HTTP 500 en esa prueba; se conserva como predeterminado por petición del usuario. Hubo otros resultados HTTP 404, 429, 503 y dos plazos agotados. Es una instantánea de solicitudes mínimas con esta clave, sin acreditar permisos permanentes o capacidad de responder preguntas complejas. Los estados se vuelven a comprobar desde la aplicación; no se presentan estos resultados históricos como disponibilidad actual garantizada.

Resultados completos: [modelos-studio.json](../reports/modelos-studio.json).

Para repetir las 19 solicitudes (consume cuota):

```powershell
.venv/Scripts/python.exe scripts/comprobar_modelos_studio.py
```

Fuentes modificadas en `C:/Users/marti/Documents/open-ontologies/studio`: `src/components/ModelSelector.tsx`, `src/components/ChatPanel.tsx`, `src/hooks/useChat.ts`, `src-tauri/src/chat.rs`, `src-tauri/src/lib.rs`, `src-tauri/sidecars/agent/index.ts` y `src-tauri/sidecars/agent/model-catalog.ts`. Pruebas nuevas: catálogo de modelos y puente de estado del chat.

## Instalación y verificación

Compilación nativa release instalada en la ruta de `scripts/studio-gemini.json`, con respaldo del ejecutable, sidecar, grafo activo y texto del chat previo. Se verificó igualdad de conjuntos RDF entre el respaldo del motor y el archivo cargado. Tras reiniciar, Studio mantiene 323,014 triples, 57 clases y 210 propiedades.

Pasaron 65 pruebas de frontend y 69 del agente (una prueba existente omitida), compilación TypeScript, build del agente y compilación nativa; el detector de interfaz no encontró incidencias. En la aplicación instalada se consultaron los 19 candidatos, se comprobó una respuesta breve de `gemma-4-26b-a4b-it`, se activó ese modelo con confirmación del agente y se regresó a `gemma-4-31b-it`. No se envió una pregunta compleja al modelo alternativo ni se acreditaron llamadas a herramientas.

Evidencia: [instalación](../reports/studio-modelos-instalacion.json) y [estados de la interfaz](../reports/studio-modelos-ui.txt).
