# Cómo revertir el patch

Desde la raíz del proyecto:

```powershell
git apply -R propuestas/ronda-3/agente-13-calificadores/patch/test_semantica.patch
git apply -R propuestas/ronda-3/agente-13-calificadores/patch/semantica_ttl.patch
git apply -R propuestas/ronda-3/agente-13-calificadores/patch/consolidar_semantica.patch
uv run python -m unittest tests.test_semantica
```

La reversión restaura los 3 archivos centrales a su estado previo
(SHA originales en `fuente/huellas.json`, sección `entradas`).
La carpeta `propuestas/ronda-3/agente-13-calificadores/` se conserva intacta
como evidencia; no requiere borrado.
