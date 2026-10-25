# Generador de entrega.json + evidencia/http-log.json (grupo salud-nacimientos).
# Verifica SHAs contra bytes reales; falla si algo no existe.
import json, hashlib, datetime

ROOT = "propuestas/investigacion-post-r6/salud-nacimientos"
EV = ROOT + "/evidencia"
FECHA = "2026-10-24"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# --- http-log (trazabilidad de consultas web) ---
HTTPLOG = [
 {"url": "http://www.dgis.salud.gob.mx/descargas/pdf/Manual_de_Instalacion_y_Operacion_del_SINAC.pdf",
  "fecha_consulta": FECHA, "http_status": 200, "tipo_observado": "application/pdf (magia %PDF-1.4 verificada)",
  "tamano_bytes": 7710525, "sha256": sha(EV + "/Manual_Instalacion_Operacion_SINAC_dgis.pdf"),
  "archivo_local": EV + "/Manual_Instalacion_Operacion_SINAC_dgis.pdf",
  "localizador": "portada P1-P3: Manual de Instalacion y Operacion SINAC, Certificado de Nacimiento Modelo 2015, SINAC Version 2.0.1, Primera edicion 2015",
  "fragmento": "Certificado de Nacimiento Modelo 2015, SINAC Version 2.0.1; 0 menciones a 2022"},
 {"url": "https://www.gob.mx/cms/uploads/attachment/file/16345/CN_ManualLlenado.pdf",
  "fecha_consulta": FECHA, "http_status": 200, "tipo_observado": "application/pdf (magia %PDF-1.4 verificada)",
  "tamano_bytes": 1459282, "sha256": sha(ROOT + "/temporales/CN_ManualLlenado_gobmx.pdf"),
  "archivo_local": ROOT + "/temporales/CN_ManualLlenado_gobmx.pdf",
  "localizador": "portada: Manual de Llenado del Certificado de Nacimiento, Modelo 2015",
  "fragmento": "byte-identico al preservado R5 (a97b4ec4...); edicion 2015, 0 menciones a 2022"},
 {"url": "http://www.dgis.salud.gob.mx/descargas/sinac/pdf/Metodologia_para_generar_indice_de_calidad_SINAC-SEED1_20200518.pdf",
  "fecha_consulta": FECHA, "http_status": 200, "tipo_observado": "application/pdf (magia %PDF-1.6 verificada)",
  "tamano_bytes": 2041492, "sha256": sha(EV + "/Metodologia_calidad_SINAC-SEED_20200518.pdf"),
  "archivo_local": EV + "/Metodologia_calidad_SINAC-SEED_20200518.pdf",
  "localizador": "P1: Metodologia para generar el indicadores de la calidad de la Informacion del SINAC y SEED; 17 pp.",
  "fragmento": "indice de calidad (cobertura/consistencia/oportunidad); 0 definiciones de variable, 0 codebook"},
 {"url": "http://www.dgis.salud.gob.mx/contenidos/sinais/s_sinac.html",
  "fecha_consulta": FECHA, "http_status": 200, "tipo_observado": "text/html (captura cruda verificada)",
  "tamano_bytes": 6551, "sha256": sha(EV + "/cap_dgis_sinac.html"),
  "archivo_local": EV + "/cap_dgis_sinac.html",
  "localizador": "pagina oficial SINAC: Ultima modificacion Jueves 13 de enero de 2022; unico documento enlazado = metodologia 2020",
  "fragmento": "Metodologia para generar el indice de la calidad de la informacion del subsistema SINAC; ningun manual de nacimiento enlazado"},
 {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/530",
  "fecha_consulta": FECHA, "http_status": 200, "tipo_observado": "text/html (captura cruda verificada)",
  "tamano_bytes": 71502, "sha256": sha(EV + "/cap_inegi_530.html"),
  "archivo_local": EV + "/cap_inegi_530.html",
  "localizador": "MEX-SALUD-SINAC-2018: periodo de referencia 2017-01-01 a 2017-12-31; documentacion concluida 2018-09-03",
  "fragmento": "La DGIS elaborara los manuales de implementacion y llenado; la pagina DGIS solo publica cubos y metodologia"},
 {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/530/data-dictionary/F1?file_name=SINAC2018",
  "fecha_consulta": FECHA, "http_status": 200, "tipo_observado": "text/html (captura cruda verificada)",
  "tamano_bytes": 148052, "sha256": sha(EV + "/cap_inegi_530_dd.html"),
  "archivo_local": EV + "/cap_inegi_530_dd.html",
  "localizador": "diccionario nacional SINAC2018: 62 variables V1-V62 con etiqueta y pregunta del CN (datos 2017)",
  "fragmento": "V18 orden_nac / V19 aten_pren / V35 apgarh / V48 clues / V54 cert_por; nombres minusculos con guion bajo, 62 vars vs 106 columnas locales"},
 {"url": "https://dof.gob.mx/nota_detalle_popup.php?codigo=5389287",
  "fecha_consulta": FECHA, "http_status": 200, "tipo_observado": "text/html (captura cruda verificada)",
  "tamano_bytes": 71216, "sha256": sha(EV + "/cap_dof_5389287.html"),
  "archivo_local": EV + "/cap_dof_5389287.html",
  "localizador": "Lineamientos de Operacion del Certificado Electronico de Nacimiento (DOF 05-mar-2014): rol Codificador con CIE-10 y catalogos contenidos en el eSINAC; Manual para la Expedicion del CN anunciado sin URL",
  "fragmento": "codificacion de patologias con base en la CIE-10 y de ocupacion habitual de acuerdo a los catalogos contenidos en el eSINAC; sin codebook publicado ni vinculo a Sonora 2022"},
]
open(EV + "/http-log.json", "w", encoding="utf-8").write(json.dumps(HTTPLOG, ensure_ascii=False, indent=1))

B = "propuestas/investigacion-post-r6/salud-nacimientos"
FUENTES = [
 {"clave": "asignacion", "ruta": "propuestas/depuracion-post-r6/significados/pendientes.json",
  "sha256": sha("propuestas/depuracion-post-r6/significados/pendientes.json"), "fecha_consulta": FECHA,
  "localizador": "/significados[n=33..85, grupo_fuente=salud-nacimientos]",
  "aplicabilidad": "Asignacion: exactamente 53 IRIs del grupo; diccionario 22202305, recurso 46977217 (SINAC 2022)."},
 {"clave": "diccionario-local", "ruta": "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json",
  "sha256": sha("data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json"), "fecha_consulta": FECHA,
  "localizador": "/definiciones (106 filas; /definiciones/<fila-1> por ID)",
  "aplicabilidad": "Fila local verificada por variable: las 53 siguen 'Pendiente de especificar' sin catalogo (re-verificado 2026-10-24)."},
 {"clave": "vista-depurada", "ruta": "reports/pendientes-depurados.json",
  "sha256": sha("reports/pendientes-depurados.json"), "fecha_consulta": FECHA,
  "localizador": "por_grupo.salud-nacimientos=53; por_conjunto.Informacion Sobre Nacimientos=53",
  "aplicabilidad": "Cotejo de conteo del grupo."},
 {"clave": "r6-salud", "ruta": "propuestas/pendientes-muse-r6/salud/entrega.json",
  "sha256": sha("propuestas/pendientes-muse-r6/salud/entrega.json"), "fecha_consulta": FECHA,
  "localizador": "/decisiones_significados (53 con diccionario 22202305); novedad_r6",
  "aplicabilidad": "Linea R6 agotada reutilizada como base, no repetida: manual SEED 2022 verificado sin vinculo; pagina DGIS sin manual; Modelo 2015 sin vigencia; Guia 2025 post-periodo."},
 {"clave": "package-nac", "ruta": "propuestas/pendientes-muse-r6/salud/evidencia/package_nacimientos.json",
  "sha256": sha("propuestas/pendientes-muse-r6/salud/evidencia/package_nacimientos.json"), "fecha_consulta": FECHA,
  "localizador": "result.resources: Diccionario 22202305 + XLSX 46977217 (2022-01-01 a 2022-09-26); version=null, url=null, fuentes_extras=''",
  "aplicabilidad": "Sistema SINAC + periodo declarados por el publicador; sin edicion ni vinculo de version (F4 ausente)."},
 {"clave": "m2015", "ruta": "propuestas/pendientes-muse-r5/catalogos-web/evidencia/CN_ManualLlenado_2015.pdf",
  "sha256": sha("propuestas/pendientes-muse-r5/catalogos-web/evidencia/CN_ManualLlenado_2015.pdf"), "fecha_consulta": FECHA,
  "url": "https://www.gob.mx/cms/uploads/attachment/file/16345/CN_ManualLlenado.pdf",
  "localizador": "portada P2: Manual de Llenado del Certificado de Nacimiento, Modelo 2015, SINAC; 91 pp.; preguntas numeradas 2-37",
  "aplicabilidad": "Manual nacional preservado examinado por ID en esta ronda; edicion 2015 sin vigencia declarada a 2022; servido hoy por gob.mx con bytes identicos (ver http-log)."},
 {"clave": "sinac-op", "ruta": EV + "/Manual_Instalacion_Operacion_SINAC_dgis.pdf",
  "sha256": sha(EV + "/Manual_Instalacion_Operacion_SINAC_dgis.pdf"), "fecha_consulta": FECHA,
  "url": "http://www.dgis.salud.gob.mx/descargas/pdf/Manual_de_Instalacion_y_Operacion_del_SINAC.pdf",
  "localizador": "P1-P3: Manual de Instalacion y Operacion SINAC, Certificado de Nacimiento Modelo 2015, SINAC Version 2.0.1, Primera edicion 2015; 115 pp.",
  "aplicabilidad": "Fuente primaria DGIS NUEVA frente a R6: tambien edicion 2015, 0 menciones a 2022; sin diccionario de variables ni codebook."},
 {"clave": "met2020", "ruta": EV + "/Metodologia_calidad_SINAC-SEED_20200518.pdf",
  "sha256": sha(EV + "/Metodologia_calidad_SINAC-SEED_20200518.pdf"), "fecha_consulta": FECHA,
  "url": "http://www.dgis.salud.gob.mx/descargas/sinac/pdf/Metodologia_para_generar_indice_de_calidad_SINAC-SEED1_20200518.pdf",
  "localizador": "P1: Metodologia para generar el indicadores de la calidad de la Informacion del SINAC y SEED; 17 pp.",
  "aplicabilidad": "Unico documento enlazado hoy por la pagina oficial SINAC; metodologia de indice de calidad, sin definiciones ni codebook: examinado y descartado."},
 {"clave": "inegi-dd", "ruta": EV + "/cap_inegi_530_dd.html",
  "sha256": sha(EV + "/cap_inegi_530_dd.html"), "fecha_consulta": FECHA,
  "url": "https://www.inegi.org.mx/rnm/index.php/catalog/530/data-dictionary/F1?file_name=SINAC2018",
  "localizador": "diccionario nacional SINAC2018, 62 variables V1-V62 (datos 2017): etiqueta + pregunta del CN por variable",
  "aplicabilidad": "Contraparte nacional NUEVA examinada por ID: preguntas exactas citadas por decision; edicion/periodo distintos (2017 vs 2022-09-26), 62 vars vs 106 columnas, nombres distintos, sin tabla de equivalencias del publicador."},
 {"clave": "dof-cen", "ruta": EV + "/cap_dof_5389287.html",
  "sha256": sha(EV + "/cap_dof_5389287.html"), "fecha_consulta": FECHA,
  "url": "https://dof.gob.mx/nota_detalle_popup.php?codigo=5389287",
  "localizador": "Lineamientos CEN (DOF 05-mar-2014): rol Codificador (CIE-10 + catalogos en eSINAC); Acuerdo de modelos DOF 27-ago-2014",
  "aplicabilidad": "Marco primario: catalogos de ocupacion/CIE viven dentro del eSINAC sin publicacion ni codebook; sin vinculo a columnas de Sonora 2022."},
 {"clave": "seed22", "ruta": "propuestas/pendientes-muse-r6/salud/evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf",
  "sha256": sha("propuestas/pendientes-muse-r6/salud/evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf"), "fecha_consulta": FECHA,
  "localizador": "P1: Manual de Llenado del Certificado de Defuncion y Certificado de Muerte Fetal Modelo 2022 (SEED)",
  "aplicabilidad": "AMBITO: defunciones/muerte fetal, no nacimientos. Explica por que NO aplica a SINAC: otro subsistema, otro certificado, otras variables; usarlo seria cruce prohibido."},
 {"clave": "http-log", "ruta": EV + "/http-log.json",
  "sha256": sha(EV + "/http-log.json"), "fecha_consulta": FECHA,
  "localizador": "7 consultas HTTP 200 con URL, fecha, tamano, SHA256, archivo local y fragmento",
  "aplicabilidad": "Trazabilidad de toda la evidencia web de esta ronda."},
]

LIM = [
 "Alcance simultaneo por conjunto, diccionario, definicion, nombre y descripcion; no autoriza cruces, homologaciones ni equivalencias.",
 "La homonimia con el manual nacional o el diccionario INEGI no acredita vinculo local: sin tabla pregunta-manual<->columna-local ni declaracion del publicador no hay promocion.",
 "Evidencia negativa acotada a las busquedas documentadas en http-log y fuentes; no ausencia universal.",
]

# contraparte nacional examinada por variable: (cita exacta, por que falla la correspondencia formal)
C = {
 "ORDENNACIMIENTO": ("INEGI V18 orden_nac: 11. Orden del nacimiento (considere vivos, muertos, multiples)", "nombre local distinto (mayusculas sin guiones); edicion 2017 vs recurso 2022; sin tabla de equivalencias del publicador"),
 "ATENCIONPRENATAL": ("INEGI V19 aten_pren: 12. Atencion prenatal. 12.1 Recibio atencion? Si/No/Se ignora; M2015 pregunta 12", "pregunta nacional sin mapa a columna local; sin codebook local ni vinculo edicion-recurso-periodo"),
 "ATENCIONPRENATALD": ("columna D: descripcion textual asociada a ATENCIONPRENATAL; sin contraparte en INEGI 62 vars", "columna gemela D sin definicion propia en ninguna fuente; inferir su sentido seria join inventado"),
 "TRIMESTREPRIMERCONSULTA": ("INEGI V20 trim_cons: 12.2 Trimestre en el que recibio la primera consulta; M2015: Trimestre en el que recibio la primera consulta", "sin valores/codigos publicados para la columna local ni vinculo del publicador"),
 "TRIMESTREPRIMERCONSULTAD": ("columna D asociada a TRIMESTREPRIMERCONSULTA; sin contraparte en INEGI", "idem columnas D"),
 "SOBREVIVIOPARTO": ("INEGI V22 sob_parto: 13. Vive la madre del nacido vivo? Si/No; M2015 pregunta 13", "pregunta nacional sin mapa a columna local; sin vinculo edicion-recurso-periodo"),
 "SOBREVIVIOPARTOD": ("columna D asociada a SOBREVIVIOPARTO; sin contraparte en INEGI", "idem columnas D"),
 "AFILIACION": ("INEGI V23/V24 derhab: 14. Afiliacion a servicio de salud (Ninguna/IMSS/ISSSTE/.../Se ignora); M2015: AFILIACION A SERVICIOS DE SALUD", "lista nacional de opciones sin mapa a codigos locales; ejemplo local aislado (2) no acredita catalogo"),
 "AFILIACIOND": ("columna D asociada a AFILIACION; sin contraparte en INEGI", "idem columnas D"),
 "INTERRUMPIOESTUDIOS": ("sin contraparte: INEGI solo V25 niv_escol (15. Escolaridad); M2015 sin rubro de interrupcion", "ni el manual ni el diccionario nacional definen esta columna; solo el publicador puede fijarla"),
 "INTERRUMPIOESTUDIOSD": ("columna D asociada; sin contraparte en ninguna fuente", "idem columnas D"),
 "CLAVEOCUPACIONHABITUAL": ("INEGI V27 cveocuphab: Codigo de la ocupacion (sin etiqueta ni pregunta); DOF: catalogos de ocupacion contenidos en el eSINAC, no publicados", "codigo sin codebook publicado; sin mapa a columna local"),
 "CLAVEOCUPACIONHABITUALD": ("INEGI V26 ocuphab: 16. Ocupacion habitual; M2015: OCUPACION HABITUAL", "texto nacional sin mapa a columna D local; sin vinculo del publicador"),
 "APGAR": ("INEGI V35 apgarh: 22.1 Apgar (a los 5 minutos); M2015 22.1 APGAR", "escala nacional sin mapa a columna local ni unidad declarada en el diccionario local"),
 "SILVERMAN": ("INEGI V36 silverman: 22.2 Silverman (a los 5 minutos); M2015 22.2 SILVERMAN", "idem APGAR"),
 "TAMIZAUDITIVO": ("INEGI V41 tam_aud: 23. Tamiz auditivo. Si/No; M2015 23. TAMIZ AUDITIVO", "opciones nacionales sin mapa a codigos locales"),
 "TAMIZAUDITIVOD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "VACUNA_BCG": ("INEGI V37 bcg: 24.1 BCG Si/No; M2015 24 BCG", "idem tamiz"),
 "VACUNA_BCGD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "VACUNAHEPATITIS_B": ("INEGI V38 hep_b: 24.2 Hepatitis B Si/No; M2015 24 Hepatitis B", "idem tamiz"),
 "VACUNAHEPATITIS_BD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "VITAMINA_A": ("INEGI V39 vit_a: 24.3 (A) Si/No; M2015 Vitaminas (A)", "idem tamiz"),
 "VITAMINA_AD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "VITAMINA_K": ("INEGI V40 vit_k: 24.4 (K) Si/No; M2015 Vitaminas (K)", "idem tamiz"),
 "VITAMINA_KD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "PRODUCTOEMBARAZO": ("INEGI V42 producto: 25. Producto de un embarazo (Unico/Gemelar/Tres o mas); M2015: PRODUCTO DE UN EMBARAZO", "opciones nacionales sin mapa a codigos locales"),
 "PRODUCTOEMBARAZOD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "ORDENPRODUCTO": ("sin contraparte directa: M2015 solo indica expedir un certificado por cada producto nacido", "sin pregunta ni codigo nacional para esta columna"),
 "TOTALPRODUCTOS": ("contexto INEGI V42 (numero total de productos); M2015: marque el numero total de productos", "conteo sin definicion de columna local ni vinculo"),
 "ANOMALIACIE1": ("INEGI V43 acelrn: 26. Anomalias congenitas, enfermedades o lesiones del nacido vivo", "rubro nacional sin mapa a columna local; sin edicion CIE aplicable declarada al recurso 2022"),
 "CODIGOCIEANOMALIA1": ("INEGI V44 cve_cie: Codigo CIE, uso exclusivo del personal codificador; DOF: codificacion con base en la CIE-10", "edicion CIE aplicable al recurso 2022 no declarada por el publicador; sin mapa a columna local"),
 "ANOMALIACIE2": ("segunda anomalia: INEGI solo documenta una (V43); sin contraparte", "estructura local de 2 anomalias sin correlato nacional publicado"),
 "CODIGOCIEANOMALIA2": ("segundo codigo: INEGI solo uno (V44); sin contraparte", "idem anterior"),
 "RESOLUCIONEMBARAZO": ("INEGI V45 procnac: 27. Resolucion del embarazo (Eutocico 1/Distocico 2/Cesarea 3/Otro 8); M2015: RESOLUCION DEL EMBARAZO", "codigos nacionales sin mapa a codigos locales"),
 "RESOLUCIONEMBARAZOD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "UTILIZOFORCEPS": ("INEGI V45 contexto: 27. Se usaron forceps? Si(1)/No(2); M2015: Se usaron forceps?", "codigos nacionales sin mapa a columna local"),
 "UTILIZOFORCEPSD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "CLUES": ("INEGI V48 clues: 28.2 Clave Unica de Establecimientos de Salud (CLUES); M2015 28.2 CLUES", "catalogo CLUES nacional sin vinculo a la columna local ni vigencia declarada al recurso 2022"),
 "TIEMPOTRASLADO": ("sin contraparte en INEGI 62 vars ni en M2015", "columna sin definicion en ninguna fuente primaria examinada"),
 "PERSONALATENDIO": ("INEGI V49 atendio: 29. Persona que atendio el parto (pregunta sin opciones en captura); M2015 29. PERSONA QUE ATENDIO EL PARTO", "pregunta nacional sin codebook publicado para la columna local"),
 "PERSONALATENDIOD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "TIPOMEDICOATENDIO": ("contexto INEGI V49/V55 (Medico Gineco-obstetra/Otro/Residente/General/MPSS/MIP); M2015: seleccione el tipo de medico", "tipologia nacional sin mapa a codigos locales"),
 "TIPOMEDICOATENDIOD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "CERTIFICADOPOR": ("INEGI V54 cert_por: 32. Certificado por (Medico pediatra 1/.../Partera 5/...); M2015 32. CERTIFICADO POR", "codigos nacionales sin mapa a codigos locales"),
 "CERTIFICADOPORD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "CLUESCERTIFICA": ("contexto INEGI V48 + M2015 34. Unidad medica que proporciono el certificado; sin variable nacional exacta", "CLUES de certificante fuera de unidad medica sin correlato publicado ni vinculo"),
 "ENTIDADFEDERATIVACERTIFICA": ("contexto INEGI V56 ent_cert: 35.10 Entidad federativa (del certificante); M2015 34-35", "ambito certificante vs unidad medica ambiguo en fuentes; sin mapa a columna local"),
 "ENTIDADFEDERATIVACERTIFICAD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "MUNICIPIOCERTIFICA": ("contexto INEGI V57 mpo_cert: 35.9 Municipio o delegacion; M2015 34-35", "idem entidad"),
 "MUNICIPIOCERTIFICAD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "LOCALIDADCERTIFICA": ("contexto INEGI V58 loc_cert: 35.8 Localidad; M2015 34-35", "idem entidad"),
 "LOCALIDADCERTIFICAD": ("columna D asociada; sin contraparte en INEGI", "idem columnas D"),
 "FECHACERTIFICADO": ("INEGI V59 fech_cert: 37. Fecha de certificacion (D/M/A); M2015 37", "formato nacional sin mapa a formato de la columna local"),
}

asig = json.load(open("propuestas/depuracion-post-r6/significados/pendientes.json", encoding="utf-8"))
nac = [s for s in asig["significados"] if s["grupo_fuente"] == "salud-nacimientos"]
assert len(nac) == 53, len(nac)
insp = json.load(open("data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json", encoding="utf-8"))
F = {f["clave"]: f for f in FUENTES}

decisiones = []
for s in nac:
    var = s["variable"]
    fila = int(s["fila"])
    idx = fila - 1
    assert insp["definiciones"][idx]["Nombre variable"] == var, (fila, var)
    cita, falla = C[var]
    hub = s["huella_fila_diccionario"]
    e2ruta = "inegi-dd" if cita.startswith("INEGI") or cita.startswith("contexto INEGI") else ("m2015" if "M2015" in cita or "Modelo" in cita else "inegi-dd")
    if "sin contraparte" in cita and "M2015" not in cita and "DOF" not in cita:
        e2ruta = "inegi-dd"
    if "DOF" in cita:
        e2ruta = "dof-cen"
    if "M2015" in cita and ("INEGI" not in cita and "contexto" not in cita):
        e2ruta = "m2015"
    decisiones.append({
     "definicion_iri": s["definicion_iri"],
     "variable": var,
     "descripcion_original": s["descripcion_original"],
     "huella_fila_diccionario": hub,
     "estado": "sigue_pendiente",
     "evidencia": [
      {"ruta": F["diccionario-local"]["ruta"], "sha256": F["diccionario-local"]["sha256"],
       "localizador": f"/definiciones/{idx} (fila {fila}, variable {var})",
       "afirmacion_soportada": "fila local verificada 2026-10-24: Descripcion='Pendiente de especificar', Catalogo de referencia='', Formato/Unidad sin definicion; tipo y ejemplo no definen el significado"},
      {"ruta": F[e2ruta]["ruta"], "sha256": F[e2ruta]["sha256"],
       "localizador": F[e2ruta]["localizador"],
       "afirmacion_soportada": f"contraparte nacional examinada: {cita}. Falla formal: {falla}"},
      {"ruta": F["http-log"]["ruta"], "sha256": F["http-log"]["sha256"],
       "localizador": "entradas " + ("inegi-dd/dof-cen" if e2ruta in ("inegi-dd", "dof-cen") else e2ruta),
       "afirmacion_soportada": "consulta primaria HTTP 200 del 2026-10-24 con SHA256 de bytes; sin declaracion del publicador que vincule edicion-recurso-periodo a Sonora 2022"},
     ],
     "vinculo_fuente_local": "SIN VINCULO: ninguna fuente del publicador (diccionario, nota, codebook o tabla pregunta-manual<->columna-local) conecta esta fila (conjunto 940de7d8, diccionario 22202305, fila %d, huella %s) con el recurso 46977217 (2022-01-01 a 2022-09-26) ni con edicion/manual alguno; la contraparte nacional citada es homonimia sin mapa local." % (fila, hub[:16]),
     "evidencia_faltante": "Exactamente lo requerido: " + s["evidencia_documental_exacta_faltante"],
     "motivo": "sigue_pendiente: " + s["dictamen_r6_motivo"] + " | Ronda actual: examen por ID de primarias SINAC (Modelo 2015 gob.mx/DGIS, metodologia 2020, diccionario INEGI 2017, DOF CEN) sin promocion: " + falla,
     "limites": LIM,
    })

entrega = {
 "grupo_fuente": "salud-nacimientos",
 "generado_en_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "ids_asignados": 53,
 "ids_decididos": len(decisiones),
 "propuestas_respaldadas": 0,
 "siguen_pendientes": sum(1 for d in decisiones if d["estado"] == "sigue_pendiente"),
 "fuentes": FUENTES,
 "decisiones": decisiones,
 "hueco_exactamente_identificado": "Falta el vinculo del publicador entre cada fila (conjunto+diccionario+fila+huella) y el recurso 46977217 (SINAC 2022-01-01 a 2022-09-26): diccionario corregido con descripciones, o nota con descripcion+codebook+tabla pregunta-manual<->columna-local y edicion aplicable. Las primarias nacionales examinadas (Modelo 2015, metodologia 2020, INEGI 2017, DOF 2014) no lo contienen y no pueden sustituirlo.",
 "busquedas_negativas_limitadas": [
  "Pagina oficial SINAC 2026-10-24: ningun manual de nacimiento enlazado (solo metodologia 2020).",
  "Manual Instalacion y Operacion SINAC (DGIS, nuevo): edicion 2015, 0 menciones a 2022.",
  "Modelo 2015 (gob.mx, bytes identicos a R5): sin vigencia a 2022; sin codebook ni mapa a columnas locales.",
  "INEGI SINAC2018 (datos 2017, 62 vars): edicion/periodo/nombres distintos; sin equivalencias del publicador.",
  "DOF CEN 2014: catalogos de ocupacion/CIE dentro del eSINAC, no publicados; sin vinculo a Sonora 2022.",
  "SEED Modelo 2022: ambito defunciones/muerte fetal; cruce a nacimientos prohibido.",
 ],
}
open(B + "/entrega.json", "w", encoding="utf-8").write(json.dumps(entrega, ensure_ascii=False, indent=1))
print("decisiones:", len(decisiones), "sha:", sha(B + "/entrega.json"))
