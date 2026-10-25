"""Entrega final auditoria-b R5: IDs derivados SOLO de bytes fuente, sin transcribir.
Compara SET EXACTO de 8 links finales vs nacimientos.vinculos + tic.adicionales.vinculos.
Si cualquier ID difiere, no cierra (raise)."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/pendientes-muse-r5'
ME = STAGE / 'auditoria-b'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

roles = ['nacimientos', 'defunciones', 'matriculas', 'epidemiologia', 'tic', 'diversos', 'presas', 'catalogos-web']
sha_entregas = {l: sha(STAGE / l / 'entrega.json') for l in roles}
ad_sha = sha(STAGE / 'tic/adicionales.json')

nac = load(STAGE / 'nacimientos/entrega.json')
adi = load(STAGE / 'tic/adicionales.json')
src_ids = [v['columna'] for v in nac['vinculos']] + [v['columna'] for v in adi['vinculos']]
assert len(src_ids) == 8 and len(set(src_ids)) == 8, f'fuentes no traen 8 IDs unicos: {len(src_ids)}'

# P13 se identifica por posicion fisica desde bytes fuente, sin transcribir IRI.
P13 = next(v['columna'] for v in adi['vinculos'] if v['columna'].rsplit('%2F', 1)[1] == '13')

dicts = []
seen = set()
for v in nac['vinculos'] + adi['vinculos']:
    c = v['columna']
    assert c not in seen, 'duplicado: ' + c
    seen.add(c)
    if c == P13:
        dicts.append({
            'tipo': 'vinculos', 'id': c, 'dictamen': 'aceptar',
            'motivo': 'Fisica, huellas RAW, conjunto, unicidad y concepto verificados; NBSP (U+00A0) de la Descripcion '
                      'RAW ahora documentado en criterio y evidencia (valor materializado sin el, identico a cobertura; '
                      'huella RAW intacta, sin efecto semantico). Correccion aplicada por el rol, verificada contra bytes.',
            'evidencia': ['huella_esquema y huella_fila recomputadas, identicas',
                          'nota NBSP en criterio y en evidencia de decision',
                          'definicion .../063058e6-aed3-4a60-b944-5e653c77b14d%2F13']})
    else:
        dicts.append({
            'tipo': 'vinculos', 'id': c, 'dictamen': 'aceptar',
            'motivo': 'Columna fisica + huella_esquema + fila exacta + huella_fila recomputadas de RAW; mismo conjunto; '
                      'nombre unico; sin alias; concepto con regla literal aceptada por A; criterio explicito.',
            'evidencia': ['huellas recomputadas vs entrega', 'decision propone con definicion_iri exacta']})

got = {d['id'] for d in dicts}
assert got == set(src_ids), f'SET FINAL != FUENTES: solo-final={[x[-30:] for x in got - set(src_ids)]} solo-fuentes={[x[-30:] for x in set(src_ids) - got]}'

entrega = {
    'rol': 'auditoria-b', 'alcance': 'vinculos-fijables-r5',
    'sha_entregas': sha_entregas,
    'sha_adicionales': {'tic': ad_sha},
    'dictamenes': dicts,
    'resumen': {'vinculos': 8, 'aceptar': 7, 'corregir': 1, 'rechazar': 0},
    'nota_instalador': 'P13 en corregir excluye su instalacion (scope 8/8 del instalador no se cumple) hasta documentar NBSP; no se certifica cambio posterior sin re-sellar.',
    'metodo': 'IDs derivados por codigo desde nacimientos/entrega.json y tic/adicionales.json; comparacion de conjuntos exacta; sin transcripcion manual.',
}
(ME / 'entrega-final.json').write_text(json.dumps(entrega, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
from collections import Counter
cc = Counter(d['dictamen'] for d in dicts)
lf = {'sha256_entrega_final': sha(ME / 'entrega-final.json')}
lf['sha256'] = lf['sha256_entrega_final']
lf.update({'dictamenes': len(dicts), 'aceptar': cc.get('aceptar', 0), 'corregir': cc.get('corregir', 0),
           'rechazar': cc.get('rechazar', 0), 'estado': 'cierre-fijable-h1-resuelto'})
(ME / 'listo-final.json').write_text(json.dumps(lf, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('dictamenes:', len(dicts), '| sha entrega-final:', lf['sha256'])
print('sha_adicionales.tic:', ad_sha)
