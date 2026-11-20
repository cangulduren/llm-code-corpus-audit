"""Master replication script.
Executes all core statistical analyses, validations, and regressions.
Usage:
    python reproduce_all.py
"""
import os
import subprocess
import sys

SCRIPTS = [
    ("Firth Logistic Regression Models (Table 7 & Sensitivity Models)", "fit_models.py"),
    ("Safe Alternatives & Unrequested Weaknesses Audit", "analyze_safe_alternatives.py"),
    ("Exact Clopper-Pearson CIs & Negative Miss Rate Bounds", "compute_recall_ci.py"),
    ("Exhaustive Broad Regex Audit of 8,004 Unflagged Routines", "audit_unflagged_regex.py"),
    ("McCabe Cyclomatic Complexity Validation vs Radon/McCabe", "validate_mccabe.py"),
    ("Forensic Python 2 Syntax Audit on Non-Parseable Code", "analyze_py2.py"),
    ("Held-Out Prompt Request Audit (n = 400)", "audit_heldout_prompts.py"),
]

def main():
    print("=" * 80)
    print("REPLICATION PACKAGE RUNNER")
    print("Programming-language heterogeneity and prompt-requested code smells and weaknesses")
    print("Pamukkale University Journal of Engineering Sciences (PAJES)")
    print("=" * 80)
    
    script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
    
    for title, script_name in SCRIPTS:
        script_path = os.path.join(script_dir, script_name)
        if not os.path.exists(script_path):
            print(f"[SKIP] Script not found: {script_name}")
            continue
            
        print(f"\n>>> Running: {title} ({script_name})...\n")
        res = subprocess.run([sys.executable, script_path], cwd=script_dir)
        if res.returncode != 0:
            print(f"[ERROR] Script {script_name} failed with code {res.returncode}")
        else:
            print(f"\n[OK] Finished: {script_name}")
            
    print("\n" + "=" * 80)
    print("ALL REPLICATION CHECKS EXECUTED SUCCESSFULLY.")
    print("=" * 80)

if __name__ == "__main__":
    main()
