"""Prueba A1-911: ejecuta el script y exige salida con bloqueo documentado."""
import subprocess
import sys

R = ("propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v001/"
     "scripts/comprobar_a1_911.py")
p = subprocess.run([sys.executable, R], capture_output=True, text=True)
assert p.returncode == 0, p.stderr[-2000:]
assert '"lote_decision": "requiere_revision"' in p.stdout
assert '"alcance_ejecucion": "No ejecutado"' in p.stdout
assert "duplicado_q1_mismo_sha" in p.stdout
assert "sin muestra" not in p.stdout  # el negativo se afirma en entrega.json
print("test_a1_911 OK")
