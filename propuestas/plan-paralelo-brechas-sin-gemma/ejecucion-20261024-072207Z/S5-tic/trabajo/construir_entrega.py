"""Construye v001/entrega.json para S5-tic (24 IDs). Solo usa bytes existentes y
asignacion.json inmutable como entrada. No modifica nada fuera de trabajo/ y v001/."""
import hashlib
import json
from pathlib import Path

PROY = Path(".")
ASIG = PROY / "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S5-tic/asignacion.json"
V001 = PROY / "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S5-tic/v001"
V001.mkdir(parents=True, exist_ok=True)
FECHA = "2026-10-24"

asig = json.loads(ASIG.read_text(encoding="utf-8"))
assert asig["rol"] == "S5-tic", asig["rol"]
casos = asig["casos"]
assert len(casos) == 24, len(casos)

OBS = {
    "ruta": "propuestas/cierre-brechas-post-r6/web-obscura/obs-diagnostico-2026-10-24.json",
    "sha256": hashlib.sha256((PROY / "propuestas/cierre-brechas-post-r6/web-obscura/obs-diagnostico-2026-10-24.json").read_bytes()).hexdigest(),
    "localizador": "/observacion/veredicto + /observacion/iframe_powerbi_src",
    "afirmacion_soportada": (
        "Inspeccion Obscura con DOM renderizado 2026-10-24T06:51:28Z de "
        "https://www.sonora.gob.mx/datos/diagnostico-entorno-digital: cascaron JS confirmado "
        "(main vacio, body 340 chars solo menu), sin cuestionario/codebook/tabla de variables "
        "extraible; contenido sustantivo en iframe PowerBI que requiere interaccion y no se afirma; "
        "sin fuente vinculada a fila/campo/recurso/edicion."
    ),
}

GATE = (
    " | Puerta S5-tic 2026-10-24: sin_pista_nueva. Verificacion SHA-256 OK de la evidencia previa; "
    "la URL https://www.sonora.gob.mx/datos/diagnostico-entorno-digital ya fue examinada por webfetch "
    "y por Obscura con DOM renderizado el mismo dia sin cuestionario extraible; barrido local sin "
    "instrumento inedito. Se cierra como brecha externa conservando la evidencia previa; no se propone significado."
)

decisiones = []
for c in casos:
    orig = c["original"]
    o_sha = hashlib.sha256(
        json.dumps(orig, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    ev = [dict(e) for e in orig["evidencia"]]
    for e in c["antecedente"]["evidencia"]:
        if e["ruta"] not in {x["ruta"] for x in ev}:
            ev.append(dict(e))
    ev.append(dict(OBS))
    decisiones.append(
        {
            "id": c["id"],
            "tipo": c["tipo"],
            "original_sha256": o_sha,
            "puerta": "sin_pista_nueva",
            "pista": None,
            "estado": "brecha_externa",
            "afirmacion_propuesta": None,
            "motivo": orig["motivo"] + GATE,
            "evidencia_faltante": orig["evidencia_faltante"],
            "evidencia": ev,
            "condicion_reapertura": (
                "Reabrir solo si aparece fuente primaria vinculada a fila/recurso/edicion que "
                "aporte el documento faltante citado en evidencia_faltante (cuestionario o instrumento "
                "del Diagnostico del Entorno Digital, o muestra de valores del recurso para el campo, "
                "con edicion y periodo acreditados). No reabre: distribuciones, nombres parecidos, "
                "ejemplos del diccionario, metadatos CKAN sin vinculo a fila, ni contenido PowerBI "
                "sin trazabilidad a campo."
            ),
            "limites": list(orig["limites"]),
        }
    )

# Fuentes: archivos tocados en esta ejecucion (hash de bytes existentes, fecha sin hora).
tocados = sorted({e["ruta"] for d in decisiones for e in d["evidencia"]})
tocados.append("propuestas/investigacion-post-r6/tic/evidencia/diagnostico-entorno-digital.bin")
fuentes = []
for r in sorted(set(tocados)):
    b = (PROY / r).read_bytes()
    if r.endswith("obs-diagnostico-2026-10-24.json"):
        loc = "lectura integra S5-tic 2026-10-24 (veredicto + iframe PowerBI)"
    elif r.endswith("nueva-tic-sonora-2026-10-24.md"):
        loc = "lectura integra S5-tic 2026-10-24 (busqueda negativa acotada del dia)"
    elif r.endswith("diagnostico-entorno-digital.bin"):
        loc = "lectura parcial S5-tic 2026-10-24 (cabecera 600 bytes: HTML cascaron JS preservado)"
    else:
        loc = "verificacion de integridad SHA-256 S5-tic 2026-10-24 (bytes identicos a lo citado; contenido examinado en rondas previas)"
    fuentes.append(
        {
            "ruta": r,
            "sha256": hashlib.sha256(b).hexdigest(),
            "url": None,
            "fecha_consulta": FECHA,
            "localizador": loc,
        }
    )

entrega = {
    "rol": "S5-tic",
    "version": "v001",
    "decisiones": decisiones,
    "fuentes": fuentes,
    "novedades": (
        "Sin novedades: ninguna pista nueva (URL/documento/anexo concreto no examinado antes) "
        "para los 24 IDs. La unica URL candidata del dia "
        "(https://www.sonora.gob.mx/datos/diagnostico-entorno-digital) ya fue examinada por "
        "webfetch y por Obscura con DOM renderizado el 2026-10-24 sin cuestionario extraible. "
        "No se repitieron busquedas genericas agotadas ni se reinspecciono la pagina sin pista. "
        "No se emitio peticion a W-web: el navegador compartido ya cubrio la pagina interactiva "
        "el mismo dia; sin URL nueva no hay nada que pedir. Paquete W-web ausente al cierre local."
    ),
}

out = V001 / "entrega.json"
out.write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("decisiones:", len(decisiones))
print("fuentes:", len(fuentes))
print("bytes:", out.stat().st_size)
