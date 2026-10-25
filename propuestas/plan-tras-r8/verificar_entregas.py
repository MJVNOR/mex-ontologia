"""Comprueba los recibos de staging sin modificar sus archivos."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'propuestas/plan-tras-r8/ejecucion-20261024'

def verificar():
    results = []
    for seal in sorted(E.rglob('congelada.json')):
        doc = json.loads(seal.read_text(encoding='utf-8-sig'))
        files = doc.get('archivos', {})
        errors = []
        if isinstance(files, list):
            files = {r['ruta']: r['sha256'] for r in files}
        if not isinstance(files, dict):
            errors.append('archivos sin esquema conocido')
            files = {}
        for relative, expected in files.items():
            if isinstance(expected, dict):
                expected = expected['sha256']
            base = ROOT if relative.startswith('propuestas/') else E / doc['rol']
            p = (base / relative).resolve()
            if not p.is_relative_to(ROOT):
                errors.append(relative + ': fuera del proyecto')
            elif not p.is_file():
                errors.append(relative + ': ausente')
            elif hashlib.sha256(p.read_bytes()).hexdigest() != expected:
                errors.append(relative + ': SHA distinto')
        results.append({'sello': seal.relative_to(ROOT).as_posix(),
                        'archivos': len(files), 'errores': errors})
    return results

if __name__ == '__main__':
    result = verificar()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(any(r['errores'] for r in result))
