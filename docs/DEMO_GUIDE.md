# College demo and viva guide

## Before you go

- Prepare the actual laptop you will present from. Install Python 3.12 and Git, clone the repository, and run `setup.bat` with internet access.
- From the project folder, run `.venv\Scripts\python.exe scripts\verify_setup.py` and `.venv\Scripts\python.exe -m unittest discover -s tests -v`.
- Launch `run.bat`, choose guest mode, and try all six tools with the files in `demo/` while Wi-Fi is disconnected.
- Keep `output/pdf/NLPApp-Mini-Project-Report.pdf` available locally. Add your college's required cover sheet/team details separately.
- Check screen readability and your output-save location. Allow the first model load to finish.
- A source ZIP does not contain installed dependencies. Do not leave setup until the viva.

## Five-minute presentation

**Opening, 30 seconds.** "Our mini project is NLPApp, a Python desktop workspace for six NLP tasks. We replaced the earlier cloud integration with local components, so analysis runs without API keys or internet after setup."

**Architecture, 45 seconds.** Explain `app.py` for the UI, `nlp_engine.py` for analysis, and `mydb.py` for optional accounts. Describe validation, one background worker, main-thread display, and copy/save. Guest mode makes the demo independent of old account data.

**Feature demonstration, 2-3 minutes.** Select each tool and load its sample:

| Tool | File | Explain |
| --- | --- | --- |
| Sentiment | `demo/sentiment.txt` | Expect a positive label. Proportions are not confidence. |
| Entities | `demo/entities.txt` | Show person/location/date predictions; try `PERSON` as a filter. |
| Summary | `demo/article.txt` | Request 2 sentences; compare with the source. |
| Spelling | `demo/spelling.txt` | Review changes such as `i is` to `I am` and `teh` to `the`. |
| Language | `demo/language.txt` | `en` indicates English; longer passages are more reliable. |
| Headline | `demo/article.txt` | A key sentence is shortened to at most 12 words. Copy or save it. |

**Verification, 30 seconds.** Explain that 17 test methods passed locally, including all six tools offline and 12 targeted quality regressions. Show verification on your destination laptop. Do not describe functional tests as an accuracy benchmark.

**Closing, 30 seconds.** "The project demonstrates local NLP integration, desktop programming, validation, hashed accounts, tests and GitHub distribution. Future work includes evaluation, multilingual support and a packaged installer."

## Common viva questions

**What is NLP?** Computational methods for human language, such as sentiment detection, finding entities and extracting summaries.

**What did you build versus reuse?** We built the UI/workflow, module integration, validation, account management, frequency-based ranking, headline logic, basic grammar rules and verification. VADER, spaCy, langdetect and SymSpell provide existing resources and algorithms.

**Did you train a model?** No. We use pretrained/library resources. We should not claim new training or an unmeasured accuracy score.

**How does the summary work?** Use spaCy sentence boundaries and lemmas, build normalized TF-IDF vectors, score similarity to the document centroid, remove duplicates and penalize overlap with already-selected sentences. Restore source order afterward.

**Is it TextRank?** No. It is a custom word-frequency baseline, not graph ranking.

**What is an entity?** A text span predicted to represent a person, place, organization, date or another category. A prediction is not factual verification.

**What does sentiment mean here?** VADER produces a compound score from -1 to +1. Thresholds are >= 0.05 positive, <= -0.05 negative, otherwise neutral. A separate sentence-level rule can identify mixed opinions; category proportions are not confidence estimates.

**Why not a large local LLM?** This version favors smaller task-specific components. A larger model would need separate quality, storage, RAM and latency evaluation.

**Why a thread?** Analysis on Tkinter's event loop could freeze the window. A worker runs analysis while the main thread displays results.

**How are passwords stored?** Salted PBKDF2-HMAC-SHA256 hashes with 600,000 iterations. Emails/names remain readable. Profiles do not protect against someone who controls the computer.

**Why is my account missing after cloning?** Local `db.json` is ignored by Git. Use guest mode or register a new local profile.

**Is it offline?** Analysis is offline after the dependencies/model are installed on that computer. Cloning and first installation need internet.

**What are the limits?** Mostly English analysis, errors with sarcasm/unfamiliar text, basic sentence splitting and grammar rules, extractive output and no corpus benchmark.

## If a demo fails

Read the README's Troubleshooting section. Use guest mode for account problems. Missing libraries/model require setup using a permitted internet connection. Do not claim that source code alone can install an absent model offline. Keep the PDF and samples for presentation support, and distinguish documentation from a successful live run.
