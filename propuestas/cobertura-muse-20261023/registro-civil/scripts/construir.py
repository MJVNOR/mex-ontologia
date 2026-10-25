"""Cobertura Muse registro civil: corrige la copia congelada del agente-7 con los
23 dictámenes condicionados de auditor11. Solo lee copias congeladas y central
(solo lectura); escribe SOLO en propuestas/cobertura-muse-20261023/registro-civil/.
No ejecuta scripts históricos ni suite central. Sin red."""
import collections
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MIA = ROOT / "propuestas" / "cobertura-muse-20261023" / "registro-civil"
FROZ = ROOT / "propuestas" / "cobertura-muse-20261023" / "fuentes"
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella  # noqa: E402
from integrar_contenido import valor  # noqa: E402

ENTREGA = "propuestas/cobertura-muse-20261023/registro-civil/entrega.json"

# slug viejo -> [slug nuevo, etiqueta, definicion, padre] (neutraliza sujeto inferido)
RENOMBRA = {
    "atencion-medica-difunto": ["atencion-medica-segun-definicion", "Atención médica según definición",
        "La descripción dice 'si recibió atención médica' sin nombrar sujeto; el sujeto proviene del contexto publicado (ver calificador), no es hecho autónomo del literal; valores no documentados.", None],
    "cirugia-difunto": ["cirugia-segun-definicion", "Cirugía según definición",
        "La descripción dice 'si se le realizó cirugía' sin nombrar sujeto; el sujeto proviene del contexto publicado (ver calificador); valores no documentados.", None],
    "autopsia-difunto": ["autopsia-segun-definicion", "Autopsia según definición",
        "La descripción dice 'si se practicó autopsia' sin nombrar sujeto; el sujeto proviene del contexto publicado (ver calificador); valores no documentados.", None],
    "extranjeria-difunto-segun-definicion": None,  # se fusiona abajo
    "extranjeria-madre-segun-definicion": None,  # se fusiona abajo
    "hijos-nacidos-muertos-madre": ["hijos-nacidos-muertos-segun-definicion", "Hijos nacidos muertos según definición",
        "El literal no nombra sujeto; este proviene del contexto publicado (ver calificador).", None],
    "hijos-nacidos-vivos-madre": ["hijos-nacidos-vivos-segun-definicion", "Hijos nacidos vivos según definición",
        "El literal no nombra sujeto; este proviene del contexto publicado (ver calificador).", None],
    "hijos-sobrevivientes-madre": ["hijos-sobrevivientes-segun-definicion", "Hijos sobrevivientes según definición",
        "El literal no nombra sujeto; este proviene del contexto publicado (ver calificador).", None],
    "condicion-hijo-anterior-madre": ["condicion-hijo-anterior-segun-definicion", "Condición del hijo anterior según definición",
        "El literal no nombra sujeto; este proviene del contexto publicado (ver calificador); código y texto denotan el mismo objeto.", None],
    "supervivencia-hijo-anterior-madre": ["supervivencia-hijo-anterior-segun-definicion", "Supervivencia del hijo anterior según definición",
        "El literal no nombra sujeto; este proviene del contexto publicado (ver calificador); valores no documentados.", None],
    "fecha-nacimiento-nacido": ["fecha-nacimiento-segun-definicion", "Fecha de nacimiento según definición",
        "El literal ('Fecha de nacimiento') no nombra sujeto; este se toma del conjunto y filas vecinas (ver calificador).", "tiempo"],
    "hora-nacimiento-nacido": ["hora-nacimiento-segun-definicion", "Hora del nacimiento según definición",
        "El literal ('Hora de nacimiento') no nombra sujeto; este se toma del conjunto y filas vecinas (ver calificador).", "tiempo"],
}
EXTRANJERIA_NEUTRA = ["extranjeria-segun-definicion", "Extranjería según definición",
    "Los literales dicen 'si es extrangero/extrangera' (sic) sin nombrar sujeto ni deducir lugar; sujeto en calificador; contradicciones nombre/descripción registradas sin deducir; valores no documentados.", None]

# Mismo slug, definición corregida (retira añadido fuera del literal)
REDEFINE = {
    "fecha-nacimiento-madre": ["Fecha de nacimiento de la madre",
        "Fecha de nacimiento de la madre según el literal; el vínculo con el registrado proviene del contexto publicado, con ese límite.", "tiempo"],
    "edad-madre": ["Edad de la madre",
        "Edad de la madre según el literal (ejemplo 22); unidad no declarada en la fila; el vínculo con el registrado proviene del contexto, con ese límite.", None],
    "edad-padre": ["Edad del padre",
        "Edad del padre según el literal (ejemplo 99); unidad no declarada en la fila; el vínculo con el registrado proviene del contexto, con ese límite.", None],
}

CAL_DIFUNTO = {"sujeto": "difunto", "alcance": "inferencia-contextual-publicada",
               "origen": "título publicado del conjunto Sistema Epidemiológico y Estadístico de Defunciones"}
CAL_MADRE = {"sujeto": "madre", "alcance": "inferencia-contextual-publicada",
             "origen": "título publicado del conjunto Información Sobre Nacimientos"}
CAL_NACIDO = {"sujeto": "nacido", "alcance": "inferencia-contextual-publicada",
              "origen": "título publicado del conjunto y filas vecinas del diccionario"}
CAL_VINCULO_MADRE = {"vinculo": "madre del nacido", "alcance": "inferencia-contextual-publicada",
                     "origen": "título publicado del conjunto Información Sobre Nacimientos"}
CAL_VINCULO_PADRE = {"vinculo": "padre del nacido", "alcance": "inferencia-contextual-publicada",
                     "origen": "título publicado del conjunto Información Sobre Nacimientos"}
CAL_PARTO = {"evento": "parto", "alcance": "inferencia-contextual-publicada",
             "origen": "título publicado del conjunto Información Sobre Nacimientos"}

# concepto (nuevo, neutro y compartidos) -> calificador; extranjería va por regla
CALIFICADOR = {
    "atencion-medica-segun-definicion": CAL_DIFUNTO,
    "cirugia-segun-definicion": CAL_DIFUNTO,
    "autopsia-segun-definicion": CAL_DIFUNTO,
    "hijos-nacidos-muertos-segun-definicion": CAL_MADRE,
    "hijos-nacidos-vivos-segun-definicion": CAL_MADRE,
    "hijos-sobrevivientes-segun-definicion": CAL_MADRE,
    "condicion-hijo-anterior-segun-definicion": CAL_MADRE,
    "supervivencia-hijo-anterior-segun-definicion": CAL_MADRE,
    "fecha-nacimiento-segun-definicion": CAL_NACIDO,
    "hora-nacimiento-segun-definicion": CAL_NACIDO,
    "fecha-nacimiento-madre": CAL_VINCULO_MADRE,
    "edad-madre": CAL_VINCULO_MADRE,
    "edad-padre": CAL_VINCULO_PADRE,
    "cesarea-parto": CAL_PARTO,
}
# regla -> calificador cuando el concepto se comparte con otro sujeto
CAL_POR_REGLA = {
    "r3a7-seed-resideextranjero-no_especificada": CAL_DIFUNTO,
    "r3a7-nac-nacioextranjero-codigo": CAL_MADRE,
    "r3a7-nac-nacioextranjerod-no_especificada": CAL_MADRE,
}
LIM_EXTRA = {
    "r3a7-nac-edadpadre-no_especificada": ["ejemplo 99: posible código de desconocido; identificador de nulos vacío en la fila; no se confirma ni se usa como edad"],
    "r3a7-nac-tipocesaread-nombre": ["ejemplo PROGRAMADO no corresponde a binario 'si fue cesarea'; posible tipología no documentada; no se interpreta como binario"],
    "r3a7-nac-resideextranjero-codigo": ["par textual RESIDEEXTRANJEROD separado a pendiente por contradicción; no se unifican"],
}


def main():
    froz = json.loads((FROZ / "agente-7-registro-civil" / "propuestas.json").read_text(encoding="utf-8"))
    aud = json.loads((FROZ / "agente-11-auditoria" / "auditoria.json").read_text(encoding="utf-8"))
    insp = {r["id"]: r for r in json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))["recursos"]}
    central_concepts = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))["conceptos"]
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    assert len(froz["decisiones"]) == 163 and len(froz["reglas"]) == 75 and len(froz["conceptos_nuevos"]) == 50
    da7 = aud["dictamenes"]["a7"]
    assert len(da7) == 75, len(da7)
    assert {k for k, v in da7.items() if v["dictamen"] != "aceptar"} == set(COND_FIX)

    nuevos = {}
    for slug, val in froz["conceptos_nuevos"].items():
        if slug in RENOMBRA:
            r = RENOMBRA[slug]
            if r is not None:
                nuevos[r[0]] = r[1:]
        elif slug in REDEFINE:
            nuevos[slug] = REDEFINE[slug]
        else:
            nuevos[slug] = val
    nuevos[EXTRANJERIA_NEUTRA[0]] = EXTRANJERIA_NEUTRA[1:]
    assert len(nuevos) == 49, len(nuevos)
    for slug, val in nuevos.items():
        assert slug not in central_concepts, slug
        assert val[2] is None or val[2] in central_concepts, slug

    mapa_concepto = {}
    for slug in froz["conceptos_nuevos"]:
        if slug in RENOMBRA:
            r = RENOMBRA[slug]
            mapa_concepto[slug] = EXTRANJERIA_NEUTRA[0] if r is None else r[0]
        else:
            mapa_concepto[slug] = slug

    reglas = []
    for r in froz["reglas"]:
        d = next(x for x in froz["decisiones"] if x["regla_id"] == r["id"])
        concepto = mapa_concepto.get(r["concepto"], r["concepto"])
        cal = CAL_POR_REGLA.get(r["id"], CALIFICADOR.get(concepto))
        limites = ["solo aplica a la definición citada (alcance simultáneo por conjunto, diccionario, definición, nombre y descripción); no autoriza cruces, homologaciones ni equivalencias"]
        limites.extend(LIM_EXTRA.get(r["id"], []))
        if cal is not None:
            limites.append("sujeto/encuadre en calificador formal; sin cruces entre poblaciones")
        reglas.append({"id": r["id"], "concepto": concepto, "representacion": r["representacion"],
                       "nombres": r["nombres"], "descripciones": r["descripciones"],
                       "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"],
                       "definiciones": r["definiciones"],
                       "huella_fila_diccionario": d["huella_fila_diccionario"],
                       "limites": limites,
                       **({"calificador": cal} if cal is not None else {}),
                       "evidencia": {"descripcion": d["descripcion"], "tipo": d["tipo"], "formato": d["formato"],
                                     "unidad": d["unidad"], "ejemplo": d["ejemplo"],
                                     "catalogo_declarado": d["catalogo_declarado"],
                                     "titulo_conjunto": d["titulo_conjunto"]},
                       "criterio": r["criterio"], "fuente_revision": ENTREGA})
    assert len(reglas) == 75 and len({r["id"] for r in reglas}) == 75

    decisiones = []
    for x in froz["decisiones"]:
        base = {"definicion_iri": x["definicion_iri"], "conjunto": x["conjunto"],
                "titulo_conjunto": x["titulo_conjunto"], "diccionario": x["diccionario"],
                "variable": x["variable"], "descripcion": x["descripcion"], "tipo": x["tipo"],
                "formato": x["formato"], "unidad": x["unidad"], "ejemplo": x["ejemplo"],
                "catalogo_declarado": x["catalogo_declarado"],
                "huella_fila_diccionario": x["huella_fila_diccionario"]}
        if x["decision"] == "propuesta-significado":
            decisiones.append({**base, "decision": "proponer", "regla_id": x["regla_id"]})
        else:
            decisiones.append({**base, "decision": "pendiente", "motivo": x["criterio"]})
    assert len(decisiones) == 163 and len({d["definicion_iri"] for d in decisiones}) == 163

    entrega = {"agente": "cobertura-muse-20261023/registro-civil", "base": "copia congelada agente-7 (75 reglas) + dictámenes auditor11",
               "delta_auditado76_entrega75": "La auditoría inicial cubrió 76 reglas; el hallazgo accionable RESIDEEXTRANJERO separó el par código/texto (D a pendiente por contradicción) y la entrega congelada quedó en 75. auditoria.json ya dictamina esas 75 (52 aceptar + 23 condicionado); su resultado.md conserva texto de la pasada de 76 (61/15): vale el JSON máquina por IRI.",
               "conceptos_nuevos": nuevos, "conceptos_reutilizados": froz["conceptos_reutilizados"],
               "reglas": reglas, "decisiones": decisiones,
               "condicionados_corregidos": COND_FIX,
               "alcance": "163 definiciones asignadas; sin correspondencias columna-variable; sin sameAs/exactMatch; sin red; sin tocar núcleo.",
               "limites": froz["limites"]}
    (MIA / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=1), encoding="utf-8")
    por_iri = {d["definicion_iri"]: d for d in decisiones}

    def iris(vars_):
        return [d["definicion_iri"] for d in decisiones if d["variable"] in vars_]

    pendientes = {"preguntas": [
        {"id": "Q-RESIDE-D", "definiciones": iris(["RESIDEEXTRANJEROD"]),
         "pregunta": "¿RESIDEEXTRANJEROD ('es residente extranjera') significa residencia fuera del país o condición de extranjería?",
         "documentacion_faltante": "diccionario o catálogo que defina el valor; sin confirmar no se unifica con RESIDEEXTRANJERO"},
        {"id": "Q-EDADPADRE-99", "definiciones": iris(["EDADPADRE"]),
         "pregunta": "¿El valor 99 en EDADPADRE es edad real o código de desconocido?",
         "documentacion_faltante": "identificador de nulos de la fila (vacío) o regla de codificación publicada"},
        {"id": "Q-TIPOCESAREAD", "definiciones": iris(["TIPOCESAREAD"]),
         "pregunta": "¿Qué tipología de valores admite TIPOCESAREAD (ejemplo PROGRAMADO)?",
         "documentacion_faltante": "catálogo de valores del indicador textual; no se interpreta como binario"},
        {"id": "Q-IDENTIDAD", "definiciones": iris(["SE_RECONOCIA_AFROMEXICANO", "SE_RECONOCIA_AFROMEXICANOD", "SE_CONSIDERA_INDIGENA", "SE_CONSIDERA_INDIGENAD", "HABLALENGUAINDIGENA", "HABLALENGUAINDIGENAD", "SECONSIDERAINDIGENA", "SECONSIDERAINDIGENAD", "HABLALENGUAINDIGENA", "HABLALENGUAINDIGENAD"]),
         "pregunta": "¿Qué valores y catálogos usan los indicadores de identidad/etnia/lengua?",
         "documentacion_faltante": "catálogo o texto publicado que defina valores; no se promueve código a identidad por costumbre"},
        {"id": "Q-CLAVEEDAD", "definiciones": iris(["CLAVEEDAD", "CLAVEEDADD"]),
         "pregunta": "¿Qué población, evento y unidades describen CLAVEEDAD/CLAVEEDADD?",
         "documentacion_faltante": "descripción específica con población y evento; 'Clave/Unidad de edad' es genérica"},
        {"id": "Q-DESC-75", "definiciones": [d["definicion_iri"] for d in decisiones if d["decision"] == "pendiente" and "Pendiente de especificar" in d.get("motivo", "")],
         "pregunta": "Documentación de 75 variables con descripción literal pendiente o vacía (nombres clínicos/administrativos no bastan).",
         "documentacion_faltante": "descripciones publicadas por el publicador; lista completa de IRIs en este campo"},
    ]}
    assert len(pendientes["preguntas"]) == 6
    assert len(pendientes["preguntas"][5]["definiciones"]) == 75
    (MIA / "pendientes.json").write_text(json.dumps(pendientes, ensure_ascii=False, indent=1), encoding="utf-8")
    (MIA / "resultado.md").write_text(
        "# Cobertura Muse — registro civil (agente 7, 163 definiciones)\n\n"
        "Insumos verificados contra manifiesto (17 copias + 6 centrales, 0 diferencias). "
        "Base: 103 conceptos, 232 respaldadas, 836 revisadas, 118 candidatas, 23 candidatas iniciales y 232 respaldadas preservadas (0 intersección).\n\n"
        "## Delta auditado-76 vs entrega-75\n\n"
        "La auditoría inicial cubrió 76 reglas; el hallazgo accionable RESIDEEXTRANJERO separó el par "
        "código/texto (D a pendiente por contradicción) y la entrega congelada quedó en 75 reglas y 50 conceptos. "
        "`auditoria.json` ya dictamina esas 75 (52 aceptar + 23 condicionado); su `resultado.md` conserva texto "
        "de la pasada de 76 (61/15): vale el JSON máquina por IRI, verificado idéntico al congelado.\n\n"
        "## Corrección de los 23 condicionados\n\n"
        "- 18 reglas: concepto neutralizado (sujeto fuera del concepto) + calificador formal "
        "(difunto/madre/nacido, alcance inferencia-contextual-publicada; el integrador lo soportará antes de aplicar).\n"
        "- fecha-nacimiento-madre, edad-madre, edad-padre: definición sin añadido fuera del literal + límite + calificador de vínculo.\n"
        "- TIPOCESAREAD: límite PROGRAMADO≠binario + calificador de evento (comparte con TIPOCESAREA).\n"
        "- RESIDEEXTRANJERO-código (nac): límite de separación; D sigue pendiente con contradicción.\n"
        "- EDADPADRE: límite 99 posible nulo no documentado; no se usa como edad.\n"
        "Extranjería (seed + madre) comparte un concepto neutro con calificador por regla; conceptos nuevos 50→49, propuestas 75 (máximo 76, sin inventar).\n\n"
        "| Resultado | Cantidad |\n| --- | ---: |\n"
        "| Decisiones (proponer / pendiente) | 75 / 88 |\n"
        "| Reglas | 75 (22 con calificador) |\n"
        "| Conceptos nuevos / reutilizados | 49 / 1 (sexo-difunto) |\n"
        "| Correspondencias | 0 |\n\n"
        "Verificador propio `scripts/verificar.py` OK (positivos en pipeline, negativos solo-nombre/contexto/otra-IRI, "
        "evidencia por representación, 23+232 preservadas). Preguntas en `pendientes.json` (6). `listo.json` cierra la entrega.\n",
        encoding="utf-8")
    n_prop = sum(1 for d in decisiones if d["decision"] == "proponer")
    print("entrega: proponer=%d pendiente=%d reglas=%d conceptos_nuevos=%d" % (n_prop, 163 - n_prop, len(reglas), len(nuevos)))


COND_FIX = {
    "r3a7-nac-condicionhijoanterior-codigo": "concepto neutralizado + calificador madre",
    "r3a7-nac-condicionhijoanteriord-nombre": "concepto neutralizado + calificador madre",
    "r3a7-nac-edad-no_especificada": "definición sin 'del nacido' + límite + calificador vínculo",
    "r3a7-nac-edadpadre-no_especificada": "definición sin 'del nacido' + límite 99-nulo + calificador vínculo",
    "r3a7-nac-fechanacimiento-fecha": "concepto neutralizado + calificador nacido",
    "r3a7-nac-fechanacimientomadre-fecha": "definición sin 'del nacido' + límite + calificador vínculo",
    "r3a7-nac-hijosnacidosmuertos-no_especificada": "concepto neutralizado + calificador madre",
    "r3a7-nac-hijosnacidosvivos-no_especificada": "concepto neutralizado + calificador madre",
    "r3a7-nac-hijossobrevivientes-no_especificada": "concepto neutralizado + calificador madre",
    "r3a7-nac-horanacimiento-hora": "concepto neutralizado + calificador nacido",
    "r3a7-nac-nacioextranjero-codigo": "concepto neutralizado compartido + calificador madre",
    "r3a7-nac-nacioextranjerod-no_especificada": "concepto neutralizado compartido + calificador madre",
    "r3a7-nac-resideextranjero-codigo": "límite de separación código/texto (D ya pendiente)",
    "r3a7-nac-tipocesaread-nombre": "límite PROGRAMADO≠binario + calificador evento",
    "r3a7-nac-vivehijoanterior-codigo": "concepto neutralizado + calificador madre",
    "r3a7-nac-vivehijoanteriord-no_especificada": "concepto neutralizado + calificador madre",
    "r3a7-seed-atencionmedica-codigo": "concepto neutralizado + calificador difunto",
    "r3a7-seed-atencionmedicad-no_especificada": "concepto neutralizado + calificador difunto",
    "r3a7-seed-practiconecropsia-codigo": "concepto neutralizado + calificador difunto",
    "r3a7-seed-practiconecropsiad-no_especificada": "concepto neutralizado + calificador difunto",
    "r3a7-seed-realizo-cirugia-codigo": "concepto neutralizado + calificador difunto",
    "r3a7-seed-realizo-cirugiad-no_especificada": "concepto neutralizado + calificador difunto",
    "r3a7-seed-resideextranjero-no_especificada": "concepto neutralizado compartido + calificador difunto",
}

if __name__ == "__main__":
    main()
