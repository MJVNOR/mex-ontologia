import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

STAGE = Path('propuestas/pendientes-muse-r4')
OUT = STAGE / 'auditoria-a'
b = json.load(open(OUT / 'borrador.json', encoding='utf-8'))

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# relectura final unica de SHAs (sin espera)
sha_entregas = {lote: sha256_file(STAGE / lote / 'entrega.json') for lote in
                ['lote-1', 'lote-2', 'lote-3', 'lote-4', 'lote-5', 'lote-6', 'ambiguedades']}
cambios = [k for k in sha_entregas if sha_entregas[k] != b['sha_entregas'][k]]

amb = json.load(open(STAGE / 'ambiguedades' / 'entrega.json', encoding='utf-8'))
inv = json.load(open(STAGE / 'investigacion' / 'entrega.json', encoding='utf-8'))
cat = json.load(open(STAGE / 'catalogos' / 'entrega.json', encoding='utf-8'))

entrega = {
    'rol': 'auditoria-a',
    'fecha_utc': datetime.now(timezone.utc).isoformat(),
    'alcance': 'Auditoria independiente de ronda 4: 175 reglas propuestas, 351 dictamenes de significados (lote-1..6), conceptos nuevos/combinados, fuentes de investigacion/catalogos y contexto de ambiguedades. Sin modificar entregas ni nucleo; sin operar Obscura (solo lectura de entrega local de investigacion); sin subagentes; sin tocar Studio.',
    'sha_entregas': sha_entregas,
    'sha_releidas_al_cierre': len(cambios) == 0,
    'dictamenes': b['dictamenes'],
    'cobertura_revision': b['cobertura'],
    'dictamen_conceptos_nuevos': {
        'total': 135,
        'dictamen': 'aceptados_en_bloque_condicionado_a_reglas',
        'motivo': 'Formato de tres elementos valido, padres vigentes o internos, sin duplicar conceptos del nucleo; cada concepto queda respaldado solo si su regla asociada es aceptada o cumple su condicion. Conceptos de reglas rechazadas (conteo-proyectos, atencion-incidencias, conteo-personas, tiempo-generico) no se incorporan.',
        'evidencia': ['ontologia/semantica.json:940 conceptos', 'verificacion check11.py: 0 defectos de formato/padre/duplicado'],
    },
    'dictamen_fuentes_investigacion': {
        'fuentes': 10,
        'dictamen': 'aceptar_uso',
        'motivo': 'Conclusiones negativas o parciales sin promociones: confirma catalogo local de Rickettsia sin acreditar uso ni version; INEGI/DGIS/CEMECE/SESNSP/CONAPO como candidatas o cubiertas-parciales; 6 negativos documentados; 135 descripciones vacias localizadas por grupos. No valida datos ni habilita cruces.',
        'evidencia': ['propuestas/pendientes-muse-r4/investigacion/entrega.json', 'pendientes_precisos:7', 'sin_promociones:true'],
    },
    'dictamen_fuentes_catalogos': {
        'referencias': 17,
        'dictamen': 'aceptar_uso',
        'motivo': '17 referencias pendientes, 0 propuestas de cambio al nucleo, 6 solicitudes de investigacion: postura conservadora correcta; fuente nacional no acredita aplicacion local ni version historica.',
        'evidencia': ['propuestas/pendientes-muse-r4/catalogos/entrega.json'],
    },
    'dictamen_ambiguedades': {
        'decisiones': 6,
        'dictamen': 'aceptar',
        'motivo': '3 elecciones de ide_id/1 condicionadas a r4-lote-1-001 (aceptada aqui: condicion cumplida); 2 de plantas con reglas vigentes r3a10-0286/0288 verificadas en nucleo; 1 pendiente de Clave en presas correcta (dos filas mismo concepto distinta hoja, sin resolucion por parecido).',
        'evidencia': ['propuestas/pendientes-muse-r4/ambiguedades/entrega.json', 'ontologia/semantica.json:r3a10-0286,r3a10-0288 existentes'],
    },
    'hallazgos': [
        'P36/P39/P40 de lote-4 (a4e8bee0): Tipo Booleano Si/No contradice conceptos de conteo/procedimiento; el limite que lo reconoce no resuelve la contradiccion: rechazadas. El mismo patron quedo correctamente pendiente en lote-2 (af14), lo que confirma el criterio.',
        'P13 tipo-pruebas (a4e8bee0, Tipo Texto, ejemplo Si): aceptada porque Texto si puede portar tipos; el ejemplo pobre no contradice el tipo. Distinto del caso booleano.',
        'Sector P2 identico en tres encuestas TIC (a4e8/c65e/f3ec) comparte un concepto sin clasificador declarado: condicionado a limite de no-equiparacion entre encuestas. Lote-2 dejo Sector pendiente en su diccionario por vaguedad; coherente con exigir limite.',
        'Bien juridico/tipo/subtipo/modalidad: separados por metodologia (municipal, fuero comun, metodologia anterior) con limites de no-comparabilidad: aceptados. Un limite de no-comparabilidad si basta cuando no hay contradiccion interna.',
        'Clave CIE en dos diccionarios de salud comparte concepto sin version: condicionada a no-equivalencia entre diccionarios.',
        'Lote-3 reutilizo el concepto vigente tiempo (exige evento/unidad/cobertura) para P3/P4/P5 Fecha y Hora con representacion hora que recorta fecha: rechazadas; lote-4/5 usaron conceptos especificos con no_especificada (correcto).',
        'Tres booleanos de existencia con representacion codigo en lote-3 (apoyo-tendencias, instrumentos previos/actuales): condicionados a no_especificada.',
        'r4-lote-2-021 fusiona ordinal generico con estudiante matriculado bajo un concepto: condicionada a concepto propio.',
        '135 descripciones vacias/pendientes: ninguna regla las interpreta; todos los pendientes estan motivados por evidencia (filas corruptas, contradicciones, truncamientos, descripciones vacias), no por falta de regla previa.',
        'Huellas de fila de las 175 reglas reproducidas desde data/portal/contenido-inspeccion.json: 175/175 OK; nombres/descripciones literales salvo recortes de espacios.',
    ],
    'pendientes': [
        'Cuestionarios completos de las encuestas TIC (P8 doble metodologia/documentacion, P7 sin sujeto, P22 truncada, P36/P39/P40 solo como existencia).',
        'Declaracion del publicador vinculando cada diccionario local a su catalogo y version (CLUES/CIE/municipios/entidades/localidades) y corte aplicable por recurso 2022-2024.',
        'Version CIE y CLUES aplicable por anio de dato; corte ageeml/INEGI por recurso.',
        'Instrumento SINAVE o manual de rickettsiosis que defina des_mpo_res/des_mpo_uni_trat; aclaracion CVE_MUN formato nnn vs ejemplo 26048.',
        'Respaldo explicito por cada una de las 135 definiciones vacias.',
        'Reentrega de las 12 reglas condicionadas con los cambios exigidos y de reemplazo para las 6 rechazadas (si se insiste, como existencia declarada, nunca como conteo/procedimiento).',
    ],
    'conteos': {
        'reglas_dictaminadas': 175,
        'aceptar': 157,
        'rechazado': 6,
        'condicionado': 12,
        'significados_revisados': 351,
    },
}
json.dump(entrega, open(OUT / 'entrega.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('cambios_sha_al_cierre:', cambios)
print('dictamenes:', len(entrega['dictamenes']))
