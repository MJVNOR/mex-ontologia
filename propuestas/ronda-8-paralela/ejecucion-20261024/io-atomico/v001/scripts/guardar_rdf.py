"""Publica un Turtle completo sin truncar el archivo que otro proceso puede leer."""
import os
from pathlib import Path
import tempfile


def serializar_atomico(graph, destination):
    destination = Path(destination)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=destination.name + '.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            graph.serialize(destination=stream, format='turtle', encoding='utf-8')
        os.replace(temporary, destination)
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
        os.replace(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
