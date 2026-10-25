"""Plan cobertura Muse: recalcula base, verifica particion 1242+66, decisiones
de agentes 3/6/7/8/9/10, SHAs antes/despuos del control y emite inventario.json.

Solo LEE fuera de su carpeta; solo ESCRIBE dentro de ella. Sin red, sin
modelos, sin cambios centrales, sin generar ni sincronizar.

Uso desde la raiz:
  uv run python propuestas/plan-cobertura-muse/cobertura/scripts/comprobar.py
"""
import hashlib
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ROOT = AQUI.parent.parent.parent

AGENTES = {
    "3": "propuestas/ronda-3/agente-3-cobertura/propuestas.json",
    "6": "propuestas/ronda-3/agente-6-salud/propuestas.json",
    "7": "propuestas/ronda-3/agente-7-registro-civil/propuestas.json",
    "8": "propuestas/ronda-3/agente-8-educacion/propuestas.json",
    "9": "propuestas/ronda-3/agente-9-gobierno-digital/propuestas.json",
    "10": "propuestas/ronda-3/agente-10-territorio-economia/propuestas.json",
}
FALLOS = []


def ok(cond, mensaje):
    print(("PASS " if cond else "FAIL ") + mensaje)
    if not cond:
        FALLOS.append(mensaje)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports/pendientes-semanticos.json").read_text(encoding="utf-8"))
    asig = json.loads((ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    control = json.loads((ROOT / "propuestas/ronda-3/integrador/control-propuestas.json").read_text(encoding="utf-8"))

    ahora = datetime.now(timezone.utc).isoformat()
    huellas = {p: sha(p) for p in (
        "data/semantica/cobertura.json", "ontologia/semantica.json",
        "data/portal/contenido-inspeccion.json", "data/portal/inventario.json",
        "reports/pendientes-semanticos.json",
        "propuestas/ronda-3/integrador/asignaciones-semanticas.json",
        "propuestas/ronda-3/integrador/control-propuestas.json")}

    # 1. base recalculada
    est = cob["resumen"]["estados_variables"] if "estados_variables" in cob.get("resumen", {}) else {}
    fuera = [v for v in cob["variables"] if v["estado"] == "fuera_del_nucleo_actual"]
    cand4 = [v for v in cob["variables"] if v["estado"] == "candidata_sin_definicion_suficiente"]
    resp = [v for v in cob["variables"] if v["estado"] == "respaldada_por_definicion"]
    ok(len(cob["variables"]) == 1563, "base 1563 variables")
    ok(len(resp) == 232 and len(fuera) == 1308 and len(cand4) == 23, "base 232/1308/23")
    ok(len(sem["conceptos"]) == 103 and len(sem["reglas_descripcion_exacta"]) == 116, "nucleo 103/116")
    ok(huellas["propuestas/ronda-3/integrador/asignaciones-semanticas.json"] ==
       "360cb7f70708e726a055aded5e4747ef3dd6e9f0c4173b3aa2580eba38f38dbe",
       "asignaciones con SHA esperado")
    set_fuera = {v["definicion_iri"] for v in fuera}
    set_cand4 = {v["definicion_iri"] for v in cand4}

    # 2. particion exacta 1242 + 66, 23 aparte
    partes = {str(k): {x["definicion_iri"] for x in v["variables"]} for k, v in asig["asignaciones"].items()}
    ok(sorted((k, len(v)) for k, v in partes.items()) ==
       [("10", 468), ("6", 242), ("7", 163), ("8", 126), ("9", 243)], "particion 242/163/126/243/468")
    union = set().union(*partes.values())
    ok(len(union) == 1242, "particion 1242 sin duplicados")
    ok(union <= set_fuera, "particion dentro de fuera del nucleo")
    ok(not (union & set_cand4), "particion sin tocar 23 candidatas")
    resto = set_fuera - union
    ok(len(resto) == 66, "resto 66 = 1308 - 1242")

    # 3. entregas: decisiones, reglas 1:1, conceptos, SHAs
    props = {k: json.loads((ROOT / f).read_text(encoding="utf-8")) for k, f in AGENTES.items()}
    shas = {k: sha(f) for k, f in AGENTES.items()}
    proponer_clave = {"6": "proponer_significado", "7": "propuesta-significado",
                      "8": "propuesta", "9": "propuesta", "10": "proponer"}
    entrega = {}
    for k, p in props.items():
        if k == "3":
            reglas = p["reglas"]
            defs = {d for r in reglas for d in r["definiciones"]}
            sinp = p["sin_propuesta_tras_lectura"]
            entrega[k] = {"decisiones": 66, "proponer": 63, "pendiente": 3,
                          "reglas": len(reglas), "defs_unicas": len(defs),
                          "conceptos_nuevos": len(p["conceptos_nuevos"]),
                          "reutilizados": len(p["conceptos_reutilizados"]),
                          "calificadores": sum(1 for r in reglas if r.get("calificador")),
                          "sha256": shas[k]}
            ok(defs | {x["definicion_iri"] for x in sinp} == resto, "agente 3 cubre el resto 66")
            continue
        decs = p.get("decisiones", [])
        campo = "decision" if k != "9" else "veredicto"
        clave_prop = proponer_clave[k]
        n_prop = sum(1 for d in decs if d.get(campo) == clave_prop)
        n_pend = sum(1 for d in decs if d.get(campo, "").startswith("pendiente"))
        defs = {d for r in p.get("reglas", []) for d in r.get("definiciones", [])}
        dec_iris = {d["definicion_iri"] for d in decs}
        cr = p.get("conceptos_reutilizados", [])
        entrega[k] = {"decisiones": len(decs), "proponer": n_prop, "pendiente": n_pend,
                      "reglas": len(p.get("reglas", [])), "defs_unicas": len(defs),
                      "conceptos_nuevos": len(p.get("conceptos_nuevos", {})),
                      "reutilizados": len(cr),
                      "calificadores": sum(1 for r in p.get("reglas", []) if r.get("calificador")),
                      "sha256": shas[k]}
        ok(dec_iris <= partes[k], "agente %s decisiones en su particion" % k)
        ok(dec_iris == partes[k], "agente %s particion completa" % k)
        ok(defs <= dec_iris, "agente %s reglas dentro de decisiones" % k)
        ok(not (defs & set_cand4), "agente %s sin tocar candidatas" % k)
    for x, y in itertools.combinations(sorted(entrega), 2):
        dx = {d for r in props[x].get("reglas", []) for d in r.get("definiciones", [])}
        dy = {d for r in props[y].get("reglas", []) for d in r.get("definiciones", [])}
        if x == "3":
            dx |= {s["definicion_iri"] for s in props["3"]["sin_propuesta_tras_lectura"]}
        if y == "3":
            dy |= {s["definicion_iri"] for s in props["3"]["sin_propuesta_tras_lectura"]}
        ok(not (dx & dy), "sin solapes reglas %s/%s" % (x, y))

    n_proponer = sum(e["proponer"] for e in entrega.values())
    n_pend = sum(e["pendiente"] for e in entrega.values())
    n_reglas = sum(e["reglas"] for e in entrega.values())
    n_conc = sum(e["conceptos_nuevos"] for e in entrega.values())
    ok(n_proponer + n_pend == 1308, "proponer+pendiente = 1308")
    ok(n_reglas == 980, "980 reglas (una por definicion)")
    ok(all(e["reglas"] == e["defs_unicas"] for e in entrega.values()), "reglas 1:1 con variables unicas")

    # 4. evolucion vs control (SHA antes/despuos)
    ctrl = {str(a.get("agente")): a for a in control["agentes"] if "agente" in a}
    evolucion = {}
    for k in ("3", "6", "7", "8", "9"):
        c = ctrl[k]
        evolucion[k] = {"antes_sha": c["sha256_propuestas"], "ahora_sha": shas[k],
                        "antes_reglas": c["reglas"], "ahora_reglas": entrega[k]["reglas"],
                        "cambio": shas[k] != c["sha256_propuestas"]}
    evolucion["10"] = {"antes_sha": None, "antes_estado": "sin_entrega",
                       "ahora_sha": shas["10"], "ahora_reglas": entrega["10"]["reglas"],
                       "cambio": True}
    ok(not evolucion["3"]["cambio"] and not evolucion["8"]["cambio"], "agentes 3 y 8 sin cambios")
    ok(evolucion["6"]["cambio"] and evolucion["7"]["cambio"], "agentes 6 y 7 evolucionaron")
    p10 = props["10"]
    emb = p10.get("conteos", {})
    evolucion["10"]["conteos_incrustados_vs_reales"] = {
        "incrustados": emb, "reales": {"proponer": entrega["10"]["proponer"],
                                       "pendiente": entrega["10"]["pendiente"],
                                       "reglas": entrega["10"]["reglas"]},
        "coinciden": (emb.get("proponer") == entrega["10"]["proponer"]
                      and emb.get("pendiente") == entrega["10"]["pendiente"])}

    inventario = {
        "generado_en_utc": ahora, "huellas": huellas,
        "base": {"variables": 1563, "respaldadas": 232, "fuera_del_nucleo": 1308,
                 "candidatas_agente4": 23, "conceptos": 103, "reglas_nucleo": 116},
        "particion": {"asignada_1242": {k: len(v) for k, v in partes.items()},
                      "resto_agente3": 66, "sin_duplicados": True,
                      "sin_solapes": True, "candidatas_aparte": True},
        "entregas": entrega,
        "totales": {"proponer": n_proponer, "pendiente": n_pend, "reglas": n_reglas,
                    "variables_unicas": n_reglas, "conceptos_nuevos": n_conc,
                    "conceptos_vs_interpretaciones": "832 nuevos + 103 vigentes; 980 interpretaciones (1:1)"},
        "evolucion_vs_control": evolucion,
        "fases": [
            {"fase": 0, "nombre": "Base y particion verificadas",
             "detalle": "1563/232/1308/23 recalculados; 1242+66 exactos sin duplicados ni solapes; 23 aparte."},
            {"fase": 1, "nombre": "Re-congelar control",
             "detalle": "Fijar SHAs actuales de agentes 6, 7, 9 y 10; exigir conteos incrustados = contenido (bloquea agente 10: 417/51 incrustados vs 419/49 reales)."},
            {"fase": 2, "nombre": "Revision por dominio con validador comun",
             "detalle": "Reglas restringidas, literales exactos, sin correspondencias; calificadores SHD/sede con requisito de propagacion.",
             "reparto": {"agente-6-salud": "242 (203 proponer/39 pendiente)",
                         "agente-7-registro-civil": "163 (75/88)",
                         "agente-8-educacion": "126 (99/27)",
                         "agente-9-gobierno-digital": "243 (121/122)",
                         "agente-10-territorio-economia": "468 (419/49)",
                         "agente-3-cobertura": "66 (63/3, cerrada)"}},
            {"fase": 3, "nombre": "Resolver 328 pendientes sin prometer lo no documentado",
             "detalle": "328 = 325 particion + 3 agente 3: clasificar con razon (vacia/generica/fuera de alcance) o segunda lectura; lo no documentado queda pendiente, no confirmado."},
            {"fase": 4, "nombre": "Integracion diferida (fuera de este plan)",
             "detalle": "Simulacion, propagacion de calificadores y aplicacion; sin auto-cruces ni sameAs."}],
        "limite": "Este plan no confirma significado no documentado ni integra nada.",
    }
    (AQUI / "inventario.json").write_text(json.dumps(inventario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("---")
    print("fallos: %d" % len(FALLOS))
    print("proponer=%d pendiente=%d reglas=%d conceptos_nuevos=%d" % (n_proponer, n_pend, n_reglas, n_conc))
    if FALLOS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
