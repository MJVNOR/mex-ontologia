"""Registra la distribución autorizada entre chats sin modificar el núcleo."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
path = ROOT / 'docs/orquestacion-ronda-3.json'
data = json.loads(path.read_text(encoding='utf-8'))
data['estado'] = 'integracion_secuencial_entre_chats'
data['coordinacion'] = {
    'instruccion_usuario': 'Coordínate con «Revisar errores de la antología»: que integre la semántica; aquí termina chat, correspondencias y cruces.',
    'integrador_semantica': '01a1685c-0a24-76d0-89e8-776e71e02dbc',
    'integrador_chat_correspondencias_cruces': '01a1670e-26ce-76b0-9bf3-d1d731c8630d',
    'senal_relevo': 'propuestas/cobertura-muse-20261023/integrador/coordinacion.json',
    'condicion_relevo': 'semantica_lista == true',
    'no_escritura_central_hasta_relevo': True,
}
for entry in data['sesiones']:
    agent = entry['agente']
    if agent in (4, 6, 7, 8, 9, 10, 11, 12):
        entry['coordinador_actual'] = data['coordinacion']['integrador_semantica']
        entry['nota'] = 'Nueva fase de cobertura; entregas de ronda 3 conservadas.'
    else:
        entry['coordinador_actual'] = data['coordinacion']['integrador_chat_correspondencias_cruces']
    if agent == 1:
        entry['estado_revision'] = 'instalado_con_respaldo; respuesta_ui_no_probada'
    if agent in (2, 5):
        entry['estado_revision'] = 'aprobada; preparacion_aislada_hasta_relevo'
if not any(e['agente'] == 13 for e in data['sesiones']):
    data['sesiones'].append({
        'agente': 13, 'sessionId': 'ses_e97998776ffeJNk5fWPTkgTWLW',
        'carpeta': 'propuestas/ronda-3/agente-13-calificadores',
        'estado_revision': 'staging_rebasado; patch_duplicado_no_aplicado',
        'coordinador_actual': data['coordinacion']['integrador_semantica'],
    })
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Coordinación registrada; 13 sesiones; núcleo sin modificar.')
