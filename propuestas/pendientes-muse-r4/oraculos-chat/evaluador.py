"""Evaluador dimensional con negacion (ronda 4, rol oraculos-chat).

Separa 5 dimensiones que el oraculo viejo mezclaba en un pasa/falla:
  veracidad, completitud, citacion, recuperacion, bloqueo_proveedor.
Regla anti-falso-rechazo: un sintagma sensible dentro de una frase negada
('no demuestra misma medida', 'sin identidad de medida', 'queda pendiente')
NO es violacion: es la negacion correcta y cuenta a favor de veracidad.

Esquema por item: cadena o lista de alternativas; {"oraculo": nombre} se
resuelve contra oraculo_local.oraculos() (conteo vigente, no numero fijado).

Uso: uv run python propuestas/pendientes-muse-r4/oraculos-chat/evaluador.py
Sin modelo, sin red, sin Studio.
"""
import json
import pathlib
import re
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
CHAT = HERE.parent / "chat"

NEG = re.compile(
    r"\b(no|sin|ni|tampoco|nunca|jamas|falta(?:n)?|pendiente(?:s)?|"
    r"queda(?:n)?\s+sin|ausencia|no\s+se\s+(?:demuestra|prueba|acredita|"
    r"afirma|concluye|establece|valida|encontr)|no\s+hay|no\s+ejecutad)",
    re.IGNORECASE)
NEG_INICIAL = ("no ", "sin ", "ni ", "tampoco ", "nunca ", "jamas ")


def norm(s):
    s = unicodedata.normalize("NFKD", s.casefold())
    return "".join(c for c in s if not unicodedata.combining(c)).replace("ñ", "n").replace("�", "n")


ABBR = ("vs.", "p. ej.", "etc.", "núm.", "art.", "ej.", "Sr.", "Sra.", "Dr.")


def frases(texto):
    blind = texto
    for i, a in enumerate(ABBR):
        blind = blind.replace(a, "\ue000%d\ue001" % i)
    parts = re.split(r"(?<=[.\n;])\s+", blind)
    return [re.sub("\ue000(\\d+)\ue001", lambda m: ABBR[int(m.group(1))], p) for p in parts]


def negada(frase, sintagma):
    i = norm(frase).find(norm(sintagma))
    if i < 0:
        return False
    return bool(NEG.search(frase[:i + len(sintagma) + 20]))


def _alts(item, oraculos):
    if isinstance(item, dict):  # {"oraculo": nombre}
        v = (oraculos or {}).get(item["oraculo"])
        return ([str(v)] if v is not None else [], True)
    items = [item] if isinstance(item, str) else list(item)
    alts, sin_resolver = [], False
    for it in items:  # la alternativa puede ser {"oraculo": ...}
        a, sr = _alts(it, oraculos) if isinstance(it, dict) else ([it], False)
        alts.extend(a)
        sin_resolver = sin_resolver or sr
    return (alts, sin_resolver and not alts)


def afirma(t, item, oraculos=None):
    alts, es_oraculo = _alts(item, oraculos)
    if es_oraculo and not alts:
        return None  # oraculo no resuelto: ni afirma ni niega
    for a in alts:
        na = norm(a)
        for f in frases(t):
            if na in norm(f) and (na.startswith(NEG_INICIAL) or not negada(f, a)):
                return True
    return False


def niega_bien(t, item, oraculos=None):
    alts, _ = _alts(item, oraculos)
    return any(norm(a) in norm(f) and negada(f, a) for a in alts for f in frases(t))


def eval_caso(caso, respuesta, oraculos=None):
    """respuesta: dict con chat/respuesta/causa. Devuelve dimensiones."""
    if respuesta is None or respuesta.get("chat") in (
            "bloqueado_otro", "bloqueado_cuota", "pendiente_cuota", "no_probado"):
        return {"veredicto": "no_evaluable",
                "razon": "sin respuesta del modelo (" + str(respuesta.get("chat")) + ")",
                "detalle": {"bloqueo_proveedor": respuesta.get("chat"),
                             "causa": (respuesta.get("causa") or "")[:120]}}
    t = respuesta["respuesta"]
    det = {"afirmado": [], "negado_ok": [], "afirmacion_indebida": [],
           "omitido": [], "citas": [], "oraculo_pendiente": []}
    for it in caso.get("afirmar", []):
        r = afirma(t, it, oraculos)
        (det["afirmado"] if r else det["omitido"]).append(it)
        if r is None:
            det["oraculo_pendiente"].append(it)
    for it in caso.get("negar", []):
        if afirma(t, it, oraculos):
            det["afirmacion_indebida"].append(it)
        elif niega_bien(t, it, oraculos):
            det["negado_ok"].append(it)
        # ausente del todo = no_aplica: no se exige negar lo no mencionado
    for it in caso.get("citas", []):
        if afirma(t, it, oraculos):
            det["citas"].append(it)
    if det["afirmacion_indebida"]:
        v = ("falla_real", "afirma lo que debia negar: " + str(det["afirmacion_indebida"]))
    elif det["omitido"] and not det["afirmado"]:
        v = ("falla_real", "omite todo el contenido requerido")
    elif det["omitido"]:
        v = ("parcial", "cubre parte pero omite: " + str(det["omitido"]))
    else:
        v = ("acierto", "afirma lo debido sin afirmaciones indebidas")
    return {"veredicto": v[0], "razon": v[1], "detalle": det}
    # ponytail: la negacion ausente no penaliza; el matiz (negar explicito vs
    # no mencionar) queda para revision manual. Ver evaluacion_manual.json.


def demo():  # ponytail: rompe si la negacion vuelve a penalizarse
    r = eval_caso(
        {"afirmar": ["igualdad aritmetica"],
         "negar": [["identidad de medida", "misma medida"]]},
        {"chat": "probado",
         "respuesta": "Hay igualdad aritmetica. No demuestra misma medida ni identidad de medida."})
    assert r["veredicto"] == "acierto", r
    r2 = eval_caso(
        {"negar": [["misma medida"]]},
        {"chat": "probado", "respuesta": "Ambas fuentes miden la misma medida."})
    assert r2["veredicto"] == "falla_real", r2
    r3 = eval_caso(
        {"afirmar": [{"oraculo": "revisadas_repo"}]},
        {"chat": "probado", "respuesta": "Hay 865 revisadas."},
        {"revisadas_repo": 865})
    assert r3["veredicto"] == "acierto", r3
    return True


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE))
    import oraculo_local
    corpus = json.loads((HERE / "corpus_mejorado.json").read_text(encoding="utf-8"))
    casos = {c["id"]: c for c in corpus["casos"]}
    orac = oraculo_local.oraculos()
    for origen in ["antes-cambio-modelo/respuestas-saneadas.json", "respuestas-saneadas.json"]:
        p = CHAT / origen
        if not p.exists():
            continue
        print("== " + origen)
        for r in json.loads(p.read_text(encoding="utf-8")):
            e = eval_caso(casos[r["id"]], r, orac)
            print(r["id"], "->", e["veredicto"], "|", e["razon"])
