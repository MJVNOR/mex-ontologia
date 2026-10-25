import copy,json,hashlib,tempfile,unittest,sys
from pathlib import Path
MINE=Path(__file__).resolve().parent.parent/'scripts'
sys.path.insert(0,str(MINE))
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from integrar_ronda_6 import validar_sobre_base,dentro
ADENDA=ROOT/'propuestas/pendientes-muse-r6/diversos-presas/adenda-presas.json'
MARKER=ROOT/'propuestas/pendientes-muse-r6/diversos-presas/adenda-presas.sha.json'

class Ronda6GuardTest(unittest.TestCase):
 def setUp(self):
  raw=ADENDA.read_bytes()
  marker=json.loads(MARKER.read_text(encoding='utf-8'))
  if hashlib.sha256(raw).hexdigest()!=marker['archivos']['adenda-presas.json']:raise ValueError('SHA corregido de adenda-presas.json no coincide')
  self.vinculo=json.loads(raw.decode('utf-8'))['vinculo_propuesto']
  self.columna=self.vinculo['columna']
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.folder=self.root/'data/r6';self.folder.mkdir(parents=True)
  self.base={'reglas_descripcion_exacta':[{'id':'r-previa'}],'vinculos_documentales_revisados':[{'columna':'col-previa'}],'conceptos':{'c-previo':['Previo','Original',None]},'observaciones_revision':['conservar']}
  self.accepted={'reglas':[],'vinculos':[],'conceptos':{},'origenes':{},'resumen':{}}
  self.write('base-semantica.json',self.base);self.write('aceptadas.json',self.accepted)
  self.write('auditorias/auditoria-a.json',{'dictamenes':[]})
  self.write('auditorias/auditoria-b.json',{'dictamenes':[]})
  self.seal()
  self.rules=copy.deepcopy(self.base)
 def write(self,p,v):
  q=self.folder/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v,ensure_ascii=False),encoding='utf-8')
 def seal(self):
  h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
  files={str(p.relative_to(self.folder)).replace('\\','/'):h(p) for p in self.folder.rglob('*.json') if p.name!='manifiesto.json'}
  self.write('manifiesto.json',{'archivos':files,'insumos':{}})
  cp=self.root/'ontologia/revision-ronda-6.json';cp.parent.mkdir(exist_ok=True);cp.write_text(json.dumps({'evidencia':'data/r6','manifiesto_sha256':h(self.folder/'manifiesto.json')}),encoding='utf-8')
 def dar_adenda(self):
  raw=ADENDA.read_bytes()
  (self.folder/'adenda-presas.json').write_bytes(raw)
  if (self.folder/'adenda-presas.json').read_bytes()!=raw:raise ValueError('Adenda copiada no idéntica')
  self.accepted['vinculos']=[copy.deepcopy(self.vinculo)]
  self.accepted['origenes']={self.columna:['adenda-presas.json']}
  self.write('aceptadas.json',self.accepted)
  self.write('auditorias/auditoria-b.json',{'dictamenes':[{'tipo':'vinculos','id':self.columna,'dictamen':'aceptar'}]})
  self.seal()
  self.rules=copy.deepcopy(self.base);self.rules['vinculos_documentales_revisados']+=self.accepted['vinculos']
 def test_extension_exacta_es_valida(self):validar_sobre_base(self.rules,self.base,self.root)
 def test_vinculo_unico_presas_valido(self):
  self.dar_adenda();validar_sobre_base(self.rules,self.base,self.root)
 def test_segundo_vinculo_falla(self):
  otro=copy.deepcopy(self.vinculo);otro['columna']=self.columna+'%2F9'
  self.accepted['vinculos']=[copy.deepcopy(self.vinculo),otro]
  self.accepted['origenes']={self.columna:['adenda-presas.json'],otro['columna']:['adenda-presas.json']}
  self.write('aceptadas.json',self.accepted);self.seal()
  self.rules=copy.deepcopy(self.base);self.rules['vinculos_documentales_revisados']+=self.accepted['vinculos']
  with self.assertRaisesRegex(ValueError,'correspondencia única'):validar_sobre_base(self.rules,self.base,self.root)
 def test_columnas_duplicadas_falla(self):
  self.accepted['vinculos']=[copy.deepcopy(self.vinculo),copy.deepcopy(self.vinculo)]
  self.accepted['origenes']={self.columna:['adenda-presas.json']};self.write('aceptadas.json',self.accepted);self.seal()
  self.rules=copy.deepcopy(self.base);self.rules['vinculos_documentales_revisados']+=self.accepted['vinculos']
  with self.assertRaisesRegex(ValueError,'duplicadas'):validar_sobre_base(self.rules,self.base,self.root)
 def test_base_modificada_falla(self):
  base=copy.deepcopy(self.base);base['observaciones_revision']=[]
  with self.assertRaisesRegex(ValueError,'Base'):validar_sobre_base(self.rules,base,self.root)
 def test_evidencia_alterada_falla(self):
  self.write('auditorias/auditoria-a.json',{'dictamenes':[{'intruso':True}]})
  with self.assertRaisesRegex(ValueError,'Evidencia'):validar_sobre_base(self.rules,self.base,self.root)
 def test_sin_aprobacion_independiente_falla(self):
  self.dar_adenda()
  self.write('auditorias/auditoria-b.json',{'dictamenes':[]});self.seal()
  with self.assertRaisesRegex(ValueError,'aprobación independiente'):validar_sobre_base(self.rules,self.base,self.root)
 def test_ruta_fuera_de_evidencia_falla(self):
  with self.assertRaisesRegex(ValueError,'fuera de carpeta'):dentro(self.root,'../otro')
 def test_origen_sin_fijar_falla(self):
  self.accepted['vinculos']=[copy.deepcopy(self.vinculo)]
  self.accepted['origenes']={self.columna:['no-fijado.json']};self.write('aceptadas.json',self.accepted);self.seal()
  self.rules=copy.deepcopy(self.base);self.rules['vinculos_documentales_revisados']+=self.accepted['vinculos']
  with self.assertRaisesRegex(ValueError,'Origen no fijado'):validar_sobre_base(self.rules,self.base,self.root)
class Ronda5ConConfigR6Test(unittest.TestCase):
 """La delegacion a R6 no salta las validaciones historicas de R5 (carga directa del staging, no del central)."""
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  (self.root/'ontologia').mkdir(parents=True,exist_ok=True)
  (self.root/'ontologia'/'revision-ronda-6.json').write_text(json.dumps({'evidencia':'data/r6','manifiesto_sha256':'x'}),encoding='utf-8')
  self.folder=self.root/'data'/'r5';(self.folder/'auditorias').mkdir(parents=True,exist_ok=True);(self.folder/'evidencia').mkdir(parents=True,exist_ok=True)
  self.base={'reglas_descripcion_exacta':[],'vinculos_documentales_revisados':[],'conceptos':{},'observaciones_revision':['ok']}
  import importlib.util as _ilu
  _p=Path(__file__).resolve().parent.parent/'scripts'/'integrar_ronda_5.py'
  _spec=_ilu.spec_from_file_location('integrar_ronda_5_staging',str(_p))
  self.r5=_ilu.module_from_spec(_spec);_spec.loader.exec_module(self.r5)
  assert 'catalogos' in self.r5.__file__.replace('\\','/'),self.r5.__file__
 def armar_r5(self,accepted):
  def write(rel,v):
   q=self.folder/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v,ensure_ascii=False),encoding='utf-8')
  write('base-semantica.json',self.base);write('aceptadas.json',accepted)
  write('auditorias/auditoria-a.json',{'dictamenes':[]});write('auditorias/auditoria-b.json',{'dictamenes':[]})
  write('evidencia/x.json',{'prueba':1})
  h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
  files={str(p.relative_to(self.folder)).replace('\\','/'):h(p) for p in self.folder.rglob('*.json') if p.name!='manifiesto.json'}
  write('manifiesto.json',{'archivos':files,'insumos':{}})
  (self.root/'ontologia'/'revision-ronda-5.json').write_text(json.dumps({'evidencia':'data/r5','manifiesto_sha256':h(self.folder/'manifiesto.json')}),encoding='utf-8')
  expected=copy.deepcopy(self.base)
  expected['reglas_descripcion_exacta'].extend(accepted['reglas'])
  expected['vinculos_documentales_revisados'].extend(accepted['vinculos'])
  return expected
 def test_r5_duplicados_falla_con_config_r6(self):
  dup={'id':'dup'}
  accepted={'reglas':[dup,copy.deepcopy(dup)],'vinculos':[],'conceptos':{},'origenes':{'dup':['evidencia/x.json']},'resumen':{}}
  rules=self.armar_r5(accepted)
  with self.assertRaisesRegex(ValueError,'duplicadas'):self.r5.validar_sobre_base(rules,copy.deepcopy(self.base),self.root)
 def test_r5_sin_aprobacion_falla_con_config_r6(self):
  accepted={'reglas':[{'id':'sola'}],'vinculos':[],'conceptos':{},'origenes':{'sola':['evidencia/x.json']},'resumen':{}}
  rules=self.armar_r5(accepted)
  with self.assertRaisesRegex(ValueError,'aprobaci.n independiente'):self.r5.validar_sobre_base(rules,copy.deepcopy(self.base),self.root)
 def test_r5_valido_llega_a_r6(self):
  accepted={'reglas':[],'vinculos':[],'conceptos':{},'origenes':{},'resumen':{}}
  rules=self.armar_r5(accepted)
  (self.root/'data'/'r6').mkdir(parents=True,exist_ok=True)
  (self.root/'data'/'r6'/'manifiesto.json').write_text('{}',encoding='utf-8')
  with self.assertRaisesRegex(ValueError,'ronda 6'):self.r5.validar_sobre_base(rules,copy.deepcopy(self.base),self.root)
if __name__=='__main__':unittest.main()
