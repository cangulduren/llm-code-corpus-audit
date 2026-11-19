import os
import json
import numpy as np
import pandas as pd
from firth_regression import fit_firth

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "processed", "valid_analyzed_dataset.csv")
KEY_PATH = os.path.join(ROOT, "data", "annotation", "key.csv")
LABELS_PATH = os.path.join(ROOT, "data", "annotation", "final_labels_A.jsonl")

df = pd.read_csv(DATA_PATH)
key_df = pd.read_csv(KEY_PATH)

with open(LABELS_PATH, "r", encoding="utf-8") as f:
    labels_A = [json.loads(line) for line in f]
labels_df = pd.DataFrame(labels_A)
annotated_A = pd.merge(key_df, labels_df, on="item")

# Filter CodeAlpaca analysis set
alpaca = df[(df["analysis_set"] == 1) & (df["dataset"] == "CodeAlpaca")].copy()
alpaca["intercept"] = 1.0
alpaca["loc_10"] = alpaca["loc"] / 10.0
alpaca["cc"] = alpaca["cyclomatic_complexity"]
alpaca["instruction_words_10"] = alpaca["instruction_words"] / 10.0
alpaca["input_words_10"] = alpaca["input_words"] / 10.0
alpaca["is_script"] = (alpaca["snippet_type"] == "script").astype(float)

# 1. Confirmed outcome (49 events, excluding unconfirmed alpaca_17064)
alpaca["y_confirmed"] = alpaca["has_vuln"].copy()
alpaca.loc[alpaca["sample_id"] == "alpaca_17064", "y_confirmed"] = 0

# 2. Annotator-based request labels
flagged_annotated = annotated_A[annotated_A["stratum"] == "flagged"].set_index("sample_id")
alpaca["req_annotator"] = 0.0
for sid, row in flagged_annotated.iterrows():
    if row.get("requested") == 1:
        alpaca.loc[alpaca["sample_id"] == sid, "req_annotator"] = 1.0

# 3. Plausible weakness outcome (n = 41 events)
alpaca["y_plausible"] = 0.0
for sid, row in flagged_annotated.iterrows():
    if row.get("relevant") == 1:
        alpaca.loc[alpaca["sample_id"] == sid, "y_plausible"] = 1.0

# 4. Security-relevant hazard subset (CWE-676, CWE-78; 20 events)
alpaca["y_security"] = 0.0
for idx, row in alpaca.iterrows():
    c = str(row["cwes"])
    if ("CWE-676" in c or "CWE-78" in c) and row["y_confirmed"] == 1:
        alpaca.loc[idx, "y_security"] = 1.0

# 5. Reliability smell subset (CWE-703, CWE-400, CWE-617; 30 events)
alpaca["y_reliability"] = 0.0
for idx, row in alpaca.iterrows():
    c = str(row["cwes"])
    if any(k in c for k in ["CWE-703", "CWE-400", "CWE-617"]) and row["y_confirmed"] == 1:
        alpaca.loc[idx, "y_reliability"] = 1.0

def report(name, y_col, req_col):
    preds = ["intercept", "loc_10", "cc", "instruction_words_10", "input_words_10", req_col, "is_script"]
    X = alpaca[preds].values
    y = alpaca[y_col].values
    res = fit_firth(X, y)
    print(f"\n{'='*70}")
    print(f"MODEL: {name} (Outcome: {y_col}, Events: {int(y.sum())}/{len(y)})")
    print(f"{'='*70}")
    print(f"{'Predictor':24s} {'Coef':>8s} {'SE':>8s} {'OR':>10s} {'95% CI':>20s} {'p-value':>10s}")
    for p_name, b, s, odds, low, high, p in zip(
        preds, res["beta"], res["se"], res["odds_ratio"], res["ci_95_lower"], res["ci_95_upper"], res["p_value"]
    ):
        ci = f"[{low:.2f}, {high:.2f}]"
        print(f"{p_name:24s} {b:8.4f} {s:8.4f} {odds:10.2f} {ci:>20s} {p:10.4g}")

if __name__ == "__main__":
    report("Table 7 Primary Model (Confirmed 49 events, Lexicon request)", "y_confirmed", "req_any")
    report("Model with Blind Annotators' Request Labels", "y_confirmed", "req_annotator")
    report("Model with 'Plausible Weakness' Outcome (41 events)", "y_plausible", "req_any")
    report("Security-Relevant Sub-model (CWE-676, CWE-78; 20 events)", "y_security", "req_any")
    report("Reliability-Smell Sub-model (CWE-703, 400, 617; 30 events)", "y_reliability", "req_any")
