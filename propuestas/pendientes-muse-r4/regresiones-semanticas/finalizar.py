"""Finaliza: compuertas estructurales + entrega.json + resultado.md + listo.json."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas' / 'pendientes-muse-r4'
OUT = STAGE / 'regresiones-semanticas'
import sys
sys.path.insert(0, str(STAGE / 'integrador' / 'codigo' / 'scripts'))
sys.path.append(str(ROOT / 'scripts'))
from consolidar_semantica import validar_calificador  # noqa: E402

RESULTS = json.loads((OUT / '_todos.json').read_text(encoding='utf-8'))


def caso(suite, cid, descripcion, esperado, ok, observacion=''):
    RESULTS.append({'suite': suite, 'id': cid, 'descripcion': descripcion,
                    'esperado': esperado, 'resultado': 'aprobado' if ok else 'fallido',
                    'observacion': observacion})


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


base = json.loads((ROOT / 'ontologia' / 'semantica.json').read_text(encoding='utf-8'))
merged_con = dict(base['conceptos'])
nuevas = []
cuentas = {}
for i in range(1, 7):
    d = json.loads((STAGE / f'lote-{i}' / 'entrega.json').read_text(encoding='utf-8'))
    cuentas[f'lote-{i}'] = {'reglas': len(d.get('reglas', [])), 'vinculos': len(d.get('vinculos', [])),
                            'coldec': len(d.get('decisiones_columnas', [])),
                            'sigdec': len(d.get('decisiones_significados', []))}
    nuevas.extend(d.get('reglas', []))
    for k, v in d.get('conceptos_nuevos', {}).items():
        merged_con[k] = v
assert len(nuevas) == 172, len(nuevas)
assert sum(c['sigdec'] for c in cuentas.values()) == 351, cuentas
nv = sum(c['vinculos'] for c in cuentas.values())
assert nv == 3596, nv  # +5 PIN ambiguos = 3601
lista_ids = {}
for i in range(1, 7):
    d = json.loads((STAGE / f'lote-{i}' / 'entrega.json').read_text(encoding='utf-8'))
    for r in d.get('reglas', []):
        lista_ids[r['id']] = {'lote': f'lote-{i}', 'definicion': r['definiciones'][0],
                              'concepto': r['concepto'], 'representacion': r.get('representacion')}
(OUT / 'lista-ids-172.json').write_text(json.dumps(lista_ids, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

# F: compuertas estructurales sobre las 175 reglas y conceptos nuevos
una_def = [r['id'] for r in nuevas if len(r.get('definiciones', [])) != 1]
caso('F-estructura', 'F-una-fila', 'cada regla restringida a exactamente una fila',
     '175 con 1 definicion', not una_def, '' if not una_def else str(una_def[:5]))

mal_fmt = [k for k, v in merged_con.items() if not (isinstance(v, list) and len(v) == 3)]
caso('F-estructura', 'F-concepto-formato', 'conceptos nuevos con formato [etiqueta, definicion, padre]',
     'formato valido', not mal_fmt, '' if not mal_fmt else str(mal_fmt[:5]))

def linaje(k):
    seen = set()
    while k is not None:
        if k in seen or k not in merged_con:
            return False
        seen.add(k)
        k = merged_con[k][2]
    return True
mal_lin = [k for k in merged_con if not linaje(k)]
caso('F-estructura', 'F-linaje', 'padres existen y sin ciclos', 'linaje valido', not mal_lin,
     '' if not mal_lin else str(mal_lin[:5]))

tocados = [k for k in base['conceptos'] if k in merged_con and merged_con[k] != base['conceptos'][k]]
caso('F-estructura', 'F-base-intacta', 'ningun concepto de base alterado', 'base intacta',
     not tocados, '' if not tocados else str(tocados[:5]))

mal_cal = []
for r in nuevas:
    if r.get('calificador'):
        try:
            validar_calificador(r['calificador'])
        except ValueError as e:
            mal_cal.append((r['id'], str(e)[:120]))
caso('F-estructura', 'F-calificadores', 'calificadores con dimensiones/valores no vacios',
     'calificadores validos', not mal_cal, '' if not mal_cal else str(mal_cal[:5]))

sin_rep = [r['id'] for r in nuevas if not r.get('representacion')]
caso('F-estructura', 'F-representacion', 'toda regla declara representacion', '175 con representacion',
     not sin_rep, '' if not sin_rep else str(sin_rep[:5]))
sin_lim = [r['id'] for r in nuevas if not r.get('limites') and not r.get('limite')]
caso('F-estructura', 'F-limites', 'toda regla declara limites', '175 con limites',
     not sin_lim, '' if not sin_lim else str(sin_lim[:5]))

# entradas con sha
entradas = {}
for p in ['ontologia/semantica.json', 'data/semantica/cobertura.json',
          'data/portal/inventario.json', 'data/portal/contenido-inspeccion.json',
          'data/portal/lote-cruces/catalogo-municipal-portal.json',
          'scripts/consolidar_semantica.py', 'scripts/integrar_contenido.py',
          'propuestas/pendientes-muse-r4/integrador/codigo/scripts/consolidar_semantica.py',
          'propuestas/pendientes-muse-r4/integrador/codigo/scripts/integrar_ronda_3.py',
          'propuestas/pendientes-muse-r4/integrador/codigo/scripts/integrar_ronda_4.py',
          'propuestas/pendientes-muse-r4/ambiguedades/entrega.json'] + \
         [f'propuestas/pendientes-muse-r4/lote-{i}/entrega.json' for i in range(1, 7)]:
    entradas[p] = sha(ROOT / p)

fallidos = [r for r in RESULTS if r['resultado'] == 'fallido']
por_suite = {}
for r in RESULTS:
    por_suite.setdefault(r['suite'], [0, 0])
    por_suite[r['suite']][1] += 1
    por_suite[r['suite']][0] += r['resultado'] == 'aprobado'

entrega = {
    'rol': 'regresiones-semanticas',
    'alcance': '172 reglas finales lote-1..6 (18+21+43+37+23+30), 351 decisiones de significado, 3601 vinculos (3596+5 PIN); generador preparado integrador/codigo/scripts',
    'pre_reentrega': 'pre-reentrega/entrega-175.json: instantanea anterior valida (1456 casos/175 reglas), archivada; no es resultado final',
    'cuentas_lotes': cuentas,
    'generador': 'propuestas/pendientes-muse-r4/integrador/codigo/scripts/consolidar_semantica.py',
    'entradas': entradas,
    'casos': [{'id': r['id'], 'suite': r['suite'], 'descripcion': r['descripcion'], 'esperado': r['esperado']}
              for r in RESULTS],
    'resultados': {
        'casos_ejecutados': len(RESULTS),
        'aprobados': len(RESULTS) - len(fallidos),
        'fallidos': len(fallidos),
        'por_suite': {k: {'aprobados': v[0], 'ejecutados': v[1]} for k, v in por_suite.items()},
        'detalle': [{'id': r['id'], 'resultado': r['resultado'], 'observacion': r['observacion']} for r in RESULTS],
    },
    'hallazgos_bloqueantes': [
        {'id': r['id'], 'descripcion': r['descripcion'], 'observacion': r['observacion']} for r in fallidos
    ],
    'limites': [
        'La propuesta combinada se construye sin instalar: no modifica ontologia/, data/, scripts/ ni integrador/.',
        'Los 5 PIN ambiguos exigen el generador preparado (definicion_iri); el nucleo instalado los rechaza.',
        'Suite E/D sinteticas usan muestras minimas pero el mismo codigo (construir/interpretacion); D incluye 4 mutaciones sobre datos reales.',
        'No se valida contenido de filas ni valores: solo que la regla alcanza su fila y ninguna ajena.',
        'Normalizacion intencional (acentos/case) verificada como conservadora de regla; no como equivalencia entre filas.',
        'Correcciones de conceptos/representaciones/limites en lotes 2/3/4/6 verificadas sobre archivos finales; sin copia previa de entregas no hay dif de contenido, solo conducta final.',
        'Retiradas r4-lote-4-025/026/027: sus definiciones no quedan respaldadas y sus 3 columnas no quedan revisadas (suite G + columna control).',
    ],
}
(OUT / 'entrega.json').write_text(json.dumps(entrega, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
(OUT / 'resultados.json').write_text(json.dumps(RESULTS, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

lineas = ['# Regresiones semanticas r4 (final)', '',
          '172 reglas finales (lote-1..6: 18+21+43+37+23+30), 351 decisiones de significado, 3601 vinculos (3596+5 PIN).',
          'Lote-4 retiro 3 contradicciones reales (r4-lote-4-025/026/027); correcciones de conceptos/representaciones/limites en 2/3/4/6 verificadas sobre archivos finales.',
          'Informe anterior 1456/175 archivado en `pre-reentrega/` como instantanea valida; no es el resultado final.',
          'Generador preparado `integrador/codigo/scripts`; combinada construida sin instalar, solo fuentes locales.',
          '', '## Cuentas verificadas', '']
for suite, (ok, tot) in sorted(por_suite.items()):
    lineas.append(f'- {suite}: {ok}/{tot} aprobados')
lineas += ['', f'Total: {len(RESULTS)-len(fallidos)}/{len(RESULTS)} aprobados, {len(fallidos)} fallidos.',
           f'Hallazgos bloqueantes: {len(fallidos)}.',
           '', '## Que verifica cada suite (conducta, no conteos)', '',
           '- A-alcance: cada regla aplica a su fila exacta; mutando conjunto/diccionario/definicion/nombre/descripcion no alcanza otra fila.',
           '- B-normalizacion: mayusculas/sin acentos conservan la regla; sentidos confundibles (mismo nombre/descripcion) discriminan.',
           '- C-preservacion: 1212 significados y 865 vinculos intactos, 175 reglas y vinculos nuevos materializados, ninguna promocion ajena, 5 PIN resueltos.',
           '- D-esquema: huella_esquema/huella_fila/descripcion/diccionario alterados abortan.',
           '- E-duplicadas: columna duplicada, regla duplicada, pin sin columna, pin incompleto, nombre ambiguo sin pin y concepto ajeno se rechazan.',
           '- F-estructura: una fila por regla, formato/linaje de conceptos, base intacta, calificadores, representacion y limites.',
           '- G-retiradas: IDs retirados ausentes, sus 3 definiciones no respaldadas, sus 3 columnas no revisadas (+1 columna control por observacion).',
           '', '## Limites', '']
lineas += [f'- {x}' for x in entrega['limites']] + ['']
(OUT / 'resultado.md').write_text('\n'.join(lineas), encoding='utf-8')
(OUT / 'listo.json').write_text(json.dumps(
    {'sha256': sha(OUT / 'entrega.json'), 'casos': len(RESULTS),
     'fallidos': len(fallidos), 'reglas': 172, 'decisiones_significado': 351,
     'vinculos': 3601}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('casos:', len(RESULTS), 'fallidos:', len(fallidos))
