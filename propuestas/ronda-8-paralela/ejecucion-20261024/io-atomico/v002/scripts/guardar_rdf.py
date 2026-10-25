"""Publica un Turtle completo sin truncar el archivo que otro proceso puede leer."""
import os
import time
from pathlib import Path
import tempfile


def serializar_atomico(graph, destination):
    destination = Path(destination)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=destination.name + '.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            graph.serialize(destination=stream, format='turtle', encoding='utf-8')
        _reemplazar_con_reintentos(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def escribir_json_atomico(value, destination):
    """Publica JSON completo por reemplazo, sin truncar la versión previa."""
    import json
    destination = Path(destination)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                dir=destination.parent, prefix=destination.name + '.',
                suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        _reemplazar_con_reintentos(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


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
