"""A3 ITAMA v002 — verifica premisas, registra busqueda y extrae nucleo ITAMA.

Que hace:
  1. Ejecuta registrar_busqueda_itama.escribir(): barrido acotado a ITAMA con
     patron/rutas/resultado en evidencia-busqueda.json.
  2. Re-deriva la ficha de 8 ejes desde archivos locales y falla si una premisa
     del bloqueo deja de cumplirse (entonces toca v003).
  3. Escribe nucleo.ttl: extracto verbatim de los 6 conceptos con IRI -itama,
     conservando la distincion sexo (2 IRIs + 2 diccionarios) vs escolaridad
     (0 conceptos ITAMA).

No afirma que el repo carezca de XLSX: solo que no hay copias ITAMA.
Sin red, sin grafo, sin escritura fuera de A3-itama/v002. Solo stdlib.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registrar_busqueda_itama as busqueda  # noqa: E402

ROOT = Path(__file__).resolve().parents[6]
V002 = Path(__file__).resolve().parents[1]
V001 = V002.parent / "v001"

A = "27a5c80c-514a-4170-a2e5-7ef40d818641"
B = "4d27a1c4-381d-4ce0-a663-0d3e23a93848"
PAR = f"{A}--{B}"

CONCEPTOS_ITAMA = (
    "delito-persona-externada-itama",
    "delito-persona-internada-itama",
    "edad-persona-externada-itama",
    "edad-persona-internada-itama",
    "sexo-persona-externada-itama",
    "sexo-persona-internada-itama",
)
SEXO_ITAMA = (
    "sexo-persona-externada-itama",
    "sexo-persona-internada-itama",
)
ESCOLARIDAD_OTROS_UNIVERSOS = (
    "escolaridad-beneficiado-mano",
    "escolaridad-difunto",
    "escolaridad-madre",
)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def buscar_id(objeto, identificador):
    if isinstance(objeto, dict):
        if objeto.get("id") == identificador:
            return objeto
        for valor in objeto.values():
            hallado = buscar_id(valor, identificador)
            if hallado is not None:
                return hallado
    elif isinstance(objeto, list):
        for valor in objeto:
            hallado = buscar_id(valor, identificador)
            if hallado is not None:
                return hallado
    return None


def iries_concepto(texto: str) -> set[str]:
    """Solo sujetos de concepto: evita capturar objetos como skos:broader."""
    return set(
        re.findall(
            r"(?m)^<https://example\.org/mex-ontologi/concept/([^>]+)> a skos:Concept",
            texto,
        )
    )


def bloque_concepto(texto: str, nombre: str) -> str:
    aguja = f"<https://example.org/mex-ontologi/concept/{nombre}> a skos:Concept"
    bloques = [b for b in texto.split("\n\n") if b.strip()]
    hallados = [b for b in bloques if b.lstrip().startswith(aguja)]
    assert len(hallados) == 1, f"bloque unico esperado para {nombre}"
    return hallados[0].strip()


def verificar_premisas(evidencia_busqueda: dict) -> dict:
    metadatos = load("data/catalogo/metadatos.json")
    cruce = load("data/portal/oportunidades-cruce.json")
    lote = load("data/portal/lote-cruces/validacion-lote.json")
    cobertura = load("data/semantica/cobertura.json")
    nucleo = (ROOT / "data/semantica/nucleo.ttl").read_text(encoding="utf-8")

    conjuntos = {c["id"]: c for c in metadatos}
    assert A in conjuntos and B in conjuntos, "conjuntos ITAMA ausentes"

    def xlsx(conjunto):
        return sorted(
            (r["id"], r["start_date"], r["end_date"])
            for r in conjuntos[conjunto]["resources"]
            if r["format"] == "XLSX"
        )

    ra, rb = xlsx(A), xlsx(B)
    assert len(ra) == 3 and len(rb) == 3, "se esperaban 3+3 recursos XLSX"
    assert {i for i, _, _ in ra + rb} == set(busqueda.IDS_XLSX), "IDs XLSX"
    periodo_comun = (min(s for _, s, _ in ra + rb), max(e for _, _, e in ra + rb))
    assert periodo_comun == ("2026-01-01", "2026-09-30"), periodo_comun

    csv = {
        r["id"]
        for c in (A, B)
        for r in conjuntos[c]["resources"]
        if r["format"] == "CSV"
    }
    assert csv == set(busqueda.IDS_DICCIONARIOS), "IDs de diccionarios"

    pares = [p for p in cruce["pares"] if p["id"] == PAR]
    assert len(pares) == 1, "par unico en cruce"
    familias = {e["familia"] for e in pares[0]["evaluacion_claves"]}
    assert {"estrato_escolaridad", "estrato_sexo", "periodo"} <= familias

    diag = buscar_id(lote, PAR)["diagnostico_muestras"]
    assert diag["a"]["filas_muestra"] == 29 and diag["b"]["filas_muestra"] == 16
    assert diag["a"]["campos"]["ESCOLARIDAD"]["nulos"] == 29
    assert diag["a"]["campos"]["SEXO"]["distintos_muestra"] == 1
    assert diag["b"]["campos"]["SEXO"]["distintos_muestra"] == 2
    assert "ESCOLARIDAD" not in diag["b"]["campos"]

    variables = [
        v for v in cobertura["variables"] if v["conjunto"] in (A, B)
    ]
    assert len(variables) == 11, len(variables)
    assert "escolaridad" not in {v["variable"] for v in variables}

    # Sexo ITAMA: IDs respaldados por diccionario local inspeccionado.
    for identificador in busqueda.IDS_DICCIONARIOS:
        inspeccion = load(
            f"data/portal/inspecciones/{identificador}.json"
        )
        assert inspeccion["ok"] and inspeccion["completo"]
        definidas = {
            d["Nombre variable"].strip().lower()
            for d in inspeccion["definiciones"]
        }
        assert "sexo" in definidas, (identificador, definidas)
        assert not any("escolaridad" in d for d in definidas), definidas

    iries = iries_concepto(nucleo)
    assert set(CONCEPTOS_ITAMA) <= iries, "faltan conceptos ITAMA"
    assert set(SEXO_ITAMA) <= iries, "faltan conceptos de sexo ITAMA"
    assert not any(
        "escolaridad" in iri and "itama" in iri for iri in iries
    ), "aparecio escolaridad ITAMA sin respaldo"
    assert set(ESCOLARIDAD_OTROS_UNIVERSOS) <= iries, "escolaridad de otros"

    # La busqueda debe ser ITAMA-acotada y no negar los XLSX del repo.
    resumen = evidencia_busqueda["resumen"]
    assert resumen["xlsx_repo_total"] > 0, "el repo tiene XLSX de otros conjuntos"
    assert resumen["xlsx_itama"] == 0, "aparecieron copias ITAMA"
    assert resumen["xlsx_repo_total"] == len(evidencia_busqueda["rutas_xlsx"])

    return {
        "recursos_xlsx": {"internamiento": len(ra), "externamiento": len(rb)},
        "periodo_comun_metadatos": {
            "inicio": periodo_comun[0],
            "fin": periodo_comun[1],
        },
        "muestras": {
            "a_filas": 29,
            "b_filas": 16,
            "a_sexo_distintos": 1,
            "b_sexo_distintos": 2,
            "a_escolaridad_nulos": 29,
            "b_escolaridad_medida": False,
        },
        "nucleo": {
            "conceptos_itama": len(CONCEPTOS_ITAMA),
            "sexo_con_iri": len(SEXO_ITAMA),
            "escolaridad_itama": 0,
        },
        "diccionarios": {
            "sexo_definido_en": len(busqueda.IDS_DICCIONARIOS),
            "escolaridad_definida_en": 0,
        },
        "busqueda": resumen,
        "decision": "BLOQUEADO",
    }


def verificar_resultados(evidencia: dict) -> dict:
    """Contrasta el analisis/inventario consolidados con un barrido fresco."""
    resultados = json.loads(
        (V002 / "resultados/analisis-a3-itama-v002.json").read_text(
            encoding="utf-8"
        )
    )
    inventario = json.loads(
        (V002 / "resultados/inventario-archivos-repo.json").read_text(
            encoding="utf-8"
        )
    )
    resumen = evidencia["resumen"]

    assert resultados["decision"] == "BLOQUEADO"
    assert resultados["analisis_agregado"]["calculado"] is False
    assert (
        resultados["inventario_copias"]["xlsx_total"]
        == resumen["xlsx_repo_total"]
        == inventario["xlsx_total"]
    )
    assert (
        resultados["inventario_copias"]["csv_total"]
        == resumen["csv_repo_total"]
        == inventario["csv_total"]
    )
    assert resultados["inventario_copias"]["coincidencias_exactas_itama"] == []
    assert inventario["coincidencias_exactas_itama"] == []
    assert resumen["copias_exactas_itama"] == 0
    assert resultados["escolaridad"]["publicada_en_hoja_de_poblacion"] is False
    assert resultados["escolaridad"]["en_diccionarios"] == {A: False, B: False}

    recursos = (
        resultados["universo_documental"]["recursos"]["internamiento"]
        + resultados["universo_documental"]["recursos"]["externamiento"]
    )
    for recurso in recursos:
        inspeccion = load(
            f"data/portal/inspecciones/{recurso['id']}.json"
        )
        assert (
            inspeccion["sha256_fragmento_o_archivo"] == recurso["sha256"]
        ), recurso["id"]
        assert inspeccion.get("completo") is True, recurso["id"]

    entrega = json.loads(
        (V002 / "entrega.json").read_text(encoding="utf-8")
    )
    cifras = entrega["cifras_verificadas"]
    assert entrega["decision"] == resultados["decision"]
    assert cifras["xlsx_en_repo"] == resumen["xlsx_repo_total"]
    assert cifras["csv_en_repo"] == resumen["csv_repo_total"]
    assert cifras["copias_exactas_itama"] == 0
    assert cifras["recursos_xlsx"] == len(busqueda.IDS_XLSX)
    assert cifras["periodo_metadatos"] == resultados["universo_documental"][
        "periodo_metadatos"
    ]
    assert cifras["muestras"] == {"a": 29, "b": 16}

    for rel, esperado in entrega["v001_intacta"].items():
        if rel != "nota":
            assert busqueda.sha256(V001 / rel) == esperado, rel

    return {
        "analisis": "resultados/analisis-a3-itama-v002.json",
        "inventario": "resultados/inventario-archivos-repo.json",
        "xlsx_en_repo": resumen["xlsx_repo_total"],
        "csv_en_repo": resumen["csv_repo_total"],
        "copias_exactas_itama": resumen["copias_exactas_itama"],
        "escolaridad_publicada_en_hoja_de_poblacion": False,
    }


def escribir_nucleo() -> Path:
    fuente = ROOT / "data/semantica/nucleo.ttl"
    texto = fuente.read_text(encoding="utf-8")
    encabezado = f"""# A3-ITAMA v002 — extracto de evidencia; NO sustituye al nucleo.
# Fuente: data/semantica/nucleo.ttl
# SHA256 fuente: {busqueda.sha256(fuente)}
# Extraido por: scripts/analisis_a3_itama_v002.py
#
# Distincion conservada:
#   - Sexo ITAMA: 2 conceptos con IRI propio ({SEXO_ITAMA[0]},
#     {SEXO_ITAMA[1]}), respaldados por los diccionarios
#     07781b38-8a53-42eb-b3b7-3c1ebc6a4415 y
#     a7ee5717-b14d-439b-9508-bada58d0d185, que definen "sexo".
#   - Escolaridad ITAMA: 0 conceptos. Los 3 conceptos de escolaridad del
#     nucleo (escolaridad-beneficiado-mano, escolaridad-difunto,
#     escolaridad-madre) pertenecen a otros universos y no definen la
#     columna ESCOLARIDAD de ITAMA.
#   - tiempo-sentencia-persona-externada se define en ITAMA pero su IRI no
#     lleva sufijo -itama; queda fuera de este extracto.

"""
    prefijos = "\n".join(
        linea for linea in texto.splitlines() if linea.startswith("@prefix")
    )
    orden = SEXO_ITAMA + tuple(
        nombre for nombre in CONCEPTOS_ITAMA if nombre not in SEXO_ITAMA
    )
    bloques = [bloque_concepto(texto, nombre) for nombre in orden]
    assert len(set(bloques)) == 6, len(set(bloques))

    destino = V002 / "nucleo.ttl"
    destino.write_text(
        encabezado + prefijos + "\n\n" + "\n\n".join(bloques) + "\n",
        encoding="utf-8",
    )
    return destino


def main() -> dict:
    evidencia = busqueda.escribir()
    resumen = verificar_premisas(evidencia)
    resumen["resultados"] = verificar_resultados(evidencia)
    destino = escribir_nucleo()
    resumen["nucleo"]["extracto"] = destino.relative_to(ROOT).as_posix()
    resumen["evidencia"] = busqueda.DESTINO.relative_to(ROOT).as_posix()
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return resumen


if __name__ == "__main__":
    main()
