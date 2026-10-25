"""Actualiza cambio_modelo/conteos a la eleccion final y regenera decisiones+SHA."""
import hashlib
import json
from pathlib import Path

MINE = Path("propuestas/pendientes-muse-r4/chat")
ev = json.loads((MINE / "evaluacion.json").read_text(encoding="utf-8"))
entrega = json.loads((MINE / "entrega.json").read_text(encoding="utf-8"))

entrega["cambio_modelo"] = {
    "autorizado": "usuario: 'Gemini 3.1 Flash Lite' y luego 'o este Gemma 4 31B'; prioridad Gemma; luego segunda opcion exacta gemini-3.1-flash-lite (segundo y ultimo candidato); mantener proveedor/cuenta/clave; sin rotar credenciales ni proxy",
    "modelo_elegido_real": "gemini-3.1-flash-lite",
    "anterior_efectivo": "gemini-3.5-flash (sigue activo en Studio vivo; nunca vuelto a llamar)",
    "id_exactitud": "IDs del listado API, no inventados",
    "cambio_aplicado": True,
    "edicion": "solo linea ONTO_LLM_MODEL en C:/Users/marti/Documents/MEX-Ontologi/.env",
    "respaldo_env_original": "C:/Users/marti/Documents/MEX-Ontologi/.env.antes-r4-chat (gemini-3.5-flash; NO sobrescrito)",
    "verificacion_sonda": "gemini-3.1-flash-lite: HTTP 200 respuesta 'ok'",
    "verificacion_corpus": "corpus 6: 3 probado (C1 totales 865/3283/12, C3 F2 con limites, C4 definicion exacta con URI), 2 falla_oraculo con respuesta real (C2 brecha F2, C5 omite 2022/candidatas), C6 429 TPM (reintento 8.5s, detenido). Manejo de contexto demostrado",
    "ensayo_gemma4": "archivado en ensayo-gemma4/ (sonda 200; corpus: C1 503, C2 429 TPM, resto pendiente_cuota; 0 utilizables). Sin mas pruebas a Gemma4 ni a gemini-3.5-flash",
    "mecanismo_recarga": "sidecar fija el modelo al arrancar; chat real lo toma tras reinicio de Studio (8137, integrador): NO reiniciado; ver reinicio-requerido.json",
    "intento_previo": "gemini-2.5-flash y gemini-2.5-flash-lite: 404 en gateway",
    "harness": ["listar_modelos.py", "sonda_modelo.py"],
}
entrega["conteos"] = {
    "casos_totales": 6,
    "corrida_final_modelo": "gemini-3.1-flash-lite",
    "chat_probado": 3,
    "falla_oraculo": 2,
    "bloqueado_cuota_tpm": 1,
    "detalle": "C1,C3,C4 probado; C2,C5 falla_oraculo con respuesta real; C6 429 TPM detenido",
    "corrida_gemma4": "archivada en ensayo-gemma4/ (0 utilizables)",
    "corrida_gemini_3_5": "archivada en antes-cambio-modelo/ (C2 falla-oraculo, C3 probado)",
    "grafo_sin_cambios_todos": True,
    "cambio_modelo_aplicado": True,
    "capas": "sidecar/API por modulos reutilizados (no E2E, no binario completo, no UI); studio-ui leida no enviada",
}

decisiones = []
for c in ev["casos"]:
    motivo = c.get("causa") or (
        "oraculo: faltan=%s alguno_ok=%s prohibidos=%s"
        % (c["evaluacion"].get("faltan"), c["evaluacion"].get("algunoOk"),
           c["evaluacion"].get("prohibidos"))
        if c.get("evaluacion") and c.get("respuesta") else
        (c.get("evaluacion", {}) or {}).get("nota", "sin evaluacion")
    )
    decisiones.append({
        "id": c["id"], "pregunta": c["pregunta"], "modelo": ev["modelo"],
        "canal": c.get("canal"), "estado": c["chat"],
        "motivo": (motivo[:500] + " [...]") if len(motivo) > 500 else motivo,
        "triples_antes": c.get("triples_antes"), "triples_despues": c.get("triples_despues"),
        "evidencia": ["propuestas/pendientes-muse-r4/chat/evaluacion.json",
                      "propuestas/pendientes-muse-r4/chat/respuestas-saneadas.json"],
    })
entrega["decisiones_chat"] = decisiones
(MINE / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

sha = hashlib.sha256((MINE / "entrega.json").read_bytes()).hexdigest()
(MINE / "listo.json").write_text(json.dumps(
    {"entrega": "entrega.json", "sha256": sha,
     "conteos": entrega["conteos"], "estado": "fase_final_completa"},
    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(sha)
