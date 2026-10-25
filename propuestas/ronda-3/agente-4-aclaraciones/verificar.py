"""Verificador del Agente-4 ronda-3 (solo lectura fuera de su carpeta).

Comprueba: 23 significados = candidatas centrales (set exacto + huellas +
literales), 3 columnas/6 vinculos, 5 observaciones (textos originales intactos,
sin sintesis llamada literal), 1 referencia (huellas 177/178/7), 14 preguntas
originales trazables bidireccionalmente (ya_resuelto sin pregunta), 836
revisadas intactas, catalogo byte-identico, sin patrones de correspondencia/
concepto nuevo, literales exactos a–o/año sin sustituto ascii, y negativos
reales (mutaciones en copia temporal deben fallar).
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parents[2]
OUT = AQUI
errs = []


def chk(cond, msg):
    if not cond:
        errs.append(msg)


cob = json.loads((BASE / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
prop = json.loads((OUT / "propuestas.json").read_text(encoding="utf-8"))
preg_txt = (OUT / "preguntas-publicador.md").read_text(encoding="utf-8")
comp = json.loads((OUT / "comparativa.json").read_text(encoding="utf-8"))
man = json.loads((OUT / "fuente/manifiesto-fuentes.json").read_text(encoding="utf-8"))


def validar(pro, cands_set, amb_cols, obs_map, n_rev_esperado):
    e = []
    decs = pro["decisiones"]
    sig = [d for d in decs if d["tipo"] == "significado"]
    amb_d = [d for d in decs if d["tipo"] == "ambiguedad"]
    obs_d = [d for d in decs if d["tipo"] == "observacion"]
    ref_d = [d for d in decs if d["tipo"] == "referencia_catalogo"]
    if len(sig) != 23:
        e.append(f"significados={len(sig)} != 23")
    if {d["definicion_iri"] for d in sig} != cands_set:
        e.append("set 23 difiere de cobertura")
    if len(amb_d) != 3 or sum(len(d["vinculos"]) for d in amb_d) != 6:
        e.append("ambiguedad != 3/6")
    if {d["columna_iri"] for d in amb_d} != amb_cols:
        e.append("set 3 columnas difiere")
    if len(obs_d) != 5 or {d["observacion_id"] for d in obs_d} != set(obs_map):
        e.append("observaciones != 5")
    if len(ref_d) != 1:
        e.append("referencias != 1")
    by_iri = {v["definicion_iri"]: v for v in cob["variables"]}
    for d in sig:
        v = by_iri.get(d["definicion_iri"])
        if v is None:
            e.append(d["id"] + ": definicion fuera de cobertura")
            continue
        if v["huella_fila_diccionario"] != d["huella_fila_diccionario"]:
            e.append(d["id"] + ": huella difiere")
        if v["descripcion"] != d.get("descripcion_original", d.get("descripcion_literal")):
            e.append(d["id"] + ": literal difiere")
    for d in obs_d:
        o = obs_map[d["observacion_id"]]
        if d.get("texto_observacion_original") != o["observacion"]:
            e.append(d["id"] + ": texto original difiere")
        if "descripcion_literal" in d:
            e.append(d["id"] + ": sintesis llamada literal")
    qmap = {q["id"]: set(q["items"]) for q in pro["preguntas_publicador"]}
    if len(qmap) != 14:
        e.append(f"preguntas={len(qmap)} != 14")
    for d in decs:
        if d["clasificacion"] == "ya_resuelto_en_integracion":
            if d["pregunta_id"] is not None:
                e.append(d["id"] + ": resuelto con pregunta")
        elif d["pregunta_id"] not in qmap or d["id"] not in qmap[d["pregunta_id"]]:
            e.append(d["id"] + ": pregunta rota")
    from collections import Counter
    c = Counter(d["clasificacion"] for d in decs)
    if (c["requiere_aclaracion_publicador"], c["documentado_con_limite"],
            c["ya_resuelto_en_integracion"]) != (23, 8, 1):
        e.append(f"clasificacion={dict(c)} != 23/8/1")
    blob = json.dumps(pro, ensure_ascii=False).lower()
    for pat in ("semantic-mapping", "corresponde_columna", "documental_revisada",
                "owl:sameas", "skos:exactmatch", "concepto_nuevo", "nuevo_concepto"):
        if pat in blob:
            e.append("patron prohibido: " + pat)
    n_rev = sum(1 for x in cob["correspondencias"] if x["estado"] == "documental_revisada")
    if n_rev != n_rev_esperado:
        e.append(f"revisadas={n_rev} != {n_rev_esperado}")
    return e


cands = {v["definicion_iri"] for v in cob["variables"]
         if v["estado"] == "candidata_sin_definicion_suficiente"}
amb = {x["columna"] for x in cob["correspondencias"] if x["estado"] == "ambigua_por_nombre"}
obs_map = {o["id"]: o for o in cob["observaciones_revision"]}

errs += validar(prop, cands, amb, obs_map, 836)

chk("'a–o'" in preg_txt and "'año'" in preg_txt, "faltan literales exactos")
chk("a-o" not in preg_txt.replace("a–o", ""), "sustituto ascii a-o")
chk(preg_txt.count("Estado ronda-3:") == 14, "estados != 14")

chk(comp["catalogo"]["bytes_identicos"] is True, "catalogo no identico")
chk(all(v == 0 for v in comp["catalogo"]["ocurrencias"].values()), "tokens en catalogo")
for nombre, meta in man["archivos"].items():
    if "sha256" in meta:
        p = OUT / "fuente" / nombre
        chk(p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == meta["sha256"],
            "huella fuente: " + nombre)

by_iri = {v["definicion_iri"]: v for v in cob["variables"]}
r = next(d for d in prop["decisiones"] if d["id"] == "R-des-mpo-res")
chk(r["filas_origen"][0]["huella_fila_diccionario"] == by_iri[
    "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177"]
    ["huella_fila_diccionario"], "R177 difiere")
chk(r["filas_origen"][1]["huella_fila_diccionario"] == by_iri[
    "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178"]
    ["huella_fila_diccionario"], "R178 difiere")
chk(r["variable_homonima_no_origen"]["huella_fila_diccionario"] == by_iri[
    "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F7"]
    ["huella_fila_diccionario"], "R fila7 difiere")

# Traza a–o/año: pipeline local fiel, divergencia lado publicador
tr = comp.get("traza_a_o", {})
chk(tr.get("codepoints_campo_inventario") == ["0x61", "0x2013", "0x6f"], "traza: inventario no es a–o")
chk(tr.get("codepoints_campo_datastore_actual") == ["0x61", "0x2013", "0x6f"], "traza: datastore no es a–o")
chk(tr.get("datastore_crudo_contiene_E2_80_93") is True, "traza: sin E2 80 93 en crudo")
chk(tr.get("datastore_crudo_contiene_C3_B1") is False, "traza: C3 B1 inesperado en crudo")
chk(tr.get("codepoints_variable_diccionario_6bcf5b63_f2") == ["0x61", "0xf1", "0x6f"],
    "traza: diccionario no es año")
chk(tr.get("csv_head_primeros_bytes_hex", "").startswith("6d756e69636970696f2c61f16f2c"),
    "traza: head no es latin-1 año")
chk(tr.get("huella_esquema_recalculada") == tr.get("huella_esquema_fijada")
    == "e0437c5f0c9a47bc7ac43aa296e8bc62125574b141e284834303e55fd3ecde32",
    "traza: huella recalculada difiere")
chk(tr.get("metodo_inspeccion_central") == "api_esquema_previo", "traza: metodo no es api")
# Negativo: con 'año' (U+00F1) la huella DEBE diferir (el check discrimina)
h_ano = hashlib.sha256(json.dumps(
    [{"nombre": ("año" if f["id"] == "a–o" else f["id"]), "tipo": f.get("type")}
     for f in next(x for x in json.loads(
         (BASE / "data/portal/inventario.json").read_text(encoding="utf-8"))["recursos"]
         if x["id"] == "ffca84a8-155e-41af-8223-0e098966cadf")["datastore"]["campos"]
     if not f["id"].startswith("_")],
    ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
chk(h_ano != "e0437c5f0c9a47bc7ac43aa296e8bc62125574b141e284834303e55fd3ecde32",
    "negativo: huella con año no difiere")

for f in ("propuestas.json", "resultado.md", "preguntas-publicador.md", "verificar.py",
          "comparativa.json", "fuente/manifiesto-fuentes.json"):
    chk((OUT / f).exists(), "falta " + f)

mut = copy.deepcopy(prop)
mut["decisiones"] = [d for d in mut["decisiones"] if d["id"] != "S-clues-12f684e9"]
chk(validar(mut, cands, amb, obs_map, 836) != [], "negativo: falta un significado no detectada")
mut2 = copy.deepcopy(prop)
sig0 = next(d for d in mut2["decisiones"] if d["tipo"] == "significado")
sig0["huella_fila_diccionario"] = "0" * 64
chk(validar(mut2, cands, amb, obs_map, 836) != [], "negativo: huella corrupta no detectada")
mut3 = copy.deepcopy(prop)
mut3["decisiones"].append({"id": "X", "tipo": "significado",
                           "definicion_iri": "https://example.org/mex-ontologi/definition/ZZ%2F1",
                           "huella_fila_diccionario": "0" * 64,
                           "descripcion_literal": "X", "clasificacion": "requiere_aclaracion_publicador",
                           "pregunta_id": "Q-PEND-SEED"})
chk(validar(mut3, cands, amb, obs_map, 836) != [], "negativo: intruso no detectado")
mut4 = copy.deepcopy(prop)
mut4["preguntas_publicador"] = mut4["preguntas_publicador"][:13]
chk(validar(mut4, cands, amb, obs_map, 836) != [], "negativo: pregunta faltante no detectada")

if errs:
    print("FALLO:")
    for x in errs:
        print(" -", x)
    raise SystemExit(1)
print("OK agente-4 ronda-3: 23 significados, 3 cols/6 vinc, 5 obs, 1 ref, "
      "14 preguntas, 836 revisadas intactas, catalogo identico, negativos OK.")
