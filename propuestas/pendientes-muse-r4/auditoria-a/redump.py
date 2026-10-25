import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r4')
WANT = {'r4-lote-2-021', 'r4-lote-3-sector-dependencia-encuestada-8', 'r4-lote-3-tiempo-9',
        'r4-lote-3-tiempo-10', 'r4-lote-3-tiempo-11',
        'r4-lote-3-apoyo-tendencias-tic-dependencia-14', 'r4-lote-3-recursos-anuales-innovacion-mencionados-16',
        'r4-lote-3-instrumentos-previos-ley-gobierno-digital-18', 'r4-lote-3-instrumentos-actuales-mejora-administracion-20',
        'r4-lote-4-002', 'r4-lote-4-003', 'r4-lote-4-004', 'r4-lote-4-008', 'r4-lote-4-009',
        'r4-lote-4-010', 'r4-lote-4-022', 'r4-lote-4-038', 'r4-lote-4-039', 'r4-lote-6-dig-sector-nombre'}
for lote in ['lote-2', 'lote-3', 'lote-4', 'lote-6']:
    d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
    for r in d['reglas']:
        if r['id'] in WANT:
            print('=' * 100)
            print(json.dumps(r, ensure_ascii=False, indent=1))
