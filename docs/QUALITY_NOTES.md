# Local NLP quality update

This update improves the processing pipeline while keeping the same local libraries/model. It does not train or fine-tune a new model, and requires no new dependency download on an already-configured computer.

## Targeted before/after checks

The following hand-selected regressions were run against the previous engine from commit `36b7603` and the updated engine. The previous engine failed each stated condition; the updated engine passed each one. These examples guide development and are **not** a representative accuracy benchmark.

| Check | Previous behavior | Updated behavior |
| --- | --- | --- |
| Repeated sentence in a solar-panel passage | Repeated the same sentence in the summary | Emits it once and includes other source content |
| `Teh enviroment is definately improving.` | Left these typos unresolved | `The environment is definitely improving.` |
| `he dont like it.` | Changed `dont` into an unrelated dictionary word | `he doesn't like it.` |
| Email `teh@example.com` and URL ending `/i` | Altered protected technical content | Preserves the email and URL exactly |
| Laboratory headline with a long relative clause | Cut the sentence mid-clause | `The college opened a new laboratory` |
| Amazing camera, terrible battery | Collapsed opposing sentences into one overall label | Reports Mixed with sentence-level evidence |
| `location` entity filter for a London passage | Returned no match | Includes London through a readable category alias |

## What changed

- Summary: spaCy parsing and lemmas, normalized TF-IDF centroid relevance, exact duplicate removal and greedy cosine redundancy penalties. Output remains extractive and in source order.
- Headline: prefer a complete short clause and avoid ending a truncated title on function words.
- Spelling: explicit common-typo fixes, conservative one/two-edit dictionary suggestions, ambiguity checks, and protected spans for URLs, emails, code, Windows paths and numbered tokens.
- Grammar: selected apostrophe, pronoun agreement and repeated-function-word rules. Suggestions still require review.
- Sentiment: sentence-level VADER evidence plus a documented heuristic for mixed opinions.
- Language: short/ambiguous passage warnings. Entity filters: readable aliases in addition to model labels.

## Validation

All 17 automated tests passed locally, including 12 new quality tests. A hidden-window smoke check verified that the desktop displays Mixed sentiment and sentence-level evidence. The PDF report and README were updated to describe the implemented algorithms.

Run the suite after installation:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Most tools still assume English. These targeted improvements do not establish performance on arbitrary documents or equivalence to a large language model.
