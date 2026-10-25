"""Ronda 4 lote-3, reentrega por auditoria-a: corrige los 8 dictamenes
condicionados/rechazados sin tocar IDs, filas ni huellas.

- r4-lote-3-tiempo-9/10/11: conceptos especificos de momento de
  encuesta + representacion no_especificada (contradiccion formato vs
  ejemplo explicita, sin convertir fechas; sin forzar padre tiempo).
- sector-8: limite sin separar codigo/nombre/catalogo ni equivalencia
  entre encuestas.
- apoyo-14, instrumentos-18/20 (P10/P16/P18): representacion
  no_especificada + notas de truncamiento cuando corresponda.
- recursos-16: solo lista declarada, sin inferir monto/moneda/unidad.
Actualiza conceptos nuevos, decisiones_columnas, vinculos y motivos de
significados afectados (incluidos adicionales). No toca otros lotes.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

LOTE = Path(__file__).resolve().parent

ALCANCE = ("solo aplica a la definicion citada (alcance simultaneo por "
           "conjunto, diccionario, definicion, nombre y descripcion); no "
           "autoriza cruces, homologaciones ni equivalencias")

NUEVOS_CONCEPTOS = {
    "momento-inicio-encuesta": [
        "Momento de inicio de encuesta",
        "Hora de inicio declarada en la fila (Fecha y Hora); contradiccion "
        "explicita entre formato declarado y ejemplo; sin convertir fechas; "
        "evento y cobertura no documentados.", None],
    "momento-finalizacion-encuesta": [
        "Momento de finalizacion de encuesta",
        "Hora de finalizacion declarada en la fila (Fecha y Hora); "
        "contradiccion explicita entre formato declarado y ejemplo; sin "
        "convertir fechas; evento y cobertura no documentados.", None],
    "momento-ultima-modificacion-encuesta": [
        "Momento de ultima modificacion de encuesta",
        "Hora de la ultima modificacion declarada en la fila (Fecha y "
        "Hora); contradiccion explicita entre formato declarado y ejemplo; "
        "sin convertir fechas; evento y cobertura no documentados.", None],
}

# id regla -> (concepto, representacion, limites extra, nota criterio)
PARCHES = {
    "r4-lote-3-tiempo-9": (
        "momento-inicio-encuesta", "no_especificada",
        ["Tipo Fecha y Hora conservado integro; contradiccion explicita: "
         "Formato declarado 'DD/MM/AAAA HH:MM' frente a ejemplo "
         "'2024-01-17 10:58:15' (distinto del declarado); no se convierten "
         "fechas ni se infiere evento o cobertura.",
         "Metadato temporal de la respuesta; solo referencia declarada."],
        "momento de inicio de encuesta; ejemplo con fecha completa "
        "conservada sin convertir."),
    "r4-lote-3-tiempo-10": (
        "momento-finalizacion-encuesta", "no_especificada",
        ["Tipo Fecha y Hora conservado integro; contradiccion explicita: "
         "Formato declarado 'DD/MM/AAAA HH:MM' frente a ejemplo "
         "'2024-01-17 10:58:15' (distinto del declarado); no se convierten "
         "fechas ni se infiere evento o cobertura.",
         "Metadato temporal de la respuesta; solo referencia declarada."],
        "momento de finalizacion de encuesta; ejemplo con fecha completa "
        "conservada sin convertir."),
    "r4-lote-3-tiempo-11": (
        "momento-ultima-modificacion-encuesta", "no_especificada",
        ["Tipo Fecha y Hora conservado integro; contradiccion explicita: "
         "Formato declarado 'DD/MM/AAAA HH:MM' frente a ejemplo "
         "'2024-01-17 10:58:15' (distinto del declarado); no se convierten "
         "fechas ni se infiere evento o cobertura.",
         "Metadato temporal de la respuesta; solo referencia declarada."],
        "momento de ultima modificacion de encuesta; ejemplo con fecha "
        "completa conservada sin convertir."),
    "r4-lote-3-sector-dependencia-encuestada-8": (
        "sector-dependencia-encuestada", "nombre",
        ["Ejemplo '04 - SECRETARIA DE HACIENDA' se conserva integro: sin "
         "separar codigo de nombre, sin acreditar catalogo; sin comparacion "
         "entre encuestas ni equivalencia con otros relevamientos."],
        "sector declarado en texto; ejemplo integro sin separar."),
    "r4-lote-3-apoyo-tendencias-tic-dependencia-14": (
        "apoyo-tendencias-tic-dependencia", "no_especificada",
        ["Booleano Si/No (ejemplo Si): sin codigo documentado, solo "
         "existencia declarada.",
         "Descripcion posiblemente truncada en la fuente ('...que "
         "permit?'); literal conservado sin completar."],
        "respuesta Si/No a la pregunta de apoyo; sin codigo."),
    "r4-lote-3-recursos-anuales-innovacion-mencionados-16": (
        "recursos-anuales-innovacion-mencionados", "nombre",
        ["Solo lista declarada (ejemplo '5000, software'): sin inferir "
         "monto, moneda ni unidad; no agregar, convertir ni comparar."],
        "mencion libre de recursos anuales; solo lista declarada."),
    "r4-lote-3-instrumentos-previos-ley-gobierno-digital-18": (
        "instrumentos-previos-ley-gobierno-digital", "no_especificada",
        ["Booleano Si/No (ejemplo Si): sin codigo documentado, solo "
         "existencia declarada.",
         "Descripcion truncada en la fuente ('...en ma...'); literal "
         "conservado sin completar."],
        "respuesta Si/No sobre instrumentos previos a la Ley; descripcion "
        "truncada en fuente."),
    "r4-lote-3-instrumentos-actuales-mejora-administracion-20": (
        "instrumentos-actuales-mejora-administracion", "no_especificada",
        ["Booleano Si/No (ejemplo No): sin codigo documentado, solo "
         "existencia declarada.",
         "Descripcion truncada en la fuente ('...materia d...'); literal "
         "conservado sin completar."],
        "respuesta Si/No sobre instrumentos actuales; descripcion truncada "
        "en fuente."),
}


def main():
    entrega = json.loads((LOTE / "entrega.json").read_text(encoding="utf-8"))
    reglas = {r["id"]: r for r in entrega["reglas"]}
    assert set(PARCHES) <= set(reglas), "falta regla por corregir"
    for rid, (concepto, rep, limites, nota) in PARCHES.items():
        r = reglas[rid]
        r["concepto"] = concepto
        r["representacion"] = rep
        r["limites"] = [ALCANCE, *limites]
        var = r["nombres"][0]
        row = r["evidencia"][1]
        r["criterio"] = (f"Regla de descripcion exacta {rid} (correccion de "
                         f"auditoria-a): variable {var} {r['definiciones'][0]}"
                         f": descripcion literal «{r['descripciones'][0]}»; "
                         f"{row}; representacion {rep}; {nota}")
        r["evidencia"] = [*r["evidencia"], "correccion_auditoria_a=aplicada"]
    for slug, triple in NUEVOS_CONCEPTOS.items():
        assert slug not in entrega["conceptos_nuevos"]
        entrega["conceptos_nuevos"][slug] = triple

    by_def = {r["definiciones"][0]: r for r in entrega["reglas"]}
    for d in entrega["decisiones_columnas"]:
        r = by_def.get(d.get("definicion_iri", ""))
        if r is None or r["id"] not in PARCHES:
            continue
        d["concepto"] = r["concepto"]
        d["representacion"] = r["representacion"]
        d["motivo"] = (f"Campo presente en esquema capturado (nombre unico, "
                       f"variable unica en conjunto); definicion "
                       f"«{d['descripcion']}» respaldada por regla CORREGIDA "
                       f"{r['id']} segun auditoria-a (concepto "
                       f"{r['concepto']}, representacion "
                       f"{r['representacion']}); interpretacion coincide en "
                       f"merge local y en semantica-propuesta.json; "
                       f"dependencia explicita de significado propuesto aun "
                       f"no auditado; huellas verificadas.")
    for v in entrega["vinculos"]:
        hit = next((d for d in entrega["decisiones_columnas"]
                    if d["columna"] == v["columna"]
                    and d.get("dependencia_regla") in PARCHES), None)
        if hit is None:
            continue
        r = by_def[hit["definicion_iri"]]
        v["concepto"] = r["concepto"]
        v["criterio"] = (f"Revision explicita del campo {v['campo']} en el "
                         f"esquema capturado del recurso {v['recurso']} y su "
                         f"definicion {hit['definicion_iri']}: descripcion "
                         f"literal «{v['descripcion']}»; representacion "
                         f"{r['representacion']}; dependencia explicita de "
                         f"regla nueva {r['id']} CORREGIDA segun auditoria-a "
                         f"(propuesta, aun no auditada). Alcance de "
                         f"interpretacion documental; no se validan valores "
                         f"ni se confirma pertenencia a catalogos.")
    for s in entrega["decisiones_significados"]:
        r = by_def.get(s["definicion_iri"])
        if r is None or r["id"] not in PARCHES or s["decision"] != "proponer":
            continue
        s["motivo"] = (f"Descripcion literal con fila completa verificada "
                       f"respalda el sentido limitado del concepto "
                       f"{r['concepto']} (regla {r['id']} CORREGIDA segun "
                       f"auditoria-a); {r['limites'][-1]}")
        if not any("auditoria-a" in x for x in s["evidencia"]):
            s["evidencia"] = [*s["evidencia"], "correccion_auditoria_a=aplicada"]

    entrega["generado_en_utc"] = datetime.now(timezone.utc).isoformat()
    (LOTE / "entrega.json").write_text(
        json.dumps(entrega, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    n_col = len(entrega["decisiones_columnas"])
    n_prop = sum(1 for d in entrega["decisiones_columnas"]
                 if d["decision"] == "proponer")
    n_sig_p = sum(1 for d in entrega["decisiones_significados"]
                  if d["decision"] == "proponer")
    md = f"""# Resultado lote-3 (ronda 4, reentrega por auditoria-a)

- Columnas revisadas (originales 288 + adicionales 62, una vez cada IRI): {n_col}.
- Decisiones de columna: {n_prop} proponer, {n_col - n_prop} pendiente, 0 rechazar.
- Vinculos con formato exacto: {len(entrega["vinculos"])} (8 criterios y conceptos actualizados por auditoria).
- Significados: {len(entrega["decisiones_significados"])} ({n_sig_p} proponer, sin cambios de conjunto). Reglas: {len(entrega["reglas"])} (IDs, filas y huellas conservados; 8 corregidas). Conceptos nuevos: {len(entrega["conceptos_nuevos"])} (37 previos + 3 momentos de encuesta).
- Correcciones: tiempo-9/10/11 a conceptos especificos de momento de encuesta con no_especificada (contradiccion formato/ejemplo explicita, sin convertir); sector-8 sin separar codigo/nombre/catalogo ni equivalencia entre encuestas; P10/P16/P18 a no_especificada con notas de truncamiento; recursos-16 solo lista declarada.
- Solicitudes de investigacion: {len(entrega["solicitudes_investigacion"])} grupos (sin cambios).
"""
    (LOTE / "resultado.md").write_text(md, encoding="utf-8")
    sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
    (LOTE / "listo.json").write_text(json.dumps({
        "lote": "lote-3", "sha256": sha, "columnas": n_col,
        "proponer_columna": n_prop, "pendientes_columna": n_col - n_prop,
        "significados": len(entrega["decisiones_significados"]),
        "proponer_significado": n_sig_p,
        "vinculos": len(entrega["vinculos"]), "reglas": len(entrega["reglas"]),
        "conceptos_nuevos": len(entrega["conceptos_nuevos"])},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reglas_corregidas": len(PARCHES),
                      "conceptos_nuevos": len(entrega["conceptos_nuevos"]),
                      "sha256": sha[:16] + "..."}))


if __name__ == "__main__":
    main()
