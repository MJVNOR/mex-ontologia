"""Genera entrega.json/md + congelada.json de T-pruebas v001.

Todos los SHA-256 se calculan aquí por código; nada se tipea a mano.
Solo escribe dentro de T-pruebas/v001/. Solo lee producción.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

V1 = Path(__file__).resolve().parent
ROOT = next(p for p in V1.parents if (p / "ontologia/semantica.json").exists())
T = ROOT / "propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path):
    return Path(path).relative_to(ROOT).as_posix()


tests = sorted((V1 / "codigo" / "tests").glob("test_*.py"))
archivos = [{"ruta": rel(p), "sha256": sha(p)} for p in tests]

# Pins de base leída (solo lectura; verifica el punto de partida R7).
base_rels = [
    "ontologia/semantica.json",
    "data/semantica/cobertura.json",
    "ontologia/revision-ronda-7.json",
    "data/integracion-ronda-7/manifiesto.json",
    "data/integracion-ronda-7/aceptadas.json",
    "data/integracion-ronda-7/delta.json",
    "reports/ronda-7.json",
    "propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/asignacion.json",
]
base = {r: sha(ROOT / r) for r in base_rels}

entrega = {
    "rol": "T-pruebas",
    "version": "v001",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "modelo": "opencode-go/muse-spark-1.3-contributor",
    "mcp": "nativo OpenCode; sin Obscura (uso exclusivo de W-web); sin Gemma/chat",
    "casos_asignados": 0,
    "decisiones": [],
    "afirmacion_exacta_acotada": (
        "Los 6 fallos de propuestas/suite-r7-inicial.log (142 pruebas) se deben "
        "a expectativas pre-R7 que no contemplan el delta aprobado R7 "
        "(31 significados + 3 vínculos; 1392+31=1423 respaldadas, 152-28=124 fuera, "
        "19-3=16 candidatas, 4475+3=4478 revisadas). Producción verifica íntegro "
        "(manifiestos, doble auditoría A+B con aceptadas_sha256 pinnado, base exacta, "
        "materialización fiel): no se propone ningún cambio en scripts/tests/ontologia/data. "
        "Se proponen copias corregidas de los 4 tests con expectativas derivadas de "
        "manifiestos (sin hardcodear conteos observados) + test_ronda_7.py "
        "(12 pruebas: integridad, aprobación SHA, base exacta, deltas cruzados, "
        "materialización, scope, 4 negativas, gancho R8). Staging: 154 pruebas OK."
    ),
    "pruebas_verificables": {
        "comando": "uv run python -m unittest discover -s propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests -t propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests",
        "total": 154,
        "resultado": "OK",
        "fallos_iniciales_produccion": 6,
        "nota": "Ejecución en staging (copias bajo v001/codigo/tests); producción solo leída, no instalada ni modificada.",
    },
    "diagnostico_fallos": [
        "test_cobertura_integrada (3): conteos/promociones calculan solo deltas R4/R5; faltan R6 (sin reglas, verificado) y R7 (28 fuera + 3 candidatas -> respaldadas, estados previos derivados de base post-R4 salvo promoción R4/R5).",
        "test_integracion_agentes/test_ronda_2/test_ronda_3_integrada (3): esperados de revisadas suman solo r6n; falta r7n derivado de aceptadas.json validado (4475+3=4478).",
        "Causa común: suite anterior a R7. reports/ronda-7.md ya anticipa adaptadores de conteos; producción íntegra, tests desactualizados.",
    ],
    "archivos_codigo": archivos,
    "cambios_produccion_propuestos": "Ninguno en scripts/ontologia/data. Solo tests (ver instrucciones_aplicacion); test_ronda_7.py es alta nueva.",
    "instrucciones_aplicacion": [
        "1. Auditar esta v001 con dos revisores independientes (código + pruebas).",
        "2. Tras aprobar: copiar v001/codigo/tests/test_cobertura_integrada.py, test_integracion_agentes.py, test_ronda_2.py y test_ronda_3_integrada.py sobre tests/ (sobrescriben expectativas; aserciones históricas preservadas).",
        "3. Añadir v001/codigo/tests/test_ronda_7.py como tests/test_ronda_7.py (alta nueva, sin colisiones).",
        "4. El resto de copias son idénticas a producción salvo resolución de raíz por marcador (equivalente en ubicación final); no requieren copia.",
        "5. Verificar: uv run python -m unittest discover -s tests -t . (esperado: todo OK).",
        "6. No instalar ni modificar scripts/, ontologia/, data/, docs/ ni reports/ con este pase.",
    ],
    "gancho_r8": "Expectativas por deltas aprobados de manifiestos (aceptadas.json validados), nunca vivo contra sí mismo. Si R8 añade reglas/vínculos (28 vínculos previstos), extender el mismo patrón con integrar_ronda_8; test_r8_hook_por_deltas_aprobados falla a propósito hasta entonces.",
    "base_sha256": base,
    "limites": [
        "Alcance T-pruebas: suite Python; no acredita significados, vigencias, joins ni identidades.",
        "Sin navegador Obscura (exclusivo W-web); sin peticiones-web.json (sin pista primaria nueva: todo el insumo es local).",
        "Sin Gemma/chat; sin mensajes externos; sin puentes ni CLI OpenCode.",
        "Correcciones futuras en v002+; esta v001 congelada no se edita.",
    ],
}

(V1 / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = [
    "# T-pruebas v001 — suite R7",
    "",
    f"Fecha UTC: {entrega['fecha_utc']}",
    "Modelo: `opencode-go/muse-spark-1.3-contributor`, MCP nativo OpenCode. Sin Gemma, sin Obscura, sin contactos externos.",
    "",
    "## Casos asignados",
    "",
    "Asignación con `casos: []`: cero ids, cero decisiones (una decisión exacta por cada id asignado).",
    "",
    "## Afirmación exacta acotada",
    "",
    entrega["afirmacion_exacta_acotada"],
    "",
    "## Pruebas verificables",
    "",
    f"- Staging: `{entrega['pruebas_verificables']['comando']}` → {entrega['pruebas_verificables']['total']} pruebas OK.",
    "- Producción solo leída; nada instalado ni modificado fuera de `T-pruebas/`.",
    "",
    "## Diagnóstico de los 6 fallos iniciales",
    "",
    *[f"- {d}" for d in entrega["diagnostico_fallos"]],
    "",
    "## Instrucciones de aplicación",
    "",
    *[f"- {s}" for s in entrega["instrucciones_aplicacion"]],
    "",
    "## Archivos de código (SHA-256 calculados por `generar-entrega.py`)",
    "",
    *[f"- `{a['ruta']}` `{a['sha256']}`" for a in archivos],
    "",
    "## Base leída (punto de partida R7)",
    "",
    *[f"- `{r}` `{h}`" for r, h in base.items()],
    "",
    "## Gancho R8",
    "",
    entrega["gancho_r8"],
    "",
]
(V1 / "entrega.md").write_text("\n".join(md), encoding="utf-8")

congelada = {
    "rol": "T-pruebas",
    "version": "v001",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "entrega_sha256": sha(V1 / "entrega.json"),
    "entrega_md_sha256": sha(V1 / "entrega.md"),
    "archivos": {a["ruta"]: a["sha256"] for a in archivos},
    "generador_sha256": sha(V1 / "generar-entrega.py"),
    "nota": "Congelada: no editar. Correcciones solo en v002+.",
}
(V1 / "congelada.json").write_text(json.dumps(congelada, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
# El sha del generador fijado arriba es previo a esta línea solo si el
# generador no cambió durante la corrida (no se autotoca): se cumple.
print(json.dumps({"entrega": congelada["entrega_sha256"], "archivos": len(archivos)}, ensure_ascii=False))
