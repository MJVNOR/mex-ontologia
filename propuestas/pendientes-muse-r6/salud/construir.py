# Ronda 6, rol salud: 85 pendientes (53 nacimientos + 32 defunciones). Solo escribe esta carpeta.
# Linea nueva R6 (no repite R5): package_show CKAN de ambos conjuntos (sistema declarado
# SINAC/SEED + periodo 2022, sin version ni vinculo de edicion) y Manual SEED Modelo 2022
# DGIS (20220930) descargado por CLI con HTTP/URL/CT/magia/SHA. Al no declarar el publicador
# vinculo edicion-recurso-periodo, el manual nacional no acredita codigo local ni vigencia:
# 85 pendientes confirmados sin inventar definiciones. SHA recomputados desde bytes.
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[2]
BASE = "https://example.org/mex-ontologi/"
DICC_NAC = "22202305-2d02-4c49-b216-cc98224357f0"
DICC_DEF = "12f684e9-f4d5-4714-933d-aa153a812174"
REC_NAC = "46977217-9396-4f9c-bddb-6616e82530b4"
REC_DEF = "6f39fc5d-e097-4954-8cd7-10e8f9dea541"
CONJ_NAC = "940de7d8-73ec-4a08-8d26-b7cc97ff17bd"
CONJ_DEF = "cd3d6e34-3789-479e-9f2b-a717b8419f9c"
PDF_REL = "propuestas/pendientes-muse-r6/salud/evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf"
PDF_SHA = "698ee48a45f0f34eaf604be9e4290a2191953c9d0460d43600ccc6d6f29b74f4"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def save(name, obj):
    (AQUI / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def huella(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def fila_txt(fila):
    return ("tipo={}; ejemplo={}; catalogo={}".format(
        fila.get("Tipo de dato", ""), (fila.get("Ejemplo de dato", "") or "").strip() or "vacio",
        fila.get("Catálogo de referencia", "") or "no declarado"))


asig = load("propuestas/pendientes-muse-r6/salud/asignacion.json")
r5nac = load("propuestas/pendientes-muse-r5/nacimientos/entrega.json")
r5def = load("propuestas/pendientes-muse-r5/defunciones/entrega.json")
falt_nac = {p["definicion_iri"]: p["evidencia_faltante"] for p in r5nac["pendientes_precisos"]}
falt_def_inv = {p["definicion_iri"]: p["documento_requerido"] for p in r5def["solicitudes_investigacion"]}
insp = {r["id"]: r for r in load("data/portal/contenido-inspeccion.json")["recursos"]}
FILAS_NAC = {i + 1: r for i, r in enumerate(insp[DICC_NAC]["definiciones"])}
FILAS_DEF = {i + 1: r for i, r in enumerate(insp[DICC_DEF]["definiciones"])}

# Novedad R6 verificada (negativa acotada, no ausencia universal).
pdf_bytes = (AQUI / "evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf").read_bytes()
pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
assert pdf_sha == PDF_SHA, "el PDF SEED 2022 debe coincidir con la descarga CLI verificada"
assert pdf_bytes[:5] == b"%PDF-", "magia PDF"
NOVEDAD = (
    "R6: linea nueva verificada sin resolver. package_show CKAN 2026-10-23 de ambos conjuntos: "
    "nacimientos declara 'Subsistema de Informacion sobre Nacimientos' (SINAC), recurso 2022-01-01 a 2022-09-26, "
    "106 variables, version=null, url=null, fuentes_extras=''; defunciones declara titulo SEED, recurso "
    "2022-01-01 a 2022-09-22, 80 variables, version=null, url=null, fuentes_extras=''. Sistema+periodo "
    "declarados, pero sin vinculo de edicion (F4 ausente). Manual nacional SEED Modelo 2022 DGIS "
    "(http://www.dgis.salud.gob.mx/descargas/seed/pdf/Manual_Llenado_CD_CMF_2022_20220930.pdf, HTTP 200, "
    "Content-Type application/pdf, magia %PDF-, 11717771 B, sha256 698ee48a...29b74f4, listado en la pagina "
    "oficial SEED-DGIS): cubre SITIO/CLUES/parentesco-informante/edad-gestacional-fetal, menciona CIE-10 una vez "
    "y 'Sonora' cero veces; sin tabla pregunta-manual<->columna-local ni declaracion del publicador que lo vincule "
    "a los recursos 2022, no acredita codigo local ni vigencia. SINAC: la pagina DGIS (ago-2023) no enlaza ningun "
    "manual de nacimiento (solo metodologia 2020); el Manual Modelo 2015 ya revisado en R5 carece de vinculo de "
    "vigencia a 2022 y la Guia Modelo 2025 (sinba, ago-2025) es post-periodo: busqueda acotada negativa. "
    "Datastore live 2026-10-23 confirma las 85 filas aun 'Pendiente de especificar' con catalogo ''. "
    "Manual 2015 y CLUES/CIE vigentes no se reutilizan (fuera de periodo). Dependencia del publicador.")

decisiones, pendientes = [], []
ok_huella = 0
for s in sorted(asig["significados"], key=lambda x: x["definicion_iri"]):
    iri = s["definicion_iri"]
    n = int(iri.rsplit("%2F", 1)[1])
    es_nac = s["diccionario"] == DICC_NAC
    fila = (FILAS_NAC if es_nac else FILAS_DEF)[n]
    h = huella(fila)
    assert h == s["huella_fila_diccionario"], iri
    ok_huella += 1
    motivo = s["dictamen_documental"]["motivo"] + " R6: sin regla revisada ni evidencia externa vinculada."
    ev = [("data/portal/contenido-inspeccion.json#recursos/{}/definiciones[{}] ({})".format(
        s["diccionario"], n, fila_txt(fila))),
        "huella_fila_diccionario={} (recomputada OK R6)".format(h),
        "datastore live 2026-10-23: descripcion='Pendiente de especificar', catalogo='' (verificado por CLI)",
        ("propuestas/pendientes-muse-r5/nacimientos/entrega.json" if es_nac
         else "propuestas/pendientes-muse-r5/defunciones/entrega.json")
        + " (dictamen previo revisado, no repetido como hallazgo)",
        "propuestas/pendientes-muse-r6/salud/evidencia/package_{}.json (R6: sistema+periodo declarados, sin edicion)".format(
            "nacimientos" if es_nac else "defunciones")]
    if not es_nac:
        ev.append("{} (R6: manual nacional Modelo 2022 verificado; sin vinculo local, no acredita)".format(PDF_REL))
    base_falt = falt_nac.get(iri) if es_nac else falt_def_inv.get(iri, "")
    if es_nac:
        falt = (base_falt + " R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 "
                "(Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.")
    else:
        falt = ("Vinculo explicito del publicador entre el recurso {} (2022-01-01 a 2022-09-22) y el Manual SEED "
                "Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. "
                "Base R5: {}. En manos del publicador.").format(REC_DEF, base_falt)
    decisiones.append({"definicion_iri": iri, "variable": s["variable"], "decision": "pendiente",
                       "motivo": motivo, "evidencia": ev,
                       "limites": ["Alcance simultaneo por conjunto, diccionario, definicion, nombre y descripcion; "
                                   "no autoriza cruces, homologaciones ni equivalencias.",
                                   "Evidencia negativa acotada a las busquedas R6 documentadas, no ausencia universal."],
                       "evidencia_faltante": falt, "novedad_r6": NOVEDAD})
    pendientes.append({"definicion_iri": iri, "variable": s["variable"],
                       "conjunto": s["conjunto"], "diccionario": s["diccionario"],
                       "descripcion": s["descripcion"], "tipo_dato": fila.get("Tipo de dato", ""),
                       "ejemplo": (fila.get("Ejemplo de dato", "") or "").strip(),
                       "motivo": s["dictamen_documental"]["motivo"],
                       "evidencia_faltante": falt, "documento_exacto_necesario": falt,
                       "en_manos_del_publicador": True})
assert ok_huella == 85, ok_huella

fuentes = [
    {"localizador": "data/portal/contenido-inspeccion.json",
     "sha256": sha("data/portal/contenido-inspeccion.json"),
     "aplicabilidad": "Diccionarios locales: 106 filas SINAC + 80 SEED; huellas 85/85 recomputadas R6."},
    {"localizador": "data/semantica/cobertura.json", "sha256": sha("data/semantica/cobertura.json"),
     "aplicabilidad": "Estados previos de las 85 variables asignadas."},
    {"localizador": "ontologia/semantica.json", "sha256": sha("ontologia/semantica.json"),
     "aplicabilidad": "Conceptos vigentes; sin reutilizacion ni conceptos nuevos (0 propuestas)."},
    {"localizador": "propuestas/pendientes-muse-r6/salud/evidencia/package_nacimientos.json",
     "sha256": sha("propuestas/pendientes-muse-r6/salud/evidencia/package_nacimientos.json"),
     "aplicabilidad": "R6: conjunto 940de7d8 declara SINAC, periodo 2022-01-01 a 2022-09-26; version/url/fuentes_extras nulos."},
    {"localizador": "propuestas/pendientes-muse-r6/salud/evidencia/package_defunciones.json",
     "sha256": sha("propuestas/pendientes-muse-r6/salud/evidencia/package_defunciones.json"),
     "aplicabilidad": "R6: conjunto cd3d6e34 titulo SEED, periodo 2022-01-01 a 2022-09-22; version/url/fuentes_extras nulos."},
    {"localizador": PDF_REL, "sha256": pdf_sha,
     "aplicabilidad": "R6: manual nacional SEED Modelo 2022 verificado (HTTP 200, PDF, 11717771 B); sin vinculo local, no acredita."},
    {"localizador": "propuestas/pendientes-muse-r5/nacimientos/entrega.json",
     "sha256": sha("propuestas/pendientes-muse-r5/nacimientos/entrega.json"),
     "aplicabilidad": "Dictamen previo 53+1 revisado; RESIDEEXTRANJEROD propuesto en R5 fuera de este alcance."},
    {"localizador": "propuestas/pendientes-muse-r5/defunciones/entrega.json",
     "sha256": sha("propuestas/pendientes-muse-r5/defunciones/entrega.json"),
     "aplicabilidad": "Dictamen previo 32 revisado; datastore/huellas re-verificados en R6."},
    {"localizador": "propuestas/pendientes-muse-r5/catalogos-web/evidencia/CN_ManualLlenado_2015.pdf",
     "sha256": sha("propuestas/pendientes-muse-r5/catalogos-web/evidencia/CN_ManualLlenado_2015.pdf"),
     "aplicabilidad": "R5 ya reviso el Manual Modelo 2015; no se repite como hallazgo (sin vinculo de vigencia a 2022)."},
]

sols = [
    {"id": "SAL-R6-01",
     "url_primaria": "https://datos.sonora.gob.mx/dataset/940de7d8-73ec-4a08-8d26-b7cc97ff17bd",
     "documento_exacto_nuevo": "Diccionario SINAC corregido con descripciones no vacias para las 53 columnas, o nota del publicador con descripcion+codebook por variable y vinculo explicito edicion-recurso-periodo al recurso 46977217 (2022-01-01 a 2022-09-26).",
     "definiciones_afectadas": sorted(s["definicion_iri"] for s in asig["significados"] if s["diccionario"] == DICC_NAC),
     "evidencia_exacta_requerida": "Captura textual de filas con descripcion no vacia, o declaracion de version/edicion aplicable al recurso 2022."},
    {"id": "SAL-R6-02",
     "url_primaria": "http://www.dgis.salud.gob.mx/contenidos/sinais/s_sinac.html",
     "documento_exacto_nuevo": "Manual SINAC de edicion 2022, o nota DGIS de vigencia del Modelo 2015 para los datos 2022 (la pagina oficial, actualizada ago-2023, no enlaza manual de nacimiento).",
     "definiciones_afectadas": sorted(s["definicion_iri"] for s in asig["significados"] if s["diccionario"] == DICC_NAC),
     "evidencia_exacta_requerida": "PDF con fecha/edicion 2022, o numeral de vigencia que cubra el periodo 2022-01-01 a 2022-09-26."},
    {"id": "SAL-R6-03",
     "url_primaria": "https://datos.sonora.gob.mx/dataset/cd3d6e34-3789-479e-9f2b-a717b8419f9c",
     "documento_exacto_nuevo": "Nota del publicador que vincule el recurso 6f39fc5d (2022-01-01 a 2022-09-22) con el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022.",
     "definiciones_afectadas": sorted(s["definicion_iri"] for s in asig["significados"] if s["diccionario"] == DICC_DEF),
     "evidencia_exacta_requerida": "Declaracion de edicion aplicable + correspondencia de campos; el manual nacional solo no acredita."},
    {"id": "SAL-R6-04",
     "url_primaria": "http://www.dgis.salud.gob.mx/contenidos/sinais/s_seed.html",
     "documento_exacto_nuevo": "Confirmacion de correspondencia para columnas D (desagregadas textuales), PARENTESCOAGRESORD (agresor, no informante), INTENCIONEVENTO/SITIOOCURRENCIALESION y JURISDICCION_CLUES(D): preguntas exactas del Manual Modelo 2022 que las definen.",
     "definiciones_afectadas": sorted(s["definicion_iri"] for s in asig["significados"] if s["diccionario"] == DICC_DEF),
     "evidencia_exacta_requerida": "Cita literal con numero de pregunta y texto; no inferir por nombre (parentesco-informante != parentesco-agresor)."},
]

entrega = {"rol": "salud", "generado_en_utc": datetime.now(timezone.utc).isoformat(),
           "alcance": "85 significados asignados (53 nacimientos SINAC + 32 defunciones SEED); R5 revisado; R6 solo linea nueva 2022.",
           "decisiones_significados": decisiones, "reglas": [], "conceptos_nuevos": {},
           "decisiones_columnas": [], "vinculos": [], "fuentes": fuentes, "pendientes": pendientes,
           "solicitudes_web_archivo": "solicitudes-web.json",
           "verificacion": {"asignados": 85, "decisiones": 85, "huella_fila_recomputada_ok": ok_huella,
                             "reglas_nuevas": 0, "conceptos_nuevos": 0, "vinculos": 0}}
save("entrega.json", entrega)
save("solicitudes-web.json", {"rol": "salud", "destinatario": "catalogos-web",
                              "nota": "Sin control de Obscura; URLs primarias realmente visitadas por CLI (HTTP 200); documentos exactos nuevos, IDs unicos SAL-R6-01..04.",
                              "solicitudes": sols})

h = hashlib.sha256((AQUI / "entrega.json").read_bytes()).hexdigest()
n_pen = sum(1 for d in decisiones if d["decision"] == "pendiente")
(AQUI / "resultado.md").write_text("\n".join([
    "# Resultado salud (ronda 6)",
    "",
    "Asignados: 85 (53 nacimientos SINAC + 32 defunciones SEED). Decisiones: 0 proponer, {} pendiente, 0 artefacto_documental.".format(n_pen),
    "Reglas nuevas: 0. Conceptos nuevos: 0. Vinculos: 0. Columnas: 0.",
    "Solicitudes web: 4 (SAL-R6-01 a SAL-R6-04, IDs nuevos; no se reutilizan nac-web-*/SW-D*).",
    "",
    "## Novedad R6 respecto de R5 (linea nueva, negativa acotada)",
    "",
    "- R5 dejo 53+32 pendientes por descripcion 'Pendiente de especificar' y sin vinculo local; nada de ello se repite como hallazgo: huellas 85/85 recomputadas y datastore live 2026-10-23 confirman que las filas siguen sin descripcion.",
    "- R6 verifico por CLI el vinculo local declarado (package_show CKAN 2026-10-23): nacimientos declara 'Subsistema de Informacion sobre Nacimientos' con periodo 2022-01-01 a 2022-09-26; defunciones declara titulo SEED con periodo 2022-01-01 a 2022-09-22. Ambos con version=null, url=null, fuentes_extras='': sistema+periodo si, edicion no (F4 ausente).",
    "- R6 descargo el Manual SEED Modelo 2022 DGIS (HTTP 200, URL final identica, Content-Type application/pdf, magia %PDF-, 11717771 B, sha256 698ee48a...29b74f4, listado en la pagina oficial SEED-DGIS): cubre SITIO/CLUES/parentesco-del-informante/edad-gestacional-fetal y menciona CIE-10 una vez, pero nombra 'Sonora' cero veces y el publicador no lo vincula a los recursos 2022; no acredita codigo local ni vigencia. No se propone por nombre (parentesco-informante != PARENTESCOAGRESORD).",
    "- SINAC: la pagina DGIS (ago-2023) no enlaza manual de nacimiento alguno; el Manual Modelo 2015 ya revisado en R5 sigue sin vinculo de vigencia a 2022 y la Guia Modelo 2025 es post-periodo. Manual 2015 y CLUES/CIE vigentes no se reutilizan (fuera de periodo).",
    "- 85 pendientes confirmados con documento exacto necesario, todo en manos del publicador (ver entrega.json -> pendientes). No se aprueba por nombre; no se inventa definicion.",
    "",
    "## Verificacion",
    "",
    "- Huellas de fila recomputadas con huella() de scripts/consolidar_semantica.py: 85/85 OK.",
    "- Fuentes con SHA recomputado desde bytes en este script (no transcritos).",
    "- Reglas, conceptos y vinculos: 0 (sin colisiones que verificar).",
    "",
    "## Archivos",
    "",
    "- entrega.json, solicitudes-web.json, resultado.md, listo.json, construir.py, evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf, evidencia/package_nacimientos.json, evidencia/package_defunciones.json",
    "- sha256(entrega.json) = {}".format(h),
    ""]) + "\n", encoding="utf-8")
save("listo.json", {"rol": "salud", "entrega": "entrega.json", "sha256": h,
                    "cuentas": {"asignados": 85, "proponer_significados": 0,
                                "pendiente_significados": n_pen, "reglas_nuevas": 0,
                                "conceptos_nuevos": 0, "decisiones_columnas": 0,
                                "vinculos": 0, "solicitudes_web": len(sols)},
                    "estado": "completo"})
print("listo sha:", h, "| decisiones:", len(decisiones), "| pendientes:", len(pendientes))
