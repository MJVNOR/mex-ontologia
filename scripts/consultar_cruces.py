"""Filtra el mapa y muestra evidencia de un par, sin consultar filas del portal."""
import argparse
import json
from construir_catalogo import ROOT
from integrar_contenido import clave


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--buscar', default='', help='Texto del título de cualquiera de los conjuntos')
    parser.add_argument('--estado', choices=['candidata_por_validar', 'exploratorio_ejecutado', 'sin_clave_detectada', 'solo_dimensiones_amplias_o_tiempo'])
    parser.add_argument('--id', help='Identificador del par para mostrar toda su evidencia')
    parser.add_argument('--limite', type=int, default=20)
    args = parser.parse_args()
    if args.limite < 1:
        parser.error('--limite debe ser positivo')
    report = json.loads((ROOT / 'data/portal/oportunidades-cruce.json').read_text(encoding='utf-8'))
    rows = [p for p in report['pares'] if (not args.id or p['id'] == args.id)
            and (not args.estado or p['estado'] == args.estado)
            and clave(args.buscar) in clave(p['titulo_a'] + ' ' + p['titulo_b'])]
    if args.id:
        if not rows:
            parser.error('No se encontró ese par con los filtros indicados')
        result = dict(rows[0])
        result['perfil_a'] = report['perfiles'][result['conjunto_a']]
        result['perfil_b'] = report['perfiles'][result['conjunto_b']]
    else:
        result = {'coincidencias': len(rows), 'mostradas': min(args.limite, len(rows)),
                  'pares': [{k: v for k, v in row.items() if k in ('id', 'titulo_a', 'titulo_b', 'estado', 'prioridad_revision', 'familias_compartidas')}
                            for row in rows[:args.limite]]}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
