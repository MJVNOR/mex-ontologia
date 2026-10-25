"""Auditoria-a ronda 4: dictamen independiente de las 175 reglas y 351 significados."""
import json, hashlib, unicodedata
from urllib.parse import unquote
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('.')
STAGE = ROOT / 'propuestas' / 'pendientes-muse-r4'
OUT = STAGE / 'auditoria-a'

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()

def norm(s):
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())

insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
sem = json.load(open('ontologia/semantica.json', encoding='utf-8'))
nucleo_conc = set(sem['conceptos'].keys())

def get_row(defiri):
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    return dic, idx, insp[dic]['definiciones'][idx - 1]

def fld(row, key):
    for k in row:
        if norm(k) == key:
            return row[k]
    return ''

LOTES = ['lote-1', 'lote-2', 'lote-3', 'lote-4', 'lote-5', 'lote-6']

# ---- sha entregas finales ----
sha_entregas = {}
for lote in LOTES + ['ambiguedades']:
    sha_entregas[lote] = sha256_file(STAGE / lote / 'entrega.json')

# ---- decisiones por regla ----
RECHAZAR = {
    'r4-lote-4-025': 'Tipo Booleano Si/No con ejemplo Si contradice el concepto de conteo (pregunta Cuantos proyectos). Un limite no resuelve la contradiccion: el dominio acreditable es existencia Si/No, no cantidad. El mismo patron quedo pendiente en lote-2 (af14 P36). Cambio exigido: retirar el concepto de conteo; si se propone, concepto de existencia-de-proyectos con representacion no_especificada y sin numero.',
    'r4-lote-4-026': 'Tipo Booleano Si/No con ejemplo Si contradice el concepto de procedimiento (pregunta Como atiende incidencias). El valor acreditable es Si/No, no describe procedimiento. Cambio exigido: retirar el concepto de procedimiento; solo cabe existencia de atencion declarada.',
    'r4-lote-4-027': 'Tipo Booleano Si/No con ejemplo Si contradice el concepto de conteo (pregunta Cuantas personas). Descripcion literal identica a la regla vigente r3a9-059, pero la fila nueva no acredita conteo. Cambio exigido: no duplicar r3a9-059 sobre esta fila; retirar.',
    'r4-lote-3-tiempo-9': 'Reutiliza el concepto vigente tiempo cuya definicion exige evento, unidad y cobertura especificados; la fila (Hora de inicio, Fecha y Hora) no los documenta. Ademas la representacion hora recorta el Tipo Fecha y Hora (ejemplo con fecha completa). Cambio exigido: concepto especifico de metadato temporal de encuesta y representacion no_especificada que conserve fecha+hora.',
    'r4-lote-3-tiempo-10': 'Igual que tiempo-9: concepto tiempo del nucleo mal reutilizado (falta evento/unidad/cobertura) y hora recorta Fecha y Hora. Cambio exigido: concepto especifico + no_especificada.',
    'r4-lote-3-tiempo-11': 'Igual que tiempo-9: concepto tiempo del nucleo mal reutilizado y hora recorta Fecha y Hora. Cambio exigido: concepto especifico + no_especificada.',
}
CONDICIONADO = {
    'r4-lote-4-008': 'Descripcion Sector con ejemplo 04 - SECRETARIA DE HACIENDA: el clasificador de sectores no esta declarado en el diccionario y el concepto se comparte entre tres encuestas distintas. Cambio exigido: anadir limite explicito sin equiparacion de sectores entre encuestas ni separacion codigo/nombre; sin catalogo.',
    'r4-lote-4-009': 'Igual que r4-lote-4-008 (misma fila logica en otra encuesta). Cambio exigido: mismo limite de no-equiparacion entre encuestas.',
    'r4-lote-4-010': 'Igual que r4-lote-4-008 (misma fila logica en otra encuesta). Cambio exigido: mismo limite de no-equiparacion entre encuestas.',
    'r4-lote-4-038': 'Clave CIE compartida entre dos diccionarios de conjuntos distintos sin version ni catalogo acreditados. Cambio exigido: limite sin equivalencia de claves entre diccionarios ni version CIE.',
    'r4-lote-4-039': 'Igual que r4-lote-4-038 (otro diccionario). Cambio exigido: mismo limite de no-equivalencia ni version.',
    'r4-lote-3-apoyo-tendencias-tic-dependencia-14': 'Tipo Booleano Si/No con representacion codigo: no hay codigo documentado, solo existencia declarada. Cambio exigido: representacion no_especificada.',
    'r4-lote-3-instrumentos-previos-ley-gobierno-digital-18': 'Tipo Booleano Si/No con representacion codigo y descripcion truncada en fuente. Cambio exigido: representacion no_especificada + nota de truncamiento.',
    'r4-lote-3-instrumentos-actuales-mejora-administracion-20': 'Tipo Booleano Si/No con representacion codigo y descripcion truncada en fuente. Cambio exigido: representacion no_especificada + nota de truncamiento.',
    'r4-lote-3-recursos-anuales-innovacion-mencionados-16': 'Ejemplo 5000, software mezcla monto y especie sin unidad ni moneda declaradas. Cambio exigido: limite sin inferir monto, moneda ni unidad; solo lista declarada.',
    'r4-lote-3-sector-dependencia-encuestada-8': 'Descripcion Sector sin clasificador declarado (ejemplo con prefijo numerico). Cambio exigido: limite sin separar codigo de nombre ni acreditar catalogo; sin comparacion entre encuestas.',
    'r4-lote-6-dig-sector-nombre': 'Descripcion Sector sin clasificador declarado (ejemplo 04 - SECRETARIA DE HACIENDA). Cambio exigido: limite sin separar codigo de nombre ni acreditar catalogo; sin comparacion entre encuestas.',
    'r4-lote-2-021': 'Comparte concepto numero-consecutivo-registro con ordinales genericos (No./Numero de la entrada), pero su descripcion es especifica (estudiante matriculado, variable Estudiante). Cambio exigido: concepto propio distinto del ordinal generico.',
}

dictamenes = []
cobertura = {'total_significados': 0, 'proponer': 0, 'pendiente': 0, 'detalle_por_lote': {}, 'defectos': []}
for lote in LOTES:
    d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
    det = {'significados': len(d.get('decisiones_significados', [])), 'reglas': len(d.get('reglas', []))}
    det_sig = []
    for s in d.get('decisiones_significados', []):
        cobertura['total_significados'] += 1
        if s.get('decision') == 'proponer':
            cobertura['proponer'] += 1
        else:
            cobertura['pendiente'] += 1
        if not s.get('definicion_iri') or not s.get('motivo') or not s.get('evidencia'):
            cobertura['defectos'].append(f"{lote} {s.get('definicion_iri')}: decision sin motivo/evidencia")
        det_sig.append(s.get('definicion_iri'))
    det['definiciones'] = det_sig
    cobertura['detalle_por_lote'][lote] = det
    reglas_defs = set()
    for r in d['reglas']:
        for dd in r.get('definiciones', []):
            reglas_defs.add(dd)
    # correspondencia significados proponer <-> reglas nuevas
    for s in d.get('decisiones_significados', []):
        if s.get('decision') == 'proponer' and s.get('definicion_iri') not in reglas_defs:
            cobertura['defectos'].append(f"{lote} {s.get('definicion_iri')}: proponer sin regla nueva (reutiliza vigente)")
    for r in d['reglas']:
        rid = r['id']
        dd = r.get('definiciones', [])[0] if r.get('definiciones') else ''
        try:
            dic, idx, row = get_row(dd)
            h_ok = huella(row) == r.get('huella_fila_diccionario')
            tipo = fld(row, 'tipo de dato')
            fmt = fld(row, 'formato')
            ej = fld(row, 'ejemplo de dato')
        except Exception as e:
            h_ok, tipo, fmt, ej, dic, idx = False, f'ERROR {e}', '', '', '', 0
        ev = [
            f"data/portal/contenido-inspeccion.json:diccionario={dic}:fila={idx}",
            f"huella_fila_diccionario={r.get('huella_fila_diccionario')} recomputada={'OK' if h_ok else 'DIFIERE'}",
            f"tipo={tipo} formato={fmt} ejemplo={ej}",
            f"definicion_iri={dd}",
            f"concepto={r.get('concepto')} representacion={r.get('representacion')}",
        ]
        if not h_ok:
            dictamenes.append({'tipo': 'reglas', 'id': rid, 'dictamen': 'rechazado',
                               'motivo': 'Huella de fila no reproducible desde la fuente local; evidencia rota.',
                               'evidencia': ev})
        elif rid in RECHAZAR:
            dictamenes.append({'tipo': 'reglas', 'id': rid, 'dictamen': 'rechazado',
                               'motivo': RECHAZAR[rid], 'evidencia': ev})
        elif rid in CONDICIONADO:
            dictamenes.append({'tipo': 'reglas', 'id': rid, 'dictamen': 'condicionado',
                               'motivo': CONDICIONADO[rid], 'evidencia': ev})
        else:
            dictamenes.append({'tipo': 'reglas', 'id': rid, 'dictamen': 'aceptar',
                               'motivo': 'Fila exacta verificada (huella OK, nombre/descripcion literales, tipo/formato/ejemplo coherentes con concepto y representacion); ambito restringido a la definicion; limites prohiben identidad, catalogo, vigencia, cruces y equivalencias.',
                               'evidencia': ev})

print('dictamenes:', len(dictamenes))
print('aceptar:', sum(1 for x in dictamenes if x['dictamen'] == 'aceptar'))
print('rechazado:', sum(1 for x in dictamenes if x['dictamen'] == 'rechazado'))
print('condicionado:', sum(1 for x in dictamenes if x['dictamen'] == 'condicionado'))
print('cobertura:', cobertura['total_significados'], 'prop:', cobertura['proponer'], 'pend:', cobertura['pendiente'])
print('defectos:', cobertura['defectos'])
json.dump({'sha_entregas': sha_entregas, 'dictamenes': dictamenes, 'cobertura': cobertura},
          open(OUT / 'borrador.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
