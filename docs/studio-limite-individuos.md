# Corrección del límite de individuos de Studio

El árbol 2D tenía un `LIMIT 2000` global en la consulta de individuos. Esto recortaba la colección antes de crear las ramas de clases y aplicar la búsqueda: algunas clases parecían vacías y la búsqueda no alcanzaba los individuos omitidos.

La consulta completa está ahora en `C:/Users/marti/Documents/open-ontologies/studio/src/lib/tree-queries.ts`, utilizada por `TreeView.tsx`. Se eliminó el límite sin sustituirlo por otro número. La consulta también admite instancias de tipos sin declaración explícita `owl:Class`, manteniendo los criterios del contador de individuos del motor. El árbol ya virtualiza las filas visibles, por lo que no crea miles de elementos DOM al expandir una clase.

## Verificación

- Consulta anterior: 2,000 individuos recuperados.
- Consulta corregida: 15,904 individuos únicos, coincidentes con el conjunto calculado desde el respaldo del grafo vivo.
- Se reciben 16,000 filas por los tipos y etiquetas múltiples; las identidades se mantienen únicas en el árbol.
- Consulta completa medida en aproximadamente 0.11 segundos en esta ejecución; no es una garantía para grafos de cualquier tamaño.
- Prueba adicional con 2,505 entidades, tipos sin declaración de clase, etiquetas multilingües y un individuo con varios tipos. Verifica que se conserva la entidad después de la posición 2,000 y se excluyen declaraciones de clases, propiedades y ontología.
- 56 pruebas de Studio aprobadas. TypeScript, Vite y la compilación nativa Tauri completados.
- Comprobación visual después de actualizar la instalación: el árbol 2D muestra `15904 individuals`, la rama de columnas muestra 6,585 y la de oportunidades muestra 3,916. El motor conserva los 154,878 triples.

El cambio conserva los filtros, selección, búsqueda, etiquetas e identidades por URI de la vista existente. No cambia la ontología ni las reglas semánticas.

Evidencia y respaldo: `reports/studio-limite-individuos.json` y la ruta de respaldo que registra. Para repetir la comprobación con Studio abierto:

```powershell
uv run python scripts/comprobar_limite_studio.py
```

El script consulta el motor local, guarda un respaldo y comprueba identidades, no solo el número total. La aplicación instalada se actualizó con el instalador NSIS generado desde las fuentes locales, preservando los demás cambios existentes. Los archivos fuente y de compilación no se restablecieron.
