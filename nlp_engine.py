"""Offline NLP. No HTTP clients, credentials, or runtime downloads."""
from collections import Counter
from functools import cached_property
from importlib.resources import files
import re

MAX_CHARACTERS = 50000
STOPWORDS = set("a an the and or but if while of in on at to for from with by is are was were be been being it its this that these those as not have has had do does did will would can could should we you they he she i my our their his her us them also very".split())


class LocalNLP:
    @staticmethod
    def validate(text):
        text = text.strip()
        if not text:
            raise ValueError("Enter some text first.")
        if len(text) > MAX_CHARACTERS:
            raise ValueError("Please use 50,000 characters or fewer.")
        return text

    @cached_property
    def sentiment_model(self):
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        return SentimentIntensityAnalyzer()

    @cached_property
    def entity_model(self):
        import spacy
        try:
            return spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
        except OSError as exc:
            raise ValueError("Install the local entity model once: python -m spacy download en_core_web_sm") from exc

    @cached_property
    def spelling_model(self):
        from symspellpy import SymSpell
        model = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary = files("symspellpy").joinpath("frequency_dictionary_en_82_765.txt")
        if not model.load_dictionary(str(dictionary), term_index=0, count_index=1):
            raise RuntimeError("The bundled spelling dictionary could not be loaded.")
        return model

    def sentiment_analysis(self, text):
        scores = self.sentiment_model.polarity_scores(self.validate(text))
        label = "Positive" if scores["compound"] >= .05 else "Negative" if scores["compound"] <= -.05 else "Neutral"
        return {"label": label, "compound": scores["compound"], "scored_labels": [
            {"label": name, "score": scores[key]} for name, key in
            [("Positive", "pos"), ("Neutral", "neu"), ("Negative", "neg")]]}

    def do_summarize(self, text, sentence_count=3):
        text = self.validate(text)
        if not 1 <= sentence_count <= 10:
            raise ValueError("Choose between 1 and 10 summary sentences.")
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
        if len(sentences) <= sentence_count:
            return " ".join(sentences)
        tokens = [[w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOPWORDS] for s in sentences]
        counts = Counter(w for words in tokens for w in words)
        ranked = sorted(range(len(sentences)), key=lambda i: sum(counts[w] for w in tokens[i]) / max(len(tokens[i]), 1) ** .5, reverse=True)
        return " ".join(sentences[i] for i in sorted(ranked[:sentence_count]))

    def do_ner(self, text, word=""):
        doc = self.entity_model(self.validate(text))
        query = word.strip().casefold()
        return [{"text": e.text, "label": e.label_, "start": e.start_char, "end": e.end_char}
                for e in doc.ents if not query or query in e.text.casefold() or query == e.label_.casefold()]

    def do_lang_detect(self, text):
        from langdetect import DetectorFactory, LangDetectException, detect_langs
        text = self.validate(text)
        if sum(c.isalpha() for c in text) < 10:
            raise ValueError("Use at least 10 letters; longer passages give better language estimates.")
        DetectorFactory.seed = 0
        try:
            return [{"language": item.lang, "probability": item.prob} for item in detect_langs(text)]
        except LangDetectException as exc:
            raise ValueError("Could not identify a language. Try a longer passage.") from exc

    def do_grammer_spelling(self, text):
        """Conservative dictionary correction plus a few explicit grammar rules."""
        from symspellpy import Verbosity
        text = self.validate(text)
        def correct(match):
            original = match.group()
            if original[0].isupper() or "'" in original or len(original) < 3:
                return original
            choices = self.spelling_model.lookup(original.lower(), Verbosity.TOP, max_edit_distance=1)
            return choices[0].term if choices else original
        text = re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", correct, text)
        text = re.sub(r"\bi\b", "I", text)
        for pattern, replacement in [(r"\bI is\b", "I am"), (r"\b(he|she|it) are\b", r"\1 is"),
                                     (r"\b(we|they|you) is\b", r"\1 are")]:
            text = re.sub(pattern, replacement, text, flags=re.I)
        text = re.sub(r"[ \t]+([,.!?;:])", r"\1", text)
        return text

    def do_headline_generation(self, text):
        sentence = self.do_summarize(text, sentence_count=1)
        words = sentence.split()
        headline = " ".join(words[:12]).rstrip(".,!?;:")
        return headline + ("…" if len(words) > 12 else "")
