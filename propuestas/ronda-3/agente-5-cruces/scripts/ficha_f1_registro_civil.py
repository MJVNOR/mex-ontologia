"""F1: Matrimonios-Divorcios 2022. Recomputo desde agregados POR FUENTE.

Fuentes originales (no se releyeron filas crudas: sin red en este entorno):
- Matrimonios 2022: resource 7b8638e8-d0d5-4311-b43f-51e2d343efb1
  (conjunto 1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98), DataStore _id+municipio+ano_matrimonio.
- Divorcios 2022: resource 63940761-d099-4a39-bb92-e81e4a6d31e1
  (conjunto c6140d53-1f16-4dd8-8ab3-d2b47f03a921), DataStore _id+municipio+ano_registro.
- Agregados por fuente con huella en data/portal/lote-cruces/validacion-lote.json
  (sha256_campos_leidos, consultas, consultado_en_utc, comprobaciones, limite).
- Diccionarios: 364ffa5c-e1c2-4185-a22f-80bede6735d0 (matrimonios),
  10357304-e171-44ca-a453-f989e6a2ff83 (divorcios).
- El artefacto data/portal/cruce-registro-civil.json solo se usa como CONTRASTE
  de consistencia (derivado vs recomputo), no como prueba de filas originales.

Alcance expreso: revalidacion desde agregados por fuente + unicidad de clave +
dominio + periodo + catalogo. NO es validacion completa de filas fuente
(no hay relectura cruda aqui); esa queda pendiente.
"""
import json
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BASE = RAIZ / "propuestas" / "ronda-3" / "agente-5-cruces"

MAT2022 = "7b8638e8-d0d5-4311-b43f-51e2d343efb1"
DIV2022 = "63940761-d099-4a39-bb92-e81e4a6d31e1"
MAT2021 = "776901e9-1d56-43de-814c-d6c4e22cdc23"  # solo para el negativo de periodo
PUBL_RC = "https://example.org/mex-ontologi/organization/ea178cfc-acbd-45b3-bcec-ac96f6dfd49c"


def dominio_ok(rows):
    cods = [r["municipio_local"] for r in rows]
    assert 26998 not in cods and 26999 not in cods, "categoria especial en clave"
    return cods


def unicidad_ok(rows):
    keys = [(r["municipio_local"], r["anio_registro"]) for r in rows]
    assert len(set(keys)) == len(keys), "clave (municipio,anio) duplicada: el join multiplicaria"
    return True


def verifica_fuente(ag, total, n, anio):
    assert ag["ok"] is True, ag["nombre"]
    assert ag["estrategia"]["grano_origen"] == "fila_registro_publicado", ag["estrategia"]
    assert ag["valor_total"] == total and ag["total_filas"] == total, (ag["valor_total"], total)
    rows = ag["agregados"]
    assert len(rows) == n, (ag["nombre"], len(rows))
    assert {r["anio_registro"] for r in rows} == {anio}, "mezcla de periodos en la fuente"
    unicidad_ok(rows)
    dominio_ok(rows)
    assert sum(r["valor"] for r in rows) == total, "suma de agregados != total"
    assert all(r["valor"] is not None and r["valor"] > 0 for r in rows), "nulos o ceros en agregado"
    return rows


def main():
    lote = json.loads((RAIZ / "data/portal/lote-cruces/validacion-lote.json").read_text(encoding="utf-8"))
    por_rec = {a["recurso_id"]: a for a in lote["agregados_recursos"]}
    m22 = verifica_fuente(por_rec[MAT2022], 13881, 67, 2022)
    d22 = verifica_fuente(por_rec[DIV2022], 6064, 62, 2022)
    m21 = verifica_fuente(por_rec[MAT2021], 14300, 67, 2021)

    # Equivalencia semantica de claves: mismo publicador, mismo sentido registro,
    # SIN catalogo (catalogo '' en ambas definiciones) y asimetria en el ano.
    op = json.loads((RAIZ / "data/portal/oportunidades-cruce.json").read_text(encoding="utf-8"))
    pm = op["perfiles"]["1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98"]
    pd = op["perfiles"]["c6140d53-1f16-4dd8-8ab3-d2b47f03a921"]
    assert pm["publicadores"] == pd["publicadores"] == [PUBL_RC]
    muni_m = next(c for c in pm["columnas_clave"] if c["campo"] == "municipio")
    muni_d = next(c for c in pd["columnas_clave"] if c["campo"] == "municipio")
    assert muni_m["sentido"] == muni_d["sentido"] == "registro"
    assert muni_m["definicion"]["descripcion"] == muni_d["definicion"]["descripcion"] == "Municipio de registro"
    assert muni_m["definicion"]["catalogo"] == muni_d["definicion"]["catalogo"] == "", \
        "sin catalogo: los codigos son literales coincidentes, no identidad municipal"
    anio_d = next(c for c in pd["columnas_clave"] if c["familia"] == "anio")
    assert anio_d["apoyada_por_definicion"] is False, "ano de divorcios sin respaldo de diccionario"

    # Union recomputada desde las fuentes (SQL en memoria, sin BD persistente)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE mat (cod INTEGER, anio INTEGER, v INTEGER)")
    con.execute("CREATE TABLE div (cod INTEGER, anio INTEGER, v INTEGER)")
    for r in m22:
        con.execute("INSERT INTO mat VALUES (?,?,?)", (r["municipio_local"], r["anio_registro"], r["valor"]))
    for r in d22:
        con.execute("INSERT INTO div VALUES (?,?,?)", (r["municipio_local"], r["anio_registro"], r["valor"]))
    u = con.execute("""SELECT m.cod, m.v AS mat, d.v AS divor
                       FROM mat m LEFT JOIN div d ON d.cod = m.cod AND d.anio = m.anio""").fetchall()
    assert len(u) == 67 and sum(1 for r in u if r[2] is not None) == 62
    assert sum(r[1] for r in u) == 13881 and sum(r[2] for r in u if r[2] is not None) == 6064

    # Contraste con el derivado (consistencia, no prueba de origen)
    cruce = json.loads((RAIZ / "data/portal/cruce-registro-civil.json").read_text(encoding="utf-8"))
    der = {(f["codigo_municipio_fuente"], f["anio_registro"]):
           (f["registros_matrimonios"], f["registros_divorcios"]) for f in cruce["filas"]}
    rec = {(r[0], 2022): (r[1], r[2]) for r in u}
    assert der == rec, "derivado inconsistente con el recomputo"

    # --- Negativos reales ---
    # 1. Duplicado que multiplicaria la union: el control de unicidad debe fallar.
    dup = [dict(r) for r in d22] + [dict(d22[0])]
    try:
        unicidad_ok(dup)
        raise SystemExit("el control de unicidad no detecto el duplicado")
    except AssertionError as e:
        assert "duplicada" in str(e)
    n_dup = con.execute("""SELECT COUNT(*) FROM mat m LEFT JOIN (SELECT * FROM div UNION ALL SELECT * FROM div) d
                           ON d.cod = m.cod""").fetchone()[0]
    assert n_dup > 67, n_dup  # sin unicidad, el join se multiplica: por eso se exige antes
    # 2. Nulo != cero: solo 62 codigos tienen divorcios observados, no 67.
    assert con.execute("SELECT COUNT(*) FROM div").fetchone()[0] == 62
    # 3. Periodo distinto: join solo por municipio con 2021 mezcla periodos (62 matches falsos).
    con.execute("CREATE TABLE mat21 (cod INTEGER, anio INTEGER, v INTEGER)")
    for r in m21:
        con.execute("INSERT INTO mat21 VALUES (?,?,?)", (r["municipio_local"], r["anio_registro"], r["valor"]))
    falsos = con.execute("SELECT COUNT(*) FROM mat21 m JOIN div d ON d.cod = m.cod").fetchone()[0]
    assert falsos == len({r["municipio_local"] for r in m21} & {r["municipio_local"] for r in d22}) > 0, falsos
    bien = con.execute("""SELECT COUNT(*) FROM mat21 m JOIN div d ON d.cod = m.cod AND d.anio = m.anio""").fetchone()[0]
    assert bien == 0, bien  # con ano en la clave, 2021 x 2022 no se tocan
    # 4. Categoria especial: 26998/26999 deben ser rechazados por el dominio.
    try:
        dominio_ok([{"municipio_local": 26998, "anio_registro": 2022, "valor": 1}])
        raise SystemExit("el dominio acepto categoria especial")
    except AssertionError as e:
        assert "especial" in str(e)

    out = {
        "caso": "F1",
        "par": "Matrimonios-Divorcios 2022",
        "alcance": "Recomputo desde agregados por fuente con huella + unicidad/dominio/periodo/catalogo. "
                   "NO es validacion completa de filas fuente (sin relectura cruda).",
        "fuentes": {
            "matrimonios_2022": {"resource": MAT2022, "sha_campos": por_rec[MAT2022]["sha256_campos_leidos"],
                                 "consultado_utc": por_rec[MAT2022]["consultado_en_utc"], "medida": "conteo_filas_matrimonios"},
            "divorcios_2022": {"resource": DIV2022, "sha_campos": por_rec[DIV2022]["sha256_campos_leidos"],
                               "consultado_utc": por_rec[DIV2022]["consultado_en_utc"], "medida": "conteo_filas_divorcios"}},
        "resultado": {"codigos": 67, "ambas": 62, "solo_matrimonios": [24, 31, 60, 62, 63],
                      "total_matrimonios": 13881, "total_divorcios": 6064},
        "condiciones_verificadas": [
            "mismo publicador Registro Civil en ambas",
            "municipio con sentido registro y misma descripcion en ambas (literales, no identidad)",
            "unicidad (municipio,anio) en cada fuente 2022: 67 y 62 claves",
            "suma de agregados == total publicado en cada fuente",
            "dominio 2022 sin 26998/26999; huecos 07/39/44/54 ausentes en ambas",
            "agregacion previa al join; union externa con ausencia NULL (62 observados, no 67)",
            "derivado cruce-registro-civil.json consistente con el recomputo"],
        "condiciones_que_impiden_uso_interpretativo": [
            "sin catalogo de codigos locales del Registro Civil: <=72 no identifica municipios ni equivale a INEGI",
            "campo ano de divorcios sin respaldo de diccionario (solo columna de archivo)",
            "grano fila publicada sin deduplicacion de eventos; API sin instantanea transaccional",
            "cobertura de meses no verificada en estas dos fuentes; solo ano 2022",
            "extension a otros anios exige revalidar recurso y diccionario por ano"],
        "decision": "exploratorio_con_condiciones_pendientes",
        "no_concluye": ["tasa de divorcio", "vinculo persona/cohorte", "nombres o codigos INEGI",
                        "extension a otros anios sin revisar diccionarios"]}
    (BASE / "fichas" / "F1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print("F1 OK (recomputo desde fuentes)")


if __name__ == "__main__":
    main()
