"""Regresiones R9 con material real copiado a tmp.

Los dictámenes simulados existen solo en tmp y prueban la validación; nunca
se usan como auditorías de producción.
"""
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from rdflib import Graph, Literal, RDF, RDFS, SKOS, URIRef

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())
STAGING=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024/K-integracion/v001'
sys.path.insert(0,str(STAGING/'scripts' if 'propuestas' in Path(__file__).parts else ROOT/'scripts'))
sys.path.insert(1,str(ROOT/'scripts'))
import integrar_ronda_9 as r9

def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

class Ronda9Test(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.folder=self.root/r9.EVIDENCIA
        shutil.copytree(STAGING/'material',self.folder)
        (self.root/'ontologia').mkdir()
        shutil.copyfile(self.folder/'base-semantica.json',self.root/'ontologia/semantica.json')
        self.seal()

    def seal(self):
        # Simula aprobación de un payload en un fixture, nunca en el proyecto.
        accepted=r9.read(self.folder/'aceptadas.json')
        accepted['archivos_instalables']={k:r9.sha(self.folder/v) for k,v in r9.ARCHIVOS.items()}
        write(self.folder/'aceptadas.json',accepted)
        for name in ('a','b'):
            write(self.folder/f'auditorias/auditoria-{name}.json',{
                'auditor':name,'dictamen':'aceptar','aceptadas_sha256':r9.sha(self.folder/'aceptadas.json'),
                'dictamenes':[{'id':x,'dictamen':'aceptar'} for x in ('P1-Q1','P1-Q3','P4-exclusion')]})
        self.manifest()

    def manifest(self):
        files={p.relative_to(self.folder).as_posix():r9.sha(p) for p in self.folder.rglob('*')
               if p.is_file() and p.name!='manifiesto.json'}
        write(self.folder/'manifiesto.json',{'format_version':1,'release':'R9','archivos':files})
        write(self.root/'ontologia/revision-ronda-9.json',{'format_version':1,'release':'R9',
            'evidencia':r9.EVIDENCIA,'manifiesto_sha256':r9.sha(self.folder/'manifiesto.json')})

    def graph(self,kind='datos'):
        return Graph().parse(self.folder/r9.ARCHIVOS[kind],format='turtle')

    def save_graph(self,g,kind='datos'):
        g.serialize(self.folder/r9.ARCHIVOS[kind],format='turtle',encoding='utf-8')
        self.seal()

    def reject(self):
        with self.assertRaises(ValueError):r9.cargar(self.root)

    def test_material_real_aceptado_y_construido(self):
        cov=r9.read(self.folder/'cobertura-r8.json')
        data,receipt,_=r9.construir(cov,r9.read(self.folder/'base-semantica.json'),r9.BASE,self.root)
        self.assertEqual(receipt['declaraciones_unidad'],2)
        self.assertEqual(len(set(data.subjects(RDF.type,r9.MEX.UnidadDeclarada))),2)
        self.assertEqual(len(r9.cargar_shapes(self.root)),6)
        self.assertEqual(len(list(data.triples((None,SKOS.broader,None)))),0)

    def test_sin_auditoria_no_carga_shapes(self):
        p=self.folder/'auditorias/auditoria-b.json'
        x=r9.read(p);x['dictamen']='rechazar';write(p,x);self.manifest()
        with self.assertRaises(ValueError):r9.cargar_shapes(self.root)

    def test_aprobacion_sha_exacta(self):
        p=self.folder/'auditorias/auditoria-a.json'
        x=r9.read(p);x['aceptadas_sha256']='0'*64;write(p,x);self.manifest();self.reject()

    def test_aprobacion_tres_casos_exactos(self):
        for field,value in [('dictamenes',[{'id':'P1-Q1','dictamen':'aceptar'}]),('auditor','b')]:
            p=self.folder/'auditorias/auditoria-a.json'
            x=r9.read(p);x[field]=value;write(p,x);self.manifest();self.reject()

    def test_evidencia_sin_rehash_rechazada(self):
        with (self.folder/'datos/unidades.ttl').open('a',encoding='utf-8') as f:f.write('\n# cambio\n')
        self.reject()

    def test_ruta_fuera_de_paquete(self):
        p=self.folder/'manifiesto.json';x=r9.read(p);x['archivos']['../escape']='0'*64;write(p,x)
        c=self.root/'ontologia/revision-ronda-9.json';y=r9.read(c);y['manifiesto_sha256']=r9.sha(p);write(c,y)
        self.reject()

    def test_nucleo_vivo_no_se_modifica(self):
        p=self.root/'ontologia/semantica.json';x=r9.read(p);x['extra']='x';write(p,x);self.reject()

    def test_snapshot_nucleo_no_se_reaprueba(self):
        p=self.folder/'base-semantica.json';x=r9.read(p);x['extra']='x';write(p,x)
        shutil.copyfile(p,self.root/'ontologia/semantica.json');self.seal();self.reject()

    def test_solo_dos_declaraciones(self):
        p=self.folder/'aceptadas.json';x=r9.read(p);x['declaraciones'].append(x['declaraciones'][0]);write(p,x)
        self.seal();self.reject()

    def test_unidad_literal_exacta_sin_normalizar(self):
        p=self.folder/'aceptadas.json';x=r9.read(p);x['declaraciones'][0]['unidad_literal']='Milimetros';write(p,x)
        self.seal();self.reject()

    def test_fila_original_inmutable(self):
        p=self.folder/'filas/P1-Q1.json';x=r9.read(p);x['Unidad de medida']='Milimetros';write(p,x)
        self.seal();self.reject()

    def test_normativa_inmutable(self):
        p=self.folder/'normativa/P1-Q1.txt';p.write_text('otra norma',encoding='utf-8');self.seal();self.reject()

    def test_objeto_variable_exacto(self):
        g=self.graph();s=URIRef(r9.PIN['P1-Q1']['sujeto']);g.set((s,r9.MEX.variableDocumentada,URIRef('urn:otra')))
        self.save_graph(g);self.reject()

    def test_literal_rdf_exacto(self):
        g=self.graph();s=URIRef(r9.PIN['P1-Q1']['sujeto']);g.set((s,r9.MEX.unidadLiteral,Literal('Milimetros')))
        self.save_graph(g);self.reject()

    def test_procedencia_completa(self):
        g=self.graph();s=URIRef(r9.PIN['P1-Q1']['sujeto']);g.remove((s,r9.PROV.wasDerivedFrom,None))
        self.save_graph(g);self.reject()

    def test_iri_qudt_http_canonica(self):
        g=self.graph();s=URIRef(r9.PIN['P1-Q1']['sujeto'])
        g.set((s,r9.MEX.unidadQudt,URIRef('https://qudt.org/vocab/unit/MilliM')))
        self.save_graph(g);self.reject()

    def test_sujeto_adicional_rechazado_aun_reaprobado(self):
        g=self.graph();g.add((URIRef(r9.PIN['P1-Q1']['variable']),r9.MEX.unidadQudt,URIRef(r9.PIN['P1-Q1']['unidad_qudt'])))
        self.save_graph(g);self.reject()

    def test_predicado_adicional_rechazado_aun_reaprobado(self):
        g=self.graph();g.add((URIRef(r9.PIN['P1-Q1']['sujeto']),SKOS.broader,URIRef('urn:x')))
        self.save_graph(g);self.reject()

    def test_modelo_no_infiere_rango(self):
        g=self.graph('modelo');g.add((r9.MEX.variableDocumentada,RDFS.range,URIRef('http://qudt.org/schema/qudt/QuantityValue')))
        self.save_graph(g,'modelo');self.reject()

    def test_tipo_property_rdf_correcto(self):
        g=self.graph('modelo');g.set((r9.MEX.unidadQudt,RDF.type,URIRef(str(RDFS)+'Property')))
        self.save_graph(g,'modelo');self.reject()

    def test_shape_no_se_reaprueba_distinta(self):
        p=self.folder/r9.ARCHIVOS['shapes'];p.write_text(p.read_text(encoding='utf-8')+'\n# cambio\n',encoding='utf-8')
        self.seal();self.reject()

    def test_resumen_r8_se_conserva(self):
        cov=r9.read(self.folder/'cobertura-r8.json');cov['resumen']['conceptos_compartidos']=0
        with self.assertRaises(ValueError):r9.construir(cov,r9.read(self.folder/'base-semantica.json'),r9.BASE,self.root)

    def test_variable_viva_con_contexto_exacto(self):
        cov=r9.read(self.folder/'cobertura-r8.json')
        for v in cov['variables']:
            if v.get('definicion_iri')==r9.PIN['P1-Q1']['definicion_iri']:v['conjunto']='otro'
        with self.assertRaises(ValueError):r9.construir(cov,r9.read(self.folder/'base-semantica.json'),r9.BASE,self.root)

if __name__=='__main__':unittest.main(verbosity=2)
