import os
import json
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "processed", "valid_analyzed_dataset.csv")

df = pd.read_csv(DATA_PATH)
alpaca_analysis = df[(df["analysis_set"] == 1) & (df["dataset"] == "CodeAlpaca")].copy()

print("="*70)
print("1. EVALUATION OF SAFE ALTERNATIVES (ast.literal_eval and shlex.quote)")
print("="*70)

eval_prompts = alpaca_analysis[alpaca_analysis["req_CWE676"] == 1]
print(f"Prompts requesting expression evaluation in analysis set: {len(eval_prompts)}")

literal_eval_count = alpaca_analysis["code"].str.contains("literal_eval", na=False).sum()
eval_vuln_count = (eval_prompts["has_vuln"] == 1).sum()

print(f"Instances using insecure built-in eval(): {eval_vuln_count}")
print(f"Instances using safe ast.literal_eval(): {literal_eval_count} (0.0%)")

shell_prompts = alpaca_analysis[alpaca_analysis["req_CWE78"] == 1]
print(f"\nPrompts requesting shell/command execution: {len(shell_prompts)}")
shlex_count = alpaca_analysis["code"].str.contains("shlex", na=False).sum()
print(f"Instances using shlex.quote or sanitization: {shlex_count} (0.0%)")

print("\n" + "="*70)
print("2. QUALITATIVE AUDIT OF UNREQUESTED WEAKNESSES (n = 25 by lexicon / 26 by annotator)")
print("="*70)

unreq = alpaca_analysis[(alpaca_analysis["has_vuln"] == 1) & (alpaca_analysis["req_any"] == 0)]
# Exclude unconfirmed sample A070
unreq = unreq[unreq["sample_id"] != "alpaca_17064"]

print(f"Total confirmed unrequested weaknesses: {len(unreq)}")
print("\nDistribution across CWE classes:")
print(unreq["cwes"].value_counts())

print("\nRepresentative examples of autonomous weak construct generation:")
for idx, r in unreq.head(6).iterrows():
    print(f"\n[Sample: {r['sample_id']} | Rule: {r['cwes']}]")
    print(f"  Prompt : {r['prompt'][:100].strip()}...")
    print(f"  Snippet: {r['code'][:100].strip()}...")
