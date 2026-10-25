import hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[3]
S=R/'propuestas/pendientes-muse-r4'
D=R/'data/integracion-ronda-4-historia'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if D.exists(): raise ValueError('Evidencia histórica ya fijada; no sobrescribir')
 audit=json.loads((S/'auditoria-b/revision-historia.json').read_text(encoding='utf-8-sig'))
 paths=['scripts/integrar_ronda_2.py','tests/test_cobertura_integrada.py','tests/test_dictamen_historico.py']
 expected=['0ec43752c581d11a62e92b1ba273fb465e949e8ff215fa02bd89571d476f80f8','12e7661986e412f29aff0c542a4bde200fe46c16310d32d7daa3cc6ca4ef47d4','0dc59b3791f6182d7e64a2f39a8ca8ef315dd671cd90b8a60c0ca910f4729963']
 for p,h in zip(paths,expected):
  if sha(R/p)!=h: raise ValueError('Reparación no coincide con revisión: '+p)
 copies={p:R/p for p in paths}
 copies.update({'auditoria/revision-historia.json':S/'auditoria-b/revision-historia.json','auditoria/listo-historia.json':S/'auditoria-b/listo-historia.json','instalacion.json':S/'integrador/reparacion-historia/instalacion.json'})
 for rel,p in copies.items():
  dest=D/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 manifest={'alcance':'Compatibilidad de dictámenes históricos con cuatro promociones explícitas de ronda 4; evidencia original intacta.','ronda4_manifiesto_sha256':'c9edd8a180b0c79cc4c3eacce3c9e52009ddb63e68951db7181c6a377da046f2','archivos':{rel:sha(D/rel) for rel in copies}}
 (D/'manifiesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(sha(D/'manifiesto.json'))
if __name__=='__main__':main()
