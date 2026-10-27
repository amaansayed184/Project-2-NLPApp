"""Targeted regressions; these examples are not an accuracy benchmark."""
import socket
import unittest
from unittest.mock import patch

from nlp_engine import LocalNLP


class QualityRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = LocalNLP()

    def setUp(self):
        network = patch.object(socket.socket, "connect", side_effect=AssertionError("Offline test"))
        network.start()
        self.addCleanup(network.stop)

    def test_summary_removes_duplicate_sentences(self):
        text = "Solar panels produce clean electricity. Solar panels produce clean electricity. Batteries store energy for use at night."
        result = self.engine.do_summarize(text, 3)
        self.assertEqual(result.count("Solar panels produce clean electricity."), 1)
        self.assertIn("Batteries store energy", result)

    def test_sentence_boundaries_preserve_abbreviations_and_decimals(self):
        sentences, _ = self.engine._ranked_sentences("Dr. Smith visited New York. He paid 3.5 million dollars.", 2)
        self.assertEqual(sentences, ["Dr. Smith visited New York.", "He paid 3.5 million dollars."])

    def test_summary_is_extractive_and_in_source_order(self):
        text = "The college opened a laboratory. Students use computers for research. Teachers support the research projects."
        sentences, _ = self.engine._ranked_sentences(text, 3)
        summary = self.engine.do_summarize(text, 2)
        selected = [sentence for sentence in sentences if sentence in summary]
        self.assertEqual(summary, " ".join(selected))
        self.assertEqual(len(selected), 2)

    def test_summary_count_validation_and_punctuation(self):
        for value in [True, 1.5, "3", 0, 11]:
            with self.assertRaises(ValueError):
                self.engine.do_summarize("A normal sentence.", value)
        with self.assertRaises(ValueError):
            self.engine.do_summarize("!!! ...")

    def test_headline_prefers_complete_short_clause(self):
        text = "The college opened a new laboratory, which will support many students in their research projects for years."
        self.assertEqual(self.engine.do_headline_generation(text), "The college opened a new laboratory")

    def test_spelling_corrects_common_long_and_capitalized_typos(self):
        self.assertEqual(self.engine.do_grammer_spelling("Teh enviroment is definately improving."),
                         "The environment is definitely improving.")

    def test_spelling_preserves_technical_content(self):
        text = "OpenAI uses Python3.12. Email teh@example.com; visit https://example.com/i and use `pip instal spacy`."
        self.assertEqual(self.engine.do_grammer_spelling(text), text)
        path = r"C:\teh\speling\v2.txt"
        self.assertEqual(self.engine.do_grammer_spelling(path), path)

    def test_spelling_preserves_multiline_code_blocks(self):
        code = "```python\ni is teh\n```"
        self.assertEqual(self.engine.do_grammer_spelling(code), code)

    def test_grammar_contractions_repetition_and_agreement(self):
        self.assertEqual(self.engine.do_grammer_spelling("he dont like it. they is ready. I are happy with the the project."),
                         "he doesn't like it. they are ready. I am happy with the project.")

    def test_mixed_sentiment_keeps_sentence_evidence(self):
        result = self.engine.sentiment_analysis("The camera is amazing. The battery is terrible.")
        self.assertEqual(result["label"], "Mixed")
        self.assertGreater(result["sentences"][0]["compound"], 0)
        self.assertLess(result["sentences"][1]["compound"], 0)

    def test_language_warns_for_short_passages(self):
        result = self.engine.do_lang_detect("This is English text.")
        self.assertIn("Short passage", result[0]["warning"])

    def test_entity_filter_accepts_human_label(self):
        entities = self.engine.do_ner("Barack Obama visited London.", "location")
        self.assertTrue(any(item["text"] == "London" for item in entities))
        self.assertTrue(all(item["label"] in {"GPE", "LOC", "FAC"} for item in entities))


if __name__ == "__main__":
    unittest.main()
