"""Regresión R8: evidencia, identidad de definición y límites del delta aprobado."""
from pathlib import Path
import copy,hashlib,json,shutil,sys,tempfile,unittest
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())
sys.path.insert(0,str(ROOT/'scripts'))
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
@unittest.skipUnless((ROOT/'ontologia/revision-ronda-8.json').exists(),'R8 no integrada')
class Ronda8Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import integrar_ronda_8
        cls.r8=integrar_ronda_8
        cls.rules=read(ROOT/'ontologia/semantica.json')
        cls.config,cls.folder,cls.base,cls.accepted,_=cls.r8.cargar()
    def fixture(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root=Path(temporary.name)
        folder=root/'data/integracion-ronda-8'
        shutil.copytree(self.folder,folder)
        (root/'ontologia').mkdir()
        shutil.copy2(ROOT/'ontologia/revision-ronda-8.json',root/'ontologia/revision-ronda-8.json')
        return root,folder
    def repin(self,root,folder):
        m=read(folder/'manifiesto.json')
        m['archivos']={rel:sha(folder/rel) for rel in m['archivos']}
        write(folder/'manifiesto.json',m)
        c=read(root/'ontologia/revision-ronda-8.json')
        c['manifiesto_sha256']=sha(folder/'manifiesto.json')
        write(root/'ontologia/revision-ronda-8.json',c)
    def test_extension_exacta_sin_significados_conceptos_nuevos(self):
        self.assertEqual(self.accepted['reglas'],[])
        self.assertEqual(self.accepted['conceptos'],{})
        self.assertEqual(len(self.accepted['vinculos']),28)
        self.r8.validar_sobre_base(self.rules,self.base)
        self.assertEqual(self.rules['reglas_descripcion_exacta'],self.base['reglas_descripcion_exacta'])
        self.assertEqual(self.rules['conceptos'],self.base['conceptos'])
    def test_manifiesto_modificado_se_rechaza(self):
        root,folder=self.fixture()
        (folder/'manifiesto.json').write_text('{}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Manifiesto'):
            self.r8.cargar(root)
    def test_iri_variable_no_sustituye_iri_definicion(self):
        root,folder=self.fixture();a=read(folder/'aceptadas.json')
        a['vinculos'][0]['definicion_iri']=a['vinculos'][0]['definicion_iri'].replace('/definition/','/documented-variable/')
        write(folder/'aceptadas.json',a);self.repin(root,folder)
        with self.assertRaises(ValueError): self.r8.cargar(root)
    def test_descripcion_nacional_no_sustituye_original_local(self):
        root,folder=self.fixture();a=read(folder/'aceptadas.json')
        a['vinculos'][0]['descripcion']='0000 = NINGUNA APARENTE; catálogo adoptado globalmente'
        write(folder/'aceptadas.json',a);self.repin(root,folder)
        with self.assertRaises(ValueError): self.r8.cargar(root)
    def test_campo_y_variable_de_otra_fila_se_rechazan(self):
        for field in ('campo','definicion_iri','huella_fila_diccionario'):
            with self.subTest(field=field):
                root,folder=self.fixture();a=read(folder/'aceptadas.json')
                a['vinculos'][0][field]=a['vinculos'][1][field]
                write(folder/'aceptadas.json',a);self.repin(root,folder)
                with self.assertRaises(ValueError): self.r8.cargar(root)
    def test_candidata_ausente_del_universo_se_rechaza(self):
        root,folder=self.fixture();c=read(folder/'cobertura-r7.json')
        target=self.accepted['vinculos'][0]['columna']
        c['correspondencias']=[m for m in c['correspondencias'] if m['columna']!=target]
        write(folder/'cobertura-r7.json',c);self.repin(root,folder)
        with self.assertRaises(ValueError): self.r8.cargar(root)
    def test_rechazo_global_no_es_aceptacion_por_ids(self):
        root,folder=self.fixture();a=read(folder/'auditorias/auditoria-a.json')
        a['dictamen']='rechazar';write(folder/'auditorias/auditoria-a.json',a);self.repin(root,folder)
        with self.assertRaises(ValueError): self.r8.validar_sobre_base(self.rules,self.base,root)
    def test_pin_auditoria_distinto_se_rechaza(self):
        root,folder=self.fixture();a=read(folder/'auditorias/auditoria-b.json')
        a['aceptadas_sha256']='0'*64;write(folder/'auditorias/auditoria-b.json',a);self.repin(root,folder)
        with self.assertRaises(ValueError): self.r8.validar_sobre_base(self.rules,self.base,root)
    def test_adicion_no_aprobada_se_rechaza(self):
        changed=copy.deepcopy(self.rules);changed['conceptos']['no-aprobado']=['x','x',None]
        with self.assertRaises(ValueError): self.r8.validar_sobre_base(changed,self.base)
if __name__=='__main__': unittest.main()
