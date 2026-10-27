"""Check the active interpreter and run all six tools with networking blocked."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    print(f"Python: {sys.version.split()[0]}\nInterpreter: {sys.executable}")
    try:
        import tkinter
        from unittest.mock import patch
        import socket
        from nlp_engine import LocalNLP

        print(f"Tkinter: available (Tk {tkinter.TkVersion})")
        engine = LocalNLP()
        paragraph = "Apple opened an office in London. The excellent new office will welcome engineers."
        jobs = [
            ("Sentiment", engine.sentiment_analysis, ("I love this excellent app!",)),
            ("Entities / English model", engine.do_ner, ("Barack Obama visited London.",)),
            ("Summary", engine.do_summarize, (paragraph, 1)),
            ("Spelling and basic grammar", engine.do_grammer_spelling, ("i is happy with teh speling.",)),
            ("Language detection", engine.do_lang_detect, ("This is a longer English sentence about a computer application.",)),
            ("Headline", engine.do_headline_generation, (paragraph,)),
        ]
        with patch.object(socket.socket, "connect", side_effect=RuntimeError("Network blocked during verification")), patch("socket.create_connection", side_effect=RuntimeError("Network blocked during verification")):
            for label, function, arguments in jobs:
                if not function(*arguments):
                    raise ValueError(f"{label} returned an empty result for the sample.")
                print(f"PASS: {label}")
    except Exception as exc:
        print(f"FAILED: {exc}")
        print("Run setup.bat, or install requirements-model.txt with this project's .venv Python.")
        return 1
    print("Ready for a demo. No network connections were allowed during these checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
