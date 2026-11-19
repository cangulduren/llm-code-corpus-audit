import numpy as np
from scipy import stats

def clopper_pearson(k, n, alpha=0.05):
    """Exact Clopper-Pearson confidence interval for a binomial proportion."""
    low = 0.0 if k == 0 else stats.beta.ppf(alpha / 2, k, n - k + 1)
    high = 1.0 if k == n else stats.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return low, high

print("="*70)
print("EXACT CLOPPER-PEARSON CONFIDENCE INTERVALS & RULE-OF-THREE BOUNDS")
print("="*70)

# Random unflagged sample: n = 150, k = 0 misses
n_rand = 150
k_rand = 0
low_r, high_r = clopper_pearson(k_rand, n_rand)
print(f"1. Random Unflagged Sample (n = {n_rand}, k = {k_rand} misses):")
print(f"   * Point estimate of miss rate: {k_rand/n_rand:.2%}")
print(f"   * Exact 95% Clopper-Pearson CI: [{low_r:.4%}, {high_r:.4%}]")
print(f"   * Rule-of-Three upper bound (3/n): {3/n_rand:.2%}")
print(f"   * Population recall lower bound: {100 - high_r*100:.2f}%")

# Combined unflagged sample: n = 300, k = 0 misses (for CWE-676, CWE-703, CWE-617, CWE-78)
n_tot = 300
k_tot = 0
low_t, high_t = clopper_pearson(k_tot, n_tot)
print(f"\n2. Combined Unflagged Sample (n = {n_tot}, k = {k_tot} misses):")
print(f"   * Point estimate of miss rate: {k_tot/n_tot:.2%}")
print(f"   * Exact 95% Clopper-Pearson CI: [{low_t:.4%}, {high_t:.4%}]")
print(f"   * Rule-of-Three upper bound (3/n): {3/n_tot:.2%}")
print(f"   * Population recall lower bound: {100 - high_t*100:.2f}%")

# CWE-400 enriched stratum: n = 150, k = 1 miss
n_enr = 150
k_enr = 1
low_e, high_e = clopper_pearson(k_enr, n_enr)
print(f"\n3. CWE-400 Enriched Stratum (n = {n_enr}, k = {k_enr} miss):")
print(f"   * Point estimate of miss rate: {k_enr/n_enr:.2%}")
print(f"   * Exact 95% Clopper-Pearson CI: [{low_e:.4%}, {high_e:.4%}]")
