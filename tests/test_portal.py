import copy
from pathlib import Path
import sys
import unittest

from rdflib import DCAT, Graph, Literal, Namespace, OWL, RDF, URIRef

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ampliar_portal import ampliar
from sincronizar_studio_portal import cambios


class PortalTest(unittest.TestCase):
    def setUp(self):
        self.base = "https://example.org/mex-ontologi/"
        self.mex = Namespace(self.base + "vocab/")
        self.inventory = {
            "generado_en_utc": "2026-10-23T00:00:00+00:00",
            "organizaciones": {"items": []}, "grupos": {"items": []}, "secciones": [],
            "paginas": [{"url": "https://www.sonora.gob.mx/datos/prueba", "nombre": "Prueba", "tipo": "herramienta",
                         "destinos_visualizacion": ["https://app.powerbi.com/view?r=publico"]}],
            "recursos": [self.resource("r1"), self.resource("r2")],
        }

    def resource(self, id_):
        return {"id": id_, "nombre": "Datos", "conjunto": "Prueba", "estructura": "esquema_datastore_verificado",
                "clasificacion": "datos_estructurados", "evidencia_clasificacion": "Formato CSV",
                "datastore": {"ok": True, "url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=" + id_ + "&limit=0",
                              "campos": [{"id": "municipio", "type": "text"}, {"id": "año", "type": "int"}]}}

    def test_columnas_con_mismo_nombre_son_entidades_distintas(self):
        g, _ = ampliar(self.inventory, self.base)
        columns = set(g.subjects(self.mex.nombreCampo, Literal("municipio")))
        self.assertEqual(len(columns), 2)
        self.assertFalse(list(g.triples((None, OWL.sameAs, None))))

    def test_reordenar_campos_no_cambia_su_identidad(self):
        g, _ = ampliar(self.inventory, self.base)
        changed = copy.deepcopy(self.inventory)
        changed["recursos"][0]["datastore"]["campos"].reverse()
        other, _ = ampliar(changed, self.base)
        self.assertEqual(set(g.subjects(RDF.type, self.mex.ColumnaObservada)), set(other.subjects(RDF.type, self.mex.ColumnaObservada)))

    def test_enlace_de_tablero_no_afirma_linaje_de_datos(self):
        g, _ = ampliar(self.inventory, self.base)
        self.assertEqual(len(set(g.subjects(RDF.type, self.mex.VisualizacionDeclarada))), 1)
        self.assertFalse(list(g.triples((None, DCAT.servesDataset, None))))

    def test_recurso_pendiente_no_fabrica_esquema(self):
        self.inventory["recursos"] = [dict(self.resource("r1"), datastore={"ok": False}, estructura="pendiente")]
        g, _ = ampliar(self.inventory, self.base)
        self.assertFalse(list(g.subjects(RDF.type, self.mex.EsquemaObservado)))

    def test_sincronizacion_conserva_ediciones_ajenas(self):
        user = (URIRef("urn:usuario"), URIRef("urn:nota"), Literal("Edición manual"))
        old = (URIRef("urn:recurso"), URIRef("urn:estado"), Literal("pendiente"))
        new = (old[0], old[1], Literal("verificado"))
        current, desired, previous = Graph(), Graph(), Graph()
        current.add(user).add(old)
        desired.add(new)
        previous.add(old)
        remove, add, managed = cambios(current, desired, previous)
        result = (current - remove) + add
        self.assertIn(user, result)
        self.assertNotIn(old, result)
        self.assertIn(new, result)
        self.assertNotIn(user, managed)

    def test_sincronizacion_repetida_no_inserta_duplicados(self):
        t = (URIRef("urn:recurso"), URIRef("urn:campo"), Literal("valor"))
        graph = Graph().add(t)
        remove, add, _ = cambios(graph, graph, graph)
        self.assertEqual((len(remove), len(add)), (0, 0))


if __name__ == "__main__":
    unittest.main()
