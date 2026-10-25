# -*- coding: utf-8 -*-
"""Construye entrega.json + pendientes.json + resultado.md del agente 8 (educacion).

Lee (solo lectura): copias congeladas de fuentes/ y manifiesto, mas insumos
centrales para verificar particion y huellas. Escribe SOLO en esta carpeta.
No ejecuta scripts historicos ni suite central. No descarga nada.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CENTRO = Path("C:/Users/marti/Documents/MEX-Ontologi")
FUENTES = CENTRO / "propuestas/cobertura-muse-20261023/fuentes"
ENTREGA_PATH = "propuestas/cobertura-muse-20261023/educacion/entrega.json"


def sha256_archivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest(), Path(p).stat().st_size


# 1. verificar copias congeladas contra manifiesto ---------------------------
manifiesto = json.load(open(FUENTES / "manifiesto.json", encoding="utf-8"))
frozen = {c["copia"]: c["sha256"] for c in manifiesto["copias"]}
for copia, esperado in frozen.items():
    real = hashlib.sha256(open(CENTRO / copia, "rb").read()).hexdigest()
    assert real == esperado, "manifiesto: %s" % copia
print("manifiesto: %d copias verificadas" % len(frozen))

SRC = json.load(open(FUENTES / "agente-8-educacion/propuestas.json", encoding="utf-8"))
assert hashlib.sha256(open(FUENTES / "agente-8-educacion/propuestas.json", "rb").read()).hexdigest() == \
    frozen["propuestas/cobertura-muse-20261023/fuentes/agente-8-educacion/propuestas.json"]

# 2. insumos centrales (lectura) para particion y huellas --------------------
asig = json.load(open(CENTRO / "propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
MINE = asig["asignaciones"]["8"]["variables"]
SEM = json.load(open(CENTRO / "ontologia/semantica.json", encoding="utf-8"))

# 3. transformar a formato estandar ------------------------------------------
decisiones = []
for d in sorted(SRC["decisiones"], key=lambda x: x["definicion_iri"]):
    nd = {"definicion_iri": d["definicion_iri"], "conjunto": d["conjunto"],
          "diccionario": d["diccionario"], "variable": d["variable"],
          "descripcion": d["descripcion"],
          "huella_fila_diccionario": d["huella_fila_diccionario"],
          "tipo_de_dato": d["tipo_de_dato"], "unidad_de_medida": d["unidad_de_medida"],
          "catalogo_de_referencia": d["catalogo_de_referencia"],
          "ejemplo_de_dato": d["ejemplo_de_dato"]}
    if d["decision"] == "propuesta":
        nd["decision"] = "proponer"
        nd["regla_id"] = d["regla_id"]
        nd["concepto"] = d["concepto"]
    else:
        nd["decision"] = "pendiente"
        nd["motivo"] = d["motivo"]
    nd["criterio"] = d.get("criterio", d.get("motivo", ""))
    nd["contexto_conjunto"] = d["contexto_conjunto"]
    decisiones.append(nd)

reglas = []
for r in SRC["reglas"]:
    nr = {"id": r["id"], "concepto": r["concepto"], "representacion": r["representacion"],
          "nombres": list(r["nombres"]), "descripciones": list(r["descripciones"]),
          "conjuntos": list(r["conjuntos"]), "diccionarios": list(r["diccionarios"]),
          "definiciones": list(r["definiciones"]),
          "huella_fila_diccionario": r["evidencia"][0]["huella_fila_diccionario"],
          "criterio": r["criterio"], "limites": [r["limite"]],
          "evidencia": r["evidencia"],
          "fuente_revision": ENTREGA_PATH}
    if "calificador" in r:
        nr["calificador"] = dict(r["calificador"])
    reglas.append(nr)

# 3b. ajuste puntual auditor 11 + integrador (estabilidad, no expansion) --------
AJUSTE = "Ajuste auditor 11 + integrador: "
for nr in reglas:
    if nr["id"] == "r3a8-034":
        assert nr["concepto"] == "nacionalidad-alumno" and nr["representacion"] == "nombre"
        assert nr["evidencia"][0]["tipo_de_dato"] == "Texto" and nr["evidencia"][0]["ejemplo_de_dato"] == " " * 10
        nr["representacion"] = "no_especificada"
        nr["limites"].append(AJUSTE + "tipo Texto y ejemplo vacío (10 espacios) no demuestran "
                                      "nombre ni código; representación no afirmada; significado "
                                      "nacionalidad-alumno permanece.")
    if nr["id"] in ("r3a8-013", "r3a8-017", "r3a8-081"):
        ev = nr["evidencia"][0]
        assert nr["concepto"] == "campo-formacion-academica" and nr["representacion"] == "codigo"
        assert ev["tipo_de_dato"] == "Número entero" and ev["ejemplo_de_dato"] == "7" and ev["catalogo_de_referencia"]
        nr["criterio"] += " " + AJUSTE + "código por tipo Número entero, ejemplo 7 y catálogo de " \
            "clasificación publicado en la fila; sin validar valores ni equiparar 7 con 07; " \
            "sin identidad, vigencia ni nueva correspondencia."
reglas.sort(key=lambda x: x["id"])

# 3c. ajuste auditoria-b (estabilidad, no expansion) ------------------------------
# Neutraliza sujeto/poblacion anadidos fuera de literal en 2 definiciones;
# sin calificador inferido como atajo. Dominio textual y limites intactos.
import copy as _copy
conceptos = _copy.deepcopy(SRC["conceptos_nuevos"])
_esp = "Modalidad cursada por el estudiante según el diccionario, con dominio publicado: Escolarizada, No escolarizada o Mixta. Población: estudiante matriculado."
assert conceptos["modalidad-cursada"][1] == _esp, "deriva en modalidad-cursada"
conceptos["modalidad-cursada"][1] = "Modalidad cursada según el diccionario, con dominio publicado: Escolarizada, No escolarizada o Mixta."
_grado = "Grado o cuatrimestre cursado por el estudiante según el diccionario. Denota el tramo curricular en curso."
assert conceptos["grado-cuatrimestre-cursado"][1] == _grado, "deriva en grado-cuatrimestre-cursado"
conceptos["grado-cuatrimestre-cursado"][1] = "Grado o cuatrimestre cursado según el diccionario. Denota el tramo curricular en curso."

# 4. conteos recalculados desde contenido -------------------------------------
n_proponer = sum(1 for d in decisiones if d["decision"] == "proponer")
n_pend = sum(1 for d in decisiones if d["decision"] == "pendiente")
assert len(decisiones) == 126 and n_proponer == 99 and n_pend == 27
assert len(reglas) == 99
usados = {d["concepto"] for d in decisiones if d["decision"] == "proponer"}
assert usados == set(SRC["conceptos_nuevos"]) | set(SRC["conceptos_reutilizados"])
assert not (set(SRC["conceptos_nuevos"]) & set(SEM["conceptos"]))
for v in SRC["conceptos_nuevos"].values():
    assert v[2] is None or v[2] in SEM["conceptos"] or v[2] in SRC["conceptos_nuevos"]
asig_iris = sorted(v["definicion_iri"] for v in MINE)
assert sorted(d["definicion_iri"] for d in decisiones) == asig_iris
assert all(v["estado"] == "fuera_del_nucleo_actual" for v in MINE)

insumos = {"copia_propuestas_agente8": FUENTES / "agente-8-educacion/propuestas.json",
           "asignaciones": CENTRO / "propuestas/ronda-3/integrador/asignaciones-semanticas.json",
           "pendientes": CENTRO / "reports/pendientes-semanticos.json",
           "cobertura": CENTRO / "data/semantica/cobertura.json",
           "semantica": CENTRO / "ontologia/semantica.json",
           "manifiesto": FUENTES / "manifiesto.json"}
fuentes = {}
for k, pth in insumos.items():
    h, b = sha256_archivo(pth)
    try:
        ruta = str(pth.relative_to(CENTRO))
    except ValueError:
        ruta = str(pth)
    fuentes[k] = {"sha256": h, "bytes": b, "ruta": ruta}

entrega = {
    "generado_en_utc": datetime.now(timezone.utc).isoformat(),
    "agente": "agente-8-educacion",
    "base_iri": "https://example.org/mex-ontologi/",
    "alcance": SRC["alcance"],
    "fuentes": fuentes,
    "decisiones": decisiones,
    "reglas": reglas,
    "conceptos_nuevos": conceptos,
    "conceptos_reutilizados": SRC["conceptos_reutilizados"],
    "limites": SRC["limites"],
    "requisitos_integracion": SRC["requisitos_integracion"],
    "conteos": {"decisiones": 126, "proponer": n_proponer, "pendiente": n_pend,
                "reglas": len(reglas),
                "conceptos_nuevos": len(SRC["conceptos_nuevos"])},
    "nota": SRC["nota"],
}
json.dump(entrega, open(BASE / "entrega.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 5. pendientes.json ----------------------------------------------------------
pendientes = []
for d in decisiones:
    if d["decision"] != "pendiente":
        continue
    m = d["motivo"]
    if "vacía" in m or "vacia" in m:
        falta = "Descripción publicada de la variable; el publicador debe completar la fila del diccionario."
    elif "genérica de orden" in m or "consecutivo" in m:
        falta = "Confirmación del publicador de que la columna es solo orden de fila sin significado."
    elif "genérica" in m:
        falta = "Leyenda o dominio de valores publicado para el campo."
    elif "confusa" in m:
        falta = "Redacción corregida y publicada de la descripción."
    else:
        falta = "Aclaración documental del publicador."
    pendientes.append({"definicion_iri": d["definicion_iri"], "variable": d["variable"],
                       "descripcion": d["descripcion"], "motivo": m,
                       "documentacion_faltante": falta})
json.dump(pendientes, open(BASE / "pendientes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 6. resultado.md breve -------------------------------------------------------
n_cal = sum(1 for r in reglas if "calificador" in r)
md = """# Agente 8 — Educación (cobertura-muse-20261023)

126 definiciones asignadas revisadas fila por fila contra copias congeladas
(SHA verificados contra `fuentes/manifiesto.json`): 99 propuestas con regla,
27 pendientes con motivo. 66 conceptos nuevos estrechos, 1 reutilización
(`programa-educativo`). 20 reglas con calificador de sede basado en literal;
el integrador los propagará al RDF.

Unidades y medidas: conteos con objeto literal de la descripción, sin tasas
ni porcentajes; edad sin unidad declarada (sin afirmar años); promedios sin
rango afirmado; sin monetarios. Poblaciones, eventos y sexos separados por
concepto; egreso≠titulación; nacimiento≠nacionalidad. Sin vigencia inferida,
sin identidad municipal, sin catálogos promovidos, sin correspondencias
columna-variable, sin sameAs/exactMatch.

Las 232 respaldadas y 23 candidatas centrales se preservan (simulación en
memoria sin cambios centrales). Conteos recalculados desde contenido:
decisiones=126, proponer=99, pendiente=27, reglas=99, conceptos_nuevos=66.

Ajuste auditor 11 + integrador: r3a8-034 (Nacionalidad) con representación
no afirmada (tipo Texto y ejemplo vacío no demuestran nombre ni código);
r3a8-013/017/081 (campo de formación) documentados como código por tipo,
ejemplo y catálogo publicado, sin validar valores ni equiparar 7 con 07.

Ajuste auditoría-b: r3a8-080 (Modalidad) y r3a8-082 (Grado) con definiciones
neutralizadas al literal, sin sujeto/población añadida ni calificador
inferido; dominio textual y límites intactos.

Reproducir (solo lee fuera de esta carpeta, sin red):
```powershell
uv run python propuestas/cobertura-muse-20261023/educacion/scripts/construir.py
$env:PYTHONDONTWRITEBYTECODE='1'
uv run python propuestas/cobertura-muse-20261023/educacion/scripts/verificar.py
```
"""
open(BASE / "resultado.md", "w", encoding="utf-8").write(md)
print("entrega=%d reglas=%d pendientes=%d calificadores=%d" % (len(decisiones), len(reglas), len(pendientes), n_cal))
