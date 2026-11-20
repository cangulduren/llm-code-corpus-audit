# Replication Package: Programming-Language Heterogeneity and Prompt-Requested Code Smells and Weaknesses in LLM Code Corpora

This repository contains the complete replication package for the empirical study:
> **"Programming-language heterogeneity and prompt-requested code smells and weaknesses in two large language model code corpora: A validated static audit of MBPP and CodeAlpaca"**  
> *Pamukkale University Journal of Engineering Sciences (PAJES)*  
> Manuscript ID: 2039152 (Major Revision)

---

## 1. Overview & Data Availability

* **Double-Anonymous Peer-Review Access:** An anonymised mirror of this repository is hosted at:  
  `https://anonymous.4open.science/r/llm-code-corpus-audit-DC03/`
* **Archival Deposit:** A permanent archival DOI (Zenodo) will be established upon completion of peer review and acceptance to preserve double-blind integrity.
* **Contents:**
  * Complete AST parsing, structural metric extraction, and detection rules for 5 CWE-mapped patterns.
  * Targeted *post hoc* request lexicon specifications.
  * Expert annotation codebook (`codebook.md`), sample definitions, random seeds, and strata sizes.
  * Raw independent labels from two blind annotators (`labels_annotator1_*`, `labels_annotator2_*`), adjudication logs (`adjudication.jsonl`), and consolidated final labels (`final_labels_*`).
  * Firth-penalised logistic regression implementations and all estimated models.
  * All 10 data tables (CSV) reported in the paper and supplementary materials.

---

## 2. Directory Structure

```
replication_package/
├── README.md                          # This documentation file
├── requirements.txt                   # Python package dependencies
├── reproduce_all.py                   # Master replication script (runs all checks)
├── data/
│   ├── annotation/
│   │   ├── codebook.md                # Annotation codebook for Tasks A, B, and C
│   │   ├── _frozen_manifest.json      # SHA-256 integrity hashes for annotation items
│   │   ├── key.csv                    # Sampling strata, item mappings, and seeds
│   │   ├── items_A.jsonl              # 350 items evaluated in Task A (Weakness patterns)
│   │   ├── items_B.jsonl              # 150 items evaluated in Task B (Parseable output typing)
│   │   ├── items_C.jsonl              # 200 items evaluated in Task C (Non-parseable taxonomy)
│   │   ├── labels_annotator1_A.jsonl  # Annotator 1 raw labels for Task A
│   │   ├── labels_annotator1_B.jsonl  # Annotator 1 raw labels for Task B
│   │   ├── labels_annotator1_C.jsonl  # Annotator 1 raw labels for Task C
│   │   ├── labels_annotator2_A.jsonl  # Annotator 2 raw labels for Task A
│   │   ├── labels_annotator2_B.jsonl  # Annotator 2 raw labels for Task B
│   │   ├── labels_annotator2_C.jsonl  # Annotator 2 raw labels for Task C
│   │   ├── adjudication.jsonl         # Adjudication notes for the 15 disagreeing fields
│   │   ├── disagreements.jsonl        # Log of initial disagreements
│   │   ├── final_labels_A.jsonl       # Adjudicated gold standard labels for Task A
│   │   ├── final_labels_B.jsonl       # Adjudicated gold standard labels for Task B
│   │   └── final_labels_C.jsonl       # Adjudicated gold standard labels for Task C
│   └── processed/
│       ├── valid_analyzed_dataset.csv # Analyzed corpus (9,953 parseable instances with metrics & flags)
│       ├── bandit_per_sample.csv      # Bandit security tool findings per instance
│       ├── results.json               # Primary machine-readable results single source of truth
│       └── summary_statistics.json    # Corpus-wide descriptive statistics
├── scripts/
│   ├── firth_regression.py            # Heinze & Schemper (2002) Firth penalised logistic regression
│   ├── fit_models.py                  # Primary, sensitivity, and disaggregated Firth models
│   ├── analyze_safe_alternatives.py   # Audit of ast.literal_eval, shlex, and unrequested weaknesses
│   ├── compute_recall_ci.py           # Clopper-Pearson exact CIs and Rule-of-Three bounds
│   ├── audit_unflagged_regex.py       # Exhaustive broad-regex scan of all 8,004 unflagged routines
│   ├── validate_mccabe.py             # Validation of AST CC against standard library mccabe
│   └── analyze_py2.py                 # Forensic Python 2 syntax audit across non-parseable instances
└── tables/
    ├── Table1_Corpus_Composition.csv
    ├── Table2_NonParseable_Taxonomy.csv
    ├── Table3_Structural_Contrasts.csv
    ├── Table4_Rules_Validation_Bandit.csv
    ├── Table5_Annotator_Agreement.csv
    ├── Table6_Prompt_Requests.csv
    ├── Table7_Firth_Models.csv
    ├── Table8_Firth_Bandit_Models.csv
    ├── Supplementary_Holm_Adjusted_Tests.csv
    └── Supplementary_Power_Simulation.csv
```

---

## 3. Installation & Requirements

The scripts require Python 3.10+ (tested on Python 3.14.5 and Python 3.15). Install the required scientific packages:

```bash
pip install -r requirements.txt
```

Core dependencies:
* `numpy`
* `scipy`
* `pandas`
* `statsmodels`
* `scikit-learn`

---

## 4. One-Click Reproduction

To run all statistical regressions, sensitivity models, recall bounds, and validation checks in a single run:

```bash
python reproduce_all.py
```

### Individual Replication Commands:

1. **Firth Penalised Logistic Regression (Table 7 & Sensitivity Models):**
   ```bash
   python scripts/fit_models.py
   ```
   *Estimates:*
   * Primary model (Confirmed 49 events): $\text{OR}_{\text{req}} = 74.22$, $p = 1.15 \times 10^{-45}$, $\text{OR}_{\text{LoC}} = 1.47$ (95% CI [0.91, 2.36], $p = 0.117$).
   * Model with blind annotators' request labels: demonstrates quasi-complete separation ($Q=1 \implies Y=1$) due to Stratum A restriction.
   * Model with expert-annotated "plausible weakness" outcome ($n = 41$): $\text{OR}_{\text{req}} = 55.32$, $p = 7.02 \times 10^{-34}$, $\text{OR}_{\text{LoC}} = 1.57$ ($p = 0.037$).
   * Disaggregated security-relevant subset (CWE-676, CWE-78; 20 events): $\text{OR}_{\text{req}} = 143.27$, $p = 4.88 \times 10^{-25}$.
   * Disaggregated reliability smell subset (CWE-703, CWE-400, CWE-617; 30 events): $\text{OR}_{\text{req}} = 46.16$, $p = 4.14 \times 10^{-24}$.
   * Cleaned lexicon model ($n = 96$ requests): $\text{OR}_{\text{req}} = 86.74$, $p = 2.45 \times 10^{-46}$, $\text{OR}_{\text{LoC}} = 1.46$ (95% CI [0.89, 2.39], $p = 0.132$), $\text{OR}_{\text{CC}} = 0.87$ [0.70, 1.10], $p = 0.251$.

2. **Safe Alternatives and Unrequested Weaknesses Analysis:**
   ```bash
   python scripts/analyze_safe_alternatives.py
   ```
   *Verifies:*
   * Share of `ast.literal_eval` across all 20,022 CodeAlpaca instances: **0.0%**. In expression evaluation requests, 9 yielded built-in `eval()`, 2 plain arithmetic, and 0 `ast.literal_eval`. For exception requests, 44 of 51 (86.3%) were answered safely.
   * Breakdown of unrequested weaknesses (25 by lexicon: 8 CWE-676, 7 CWE-703, 6 CWE-617, 4 CWE-400; 26 by annotator judgements; 27 when reclassifying prompt false positives).

3. **Recall Estimation and Clopper-Pearson Exact Confidence Intervals:**
   ```bash
   python scripts/compute_recall_ci.py
   python scripts/audit_unflagged_regex.py
   ```
   *Calculates:*
   * 150 random unflagged sample (0 misses): exact 95% Clopper-Pearson upper bound on miss rate = 2.43% (Rule of Three = 2.00%).
   * 300 combined unflagged sample: for CWE-400, 1 miss in 300 gives 0.33% [0.01%, 1.84%]; for other 4 classes, 0 misses gives exact 95% Clopper-Pearson upper bound = 1.22% (Rule of Three = 1.00%).
   * Broad regex audit of all 8,004 unflagged routines: confirmed zero additional omitted instances among the audited syntactic pattern forms upon structural filtering (633 -> 101 candidates, all verified benign); non-constant loop flaws were not screened corpus-wide and remain bounded solely by the negative audit sample (exact Clopper-Pearson 95% upper bound of 1.84% for CWE-400).

4. **AST Cyclomatic Complexity Implementation Validation:**
   ```bash
   python scripts/validate_mccabe.py
   ```
   *Evaluates our AST CC against standard `mccabe` across 1,000 sampled routines:*
   * Exact agreement: **97.00%**.
   * Pearson correlation: **$r = 0.9930$**.
   * Mean absolute difference: **0.033**.

5. **Python 2 Syntax Forensic Audit:**
   ```bash
   python scripts/analyze_py2.py
   ```
   *Audits all 11,043 non-parseable instances under CPython 3.14:*
   * Python 2 tokens observed: 87 instances (< 0.8% of non-parseable; 55 are SQL `<>` inequality false triggers).
   * Explicitly prompting for Python while using Python 2 syntax: **3 instances (< 0.03% of non-parseable outputs)**.

---

## 5. Request Lexicon Formal Specifications

The targeted *post hoc* lexicon applied to prompts matches the following case-insensitive terms and regular expressions:
* **CWE-676:** `eval`, `exec`, `compile`, `__import__`, `evaluate`
* **CWE-703:** `try`, `except`, `catch`, `handle exception`, `error handling`
* **CWE-400:** `infinite`, `forever`, `server`, `loop forever`, `unbounded loop`
* **CWE-617:** `assert`, `assertion`
* **CWE-78:** `os.system`, `subprocess`, `shell`, `command line`, `terminal`

*Performance metrics:*
* Flagged by lexicon as requested across corpus: 125 prompts (24 confirmed weak, 74 safe, 27 natural-language false matches)
* Overall precision for construct requests: **76.8%–78.4%** (96–98/125 true requests)
* Conditional precision on flagged snippets: **91.67%** (22/24)
* Unconditional weakness yield: **17.6%** (22/125)

---

## 6. Ethics & Anonymity Statement

This replication package has been sanitised in strict compliance with double-anonymous peer-review standards. All personal author names, institutional affiliations, contact emails, and ORCID identifiers have been expunged from the code, metadata, and git commit history. The repository can be browsed anonymously via the `anonymous.4open.science` URL provided above.
