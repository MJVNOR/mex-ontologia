"""Conserva el reporte intermedio de una regeneración detenida por conteos antiguos."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import consolidar_semantica as c
E=ROOT/'propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z'
try:
    c.generar()
except ValueError as exc:
    tb=exc.__traceback__
    while tb.tb_next: tb=tb.tb_next
    report=tb.tb_frame.f_locals['semantic']
    out=E/'integracion/diagnostico-conteos-r7.json'
    assert not out.exists()
    out.write_text(json.dumps({'motivo':str(exc),'reporte_intermedio':report},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report['resumen'],ensure_ascii=False))
