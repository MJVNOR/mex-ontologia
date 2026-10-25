"""Regresión: ejecutar el CLI instalado en reports sin sobrescribir fuentes."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'config.toml').is_file())
E=ROOT/'propuestas/ampliacion-post-r9/ejecucion-20261024'
CANDIDATO=E/'K-publicador/v001/scripts/publicar_top50_r9.py'
SCRIPT=ROOT/'scripts/publicar_top50_r9.py' if Path(__file__).parent==ROOT/'tests' else CANDIDATO
spec=importlib.util.spec_from_file_location('publicador_regresion',SCRIPT)
pub=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)

class PublicadorInstaladoTest(unittest.TestCase):
    def test_cli_instalado_reports_y_fuentes_intactas(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for rel in [*pub.FUENTES.values(),'pyproject.toml']:
                dest=root/rel
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/rel,dest)
            installed=root/'scripts/publicar_top50_r9.py'
            installed.parent.mkdir()
            shutil.copyfile(SCRIPT,installed)
            foto=lambda:{rel:(hashlib.sha256((root/rel).read_bytes()).hexdigest(),(root/rel).stat().st_mtime_ns) for rel in pub.FUENTES.values()}
            antes=foto()
            res=subprocess.run([sys.executable,str(installed)],cwd=root,capture_output=True,text=True,
                env={**os.environ,'PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'})
            self.assertEqual(res.returncode,0,res.stderr)
            self.assertEqual(foto(),antes)
            for suffix in ('.json','.md','.html'):
                self.assertEqual((root/'reports'/(pub.NOMBRE+suffix)).read_bytes(),
                    (E/'T-top50/v002'/(pub.NOMBRE+suffix)).read_bytes())
            result=json.loads((root/'reports'/(pub.NOMBRE+'.json')).read_text(encoding='utf-8'))
            self.assertEqual(len(result['filas']),50)

    def test_destinos_fuentes_y_sellados_siguen_prohibidos(self):
        for target in [ROOT/'data/portal',E/'T-top50/v001']:
            with self.subTest(target=str(target)):
                with self.assertRaises(SystemExit):
                    pub._comprobar_destino(ROOT,target)

if __name__=='__main__':
    unittest.main()
