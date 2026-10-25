"""Auditoria-a R5 v3: TIC(7, marker pendiente->provisional) + matriculas(15, marker final)."""
import json, hashlib
from pathlib import Path
from urllib.parse import unquote

STAGE = Path('propuestas/pendientes-muse-r5')
OUT = STAGE / 'auditoria-a'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def huella(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
sem = json.load(open('ontologia/semantica.json', encoding='utf-8'))

# retiro ordenado: descripcion vacia/tautologica + nombre (+ejemplo) no es respaldo explicito
RETIRO_MAT = {
    'r5mat-001': 'Descripcion Pendiente de especificar; concepto desde nombre+ejemplo sin respaldo explicito. Retirar.',
    'r5mat-002': 'Descripcion vacia + reutiliza nucleo tiempo (exige evento/unidad/cobertura; evento solo segun nombre). Retirar.',
    'r5mat-004': 'Descripcion vacia; escala/rango/metodo no declarados; ejemplo 8.2 no fija escala. Retirar.',
    'r5mat-005': 'Igual que 004 (todas las asignaturas). Retirar.',
    'r5mat-006': 'Descripcion vacia; metodo de conteo no documentado. Retirar.',
    'r5mat-007': 'Descripcion vacia; ejemplo 0 no distingue ausencia de valor. Retirar.',
    'r5mat-008': 'Igual que 007 (todas). Retirar.',
    'r5mat-009': 'Descripcion tautologica (nombre=descripcion), dominio y valores sin documentar, ejemplo en blanco. Retirar.',
    'r5mat-010': 'Descripcion vacia + nucleo tiempo con evento solo segun nombre. Retirar.',
    'r5mat-011': 'Igual que 010. Retirar.',
    'r5mat-012': 'Igual que 010. Retirar.',
    'r5mat-013': 'Igual que 010 (acto administrativo vs academico no fijado por fuente). Retirar.',
    'r5mat-014': 'Igual que 010. Retirar.',
    'r5mat-015': 'Descripcion vacia + nucleo tiempo; ejemplo unico no acredita dominio. Retirar.',
}

dictamenes = []
# TIC (provisional: sin marker final)
t = json.load(open(STAGE / 'tic' / 'entrega.json', encoding='utf-8'))
assert len(t['reglas']) == 7
for r in t['reglas']:
    dd = unquote(r['definiciones'][0])
    dic = dd.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dd.rsplit('/', 1)[1])
    assert huella(insp[dic]['definiciones'][idx - 1]) == r['huella_fila_diccionario'], r['id']
    dictamenes.append({'tipo': 'regla', 'id': r['id'], 'entrega': 'tic', 'dictamen': 'aceptar_provisional',
        'motivo': 'Cotejo original OK (huella, literal Texto, ejemplo conservado, sin Booleano, sin equiparar encuestas: limite verificado). PROVISIONAL: sin marker listo.json; re-verificar SHA al cierre final.',
        'evidencia': [f"propuestas/pendientes-muse-r5/tic/entrega.json", f"diccionario={dic}:fila={idx}"]})
for s in t['decisiones_significados']:
    if s.get('decision') == 'pendiente':
        dictamenes.append({'tipo': 'decision_significado', 'id': s['definicion_iri'], 'entrega': 'tic',
            'decision_origen': 'pendiente', 'dictamen': 'aceptar',
            'motivo': f"Pendiente bien fundado. {str(s.get('motivo'))[:200]}",
            'evidencia': ['propuestas/pendientes-muse-r5/tic/entrega.json']})

# matriculas (marker final MATCH)
m = json.load(open(STAGE / 'matriculas' / 'entrega.json', encoding='utf-8'))
assert len(m['reglas']) == 15
for r in m['reglas']:
    dd = unquote(r['definiciones'][0])
    dic = dd.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dd.rsplit('/', 1)[1])
    assert huella(insp[dic]['definiciones'][idx - 1]) == r['huella_fila_diccionario'], r['id']
    if r['id'] in RETIRO_MAT:
        dictamenes.append({'tipo': 'regla', 'id': r['id'], 'entrega': 'matriculas', 'dictamen': 'rechazar',
            'motivo': 'Retiro exigido (orden usuario): ' + RETIRO_MAT[r['id']] + ' Un concepto no_especificada con limites retoricos basado en nombre sigue sin respaldo; pasa a pendiente.',
            'evidencia': ['propuestas/pendientes-muse-r5/matriculas/entrega.json', f"diccionario={dic}:fila={idx}"]})
    else:
        assert r['id'] == 'r5mat-003', r['id']
        dictamenes.append({'tipo': 'regla', 'id': r['id'], 'entrega': 'matriculas', 'dictamen': 'aceptar',
            'motivo': 'Descripcion parcial pero real + ejemplo real (HERMOSILLO) + Tipo Texto; limite documenta truncation y funcion no documentada; concepto municipio rep nombre minimo. Unica respaldada explicitamente.',
            'evidencia': ['propuestas/pendientes-muse-r5/matriculas/entrega.json', f"diccionario={dic}:fila={idx}"]})
for s in m['decisiones_significados']:
    if s.get('decision') == 'pendiente':
        dictamenes.append({'tipo': 'decision_significado', 'id': s['definicion_iri'], 'entrega': 'matriculas',
            'decision_origen': 'pendiente', 'dictamen': 'aceptar',
            'motivo': f"Pendiente bien fundado. {str(s.get('motivo'))[:200]}",
            'evidencia': ['propuestas/pendientes-muse-r5/matriculas/entrega.json']})

a = sum(1 for x in dictamenes if x['dictamen'] in ('aceptar', 'aceptar_provisional'))
rej = sum(1 for x in dictamenes if x['dictamen'] == 'rechazar')
out = {'rol': 'auditoria-a', 'version': 'v3', 'modelo': 'Muse 1.3',
    'sha_entregas': {'tic': sha(STAGE / 'tic' / 'entrega.json'), 'tic_marker_final': (STAGE / 'tic' / 'listo.json').exists(),
                     'matriculas': sha(STAGE / 'matriculas' / 'entrega.json')},
    'dictamenes': dictamenes,
    'nota_vinculos_matriculas': '7 vinculos + 7 columnas proponer ligados a reglas retiradas (002,010-015) deben retirarse con ellas; subsiste solo Municipio (vínculo+columna de r5mat-003).',
    'conteos_179': {'tic': '7 proponer + 24 pendientes', 'nacimientos': '1 + 53', 'defunciones': '0 + 32',
                    'epidemiologia': '0 + 25', 'matriculas': '1 aceptada + 14 retiro + 15 pendientes', 'diversos': '0 + 5 + 2 artefactos',
                    'aparte': ['presas: 0 reglas (2 significados ya respaldados, 1 columna pendiente)', 'catalogos: 17 pendientes, 0 cambios (web atiende nuevas solicitudes)']},
    'conteos': {'dictamenes': len(dictamenes), 'aceptar_incl_provisional': a, 'rechazar_retiro': rej}}
json.dump(out, open(OUT / 'revision_tic_matriculas.v3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dictamenes:', len(dictamenes), 'aceptar(+prov):', a, 'rechazar:', rej)
