"""Genera resultado.md y propuestas.json desde resultados_intermedios.json."""
import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
d = json.loads((BASE / "resultados_intermedios.json").read_text(encoding="utf-8"))
res = d["resultados"]
fecha = d["fecha_utc"]

VAR = {}
for r in res:
    VAR.setdefault(r["variable_id"], r)

md = []
md.append("# Aplicacion de catalogos territoriales a archivos de datos\n")
md.append(f"Fecha de comprobacion (UTC): {fecha}\n")
md.append("Ocho variables documentadas con recurso de catalogo ya identificado "
          "(ontologia/territorio.json). No se reidentifica ni se propone ningun catalogo nuevo.\n")
md.append("## Alcance y metodo\n")
md.append("- Solo se leyeron columnas de clave, periodo (A\u00d1O/A\u00f1o) y nombre "
          "(NOM_MUN/NOM_ENT cuando existe). No se descargaron ni conservaron filas de personas; "
          "solo controles y conjuntos de claves.")
md.append("- Codigo original conservado; comparacion con `strip`. "
          "Transformacion propuesta: `strip` al comparar. Sin relleno (`zfill`) ni prefijos: "
          "las ocho referencias usan sus propias claves (la transformacion `26 + municipio a tres digitos` "
          "pertenece a otros casos y no se aplica aqui).")
md.append("- Cobertura (`completa`/`muestral`) y resultado (`compatible`/`compatible_con_excepciones`/"
          "`no_compatible`/`sin_columna_fisica`) se registran por separado.")
md.append("- Repetir un codigo en distintas filas (formato largo) no es por si solo un error.")
md.append("- Alias `Magdalena de Kino / Magdalena` (id `magdalena-sonora`, ontologia/territorio.json) "
          "vigilado solo en las entradas registradas; en los datos aparece `Magdalena`, sin activar el alias.")
md.append("- Compatibilidad de valores no demuestra vigencia historica ni autoriza cruces entre "
          "poblaciones, periodos o niveles de agregacion.\n")

md.append("## Resumen por variable documentada\n")
md.append("| Var | Variable | Conjunto | Recursos de datos | Periodos | Cobertura | Resultado |")
md.append("| --- | --- | --- | ---: | --- | --- | --- |")
for vid in ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"]:
    rs = [r for r in res if r["variable_id"] == vid and r["estado_resultado"] != "sin_columna_fisica"]
    r0 = next(r for r in res if r["variable_id"] == vid)
    pers = sorted({r["periodo"] for r in rs})
    per = pers[0] if len(pers) == 1 and "1990" in pers[0] else (pers[0] + "–" + pers[-1] if len(pers) > 1 else pers[0])
    est = "; ".join(sorted({r["estado_resultado"] for r in rs}))
    md.append(f"| {vid} | {r0['variable']} | {r0['titulo'][:45]} | {len(rs)} | {per} | completa | {est} |")
md.append("")
md.append("Nota: V6 (Clave_Ent, victimas) no tiene columna fisica en el recurso 2015 "
          "(`4c1f984e…`), que trae `Cve. Municipio` sin respaldo en el diccionario `a8a09044…`; "
          "ese recurso queda `sin_columna_fisica` para V6.\n")

md.append("## Detalle por recurso, columna y periodo\n")
for r in res:
    md.append(f"### {r['variable_id']} · {r['variable']} · recurso `{r['recurso_datos'][:8]}…` · periodo {r['periodo']}\n")
    md.append(f"- Comprobacion: valores distintos de la columna fisica "
              f"{('`' + r['columna_fisica'] + '`') if r['columna_fisica'] else '— (ausente)'} "
              f"contra `{r['referencia']['recurso'][:8]}…/{r['referencia']['hoja']}` "
              f"({r['referencia']['entradas']} entradas).")
    ub = r.get("columna_ubicacion")
    if ub:
        md.append(f"- Ubicacion fisica: hoja `{ub['hoja']}`, columna `{ub['letra']}` "
                  f"(posicion {ub['indice_1based']}), encabezado `{ub['encabezado']}`.")
    else:
        md.append(f"- Ubicacion fisica: sin columna fisica en el recurso; encabezado extraido del archivo: "
                  f"{r['consulta']['header_fisico']}.")
    md.append(f"- Significado: {r['significado']}.")
    c = r["cobertura"]
    if c.get("revision_encabezado"):
        md.append(f"- Cobertura: revision de encabezado **{c['revision_encabezado']}**; "
                  f"validacion de valores **{c['validacion_valores']}**.")
    else:
        md.append(f"- Cobertura: {r['estado_cobertura']} — {c['filas']} filas leidas, "
              f"{c['claves_distintas']} claves distintas"
              + (f", periodos: {c['anios_distintos'][0]}–{c['anios_distintos'][-1]} ({len(c['anios_distintos'])})" if c["anios_distintos"] and len(c["anios_distintos"]) > 1 else
                 (f", a\u00f1o: {c['anios_distintos'][0]}" if c["anios_distintos"] else "")) + ".")
    md.append(f"- Coincidencias: {r['coincidencias']['n']} de {c['claves_distintas'] if c['claves_distintas'] is not None else '?'} "
              f"claves en el catalogo.")
    e = r["excepciones"]
    md.append(f"- Excepciones: nulos={e['nulos']}; "
              f"especiales_no_municipales={e['especiales_no_municipales'] or '—'}; "
              f"sin_correspondencia={e['sin_correspondencia'] or '—'}" +
              (f"; nota: {e['nota']}" if e.get("nota") else "") + ".")
    if r["coherencia_compuesta"]:
        md.append(f"- Coherencia compuesta CLAVE↔CLAVE_ENT ({r['coherencia_compuesta'].get('regla', '')}): "
                  f"{r['coherencia_compuesta']['pares_distintos']} pares distintos, "
                  f"incoherentes={r['coherencia_compuesta']['incoherentes'] or 'ninguno'}.")
    if r["contradicciones_nombre"] is not None:
        md.append(f"- Nombres (NOM_MUN leido): "
                  f"{'sin contradicciones (un nombre por codigo)' if not r['contradicciones_nombre'] else r['contradicciones_nombre']}; "
                  f"26036 → {r['magdalena_26036_nombres']}.")
    md.append(f"- Transformacion propuesta: {r['transformacion_propuesta']}; "
              f"observadas en lectura: {e['transformaciones_observadas'] or '—'}.")
    md.append(f"- Consulta: {r['consulta']['metodo']} — `{r['consulta']['archivo_local']}`, "
              f"SHA-256 `{r['consulta']['sha256_archivo'][:16]}…`, {r['consulta']['fecha_utc']}.")
    md.append(f"- Estado del resultado: **{r['estado_resultado']}**. Limitaciones: {r['limitaciones']}\n")

md.append("## Casos especiales\n")
md.append("- `26998` (No Especificado) y `26999` (Otros Municipios): pertenecen al catalogo "
          "`36d3ac85…/cat_municipio` y, simultaneamente, son categorias no municipales "
          "(aparecen en los 11 recursos anuales de incidencia 2015–2025).")
md.append("- Victimas 2015 (`4c1f984e…`): 7252 filas con `Cve. Municipio` (74 claves 26001–26072 + "
          "26998/26999); esa columna no tiene respaldo en el diccionario `a8a09044…`, por lo que "
          "no se homologa con `Clave_Ent` ni se evalua contra `cat_entidad`.")
md.append("- Encabezados de periodo con `enye` (`A\u00d1O` en XLSX, `A\u00f1o` en CSV, UTF-8 con BOM en CSV); "
          "la lectura conserva el texto fisico y solo aplica `strip`.")
md.append("- SHA-256 completos de cada archivo descargado y de cada catalogo en `propuestas.json`; "
          "conjuntos de claves (original + normalizado) en `claves/`.\n")

(BASE / "resultado.md").write_text("\n".join(md), encoding="utf-8")

prop = []
for r in res:
    prop.append({
        "variable_id": r["variable_id"],
        "diccionario": r["diccionario"],
        "variable": r["variable"],
        "huella_fila_diccionario": r["huella_fila_diccionario"],
        "significado_respaldado_vs_columna": r["significado"],
        "conjunto": r["conjunto"],
        "titulo_conjunto": r["titulo"],
        "recurso_datos": r["recurso_datos"],
        "periodo": r["periodo"],
        "formato": r["formato"],
        "columna_fisica": r["columna_fisica"],
        "columna_ubicacion": r.get("columna_ubicacion"),
        "ubicaciones_leidas": r.get("ubicaciones_leidas", {}),
        "referencia_catalogo": r["referencia"],
        "consulta": r["consulta"],
        "cobertura": r["cobertura"],
        "coincidencias": r["coincidencias"],
        "excepciones": r["excepciones"],
        "coherencia_compuesta": r["coherencia_compuesta"],
        "contradicciones_nombre": r["contradicciones_nombre"],
        "magdalena_26036_nombres": r["magdalena_26036_nombres"],
        "transformacion_propuesta": r["transformacion_propuesta"],
        "estado_cobertura": r["estado_cobertura"],
        "estado_resultado": r["estado_resultado"],
        "limitaciones": r["limitaciones"],
        "aplica_al_grafo": False,
    })
(BASE / "propuestas.json").write_text(
    json.dumps({"fecha_utc": fecha,
                "nota": "Propuestas de comprobacion; no aplican asociaciones al grafo central.",
                "comprobaciones": prop}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"md + json escritos: {len(prop)} comprobaciones")
