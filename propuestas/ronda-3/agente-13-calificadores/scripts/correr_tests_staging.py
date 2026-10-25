"""Ejecuta la propuesta de tests centrales (staging/test_semantica.py) contra el
staging parcheado, en una estructura temporal que imita tests/ + ontologia/.
Todo dentro de la carpeta propia. No toca el núcleo."""
import shutil
import sys
import unittest
from pathlib import Path

A13 = Path(__file__).resolve().parents[1]
ROOT = A13.parents[2]
TMP = A13 / "tmp_check"
sys.dont_write_bytecode = True
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(A13 / "staging"))

if TMP.exists():
    shutil.rmtree(TMP)
(TMP / "tests").mkdir(parents=True)
(TMP / "ontologia").mkdir(parents=True)
shutil.copy(A13 / "staging" / "test_semantica.py", TMP / "tests" / "test_semantica.py")
shutil.copy(ROOT / "ontologia" / "semantica.json", TMP / "ontologia" / "semantica.json")

loader = unittest.TestLoader()
suite = loader.discover(start_dir=str(TMP / "tests"), pattern="test_semantica.py",
                        top_level_dir=str(TMP / "tests"))
res = unittest.TextTestRunner(verbosity=1).run(suite)
shutil.rmtree(TMP, ignore_errors=True)
print("proposed-central-tests:", "OK" if res.wasSuccessful() else "FAIL",
      "ran=%d errors=%d failures=%d" % (res.testsRun, len(res.errors), len(res.failures)))
sys.exit(0 if res.wasSuccessful() else 1)
