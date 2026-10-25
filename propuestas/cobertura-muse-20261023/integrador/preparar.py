"""Fija insumos y respaldo antes de la ampliación semántica."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'propuestas/cobertura-muse-20261023'

def main():
    manifest = OUT / 'fuentes/manifiesto.json'
    if manifest.exists():
        raise SystemExit('La instantánea ya existe; no se reemplaza.')
    (OUT / 'fuentes').mkdir(parents=True, exist_ok=True)
    files = []
    for name in ('agente-3-cobertura', 'agente-6-salud', 'agente-7-registro-civil',
                 'agente-8-educacion', 'agente-9-gobierno-digital',
                 'agente-10-territorio-economia', 'agente-11-auditoria',
                 'agente-12-auditoria-salud'):
        for filename in ('propuestas.json', 'auditoria.json', 'resultado.md'):
            source = ROOT / 'propuestas/ronda-3' / name / filename
            if source.exists():
                target = OUT / 'fuentes' / name / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                raw = source.read_bytes()
                target.write_bytes(raw)
                files.append({'origen': source.relative_to(ROOT).as_posix(),
                              'copia': target.relative_to(ROOT).as_posix(),
                              'sha256': hashlib.sha256(raw).hexdigest()})
    basepaths = ['ontologia/semantica.json', 'data/semantica/cobertura.json',
                 'data/portal/contenido-inspeccion.json', 'data/portal/inventario.json',
                 'reports/pendientes-semanticos.json',
                 'propuestas/ronda-3/integrador/asignaciones-semanticas.json']
    sources = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in basepaths}
    backup = OUT / 'integrador/antes-cobertura.zip'
    with ZipFile(backup, 'x', ZIP_DEFLATED) as archive:
        for folder in ('ontologia', 'scripts', 'tests', 'shapes', 'queries', 'docs', 'reports'):
            for path in (ROOT / folder).rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts:
                    archive.write(path, path.relative_to(ROOT).as_posix())
        for name in ('README.md', 'PLAN.md', 'config.toml'):
            archive.write(ROOT / name, name)
    data = {'generado_en_utc': datetime.now(timezone.utc).isoformat(),
            'copias': files, 'insumos_centrales': sources,
            'respaldo': backup.relative_to(ROOT).as_posix(),
            'sha256_respaldo': hashlib.sha256(backup.read_bytes()).hexdigest()}
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Instantánea: {len(files)} archivos; {len(sources)} insumos; respaldo creado.')

if __name__ == '__main__':
    main()
