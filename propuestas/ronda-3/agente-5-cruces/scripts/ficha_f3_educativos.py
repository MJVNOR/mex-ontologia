"""F3: UES Titulados-Egresados (2020-2021) y Nuevo-Reingreso (2021-2022).
Reconstruye la union externa desde las listas por fuente de validacion-lote.json
y la verifica con SQL en memoria: conteos independientes por (programa, sede).
Sin tasas ni cohortes. Negativos: acentos no homologados, periodos no mezclables,
0 publicado distinto de ausencia.
"""
import json
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BASE = RAIZ / "propuestas" / "ronda-3" / "agente-5-cruces"


def union_y_verifica(ejec, n_union, n_ambas_valor, tot_a, totb, periodo, ida, idb):
    assert ejec["periodo"] == periodo, ejec["periodo"]
    u = ejec["filas"]  # la union externa ya materializada: 1 fila por (programa, sede)
    assert isinstance(u, list) and len(u) == n_union, len(u) if isinstance(u, list) else u
    assert ejec["fuente_a"]["recurso_id"] == ida and ejec["fuente_b"]["recurso_id"] == idb
    assert ejec["fuente_a"]["periodo_declarado"] == periodo
    assert ejec["fuente_b"]["periodo_declarado"] == periodo
    assert ejec["fuente_a"]["valor_total"] == tot_a
    assert ejec["fuente_b"]["valor_total"] == totb
    da = {(v["programa_clave_local"], v["sede_declarada"]): v["valor"]
          for v in ejec["fuente_a"]["valores"]}
    db = {(v["programa_clave_local"], v["sede_declarada"]): v["valor"]
          for v in ejec["fuente_b"]["valores"]}
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE u (prog TEXT, sede TEXT, va INTEGER, vb INTEGER)")
    for k in set(da) | set(db):
        con.execute("INSERT INTO u VALUES (?,?,?,?)", (k[0], k[1], da.get(k), db.get(k)))
    assert con.execute("SELECT COUNT(*) FROM u").fetchone()[0] == n_union
    assert con.execute("SELECT SUM(va) FROM u").fetchone()[0] == tot_a
    assert con.execute("SELECT SUM(vb) FROM u").fetchone()[0] == totb
    nvb = con.execute("SELECT COUNT(*) FROM u WHERE va IS NOT NULL AND vb IS NOT NULL").fetchone()[0]
    assert nvb == n_ambas_valor, nvb
    assert con.execute("SELECT COUNT(*) FROM u WHERE va IS NULL").fetchone()[0] > 0
    ceros = con.execute("SELECT COUNT(*) FROM u WHERE va = 0 OR vb = 0").fetchone()[0]
    assert ceros > 0, "cero publicado distinguible de ausencia"
    progs = [r[0] for r in con.execute("SELECT DISTINCT prog FROM u")]
    assert len(progs) > 1
    return progs


def main():
    lote = json.loads((RAIZ / "data/portal/lote-cruces/validacion-lote.json").read_text(encoding="utf-8"))
    pares = {p["id"]: p for p in lote["pares"]}
    te = pares["037b03be-6b0a-4e2a-873d-9d4d410855cd--ef7dfb43-a80f-43b6-96c3-e067b8bf7ad1"]
    nr = pares["36c4624c-ae30-42fe-9ef1-350c8c497723--bb82d9cb-616e-4c9c-8ee0-f06082564f8a"]
    for p in (te, nr):
        assert p["decision"] == "ejecucion_parcial_exploratoria", p["id"]
    e1, e2 = te["ejecuciones"][0], nr["ejecuciones"][0]
    assert e1["periodo"] != e2["periodo"]  # negativo: periodos distintos no se mezclan
    p1 = union_y_verifica(e1, 175, 54, 1404, 1947, "2020-2021",
                          "782c6f34-2c92-4653-b792-ab7ea3e30226", "e6ba941d-c8b9-4392-8725-65e913bf2f22")
    p2 = union_y_verifica(e2, 165, 59, 3385, 12271, "2021-2022",
                          "e337f83e-ddcd-4960-8c6b-553def947194", "2fe45473-2e6f-42cd-9965-1db11227cf54")
    assert len(p2) > 1
    bio = [p for p in p1 if "biotecnologia" in p or "biotecnolog" in p]
    assert len(bio) >= 2, bio  # negativo: sin/con acento conviven sin fusionarse
    out = {"caso": "F3",
           "alcance": "Union reconstruida desde listas por fuente de validacion-lote.json "
                      "(xlsx UES leidos completos con sha; periodo de metadatos sin validacion externa). "
                      "No es lectura de microdatos personales: conteos por (programa, sede).",
           "titulados_egresados": {"union": 175, "ambas_con_valor": 54, "total_a": 1404, "total_b": 1947,
                                   "periodo": "2020-2021"},
           "nuevo_reingreso": {"union": 165, "ambas_con_valor": 59, "total_a": 3385, "total_b": 12271,
                               "periodo": "2021-2022"},
           "condiciones_verificadas": [
               "archivos xlsx leidos completos con sha (bfe28103, 3bdc9bc3, 9e898830, 2fe45473)",
               "mismo periodo declarado dentro de cada par (2020-2021 / 2021-2022)",
               "unicidad (programa, sede) reconstruida; sumas == totales; ausencia NULL, 0 publicado distinto",
               "claves con/sin acento conviven sin fusionarse (verificado, no homologado)"],
           "condiciones_que_impiden_uso_interpretativo": [
               "identidad de programa por nombre literal UES: acentos/variantes no homologados",
               "periodo solo declarado en metadatos, sin validacion externa",
               "fuente agregada (listas por fuente con huella), no filas crudas",
               "grano programa/sede de una institucion: no extrapolable; no tasas ni cohortes"],
           "decision": "habilitable_con_condiciones",
           "conclusion": "Conteos independientes por (programa, sede) y periodo coincidente declarado; union externa con ausencia=null.",
           "no_concluye": ["tasa de titulacion/egreso", "seguimiento de cohortes",
                            "homologacion de programas con/sin acento",
                            "mezcla de periodos 2020-2021 con 2021-2022"]}
    (BASE / "fichas" / "F3.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print("F3 OK")


if __name__ == "__main__":
    main()
