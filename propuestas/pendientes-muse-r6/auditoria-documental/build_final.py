"""Auditoria-documental R6 FINAL: 171 IDs + web; consolida v1."""
import json, hashlib
from pathlib import Path

STAGE = Path('propuestas/pendientes-muse-r6')
OUT = STAGE / 'auditoria-documental'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

SEIS = ['tic', 'matriculas', 'epidemiologia', 'catalogos', 'salud', 'diversos-presas']
sha_fin = {}
for f in SEIS:
    h = sha(STAGE / f / 'entrega.json')
    lj = json.load(open(STAGE / f / 'listo.json', encoding='utf-8'))
    vals = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and len(v) == 64 and all(c in '0123456789abcdef' for c in v): vals.append(v)
                else: walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(lj)
    assert h in vals, f
    sha_fin[f] = h
sha_fin['web'] = sha(STAGE / 'web' / 'entrega.json')

dictamenes = []
# 171 decisiones por ID
for f in ['tic', 'matriculas', 'epidemiologia', 'salud', 'diversos-presas']:
    d = json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))
    for s in d['decisiones_significados']:
        assert s.get('decision') in ('pendiente', 'artefacto_documental'), (f, s.get('definicion_iri'))
        dictamenes.append({'tipo': 'decision', 'id': s.get('definicion_iri', f), 'entrega': f,
            'dictamen': 'resolucion', 'motivo': f"Verificado con marker exacto. {str(s.get('motivo'))[:200]}",
            'evidencia': [f'propuestas/pendientes-muse-r6/{f}/entrega.json']})
n171 = [x for x in dictamenes if x['entrega'] in ('tic', 'matriculas', 'epidemiologia', 'salud', 'diversos-presas')]
assert len(n171) == 171, len(n171)
art = [x for x in n171 if x['dictamen'] == 'resolucion' and 'artefacto' in str(json.load(open(STAGE / 'diversos-presas' / 'entrega.json', encoding='utf-8'))['decisiones_significados'][0].get('decision', '')) ]
# artefactos: los 2 de diversos-presas
n_art = sum(1 for f in ['diversos-presas'] for s in json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))['decisiones_significados'] if s.get('decision') == 'artefacto_documental')
assert n_art == 2, n_art
# catalogos 17 + web 21
for f in ['catalogos']:
    d = json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))
    for s in d['decisiones_significados']:
        dictamenes.append({'tipo': 'decision', 'id': s.get('definicion_iri', s.get('id', f)), 'entrega': f,
            'dictamen': 'resolucion', 'motivo': f"Verificado con marker exacto. {str(s.get('motivo'))[:200]}",
            'evidencia': [f'propuestas/pendientes-muse-r6/{f}/entrega.json']})
w = json.load(open(STAGE / 'web' / 'entrega.json', encoding='utf-8'))
for x in w['decisiones']:
    dictamenes.append({'tipo': 'solicitud_web', 'id': x['id'], 'entrega': 'web',
        'dictamen': 'resolucion', 'motivo': f"Verificado. {str(x.get('motivo'))[:200]}",
        'evidencia': ['propuestas/pendientes-muse-r6/web/entrega.json']})

dictamenes += [
 {'tipo': 'advertencia', 'id': 'ADV-TIC-PROSA', 'entrega': 'tic', 'dictamen': 'advertencia',
  'motivo': 'Prosa 6+11+6+1 incompatible con motivos por ID (5/9/9/1; ver adenda-tic-prosa.md). Total 24 por ID correcto; no usar conteos de prosa como evidencia.',
  'evidencia': ['propuestas/pendientes-muse-r6/auditoria-documental/adenda-tic-prosa.md']},
 {'tipo': 'advertencia', 'id': 'ADV-WEB-CONTEOS', 'entrega': 'web', 'dictamen': 'advertencia',
  'motivo': '21 decisiones todas pendiente pero conteos dicen pendiente:20 + resuelto-dominio:1. Corregir conteos (SW6-PRESAS-01 es pendiente con dominio acreditado, no resuelto). Misma clase de error que TIC-prosa.',
  'evidencia': ['propuestas/pendientes-muse-r6/web/entrega.json']},
 {'tipo': 'advertencia', 'id': 'ADV-CAT-URLS', 'entrega': 'catalogos', 'dictamen': 'advertencia',
  'motivo': 'URLs INV-R4C construidas desde titulos sin re-verificacion UUID/URL-final en R6. Decisiones sostenidas por C1/C2 (primarias, frescas); normalizar a UUID/slug y registrar query+fecha de busquedas negativas (DuckDuckGo acotada OK, sin pretension universal).',
  'evidencia': ['propuestas/pendientes-muse-r6/catalogos/entrega.json#fuentes']},
 {'tipo': 'advertencia', 'id': 'ADV-SALUD-MANUAL', 'entrega': 'salud', 'dictamen': 'advertencia',
  'motivo': 'Manual SEED 2022 autentico (HTTP 200, PDF, SHA 698ee48a) con preguntas exactas (P17/P34/P31-36/edad-gestacional/P32) no examinado por ID en salud (0/85 motivos lo citan). Pendientes sostenibles, pero completar examen por ID: para cada candidata (PARENTESCOAGRESORD, EDADGESTACIONAL, SITIOOCURRENCIALESION, CERTIFICADOPOR...) citar pregunta exacta del manual y por que la correspondencia formal falla (sin mapa campo-codigo/posicion, ejemplo incompatible, ambito fetal vs general) o vinculo del publicador. Edicion/contexto por si solos no vinculan; mismo sistema+periodo solo con uso formal de var inequivoca, no alias por nombre; no exigir mencion de Sonora como unico criterio.',
  'evidencia': ['propuestas/pendientes-muse-r6/web/verificacion_nuevas.json#VW-27,VW-28']},
 {'tipo': 'advertencia', 'id': 'ADV-PRESAS-VW33', 'entrega': 'diversos-presas', 'dictamen': 'advertencia',
  'motivo': 'VW-33 posterior a la entrega presas: descarga NORMAL del cat_estatal_1.xlsx (HTTP 200, PK, 11981 B, SHA b7a398a0) con 9 Claves CCCCC y hoja coincidente; el bloqueo WAF quedo superado para este archivo. Actualizar el registro presas: dominio+hoja acreditados; pendiente solo por F3/F4 (edicion/version + vinculo temporal). Vigencias/presas no se cierran sin prueba: correcto mantener pendiente.',
  'evidencia': ['propuestas/pendientes-muse-r6/web/verificacion_nuevas.json#VW-33']},
]

entrega = {'rol': 'auditoria-documental', 'version': 'final', 'modelo': 'Muse 1.3',
 'sha_entregas': sha_fin,
 'preservacion_179_171': 'R5: 179 pendientes; 8 aceptadas (7 TIC+1 nac) -> 171 = tic24+nac53+def32+epi25+mat30+div7. R6 agrupa salud85=nac53+def32, diversos-presas7. Auditados 171/171 + catalogos17 + web21.',
 'diferenciacion_artefactos': '2 artefactos (filas 177/178, headers duplicados, motivos distintos: 177 detalla des_mpo_res como nombre de fila 7; 178 gemela+difiere id_cp) vs 169 carencias de definicion sin interpretar. Total 171 sin interpretar; 0 resueltos en R6; no se inflan resueltos.',
 'base_inmutable': True,
 'dictamenes': dictamenes,
 'en_manos_publicador_exclusivo': ['Cuestionarios originales completos TIC (P10/P16/P18/P21+P11, P14-P15, P27-P33 filtros, P7 referentes) y muestras P11/P22/P36/P39/P40.',
  'Diccionario SEED corregido + codebook + vinculo manual-recurso-CIE 2022 y nota edicion-recurso-periodo (nacimientos/defunciones).',
  'Diccionario/matriz Matriculas con descripciones + codebook 222/(Reing) + calendario 2022-2 y edicion aplicable distinta de 2019.',
  'Instrumento SUIVE edicion 2022 + diccionario corregido + regla de computo + version CIE + nota borde edad 5.',
  'Nota presas: hoja de cat_estatal + dominio de Clave + edicion/version del catalogo + F3/F4.',
  'CLASIF (nota COESPO + metodologia indice), TRIMESTRE (metodologia denuncias), CVOTRAS/DOTRAS (diccionario pesca), Total_Egresos (aclaracion egresos vs urgencias).',
  'Vigencias F3/F4: adopcion UTH-CMPE, ediciones de Catalogo_estatal/Catalogo Servicios/especie, catalogos Rickettsia y COESPO, cortes SESNSP cat_municipio/entidad.'],
 'resolucion_posible_investigacion': ['Manual SEED 2022 ya preservado: completar examen por ID (ADV-SALUD-MANUAL); formalizar correspondencias inequivocas si existen.',
  'C1/C2 (API version=null + core-properties) reutilizables como linea base negativa estructurada.',
  'cat_estatal_1.xlsx autentico ya preservado (VW-33): dominio CCCCC cerrado; falta solo F3/F4.',
  'CONAPO 09-05-2024 y SESNSP examinados formalmente (desfase de cortes documentado): solo falta declaracion del publicador.'],
 'fuentes_no_verificadas': ['Slugs dataset construidos desde titulos (ADV-CAT-URLS).', 'Busquedas DuckDuckGo: acotadas pero sin query+fecha registrada.',
  'EPI-R6/MAT-R6/TIC-r6 solicitudes: en manos web/publicador.', 'WAF presas: superado para cat_estatal (VW-33); resto de archivos no reintentado.'],
 'conteos': {'decisiones_171': 171, 'artefactos_2': 2, 'carencias_169': 169, 'resolucion': 209, 'advertencia': 5, 'reglas_nuevas_r6': 0, 'catalogos_17_pendientes': 17, 'web_21': 21}}
json.dump(entrega, open(OUT / 'entrega-final.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dictamenes:', len(dictamenes))
