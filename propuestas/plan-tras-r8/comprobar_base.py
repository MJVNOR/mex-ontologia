"""Verifica la base y el respaldo R8 antes de instalar la siguiente ronda."""
from pathlib import Path
import hashlib
import json
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'propuestas/plan-tras-r8/ejecucion-20261024'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

if __name__ == '__main__':
    dest = E / 'comprobacion-base.json'
    if dest.exists(): raise ValueError('No sobrescribir recibo previo')
    base = read(E / 'base.json')
    discrepancias = [p for p,h in base['sha256'].items() if sha(ROOT/p) != h]
    backup = read(E / 'respaldo-previo.json')
    assert sha(ROOT/backup['zip']) == backup['zip_sha256'], 'SHA ZIP'
    with zipfile.ZipFile(ROOT/backup['zip']) as z:
        fallos_zip = [p for p,m in backup['archivos'].items()
                      if hashlib.sha256(z.read(p)).hexdigest() != m['sha256']]
    result = {'fecha_utc': datetime.now(timezone.utc).isoformat(),
              'base_sha256': sha(E/'base.json'),
              'discrepancias_base': discrepancias, 'discrepancias_respaldo': fallos_zip,
              'archivos_respaldados':len(backup['archivos']),
              'gemma':'excluido'}
    assert not discrepancias and not fallos_zip, result
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
