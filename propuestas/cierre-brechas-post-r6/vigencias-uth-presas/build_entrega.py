import json, hashlib, pathlib

D = 'propuestas/cierre-brechas-post-r6/vigencias-uth-presas'
PFX = D + '/'
EV = D + '/evidencia'
FECHA = '2026-10-24'

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

asig = json.load(open(D + '/asignacion.json', encoding='utf-8'))
casos = {c['id']: c for c in asig['casos']}

# SHAs verificados por bytes (no inventados)
H = {pathlib.Path(p).name: sha(p) for p in sorted(pathlib.Path(EV).glob('*'))}
H['cmpe2016_inegi.pdf'] = '66ba2fd24aa01d82684df52677b792e17fe55d38273d6325ff4f6f66a3ef714b'  # re-verificado por bytes arriba
H['xlsx_uth_53bd5e97'] = '53bd5e971a033998ed8a72317b6ad1e69314d82463220d8cfd156dfad9034259'
H['xlsx_presas_612b2b11'] = '612b2b11192b97ae7328f80c8a5d1c545e117da46dd436a9b077aaf824b1525f'
H['pendientes-ronda-5.json'] = '46f3b6f8826379be5124fb85cf6128b705fbe90deebf2c99bff64098608c8f11'
H['pendientes-muse-r6_catalogos_entrega.json'] = '649bbe7e5feca82b7e8d5c5144de78b1d8ceccb1c217ca976347b1c9a05cb74b'

API = {
 'V01': PFX + 'evidencia/api_package_V01_403912fd-5853-4e18-8256-f77206f855bd_2026-10-24.json',
 'V02': PFX + 'evidencia/api_package_V02_e5aad52d-5760-481c-ba65-db0ba4a5315e_2026-10-24.json',
 'V03': PFX + 'evidencia/api_package_V03_e7a3d62f-4ace-479c-aa52-1c9e384dc429_2026-10-24.json',
 'V04': PFX + 'evidencia/api_package_V04_85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f_2026-10-24.json',
 'V05': PFX + 'evidencia/api_package_V05_ee8f639f-5e89-46ae-93b9-934b05fc6233_2026-10-24.json',
}
HN = {k: sha(v) for k, v in API.items()}
AC_PDF = PFX + 'evidencia/acuerdo_cmpe_uso_obligatorio_2026-10-24.pdf'
AC_TXT = PFX + 'evidencia/acuerdo_cmpe_texto_2026-10-24.txt'
ORG = PFX + 'evidencia/org_uth_2026-10-24.html'
PAG1960 = PFX + 'evidencia/recurso_1960-1969_pagina_2026-10-24.html'

ev_acuerdo = {'ruta': AC_PDF, 'sha256': sha(AC_PDF),
    'localizador': 'texto extraído: DOF 16-04-2012; ACUERDO PRIMERO (clasificador obligatorio para Unidades del Estado) + TRANSITORIOS (plazo 3 años); sin mención a UTH ni a periodos 2022-2026',
    'afirmacion_soportada': 'Existe mandato nacional de uso obligatorio de la CMPE (DOF 16-04-2012) para Unidades del Estado en actividades SNIEG de estadísticas de educación; el documento no cita al publicador UTH, ni la edición 2016 vinculada a recurso alguno, ni periodos de aplicación. NEUTRO para F4: marco obligatorio genérico, no vínculo edición-recurso-periodo del publicador.'}
ev_org = {'ruta': ORG, 'sha256': sha(ORG),
    'localizador': '7 conjuntos listados (Reingreso, Matrículas, Discapacidad, Promedio, Titulados, Egresados, Nuevo ingreso); nota Matrículas: campo de formación académica, fuente interna',
    'afirmacion_soportada': 'Re-verificación en vivo 2026-10-24 del patrón W01: el portal UTH describe campo de formación académica (Matrículas) sin declarar CMPE, edición ni versión. NEGATIVO F4 (re-confirma R5/R6, no es fuente nueva de cierre).'}

def ev_api(vid, pid, extra_loc, extra_af):
    return {'ruta': API[vid], 'sha256': HN[vid], 'localizador': extra_loc,
            'afirmacion_soportada': extra_af}

decisiones = []

# V01-V04 comparten catálogo; F3 acreditada por cmpe pdf; F4 ausente
for vid in ['V01', 'V02', 'V03', 'V04']:
    c = casos[vid]
    nres = {'V01': 15, 'V02': 16, 'V03': 6, 'V04': 6}[vid]
    per = '; '.join(c['periodos_declarados_por_titulo'])
    evs = [
        ev_api(vid, c['conjunto']['id'], f"result.version=null; fuentes_extras vacías; {nres} recursos; Catalogo size 10433 = sha local 53bd5e97; fechas Catalogo/Diccionario 1989-06-04" + ('; Catalogo Egresados start 2016-01-01/end 2025-01-01 (cobertura manual)' if vid == 'V04' else ''),
            f"API CKAN en vivo {FECHA}: sin edición declarada (version=null), sin vínculo CMPE-periodos en metadatos; los títulos de recursos ({per}) son declaración de partición de publicación, no acreditación F4 (criterio: títulos no acreditan)."),
        ev_org,
        ev_acuerdo,
        {'ruta': 'data/integracion/fuentes/53bd5e971a033998ed8a72317b6ad1e69314d82463220d8cfd156dfad9034259.xlsx', 'sha256': H['xlsx_uth_53bd5e97'],
         'localizador': 'bytes locales; size 10433 = API; interior sin celdas de versión/periodo (R4 vigente, re-verificado R6)',
         'afirmacion_soportada': 'El catálogo compartido UTH carece de edición/version/fecha declarada en su interior.'},
        {'ruta': 'data/integracion-ronda-2/entregas/agente-4-vigencia/evidencia/externa/cmpe2016_inegi.pdf', 'sha256': H['cmpe2016_inegi.pdf'],
         'localizador': 'p.2 catalogación INEGI c2016; p.8 segunda edición',
         'afirmacion_soportada': 'F3 acreditada: edición CMPE 2016 existe como documento primario nacional; no acredita adopción UTH ni periodos (F4).'},
    ]
    decisiones.append({
        'id': vid, 'estado': 'sigue_pendiente', 'original': c,
        'motivo': f"F3 acreditada (CMPE 2016, evidencia primaria). F4 ausente tras contraste {FECHA}: API en vivo confirma version=null y extras vacíos; portal UTH en vivo no declara CMPE; Acuerdo de uso obligatorio (DOF 16-04-2012) es mandato genérico nacional sin vínculo UTH-periodos; ningún documento del publicador vincula la CMPE 2016 con ({per}).",
        'evidencia_faltante': c['documento_requerido_exacto'],
        'evidencia': evs, 'propuesta': None,
        'limites': c['limites'] + ['Los títulos de recursos CKAN y el conteo de recursos no acreditan F4.',
            'El Acuerdo de uso obligatorio (marco nacional) no se usa como vínculo del publicador ni como edición vinculada a recurso/periodo.',
            'Sin joins ni identidad de catálogos automática; sin inferir vigencia del nombre del archivo.'],
    })

c5 = casos['V05']
per5 = '; '.join(c5['periodos_declarados_por_titulo'])
decisiones.append({
    'id': 'V05', 'estado': 'sigue_pendiente', 'original': c5,
    'motivo': f"F3+F4 ausentes tras contraste {FECHA}: API en vivo confirma version=null, extras vacías, Catalogo size 15123 = local, fechas placeholder 1989-06-04; recurso 1960-1969 (id 4d1bb645) con url vacía, size 541916, state active; página HTML del recurso sin href de descarga (plantilla genérica). Sin declaración de edición/versión/fecha del Catálogo_estatal ni vínculo con ({per5}).",
    'evidencia_faltante': c5['documento_requerido_exacto'],
    'evidencia': [
        ev_api('V05', c5['conjunto']['id'], 'recurso 1960-1969 id 4d1bb645: url="", url_type="", size 541916, state active, start 1960-01-01/end 1969-12-31; Catalogo size 15123 = local; version=null',
            f"API CKAN en vivo {FECHA}: constancia estructurada del hueco de descarga 1960-1969 (url vacía) con cobertura declarada 1960-01-01/1969-12-31; sin edición del catálogo."),
        {'ruta': PAG1960, 'sha256': sha(PAG1960),
         'localizador': 'texto genérico de plantilla presente + 0 hrefs download; 1 href interno con id (vista, no descarga); metadatos visibles Start 1960-01-01/End 1969-12-31, Size 529,2 KiB',
         'afirmacion_soportada': 'Doble capa HTML+API 2026-10-24: la página muestra botón genérico sin enlace real de descarga; el hueco persiste (más preciso que R6, que solo tenía API). No acredita F3 ni F4.'},
        {'ruta': 'data/territorio/fuentes/f5060479-ee16-49b5-99d4-09aabef8042e.xlsx', 'sha256': H['xlsx_presas_612b2b11'],
         'localizador': 'bytes locales; size 15123 = API; interior Catálogo_estatal/Municipios/Regiones sin celdas de versión/periodo',
         'afirmacion_soportada': 'El catálogo de presas carece de edición/version/fecha declarada en su interior.'},
    ],
    'propuesta': None,
    'limites': c5['limites'] + ['El texto genérico de plantilla HTML no equivale a URL de descarga; error/plantilla no se confunde con existencia.',
        'Sin joins por compartir Clave; sin inferir vigencia del nombre del archivo.'],
})

fuentes = [
    {'ruta': API['V01'], 'sha256': HN['V01'], 'url': 'https://datos.sonora.gob.mx/api/3/action/package_show?id=403912fd-5853-4e18-8256-f77206f855bd', 'fecha_consulta': FECHA, 'localizador': 'version; fuentes_extras; resources[].size/start_date/end_date (15 recursos)'},
    {'ruta': API['V02'], 'sha256': HN['V02'], 'url': 'https://datos.sonora.gob.mx/api/3/action/package_show?id=e5aad52d-5760-481c-ba65-db0ba4a5315e', 'fecha_consulta': FECHA, 'localizador': 'version; fuentes_extras; resources (16 recursos)'},
    {'ruta': API['V03'], 'sha256': HN['V03'], 'url': 'https://datos.sonora.gob.mx/api/3/action/package_show?id=e7a3d62f-4ace-479c-aa52-1c9e384dc429', 'fecha_consulta': FECHA, 'localizador': 'version; fuentes_extras; resources (6 recursos)'},
    {'ruta': API['V04'], 'sha256': HN['V04'], 'url': 'https://datos.sonora.gob.mx/api/3/action/package_show?id=85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f', 'fecha_consulta': FECHA, 'localizador': 'version; resources Catalogo 2016-01-01/2025-01-01 (cobertura, NEUTRO)'},
    {'ruta': API['V05'], 'sha256': HN['V05'], 'url': 'https://datos.sonora.gob.mx/api/3/action/package_show?id=ee8f639f-5e89-46ae-93b9-934b05fc6233', 'fecha_consulta': FECHA, 'localizador': 'recurso 4d1bb645 url/size/state; Catalogo size; version'},
    {'ruta': PAG1960, 'sha256': sha(PAG1960), 'url': 'https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos/resource/4d1bb645-19da-407f-8182-b0be2d7b7485', 'fecha_consulta': FECHA, 'localizador': 'botón plantilla sin href download; metadatos Start/End/Size'},
    {'ruta': ORG, 'sha256': sha(ORG), 'url': 'https://datos.sonora.gob.mx/organization/uth', 'fecha_consulta': FECHA, 'localizador': '7 conjuntos; notas sin CMPE'},
    {'ruta': AC_PDF, 'sha256': sha(AC_PDF), 'url': 'https://www.snieg.mx/DocumentacionPortal/Normatividad/vigente/Acuerdo_CMPE160412.pdf', 'fecha_consulta': FECHA, 'localizador': 'DOF 16-04-2012; ACUERDO PRIMERO + TRANSITORIOS (vía descarga directa; webfetch rechazó content-type pdf; variante /Vigente/ devolvió 404 registrado como error HTTP, no inexistencia)'},
    {'ruta': AC_TXT, 'sha256': sha(AC_TXT), 'url': 'https://www.snieg.mx/DocumentacionPortal/Normatividad/vigente/Acuerdo_CMPE160412.pdf', 'fecha_consulta': FECHA, 'localizador': 'extracción local pypdf (6004 caracteres) para cita; el primario es el PDF'},
    {'ruta': 'reports/pendientes-ronda-5.json', 'sha256': H['pendientes-ronda-5.json'], 'url': '', 'fecha_consulta': '2026-10-23 (previa)', 'localizador': 'decisiones_significados id=V01..V05 (W01-W09, R4)'},
    {'ruta': 'propuestas/pendientes-muse-r6/catalogos/entrega.json', 'sha256': H['pendientes-muse-r6_catalogos_entrega.json'], 'url': '', 'fecha_consulta': '2026-10-23 (previa)', 'localizador': 'decisiones id=V01..V05 + novedad_r6 C1/C2'},
]

entrega = {
    'tarea': 'vigencias-uth-presas', 'tipo': 'vigencias',
    'decisiones': decisiones, 'fuentes': fuentes,
    'novedades_frente_a_investigacion_previa': [
        'API CKAN re-verificada en vivo 2026-10-24 para los 5 packages (nuevo corte temporal vs R6 2026-10-23): version=null x5, extras vacías, sizes idénticos a locales; V01/V02 muestran recursos 2025-2026 añadidos (títulos de partición, no F4).',
        'V05 doble capa nueva: página HTML del recurso 1960-1969 guardada (0 hrefs download pese a texto de plantilla) + API con url vacía; el hueco queda constatado en ambas capas, más preciso que R6 (solo API).',
        'Acuerdo de uso obligatorio de la CMPE (DOF 16-04-2012, PDF primario local 0916f603) incorporado como fuente primaria nueva: mandato genérico nacional para Unidades del Estado; NEUTRO para F4 por no citar UTH, edición 2016 vinculada a recurso, ni periodos.',
        'Portal UTH re-verificado en vivo (7 conjuntos, notas sin CMPE): confirma patrón negativo W01 sin repetir navegación Obscura.',
        'Ninguna novedad revierte un pendiente ni acredita F4/F3 faltante: 5 sigue_pendiente, 0 propuestas, 0 vínculos, 0 joins.',
    ],
    'busquedas_limitadas': 'ver busquedas-limitadas.json (3 consultas nativas + API directa; límites y errores HTTP registrados)',
}

out = D + '/entrega.json'
pathlib.Path(out).write_text(json.dumps(entrega, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
print('entrega.json', sha(out))
ids = [d['id'] for d in decisiones]
print('ids:', ids, 'unicos:', len(set(ids)) == len(ids))
