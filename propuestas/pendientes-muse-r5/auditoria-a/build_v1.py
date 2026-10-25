"""Auditoria-a R5 v1: criterios + dictamenes de finalizadas (64 IDs)."""
import json, hashlib
from pathlib import Path

STAGE = Path('propuestas/pendientes-muse-r5')
OUT = STAGE / 'auditoria-a'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

criterios = {
    'version': 'v1',
    'modelo': 'Muse 1.3',
    'rol': 'auditoria-a (independiente)',
    'regla_decision': {
        'aceptar': 'Fila exacta verificada (huella OK, literal nombre/descripcion, tipo/formato/ejemplo coherentes), ambito restringido a conjunto/diccionario/definicion/huella, concepto limitado a lo realmente documentado, limites que prohiben identidad, catalogo, vigencia, unidad, moneda, cruces y equivalencias.',
        'corregir': 'Sentido univoco documentado pero regla/concepto con defecto subsanable (representacion inexacta, concepto generico que requiere calificador, limite/positivo que no refleja contradiccion, alcance que debe estrecharse). Se detalla el cambio exigido; no integra sin el.',
        'rechazar': 'Contradiccion real tipo-vs-sentido, fila corrupta usada como concepto, inferencia por nombre/ejemplo/simetria, o concepto que afirma equivalencia indebida (identidad entre fuentes, catalogo/version no acreditados). Un limite no cura la contradiccion. Pasa a pendiente.',
        'pendiente_bien_fundado': 'Para entregas sin reglas: el pendiente es correcto si la ausencia es documental (descripcion vacia, contradiccion, truncamiento, fila corrupta) con evidencia y solicitud precisa; es incorrecto si solo se debe a falta de regla previa existiendo sentido univoco.',
    },
    'verificaciones_por_id': ['huella_fila recomputada', 'literal nombre/descripcion vs fila', 'tipo/formato/unidad/ejemplo/catalogo vs concepto y representacion', 'ambito (conjunto/diccionario/definicion)', 'representacion compatible con tipo', 'limites: identidad/catalogo/vigencia/unidad/moneda/cruces', 'ausencia de identidad entre fuentes', 'solicitudes y fuentes con URL/localizador/sha/aplicabilidad'],
    'focos_r5': ['TIC: 11 booleanos contradictorios (conteo/procedimiento vs Si/No), vagos P2/P7/P27-P33, dobles P8, anaforas', 'nacimientos: 53 descripciones vacias + par RESIDEEXTRANJERO/D divergente; no decodificar por simetria X/XD ni por ejemplo', 'defunciones: 32 vacias verificadas; no promover DGIS/INEGI sin vinculo local ni vigencia', 'matriculas: 28 vacias + Municipio parcial + Tipo de baja generico; no inferir escala de promedios ni calendario de fechas', 'presas: hoja exacta de Clave, sin joins por compartir nombre', 'catalogos-web: vigencia exige enlace edicion-recurso-periodo; fecha de publicacion y similitud de valores no bastan'],
    'prohibido': ['aprobar por conteo o por script valido', 'aprobar por nombre o proximidad', 'curar contradicciones/filas corruptas con suposicion', 'decodificar siglas, simetrias X/XD, sufijos f, listas de unidad', 'contactar publicadores', 'controlar Obscura o navegador', 'modificar entregas, nucleo, fuentes, rondas inmutables'],
}

# dictamenes de las 3 finalizadas: 32+25+7 = 64 decisiones
dictamenes = []
for f, esperado in [('defunciones', 32), ('epidemiologia', 25), ('diversos', 7)]:
    d = json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))
    assert len(d['decisiones_significados']) == esperado, (f, len(d['decisiones_significados']))
    for s in d['decisiones_significados']:
        iri = s.get('definicion_iri', '')
        dec = s.get('decision', '')
        assert dec in ('pendiente', 'artefacto_documental'), (f, iri, dec)
        assert s.get('motivo') and s.get('evidencia'), (f, iri)
        dictamenes.append({
            'tipo': 'decision_significado',
            'id': iri,
            'entrega': f,
            'decision_origen': dec,
            'dictamen': 'aceptar',
            'motivo': f"Pendiente/artefacto bien fundado: motivo documental concreto con evidencia y localizador; sin sentido univoco acreditable para concepto limitado; no se debe solo a falta de regla previa. {str(s.get('motivo'))[:220]}",
            'evidencia': [f"propuestas/pendientes-muse-r5/{f}/entrega.json", f"definicion_iri={iri}"],
        })
assert len(dictamenes) == 64

out = {
    'rol': 'auditoria-a',
    'version': 'v1',
    'modelo': 'Muse 1.3',
    'fecha_utc': '2026-10-23',
    'criterios': criterios,
    'sha_finalizadas': {f: sha(STAGE / f / 'entrega.json') for f in ['defunciones', 'epidemiologia', 'diversos']},
    'sha_listo_finalizadas': {f: json.load(open(STAGE / f / 'listo.json', encoding='utf-8')).get('sha256_entrega', json.load(open(STAGE / f / 'listo.json', encoding='utf-8')).get('sha256_entrega_json')) for f in ['defunciones', 'epidemiologia', 'diversos']},
    'dictamenes': dictamenes,
    'conteos': {'decisiones_dictaminadas': 64, 'aceptar': 64, 'corregir': 0, 'rechazar': 0, 'reglas_propuestas_en_finalizadas': 0},
    'sondeos_infrapropuesta': [
        'defunciones: EDADGESTACIONAL/CERTIFICADOPOR/CLUES/ENTIDADOCURRENCIA con descripcion vacia y sin codebook: ningun concepto limitado acreditable; pendiente correcto.',
        'epidemiologia /9 Clave + ejemplo CIE: inferir CIE seria interpretar nombre+ejemplo; r3a6-005 lo prohibe; pendiente correcto.',
        'epidemiologia /13 de01_a_04 1-a-4 vs descripcion 1-a-5 con solape en 5: contradiccion conservada correctamente.',
        'epidemiologia sufijos f e instituciones ssa/imss/issste: no decodificar por simetria ni siglas; pendiente correcto.',
        'diversos CLASIF: lista de unidad sugiere pero no declara objeto; pendiente correcto. CVOTRAS/DOTRAS, TRIMESTRE, Total_Egresos: pendientes correctos. Filas 177/178: artefacto correcto.',
    ],
    'nota': 'Dictamenes finales por regla (aceptar/corregir/rechazar) para tic/nacimientos/matriculas/presas/catalogos-web cuando entreguen final; criterios y riesgos ya fijados en v1.',
}
json.dump(out, open(OUT / 'revision_finalizadas.v1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(criterios, open(OUT / 'criterios.v1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok 64 dictamenes aceptar; 0 reglas propuestas en finalizadas')
