# NLPApp - Offline Text Studio

**College mini project | Python desktop application | Six local NLP tools**

NLPApp lets you analyze text through a Tkinter desktop interface. It replaces the original NLP Cloud integration with local libraries and algorithms. **No API key, paid service, GPU, or internet connection is needed while analyzing text.** Internet is required for the first installation on each computer.

[Project report (PDF)](output/pdf/NLPApp-Mini-Project-Report.pdf) · [Editable report](docs/project-report.md) · [College demo and viva guide](docs/DEMO_GUIDE.md) · [Setup troubleshooting](#troubleshooting)

See [quality improvements and before/after examples](docs/QUALITY_NOTES.md) for the latest local NLP update. Existing installations can pull the changes without downloading a new model.

## What our mini project does

The goal is to bring common natural language processing tasks into one simple, private desktop workspace. Users enter text, select a task, and inspect, copy, or save the output. Accounts are optional: **Continue as guest** gives access to all six tools.

| Feature | How it works | Practical limit |
| --- | --- | --- |
| Sentiment analysis | VADER with sentence-level evidence and a mixed-opinion check | Intended for English; scores are not confidence estimates |
| Named entity recognition | Pretrained local spaCy `en_core_web_sm` model | English entities; predictions can be incorrect |
| Summarization | Lemmatized TF-IDF centroid ranking with duplicate removal and a redundancy penalty | Extracts up to 1-10 unique source sentences; does not rewrite them |
| Spelling & basic grammar | Conservative SymSpell suggestions, common-typo fixes, agreement/contraction rules | Protects URLs, emails, code, paths and numbered tokens; review corrections |
| Language detection | langdetect language profiles with a fixed random seed | At least 10 letters; short or mixed-language text is unreliable |
| Headline generator | Rank sentences, prefer a short complete clause, then cap at 12 words | Avoids trailing function words; still extractive and may need editing |

Other features include multiline input, word/character counts, UTF-8 text-file loading, copy/save results, input validation and background processing. The text limit is 50,000 characters; imported files must be no larger than 200,000 bytes.

## Run it on another laptop: Windows

### 1. Prepare that laptop before college

- Install **64-bit Python 3.12** from [python.org](https://www.python.org/downloads/). Include **pip**, **Tcl/Tk**, and the Python launcher; select **Add Python to PATH** if offered. Python 3.10-3.13 is supported by the setup helper; 3.12 is recommended for a consistent setup. Avoid using a newer unsupported Python version for this demo.
- Install [Git for Windows](https://git-scm.com/downloads/win).
- Use a normal writable folder, such as Documents, and have internet available during setup. A standard CPU is sufficient; no GPU is required. Allow space for Python, the virtual environment, and downloaded packages. The project has not been benchmarked for a minimum RAM specification.
- You do **not** need VS Code, a GitHub login for a public clone, API keys, an `.env` file, a database server, or a paid account.

Open **PowerShell** in the folder where you want the project:

```powershell
git clone https://github.com/amaansayed184/Project-2-NLPApp.git
cd Project-2-NLPApp
.\setup.bat
```

The setup helper creates `.venv`, installs `requirements-model.txt` including the English entity model, and checks all six tools with networking blocked. Wait for **Setup complete**. Run this once on the laptop you will actually use in college.

If Git is unavailable, select **Code > Download ZIP** on GitHub, extract the ZIP fully, open the extracted project folder, and double-click `setup.bat`. Do not run scripts from inside the ZIP preview.

### 2. Launch the app

Double-click **`run.bat`**, or run:

```powershell
.\run.bat
```

Choose **Continue as guest**, select a tool, load one of the files in `demo/`, and click **Analyze text**. Results can be copied or saved as `.txt`.

### 3. Check the installation before leaving

From the project folder, run:

```powershell
.\.venv\Scripts\python.exe scripts\verify_setup.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Confirm the setup check reports all six tools as **PASS** and the tests end with **OK**. Then disconnect Wi-Fi, open `run.bat`, and manually try all six tools. This checks the actual laptop and its graphical environment. Setup verification checks Tkinter availability but does not open a window.

**Important:** cloning downloads the source, not Python, the libraries, or the model. Your current laptop's `.venv` and accounts are intentionally excluded from Git. **Do not copy `.venv` between computers; recreate it using setup on the new computer.** If the college laptop has no internet, complete installation on that same laptop beforehand, or arrange internet for the initial installation. A source ZIP alone is not a complete offline installer.

### Manual setup if you prefer commands

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-model.txt
.\.venv\Scripts\python.exe scripts\verify_setup.py
.\.venv\Scripts\python.exe app.py
```

These commands use the virtual environment's interpreter directly. You do not need to activate it or change PowerShell's execution policy.

## macOS and Linux

Install Git, Python 3.12 with pip/venv, and Tk support. On Debian/Ubuntu, the OS packages are commonly `python3-tk` and `python3-venv`; use the matching Tk package for your Python version. Then:

```bash
git clone https://github.com/amaansayed184/Project-2-NLPApp.git
cd Project-2-NLPApp
python3 --version  # use a supported version; 3.12 is recommended
python3 scripts/setup_project.py
.venv/bin/python scripts/verify_setup.py
.venv/bin/python app.py
```

`setup.bat` and `run.bat` are Windows helpers. macOS/Linux instructions are provided for portability; the desktop smoke test was performed on Windows, not on every operating system.

## Demo in college

1. Start `run.bat` and choose **Continue as guest**.
2. Load `demo/sentiment.txt`; show the positive result. Explain that proportions are not confidence scores.
3. Choose **Named entities**, load `demo/entities.txt`, and run it. Try `PERSON` in the optional filter.
4. Choose **Summarization**, load `demo/article.txt`, and request two sentences. Explain extractive summarization.
5. Choose **Spelling & basic grammar**, load `demo/spelling.txt`, and review the changes.
6. Choose **Language detection**, load `demo/language.txt`, and explain the `en` code.
7. Choose **Headline generator**, load `demo/article.txt`, then copy or save the output.
8. Show that analysis still works with Wi-Fi disconnected after setup.

Read [the demo and viva guide](docs/DEMO_GUIDE.md) for a short presentation script, expected behavior and answers to common questions.

## Architecture and algorithms

```text
Text entry / .txt file
        |
        v
Tkinter interface (app.py) -- optional accounts --> mydb.py --> local db.json
        |
        v
Validate input --> background worker --> LocalNLP (nlp_engine.py)
                                        | VADER
                                        | spaCy English model
                                        | sentence ranking
                                        | SymSpell + grammar rules
                                        | langdetect
        |
        v
Main-thread result display --> Copy / Save .txt
```

The worker executes one analysis job at a time; Tkinter polls for completion on the main thread. Models and dictionaries are loaded lazily and cached in the engine. There are no cloud inference calls or runtime model downloads. `api_handling.py` preserves the old `API` import name as an alias for `LocalNLP`; it no longer contacts an API.

The summarizer uses spaCy sentence boundaries and lemmas, removes stopwords and duplicate sentences, and builds normalized sparse TF-IDF vectors. It scores relevance against the document centroid and greedily selects sentences with a cosine-similarity redundancy penalty, then restores source order. It does not construct an all-pairs similarity matrix. The headline uses the same ranking, prefers a complete short clause, and caps output at 12 words while avoiding trailing function words.

Sentiment now includes sentence-level compound scores and can mark opposing opinions as **Mixed**. Language detection warns about short or ambiguous passages. Entity filters accept readable categories such as `people`, `location` and `company` as well as spaCy labels. No new model training or extra dependency download is needed for these improvements.

The project integrates pretrained/library components; **we have not trained a new NLP model**. See the [report](output/pdf/NLPApp-Mini-Project-Report.pdf) for module design, methodology, test evidence, limitations, and future work.

## Accounts and data

- Accounts are optional and local to each computer. A fresh clone starts without your existing account database. Guest mode needs no registration.
- Passwords use salted PBKDF2-HMAC-SHA256 with 600,000 iterations. Legacy plaintext records are converted on startup while preserving login.
- Email addresses and names remain readable in local `db.json`. Local accounts are profiles, not a security boundary against someone who controls the computer.
- Input text and results are not automatically persisted. Saving a result writes a file only where you choose. Text copied to the clipboard is managed by the operating system.
- `db.json`, `.venv`, IDE settings, caches, and `.env` files are ignored by Git. Do not commit credentials or personal data.
- Earlier repository history contained embedded NLP Cloud keys and account records. Revoke those old keys and change any reused passwords. Removing them from the latest version does not erase older commits.

## Testing and what has been verified

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Seventeen automated test methods cover all six tools offline, input limits, accounts, and targeted NLP regressions. New checks cover duplicate removal, abbreviations/decimals, source-order extraction, complete-clause headlines, mixed opinions, readable entity filters, short-language warnings, common typos, grammar rules and preservation of URLs/emails/code/paths/version numbers. All 17 passed locally. A Windows desktop smoke test also checked the guest workspace, background analysis, result display, and navigation during a running job.

These are functional checks, **not** dataset accuracy benchmarks or proof that every sentence is handled correctly. GitHub Actions is configured to install the libraries/model and run the automated suite on pushes and pull requests. Check the repository's **Actions** tab for the status of an individual run.

The setup helper was also tested in a separate clean project copy using **Python 3.12.0 on Windows**. It created a new virtual environment, installed dependencies/model, and passed all six offline verification jobs and the original five tests. The current suite contains 17 tests. Still run the checks on your actual college laptop.

## Project structure

```text
Project-2-NLPApp/
  app.py                         Desktop interface and background jobs
  nlp_engine.py                  Six local NLP implementations
  api_handling.py                Compatibility alias; no cloud calls
  mydb.py                        Local account validation and hashed storage
  requirements.txt               NLP library dependencies
  requirements-model.txt         Libraries plus the English spaCy model
  setup.bat                      One-time Windows setup
  run.bat                        Windows launcher
  scripts/setup_project.py       Cross-platform setup implementation
  scripts/verify_setup.py        Check all six tools without networking
  scripts/build_report.py        Rebuild PDF (optional authoring dependencies)
  demo/                          Text samples for the college demo
  tests/test_offline.py          Functional and account tests
  tests/test_quality.py          Targeted NLP quality regressions
  docs/project-report.md         Editable report source
  docs/DEMO_GUIDE.md             Presentation, checklist and viva questions
  output/pdf/                    Ready-to-read project report
  .github/workflows/tests.yml    Automated test workflow
```

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `python` or `py` is not recognized / opens the Store | Install 64-bit Python 3.12 from python.org with the launcher and PATH option; reopen PowerShell. Use `py -3.12` in manual commands. |
| Unsupported Python version or packages try to compile | Use Python 3.12. If an old `.venv` was created with another Python, rename it as a backup and rerun setup. Do not delete `db.json`. |
| Setup has a network, proxy, certificate, or GitHub download error | Internet is needed for first installation, including the model hosted on GitHub. Use a working permitted connection or ask the lab administrator; rerun setup. Do not disable certificate checks. |
| `No module named ...` | Run `setup.bat`; launch with `run.bat` or `.venv\Scripts\python.exe`, not a different global interpreter. |
| English model is missing / spaCy E050 | Run `.\.venv\Scripts\python.exe -m pip install -r requirements-model.txt`, then restart the app. |
| Tkinter / Tcl/Tk error | Modify the Python installation and enable Tcl/Tk. On Linux, install the matching Tk package. Use a graphical desktop session. |
| PowerShell blocks activation scripts | No activation is required. Use the exact `.venv\Scripts\python.exe` commands shown above. |
| App closes immediately | Run `.\run.bat` from PowerShell to read the error, then rerun setup and verification. |
| Cannot save accounts or results | Extract the project to a writable local folder. Avoid running inside a ZIP or a restricted system folder. |
| Cannot sign in on the new laptop | Accounts do not travel through GitHub. Use guest mode or register a new local account. |
| Short text gives a strange language result | Use a full paragraph with at least 10 letters; mixed-language estimates may be unreliable. |
| Corrupt `db.json` | Keep a backup. Close the app and restore a known-good copy, or rename the damaged file and restart to begin without accounts. |

## Updating a clone later

```powershell
git status
git pull --ff-only origin master
.\setup.bat
.\run.bat
```

Run `git status` first. If you have local source changes, commit or back them up before pulling; do not discard them. Setup is safe to rerun and does not remove your local account database. A new dependency version may require internet again.

To contribute your own changes, use a branch and review the files before committing. Only maintainers need permission to push; classmates can clone a public repository without push access.

## Report, references and scope

The [PDF report](output/pdf/NLPApp-Mini-Project-Report.pdf) and [editable source](docs/project-report.md) explain the implemented system. Add your college's required cover sheet, student names, roll numbers, guide details and signatures separately; these have not been invented. No dataset benchmark, survey result or model-training result is claimed.

Primary library references: [VADER](https://github.com/cjhutto/vaderSentiment), [spaCy models](https://spacy.io/usage/models), [SymSpellPy](https://symspellpy.readthedocs.io/en/latest/examples/lookup.html), [langdetect](https://pypi.org/project/langdetect/).

To regenerate the PDF, install `reportlab` in an authoring environment and run `python scripts/build_report.py`. Report-generation packages are not required to run the NLP application.
