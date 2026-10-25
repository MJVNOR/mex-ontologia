"""F2: Proyecciones Grandes grupos x Indicadores. VALIDACION NUEVA sobre originales fijados.
NO reutiliza la inspeccion heuristica anterior como prueba (quedo refutada: el XLSX
real si tiene datos). Lee copias fijadas data/integracion/fuentes/<sha>.xlsx
(manifiesto ronda 1, SHAs verificados aqui).
- Grandes grupos (sha 24301617...): parsing del sheet XML por streaming con
  COORDENADAS Excel (atributo r): openpyxl read_only TRUNCA a 1 fila y el modo
  completo falla por un drawing roto (rel a drawing1.xml inexistente); por eso
  parser propio con context managers. ponytail: propio solo por esa limitacion.
  Celdas omitidas NO desplazan: se colocan por coordenada; huecos y formulas sin
  cache se registran como missing y la fila se rechaza (probado con negativos).
- Indicadores (sha e0e21aad...): openpyxl read_only (completo: 3672 filas).
Cruce NUEVO 2020 por (CLAVE,ANO) con agregacion SEXO previa; POB_TOTAL(H+M) vs
POB_MIT_MUN como yuxtaposicion (constructos distintos). Sin datos personales.
Hechos sincronizados: cobertura 1990-2040 OBSERVADA en ambos originales;
cruce ano por ano NO ejecutado; solo 2020 cruzado (verificado en el script).
Escribe fichas/claves-2020.json (72 agregados municipales 2020 con procedencia).
Alcance: validacion 2020 sobre originales; serie cruzada y vigencia de catalogo
pendientes (no_acreditada F3/F4 en matriz-vigencia ronda 2).
"""
import hashlib
import json
import sqlite3
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import openpyxl

RAIZ = Path(__file__).resolve().parents[4]
BASE = RAIZ / "propuestas" / "ronda-3" / "agente-5-cruces"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
GG_SHA = "24301617b6a5d89cf99b34ed4d512324cedde52e0c625de9457238e3d8fa340c"
IND_SHA = "e0e21aad3a84b4059efaf7525233ac05b08ced300f0f851fbadaab94057c027a"
GG_COLS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def col_to_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def split_ref(ref):
    i = 0
    while i < len(ref) and ref[i].isalpha():
        i += 1
    return ref[:i], int(ref[i:])


def cell_literal(c, strs):
    """Valor literal; formulas SOLO por cache (<v>); sin cache -> (None, 'formula_sin_cache')."""
    f = c.find(NS + "f")
    v = c.find(NS + "v")
    if f is not None and (v is None or v.text is None):
        return None, "formula_sin_cache"
    t = c.get("t")
    if t == "inlineStr":
        it = c.find(NS + "is")
        return ("".join(x.text or "" for x in it.iter(NS + "t")) if it is not None else None), None
    if v is None or v.text is None:
        return None, "vacio"
    if t == "s":
        return strs[int(v.text)], None
    if t == "str":
        return v.text, None
    if t == "e":
        return None, "error:" + v.text
    return v.text, None


def parse_row_cells(row_el, strs):
    """Coloca por coordenada; devuelve (valores[11], missing[], flags[])."""
    placed, missing, flags = {}, [], []
    for c in row_el.findall(NS + "c"):
        ref = c.get("r")
        assert ref is not None, "celda sin coordenada r"
        letters, _ = split_ref(ref)
        assert letters in GG_COLS, f"columna fuera de A-K: {ref}"
        v, flag = cell_literal(c, strs)
        placed[letters] = v
        if flag:
            flags.append((ref, flag))
    for L in GG_COLS:
        if L not in placed:
            missing.append(L)
    return [placed.get(L) for L in GG_COLS], missing, flags


def parse_grandes_grupos(path):
    """Streaming del sheet XML original. Rechaza filas con huecos/formulas sin cache."""
    with zipfile.ZipFile(path) as z:
        with z.open("xl/sharedStrings.xml") as fh:
            sroot = ET.parse(fh).getroot()
        strs = ["".join(t.text or "" for t in si.iter(NS + "t")) for si in sroot]
        with z.open("xl/worksheets/sheet1.xml") as fh:
            ctx = ET.iterparse(fh, events=("end",))
            hdr, rows, rechazadas = None, [], []
            for _ev, el in ctx:
                if el.tag == NS + "row":
                    rnum = el.get("r")
                    assert rnum is not None, "fila sin coordenada r"
                    vals, missing, flags = parse_row_cells(el, strs)
                    if hdr is None:
                        assert not missing and not flags, (missing, flags)
                        hdr = vals
                    elif missing or flags or any(v is None for v in vals):
                        rechazadas.append((int(rnum), missing, flags))
                    else:
                        rows.append((int(rnum), vals))
                    el.clear()
    return hdr, rows, rechazadas


def test_parser_negativos():
    """Negativos sinteticos: hueco interno, formula sin cache, fila corta."""
    frag = ('<row xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" r="9">'
            '<c r="A9" t="s"><v>0</v></c><c r="C9" t="n"><v>5</v></c>'
            '<c r="D9"><f>SUM(A9:C9)</f></c></row>')
    row = ET.fromstring(frag)
    vals, missing, flags = parse_row_cells(row, ["CLAVE"])
    assert vals[0] == "CLAVE" and vals[2] == "5", vals  # C no se desplaza a B
    assert "B" in missing, missing  # hueco registrado, no rellenado
    assert vals[1] is None
    assert ("D9", "formula_sin_cache") in flags, flags  # cache data_only ausente
    frag2 = ('<row xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" r="10">'
             + "".join(f'<c r="{L}10" t="n"><v>1</v></c>' for L in "ABCDEFGHIJ") + "</row>")
    vals2, missing2, flags2 = parse_row_cells(ET.fromstring(frag2), [])
    assert "K" in missing2 and not flags2, (missing2, flags2)  # fila corta rechazable
    print("parser negativos OK: hueco, formula_sin_cache, fila_corta")


def main():
    test_parser_negativos()
    gg_path = RAIZ / "data" / "integracion" / "fuentes" / f"{GG_SHA}.xlsx"
    ind_path = RAIZ / "data" / "integracion" / "fuentes" / f"{IND_SHA}.xlsx"
    assert sha256(gg_path) == GG_SHA and sha256(ind_path) == IND_SHA
    man = json.loads((RAIZ / "data" / "integracion" / "manifiesto.json").read_text(encoding="utf-8"))
    man_s = json.dumps(man)
    assert GG_SHA in man_s and IND_SHA in man_s, "origenes fijados en manifiesto"

    hdr_g, gg, rechazadas = parse_grandes_grupos(str(gg_path))
    assert hdr_g == ["CLAVE", "CLAVE_ENT", "NOM_ENT", "NOM_MUN", "SEXO", "AÑO",
                     "POB_00_11", "POB_12_29", "POB_30_59", "POB_60_mm", "POB_TOTAL"], hdr_g
    assert rechazadas == [], rechazadas  # cero huecos/formulas en el original real
    assert len(gg) == 7344, len(gg)  # n filas reales cuantificadas
    with zipfile.ZipFile(str(gg_path)) as z:
        n_f = z.read("xl/worksheets/sheet1.xml").decode("utf-8", errors="replace").count("<f ")
        assert n_f == 0 and "<f>" not in z.read("xl/worksheets/sheet1.xml").decode("utf-8", errors="replace"), \
            "el original no usa formulas: cache data_only ausente por construccion"
    sexos = {r[4] for _, r in gg}
    assert sexos == {"HOMBRES", "MUJERES"}, sexos
    anos_gg = {r[5] for _, r in gg}
    assert anos_gg == {str(a) for a in range(1990, 2041)}, "cobertura 1990-2040 OBSERVADA en GG"
    assert {r[1] for _, r in gg} == {"26"} and {r[2] for _, r in gg} == {"Sonora"}
    assert len({(r[0], r[4], r[5]) for _, r in gg}) == 7344, "clave (CLAVE,SEXO,ANO) unica"
    assert all(sum(map(int, r[6:10])) == int(r[10]) for _, r in gg), "suma grupos == POB_TOTAL 7344/7344"

    wb = openpyxl.load_workbook(str(ind_path), read_only=True, data_only=True)
    ws = wb["Sheet 1"]
    it = ws.iter_rows(values_only=False)
    hdr_row = next(it)
    hdr_i = [c.value for c in hdr_row]
    assert [str(c) for c in hdr_i[:5]] == ["CLAVE", "CLAVE_ENT", "NOM_ENT", "NOM_MUN", "AÑO"], hdr_i[:5]
    ind = []
    for row in it:
        assert len(row) >= 8
        ind.append((row[0].row, str(row[0].value), str(row[4].value), row[3].value, row[7].value))
    wb.close()
    assert len(ind) == 3672, len(ind)
    assert len({(c, a) for _, c, a, _, _ in ind}) == 3672, "clave (CLAVE,ANO) unica"
    anos_ind = {a for _, _, a, _, _ in ind}
    assert anos_ind == {str(a) for a in range(1990, 2041)}, "cobertura 1990-2040 OBSERVADA en IND"

    # Cruce NUEVO 2020 por (CLAVE,ANO) con agregacion SEXO previa. SQL en memoria.
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE gg (cod TEXT, anio TEXT, sexo TEXT, total INTEGER)")
    con.execute("CREATE TABLE ind (cod TEXT, anio TEXT, nom TEXT, pob INTEGER)")
    for _, r in gg:
        con.execute("INSERT INTO gg VALUES (?,?,?,?)", (r[0], r[5], r[4], int(r[10])))
    for _, c, a, n_, p in ind:
        con.execute("INSERT INTO ind VALUES (?,?,?,?)", (c, a, n_, p))
    u = con.execute("""SELECT g.cod, SUM(g.total), i.pob, i.nom
                       FROM gg g JOIN ind i ON i.cod = g.cod AND i.anio = g.anio
                       WHERE g.anio = '2020' GROUP BY g.cod""").fetchall()
    assert len(u) == 72, len(u)
    assert all(r[1] == r[2] for r in u), "POB_TOTAL(H+M) == POB_MIT_MUN en 72/72 (2020)"
    assert {r[0] for r in u} == {c for _, c, a, _, _ in ind if a == "2020"}
    nom_g = {r[0]: r[3] for _, r in gg if r[5] == "2020" and r[4] == "HOMBRES"}
    nom_i = {c: n_ for _, c, a, n_, _ in ind if a == "2020"}
    assert set(nom_g) == set(nom_i) and len(nom_g) == 72
    assert sum(1 for k in nom_g if nom_g[k] == nom_i[k]) == 72, "nombres literales 72/72"
    # Hechos sincronizados: cobertura observada 1990-2040 en ambos; SOLO 2020 cruzado en detalle.
    assert anos_gg == anos_ind == {str(a) for a in range(1990, 2041)}
    sin_filtro = con.execute("""SELECT COUNT(*) FROM gg g JOIN ind i
                                ON i.cod=g.cod AND i.anio=g.anio""").fetchone()[0]
    assert sin_filtro == 7344, sin_filtro  # cada fila IND casa con 2 SEXO: join total NO validado ano por ano
    u_anos = ["2020"]  # unico ano con verificacion de cobertura/nombres/coherencia

    # --- Negativos reales ---
    mult = con.execute("""SELECT COUNT(*) FROM gg g JOIN ind i ON i.cod = g.cod
                          WHERE g.anio='2020' AND i.anio='2020'""").fetchone()[0]
    assert mult == 144, mult  # sin agregar SEXO, el join multiplica x2
    cero = con.execute("""SELECT COUNT(*) FROM gg g JOIN ind i ON i.cod=g.cod AND i.anio=g.anio
                          WHERE g.anio='2020' AND i.anio='2021'""").fetchone()[0]
    assert cero == 0, cero  # periodo distinto no se toca con ANO en la clave
    falsos = con.execute("""SELECT COUNT(*) FROM
                            (SELECT DISTINCT cod FROM gg WHERE anio='2020') g
                            JOIN (SELECT DISTINCT cod FROM ind WHERE anio='2021') i ON i.cod=g.cod""").fetchone()[0]
    assert falsos == 72, falsos  # sin ANO daria 72 falsos: por eso es obligatoria
    dup = [(r[0], r[4], r[5]) for _, r in gg] + [(gg[0][1][0], gg[0][1][4], gg[0][1][5])]
    assert len(set(dup)) != len(dup), "el control debe detectar el duplicado"
    mv = json.loads((RAIZ / "propuestas" / "ronda-2" / "agente-4-vigencia" / "matriz-vigencia.json")
                    .read_text(encoding="utf-8"))
    refs = [r for r in mv["referencias"] if r["conjunto"] in
            ("943d0723-afbb-470a-8fe8-d62e8671de84", "960ef0a9-73ed-4191-ae0b-b868d7e48292")]
    assert len(refs) == 4 and all(r["f3_edicion"]["edicion_acreditada_externa"] is False for r in refs)

    # claves-2020.json: 72 agregados municipales con procedencia (sin datos personales).
    fila_ind = {}
    for filerow, c, a, _n, _p in ind:
        if a == "2020":
            fila_ind[c] = filerow
    fila_gg = {}
    for filerow, r in gg:
        if r[5] == "2020":
            fila_gg.setdefault(r[0], {})[r[4]] = filerow
    claves = []
    for r in sorted(u, key=lambda x: x[0]):
        cod = r[0]
        claves.append({"codigo_origen": cod, "anio": "2020",
                       "nombre_grandes_grupos": nom_g[cod], "nombre_indicadores": nom_i[cod],
                       "pob_total_h_m": r[1], "pob_mit_mun": r[2], "igualdad": bool(r[1] == r[2]),
                       "fuente_grandes_grupos": {"sha256": GG_SHA, "hoja": "Sheet 1",
                                                 "fila_hombres": fila_gg[cod]["HOMBRES"],
                                                 "fila_mujeres": fila_gg[cod]["MUJERES"]},
                       "fuente_indicadores": {"sha256": IND_SHA, "hoja": "Sheet 1",
                                              "fila": fila_ind[cod]}})
    assert len(claves) == 72 and all(c["igualdad"] for c in claves)
    (BASE / "fichas" / "claves-2020.json").write_text(
        json.dumps({"cruce": "Grandes grupos x Indicadores 2020 por (CLAVE,ANO)",
                    "anos_observados_ambos": "1990-2040", "anos_cruzados": ["2020"],
                    "filas": claves}, indent=1, ensure_ascii=False), encoding="utf-8")

    out = {
        "caso": "F2",
        "alcance": "Validacion NUEVA 2020 sobre originales fijados (7344 + 3672 filas reales leidas). "
                   "No reutiliza la inspeccion heuristica anterior como prueba (quedo refutada).",
        "fuentes": {"grandes_grupos": {"sha256": GG_SHA, "filas": 7344, "grano": "(CLAVE,SEXO,ANO)",
                                        "anos_observados": "1990-2040"},
                    "indicadores": {"sha256": IND_SHA, "filas": 3672, "grano": "(CLAVE,ANO)",
                                    "anos_observados": "1990-2040"}},
        "cruce_2020": {"claves": 72, "nombres_exactos": "72/72", "pob_coherente": "72/72",
                       "detalle": "fichas/claves-2020.json"},
        "serie": {"cobertura_observada_ambos": "1990-2040",
                  "cruce_ano_por_ano": "NO ejecutado",
                  "anos_cruzados": ["2020"]},
        "condiciones_verificadas": [
            "SHAs de originales == manifiesto ronda 1",
            "headers reales resueltos (CLAVE,CLAVE_ENT,NOM_ENT,NOM_MUN,SEXO/ANO,medidas)",
            "filas con 11 columnas ordenadas por coordenada; 0 huecos, 0 formulas en el original",
            "unicidad (CLAVE,SEXO,ANO) y (CLAVE,ANO); 72 claves identicas",
            "suma de grupos == POB_TOTAL en 7344/7344",
            "cruce 2020: cobertura 72/72, nombres 72/72, coherencia POB 72/72"],
        "condiciones_que_impiden_uso_interpretativo": [
            "vigencia de catalogos no_acreditada (F3/F4 ausentes): edition/aplicabilidad no demostrada",
            "cruce ano por ano 1990-2040 NO ejecutado; solo 2020 cruzado",
            "constructos distintos (suma de grupos vs mitad de ano): yuxtaposicion, no identidad de medida",
            "sin equivalencia INEGI afirmada; codigos literales coincidentes"],
        "decision": "exploratorio_con_condiciones_pendientes",
        "no_concluye": ["cruce ano por ano 1990-2040", "identidad de medida entre fuentes",
                        "equivalencia INEGI", "causalidad"]}
    (BASE / "fichas" / "F2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print("F2 OK (originales, cruce nuevo 2020)")


if __name__ == "__main__":
    main()
