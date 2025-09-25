
"""
pipeline_spacy.py
A tiny CLI to run the same analysis from the notebook on a text file.
Usage:
    python pipeline_spacy.py --in sample_text.txt --out outputs --model en_core_web_sm
"""
import argparse, sys, subprocess
from pathlib import Path

def ensure_spacy_model(model_name: str = "en_core_web_sm"):
    try:
        import spacy
        spacy.load(model_name)
        return model_name
    except Exception:
        print(f"Downloading spaCy model: {model_name} ...")
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=False)
        import spacy as _sp
        _sp.load(model_name)
        return model_name

def analyze_to_csv(text: str, out_dir: Path, model_name: str):
    import spacy, pandas as pd
    nlp = spacy.load(model_name)
    doc = nlp(text)

    tokens = []
    for t in doc:
        if t.is_space or t.is_punct:
            continue
        tokens.append({"text": t.text, "pos": t.pos_, "lemma": t.lemma_, "dep": t.dep_, "head": t.head.text})

    ents = [{"text": e.text, "label": e.label_, "start": e.start_char, "end": e.end_char} for e in doc.ents]
    deps = [{"text": t.text, "pos": t.pos_, "dep": t.dep_, "head": t.head.text, "head_pos": t.head.pos_} for t in doc]
    chunks = [{"chunk": c.text, "root": c.root.text, "root_dep": c.root.dep_} for c in doc.noun_chunks]

    out_dir.mkdir(exist_ok=True, parents=True)
    import pandas as pd
    pd.DataFrame(tokens).to_csv(out_dir / "cli_tokens.csv", index=False)
    pd.DataFrame(ents).to_csv(out_dir / "cli_entities.csv", index=False)
    pd.DataFrame(deps).to_csv(out_dir / "cli_dependencies.csv", index=False)
    pd.DataFrame(chunks).to_csv(out_dir / "cli_noun_chunks.csv", index=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", type=str, required=True, help="Path to a .txt file")
    ap.add_argument("--out", dest="outdir", type=str, default="outputs", help="Where to write CSVs")
    ap.add_argument("--model", dest="model", type=str, default="en_core_web_sm", help="spaCy model to load")
    args = ap.parse_args()

    infile = Path(args.infile)
    if not infile.exists():
        print(f"Input file not found: {infile}", file=sys.stderr)
        sys.exit(2)

    model = ensure_spacy_model(args.model)
    text = infile.read_text(encoding="utf-8")
    analyze_to_csv(text, Path(args.outdir), model)
    print("Done. CSVs written to", args.outdir)

if __name__ == "__main__":
    main()
