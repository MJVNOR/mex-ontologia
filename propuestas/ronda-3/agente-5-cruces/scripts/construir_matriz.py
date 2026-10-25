"""Matriz TRIAJE (no exhaustividad demostrada). Solo lectura.
Entradas: oportunidades-cruce.json (3916) + validacion-lote.json (98).
Decisiones por operacion, no prohibiciones universales:
 habilitable_con_condiciones: UES programa/sede, archivos completos; solo conteos.
 exploratorio_con_condiciones_pendientes: F1 agregados RC sin filas crudas/catalogo;
  F2 cruce nuevo 2020 sobre originales con vigencia/serie pendientes.
 no_comparable: SOLO no concatenar misma-familia anterior vs actual como misma serie.
 no_validado: fallo del lote por error/fuente faltante; no demuestra incompatibilidad.
 exploratorio: clave compartida sin estrategia validada. pendiente: resto.
"""
import json
from pathlib import Path
from collections import Counter

RAIZ = Path(__file__).resolve().parents[4]
BASE = RAIZ / "propuestas" / "ronda-3" / "agente-5-cruces"

# Pares misma-familia delictiva con metodologias distintas: la UNICA operacion
# excluida es concatenarlas como misma serie/medida (cambio metodologico en el
# titulo + lote: falta catalogo de correspondencia). Otras yuxtaposiciones por
# variables comparables no quedan evaluadas ni prohibidas.
NO_CONCATENAR_MISMA_SERIE = {
    "93ca5e1c-702e-4e62-bc61-638907be184a--e0a72310-dca9-4b3b-b9a5-2445e4fde598",  # Incidencia actual vs anterior
    "b82c4430-8e88-4d41-8c47-ec55c591e882--caf587a5-23ac-496b-85d4-6ceb1d615d78",  # Victimas anterior vs actual
}


def decidir(par, lote_por_id):
    pid = par["id"]
    rev = "--".join(pid.split("--")[::-1])
    lid = lote_por_id.get(pid) or lote_por_id.get(rev)
    # El fallo integral del lote (error/fuente faltante) NO demuestra
    # incompatibilidad: triaje no_validado, no prohibicion.
    if lid and lid.get("decision") == "fallo_validacion_integral":
        return "no_validado", ("lote: ninguna pareja de recursos supero comprobaciones; "
                               "error o fuente faltante no demuestra incompatibilidad")
    if pid in NO_CONCATENAR_MISMA_SERIE or rev in NO_CONCATENAR_MISMA_SERIE:
        return "no_comparable", ("no concatenar como misma serie/medida: metodologias anterior vs "
                                 "actual; otras yuxtaposiciones por variables comparables no evaluadas")
    if par["estado"] == "exploratorio_ejecutado":
        return "exploratorio_con_condiciones_pendientes", ("Registro Civil 2022: mismo sentido registro, "
            "mismo publicador; quedan bloqueos interpretativos y no hay lectura de filas crudas")
    if lid and lid.get("decision") == "ejecucion_parcial_exploratoria":
        return "habilitable_con_condiciones", "UES: mismo periodo y grano programa/sede; solo conteos"
    if par["id"] == "943d0723-afbb-470a-8fe8-d62e8671de84--960ef0a9-73ed-4191-ae0b-b868d7e48292":
        return "exploratorio_con_condiciones_pendientes", ("cruce nuevo 2020 sobre originales; "
            "vigencia de catalogo y serie completa pendientes")
    if par["estado"] == "candidata_por_validar" and lid and lid.get("decision") == "requiere_revision":
        return "exploratorio", "clave compartida con catalogo posible; falta estrategia de agregacion"
    if par["estado"] == "candidata_por_validar":
        return "pendiente", "candidata sin validacion de medidas/grano/periodo"
    return "pendiente", par["estado"]


def main():
    op = json.loads((RAIZ / "data/portal/oportunidades-cruce.json").read_text(encoding="utf-8"))
    lote = json.loads((RAIZ / "data/portal/lote-cruces/validacion-lote.json").read_text(encoding="utf-8"))
    lote_por_id = {}
    for p in lote["pares"]:
        lote_por_id[p["id"]] = p
        lote_por_id["--".join(p["id"].split("--")[::-1])] = p
    filas = []
    for par in op["pares"]:
        dec, motivo = decidir(par, lote_por_id)
        filas.append({"id": par["id"], "a": par["titulo_a"], "b": par["titulo_b"],
                      "familias": par["familias_compartidas"], "estado_origen": par["estado"],
                      "decision": dec, "motivo": motivo})
    grupos = Counter()
    for f in filas:
        grupos[(tuple(sorted(f["familias"])), f["decision"])] += 1
    resumen = {"total": len(filas), "decisiones": dict(Counter(f["decision"] for f in filas)),
               "grupos_top": [{"familias": list(k[0]), "decision": k[1], "n": v}
                              for k, v in grupos.most_common(25)]}
    (BASE / "matriz-cruces.json").write_text(
        json.dumps({"criterio": __doc__.splitlines()[8:14], "resumen": resumen, "filas": filas},
                   indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(resumen, indent=1, ensure_ascii=False))
    # Negativos reales: el par invertido no existe aparte; el fallo del lote
    # esta registrado pero ya no se etiqueta como prohibicion universal
    inv = "--".join(filas[0]["id"].split("--")[::-1])
    assert inv not in {f["id"] for f in filas}
    assert "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5" in lote_por_id
    decs = Counter(f["decision"] for f in filas)
    assert decs["habilitable_con_condiciones"] == 2, decs  # solo UES
    assert decs["exploratorio_con_condiciones_pendientes"] == 2, decs  # F1 + F2
    assert decs["no_validado"] == 2, decs  # fallo del lote, incompatibilidad no demostrada
    assert decs["no_comparable"] == 2, decs  # solo misma-serie anterior vs actual
    assert sum(decs.values()) == 3916
    print("MATRIZ OK:", len(filas))


if __name__ == "__main__":
    main()
