# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 7

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Dr. Kai Zhang, Associate Professor of Electrical Engineering. Expertise in deep unfolding architectures, optimization-based signal processing, and statistical methodology in machine learning research. Published 30+ papers on LISTA variants and sparse recovery.

### Review Focus
Experimental design rigor, statistical validity (power analysis, effect sizes, multiple comparisons), reproducibility of training protocols, and proper ablation methodology.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
5 — This paper falls squarely within my methodological expertise. I have published extensively on LISTA variants and am very familiar with the statistical methods used.

### Summary Assessment
This paper presents a methodologically sound analysis of LISTA for sparse channel estimation. The experimental design is comprehensive, covering 13 experiments with proper controls. The standout methodological contribution is the progression from 5-seed to 20-seed ablation with paired t-tests and Cohen's d effect sizes—the paper transparently acknowledges the initial false negative, which demonstrates good scientific practice. The BER analysis with 200 realizations per SNR point and paired t-tests is appropriately powered. However, I have concerns about: (1) the cross-table inconsistency in reported NMSE values, (2) the lack of multiple comparison correction across the 7 SNR points in Table 1, and (3) the missing confidence intervals for BER estimates. These are addressable issues that do not undermine the paper's core findings. I recommend Minor Revision.

---

## Strengths

### S1: Progressive Ablation with Transparent Power Analysis
The paper conducts ablation at two sample sizes (5 seeds in Table 5, 20 seeds in Table 11) and transparently reports that the 5-seed result was a false negative. The 20-seed experiment reports paired t-tests with Cohen's d effect sizes (d = 1.5, 18.4, 24.1), providing clear evidence of practical significance. This is excellent methodology that should be standard in the deep learning literature.

### S2: BER Validation with Appropriate Sample Size
The BER analysis uses 200 channel realizations per SNR point across 5 seeds (1000 total per condition). Paired t-tests with 95% CIs are reported for all LISTA vs. OMP comparisons. This is a significant improvement over typical papers that report BER without error bars or statistical testing.

### S3: Consistent Training Protocol with Clear Documentation
The paper clearly documents the mixed-SNR training protocol (SNR ∈ [0, 30] dB, Adam optimizer, cosine annealing, gradient clipping). The rationale for mixed-SNR training (single model across all conditions) is well-explained and avoids the common pitfall of training-test protocol mismatch.

### S4: LISTA-CP Diagnostic Analysis
The LISTA-CP comparison (Section 4.8) includes training log diagnostics confirming that the weight clipping constraint was never activated. This level of diagnostic detail is rare and provides genuine insight into why LISTA and LISTA-CP perform identically.

---

## Weaknesses

### W1: Cross-Table Inconsistency Requires Resolution
**Problem**: Table 1 (NMSE vs SNR) reports LISTA at -24.25 ± 0.40 dB for (N=64, K=5, M=256, L=20, SNR=20), while Table 3 (NMSE vs channel length) reports -32.29 ± 0.85 dB for the same nominal configuration. The paper attributes this to "independently trained models with different training distributions" (Section 4.3).
**Why it matters**: An ~8 dB discrepancy between tables with identical nominal parameters undermines reproducibility. Readers cannot determine which value is "correct" or how to reproduce either result.
**Suggestion**: (a) Add a "Training Protocol" column to every results table, (b) rerun Table 3 with the mixed-SNR model for direct comparison, or (c) consolidate all experiments under a single training protocol.
**Severity**: Major

### W2: No Multiple Comparison Correction
**Problem**: Table 1 reports paired t-tests at 7 SNR points without correction for multiple comparisons. At α = 0.05, the family-wise error rate for 7 independent tests is 1 - (1-0.05)^7 ≈ 0.30.
**Why it matters**: Some reported significant differences may be false positives. The SNR = 0 dB comparison (p < 0.01) may survive correction, but borderline cases (e.g., SNR = 5 dB, p = 0.24) need careful interpretation.
**Suggestion**: Apply Bonferroni or Holm correction to the family of t-tests in each table, or explicitly state that p-values are reported without correction and interpret accordingly.
**Severity**: Minor

### W3: BER Confidence Intervals Not Reported
**Problem**: Tables 10-12 report BER means and standard deviations but not 95% confidence intervals. For 5 seeds, the t-distribution critical value at 95% is 2.776, making CIs approximately ±2.776 × SE.
**Why it matters**: CIs are more interpretable than p-values for assessing practical significance. The paper claims "no BER penalty" but without CIs, readers cannot assess the precision of this claim.
**Suggestion**: Add 95% CIs to all BER tables, or at minimum report them for the key comparison (LISTA vs OMP at SNR ≥ 5 dB under MMSE).
**Severity**: Minor

### W4: Training Variability Not Reported
**Problem**: The paper reports mean ± std over 5 seeds for NMSE but does not report training variability (e.g., how much does the final NMSE vary across random initializations?). The 20-seed ablation (Table 11) shows std of 0.31-0.91 dB, but the main experiments use only 5 seeds.
**Why it matters**: With 5 seeds, the standard error of the mean is std/√5 ≈ 0.45× std. For LISTA at SNR=20 (std = 0.40), the SE is 0.18 dB, giving a 95% CI of ±0.50 dB. This is adequate but tight.
**Suggestion**: Report the standard error (SE = std/√n) alongside std in all tables, or increase seed count to 10 for the main experiments.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title accurately reflects the paper's scope. The "Analysis" framing is appropriate.
- Abstract contains excessive statistical detail (200 realizations, paired t-tests, 95% CI, 5 seeds) that should be in Methods.

### Introduction
- Clear enumeration of contributions. The motivation is well-articulated.
- Contribution #1 (NMSE saturation analysis) and #5 (SNR mitigation) overlap—consider merging.

### Methodology (Section 3)
- LISTA architecture description is clear and standard.
- The loss function discussion (scale-invariant NMSE) is insightful and correctly identified as the likely cause of saturation.
- Parameter analysis (N_params = L × (N² + 2)) is correct.

### Experiments (Section 4)
- **Experiment 1 (NMSE vs SNR)**: Well-designed. The SNR range [-5, 40] dB covers in-distribution and out-of-distribution.
- **Experiment 2 (NMSE vs Sparsity)**: Good. The K=15 divergence (one seed) is properly noted.
- **Experiment 3 (NMSE vs Channel Length)**: Cross-table inconsistency (W1) is the main issue. The N=256 divergence is properly diagnosed.
- **Experiment 4 (Depth Analysis)**: Clean and informative. L=10-20 recommendation is well-supported.
- **Experiment 5 (Ablation)**: Excellent methodology. The 5→20 seed progression is commendable.
- **Experiment 6 (Generalization)**: Adequate but could be more systematic (e.g., train on Gaussian, test on ITU with quantitative generalization gap).
- **Experiment 7 (Practical Deployment)**: Runtime comparison is useful but the caveat about Python overhead is important.
- **Experiment 8 (LISTA-CP)**: Diagnostic analysis is a strength.
- **Experiment 9 (SNR Mitigation)**: Well-designed. The 3 narrow-range strategies provide good coverage.
- **Experiment 10 (BER)**: The standout experiment. 200 realizations with paired t-tests is appropriate.
- **Experiment 11 (20-seed Ablation)**: Excellent. The effect sizes (d = 1.5, 18.4, 24.1) are compelling.
- **Experiment 12 (Mechanism Analysis)**: The error sparsity analysis is novel and insightful.
- **Experiment 13 (Hardware)**: Theoretical analysis is useful but should be clearly labeled as such.

### Discussion
- The "training artifact vs. architectural limitation" discussion is well-reasoned.
- The 3 evidence points (scale-invariant loss, SNR-specific training, LISTA-CP constraints) are convincing.

### References
- Good coverage. Statistical methodology references (paired t-tests, Cohen's d) are appropriately cited.

---

## Questions for Authors

1. Can you provide a supplementary table showing the exact training hyperparameters (learning rate, batch size, epochs, random seed) for each experiment to enable full reproducibility?

2. For the 20-seed ablation (Table 11), did you verify normality of the NMSE distribution before applying paired t-tests? With n=20, the t-test is robust to non-normality, but a Shapiro-Wilk test would strengthen the claim.

3. The BER analysis uses "paired t-tests" for LISTA vs OMP. Are these paired across the 5 seeds (each seed produces one BER estimate, then paired across seeds) or across the 200 realizations? The pairing structure affects the test statistic.

---

## Minor Issues

### Language / Grammar
- Section 4.5, line 3: "all three learnable components are significant" — specify "individually significant" to distinguish from joint significance
- Table 11 footnote: "n=20 seeds" — should be "n = 20 random seeds"

### Figures and Tables
- Table 1: Add effect size (Cohen's d) alongside p-values for completeness
- Table 5 vs Table 11: Consider side-by-side comparison to highlight the power analysis insight
- Figure 3 (NMSE vs channel length): The N=256 outlier makes the y-axis range awkward; consider a separate panel

### Statistical Reporting
- All tables: Report exact p-values (not just "p < 0.01") for transparency
- BER tables: Add 95% CIs for the key comparisons

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | BER-NMSE mechanism analysis is novel; LISTA application is incremental |
| Methodological Rigor (25%) | 82 | Strong | Good statistical testing, proper ablation, but cross-table inconsistency |
| Evidence Sufficiency (25%) | 80 | Strong | Comprehensive experiments with appropriate sample sizes |
| Argument Coherence (15%) | 84 | Strong | Clear logical flow, honest limitations |
| Writing Quality (15%) | 78 | Strong | Well-written, some verbosity |
| **Weighted Average** | **78.0** | **Minor Revision** | |
