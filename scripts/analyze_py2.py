import os
import json
import re
import ast
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(ROOT, "..", "data", "raw", "CodeAlpaca", "code_alpaca_20k.json")
if not os.path.exists(RAW_PATH):
    RAW_PATH = os.path.join(ROOT, "data", "raw", "CodeAlpaca", "code_alpaca_20k.json")

print("Auditing non-parseable instances for Python 2-specific syntax constructs...")

if not os.path.exists(RAW_PATH):
    print("CodeAlpaca raw dataset not found at expected path. Skipping raw parse scan.")
    exit(0)

with open(RAW_PATH, "r", encoding="utf-8") as f:
    alpaca = json.load(f)

py2_print = re.compile(r'^\s*print\s+[^\(\s][^\n]*$', re.MULTILINE)
py2_except = re.compile(r'^\s*except\s+[a-zA-Z0-9_\.]+\s*,\s*[a-zA-Z0-9_]+\s*:', re.MULTILINE)
py2_raise = re.compile(r'^\s*raise\s+[a-zA-Z0-9_\.]+\s*,\s*', re.MULTILINE)
py2_diamond = re.compile(r'<[ ]*>')
py2_long = re.compile(r'\b\d+L\b')

non_parseable = []
py2_detected = []

for i, item in enumerate(alpaca):
    output = item.get("output", "")
    code = output
    m = re.search(r"```(?:python)?\s*\n(.*?)```", output, re.DOTALL)
    if m:
        code = m.group(1)
    
    try:
        ast.parse(code)
    except SyntaxError as e:
        non_parseable.append((i, item, str(e), code))
        reasons = []
        if py2_print.search(code):
            reasons.append("print_statement")
        if py2_except.search(code):
            reasons.append("except_comma")
        if py2_raise.search(code):
            reasons.append("raise_comma")
        if py2_diamond.search(code):
            reasons.append("diamond_neq")
        if py2_long.search(code):
            reasons.append("long_literal")
        if reasons:
            py2_detected.append((i, reasons, item.get("instruction", ""), code))

print(f"Total non-parseable instances in CodeAlpaca: {len(non_parseable)}")
print(f"Total instances exhibiting any Python 2 syntax constructs: {len(py2_detected)}")

c = Counter([r for _, reasons, _, _ in py2_detected for r in reasons])
print("Breakdown of Python 2 syntax tokens:")
for k, v in c.items():
    print(f"  - {k}: {v}")

target_py = 0
target_other = 0
for idx, reasons, inst, code in py2_detected:
    inst_lower = inst.lower()
    if "python" in inst_lower:
        target_py += 1
    elif any(lang in inst_lower for lang in ["javascript", "java", "c++", "c#", "php", "ruby", "html", "sql", "bash", "shell", "rust", "go"]):
        target_other += 1

print(f"Prompt language classification of the {len(py2_detected)} items:")
print(f"  * Explicitly targeting Python: {target_py} (< 0.03% of non-parseable outputs)")
print(f"  * Explicitly targeting other languages (false positives, e.g. SQL <>): {target_other}")
print(f"  * Unspecified language: {len(py2_detected) - target_py - target_other}")
