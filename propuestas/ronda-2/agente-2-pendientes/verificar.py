"""Verifica la entrega del Agente-2 ronda-2 contra fuentes centrales (solo lectura)."""
import json
import sys
import tomllib
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE / "scripts"))
from consolidar_semantica import columnas  # solo lectura: recomputa IRIs y huellas

OUT = BASE / "propuestas/ronda-2/agente-2-pendientes"
errs = []


def chk(cond, msg):
    if not cond:
        errs.append(msg)


cob = json.loads((BASE / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
prop = json.loads((OUT / "propuestas.json").read_text(encoding="utf-8"))
preg_txt = (OUT / "preguntas-publicador.md").read_text(encoding="utf-8")
res_txt = (OUT / "resultado.md").read_text(encoding="utf-8")
decs = prop["decisiones"]

# Conjuntos exactos centrales
cands = [v for v in cob["variables"] if v["estado"] == "candidata_sin_definicion_suficiente"]
amb = [x for x in cob["correspondencias"] if x["estado"] == "ambigua_por_nombre"]
by_iri = {v["definicion_iri"]: v for v in cob["variables"]}
obs = {o["id"]: o for o in cob["observaciones_revision"]}

sig = [d for d in decs if d["tipo"] == "significado"]
amb_d = [d for d in decs if d["tipo"] == "ambiguedad"]
obs_d = [d for d in decs if d["tipo"] == "observacion"]
ref_d = [d for d in decs if d["tipo"] == "referencia_catalogo"]

chk(len(sig) == len(cands) == 23, "significados != 23 centrales")
chk({d["definicion_iri"] for d in sig} == {v["definicion_iri"] for v in cands}, "set 23 difiere u omite/duplica")
chk(len({d["id"] for d in decs}) == len(decs) == 32, "ids duplicados o conteo != 32")
chk(len(amb_d) == 3 and sum(len(d["vinculos"]) for d in amb_d) == 6, "ambiguedad != 3/6")
chk({d["columna_iri"] for d in amb_d} == {x["columna"] for x in amb}, "set 3 columnas difiere")
chk(len(obs_d) == len(obs) == 5, "observaciones != 5")
chk({d["observacion_id"] for d in obs_d} == set(obs), "set 5 observaciones difiere")
chk(len(ref_d) == 1, "referencias != 1")

# Huellas de fila contra cobertura.json
for d in sig:
    v = by_iri[d["definicion_iri"]]
    chk(v["huella_fila_diccionario"] == d["huella_fila_diccionario"], d["id"] + ": huella fila difiere")
    chk(v["descripcion"] == d.get("descripcion_original", d.get("descripcion_literal")), d["id"] + ": literal difiere")
for d in amb_d:
    for v in d["vinculos"]:
        chk(v["variable_iri"].replace("documented-variable", "definition") == v["definicion_iri"], d["id"] + ": IRI par difiere")
        chk(v["evidencia_textual"] == "ide_col", d["id"] + ": evidencia difiere")

# IRIs fisicas y huellas de esquema recomputadas (solo lectura)
inv = json.loads((BASE / "data/portal/inventario.json").read_text(encoding="utf-8"))
ins = json.loads((BASE / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
base = tomllib.loads((BASE / "config.toml").read_text(encoding="utf-8"))["catalogo"]["base_iri"]
cols = {(c["iri"], c["recurso"]): c["huella_esquema"] for c in columnas(inv, ins, base)}
for d in amb_d + [x for x in obs_d if x.get("columna_iri")]:
    chk((d["columna_iri"], d["recurso"]) in cols, d["id"] + ": columna IRI sin fuente")
    if (d["columna_iri"], d["recurso"]) in cols:
        chk(cols[(d["columna_iri"], d["recurso"])] == d["huella_esquema"], d["id"] + ": huella esquema difiere")
for d in obs_d:
    if d.get("huella_fila_diccionario"):
        chk(obs[d["observacion_id"]].get("huella_fila_diccionario") == d["huella_fila_diccionario"], d["id"] + ": huella fila difiere")

# Literalidad observaciones: textos originales intactos, sin sintesis llamada literal
for d in obs_d:
    o = obs[d["observacion_id"]]
    chk(d.get("texto_observacion_original") == o["observacion"], d["id"] + ": texto original difiere")
    chk("descripcion_literal" not in d, d["id"] + ": sintesis llamada literal")
for d in (x for x in obs_d if x["observacion_id"] in ("anio-nacimientos-2024", "anio-divorcios-2023")):
    o = obs[d["observacion_id"]]
    chk(d["campo_original"] == o["campo"], d["id"] + ": campo_original difiere")
    chk("variable_diccionario_original" in d and d["variable_diccionario_original"] not in ("anio", "anio_registro"),
        d["id"] + ": variable original con ascii")
chk("'a–o'" in preg_txt and "'año'" in preg_txt, "preguntas sin literales exactos a–o/ano")
chk("a-o" not in preg_txt.replace("a–o", ""), "preguntas con sustituto ascii a-o")
rev = next(m["revision"] for m in cob["correspondencias"]
           if m.get("campo") == "anio_registro" and m.get("recurso") == "f05dfd7e-88c9-42c4-ab88-e849fc277155")
dv = next(d for d in obs_d if d["observacion_id"] == "anio-divorcios-2023")
chk(dv["revision_existente"] == rev, "revision Divorcios no integra/citada parcial")
for k in ("columna", "huella_esquema", "huella_fila_diccionario", "criterio", "descripcion", "fuente_revision"):
    chk(k in dv["revision_existente"], "revision Divorcios sin " + k)

# Referencia des_mpo_res
r = ref_d[0]
chk(r["filas_origen"][0]["huella_fila_diccionario"] == by_iri[
    "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177"]["huella_fila_diccionario"], "R177 difiere")
chk(r["filas_origen"][1]["huella_fila_diccionario"] == by_iri[
    "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178"]["huella_fila_diccionario"], "R178 difiere")
chk(r["variable_homonima_no_origen"]["huella_fila_diccionario"] == by_iri[
    "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F7"]["huella_fila_diccionario"], "R fila7 difiere")

# CVE_LOC: estructura observada si, pregunta por composicion no
cve = next(d for d in sig if d["id"] == "S-cve-loc-251309e5")
chk("2+3+4" in cve["afirma_con_limite"] or "9=2+3+4" in cve["afirma_con_limite"], "CVE_LOC sin composicion observada")
chk("vigencia" in cve["no_afirma"] and "oficial" in cve["no_afirma"], "CVE_LOC sin limite oficial/vigencia")
chk(cve.get("estructura_observada", {}).get("composicion") == "CVE_LOC(9)=ENT(2)+MUN(3)+LOC(4)", "CVE_LOC sin estructura")
qc = next(q for q in prop["preguntas_publicador"] if q["id"] == "Q-CLAVE-GEO")
chk("ya esta observada" in qc["texto"] and "nivel territorial" not in qc["texto"], "Q-CLAVE-GEO pregunta lo observado")

# Pregunta<->items bidireccional, ya_resuelto sin pregunta
qmap = {q["id"]: set(q["items"]) for q in prop["preguntas_publicador"]}
allitems = [i for s in qmap.values() for i in s]
chk(len(allitems) == len(set(allitems)), "item en dos preguntas")
for d in decs:
    if d["clasificacion"] == "ya_resuelto_en_integracion":
        chk(d["pregunta_id"] is None and d["id"] not in allitems, d["id"] + ": ya_resuelto con pregunta")
    else:
        chk(d["pregunta_id"] in qmap and d["id"] in qmap[d["pregunta_id"]], d["id"] + ": relacion pregunta rota")
chk({d["id"] for d in decs if d["pregunta_id"]} == set(allitems), "items huerfanos o faltantes")
chk(next(q for q in prop["preguntas_publicador"] if q["id"] == "Q-FIEBRE-DICC")["items"] ==
    sorted([d["id"] for d in amb_d] + [r["id"]]), "Q-FIEBRE-DICC no agrupa 3+1")

# Sin correspondencias nuevas
blob = json.dumps(prop, ensure_ascii=False).lower()
for pat in ("semantic-mapping", "corresponde_columna", "documental_revisada", "owl:sameas", "skos:exactmatch"):
    chk(pat not in blob, "patron prohibido: " + pat)

for f in ("propuestas.json", "resultado.md", "preguntas-publicador.md", "verificar.py"):
    chk((OUT / f).exists(), "falta " + f)

if errs:
    print("FALLO:")
    for e in errs:
        print(" -", e)
    raise SystemExit(1)
print(f"OK: {len(sig)} significados, {len(amb_d)} columnas/{sum(len(d['vinculos']) for d in amb_d)} vinculos, "
      f"{len(obs_d)} observaciones, {len(ref_d)} referencia; IRIs y huellas (fila+esquema) verificadas.")
