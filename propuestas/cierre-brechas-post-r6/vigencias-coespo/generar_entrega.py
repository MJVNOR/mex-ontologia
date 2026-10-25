"""Generador de entrega vigencias-coespo (V09,V10,V11,V12,V15,V16).
Serializa con json.dumps; calcula SHA-256 reales de la evidencia local.
Solo escribe dentro de propuestas/cierre-brechas-post-r6/vigencias-coespo/.
"""
import hashlib
import json
from pathlib import Path

BASE = Path("propuestas/cierre-brechas-post-r6/vigencias-coespo")
EV = BASE / "evidencia"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


asig = json.loads((BASE / "asignacion.json").read_text(encoding="utf-8"))
casos = {c["id"]: c for c in asig["casos"]}
assert set(casos) == {"V09", "V10", "V11", "V12", "V15", "V16"}, sorted(casos)

FECHA = "2026-10-24"
XLSX_SHA = "ea54aad30b7342ce678d1d66157325a5cbaa492380ee4d807b20918198c5b0f5"

ev_archivos = [
    "propuestas/cierre-brechas-post-r6/vigencias-coespo/evidencia/coespo-proyecciones-poblacion-extracto.md",
    "propuestas/cierre-brechas-post-r6/vigencias-coespo/evidencia/coespo-publicacion-2024-07-11-extracto.md",
    "propuestas/cierre-brechas-post-r6/vigencias-coespo/evidencia/dataset-grupos-quinquenales-extracto.md",
    "propuestas/cierre-brechas-post-r6/vigencias-coespo/evidencia/catalogo-recurso-d7c4b8b2-metadatos.md",
    "propuestas/cierre-brechas-post-r6/vigencias-coespo/evidencia/verificacion-local-xlsx.md",
]
for r in ev_archivos:
    assert Path(r).exists(), r

hoja = {
    "V09": "Catalogo_Municipios / CLAVE",
    "V10": "Catalogo_Estado / CLAVE_ENT",
    "V11": "Catalogo_Municipios / CLAVE",
    "V12": "Catalogo_Estado / CLAVE_ENT",
    "V15": "Catalogo_Municipios / CLAVE",
    "V16": "Catalogo_Estado / CLAVE_ENT",
}
periodo = {
    "V09": "1990-2019 reconstruccion; 2020-2040 proyecciones",
    "V10": "1990-2019 reconstruccion; 2020-2040 proyecciones",
    "V11": "1990-2019 reconstruccion; 2020-2040 proyecciones",
    "V12": "1990-2019 reconstruccion; 2020-2040 proyecciones",
    "V15": "1990-2040",
    "V16": "1990-2040",
}

MOTIVO = (
    "sigue_pendiente: F3+F4 ausentes. Pistas nuevas examinadas 2026-10-24 "
    "(pagina COESPO Proyecciones de Poblacion; publicacion COESPO 11-07-2024; "
    "pagina de recurso Catalogo d7c4b8b2 con metadatos 05-09-2024): ninguna "
    "declara edicion/version/fecha del catalogo.xlsx (sha {sha}, {hj}) ni lo "
    "vincula con {per}. La publicacion COESPO 11-07-2024 solo cita la base de "
    "DATOS CONAPO 1990-2040 (contexto F3 parcial de fuente, ya conocido por "
    "W05/W06), sin edicion del catalogo local. Las fechas de portal "
    "(05-09-2024) y de API/core-properties estan excluidas por el criterio de "
    "aceptacion. Interior xlsx re-verificado hoy: sin celdas de version/periodo. "
    "Desfase de corte intacto (local vs CONAPO 1990-2020/2021-2040)."
)

FALTANTE = (
    "Documento del publicador (COESPO/DEP-CAT-R6-04) que cite edicion/version/fecha "
    "de catalogo.xlsx (sha {sha}, {hj}) y recurso {rec} y periodos de aplicacion "
    "({per}), con fecha o firma; mas aclaracion del desfase de corte vs CONAPO "
    "09-05-2024. Verificable (URL o copia local con SHA)."
)

decisiones = []
for vid in ["V09", "V10", "V11", "V12", "V15", "V16"]:
    c = casos[vid]
    rec = c["catalogo"]["recurso_catalogo"]
    decisiones.append(
        {
            "id": vid,
            "estado": "sigue_pendiente",
            "original": c,
            "motivo": MOTIVO.format(sha=XLSX_SHA, hj=hoja[vid], per=periodo[vid]),
            "evidencia_faltante": FALTANTE.format(
                sha=XLSX_SHA, hj=hoja[vid], rec=rec, per=periodo[vid]
            ),
            "evidencia": [
                {
                    "ruta": r,
                    "sha256": sha(Path(r)),
                    "localizador": loc,
                    "afirmacion_soportada": af,
                }
                for (r, loc, af) in [
                    (
                        ev_archivos[0],
                        "literales de descargas + seccion 'Lo que NO contiene'",
                        "La pagina COESPO (pista nueva) no declara edicion/version/fecha del catalogo ni vinculo con periodos.",
                    ),
                    (
                        ev_archivos[1],
                        "cuerpo literal + seccion 'Lo que NO contiene'",
                        "COESPO 11-07-2024 cita la base de datos CONAPO 1990-2040, sin edicion del catalogo local ni periodos de aplicacion.",
                    ),
                    (
                        ev_archivos[2],
                        "Descripcion + Fuentes extras",
                        "El conjunto CKAN declara periodos por titulo y fuente CONAPO, sin edicion del catalogo (re-verificacion W05).",
                    ),
                    (
                        ev_archivos[3],
                        "tabla Metadatos",
                        "El recurso Catalogo solo trae fechas operativas de portal (05-09-2024), que no acreditan F3+F4.",
                    ),
                    (
                        ev_archivos[4],
                        "Interior openpyxl + SHA",
                        "catalogo.xlsx (sha ea54aad3) sin celdas de version/periodo; 2475 municipios = procedencia, no vigencia.",
                    ),
                ]
            ],
            "limites": c["limites"],
        }
    )

fuentes = [
    {
        "ruta": r,
        "sha256": sha(Path(r)),
        "url": u,
        "fecha_consulta": FECHA,
        "localizador": loc,
    }
    for (r, u, loc) in [
        (
            ev_archivos[0],
            "https://coespo.sonora.gob.mx/informacion-institucional/indicadores/proyecciones-de-poblacion",
            "lista de descargas; ausencia de declaracion de edicion del catalogo",
        ),
        (
            ev_archivos[1],
            "https://coespo.sonora.gob.mx/acciones/dependencia/publicacion-de-proyecciones-de-poblacion-de-sonora-y-sus-municipios",
            "cuerpo: base de datos CONAPO 1990-2040; cabecera 11 Julio 2024",
        ),
        (
            ev_archivos[2],
            "https://datos.sonora.gob.mx/dataset/Proyecciones%20de%20poblaci%C3%B3n%20-%20Grupos%20quinquenales%20de%20edad",
            "Descripcion; Recursos; Informacion adicional (Fuentes extras)",
        ),
        (
            ev_archivos[3],
            "https://datos.sonora.gob.mx/dataset/Proyecciones%20de%20poblaci%C3%B3n%20-%20Grandes%20grupos%20de%20edad/resource/d7c4b8b2-568f-4349-a1ed-23fa93189e83",
            "tabla Metadatos (05-09-2024); enlace de descarga",
        ),
        (
            ev_archivos[4],
            "local: data/territorio/fuentes/de5c06c7-03d7-4ed4-a9fc-ec7d10b024f0.xlsx",
            "hojas Catalogo_Estado/Catalogo_Municipios; cabeceras; conteos 33/2476",
        ),
    ]
]

entrega = {
    "tarea": "vigencias-coespo",
    "tipo": "vigencias",
    "decisiones": decisiones,
    "fuentes": fuentes,
    "novedades_frente_a_investigacion_previa": (
        "NUEVO 2026-10-24 (no estaba en W01-W09 ni R6-C1/C2): pagina COESPO "
        "Proyecciones de Poblacion (lista descargas CONAPO-ProyeccionesMunicipales1990-2040.xlsx, "
        "diccionario 2023, series 2015-2030/2010-2030) y publicacion COESPO 11-07-2024 "
        "(herramienta con base CONAPO 1990-2040). Ambas dan contexto F3 parcial de la "
        "FUENTE DE DATOS, pero NINGUNA declara edicion/version/fecha del catalogo.xlsx "
        "ni lo vincula con periodos: resultado negativo para el documento exacto, no "
        "reversion de pendientes. RE-VERIFICADO sin novedad: dataset CKAN (W05), "
        "metadatos de recurso (fechas operativas 05-09-2024, excluidas por criterio), "
        "interior xlsx (F3 negativo). La igualdad del conteo 2475 con CONAPO se registra "
        "como prueba de procedencia, no de vigencia. Ningun dato conocido se presenta "
        "como nuevo."
    ),
    "busquedas_limitadas": [
        "web nativa 2026-10-24: COESPO proyecciones/catalogo/version; CONAPO metodologia 2024; portal datos.sonora proyecciones COESPO (3 consultas, via herramienta web nativa).",
        "NO se manejo el navegador Obscura compartido desde este agente (reservado al agente web-obscura); peticiones dejadas en peticiones-web.json; carpeta web-obscura inexistente al momento de entregar (sin resultados que leer).",
        "No se descargo el xlsx CONAPO-ProyeccionesMunicipales1990-2040.xlsx de COESPO: archivo de DATOS nacional, no declara edicion del catalogo local; descarga innecesaria.",
        "No se repitio la linea agotada R6-C1/R6-C2 (API package_show, core-properties) ni W06 (documento CONAPO 09-05-2024): se citan como contraste, no como evidencia nueva.",
        "Sin contacto con publicadores ni mensajes externos; sin puentes/CLI; sin tests (prohibido por instruccion).",
    ],
}

texto = json.dumps(entrega, ensure_ascii=False, indent=1, sort_keys=True)
assert json.loads(texto)["decisiones"][0]["id"] == "V09"
ids = [d["id"] for d in entrega["decisiones"]]
assert sorted(ids) == ["V09", "V10", "V11", "V12", "V15", "V16"] and len(set(ids)) == 6
(BASE / "entrega.json").write_text(texto, encoding="utf-8")
print("entrega.json OK", len(texto), "ids:", ",".join(ids))
