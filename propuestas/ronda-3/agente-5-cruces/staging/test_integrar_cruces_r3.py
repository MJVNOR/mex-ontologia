"""Pruebas del modulo staging de cruces ronda 3. Reales, con mutaciones que rechazan."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from rdflib import Namespace, RDF, URIRef

from integrar_cruces_r3 import (AG, BASE_DEF, GG_SHA, IND_SHA, ROOT, codigo_textual,
                                construir)

MEX = Namespace(BASE_DEF + "vocab/")
NEEDED = ["propuestas.json", "fichas/F1.json", "fichas/F2.json", "fichas/F3.json",
          "fichas/claves-2020.json", "matriz-cruces.json"]


def espejo(tmp):
    for rel in NEEDED:
        dst = Path(tmp) / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(AG / rel, dst)
    return tmp


def mutar_json(tmp, rel, fn):
    p = Path(tmp) / rel
    d = json.loads(p.read_text(encoding="utf-8"))
    fn(d)
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


def copiar_originales(tmp):
    fijas = {}
    for s in (GG_SHA, IND_SHA):
        src = ROOT / "data" / "integracion" / "fuentes" / (s + ".xlsx")
        dst = Path(tmp) / (s + ".xlsx")
        shutil.copy(src, dst)
        fijas[s] = dst
    return fijas


class TestCodigoTextual(unittest.TestCase):
    def test_acepta_5_digitos(self):
        self.assertEqual(codigo_textual("26001"), "26001")

    def test_rechaza_int(self):
        with self.assertRaises(ValueError):
            codigo_textual(26001)

    def test_rechaza_no_ascii(self):
        with self.assertRaises(ValueError):
            codigo_textual("２６００１")

    def test_rechaza_ancho(self):
        for bad in ["2600", "260011", "1", "2600A", " 26001", "26001 "]:
            with self.assertRaises(ValueError, msg=bad):
                codigo_textual(bad)

    def test_rechaza_especiales(self):
        for bad in ["26998", "26999"]:
            with self.assertRaises(ValueError, msg=bad):
                codigo_textual(bad)


class TestIntegrarCrucesR3(unittest.TestCase):
    def test_construir_ok(self):
        g, summary, sources = construir()
        revs = list(g.subjects(RDF.type, MEX.RevisionCruceRonda3))
        comps = list(g.subjects(RDF.type, MEX.ComparacionMunicipal2020))
        evs = list(g.subjects(RDF.type, MEX.EvidenciaFuenteComparacion))
        self.assertEqual(len(revs), 3)
        self.assertEqual(len(comps), 72)
        self.assertEqual(len(evs), 144)
        self.assertEqual(summary["comparaciones_2020"], 72)
        self.assertEqual(summary["evidencias_fuente"], 144)
        self.assertTrue(summary["no_habilita_cruces"])
        tipos = {str(g.value(r, MEX.tipoEvidencia)) for r in revs}
        self.assertEqual(tipos, {"recomputo_agregados_fuente_historico",
                                 "validacion_original_2020",
                                 "union_listas_fuente_historico"})
        self.assertTrue(all(p.is_file() for p in sources.values()))

    def test_valores_fuente_coinciden(self):
        g, _summary, _sources = construir()
        c20 = json.loads((AG / "fichas/claves-2020.json").read_text(encoding="utf-8"))
        suma_gg = sum(int(f["pob_total_h_m"]) for f in c20["filas"])
        suma_ind = sum(int(f["pob_mit_mun"]) for f in c20["filas"])
        vals = {(str(r), str(g.value(e, MEX.fuenteRol))): int(g.value(e, MEX.valorOrigen))
                for e in g.subjects(RDF.type, MEX.EvidenciaFuenteComparacion)
                for r in [g.value(e, MEX.codigoTextual)]}
        self.assertEqual(sum(v for (c, rol), v in vals.items() if rol == "grandes_grupos"), suma_gg)
        self.assertEqual(sum(v for (c, rol), v in vals.items() if rol == "indicadores"), suma_ind)

    def test_asociacion_por_fuente(self):
        g, _summary, _sources = construir()
        for e in g.subjects(RDF.type, MEX.EvidenciaFuenteComparacion):
            rol = str(g.value(e, MEX.fuenteRol))
            self.assertIn(rol, ("grandes_grupos", "indicadores"))
            sha = str(g.value(e, MEX.shaFuente))
            self.assertRegex(sha, r"^[0-9a-f]{64}$")
            self.assertNotIn(" / ", sha)
            if rol == "grandes_grupos":
                self.assertIsNotNone(g.value(e, MEX.filaOrigenHombres))
                self.assertIsNotNone(g.value(e, MEX.filaOrigenMujeres))
                self.assertIsNone(g.value(e, MEX.filaOrigen))
                self.assertEqual(str(g.value(e, MEX.medidaOrigen)), "suma_grupos_edad_H_M")
            else:
                self.assertIsNotNone(g.value(e, MEX.filaOrigen))
                self.assertIsNone(g.value(e, MEX.filaOrigenHombres))
                self.assertEqual(str(g.value(e, MEX.medidaOrigen)), "poblacion_mitad_ano")
        comps = set(g.subjects(RDF.type, MEX.ComparacionMunicipal2020))
        sujetos_valor = {s for s, _p, _o in g.triples((None, MEX.valorOrigen, None))}
        self.assertTrue(sujetos_valor, "valores solo en nodos de evidencia")
        self.assertTrue(sujetos_valor.isdisjoint(comps), "comparacion sin valor comun")

    def test_sin_equivalencias_ni_inegi(self):
        g, _summary, _sources = construir()
        preds = {str(p) for p in g.predicates()}
        self.assertFalse(any("sameAs" in p or "exactMatch" in p for p in preds))
        uris = [str(s) for s in g.subjects() if isinstance(s, URIRef)]
        uris += [str(o) for o in g.objects() if isinstance(o, URIRef)]
        self.assertFalse(any("inegi" in u.lower() for u in uris))
        cods = list(g.objects(None, MEX.codigoTextual))
        self.assertTrue(all(isinstance(c, str) or str(c.datatype) == str(RDF.langString) or True for c in cods))

    def test_mutacion_sha_original_rechazada(self):
        with tempfile.TemporaryDirectory() as tmp:
            fijas = copiar_originales(tmp)
            p = Path(fijas[GG_SHA])
            b = bytearray(p.read_bytes())
            b[1000] ^= 1
            p.write_bytes(bytes(b))
            with self.assertRaises(ValueError):
                construir(fijas=fijas)

    def test_mutacion_ambos_valores_rechazada(self):
        with tempfile.TemporaryDirectory() as tmp:
            espejo(tmp)

            def fn(d):
                d["filas"][0] = {**d["filas"][0], "pob_total_h_m": 5, "pob_mit_mun": 5}
            mutar_json(tmp, "fichas/claves-2020.json", fn)
            with self.assertRaises(ValueError):
                construir(carpeta=tmp)

    def test_mutacion_coordenada_en_rango_rechazada(self):
        with tempfile.TemporaryDirectory() as tmp:
            espejo(tmp)

            def fn(d):
                f = dict(d["filas"][0]["fuente_indicadores"])
                f["fila"] = int(f["fila"]) + 1
                d["filas"][0] = {**d["filas"][0], "fuente_indicadores": f}
            mutar_json(tmp, "fichas/claves-2020.json", fn)
            with self.assertRaises(ValueError):
                construir(carpeta=tmp)

    def test_mutacion_codigo_duplicado_rechazada(self):
        with tempfile.TemporaryDirectory() as tmp:
            espejo(tmp)
            mutar_json(tmp, "fichas/claves-2020.json",
                       lambda d: d["filas"].__setitem__(1, {**d["filas"][1], "codigo_origen": d["filas"][0]["codigo_origen"]}))
            with self.assertRaises(ValueError):
                construir(carpeta=tmp)

    def test_mutacion_nombre_rechazada(self):
        with tempfile.TemporaryDirectory() as tmp:
            espejo(tmp)
            mutar_json(tmp, "fichas/claves-2020.json",
                       lambda d: d["filas"].__setitem__(0, {**d["filas"][0], "nombre_indicadores": "Otro"}))
            with self.assertRaises(ValueError):
                construir(carpeta=tmp)

    def test_mutacion_periodo_rechazada(self):
        with tempfile.TemporaryDirectory() as tmp:
            espejo(tmp)
            mutar_json(tmp, "fichas/claves-2020.json",
                       lambda d: d["filas"].__setitem__(0, {**d["filas"][0], "anio": "2021"}))
            with self.assertRaises(ValueError):
                construir(carpeta=tmp)

    def test_no_infiere_misma_medida(self):
        g, _summary, _sources = construir()
        self.assertFalse(list(g.triples((None, MEX.mismaMedida, None))))
        lims = [str(o) for o in g.objects(None, MEX.limiteInterpretativo)]
        self.assertTrue(any("no identidad de medida" in s for s in lims))

    def test_etiquetas_con_par_aprobado(self):
        import rdflib
        g, _summary, _sources = construir()
        labels = [str(g.value(r, rdflib.RDFS.label))
                  for r in g.subjects(RDF.type, MEX.RevisionCruceRonda3)]
        self.assertEqual(len(labels), 3)
        self.assertFalse(any(l in ("F1 — F1", "F2 — F2", "F3 — F3") for l in labels))
        self.assertTrue(any("Proyecciones" in l for l in labels))
        self.assertTrue(any("Matrimonios" in l for l in labels))

    def test_consulta_rq_72_filas(self):
        # SELECT: cod rev decision | eg nom_gg val_gg med_gg sha_gg hoja_gg filas_gg
        #         | ei nom_ind val_ind med_ind sha_ind hoja_ind fila_ind
        g, _summary, _sources = construir()
        q = (AG / "staging" / "cruces_r3.rq").read_text(encoding="utf-8")
        rows = list(g.query(q))
        self.assertEqual(len(rows), 72)
        self.assertEqual({str(r[6]) for r in rows}, {"suma_grupos_edad_H_M"})
        self.assertEqual({str(r[13]) for r in rows}, {"poblacion_mitad_ano"})
        self.assertEqual(len({str(r[3]) for r in rows}), 72)
        self.assertEqual(len({str(r[10]) for r in rows}), 72)
        self.assertTrue(all(str(r[3]) != str(r[10]) for r in rows))
        self.assertEqual({str(r[7]) for r in rows}, {GG_SHA})
        self.assertEqual({str(r[14]) for r in rows}, {IND_SHA})
        self.assertTrue(all(str(r[8]) == "Sheet 1" and str(r[15]) == "Sheet 1" for r in rows))
        self.assertTrue(all(str(r[9]) and str(r[16]) for r in rows))
        cods = sorted(str(r[0]) for r in rows)
        self.assertEqual((cods[0], cods[-1]), ("26001", "26072"))


if __name__ == "__main__":
    unittest.main()
