# NLPApp — Offline text studio

A Python/Tkinter desktop app for exploring text on your own computer. No API keys, subscriptions, cloud inference, or GPU are needed. Internet is needed only to install the packages and English model once. Analysis runs offline afterward.

## Quick start (Windows, Python 3.10–3.13)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-model.txt
.\.venv\Scripts\python.exe app.py
```

On Linux/macOS, use `.venv/bin/python` instead; Linux may also need its distribution's `python3-tk` package. The current installation in this folder is ready to launch with `.venv\Scripts\python.exe app.py`.

Choose **Continue as guest**, or create a local account. Pick a tool, paste a paragraph or load a UTF-8 `.txt` file, and click **Analyze text**. Copy or save the result. Inputs are limited to 50,000 characters. Text and results are not automatically saved.

## Tools and practical limits

| Tool | Local implementation | What to expect |
| --- | --- | --- |
| Sentiment | VADER | English lexicon/rule scores; sarcasm and domain language can be misread. Scores are not confidence estimates. |
| Named entities | spaCy `en_core_web_sm` | English people, places, organizations and other entity types, with offsets. Optional text or entity-label filter, such as `PERSON`. |
| Summarization | Word-frequency sentence ranking | Extracts 1–10 original sentences in source order. Best with English prose; no rewriting. |
| Spelling & basic grammar | SymSpell bundled dictionary + rules | Corrects some English typos and a few agreement/punctuation mistakes. Preserves capitalized words and contractions. Review suggestions; this is not a full grammar checker. |
| Language detection | langdetect | Language codes with estimated probabilities. At least 10 letters; short or mixed-language text can be unreliable. |
| Headlines | Ranked sentence, capped at 12 words | Extractive title; may need editing and does not generate new facts. |

The local methods are lighter than a large cloud language model and do not promise equivalent accuracy. No model or dictionary is downloaded at runtime. If the entity model is missing, install it with `python -m spacy download en_core_web_sm` inside your virtual environment, then restart the app. See [spaCy's model documentation](https://spacy.io/usage/models).

## Accounts and privacy

Accounts live in `db.json`, beside the app, and are optional. Passwords use salted PBKDF2-HMAC-SHA256 with 600,000 iterations. Existing plaintext records are migrated at startup without changing passwords. Email addresses remain readable locally. This is a local profile system, not a security boundary against someone who controls your computer. Keep a backup of your database if you need your accounts.

`db.json`, virtual environments, IDE files, caches and environment files are excluded from Git. The old project included embedded NLP Cloud credentials and account data: revoke those old keys in NLP Cloud and change any reused passwords. Removing files in a new commit does not remove them from older repository history.

## Development and tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover all six tools with socket connections blocked, input limits, registration, password hashing, legacy migration and damaged database handling. GitHub Actions installs the dependencies/model before running these offline tests.

- `app.py`: Tkinter workspace, optional login, background jobs, import/export.
- `nlp_engine.py`: reusable local analysis engine.
- `api_handling.py`: compatibility import for the old `API` class name; no cloud calls.
- `mydb.py`: validated account storage with atomic writes.
- `requirements-model.txt`: full installation including the local English model.

## GitHub updates

Repository: https://github.com/amaansayed184/Project-2-NLPApp

```powershell
git status
git add app.py nlp_engine.py api_handling.py mydb.py readme.md requirements.txt requirements-model.txt tests .github .gitignore
git commit -m "Improve offline NLP studio"
git push origin master
```

Do not commit local account data or credentials.
