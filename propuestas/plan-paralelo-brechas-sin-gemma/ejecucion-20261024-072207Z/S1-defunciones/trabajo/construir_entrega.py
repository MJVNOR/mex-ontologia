"""Construye registro de primera puerta, peticion web y entrega v001 de S1-defunciones."""
import json, hashlib
from datetime import datetime, timezone

BASE = "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S1-defunciones"
AHORA = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def sha_file(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

asig = json.load(open(f"{BASE}/asignacion.json", encoding="utf-8"))
casos = asig["casos"]
assert len(casos) == 32, len(casos)

# 1. Verificar SHA de evidencia previa citada en antecedentes
rutas = set()
for c in casos:
    for e in c["antecedente"].get("evidencia", []) + c["original"].get("evidencia", []):
        rutas.add(e["ruta"])
bad = []
for r in sorted(rutas):
    try:
        h = sha_file(r)
    except FileNotFoundError:
        bad.append((r, "FALTA_ARCHIVO"))
        continue
    # comparar contra cada sha declarado para esa ruta
    decl = set()
    for c in casos:
        for e in c["antecedente"].get("evidencia", []) + c["original"].get("evidencia", []):
            if e["ruta"] == r:
                decl.add(e["sha256"])
    if h not in decl:
        bad.append((r, f"SHA_DIFERENTE actual={h} declarados={sorted(decl)}"))
print("archivos previos verificados:", len(rutas), "problemas:", bad)

# 2. Registro de primera puerta
pares = {"%2F38", "%2F72", "%2F73", "%2F74", "%2F75"}  # IDs ligados a pares estructurales (dependencias-correspondencias.json)
registro = {
    "rol": "S1-defunciones",
    "fecha_utc": AHORA,
    "metodo": "webfetch/websearch independientes + material local; sin Obscura (reservado a W-web)",
    "comprobaciones": [
        {"url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=cd3d6e34-3789-479e-9f2b-a717b8419f9c",
         "fecha_consulta": "2026-10-24",
         "resultado": "cambio_de_fuente_por_comprobar examinado sin novedad: metadata_modified 2025-08-15, 2 recursos, notes y descriptions identicos a lo ya examinado en R6/ronda-3; sin codebook, sin tabla columna<->campo, sin edicion CIE, sin distincion fetal/general. Re-descargar lo mismo no es pista nueva."},
        {"url": "http://www.dgis.salud.gob.mx/contenidos/sinais/s_clues.html",
         "fecha_consulta": "2026-10-24",
         "archivo": "trabajo/fuentes-nuevas/s_clues_2026-10-24.txt",
         "resultado": "negativo: pagina administrativa del Subsistema CLUES (ultima modificacion 2025-06-26, post-periodo); enumera informacion captada (entidad/municipio/localidad, tipo, institucion) sin campo 'jurisdiccion', sin codebook campo-codigo, sin edicion aplicable al recurso 2022, sin vinculo al extracto Sonora. No define JURISDICCION_CLUES(D) ni valida ejemplos '6'/'SAN LUIS RIO COLORADO'."},
        {"url": "https://www.sonora.gob.mx/datos/defunciones",
         "fecha_consulta": "2026-10-24",
         "resultado": "sin texto util por lectura simple (solo chrome de navegacion; aplicacion renderizada). No reintentado con genericos: se deriva una peticion acotada a W-web (trabajo/peticiones-web.json S1-WEB-01) sobre ambito general/fetal y fuente/periodo declarados."},
        {"url": "http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html",
         "fecha_consulta": None,
         "resultado": "ya examinado por cobertura-muse 2026-10-23 (plan-cobertura-muse/investigacion-obscura/evidencia.json): sin confirmacion, vigencia no acreditada. No re-examinado."},
    ],
    "puerta_por_id": {},
}
for c in casos:
    suf = "%2F" + c["id"].split("%2F")[-1]
    registro["puerta_por_id"][c["id"]] = {
        "variable": c["original"]["variable"],
        "puerta": "sin_pista_nueva",
        "detalle": "Examen SEED-2022 por ID ya hecho + contraste DGIS DEFUN 2022 ya hecho (antecedente 2026-10-24). "
                   "Comprobaciones v001 (package_show sin cambios; s_clues.html sin codebook) no aportan codebook/tabla campo-codigo-edicion no examinada. "
                   + ("ID ligado a par estructural candidato (dependencias-correspondencias.json); sin definicion no hay promocion." if suf in pares else "Sin par estructural dependiente."),
    }
json.dump(registro, open(f"{BASE}/trabajo/registro-primera-puerta.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 3. Peticion web a W
fetales = [c["id"] for c in casos if c["id"].split("%2F")[-1] in
           ["17", "32", "33", "34", "35", "36", "37", "38", "76", "77"]]
peticiones = {
    "rol": "S1-defunciones",
    "fecha_utc": AHORA,
    "peticiones": [{
        "id": "S1-WEB-01",
        "ids_casos": fetales,
        "pregunta": "En la herramienta https://www.sonora.gob.mx/datos/defunciones (renderizada; lectura simple solo devuelve el menu): "
                    "¿declara si 'Defunciones 2022' cubre solo certificado general o tambien muerte fetal, y que fuente/periodo/SEED declara?",
        "por_que_esta_fuente": "Unica fuente del publicador aun no examinada con render; podria fijar el ambito fetal-vs-general de 10 IDs ambiguos. No resuelve definiciones ni codebooks aunque responda.",
        "novedad": "Pagina enlazada desde la portada del portal, nunca examinada (fetch 2026-10-24 sin texto util).",
        "examinado_antes": ["pagina dataset CKAN", "pagina recurso 6f39fc5d", "package_show", "Manual SEED 2022",
                            "pagina SEED DGIS", "descriptor DGIS DEFUN 2022 + catalogos", "s_clues.html", "clues_gobmx.html"],
        "resultado": "pendiente",
    }],
}
json.dump(peticiones, open(f"{BASE}/trabajo/peticiones-web.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 4. Entrega v001
GATE = (" Primera puerta v001: sin_pista_nueva. Re-verificacion package_show 2026-10-24 sin cambios "
        "(sin codebook/tabla/edicion); s_clues.html 2026-10-24 negativo para codebook campo-codigo "
        "(ver trabajo/registro-primera-puerta.json). No se repiten busquedas genericas agotadas.")
decisiones = []
for c in casos:
    orig = c["original"]
    ant = c["antecedente"]
    o_sha = hashlib.sha256(json.dumps(orig, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()
    suf = "%2F" + c["id"].split("%2F")[-1]
    ev = []
    for e in ant.get("evidencia", []):
        ev.append({"ruta": e["ruta"], "sha256": e["sha256"],
                   "localizador": e.get("localizador", ""),
                   "afirmacion_soportada": e.get("afirmacion_soportada", "")})
    lims = list(ant.get("limites", []))
    lims.append("v001: sin re-examen SEED por ID (ya hecho); codebook/tabla campo-codigo-edicion no examinada: ninguna localizada.")
    if suf in pares:
        lims.append("ID ligado a par estructural candidato (dependencias-correspondencias.json, estado candidata_por_nombre): sin definicion propuesta el par permanece par_estructural_revisado_significado_pendiente.")
    decisiones.append({
        "id": c["id"],
        "tipo": c["tipo"],
        "original_sha256": o_sha,
        "puerta": "sin_pista_nueva",
        "pista": None,
        "estado": "brecha_externa",
        "afirmacion_propuesta": None,
        "motivo": ant.get("motivo", "") + GATE,
        "evidencia_faltante": ant.get("evidencia_faltante", ""),
        "evidencia": ev,
        "condicion_reapertura": "Reapertura solo si el publicador (Secretaria de Salud Publica de Sonora, Inteligencia de Datos) publica: "
                                + ant.get("evidencia_faltante", "") + " Adenda posible del coordinador si W-web (S1-WEB-01) aporta documento resolutivo.",
        "limites": lims,
    })

fuentes = [{
    "ruta": "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S1-defunciones/trabajo/fuentes-nuevas/s_clues_2026-10-24.txt",
    "sha256": sha_file(f"{BASE}/trabajo/fuentes-nuevas/s_clues_2026-10-24.txt"),
    "url": "http://www.dgis.salud.gob.mx/contenidos/sinais/s_clues.html",
    "fecha_consulta": "2026-10-24",
    "localizador": "Pagina completa (texto): objetivo/cobertura/informacion captada; ultima modificacion 2025-06-26",
}]
entrega = {
    "rol": "S1-defunciones",
    "version": "v001",
    "decisiones": decisiones,
    "fuentes": fuentes,
    "novedades": {
        "propuestas_acreditadas": 0,
        "brechas_externas": 32,
        "accesos_no_resueltos": 0,
        "nuevo_verificado": ["package_show cd3d6e34 re-verificado 2026-10-24 sin cambios (no es pista nueva)",
                             "s_clues.html examinado 2026-10-24: negativo para codebook campo-codigo-edicion",
                             "sonora.gob.mx/datos/defunciones sin texto por lectura simple -> peticion S1-WEB-01 a W-web (pendiente, no bloquea cierre local)"],
    },
}
raw = json.dumps(entrega, ensure_ascii=False, separators=(",", ":"))
open(f"{BASE}/v001/entrega.json", "w", encoding="utf-8").write(raw)
# verificar cargable + conteos
rec = json.load(open(f"{BASE}/v001/entrega.json", encoding="utf-8"))
assert len(rec["decisiones"]) == 32
assert {d["id"] for d in rec["decisiones"]} == {c["id"] for c in casos}
assert all(d["estado"] == "brecha_externa" and d["pista"] is None and d["afirmacion_propuesta"] is None for d in rec["decisiones"])
print("entrega.json OK: 32 decisiones brecha_externa, cargable")
