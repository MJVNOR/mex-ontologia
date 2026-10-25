"""Ronda 4 - ambiguedades: genera entrega.json desde fuentes locales verificadas."""
import hashlib
import json

ROOT = __import__("pathlib").Path(__file__).resolve().parents[3]


def H(v):
    return hashlib.sha256(
        json.dumps(v, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")).hexdigest()


ci = json.load(open(ROOT / "data/portal/contenido-inspeccion.json", encoding="utf-8"))
ci_r = {x["id"]: x for x in ci["recursos"]}
cov = json.load(open(ROOT / "data/semantica/cobertura.json", encoding="utf-8"))
cov_v = {(v.get("diccionario"), v.get("definicion_iri", "").split("%2F")[-1]): v
         for v in cov["variables"]}


def tabla(rid, hoja_frag):
    ts = [t for t in ci_r[rid]["tablas"] if t["hoja"] == hoja_frag or hoja_frag in t["hoja"]]
    assert len(ts) == 1, (rid, hoja_frag)
    return ts[0]


def fila_dict(dic_id, n):
    d = json.load(open(ROOT / f"data/portal/inspecciones/{dic_id}.json", encoding="utf-8"))
    return d["definiciones"][n - 1]


D_FIEBRE = "33d0a99e-c721-496f-a05e-07646e9ae42a"
D_PRESAS = "bfb8788b-8ce3-475e-8bbd-dd1c5154c877"
D_PLANTAS = "a6cdb7ad-ec32-44aa-851d-684947df4243"

t_fiebre = tabla("30b18862-f126-41ac-b41f-ce7126f3ac9b", "Hoja1")
t_presas = tabla("4219d141-5084-4308-bda3-d44ca28a4f53", "cat_estatal")
t_plantas = [t for t in ci_r["d9a86127-179c-45c9-94ef-8eae89c0148f"]["tablas"]
             if "Plantas" in t["hoja"]][0]
h_fiebre, h_presas, h_plantas = H(t_fiebre), H(t_presas), H(t_plantas)
assert h_fiebre == "f03b5732507b88affaa1ea216befbbbd86fbe0b3cf1e24036c22292a8ae10014"
assert h_presas == "29af60e8a6e9e2026623388d9e06cddb2689bfd25de8db395ab97bf7e47eecfd"
assert h_plantas == "e928d39718d96e8ffa7b6c4e93204926c3d6ddfa8cfb320dd55b9d520e8f175c"

f1 = fila_dict(D_FIEBRE, 1)
f177 = fila_dict(D_FIEBRE, 177)
f178 = fila_dict(D_FIEBRE, 178)
h_f1, h_f177, h_f178 = H(f1), H(f177), H(f178)
assert h_f1 == cov_v[(D_FIEBRE, "1")]["huella_fila_diccionario"]
assert h_f177 == cov_v[(D_FIEBRE, "177")]["huella_fila_diccionario"]
assert h_f178 == cov_v[(D_FIEBRE, "178")]["huella_fila_diccionario"]

p1, p4 = fila_dict(D_PRESAS, 1), fila_dict(D_PRESAS, 4)
u9, u11 = fila_dict(D_PLANTAS, 9), fila_dict(D_PLANTAS, 11)
H_P1, H_P4, H_U9, H_U11 = H(p1), H(p4), H(u9), H(u11)
assert H_P1 == "87295257ea33a0a7d02963306433c01568b34189c09aa867351ac9f19faee0e4"
assert H_P4 == "d120834445f43d0bb67d135c256e73c91984a2fad6ec8ddbc5639c023dd44153"
assert H_U9 == "7d4b4ed61114b9f8b7bd8605475246ec1d22a3518f3798f67fdf4b0be570d632"
assert H_U11 == "d33c36c8f0d76e45ad837aba00fadf0bf6fe0b45105dfe5d404c005b27c8e788"
# Verificado: cobertura.json registra literalmente el mismo valor; no hay discrepancia
# (la anterior fue error de transcripcion propio, retirado).

NOM_FIEBRE = f1.get("Nombre variable")
DES_F1 = f1.get("Descripción")
# Control final: el generador materializa via valor() con strip; la descripcion del
# vinculo usa el valor materializado exacto (sin espacio final). La huella de fila
# RAW (con espacio) queda intacta.
DES_F1_MAT = DES_F1.strip()
assert DES_F1_MAT == cov_v[(D_FIEBRE, "1")]["descripcion"]
DES_U9 = u9.get("Descripción")
DES_U11 = u11.get("Descripción")

COLS_FIEBRE = [
    ("30b18862-f126-41ac-b41f-ce7126f3ac9b", "Fiebre manchada 2023",
     "https://example.org/mex-ontologi/file-column/30b18862-f126-41ac-b41f-ce7126f3ac9b%2FHoja1%2F1"),
    ("4121cf57-1e4a-4fb0-b175-3805edffca2c", "Fiebre manchada 2022",
     "https://example.org/mex-ontologi/file-column/4121cf57-1e4a-4fb0-b175-3805edffca2c%2FHoja1%2F1"),
    ("cc6c566f-3088-41cd-b99f-169c5cf6090c", "Fiebre manchada 2024",
     "https://example.org/mex-ontologi/file-column/cc6c566f-3088-41cd-b99f-169c5cf6090c%2FHoja1%2F1"),
]

DEP_LOTE1 = ("propuestas/pendientes-muse-r4/lote-1/entrega.json regla r4-lote-1-001 "
             "(concepto numero-identificacion-registro-rickettsia, estado completo-segunda-revision)")
decisiones = []
for rid, titulo, col in COLS_FIEBRE:
    decisiones.append({
        "columna": col, "recurso": rid, "campo": "ide_id",
        "decision": "proponer",
        "definicion_iri": f"https://example.org/mex-ontologi/definition/{D_FIEBRE}%2F1",
        "motivo": ("eleccion explicita de /1 por exclusion estructural, no por nombre: "
                   "las filas /177 y /178 reproducen el encabezado como dato "
                   "(Tipo='ide_sex', Formato='ide_eda_ano', ...) y su texto 'ide_col' nombra "
                   "la columna fisica pos 5, distinta de pos 1; la fila genuina /1 "
                   "(Numerico, ejemplo 13468731) corresponde a pos 1. "
                   "CONDICIONADO a aprobacion semantica de " + DEP_LOTE1 + "."),
        "evidencia": [
            f"data/portal/contenido-inspeccion.json recurso {rid} hoja Hoja1 pos 1 = 'ide_id', "
            "pos 5 = 'ide_col' (columna distinta)",
            "metodo_encabezado=heuristica_requiere_revision (rutina de captura)",
            f"data/portal/inspecciones/{D_FIEBRE}.json filas 175-176 vacias; filas 177-178 "
            "reproducen el encabezado con campos desplazados",
            f"huella_esquema={h_fiebre} huella_fila_1={h_f1} "
            f"huella_fila_177={h_f177} huella_fila_178={h_f178}",
            "cobertura: /177 y /178 fuera_del_nucleo_actual sin concepto (artefactos)",
            "dependencia explicita: " + DEP_LOTE1,
            f"definicion https://example.org/mex-ontologi/definition/{D_FIEBRE}%2F1",
        ],
    })

decisiones.append({
    "columna": "https://example.org/mex-ontologi/file-column/4219d141-5084-4308-bda3-d44ca28a4f53%2Fcat_estatal%2F1",
    "recurso": "4219d141-5084-4308-bda3-d44ca28a4f53", "campo": "Clave",
    "decision": "pendiente",
    "motivo": ("dos filas Clave con el mismo concepto pero distinta hoja y descripción "
               "(/1 Histórico_presas, /4 Catálogo_estatal); la hoja física 'cat_estatal' "
               "no iguala exactamente a ninguna tras normalizar (cat≠catálogo). "
               "No se resuelve por parecido."),
    "evidencia": [
        "data/portal/contenido-inspeccion.json recurso 4219d141-5084-4308-bda3-d44ca28a4f53 "
        "hoja cat_estatal pos 1 = 'Clave' (17 campos, sin columna Clave duplicada)",
        "metodo_encabezado=heuristica_requiere_revision (rutina de captura)",
        f"data/portal/inspecciones/{D_PRESAS}.json fila 1 hoja 'Histórico_presas', "
        "fila 4 hoja 'Catálogo_estatal'",
        f"huella_esquema={h_presas} huella_fila_1={H_P1} huella_fila_4={H_P4}",
        "cobertura: ambas respaldada_por_definicion, concepto clave-identificadora-presa",
    ],
})

C9 = ("https://example.org/mex-ontologi/file-column/d9a86127-179c-45c9-94ef-8eae89c0148f"
      "%2FPlantas%20El%C3%A9ctricas%20en%20Sonora%2F9")
C11 = ("https://example.org/mex-ontologi/file-column/d9a86127-179c-45c9-94ef-8eae89c0148f"
       "%2FPlantas%20El%C3%A9ctricas%20en%20Sonora%2F11")
decisiones.append({
    "columna": C9, "recurso": "d9a86127-179c-45c9-94ef-8eae89c0148f",
    "campo": "Unidad de Medida", "decision": "proponer",
    "definicion_iri": f"https://example.org/mex-ontologi/definition/{D_PLANTAS}%2F9",
    "motivo": ("encabezados idénticos distinguidos por posición ordinal y vecinos: "
               "columna 9/16 entre 'Capacidad Autorizada' (8) y 'Generación Estimada' (10), "
               "igual orden que las filas 8-9-10 del diccionario; descripción de capacidad. "
               "Regla existente r3a10-0286, sin crear regla nueva."),
    "evidencia": [
        "data/portal/contenido-inspeccion.json recurso d9a86127-179c-45c9-94ef-8eae89c0148f "
        "hoja Plantas Eléctricas en Sonora pos 8='Capacidad Autorizada' pos 9='Unidad de Medida' "
        "pos 10='Generación Estimada' pos 11='Unidad de Medida'",
        "metodo_encabezado=heuristica_requiere_revision (rutina de captura)",
        f"data/portal/inspecciones/{D_PLANTAS}.json orden 8-9-10-11 idéntico al esquema (16/16)",
        f"huella_esquema={h_plantas} huella_fila_9={H_U9}",
        "cobertura: /9 respaldada_por_definicion concepto unidad-capacidad-planta-electrica",
        f"definicion https://example.org/mex-ontologi/definition/{D_PLANTAS}%2F9 regla r3a10-0286",
    ],
})
decisiones.append({
    "columna": C11, "recurso": "d9a86127-179c-45c9-94ef-8eae89c0148f",
    "campo": "Unidad de Medida", "decision": "proponer",
    "definicion_iri": f"https://example.org/mex-ontologi/definition/{D_PLANTAS}%2F11",
    "motivo": ("columna 11/16 entre 'Generación Estimada' (10) y 'Energético Primario' (12), "
               "igual orden que las filas 10-11-12 del diccionario; descripción de generación. "
               "Regla existente r3a10-0288, sin crear regla nueva."),
    "evidencia": [
        "data/portal/contenido-inspeccion.json recurso d9a86127-179c-45c9-94ef-8eae89c0148f "
        "pos 10='Generación Estimada' pos 11='Unidad de Medida' pos 12='Energético Primario'",
        "metodo_encabezado=heuristica_requiere_revision (rutina de captura)",
        f"huella_esquema={h_plantas} huella_fila_11={H_U11}",
        "cobertura: /11 respaldada_por_definicion concepto unidad-generacion-planta-electrica",
        f"definicion https://example.org/mex-ontologi/definition/{D_PLANTAS}%2F11 regla r3a10-0288",
    ],
})

CRIT = ("Revisión explícita del campo en el esquema de este recurso y su fila de diccionario "
        "en el mismo conjunto: nombre, posición ordinal, vecinos, descripción y representación. "
        "Alcance de interpretación documental; no se validan valores ni se confirma "
        "pertenencia a catálogos.")
CRIT_FIEBRE = ("Exclusion estructural de filas artefacto /177 y /178 (encabezado repetido "
               "como dato, campos desplazados) y eleccion explicita de la fila genuina /1 "
               "para esta columna fisica: nombre, posicion, descripcion y fila completa. "
               "CONDICIONADO a aprobacion semantica de regla r4-lote-1-001 de lote-1. "
               "Alcance documental; no valida valores ni identidad.")
vinculos = [
    {"recurso": "d9a86127-179c-45c9-94ef-8eae89c0148f", "campo": "Unidad de Medida",
     "columna": C9, "diccionario": D_PLANTAS,
     "definicion_iri": f"https://example.org/mex-ontologi/definition/{D_PLANTAS}%2F9",
     "concepto": "unidad-capacidad-planta-electrica", "descripcion": DES_U9,
     "huella_esquema": h_plantas, "huella_fila_diccionario": H_U9, "criterio": CRIT},
    {"recurso": "d9a86127-179c-45c9-94ef-8eae89c0148f", "campo": "Unidad de Medida",
     "columna": C11, "diccionario": D_PLANTAS,
     "definicion_iri": f"https://example.org/mex-ontologi/definition/{D_PLANTAS}%2F11",
     "concepto": "unidad-generacion-planta-electrica", "descripcion": DES_U11,
     "huella_esquema": h_plantas, "huella_fila_diccionario": H_U11, "criterio": CRIT},
]
for rid, titulo, col in COLS_FIEBRE:
    vinculos.append(
        {"recurso": rid, "campo": "ide_id", "columna": col, "diccionario": D_FIEBRE,
         "definicion_iri": f"https://example.org/mex-ontologi/definition/{D_FIEBRE}%2F1",
         "concepto": "numero-identificacion-registro-rickettsia", "descripcion": DES_F1_MAT,
         "huella_esquema": h_fiebre, "huella_fila_diccionario": h_f1,
         "criterio": CRIT_FIEBRE + " Dependencia explicita: " + DEP_LOTE1 + "."})

entrega = {
    "decisiones_columnas": decisiones,
    "vinculos": vinculos,
    "decisiones_significados": [
        {"definicion_iri": f"https://example.org/mex-ontologi/definition/{D_FIEBRE}%2F1",
         "decision": "pendiente",
         "motivo": "significado propuesto por lote-1 (r4-lote-1-001); este rol no duplica "
                   "la decision y la toma como dependencia explicita de sus 3 vinculos",
         "evidencia": [f"diccionario {D_FIEBRE} variable 'ide_id' ejemplo '13468731'",
                       f"huella_fila_diccionario={h_f1}",
                       "dependencia: " + DEP_LOTE1]},
        {"definicion_iri": f"https://example.org/mex-ontologi/definition/{D_FIEBRE}%2F177",
         "decision": "pendiente",
         "motivo": "artefacto: fila de encabezado repetida como dato, no es definición; "
                   "solicitar exclusión, no interpretación",
         "evidencia": [f"diccionario {D_FIEBRE} fila 177 reproduce el encabezado",
                       f"huella_fila_diccionario={h_f177}"]},
        {"definicion_iri": f"https://example.org/mex-ontologi/definition/{D_FIEBRE}%2F178",
         "decision": "pendiente",
         "motivo": "artefacto: fila de encabezado repetida como dato, no es definición; "
                   "solicitar exclusión, no interpretación",
         "evidencia": [f"diccionario {D_FIEBRE} fila 178 reproduce el encabezado",
                       f"huella_fila_diccionario={h_f178}"]},
    ],
    "reglas": [],
    "conceptos_nuevos": {},
    "solicitudes_investigacion": [
        {"definicion_iri": f"https://example.org/mex-ontologi/definition/{D_FIEBRE}%2F1",
         "fuente_probable": "lote-1 (regla r4-lote-1-001 ya entregada)",
         "documento_requerido": "DEPENDENCIA LITERAL: los 3 vinculos fiebre ide_id -> /1 "
                                "verifican solo si se aprueba r4-lote-1-001 "
                                "(concepto numero-identificacion-registro-rickettsia); "
                                "sin esa aprobacion quedan sin efecto, no se recurre a /177 ni /178"},
        {"definicion_iri": f"https://example.org/mex-ontologi/definition/{D_PRESAS}%2F4",
         "fuente_probable": "publicador del conjunto 8c1f452e-7967-4c6b-a7b5-f2279360ad6c",
         "documento_requerido": "confirmación de que la hoja cat_estatal del recurso "
                                "4219d141 corresponde a la hoja Catálogo_estatal del diccionario "
                                "y si Histórico_presas comparte el mismo dominio de clave"},
        {"definicion_iri": "observacion:egresos-descripcion-urgencias",
         "fuente_probable": "publicador del conjunto 8993c917-47d8-4304-8141-5f481fe04301",
         "documento_requerido": "aclaración: Total_Egresos descrito como "
                                "«Total de urgencias atendidas»; confirmar si la columna cuenta "
                                "egresos o urgencias (huella fila 98c73e56ff407766447b52e08850d0b8669"
                                "f6979145b4c66fac1f1f83aec9f05)"},
        {"definicion_iri": "observacion:municipio-formato-ejemplo",
         "fuente_probable": "publicador del conjunto e262a488-69e5-4064-bd2b-191c5c8fc9f9",
         "documento_requerido": "significado municipal ya resuelto (vinculo concepto municipio); "
                                "pendiente solo composicion del codigo: formato nnn frente a ejemplo "
                                "26048; confirmar si CVE_MUN es municipal (3) o CVEGEO compuesta (5), "
                                "sin asignar sistema CVEGEO "
                                "(huella fila 35fb21e0399a3deac2b1b7f445571a06988617992f9c59a5f2f1158800cadf4e)"},
        {"definicion_iri": "observacion:fecha-ejemplo-numerico",
         "fuente_probable": "publicador del conjunto 8b4edefe-cb1a-401c-90c6-05548779defd",
         "documento_requerido": "significado fecha-precipitacion ya resuelto (vinculo vigente); "
                                "pendiente solo codificacion: formato DD/MM/AAAA frente a ejemplo 45658 "
                                "(serial Excel); confirmar representacion antes de convertir "
                                "(huella fila 30327f4dedbb05f89246855460f47751bd99521eb112577e5fd359df460b0754)"},
        {"definicion_iri": "observacion:anio-nacimientos-2024",
         "fuente_probable": "publicador del conjunto df2d60f5-2243-4bb0-885a-941aa8a657f5",
         "documento_requerido": "confirmación de que el campo datastore «a–o» del recurso "
                                "ffca84a8 es año (mojibake de ñ) y equivale a la variable año "
                                "del diccionario 6bcf5b63-0855-4f3b-81a0-4bca82e97272"},
        {"definicion_iri": "observacion:anio-divorcios-2023-nota-historica",
         "fuente_probable": "ontologia/semantica.json (865 vinculos vigentes)",
         "documento_requerido": "NINGUNA REVISION NUEVA: el alias anio_registro -> año_registro "
                                "para f05dfd7e-88c9-42c4-ab88-e849fc277155 ya esta resuelto "
                                "como documental_revisada (variable año_registro, concepto anio-registro); "
                                "la observacion se conserva solo como nota historica"},
    ],
}

out = ROOT / "propuestas/pendientes-muse-r4/ambiguedades/entrega.json"
out.write_text(json.dumps(entrega, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("entrega.json OK;", out.stat().st_size, "bytes")
