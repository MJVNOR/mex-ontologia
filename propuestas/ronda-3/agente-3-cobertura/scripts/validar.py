"""Validador real de propuestas de significado (agente 3, ronda 3).

Una sola funcion, `validar_propuestas(prop, fuentes, asignacion)`, usada por
la construccion (auto-chequeo) y por la verificacion (positivo y negativos).
Devuelve una lista de errores [{"codigo", "detalle"}]; vacia = valida.
Sin efectos laterales. Solo stdlib. No lee archivos.
"""

CAMPOS_REGLA = ("id", "concepto", "representacion", "descripciones", "nombres",
                "conjuntos", "diccionarios", "definiciones", "criterio",
                "fuente_revision", "alcance", "positivo", "contraejemplo",
                "limite", "evidencia")


def validar_propuestas(prop, fuentes, asignacion):
    errores = []

    def err(codigo, detalle):
        errores.append({"codigo": codigo, "detalle": detalle})

    variables = fuentes.get("variables_por_iri", {})
    ids_nucleo = set(fuentes.get("ids_reglas", ()))
    conceptos_nucleo = set(fuentes.get("conceptos", ()))
    representaciones = set(fuentes.get("representaciones", ()))
    filas = fuentes.get("filas", {})
    frontera = set((asignacion or {}).get("frontera", ()))
    esperadas = (asignacion or {}).get("cubiertas_esperadas")

    nuevos = prop.get("conceptos_nuevos", {})
    for c, triple in nuevos.items():
        if c in conceptos_nucleo:
            err("CONCEPTO_NUEVO_COLISIONA", c)
        if not isinstance(triple, list) or len(triple) != 3 or not triple[0] or not triple[1]:
            err("CONCEPTO_SIN_DOC", c)
        elif triple[2] is not None and triple[2] not in conceptos_nucleo and triple[2] not in nuevos:
            err("BROADER_INVALIDO", c + " -> " + str(triple[2]))

    vistos = set()
    tocadas = set()
    por_concepto = {}
    for r in prop.get("reglas", []):
        rid = r.get("id", "?")
        for campo in CAMPOS_REGLA:
            if campo not in r:
                err("CAMPO_FALTANTE", rid + " :: " + campo)
        if rid in vistos:
            err("ID_DUPLICADO", rid)
        vistos.add(rid)
        if rid in ids_nucleo:
            err("ID_COLISIONA_NUCLEO", rid)
        concepto = r.get("concepto")
        if concepto not in conceptos_nucleo and concepto not in nuevos:
            err("CONCEPTO_DESCONOCIDO", rid + " :: " + str(concepto))
        if r.get("representacion") not in representaciones:
            err("REPRESENTACION_INVALIDA", rid + " :: " + str(r.get("representacion")))
        n = len(r.get("definiciones", []))
        if n == 0 or len(r.get("descripciones", [])) != n or len(r.get("nombres", [])) != n:
            err("LISTAS_DISPARES", rid)
        if not r.get("conjuntos") or not r.get("diccionarios") or not r.get("definiciones"):
            err("SIN_RESTRICCION", rid)
        por_concepto.setdefault(concepto, []).append(r)
        prosa = " ".join(str(r.get(k, "")) for k in ("alcance", "positivo", "contraejemplo", "limite"))
        for iri, desc, nom in zip(r.get("definiciones", []), r.get("descripciones", []),
                                  r.get("nombres", [])):
            if "/column/" in iri or "/file-column/" in iri:
                err("IRI_COLUMNA", rid + " :: " + iri)
                continue
            v = variables.get(iri)
            if v is None:
                err("IRI_DESCONOCIDA", rid + " :: " + iri)
                continue
            if v.get("descripcion") != desc:
                err("LITERAL_DIFERENTE", rid + " :: descripcion :: " + nom)
            if v.get("variable") != nom:
                err("LITERAL_DIFERENTE", rid + " :: nombre :: " + nom)
            if v.get("diccionario") not in r.get("diccionarios", []):
                err("LITERAL_DIFERENTE", rid + " :: diccionario :: " + nom)
            if v.get("conjunto") not in r.get("conjuntos", []):
                err("LITERAL_DIFERENTE", rid + " :: conjunto :: " + nom)
            if v.get("estado") != "fuera_del_nucleo_actual":
                err("ESTADO_NO_FUERA", rid + " :: " + nom + " :: " + str(v.get("estado")))
            if iri in frontera:
                err("FRONTERA_AGENTE4", rid + " :: " + iri)
            tocadas.add((v.get("diccionario"), v.get("variable")))
        ev = r.get("evidencia")
        if not isinstance(ev, list) or len(ev) != len(r.get("definiciones", [])):
            err("EVIDENCIA_FALTANTE", rid)
        else:
            for e, iri in zip(ev, r.get("definiciones", [])):
                f = filas.get((e.get("diccionario"), e.get("variable")))
                if f is None:
                    err("EVIDENCIA_SIN_FUENTE", rid + " :: " + str(e.get("variable")))
                    continue
                for campo, llave in (("descripcion", "descripcion"),
                                     ("unidad_de_medida", "unidad"),
                                     ("tipo_de_dato", "tipo"), ("ejemplo_de_dato", "ejemplo")):
                    if e.get(campo) != f.get(llave):
                        err("EVIDENCIA_DIFERENTE", rid + " :: " + campo)
        for desc in r.get("descripciones", []):
            if desc and desc in prosa:
                err("PROSA_TRANSCRIBE", rid)

    for c, rs in por_concepto.items():
        if len(rs) > 1:
            if any(x.get("calificador") is None for x in rs):
                err("CALIFICADOR_FALTANTE", c)
            cals = [str(sorted((x.get("calificador") or {}).items())) for x in rs]
            if len(set(cals)) != len(rs):
                err("CALIFICADOR_DUPLICADO", c)

    if esperadas is not None:
        faltan = set(esperadas) - set(tocadas)
        sobran = set(tocadas) - set(esperadas)
        if faltan:
            err("COBERTURA_INCOMPLETA", str(sorted(faltan)))
        if sobran:
            err("COBERTURA_EXCEDIDA", str(sorted(sobran)))

    return errores
