"""Prueba de origen del literal a–o (U+2013): recalcula la huella de esquema.

huella_esquema e0437c5f... = sha256(json([{nombre,tipo}...])) sobre los campos
datastore del inventario (consolidar_semantica.columnas). Resultado:
- con los campos tal cual estan en el inventario ('a–o', U+2013) la huella
  coincide con la fijada -> el pipeline central es fiel al datastore;
- sustituyendo por 'año' (U+00F1) la huella difiere -> 'a–o' no es artefacto
  de nuestros lectores (tablas() daria 'año' por cp1252; ademas este recurso
  se inspecciono por metodo api_esquema_previo, sin lectura de archivo).
Conclusion: la divergencia archivo (latin-1 'año', bytes 61 F1 6F) vs
datastore ('a–o', U+2013) esta del lado del publicador (ingesta CKAN).
"""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[4]
FIJADA = "e0437c5f0c9a47bc7ac43aa296e8bc62125574b141e284834303e55fd3ecde32"
inv = json.loads((BASE / "data/portal/inventario.json").read_text(encoding="utf-8"))
r = next(x for x in inv["recursos"] if x["id"] == "ffca84a8-155e-41af-8223-0e098966cadf")
campos = [f for f in r["datastore"]["campos"] if not f["id"].startswith("_")]
print("codepoints campo 2:", [hex(ord(c)) for c in campos[1]["id"]])


def huella(value):
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")).hexdigest()


h_tal_cual = huella([{"nombre": f["id"], "tipo": f.get("type")} for f in campos])
print("huella inventario tal cual:", h_tal_cual)
print("coincide con fijada:", h_tal_cual == FIJADA)
alt = [dict(f) for f in campos]
alt[1]["id"] = "año"
h_ano = huella([{"nombre": f["id"], "tipo": f.get("type")} for f in alt])
print("huella con 'año' (U+00F1):", h_ano)
print("difiere de la fijada:", h_ano != FIJADA)
