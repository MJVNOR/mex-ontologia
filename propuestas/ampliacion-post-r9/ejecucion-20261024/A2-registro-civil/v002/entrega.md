# A2 — Registro civil (v002)

Par: `1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5`.
Rol: A2-registro-civil. Modelo: `opencode/deepseek-v4.1-flash-free` (Free; v001 Muse queda intacta).
Resultado: **BLOQUEADO** — sin comparación de volúmenes ni join.

v002 reproduce el análisis de v001 sin cambiar veredicto, cifras ni ejes.
Solo corrige dos hallazgos menores del dictamen `R-documental/v001`.

## Correcciones

| ID | Antes | Después |
|----|-------|---------|
| H-02 | MD: 10 Matrimonios / 15 Nacimientos; JSON: 11 / 16 sin desglose | 10 recursos de datos + 1 diccionario = 11; 15 + 1 = 16 |
| H-04 | Fuentes sin SHA256 de archivo completo | SHA256 y bytes de las 4 fuentes, calculados por código |
| B-A2-11 | Cita "Diagnostico" sin tilde | Cita literal "Diagnóstico de muestra; ..." |
| B-A2-12 | "Anio-Mes de registro" como variable única | "Año de registro" y "Mes de registro" separadas (Matrimonios incluye "Dia de registro") |

## Fuentes ancladas (H-04)

| Fuente | Bytes | SHA256 |
|--------|-------|--------|
| `reports/catalogo-perfil.json` | 227576 | `aae23b2eb8f8e37cbee18d86c0cac7c73f0899f02fbd417bc90d01a8fd54fc43` |
| `data/portal/contenido-inspeccion.json` | 2652648 | `61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb` |
| `data/portal/oportunidades-cruce.json` | 9645149 | `40f107d5cf9c11ce937073ac2f7b5b0e3c9db8c342f7414cecb0f0744e0d0c14` |
| `data/portal/lote-cruces/validacion-lote.json` | 1478239 | `9031b875b1bf7873722f74847abbbce9b87201415f43788f60be1a75b50ede19` |

## Bloqueo (sin cambios respecto de v001)

1. Grano: evento matrimonial vs agregado mensual de nacimientos.
2. Unicidad/cardinalidad: muestras n=100 no demuestran universo ni cobertura.
3. Nacimientos: `total ≠ hombres+mujeres` en 5/6 pruebas; meses faltantes.
4. Ámbito de registro, sin residencia ni correspondencia de códigos acreditada.
5. Poblaciones distintas; sin causalidad ni tasas.

Ficha de 8 ejes: `A2-pregunta-ficha.md` (entrega separada, sin datos nuevos).
Detalle máquina: `resultados.json`.

## Reproducir y sellar

```powershell
.venv/Scripts/python.exe propuestas/ampliacion-post-r9/ejecucion-20261024/A2-registro-civil/v002/scripts/analizar.py
.venv/Scripts/python.exe -B -m unittest discover -s propuestas/ampliacion-post-r9/ejecucion-20261024/A2-registro-civil/v002/tests
.venv/Scripts/python.exe propuestas/ampliacion-post-r9/ejecucion-20261024/A2-registro-civil/v002/scripts/sellar.py
```

`sello.json` fija SHA256 de cada archivo; `sello.sha256` fija el del sello.
El sello no se hashea a sí mismo y no incluye `__pycache__` ni `.pyc`.
Sin red, sin grafo, sin joins, sin cambios en IRI/Gemma/manifiestos R1–R9 ni raíz.
