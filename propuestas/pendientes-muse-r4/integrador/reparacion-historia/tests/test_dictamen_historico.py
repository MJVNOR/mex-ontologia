import copy
import unittest

from integrar_ronda_2 import validar_estado_dictamen

class DictamenHistoricoTest(unittest.TestCase):
    def setUp(self):
        self.decision={'definicion_iri':'def-1','huella_fila_diccionario':'fila-1'}
        self.variable={**self.decision,'estado':'candidata_sin_definicion_suficiente'}
        self.rule={'id':'r4-1','concepto':'nuevo','huella_fila_diccionario':'fila-1'}
        self.approved={'def-1':self.rule}

    def test_pendiente_original_no_es_promovido(self):
        self.assertFalse(validar_estado_dictamen(self.variable,self.decision,{}))
        self.assertEqual(self.variable['estado'],'candidata_sin_definicion_suficiente')

    def test_resolucion_posterior_exige_regla_exacta(self):
        self.variable.update(estado='respaldada_por_definicion',regla='r4-1',concepto='nuevo')
        self.assertTrue(validar_estado_dictamen(self.variable,self.decision,self.approved))
        with self.assertRaises(ValueError):
            validar_estado_dictamen(self.variable,self.decision,{})
        for field in ['regla','concepto','definicion_iri','huella_fila_diccionario']:
            changed=copy.deepcopy(self.variable)
            changed[field]='otra'
            with self.subTest(field=field),self.assertRaises(ValueError):
                validar_estado_dictamen(changed,self.decision,self.approved)

    def test_huella_de_aprobacion_y_estado_no_se_omiten(self):
        self.variable.update(estado='respaldada_por_definicion',regla='r4-1',concepto='nuevo')
        altered={'def-1':dict(self.rule,huella_fila_diccionario='otra')}
        with self.assertRaises(ValueError):
            validar_estado_dictamen(self.variable,self.decision,altered)
        self.variable['estado']='fuera_del_nucleo_actual'
        with self.assertRaises(ValueError):
            validar_estado_dictamen(self.variable,self.decision,self.approved)

if __name__=='__main__':
    unittest.main()
