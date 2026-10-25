"""Genera entrega.json/md + congelada.json de T-pruebas v002.

Todos los SHA-256 se calculan aquí por código; nada se tipea a mano.
Solo escribe dentro de T-pruebas/v002/. Solo lee producción. v001 intacta.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

V2 = Path(__file__).resolve().parent
ROOT = next(p for p in V2.parents if (p / "ontologia/semantica.json").exists())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path):
    return Path(path).relative_to(ROOT).as_posix()


tests = sorted((V2 / "codigo" / "tests").glob("test_*.py"))
assert [p.name for p in tests] == [
    "test_cobertura_integrada.py",
    "test_integracion_agentes.py",
    "test_ronda_2.py",
    "test_ronda_3_integrada.py",
    "test_ronda_7.py",
], "v002 contiene solo los 5 archivos finales"
archivos = [{"ruta": rel(p), "sha256": sha(p)} for p in tests]

base_rels = [
    "ontologia/semantica.json",
    "data/semantica/cobertura.json",
    "ontologia/revision-ronda-7.json",
    "data/integracion-ronda-7/manifiesto.json",
    "data/integracion-ronda-7/aceptadas.json",
    "data/integracion-ronda-7/delta.json",
    "data/integracion-ronda-7/base-semantica.json",
    "reports/ronda-7.json",
    "propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/asignacion.json",
    "propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/congelada.json",
]
base = {r: sha(ROOT / r) for r in base_rels}

entrega = {
    "rol": "T-pruebas",
    "version": "v002",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "modelo": "opencode-go/muse-spark-1.3-contributor",
    "mcp": "nativo OpenCode; sin Obscura (exclusivo W-web); sin Gemma/chat",
    "casos_asignados": 0,
    "decisiones": [],
    "afirmacion_exacta_acotada": (
        "v002 preserva v001 y hace los 5 tests finales compatibles con R8 "
        "(28 vínculos M1/M2, 0 reglas, 0 conceptos) por deltas aceptados validados "
        "(cadena revision→manifiesto→SHAs, sin importar ni diseñar integrador) y "
        "baseline R7 pinnada (base_sha256 verificado), sin hardcodear 4506 ni "
        "comparar el vivo consigo mismo. Revisadas = base pinnada + deltas R7+R8; "
        "candidatas = 17 + 28 − promovidas R8. Validadores de igualdad exacta "
        "R4→R7 corren sobre era R7 (vivo menos delta R8 validado). Scope R7, "
        "doble aprobación A+B y negativas intactos. Subset staging en R7: 35 OK."
    ),
    "pruebas_verificables": {
        "comando": "uv run python -m unittest discover -s propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests -t propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests",
        "total": 35,
        "resultado": "OK",
        "nota": "Subset (5 archivos) en staging sobre R7; producción solo leída. "
        "Simulación post-R8 (era = vivo − 28 nuevas): validar_extension_vinculos "
        "devuelve las 29 adiciones; aritmética 4475+3+28=4506 y candidatas 17.",
    },
    "cambios_frente_a_v001": [
        "Helper _aceptadas_ronda(n) por deltas validados (reemplaza vía R8 sin integrador).",
        "test_conteos: estados previos desde base de cobertura + overlay de promociones; bucle R8 general.",
        "test_significados/condicionados: cargar congelado en vez de validar vivo; promociones R8 no-op.",
        "Revisadas: + r8n validado en agentes/ronda_2/ronda_3/test_ronda_7; ancla cruzado con baseline pinnada.",
        "test_ronda_3: validador histórico sobre era R7.",
        "test_ronda_7: exactitud por aritmética pinnada; candidatas descuentan R8; scope R8 solo-vínculos; "
        "construir sobre era; hook sustituido por test real (verde antes y después de instalar R8).",
    ],
    "archivos_codigo": archivos,
    "cambios_produccion_propuestos": "Ninguno en scripts/ontologia/data. Solo tests (ver instrucciones_aplicacion).",
    "instrucciones_aplicacion": [
        "1. Auditar esta v002 con dos revisores independientes (código + pruebas).",
        "2. Tras aprobar, aplicar sobre tests/ los 5 archivos finales de v002/codigo/tests/ "
        "(4 sobrescriben a v001 ya aplicada o a producción pre-R7; test_ronda_7.py es alta).",
        "3. Al instalar R8 (config + manifiesto + aceptadas + regeneración), la suite debe seguir en verde "
        "sin tocar tests: los bloques R8 se activan solos por deltas validados.",
        "4. Verificar en era R7 y tras R8: uv run python -m unittest discover -s tests -t <dir-tests>.",
        "5. No editar v001 (congelada), I-codigo/, scripts/, ontologia/, data/, docs/ ni reports/ con este pase.",
    ],
    "base_sha256": base,
    "limites": [
        "Alcance T-pruebas: suite Python; no acredita significados, vigencias, joins ni identidades.",
        "Sin navegador Obscura (exclusivo W-web); sin peticiones-web.json (insumo local).",
        "Sin Gemma/chat; sin mensajes externos; sin puentes ni CLI OpenCode.",
        "Validadores R4→R7 sobre el vivo fallarían tras R8 sin integrador nuevo (no diseñado aquí); "
        "v002 los corre sobre era R7 + aritmética pinnada. La carga de cobertura (cargar_evidencia) "
        "es solo-manifiesto y tolera adiciones como ya hizo con R7.",
        "Correcciones futuras en v003+; esta v002 congelada no se edita.",
    ],
}

(V2 / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = [
    "# T-pruebas v002 — suite compatible R8",
    "",
    f"Fecha UTC: {entrega['fecha_utc']}",
    "Modelo: `opencode-go/muse-spark-1.3-contributor`, MCP nativo OpenCode. Sin Gemma, sin Obscura, sin contactos externos. v001 preservada y congelada.",
    "",
    "## Casos asignados",
    "",
    "Asignación con `casos: []`: cero ids, cero decisiones.",
    "",
    "## Afirmación exacta acotada",
    "",
    entrega["afirmacion_exacta_acotada"],
    "",
    "## Pruebas verificables",
    "",
    f"- Subset staging: `{entrega['pruebas_verificables']['comando']}` → {entrega['pruebas_verificables']['total']} pruebas OK.",
    "- Producción solo leída; nada instalado ni modificado fuera de `T-pruebas/v002/`.",
    "",
    "## Cambios frente a v001",
    "",
    *[f"- {c}" for c in entrega["cambios_frente_a_v001"]],
    "",
    "## Instrucciones de aplicación",
    "",
    *[f"- {s}" for s in entrega["instrucciones_aplicacion"]],
    "",
    "## Archivos de código (SHA-256 programáticos)",
    "",
    *[f"- `{a['ruta']}` `{a['sha256']}`" for a in archivos],
    "",
    "## Base leída",
    "",
    *[f"- `{r}` `{h}`" for r, h in base.items()],
    "",
]
(V2 / "entrega.md").write_text("\n".join(md), encoding="utf-8")

congelada = {
    "rol": "T-pruebas",
    "version": "v002",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "entrega_sha256": sha(V2 / "entrega.json"),
    "entrega_md_sha256": sha(V2 / "entrega.md"),
    "archivos": {a["ruta"]: a["sha256"] for a in archivos},
    "generador_sha256": sha(V2 / "generar-entrega.py"),
    "nota": "Congelada: no editar. Correcciones solo en v003+.",
}
(V2 / "congelada.json").write_text(json.dumps(congelada, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"entrega": congelada["entrega_sha256"], "archivos": len(archivos)}, ensure_ascii=False))
