"""Genera los 4 parches R8 con contextos byte-exactos. Solo staging I-codigo."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "patches"
OUT.mkdir(exist_ok=True)


def make_patch(rel, replacements, ctx=3, name=None):
    text = (ROOT / rel).read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    for old_block, new_block in replacements:
        assert text.count(old_block) == 1, f"ancla no única en {rel}: {old_block[:60]!r}"
    # construcción directa: para cada reemplazo emite hunk con -old/+new
    # rodeado de ctx líneas de contexto exactas del archivo
    out = [f"--- a/{rel}\n", f"+++ b/{rel}\n"]
    for old_block, new_block in replacements:
        idx = text.index(old_block)
        start = text.count("\n", 0, idx)
        old_lines = old_block.splitlines(keepends=True)
        new_lines = new_block.splitlines(keepends=True)
        pre = lines[max(0, start - ctx): start]
        post = lines[start + len(old_lines): start + len(old_lines) + ctx]
        hunk_old = len(pre) + len(old_lines) + len(post)
        hunk_new = len(pre) + len(new_lines) + len(post)
        out.append(f"@@ -{start - len(pre) + 1},{hunk_old} +{start - len(pre) + 1},{hunk_new} @@\n")
        for l in pre:
            out.append(" " + l)
        for l in old_lines:
            out.append("-" + l)
        for l in new_lines:
            out.append("+" + l)
        for l in post:
            out.append(" " + l)
    (OUT / (name or (Path(rel).stem + ".patch"))).write_text("".join(out), encoding="utf-8")
    print("ok", name or rel)


PROLOGO = (
    "        from integrar_ronda_8 import cargar as cargar_ronda_8, preparar_proyeccion_r7\n"
    "        semantic_vivo = semantic\n"
    "        r8c, r8f, r8base, r8accepted, r8sources = cargar_ronda_8()\n"
    "        sources.update({k: v for k, v in r8sources.items() if k not in sources})\n"
    "        semantic, delta8 = preparar_proyeccion_r7(\n"
    "            semantic, r7base, r7accepted, r8base, r8accepted, r8f)\n"
)
EPILOGO_R2 = (
    "        # Delta R8 real aprobado: derivado del lote A/B, nada observado.\n"
    "        vinc8 = {v['columna'] for v in r8accepted['vinculos']}\n"
    "        pre_cand8 = {m['columna'] for m in semantic['correspondencias']\n"
    "                     if m['estado'] == 'candidata_por_nombre'}\n"
    "        if not vinc8 <= pre_cand8:\n"
    "            raise ValueError('Vínculo R8 fuera de candidatas R7')\n"
    "        en_vivo8 = {m['columna'] for m in semantic_vivo['correspondencias']\n"
    "                    if m['estado'] == 'candidata_por_nombre'}\n"
    "        if en_vivo8 != pre_cand8 - vinc8:\n"
    "            raise ValueError('R8 altera candidatas fuera del delta aprobado')\n"
    "        expected['revisadas'] += delta8['n_vinculos']\n"
    "        expected['candidatas'] -= delta8['n_vinculos']\n"
)
EPILOGO_ENT = (
    "        # Delta R8 real aprobado sobre el reporte vivo (derivado, nada observado).\n"
    "        res8 = semantic_vivo['resumen']\n"
    "        if res8['estados_correspondencias']['documental_revisada'] != 4478 + delta8['n_vinculos'] \\\n"
    "                or res8['estados_correspondencias']['candidata_por_nombre'] != 45 - delta8['n_vinculos']:\n"
    "            raise ValueError('R8 sin delta de correspondencias derivado')\n"
    "        if res8['conceptos_compartidos'] != 1106 + delta8['n_conceptos']:\n"
    "            raise ValueError('R8 sin delta de conceptos derivado')\n"
    "        est8 = res8['estados_variables']\n"
    "        if est8['respaldada_por_definicion'] != 1423 + delta8['n_reglas'] \\\n"
    "                or est8['candidata_sin_definicion_suficiente'] != 16 - delta8['de_candidatas']:\n"
    "            raise ValueError('R8 sin delta de variables derivado')\n"
    "        if est8['respaldada_por_definicion'] + est8['fuera_del_nucleo_actual'] \\\n"
    "                + est8['candidata_sin_definicion_suficiente'] != res8['definiciones_con_nombre_examinadas']:\n"
    "            raise ValueError('R8 sin conservación total derivada')\n"
    "        if delta8['n_reglas']:\n"
    "            if res8['columnas_con_correspondencia'] < 4523:\n"
    "                raise ValueError('R8 redujo columnas con correspondencia')\n"
    "        elif res8['columnas_con_correspondencia'] != 4523:\n"
    "            raise ValueError('Pin histórico de columnas con correspondencia alterado')\n"
    "        variables8 = {v['definicion_iri']: v for v in semantic_vivo['variables']}\n"
    "        for row in r8accepted['reglas']:\n"
    "            observed = variables8[row['definiciones'][0]]\n"
    "            if observed.get('estado') != 'respaldada_por_definicion' \\\n"
    "                    or observed.get('regla') != row['id'] \\\n"
    "                    or observed.get('concepto') != row['concepto'] \\\n"
    "                    or observed.get('huella_fila_diccionario') != row['huella_fila_diccionario']:\n"
    "                raise ValueError('Regla R8 no materializada: ' + row['id'])\n"
    "        expected['conceptos'] += delta8['n_conceptos']\n"
    "        expected['variables_respaldadas'] += delta8['n_reglas']\n"
    "        expected['variables_pendientes'] -= delta8['de_candidatas']\n"
    "        expected['correspondencias_revisadas'] += delta8['n_vinculos']\n"
    "        semantic = semantic_vivo\n"
)

# 01 ------------------------------------------------------------------
t7 = (ROOT / "scripts/integrar_ronda_7.py").read_text(encoding="utf-8")
a1 = ('    if rules != expected:\n'
      '        raise ValueError("Ronda 7 permite solo la base y las adiciones auditadas exactas")\n')
b1 = ('    if (root / "ontologia/revision-ronda-8.json").exists():\n'
      "        import sys as _sys\n"
      "        _here = str(Path(__file__).resolve().parent)\n"
      "        if _here not in _sys.path:\n"
      "            _sys.path.insert(0, _here)\n"
      "        from integrar_ronda_8 import validar_sobre_base as validar_ronda_8\n"
      "        return validar_ronda_8(rules, expected, root)\n" + a1)
i = t7.index("    # Valida además toda la cadena histórica R4")
j = t7.index("    # no se reemplazan manifiestos anteriores.\n") + len("    # no se reemplazan manifiestos anteriores.\n")
a2 = t7[i:j]
b2 = ("    # Valida además toda la cadena histórica R4→R5→R6→R7→R8. R4 invoca\n"
      "    # validar_sobre_base (R5 delega a R6; R6 delega a R7; R7 delega a R8 si\n"
      "    # existe su config);\n"
      "    # no se reemplazan manifiestos anteriores.\n")
make_patch("scripts/integrar_ronda_7.py", [(a1, b1), (a2, b2)], name="01-integrar_ronda_7-delegacion.patch")

# 02 ------------------------------------------------------------------
t = (ROOT / "scripts/consolidar_semantica.py").read_text(encoding="utf-8")
a = ("    if (ROOT / 'ontologia/revision-ronda-7.json').exists():\n"
     "        from integrar_ronda_7 import construir as integrar_ronda_7\n"
     "        r7_data, r7_report, r7_sources = integrar_ronda_7(report, rules, base)\n"
     "        data += r7_data\n"
     "        report['integracion_ronda_7'] = r7_report\n"
     "        sources.update(r7_sources)\n")
b = a + ("    if (ROOT / 'ontologia/revision-ronda-8.json').exists():\n"
         "        from integrar_ronda_8 import construir as integrar_ronda_8\n"
         "        r8_data, r8_report, r8_sources = integrar_ronda_8(report, rules, base)\n"
         "        data += r8_data\n"
         "        report['integracion_ronda_8'] = r8_report\n"
         "        sources.update(r8_sources)\n")
make_patch("scripts/consolidar_semantica.py", [(a, b)], name="02-consolidar_semantica-hook.patch")

# 03a -----------------------------------------------------------------
t = (ROOT / "scripts/integrar_ronda_2.py").read_text(encoding="utf-8")
a = ("        sources.update({k: v for k, v in r7sources.items() if k not in sources})\n")
b = a + ("        # R8: proyección del reporte vivo a su equivalente R7; el bloque\n"
         "        # histórico siguiente corre intacto y el delta R8 se valida después.\n" + PROLOGO)
c = ("        expected['candidatas'] = len(viejas) + len(nuevas)\n"
     "        if expected['candidatas'] != 45:\n"
     "            raise ValueError('R7 sin 45 candidatas derivadas (17 + 28)')\n")
d = c + EPILOGO_R2
make_patch("scripts/integrar_ronda_2.py", [(a, b), (c, d)], name="03a-adaptador-ronda-2-proyeccion.patch")

# 03b -----------------------------------------------------------------
a = ("        sources.update({k: v for k, v in r7sources.items() if k not in sources})\n")
b = a + ("        # R8: proyección del reporte vivo a su equivalente R7; el bloque\n"
         "        # histórico siguiente corre intacto y el delta R8 se valida después.\n" + PROLOGO)
c = ("                raise ValueError('Regla R7 no materializada: ' + row['id'])\n")
d = c + EPILOGO_ENT
make_patch("scripts/integrar_entregas.py", [(a, b), (c, d)], name="03b-adaptador-entregas-proyeccion.patch")
