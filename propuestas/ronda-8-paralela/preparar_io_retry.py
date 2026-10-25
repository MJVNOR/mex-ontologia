from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
out=E/'io-atomico/v002';assert not out.exists()
(out/'scripts').mkdir(parents=True);(out/'tests').mkdir()
code=(ROOT/'scripts/guardar_rdf.py').read_text(encoding='utf-8')
assert code.count('os.replace(temporary, destination)')==2
code=code.replace('import os\n','import os\nimport time\n',1).replace('os.replace(temporary, destination)','_reemplazar_con_reintentos(temporary, destination)')
code+='''

def _reemplazar_con_reintentos(source, destination):
    """Espera brevemente bloqueos de compartición de Windows; conserva errores."""
    pausas = (0.05, 0.1, 0.25, 0.5, 1, 2, 4, 8, 16)
    for intento in range(len(pausas) + 1):
        try:
            os.replace(source, destination)
            return
        except OSError as error:
            if getattr(error, 'winerror', None) not in (5, 32, 1224) or intento == len(pausas):
                raise
            time.sleep(pausas[intento])
'''
(out/'scripts/guardar_rdf.py').write_text(code,encoding='utf-8')
code=(ROOT/'tests/test_guardar_json.py').read_text(encoding='utf-8')
code=code.replace('import json,sys,tempfile,unittest','import json,sys,tempfile,unittest,os',1)
extra='''    def test_bloqueo_windows_transitorio_se_reintenta(self):
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
'''
marker="if __name__=='__main__': unittest.main()";assert code.count(marker)==1
code=code.replace(marker,extra+marker)
(out/'tests/test_guardar_json.py').write_text(code,encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
(out/'congelada.json').write_text(json.dumps({'alcance':'Reintentos limitados a 31.9 s acumulados sólo para WinError5/32/1224; errores restantes inmediatos; publicación atómica preserva versión previa.','archivos':[{'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(out.rglob('*.py'))]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(out))
