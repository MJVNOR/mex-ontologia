"""Evita truncar JSON que Windows pueda mantener abierto o mapeado."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
out=E/'io-atomico/v001';assert not out.exists()
(out/'scripts').mkdir(parents=True);(out/'tests').mkdir()
code=(ROOT/'scripts/guardar_rdf.py').read_text(encoding='utf-8')
code+='''

def escribir_json_atomico(value, destination):
    """Publica JSON completo por reemplazo, sin truncar la versión previa."""
    import json
    destination = Path(destination)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\\n',
                dir=destination.parent, prefix=destination.name + '.',
                suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write('\\n')
        os.replace(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
'''
(out/'scripts/guardar_rdf.py').write_text(code,encoding='utf-8')
code=(ROOT/'scripts/consolidar_semantica.py').read_text(encoding='utf-8')
assert code.count('import json\n')==1
code=code.replace('import json\n','import json\nfrom guardar_rdf import escribir_json_atomico\n',1)
old="(OUT / 'cobertura.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')"
assert code.count(old)==1
code=code.replace(old,"escribir_json_atomico(report, OUT / 'cobertura.json')")
old="(ROOT / 'data/territorio/verificacion.json').write_text(json.dumps(territorial_report, ensure_ascii=False, indent=2) + '\\n', encoding='utf-8')"
assert code.count(old)==1
code=code.replace(old,"escribir_json_atomico(territorial_report, ROOT / 'data/territorio/verificacion.json')")
(out/'scripts/consolidar_semantica.py').write_text(code,encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
seal={'motivo':'Windows rechazó truncar cobertura.json (OSError22); publicación por reemplazo atómico con conservación de versión previa. Sin cambios de semántica ni validadores.','archivos':[{'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(out.rglob('*.py'))]}
(out/'codigo-preparado.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(out))
