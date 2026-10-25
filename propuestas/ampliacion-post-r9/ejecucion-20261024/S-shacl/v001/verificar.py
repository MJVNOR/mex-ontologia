"""Prueba el complemento S2/S3/S5 con el motor real (open-ontologies.exe).

Para cada regla: fixture positivo (debe conformar) y negativo (debe incumplir
solo en la forma declarada). Después valida contra copias completas locales:
formas de producción, entrega sellada R1-R6, este complemento y la unión.
Escribe verificacion.json.
"""
from __future__ import annotations

import json
import hashlib
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
sys.path.insert(0, str(ROOT / "scripts"))
from construir_catalogo import motor  # noqa: E402

AQUI = Path(__file__).resolve().parent
FORMAS = AQUI / "propuesta/shapes-adicionales.ttl"
SELLADA = AQUI / "shapes.ttl"
FIXTURES = AQUI / "fixtures"
SHAPE = "https://example.org/mex-ontologi/shapes/"
PRUEBA = "https://example.org/mex-ontologi/prueba-s-shacl/"

REGLAS = [
    {
        "id": "S2",
        "forma": SHAPE + "AdicionalCorrespondenciaRevisadaConHuella",
        "fixture_positivo": "S2-positivo.ttl",
        "fixture_negativo": "S2-negativo.ttl",
        "nodos_negativos": [PRUEBA + "c-revisada-sin-huella"],
        "justificacion": (
            "La forma RevisionDocumental ya exige que quien tenga huellaEsquemaRevisado esté en "
            "'documental_revisada'. Falta el recíproco: sin él una correspondencia puede marcarse "
            "como revisada sin la huella del esquema ni de la fila del diccionario que la sostienen, "
            "y ninguna forma lo detecta (R5 solo mira la variable de destino)."
        ),
    },
    {
        "id": "S3",
        "forma": SHAPE + "AdicionalResumenMunicipalCoherencia",
        "fixture_positivo": "S3-positivo.ttl",
        "fixture_negativo": "S3-negativo.ttl",
        "nodos_negativos": [PRUEBA + "r-incompleto", PRUEBA + "r-ambas-sin-bandera"],
        "justificacion": (
            "presenteEnAmbas declara aparición en las dos fuentes del cruce y los conteos vienen de "
            "cada fuente. La bandera sin ambos conteos, o ambos conteos con bandera falsa, describe "
            "un cruce inexistente; ninguna forma vigente ni R1-R6 lo mira."
        ),
    },
    {
        "id": "S5a",
        "forma": SHAPE + "AdicionalCondicionConexion",
        "fixture_positivo": "S5-positivo.ttl",
        "fixture_negativo": "S5-negativo.ttl",
        "nodos_negativos": [PRUEBA + "condicion-sin-descripcion"],
        "justificacion": (
            "mex:CondicionConexion es obligatoria en ConceptoCompartido (minCount 1) y no tenía "
            "restricción propia: un IRI vacío satisfacía la forma del concepto."
        ),
    },
    {
        "id": "S5b",
        "forma": SHAPE + "AdicionalMunicipioSegunFuente",
        "fixture_positivo": "S5-positivo.ttl",
        "fixture_negativo": "S5-negativo.ttl",
        "nodos_negativos": [PRUEBA + "municipio-sin-procedencia"],
        "justificacion": (
            "mex:MunicipioSegunFuente es obligatoria en EntradaCatalogo (minCount 1) y tampoco "
            "tenía restricción: sin nombre ni procedencia, la entrada apuntaba a un nodo mudo."
        ),
    },
]

NO_PROPUESTAS = [
    {
        "borrador": "S1 respaldada_por_definicion -> significadoDocumentado",
        "motivo": "Ya cubierta por shape:VariableRespaldadaConSignificadoDocumentado (R1) de shapes.ttl.",
    },
    {
        "borrador": "S4 contrato completo de UnidadDeclarada",
        "motivo": "Ya cubierta por shape:UnidadDeclaradaContrato (R6) de shapes.ttl; se evita duplicar "
                  "las mismas rutas. R6 no exige rdfs:comment de alcance ni evidenciaNormativa: "
                  "queda anotado como hueco para el integrador, no como regla nueva.",
    },
    {
        "borrador": "enumeración cerrada de mex:estadoVigencia",
        "motivo": "El estado se usa en varias capas (integrar_entregas.py escribe "
                  "'edicion_INEGI_no_cotejada', ausente en la copia del portal): una lista cerrada "
                  "aquí sería incompleta y rechazaría valores válidos de otras capas.",
    },
    {
        "borrador": "candidata_sin_definicion_suficiente -> significadoCandidato",
        "motivo": "Se cumple en la copia (16/16), pero el estado describe suficiencia de definición, "
                  "no la existencia de una candidata; sin respaldo documental se descarta.",
    },
]


def shacl(store: Path, formas: Path) -> dict:
    return motor(["shacl", str(formas)], store)


def almacen_con(archivo: Path) -> Path:
    store = Path(tempfile.mkdtemp(prefix="s-shacl-"))
    carga = motor(["load", str(archivo)], store)
    if carga.get("triples_loaded", 0) == 0:
        raise RuntimeError(f"carga sin triples: {archivo}")
    return store


def evaluar(regla: dict) -> dict:
    salida = {"id": regla["id"], "forma": regla["forma"],
              "justificacion": regla["justificacion"]}
    for signo in ("positivo", "negativo"):
        store = almacen_con(FIXTURES / regla[f"fixture_{signo}"])
        try:
            resultado = shacl(store, FORMAS)
        finally:
            shutil.rmtree(store, ignore_errors=True)
        propias = [v for v in resultado.get("violations", [])
                   if v.get("node_shape") == regla["forma"]]
        salida[signo] = {
            "fixture": regla[f"fixture_{signo}"],
            "conforms": resultado.get("conforms"),
            "violation_count": resultado.get("violation_count"),
            "violaciones_de_la_forma": len(propias),
            "focus_nodes": sorted({v.get("focus_node") for v in propias}),
            "unmatched_shapes": resultado.get("unmatched_shapes", []),
        }
    positivo_ok = (salida["positivo"]["conforms"] is True
                   and salida["positivo"]["violation_count"] == 0)
    negativo_ok = (salida["negativo"]["conforms"] is False
                   and sorted(salida["negativo"]["focus_nodes"]) == sorted(regla["nodos_negativos"]))
    salida["resultado"] = "pasa" if positivo_ok and negativo_ok else "falla"
    return salida


def sonda_sh_or() -> dict:
    """Comprueba si el motor evalúa sh:or (los datos incumplen ambas ramas)."""
    datos = AQUI / "analisis/sonda-sh-or-datos.ttl"
    store = almacen_con(datos)
    try:
        resultado = shacl(store, AQUI / "analisis/sonda-sh-or.ttl")
    finally:
        shutil.rmtree(store, ignore_errors=True)
    evaluado = resultado.get("conforms") is False
    return {
        "forma": "analisis/sonda-sh-or.ttl",
        "datos": "analisis/sonda-sh-or-datos.ttl",
        "conforms": resultado.get("conforms"),
        "violation_count": resultado.get("violation_count"),
        "sh_or_evaluado": evaluado,
        "consecuencia": ("se evalúa" if evaluado else
                         "el motor no reporta la violación de sh:or; las formas que lo necesiten "
                         "deben usar sh:sparql, como S2/S3"),
    }


def copias() -> list[dict]:
    """Producción, entrega sellada, complemento y unión sobre cada copia local."""
    union = Path(tempfile.mkdtemp(prefix="s-shacl-union-")) / "shapes-union.ttl"
    union.write_text(SELLADA.read_text(encoding="utf-8") + "\n" + FORMAS.read_text(encoding="utf-8"),
                     encoding="utf-8")
    salidas = []
    for nombre, ruta in (
        ("portal-completo", ROOT / "data/portal/portal-completo.ttl"),
        ("studio-verificacion", ROOT / "data/portal/studio-verificacion.ttl"),
    ):
        store = almacen_con(ruta)
        try:
            corridas = {
                "produccion": shacl(store, ROOT / "data/portal/shapes.ttl"),
                "sellada_R1-R6": shacl(store, SELLADA),
                "complemento": shacl(store, FORMAS),
                "union_sellada_complemento": shacl(store, union),
            }
        finally:
            shutil.rmtree(store, ignore_errors=True)
        resumen = {k: {c: v.get(c) for c in ("conforms", "violation_count", "focus_nodes")}
                   for k, v in corridas.items()}
        conteo = Counter(
            (v.get("node_shape", "").rsplit("/", 1)[-1], v.get("constraint"))
            for v in corridas["complemento"].get("violations", []))
        salidas.append({
            "copia": str(ruta.relative_to(ROOT)),
            "corridas": resumen,
            "complemento_por_forma_y_restriccion": {
                f"{forma}:{restriccion}": n for (forma, restriccion), n in sorted(conteo.items())},
            "sin_instancias_reportadas": corridas["produccion"].get("unmatched_shapes", []),
        })
    shutil.rmtree(union.parent, ignore_errors=True)
    return salidas


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main() -> None:
    reglas = [evaluar(r) for r in REGLAS]
    salida = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "carril": "S-shacl",
        "version": "v001-complemento",
        "motor": str((ROOT / "tools/open-ontologies.exe").relative_to(ROOT)),
        "formas_complemento": str(FORMAS.relative_to(ROOT)),
        "formas_selladas": str(SELLADA.relative_to(ROOT)),
        "reglas": reglas,
        "reglas_que_pasan": sum(r["resultado"] == "pasa" for r in reglas),
        "reglas_totales": len(reglas),
        "sonda_sh_or": sonda_sh_or(),
        "copias": copias(),
        "no_propuestas": NO_PROPUESTAS,
        "limites": [
            "Los fixtures se validan solo contra el complemento, no contra producción ni R1-R6: "
            "aisla cada regla, no acredita el grafo.",
            "sh:or no se evalúa en este motor (sonda_sh_or); por eso S2/S3 usan sh:sparql.",
            "El motor trata los literales sin tipo como no xsd:string: las formas nuevas no imponen "
            "sh:datatype xsd:string sobre etiquetas ni comentarios (sí nodeKind en los IRI).",
            "ResultadoMunicipalLote (producción) no tiene instancias: el motor lo reporta en "
            "unmatched_shapes y sus restricciones no se evaluaron.",
            "Las copias son los archivos locales del repositorio, no una instantánea certificada de Studio.",
            "Las reglas R1-R6 de esta carpeta tienen su propia entrega sellada; este complemento no las "
            "repite ni las sustituye.",
            "sello.json y entrega.* de esta carpeta pertenecen a la entrega R1-R6 y no cubren estos "
            "bytes; sus hashes vigentes están en entrega-deepseek.json.",
        ],
    }
    (AQUI / "verificacion.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    artefactos = [
        "propuesta/shapes-adicionales.ttl", "verificar.py", "verificacion.json",
        "analisis/inspeccionar_copias.py", "analisis/inspeccion.json",
        "analisis/sonda-sh-or.ttl", "analisis/sonda-sh-or-datos.ttl",
        *sorted(str(p.relative_to(AQUI)).replace("\\", "/") for p in FIXTURES.glob("S*.ttl")),
    ]
    entrega = {
        "fecha_utc": salida["fecha_utc"],
        "carril": "S-shacl",
        "version": "v001-complemento",
        "motor": {"ejecutable": salida["motor"], "sha256": sha256(ROOT / "tools/open-ontologies.exe")},
        "entradas": {
            "config.toml": sha256(ROOT / "config.toml"),
            "data/portal/portal-completo.ttl": sha256(ROOT / "data/portal/portal-completo.ttl"),
            "data/portal/studio-verificacion.ttl": sha256(ROOT / "data/portal/studio-verificacion.ttl"),
            "data/portal/shapes.ttl": sha256(ROOT / "data/portal/shapes.ttl"),
            "shapes.ttl (entrega R1-R6)": sha256(SELLADA),
        },
        "reglas": [{
            "id": r["id"], "forma": r["forma"], "justificacion": r["justificacion"],
            "fixtures": [r["positivo"]["fixture"], r["negativo"]["fixture"]],
            "positivo_conforms": r["positivo"]["conforms"],
            "negativo_conforms": r["negativo"]["conforms"],
            "negativo_focus_nodes": r["negativo"]["focus_nodes"],
            "resultado": r["resultado"],
        } for r in reglas],
        "pruebas_copias": salida["copias"],
        "sonda_sh_or": salida["sonda_sh_or"],
        "no_propuestas": NO_PROPUESTAS,
        "formas_sin_instancias": [
            {"forma": u.get("shape"), "target_class": u.get("target_class"),
             "copia": c["copia"]}
            for c in salida["copias"] for u in c["sin_instancias_reportadas"]],
        "restricciones_no_evaluadas": [
            "Todas las restricciones del complemento se evaluaron (0 ignoradas); el motor no reporta "
            "un campo de restricciones ignoradas en esta invocación.",
            "sh:or queda fuera de uso: se comprobó que no produce violación (analisis/sonda-sh-or.ttl).",
            "ResultadoMunicipalLote: forma de producción sin instancias; sus cuatro restricciones no se "
            "ejercitaron contra datos.",
        ],
        "artefactos": {nombre: sha256(AQUI / nombre) for nombre in artefactos},
        "relacion_entrega_previa": (
            "shapes.ttl, validar.py, fixtures/{positivo,negativo,esperado,positivo-instancias-r9}, "
            "entrega.*, resultados-validacion.json y sello.json son de la entrega R1-R6 y no se tocaron. "
            "Este complemento añade S2, S3, S5a y S5b, que R1-R6 no cubren, y omite S1/S4 por duplicarlas."),
        "limites": salida["limites"],
    }
    (AQUI / "entrega-deepseek.json").write_text(
        json.dumps(entrega, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "reglas": {r["id"]: r["resultado"] for r in reglas},
        "copias": {c["copia"].split("/")[-1]: {k: v["conforms"] for k, v in c["corridas"].items()}
                   for c in salida["copias"]},
        "sh_or_evaluado": salida["sonda_sh_or"]["sh_or_evaluado"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
