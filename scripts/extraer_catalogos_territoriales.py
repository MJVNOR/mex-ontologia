"""Lee solo catálogos territoriales publicados; conserva celdas y codificación originales."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/territorio'
LAYOUTS = {
    'Catalogo_Estado': ('entidad', 'CLAVE_ENT', 'NOM_ENT', None),
    'Catalogo_Municipios': ('municipio_compuesto', 'CLAVE', 'NOM_MUN', 'CLAVE_ENT'),
    'Municipios': ('municipio_local', 'MUNI', 'MUNICIPIOS', None),
    'cat_municipio': ('municipio_compuesto', 'Cve. Municipio', 'Municipio', None),
    'cat_entidad': ('entidad', 'Clave_Ent', 'Entidad', None),
}


def codigo(value):
    """Keep text zeroes. Only integral finite positive numeric IDs are accepted."""
    if isinstance(value, bool) or value is None:
        raise ValueError('Código vacío o booleano')
    if isinstance(value, (int, float)):
        if not (value >= 0 and value < 10**12 and int(value) == value):
            raise ValueError('Código numérico no entero o fuera de rango')
        return str(int(value))
    if not isinstance(value, str) or not value.isascii() or not value.isdigit():
        raise ValueError('Código textual no numérico: ' + repr(value))
    return value


def extraer(path, resource, sheets):
    records = []
    book = openpyxl.load_workbook(path, read_only=True, data_only=False)
    try:
        for sheet_name in sheets:
            level, code_field, name_field, parent_field = LAYOUTS[sheet_name]
            sheet = book[sheet_name]
            iterator = sheet.iter_rows()
            header = [c.value for c in next(iterator)]
            for field in [code_field, name_field, *([parent_field] if parent_field else [])]:
                if header.count(field) != 1:
                    raise ValueError('Encabezado no único o ausente: ' + field)
            code_index, name_index = header.index(code_field), header.index(name_field)
            rows, all_count = [], 0
            seen = set()
            for row_number, cells in enumerate(iterator, 2):
                if not any(c.value is not None for c in cells):
                    continue
                all_count += 1
                if all_count > 20000:
                    raise ValueError('Catálogo excede presupuesto de lectura; no se presenta como completo')
                indexes = [code_index, name_index] + ([header.index(parent_field)] if parent_field else [])
                if any(cells[i].data_type == 'f' for i in indexes):
                    raise ValueError('Código o nombre depende de fórmula no evaluada')
                code = codigo(cells[code_index].value)
                if code in seen:
                    raise ValueError('Clave repetida dentro de la referencia: ' + code)
                seen.add(code)
                name = cells[name_index].value
                if not isinstance(name, str) or not name.strip():
                    raise ValueError('Nombre vacío')
                parent = codigo(cells[header.index(parent_field)].value) if parent_field else None
                # Retain only Sonora in national municipality tables; scan all rows.
                if level == 'municipio_compuesto' and parent_field and parent != '26':
                    continue
                if level == 'municipio_local' and not 1 <= int(code) <= 72:
                    raise ValueError('Código local municipal fuera de 1..72')
                if level == 'municipio_compuesto' and not code.startswith('26'):
                    raise ValueError('Código seleccionado fuera de Sonora')
                rows.append({'codigo': code, 'nombre': name, 'entidad': parent,
                             'fila': row_number, 'celda_codigo': cells[code_index].coordinate,
                             'celda_nombre': cells[name_index].coordinate,
                             'tipo_celda_codigo': cells[code_index].data_type,
                             'formato_celda_codigo': cells[code_index].number_format})
            records.append({'recurso': resource['id'], 'conjunto': resource['conjunto_id'], 'titulo_conjunto': resource['conjunto'],
                            'fuente': resource['url'], 'hoja': sheet_name, 'nivel': level,
                            'campo_codigo': code_field, 'campo_nombre': name_field, 'campo_entidad': parent_field,
                            'posicion_codigo': code_index + 1,
                            'filas_completas_leidas': all_count, 'filas_retenidas': len(rows),
                            'alcance': 'Sonora' if level != 'entidad' else 'Todas las entidades publicadas',
                            'archivo_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                            'archivo': str(path.relative_to(ROOT)), 'entradas': rows})
    finally:
        book.close()
    return records


def descargar(url, path):
    with urlopen(Request(url, headers={'User-Agent': 'MEX-Ontologi/0.4 (territorial references)'}), timeout=40) as response:
        if response.status != 200:
            raise ValueError('Respuesta HTTP incompleta')
        data = response.read(12 * 1024 * 1024 + 1)
    if len(data) > 12 * 1024 * 1024:
        raise ValueError('Archivo excede presupuesto de lectura')
    path.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    inventory_path = ROOT / 'data/portal/inventario.json'
    inspection_path = ROOT / 'data/portal/contenido-inspeccion.json'
    inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
    inspections = {r['id']: r for r in json.loads(inspection_path.read_text(encoding='utf-8'))['recursos']}
    folder = OUT / 'fuentes'
    folder.mkdir(parents=True, exist_ok=True)
    refs = []
    for resource in inventory['recursos']:
        if resource['nombre'].casefold() not in {'catalogo', 'catálogo'}:
            continue
        sheets = [t['hoja'] for t in inspections[resource['id']].get('tablas', []) if t['hoja'] in LAYOUTS]
        if not sheets:
            continue
        path = folder / (resource['id'] + '.xlsx')
        if args.refresh or not path.exists():
            descargar(resource['url'], path)
        refs.extend(extraer(path, resource, sheets))
    result = {'generado_en_utc': datetime.now(timezone.utc).isoformat(), 'referencias': refs,
              'huellas_entrada': {'inventario': hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
                                  'inspeccion': hashlib.sha256(inspection_path.read_bytes()).hexdigest()}}
    (OUT / 'catalogos.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'archivos': len({r['recurso'] for r in refs}), 'referencias': len(refs),
                      'entradas_retenidas': sum(len(r['entradas']) for r in refs)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
