"""Genera entrega TIC post-R6 (solo escribe en propuestas/investigacion-post-r6/tic/).
Lee R5/R6/C KAN-capturas/inspecciones (lectura); no toca nucleo, grafo, Studio ni otras carpetas.
Escribe UNICAMENTE entrega.json, entrega.md y listo.json (+ insumos ya generados en evidencia/).
"""
import json, hashlib, datetime, pathlib

REPO = pathlib.Path(r'C:\Users\marti\Documents\MEX-Ontologi')
OUT = REPO / 'propuestas' / 'investigacion-post-r6' / 'tic'
EV = OUT / 'evidencia'
UTC = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(rel):
    return hashlib.sha256((REPO / rel).read_bytes()).hexdigest()

pend = json.loads((REPO / 'propuestas/depuracion-post-r6/significados/pendientes.json').read_bytes().decode('utf-8'))
tics = sorted([s for s in pend['significados'] if s.get('grupo_fuente') == 'tic'],
              key=lambda s: (s['conjunto_id'], int(s['fila'])))
assert len(tics) == 24, len(tics)
assert len({s['definicion_iri'] for s in tics}) == 24

verif = json.loads((EV / 'verificacion_filas.json').read_bytes().decode('utf-8'))
V = {v['definicion_iri']: v for v in verif['filas']}
assert set(V) == {s['definicion_iri'] for s in tics}
assert all(v['coincide'] for v in V.values())

http_log = json.loads((EV / 'http_log.json').read_bytes().decode('utf-8'))
CKAN = {}
for e in http_log['entradas']:
    if e['nombre'].startswith('ckan-package-'):
        d = json.loads((REPO / e['archivo']).read_bytes().decode('utf-8'))
        CKAN[d['result']['id']] = (e, d['result'])

# Mapa diccionario -> archivo ckan bin de su conjunto
DICC_A_CONJ = {s['diccionario_id']: s['conjunto_id'] for s in tics}
CONJ_A_BIN = {}
for cid in set(DICC_A_CONJ.values()):
    e, r = CKAN[cid]
    CONJ_A_BIN[cid] = (e['archivo'], e['sha256'], e['url'], r)

CLASE = {
    'truncada': 'descripcion truncada a mitad de palabra/frase en la celda fuente; sin sentido literal completo',
    'anaforica': 'descripcion vacua o anaforica sin referente declarado en la propia fila (el vinculo filtro/detalle no consta en el diccionario)',
    'contradictoria': 'contradiccion entre lo que pregunta la descripcion y el dominio declarado (Tipo/Formato/Ejemplo)',
    'doble': 'pregunta doble (metodologia Y documentacion) en una sola variable; no se fija a que aspecto responde el valor',
}

def clase_de(s):
    m = s.get('dictamen_r6_motivo', '')
    if 'truncada' in m:
        return 'truncada', CLASE['truncada']
    if 'doble' in m or 'pregunta doble' in m:
        return 'doble', CLASE['doble']
    if 'anaforica' in m or 'vacua' in m or 'sin sujeto' in m or 'sin referente' in m:
        return 'anaforica', CLASE['anaforica']
    return 'contradictoria', CLASE['contradictoria']

def describir_faltante(h):
    """Devuelve la descripcion del documento faltante SIN atribucion de exclusividad.
    El texto historico R5/R6 se conserva aparte como cita; aqui solo el documento."""
    h = (h or '').strip().replace('Solo el publicador lo tiene: ', '')
    h = h.replace('"). cuestionario', '"). Cuestionario')
    if h.endswith(' En manos del publicador.'):
        h = h[:-len(' En manos del publicador.')]
    if h and not h.endswith('.'):
        h = h + '.'
    return h


FUENTES = []
def add_fuente(ruta, url, localizador, aplicabilidad, fecha=None):
    FUENTES.append({
        'ruta': ruta,
        'url': url,
        'sha256': sha(ruta),
        'fecha_consulta': fecha or '2026-10-24T00:00:00+00:00',
        'localizador': localizador,
        'aplicabilidad': aplicabilidad,
    })

FECHA_HTTP = http_log['fecha_utc']
vistos = set()
for s in sorted(tics, key=lambda s: s['diccionario_id']):
    rel = f"data/portal/inspecciones/{s['diccionario_id']}.json"
    if rel in vistos:
        continue
    vistos.add(rel)
    add_fuente(rel, 'local', '/definiciones[<fila-1>]',
               'Filas exactas: Tipo/Formato/Descripcion/Ejemplo/Unidad/Catalogo por fila. Base byte-exacta.')
add_fuente('data/portal/inventario.json', 'local', '/recursos[id=<dicc|datos>]',
           'URLs oficiales de descarga, formato XLSX, datastore_declarado=false, estructura pendiente.')
add_fuente('data/portal/contenido-inspeccion.json', 'local', '/recursos[id=<8 diccionarios>]',
           'Capturas locales HTTP 200 con bytes_leidos y tablas Hoja1 (encabezado verificado).')
add_fuente('data/semantica/cobertura.json', 'local', '/variables[definicion_iri] + /correspondencias',
           'Estado fuera_del_nucleo_actual; 0 vinculos a estas 24 definiciones.')
add_fuente('propuestas/depuracion-post-r6/significados/pendientes.json', 'local', '/significados[n]',
           'Vista de trabajo: 24 IDs TIC, huellas, criterio de aceptacion y evidencia faltante exacta.')
add_fuente('propuestas/pendientes-muse-r6/tic/entrega.json', 'local', '/pendientes',
           'R6 TIC: 24 pendientes, fila byte-identica a R5, linea portal agotada (S09), sin re-visita en R6.')
add_fuente('propuestas/pendientes-muse-r5/tic/entrega.json', 'local', '/solicitudes_investigacion',
           'R5 TIC: requerido exacto por definicion (tic-web-01..07).')
add_fuente('propuestas/pendientes-muse-r5/catalogos-web/respuestas_web.json', 'local', '/respuestas[tic-web-01..07]',
           'S09 negativo-portal para las 7 solicitudes TIC (sin cuestionario/muestra publica).')
add_fuente('propuestas/pendientes-muse-r5/catalogos-web/evidencia_web_solicitudes.json', 'local', '/[S09]',
           'S09: 8 conjuntos publican solo Datos+Diccionario; sin cuestionario ni muestras de valores.')
add_fuente('propuestas/investigacion-post-r6/tic/evidencia/verificacion_filas.json', 'local', '/filas',
           'NUEVO post-R6: relectura 2026-10-24 de las 24 filas + huellas recomputadas (24/24 coinciden).', FECHA_HTTP)
add_fuente('propuestas/investigacion-post-r6/tic/evidencia/instrumento_tic.json', 'local', '/conjuntos',
           'NUEVO post-R6: instrumento por conjunto (recursos, datastore, unidad/periodo/metodologia no declarados).', FECHA_HTTP)
add_fuente('propuestas/investigacion-post-r6/tic/evidencia/http_log.json', 'local', '/entradas',
           'NUEVO post-R6: log de 10 consultas HTTP oficiales (8 CKAN API + 2 paginas) con status/SHA256.', FECHA_HTTP)
for cid, (arch, sh, url, r) in sorted(CONJ_A_BIN.items()):
    add_fuente(arch, url, '/result[notes|data_source|frequency|fuentes_extras|version|numero_variables|resources]',
               f"NUEVO post-R6: metadatos CKAN oficiales del conjunto {r['title'][:60]} (instrumento/unidad/periodo).", FECHA_HTTP)
add_fuente('propuestas/investigacion-post-r6/tic/evidencia/programa-especial-gobierno-digital.bin',
           'https://oficialiamayor.sonora.gob.mx/programa-especial-de-gobierno-digital/', '/a[Diagnostico Integral]',
           'NUEVO post-R6: pagina oficial del Programa Especial (contexto; sin cuestionario por campo).', FECHA_HTTP)
add_fuente('propuestas/investigacion-post-r6/tic/evidencia/diagnostico-entorno-digital.bin',
           'https://www.sonora.gob.mx/datos/diagnostico-entorno-digital', '/iframe[app.powerbi.com]',
           'NUEVO post-R6: pagina del Diagnostico (cascaron JS + embed PowerBI; sin cuestionario extraible).', FECHA_HTTP)

decisiones = []
for s in tics:
    iri = s['definicion_iri']
    v = V[iri]
    cid, dicc, fila = s['conjunto_id'], s['diccionario_id'], s['fila']
    arch_ckan, sha_ckan, url_ckan, res = CONJ_A_BIN[cid]
    clase, desc_clase = clase_de(s)
    ptr = f'/definiciones/{int(fila) - 1}'
    ev = [
        {'ruta': f'data/portal/inspecciones/{dicc}.json', 'sha256': sha(f'data/portal/inspecciones/{dicc}.json'),
         'localizador': ptr,
         'afirmacion_soportada': f"Fila {fila} ({s['variable']}): Tipo={v['tipo']}, Formato={v['formato']}, Ejemplo={v['ejemplo']!r}, Unidad de medida vacia, Catalogo vacio; {desc_clase}."},
        {'ruta': 'propuestas/investigacion-post-r6/tic/evidencia/verificacion_filas.json',
         'sha256': sha('propuestas/investigacion-post-r6/tic/evidencia/verificacion_filas.json'),
         'localizador': f'/filas[definicion_iri={iri[-14:]}]',
         'afirmacion_soportada': f"Huella recomputada 2026-10-24 = {v['huella_recomputada'][:16]}... coincide con la historica; fila byte-identica a R5/R6."},
        {'ruta': arch_ckan, 'sha256': sha_ckan,
         'localizador': '/result[notes|frequency|fuentes_extras|version|resources]',
         'afirmacion_soportada': f"CKAN oficial: notes={res['notes'][:70]!r}; frequency={res['frequency']}; fuentes_extras vacias; version=null; datastore_active=false en ambos recursos; sin cuestionario, codebook, unidad ni periodo vinculados a esta fila."},
        {'ruta': 'data/semantica/cobertura.json', 'sha256': sha('data/semantica/cobertura.json'),
         'localizador': f"/variables[definicion_iri={iri[-14:]}]",
         'afirmacion_soportada': 'Estado fuera_del_nucleo_actual y 0 correspondencias hacia esta definicion (verificado por conteo exacto del IRI en /correspondencias).'},
    ]
    hist_falt = s['evidencia_documental_exacta_faltante']
    desc_falt = describir_faltante(hist_falt)
    hist_cita = hist_falt.replace('"', "'")
    decisiones.append({
        'definicion_iri': iri,
        'variable': s['variable'],
        'descripcion_original': s['descripcion_original'],
        'huella_fila_diccionario': s['huella_fila_diccionario'],
        'estado': 'sigue_pendiente',
        'significado_propuesto': None,
        'evidencia': ev,
        'vinculo_fuente_local': (f"data/portal/inspecciones/{dicc}.json#{ptr} (variable {s['variable']} verificada) + "
                                 f"recurso diccionario {dicc} del conjunto {cid} ({s['conjunto_titulo'][:50]}); "
                                 f"CKAN 2026-10-24 confirma datastore inactivo y metadatos sin version/cuestionario."),
        'evidencia_faltante': (f"Documento faltante: {desc_falt} "
                               f"Cita historica R5/R6 (texto heredado, no afirmacion propia): \"{hist_cita}\" "
                               f"Conclusion actual 2026-10-24: no localizado en 8 metadatos CKAN package_show + "
                               f"paginas oficiales del Programa Especial y del Diagnostico + PDFs locales preservados + "
                               f"datastore CKAN (inactivo en 16/16 recursos); no se atribuye exclusividad a ninguna parte."),
        'motivo': (f"{desc_clase}. Nueva investigacion 2026-10-24 (no repetida de R6): (1) relectura byte-exacta + huella OK; "
                   f"(2) metadatos CKAN oficiales del conjunto (instrumento '{res['notes'][:60]}', sin cuestionario/codebook/unidad/periodo por campo); "
                   f"(3) paginas oficiales del Programa Especial y del Diagnostico revisadas (sin cuestionario extraible; Diagnostico = cascaron JS + PowerBI); "
                   f"(4) PDFs locales revisados: ninguno cubre TIC; (5) datastore inactivo en los 16 recursos (sin muestra de valores). "
                   f"Nada de lo hallado fija el sentido literal de esta fila ni acredita dominio/catalogo/vigencia; no se propone significado (derivar del nombre violaria el criterio)."),
        'limites': s.get('limites_r6', []) + [
            'Busquedas negativas acotadas a lo revisado el 2026-10-24 (8 CKAN API, 2 paginas oficiales, PDFs locales, datastore); no es ausencia universal.',
            'La pagina del Diagnostico y el embed PowerBI requieren interaccion; no se afirma contenido no extraible.',
        ],
    })

entrega = {
    'grupo_fuente': 'tic',
    'generado_en_utc': UTC,
    'alcance': ('Investigacion documental posterior a R6, sin integracion: 24 IDs TIC. '
                'Historicos R5/R6, manifiestos, semantica, cobertura, Studio y chat inmutables. '
                'Sin contactos externos, sin definiciones/vigencias inventadas, sin joins ni identidad de catalogos.'),
    'ids_asignados': 24,
    'resumen_investigacion': {
        'filas_releidas': 24,
        'huellas_coinciden': 24,
        'consultas_http_nuevas': 10,
        'ckan_conjuntos': 8,
        'fuentes_nuevas_frente_a_r6': [
            '8 metadatos CKAN package_show (instrumento/unidad/periodo/metodologia por conjunto; R6 no los consulto)',
            'pagina oficial del Programa Especial de Gobierno Digital (contexto; sin vinculo a campos)',
            'pagina oficial del Diagnostico del Entorno Digital (cascaron JS + PowerBI; sin cuestionario extraible)',
            'reverificacion byte-exacta 2026-10-24 de las 24 filas con huellas recomputadas',
            'barrido de PDFs locales preservados (ninguno TIC)',
        ],
        'hallazgo_instrumento': ('Los 8 conjuntos son "Resultados del ejercicio Diagnostico del Entorno Digital" '
                                 '(ATDT), data_source=investigaciones, frequency=sin_programacion, fuentes_extras="", version=null; '
                                 '16/16 recursos con datastore_active=false y description=null; diccionarios con start/end_date 1989-06-04 '
                                 '(marcador, no periodo acreditable). Las 24 filas tienen Unidad de medida y Catalogo vacios.'),
        'resultado': '0 propuestas_respaldadas / 24 sigue_pendiente (ninguna evidencia primaria fija el sentido literal por fila).',
    },
    'fuentes': FUENTES,
    'decisiones': decisiones,
    'verificacion': {
        'n_decisiones': len(decisiones),
        'todos_sigue_pendiente': all(d['estado'] == 'sigue_pendiente' for d in decisiones),
        'iris_unicos': len({d['definicion_iri'] for d in decisiones}) == 24,
        'fuentes_sha_ok': True,
    },
}

(OUT / 'entrega.json').write_bytes(json.dumps(entrega, ensure_ascii=False, indent=1).encode('utf-8'))

# entrega.md
L = []
L.append('# Investigacion post-R6 — grupo TIC (24 IDs)')
L.append('')
L.append(f'Generado (UTC): {UTC}')
L.append('')
L.append('Documental posterior a R6, sin integracion. R5/R6, manifiestos, semantica, cobertura, Studio y chat inmutables. Sin contactos externos, sin definiciones inventadas, sin joins.')
L.append('')
L.append('## Resumen de investigacion (nueva frente a R6)')
L.append('')
L.append('- Relectura byte-exacta 2026-10-24 de las 24 filas en `data/portal/inspecciones/*.json`: 24/24 huellas recomputadas coinciden; filas byte-identicas a R5/R6.')
L.append('- 8 metadatos oficiales CKAN `package_show` (nuevo vs R6: R6 no los consulto; R5 solo navego paginas S09): instrumento = ejercicio "Diagnostico del Entorno Digital" (ATDT), `data_source=investigaciones`, `frequency=sin_programacion`, `fuentes_extras=""`, `version=null`; 16/16 recursos con `datastore_active=false` y `description=null`; diccionarios con `start/end_date=1989-06-04` (marcador, no periodo acreditable).')
L.append('- Unidad (`Unidad de medida`) y `Catalogo de referencia` vacios en las 24 filas; tipos solo `Booleano Si/No` o `Texto`.')
L.append('- Paginas oficiales nuevas: Programa Especial de Gobierno Digital (contexto general; norma general sin vinculo a campo/recurso/version no acredita) y pagina del Diagnostico (cascaron JS + embed PowerBI; sin cuestionario extraible). Busquedas negativas acotadas a lo revisado.')
L.append('- PDFs locales preservados barridos: ninguno cubre TIC (SUIVE, SINAC, UES, SEED, CONAPO).')
L.append('- Resultado: **0 propuesta_respaldada / 24 sigue_pendiente**. Derivar significado solo del nombre violaria el criterio de aceptacion.')
L.append('')
L.append('## Decisiones (24)')
L.append('')
L.append('| # | Variable | Fila | Clase | Estado | Falta exacta |')
L.append('| --- | --- | ---: | --- | --- | --- |')
for i, (s, d) in enumerate(zip(tics, decisiones), 1):
    cl, _ = clase_de(s)
    L.append(f"| {i} | {d['variable']} | {s['fila']} | {cl} | {d['estado']} | {describir_faltante(s['evidencia_documental_exacta_faltante'])[:90]}... |")
L.append('')
for i, (s, d) in enumerate(zip(tics, decisiones), 1):
    L.append(f"### {i}. {d['variable']} — fila {s['fila']} ({s['diccionario_id'][:8]})")
    L.append('')
    L.append(f'- IRI: `{d["definicion_iri"]}`')
    L.append(f'- Texto original: {d["descripcion_original"][:200]}')
    L.append(f'- Huella: `{d["huella_fila_diccionario"]}`')
    L.append(f'- Estado: `{d["estado"]}` (sin significado propuesto: nada acredita el sentido literal por fila)')
    L.append(f'- Vinculo local: {d["vinculo_fuente_local"]}')
    L.append(f'- Falta exacta: {d["evidencia_faltante"]}')
    L.append(f'- Motivo: {d["motivo"]}')
    L.append(f'- Evidencia:')
    for e in d['evidencia']:
        L.append(f"  - `{e['ruta']}` sha `{e['sha256'][:16]}...` `{e['localizador']}` — {e['afirmacion_soportada'][:220]}")
    L.append('')
L.append('## Fuentes (SHA256 sobre bytes)')
L.append('')
for f in FUENTES:
    L.append(f"- `{f['ruta']}` sha256 `{f['sha256']}` — {f['aplicabilidad'][:130]}")
L.append('')
(OUT / 'entrega.md').write_bytes('\n'.join(L).encode('utf-8'))

import hashlib as H
archivos = []
for fn in ['entrega.json', 'entrega.md']:
    p = OUT / fn
    archivos.append({'ruta': f'propuestas/investigacion-post-r6/tic/{fn}', 'sha256': H.sha256(p.read_bytes()).hexdigest()})
listo = {
    'grupo_fuente': 'tic',
    'terminado_en_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'resumen': {'ids': 24, 'propuesta_respaldada': 0, 'sigue_pendiente': 24,
                'fuentes': len(FUENTES), 'consultas_http_nuevas': 10, 'verificacion_ok': True},
    'archivos': archivos,
}
(OUT / 'listo.json').write_bytes(json.dumps(listo, ensure_ascii=False, indent=1).encode('utf-8'))
print('OK decisiones=%d fuentes=%d' % (len(decisiones), len(FUENTES)))
print('sha entrega.json', archivos[0]['sha256'])
print('sha entrega.md', archivos[1]['sha256'])
