"""Genera entrega.json + pendientes.json del especialista gobierno digital.

Lee (read-only): copia congelada fuentes/agente-9-gobierno-digital/,
insumos centrales y manifiesto. Escribe SOLO en
propuestas/cobertura-muse-20261023/gobierno-digital/.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
assert AQUI.name == "gobierno-digital", AQUI
ROOT = AQUI.parents[2]
assert (ROOT / "propuestas" / "cobertura-muse-20261023" / "fuentes" / "manifiesto.json").exists()

sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella  # noqa: E402
from integrar_contenido import valor  # noqa: E402

BASE = "https://example.org/mex-ontologi/"
ENTREGA = "propuestas/cobertura-muse-20261023/gobierno-digital/entrega.json"

FALTANTE = {
    "metadato-captura": "Nada: es metadato operativo de captura, no requiere significado documental.",
    "respuesta-abierta": "Dominio o catalogo publicado de respuestas, o dictamen del publicador que cierre el referente.",
    "generica-fragmento": "Literal autocontenido en el diccionario publicado.",
    "truncada-en-fuente": "Texto completo de la descripcion en el diccionario publicado.",
    "contradiccion-tipo-descripcion": "Aclaracion del publicador (tipo de dato o literal).",
    "contexto-dependiente-pregunta-previa": "Literal autocontenido o regla publicada de combinacion de preguntas.",
}

AJUSTE_ETIQUETA = {
    "acciones-mejora-competencias-humanas": "Acciones o estrategias de mejora de competencias humanas",
    "comite-colegiado-decisiones-tic": "Comite o cuerpo colegiado de decisiones TIC",
}

# Correccion integrador+auditor: existencia (P8) y nombre (P9) NO comparten concepto.
SPLIT_UNIDAD = {
    "existencia-unidad-coordinadora-tic": [
        "Unidad coordinadora de TIC existente",
        "La dependencia coordinadora declara contar con una unidad coordinadora de TIC (respuesta Si/No del Diagnostico del Entorno Digital, APE Sonora). Atributo de existencia declarada; no acredita nombre, organigrama ni adscripcion. Se distingue del nombre de la unidad (concepto separado: medida de atributo distinta de identificador nominal).",
        None],
    "nombre-unidad-coordinadora-tic": [
        "Nombre de la unidad coordinadora de TIC",
        "Nombre indicado de la unidad coordinadora de TIC (texto del Diagnostico del Entorno Digital, APE Sonora). Identificador nominal declarado; no acredita existencia operativa. Se distingue de la existencia de la unidad (concepto separado).",
        None],
}
REGLA_A_SPLIT = {"P8": "existencia-unidad-coordinadora-tic", "P9": "nombre-unidad-coordinadora-tic"}

# Redaccion atributo-solo-literal para los 3 casos con ejemplo contradictorio
DEFINICION_OVERRIDE = {
    "volumen-almacenamiento-neto-gb": (
        "Volumen neto de almacenamiento declarado para el datacenter, en la unidad indicada en el propio literal (GB). "
        "El diccionario declara tipo Numerico pero su ejemplo ('No') no es numerico; la contradiccion se conserva como limite tecnico y no se afirman valores."),
    "volumen-procesamiento-neto-cpus": (
        "Volumen neto de procesamiento declarado, en la unidad indicada en el propio literal (cantidad de CPUs). "
        "El diccionario declara tipo Numerico pero su ejemplo ('Si') no es numerico; la contradiccion se conserva como limite tecnico y no se afirman valores."),
    "presupuesto-anual-tic-sector-sin-rh": (
        "Presupuesto anual asignado del sector en materia TIC, excluyendo recursos humanos, segun el literal de la pregunta. "
        "El diccionario declara tipo Entero pero su ejemplo ('Platicas, reuniones, etc') no es numerico; la contradiccion se conserva como limite tecnico y no se afirman montos."),
}
LIMITE_TECNICO = {
    ("bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1", "P11"): "Contradiccion tecnica tipo<->ejemplo: tipo declarado Numerico frente a ejemplo 'No'; se capturan tipo+ejemplo en evidencia sin afirmar valores.",
    ("bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1", "P12"): "Contradiccion tecnica tipo<->ejemplo: tipo declarado Numerico frente a ejemplo 'Si'; se capturan tipo+ejemplo en evidencia sin afirmar valores.",
    ("8f8e3cfb-e551-4a95-b382-4999351c5f29", "P7"): "Contradiccion tecnica tipo<->ejemplo: tipo declarado Entero frente a ejemplo no numerico; se capturan tipo+ejemplo en evidencia sin afirmar montos.",
}

LIMITE_EXTRA = {
    ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d", "P16"): "El 'etc.' final deja abierto el catálogo de asuntos atendidos; la regla cubre la existencia del servicio.",
    ("af14d207-7697-4d52-b99b-46a35a1b76ac", "P16"): "El 'etc.' final deja abierto el catálogo de asuntos atendidos; la regla cubre la existencia del servicio.",
    ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d", "P29"): "El 'etc.' final deja abierto el alcance normativo; la regla cubre los rubros nombrados.",
    ("af14d207-7697-4d52-b99b-46a35a1b76ac", "P29"): "El 'etc.' final deja abierto el alcance normativo; la regla cubre los rubros nombrados.",
}


def main():
    fz = json.load(open(ROOT / "propuestas/cobertura-muse-20261023/fuentes/agente-9-gobierno-digital/propuestas.json", encoding="utf-8"))
    assert len(fz["decisiones"]) == 243 and len(fz["reglas"]) == 121 and len(fz["conceptos_nuevos"]) == 85

    # Recomputo de huellas desde inspeccion central (read-only) para no arrastrar errores
    insp = {}
    for d in {x["diccionario"] for x in fz["decisiones"]}:
        insp[d] = json.load(open(str(ROOT / "data/portal/inspecciones" / (d + ".json")), encoding="utf-8"))
    for x in fz["decisiones"]:
        rows = [r for r in insp[x["diccionario"]]["definiciones"] if str(r.get("Nombre variable")) == x["variable"]]
        assert len(rows) == 1, (x["diccionario"], x["variable"])
        assert huella(rows[0]) == x["huella_fila_diccionario"], (x["diccionario"], x["variable"])

    # Conceptos compartidos entre conjuntos -> calificador formal de instrumento
    usos = {}
    for r in fz["reglas"]:
        usos.setdefault(r["concepto"], set()).update(r["conjuntos"])
    compartidos = {c for c, cs in usos.items() if len(cs) > 1}
    assert compartidos, "se esperaba uso compartido entre instrumentos pares"

    conceptos = {}
    for slug, (label, definicion, padre) in fz["conceptos_nuevos"].items():
        if slug == "unidad-coordinadora-tic":
            continue
        if slug in DEFINICION_OVERRIDE:
            definicion = DEFINICION_OVERRIDE[slug]
        conceptos[slug] = [AJUSTE_ETIQUETA.get(slug, label), definicion, padre]
    for slug, triple in SPLIT_UNIDAD.items():
        conceptos[slug] = triple

    reglas = []
    for r in sorted(fz["reglas"], key=lambda x: x["id"]):
        dec = next(d for d in fz["decisiones"] if d.get("regla") == r["id"])
        key = (r["diccionarios"][0], r["nombres"][0])
        slug = REGLA_A_SPLIT.get(r["nombres"][0], r["concepto"]) if r["concepto"] == "unidad-coordinadora-tic" else r["concepto"]
        lims = [r["limite"]]
        if key in LIMITE_EXTRA:
            lims.append(LIMITE_EXTRA[key])
        if key in LIMITE_TECNICO:
            lims.append(LIMITE_TECNICO[key])
        cal = None
        if r["concepto"] in compartidos:
            cal = {"instrumento": dec.get("titulo_conjunto", "")}
            assert cal["instrumento"], r["id"]
        regla = {"id": r["id"], "concepto": slug, "representacion": r["representacion"],
                       "nombres": r["nombres"], "descripciones": r["descripciones"],
                       "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"],
                       "definiciones": r["definiciones"],
                       "huella_fila_diccionario": r["evidencia"][0]["huella_fila_diccionario"]
                       if "huella_fila_diccionario" in r["evidencia"][0] else dec["huella_fila_diccionario"],
                       "limites": lims,
                       "criterio": r["criterio"], "alcance": r["alcance"],
                       "positivo": r["positivo"], "contraejemplo": r["contraejemplo"],
                       "evidencia": r["evidencia"],
                       "fuente_revision": ENTREGA}
        if cal is not None:
            regla["calificador"] = cal
        reglas.append(regla)

    decisiones = []
    pendientes = []
    for d in sorted(fz["decisiones"], key=lambda x: x["definicion_iri"]):
        base = {"definicion_iri": d["definicion_iri"], "conjunto": d["conjunto"],
                "titulo_conjunto": d.get("titulo_conjunto", ""), "diccionario": d["diccionario"],
                "variable": d["variable"], "descripcion": d["descripcion"],
                "tipo_de_dato": d["tipo_de_dato"], "unidad_de_medida": d["unidad_de_medida"],
                "ejemplo_de_dato": d["ejemplo_de_dato"], "catalogo_de_referencia": d["catalogo_de_referencia"],
                "huella_fila_diccionario": d["huella_fila_diccionario"], "criterio": d["criterio"]}
        if d["veredicto"] == "propuesta":
            slug = REGLA_A_SPLIT.get(d["variable"], d["concepto"]) if d["concepto"] == "unidad-coordinadora-tic" else d["concepto"]
            decisiones.append({**base, "decision": "proponer", "regla_id": d["regla"],
                               "concepto": slug})
        else:
            decisiones.append({**base, "decision": "pendiente", "motivo": d["motivo"], "razon": d["razon"]})
            pendientes.append({"definicion_iri": d["definicion_iri"], "conjunto": d["conjunto"],
                               "titulo_conjunto": d.get("titulo_conjunto", ""), "diccionario": d["diccionario"],
                               "variable": d["variable"], "descripcion": d["descripcion"],
                               "motivo": d["motivo"], "razon": d["razon"],
                               "faltante": FALTANTE[d["motivo"]]})

    def sha(p):
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    mani = ROOT / "propuestas/cobertura-muse-20261023/fuentes/manifiesto.json"
    entrega = {"generado_en_utc": datetime.now(timezone.utc).isoformat(),
               "agente": "gobierno-digital (especialista, 243 definiciones agente 9)",
               "base_iri": BASE,
               "alcance": ("Particion exclusiva del agente 9: 243 definiciones fuera_del_nucleo_actual de 10 diccionarios "
                           "del Diagnostico del Entorno Digital (APE Sonora). Respuestas declaradas en encuesta, no hechos verificados. "
                           "Sin correspondencias columna-variable; sin sameAs/exactMatch."),
               "huellas_entrada": {
                   "manifiesto_fuentes": sha(mani),
                   "copia_agente9_propuestas": sha(ROOT / "propuestas/cobertura-muse-20261023/fuentes/agente-9-gobierno-digital/propuestas.json"),
                   "copia_agente9_resultado": sha(ROOT / "propuestas/cobertura-muse-20261023/fuentes/agente-9-gobierno-digital/resultado.md"),
                   "asignaciones_semanticas": sha(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json"),
                   "cobertura": sha(ROOT / "data/semantica/cobertura.json"),
                   "inspeccion": sha(ROOT / "data/portal/contenido-inspeccion.json"),
                   "inventario": sha(ROOT / "data/portal/inventario.json"),
                   "pendientes": sha(ROOT / "reports/pendientes-semanticos.json"),
                   "semantica": sha(ROOT / "ontologia/semantica.json")},
               "conceptos_nuevos": conceptos,
               "conceptos_reutilizados": [],
               "reglas": reglas,
               "decisiones": decisiones,
               "conteos": {"decisiones": len(decisiones),
                           "proponer": sum(1 for d in decisiones if d["decision"] == "proponer"),
                           "pendiente": sum(1 for d in decisiones if d["decision"] == "pendiente"),
                           "reglas": len(reglas), "conceptos_nuevos": len(conceptos)}}
    out = AQUI / "entrega.json"
    with io.open(str(out), "w", encoding="utf-8") as fh:
        json.dump(entrega, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with io.open(str(AQUI / "pendientes.json"), "w", encoding="utf-8") as fh:
        json.dump({"generado_en_utc": entrega["generado_en_utc"], "total": len(pendientes),
                   "pendientes": sorted(pendientes, key=lambda x: x["definicion_iri"])}, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(json.dumps(entrega["conteos"], indent=1))
    print("reglas con calificador:", sum(1 for r in reglas if "calificador" in r))


if __name__ == "__main__":
    main()
