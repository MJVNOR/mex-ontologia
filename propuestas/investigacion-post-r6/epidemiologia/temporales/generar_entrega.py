import json, hashlib, os

ROOT = os.getcwd()
OUT = 'propuestas/investigacion-post-r6/epidemiologia'
EV = OUT + '/evidencia'

def sha(p):
    return hashlib.sha256(open(os.path.join(ROOT, p), 'rb').read()).hexdigest()

pend = json.load(open('propuestas/depuracion-post-r6/significados/pendientes.json', encoding='utf-8'))
epis = [s for s in pend['significados'] if s['grupo_fuente'] == 'epidemiologia']
assert len(epis) == 25, len(epis)

DICC = 'data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json'
HOJA = 'data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json'
MANUAL = 'propuestas/pendientes-muse-r5/catalogos-web/evidencia/manual_suive_32.pdf'
DS = EV + '/datastore_diccionario_2026-10-24.json'
PKG = EV + '/package_show_2026-10-24.json'
EXAM = EV + '/examen_manual_suive32_paginas.txt'
LOG = EV + '/http_log.json'

MANUAL_SHA = 'f35746a0353c902b03d8ae01f703d1dfafdf3ad4bbf01777b648353d1b833757'
assert sha(MANUAL) == MANUAL_SHA

# Examen manual por variable -> paginas que lo tocan y por que no acredita
EXAMEN = {
    'cve_cie10': ('p18', 'Manual p18: cada enfermedad incluye codigo CIE 10 (generico nacional, sin version/edicion); ejemplo local A04/A08-A09 no aparece en el manual.'),
    'acumulado': ('p26', 'Manual p26: acumulado = total de casos acumulados hasta la semana epidemiologica del ano actual (concepto analitico nacional, no regla de computo de la columna local pos 11).'),
    'de01_a_04': ('p18', 'Manual p18: formato nacional de 30 columnas con tabulacion por edad (layout distinto de las 59 locales); no fija intervalo 01-04 ni resuelve contradiccion nombre/descripcion ni solape edad 5.'),
    'se_ignoran': ('p50', 'Manual p50: recuadro Ign. = casos de edad ignorada en pantalla SUAVE nacional; no es definicion de la columna local pos 23 ni vinculo edicion-recurso-periodo.'),
}
F_DEFAULT = ('p18', 'Manual p18: subdivision por sexo del formato nacional; no define la convencion de sufijo f local. Inferir f=femenino por totalf esta prohibido sin respaldo explicito.')
INST = ('p17', 'Manual p17: instituciones nacionales SSA, IMSS, ISSSTE, Otras, IMSS-Prospera, DIF, PEMEX, SEDENA, SEMAR; conjunto DISTINTO de las 9 columnas locales (imss_ord/imss_sol/d_if/sedemar vs IMSS-Prospera/DIF/SEMAR). Sin equivalencia autorizada.')

FALTANTE = {
    'cve_cie10': 'EPI-R6-01 + EPI-R6-03: instrumento SUIVE edicion aplicable 2022 que fije objeto de cve_cie10 y version de catalogo CIE vinculada al recurso 1689b19c; o diccionario corregido/nota del publicador.',
    'acumulado': 'EPI-R6-01 + EPI-R6-02: documento del publicador que fije objeto y periodo/regla de acumulacion de la columna pos 11; o diccionario corregido con regla de computo (totalm/totalf no la definen).',
    'de01_a_04': 'EPI-R6-01 + EPI-R6-03: nota del publicador que fije el intervalo real (nombre 01-04 vs descripcion entre 1 y 5) y el tratamiento de la edad 5 frente a de05_a_09.',
}
FALTANTE_DEF = 'EPI-R6-01 + EPI-R6-02: diccionario corregido con descripcion para la columna {var} pos {fila}, o nota del publicador que fije su sentido literal citando conjunto+diccionario+fila+huella y vincule edicion-recurso-periodo.'

decisiones = []
for s in sorted(epis, key=lambda x: x['n']):
    var = s['variable']
    fila = int(s['fila'])
    idx = fila - 1
    iri = s['definicion_iri']
    desc = s['descripcion_original']
    huella = s['huella_fila_diccionario']
    if var in EXAMEN:
        pg, exam_txt = EXAMEN[var]
    elif var in ('ssa', 'imss_ord', 'issste', 'otras', 'imss_sol', 'd_if', 'pemex', 'sedena', 'sedemar'):
        pg, exam_txt = INST
    else:
        pg, exam_txt = F_DEFAULT
    falt = FALTANTE.get(var, FALTANTE_DEF.format(var=var, fila=fila))
    ev = [
        {'ruta': DICC, 'sha256': sha(DICC), 'localizador': f'/definiciones/{idx} (Nombre variable={var})',
         'afirmacion_soportada': f"Descripcion={desc!r}, catalogo de referencia vacio, ejemplo registrado; huella {huella}."},
        {'ruta': HOJA, 'sha256': sha(HOJA), 'localizador': f'hoja=SUIVE posicion_original={fila} (id={var})',
         'afirmacion_soportada': f'Columna fisica {var} observada en pos {fila} del esquema de 59 campos; sin documentar su computo.'},
        {'ruta': DS, 'sha256': sha(DS), 'localizador': f"records[_id={fila}] Nombre variable={var}",
         'afirmacion_soportada': f'Live 2026-10-24 confirma desc={desc!r} y catalogo vacio; sin cambios vs R6.'},
        {'ruta': EXAM, 'sha256': sha(EXAM), 'localizador': f'paginas del manual: {pg}',
         'afirmacion_soportada': exam_txt},
        {'ruta': LOG, 'sha256': sha(LOG), 'localizador': 'consultas package_show/datastore/manual + 403 xlsx/csv/boletin',
         'afirmacion_soportada': 'Package sin cambios (fuentes_extras vacio, version null); manual fresco byte-identico Last-Modified 2021-08-10 < periodo 2022; descargas bloqueadas 403 sin evadir.'},
    ]
    decisiones.append({
        'definicion_iri': iri,
        'variable': var,
        'descripcion_original': desc,
        'huella_fila_diccionario': huella,
        'estado': 'sigue_pendiente',
        'significado_propuesto': None,
        'evidencia': ev,
        'vinculo_fuente_local': f'Diccionario {DICC} /definiciones/{idx} ({var}, fila {fila}, huella citada) + hoja SUIVE {HOJA} pos {fila} + edicion package datos.sonora.gob.mx dca16d84 (recurso 1689b19c, 2022-01-01/2022-12-31). Vinculo verificado: columna fisica existe; NO acredita sentido (descripcion pendiente/generica).',
        'evidencia_faltante': falt,
        'motivo': f"{exam_txt} Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre, ejemplo aislado ni catalogo nacional generico sin vinculo local. Criterio R6 conservado.",
        'limites': ['Alcance simultaneo por conjunto, diccionario, definicion, nombre y descripcion; no autoriza cruces, homologaciones ni equivalencias.', 'Evidencia negativa acotada a las busquedas 2026-10-24 documentadas en http_log.json, no ausencia universal.'],
    })

fuentes = [
    {'ruta': PKG, 'url': 'https://datos.sonora.gob.mx/api/3/action/package_show?id=dca16d84-dbf0-4501-b702-dc6372a480ea', 'sha256': sha(PKG), 'fecha_consulta': '2026-10-24', 'localizador': 'result.resources[1] edicion 2022; result.fuentes_extras; result.version', 'rol': 'Fija edicion aplicable y confirma sin Fuentes extras ni nota metodologica (sin cambios vs R6).'},
    {'ruta': DS, 'url': 'https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=2334deaa-dd0c-444e-b038-4cc556ad715d&limit=60&offset=0', 'sha256': sha(DS), 'fecha_consulta': '2026-10-24', 'localizador': 'records[_id=9..44]', 'rol': 'Revalidacion live: descripciones y catalogos vacios sin cambios vs R6.'},
    {'ruta': LOG, 'url': None, 'origen': 'generado local 2026-10-24 (cabeceras curl + resultados webfetch/websearch)', 'sha256': sha(LOG), 'fecha_consulta': '2026-10-24', 'localizador': 'consultas[] + busquedas_web_limitadas[]', 'rol': 'Log HTTP y busquedas negativas acotadas (manual 200 byte-identico; xlsx/csv/boletin 403 Cloudflare sin evadir).'},
    {'ruta': EXAM, 'url': 'https://epidemiologia.salud.gob.mx/gobmx/salud/documentos/manuales/32_ManualSuive.pdf', 'origen': 'texto extraido del preservado local (byte-identico al fresco 2026-10-24)', 'sha256': sha(EXAM), 'fecha_consulta': '2026-10-24', 'localizador': 'paginas 17, 18, 24, 26, 50 (texto integro normalizado)', 'rol': 'Examen por ID nuevo frente a R6: el manual nacional no acredita ninguna de las 25 columnas (30 vs 59 columnas; instituciones distintas; Last-Modified 2021-08-10 < 2022).'},
    {'ruta': MANUAL, 'url': 'https://epidemiologia.salud.gob.mx/gobmx/salud/documentos/manuales/32_ManualSuive.pdf', 'origen': 'preservado local revalidado fresco 2026-10-24 (mismo SHA)', 'sha256': MANUAL_SHA, 'fecha_consulta': '2026-10-24', 'localizador': 'bytes completos; pp. 17, 18, 24, 26, 50', 'rol': 'Instrumento nacional de contexto; sin vinculo edicion-recurso-periodo con el recurso local 2022.'},
    {'ruta': DICC, 'url': None, 'origen': 'inspeccion local preservada', 'sha256': sha(DICC), 'fecha_consulta': '2026-10-23 (preservada; revalidada via datastore 2026-10-24)', 'localizador': '/definiciones/8, /definiciones/10, /definiciones/12, /definiciones/22..43', 'rol': 'Fila de diccionario por cada ID (descripcion/ejemplo/catalogo + huella).'},
    {'ruta': HOJA, 'url': None, 'origen': 'inspeccion local preservada', 'sha256': sha(HOJA), 'fecha_consulta': '2026-10-23 (preservada)', 'localizador': 'hoja=SUIVE posiciones 9, 11, 13, 23..44 (59 campos)', 'rol': 'Esquema fisico: posicion de cada columna local.'},
]

entrega = {
    'grupo_fuente': 'epidemiologia',
    'generado_en_utc': '2026-10-24T06:25:00+00:00',
    'ids_asignados': 25,
    'resumen_investigacion': 'Revalidacion fresca 2026-10-24 del package (sin cambios: version null, fuentes_extras vacio, edicion 2022-01-01/2022-12-31) y del datastore del diccionario (59 filas; 22 en Pendiente de especificar; catalogos vacios). Novedad frente a R6: (1) examen por ID del Manual SUIVE 32 (pp. 17, 18, 24, 26, 50) que R6 solo cito como contexto: el instrumento nacional no acredita ninguna columna local (formato de 30 columnas vs 59 locales; lista de instituciones distinta; acumulado como concepto analitico semanal sin regla de computo local; Ign. de pantalla SUAVE sin vinculo; sin version CIE vinculada al recurso 2022); (2) re-descarga del manual desde URL oficial DGE: byte-identico (mismo SHA), Last-Modified 2021-08-10 anterior al periodo 2022, luego sin vinculo edicion-recurso-periodo; (3) busquedas web nuevas acotadas: sin edicion 2022 del instrumento ni codebook/nota del publicador Sonora; boletin Sonora SE 37 pista bloqueada por 403. Resultado: 0 propuestas (ningun ID satisface el criterio de aceptacion: documento del publicador que fije sentido literal con conjunto+diccionario+fila+huella y vincule edicion-recurso-periodo, o diccionario corregido/codebook aplicable); 25 siguen pendientes con hueco exacto identificado.',
    'fuentes': fuentes,
    'decisiones': decisiones,
    'conteo': {'propuesta_respaldada': 0, 'sigue_pendiente': 25},
}
p = OUT + '/entrega.json'
json.dump(entrega, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('entrega.json', sha(p))
