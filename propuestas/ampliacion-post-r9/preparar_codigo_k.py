"""Corrección coordinada del integrador I; solo crea staging propio."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ampliacion-post-r9/ejecucion-20261024'
OUT=E/'K-codigo/v001'
assert not OUT.exists()
(OUT/'scripts').mkdir(parents=True)
sources={}
for name in ('integrar_ronda_10.py','consolidar_semantica.py','ampliar_portal.py'):
    source=E/'I-codigo/v001/scripts'/name
    sources[name]=hashlib.sha256(source.read_bytes()).hexdigest()
    shutil.copyfile(source,OUT/'scripts'/name)
p=OUT/'scripts/integrar_ronda_10.py'
text=p.read_text(encoding='utf-8')
old="allowed = (str(SH), str(RDF), str(RDFS), str(XSD), str(MEX), BASE)"
assert text.count(old)==1
text=text.replace(old,"allowed = (str(SH), str(RDF), str(RDFS), str(XSD), str(MEX), str(PROV), BASE)")
old="    node_shapes = any(True for _ in graph.subjects(RDF.type, SH.NodeShape))"
new="""    declared = {f['id'] for f in formas}
    actual = {str(s).rsplit('/', 1)[-1]
              for s in graph.subjects(RDF.type, SH.NodeShape)}
    if actual != declared:
        raise ValueError('IDs de formas R10 no coinciden con NodeShapes reales')
    node_shapes = bool(actual)"""
assert text.count(old)==1
text=text.replace(old,new)
p.write_text(text,encoding='utf-8')
(OUT/'origen.json').write_text(json.dumps({'origen':'I-codigo/v001', 'sha256':sources,
    'cambios':['Admitir namespace PROV en objetos SHACL (sh:path prov:wasDerivedFrom real).',
               'Exigir igualdad de IDs declarados con nombres locales NodeShape reales.'],
    'aprobacion':'pendiente_revision_independiente'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(OUT)
