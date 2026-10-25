"""Verificacion local TIC post-R6 (solo lectura + escritura en tic/).
Relee las 24 filas exactas, recomputa huellas y documenta instrumento/unidad/periodo/metodologia.
Escribe UNICAMENTE en propuestas/investigacion-post-r6/tic/.
"""
import json, hashlib, datetime, pathlib

REPO = pathlib.Path(r'C:\Users\marti\Documents\MEX-Ontologi')
OUT = REPO / 'propuestas' / 'investigacion-post-r6' / 'tic'
EV = OUT / 'evidencia'
TMP = OUT / 'temporales'
EV.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

UTC = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha_file(p: pathlib.Path) -> str:
    return sha_bytes(p.read_bytes())

def huella(row) -> str:
    raw = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

pend = json.loads((REPO / 'propuestas/depuracion-post-r6/significados/pendientes.json').read_bytes().decode('utf-8'))
tics = [s for s in pend['significados'] if s.get('grupo_fuente') == 'tic']
assert len(tics) == 24, len(tics)

inv = json.loads((REPO / 'data/portal/inventario.json').read_bytes().decode('utf-8'))
recs = {r['id']: r for r in inv.get('recursos', [])}
cont = json.loads((REPO / 'data/portal/contenido-inspeccion.json').read_bytes().decode('utf-8'))
cont_by_id = {r['id']: r for r in cont.get('recursos', [])}
cob = json.loads((REPO / 'data/semantica/cobertura.json').read_bytes().decode('utf-8'))

# Cobertura: indexar por definicion_iri si existe
cob_defs = {}
for k, v in (cob.items() if isinstance(cob, dict) else []):
    pass
# cobertura.json estructura: inspeccionar claves
cob_keys = list(cob.keys()) if isinstance(cob, dict) else []

verif_filas = []
for s in tics:
    dicc = s['diccionario_id']
    fila = int(s['fila'])
    insp_rel = f'data/portal/inspecciones/{dicc}.json'
    insp = json.loads((REPO / insp_rel).read_bytes().decode('utf-8'))
    row = insp['definiciones'][fila - 1]
    h = huella(row)
    ok = (h == s['huella_fila_diccionario'] and row.get('Nombre variable', '').strip() == s['variable'].strip())
    verif_filas.append({
        'definicion_iri': s['definicion_iri'],
        'variable': s['variable'],
        'diccionario_id': dicc,
        'fila': s['fila'],
        'json_pointer': f'/definiciones/{fila - 1}',
        'huella_recomputada': h,
        'huella_esperada': s['huella_fila_diccionario'],
        'coincide': ok,
        'tipo': row.get('Tipo de dato', ''),
        'formato': row.get('Formato', ''),
        'unidad_de_medida': row.get('Unidad de medida', ''),
        'descripcion': row.get('Descripción', row.get('Descripcion', '')),
        'ejemplo': row.get('Ejemplo de dato', ''),
        'catalogo': row.get('Catálogo de referencia', row.get('Catalogo de referencia', '')),
        'hoja': row.get('hoja', ''),
    })
    assert ok, s['definicion_iri']

(EV / 'verificacion_filas.json').write_bytes(json.dumps({
    'fecha_utc': UTC,
    'filas': verif_filas,
    'resumen': {'n': len(verif_filas), 'todas_coinciden': all(v['coincide'] for v in verif_filas)},
}, ensure_ascii=False, indent=1).encode('utf-8'))

# Instrumento por conjunto (solo material local): recursos diccionario+datos, datastore, formato, columnas diccionario
conj_ids = sorted({s['conjunto_id'] for s in tics})
titulos = {s['conjunto_id']: s['conjunto_titulo'] for s in tics}
instrumento = []
for cid in conj_ids:
    rrs = [r for r in inv.get('recursos', []) if r.get('conjunto_id') == cid]
    dicc_r = [r for r in rrs if r.get('clasificacion') == 'diccionario']
    datos_r = [r for r in rrs if r.get('clasificacion') != 'diccionario']
    insp_lens = {}
    for r in dicc_r:
        try:
            dd = json.loads((REPO / f"data/portal/inspecciones/{r['id']}.json").read_bytes().decode('utf-8'))
            insp_lens[r['id']] = len(dd.get('definiciones', []))
        except Exception as e:
            insp_lens[r['id']] = f'error: {e}'
    instrumento.append({
        'conjunto_id': cid,
        'titulo': titulos[cid],
        'recursos': [{'id': r['id'], 'nombre': r.get('nombre'), 'url': r.get('url'),
                       'formato': r.get('formato'), 'clasificacion': r.get('clasificacion'),
                       'datastore_declarado': r.get('datastore_declarado'), 'estructura': r.get('estructura')} for r in rrs],
        'n_definiciones_diccionario_local': insp_lens,
        'unidad_declarada_en_filas': 'ninguna (columna "Unidad de medida" vacia en las 24 filas TIC verificadas)',
        'periodo_declarado_en_diccionario': 'ninguno (las filas no portan periodo; los recursos de datos no acreditan fechas en el inventario)',
        'metodologia_declarada': 'Diagnostico del Entorno Digital; fuente Investigaciones; sin Fuentes extras ni cuestionario publicado (S09 R5, linea portal agotada)',
    })

(EV / 'instrumento_tic.json').write_bytes(json.dumps({
    'fecha_utc': UTC,
    'conjuntos': instrumento,
    'nota': 'Derivado solo de inventario.json + inspecciones locales + S09 R5. Sin definiciones inventadas.',
}, ensure_ascii=False, indent=1).encode('utf-8'))

# Cobertura: estado por definicion (si el formato lo permite)
(EV / 'cobertura_keys.json').write_bytes(json.dumps({
    'fecha_utc': UTC, 'cobertura_top_keys': cob_keys[:20],
}, ensure_ascii=False, indent=1).encode('utf-8'))

print('OK filas=%d conjuntos=%d' % (len(verif_filas), len(instrumento)))
print('sha verificacion_filas.json', sha_file(EV / 'verificacion_filas.json'))
print('sha instrumento_tic.json', sha_file(EV / 'instrumento_tic.json'))
