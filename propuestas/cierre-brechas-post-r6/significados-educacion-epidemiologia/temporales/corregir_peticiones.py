"""Correccion formal de peticiones-web.json (dictamen auditoria-significados-anomalias).

- casos: listas IRI completas desde asignacion.json (sin abreviaturas).
- WEB-EPI-02: 23 IDs (25 epi menos /9 y /11 de WEB-EPI-01).
- WEB-MAT-01/02: alcance muestra (4+4 de 30); WEB-MAT-00: 22 no preguntadas,
  cubiertas por revision local/investigacion agotada, sin nueva busqueda.
- estado por peticion + referencia a cobertura web-obscura (ruta+SHA) si atendida;
  lo no atendido queda pendiente, nada no factible se cuenta como cumplido.
- Serializa con json.dumps; refresca cierrelisto.json al final y congela.
No toca asignacion.json ni fuentes historicas; no rehace investigacion.
"""
import hashlib
import json
from pathlib import Path

BASE = Path(".")
CARP = Path("propuestas/cierre-brechas-post-r6/significados-educacion-epidemiologia")
COB = "propuestas/cierre-brechas-post-r6/web-obscura/cobertura-peticiones.json"
COB_SHA = hashlib.sha256((BASE / COB).read_bytes()).hexdigest()

asig = json.loads((CARP / "asignacion.json").read_text(encoding="utf-8"))
epi = [c["definicion_iri"] for c in asig["casos"] if c.get("grupo_fuente") == "epidemiologia"]
mat = [c["definicion_iri"] for c in asig["casos"] if c.get("grupo_fuente") == "matriculas"]
assert len(epi) == 25 and len(mat) == 30

EPI_01 = [i for i in epi if i.split("%2F")[1] in ("9", "11")]
EPI_02 = [i for i in epi if i not in EPI_01]
MAT_01 = [i for i in mat if i.split("%2F")[1] in ("8", "12", "58", "54")]
MAT_02 = [i for i in mat if i.split("%2F")[1] in ("63", "64", "65", "66")]
MAT_00 = [i for i in mat if i not in MAT_01 + MAT_02]
assert len(EPI_01) == 2 and len(EPI_02) == 23
assert len(MAT_01) == 4 and len(MAT_02) == 4 and len(MAT_00) == 22
assert len(set(EPI_01 + EPI_02)) == 25 and len(set(MAT_01 + MAT_02 + MAT_00)) == 30

cob_ref = {"ruta": COB, "sha256": COB_SHA,
           "nota": "Entrada de esta carpeta: atendida parcial via webfetch-nativa "
                   "(F-SUIVE-01: manual SUIVE-32 + formato SUIVE-1 2021 + boletin; "
                   "referente nacional sin vinculo del publicador). Negativo acotado, no resuelve."}

pet = {
    "agente": "significados-educacion-epidemiologia",
    "destinatario": "agente web-obscura",
    "fecha": "2026-10-24",
    "nota": "NO manejar navegador Obscura desde otro agente; estas peticiones son para el "
            "agente web-obscura. Casos siempre como listas IRI completas de asignacion.json.",
    "peticiones": [
        {"id": "WEB-EPI-01", "casos": EPI_01, "conteo": 2, "alcance": "completa",
         "consulta": "Manual SUIVE/SUAVE edicion 2022 (DGE/Sonora) que fije objeto de cve_cie10 "
                     "+ version CIE vinculada al recurso 1689b19c y regla de computo de columna acumulado pos 11",
         "urls_sugeridas": [
             "https://datos.sonora.gob.mx/dataset/dca16d84-dbf0-4501-b702-dc6372a480ea",
             "https://www.gob.mx/salud/acciones-y-programas/sistema-unico-de-informacion-para-la-vigilancia-epidemiologica-suive"],
         "brecha": "EPI-R6-01 + EPI-R6-03: sin instrumento edicion 2022 ni version CIE vinculada; "
                   "manual preservado es 2021-08-10 (anterior al periodo 2022).",
         "estado": "atendida_parcial_negativa",
         "resultado_web_obscura": cob_ref},
        {"id": "WEB-EPI-02", "casos": EPI_02, "conteo": 23, "alcance": "completa",
         "consulta": "Nota/diccionario corregido del publicador Sonora que fije intervalo 01-04 vs "
                     "'entre 1 y 5', solape edad 5, convencion sufijo f (serie 24-35 y se_ignoraf), "
                     "sentido de se_ignoran y objeto contado de columnas institucionales "
                     "(ssa/imss_ord/issste/otras/imss_sol/d_if/pemex/sedena/sedemar)",
         "urls_sugeridas": [
             "https://datos.sonora.gob.mx/dataset/dca16d84-dbf0-4501-b702-dc6372a480ea"],
         "brecha": "EPI-R6-01 + EPI-R6-02: 22 filas 'Pendiente de especificar'; manual nacional "
                   "(30 cols, otra lista institucional) no resuelve layout local de 59 cols.",
         "estado": "atendida_parcial_negativa",
         "resultado_web_obscura": cob_ref},
        {"id": "WEB-MAT-01", "casos": MAT_01, "conteo": 4, "alcance": "muestra",
         "consulta": "Documento UES/COESPO 2022 (guia, calendario 2022-2, diccionario o muestra de "
                     "valores) que defina la clave '222 (Reing)'/'222 (NI)' y el ciclo actual/senalado "
                     "de referencia del recurso Matriculas-2022-2",
         "urls_sugeridas": ["https://datos.sonora.gob.mx/ (conjunto matriculas UES, recurso 58f2d5a6)"],
         "brecha": "Sin definicion de la clave 222/221/223 ni del ciclo de referencia; dominio empirico no fija sentido.",
         "estado": "atendida_parcial_negativa",
         "resultado_web_obscura": cob_ref},
        {"id": "WEB-MAT-02", "casos": MAT_02, "conteo": 4, "alcance": "muestra",
         "consulta": "Norma UES era-2022 que contenga 'no exigibilidad' o 'examen profesional' como "
                     "alternativa de titulacion (Guia feb2023 solo trae 'Constancia de No Exigibilidad' "
                     "como tramite, posterior al periodo 2022-2 y sin vinculo a fila+huella)",
         "urls_sugeridas": ["https://ues.mx/archivos/conocenos/normatividad",
                            "https://ues.sonora.edu.mx/proyectos/titulacion"],
         "brecha": "Terminos sin norma vinculada a edicion-recurso-periodo 2022-2.",
         "estado": "pendiente",
         "resultado_web_obscura": None,
         "nota_revision_local": "Guia UES feb2023 examinada localmente (PDF+TXT con SHA en esta carpeta): "
                                "'No Exigibilidad' solo como constancia de tramite, no resolutoria; ver entrega.json."},
        {"id": "WEB-MAT-00", "casos": MAT_00, "conteo": 22, "alcance": "revision_local",
         "consulta": "Sin nueva busqueda: 22 IDs de matriculas cubiertos por revision local "
                     "(datastore live 2026-10-24 sin cambios + distribuciones empiricas del recurso "
                     "58f2d5a6 + normativa UES 2019/2021/2022_01/2023/2026 ya examinada).",
         "urls_sugeridas": [],
         "brecha": "Investigacion agotada para estos IDs; forzar busqueda repetiria lineas cerradas.",
         "estado": "cubierta_revision_local",
         "resultado_web_obscura": None,
         "referencia_local": "entrega.json (decisiones y fuentes con SHA re-verificado) en esta carpeta."},
    ],
    "conteos": {"peticiones": 5, "ids_epidemiologia": 25, "ids_matriculas": 30,
                "ids_cubiertos_web": 33, "ids_cubiertos_revision_local": 22, "ids_total": 55},
}

(CARP / "peticiones-web.json").write_text(
    json.dumps(pet, ensure_ascii=False, indent=2), encoding="utf-8")
chk = json.loads((CARP / "peticiones-web.json").read_text(encoding="utf-8"))
assert chk["conteos"]["ids_total"] == 55
assert sum(p["conteo"] for p in chk["peticiones"]) == 55
assert all(isinstance(p["casos"], list) and all(c.startswith("https://") for c in p["casos"])
           for p in chk["peticiones"])
assert all("..." not in json.dumps(p["casos"]) for p in chk["peticiones"])

# Nota actual en entrega.json/md: cobertura parcial disponible (ruta+SHA), sin reabrir fondo.
ent = json.loads((CARP / "entrega.json").read_text(encoding="utf-8"))
ent["novedades_frente_a_investigacion_previa"][3] = (
    "Cobertura web-obscura disponible tras el cierre: " + COB + " (sha256 " + COB_SHA + "): "
    "peticiones de esta carpeta atendidas parcialmente via webfetch-nativa (F-SUIVE-01, referente "
    "nacional sin vinculo del publicador); negativo acotado, nada promovido. WEB-MAT-02 sigue "
    "pendiente; 22 matriculas cubiertas por revision local (WEB-MAT-00 en peticiones-web.json).")
ent["busquedas_limitadas"][3] = {
    "proveedor_herramienta": "web-obscura / cobertura-peticiones.json",
    "consulta": "peticiones-web.json (WEB-EPI-01/02, WEB-MAT-01/02)",
    "url": "", "fecha": "2026-10-24",
    "resultado": "Atendida parcial via webfetch-nativa (F-SUIVE-01 y fuentes F-*): referentes "
                 "nacionales sin vinculo del publicador; negativo acotado, sin promocion.",
    "fuente_primaria": COB + " sha256:" + COB_SHA}
(CARP / "entrega.json").write_text(
    json.dumps(ent, ensure_ascii=False, indent=2), encoding="utf-8")
json.loads((CARP / "entrega.json").read_text(encoding="utf-8"))

md = (CARP / "entrega.md").read_text(encoding="utf-8")
md = md.replace(
    "Resto de busquedas nativas sin pista primaria nueva;\n web-obscura pendiente (peticiones-web.json).",
    "Resto de busquedas nativas sin pista primaria nueva;\n cobertura web-obscura parcial y negativa en `" + COB + "` (sha256 `" + COB_SHA[:16] + "`...); WEB-MAT-02 pendiente, 22 matriculas en revision local.")
(CARP / "entrega.md").write_text(md, encoding="utf-8")

# Refresca marcador de todos los archivos al FINAL y congela.
archivos = ["peticiones-web.json", "entrega.json", "entrega.md",
            "Guia_Opciones_Titulacion_UES_feb2023.pdf",
            "Guia_Opciones_Titulacion_UES_feb2023.txt",
            "temporales/generar_entrega.py", "temporales/corregir_peticiones.py"]
cierre = {
    "archivos": [{"ruta": str(CARP / n),
                  "sha256": hashlib.sha256((CARP / n).read_bytes()).hexdigest()}
                 for n in archivos],
    "conteos": {"decisiones": 55, "sigue_pendiente": 55,
                "propuesta_resolucion": 0, "fuentes": 12},
}
(CARP / "cierrelisto.json").write_text(
    json.dumps(cierre, ensure_ascii=False, indent=2), encoding="utf-8")
print("OK: peticiones=%d, ids=%d, archivos=%d"
      % (len(chk["peticiones"]), sum(p["conteo"] for p in chk["peticiones"]), len(archivos)))
