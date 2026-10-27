import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from mydb import Database
from nlp_engine import LocalNLP


class OfflineNLPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = LocalNLP()

    def test_all_tools_with_network_disabled(self):
        with patch.object(socket.socket, "connect", side_effect=AssertionError("Network is forbidden")), patch("socket.create_connection", side_effect=AssertionError("Network is forbidden")):
            e = self.engine
            self.assertEqual(e.sentiment_analysis("This is excellent. I love it!")["label"], "Positive")
            self.assertEqual(e.sentiment_analysis("This is awful. I hate it!")["label"], "Negative")
            text = "Apple opened an office in London. Apple hired engineers for the office. Rain fell yesterday."
            summary = e.do_summarize(text, 1)
            self.assertIn(summary, text)
            entities = e.do_ner("Barack Obama visited London on Monday.")
            self.assertTrue(any(item["label"] == "PERSON" for item in entities))
            self.assertTrue(any(item["text"] == "London" for item in entities))
            self.assertTrue(all(item["label"] == "PERSON" for item in e.do_ner("Barack Obama visited London.", "PERSON")))
            self.assertEqual(e.do_lang_detect("This is a long English sentence about a wonderful computer application.")[0]["language"], "en")
            self.assertEqual(e.do_grammer_spelling("i is happy with teh speling."), "I am happy with the spelling.")
            self.assertLessEqual(len(e.do_headline_generation(text).split()), 12)

    def test_input_limits(self):
        for method in [self.engine.sentiment_analysis, self.engine.do_summarize, self.engine.do_ner,
                       self.engine.do_lang_detect, self.engine.do_grammer_spelling, self.engine.do_headline_generation]:
            for invalid in ["  ", "x" * 50001]:
                with self.assertRaises(ValueError):
                    method(invalid)
        with self.assertRaises(ValueError):
            self.engine.do_lang_detect("1234 !")


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "accounts.json"
        self.db = Database(self.path)

    def test_registration_login_and_salted_storage(self):
        self.assertTrue(self.db.add_data("Tester", "Test@example.com", "password123"))
        self.assertFalse(self.db.add_data("Tester", "TEST@example.com", "password123"))
        self.assertTrue(self.db.search(" TEST@example.com ", "password123"))
        self.assertFalse(self.db.search("test@example.com", "incorrect"))
        self.db.add_data("Other", "other@example.com", "password123")
        data = json.loads(self.path.read_text())
        self.assertNotIn("password123", self.path.read_text())
        self.assertNotEqual(data["test@example.com"]["password_hash"], data["other@example.com"]["password_hash"])

    def test_legacy_migration_preserves_login(self):
        self.path.write_text(json.dumps({"Old@example.com": ["Old", "oldpass"]}))
        self.db.migrate_legacy()
        self.assertTrue(self.db.search("old@example.com", "oldpass"))
        self.assertNotIn("oldpass", self.path.read_text())

    def test_invalid_accounts_and_corrupt_storage(self):
        for name, email, password in [("", "x@example.com", "password123"), ("X", "invalid", "password123"), ("X", "x@example.com", "short")]:
            with self.assertRaises(ValueError):
                self.db.add_data(name, email, password)
        self.path.write_text("broken json")
        with self.assertRaises(ValueError):
            self.db.search("x@example.com", "password123")
        self.assertEqual(self.path.read_text(), "broken json")


if __name__ == "__main__":
    unittest.main()
