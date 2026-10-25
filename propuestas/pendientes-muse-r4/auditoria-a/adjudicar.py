import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

STAGE = Path('propuestas/pendientes-muse-r4')
OUT = STAGE / 'auditoria-a'
ent = json.load(open(OUT / 'entrega.json', encoding='utf-8'))

NUEVOS = {
    'r4-lote-4-022': (
        'condicionado',
        'H1 adjudicado: el patron es el mismo que P36/P39/P40 (pregunta cuyo ejemplo Si no expresa la medida), pero el Tipo es Texto (no Booleano): Texto si puede portar tipos, el ejemplo pobre no lo hace inexpresable. No se rechaza; se exige reforzar positivo y limite a: respuesta de texto libre declarada; el ejemplo (Si) no tipifica; no tabular como categorica ni agregar. Sin ese refuerzo no integra.',
    ),
    'r4-lote-4-002': (
        'condicionado',
        'H2 adjudicado: concepto generico sin calificador de metodologia convive con tipo-delito-fuero-comun, tipo-delito-municipal-anterior y tipo-delito-victima-anterior. El alcance por definicion y el nucleo (cruces exigen condiciones) impiden el cruce automatico, pero el concepto reutilizable fuera de contexto invita a la equivalencia indebida. Se exige calificador de metodologia en el concepto (p. ej. tipo-delito-registrado-municipal) o limite explicito de no-comparabilidad entre metodologias. Sin eso no integra. r4-lote-4-001 ya califica y queda aceptado.',
    ),
    'r4-lote-4-003': (
        'condicionado',
        'H2 adjudicado: igual que r4-lote-4-002 para subtipo (subtipo-delito-registrado-municipal o limite de no-comparabilidad entre metodologias).',
    ),
    'r4-lote-4-004': (
        'condicionado',
        'H2 adjudicado: igual que r4-lote-4-002 para modalidad (modalidad-delito-registrado-municipal o limite de no-comparabilidad entre metodologias).',
    ),
}

n = 0
for d in ent['dictamenes']:
    if d['id'] in NUEVOS:
        d['dictamen'], d['motivo'] = NUEVOS[d['id']]
        d['evidencia'].append('adjudicacion: auditoria-medidas H1/H2 (extra autorizada); juicio propio conserva revision independiente')
        n += 1
assert n == 4, n

ent['adjudicacion_h1_h10'] = [
    {'h': 'H1', 'clase': 'confirmado_resuelto_por_rechazo_y_condicionado',
     'detalle': '025/026/027 rechazadas (Booleano vs conteo/procedimiento: el concepto mismo es el overclaim; un limite que diga "no usar como conteo" sobre un concepto llamado conteo es incoherente). 022 condicionada (Texto si puede portar tipos; se exige refuerzo de positivo/limite, no tabular). No se adopta el condicionado de medidas para 025/026/027: conservar el concepto de conteo con limite reforzado seguiria incorporando una medida no acreditada.',
     'reglas': ['r4-lote-4-025', 'r4-lote-4-026', 'r4-lote-4-027', 'r4-lote-4-022']},
    {'h': 'H2', 'clase': 'confirmado_resuelto_por_condicionado',
     'detalle': '002/003/004 condicionadas (calificador de metodologia o limite de no-comparabilidad). 001 aceptada (ya califica: bien-juridico-afectado-delito-municipal). No se rechaza por uso potencial indebido: ninguna regla afirma equivalencia entre metodologias; el alcance es por definicion exacta y el nucleo exige condiciones para cruzar.',
     'reglas': ['r4-lote-4-001', 'r4-lote-4-002', 'r4-lote-4-003', 'r4-lote-4-004']},
    {'h': 'H3', 'clase': 'confirmado_resuelto_por_rechazo_y_limite_existente',
     'detalle': 'tiempo-9/10/11 rechazadas (concepto tiempo mal reutilizado + hora recorta Fecha y Hora). Los relojes P3/P4/P5 de lote-2/4/5/6 con no_especificada y limite que documenta la contradiccion formato-vs-ejemplo quedan aceptados: la representacion no fija formato y el limite es honesto.',
     'reglas': ['r4-lote-3-tiempo-9', 'r4-lote-3-tiempo-10', 'r4-lote-3-tiempo-11']},
    {'h': 'H4', 'clase': 'confirmado_parcial_resuelto_por_condicionado_y_limite_existente',
     'detalle': 'Juicio aplicado: compartir concepto NO habilita cruce ni identidad automaticamente; el nucleo exige condiciones y cada regla fija fuente/dataset exactos. Resuelto por condicionado solo donde el concepto compartido es un clasificador sustantivo entre encuestas (sector 008/009/010; CIE 038/039). Para roles de metadatos (identificador, momento/hora, comentarios, razon/procedimiento/decision/autorizacion) y uso intra-encuesta basta alcance+limite: no se rechaza por uso potencial indebido pues ninguna regla afirma equivalencia.',
     'reglas': ['r4-lote-4-008', 'r4-lote-4-009', 'r4-lote-4-010', 'r4-lote-4-038', 'r4-lote-4-039']},
    {'h': 'H5', 'clase': 'confirmado_resuelto_por_condicionado',
     'detalle': '14/18/20 condicionadas (representacion codigo sin base -> no_especificada; 18/20 mas nota de truncamiento). Semana-5 con codigo como ordinal tolerable queda aceptada sin cruzar calendarios.',
     'reglas': ['r4-lote-3-apoyo-tendencias-tic-dependencia-14', 'r4-lote-3-instrumentos-previos-ley-gobierno-digital-18', 'r4-lote-3-instrumentos-actuales-mejora-administracion-20']},
    {'h': 'H6', 'clase': 'confirmado_limite_existente_suficiente_mas_solicitud',
     'detalle': '001 aceptada: el limite es honesto y el ejemplo ("La vida y la Integridad corporal") fija un sentido univoco dentro de su definicion; no se extiende fuera de ella. Se registra solicitud de investigacion por la redaccion defectuosa ("Campo en la que el delito se realizo").',
     'reglas': ['r4-lote-4-001']},
    {'h': 'H7', 'clase': 'confirmado_limite_existente_suficiente',
     'detalle': 'Patron codigo+nombre por separado correcto y sin fusion; no separar prefijo de sector; CIE como clave declarada sin catalogo/version; CVE_LOC distinta de AGEB. Aceptaciones mantenidas.',
     'reglas': []},
    {'h': 'H8', 'clase': 'confirmado_sin_cambios',
     'detalle': 'Padres solo tiempo/mes sin agregar unidad, moneda, escala ni identidad; montos, cantidades, CQ y edad con padre null y limites correctos. Verificado contra ontologia fuente.',
     'reglas': []},
    {'h': 'H9', 'clase': 'confirmado_sin_cambios',
     'detalle': 'Ninguna regla introduce municipio/capacidad/generacion; mineria solo mes sin anio, presas solo fecha de registro, Ceresos periodo textual. Advertencia de no cruzar CVE_LOC con municipios/AGEB ya cubierta por su limite.',
     'reglas': []},
    {'h': 'H10', 'clase': 'confirmado_limite_existente_suficiente',
     'detalle': 'Sujetos calificados no intercambiables (madre, difunto, victima-anterior, alumno, dependencia/personal TIC). Identificadores locales con limite de ordinal local correcto; el concepto compartido no se lee como identidad transversal.',
     'reglas': []},
]

ent['pendientes'].append(
    'H6: solicitar al publicador la redaccion normativa de Bien juridico afectado (5f46e4b8, "Campo en la que el delito se realizo") y confirmar si el dominio es el catalogo de bien juridico de la metodologia municipal; sin extender el concepto fuera de su definicion.'
)
ent['fecha_utc'] = datetime.now(timezone.utc).isoformat()
ent['alcance'] += ' Incorpora y adjudica H1-H10 de auditoria-medidas/entrega.json (extra autorizada por el usuario) manteniendo revision independiente: 4 dictamenes ajustados por ID (022, 002, 003, 004).'
ent['sha_entregas'] = {lote: hashlib.sha256((STAGE / lote / 'entrega.json').read_bytes()).hexdigest()
                       for lote in ['lote-1', 'lote-2', 'lote-3', 'lote-4', 'lote-5', 'lote-6', 'ambiguedades']}
ent['sha_releidas_al_cierre'] = True
a = sum(1 for d in ent['dictamenes'] if d['dictamen'] == 'aceptar')
r = sum(1 for d in ent['dictamenes'] if d['dictamen'] == 'rechazado')
c = sum(1 for d in ent['dictamenes'] if d['dictamen'] == 'condicionado')
assert (a, r, c) == (153, 6, 16), (a, r, c)
ent['conteos'] = {'reglas_dictaminadas': 175, 'aceptar': a, 'rechazado': r, 'condicionado': c,
                  'significados_revisados': 351}

json.dump(ent, open(OUT / 'entrega.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', a, r, c)
