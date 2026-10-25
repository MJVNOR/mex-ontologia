"""Dos pruebas históricas deben validar el estado vigente por la cadena R4→R8."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
out=E/'ajuste-tests/v001'
assert not out.exists()
out.mkdir(parents=True)
changes=[('test_ronda_3_integrada.py',"validar_extension_vinculos(_reglas_era_r7(self.rules), self.previous)","validar_extension_vinculos(self.rules, self.previous)"),('test_ronda_7.py',"R7.construir(self.report, _reglas_era_r7(self.rules), base_iri)","R7.construir(self.report, self.rules, base_iri)")]
for name,old,new in changes:
    text=(ROOT/'tests'/name).read_text(encoding='utf-8')
    assert text.count(old)==1
    text=text.replace(old,new)
    text=text.replace('# Sobre la era R7 (el constructor R7 no conoce R8 por diseño).','# La cadena vigente R4→R8 valida el lote completo y conserva el prefijo R7.')
    text=text.replace('# v002: la cadena R4→R7 no conoce R8; se valida sobre la era R7\n        # (vivo menos delta R8 validado). La equivalencia vivo = era + R8\n        # la prueba la aritmética pinnada de test_ronda_7.','# La cadena vigente valida R8 y comprueba por separado el prefijo histórico\n        # R3. Sus aserciones de 836+29 se conservan íntegras.')
    (out/name).write_text(text,encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
(out/'congelada.json').write_text(json.dumps({'motivo':'La cadena histórica ya delega R8; validar la foto R7 sin sus 28 adiciones produce un rechazo legítimo. Se pasa el estado vigente a los validadores y se conservan las aserciones históricas.','archivos':[{'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(out.glob('*.py'))]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(out))
