"""Los encabezados duplicados solo se resuelven por revisión física y definición exactas."""
import copy
import unittest

from consolidar_semantica import construir, columnas, huella

class SeleccionDocumentalTest(unittest.TestCase):
    def setUp(self):
        self.base='https://example.org/prueba/'
        self.rules={'alcance':'Prueba','conceptos':{},'condiciones':{},'distinciones':[],
                    'reglas_descripcion_exacta':[],'vinculos_documentales_revisados':[], 'observaciones_revision':[]}
        for key in ['municipio-registro','municipio-residencia','municipio-defuncion',
                    'anio-registro','anio-defuncion','organizacion-publicadora','organizacion-capturadora','capacidad','generacion']:
            self.rules['conceptos'][key]=[key,'Definición de prueba',None]
        self.inventory={'recursos':[
            {'id':'dic','conjunto_id':'d','conjunto':'Prueba','clasificacion':'diccionario'},
            {'id':'r','conjunto_id':'d','conjunto':'Prueba','clasificacion':'datos_estructurados','url':'https://example.org/r'}]}
        self.rows=[{'Nombre variable':'Unidad','Descripción':'Unidad de capacidad'},
                   {'Nombre variable':'Unidad','Descripción':'Unidad de generación'}]
        self.inspection={'recursos':[
            {'id':'dic','ok':True,'definiciones':self.rows},
            {'id':'r','ok':True,'tablas':[{'hoja':'Datos','campos':[
                {'id':'Unidad','posicion_original':1},{'id':'Unidad','posicion_original':2}]}]}]}
        for i,concept in enumerate(['capacidad','generacion'],1):
            self.rules['reglas_descripcion_exacta'].append({'id':'r'+str(i),'concepto':concept,
                'nombres':['Unidad'],'descripciones':[self.rows[i-1]['Descripción']],
                'conjuntos':['d'],'diccionarios':['dic'],'definiciones':[self.base+'definition/dic%2F'+str(i)],
                'representacion':'no_especificada'})
        self.cols=columnas(self.inventory,self.inspection,self.base)

    def link(self,i):
        col=self.cols[i]
        return {'recurso':'r','campo':'Unidad','columna':col['iri'],'diccionario':'dic',
                'definicion_iri':self.base+'definition/dic%2F'+str(i+1),
                'concepto':['capacidad','generacion'][i], 'descripcion':self.rows[i]['Descripción'],
                'huella_esquema':col['huella_esquema'],'huella_fila_diccionario':huella(self.rows[i]),
                'criterio':'Posición física, fila y contexto documental revisados'}

    def build(self):
        return construir(self.inventory,self.inspection,self.rules,None,self.base)[2]

    def test_sin_revision_conserva_cuatro_alternativas_ambiguas(self):
        mappings=self.build()['correspondencias']
        self.assertEqual(len(mappings),4)
        self.assertEqual({r['estado'] for r in mappings},{'ambigua_por_nombre'})

    def test_seleccion_expresa_conserva_destinos_distintos(self):
        self.rules['vinculos_documentales_revisados']=[self.link(0),self.link(1)]
        rows=self.build()['correspondencias']
        self.assertEqual(len(rows),2)
        self.assertEqual({r['estado'] for r in rows},{'documental_revisada'})
        self.assertEqual({r['concepto'] for r in rows},{'capacidad','generacion'})

    def test_sin_definicion_no_se_resuelve_por_posicion_implicitamente(self):
        link=self.link(0)
        link.pop('definicion_iri')
        self.rules['vinculos_documentales_revisados']=[link]
        with self.assertRaises(ValueError):
            self.build()

    def test_seleccion_sin_columna_o_con_huella_cambiada_falla(self):
        for field in ['columna','huella_fila_diccionario']:
            link=self.link(0)
            if field=='columna':
                link.pop(field)
            else:
                link[field]='alterada'
            self.rules['vinculos_documentales_revisados']=[link]
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.build()

if __name__=='__main__':
    unittest.main()
