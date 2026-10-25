"""La ampliación rechaza cambios ajenos, evidencia alterada y aprobaciones ausentes."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from integrar_ronda_4 import validar

class EvidenciaRonda4Test(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.folder=self.root/'data/r4'
        self.folder.mkdir(parents=True)
        self.base={'conceptos':{'base':['Base','Definición',None]},
                   'reglas_descripcion_exacta':[],
                   'vinculos_documentales_revisados':[{'columna':'previa'}],
                   'condiciones':{'periodo':'Conservar periodo'}}
        self.link={'columna':'nueva','concepto':'base'}
        self.accepted={'reglas':[],'vinculos':[self.link],'conceptos':{},'origenes':{},'resumen':{}}
        self.rules=copy.deepcopy(self.base)
        self.rules['vinculos_documentales_revisados'].append(self.link)
        self.write('base-semantica.json',self.base)
        self.write('aceptadas.json',self.accepted)
        self.write('auditorias/auditoria-a.json',{'dictamenes':[]})
        self.write('auditorias/auditoria-b.json',{'dictamenes':[{'tipo':'vinculos','id':'nueva','dictamen':'aceptar'}]})
        self.freeze()

    def tearDown(self):
        self.temp.cleanup()

    def write(self,relative,obj):
        path=self.folder/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(obj),encoding='utf-8')

    def freeze(self):
        manifest={'archivos':{p.relative_to(self.folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in self.folder.rglob('*.json') if p.name!='manifiesto.json'},'insumos':{}}
        self.write('manifiesto.json',manifest)
        config={'evidencia':'data/r4','manifiesto_sha256':hashlib.sha256((self.folder/'manifiesto.json').read_bytes()).hexdigest()}
        (self.root/'ontologia').mkdir(exist_ok=True)
        (self.root/'ontologia/revision-ronda-4.json').write_text(json.dumps(config),encoding='utf-8')

    def test_acepta_solo_extension_exacta(self):
        validar(self.rules,self.root)

    def test_rechaza_cambio_de_base_y_adicion_no_aprobada(self):
        for change in ['base','adicion','condicion']:
            altered=copy.deepcopy(self.rules)
            if change=='base':
                altered['vinculos_documentales_revisados'][0]['columna']='otra'
            elif change=='adicion':
                altered['vinculos_documentales_revisados'].append({'columna':'tercera'})
            else:
                altered['condiciones']['periodo']='Suprimir periodo'
            with self.subTest(change=change), self.assertRaises(ValueError):
                validar(altered,self.root)

    def test_rechaza_evidencia_alterada_tras_fijacion(self):
        self.write('aceptadas.json',dict(self.accepted,vinculos=[]))
        with self.assertRaisesRegex(ValueError,'Evidencia de ronda 4 modificada'):
            validar(self.rules,self.root)

    def test_rechaza_vinculo_sin_dictamen_aceptar(self):
        self.write('auditorias/auditoria-b.json',{'dictamenes':[{'tipo':'vinculos','id':'nueva','dictamen':'condicionado'}]})
        self.freeze()
        with self.assertRaisesRegex(ValueError,'sin aprobación independiente'):
            validar(self.rules,self.root)

    def test_rechaza_duplicacion_de_columna_aun_con_manifiesto(self):
        self.accepted['vinculos'].append(self.link)
        self.write('aceptadas.json',self.accepted)
        self.freeze()
        self.rules['vinculos_documentales_revisados'].append(self.link)
        with self.assertRaisesRegex(ValueError,'duplicadas'):
            validar(self.rules,self.root)

    def test_rechaza_ruta_fuera_de_evidencia(self):
        manifest=json.loads((self.folder/'manifiesto.json').read_text())
        manifest['archivos']['../../fuera.json']='irrelevante'
        self.write('manifiesto.json',manifest)
        config_path=self.root/'ontologia/revision-ronda-4.json'
        config=json.loads(config_path.read_text())
        config['manifiesto_sha256']=hashlib.sha256((self.folder/'manifiesto.json').read_bytes()).hexdigest()
        config_path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError,'fuera de su carpeta'):
            validar(self.rules,self.root)

if __name__=='__main__':
    unittest.main()
