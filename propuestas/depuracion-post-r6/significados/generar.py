"""Generador v2 de propuestas/depuracion-post-r6/significados/.
Lee R5/R6/auditoria/inspecciones; no toca nucleo, grafo, Studio ni archivos ajenos.
Escribe UNICAMENTE pendientes.json, pendientes.md y listo.json. UTF-8 explicito.
"""
import json, hashlib, re, datetime, pathlib
from collections import Counter

REPO = pathlib.Path(r'C:\Users\marti\Documents\MEX-Ontologi')
OUT = REPO / 'propuestas' / 'depuracion-post-r6' / 'significados'

def load(rel):
    return json.loads((REPO / rel).read_bytes().decode('utf-8'))

def sha(rel):
    return hashlib.sha256((REPO / rel).read_bytes()).hexdigest()

R5 = load('reports/pendientes-ronda-5.json')
SIGS_R5 = R5['significados']
IDX_R5 = {}
for i, s in enumerate(SIGS_R5):
    assert s['definicion_iri'] not in IDX_R5
    IDX_R5[s['definicion_iri']] = i
assert len(SIGS_R5) == 171

AUD_REL = 'propuestas/pendientes-muse-r6/auditoria-documental/entrega-final.json'
AUD = load(AUD_REL)
IDX_AUD = {}
for j, x in enumerate(AUD['dictamenes']):
    if x.get('tipo') == 'decision' and x.get('id') not in IDX_AUD:
        IDX_AUD[x['id']] = j

ROLES = ['salud', 'matriculas', 'epidemiologia', 'tic', 'diversos-presas']
ENT = {r: load(f'propuestas/pendientes-muse-r6/{r}/entrega.json') for r in ROLES}
ROL_ENTREGA = {r: f'propuestas/pendientes-muse-r6/{r}/entrega.json' for r in ROLES}
DEC, FALT = {}, {}
for rol, d in ENT.items():
    for x in d.get('decisiones_significados', []) or d.get('decisiones', []):
        iri = x.get('definicion_iri')
        if iri:
            assert iri not in DEC, iri
            DEC[iri] = (rol, x)
    for p in d.get('pendientes', []):
        if 'definicion_iri' in p and 'iris' not in p:
            FALT[p['definicion_iri']] = p
        elif 'iris' in p:
            for iri in p['iris']:
                FALT[iri] = {'detalle': p.get('detalle', ''), 'id': p.get('id', '')}

EXCLUIDOS = [
    'https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177',
    'https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178',
]
INSP_177 = load('data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json')
assert len(INSP_177['definiciones']) == 178
f177, f178 = INSP_177['definiciones'][176], INSP_177['definiciones'][177]
assert (f177.get('Nombre variable'), f177.get('Tipo de dato'), f177.get('Formato')) == ('ide_id', 'ide_sex', 'ide_eda_ano')
assert (f178.get('Nombre variable'), f178.get('Tipo de dato'), f178.get('Formato')) == ('ide_id', 'ide_sex', 'ide_eda_ano')
assert (f177.get('Ejemplo de dato'), f178.get('Ejemplo de dato')) == ('ide_cp', 'id_cp')

RE_UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
RE_HOJA = re.compile(r'hoja=([A-Za-z0-9_ ]+?)(?::|\)|,|;|$)|fila (Hoja1)|hoja \'([^\']+)\'|\b(Hoja1)\b|hoja (SUIVE)')
RE_POS = re.compile(r'posicion=(\d+)|campo pos (\d+)|fila Hoja1 (\S+)|definiciones\[(\d+)\]')
RE_BRACK = re.compile(r'definiciones\[\d+\]')

def extraer(texto):
    hoja, posfis, citas = 'desconocido', 'desconocido', []
    h = RE_HOJA.search(texto)
    if h:
        hoja = next((g for g in h.groups() if g), 'desconocido').strip()
    q = RE_POS.search(texto)
    if q:
        posfis = next((g for g in q.groups() if g), 'desconocido')
    for frag in texto.split(' | '):
        if any(k in frag for k in ('inspecciones/', 'contenido-inspeccion', 'hoja', 'Hoja1', 'posicion', 'campo pos', 'Recurso', 'recurso', 'definiciones[')):
            frag = frag.strip()
            if frag and frag not in citas:
                citas.append(frag)
            if len(citas) == 3:
                break
    return hoja, posfis, citas if citas else ['desconocido']

def recurso_datos(faltante_texto):
    m = RE_UUID.search(faltante_texto or '')
    if m:
        return 'citado_sin_vinculo:' + m.group(0)
    return 'no_acreditado'

CRITERIO = ('Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada '
    'a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila '
    '(conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario '
    'corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia '
    'primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, '
    'ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.')
NOTA_MANOS = ('El documento exacto requerido esta en manos del publicador segun R6; esto no demuestra '
    'que toda investigacion adicional sea imposible (ver notas_grupo con lineas alternativas acotadas).')

INSP_CACHE = {}
def inspeccion(dicc_id):
    if dicc_id not in INSP_CACHE:
        rel = f'data/portal/inspecciones/{dicc_id}.json'
        d = load(rel)
        INSP_CACHE[dicc_id] = (rel, sha(rel), d)
    return INSP_CACHE[dicc_id]

significados = []
for s in SIGS_R5:
    iri = s['definicion_iri']
    if iri in EXCLUIDOS:
        continue
    assert iri in DEC, iri
    assert iri in IDX_AUD, iri
    rol, dec = DEC[iri]
    p = FALT.get(iri, {})
    falt = (p.get('documento_exacto_necesario') or p.get('evidencia_faltante')
            or p.get('requerido') or p.get('detalle') or 'desconocido')
    ev = dec.get('evidencia', []) or ['desconocido']
    blob = ' | '.join([dec.get('motivo', '')] + [str(e) for e in (ev if isinstance(ev, list) else [ev])] + [str(falt)])
    hoja, posfis, citas = extraer(blob)
    fila = iri.split('%2F')[-1]
    assert fila.isdigit(), iri
    rel_insp, sha_insp, d_insp = inspeccion(s['diccionario'])
    defs = d_insp['definiciones']
    assert len(defs) >= int(fila), (iri, len(defs))
    obs = defs[int(fila) - 1].get('Nombre variable', '').strip()
    assert obs == s.get('variable', '').strip(), (iri, obs, s.get('variable'))
    nota_ind = None
    if any(RE_BRACK.search(c) for c in citas):
        nota_ind = ('citas textuales R6 usan indice original 1-based (p. ej. definiciones[%s] = fila %s); '
                    'no es JSON pointer; el localizador verificado usa /definiciones/%d'
                    % (fila, fila, int(fila) - 1))
    grupo = ('salud-defunciones' if s['conjunto'] == 'cd3d6e34-3789-479e-9f2b-a717b8419f9c'
             else 'salud-nacimientos' if rol == 'salud'
             else {'matriculas': 'matriculas', 'epidemiologia': 'epidemiologia', 'tic': 'tic'}.get(rol, 'diversos'))
    significados.append({
        'definicion_iri': iri,
        'variable': s.get('variable', 'desconocido'),
        'descripcion_original': s.get('descripcion', 'desconocido'),
        'conjunto_id': s.get('conjunto', 'desconocido'),
        'conjunto_titulo': s.get('titulo_conjunto', 'desconocido'),
        'diccionario_id': s.get('diccionario', 'desconocido'),
        'fila': fila,
        'huella_fila_diccionario': s.get('huella_fila_diccionario', 'desconocido'),
        'catalogo_declarado': s.get('catalogo_declarado', 'desconocido'),
        'estado_cobertura': s.get('estado', 'desconocido'),
        'recurso_diccionario_id': s.get('diccionario', 'desconocido'),
        'recurso_de_datos': recurso_datos(str(falt)),
        'nota_recurso': ('recurso_diccionario_id conocido (locator del diccionario); recurso_de_datos '
                         'sin vinculo acreditado a columnas de datos: no se inventa mapeo; '
                         '"citado_sin_vinculo:<uuid>" solo recoge el recurso mencionado en la evidencia '
                         'faltante, sin acreditar correspondencia con columnas fisicas.'),
        'tabla_hoja': hoja,
        'posicion_fisica': posfis,
        'localizacion_r6': citas,
        'nota_indice_original': nota_ind,
        'grupo_fuente': grupo,
        'rol_r6': rol,
        'estado': 'sin_documentacion_suficiente',
        'dictamen_r6_motivo': dec.get('motivo', 'desconocido'),
        'evidencia_r6': ev,
        'evidencia_documental_exacta_faltante': falt,
        'en_manos_del_publicador': bool(p.get('en_manos_del_publicador', True)),
        'nota_en_manos': NOTA_MANOS,
        'criterio_aceptacion_futura': CRITERIO,
        'limites_r6': dec.get('limites', []),
        'localizadores_verificados': {
            'r5_significado': {'ruta': 'reports/pendientes-ronda-5.json', 'sha256': sha('reports/pendientes-ronda-5.json'),
                               'json_pointer': f'/significados/{IDX_R5[iri]}'},
            'inspeccion_fila': {'ruta': rel_insp, 'sha256': sha_insp,
                                'json_pointer': f'/definiciones/{int(fila) - 1}',
                                'verificado_variable': True},
            'auditoria_dictamen': {'ruta': AUD_REL, 'sha256': sha(AUD_REL),
                                   'json_pointer': f'/dictamenes/{IDX_AUD[iri]}',
                                   'dictamen': AUD['dictamenes'][IDX_AUD[iri]].get('dictamen', 'desconocido')},
            'entrega_r6_que_confirma': ROL_ENTREGA[rol],
        },
    })

ORDEN = ['salud-defunciones', 'salud-nacimientos', 'matriculas', 'epidemiologia', 'tic', 'diversos']
significados.sort(key=lambda x: (ORDEN.index(x['grupo_fuente']), x['conjunto_id'], int(x['fila'])))
for i, x in enumerate(significados, 1):
    x2 = {'n': i}
    x2.update(x)
    significados[i - 1] = x2

conteo_grupos = Counter(x['grupo_fuente'] for x in significados)
iris = [x['definicion_iri'] for x in significados]
assert len(significados) == 169 and sum(conteo_grupos.values()) == 169
assert len(set(iris)) == 169 and set(iris) <= set(IDX_R5)
assert len(significados) + len(EXCLUIDOS) == 171
diccs = sorted({x['diccionario_id'] for x in significados})
assert len(diccs) == 16, diccs
assert sorted(conteo_grupos.keys()) == sorted(ORDEN)

NOTAS_GRUPO = [
    {'grupo_fuente': 'salud-defunciones', 'n': 32, 'nota': 'ADV-SALUD-MANUAL (auditoria R6, advertencia): Manual SEED 2022 autentico preservado (HTTP 200, PDF) no examinado por ID en salud (0/85 motivos lo citan). Linea alternativa acotada: completar examen por ID citando pregunta exacta del manual y por que la correspondencia formal falla (sin mapa campo-codigo/posicion, ejemplo incompatible, ambito fetal vs general) o vinculo del publicador; sin promover definiciones; no se resuelve ahora. Declaraciones publicas necesarias: diccionario SEED corregido + codebook + vinculo manual-recurso-CIE 2022 y nota edicion-recurso-periodo.'},
    {'grupo_fuente': 'salud-nacimientos', 'n': 53, 'nota': 'Aplica ADV-SALUD-MANUAL como linea alternativa (examen por ID del manual preservado, sin promocion). Declaraciones publicas necesarias: diccionario SINAC corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Nacimientos 2022. No se resuelve ahora.'},
    {'grupo_fuente': 'matriculas', 'n': 30, 'nota': 'R5 ya reviso reglamentos 2019/2022 y guia 2023; R6 confirma linea agotada. Declaracion publica necesaria: diccionario/matriz con descripciones + codebook + calendario 2022-2 y edicion aplicable distinta de 2019. No se resuelve ahora.'},
    {'grupo_fuente': 'epidemiologia', 'n': 25, 'nota': 'Linea base negativa reutilizable: C1 (API version=null) + C2 (core-properties). Declaracion publica necesaria: instrumento SUIVE edicion 2022 + diccionario corregido + regla de computo + version CIE + nota borde edad 5. No se resuelve ahora.'},
    {'grupo_fuente': 'tic', 'n': 24, 'nota': 'Linea portal agotada (S09 negativo, no repetida en R6). Declaraciones publicas necesarias: cuestionarios originales completos y muestras. Que esten en manos del publicador no cierra otras lineas primarias inequivocas futuras. No se resuelve ahora.'},
    {'grupo_fuente': 'diversos', 'n': 5, 'nota': 'cat_estatal_1.xlsx autentico preservado (VW-33, dominio CCCCC; falta F3/F4); CONAPO 09-05-2024 y SESNSP examinados (falta declaracion del publicador). Resto segun evidencia faltante por fila. No se resuelve ahora.'},
]

FUENTES_DEF = [
    ('reports/pendientes-ronda-5.json', 'Base: 171 significados con dictamen documental R5.'),
    ('reports/pendientes-semanticos.json', 'Cotejo: 171 variables pendientes vigentes.'),
    ('data/semantica/cobertura.json', 'Cotejo: estados de cobertura actuales.'),
    ('propuestas/pendientes-muse-r6/salud/entrega.json', 'R6 salud: 85 decisiones pendiente + evidencia faltante exacta.'),
    ('propuestas/pendientes-muse-r6/matriculas/entrega.json', 'R6 matriculas: 30 decisiones pendiente + evidencia faltante exacta.'),
    ('propuestas/pendientes-muse-r6/epidemiologia/entrega.json', 'R6 epidemiologia: 25 decisiones pendiente + evidencia faltante exacta.'),
    ('propuestas/pendientes-muse-r6/tic/entrega.json', 'R6 tic: 24 decisiones pendiente + requerido exacto.'),
    ('propuestas/pendientes-muse-r6/diversos-presas/entrega.json', 'R6 diversos-presas: 5 pendiente + 2 artefactos (filas 177/178).'),
    ('data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json', 'Verificacion independiente filas corruptas 177/178 (178 definiciones, encabezados como valores).'),
    ('reports/ronda-6.json', 'Cotejo: R6 resolvio 1 vinculo presas (columna), 0 significados; 171 siguen sin respaldo.'),
    (AUD_REL, 'Auditoria R6: 188 decisiones verificadas + ADV-SALUD-MANUAL y lineas alternativas; conteos 171=169+2.'),
]
for dicc in diccs:
    FUENTES_DEF.append((f'data/portal/inspecciones/{dicc}.json',
                        'Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).'))
fuentes = [{'localizador': rel, 'sha256': sha(rel), 'aplicabilidad': ap} for rel, ap in FUENTES_DEF]

tabla = [{'grupo_fuente': g, 'n': conteo_grupos.get(g, 0)} for g in ORDEN]
pend = {
    'tarea': 'tarea2: organizar los 169 significados reales sin documentacion suficiente tras R6',
    'generado_en_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'alcance': '171 significados pendientes R5 menos 2 filas corruptas excluidas solo de esta vista = 169 reales sin_documentacion_suficiente. R6 no resolvio ningun significado (1 vinculo de columna presas). Sin definiciones inventadas: donde el detalle por fila no consta, figura desconocido.',
    'nota_indices': 'Las citas textuales historicas R6 usan indice original 1-based (p. ej. definiciones[17] = fila 17) y se conservan como cita; los localizadores_verificados usan JSON pointer 0-based (/definiciones/16). Ver nota_indice_original por registro.',
    'nota_recursos': 'recurso_diccionario_id es el locator conocido del diccionario; recurso_de_datos distingue no_acreditado de citado_sin_vinculo:<uuid> (recurso mencionado en evidencia, sin correspondencia acreditada con columnas fisicas; no se inventa mapeo).',
    'conteo': len(significados),
    'porque_171_original_igual_169_reales_mas_2_corruptos': {
        'total_r5': 171, 'corruptas_excluidas_de_esta_vista': 2, 'reales_en_esta_vista': 169,
        'detalle_corruptas': 'Filas 177/178 del diccionario 33d0a99e-c721-496f-a05e-07646e9ae42a (Fiebre manchada): valores = nombres de encabezados (ide_id/ide_sex/ide_eda_ano/...); difieren solo en Ejemplo (ide_cp vs id_cp); catalogo des_mpo_res es posicion de columna, no referencia real. Verificado en inspeccion local, no solo en dictamen.',
        'quien_documenta_exclusion': 'otro agente (solo se listan aqui para cotejo en lista_ids_2_excluidos)'},
    'lista_ids_2_excluidos': [
        {'definicion_iri': EXCLUIDOS[0], 'variable': 'ide_id', 'fila': '177',
         'motivo': 'fila corrupta: repite la cabecera del diccionario como valores; catalogo_declarado des_mpo_res es posicion de columna, no referencia real',
         'verificacion_independiente': 'inspeccion local idx176: Nombre variable=ide_id, Tipo=ide_sex, Formato=ide_eda_ano, Ejemplo=ide_cp',
         'localizador_verificado': {'ruta': 'data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json',
                                    'sha256': sha('data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json'),
                                    'json_pointer': '/definiciones/176'}},
        {'definicion_iri': EXCLUIDOS[1], 'variable': 'ide_id', 'fila': '178',
         'motivo': 'fila corrupta gemela de la 177 (encabezados como valores, difiere solo en id_cp)',
         'verificacion_independiente': 'inspeccion local idx177: Nombre variable=ide_id, Tipo=ide_sex, Formato=ide_eda_ano, Ejemplo=id_cp',
         'localizador_verificado': {'ruta': 'data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json',
                                    'sha256': sha('data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json'),
                                    'json_pointer': '/definiciones/177'}},
    ],
    'tabla_resumen_por_fuente': tabla,
    'notas_grupo': NOTAS_GRUPO,
    'fuentes_json': fuentes,
    'verificacion': {
        'unicidad_iris_169': True, 'trazabilidad_todos_en_r5_171': True,
        'suma_grupos_igual_169': True, 'reales_mas_excluidos_igual_171': len(significados) + len(EXCLUIDOS) == 171,
        'conteo_grupos': dict(conteo_grupos), 'diccionarios_distintos_16': diccs,
        'r6_sin_significados_resueltos': True,
        'inspeccion_fila_variable_169_de_169': True},
    'significados': significados,
}

OUT.mkdir(parents=True, exist_ok=True)
pj = OUT / 'pendientes.json'
pj.write_bytes(json.dumps(pend, ensure_ascii=False, indent=2).encode('utf-8'))

L = []
L.append('# Significados sin documentacion suficiente tras R6: 169 reales')
L.append('')
L.append(f'Generado (UTC): {pend["generado_en_utc"]}')
L.append('')
L.append('171 originales R5 − 2 filas corruptas (excluidas solo de esta vista; otro agente documenta la exclusion) = **169 reales** con estado `sin_documentacion_suficiente`. R6 no resolvio ningun significado (solo 1 vinculo de columna presas). Sin definiciones inventadas: donde el detalle por fila no consta, figura `desconocido`.')
L.append('')
L.append('169+2=171 verificado: 169 IRIs unicos y trazables a R5 + 2 excluidos para cotejo. JSON UTF-8.')
L.append('')
L.append('**Indices**: las citas historicas R6 usan indice original 1-based (`definiciones[17]` = fila 17) y se conservan como cita; `localizadores_verificados` usa JSON pointer 0-based (`/definiciones/16`).')
L.append('')
L.append('**Recursos**: `recurso_diccionario_id` conocido (locator del diccionario); `recurso_de_datos` distingue `no_acreditado` de `citado_sin_vinculo:<uuid>` sin inventar mapeo a columnas de datos.')
L.append('')
L.append('## Resumen por grupo de fuente (6 grupos, suma 169; 16 diccionarios)')
L.append('')
L.append('| Grupo | n | Nota |')
L.append('| --- | ---: | --- |')
for ng in NOTAS_GRUPO:
    L.append(f'| {ng["grupo_fuente"]} | {ng["n"]} | {ng["nota"]} |')
L.append('| **Total** | **169** | |')
L.append('')
L.append('## 2 filas excluidas solo de esta vista (cotejo)')
L.append('')
for e in pend['lista_ids_2_excluidos']:
    lv = e['localizador_verificado']
    L.append(f'- `{e["definicion_iri"]}` fila {e["fila"]}: {e["motivo"]}. {e["verificacion_independiente"]}. Locator: `{lv["ruta"]}` `{lv["json_pointer"]}` sha `{lv["sha256"][:16]}…`.')
L.append('')
L.append('## Fuentes consultadas (SHA256 desde bytes)')
L.append('')
for f in fuentes:
    L.append(f'- `{f["localizador"]}` sha256 `{f["sha256"]}` — {f["aplicabilidad"]}')
L.append('')
for g in ORDEN:
    L.append(f'## Grupo {g} ({conteo_grupos.get(g, 0)})')
    L.append('')
    for x in [s for s in significados if s['grupo_fuente'] == g]:
        lv = x['localizadores_verificados']
        L.append(f'### {x["n"]}. {x["variable"]} — fila {x["fila"]}')
        L.append('')
        L.append(f'- IRI: `{x["definicion_iri"]}`')
        L.append(f'- Texto original: {x["descripcion_original"]}')
        L.append(f'- Localizacion: conjunto `{x["conjunto_id"]}` / diccionario `{x["diccionario_id"]}` / fila {x["fila"]} / huella `{x["huella_fila_diccionario"]}` / recurso_diccionario `{x["recurso_diccionario_id"]}` / recurso_datos `{x["recurso_de_datos"]}` / tabla-hoja `{x["tabla_hoja"]}` / pos-fisica `{x["posicion_fisica"]}` / catalogo declarado `{x["catalogo_declarado"]}`')
        L.append(f'- Localizadores verificados: R5 `{lv["r5_significado"]["json_pointer"]}` / inspeccion `{lv["inspeccion_fila"]["ruta"]}` `{lv["inspeccion_fila"]["json_pointer"]}` (variable OK) / auditoria `{lv["auditoria_dictamen"]["json_pointer"]}` ({lv["auditoria_dictamen"]["dictamen"]}) / confirma `{lv["entrega_r6_que_confirma"]}`')
        if x['nota_indice_original']:
            L.append(f'- Nota indice: {x["nota_indice_original"]}')
        for c in x['localizacion_r6'][:3]:
            L.append(f'  - cita: {c}')
        L.append(f'- Estado: `{x["estado"]}` (cobertura: `{x["estado_cobertura"]}`; rol R6: {x["rol_r6"]})')
        L.append(f'- Motivo R6: {x["dictamen_r6_motivo"]}')
        L.append(f'- Falta exacta: {x["evidencia_documental_exacta_faltante"]}')
        L.append(f'- Criterio futuro: {x["criterio_aceptacion_futura"]}')
        L.append('')
pm = OUT / 'pendientes.md'
pm.write_bytes('\n'.join(L).encode('utf-8'))

h_pend = hashlib.sha256(pj.read_bytes()).hexdigest()
h_md = hashlib.sha256(pm.read_bytes()).hexdigest()
lst = {
    'tarea': 'tarea2 significados post-R6 (v2: localizadores verificados)',
    'terminado_en_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'resumen': {'reales': 169, 'excluidos_vista': 2, 'origen_r5': 171,
                'reales_mas_excluidos': 169 + 2,
                'por_grupo': dict(conteo_grupos), 'diccionarios': 16, 'grupos': 6,
                'verificacion_ok': True},
    'archivos': [
        {'ruta': 'propuestas/depuracion-post-r6/significados/pendientes.json', 'sha256': h_pend},
        {'ruta': 'propuestas/depuracion-post-r6/significados/pendientes.md', 'sha256': h_md}],
    'fuentes_sha256': {f['localizador']: f['sha256'] for f in fuentes},
}
(OUT / 'listo.json').write_bytes(json.dumps(lst, ensure_ascii=False, indent=2).encode('utf-8'))
print('OK reales=%d grupos=%s diccs=%d' % (len(significados), dict(conteo_grupos), len(diccs)))
print('sha pendientes.json', h_pend)
print('sha pendientes.md', h_md)
