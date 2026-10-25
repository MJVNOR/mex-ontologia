"""Prepara la entrada de integracion de las 29 correspondencias aprobadas.

Lee `propuestas.json` CONGELADA (SHA-256 fijado abajo; no modificar esa
entrega) y el estado central integrado (solo lectura). Construye
`entrada_integracion_29.json`: las 29 entradas con el mismo formato de
`vinculos_documentales_revisados` de `ontologia/semantica.json`, usando
descripcion literal, campos exactos y ambas huellas.

No escribe nucleo, motor ni otras carpetas: solo genera el archivo de
entrada en ESTA carpeta. La simulacion conserva las 836 previas exactas
y produce 865, sin asumir totales de candidatas tras la ampliacion
semantica en curso.

Uso: uv run python propuestas/ronda-3/agente-2-correspondencias/preparar_integracion.py
"""
import hashlib
import json
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, columnas  # noqa: E402

CONGELADO_SHA = "83593587f2ccb39a26f6851bdd3dcf1129ef901ddd1ec9e1db03bdcc9508e1d2"
ENTRADA = "entrada_integracion_29.json"


def sha256_archivo(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def cargar_central():
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
    ins = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
    base = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]["base_iri"]
    return sem, cob, inv, ins, base


def hoja_de(iri_columna):
    if "/file-column/" in iri_columna:
        segs = unquote(iri_columna.split("/file-column/")[1]).split("/")
        if len(segs) >= 3:
            return segs[1]
    return ""


def sin_agudos(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                   if c not in {"\u0300", "\u0301", "\u0302", "\u0308"})


def validar_entradas(entradas, sem, cols_calc, var_por_def, rec_por_id, previas):
    """Valida cada entrada contra el estado central; ValueError si algo falla."""
    reglas = {r["id"] for r in sem["reglas_descripcion_exacta"]}
    conceptos = set(sem["conceptos"].keys())
    vistas = set()
    for e in entradas:
        esperadas = {"recurso", "campo", "columna", "diccionario", "concepto",
                     "descripcion", "huella_esquema", "huella_fila_diccionario", "criterio"}
        if set(e.keys()) != esperadas:
            raise ValueError("Claves incompatibles con vinculo central: " + e.get("columna", "?"))
        col = cols_calc.get(e["columna"])
        if col is None:
            raise ValueError("Columna fisica inexistente: " + e["columna"])
        if (col["recurso"], col["campo"], col["conjunto"]) != (e["recurso"], e["campo"], col["conjunto"]):
            raise ValueError("Campo/recurso no coincide con esquema fisico: " + e["columna"])
        if col["huella_esquema"] != e["huella_esquema"]:
            raise ValueError("Huella de esquema alterada: " + e["columna"])
        v = None
        # La entrada central no guarda definicion_iri: se localiza por (diccionario, descripcion literal).
        candidatos = [x for x in var_por_def.values()
                      if x["diccionario"] == e["diccionario"] and x["descripcion"] == e["descripcion"]]
        if len(candidatos) != 1:
            raise ValueError("Descripcion literal no identifica variable unica: " + e["columna"])
        v = candidatos[0]
        if v["huella_fila_diccionario"] != e["huella_fila_diccionario"]:
            raise ValueError("Huella de fila alterada: " + e["columna"])
        if v.get("concepto") != e["concepto"]:
            raise ValueError("Concepto alterado: " + e["columna"])
        if v.get("estado") != "respaldada_por_definicion" or v.get("regla") not in reglas or e["concepto"] not in conceptos:
            raise ValueError("Variable sin respaldo vigente: " + e["columna"])
        if v.get("conjunto") != col["conjunto"]:
            raise ValueError("Distinto conjunto: " + e["columna"])
        titulo = (rec_por_id.get(e["recurso"], {}).get("nombre") or "")
        if "catalogo" in sin_agudos(titulo).lower() or hoja_de(e["columna"]).lower().startswith("cat_"):
            raise ValueError("Catalogo frente a tabla de observaciones: " + e["columna"])
        llave = (e["recurso"], e["campo"], e["columna"])
        if llave in previas:
            raise ValueError("Solapa con revision previa: " + e["columna"])
        if llave in vistas:
            raise ValueError("Duplicada en la entrada: " + e["columna"])
        vistas.add(llave)
    return vistas


def main():
    prop_path = OUT / "propuestas.json"
    if sha256_archivo(prop_path) != CONGELADO_SHA:
        raise ValueError("propuestas.json aprobada cambio (SHA distinto del congelado)")
    prop = json.loads(prop_path.read_text(encoding="utf-8"))
    if len(prop["propuestas_revisadas"]) != 29:
        raise ValueError("Se esperaban 29 propuestas aprobadas")
    sem, cob, inv, ins, base = cargar_central()
    previas = {(r["recurso"], r["campo"], r["columna"]) for r in sem["vinculos_documentales_revisados"]}
    if len(sem["vinculos_documentales_revisados"]) != 836 or len(previas) != 836:
        raise ValueError("Las 836 previas no estan exactas")
    cols_calc = {c["iri"]: c for c in columnas(inv, ins, base)}
    var_por_def = {v["definicion_iri"]: v for v in cob["variables"]}
    rec_por_id = {r["id"]: r for r in inv["recursos"]}

    entradas = []
    for p in sorted(prop["propuestas_revisadas"], key=lambda x: x["columna"]):
        entradas.append({"recurso": p["recurso"], "campo": p["campo"], "columna": p["columna"],
                         "diccionario": p["diccionario"], "concepto": p["concepto"],
                         "descripcion": p["descripcion"], "huella_esquema": p["huellas"]["huella_esquema"],
                         "huella_fila_diccionario": p["huellas"]["huella_fila_diccionario"],
                         "criterio": p["criterio"]})
    validar_entradas(entradas, sem, cols_calc, var_por_def, rec_por_id, previas)
    total = len(previas | {(e["recurso"], e["campo"], e["columna"]) for e in entradas})
    if total != 865:
        raise ValueError("Simulacion no produce 865")
    salida = {"generado_en_utc": datetime.now(timezone.utc).isoformat(),
              "sha_propuestas_congelada": CONGELADO_SHA,
              "conteos": {"previas_exactas": 836, "nuevas": 29, "total_simulado": 865},
              "nota": ("Entradas con formato de vinculos_documentales_revisados para el integrador. "
                       "No se asume total de candidatas tras la ampliacion semantica en curso."),
              "entradas": entradas}
    (OUT / ENTRADA).write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(salida["conteos"], ensure_ascii=False) + " -> " + ENTRADA)


if __name__ == "__main__":
    main()
