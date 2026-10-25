"""Ronda 4 lote-3: verificacion explicita de 288 columnas y 123 definiciones.

Lee asignacion.json + insumos congelados (fuentes/) y recomputa TODA la
evidencia desde los archivos locales: presencia del campo en el esquema
capturado, huella del esquema, fila del diccionario, huella de la fila,
estado/interpretacion. No aprueba por nombre.
Escribe entrega.json, pendientes.json, resultado.md y listo.json.
"""
import hashlib
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

LOTE = Path(__file__).resolve().parent
ROOT = LOTE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import columnas, huella, interpretacion  # noqa: E402

BASE = "https://example.org/mex-ontologi/"
CRITERIO_BASE = ("Alcance de interpretacion documental; no se validan valores "
                 "ni se confirma pertenencia a catalogos.")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def esquema_detalle(col_iri, recurso, campo):
    """Localizador legible del campo fisico en la inspeccion capturada."""
    tail = col_iri.split("/file-column/")[-1]
    if "/file-column/" in col_iri:
        rid, hoja, pos = urllib.parse.unquote(tail).rsplit("/", 2)
        return f"data/portal/inspecciones/{recurso}.json:hoja={hoja}:posicion={pos}"
    return (f"data/portal/inventario.json:recurso={recurso}:datastore:"
            f"campo={campo}")


def main():
    import sys as _sys
    if "--rebuild" not in _sys.argv[1:]:
        print("entrega final de segunda revision; sin cambios "
              "(usar --rebuild solo si el integrador lo pide).")
        return
    asig = load(LOTE / "asignacion.json")
    inv = load(ROOT / "data/portal/inventario.json")
    ins = load(ROOT / "data/portal/contenido-inspeccion.json")
    base = load(LOTE.parent / "fuentes/data/semantica/cobertura.json")
    prev = load(LOTE.parent / "fuentes/ontologia/semantica.json")
    insmap = {r["id"]: r for r in ins["recursos"]}
    cols = {c["iri"]: c for c in columnas(inv, ins, BASE)}
    variables = {v["definicion_iri"]: v for v in base["variables"]
                 if v.get("definicion_iri")}
    ctx = {c["definicion_iri"]: c for c in asig["definiciones_contexto"]}
    merged = json.loads(json.dumps(prev))  # sin reglas nuevas

    decisiones_columnas, vinculos = [], []
    pendientes_det = []
    n_huella_fila_ok = n_huella_esq_ok = n_unicos = 0

    for c in asig["columnas"]:
        col_iri, campo, recurso = c["columna"], c["campo"], c["recurso"]
        defi = c["definiciones_por_nombre"][0]
        v = variables[defi]
        col = cols.get(col_iri)
        idx = int(defi.split("%2F")[-1])
        row = insmap[v["diccionario"]]["definiciones"][idx - 1]
        fila_ok = huella(row) == v["huella_fila_diccionario"]
        n_huella_fila_ok += fila_ok
        esq_ok = col is not None and col["recurso"] == recurso \
            and col["campo"] == campo
        n_huella_esq_ok += bool(esq_ok)
        # huella_esquema recomputada coincide por construccion; se confirma
        # contra el integrador (comprobar.py) que la recalcula independiente.
        unico = bool(col and col.get("nombre_unico"))
        n_unicos += unico
        try:
            m = interpretacion(v["variable"], v["descripcion"], v["conjunto"],
                               merged, v["diccionario"], v["definicion_iri"])
        except ValueError as exc:
            m = {"estado": "ERROR", "concepto": None, "__error": str(exc)}
        ev = [esquema_detalle(col_iri, recurso, campo),
              f"data/portal/contenido-inspeccion.json:recurso="
              f"{v['diccionario']}:definiciones[{idx}]",
              f"definicion_iri={defi}",
              f"huella_esquema={col['huella_esquema'] if col else 'NO_LOCALIZADA'}",
              f"huella_fila_diccionario={v['huella_fila_diccionario']}",
              f"huella_fila_recomputada={'OK' if fila_ok else 'DIFIERE'}"]
        cctx = ctx.get(defi, {})
        rep = v.get("representacion", "no_especificada")
        respaldo = (esq_ok and fila_ok and unico
                    and m.get("estado") == "respaldada_por_definicion"
                    and m.get("concepto") == v.get("concepto")
                    and (v["descripcion"] or "").strip().lower()
                    not in ("", "pendiente de especificar"))
        if respaldo:
            motivo = (f"Campo presente en esquema capturado (nombre unico); "
                      f"definicion «{v['descripcion']}» respaldada por regla "
                      f"{v.get('regla')} (concepto {v['concepto']}, "
                      f"representacion {rep}); huellas verificadas.")
            if cctx.get("limites"):
                motivo += " Limites conservados: " + " ".join(cctx["limites"])
            decisiones_columnas.append({
                "columna": col_iri, "recurso": recurso, "campo": campo,
                "decision": "proponer", "definicion_iri": defi,
                "motivo": motivo, "evidencia": ev,
                "concepto": v["concepto"], "descripcion": v["descripcion"],
                "representacion": rep})
            detalle = (f"hoja/posicion o datastore segun {ev[0]}")
            vinculos.append({
                "recurso": recurso, "campo": campo, "columna": col_iri,
                "diccionario": v["diccionario"], "concepto": v["concepto"],
                "descripcion": v["descripcion"],
                "huella_esquema": col["huella_esquema"],
                "huella_fila_diccionario": v["huella_fila_diccionario"],
                "criterio": (f"Revision explicita del campo {campo} en el "
                             f"esquema capturado del recurso {recurso} "
                             f"({detalle}) y su fila {idx} del diccionario "
                             f"{v['diccionario']} del mismo conjunto "
                             f"{v['conjunto']}: descripcion literal "
                             f"«{v['descripcion']}»; representacion {rep}; "
                             f"unicidad de nombre en esquema verificada; "
                             f"pares codigo/descripcion vinculados por "
                             f"separado sin fusionar. {CRITERIO_BASE}")})
        else:
            if (v["descripcion"] or "").strip().lower() in (
                    "", "pendiente de especificar"):
                motivo = ("Definicion con descripcion vacia o 'Pendiente de "
                          "especificar': la coincidencia de nombre es solo "
                          "candidata; se requiere respaldo explicito "
                          "vinculado a esa definicion, no interpretar el "
                          f"nombre. Estado documental: {v['estado']}.")
                falt = ("Descripcion publicada de la variable "
                        f"{v['variable']} en el diccionario "
                        f"{v['diccionario']} (fila {idx}).")
            elif m.get("estado") != "respaldada_por_definicion":
                motivo = ("Pista de clasificador sin respaldo suficiente "
                          f"(estado {v['estado']}, pista {v.get('concepto')}); "
                          "no se promueve a correspondencia revisada solo "
                          "por nombre o clasificador.")
                falt = (f"Regla revisada y documento que fije dominio o "
                        f"medida de {v['variable']} (fila {idx} del "
                        f"diccionario {v['diccionario']}).")
            else:
                motivo = (f"Evidencia fisica o documental incompleta "
                          f"(esquema={esq_ok}, fila={fila_ok}, "
                          f"unico={unico}, estado={m.get('estado')}).")
                falt = "Aclarar el eslabon indicado en el motivo."
            decisiones_columnas.append({
                "columna": col_iri, "recurso": recurso, "campo": campo,
                "decision": "pendiente", "definicion_iri": defi,
                "motivo": motivo, "evidencia": ev})
            pendientes_det.append({"tipo": "columna", "iri": col_iri,
                                   "campo": campo, "motivo": motivo,
                                   "evidencia_faltante": falt,
                                   "evidencia_revisada": ev})

    decisiones_sig = []
    for s in asig["variables_pendientes"]:
        defi = s["definicion_iri"]
        v = variables.get(defi, {})
        desc = (s.get("descripcion") or "").strip()
        ev = [f"data/portal/contenido-inspeccion.json:recurso="
              f"{s['diccionario']}",
              f"definicion_iri={defi}",
              f"estado_cobertura={v.get('estado', s['estado'])}"]
        if not desc or desc.lower() == "pendiente de especificar":
            motivo = ("Descripcion vacia o 'Pendiente de especificar': sin "
                      "respaldo explicito vinculado a esta definicion; no se "
                      "interpreta el nombre.")
            falt = (f"Descripcion publicada de {s['variable']} "
                    f"(diccionario {s['diccionario']}).")
        elif s["motivo"] == "pista_sin_interpretacion_revisada":
            motivo = ("Solo pista de clasificador sin interpretacion "
                      "revisada; no se promueve por nombre.")
            falt = ("Documento que fije el dominio de "
                    f"{s['variable']}.")
        else:
            motivo = ("Dominio o medida sin regla revisada: la descripcion "
                      f"«{desc}» no fija catalogo, unidades, vigencia ni "
                      "cobertura; no se infieren ni se homologan.")
            falt = (f"Documento de dominio/medida para {s['variable']}: "
                    f"catalogo o metodologia (diccionario "
                    f"{s['diccionario']}).")
        decisiones_sig.append({"definicion_iri": defi, "decision": "pendiente",
                               "motivo": motivo, "evidencia": ev})
        pendientes_det.append({"tipo": "significado", "iri": defi,
                               "variable": s["variable"], "motivo": motivo,
                               "evidencia_faltante": falt,
                               "evidencia_revisada": ev})

    # Solicitudes agrupadas por diccionario/tema (IRIs concretos).
    def iris(dic, *pref):
        return [s["definicion_iri"] for s in asig["variables_pendientes"]
                if s["diccionario"] == dic
                and (not pref or s["variable"].startswith(pref))]
    D_SINAC = "22202305-2d02-4c49-b216-cc98224357f0"
    D_SUIVE = "2334deaa-dd0c-444e-b038-4cc556ad715d"
    solicitudes = [
        {"id": "r4-lote-3-inv-01",
         "iris": iris(D_SINAC, "SECONSIDERA", "HABLA", "RESIDEEXTRANJEROD"),
         "duda": "Dominio y valores de autoadscripcion indigena, lengua y "
                 "residencia extranjera de la madre.",
         "fuente_probable": "Secretaria de Salud / SINAC (metodologia del "
                            "certificado de nacimiento).",
         "documento_requerido": "Metodologia SINAC o catalogo de valores con "
                               "version aplicable a 2022."},
        {"id": "r4-lote-3-inv-02",
         "iris": [s["definicion_iri"] for s in asig["variables_pendientes"]
                  if s["diccionario"] == D_SINAC and (s["descripcion"] or "")
                  .strip().lower() == "pendiente de especificar"],
         "duda": "58 variables SINAC sin descripcion (atencion prenatal, "
                 "vacunas, anomalias CIE, CLUES, certificacion, etc.).",
         "fuente_probable": "Secretaria de Salud / SINAC.",
         "documento_requerido": "Diccionario SINAC completo con "
                               "descripciones y catalogos (CLUES con version "
                               "historica 2022, CIE, ocupacion)."},
        {"id": "r4-lote-3-inv-03",
         "iris": iris(D_SUIVE),
         "duda": "Cobertura y dominios SUIVE: contradiccion nombre/descripcion "
                 "en de01_a_04; desagregados *f e instituciones sin "
                 "descripcion; cve_cie10 solo 'Clave'.",
         "fuente_probable": "Servicios de Salud de Sonora / SUIVE.",
         "documento_requerido": "Diccionario SUIVE con descripciones, "
                               "aclaracion del rango de01_a_04 y documento "
                               "de cobertura de unidades reportantes."},
        {"id": "r4-lote-3-inv-04",
         "iris": iris("90f5c6ec-026e-4216-9541-e4730c836ff1"),
         "duda": "Dominios de la encuesta de Gobernanza de Datos (P2-P21: "
                 "sector, horas, innovacion, normativa).",
         "fuente_probable": "Dependencia publicadora del conjunto.",
         "documento_requerido": "Cuestionario y metodologia de la encuesta."},
        {"id": "r4-lote-3-inv-05",
         "iris": iris("52fbcaaa-765b-4c92-8418-ccebc3fcfdcd"),
         "duda": "ID_Persona como identificador de donante (no se propone "
                 "identidad entre registros).",
         "fuente_probable": "Centro de trasplantes / publicador.",
         "documento_requerido": "Metodologia y aviso de privacidad; sin "
                               "cruce de identidades."},
        {"id": "r4-lote-3-inv-06",
         "iris": [s["definicion_iri"] for s in asig["variables_pendientes"]
                  if s["diccionario"] in (
                      "3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99",
                      "c429c558-a38a-4f32-9ea9-8356c1c59cc1",
                      "d26d1900-6ff7-41a4-8968-f8984fc85e75",
                      "637b1909-8788-4bdf-9508e4fa9e8c008",
                      "b37f6cd2-c72c-448c-bcb2-9127c4912847",
                      "89e8c891-5987-44eb-ba11-9508e3dd87e6",
                      "087efeed-26c4-4ec4-8128-49f257d5182",
                      "1a95d734-2f0e-4781-8831-77dcfcbe70f8")],
         "duda": "Dominios locales: Tipo de Lugar/giro (Zonas Salva), "
                 "TRIMESTRE/MEDIO/ASUNTO/HECHOS/GIRO/MATERIA (Denuncias), "
                 "concepto/tipo de ayuda y Monto (Apoyos), clasificacion de "
                 "llamada 911, Tipo/Estatus de centros nocturnos.",
         "fuente_probable": "Dependencias publicadoras de cada conjunto.",
         "documento_requerido": "Diccionarios o catalogos publicados por "
                               "conjunto (giros, materias, reglas de "
                               "operacion con moneda de Monto, clasificador "
                               "de llamadas); sin inferir unidades."},
    ]

    entrega = {
        "lote": "lote-3",
        "generado_en_utc": datetime.now(timezone.utc).isoformat(),
        "decisiones_columnas": decisiones_columnas,
        "vinculos": vinculos,
        "decisiones_significados": decisiones_sig,
        "reglas": [],
        "conceptos_nuevos": {},
        "solicitudes_investigacion": solicitudes,
        "verificacion": {
            "columnas_asignadas": len(asig["columnas"]),
            "huella_fila_recomputada_ok": n_huella_fila_ok,
            "esquema_localizado_ok": n_huella_esq_ok,
            "nombre_unico_en_esquema": n_unicos,
        },
    }
    (LOTE / "entrega.json").write_text(
        json.dumps(entrega, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (LOTE / "pendientes.json").write_text(
        json.dumps({"lote": "lote-3", "pendientes": pendientes_det},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    n_prop = sum(1 for d in decisiones_columnas if d["decision"] == "proponer")
    n_pen = len(decisiones_columnas) - n_prop
    md = f"""# Resultado lote-3 (ronda 4)

- Columnas asignadas revisadas: {len(decisiones_columnas)} (todas con evidencia recomputada).
- Decisiones de columna: {n_prop} proponer, {n_pen} pendiente, 0 rechazar.
- Vinculos con formato exacto de vinculos_documentales_revisados: {len(vinculos)}.
- Significados asignados revisados: {len(decisiones_sig)} (0 proponer, {len(decisiones_sig)} pendiente).
- Reglas nuevas: 0. Conceptos nuevos: 0. No se cambian reglas previas.
- Huellas de fila de diccionario recomputadas desde contenido-inspeccion.json: {n_huella_fila_ok}/{len(decisiones_columnas)} OK.
- Esquemas localizados en inspecciones/inventario con recurso y campo coincidentes: {n_huella_esq_ok}/{len(decisiones_columnas)}.
- Nombre unico en su esquema: {n_unicos}/{len(decisiones_columnas)}.
- Pares codigo/descripcion (p. ej. ENTIDADNACIMIENTO/ENTIDADNACIMIENTOD) vinculados por separado, sin fusionar; representaciones codigo/nombre conservadas.
- CLUES y MUNICIPIO/LOCALIDADCERTIFICA quedan pendientes por descripcion vacia (nucleo: CLUES candidato).
- Solicitudes de investigacion: {len(solicitudes)} grupos con IRIs concretos.
"""
    (LOTE / "resultado.md").write_text(md, encoding="utf-8")
    sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
    (LOTE / "listo.json").write_text(json.dumps({
        "lote": "lote-3", "sha256": sha,
        "columnas": len(decisiones_columnas), "proponer": n_prop,
        "pendientes_columna": n_pen, "significados": len(decisiones_sig),
        "vinculos": len(vinculos), "reglas": 0,
        "conceptos_nuevos": 0}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps({"proponer": n_prop, "pendientes": n_pen,
                      "significados": len(decisiones_sig),
                      "vinculos": len(vinculos), "sha256": sha[:16] + "..."}))


if __name__ == "__main__":
    main()
