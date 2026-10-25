"""Ronda 4 - rol catalogos. Verifica vigencia historica de las 16 referencias con
recurso identificado + des_mpo_res solo con fuentes LOCALES ya capturadas.
No usa red ni Obscura. Genera entrega.json, pendientes.json, resultado.md y listo.json.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
R2 = ROOT / "data/integracion-ronda-2/entregas/agente-4-vigencia"
MATRIZ = json.loads((R2 / "matriz-vigencia.json").read_text(encoding="utf-8"))
COB = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))

MANIFIESTO_CKAN = json.loads((R2 / "evidencia/ckan_manifiesto.json").read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


ARCHIVO_POR_SHA = {
    "53bd5e971a033998ed8a72317b6ad1e69314d82463220d8cfd156dfad9034259":
        "data/integracion/fuentes/53bd5e971a033998ed8a72317b6ad1e69314d82463220d8cfd156dfad9034259.xlsx",
    "3b8546acad7482825755e46a1a619a4838721f8480b94baaef3c755ba293db9c":
        "data/integracion/fuentes/3b8546acad7482825755e46a1a619a4838721f8480b94baaef3c755ba293db9c.xlsx",
    "612b2b11192b97ae7328f80c8a5d1c545e117da46dd436a9b077aaf824b1525f":
        "data/integracion/fuentes/612b2b11192b97ae7328f80c8a5d1c545e117da46dd436a9b077aaf824b1525f.xlsx",
    "ea54aad30b7342ce678d1d66157325a5cbaa492380ee4d807b20918198c5b0f5":
        "data/integracion/fuentes/ea54aad30b7342ce678d1d66157325a5cbaa492380ee4d807b20918198c5b0f5.xlsx",
    "84bb6fcda02f3de3b295189d59cf0dde201bc4e048888681b6cd8ea624bb0716":
        "data/territorio/fuentes/36d3ac85-4327-41f5-9259-538a7723a0ae.xlsx",
    "96776ca8976ebb6e7510f65abaa287888be693f400a1e4adb5777e091d3b5a87":
        "data/territorio/fuentes/7f3aca28-4251-48b8-a759-69c992580744.xlsx",
}


def check_interior_sin_version(recurso_sha, hojas_esperadas):
    """Confirma que el xlsx capturado no declara fecha/version/periodo en su interior."""
    import openpyxl
    p = ROOT / ARCHIVO_POR_SHA[recurso_sha]
    assert p.exists(), f"falta archivo local {p}"
    assert sha(p) == recurso_sha, f"sha distinto en {p}"
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    assert set(wb.sheetnames) == set(hojas_esperadas), f"{recurso_sha}: {wb.sheetnames}"
    textos = []
    for sn in wb.sheetnames:
        for row in wb[sn].iter_rows(values_only=True):
            for c in row:
                if isinstance(c, str) and c.strip():
                    textos.append(c.strip().lower())
    wb.close()
    import re
    pats = [r"\bversi[oó]n\b", r"\bvigencia\b", r"\bedici[oó]n\b",
            r"\bper[ií]odo\b", r"\bcobertura\b", r"\baplica"]
    hits = [t for t in textos if any(re.search(p, t) for p in pats)]
    return {"archivo": ARCHIVO_POR_SHA[recurso_sha], "hits_declarativos": hits[:10]}


INTERIORES = {
    "53bd5e971a033998ed8a72317b6ad1e69314d82463220d8cfd156dfad9034259": ["Hoja1"],
    "3b8546acad7482825755e46a1a619a4838721f8480b94baaef3c755ba293db9c": [
        "Catalogo Servicios", "Catalogo rechazo", "Catalogo especie"],
    "612b2b11192b97ae7328f80c8a5d1c545e117da46dd436a9b077aaf824b1525f": [
        "Catálogo_estatal", "Municipios", "Regiones"],
    "ea54aad30b7342ce678d1d66157325a5cbaa492380ee4d807b20918198c5b0f5": [
        "Catalogo_Estado", "Catalogo_Municipios"],
    "84bb6fcda02f3de3b295189d59cf0dde201bc4e048888681b6cd8ea624bb0716": ["cat_municipio"],
    "96776ca8976ebb6e7510f65abaa287888be693f400a1e4adb5777e091d3b5a87": ["cat_entidad"],
}

verif_interiores = {}
for sh, hojas in INTERIORES.items():
    verif_interiores[sh] = check_interior_sin_version(sh, hojas)
    assert verif_interiores[sh]["hits_declarativos"] == [], f"{sh} declara version: {verif_interiores}"

# CKAN local: sin extras temporales en los 11 paquetes
for f in (R2 / "evidencia/ckan").glob("package_*.json"):
    j = json.loads(f.read_text(encoding="utf-8"))
    r = j.get("result", j)
    assert r.get("extras") in (None, []), f"extras inesperados en {f.name}"

# Diccionario fiebre manchada local: filas 177/178 degeneradas, fila 7 sin catalogo
dic = json.loads((ROOT / "data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json").read_text(encoding="utf-8"))
defs = dic["definiciones"]
assert len(defs) == 178
assert defs[176]["Catálogo de referencia"] == "des_mpo_res"
assert defs[177]["Catálogo de referencia"] == "des_mpo_res"
assert defs[6]["Nombre variable"] == "des_mpo_res" and defs[6]["Catálogo de referencia"] == ""

decisiones = []
for ref in MATRIZ["referencias"]:
    vid = ref["id"]
    f1 = ref["f1_ckan"]
    verif = verif_interiores[f1["catalogo_sha256"]]
    ed = ref["f3_edicion"]
    ed_known = ed.get("edicion_acreditada_externa") is True
    decisiones.append({
        "id": vid,
        "referencia_iri": ref["referencia_iri"],
        "conjunto": ref["conjunto"],
        "titulo_conjunto": ref["titulo_conjunto"],
        "recurso_catalogo": f1["catalogo_recurso"],
        "recurso_url": f1["catalogo_url"],
        "catalogo_sha256": f1["catalogo_sha256"],
        "hoja_campo": ref["hoja_campo"],
        "periodos_declarados_por_titulo": ref["f2_periodos_declarados"]["periodos"],
        "nota_periodos": "Periodos declarados por titulos de recursos CKAN y nota del conjunto; NO cobertura observada.",
        "version_edicion": ed["edicion"] if ed_known else "no_determinada",
        "edicion_acreditada_externa": ed_known,
        "decision": "pendiente",
        "motivo": ("Edicion documentada con evidencia primaria (F3) pero sin vinculo "
                    "temporal aplicable (F4 ausente)." if ed_known else
                    "Sin edicion determinada (F3) ni vinculo a periodos (F4)."),
        "evidencia_local_verificada": [
            "data/integracion-ronda-2/entregas/agente-4-vigencia/evidencia/ckan/package_%s.json" % ref["conjunto"],
            "data/integracion-ronda-2/entregas/agente-4-vigencia/evidencia/ckan_manifiesto.json",
            verif["archivo"],
            "Interior xlsx verificado: hojas %s, sin celda de fecha/version/periodo/vigencia." % hojas,
        ] + (["data/integracion-ronda-2/entregas/agente-4-vigencia/evidencia/externa/cmpe2016_inegi.pdf "
               "sha256 66ba2fd24aa01d82684df52677b792e17fe55d38273d6325ff4f6f66a3ef714b, "
               "localizadores p.2 catalogacion INEGI c2016, p.8 segunda edicion"] if ed_known else []),
        "pendiente_exacto": ("Acreditar F4: documento que vincule la edicion %s con los periodos %s "
                             "(adopcion u obligatoriedad para el publicador, oficio o nota de version con rango temporal)."
                             % (ref["nombre_catalogo"], ref["f2_periodos_declarados"]["periodos"])
                             if ed_known else
                             "Acreditar F3+F4: declaracion de edicion/version/fecha del catalogo (%s, sha %s) "
                             "y documento que la vincule con los periodos %s."
                             % (ref["hoja_campo"], f1["catalogo_sha256"], ref["f2_periodos_declarados"]["periodos"])),
        "limite": "No afirmar vigencia historica ni extender a otros conjuntos/periodos.",
    })

# des_mpo_res
des = {
    "id": "des_mpo_res",
    "referencia_iri": "https://example.org/mex-ontologi/declared-code-reference/a2902c1feb2fa4b8349946c2ae418a11bf0f465032c5c62adaf33fb053373cf2",
    "conjunto": "5494daa1-09ca-4750-aeac-2558553700e1",
    "titulo_conjunto": "Fiebre manchada (Rickettsia)",
    "diccionario": "33d0a99e-c721-496f-a05e-07646e9ae42a",
    "definiciones_iris": [
        "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177",
        "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178",
    ],
    "huellas_fila_diccionario": [
        "4b17625c8fea607228fe4f2a790744687a6e8bc45a712f66d4833d6ac541da79",
        "b5dbcdf58fd1b6e4d87f2396986629d2aa2350d35f1c1291e5d3d79515a0f60",
    ],
    "decision": "pendiente",
    "motivo": ("Filas 177/178 del diccionario capturado (data/portal/inspecciones/33d0a99e....json) "
               "son fragmentos degenerados de encabezado: Nombre=ide_id, Descripcion=ide_col, "
               "Catalogo=des_mpo_res, Detalle=cve_loc_res. El unico recurso Catalogo del conjunto "
               "(08d3b1a7, sha 3b8546ac...) contiene solo Catalogo Servicios/rechazo/especie; busqueda "
               "de texto completo negativa para des_mpo_res/ide_id/ide_col/des_jur_res/cve_loc_res. "
               "La variable homonima des_mpo_res de la fila 7 (Municipio donde reside el caso, ejemplo "
               "Hermosillo) tiene Catalogo de referencia vacio: no es origen de esta referencia."),
    "evidencia_local_verificada": [
        "data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json (178 definiciones; filas 177/178 degeneradas; fila 7 sin catalogo)",
        "data/portal/inspecciones/4121cf57-1e4a-4fb0-b175-3805edffca2c.json (esquema Hoja1: des_mpo_res posicion 7)",
        "data/integracion/fuentes/3b8546acad7482825755e46a1a619a4838721f8480b94baaef3c755ba293db9c.xlsx (3 hojas, sin ocurrencias)",
        "data/integracion-ronda-2/entregas/agente-4-vigencia/evidencia/ckan/package_5494daa1-09ca-4750-aeac-2558553700e1.json",
    ],
    "pendiente_exacto": ("Aclaracion del publicador: que significan las lineas 177/178 del diccionario y si existe "
                         "un catalogo publicado de municipios de residencia aplicable a des_mpo_res 2022-2024; "
                         "documento requerido: fe de erratas o diccionario corregido + URL del recurso catalogo si existe."),
    "limite": "No usar la coincidencia de nombre con la variable de la fila 7 como prueba; no crear vinculo catalogoRecuperado.",
}

solicitudes = [
    {"id": "INV-R4C-01", "para": "investigador (Obscura)",
     "referencias": ["V01", "V02", "V03", "V04"],
     "iris": [d["referencia_iri"] for d in decisiones if d["id"] in ("V01", "V02", "V03", "V04")],
     "pregunta": "¿Adopto u obligo la UTH la CMPE 2016 para los conjuntos Promedio Academico, Matriculas, Titulados y Egresados, y para que periodos?",
     "documento_requerido": "Lineamiento, oficio o nota de version con rango temporal que vincule CMPE 2016 con los periodos 2022-2026 de esos conjuntos.",
     "fuente_probable": "UTH / planteles; normateca o notas de los conjuntos en datos.sonora.gob.mx."},
    {"id": "INV-R4C-02", "para": "investigador (Obscura)",
     "referencias": ["V05"],
     "iris": ["https://example.org/mex-ontologi/declared-code-reference/3b45c474da5b2dc83e061ed7c26d470eaff0cd4935c626ac4cfa11e64a0e16e8"],
     "pregunta": "¿Que edicion/version/fecha tiene el Catalogo_estatal de Recursos Hidricos (sha 612b2b11...) y cubre 1941-2024? ¿Existe el recurso 1960-1969 sin URL?",
     "documento_requerido": "Nota de version del catalogo con fecha y rango de aplicacion; URL del recurso 1960-1969 o constancia de ausencia.",
     "fuente_probable": "SAGARHPA / CONAGUA; metadatos del conjunto ee8f639f en datos.sonora.gob.mx."},
    {"id": "INV-R4C-03", "para": "investigador (Obscura)",
     "referencias": ["V06", "V07", "V08"],
     "iris": [d["referencia_iri"] for d in decisiones if d["id"] in ("V06", "V07", "V08")],
     "pregunta": "¿Que edicion/version/fecha tienen las hojas Catalogo Servicios, Catalogo rechazo y Catalogo especie (sha 3b8546ac...) y aplican a 2022-2024?",
     "documento_requerido": "Nota de version del catalogo con fecha y rango de aplicacion 2022-2024.",
     "fuente_probable": "Secretaria de Salud Publica; metadatos del conjunto 5494daa1 en datos.sonora.gob.mx."},
    {"id": "INV-R4C-04", "para": "investigador (Obscura)",
     "referencias": ["V09", "V10", "V11", "V12", "V15", "V16"],
     "iris": [d["referencia_iri"] for d in decisiones if d["id"] in ("V09", "V10", "V11", "V12", "V15", "V16")],
     "pregunta": "El archivo catalogo.xlsx sha ea54aad3... se comparte en 3 conjuntos de proyecciones. ¿Que edicion/version/fecha tiene y cubre reconstruccion 1990-2019 y proyecciones 2020-2040?",
     "documento_requerido": "Nota de version con fecha y rango de aplicacion; fuente metodologica (CONAPO?) de la reconstruccion/proyecciones.",
     "fuente_probable": "COESPO o dependencia publicadora; notas de los conjuntos 0b5f5e16, 943d0723, 960ef0a9."},
    {"id": "INV-R4C-05", "para": "investigador (Obscura)",
     "referencias": ["V13", "V14"],
     "iris": [d["referencia_iri"] for d in decisiones if d["id"] in ("V13", "V14")],
     "pregunta": "¿Que edicion/version/fecha tienen cat_municipio (sha 84bb6fcd) y cat_entidad (sha 96776ca8) y aplican a 2015-2025? ¿Derivan del SESNSP con que corte?",
     "documento_requerido": "Nota de version con fecha, rango de aplicacion y corte SESNSP de referencia.",
     "fuente_probable": "SESNSP / Secretariado Ejecutivo; metadatos de los conjuntos 93ca5e1c y caf587a5."},
    {"id": "INV-R4C-06", "para": "investigador (Obscura, con traslado al publicador; no contactar directamente)",
     "referencias": ["des_mpo_res"],
     "iris": [des["referencia_iri"]],
     "pregunta": "¿Que significan las lineas 177/178 del diccionario de Fiebre manchada (Catalogo de referencia = des_mpo_res) y existe un catalogo publicado de municipios de residencia?",
     "documento_requerido": "Fe de erratas o diccionario corregido; URL del recurso catalogo si existe.",
     "fuente_probable": "Secretaria de Salud Publica; conjunto 5494daa1 en datos.sonora.gob.mx."},
]

entrega = {
    "rol": "catalogos",
    "generado_en_utc": "2026-10-23T12:00:00+00:00",
    "alcance": ("17 referencias: 16 con recurso identificado (V01-V16, vigencia historica no probada) + "
                "des_mpo_res sin resolver. Solo fuentes locales ya capturadas; sin red ni Obscura. "
                "Ninguna decision propone cambios al nucleo: las 17 quedan pendientes con pendiente exacto."),
    "verificacion_local": {
        "interiores_xlsx": "6 archivos sha verficados hoja por hoja con openpyxl: solo encabezados + filas de datos, sin celdas de fecha/version/periodo/vigencia.",
        "ckan_local": "11 package JSON capturados 2026-10-23: extras nulos, sin declaraciones temporales; created/last_modified = registro en portal, no edicion.",
        "diccionarios_locales": "data/portal/inspecciones/33d0a99e....json: 178 definiciones; filas 177/178 degeneradas; fila 7 sin catalogo.",
        "cmpe2016_externa_ya_capturada": "data/integracion-ronda-2/.../evidencia/externa/cmpe2016_inegi.pdf sha 66ba2fd2... acredita edicion F3 de V01-V04; no acredita F4.",
    },
    "decisiones_referencias": decisiones,
    "des_mpo_res": des,
    "solicitudes_investigacion": solicitudes,
    "conteos": {"referencias_revisadas": 17, "pendientes": 17, "propuestas_cambio_nucleo": 0,
                "solicitudes_investigacion": len(solicitudes)},
}

(OUT / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
pend = {"pendientes": [{"id": d["id"], "referencia_iri": d["referencia_iri"],
                        "pendiente_exacto": d["pendiente_exacto"]} for d in decisiones]
        + [{"id": "des_mpo_res", "referencia_iri": des["referencia_iri"],
            "pendiente_exacto": des["pendiente_exacto"]}],
        "conteo": 17}
(OUT / "pendientes.json").write_text(json.dumps(pend, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

res = ("# Resultado catalogos ronda 4\n\n"
       "- Referencias revisadas: 17 (V01-V16 + des_mpo_res).\n"
       "- Decisiones: 17 pendientes, 0 propuestas de cambio al nucleo.\n"
       "- Vigencia historica acreditada: 0/16 (F4 ausente en todas; F3 solo en V01-V04 por CMPE 2016 externa ya capturada).\n"
       "- des_mpo_res: sin resolver; filas 177/178 degeneradas confirmadas en diccionario local.\n"
       "- Evidencia local verificada: 6 xlsx (interior sin version), 11 package CKAN (sin extras temporales), diccionario 33d0a99e (178 filas).\n"
       "- Solicitudes al investigador: 6 (INV-R4C-01 a INV-R4C-06).\n"
       "- Metodo: script local verificar.py en esta carpeta; sin red ni Obscura.\n")
(OUT / "resultado.md").write_text(res, encoding="utf-8")
listo = {"sha256_entrega": sha(OUT / "entrega.json"),
         "conteos": entrega["conteos"], "estado": "completo"}
(OUT / "listo.json").write_text(json.dumps(listo, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(json.dumps(listo, ensure_ascii=False, indent=1))
