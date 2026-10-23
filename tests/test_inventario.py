from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import inventariar_portal as portal


class InventarioTest(unittest.TestCase):
    def test_diccionario_no_se_confunde_con_datos_geograficos(self):
        tipo, _ = portal.clasificar({"name": "Diccionario de variables", "format": "CSV"}, "Geometrías municipales")
        self.assertEqual(tipo, "diccionario")

    def test_geografia_se_marca_como_candidata(self):
        tipo, _ = portal.clasificar({"name": "Datos", "format": "JSON"}, "Geometrías municipales")
        self.assertEqual(tipo, "candidato_geoespacial")

    def test_iframe_dinamico_conserva_destino_sin_ejecutar_script(self):
        body = "<title>Mapa</title><iframe id='mapa'></iframe><script>window.powerbiPaths={desktop:'https://inteligenciadedatos.sonora.gob.mx/accesos-publicos',mobile:'javascript:alert(1)'};</script>"
        with patch.object(portal, "leer", return_value={"ok": True, "url": "https://www.sonora.gob.mx/datos/mapa", "content_type": "text/html", "body": body}):
            result = portal.inspeccionar_pagina({"url": "https://www.sonora.gob.mx/datos/mapa"})
        self.assertEqual(result["destinos_visualizacion"], ["https://inteligenciadedatos.sonora.gob.mx/accesos-publicos"])

    def test_datastore_pide_cero_filas_y_no_conserva_valores(self):
        with patch.object(portal, "api", return_value={"ok": True, "url": "https://example.org/api", "result": {"total": 10, "fields": [{"id": "municipio", "type": "text"}], "records": [{"municipio": "valor no conservado"}]}}) as request:
            result = portal.comprobar_datastore("recurso")
        request.assert_called_once_with("datastore_search", resource_id="recurso", limit=0)
        self.assertNotIn("records", result)
        self.assertEqual(result["registros_recibidos_descartados"], 1)

    def test_error_no_se_presenta_como_esquema_verificado(self):
        with patch.object(portal, "api", return_value={"ok": False, "url": "https://example.org/api", "error": "404"}):
            result = portal.comprobar_datastore("recurso")
        self.assertFalse(result["ok"])
        self.assertNotIn("campos", result)

    def test_lista_de_nombres_no_pierde_organizaciones_sin_conjuntos(self):
        responses = [
            {"ok": True, "url": "https://example.org/list", "result": ["con_datos", "sin_datos"]},
            {"ok": True, "url": "https://example.org/list?all_fields=true", "result": [{"name": "con_datos", "id": "1"}]},
            {"ok": True, "result": {"name": "sin_datos", "id": "2", "package_count": 0}},
        ]
        with patch.object(portal, "api", side_effect=responses):
            result = portal.listar_entidades("organization")
        self.assertEqual([item["name"] for item in result["result"]], ["con_datos", "sin_datos"])


if __name__ == "__main__":
    unittest.main()
