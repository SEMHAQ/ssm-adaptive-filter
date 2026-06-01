# Peer Review Report — Methodology Reviewer (R1)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 6

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology

### Reviewer Identity
Prof. Kai Zhang, Professor of Statistical Signal Processing. Expertise in compressed sensing theory, optimization algorithms for sparse recovery, and experimental methodology for computational research.

### Review Focus
Research design rigor, statistical validity, reproducibility of computational experiments, fairness of baseline comparisons, and completeness of experimental reporting. I particularly examine whether statistical claims are supported by adequate power and appropriate tests.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Accept**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
5 — This paper falls squarely within my expertise: sparse recovery algorithms, statistical validation of computational experiments, and methodology for comparing estimation algorithms.

### Summary Assessment
This paper presents a comprehensive evaluation of LISTA for sparse channel estimation, with 13 experiments covering NMSE performance, BER validation, ablation studies, generalization, and hardware complexity. The methodology is generally sound, with notable strengths in the 20-seed ablation with proper statistical testing and the 200-realization BER validation. The mixed-SNR training protocol and cross-table consistency disclosure are commendable.

However, I have identified several methodological concerns: (1) the baseline comparison grid search details are insufficiently reported — the specific validation metric and selection criterion for LMS/NLMS step sizes are not stated; (2) the BER experiment uses 5 seeds but the confidence intervals are computed over seeds, not over realizations, which may underestimate variability; (3) the support recovery analysis (Table 10) uses only 3 seeds instead of the 5 used elsewhere, creating inconsistency; (4) the noise enhancement analysis (Table 11) reverses at SNR=30 dB without adequate explanation. These are addressable issues that do not undermine the core findings.

I recommend Minor Revision. The statistical methodology is substantially improved from what I expect was an earlier round, and the remaining issues are minor.

---

## Strengths

### S1: Exceptional Ablation Study Design
The 20-seed ablation study (Section 4.11, Table 6) with paired t-tests and Cohen's d effect sizes is exemplary. The paper honestly acknowledges that the initial 5-seed ablation (Table 5) produced false negatives due to low statistical power (~15–20% for medium effects). The follow-up with n=20 seeds correctly identifies all three components as significant (p < 0.001). This is a model of how ablation studies should be conducted and reported in deep learning research.

### S2: BER Validation with Adequate Power
The BER experiments (Section 4.10) use 200 channel realizations per SNR point with 5 random seeds, paired t-tests, and explicit p-value reporting. The distinction between "comparable" (QPSK, p > 0.05) and "significantly better" (16-QAM, p < 0.05) is precisely stated. The MMSE comparison (Table 9) provides important context for the ZF-specificity claim.

### S3: Transparent Cross-Table Consistency Disclosure
The authors proactively explain the ~8 dB discrepancy between Table 1 (SNR sweep, −24.25 dB) and Table 3 (channel length, −32.29 dB) at the same nominal configuration (Section 4.3). This transparency is rare and commendable — it clearly explains that different training distributions produce different results, which is an important finding in itself.

### S4: Comprehensive Generalization Testing
The paper tests generalization across three axes: sparsity mismatch (Section 4.6.1), SNR mismatch (Section 4.6.2), and cross-distribution (ITU channels, Section 4.7.2). The channel length divergence at N=256 (Table 3) is honestly reported as a scalability limit.

### S5: Reproducibility Details
Training hyperparameters are fully specified (Section 4.1): Adam optimizer, learning rate 5×10⁻⁴, weight decay 10⁻⁵, cosine annealing, gradient clipping max norm 5.0, batch size 256, 200 epochs. Data generation parameters are clear (10K training, 2K validation, 2K test). This enables reproducibility.

---

## Weaknesses

### W1: Insufficient Baseline Tuning Details
**Problem**: The paper states that baseline hyperparameters are "optimized via grid search on the validation set" (Section 4.1), but does not specify: (a) what validation metric was used for selection (NMSE? BER? something else?), (b) whether the grid search was per-SNR or across all SNRs, (c) the grid search results or convergence behavior. For LMS and NLMS, the step size ranges are given (μ ∈ {0.001, 0.005, 0.01, 0.02, 0.05} for LMS), but the selection criterion is unclear.
**Why it matters**: If baselines are suboptimally tuned, the comparison is unfair. OMP uses "oracle K" which is already favorable, but LMS/NLMS tuning could significantly affect results.
**Suggestion**: Add a supplementary table showing the grid search results for LMS/NLMS step sizes across SNR levels. Specify the selection criterion (e.g., "minimum average NMSE on validation set"). Consider reporting the sensitivity of results to step size choice.
**Severity**: Minor

### W2: Inconsistent Seed Count in Support Recovery Analysis
**Problem**: Table 10 (support recovery) reports results over "200 realizations, 3 seeds," while all other experiments use 5 seeds. The paper does not explain why 3 seeds were used here instead of 5.
**Why it matters**: Inconsistent seed counts across experiments undermine the paper's otherwise rigorous statistical standards. If 3 seeds were used due to computational constraints, this should be stated.
**Suggestion**: Use 5 seeds consistently across all experiments, or explicitly justify the reduced seed count for Table 10.
**Severity**: Minor

### W3: Noise Enhancement Reversal at SNR=30 dB
**Problem**: Table 11 shows LISTA's noise enhancement advantage reverses at SNR=30 dB (LISTA: 25.3 vs OMP: 6.1). The paper explains this occurs because "LISTA's slight support recovery errors (J = 0.93) create occasional spectral nulls" at high SNR. However, this explanation is given without quantitative support — how many nulls? How severe?
**Why it matters**: The reversal undermines the generality of the noise enhancement mechanism. If the advantage is SNR-dependent, this should be clearly stated as a limitation of the BER advantage.
**Suggestion**: Provide additional analysis of the noise enhancement distribution at SNR=30 dB. Show the histogram of 1/|Ĥ(f)|² values for LISTA vs OMP to demonstrate whether the reversal is due to a few extreme values or a systematic shift. If computational resources are limited, at least acknowledge the reversal as a limitation in the Discussion.
**Severity**: Minor

### W4: BER Confidence Interval Computation
**Problem**: The paper states "95% confidence intervals across 5 random seeds" for BER experiments. With n=5 seeds, the t-based confidence interval is very wide (t₀.₀₂₅,₄ = 2.776), which may explain why many LISTA vs OMP comparisons are "not significant." The paper does not report the actual confidence interval widths.
**Why it matters**: With only 5 seeds, the statistical power to detect small BER differences is limited. The "not significant" results for QPSK BER may reflect insufficient power rather than true equivalence.
**Suggestion**: Report the 95% CI widths for key BER comparisons. Consider increasing to 10 seeds if computationally feasible. Alternatively, use equivalence testing (TOST) to demonstrate that LISTA and OMP BER are equivalent within a pre-specified margin, rather than relying on non-significant p-values.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title accurately reflects the paper's scope. "Analysis" is the right framing.
- Abstract is comprehensive but overly long. The statistical details (200 realizations, 5 seeds, p-values) should be in the methods section, not the abstract.

### Methodology / Research Design
- The mixed-SNR training protocol (Section 4.1) is well-designed for producing a single model across conditions.
- The use of BPSK pilot signals (±1) is standard but should be noted as a limitation — real systems use more complex pilot structures.
- The NMSE loss function (Equation 7) with ε = 10⁻¹⁰ is appropriate.

### Data Generation
- The i.i.d. Gaussian tap amplitude model (Section 4.1) is standard for sparse recovery benchmarks.
- The uniform random tap location model is appropriate.
- The 10K/2K/2K train/validation/test split is reasonable for the problem size.

### Statistical Analysis
- Paired t-tests are appropriate for seed-wise comparisons.
- Cohen's d effect sizes are reported for ablation (Table 6) — excellent.
- The distinction between "ns" (p > 0.05) and significance levels is clear.
- Missing: normality assumption checks for t-tests (though with n=20 seeds, CLT applies).

### Results Presentation
- Tables are well-formatted with mean ± std.
- The use of bold for best results per row is helpful.
- The footnote system (†, ‡, §) for caveats is clear and informative.

---

## Questions for Authors

1. What validation metric was used for the grid search of LMS/NLMS step sizes and LASSO regularization parameter? Was it NMSE on the validation set, or something else? Please add this detail.

2. Why were only 3 seeds used for the support recovery analysis (Table 10) instead of the 5 seeds used elsewhere? If this was a computational constraint, please state it explicitly.

3. For the QPSK BER "not significant" results (Table 7), have you considered using equivalence testing (TOST — Two One-Sided Tests) to formally demonstrate that LISTA and OMP BER are equivalent within a pre-specified margin? This would be stronger than relying on non-significant p-values.

4. The noise enhancement reversal at SNR=30 dB (Table 11) deserves more analysis. Can you provide the distribution of noise enhancement values (not just the mean) to understand whether the reversal is driven by outliers?

---

## Minor Issues

### Statistical Reporting
- Table 6 (ablation 20 seeds): Report the Wilcoxon signed-rank test p-values alongside the t-test p-values for completeness (the paper mentions "non-parametric" but only shows t-test results).
- Table 10 (support recovery): Report standard deviations or confidence intervals, not just means.

### Experimental Details
- Section 4.1: Specify the random seed used for data generation (separate from the 5 training seeds).
- Section 4.7.1: The LISTA-CP weight clipping implementation details are good, but the specific clipping threshold (1.0) should be stated in the methods section, not just the results.

### Figures
- Figure 1 (NMSE vs SNR): Add error bars (std over 5 seeds) to the plot.
- Figure 2 (NMSE vs sparsity): The divergence at K=15 (one seed) should be marked with a distinct marker.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | LISTA is well-known; contribution is analytical. BER-NMSE mechanism is novel. |
| Methodological Rigor (25%) | 74 | Strong | Good statistical validation. Grid search details insufficient. Inconsistent seed count. |
| Evidence Sufficiency (25%) | 78 | Strong | 13 experiments, 20-seed ablation, 200-realization BER. Missing DL baselines. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow. Mechanism analysis is well-argued. |
| Writing Quality (15%) | 70 | Adequate | Generally clear. Some dense passages. Abstract too long. |
| Literature Integration (optional) | 65 | Adequate | Good coverage of classical methods. Missing recent DL channel estimation papers. |
| Significance & Impact (optional) | 62 | Adequate | Useful reference for practitioners. Limited by lack of architectural novelty. |
| **Weighted Average** | **71.2** | **Minor Revision** | |

---

**Decision**: Minor Revision — The methodology is substantially improved with proper statistical validation. Remaining issues (baseline tuning details, inconsistent seeds, noise enhancement reversal) are minor and addressable.
