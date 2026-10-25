import json,sys,tempfile,unittest
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
if __name__=='__main__': unittest.main()
