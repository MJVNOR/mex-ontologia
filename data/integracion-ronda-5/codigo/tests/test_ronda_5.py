import copy,json,hashlib,tempfile,unittest,sys
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())
sys.path.insert(0,str(ROOT/'scripts'))
if not (ROOT/'scripts/integrar_ronda_5.py').exists():sys.path.insert(0,str(ROOT/'propuestas/pendientes-muse-r5/integrador/codigo/scripts'))
from integrar_ronda_5 import validar_sobre_base,dentro

class Ronda5GuardTest(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.folder=self.root/'data/r5';self.folder.mkdir(parents=True)
  self.base={'reglas_descripcion_exacta':[{'id':'base'}],'vinculos_documentales_revisados':[{'columna':'col-base'}],'conceptos':{'base':['Base','Original',None]},'observaciones_revision':['conservar']}
  self.accepted={'reglas':[{'id':'r5'}],'vinculos':[{'columna':'col-r5'}],'conceptos':{'r5':['R5','Añadido',None]},'origenes':{'r5':['base-semantica.json'],'col-r5':['base-semantica.json']}}
  self.write('base-semantica.json',self.base);self.write('aceptadas.json',self.accepted)
  self.write('auditorias/auditoria-a.json',{'dictamenes':[{'tipo':'reglas','id':'r5','dictamen':'aceptar'}]})
  self.write('auditorias/auditoria-b.json',{'dictamenes':[{'tipo':'vinculos','id':'col-r5','dictamen':'aceptar'}]})
  self.seal()
  self.rules=copy.deepcopy(self.base);self.rules['reglas_descripcion_exacta']+=self.accepted['reglas'];self.rules['vinculos_documentales_revisados']+=self.accepted['vinculos'];self.rules['conceptos'].update(self.accepted['conceptos'])
 def write(self,p,v):
  q=self.folder/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v,ensure_ascii=False),encoding='utf-8')
 def seal(self):
  h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
  files={str(p.relative_to(self.folder)).replace('\\','/'):h(p) for p in self.folder.rglob('*.json') if p.name!='manifiesto.json'}
  self.write('manifiesto.json',{'archivos':files,'insumos':{}})
  cp=self.root/'ontologia/revision-ronda-5.json';cp.parent.mkdir(exist_ok=True);cp.write_text(json.dumps({'evidencia':'data/r5','manifiesto_sha256':h(self.folder/'manifiesto.json')}),encoding='utf-8')
 def test_extension_exacta_es_valida(self):validar_sobre_base(self.rules,self.base,self.root)
 def test_regla_no_aprobada_falla(self):
  self.rules['reglas_descripcion_exacta'].append({'id':'intrusa'})
  with self.assertRaisesRegex(ValueError,'adiciones auditadas'):validar_sobre_base(self.rules,self.base,self.root)
 def test_base_modificada_falla(self):
  base=copy.deepcopy(self.base);base['observaciones_revision']=[]
  with self.assertRaisesRegex(ValueError,'Base'):validar_sobre_base(self.rules,base,self.root)
 def test_evidencia_alterada_falla(self):
  self.write('auditorias/auditoria-a.json',{'dictamenes':[]})
  with self.assertRaisesRegex(ValueError,'Evidencia'):validar_sobre_base(self.rules,self.base,self.root)
 def test_sin_aprobacion_independiente_falla_aun_con_manifiesto(self):
  self.write('auditorias/auditoria-b.json',{'dictamenes':[]});self.seal()
  with self.assertRaisesRegex(ValueError,'aprobación independiente'):validar_sobre_base(self.rules,self.base,self.root)
 def test_concepto_anterior_no_se_sustituye(self):
  self.accepted['conceptos']['base']=['Otro','Alterado',None];self.write('aceptadas.json',self.accepted);self.seal()
  with self.assertRaisesRegex(ValueError,'sustituyó concepto'):validar_sobre_base(self.rules,self.base,self.root)
 def test_ruta_fuera_de_evidencia_falla(self):
  with self.assertRaisesRegex(ValueError,'fuera de carpeta'):dentro(self.root,'../otro')
 def test_manifiesto_incompleto_falla(self):
  self.write('manifiesto.json',{'otro':{}})
  cp=self.root/'ontologia/revision-ronda-5.json';config=json.loads(cp.read_text(encoding='utf-8'));config['manifiesto_sha256']=hashlib.sha256((self.folder/'manifiesto.json').read_bytes()).hexdigest();cp.write_text(json.dumps(config),encoding='utf-8')
  with self.assertRaisesRegex(ValueError,'incompleto'):validar_sobre_base(self.rules,self.base,self.root)
 def test_origen_sin_fijar_falla(self):
  self.accepted['origenes']['r5']=['no-fijado.json'];self.write('aceptadas.json',self.accepted);self.seal()
  with self.assertRaisesRegex(ValueError,'Origen no fijado'):validar_sobre_base(self.rules,self.base,self.root)
if __name__=='__main__':unittest.main()
