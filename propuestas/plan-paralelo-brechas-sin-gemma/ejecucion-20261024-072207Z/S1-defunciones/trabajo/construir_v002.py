"""Reevaluacion de precision v002 S1-defunciones: sin material nuevo, sin promociones forzadas."""
import json, hashlib
from datetime import datetime, timezone

B = "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S1-defunciones"
AHORA = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def sha_file(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# Verificar SHA de la evidencia de ambito (conocida, no nueva)
HL = "propuestas/investigacion-post-r6/salud-defunciones/evidencia/http_log.json"
assert sha_file(HL) == "3e5fb718750f1d6fe1d8a5a35b27d2c5833614e0773c87cb65bbb5a11f360fe9"
AMBITO_EV = {"ruta": HL,
             "sha256": "3e5fb718750f1d6fe1d8a5a35b27d2c5833614e0773c87cb65bbb5a11f360fe9",
             "localizador": "consultas_http[2].hallazgos (s_seed.html)",
             "afirmacion_soportada": "DGIS declara fuente 'Certificados de Defuncion y Muerte Fetal; muertes accidentales/violentas solo para Defunciones': el bloque de muerte violenta/lesion es de ambito general (no fetal). Solo fija ambito, no definicion ni codigos."}
AMBITO_IDS = {"53", "54", "67", "68", "69"}

PREF = (" Reevaluacion v002 (sin material nuevo; descriptores DEFUN2022/SINAC ya conocidos, verificados por lectura directa "
        "del xlsx de 73 campos y los csv de catalogos; no se presentan como novedad):")
DIF = {
 "17": " diferencia concreta: alias de identificador (EDADGESTACIONAL vs sem_gest) + horquilla de ambito que el instrumento no resuelve (fetal preg 2, semanas desde FUM obligatoria, vs general preg 10.2, solo <28 dias con 99); ejemplo local vacio sin unidad.",
 "30": " diferencia concreta y probada de codigos: ejemplo local '4' (1 digito) no es miembro del conjunto formal (011..100,110,997,998,999, 3 caracteres; ocupacion.csv de 57 filas verificado); el instrumento (preg 14) captura texto libre sin claves. Precedente de recodificacion local: invalida suponer la codificacion nacional en otras columnas.",
 "31": " diferencia concreta: literal 'NO OCUPADO, JUBILADO O PENSIONADO' ausente del catalogo formal ocupacion.csv (57 entradas verificadas); alias de identificador; sin codebook local.",
 "32": " diferencia concreta de sujeto y campo: dos candidatos formales (cond_act del fallecido vs ocurr_trab en desempeno del trabajo) y dos preguntas-manual (general 14.1 fallecido vs fetal 31.1 madre); ejemplo '2'=No en ambos; el instrumento no fija campo ni sujeto.",
 "33": " diferencia concreta: misma horquilla de sujeto y campo que /32; literal 'NO' coherente con 2=No en ambos candidatos sin fijar ninguno.",
 "34": " diferencia concreta: alias (AFILIACION vs derechohab) + horquilla de sujeto (preg 15 fallecido vs fetal preg 32 madre); codificacion numerica local no publicada (el manual no trae codigos); la coherencia 2<->IMSS con /35 es interna, no formal.",
 "35": " diferencia concreta: alias + misma horquilla de sujeto; 'IMSS' figura en el manual solo como institucion calificadora, no como opcion cerrada de catalogo.",
 "36": " diferencia concreta: alias (SITIODEFUNCION vs sitio_ocur) + horquilla de ambito (preg 19 defuncion vs fetal preg 9 expulsion); el propio instrumento formal mezcla institucion (1-9) y sitio (10-12) en un solo campo (sitio_ocurrencia.csv verificado: 3=IMSS).",
 "37": " diferencia concreta: alias + misma horquilla; 'IMSS' es institucion, no sitio (preg 19 pide sitio; la institucion va en 19.1/19.2): posible captura cruzada que ninguna fuente fija.",
 "38": " diferencia concreta: ausencia en el instrumento nacional (73 campos verificados, ninguno de establecimiento) + horquilla de ambito (preg 19.2 defuncion vs fetal 9.2); formato del ejemplar 'SRIMS000915' sin patron verificable en el manual.",
 "53": " ambito general fijado en v002 (preg 24 + hallazgo DGIS: violentas solo para Defunciones). Diferencia restante: alias (MUERTEACCIDENTALVIOLENTA vs natviole) + codificacion local no publicada (manual sin codigos; 2=No nacional no basta por el precedente de recodificacion de /30).",
 "54": " ambito general fijado en v002 (igual que /53). Diferencia restante: alias + literal 'NO' sin codebook local que lo fije.",
 "55": " diferencia concreta: alias (INTENCIONEVENTO vs presunto) + ninguna pregunta del instrumento se titula 'intencion' (negativa acotada); ejemplo '8' ('No aplica para muerte natural' en presunta_defuncion_violenta.csv verificado) coherente, pero igualdad de valores no basta; codificacion local no publicada.",
 "56": " diferencia concreta: alias + literal 'NO APLICA' coherente con CVE 8 nacional sin que el publicador fije el campo.",
 "57": " diferencia concreta: alias (CIECAUSABASICA vs causa_def) + edicion CIE del extracto no declarada (el manual menciona CIE-10 una sola vez, sin edicion); U071 consta en el catalogo nacional 2022 ('COVID-19, virus identificado', 4111 filas verificadas), pero un valor igual no prueba mismo codebook.",
 "58": " diferencia concreta: alias + literal identico modulo mayusculas al nacional U071, con la misma objecion de edicion y vinculo.",
 "63": " diferencia concreta: alias + horquilla triple de campo (embarazo vs rel_emba vs complicaro; los tres 1,2,8,9 con 8='No aplica...'); ejemplo '8' no fija campo; el instrumento no lo determina.",
 "64": " diferencia concreta: misma horquilla triple que /63; literal 'NO APLICA' sin campo fijado.",
 "67": " ambito general fijado en v002 (bloque de lesion de muerte violenta). Diferencia restante: alias (SITIOOCURRENCIALESION vs lugar_ocur) + codificacion local no publicada ('88'='No aplica para muerte natural' en lugar_ocurrencia.csv verificado; igualdad no basta).",
 "68": " ambito general fijado en v002 (igual que /67). Diferencia restante: alias + literal 'NO APLICA' sin codebook local.",
 "69": " ambito general fijado en v002 (bloque de lesion). Diferencia concreta: alias (PARENTESCOAGRESORD vs par_agre) + el catalogo formal trae 74 opciones (1..72,88,99; 88='No aplica' verificado) que exceden las opciones del manual (preg 34): sin correspondencia biunivoca; literal sin fijar.",
 "70": " diferencia concreta con desajuste en ambas ramas: ejemplo '88' no es miembro de ent_ocurr (01..32,99) en la rama ocurrencia; en la rama lesion (ent_ocules 01..35,88,99) el nombre local no corresponde (alias + sujeto lesion vs defuncion). Ninguna rama es inequivoca.",
 "71": " diferencia concreta: misma horquilla con desajuste que /70; literal 'NO APLICA' sin ambito fijado.",
 "72": " diferencia concreta y probada de codigos: '997' no es miembro ni de mun_ocurr (001..570,999) ni de mun_ocules (001..570,888,999) (rangos del descriptor verificados); alias + recodificacion local.",
 "73": " diferencia concreta: par 997/'NO APLICA' sin contraparte formal en ninguna rama (ver /72).",
 "74": " diferencia concreta y probada de codigos: '9997' fuera de loc_ocurr (0001..6999,777,9999) y de loc_ocules (0001..6999,777,8888,9999); alias.",
 "75": " diferencia concreta: par 9997/'NO APLICA' sin contraparte formal en ninguna rama (ver /74).",
 "76": " diferencia concreta: alias (CERTIFICADOPOR vs cond_cert) + doble certificado (preg 37 general vs fetal 36); ejemplo '3'='Otro medico' (certificante.csv verificado) coherente pero igualdad no basta; codificacion local no publicada.",
 "77": " diferencia concreta: alias + misma horquilla de certificado; literal 'OTRO MEDICO' sin codebook local.",
 "78": " diferencia concreta de representacion: columna local unica tipo Fecha (ej. '1/6/2022 0:00') vs instrumento nacional con TRES campos (dia_cert/mes_cert/anio_cert); el instrumento no determina particion ni formato.",
 "79": " diferencia concreta: ausencia total (ninguno de los 73 campos nacionales; 'jurisdiccion' en el manual solo como ambito administrativo, nunca pregunta); el nombre sugiere derivacion por catalogo (join), prohibida por criterio.",
 "80": " diferencia concreta: misma ausencia que /79; el literal 'SAN LUIS RIO COLORADO' nombra un municipio, no una jurisdiccion.",
}

v001 = json.load(open(f"{B}/v001/entrega.json", encoding="utf-8"))
asig = json.load(open(f"{B}/asignacion.json", encoding="utf-8"))
decisiones = []
for d in v001["decisiones"]:
    suf = d["id"].split("%2F")[-1]
    c = next(x for x in asig["casos"] if x["id"] == d["id"])
    o_sha = hashlib.sha256(json.dumps(c["original"], ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()
    assert o_sha == d["original_sha256"], suf
    ev = list(d["evidencia"])
    lims = list(d["limites"])
    if suf in AMBITO_IDS:
        ev = ev + [AMBITO_EV]
        lims = lims + ["v002: el hallazgo DGIS solo fija el ambito general del bloque violenta/lesion; no aporta definicion, codigos ni vinculo al recurso."]
    decisiones.append({
        "id": d["id"], "tipo": d["tipo"], "original_sha256": o_sha,
        "puerta": "sin_pista_nueva", "pista": None, "estado": "brecha_externa",
        "afirmacion_propuesta": None,
        "motivo": d["motivo"] + PREF + DIF[suf],
        "evidencia_faltante": d["evidencia_faltante"], "evidencia": ev,
        "condicion_reapertura": d["condicion_reapertura"], "limites": lims,
    })

registro = {"rol": "S1-defunciones", "version_base": "v001", "fecha_utc": AHORA,
            "metodo": "Relectura directa del descriptor DEFUN 2022 (73 campos) y catalogos nacionales ya conocidos; sin material nuevo, sin Obscura, sin búsquedas genericas.",
            "carga_probatoria": "sistema(SEED)+edicion(2022)+identificador exacto+representacion+ambito, sin exigir mencion de Sonora; igualdad de valores insuficiente; ningun identificador local coincide exactamente con un mnemonico nacional.",
            "razon_cero_promociones": "Alias universal de identificadores; recodificacion local probada (/30 '4' de 1 digito vs 3 nacionales; /72 '997' y /74 '9997' fuera de ambos rangos) que invalida suponer la codificacion nacional; horquillas de sujeto/ambito no resueltas (fallecido vs madre; ocurrencia vs lesion; triple campo de embarazo); codificacion local no publicada en ningun caso; ausencias totales (/38 sin campo nacional; /79-/80 sin campo ni pregunta).",
            "ambito_fijado_v002": "Bloque violenta/lesion (/53,/54,/67,/68,/69): general, por preg 24/manuales + hallazgo DGIS s_seed.html. No se extiende a otros IDs.",
            "diferencias": DIF}
json.dump(registro, open(f"{B}/trabajo/registro-reevaluacion-v002.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

entrega = {"rol": "S1-defunciones", "version": "v002", "decisiones": decisiones,
           "fuentes": v001["fuentes"],
           "novedades": {"propuestas_acreditadas": 0, "brechas_externas": 32, "accesos_no_resueltos": 0,
                         "material_nuevo": "ninguno: reinterpretacion explicita de descriptores ya conocidos para los dos auditores; v001 congelada intacta"}}
raw = json.dumps(entrega, ensure_ascii=False, separators=(",", ":"))
open(f"{B}/v002/entrega.json", "w", encoding="utf-8").write(raw)
rec = json.load(open(f"{B}/v002/entrega.json", encoding="utf-8"))
assert len(rec["decisiones"]) == 32 and all(x["estado"] == "brecha_externa" for x in rec["decisiones"])
print("v002 entrega.json OK")
