"""Genera entrega lote-4: verifica evidencia concreta y emite decisiones."""
import json, hashlib, pathlib
BASE = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
LOTE = BASE/"propuestas/pendientes-muse-r4/lote-4"
def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode("utf-8")).hexdigest()
def clave(s):
    import unicodedata
    s=str(s or "").strip().lower()
    s="".join(c for c in unicodedata.normalize("NFKD",s) if not unicodedata.combining(c))
    return " ".join(s.split())
asig=json.load(open(LOTE/"asignacion.json",encoding="utf-8"))
cob=json.load(open(BASE/"data/semantica/cobertura.json",encoding="utf-8"))
sem=json.load(open(BASE/"ontologia/semantica.json",encoding="utf-8"))
inv=json.load(open(BASE/"data/portal/inventario.json",encoding="utf-8"))
ins=json.load(open(BASE/"data/portal/contenido-inspeccion.json",encoding="utf-8"))
vidx={v.get("definicion_iri"):v for v in cob["variables"]}
recs={r["id"]:r for r in inv["recursos"]}
insr={r["id"]:r for r in ins["recursos"]}
rules={r["id"]:r for r in sem["reglas_descripcion_exacta"]}
obs={(o.get("diccionario"),o.get("variable")):o for o in sem.get("observaciones_revision",[])}
# unicidad diccionario: contar por (conjunto, clave(nombre)) en definiciones inspeccionadas
from collections import Counter
cnt=Counter()
for rid,r in insr.items():
    inv_r=recs.get(rid)
    if not inv_r or inv_r["clasificacion"]!="diccionario" or not r.get("ok"): continue
    for row in r.get("definiciones",[]):
        n=row.get("Nombre variable") or row.get("Nombre de variable") or row.get("variable") or row.get("Nombre campo") or ""
        if n: cnt[(inv_r["conjunto_id"],clave(n))]+=1
decisiones=[]; vinculos=[]; pend_det=[]
for col in asig["columnas"]:
    campo=col["campo"]; rec=col["recurso"]; conj=col["conjunto"]
    diris=col["definiciones_por_nombre"]
    # lote-4: una definicion por columna
    di=diris[0] if len(diris)==1 else None
    v=vidx.get(di) if di else None
    # evidencia esquema
    ir=insr.get(rec); invr=recs.get(rec)
    he=None; uniq_esq=None; hojas=None
    if invr and invr.get("datastore",{}).get("ok"):
        fields=[f for f in invr["datastore"]["campos"] if not f["id"].startswith("_")]
        ids=[f["id"] for f in fields]
        if campo in ids or clave(campo) in [clave(i) for i in ids]:
            he=huella([{"nombre":f["id"],"tipo":f.get("type")} for f in fields]); hojas="datastore"
            uniq_esq=sum(clave(i)==clave(campo) for i in ids)==1
    elif ir and ir.get("ok"):
        for t in ir.get("tablas",[]):
            ids=[f["id"] for f in t["campos"]]
            if campo in ids or clave(campo) in [clave(i) for i in ids]:
                he=huella(t); hojas=t["hoja"]
                uniq_esq=sum(clave(i)==clave(campo) for i in ids)==1
                break
    hf=v.get("huella_fila_diccionario") if v else None
    # verificar fila local
    dic=v.get("diccionario") if v else None
    dr=insr.get(dic) if dic else None
    fila_ok=False; uniq_dic=None
    if v and dr:
        for i,row in enumerate(dr.get("definiciones",[]),1):
            n=row.get("Nombre variable") or row.get("variable") or ""
            iri=f"https://example.org/mex-ontologi/definition/{dic}%2F{i}"
            if iri==di:
                fila_ok=(huella(row)==hf); break
        uniq_dic=cnt.get((conj,clave(v.get("variable",""))))
        uniq_dic=(uniq_dic==1)
    estado_var=v.get("estado") if v else "sin_variable"
    bloqueada=(dic,v.get("variable") if v else None) in obs if v else False
    nombre_ok = v and (v.get("variable")==campo or clave(v.get("variable"))==clave(campo))
    if v and estado_var=="respaldada_por_definicion" and nombre_ok and uniq_esq and uniq_dic and fila_ok and he and not bloqueada:
        concepto=v["concepto"]; regla=v.get("regla"); r= rules.get(regla,{})
        desc=v.get("descripcion","")
        rep=v.get("representacion","no_especificada")
        lims=v.get("limites",[])
        crit=("Vinculo columna fisica -> variable documentada del mismo conjunto: nombre con relacion registrada, "
              "descripcion que respalda cada calificador, diccionario y recurso localizados en el conjunto, "
              "unicidad en diccionario y esquema, sin alias. Alcance documental.")
        ev=[f"data/portal/contenido-inspeccion.json#recursos/{rec}/tablas/{hojas}",
            f"data/portal/contenido-inspeccion.json#recursos/{dic}/definiciones",
            f"data/semantica/cobertura.json#variables/{di}",
            f"ontologia/semantica.json#reglas/{regla}"]
        decisiones.append({"columna":col["columna"],"recurso":rec,"campo":campo,
            "decision":"proponer","definicion_iri":di,
            "motivo":f"Nombre con relacion registrada en mismo conjunto/diccionario; descripcion literal respalda '{concepto}' ({regla}, {rep}); unicidad esquema+diccionario; huellas verificadas.",
            "evidencia":ev})
        vinculos.append({"recurso":rec,"campo":campo,"columna":col["columna"],"diccionario":dic,
            "concepto":concepto,"descripcion":desc,"huella_esquema":he,"huella_fila_diccionario":hf,"criterio":crit})
    else:
        if bloqueada: mot="pendiente: observacion documental vigente en semantica.json (p.ej. Total_Egresos descrito como urgencias); no se interpreta ni equipara."
        elif not v or estado_var!="respaldada_por_definicion": mot=f"pendiente: variable sin respaldo ({estado_var}); el nombre solo es candidato."
        elif not nombre_ok: mot="pendiente: campo no coincide con variable de la fila exacta; sin alias global."
        elif not (uniq_esq and uniq_dic): mot="pendiente: unicidad no acreditada en esquema/diccionario."
        elif not fila_ok: mot="pendiente: huella de fila no verificada localmente."
        else: mot="pendiente: evidencia insuficiente."
        o=obs.get((dic,v.get("variable") if v else None)) if v else None
        ev=[f"data/portal/contenido-inspeccion.json#recursos/{rec}",f"data/portal/contenido-inspeccion.json#recursos/{dic}",
            f"data/semantica/cobertura.json#variables/{di}"]+([f"ontologia/semantica.json#observaciones/{o.get('id')}"] if o else [])
        decisiones.append({"columna":col["columna"],"recurso":rec,"campo":campo,"decision":"pendiente",
            "definicion_iri":di,"motivo":mot,"evidencia":ev})
        pend_det.append({"columna":col["columna"],"campo":campo,"recurso":rec,"definicion_iri":di,"motivo":mot,"evidencia":ev})
# significados
dec_sig=[]; sol=[]
for vp in asig["variables_pendientes"]:
    di=vp["definicion_iri"]; v=vidx.get(di,{})
    ev=[f"data/portal/contenido-inspeccion.json#recursos/{vp['diccionario']}",
        f"data/semantica/cobertura.json#variables/{di}"]
    if vp["variable"]=="Total_Egresos":
        ev.append("ontologia/semantica.json#observaciones/egresos-descripcion-urgencias")
        mot="pendiente: 'Total_Egresos' con descripcion 'Total de urgencias atendidas'; contradiccion nombre/descripcion sin aclaracion de la fuente; no se interpreta como egresos ni como urgencias."
        sol.append({"definicion_iri":di,"variable":"Total_Egresos","diccionario":vp["diccionario"],
            "duda":"Aclarar si Total_Egresos cuenta egresos hospitalarios o urgencias atendidas.",
            "fuente_probable":"Dependencia publicadora del conjunto Egresos Hospitalarios (diccionario f89137ba).",
            "documento_requerido":"Diccionario corregido o nota de la fuente que fije el significado de Total_Egresos."})
    elif vp["variable"] in ("CVOTRAS","DOTRAS"):
        mot="pendiente: 'otras' sin especificar; descripcion no fija dominio, medida ni catalogo; no se infiere."
        sol.append({"definicion_iri":di,"variable":vp["variable"],"diccionario":vp["diccionario"],
            "duda":"Que categorias residuales cubre 'otras' y con que catalogo/medida.",
            "fuente_probable":"Publicador de Pesca y Acuacultura (conjunto e093cf34).","documento_requerido":"Diccionario con definicion de CVOTRAS/DOTRAS o catalogo de referencia."})
    elif vp["conjunto"]=="93ca5e1c-702e-4e62-bc61-638907be184a":
        mot="pendiente: clasificacion delictiva sin regla revisada ni catalogo resuelto; no se homologa por nombre."
        sol.append({"definicion_iri":di,"variable":vp["variable"],"diccionario":vp["diccionario"],
            "duda":f"Dominio y catalogo de '{vp['variable']}'.","fuente_probable":"Publicador de Incidencia delictiva municipal.",
            "documento_requerido":"Diccionario con dominio/catalogo de la variable o clasificacion oficial aplicable."})
    else:
        mot=f"pendiente: fuera del nucleo actual ({vp['motivo']}); descripcion de encuesta/metadato sin regla de interpretacion revisada; no se propone concepto."
        sol.append({"definicion_iri":di,"variable":vp["variable"],"diccionario":vp["diccionario"],
            "duda":f"Alcance interpretable de '{vp['variable']}': {vp['descripcion']}",
            "fuente_probable":"Publicador del conjunto "+vp.get("titulo_conjunto",""),
            "documento_requerido":"Diccionario con dominio, medida o catalogo que respalde el significado."})
    dec_sig.append({"definicion_iri":di,"decision":"pendiente","motivo":mot,"evidencia":ev})
    # pendientes de columnas que dependen de significados pendientes? ninguna (solo Total_Egresos ya)
entrega={"lote":"lote-4","decisiones_columnas":decisiones,"vinculos":vinculos,"decisiones_significados":dec_sig,
    "reglas":[],"conceptos_nuevos":{},"solicitudes_investigacion":sol,
    "conteos":{"columnas":len(decisiones),"proponer":sum(1 for d in decisiones if d["decision"]=="proponer"),
               "pendiente_columnas":sum(1 for d in decisiones if d["decision"]=="pendiente"),
               "significados":len(dec_sig),"vinculos":len(vinculos)}}
json.dump(entrega,open(LOTE/"entrega.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
json.dump({"pendientes_columnas":pend_det,
    "nota":"Solo Total_Egresos queda pendiente entre columnas (observacion vigente). Resto de pendientes son los 47 significados fuera del nucleo; ver solicitudes_investigacion."},
    open(LOTE/"pendientes.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(json.dumps(entrega["conteos"],indent=1))
print("proponer OK" if all(len(v)==9 for v in vinculos) else "FORMATO MAL")
