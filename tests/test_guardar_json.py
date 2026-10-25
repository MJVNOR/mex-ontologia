import json,sys,tempfile,unittest,os
from pathlib import Path
from unittest.mock import patch
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())
STAGING=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(STAGING if STAGING.exists() else ROOT/'scripts'))
from guardar_rdf import escribir_json_atomico
class GuardarJSONTest(unittest.TestCase):
    def test_publica_json_completo_con_lexico(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reporte.json';p.write_bytes(b'anterior')
            value={'codigo':' 0001 á ','lista':[1,None,True]}
            escribir_json_atomico(value,p)
            self.assertEqual(json.loads(p.read_text(encoding='utf-8')),value)
            self.assertEqual(list(Path(d).iterdir()),[p])
    def test_serializacion_fallida_conserva_anterior(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reporte.json';p.write_bytes(b'anterior')
            with self.assertRaises(TypeError): escribir_json_atomico({'no_json':object()},p)
            self.assertEqual(p.read_bytes(),b'anterior')
            self.assertEqual(list(Path(d).iterdir()),[p])
    def test_bloqueo_reemplazo_conserva_anterior(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reporte.json';p.write_bytes(b'anterior')
            with patch('guardar_rdf.os.replace',side_effect=PermissionError('bloqueado')):
                with self.assertRaises(PermissionError): escribir_json_atomico({'nuevo':1},p)
            self.assertEqual(p.read_bytes(),b'anterior')
            self.assertEqual(list(Path(d).iterdir()),[p])
    def test_bloqueo_windows_transitorio_se_reintenta(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reporte.json';p.write_bytes(b'anterior')
            real_replace=os.replace
            calls=[]
            def replace(source,destination):
                calls.append(1)
                if len(calls)==1:
                    error=PermissionError('comparticion temporal');error.winerror=32
                    raise error
                return real_replace(source,destination)
            with patch('guardar_rdf.os.replace',side_effect=replace), patch('guardar_rdf.time.sleep') as sleep:
                escribir_json_atomico({'nuevo':1},p)
            self.assertEqual(json.loads(p.read_text(encoding='utf-8')),{'nuevo':1})
            self.assertEqual(len(calls),2)
            sleep.assert_called_once()
            self.assertEqual(list(Path(d).iterdir()),[p])
    def test_bloqueo_windows_persistente_tiene_limite_y_conserva_anterior(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reporte.json';p.write_bytes(b'anterior')
            error=PermissionError('comparticion persistente');error.winerror=5
            with patch('guardar_rdf.os.replace',side_effect=error) as replace, patch('guardar_rdf.time.sleep'):
                with self.assertRaises(PermissionError): escribir_json_atomico({'nuevo':1},p)
            self.assertGreater(replace.call_count,1)
            self.assertLessEqual(replace.call_count,10)
            self.assertEqual(p.read_bytes(),b'anterior')
            self.assertEqual(list(Path(d).iterdir()),[p])
if __name__=='__main__': unittest.main()
