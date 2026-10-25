"""A2 Registro civil (Matrimonios/Nacimientos): analisis separado reproducible.

Lee SOLO documentos/datos locales existentes. No red, no grafo, no Studio.
Verifica los 8 ejes del plan y emite veredicto COMPARABLE o BLOQUEADO.
Uso: uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A2-registro-civil/v001/scripts/analizar.py
"""
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parents[1]
PAR_ID = "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5"
MAT = "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98"
NAC = "df2d60f5-2243-4bb0-885a-941aa8a657f5"
DIC_MAT = "364ffa5c-e1c2-4185-a22f-80bede6735d0"
DIC_NAC = "6bcf5b63-0855-4f3b-81a0-4bca82e97272"


def load(rel):
    with open(REPO / rel, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def main():
    perfil = load("reports/catalogo-perfil.json")
    inspeccion = load("data/portal/contenido-inspeccion.json")
    oport = load("data/portal/oportunidades-cruce.json")
    lote = load("data/portal/lote-cruces/validacion-lote.json")

    inv = {c["id"]: c for c in perfil["inventario"]}
    mat, nac = inv[MAT], inv[NAC]
    recs = {r["id"]: r for r in inspeccion["recursos"]}
    dic_mat = next(d for d in recs[DIC_MAT]["definiciones"])
    dic_nac = next(d for d in recs[DIC_NAC]["definiciones"])
    defs_mat = {d["Nombre variable"]: d for d in recs[DIC_MAT]["definiciones"]}
    defs_nac = {d["Nombre variable"]: d for d in recs[DIC_NAC]["definiciones"]}
    par_op = next(p for p in oport["pares"] if p["id"] == PAR_ID)
    par_lote = next(p for p in lote["pares"] if p["id"] == PAR_ID)

    ejes = {}
    # 1 claves: coincidencia solo textual de "municipio"; sin catalogo de correspondencia
    ejes["claves"] = {
        "veredicto": "no_acreditada",
        "evidencia": "oportunidades: estado candidata_por_validar, familia municipio con "
        "pendientes verificar_catalogo_dominio_unicidad_y_contexto_de_clave y "
        "municipio_puede_requerir_entidad_como_clave_compuesta; "
        "nombres_campos_coincidentes_sin_garantia_semantica=[municipio]",
    }
    # 2 grano: matrimonios fila=evento (dia/edades/sexos), nacimientos fila=agregado (hombres/mujeres/total)
    ejes["grano"] = {
        "veredicto": "distinto_bloquea_join",
        "evidencia": f"diccionario Matrimonios vars={sorted(defs_mat)} (evento con dia_matrimonio, "
        f"edad/sexo contrayentes); diccionario Nacimientos vars={sorted(defs_nac)} "
        "(conteo agregado hombres/mujeres/total por municipio-anio-mes)",
    }
    # 3 unicidad: muestras n=100 declaran no demostrar unicidad
    ejes["unicidad"] = {
        "veredicto": "no_acreditada",
        "evidencia": "validacion-lote diagnostico_muestras alcance en a y b: "
        "'Diagnostico de muestra; no demuestra unicidad ni cobertura integral'",
    }
    # 4 cardinalidad: total!=hombres+mujeres y meses faltantes en nacimientos
    errores_b = [t["error_b"] for t in par_lote["pruebas_recursos"]]
    ejes["cardinalidad"] = {
        "veredicto": "no_acreditada",
        "evidencia": f"decision={par_lote['decision']}; errores_b={errores_b}",
    }
    # 5 poblacion: eventos distintos, sin vinculo persona
    ejes["poblacion"] = {
        "veredicto": "distinta",
        "evidencia": "matrimonios=actos (2 contrayentes por fila, sin id persona); "
        "nacimientos=conteos agregados por sexo; poblaciones distintas explicitas, sin join de personas",
    }
    # 6 periodo: anios coincidentes solo en nombres de recurso 2015-2024; ambito registro
    ejes["periodo_ambito"] = {
        "veredicto": "comparable_solo_en_registro_no_acreditado_para_join",
        "evidencia": "anios_coincidentes_solo_en_nombres 2015-2024; ambos diccionarios: "
        "'Municipio de registro'/'Anio-Mes de registro'; ningun campo de residencia "
        "en definiciones locales; municipio sin catalogo de correspondencia",
    }
    # 7 unidades: conteo de filas/eventos vs conteos agregados; no personas, no tasas
    ejes["unidades"] = {
        "veredicto": "no_homologables_sin_regla",
        "evidencia": "matrimonios: fila=1 evento; nacimientos: fila=agregado con total; "
        "pendiente validar_unidades_de_medidas_seleccionadas; sin tasas poblacionales",
    }
    # 8 cobertura: meses faltantes <> cero; muestras no universo
    ejes["cobertura"] = {
        "veredicto": "no_acreditada",
        "evidencia": "prueba 2016: 'Faltan meses por municipio; ausencia no equivale a cero'; "
        "muestras n=100 con total_declarado (Mat2023=14685, Nac2024=627) de recursos/anios distintos",
    }

    causas = [
        "grano distinto (evento vs agregado) impide join fila a fila",
        "unicidad/cardinalidad no acreditadas: muestras n=100 declaran no demostrar unicidad ni cobertura",
        "inconsistencia interna en Nacimientos: total != hombres+mujeres en 5/6 pruebas; meses faltantes",
        "municipio/periodo solo de registro, sin residencia y sin catalogo de correspondencia de codigos",
        "poblaciones distintas (actos vs conteos de nacidos); prohibidas causalidad y tasas poblacionales",
    ]
    veredicto = "BLOQUEADO"
    resultado = {
        "par": PAR_ID,
        "pregunta": "Que volumenes de matrimonios y nacimientos se registran en un periodo "
        "y ambito territorial documentalmente comparables?",
        "veredicto": veredicto,
        "comparacion_volumenes": None,
        "join_grafo": None,
        "causas_bloqueo": causas,
        "ejes": ejes,
        "fuentes_locales": {
            "reports/catalogo-perfil.json": {
                "mat_recursos": len(mat["recursos"]),
                "nac_recursos": len(nac["recursos"]),
            },
            "data/portal/contenido-inspeccion.json": {
                "diccionario_matrimonios_sha256": recs[DIC_MAT]["sha256_fragmento_o_archivo"],
                "diccionario_nacimientos_sha256": recs[DIC_NAC]["sha256_fragmento_o_archivo"],
            },
            "data/portal/oportunidades-cruce.json": {"estado_par": par_op["estado"]},
            "data/portal/lote-cruces/validacion-lote.json": {"decision_par": par_lote["decision"]},
        },
        "metodo": "solo_datos_documentos_locales; sin_red; sin_grafo; sin_studio",
    }
    with open(OUT / "resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)

    entregables = ["A2-pregunta-ficha.md", "resultados.md", "resultados.json",
                   "scripts/analizar.py", "tests/test_bloqueo.py"]
    congelada = {"par": PAR_ID, "veredicto": veredicto, "archivos": {}}
    for rel in entregables:
        congelada["archivos"][rel] = sha256_file(OUT / rel)
    with open(OUT / "congelada.json", "w", encoding="utf-8") as f:
        json.dump(congelada, f, ensure_ascii=False, indent=1)
    # ponytail: hash propio fuera del json para no autorreferenciarse
    with open(OUT / "congelada.sha256", "w", encoding="utf-8") as f:
        f.write(sha256_file(OUT / "congelada.json") + "  congelada.json\n")
    print(veredicto + ": " + "; ".join(causas))


if __name__ == "__main__":
    main()
