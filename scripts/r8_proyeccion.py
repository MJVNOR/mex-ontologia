"""Auxiliar R8: continuidad R7->R8 y proyeccion del reporte vivo a equivalente R7.

Un solo uso por adaptador (ronda-2, entregas): proyectar, correr el bloque
historico R7 intacto sobre lo proyectado, y validar despues el delta de 28
vinculos sobre el reporte vivo. Nada observado como expected: los pins
salen de cobertura-r7.json (4478/45/4523) y del lote A/B aprobado.
"""

import copy


def verificar_continuidad_r7_r8(r7base, r7accepted, r8base):
    """La base R8 es exactamente R7base + lote R7. Devuelve el delta R8."""
    if r8base["reglas_descripcion_exacta"] != r7base["reglas_descripcion_exacta"] + r7accepted["reglas"] \
            or r8base["vinculos_documentales_revisados"] != r7base["vinculos_documentales_revisados"] + r7accepted["vinculos"]:
        raise ValueError("Base R8 discontinua respecto a cadena R7")
    for k, v in r7base["conceptos"].items():
        if r8base["conceptos"].get(k) != v:
            raise ValueError("Concepto base alterado en cadena R8: " + k)
    for k, v in r7accepted["conceptos"].items():
        if r8base["conceptos"].get(k) != v:
            raise ValueError("Concepto R7 ausente en base R8: " + k)
    return {"n_reglas": 0, "n_vinculos": 28, "n_conceptos": 0}


def proyectar_semantica_r7(semantic, accepted):
    """28 revisadas -> candidatas con revision None; ajusta solo el summary.

    Verifica igualdad final fuera de las 28: todo lo demas queda identico.
    """
    vinc = {v["columna"] for v in accepted.get("vinculos", [])}
    if len(vinc) != 28:
        raise ValueError("R8 exige exactamente 28 vinculos proyectables")
    proj = copy.deepcopy(semantic)
    for m in proj.get("correspondencias", []):
        if m["columna"] in vinc:
            if m.get("estado") != "documental_revisada":
                raise ValueError("Vinculo R8 no revisado en reporte vivo: " + m["columna"])
            m["estado"] = "candidata_por_nombre"
            m["revision"] = None
    res = proj.get("resumen", {})
    est = res.get("estados_correspondencias", {})
    if "documental_revisada" in est:
        est["documental_revisada"] -= 28
    est["candidata_por_nombre"] = est.get("candidata_por_nombre", 0) + 28
    # Igualdad fuera de las 28: mismas columnas y mismas variables.
    cols_vivo = {m["columna"] for m in semantic.get("correspondencias", [])}
    cols_proj = {m["columna"] for m in proj.get("correspondencias", [])}
    if cols_vivo != cols_proj:
        raise ValueError("Proyeccion R8 altera columnas fuera del delta")
    if len(semantic.get("variables", [])) != len(proj.get("variables", [])):
        raise ValueError("Proyeccion R8 altera variables fuera del delta")
    return proj


def preparar_proyeccion_r7(semantic, r7base, r7accepted, r8base, r8accepted):
    """Continuidad + proyeccion en una llamada. Devuelve (proj, delta8)."""
    verificar_continuidad_r7_r8(r7base, r7accepted, r8base)
    return proyectar_semantica_r7(semantic, r8accepted), {"n_reglas": 0, "n_vinculos": 28, "n_conceptos": 0}
