"""Fija las versiones finales utilizadas, incluyendo vistas derivadas negativas."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
folders=['C1-candidatas/v001','C2-oportunidades/v001','C3-cobertura/v001',
         'C4-referencias/v002','P1-qudt/v003','P2-owl-time/v001','P2-owl-time/consultas',
         'P3-jerarquia-clinica/v001','P3-jerarquia-clinica/consultas',
         'P4-shacl-versionado/v001','P4-shacl-versionado/v002',
         'W-estandares/v003','W-estandares/v002/normativa',
         'A-auditoria-semantica/v001','A-auditoria-semantica/v003','A-auditoria-semantica/v004',
         'B-auditoria-tecnica/v001','B-auditoria-tecnica/v003', 'K-integracion/v001']
paths={p for f in folders for p in (E/f).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
paths|={E/'P2-owl-time/congelada.json',E/'P3-jerarquia-clinica/congelada.json',
        ROOT/'docs/versionado-y-lanzamientos.md',E/'comprobacion-base.json'}
dest=E/'seleccion-final.json';assert not dest.exists()
data={'format_version':1,'release':'R9','archivos':[{'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(paths)],
      'versiones':folders,'decisiones':{
          'C1':'17 candidatas trazadas; cero promociones',
          'C2':'1191 oportunidades con prioridad y top50; cero joins aprobados',
          'C3':'5523 columnas reconciliadas; cinco observaciones',
          'C4':'19 casos y 104 evidencias; organismos de metadatos primarios; ninguna solicitud enviada',
          'P1':'Q1/Q3 integradas con literales exactos; Q2 negativo fuera del grafo',
          'P2':'negativa: cero intervalos con bordes suficientes',
          'P3':'negativa: 101 conceptos sin jerarquía documental suficiente',
          'P4':'exclusión documentado/candidato sobre 1442 focos y cuatro fixtures',
          'W':'normas verificadas; HectoM3/HectoHA rechazados; corrección de hash en v003',
          'K':'material exacto aceptado por a+b; I-codigo descartado'}}
dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'archivos':len(paths),'sha256':sha(dest)}))
