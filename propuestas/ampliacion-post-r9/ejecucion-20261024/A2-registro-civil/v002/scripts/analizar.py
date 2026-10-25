"""A2 Registro civil (Matrimonios/Nacimientos): analisis separado reproducible (v002).

Lee SOLO documentos/datos locales existentes. No red, no grafo, no Studio.
Reproduce el analisis de v001 sin cambiar veredicto, cifras ni ejes.
Corrige del dictamen R-documental/v001:
  H-02: distingue recursos de datos de diccionario (10+1 y 15+1).
  H-04: anade SHA256 de archivo completo y bytes de las cuatro fuentes.
Uso: .venv/Scripts/python.exe propuestas/ampliacion-post-r9/ejecucion-20261024/A2-registro-civil/v002/scripts/analizar.py
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

PERFIL = "reports/catalogo-perfil.json"
INSPECCION = "data/portal/contenido-inspeccion.json"
OPORT = "data/portal/oportunidades-cruce.json"
LOTE = "data/portal/lote-cruces/validacion-lote.json"


def load(rel):
    with open(REPO / rel, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def huella(rel):
    p = REPO / rel
    return {"sha256": sha256_file(p), "bytes": p.stat().st_size}


def main():
    perfil = load(PERFIL)
    inspeccion = load(INSPECCION)
    oport = load(OPORT)
    lote = load(LOTE)

    inv = {c["id"]: c for c in perfil["inventario"]}
    mat, nac = inv[MAT], inv[NAC]
    recs = {r["id"]: r for r in inspeccion["recursos"]}
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
        "'Diagnóstico de muestra; no demuestra unicidad ni cobertura integral'",
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
        "'Municipio de registro', 'Año de registro' y 'Mes de registro' (Matrimonios "
        "incluye 'Dia de registro'); ningun campo de residencia en definiciones locales; "
        "municipio sin catalogo de correspondencia",
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
            PERFIL: {
                **huella(PERFIL),
                # H-02: total incluye 1 diccionario; los recursos de datos son el resto
                "mat_recursos": len(mat["recursos"]),
                "mat_recursos_datos": sum(1 for r in mat["recursos"] if r["id"] != DIC_MAT),
                "mat_diccionarios": sum(1 for r in mat["recursos"] if r["id"] == DIC_MAT),
                "nac_recursos": len(nac["recursos"]),
                "nac_recursos_datos": sum(1 for r in nac["recursos"] if r["id"] != DIC_NAC),
                "nac_diccionarios": sum(1 for r in nac["recursos"] if r["id"] == DIC_NAC),
            },
            INSPECCION: {
                **huella(INSPECCION),
                "diccionario_matrimonios_sha256": recs[DIC_MAT]["sha256_fragmento_o_archivo"],
                "diccionario_nacimientos_sha256": recs[DIC_NAC]["sha256_fragmento_o_archivo"],
            },
            OPORT: {**huella(OPORT), "estado_par": par_op["estado"]},
            LOTE: {**huella(LOTE), "decision_par": par_lote["decision"]},
        },
        "metodo": "solo_datos_documentos_locales; sin_red; sin_grafo; sin_studio",
        "modelo": "opencode/deepseek-v4.1-flash-free",
        "version": "v002",
    }
    with open(OUT / "resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
    print(veredicto + ": " + "; ".join(causas))


if __name__ == "__main__":
    main()
