"""Sincroniza solo los triples de la ampliación en Studio y conserva sus demás ediciones."""

from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen

from rdflib import Graph, Literal, XSD
from rdflib.compare import isomorphic

from construir_catalogo import ROOT, motor

API = "http://127.0.0.1:8137/api"


def api(path, payload):
    req = Request(API + path, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=60) as response:
        result = json.load(response)
    if isinstance(result, dict) and (result.get("error") or result.get("ok") is False):
        raise RuntimeError(str(result))
    return result


def cambios(current, desired, previous):
    """No retirar triples ajenos al conjunto gestionado por esta sincronización."""
    remove = previous - desired
    add = desired - current
    owned = (previous & desired) + add
    return remove, add, owned


def normalizar_cadenas(graph):
    """Compara las dos escrituras equivalentes de cadenas RDF 1.1.

    El motor exporta xsd:string como literal simple. Se conserva el léxico,
    incluido el espacio y los ceros; los idiomas y otros tipos no se cambian.
    """
    result = Graph()
    for prefix, namespace in graph.namespaces():
        result.bind(prefix, namespace)
    for subject, predicate, value in graph:
        if isinstance(value, Literal) and value.datatype == XSD.string:
            value = Literal(str(value))
        result.add((subject, predicate, value))
    return result


def main():
    folder = ROOT / "data/portal"
    desired = normalizar_cadenas(Graph().parse(folder / "ampliacion.ttl", format="turtle"))
    managed_file = folder / "studio-managed.ttl"
    previous = Graph()
    if managed_file.exists():
        previous.parse(managed_file, format="turtle")
    previous = normalizar_cadenas(previous)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = ROOT / "data/backups" / f"studio-antes-portal-{stamp}.ttl"
    backup.parent.mkdir(parents=True, exist_ok=True)
    api("/save", {"path": str(backup), "format": "turtle"})
    current = normalizar_cadenas(Graph().parse(backup, format="turtle"))
    remove, add, owned = cambios(current, desired, previous)
    expected = (current - remove) + add
    expected_file = folder / "studio-previsto.ttl"
    expected.serialize(expected_file, format="turtle", encoding="utf-8")
    validation_store = ROOT / "store" / ("studio-validacion-" + stamp)
    motor(["load", str(expected_file)], validation_store)
    validation = motor(["shacl", str(folder / "shapes.ttl")], validation_store)
    if validation.get("conforms") is not True:
        raise RuntimeError("El estado previsto de Studio no supera SHACL; no se aplicaron cambios: " + json.dumps(validation, ensure_ascii=False))
    observed_file = folder / "studio-verificacion.ttl"
    api("/save", {"path": str(observed_file), "format": "turtle"})
    if not isomorphic(current, normalizar_cadenas(Graph().parse(observed_file, format="turtle"))):
        raise RuntimeError("Studio cambió durante la preparación. No se aplicaron cambios; vuelve a ejecutar cuando termine la edición.")
    addfile = folder / "studio-insertar.ttl"
    add.serialize(addfile, format="turtle", encoding="utf-8")
    # DELETE DATA va por bloques; /load lee el archivo local sin enviar todo en HTTP.
    statements = [f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in remove]
    for offset in range(0, len(statements), 200):
        api("/update", {"query": "DELETE DATA {\n" + "\n".join(statements[offset:offset + 200]) + "\n}"})
    if len(add):
        api("/load", {"path": str(addfile)})
    api("/save", {"path": str(observed_file), "format": "turtle"})
    observed = normalizar_cadenas(Graph().parse(observed_file, format="turtle"))
    if not isomorphic(observed, expected):
        raise RuntimeError("Studio cambió durante la sincronización o no aplicó los cambios esperados. Conserva el respaldo y revisa antes de repetir.")
    canonical_pending = False
    recovery = None
    try:
        api("/save", {"path": str(ROOT / "data/catalogo/studio-live.ttl"), "format": "turtle"})
    except RuntimeError as error:
        if 'os error 1224' not in str(error):
            raise
        # Windows no permite reemplazar un archivo que sigue mapeado por
        # Studio. El grafo ya fue comprobado: fijar una copia nueva y emitir
        # el recibo sin repetir DELETE/LOAD ni perder la propiedad gestionada.
        recovery = ROOT / 'data/backups' / f'studio-sincronizado-{stamp}.ttl'
        api('/save', {'path': str(recovery), 'format': 'turtle'})
        canonical_pending = True
    owned.serialize(managed_file, format="turtle", encoding="utf-8")
    report = {"respaldo": str(backup.relative_to(ROOT)), "triples_insertados": len(add), "triples_retirados_gestionados": len(remove),
              "triples_totales_studio": len(observed), "triples_gestionados": len(owned), "verificado": True, "shacl": validation}
    if canonical_pending:
        import hashlib
        report.update(archivo_canonico_pendiente=True, copia_viva_recuperacion=str(recovery.relative_to(ROOT)),
                      copia_sha256=hashlib.sha256(recovery.read_bytes()).hexdigest())
    (ROOT / "reports/studio-portal-sync.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
