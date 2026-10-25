import json, hashlib

P = "https://example.org/mex-ontologi/definition/"
a = json.load(open("asignacion.json", encoding="utf-8"))
iris = [c["definicion_iri"] for c in a["casos"]]
assert len(iris) == 29 and len(set(iris)) == 29
tic = [i for i in iris if "3851f1c3" in i or "bdbf043f" in i or "f3ecd3d2" in i
       or "8f8e3cfb" in i or "c65eb4e7" in i or "063058e6" in i
       or "a4e8bee0" in i or "af14d207" in i]
assert len(tic) == 24, len(tic)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

R = "obs-sha-no-aplica"
w = "../web-obscura/"
obs_diag = w + "obs-diagnostico-2026-10-24.json"
obs_dgis = w + "obs-dgis-2026-10-24.json"

pet = {
    "fecha": "2026-10-24",
    "nota": ("Navegacion Obscura compartida reservada al agente web-obscura; "
             "este archivo es la peticion. Al crearla (2026-10-24 temprano) el paquete "
             "web-obscura aun no habia salido; resultados disponibles despues se "
             "referencian abajo con ruta y SHA, sin alterar originales ni fuentes historicas."),
    "consultas": [
        {"id": "WEB-TIC-01", "estado": "atendida_negativa",
         "casos": sorted(tic),
         "conteo_casos": 24, "alcance": "total",
         "consulta": "Sonora Diagnostico del Entorno Digital: cuestionario/codebook que fije referentes, textos completos y dominios (24 IDs TIC)",
         "url_sugerida": "https://datos.sonora.gob.mx/",
         "utilidad": "Cuestionario/codebook vinculado a fila",
         "resultado_web_obscura": {
             "ruta": "propuestas/cierre-brechas-post-r6/web-obscura/obs-diagnostico-2026-10-24.json",
             "sha256": sha(obs_diag),
             "veredicto": "Negativo via DOM renderizado: cascaron JS + PowerBI, sin cuestionario extraible. No se cuenta como cumplida: brecha intacta."}},
        {"id": "WEB-DIV-EGR", "estado": "atendida_negativa",
         "casos": [P + "f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15"],
         "conteo_casos": 1, "alcance": "total",
         "consulta": "DGIS Descripcion de variables egresos hospitalarios (Total_Egresos: egresos vs urgencias)",
         "url_sugerida": "https://www.gob.mx/salud/acciones-y-programas/direccion-general-de-informacion-en-salud-dgis",
         "utilidad": "Tabla de variables aplicable a la fila",
         "resultado_web_obscura": {
             "ruta": "propuestas/cierre-brechas-post-r6/web-obscura/obs-dgis-2026-10-24.json",
             "sha256": sha(obs_dgis),
             "veredicto": "Negativo via DOM renderizado: pagina carga sin tabla (text_len 9, iframe Fuentes vacio). No se cuenta como cumplida."}},
        {"id": "WEB-DIV-CLASIF", "estado": "pendiente",
         "casos": [P + "67156807-2013-4117-9ca9-394aea647127%2F5"],
         "conteo_casos": 1, "alcance": "total",
         "consulta": "CONAPO IMUC 2020: documento que declare que clasifica CLASIF (limite C1)",
         "url_sugerida": "https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372",
         "utilidad": "Objeto clasificado",
         "resultado_web_obscura": None},
        {"id": "WEB-DIV-TRIM", "estado": "pendiente",
         "casos": [P + "3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2"],
         "conteo_casos": 1, "alcance": "total",
         "consulta": "Sonora PROAES: metodologia que defina 'estrato' (TRIMESTRE)",
         "url_sugerida": "https://datos.sonora.gob.mx/",
         "utilidad": "Definicion de estrato",
         "resultado_web_obscura": None},
        {"id": "WEB-DIV-PESCA", "estado": "pendiente",
         "casos": [P + "863b9cc8-daeb-4430-b835-6a0ced5abd31%2F7",
                   P + "863b9cc8-daeb-4430-b835-6a0ced5abd31%2F8"],
         "conteo_casos": 2, "alcance": "total",
         "consulta": "Sonora SAGARHPA pesca: diccionario/metodologia que complete Clave/Nombre de otras",
         "url_sugerida": "https://datos.sonora.gob.mx/",
         "utilidad": "Objeto y catalogo de 'otras'",
         "resultado_web_obscura": None},
    ],
}
tot = sum(c["conteo_casos"] for c in pet["consultas"])
assert tot == 29, tot
flat = [i for c in pet["consultas"] for i in c["casos"]]
assert sorted(flat) == sorted(iris), "cobertura IRI inexacta"
assert all(i.startswith(P) and "%2F" in i for i in flat), "abreviatura detectada"

open("peticiones-web.json", "w", encoding="utf-8").write(json.dumps(pet, ensure_ascii=False, indent=1))
json.load(open("peticiones-web.json", encoding="utf-8"))
print("peticiones OK: 5 consultas, 29 IRIs, 2 atendidas_negativas, 3 pendientes")

# Re-serializar entrega.json con json.dumps y verificar carga (sin cambios de fondo)
e = json.load(open("entrega.json", encoding="utf-8"))
assert len(e["decisiones"]) == 29
open("entrega.json", "w", encoding="utf-8").write(json.dumps(e, ensure_ascii=False, indent=1))
json.load(open("entrega.json", encoding="utf-8"))
print("entrega.json re-serializada y cargable")

# Refrescar marcador final de todos los archivos y congelar
arch = ["entrega.json", "entrega.md", "peticiones-web.json",
        "evidencia/nueva-dgis-egresos-2026-10-24.md",
        "evidencia/nueva-tic-sonora-2026-10-24.md",
        "evidencia/nueva-diversos-2026-10-24.md",
        "verifica.py", "corrige_peticiones.py"]
files = [{"ruta": p, "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest()} for p in arch]
json.dump({"archivos": files,
           "conteos": {"decisiones": 29, "sigue_pendiente": 29, "propuesta_resolucion": 0,
                       "consultas_web": 5, "atendidas_negativas": 2, "pendientes": 3}},
          open("cierrelisto.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cierrelisto OK:", len(files), "archivos")
