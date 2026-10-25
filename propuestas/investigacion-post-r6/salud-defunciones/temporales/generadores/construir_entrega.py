"""Construye entrega.json y listo.json para salud-defunciones (post-R6).
Lee asignacion (pendientes.json), inspeccion local y examen_por_id.json;
verifica SHA de insumos y emite decisiones 32/32 (todas sigue_pendiente).
Uso: uv run python propuestas/investigacion-post-r6/salud-defunciones/temporales/generadores/construir_entrega.py
"""
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
OUT = REPO / "propuestas/investigacion-post-r6/salud-defunciones"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    pdf = REPO / "propuestas/pendientes-muse-r6/salud/evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf"
    insp = REPO / "data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json"
    asig = REPO / "propuestas/depuracion-post-r6/significados/pendientes.json"
    pack = REPO / "propuestas/pendientes-muse-r6/salud/evidencia/package_defunciones.json"
    exam = OUT / "evidencia/examen_por_id.json"
    httplog = OUT / "evidencia/http_log.json"
    paginas = OUT / "evidencia/manual_seed2022_paginas.txt"
    rev = OUT / "evidencia/revision_vinculo_formal.json"

    assert pdf.read_bytes()[:5] == b"%PDF-", "magia PDF"
    assert sha(pdf) == "698ee48a45f0f34eaf604be9e4290a2191953c9d0460d43600ccc6d6f29b74f4", "SHA PDF"
    assert sha(insp) == "2094c24f84a07d1a7e9e7f3c9e663b6923e51508a71678eea74860232f2c1179", "SHA inspeccion"

    pend = json.loads(asig.read_text(encoding="utf-8"))
    mios = [s for s in pend["significados"] if s["grupo_fuente"] == "salud-defunciones"]
    assert len(mios) == 32, f"asignados={len(mios)}"
    examd = {e["n"]: e for e in json.loads(exam.read_text(encoding="utf-8"))["entradas"]}
    assert len(examd) == 32 and set(examd) == {s["n"] for s in mios}, "examen 32/32"

    fuentes = [
        {"id": "F1", "ruta": str(pdf.relative_to(REPO)).replace("\\", "/"),
         "url": "http://www.dgis.salud.gob.mx/descargas/seed/pdf/Manual_Llenado_CD_CMF_2022_20220930.pdf",
         "sha256": sha(pdf), "fecha_consulta": "2026-10-24",
         "localizador": "portada p1 (Modelo 2022); vigencia p17; preguntas por ID en decisiones",
         "descripcion": "Manual SEED Modelo 2022 autentico preservado; re-descarga 2026-10-24 byte-identica (HTTP 200, 11717771 B)"},
        {"id": "F2", "ruta": str(insp.relative_to(REPO)).replace("\\", "/"), "url": None,
         "sha256": sha(insp), "fecha_consulta": "2026-10-24",
         "localizador": "/definiciones/<fila-1> (0-based)",
         "descripcion": "Inspeccion local del diccionario: tipo/ejemplo/descripcion por fila"},
        {"id": "F3", "ruta": str(asig.relative_to(REPO)).replace("\\", "/"), "url": None,
         "sha256": sha(asig), "fecha_consulta": "2026-10-24",
         "localizador": "significados n=1..32 de salud-defunciones",
         "descripcion": "Asignacion del grupo (32 IDs) con huellas y criterio de aceptacion R6"},
        {"id": "F4", "ruta": str(httplog.relative_to(REPO)).replace("\\", "/"), "url": None,
         "sha256": sha(httplog), "fecha_consulta": "2026-10-24",
         "localizador": "consultas_http + busquedas_negativas_acotadas",
         "descripcion": "Log HTTP propio: HEAD/GET manual + pagina SEED-DGIS + negativas acotadas"},
        {"id": "F5", "ruta": str(exam.relative_to(REPO)).replace("\\", "/"), "url": None,
         "sha256": sha(exam), "fecha_consulta": "2026-10-24",
         "localizador": "entradas n=1..32 (pregunta/pagina/cita/ambito/veredicto/bloqueo)",
         "descripcion": "Examen por ID del manual (ADV-SALUD-MANUAL), propio de esta entrega"},
        {"id": "F6", "ruta": str(paginas.relative_to(REPO)).replace("\\", "/"), "url": None,
         "sha256": sha(paginas), "fecha_consulta": "2026-10-24",
         "localizador": "===== PAGINA <1..103> =====",
         "descripcion": "Extraccion textual propia del PDF (pypdf) con marcadores de pagina"},
        {"id": "F7", "ruta": str(pack.relative_to(REPO)).replace("\\", "/"), "url": None,
         "sha256": sha(pack), "fecha_consulta": "2026-10-24",
         "localizador": "result.resources[] (Diccionario 12f684e9; Defunciones 2022 6f39fc5d)",
         "descripcion": "package_show R6: sistema SEED, periodo 2022-01-01 a 2022-09-22, version=null, recurso XLSX datastore_active=false"},
        {"id": "F8", "ruta": str(rev.relative_to(REPO)).replace("\\", "/"), "url": None,
         "sha256": sha(rev), "fecha_consulta": "2026-10-24",
         "localizador": "criterio + prong1 + prong2 + tabla_por_id (32) + conclusion",
         "descripcion": "Revision critica de la via alternativa (sistema+periodo+uso formal por codigos/posicion), propia de esta entrega"},
    ]
    revd = json.loads(rev.read_text(encoding="utf-8"))
    assert len(revd["tabla_por_id"]) == 32, "tabla formal 32/32"

    decisiones = []
    for s in sorted(mios, key=lambda x: x["n"]):
        e = examd[s["n"]]
        ev = [
            {"ruta": fuentes[0]["ruta"], "sha256": fuentes[0]["sha256"],
             "localizador": f"pp.{','.join(map(str, e['paginas']))} (preg {e['pregunta_manual']})" if e["pregunta_manual"] else "busqueda acotada pp1-103 (0 preguntas)",
             "afirmacion_soportada": f"Veredicto {e['veredicto']}: {e['cita_breve'][:220]}"},
            {"ruta": fuentes[1]["ruta"], "sha256": fuentes[1]["sha256"],
             "localizador": f"/definiciones/{int(s['fila']) - 1}",
             "afirmacion_soportada": f"Fila local: tipo={e['tipo_local']}, ejemplo={e['ejemplo_local']!r}, descripcion='Pendiente de especificar', catalogo=''"},
        ]
        if e["veredicto"] in ("sin-pregunta", "incompatible"):
            ev.append({"ruta": fuentes[3]["ruta"], "sha256": fuentes[3]["sha256"],
                       "localizador": "busquedas_negativas_acotadas",
                       "afirmacion_soportada": "Negativas acotadas que sostienen el veredicto (jurisdiccion/intencion-literal/codebook/edicion)"})
        decisiones.append({
            "definicion_iri": s["definicion_iri"], "variable": s["variable"],
            "descripcion_original": s["descripcion_original"],
            "huella_fila_diccionario": s["huella_fila_diccionario"],
            "estado": "sigue_pendiente",
            "evidencia": ev,
            "vinculo_fuente_local": (
                "Sin vinculo apto para promocion: ninguna pregunta-manual corresponde; "
                if e["veredicto"] == "sin-pregunta" else
                f"Vinculo solo tematico a preg {e['pregunta_manual']} del Manual Modelo 2022 (ambito {e['ambito']}), "
                "sin tabla pregunta<->columna del publicador ni codebook/edicion: insuficiente para promocion. "
            ) + "Recurso de datos citado sin vinculo (XLSX, datastore_active=false).",
            "evidencia_faltante": ("Nota del publicador que vincule el recurso 6f39fc5d (2022-01-01 a 2022-09-22) con "
                f"la preg {e['pregunta_manual']} del Manual SEED Modelo 2022 para esta fila (huella {s['huella_fila_diccionario'][:12]}...), "
                "con tabla pregunta<->columna y codebook/edicion aplicable (para CIE: edicion que contenga el codigo local)."),
            "motivo": f"sigue_pendiente: examen por ID del manual autentico da veredicto {e['veredicto']} ({e['ambito']}). {e['bloqueo']}",
            "limites": ["Alcance simultaneo por conjunto+diccionario+fila+huella; no autoriza cruces, joins ni identidad de catalogos.",
                        "Extracto textual (pypdf) sin layout/imagenes; paginas citadas verificables en el PDF.",
                        "Negativas acotadas a lo revisado (F4), no ausencia universal."],
        })

    entrega = {
        "grupo_fuente": "salud-defunciones",
        "generado_en_utc": "2026-10-24T23:30:00+00:00",
        "alcance": "32/32 IDs asignados examinados por ID contra el PDF autentico SEED Modelo 2022 (ADV-SALUD-MANUAL). 0 propuestas: ninguna fila satisface el criterio de aceptacion R6.",
        "fuentes": fuentes,
        "decisiones": decisiones,
        "resumen_investigacion": {
            "metodo": "Re-descarga byte-identica del PDF + confirmacion de listado en pagina SEED-DGIS + extraccion 103 pp + examen por ID 32/32 con pregunta/pagina/cita/ambito (fetal vs general).",
            "veredictos": {"ambiguo": 12, "compatible-tematica": 17, "incompatible": 1, "sin-pregunta": 2},
            "nuevo_frente_a_r6": ["Re-descarga 2026-10-24 byte-identica (SHA coincide; Last-Modified 2022-10-19)",
                "Pagina SEED-DGIS confirma listado vigente del Manual Modelo 2022 (modif. 2024-12-02)",
                "Examen por ID 32/32 (R6: 0/85; correccion de auditoria aplicada): 12 ambiguos, 17 compatibles-tematicos por falta de vinculo (incluidos n=14 NO APLICA sin codebook y n=15/16 con edicion CIE no documentada), 1 incompatible formal (n=2, clave numerica sin counterpart), 2 sin pregunta (JURISDICCION_CLUES[D])",
                "Recurso de datos XLSX con datastore_active=false: sin mapeo fisico verificable",
                "Vigencia Modelo 2022 p17 (2022-2026) acredita modelo, no vinculo publicador-recurso"],
            "staging": "Nada que estadificar: 0 propuestas_respaldadas; sin cambios al nucleo.",
            "bloqueo_general": "Falta el vinculo explicito del publicador (recurso 6f39fc5d <-> Manual Modelo 2022, tabla pregunta<->columna, codebook/edicion por fila). En manos del publicador.",
        },
        "revision_vinculo_formal": {
            "criterio": revd["criterio_probatorio"],
            "prong1_sistema_periodo": "ACREDITADO como marco necesario no suficiente: SEED en dos certificados + Modelo 2022 vigente 2022-2026 (p17) cubriendo el periodo del recurso 2022-01-01 a 2022-09-22. No exige mencion a Sonora.",
            "prong2_uso_formal": "FALLA en 32/32: sin codebook numerico publicado, serie-9 manual vs serie-8 local, sin tabla pregunta<->columna, posiciones inconmensurables. Veredicto por ID en F8.",
            "conclusion": revd["conclusion"],
            "detalle_en": {"ruta": str(rev.relative_to(REPO)).replace("\\", "/"), "sha256": sha(rev)},
        },
    }
    (OUT / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2), encoding="utf-8")

    artefactos = ["entrega.json", "entrega.md", "evidencia/examen_por_id.json",
                  "evidencia/http_log.json", "evidencia/manual_seed2022_paginas.txt",
                  "evidencia/revision_vinculo_formal.json"]
    listo = {"grupo_fuente": "salud-defunciones", "fecha_utc": "2026-10-24",
             "artefactos": [{"ruta": f"propuestas/investigacion-post-r6/salud-defunciones/{a}",
                             "sha256": sha(OUT / a)} for a in artefactos]}
    (OUT / "listo.json").write_text(json.dumps(listo, ensure_ascii=False, indent=2), encoding="utf-8")
    print("decisiones:", len(decisiones), "| artefactos:", len(artefactos), "| OK")


if __name__ == "__main__":
    main()
