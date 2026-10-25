#!/usr/bin/env python3
"""Genera capas-normativas.json, entrega.json/md y congelada.json de W-estandares v002.

No transcribe metadatos: los extrae de las capturas de evidencia y sella por SHA-256
calculado sobre los bytes reales de cada archivo. Si una captura no contiene el
sujeto http, la version 3.5.3, el simbolo o la etiqueta esperados, aborta sin sellar.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # .../W-estandares/v002
REPO = ROOT.parents[4]
EJECUCION = ROOT.parents[1]

PREDICADO = re.compile(r"^(?:qudt|rdfs|skos|rdf):[A-Za-z0-9_]+$")
ETIQUETA = re.compile(r"^[\u201c\"](.*)[\u201d\"]@([A-Za-z-]+)$")
ETIQUETA_SIN_IDIOMA = re.compile(r"^[\u201c\"](.*)[\u201d\"]$")
VERSION = re.compile(r"http://qudt\.org/(\d+\.\d+\.\d+)/vocab/unit")

CASOS = [
    {
        "id": "Q-W-01",
        "caso": "Q-U01",
        "literal": "Toneladas",
        "archivo": "unit-TON_Metric-evidencia.txt",
        "termino": "TON_Metric",
        "simbolo": "t",
        "etiqueta_es": None,
        "etiqueta_en": "Metric Ton",
    },
    {
        "id": "Q-W-02",
        "caso": "Q-U02",
        "literal": "Kilogramos",
        "archivo": "unit-KiloGM-evidencia.txt",
        "termino": "KiloGM",
        "simbolo": "kg",
        "etiqueta_es": "Kilogramo",
        "etiqueta_en": "Kilogram",
    },
    {
        "id": "Q-W-03",
        "caso": "Q-U03",
        "literal": "MW",
        "archivo": "unit-MegaW-evidencia.txt",
        "termino": "MegaW",
        "simbolo": "MW",
        "etiqueta_es": "Megavatio",
        "etiqueta_en": "Megawatt",
    },
    {
        "id": "Q-W-04",
        "caso": "Q-U04",
        "literal": "GWh",
        "archivo": "unit-GigaW-HR-evidencia.txt",
        "termino": "GigaW-HR",
        "simbolo": "GW\u00b7h",
        "etiqueta_es": None,
        "etiqueta_en": "Gigawatt Hour",
    },
    {
        "id": "Q-W-05",
        "caso": "Q-U05",
        "literal": "Porcentaje",
        "archivo": "unit-PERCENT-evidencia.txt",
        "termino": "PERCENT",
        "simbolo": "%",
        "etiqueta_es": None,
        "etiqueta_en": "Percent",
    },
    {
        "id": "Q-W-06",
        "caso": "Q-U06",
        "literal": "Grados celcius",
        "archivo": "unit-DEG_C-evidencia.txt",
        "termino": "DEG_C",
        "simbolo": "\u00b0C",
        "etiqueta_es": "Grado Celsius",
        "etiqueta_en": "Degree Celsius",
    },
]

NOTAS = {
    "Q-W-01": "Sujeto verificado. QUDT no publica etiqueta @es para este termino: solo @en. "
    "El literal local 'Toneladas' no elige variante por si mismo; la variante aplicable "
    "requiere evidencia local. Sin alias ni factores.",
    "Q-W-02": "Sujeto verificado con etiqueta @es y simbolo kg. Sin alias ni factores.",
    "Q-W-03": "Sujeto verificado con etiqueta @es y simbolo MW. Sin alias ni factores.",
    "Q-W-04": "Sujeto verificado. El simbolo QUDT es GW\u00b7h, no 'GWh'; ucumCode GW.h y "
    "uneceCommonCode GWH. No hay etiqueta @es. La diferencia se conserva y no se declara alias.",
    "Q-W-05": "Sujeto verificado. QUDT no publica etiqueta @es (solo @en). conversionMultiplier "
    "0.01 pertenece al termino normativo; no se aplica a datos locales.",
    "Q-W-06": "Sujeto verificado con etiqueta @es 'Grado Celsius' y simbolo \u00b0C. El literal "
    "local con error ortografico no se normaliza en W; la asignacion queda para Q.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def captura(texto: str) -> str:
    inicio = "COPIA TEXTUAL (document.body.innerText):\n---\n"
    fin = "\n---\nLOCALIZADORES:"
    i = texto.index(inicio) + len(inicio)
    j = texto.index(fin, i)
    return texto[i:j]


def siguiente_no_vacio(lineas: list[str], i: int) -> str:
    for linea in lineas[i + 1 :]:
        if linea.strip():
            return linea.strip()
    raise AssertionError("predicado sin valor")


def despojar_comillas(valor: str) -> str:
    return valor.strip().strip("\u201c\u201d\"")


def leer_caso(caso: dict) -> dict:
    ruta = ROOT / "normativa" / caso["archivo"]
    texto = ruta.read_text(encoding="utf-8")
    cuerpo = captura(texto)
    lineas = cuerpo.splitlines()

    iri = f"http://qudt.org/vocab/unit/{caso['termino']}"
    assert lineas[0].strip() == f"unit:{caso['termino']}", ruta
    assert lineas[1].strip() == iri, ruta
    assert f'URL navegable (verificada por Obscura): https://qudt.org/vocab/unit/{caso["termino"]}' in texto
    assert f"IRI canonica del sujeto RDF: {iri}" in texto

    versiones = VERSION.findall(cuerpo)
    assert versiones, f"sin isDefinedBy en {ruta}"
    assert set(versiones) == {"3.5.3"}, f"version distinta de 3.5.3 en {ruta}: {versiones}"

    generado = re.search(r"Generated (\S+)", cuerpo)
    assert generado, ruta
    assert generado.group(1) == "2026-10-20T17:45:20.378+00:00", ruta

    simbolo = despojar_comillas(siguiente_no_vacio(lineas, lineas.index("qudt:symbol")))
    assert simbolo == caso["simbolo"], f"simbolo {simbolo!r} != {caso['simbolo']!r} en {ruta}"

    i = lineas.index("dcterms:description")
    definicion: list[str] = []
    for linea in lineas[i + 1 :]:
        limpia = linea.strip()
        if not limpia:
            continue
        if limpia.startswith("Generated ") or PREDICADO.match(limpia):
            break
        definicion.append(limpia)
    assert definicion, ruta

    i = lineas.index("rdfs:label")
    etiquetas: dict[str, list[str]] = {}
    for linea in lineas[i + 1 :]:
        limpia = linea.strip()
        if limpia.startswith("Generated ") or PREDICADO.match(limpia):
            break
        con_idioma = ETIQUETA.match(limpia)
        if con_idioma:
            etiquetas.setdefault(con_idioma.group(2), []).append(con_idioma.group(1))
            continue
        sin_idioma = ETIQUETA_SIN_IDIOMA.match(limpia)
        if sin_idioma and not limpia.startswith("Show "):
            etiquetas.setdefault("sin-idioma", []).append(sin_idioma.group(1))

    if caso["etiqueta_es"] is None:
        assert "es" not in etiquetas, f"aparecio etiqueta @es no esperada en {ruta}"
    else:
        assert caso["etiqueta_es"] in etiquetas.get("es", []), ruta
    assert caso["etiqueta_en"] in etiquetas.get("en", []), ruta

    return {
        "id": caso["id"],
        "caso": caso["caso"],
        "literal_local": caso["literal"],
        "sujeto_rdf": iri,
        "url_navegable": f"https://qudt.org/vocab/unit/{caso['termino']}",
        "version": {
            "qudt": versiones[0],
            "isDefinedBy": f"http://qudt.org/{versiones[0]}/vocab/unit",
            "vocabulario_generado": generado.group(1),
        },
        "simbolo": simbolo,
        "etiquetas": {
            "es": etiquetas.get("es", []),
            "en": etiquetas.get("en", []),
            "sin_idioma": etiquetas.get("sin-idioma", []),
        },
        "definicion": {
            "predicado": "dcterms:description",
            "texto": " ".join(definicion),
        },
        "evidencia": {
            "ruta": rel(ruta),
            "sha256": sha256(ruta),
            "bytes": ruta.stat().st_size,
        },
        "nota": NOTAS[caso["id"]],
    }


def escribir_json(ruta: Path, datos: dict) -> None:
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ahora = dt.datetime.now(dt.timezone.utc).isoformat()
    (ROOT / "peticiones").mkdir(exist_ok=True)
    registros = [leer_caso(caso) for caso in CASOS]
    assert len({r["sujeto_rdf"] for r in registros}) == 6

    solicitud = EJECUCION / "Q-unidades" / "peticiones-web.json"
    base = EJECUCION / "base.json"
    trazas = ROOT / "normativa" / "trazas-consulta-v002.md"

    capas = {
        "rol": "W-estandares",
        "version": "v002",
        "fecha_utc": ahora,
        "capa_normativa_version": {
            "estandar": "QUDT",
            "version": "3.5.3",
            "namespace_unidades": "http://qudt.org/3.5.3/vocab/unit",
            "vocabulario_generado": "2026-10-20T17:45:20.378+00:00",
            "regla_sujeto": "sujeto RDF en http://qudt.org/vocab/unit/<TERMINO>; la URL https navegable no sustituye la IRI",
        },
        "capas_por_termino": registros,
    }
    escribir_json(ROOT / "normativa" / "capas-normativas.json", capas)

    fuentes = [
        {
            "localizador": f"{r['id']} sujeto {r['sujeto_rdf']}; QUDT {r['version']['qudt']}; symbol {r['simbolo']}",
            "ruta": r["evidencia"]["ruta"],
            "sha256": r["evidencia"]["sha256"],
            "url": r["url_navegable"],
        }
        for r in registros
    ]
    fuentes.extend(
        [
            {
                "localizador": "Capas normativas por termino extraidas de las capturas",
                "ruta": rel(ROOT / "normativa" / "capas-normativas.json"),
                "sha256": sha256(ROOT / "normativa" / "capas-normativas.json"),
            },
            {
                "localizador": "Trazas de navegacion Obscura y diferencias literal/termino",
                "ruta": rel(trazas),
                "sha256": sha256(trazas),
            },
            {
                "localizador": "Peticiones Q-W-01..06 origen",
                "ruta": rel(solicitud),
                "sha256": sha256(solicitud),
            },
            {
                "localizador": "Base congelada R9 de la ejecucion",
                "ruta": rel(base),
                "sha256": sha256(base),
            },
        ]
    )

    entrega = {
        "rol": "W-estandares",
        "version": "v002",
        "fecha_utc": ahora,
        "estado": "propuesta_para_auditar",
        "modelo": "opencode/deepseek-v4.1-flash-free",
        "mcp": "nativo OpenCode tools.obscura.*, sin puentes CLI",
        "navegador": "Obscura exclusivo para W",
        "base": {
            "release": "R9",
            "congelada": rel(base),
            "sha256": sha256(base),
        },
        "solicitud": {
            "ruta": rel(solicitud),
            "sha256": sha256(solicitud),
            "peticiones": len(CASOS),
        },
        "norma": capas["capa_normativa_version"],
        "resultados": [
            {
                "id": r["id"],
                "caso": r["caso"],
                "estado": "verificado",
                "sujeto_rdf": r["sujeto_rdf"],
                "url": r["url_navegable"],
                "version": r["version"]["qudt"],
                "simbolo": r["simbolo"],
                "etiqueta_es": r["etiquetas"]["es"][0] if r["etiquetas"]["es"] else None,
                "etiqueta_en": r["etiquetas"]["en"][0] if r["etiquetas"]["en"] else None,
                "definicion_predicado": r["definicion"]["predicado"],
                "evidencia": r["evidencia"],
                "conclusion": f"IRI exacta {r['sujeto_rdf']} en QUDT {r['version']['qudt']}.",
                "nota": r["nota"],
            }
            for r in registros
        ],
        "resumen": {
            "peticiones_recibidas": len(CASOS),
            "peticiones_atendidas": len(CASOS),
            "unidades_verificadas": len(registros),
            "negativos_normativos": 0,
            "alias_inventados": 0,
            "casos_locales_promovidos": 0,
            "evidencias_nuevas_para_integrar": 0,
        },
        "fuentes": fuentes,
        "condiciones_de_aceptacion": [
            "Solo se aceptan como normativos los sujetos http://qudt.org/vocab/unit/... capturados y sellados aqui.",
            "La verificacion acredita existencia, version, simbolo, etiqueta y definicion del termino; no acredita que el literal local use ese termino.",
            "Las diferencias de simbolo (GW\u00b7h vs GWh) y la ausencia de etiqueta @es se conservan; no se declaran alias.",
            "Ningun factor de conversion se aplica ni se propone en esta entrega.",
            "Sin evidencia local adicional, cada asignacion literal->termino sigue pendiente en Q.",
        ],
        "limites": [
            "Escritura exclusiva en propuestas/ampliacion-post-r9/ejecucion-20261024/W-estandares/v002/.",
            "config.toml, IRI base example.org, manifiestos R1-R9, ontologia, shapes, datos, grafo y Studio intactos.",
            "Gemma excluido; sin contactos a publicadores; sin busquedas agotadas repetidas (hm3/HectoM3 no se sondeo).",
            "Fuente normativa != evidencia local; no se promueve ningun caso local.",
        ],
        "entregables": [
            "v002/entrega.json",
            "v002/entrega.md",
            "v002/normativa/capas-normativas.json",
            "v002/normativa/trazas-consulta-v002.md",
            "v002/normativa/unit-TON_Metric-evidencia.txt",
            "v002/normativa/unit-KiloGM-evidencia.txt",
            "v002/normativa/unit-MegaW-evidencia.txt",
            "v002/normativa/unit-GigaW-HR-evidencia.txt",
            "v002/normativa/unit-PERCENT-evidencia.txt",
            "v002/normativa/unit-DEG_C-evidencia.txt",
            "v002/peticiones/atencion-peticiones-v002.json",
            "v002/scripts/generar_y_sellar.py",
            "v002/congelada.json",
        ],
    }
    escribir_json(ROOT / "entrega.json", entrega)

    filas = [
        "| id | caso | literal local | sujeto RDF (http) | version | simbolo | etiqueta |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in registros:
        etiqueta = r["etiquetas"]["es"][0] if r["etiquetas"]["es"] else f"{r['etiquetas']['en'][0]} (sin @es)"
        filas.append(
            f"| {r['id']} | {r['caso']} | {r['literal_local']} | {r['sujeto_rdf']} | "
            f"{r['version']['qudt']} | {r['simbolo']} | {etiqueta} |"
        )

    md = [
        "# W-estandares v002 - respuestas QUDT 3.5.3",
        "",
        f"Fecha UTC: {ahora}. Estado: propuesta para auditar.",
        "Obscura via MCP nativo OpenCode; sin puentes CLI. Seis peticiones Q atendidas.",
        "",
        "## Respuestas",
        "",
        *filas,
        "",
        "Cada sujeto se capturo en su pagina oficial, con `rdfs:isDefinedBy`",
        "`http://qudt.org/3.5.3/vocab/unit` y `Generated 2026-10-20T17:45:20.378+00:00`.",
        "",
        "## Limites que no se normalizan",
        "",
        "- TON_Metric, GigaW-HR y PERCENT no tienen etiqueta `@es` en QUDT; se conserva la etiqueta `@en`.",
        "- GigaW-HR declara simbolo `GW\u00b7h`, no `GWh`; `ucumCode` es `GW.h` y `uneceCommonCode` `GWH`.",
        "- El literal local `Grados celcius` (sic) no se corrige en esta capa.",
        "- `Toneladas` no elige por si mismo entre variantes; la decision requiere evidencia local de Q.",
        "",
        "Ningun alias, factor de conversion ni caso local se promueve desde estas fuentes.",
        "Sellos SHA-256 en `congelada.json`, calculados por `scripts/generar_y_sellar.py`.",
    ]
    (ROOT / "entrega.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # atencion-peticiones: respuesta por id, con hash de la evidencia correspondiente
    atencion = {
        "rol": "W-estandares",
        "version": "v002",
        "fecha_utc": ahora,
        "solicitud_origen": rel(solicitud),
        "solicitud_sha256": sha256(solicitud),
        "respuestas": [
            {
                "id": r["id"],
                "caso": r["caso"],
                "atendida": True,
                "sujeto_rdf": r["sujeto_rdf"],
                "url": r["url_navegable"],
                "version": r["version"]["qudt"],
                "simbolo": r["simbolo"],
                "etiquetas": r["etiquetas"],
                "definicion": r["definicion"],
                "evidencia": r["evidencia"],
                "nota": r["nota"],
            }
            for r in registros
        ],
        "pendientes": [],
    }
    escribir_json(ROOT / "peticiones" / "atencion-peticiones-v002.json", atencion)

    # sello: todos los archivos de la version menos el propio sello
    sello = {
        "rol": "W-estandares",
        "version": "v002",
        "fecha_utc": ahora,
        "nota": "SHA-256 calculado por scripts/generar_y_sellar.py sobre los bytes en disco; "
        "no se incluye a si mismo; no editar v002 tras congelar, corregir en v003.",
        "archivos": [],
    }
    for ruta in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        if ruta.name == "congelada.json":
            continue
        sello["archivos"].append(
            {"ruta": rel(ruta), "sha256": sha256(ruta), "bytes": ruta.stat().st_size}
        )
    escribir_json(ROOT / "congelada.json", sello)

    # verificacion final contra disco
    for entrada in sello["archivos"]:
        ruta = REPO / entrada["ruta"]
        assert sha256(ruta) == entrada["sha256"], entrada["ruta"]
        assert ruta.stat().st_size == entrada["bytes"], entrada["ruta"]
    print(f"OK: {len(sello['archivos'])} archivos sellados y verificados; "
          f"{len(registros)} respuestas QUDT 3.5.3.")


if __name__ == "__main__":
    main()
