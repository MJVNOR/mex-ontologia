import hashlib, json, pathlib
BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\propuestas\ronda-3\agente-1-chat")

def info(rel):
    b = (BASE / rel).read_bytes()
    return {"ruta": rel, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

propuesta = {
  "archivos_modificados_upstream": [
    "studio/src-tauri/sidecars/agent/graphrag.ts",
    "studio/src-tauri/sidecars/agent/index.ts",
  ],
  "base_original": {
    "graphrag_ts_sha256": "ae43065f04a7ea16aa8409bef3475da0f7ca24b4a607e03de658130d772e0",
    "graphrag_ts_bytes": 23598,
    "index_ts_sha256": "5464143f124ce93726e6e113e34d481abbbdd5e7d9f5871e",
    "index_ts_bytes": 13315,
    "instalado_dist_index_js_sha256": "PENDIENTE_DESDE_HUELLAS",
    "instalado_dist_index_js_bytes": 0,
    "nota": "Fuente sin cambios desde ronda 2; bundle instalado identico al de ronda 2. Rebuild local no reproduce el bundle: identidad byte a byte no demostrable con el toolchain actual.",
  },
  "cambios_graphrag_ts": {
    "correspondenceStatusOverview": "GROUP BY nativo con COUNT(DISTINCT ?mapping) sobre estadoCorrespondencia; predicado por sufijo; texto COMPLETE con total.",
    "resourceCorrespondenceContext_v2": "Resuelve recursos REALES RecursoCatalogado por titulo (palabras identificadoras con variantes singular/plural) y anio por periodo declarado inicioDeclarado/finDeclarado (etiqueta solo como respaldo). Columnas via recurso->esquema->columna; conteos COUNT(DISTINCT ?mapping) por recurso con desglose; ejemplos paginados completos, revisados primero. AND, luego OR multi-recurso; si nada resuelve devuelve UNRESOLVED con candidatos y SIN conteos ni cero. COMPLETE solo para IRIs resueltos con paginas completas; PARTIAL si falta vocabulario o columnas.",
    "variableStatusOverview": "GROUP BY nativo sobre estadoSemantico, separado del tallaje de correspondencias.",
    "intentos": "wantsCorrespondenceOverview/wantsResourceScope/wantsVariableOverview + resourceKeywords/questionYears/keywordVariants deterministicos; sin modelo.",
    "retrieve": "Los tres contextos se consultan en paralelo al anclaje; preguntas sin variable nombrada o sin anclas ya devuelven conteos COMPLETE.",
    "asContext_y_prompt": "Secciones GLOBAL/RESOURCE/VARIABLE con alcance; prompt: conteos globales solo del overview, recurso resuelto a IRIs con desglose, separar estadoSemantico de estadoCorrespondencia, no generalizar recurso/anio.",
  },
  "cambios_index_ts": {
    "guardia_sin_anclas": "La rama de respuesta vacia exige ademas ausencia de los tres contextos (1 linea). Sin cambios de arquitectura ni proveedores.",
  },
  "conteos_base_motor_vivo_2026_10_23": {
    "conceptos": 103,
    "variables_respaldadas": 232,
    "variables_candidatas": 23,
    "variables_fuera_nucleo": 11,
    "documental_revisada": 836,
    "candidata_por_nombre": 118,
    "ambigua_por_nombre": 6,
    "total_correspondencias": 960,
    "matrimonios_2022_columnas_via_esquema": 9,
    "matrimonios_2022_mapeos_revisados": 4,
  },
  "entregables": {
    "parche_aplicable": [info("parche/graphrag.ts.patch"), info("parche/index.ts.patch")],
    "parche_archivos_completos": [info("parche/graphrag.ts"), info("parche/index.ts")],
    "pruebas_offline": [info("trabajo/recuperacion-r3.test.ts")],
    "prueba_e2e_real": [info("trabajo/recuperacion-e2e.test.ts")],
    "evidencia": [info("evidencia/e2e_recuperacion.json"), info("evidencia/evaluacion_C05_C06.json"),
                  info("evidencia/verificacion-live.log"), info("evidencia/verificacion.log"),
                  info("evidencia/resumen_base.json")],
    "verificadores": ["scripts/verificar_entrega.py", "scripts/evaluar_C05_C06.py",
                      "scripts/verificar_base2.py", "scripts/generar_parche.py",
                      "scripts/registrar_huellas.py", "scripts/build_identidad.py"],
  },
  "verificacion": {
    "offline": "25 pruebas (24 pasan + 1 e2e omitida sin live) + tsc --strict limpio",
    "live": "e2e con retrieve()/asContext() reales sobre HTTP 8137: C06 6/118/836 total 960; C05 Matrimonios 2022 resuelto a IRI con 4 revisadas (incluye mapping c92aecbb...); parafrasis natural y singular resuelven sin UNRESOLVED ni falso cero; 0 peticiones a modelos",
  },
  "instalacion": {
    "pasos": ["Respaldar dist/index.js instalado y graphrag.ts/index.ts del repo.",
              "Aplicar parche/graphrag.ts.patch e index.ts.patch en studio/src-tauri/sidecars/agent/.",
              "Recompilar con npm run build, comparar y registrar SHA del bundle.",
              "Reiniciar Studio; comprobar C05/C06 y conteos globales.",
              "Si algo falla, aplicar reversion."],
    "reversion": ["Restaurar respaldos, recompilar, reinstalar bundle anterior, reiniciar Studio."],
  },
  "limites": [
    "UI de Studio no probada; APIs/fuente no equivalen a UI.",
    "0 peticiones a modelos: la recuperacion es determinista y la cuota fallo en ronda 2.",
    "COMPLETE de recurso solo para IRIs resueltos con paginas completas; heuristica incompleta rinde UNRESOLVED/PARTIAL sin ceros.",
    "Conteos 836/118/6 son verdades del grafo vivo a 2026-10-23; 162/792 historico.",
    "Rebuild local no reproduce el bundle instalado.",
    "Sin node_modules ni secretos copiados; sin consolidar/ampliar/sincronizar; sin despliegue.",
  ],
  "pendientes_para_integrador": [
    "Revisar y aplicar parche; recompilar e instalar segun plan; comprobar C05/C06 en Studio; decidir si las pruebas entran al repo upstream.",
  ],
}
# sha del instalado desde el registro de huellas (fuente verificada)
_huellas = json.loads((BASE / "fuente" / "huellas.json").read_text(encoding="utf-8"))
propuesta["base_original"]["instalado_dist_index_js_sha256"] = _huellas["_instalado"]["sha256"]
propuesta["base_original"]["instalado_dist_index_js_bytes"] = _huellas["_instalado"]["bytes"]
(BASE / "propuestas.json").write_text(json.dumps(propuesta, indent=2, ensure_ascii=False), encoding="utf-8")
print("propuestas.json OK", propuesta["base_original"]["instalado_dist_index_js_sha256"])
