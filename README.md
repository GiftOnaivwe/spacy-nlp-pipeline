# spacy-nlp-pipeline

A clean, productionâ€‘minded mini NLP pipeline built with **spaCy**

##  Features
- **Reproducible notebook**: modular functions, clear sections, and a self check.
- **CLI utility**: run the pipeline on any `.txt` file and export tidy CSVs.
- **Portfolioâ€‘ready**: consistent structure, outputs folder, and README docs.

## Pipeline Overview
The pipeline uses spaCy to produce four tidy tables:
- **tokens** token, lemma, POS, dependency head, stopword flag
- **entities** entity text, label, start/end offsets
- **dependencies** token dependency relation and head
- **noun_chunks** base noun phrases with root info

By default, the notebook filters to common content POS (`NOUN, PROPN, VERB, ADJ, ADV, NUM`) and lowercases lemmas for normalization. You can tweak this via `PipelineConfig`.

---

## Outputs (example)
After running on `sample_text.txt`, you'll see files like:

```
outputs/
- sample_tokens.csv
- sample_entities.csv
- ample_dependencies.csv
- sample_noun_chunks.csv
```

Inspect in Excel, pandas, or your data viz tool of choice.

---

##  Minimal Testing
The notebook includes a basic smoke test:
```python
assert "tokens" in dfs and not dfs["tokens"].empty
assert len(dfs["dependencies"]) >= len(dfs["tokens"])
```
Add your own checks or migrate to `pytest` for more thorough coverage.

---

**CSV not created**  
Verify write permissions and that `outputs/` exists (the notebook creates it automatically).

---
