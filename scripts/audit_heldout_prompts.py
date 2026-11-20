"""Held-out empirical audit of unflagged CodeAlpaca prompts for construct requests.

Addresses Reviewer 1's request for held-out evaluation of construct requests
among unflagged prompts (lexicon false negatives).
"""
import os
import json
import numpy as np
from scipy import stats
from sklearn.metrics import cohen_kappa_score

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_PATH = os.path.join(ROOT, "data", "annotation", "items_heldout_prompts.jsonl")
ANN1_PATH = os.path.join(ROOT, "data", "annotation", "labels_annotator1_heldout.jsonl")
ANN2_PATH = os.path.join(ROOT, "data", "annotation", "labels_annotator2_heldout.jsonl")
FINAL_PATH = os.path.join(ROOT, "data", "annotation", "final_labels_heldout.jsonl")

def clopper_pearson(k, n, alpha=0.05):
    """Exact Clopper-Pearson confidence interval for a binomial proportion."""
    low = 0.0 if k == 0 else stats.beta.ppf(alpha / 2, k, n - k + 1)
    high = 1.0 if k == n else stats.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return low, high

def main():
    print("=" * 70)
    print("HELD-OUT AUDIT OF UNFLAGGED PROMPTS FOR CONSTRUCT REQUESTS")
    print("=" * 70)

    with open(ITEMS_PATH, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f]
    with open(ANN1_PATH, "r", encoding="utf-8") as f:
        ann1 = [json.loads(line) for line in f]
    with open(ANN2_PATH, "r", encoding="utf-8") as f:
        ann2 = [json.loads(line) for line in f]
    with open(FINAL_PATH, "r", encoding="utf-8") as f:
        final = [json.loads(line) for line in f]

    n = len(items)
    y1 = [x["requested"] for x in ann1]
    y2 = [x["requested"] for x in ann2]
    yf = [x["requested"] for x in final]

    k = sum(yf)
    agree = sum(a == b for a, b in zip(y1, y2)) / n
    kappa = cohen_kappa_score(y1, y2) if len(set(y1 + y2)) > 1 else 1.0
    low, high = clopper_pearson(k, n)
    rule_of_three = 3.0 / n

    print(f"Sample size: n = {n} randomly drawn from 7,929 unflagged prompts (seed: 42)")
    print(f"Annotator 1 requests identified: {sum(y1)}")
    print(f"Annotator 2 requests identified: {sum(y2)}")
    print(f"Annotator raw agreement: {agree:.1%}")
    print(f"Cohen's kappa: κ = {kappa:.4f}")
    print(f"Adjudicated construct requests: {k} / {n} ({k / n:.2%})")
    print(f"Exact 95% Clopper-Pearson CI: [{low:.4%}, {high:.4%}] (upper bound: {high * 100:.2f}%)")
    print(f"Rule-of-Three upper bound (3/n): {rule_of_three:.2%}")
    print(f"Lexicon Negative Predictive Value (NPV) on unflagged prompts: >= {(1.0 - high) * 100:.2f}%")
    print("=" * 70)

if __name__ == "__main__":
    main()
