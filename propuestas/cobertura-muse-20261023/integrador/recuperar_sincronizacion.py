"""Cierra la sincronización aplicada, tras verificar equivalencia RDF 1.1.

No vuelve a insertar ni retirar triples. Conserva los archivos de la ejecución
fallida y reconstruye exactamente la propiedad calculada antes de aplicar.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

from rdflib import Graph
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir_catalogo import motor
from sincronizar_studio_portal import api, normalizar_cadenas

folder = ROOT / 'data/portal'
stage = ROOT / 'propuestas/cobertura-muse-20261023/integrador/sync-fallida'
stage.mkdir(exist_ok=False)
for name in ('studio-previsto.ttl', 'studio-verificacion.ttl', 'studio-insertar.ttl', 'studio-managed.ttl'):
    shutil.copyfile(folder / name, stage / name)
parse = lambda path: Graph().parse(path, format='turtle')
normalize = normalizar_cadenas
expected_raw = parse(stage / 'studio-previsto.ttl')
observed_raw = parse(stage / 'studio-verificacion.ttl')
expected, observed = normalize(expected_raw), normalize(observed_raw)
if not isomorphic(expected, observed):
    raise ValueError('La diferencia no se limita a equivalencia de cadenas RDF 1.1')
desired = normalize(parse(folder / 'ampliacion.ttl'))
previous = normalize(parse(stage / 'studio-managed.ttl'))
inserted = normalize(parse(stage / 'studio-insertar.ttl'))
owned = (previous & desired) + inserted
if len(owned - desired):
    raise ValueError('Los triples insertados no pertenecen al grafo deseado')
# Reconstituir y verificar también el estado inicial de la operación fallida.
backup = ROOT / 'data/backups/studio-antes-portal-20261023T112609936613Z.ttl'
before = normalize(parse(backup))
removed = previous - desired
if not isomorphic((before - removed) + inserted, expected):
    raise ValueError('Los recibos de la operación no reproducen el estado previsto')
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
fresh = stage / 'studio-actual.ttl'
api('/save', {'path': str(fresh), 'format': 'turtle'})
if not isomorphic(normalize(parse(fresh)), expected):
    raise ValueError('Studio cambió después de la sincronización fallida; revisar antes de recuperar')
canonical = stage / 'studio-previsto-canonico.ttl'
expected.serialize(canonical, format='turtle', encoding='utf-8')
store = ROOT / 'store' / ('studio-recuperacion-cobertura-' + stamp)
motor(['load', str(canonical)], store)
validation = motor(['shacl', str(folder / 'shapes.ttl')], store)
if validation.get('conforms') is not True:
    raise ValueError('La recuperación no supera SHACL')
fresh2 = stage / 'studio-actual-verificado.ttl'
api('/save', {'path': str(fresh2), 'format': 'turtle'})
final = normalize(parse(fresh2))
if not isomorphic(final, expected) or len(owned - final):
    raise ValueError('Studio cambió durante la validación de recuperación')
if (stage / 'studio-managed.ttl').read_bytes() != (folder / 'studio-managed.ttl').read_bytes():
    raise ValueError('El registro de propiedad cambió durante la recuperación')
api('/save', {'path': str(ROOT / 'data/catalogo/studio-live.ttl'), 'format': 'turtle'})
owned.serialize(folder / 'studio-managed.ttl', format='turtle', encoding='utf-8')
report = {'respaldo': backup.relative_to(ROOT).as_posix(),
          'triples_insertados': len(inserted), 'triples_retirados_gestionados': len(removed),
          'triples_totales_studio': len(final), 'triples_gestionados': len(owned),
          'verificado': True, 'shacl': validation,
          'recuperacion': {'sin_nuevas_mutaciones_de_triples': True,
                          'causa': 'Equivalencia RDF 1.1 de xsd:string y literal simple',
                          'diferencias_sintacticas_por_lado': len(expected_raw-observed_raw),
                          'recibos': stage.relative_to(ROOT).as_posix(),
                          'isomorfismo_canonico': True},
          'propiedad_reconstruida_desde_insertados': True}
(ROOT / 'reports/studio-portal-sync.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(ROOT / 'reports/cobertura-muse-recuperacion-sync.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k != 'shacl'}, ensure_ascii=True, indent=2))
