import numpy as np
from scipy import stats

def fit_firth(X, y, max_iter=100, tol=1e-6):
    """
    Firth penalized logistic regression via Newton-Raphson.
    Reference: Heinze & Schemper (2002), Statistics in Medicine.
    Returns dictionary with coefficients, standard errors, odds ratios, and p-values.
    """
    n, p = X.shape
    beta = np.zeros(p)
    
    for it in range(max_iter):
        eta = np.clip(X @ beta, -30, 30)
        pi = 1.0 / (1.0 + np.exp(-eta))
        w = np.maximum(pi * (1.0 - pi), 1e-12)
        
        # Information matrix I = X^T W X
        XtW = X.T * w
        info = XtW @ X
        
        try:
            info_inv = np.linalg.inv(info)
        except np.linalg.LinAlgError:
            info_inv = np.linalg.pinv(info)
            
        # Hat matrix diagonals h_i
        H_diag = np.sum((X @ info_inv) * (X * w[:, None]), axis=1)
        
        # Modified score: U* = X^T [ y - pi + H_diag * (0.5 - pi) ]
        u_star = X.T @ (y - pi + H_diag * (0.5 - pi))
        delta = info_inv @ u_star
        
        beta_new = beta + delta
        if np.max(np.abs(delta)) < tol:
            beta = beta_new
            break
        beta = beta_new
        
    eta = np.clip(X @ beta, -30, 30)
    pi = 1.0 / (1.0 + np.exp(-eta))
    w = np.maximum(pi * (1.0 - pi), 1e-12)
    info = (X.T * w) @ X
    info_inv = np.linalg.inv(info)
    se = np.sqrt(np.diag(info_inv))
    
    return {
        'beta': beta,
        'se': se,
        'odds_ratio': np.exp(beta),
        'ci_95_lower': np.exp(beta - 1.96 * se),
        'ci_95_upper': np.exp(beta + 1.96 * se),
        'p_value': 2 * (1 - stats.norm.cdf(np.abs(beta / se))),
        'iterations': it
    }
