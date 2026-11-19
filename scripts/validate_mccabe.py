import os
import ast
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "processed", "valid_analyzed_dataset.csv")

class McCabeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.complexity += 1
        self.generic_visit(node)

def calc_cc(code):
    try:
        tree = ast.parse(code)
        v = McCabeVisitor()
        v.visit(tree)
        return v.complexity
    except Exception:
        return np.nan

df = pd.read_csv(DATA_PATH)
sample = df[df["analysis_set"] == 1].sample(1000, random_state=42)

calc_vals = np.array([calc_cc(c) for c in sample["code"]])
stored_vals = sample["cyclomatic_complexity"].values

valid = ~np.isnan(calc_vals)
diff = calc_vals[valid] - stored_vals[valid]

print("="*70)
print(f"VALIDATION OF AST CC IMPLEMENTATION VS STANDARD MCCABE (n = {valid.sum()})")
print("="*70)
print(f"Exact match rate: {(diff == 0).sum()} / {len(diff)} ({(diff == 0).mean():.2%})")
print(f"Pearson correlation coefficient: {np.corrcoef(calc_vals[valid], stored_vals[valid])[0, 1]:.6f}")
print(f"Mean absolute difference: {np.abs(diff).mean():.4f}")
print(f"Max absolute difference: {np.max(np.abs(diff))}")
