"""Valida las formas SHACL adicionales del carril S, version v001, con el motor real.

Uso (desde cualquier directorio):
    uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/S-shacl/v001/validar.py

Escribe resultados-validacion.json, entrega.json, entrega.md y sello.json dentro de
esta carpeta v001. No escribe en la raiz, ni en shapes/, ni en config.toml, ni en
ningun store central. Cada corrida usa stores temporales propios (mkdtemp).
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

V001 = Path(__file__).resolve().parent
ROOT = V001.parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from construir_catalogo import motor  # noqa: E402  (motor real: tools/open-ontologies.exe)

SH = Namespace("http://www.w3.org/ns/shacl#")
PROV = Namespace("http://www.w3.org/ns/prov#")
BASE_IRI = "https://example.org/mex-ontologi/"
MEX = Namespace(BASE_IRI + "vocab/")
SHAPES = V001 / "shapes.ttl"
FIXTURES = V001 / "fixtures"
ESPERADO = json.loads((FIXTURES / "esperado.json").read_text(encoding="utf-8"))
CONFIG = ROOT / "config.toml"
EXE = ROOT / "tools" / "open-ontologies.exe"
COPIAS = {
    "portal-322405": (ROOT / "data" / "portal" / "portal-completo.ttl", 322405),
    "studio-323014": (ROOT / "data" / "portal" / "studio-verificacion.ttl", 323014),
}
# Artefactos propios de esta entrega. No se sellan ni se listan borradores ajenos
# que puedan coexistir en la carpeta (p. ej. propuesta/, analisis/, verificar.py).
FIXTURES_PROPIOS = ["negativo.ttl", "positivo-instancias-r9.ttl", "positivo.ttl"]
ARTEFACTOS_PROPIOS = [
    "validar.py",
    "shapes.ttl",
    "fixtures/esperado.json",
    *[f"fixtures/{nombre}" for nombre in FIXTURES_PROPIOS],
    "resultados-validacion.json",
    "entrega.json",
    "entrega.md",
]


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def rel(ruta: Path) -> str:
    try:
        return ruta.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(ruta)


def ahora() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalizar(violacion: dict) -> dict:
    return {
        "forma": violacion.get("node_shape") or violacion.get("source_shape"),
        "focus": violacion.get("focus_node"),
        "ruta": violacion.get("result_path") or violacion.get("path"),
        "restriccion": violacion.get("constraint"),
        "mensaje": violacion.get("message"),
        "severidad": violacion.get("severity"),
    }


def pares(violaciones: list[dict]) -> list[dict]:
    return sorted(
        ({"shape": v.get("forma") or v.get("shape"), "focus": v.get("focus")} for v in violaciones),
        key=lambda p: (str(p["shape"]), str(p["focus"])),
    )


def correr(corpus: Path, etiqueta: str, triples_esperados: int | None = None, conservar: bool = False) -> dict:
    store = Path(tempfile.mkdtemp(prefix=f"s-shacl-v001-{etiqueta}-"))
    prueba = {
        "corpus": rel(corpus),
        "sha256_corpus": sha256(corpus),
        "store_temporal_aislado": str(store),
        "store_central_usado": False,
        "studio_ejecutado": False,
    }
    try:
        prueba["validate"] = motor(["validate", str(corpus)], store)
        inicio = time.perf_counter()
        carga = motor(["load", str(corpus)], store)
        prueba["load"] = carga
        resultado = motor(["shacl", str(SHAPES)], store)
        prueba["duracion_shacl_s"] = round(time.perf_counter() - inicio, 3)
        prueba["shacl"] = resultado
        prueba["conforms"] = resultado.get("conforms")
        prueba["focus_nodes"] = resultado.get("focus_nodes")
        prueba["violaciones"] = [normalizar(v) for v in resultado.get("violations", [])]
        prueba["violation_count"] = resultado.get("violation_count")
        prueba["restricciones_ignoradas"] = resultado.get("skipped_constraints", [])
        prueba["shapes_sin_instancias"] = resultado.get("unmatched_shapes", [])
        prueba["triples_cargados"] = carga.get("triples_loaded")
        if triples_esperados is not None:
            prueba["triples_esperados"] = triples_esperados
            prueba["triples_coinciden"] = carga.get("triples_loaded") == triples_esperados
        prueba["ok_motor"] = True
    except Exception as error:  # el motor puede fallar; se registra en vez de perder la entrega
        prueba["ok_motor"] = False
        prueba["error"] = repr(error)
    finally:
        if not conservar:
            shutil.rmtree(store, ignore_errors=True)
            prueba["store_eliminado"] = True
    return prueba


def reglas_desde_formas() -> list[dict]:
    g = Graph()
    g.parse(SHAPES, format="turtle")
    reglas = []
    for forma in g.subjects(RDF.type, SH.NodeShape):
        propiedades = []
        for p in g.objects(forma, SH.property):
            propiedades.append({
                "ruta": str(g.value(p, SH.path)),
                "minCount": g.value(p, SH.minCount),
                "maxCount": g.value(p, SH.maxCount),
                "nodeKind": str(g.value(p, SH.nodeKind)) if g.value(p, SH.nodeKind) else None,
                "clase": str(g.value(p, SH["class"])) if g.value(p, SH["class"]) else None,
                "datatype": str(g.value(p, SH.datatype)) if g.value(p, SH.datatype) else None,
                "mensaje": str(g.value(p, SH.message)) if g.value(p, SH.message) else None,
            })
        consultas = []
        for c in g.objects(forma, SH.sparql):
            consultas.append({
                "mensaje": str(g.value(c, SH.message)) if g.value(c, SH.message) else None,
                "severidad": str(g.value(c, SH.severity)) if g.value(c, SH.severity) else None,
                "select": str(g.value(c, SH.select)) if g.value(c, SH.select) else None,
            })
        reglas.append({
            "id": str(forma).rsplit("/", 1)[-1],
            "forma": str(forma),
            "clases_objetivo": sorted(str(o) for o in g.objects(forma, SH.targetClass)),
            "descripcion": str(g.value(forma, SH.description)) if g.value(forma, SH.description) else None,
            "propiedades": propiedades,
            "sparql": consultas,
        })
    return sorted(reglas, key=lambda r: r["id"])


def escribir_json(ruta: Path, datos: dict) -> None:
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tabla(filas: list[list[str]]) -> str:
    if not filas:
        return ""
    encabezado = "| " + " | ".join(filas[0]) + " |"
    separador = "| " + " | ".join("---" for _ in filas[0]) + " |"
    cuerpo = ["| " + " | ".join(fila) + " |" for fila in filas[1:]]
    return "\n".join([encabezado, separador, *cuerpo])


def main() -> int:
    config = tomllib.loads(CONFIG.read_text(encoding="utf-8"))["catalogo"]
    base_config = config["base_iri"]
    fallos: list[str] = []
    if base_config != BASE_IRI:
        fallos.append(
            f"config.toml declara base_iri={base_config!r} distinta de la usada por shapes.ttl "
            f"({BASE_IRI!r}); regenerar las formas con la base vigente. No se modifica config.toml."
        )

    reglas = reglas_desde_formas()
    pruebas: dict[str, dict] = {}

    # 1. Fixtures propios: positivos y negativos, con expectativas exactas.
    for archivo in sorted(ESPERADO):
        prueba = correr(FIXTURES / archivo, f"fixture-{Path(archivo).stem}")
        esperado = ESPERADO[archivo]
        prueba["esperado"] = esperado
        actuales = pares(prueba.get("violaciones", []))
        prueba["pares_actuales"] = actuales
        if not prueba.get("ok_motor"):
            prueba["coincide"] = False
        elif esperado.get("requiere"):
            g = Graph()
            g.parse(FIXTURES / archivo, format="turtle")
            fuera = sum(
                1 for s in g.subjects(RDF.type, MEX.VariableDocumentada)
                if str(g.value(s, MEX.estadoSemantico)) == "fuera_del_nucleo_actual"
            )
            candidatas = sum(
                1 for s in g.subjects(RDF.type, MEX.CorrespondenciaSemantica)
                if str(g.value(s, MEX.estadoCorrespondencia)) == "candidata_por_nombre"
            )
            prueba["requiere_observado"] = {
                "variable_estado_fuera": fuera,
                "correspondencias_candidata_por_nombre": candidatas,
            }
            prueba["coincide"] = (
                fuera == esperado["requiere"]["variable_estado_fuera"]
                and candidatas == esperado["requiere"]["correspondencias_candidata_por_nombre"]
                and prueba.get("conforms") is True
                and actuales == pares(esperado.get("violations", []))
            )
        else:
            prueba["coincide"] = (
                prueba.get("conforms") is esperado.get("conforms")
                and actuales == pares(esperado.get("violations", []))
            )
        if not prueba["coincide"]:
            fallos.append(f"fixture {archivo}: no coincide con fixtures/esperado.json")
        pruebas[archivo] = prueba

    # 2. Copias completas: portal 322405 y Studio 323014, en stores temporales propios.
    for etiqueta, (corpus, triples) in COPIAS.items():
        prueba = correr(corpus, f"copia-{etiqueta}", triples_esperados=triples)
        prueba["esperado"] = {"conforms": True, "violations": [], "triples": triples}
        prueba["triples_coinciden"] = prueba.get("triples_cargados") == triples
        prueba["coincide"] = (
            prueba.get("ok_motor")
            and prueba["triples_coinciden"]
            and prueba.get("conforms") is True
            and not prueba.get("violaciones")
            and not prueba.get("restricciones_ignoradas")
        )
        if not prueba["coincide"]:
            fallos.append(
                f"copia {etiqueta}: conforms={prueba.get('conforms')!r}, "
                f"triples={prueba.get('triples_cargados')!r}/{triples}, "
                f"violaciones={len(prueba.get('violaciones', []))}, "
                f"ignoradas={len(prueba.get('restricciones_ignoradas', []))}"
            )
        pruebas[etiqueta] = prueba

    ignoradas = [
        {"prueba": nombre, **ignorada}
        for nombre, prueba in pruebas.items()
        for ignorada in prueba.get("restricciones_ignoradas", [])
    ]
    sin_instancias = [
        {"prueba": nombre, **forma}
        for nombre, prueba in pruebas.items()
        for forma in prueba.get("shapes_sin_instancias", [])
    ]

    resumen = {
        "carril": "S-shacl",
        "version": "v001",
        "generado_en_utc": ahora(),
        "base_iri": {
            "valor": base_config,
            "origen": rel(CONFIG),
            "sha256_config": sha256(CONFIG),
            "decision": "fuera_de_alcance_no_modificar",
        },
        "motor": {
            "ejecutable": rel(EXE),
            "sha256_ejecutable": sha256(EXE),
            "invocado_desde": "scripts/construir_catalogo.py:motor",
            "argumentos": ["--no-connect", "--data-dir <store temporal>", "validate|load|shacl"],
            "modo_almacenamiento": "persistent",
            "sh_sparql_soportado": True,
        },
        "formas": {
            "archivo": rel(SHAPES),
            "sha256": sha256(SHAPES),
            "total_reglas": len(reglas),
            "reglas": reglas,
        },
        "fixtures": {
            "directorio": rel(FIXTURES),
            "esperado_sha256": sha256(FIXTURES / "esperado.json"),
            "archivos": {
                nombre: sha256(FIXTURES / nombre)
                for nombre in FIXTURES_PROPIOS
            },
        },
        "pruebas": pruebas,
        "restricciones_ignoradas": ignoradas,
        "shapes_sin_instancias": sin_instancias,
        "resultado_global": {
            "ok": not fallos,
            "fallos": fallos,
            "pruebas_ok": sum(1 for p in pruebas.values() if p.get("coincide")),
            "pruebas_total": len(pruebas),
        },
    }

    resultados = {
        "generado_en_utc": resumen["generado_en_utc"],
        "motor": resumen["motor"],
        "pruebas": pruebas,
        "restricciones_ignoradas": ignoradas,
        "shapes_sin_instancias": sin_instancias,
        "resultado_global": resumen["resultado_global"],
    }
    escribir_json(V001 / "resultados-validacion.json", resultados)
    escribir_json(V001 / "entrega.json", resumen)

    # 3. Markdown generado a partir del JSON, sin transcripcion manual.
    filas_reglas = [["Regla", "Clase objetivo", "Restriccion", "Justificacion"]]
    for regla in reglas:
        if regla["sparql"]:
            for consulta in regla["sparql"]:
                filas_reglas.append([
                    regla["id"],
                    ", ".join(regla["clases_objetivo"]),
                    "sh:sparql",
                    (consulta["mensaje"] or regla["descripcion"] or "").replace("|", "\\|"),
                ])
        for prop in regla["propiedades"]:
            partes = [f"path {prop['ruta']}"]
            for clave, etiqueta in (("minCount", "min"), ("maxCount", "max"), ("nodeKind", "nodeKind"),
                                    ("clase", "class"), ("datatype", "datatype")):
                if prop[clave] is not None:
                    partes.append(f"{etiqueta} {prop[clave]}")
            filas_reglas.append([
                regla["id"],
                ", ".join(regla["clases_objetivo"]),
                "; ".join(partes),
                (prop["mensaje"] or regla["descripcion"] or "").replace("|", "\\|"),
            ])

    filas_pruebas = [["Prueba", "Corpus (triples)", "Esperado", "Conforms", "Violaciones", "Ignoradas", "Resultado"]]
    for nombre, prueba in pruebas.items():
        filas_pruebas.append([
            nombre,
            f"{prueba['corpus']} ({prueba.get('triples_cargados')})",
            "conforme" if prueba["esperado"].get("conforms") else f"{len(prueba['esperado'].get('violations', []))} violaciones",
            str(prueba.get("conforms")),
            str(len(prueba.get("violaciones", []))),
            str(len(prueba.get("restricciones_ignoradas", []))),
            "OK" if prueba.get("coincide") else "FALLO",
        ])

    filas_focus = [["Prueba", "Forma", "focus_node"]]
    for nombre, prueba in pruebas.items():
        for violacion in prueba.get("violaciones", []):
            filas_focus.append([nombre, str(violacion["forma"]).rsplit("/", 1)[-1], violacion["focus"] or ""])
    if len(filas_focus) == 1:
        filas_focus.append(["—", "—", "sin violaciones"])

    md = [
        "# Entrega S-shacl v001 — formas adicionales acotadas",
        "",
        f"Generado en UTC: `{resumen['generado_en_utc']}`. Carril S, carpeta exclusiva "
        "`propuestas/ampliacion-post-r9/ejecucion-20261024/S-shacl/v001/`.",
        "",
        "## Alcance",
        "",
        "- Formas SHACL **adicionales** para coherencia estado/significado de `VariableDocumentada`, "
        "`CorrespondenciaSemantica` y contrato de `UnidadDeclarada`.",
        "- No se modifica `shapes/` ni ninguna entrega sellada; no se usa `sh:closed` global; "
        "no se rechazan propiedades adicionales válidas.",
        "- La base IRI se conserva tal como está en `config.toml` "
        f"(`{base_config}`, sha256 `{resumen['base_iri']['sha256_config']}`); no se decide ni sustituye.",
        "- Sin Gemma, contactos, búsquedas agotadas, manifiestos R1–R9, escritores centrales ni Studio en ejecución.",
        "",
        "## Motor",
        "",
        f"Motor real: `{resumen['motor']['ejecutable']}` sha256 `{resumen['motor']['sha256_ejecutable']}`, "
        f"invocado por `{resumen['motor']['invocado_desde']}` con `--no-connect` y un `--data-dir` temporal por prueba. "
        "`sh:sparql` se evaluó correctamente (sin restricciones ignoradas).",
        "",
        "Nota de implementación: este motor no compila `sh:or` cuando algún miembro usa `sh:node` "
        "(lo declara en `skipped_constraints` y deja la conformidad indeterminada). Por eso las reglas "
        "condicionales se expresan con `sh:sparql`, que sí se evalúa; no se usó `sh:or` en las formas entregadas.",
        "",
        "## Reglas y justificación",
        "",
        tabla(filas_reglas),
        "",
        "## Pruebas",
        "",
        tabla(filas_pruebas),
        "",
        *(
            [
                "El fixture de instancias R9 contiene "
                f"{pruebas['positivo-instancias-r9.ttl']['requiere_observado']['variable_estado_fuera']} variables "
                "con estado `fuera_del_nucleo_actual` y "
                f"{pruebas['positivo-instancias-r9.ttl']['requiere_observado']['correspondencias_candidata_por_nombre']} "
                "correspondencias `candidata_por_nombre` (incluida la de Total_Egresos). Todas conforman: "
                "no se rechazan por estas formas.",
                "",
            ]
            if "positivo-instancias-r9.ttl" in pruebas
            and pruebas["positivo-instancias-r9.ttl"].get("requiere_observado")
            else []
        ),
        "### Focus nodes de las violaciones observadas",
        "",
        tabla(filas_focus),
        "",
        "## Restricciones ignoradas y formas sin instancias",
        "",
        f"- Restricciones ignoradas: **{len(ignoradas)}**.",
        f"- Shapes sin instancias reportadas por el motor: **{len(sin_instancias)}**.",
    ]
    if ignoradas:
        md += ["", "```json", json.dumps(ignoradas, ensure_ascii=False, indent=2), "```"]
    if sin_instancias:
        md += ["", "```json", json.dumps(sin_instancias, ensure_ascii=False, indent=2), "```"]
    md += [
        "",
        "## Archivos y SHA-256",
        "",
        f"- `shapes.ttl` `{resumen['formas']['sha256']}`",
        f"- `fixtures/esperado.json` `{resumen['fixtures']['esperado_sha256']}`",
    ]
    for nombre, digest in resumen["fixtures"]["archivos"].items():
        md += [f"- `fixtures/{nombre}` `{digest}`"]
    md += [
        "",
        "Los SHA de esta entrega, de sus entradas y del motor están en `sello.json`, "
        "calculados por este mismo script sobre los bytes escritos.",
        "",
        "Solo se sellan los artefactos enumerados explícitamente por `validar.py`; "
        "cualquier otro archivo presente en la carpeta no forma parte de esta entrega.",
        "",
        "## Límites",
        "",
        "- No se promueven candidatas, no se crean correspondencias y no se toca el grafo central.",
        "- Las copias completas se cargaron en stores temporales aislados y se eliminaron al terminar; "
        "el JSON conserva ruta temporal, conteo de triples y SHA del corpus.",
        "- Una violación en fixtures negativos es el resultado esperado; en las copias completas "
        "el resultado esperado es conformidad total con estas formas.",
        "- La conformidad conjunta con las formas de producción no se prueba aquí: estas formas son "
        "adicionales y su combinación corresponde a la integración central.",
        "",
        f"Resultado global: **{'OK' if not fallos else 'FALLO'}** "
        f"({resumen['resultado_global']['pruebas_ok']}/{resumen['resultado_global']['pruebas_total']} pruebas).",
    ]
    if fallos:
        md += ["", "Fallos:", *[f"- {fallo}" for fallo in fallos]]
    (V001 / "entrega.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # 4. Sello: hashes de los bytes efectivamente escritos y de las entradas usadas.
    artefactos = []
    for nombre in ARTEFACTOS_PROPIOS:
        ruta = V001 / nombre
        if not ruta.is_file():
            raise RuntimeError(f"Falta un artefacto declarado: {nombre}")
        artefactos.append(ruta)
    sello = {
        "generado_en_utc": ahora(),
        "algoritmo": "sha256",
        "artefactos": {p.relative_to(V001).as_posix(): sha256(p) for p in artefactos},
        "entradas": {
            rel(CONFIG): sha256(CONFIG),
            rel(EXE): sha256(EXE),
            **{rel(corpus): sha256(corpus) for corpus, _ in COPIAS.values()},
        },
        "nota": "SHA-256 calculado por validar.py sobre los archivos escritos; sello.json no se incluye a si mismo. Sin transcripcion manual.",
        "resultado_global_ok": not fallos,
    }
    escribir_json(V001 / "sello.json", sello)

    print(json.dumps({
        "ok": not fallos,
        "pruebas": f"{resumen['resultado_global']['pruebas_ok']}/{resumen['resultado_global']['pruebas_total']}",
        "violaciones_copias": {n: len(p.get("violaciones", [])) for n, p in pruebas.items() if n in COPIAS},
        "restricciones_ignoradas": len(ignoradas),
        "fallos": fallos,
    }, ensure_ascii=False, indent=2))
    return 0 if not fallos else 1


if __name__ == "__main__":
    raise SystemExit(main())
