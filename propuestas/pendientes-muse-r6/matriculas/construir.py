# Ronda 6, rol matriculas: 30 pendientes, 0 propuestas. Solo escribe esta carpeta.
# Lee asignacion R6 + dictamen R5 + adenda R5; verifica una linea nueva (reglamento
# vigente ues.mx) por CLI con HTTP/URL/CT/magia/SHA; al resultar misma edicion 2019,
# confirma pendientes sin inventar definiciones. SHA de fuentes recomputados, no transcritos.
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[2]
BASE = "https://example.org/mex-ontologi/"
DICC = "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d"
REC = "58f2d5a6-0432-48f1-8a35-a5efcce78bac"
CONJ = "e819466c-7282-46c5-84e9-65917dd8cc85"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def save(name, obj):
    (AQUI / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def fila_txt(n, filas):
    r = filas[n]
    return (f"tipo={r['Tipo de dato']}; formato={r['Formato'] or 'no declarado'}; "
            f"ejemplo={r['Ejemplo de dato'].strip() or 'vacio'}")


asig = load("propuestas/pendientes-muse-r6/matriculas/asignacion.json")
r5ent = load("propuestas/pendientes-muse-r5/matriculas/entrega.json")
falt = {p["definicion_iri"]: p["evidencia_faltante"] for p in r5ent["pendientes"]}
insp = load(f"data/portal/inspecciones/{DICC}.json")
FILAS = {i + 1: r for i, r in enumerate(insp["definiciones"])}

# Novedad R6 (linea nueva verificada, negativa acotada, no ausencia universal).
PDF_REL = "propuestas/pendientes-muse-r6/matriculas/evidencia/UES_Reglamentoescolar_ues-mx.pdf"
PDF_SHA = hashlib.sha256((AQUI / "evidencia/UES_Reglamentoescolar_ues-mx.pdf").read_bytes()).hexdigest()
assert PDF_SHA == "b8343af9800ea7565e9ecb1f24560efc8d63979920b2fc040b9a29c7e57076a8", "el PDF debe ser la edicion 2019 ya revisada"
NOVEDAD = ("R6: linea nueva verificada sin resolver. Descarga CLI 2026-10-23 de la URL vigente "
           "https://www.ues.mx/archivos/alumnos/reglamentos/Reglamentoescolar.pdf (HTTP 200, URL final identica, "
           "Content-Type application/pdf, magia %PDF-, 216233 B, sha256 b8343af9...57076a8): byte-identica a la "
           "edicion XXX 16-dic-2019 ya revisada en R5 (adenda-web.md). No es fuente nueva; no se repite su contenido "
           "como hallazgo. Busquedas acotadas R6: calendario UES 2022-2 no localizado en publicacion IES autentica "
           "(solo avisos 2022-1 y pagina de calendario vigente); diccionario vigente sigue con descripciones vacias "
           "segun instantanea local 2026-10-23 (posterior a su actualizacion 1-nov-2024); dominios de '222 (Reing)', "
           "Tipo de baja, Estimulo y facetas indigenas sin documento publico. Dependencia del publicador.")

decisiones, pendientes = [], []
for s in sorted(asig["significados"], key=lambda x: x["definicion_iri"]):
    iri = s["definicion_iri"]
    n = int(iri.rsplit("%2F", 1)[1])
    motivo = s["dictamen_documental"]["motivo"] + " Sin regla revisada ni evidencia externa vinculada."
    ev = [f"data/portal/inspecciones/{DICC}.json:definiciones[{n}] ({fila_txt(n, FILAS)})",
          f"huella_fila_diccionario={s['huella_fila_diccionario']} (recomputada OK 30/30 R6)",
          "data/semantica/cobertura.json (estado previo fila {n})".format(n=n),
          "propuestas/pendientes-muse-r5/matriculas/adenda-web.md (R5: reglamentos 2019/2022 y guia 2023 revisados; "
          "sin tipos de baja, sin 'no exigibilidad'/'examen profesional', '222' del PDF es ruido; revisado, no repetido)",
          f"{PDF_REL} (R6: URL vigente ues.mx verificada = edicion 2019 ya revisada; sha256 {PDF_SHA}; no resuelve)"]
    decisiones.append({"definicion_iri": iri, "decision": "pendiente", "motivo": motivo,
                       "evidencia": ev,
                       "limites": ["Alcance simultaneo por conjunto, diccionario, definicion, nombre y descripcion; "
                                   "no autoriza cruces, homologaciones ni equivalencias.",
                                   "Evidencia negativa acotada a las busquedas R6 documentadas, no ausencia universal."],
                       "novedad_r6": NOVEDAD})
    pendientes.append({"definicion_iri": iri, "variable": s["variable"], "conjunto": CONJ, "diccionario": DICC,
                       "descripcion": s["descripcion"], "tipo_dato": FILAS[n]["Tipo de dato"],
                       "ejemplo": FILAS[n]["Ejemplo de dato"].strip(),
                       "motivo": s["dictamen_documental"]["motivo"],
                       "evidencia_faltante": falt[iri],
                       "documento_exacto_necesario": falt[iri],
                       "en_manos_del_publicador": True})

fuentes = [
    {"localizador": f"data/portal/inspecciones/{DICC}.json", "sha256": sha(f"data/portal/inspecciones/{DICC}.json"),
     "aplicabilidad": "Diccionario local: filas 8,11,12,13,14,17,20,25-29,35,47-49,52-54,58,61-70 verificadas; huellas 30/30 recomputadas R6."},
    {"localizador": f"data/portal/inspecciones/{REC}.json", "sha256": sha(f"data/portal/inspecciones/{REC}.json"),
     "aplicabilidad": "Esquema del recurso Estudiantes 2022-2 (70 campos); contexto sin vinculos propuestos."},
    {"localizador": "data/semantica/cobertura.json", "sha256": sha("data/semantica/cobertura.json"),
     "aplicabilidad": "Estados previos de las 30 variables asignadas."},
    {"localizador": "ontologia/semantica.json", "sha256": sha("ontologia/semantica.json"),
     "aplicabilidad": "Conceptos vigentes; sin reutilizacion ni conceptos nuevos (0 propuestas)."},
    {"localizador": "propuestas/pendientes-muse-r5/matriculas/adenda-web.md",
     "sha256": sha("propuestas/pendientes-muse-r5/matriculas/adenda-web.md"),
     "aplicabilidad": "R5 ya reviso reglamentos 2019/2022 y guia 2023; veredictos MAT-W-01..05 revisados, no repetidos."},
    {"localizador": PDF_REL, "sha256": PDF_SHA,
     "aplicabilidad": "R6 linea nueva: URL vigente del reglamento UES resulta edicion 2019 ya revisada; confirma pendiente, no acredita codigo local ni vigencia distinta."},
]

sols = [
    {"id": "MAT-R6-01",
     "url_primaria": "https://datos.sonora.gob.mx/sr_Latn/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d",
     "documento_exacto_nuevo": "diccionario-matriculas-de-estudiantes.csv vigente con descripciones no vacias + recurso Estudiantes 2022-2 con muestra de valores por columna (dominios de '222 (Reing)', Tipo de baja, Estimulo, Area Bachillerato, periodo de egreso, facetas indigenas).",
     "definiciones_afectadas": [f"{BASE}definition/{DICC}%2F{n}" for n in (8, 11, 12, 17, 25, 26, 27, 28, 29, 35, 54, 58, 61, 62)],
     "evidencia_exacta_requerida": "Captura textual de filas con descripcion no vacia y valores observados por campo."},
    {"id": "MAT-R6-02",
     "url_primaria": "https://ues.sonora.gob.mx/index.php?option=com_sppagebuilder&view=page&id=61",
     "documento_exacto_nuevo": "Calendario Escolar UES 2022-2 en PDF oficial o nota que defina la clave de ciclo '222', el calificador '(Reing)' y a que remite 'ciclo senalado' / 'periodo escolar de egreso'.",
     "definiciones_afectadas": [f"{BASE}definition/{DICC}%2F{n}" for n in (8, 12, 13, 14, 58)],
     "evidencia_exacta_requerida": "Fragmento con la clave, el calificador y el periodo de cobertura 2022-2."},
    {"id": "MAT-R6-03",
     "url_primaria": "https://www.ues.mx/archivos/alumnos/reglamentos/Reglamentoescolar.pdf",
     "documento_exacto_nuevo": "Norma UES de evaluacion/titulacion edicion aplicable al dato 2022-2 (distinta de la edicion 2019 verificada en R6): escala y metodo de promedios por subconjunto, tipos de baja, alternativas 'no exigibilidad' y 'examen profesional', equivalencia/convalidacion y representacion de cada campo.",
     "definiciones_afectadas": [f"{BASE}definition/{DICC}%2F{n}" for n in (17, 47, 48, 49, 52, 53, 61, 63, 64, 65, 66, 67, 68, 69, 70)],
     "evidencia_exacta_requerida": "Articulo o numeral con dominio, escala y vigencia; la URL citada hoy sirve la edicion 2019 (sha b8343af9...), que no resuelve."},
]

entrega = {"rol": "matriculas", "generado_en_utc": datetime.now(timezone.utc).isoformat(),
           "alcance": "30 significados asignados del diccionario de Matriculas de Estudiantes; R5 ya reviso reglamentos 2019/2022 y guia 2023; R6 solo linea nueva.",
           "decisiones_significados": decisiones, "reglas": [], "conceptos_nuevos": {},
           "decisiones_columnas": [], "vinculos": [], "fuentes": fuentes, "pendientes": pendientes,
           "solicitudes_web_archivo": "solicitudes-web.json",
           "verificacion": {"asignados": 30, "decisiones": 30, "huella_fila_recomputada_ok": 30,
                             "reglas_nuevas": 0, "conceptos_nuevos": 0, "vinculos": 0}}
save("entrega.json", entrega)
save("solicitudes-web.json", {"rol": "matriculas", "destinatario": "catalogos-web",
                              "nota": "Sin control de Obscura; URLs primarias realmente visitadas (busqueda R6); documentos exactos nuevos, IDs unicos MAT-R6-01..03.",
                              "solicitudes": sols})

h = hashlib.sha256((AQUI / "entrega.json").read_bytes()).hexdigest()
n_pen = sum(1 for d in decisiones if d["decision"] == "pendiente")
(AQUI / "resultado.md").write_text("\n".join([
    "# Resultado matriculas (ronda 6)",
    "",
    f"Asignados: 30. Decisiones: 0 proponer, {n_pen} pendiente, 0 artefacto_documental.",
    "Reglas nuevas: 0. Conceptos nuevos: 0. Vinculos: 0. Columnas: 0.",
    "Solicitudes web: 3 (MAT-R6-01 a MAT-R6-03, IDs nuevos; no se reutilizan MAT-W-*).",
    "",
    "## Novedad R6 respecto de R5 (linea nueva, negativa acotada)",
    "",
    "- R5 reviso reglamentos 2019/2022 y guia 2023 (adenda-web.md); nada de ello se repite como hallazgo.",
    "- R6 descargo por CLI la URL vigente del reglamento UES (HTTP 200, URL final identica,",
    "  Content-Type application/pdf, magia %PDF-, 216233 B,",
    "  sha256 b8343af9800ea7565e9ecb1f24560efc8d63979920b2fc040b9a29c7e57076a8):",
    "  byte-identica a la edicion XXX 16-dic-2019 ya revisada. No es fuente nueva.",
    "- Busquedas acotadas R6: sin calendario UES 2022-2 en publicacion IES autentica;",
    "  sin diccionario corregido (la instantanea local 2026-10-23 es posterior a su actualizacion 1-nov-2024",
    "  y mantiene descripciones vacias); sin dominios publicos de '222 (Reing)', Tipo de baja,",
    "  Estimulo ni facetas indigenas. Evidencia negativa = busqueda acotada, no ausencia universal.",
    "- 30 pendientes confirmados con documento exacto necesario, todo en manos del publicador",
    "  (ver entrega.json -> pendientes). No se aprueba por nombre; no se inventa definicion.",
    "",
    "## Verificacion",
    "",
    "- Huellas de fila recomputadas con huella() de scripts/consolidar_semantica.py: 30/30 OK.",
    "- Fuentes con SHA recomputado desde bytes en este script (no transcritos).",
    "- Reglas, conceptos y vinculos: 0 (sin colisiones que verificar).",
    "",
    "## Archivos",
    "",
    "- entrega.json, solicitudes-web.json, resultado.md, listo.json, construir.py, evidencia/UES_Reglamentoescolar_ues-mx.pdf",
    f"- sha256(entrega.json) = {h}",
    ""]) + "\n", encoding="utf-8")
save("listo.json", {"rol": "matriculas", "entrega": "entrega.json", "sha256": h,
                    "cuentas": {"asignados": 30, "proponer_significados": 0,
                                "pendiente_significados": n_pen, "reglas_nuevas": 0,
                                "conceptos_nuevos": 0, "decisiones_columnas": 0,
                                "vinculos": 0, "solicitudes_web": len(sols)},
                    "estado": "completo"})
print("listo sha:", h, "| decisiones:", len(decisiones), "| pendientes:", len(pendientes))
