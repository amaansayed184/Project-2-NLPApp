"""Offline NLP. No HTTP clients, credentials, or runtime downloads."""
from collections import Counter
from functools import cached_property
from importlib.resources import files
import math
import re

MAX_CHARACTERS = 50000
STOPWORDS = set("a an the and or but if while of in on at to for from with by is are was were be been being it its this that these those as not have has had do does did will would can could should we you they he she i my our their his her us them also very".split())


class LocalNLP:
    @staticmethod
    def validate(text):
        if not isinstance(text, str):
            raise ValueError("Text must be a string.")
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
    def sentence_model(self):
        import spacy
        pipeline = spacy.blank("en")
        pipeline.add_pipe("sentencizer")
        return pipeline

    @cached_property
    def entity_model(self):
        import spacy
        try:
            return spacy.load("en_core_web_sm")
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
        text = self.validate(text)
        scores = self.sentiment_model.polarity_scores(text)
        label = "Positive" if scores["compound"] >= .05 else "Negative" if scores["compound"] <= -.05 else "Neutral"
        sentences = [{"text": span.text.strip(), "compound": self.sentiment_model.polarity_scores(span.text)["compound"]}
                     for span in self.sentence_model(text).sents if span.text.strip()]
        positive = sum(item["compound"] >= .3 for item in sentences)
        negative = sum(item["compound"] <= -.3 for item in sentences)
        if positive and negative and min(positive, negative) / (positive + negative) >= .25 and abs(scores["compound"]) < .5:
            label = "Mixed"
        return {"label": label, "compound": scores["compound"], "sentences": sentences, "scored_labels": [
            {"label": name, "score": scores[key]} for name, key in
            [("Positive", "pos"), ("Neutral", "neu"), ("Negative", "neg")]]}

    @staticmethod
    def _cosine(left, right):
        return sum(value * right.get(key, 0.0) for key, value in left.items())

    def _ranked_sentences(self, text, count):
        """Sparse TF-IDF centroid relevance with greedy redundancy reduction.

        Runs in O(sentence_count * requested_count * vocabulary_per_sentence),
        rather than constructing a quadratic all-pairs similarity matrix.
        """
        doc = self.entity_model(text, disable=["ner"])
        sentences, tokens, seen = [], [], set()
        for sentence in doc.sents:
            content = sentence.text.strip()
            signature = " ".join(re.findall(r"\w+", content.casefold()))
            if not signature or signature in seen:
                continue
            seen.add(signature)
            sentences.append(content)
            tokens.append([t.lemma_.casefold() for t in sentence
                           if t.is_alpha and not t.is_stop and t.lemma_.casefold() not in STOPWORDS])
        if not sentences:
            raise ValueError("Enter a passage containing words to summarize.")
        frequencies = Counter(term for terms in tokens for term in set(terms))
        vectors = []
        for terms in tokens:
            vector = {term: (1 + math.log(number)) * (1 + math.log((1 + len(tokens)) / (1 + frequencies[term])))
                      for term, number in Counter(terms).items()}
            norm = math.sqrt(sum(v * v for v in vector.values())) or 1
            vectors.append({term: value / norm for term, value in vector.items()})
        centroid = Counter()
        for vector in vectors:
            centroid.update(vector)
        norm = math.sqrt(sum(v * v for v in centroid.values())) or 1
        centroid = {term: value / norm for term, value in centroid.items()}
        relevance = [self._cosine(vector, centroid) * min(1.0, len(tokens[i]) / 4)
                     + (0.06 / (i + 1) if tokens[i] else 0) for i, vector in enumerate(vectors)]
        selected = []
        remaining = set(range(len(sentences)))
        for _ in range(min(count, len(sentences))):
            candidate = max(sorted(remaining), key=lambda i: relevance[i] - .45 * max(
                (self._cosine(vectors[i], vectors[j]) for j in selected), default=0))
            selected.append(candidate)
            remaining.remove(candidate)
        return sentences, selected

    def do_summarize(self, text, sentence_count=3):
        text = self.validate(text)
        if isinstance(sentence_count, bool) or not isinstance(sentence_count, int) or not 1 <= sentence_count <= 10:
            raise ValueError("Choose between 1 and 10 summary sentences.")
        sentences, selected = self._ranked_sentences(text, sentence_count)
        return " ".join(sentences[i] for i in sorted(selected))

    def do_ner(self, text, word=""):
        text = self.validate(text)
        doc = self.entity_model(text)
        query = word.strip().casefold()
        aliases = {"person": {"PERSON"}, "people": {"PERSON"}, "organization": {"ORG"},
                   "organisation": {"ORG"}, "company": {"ORG"}, "location": {"GPE", "LOC", "FAC"},
                   "place": {"GPE", "LOC", "FAC"}, "date": {"DATE"}, "money": {"MONEY"}}
        labels = aliases.get(query, {query.upper()})
        return [{"text": e.text, "label": e.label_, "start": e.start_char, "end": e.end_char}
                for e in doc.ents if not query or query in e.text.casefold() or e.label_ in labels]

    def do_lang_detect(self, text):
        from langdetect import DetectorFactory, LangDetectException, detect_langs
        text = self.validate(text)
        if sum(c.isalpha() for c in text) < 10:
            raise ValueError("Use at least 10 letters; longer passages give better language estimates.")
        DetectorFactory.seed = 0
        try:
            guesses = detect_langs(text)
            warning = ""
            if guesses[0].prob < .8 or (len(guesses) > 1 and guesses[0].prob - guesses[1].prob < .2):
                warning = "Ambiguous language estimate. Try a longer passage in one language."
            elif sum(c.isalpha() for c in text) < 40:
                warning = "Short passage: the language estimate may be unreliable."
            return [{"language": item.lang, "probability": item.prob, "warning": warning} for item in guesses]
        except LangDetectException as exc:
            raise ValueError("Could not identify a language. Try a longer passage.") from exc

    def do_grammer_spelling(self, text):
        """Correct prose conservatively while keeping technical content intact."""
        from symspellpy import Verbosity
        text = self.validate(text)
        common = {"teh": "the", "recieve": "receive", "recieved": "received", "definately": "definitely",
                  "seperate": "separate", "grammer": "grammar", "langauge": "language", "adress": "address",
                  "accomodate": "accommodate", "enviroment": "environment", "occured": "occurred"}
        def correct(match):
            original = match.group()
            lower = original.lower()
            if original.isupper() or "'" in original or len(original) < 3:
                return original
            if lower in common:
                replacement = common[lower]
                return replacement.capitalize() if original[0].isupper() else replacement
            if original[0].isupper() or lower in self.spelling_model.words:
                return original
            choices = self.spelling_model.lookup(lower, Verbosity.CLOSEST, max_edit_distance=2 if len(lower) >= 6 else 1)
            # Avoid speculative substitutions for rare or similarly likely words.
            if choices and choices[0].count >= 1000 and (len(choices) == 1 or choices[0].count >= 3 * choices[1].count):
                return choices[0].term
            return original

        def prose(value):
            # Resolve common missing apostrophes before dictionary lookup can
            # turn a contraction into an unrelated word such as 'done'.
            value = re.sub(r"\b(dont|doesnt|isnt|arent|wasnt|werent|didnt|couldnt|shouldnt|wouldnt|havent|hasnt)\b",
                           lambda m: m.group()[:-1] + "'t", value, flags=re.I)
            value = re.sub(r"\bcant\b", "can't", value, flags=re.I)
            value = re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", correct, value)
            value = re.sub(r"\bi\b", "I", value)
            rules = [(r"\bI (?:is|are)\b", "I am"), (r"\b(he|she|it) (?:are|am)\b", r"\1 is"),
                     (r"\b(we|they|you) (?:is|am)\b", r"\1 are"),
                     (r"\b(he|she|it) don't\b", r"\1 doesn't"),
                     (r"\b(I|we|they|you) doesn't\b", r"\1 don't"),
                     (r"\b(the|a|an|is|are|was|were|to|of|and|in|on)([ \t]+)\1\b", r"\1")]
            for pattern, replacement in rules:
                value = re.sub(pattern, replacement, value, flags=re.I)
            return re.sub(r"[ \t]+([,.!?;:])", r"\1", value)

        protected = re.compile(r"```[\s\S]*?```|`[^`\n]*`|https?://\S+|www\.\S+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|[A-Za-z]:\\[^\s]+|\b[\w.-]*\d[\w.-]*\b")
        pieces, end = [], 0
        for match in protected.finditer(text):
            pieces.extend([prose(text[end:match.start()]), match.group()])
            end = match.end()
        pieces.append(prose(text[end:]))
        return "".join(pieces)

    def do_headline_generation(self, text):
        text = self.validate(text)
        sentences, selected = self._ranked_sentences(text, 1)
        sentence = sentences[selected[0]]
        words = sentence.split()
        # Prefer a complete short clause to an arbitrary mid-clause cut.
        if len(words) > 12:
            clauses = re.split(r"[,;:]\s+", sentence)
            if 5 <= len(clauses[0].split()) <= 12:
                return clauses[0].rstrip(".,!?;:")
        kept = words[:12]
        while len(kept) > 3 and kept[-1].casefold().strip(".,!?") in {"a", "an", "the", "and", "or", "of", "to", "in", "for", "with", "by", "at"}:
            kept.pop()
        headline = " ".join(kept).rstrip(".,!?;:")
        return headline + ("…" if len(words) > 12 else "")
