# Ronda 6, rol epidemiologia: 25 pendientes, 0 propuestas. Solo escribe esta carpeta.
# Linea nueva R6 (no repite R5): metadatos frescos del package (edicion 2022 fijada por
# start/end_date, sin Fuentes extras), estructura espejo f / bloque institucional / bloque
# mensual+totalm/totalf observada en el esquema fisico, huellas recomputadas 25/25, y
# correccion del SHA del manual SUIVE citado en R06 (tenia 62 caracteres, imposible).
# Manual32 solo contexto: sin vinculo edicion-recurso-periodo no acredita nada local.
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[2]
BASE = "https://example.org/mex-ontologi/"
DICC = "2334deaa-dd0c-444e-b038-4cc556ad715d"
XLSX = "1689b19c-b0dc-4e39-bf07-e3a2e684ef1a"
CONJ = "dca16d84-dbf0-4501-b702-dc6372a480ea"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def save(name, obj):
    (AQUI / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def huella(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


asig = load("propuestas/pendientes-muse-r6/epidemiologia/asignacion.json")
r5ent = load("propuestas/pendientes-muse-r5/epidemiologia/entrega.json")
falt = {p["iri"]: p["evidencia_faltante"] for p in r5ent["pendientes"]}
insp = load(f"data/portal/inspecciones/{DICC}.json")
fis = load(f"data/portal/inspecciones/{XLSX}.json")
FILAS = {i + 1: r for i, r in enumerate(insp["definiciones"])}
r5pkg = load("propuestas/pendientes-muse-r5/epidemiologia/evidencia/ckan_package_vigilancia.json")["result"]
r6meta = json.loads((AQUI / "evidencia/metadatos_r6.json").read_text(encoding="utf-8"))
cob = load("data/semantica/cobertura.json")
base = load("propuestas/pendientes-muse-r6/base.json")

# 1) Base intacta (solo lectura): cobertura coincide con base.json R6.
assert sha("data/semantica/cobertura.json") == base["sha"]["data/semantica/cobertura.json"], "base R6 alterada"

# 2) Huellas de fila recomputadas 25/25.
ok_h = 0
for s in asig["significados"]:
    n = int(s["definicion_iri"].rsplit("%2F", 1)[1])
    assert huella(FILAS[n]) == s["huella_fila_diccionario"], f"huella distinta fila {n}"
    ok_h += 1
assert ok_h == 25 == asig["conteo"]

# 3) Metadatos frescos R6 sin cambios vs R5: edicion 2022 fijada, sin Fuentes extras.
r5res = {r["id"]: r for r in r5pkg["resources"]}
for r in r6meta["recursos"]:
    o = r5res[r["id"]]
    for k in ("start_date", "end_date", "last_modified", "size", "format", "name"):
        assert str(r[k]) == str(o[k]), f"cambio en recurso {r['id']}.{k}"
assert r6meta["conjunto"]["fuentes_extras"] == r5pkg["fuentes_extras"] == ""
assert r6meta["conjunto"]["metadata_modified"] == r5pkg["metadata_modified"]

# 4) Estructura fisica observada (hoja SUIVE, 59 campos): espejo f, bloque
# institucional, bloque mensual+totales. Solo estructura, sin interpretar f.
campos = fis["tablas"][0]["campos"]
nombres = [c["id"] for c in campos]
assert len(nombres) == 59
bloq_a = nombres[11:23]   # pos 12-23 sin sufijo
bloq_f = nombres[23:35]   # pos 24-35 con sufijo
bloq_i = nombres[35:44]   # pos 36-44 institucional
bloq_m = nombres[44:59]   # pos 45-59 meses+periodo+totales
assert bloq_f == ["menores_1f", "de01_a_04f", "de05_a_09f", "de10_a_14f", "de15_a_19f",
                  "de20_a_24f", "de25_a_44f", "de45_a_49f", "de50_a_59f", "de60_a_64f",
                  "de65_y_maf", "se_ignoraf"]  # espejo exacto salvo de65_y_mas->de65_y_maf
assert [a for a in bloq_a if a not in ("de65_y_mas", "se_ignoran")] == \
       [b[:-1] for b in bloq_f if b not in ("de65_y_maf", "se_ignoraf")]
assert bloq_i == ["ssa", "imss_ord", "issste", "otras", "imss_sol", "d_if", "pemex", "sedena", "sedemar"]
assert bloq_m[-3:] == ["periodo", "totalm", "totalf"]
ESTRUCTURA = (f"SUIVE 59 campos: edad 12+12 espejo (pos12-23 {bloq_a[0]}..{bloq_a[-1]} / "
              f"pos24-35 {bloq_f[0]}..{bloq_f[-1]}), institucional pos36-44 ({','.join(bloq_i)}), "
              "mensual pos45-56 + periodo/totalm/totalf pos57-59. totalm='Total acumulado de "
              "Hombres', totalf='Total acumulado de Mujeres': unico 'acumulado' con objeto+particion, "
              "sin definir acumulado pos11 ni el sufijo f.")

# 5) Manual SUIVE 32 solo contexto + correccion: R06 cito SHA de 62 caracteres
# (imposible para SHA-256); el valor correcto desde bytes es el de 64.
PDF_REL_R5 = "propuestas/pendientes-muse-r5/catalogos-web/evidencia/manual_suive_32.pdf"
PDF_SHA = sha(PDF_REL_R5)
assert len(PDF_SHA) == 64 and PDF_SHA.startswith("f35746a0353c902b")
assert len("f35746a035c902b03d8ae1f703d1dfafdf3ad4bbf01777b648353d1b833757") == 62

# 6) Reintento CLI directo del xlsx 2026-10-23: 403 Cloudflare ( documented, sin evadir);
# se reutiliza la inspeccion previa 2026-10-23 como contexto, no como descarga nueva.

NOVEDAD = ("R6 linea nueva sin resolver. (a) Metadatos frescos 2026-10-23 del package: recurso "
           "de datos = edicion 'Vigilancia Epidemiológica - 2022' (2022-01-01/2022-12-31, "
           "3475599 B, publisher Inteligencia de Datos, region Caborca/Cajeme/Hermosillo/Navojoa/"
           "Santa Ana), diccionario CSV 2024-10-31; fuentes_extras vacio y sin nota metodologica: "
           "sin cambios vs R5. (b) Estructura fisica SUIVE verificada: " + ESTRUCTURA +
           " (c) Manual SUIVE 32 solo contexto: SHA correcto desde bytes " +
           PDF_SHA[:12] + "..." + PDF_SHA[-8:] + " (64 hex); el citado en R06 tenia 62 y era "
           "errata; Last-Modified 2021-08-10 precede al periodo 2022 sin vinculo "
           "edicion-recurso-periodo, luego no acredita columnas locales. (d) Reintento CLI del xlsx "
           "2026-10-23 = HTTP 403 Cloudflare; sin evadir WAF. Todo lo pendiente sigue en manos del "
           "publicador; evidencia negativa acotada, no ausencia universal.")

def fila_txt(n):
    r = FILAS[n]
    return (f"tipo={r['Tipo de dato']}; formato={r['Formato'] or 'no declarado'}; "
            f"desc={r['Descripción']}; ejemplo={r['Ejemplo de dato']}")

decisiones, pendientes = [], []
for s in sorted(asig["significados"], key=lambda x: x["definicion_iri"]):
    iri = s["definicion_iri"]
    n = int(iri.rsplit("%2F", 1)[1])
    motivo = (s["dictamen_documental"]["motivo"]
              + " Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.")
    ev = [f"data/portal/inspecciones/{DICC}.json:definiciones[{n}] ({fila_txt(n)})",
          f"huella_fila_diccionario={s['huella_fila_diccionario']} (recomputada OK 25/25 R6)",
          "data/semantica/cobertura.json (estado previo: fuera_del_nucleo_actual)",
          f"data/portal/inspecciones/{XLSX}.json:hoja=SUIVE:posicion={n} (esquema fisico 59 campos)",
          "propuestas/pendientes-muse-r6/epidemiologia/evidencia/metadatos_r6.json "
          "(R6: package fresco sin cambios; edicion datos 2022-01-01/2022-12-31; sin Fuentes extras)",
          "propuestas/pendientes-muse-r5/epidemiologia/entrega.json (R5 revisado, no repetido como hallazgo)",
          f"{PDF_REL_R5} (contexto R6: manual nacional, sha {PDF_SHA[:12]}..., sin vinculo local)"]
    decisiones.append({"definicion_iri": iri, "decision": "pendiente", "motivo": motivo,
                       "evidencia": ev,
                       "limites": ["Alcance simultaneo por conjunto, diccionario, definicion, nombre y "
                                   "descripcion; no autoriza cruces, homologaciones ni equivalencias.",
                                   "Evidencia negativa acotada a las busquedas R6 documentadas, no "
                                   "ausencia universal."],
                       "novedad_r6": NOVEDAD})
    pendientes.append({"definicion_iri": iri, "variable": s["variable"], "conjunto": CONJ,
                       "diccionario": DICC, "descripcion": s["descripcion"],
                       "tipo_dato": FILAS[n]["Tipo de dato"], "ejemplo": FILAS[n]["Ejemplo de dato"],
                       "motivo": s["dictamen_documental"]["motivo"],
                       "evidencia_faltante": falt[iri], "documento_exacto_necesario": falt[iri],
                       "en_manos_del_publicador": True})

fuentes = [
    {"localizador": f"data/portal/inspecciones/{DICC}.json", "sha256": sha(f"data/portal/inspecciones/{DICC}.json"),
     "aplicabilidad": "Diccionario local: 59 filas; huellas 25/25 recomputadas R6; descripciones literales y catalogo declarado vacio."},
    {"localizador": f"data/portal/inspecciones/{XLSX}.json", "sha256": sha(f"data/portal/inspecciones/{XLSX}.json"),
     "aplicabilidad": "Esquema fisico hoja SUIVE 59 campos pos1-59; espejo f, bloque institucional y mensual+totales observados sin interpretar."},
    {"localizador": "propuestas/pendientes-muse-r6/epidemiologia/evidencia/metadatos_r6.json",
     "sha256": sha("propuestas/pendientes-muse-r6/epidemiologia/evidencia/metadatos_r6.json"),
     "aplicabilidad": "R6: package fresco 2026-10-23 sin cambios; edicion datos 2022 fijada; sin Fuentes extras ni nota metodologica."},
    {"localizador": "propuestas/pendientes-muse-r5/epidemiologia/evidencia/ckan_package_vigilancia.json",
     "sha256": sha("propuestas/pendientes-muse-r5/epidemiologia/evidencia/ckan_package_vigilancia.json"),
     "aplicabilidad": "Instantanea R5 contra la que se compara (sin cambios R6)."},
    {"localizador": "data/semantica/cobertura.json", "sha256": sha("data/semantica/cobertura.json"),
     "aplicabilidad": "Estados previos de las 25 variables; coincide con base.json R6 (base intacta)."},
    {"localizador": PDF_REL_R5, "sha256": PDF_SHA,
     "aplicabilidad": "Contexto R6: manual nacional preservado; SHA corregido (R06 cito 62 hex); Last-Modified 2021-08-10 sin vinculo al recurso Sonora 2022."},
    {"localizador": "propuestas/pendientes-muse-r5/epidemiologia/entrega.json",
     "sha256": sha("propuestas/pendientes-muse-r5/epidemiologia/entrega.json"),
     "aplicabilidad": "Dictamen R5 revisado caso por caso; motivos confirmados con evidencia fresca R6."},
]

D = lambda *ns: [f"{BASE}definition/{DICC}%2F{n}" for n in ns]
sols = [
    {"id": "EPI-R6-01",
     "url_primaria": "https://datos.sonora.gob.mx/dataset/dca16d84-dbf0-4501-b702-dc6372a480ea",
     "documento_exacto_nuevo": "Instrumento SUIVE (manual/formato semanal) edicion aplicable al periodo "
      "2022-01-01/2022-12-31 del recurso 1689b19c, o nota del publicador Sonora que vincule edicion-recurso-periodo: "
      "objeto y version de cve_cie10; objeto y periodo/regla de acumulado; particion que denota el sufijo f; "
      "objeto contado del bloque ssa/imss_ord/issste/otras/imss_sol/d_if/pemex/sedena/sedemar. El portal hoy no "
      "publica Fuentes extras ni nota (verificado fresco R6).",
     "definiciones_afectadas": D(9, 11, 13, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44),
     "evidencia_exacta_requerida": "Fragmento con definicion por columna + vinculo edicion-recurso-periodo; URL, fecha y SHA del documento."},
    {"id": "EPI-R6-02",
     "url_primaria": "https://datos.sonora.gob.mx/dataset/dca16d84-dbf0-4501-b702-dc6372a480ea/resource/2334deaa-dd0c-444e-b038-4cc556ad715d",
     "documento_exacto_nuevo": "Diccionario corregido con descripcion para las 22 columnas hoy en 'Pendiente de "
      "especificar' + regla de computo de acumulado/totalm/totalf (preguntas cuantitativas verificables en el xlsx: "
      "¿totalm = suma serie sin sufijo? ¿totalf = suma serie f? ¿relacion acumulado vs totalm+totalf vs meses? "
      "¿f denota una particion por sexo dado totalf='Total acumulado de Mujeres'?).",
     "definiciones_afectadas": D(11, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44),
     "evidencia_exacta_requerida": "Filas del diccionario con descripcion no vacia + respuestas si/no a cada pregunta de computo."},
    {"id": "EPI-R6-03",
     "url_primaria": "https://datos.sonora.gob.mx/dataset/dca16d84-dbf0-4501-b702-dc6372a480ea",
     "documento_exacto_nuevo": "Version CIE aplicable al recurso 2022 para cve_cie10 (ejemplo 'A04, A08-A09 excepto "
      "A08.0', catalogo declarado vacio) + nota que fije el intervalo real de de01_a_04 (nombre 01-04 vs descripcion "
      "'entre 1 y 5 anos') y el tratamiento de la edad 5 frente a de05_a_09 ('entre 5 y 9').",
     "definiciones_afectadas": D(9, 13),
     "evidencia_exacta_requerida": "Vinculo version-recurso-periodo + texto que resuelva nombre vs descripcion y el solape en edad 5."},
]

entrega = {"rol": "epidemiologia", "generado_en_utc": datetime.now(timezone.utc).isoformat(),
           "alcance": ("25 significados del diccionario de Vigilancia Epidemiológica; R5 dejo 25 pendientes "
                       "con SW-EPI-01..03; R6 aporta metadatos frescos + estructura fisica + correccion SHA; "
                       "manual32 solo contexto."),
           "decisiones_significados": decisiones, "reglas": [], "conceptos_nuevos": {},
           "decisiones_columnas": [], "vinculos": [], "fuentes": fuentes, "pendientes": pendientes,
           "solicitudes_web_archivo": "solicitudes-web.json",
           "verificacion": {"asignados": 25, "decisiones": 25, "huella_fila_recomputada_ok": ok_h,
                             "reglas_nuevas": 0, "conceptos_nuevos": 0, "vinculos": 0}}
save("entrega.json", entrega)
save("solicitudes-web.json", {"rol": "epidemiologia", "destinatario": "web",
                              "nota": "Sin control de Obscura; IDs nuevos EPI-R6-01..03 (no reutilizan SW-EPI-*); "
                                       "URLs primarias del portal verificadas (R5 R05 + revalidacion R6).",
                              "solicitudes": sols})

h = hashlib.sha256((AQUI / "entrega.json").read_bytes()).hexdigest()
n_pen = sum(1 for d in decisiones if d["decision"] == "pendiente")
(AQUI / "resultado.md").write_text("\n".join([
    "# Resultado epidemiología (ronda 6)",
    "",
    f"Asignados: 25. Decisiones: 0 proponer, {n_pen} pendiente, 0 artefacto_documental.",
    "Reglas nuevas: 0. Conceptos nuevos: 0. Vínculos: 0. Columnas: 0.",
    "Solicitudes web: 3 (EPI-R6-01 a EPI-R6-03, IDs nuevos; no reutilizan SW-EPI-*).",
    "",
    "## Novedad R6 respecto de R5 (línea nueva, sin repetir negativos)",
    "",
    "- Metadatos frescos 2026-10-23 del package (evidencia/metadatos_r6.json): sin cambios vs R5. "
    "Fijan la edición aplicable: recurso 'Vigilancia Epidemiológica - 2022' "
    "(2022-01-01/2022-12-31, 3475599 B, Inteligencia de Datos, Caborca/Cajeme/Hermosillo/Navojoa/Santa Ana); "
    "diccionario CSV 2024-10-31; fuentes_extras vacío, sin nota metodológica.",
    "- Estructura física SUIVE (59 campos, posiciones verificadas): serie edad 12+12 en espejo "
    "exacto (pos12-23 sin sufijo / pos24-35 con sufijo f, salvo de65_y_mas→de65_y_maf); bloque "
    "institucional pos36-44 (ssa, imss_ord, issste, otras, imss_sol, d_if, pemex, sedena, sedemar); "
    "bloque mensual pos45-56 + periodo/totalm/totalf pos57-59. totalm/totalf ('Total acumulado de "
    "Hombres/Mujeres') es el único 'acumulado' con objeto+partición; no define acumulado pos11 ni el sufijo f.",
    "- Manual SUIVE 32 solo contexto + corrección: SHA correcto desde bytes " + PDF_SHA + " (64 hex); "
    "el citado en R06 tenía 62 y era errata. Last-Modified 2021-08-10 precede al periodo 2022 y no hay "
    "vínculo edición-recurso-periodo: no acredita ninguna columna local.",
    "- Reintento CLI directo del xlsx 2026-10-23 → HTTP 403 Cloudflare; sin evadir WAF. Se reutiliza la "
    "inspección previa 2026-10-23 como contexto, no como descarga nueva.",
    "- Huellas de fila recomputadas con huella() de scripts/consolidar_semantica.py: 25/25 OK; "
    "base R6 intacta (cobertura.json coincide con base.json).",
    "- 25 pendientes confirmados con documento exacto necesario, todo en manos del publicador "
    "(ver entrega.json → pendientes). No se aprueba por nombre; no se inventa definición.",
    "",
    "## Verificación",
    "",
    "- Fuentes con SHA recomputado desde bytes en este script (no transcritos).",
    "- Reglas, conceptos y vínculos: 0 (sin colisiones que verificar).",
    "",
    "## Archivos",
    "",
    "- entrega.json, solicitudes-web.json, resultado.md, listo.json, construir.py, evidencia/metadatos_r6.json",
    f"- sha256(entrega.json) = {h}",
    ""]) + "\n", encoding="utf-8")
save("listo.json", {"rol": "epidemiologia", "entrega": "entrega.json", "sha256": h,
                    "cuentas": {"asignados": 25, "proponer_significados": 0,
                                "pendiente_significados": n_pen, "reglas_nuevas": 0,
                                "conceptos_nuevos": 0, "decisiones_columnas": 0,
                                "vinculos": 0, "solicitudes_web": len(sols)},
                    "estado": "completo"})
print("listo sha:", h, "| decisiones:", len(decisiones), "| pendientes:", len(pendientes))
