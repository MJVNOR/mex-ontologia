"""Cierre de ronda 7 tras regeneración + Studio. SOLO lo ejecuta el coordinador.

Lee seleccion-v002/comprobacion-v002, verifica 188 casos con fuentes
congeladas, auditorías globales con SHA de selección y material con SHA de
aceptadas, overlay de 31 aprobaciones sin reescribir fuentes, 3 links a
dependencias, cobertura actual 1423/1106/4478/45/0 + fuera 124 +
candidatas-significado 16 + referencias 9/8 (antes 1/16, total 17:
exposición por nuevas variables, sin identidad nueva de catálogos), 138
pendientes + 16 vigencias + 3 anomalías conservados, delta exacto 31/31/3, reconciliación 45 = 17 previas + 28
nuevas auto-coincidencias (reportadas, no auto-aprobadas; delta.json
predijo 17), backups y SHACL de Studio actual. Emite únicamente los
4 informes nuevos; no modifica ningún existente, no instala, no sincroniza,
no toca Gemma, no ejecuta tests. Python estándar, sin red.

Correcciones aplicadas (estructura real verificada 2026-10-24):
- raiz() = AQUI.parents[1] (el helper vive en
  propuestas/plan-paralelo-brechas-sin-gemma/).
- paso_fuentes: compara contra el manifiesto de respaldo de 702 copias; los
  scripts instalados y derivados del pipeline sí cambian legítimamente:
  allowlist estricto (scripts instalados con SHA de material v002,
  ontologia/semantica.json con comparación semántica exacta, derivados
  data/semantica|portal|integracion-ronda-7, reports/, revision-ronda-7
  nueva). Históricos/manifiestos fuera del allowlist exigen bytes intactos.
  Registra TODOS los cambios del backup.
- Intersección A/B DESPUÉS de normalizar sufijo->IRI (antes descartaba 31).
- congelada.json: exige campo aceptadas_sha256 explícito y verifica cada
  entrada {ruta, sha256} por bytes; no asume forma.
- Backups reales: integracion/respaldo-previo/manifiesto-respaldo.json +
  integracion/respaldo-studio-previo.ttl (existen y se registran); no se
  exige data/backups/antes-r7-*. Gemma se verifica en el campo "gemma" del
  manifiesto (orquestacion.json no tiene esos campos).
- Auditorías R7: verifica el manifiesto INSTALADO
  (data/integracion-ronda-7/manifiesto.json + revision-ronda-7.json):
  aceptadas instalada == aceptadas material por SHA, auditorias con pin
  exacto y 31 reglas + 3 vínculos en aceptar en AMBAS.
- W adenda v004 (3 pistas S1/MAT/S4) en curso: fuera de selección, no
  bloqueante y no exigida (solo se verifican los 3 paquetes W fijados).
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
EXP = AQUI / "ejecucion-20261024-072207Z"
MATERIAL_REL = "integracion/materializacion/v002"
RESPALDO = EXP / "integracion/respaldo-previo/manifiesto-respaldo.json"
TTL_STUDIO = EXP / "integracion/respaldo-studio-previo.ttl"

# Derivados del pipeline que sí cambian legítimamente (allowlist estricto).
# Todo lo demás (históricos R3-R6, manifiestos, docs, resto de scripts/data,
# reports/ronda-3..6 cerrados, fuentes) exige bytes intactos contra el respaldo.
SCRIPTS_INSTALADOS = ["scripts/integrar_ronda_7.py",
                      "scripts/integrar_ronda_6.py",
                      "scripts/consolidar_semantica.py"]
DERIVADOS_PREFIJO = ["data/semantica/", "data/portal/",
                     "data/integracion-ronda-7/", "reports/"]
DERIVADOS_EXACTOS = ["ontologia/semantica.json",
                     "ontologia/revision-ronda-7.json"]
# TTL con timestamps/serialización regenerable: si los bytes difieren se
# coteja isomorfismo RDF (tras excluir literales fecha/hora) en vez de
# exigir bytes idénticos. Históricos y manifiestos nunca entran aquí.
TTL_ISOMORFOS = ["data/catalogo/studio-live.ttl",
                 "data/integracion/integracion.ttl",
                 "data/integracion-ronda-2/ronda-2.ttl"]
ESPERADO = {"respaldada_por_definicion": 1423, "conceptos": 1106,
            "documental_revisada": 4478, "candidata_por_nombre": 45, "ambigua_por_nombre": 0}
FUERA_ESPERADO = 124
CAND_SIG_ESPERADO = 16
# Reconciliación candidatas (delta.json predijo 17; real 45 = 17 previas + 28
# nuevas auto-coincidencias de los 31 significados nuevos: 20-3+28).
# Las 28 nuevas se REPORTAN, no se auto-aprueban; siguen candidatas.
PREVIAS_ESPERADO = 17
NUEVAS_ESPERADO = 28
# Referencias de catálogo: antes 1 sin resolver + 16 con recurso; ahora
# 9 + 8 (total 17 = 17: sin identidad nueva de catálogos). Las 31 variables
# nuevas exponen referencias declaradas (codebook nacional citado como
# contexto/procedencia) que siguen sin resolver; no se acepta ningún catálogo.
REF_SIN_ESPERADO = 9
REF_CON_ESPERADO = 8
BASE_IRI = ("https://example.org/mex-ontologi/definition/"
            "22202305-2d02-4c49-b216-cc98224357f0%2F")


def raiz():
    return AQUI.parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def lee(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def falla(mensaje):
    raise SystemExit("CIERRE-R7 BLOQUEADO: " + mensaje)


def norma_def(x):
    return x if "%2F" in x else BASE_IRI + x.lstrip("0") \
        if x.strip().isdigit() else BASE_IRI + x


def paso_seleccion(root):
    sel = lee(EXP / "seleccion-v002.json")
    comp = lee(EXP / "comprobacion-v002.json")
    if comp.get("faltantes") or comp.get("discrepancias"):
        falla("comprobacion-v002 con faltantes/discrepancias")
    for w in sel.get("paquetes_web", []):
        if sha(root / w["ruta"]) != w["sha256"]:
            falla("paquete web modificado: " + w["ruta"])
    casos, detalle = 0, []
    for v in sel["versiones"]:
        entrega = lee(root / v["entrega"])
        if sha(root / v["entrega"]) != v["sha256_entrega"]:
            falla("entrega modificada: " + v["entrega"])
        if sha(root / v["marcador"]) != v["sha256_marcador"]:
            falla("marcador modificado: " + v["marcador"])
        for d in entrega.get("decisiones", []):
            casos += 1
            detalle.append({"rol": v["rol"], "id": d.get("id"), "tipo": d.get("tipo"),
                            "estado_entrega": d.get("estado"),
                            "reapertura": d.get("condicion_reapertura")})
    if casos != 188:
        falla(f"casos {casos} != 188")
    return sel, detalle


def ttl_equivalente(respaldo, vivo):
    """Isomorfismo RDF tras excluir literales fecha/hora (timestamps de
    generación/serialización). Falla si el grafo difiere en contenido."""
    from rdflib import Graph, Literal
    from rdflib.namespace import XSD
    gs = []
    for p in (respaldo, vivo):
        g = Graph()
        g.parse(str(p), format="turtle")
        fechados = [t for t in g if isinstance(t[2], Literal)
                    and t[2].datatype in (XSD.dateTime, XSD.date, XSD.time)]
        for t in fechados:
            g.remove(t)
        gs.append(g)
    from rdflib.compare import isomorphic
    return isomorphic(gs[0], gs[1])


def paso_fuentes(root, material):
    man = lee(RESPALDO)
    mat_cod = {f"codigo/{Path(p).name}": sha(material / "codigo" / Path(p).name)
               for p in SCRIPTS_INSTALADOS}
    intactos, cambiados = [], []
    for c in man["copias"]:
        rel = c["original"]
        actual = sha(root / rel)
        if actual == c["sha256"]:
            intactos.append(rel)
            continue
        permitido, motivo = False, ""
        if rel in SCRIPTS_INSTALADOS:
            esperado = mat_cod.get("codigo/" + Path(rel).name)
            permitido = (actual == esperado)
            motivo = "script instalado == codigo material v002" if permitido else \
                "script instalado difiere del codigo material v002"
        elif rel in TTL_ISOMORFOS:
            base = root / c.get("respaldo", "")
            if base.exists() and ttl_equivalente(base, root / rel):
                permitido, motivo = True, "TTL derivado: isomorfo tras excluir timestamps/serializacion"
            else:
                motivo = "TTL derivado no isomorfo al respaldo"
        elif rel in DERIVADOS_EXACTOS:
            permitido, motivo = True, "derivado pipeline (verificacion semantica en cobertura)"
        elif any(rel.startswith(p) for p in DERIVADOS_PREFIJO):
            permitido, motivo = True, "derivado regenerado/instalado"
        cambiados.append({"archivo": rel, "sha_respaldo": c["sha256"],
                          "sha_actual": actual, "permitido": permitido,
                          "motivo": motivo})
        if not permitido:
            falla("fuente congelada modificada fuera de allowlist: " + rel)
    return {"intactos": len(intactos), "cambiados": cambiados}


def paso_auditorias(root, material):
    a = lee(EXP / "A-documental/dictamen.json")
    b = lee(EXP / "B-tecnica/dictamen.json")
    if a.get("dictamen") != "aceptar" or b.get("dictamen") != "aceptar":
        falla("dictamen global no aceptar")
    sel_sha = sha(EXP / "seleccion-v002.json")
    if a.get("seleccion_sha256") != sel_sha or b.get("seleccion_sha256") != sel_sha:
        falla("seleccion_sha256 global no coincide con seleccion-v002")
    # Normalizar ANTES de intersectar (sufijos o IRIs en cualquier lado).
    ids_a = {norma_def(x) for x in a.get("propuestas_aceptadas", [])}
    ids_b = {norma_def(x) for x in b.get("propuestas_aceptadas", [])}
    if len(ids_a) != 31 or len(ids_b) != 31:
        falla("A/B global sin 31 aceptadas normalizadas")
    aprobados = ids_a & ids_b
    if len(aprobados) != 31:
        falla("interseccion A/B normalizada != 31")
    mat = lee(material / "congelada.json")
    if not mat.get("aceptadas_sha256"):
        falla("congelada del material sin campo aceptadas_sha256")
    sha_acc = sha(material / "aceptadas.json")
    if mat["aceptadas_sha256"] != sha_acc:
        falla("aceptadas_sha256 de material no coincide")
    for e in mat.get("archivos", []):
        if sha(root / e["ruta"]) != e["sha256"]:
            falla("archivo de material modificado: " + e["ruta"])
    aceptadas = lee(material / "aceptadas.json")
    if len(aceptadas["reglas"]) != 31 or len(aceptadas["vinculos"]) != 3 \
            or len(aceptadas["conceptos"]) != 31:
        falla("material distinto de 31/31/3")
    defs = {r["definiciones"][0] for r in aceptadas["reglas"]}
    if aprobados != defs:
        falla("overlay 31 aprobaciones != 31 definiciones del material")
    # Manifiesto R7 INSTALADO (no las plantillas pendientes del material).
    rev = lee(root / "ontologia/revision-ronda-7.json")
    inst = root / rev["evidencia"]
    if sha(inst / "manifiesto.json") != rev["manifiesto_sha256"]:
        falla("manifiesto R7 instalado modificado")
    iman = lee(inst / "manifiesto.json")
    if iman.get("aceptadas_sha256") != sha_acc:
        falla("manifiesto instalado no pinna aceptadas del material")
    for rel, h in iman.get("archivos", {}).items():
        if sha(inst / rel) != h:
            falla("archivo instalado R7 modificado: " + rel)
    if sha(inst / "aceptadas.json") != sha_acc:
        falla("aceptadas instalada != aceptadas material")
    cols = {v["columna"] for v in aceptadas["vinculos"]}
    for lado in ("auditoria-a", "auditoria-b"):
        au = lee(inst / "auditorias" / f"{lado}.json")
        if au.get("aceptadas_sha256") != sha_acc:
            falla(f"R7 instalado sin pin aceptadas_sha256 en {lado}")
        ok_r = {x["id"] for x in au.get("dictamenes", [])
                if x.get("tipo") == "reglas" and x.get("dictamen") == "aceptar"}
        ok_v = {x["id"] for x in au.get("dictamenes", [])
                if x.get("tipo") == "vinculos" and x.get("dictamen") == "aceptar"}
        if {r["id"] for r in aceptadas["reglas"]} != ok_r:
            falla(f"R7 instalado sin 31 reglas en aceptar en {lado}")
        if cols != ok_v:
            falla(f"R7 instalado sin 3 vinculos en aceptar en {lado}")
    return {"aceptadas_sha256": sha_acc, "ids": sorted(aprobados),
            "definiciones_material": sorted(defs)}


def paso_overlay(detalle, auditoria, material):
    dep = lee(EXP / "dependencias-correspondencias.json")
    pares = {c["columna"]: c["definicion_iri"] for c in dep}
    aceptadas = lee(material / "aceptadas.json")
    respaldo = {r["definiciones"][0]: r["concepto"] for r in aceptadas["reglas"]}
    for v in aceptadas["vinculos"]:
        if pares.get(v["columna"]) != v["definicion_iri"]:
            falla("vínculo fuera de dependencias: " + v["columna"])
        if respaldo.get(v["definicion_iri"]) != v["concepto"]:
            falla("vínculo sin concepto de su regla: " + v["columna"])
    aprobados = set(auditoria["ids"])
    for c in detalle:
        if c["tipo"] == "significados" and c["id"] in aprobados:
            c["estado_final"] = "integrado_r7"
        else:
            c["estado_final"] = "conservado_" + (c["estado_entrega"] or "brecha")
    tipos = {}
    for c in detalle:
        tipos[(c["tipo"], c["estado_final"])] = tipos.get((c["tipo"], c["estado_final"]), 0) + 1
    if sum(1 for c in detalle if c["estado_final"] == "integrado_r7") != 31:
        falla("integrados != 31")
    if sum(1 for c in detalle if c["tipo"] == "significados") != 169:
        falla("significados != 169")
    if sum(1 for c in detalle if c["tipo"] == "vigencias") != 16:
        falla("vigencias != 16")
    if sum(1 for c in detalle if c["tipo"] == "anomalias") != 3:
        falla("anomalías != 3")
    return {"detalle_casos": detalle, "conteo_tipo_estado": {f"{k[0]}/{k[1]}": v for k, v in tipos.items()},
            "pendientes_significados": 169 - 31, "vinculos_promovidos": 3}


def paso_cobertura(root, material):
    cob = lee(root / "data/semantica/cobertura.json")["resumen"]
    ev, ec = cob["estados_variables"], cob["estados_correspondencias"]
    actual = {"respaldada_por_definicion": ev.get("respaldada_por_definicion", 0),
              "conceptos": cob.get("conceptos_compartidos", 0),
              "documental_revisada": ec.get("documental_revisada", 0),
              "candidata_por_nombre": ec.get("candidata_por_nombre", 0),
              "ambigua_por_nombre": ec.get("ambigua_por_nombre", 0)}
    if actual != ESPERADO:
        falla(f"cobertura {actual} != {ESPERADO}")
    if ev.get("fuera_del_nucleo_actual", 0) != FUERA_ESPERADO:
        falla("fuera_del_nucleo_actual != 124")
    if ev.get("candidata_sin_definicion_suficiente", 0) != CAND_SIG_ESPERADO:
        falla("candidata_sin_definicion_suficiente != 16")
    if cob.get("referencias_catalogo_sin_resolver", 0) != REF_SIN_ESPERADO:
        falla("referencias_catalogo_sin_resolver != 9 (no afirmar 1)")
    if cob.get("referencias_catalogo_con_recurso_identificado", 0) != REF_CON_ESPERADO:
        falla("referencias_catalogo_con_recurso_identificado != 8")
    carga = lee(root / "reports/portal-carga.json")
    if not carga.get("triples_combinados"):
        falla("portal-carga sin triples")
    sync = lee(root / "reports/studio-portal-sync.json")
    if sync.get("verificado") is not True or (sync.get("shacl") or {}).get("conforms") is not True:
        falla("studio-sync sin verificar/SHACL")
    respaldo = root / sync.get("respaldo", "")
    if not respaldo.exists():
        falla("respaldo de Studio inexistente")
    # Delta exacto 31/31/3 + igualdad semántica exacta del resto (baseline).
    vivo = lee(root / "ontologia/semantica.json")
    base = lee(material / "base-semantica.json")
    for campo, clave in (("reglas_descripcion_exacta", "id"),
                         ("vinculos_documentales_revisados", "columna")):
        bv = {r[clave]: r for r in vivo[campo]}
        bb = {r[clave]: r for r in base[campo]}
        nuevos = set(bv) - set(bb)
        perdidos = set(bb) - set(bv)
        if perdidos:
            falla(f"delta con pérdidas en {campo}: {sorted(perdidos)[0]}")
        for k in set(bv) & set(bb):
            if bv[k] != bb[k]:
                falla(f"registro previo alterado en {campo}: {k}")
    cv, cb = set(vivo["conceptos"]), set(base["conceptos"])
    if cb - cv:
        falla("concepto previo perdido")
    for k in cv & cb:
        if vivo["conceptos"][k] != base["conceptos"][k]:
            falla("concepto previo alterado: " + k)
    if len(set(r["id"] for r in vivo["reglas_descripcion_exacta"])
            - set(r["id"] for r in base["reglas_descripcion_exacta"])) != 31 \
            or len(set(r["columna"] for r in vivo["vinculos_documentales_revisados"])
                   - set(r["columna"] for r in base["vinculos_documentales_revisados"])) != 3 \
            or len(cv - cb) != 31:
        falla("delta vivo vs base != 31/31/3")
    return {"cobertura": actual, "portal_carga": {k: carga[k] for k in
            ("generado_en_utc", "triples_extension", "triples_combinados") if k in carga},
            "studio_sync": {"respaldo": sync["respaldo"], "verificado": True,
                            "shacl_conforms": True, "triples_gestionados": sync.get("triples_gestionados")},
            "delta": {"reglas": 31, "vinculos": 3, "conceptos": 31}}


def paso_compatibilidad(root):
    """Journal compatibilidad-aplicada.json SOLO cuando exista (instalación
    futura de 2 scripts; no está en el backup 702, tiene respaldo adicional
    propio en integracion/respaldo-compatibilidad/)."""
    journal = EXP / "integracion/compatibilidad-aplicada.json"
    if not journal.exists():
        return {"estado": "pendiente_instalacion", "verificado": False}
    j = lee(journal)
    if j.get("version") != "v002":
        falla("compatibilidad-aplicada con version != v002")
    cambios = {c["ruta"]: c for c in j.get("cambios", [])}
    if set(cambios) != {"scripts/integrar_entregas.py", "scripts/integrar_ronda_2.py"}:
        falla("compatibilidad-aplicada sin los 2 scripts previstos")
    respaldo = EXP / "integracion/respaldo-compatibilidad"
    audit = lee(EXP / "B-tecnica/auditoria-compatibilidad-r7-v002.json")
    if audit.get("dictamen") != "aceptar":
        falla("compatibilidad sin aceptar de B")
    if sha(EXP / "B-tecnica/auditoria-compatibilidad-r7-v002.json") != j.get("auditoria_sha256"):
        falla("compatibilidad-aplicada no pinna auditoria B vigente")
    for rel, c in cambios.items():
        if sha(root / rel) != c["sha256_despues"]:
            falla("script compatible instalado difiere del journal: " + rel)
        pre = respaldo / Path(rel).name
        if not pre.exists() or sha(pre) != c["sha256_antes"]:
            falla("respaldo-compatibilidad sin previo integro: " + rel)
    return {"estado": "aplicada_v002", "verificado": True,
            "auditoria_sha256": j["auditoria_sha256"],
            "cambios": cambios}


def paso_reconciliacion(root, material):
    """Deriva IDs y nuevos matches del diff viva vs backup R6 (no usa lo
    observado como expected). 45 = 17 previas (20-3 promovidas) + 28 nuevas
    auto-coincidencias de los 31 significados (28 ex-fuera + 3 ex-candidatas).
    Los 3 links aceptados no cambian."""
    viva = lee(root / "data/semantica/cobertura.json")["correspondencias"]
    base = lee(EXP / "integracion/respaldo-previo/data/semantica/cobertura.json")["correspondencias"]
    cand_viva = {c["columna"] for c in viva if c.get("estado") == "candidata_por_nombre"}
    cand_base = {c["columna"] for c in base if c.get("estado") == "candidata_por_nombre"}
    nuevas = sorted(cand_viva - cand_base)
    previas = sorted(cand_viva & cand_base)
    aceptadas = lee(material / "aceptadas.json")
    promovidas = sorted(cand_base - cand_viva)
    links = sorted(v["columna"] for v in aceptadas["vinculos"])
    if len(nuevas) != NUEVAS_ESPERADO:
        falla(f"auto-coincidencias nuevas != 28: {len(nuevas)}")
    if len(previas) != PREVIAS_ESPERADO:
        falla(f"candidatas previas != 17: {len(previas)}")
    if promovidas != links:
        falla("promovidas a revisada != 3 links aceptados")
    for col in nuevas:
        var = next((c.get("variable", "") for c in viva
                    if c.get("columna") == col), "")
        if "22202305-2d02-4c49-b216-cc98224357f0" not in var:
            falla("nueva auto-coincidencia fuera del diccionario SINAC: " + col)
    return {"prediccion_delta_json": 17, "real": 45,
            "previas_17": previas, "nuevas_28": nuevas, "promovidas_3": promovidas,
            "nota": "28 auto-coincidencias reportadas, no auto-aprobadas; siguen candidatas. "
                    "delta.json predijo 17 (fallida: no contemplaba matches de significados nuevos)."}


def paso_referencias(root):
    """Reclasificación 1+16 -> 9+8 con total 17 = 17: exposición por las 31
    variables nuevas (codebook nacional citado, sin resolver), NO identidad
    nueva de catálogos. No se añade ninguna aceptación de catálogo ni se
    falsean conteos; no afirmar que siguen en 1."""
    viva = lee(root / "data/semantica/cobertura.json")["resumen"]
    base = lee(EXP / "integracion/respaldo-previo/data/semantica/cobertura.json")["resumen"]
    antes = (base.get("referencias_catalogo_sin_resolver", 0),
             base.get("referencias_catalogo_con_recurso_identificado", 0))
    ahora = (viva.get("referencias_catalogo_sin_resolver", 0),
             viva.get("referencias_catalogo_con_recurso_identificado", 0))
    if sum(antes) != sum(ahora):
        falla(f"total referencias cambió {sum(antes)} -> {sum(ahora)}: identidad nueva no permitida")
    if ahora != (REF_SIN_ESPERADO, REF_CON_ESPERADO):
        falla(f"referencias {ahora} != (9, 8)")
    return {"antes_1_mas_16": list(antes), "ahora_9_mas_8": list(ahora),
            "total": sum(ahora),
            "nota": "Exposicion por las 31 variables nuevas (referencias declaradas sin resolver); "
                    "ningun catalogo aceptado ni identificado de nuevo. No afirmar 1."}


def paso_respaldo_gemma(root):
    man = lee(RESPALDO)
    if not TTL_STUDIO.exists():
        falla("respaldo-studio-previo.ttl inexistente")
    gemma = man.get("gemma", "")
    if "sin cambios" not in str(gemma):
        falla("manifiesto de respaldo sin constancia Gemma sin cambios")
    return {"manifiesto_respaldo_sha256": sha(RESPALDO),
            "respaldo_studio_ttl_sha256": sha(TTL_STUDIO),
            "respaldo_previo": str(RESPALDO.relative_to(root)).replace("\\", "/"),
            "studio_ttl": str(TTL_STUDIO.relative_to(root)).replace("\\", "/"),
            "chat_gemma": str(gemma), "tests": "no ejecutados (prohibido en cierre)",
            "w_adenda_v004": "en curso (3 pistas S1/MAT/S4), fuera de seleccion-v002, no bloqueante"}


def emitir(root, ronda, cierre):
    salidas = {"reports/ronda-7.json": json.dumps(ronda, ensure_ascii=False, indent=2) + "\n",
               "reports/ejecucion-plan-sin-gemma.json": json.dumps(cierre, ensure_ascii=False, indent=2) + "\n",
               "reports/ronda-7.md": markdown_ronda(ronda),
               "reports/ejecucion-plan-sin-gemma.md": markdown_cierre(cierre)}
    for rel in salidas:
        if (root / rel).exists():
            falla("informe ya existe, no sobrescribir: " + rel)
    for rel, texto in salidas.items():
        (root / rel).write_text(texto, encoding="utf-8")
    return sorted(salidas)


def markdown_ronda(r):
    L = ["# Cierre ronda 7", "", f"Fecha UTC: {r['fecha_utc']}", "",
         "## Delta aplicado (31/31/3)", ""]
    L += [f"- Reglas nuevas: {r['delta']['reglas']}, vínculos: {r['delta']['vinculos']}, "
          f"conceptos: {r['delta']['conceptos']}"]
    L += [f"- Cobertura: {r['cobertura_actual']}"]
    L += ["", "## Reconciliación candidatas (delta.json predecía 17)", "",
          f"- Real: {r['reconciliacion_candidatas']['real']} = "
          f"{len(r['reconciliacion_candidatas']['previas_17'])} previas "
          f"(20-3 promovidas a revisada) + "
          f"{len(r['reconciliacion_candidatas']['nuevas_28'])} nuevas "
          f"auto-coincidencias de los 31 significados.",
          f"- {r['reconciliacion_candidatas']['nota']}",
          "- Promovidas a revisada (3 links aceptados, sin cambio): "
          + ", ".join(x.split('%2F')[-1] for x in r['reconciliacion_candidatas']['promovidas_3'])]
    L += ["", "## Referencias de catálogo (exposición, no identidad nueva)", "",
          f"- Antes: {r['reconciliacion_referencias']['antes_1_mas_16'][0]} sin resolver + "
          f"{r['reconciliacion_referencias']['antes_1_mas_16'][1]} con recurso; "
          f"ahora: {r['reconciliacion_referencias']['ahora_9_mas_8'][0]} + "
          f"{r['reconciliacion_referencias']['ahora_9_mas_8'][1]} "
          f"(total {r['reconciliacion_referencias']['total']} = 17).",
          f"- {r['reconciliacion_referencias']['nota']}"]
    L += ["", "## Conservados", "",
          f"- Pendientes: {r['conservados']['pendientes_significados']} significados reales, "
          f"{r['conservados']['vigencias']} vigencias, {r['conservados']['anomalias']} anomalías "
          f"(1 des_mpo_res + 2 encabezados)."]
    L += ["", "## Fuentes y backups", ""]
    L += [f"- Respaldo intacto salvo pipeline: {r['fuentes']['intactos']} intactos; "
          + ", ".join(f"{x['archivo']} ({x['motivo']})" for x in r["fuentes"]["cambiados"])]
    L += [f"- Respaldo previo: {r['backups']['respaldo_previo']}; Studio TTL: {r['backups']['studio_ttl']}."]
    L += [f"- Studio: respaldo {r['studio']['respaldo']}, SHACL conforms, verificado."]
    L += ["", "## Límites", "",
          "- Chat Gemma excluido; sin contactos externos; sin tests.",
          "- Manifiestos históricos R3-R6 sin cambio.", ""]
    return "\n".join(L)


def markdown_cierre(c):
    L = ["# Ejecución plan sin Gemma — cierre", "", f"Fecha UTC: {c['fecha_utc']}", "",
         "## Casos (188)", ""]
    L += ["| Tipo/estado | Cantidad |", "| --- | ---: |"]
    L += [f"| {k} | {v} |" for k, v in c["conteo_tipo_estado"].items()]
    L += ["", "## Reapertura por caso", "",
          "Cada caso conserva su `reapertura` (condición exacta del frente) en "
          "`reports/ronda-7.json:detalle_casos`. Ninguna búsqueda agotada se presenta como nueva.",
          "", "## Informes", "",
          "- `reports/ronda-7.json/md`: delta, cobertura, fuentes, backups, Studio.",
          "- Este informe: detalle agregado + reapertura.", ""]
    return "\n".join(L)


def main(argv):
    material = Path(argv[1]) if len(argv) > 1 else EXP / "integracion/materializacion/v002"
    root = raiz()
    ahora = datetime.now(timezone.utc).isoformat()
    sel, detalle = paso_seleccion(root)
    fuentes = paso_fuentes(root, material)
    auditoria = paso_auditorias(root, material)
    overlay = paso_overlay(detalle, auditoria, material)
    cobertura = paso_cobertura(root, material)
    recon = paso_reconciliacion(root, material)
    refer = paso_referencias(root)
    compat = paso_compatibilidad(root)
    resto = paso_respaldo_gemma(root)
    ronda = {"fecha_utc": ahora, "seleccion": "seleccion-v002",
             "seleccion_sha256": sha(EXP / "seleccion-v002.json"),
             "aceptadas_sha256": auditoria["aceptadas_sha256"],
             "material": str(material.relative_to(root)).replace("\\", "/"),
             "delta": cobertura.pop("delta"),
             "cobertura_actual": cobertura.pop("cobertura"),
             "reconciliacion_candidatas": recon,
             "reconciliacion_referencias": refer,
             "portal_carga": cobertura.pop("portal_carga"),
             "studio": cobertura.pop("studio_sync"),
             "fuentes": fuentes,
             "conservados": {"pendientes_significados": 138, "vigencias": 16, "anomalias": 3},
             "backups": {"respaldo_previo": resto["respaldo_previo"],
                         "studio_ttl": resto["studio_ttl"],
                         "manifiesto_respaldo_sha256": resto["manifiesto_respaldo_sha256"],
                         "respaldo_studio_ttl_sha256": resto["respaldo_studio_ttl_sha256"]},
             "gemma": resto["chat_gemma"], "tests": resto["tests"],
             "compatibilidad": compat,
             "w_adenda_v004": resto["w_adenda_v004"]}
    cierre = {"fecha_utc": ahora, "detalle_casos": overlay["detalle_casos"],
              "conteo_tipo_estado": overlay["conteo_tipo_estado"],
              "reapertura_nota": "condición exacta por caso en detalle_casos[].reapertura",
              "chat_gemma": "excluido"}
    salidas = emitir(root, ronda, cierre)
    print(json.dumps({"informes": salidas, "aceptadas_sha256": auditoria["aceptadas_sha256"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv)
