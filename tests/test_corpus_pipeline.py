import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "corpus_pipeline.py"
SPEC = importlib.util.spec_from_file_location("corpus_pipeline", SCRIPT)
assert SPEC and SPEC.loader
pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pipeline)


class CorpusPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "corpus"
        pipeline.ensure_layout(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def run_command(self, *arguments):
        return pipeline.main(["--root", str(self.root), *arguments])

    def add_fixture(self):
        inbox = pipeline.paths(self.root)["inbox"]
        text = (
            "TÍTULO DE PRUEBA\r\n"
            "\r\n"
            "[[PAGE: 1]]\r\n"
            "Capítulo 1 — Contexto\r\n"
            "La evidencia geológica no demuestra por sí sola una civilización.\r\n"
            "\r\n"
            "[[PAGE: 2]]\r\n"
            "Una hipótesis debe conservar su contexto y sus fuentes.\r\n"
        )
        source = inbox / "Autora_2026_Prueba_es.txt"
        source.write_bytes(text.encode("utf-8"))
        sidecar = {
            "title": "Prueba de trazabilidad",
            "creators": ["Autora, Ana"],
            "year": 2026,
            "edition": "Primera edición",
            "language": "es",
            "scope": {"status": "COMPLETA"},
            "classification": {
                "domains": ["MET"],
                "document_type": "MONOGRAFIA_ACADEMICA",
                "functions": ["APORTA_METODO"],
                "theory_ids": ["H01"],
                "corpus_status": "CANDIDATA"
            },
            "provenance": {"copy_source": "fixture local"}
        }
        (inbox / "Autora_2026_Prueba_es.txt.meta.json").write_text(
            json.dumps(sidecar), encoding="utf-8"
        )
        return source

    def test_end_to_end_and_fixity(self):
        original = self.add_fixture()
        original_hash = pipeline.sha256_file(original)
        self.assertEqual(self.run_command("inventory"), 0)

        manifest = pipeline.read_jsonl(pipeline.paths(self.root)["manifest"])
        self.assertEqual(len(manifest), 1)
        record = manifest[0]
        self.assertEqual(record["source_id"], "DCA-000001")
        self.assertEqual(record["fixity"]["original_sha256"], original_hash)
        self.assertEqual(record["metadata_missing"], [])
        self.assertEqual(record["text"]["page_markers"], 2)
        self.assertIn("\n", (self.root / record["normalized_path"]).read_text("utf-8"))
        self.assertNotIn("\r", (self.root / record["normalized_path"]).read_text("utf-8"))

        self.assertEqual(self.run_command("audit"), 0)
        self.assertEqual(self.run_command("chunk", "--max-chars", "500"), 0)
        chunks = pipeline.read_jsonl(pipeline.paths(self.root)["chunks"])
        self.assertGreaterEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["line_start"], 1)
        self.assertEqual(chunks[0]["source_sha256"], original_hash)

        self.assertEqual(
            self.run_command("search", "--query", "evidencia geológica", "--top", "3"),
            0,
        )
        self.assertEqual(
            self.run_command("select", "--source-id", "DCA-000001", "--lines", "3:5"),
            0,
        )
        self.assertEqual(self.run_command("verify"), 0)
        self.assertEqual(pipeline.sha256_file(original), original_hash)

    def test_duplicate_content_shares_one_document_record(self):
        source = self.add_fixture()
        duplicate = source.parent / "copia.txt"
        duplicate.write_bytes(source.read_bytes())
        self.assertEqual(self.run_command("inventory"), 0)
        manifest = pipeline.read_jsonl(pipeline.paths(self.root)["manifest"])
        self.assertEqual(len(manifest), 1)
        self.assertEqual(len(manifest[0]["files"]), 2)
        self.assertIn("EXACT_DUPLICATE_PATHS", manifest[0]["audit_flags"])

    def test_embedded_metadata_is_read_without_altering_source(self):
        inbox = pipeline.paths(self.root)["inbox"]
        source = inbox / "seleccion.txt"
        source.write_text(
            "=== CASSANDRA SOURCE METADATA ===\n"
            "title: Obra extensa\n"
            "creators: Autora Uno; Editor Dos\n"
            "year: 1980\n"
            "edition: edición crítica\n"
            "language: es\n"
            "scope: selección\n"
            "included_units: libro 1, versos 10-20\n"
            "document_type: EDICION_CRITICA\n"
            "copy_source: biblioteca local\n"
            "=== BEGIN SOURCE TEXT ===\n"
            "Texto conservado.\n",
            encoding="utf-8",
        )
        original_hash = pipeline.sha256_file(source)
        self.assertEqual(self.run_command("inventory"), 0)
        record = pipeline.read_jsonl(pipeline.paths(self.root)["manifest"])[0]
        self.assertEqual(record["bibliographic"]["title"], "Obra extensa")
        self.assertEqual(record["bibliographic"]["creators"], ["Autora Uno", "Editor Dos"])
        self.assertEqual(record["scope"]["status"], "SELECCION_SIN_VERIFICAR")
        self.assertEqual(record["metadata_source"], "embedded_header")
        self.assertEqual(pipeline.sha256_file(source), original_hash)

    def test_changed_bytes_receive_new_identifier_and_is_flagged(self):
        source = self.add_fixture()
        self.assertEqual(self.run_command("inventory"), 0)
        source.write_text("contenido sustituido", encoding="utf-8")
        self.assertEqual(self.run_command("inventory"), 0)
        manifest = pipeline.read_jsonl(pipeline.paths(self.root)["manifest"])
        self.assertEqual([item["source_id"] for item in manifest], ["DCA-000002"])
        self.assertIn("PATH_CONTENT_CHANGED_FROM:DCA-000001", manifest[0]["audit_flags"])
        registry = pipeline.read_jsonl(pipeline.paths(self.root)["registry"])
        self.assertEqual([item["source_id"] for item in registry], ["DCA-000001", "DCA-000002"])
        history = list((pipeline.paths(self.root)["indexes"] / "history").glob("*.jsonl"))
        self.assertEqual(len(history), 1)


if __name__ == "__main__":
    unittest.main()
