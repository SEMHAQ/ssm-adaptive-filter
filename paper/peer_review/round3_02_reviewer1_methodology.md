# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 3

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology Expert

### Reviewer Identity
Dr. Marcus Chen, Research Scientist, Google DeepMind (Communications ML Team). Expertise in deep unfolding architectures, statistical validation of ML systems, and reproducibility in computational research. Published on LISTA variants and their convergence properties. Focus: experimental design rigor, ablation methodology, statistical validity, reproducibility.

### Review Focus
Research design rigor, ablation methodology, statistical validity, effect size reporting, reproducibility, and completeness of experimental evidence. I evaluate whether the experimental conclusions are justified by the data and whether the experiments are sufficient to support the claims.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
5 — Deep unfolding and statistical validation are my core expertise. I have published on LISTA variants and am very confident in my assessment.

### Summary Assessment
This manuscript provides a comprehensive empirical evaluation of LISTA for sparse channel estimation, covering 11 experiments across multiple dimensions. The ablation study with 20 seeds and proper statistical testing is the methodological highlight. However, the BER analysis—the paper's most novel contribution—lacks the methodological rigor of the NMSE experiments: no statistical testing, no error bars on individual BER points, no analysis of the mechanism behind the BER-NMSE disconnect. The paper also has several experimental gaps (no MMSE equalization, no complex-valued channels, no frequency-selective fading) that limit the generalizability of the findings. The NMSE saturation explanation is plausible but not experimentally validated. I recommend Major Revision to address these methodological gaps before publication.

---

## Strengths

### S1: Ablation Study Sets a Good Standard
The 20-seed ablation with paired t-tests and Cohen's d (Section 4.11, Table 9) is exemplary. The authors transparently report that the initial 5-seed study was underpowered and proactively conducted the follow-up. The effect sizes are large and unambiguous: d=18.4 for threshold, d=24.1 for shared parameters. This is the kind of rigorous ablation that deep learning papers should aspire to.

### S2: Mixed-SNR Training Eliminates Confounds
The decision to use mixed-SNR training (random SNR from [0, 30] dB per batch) and evaluate a single model across all conditions is methodologically sound. It eliminates the confound of training-procedure differences between tables, which is a common issue in deep learning papers that train separate models for each experimental condition.

### S3: LISTA-CP Diagnostic Analysis
The LISTA-CP comparison (Section 4.8) goes beyond simple performance comparison to explain *why* the two architectures are identical: the weight clipping constraint is never activated because the spectral norm ||W^(k) - I||_2 = 0.34 < 1.0. This diagnostic analysis adds genuine insight and demonstrates methodological maturity.

### S4: Transparent Limitation Reporting
The authors explicitly report divergence at N=256 (3/5 seeds yield positive NMSE), divergence at K=15 (one seed), and the Python-only speed caveat. This transparency is appreciated and allows readers to assess the boundaries of the findings.

---

## Weaknesses

### W1: BER Analysis Lacks Statistical Rigor
**Problem**: The BER results (Tables 10–11) report mean ± std over 5 seeds, but no statistical tests are performed. The paper claims LISTA achieves "competitive" or "better" BER than OMP, but at high SNR the differences are very small (e.g., QPSK at SNR=30: LISTA 0.0006 vs OMP 0.0004, a 0.0002 difference). With only 5 seeds and 50 channel realizations per point, the statistical power to detect such small differences is very low. No confidence intervals, no paired t-tests, no effect sizes.

**Why it matters**: The BER analysis is the paper's most novel finding. If the "better BER" claim is not statistically significant, the paper's main contribution collapses.

**Suggestion**: (1) Add paired t-tests between LISTA and OMP BER at each SNR point. (2) Increase the number of channel realizations per SNR point (50 is low for BER estimation; 200–500 would be more reliable). (3) Report 95% confidence intervals. (4) If the differences are not statistically significant, revise the claims accordingly.

**Severity**: Critical

### W2: No Mechanism Analysis for BER-NMSE Disconnect
**Problem**: The paper claims LISTA's "error structure is more favorable for zero-forcing equalization" but provides no analysis of what this means quantitatively. No measurement of: (a) tap-location accuracy (how often LISTA identifies the correct K non-zero taps), (b) the equalizer's noise enhancement factor ||(X^T X)^{-1} X^T||^2, (c) the condition number of the estimated channel matrix, (d) the distribution of estimation errors (sparse vs. dense).

**Why it matters**: Without mechanism analysis, the BER finding is an empirical observation without explanation. The reader cannot assess whether the finding will generalize to other scenarios.

**Suggestion**: Add a diagnostic section that measures: (1) support set recovery accuracy (Jaccard index between estimated and true non-zero tap locations) for LISTA vs. OMP; (2) the equalizer's noise enhancement factor; (3) the sparsity of the estimation error (what fraction of LISTA's error is concentrated on true tap locations vs. spread across all taps). This would transform the finding from "LISTA has better BER" to "LISTA has better BER *because* X."

**Severity**: Critical

### W3: NMSE Saturation Explanation Not Experimentally Validated
**Problem**: Section 5.1 attributes the NMSE saturation to three factors: (1) fixed-depth architecture, (2) scale-invariant NMSE loss, (3) soft-thresholding bias floor. However, only factor (1) is partially validated (the depth experiment in Section 4.4). Factors (2) and (3) are asserted without experimental evidence.

**Why it matters**: If the saturation mechanism is not understood, mitigation strategies (like SNR-specific training) are discovered by trial-and-error rather than principled design.

**Suggestion**: Validate the three factors experimentally: (1) Train LISTA with MSE loss instead of NMSE loss—does the saturation improve? (2) Replace soft-thresholding with hard-thresholding—does the bias floor change? (3) Use the SNR-specific training results to argue whether the saturation is a loss-function issue or an architecture issue.

**Severity**: Major

### W4: No MMSE Equalization Results
**Problem**: All BER results use zero-forcing (ZF) equalization. MMSE equalization is the standard in practical systems and may behave differently with LISTA vs. OMP channel estimates, particularly at low SNR where ZF is known to amplify noise.

**Why it matters**: If the BER advantage only holds for ZF equalization, the practical relevance is limited since most modern systems use MMSE.

**Suggestion**: Add BER results with MMSE equalization for at least QPSK. If the finding holds for MMSE, it strengthens the paper significantly. If it doesn't, the paper should discuss this limitation.

**Severity**: Major

### W5: No Error Bars on BER Figures
**Problem**: Tables 10–11 report mean ± std, but the paper references BER figures (not shown in the LaTeX). Without error bars, visual inspection of BER curves cannot distinguish signal from noise.

**Why it matters**: BER plots are the standard way to present these results; without error bars, the visual impression may be misleading.

**Suggestion**: Ensure all BER figures include error bars (±1 std or 95% CI) and use log scale for the y-axis.

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title accurately describes the content. "Analysis" is the right framing.
- Abstract line: "LISTA achieves competitive BER with OMP for QPSK and better BER for 16-QAM" — this claim needs statistical validation (see W1).

### Introduction
- The six contributions are well-organized. Contribution 2 (BER) should be the centerpiece given its novelty.
- The research gap is clearly identified: prior work lacks systematic characterization.

### Methodology / Research Design
- Data generation: 10K training, 2K validation, 2K test is reasonable for the problem size.
- Baselines: Grid search over LMS/NLMS step sizes and LASSO λ is appropriate. Oracle K for OMP is noted.
- LISTA configuration: L=20, N=64, M=256, K=5 are standard and well-motivated.
- Training: Adam with cosine annealing, gradient clipping—standard and appropriate.

### Results / Findings
- Table 1 (NMSE vs SNR): The saturation at ~-25 dB is clearly visible. The std values are small, indicating stable training.
- Table 3 (channel length): N=256 divergence is an important finding. The pilot ratio M/N=1 explanation is plausible.
- Table 9 (ablation 20 seeds): Excellent statistical reporting. The effect sizes are unambiguous.
- Tables 10–11 (BER): See W1 regarding statistical rigor.

### Discussion
- Section 5.1 is the weakest part of the discussion. The BER-NMSE disconnect explanation needs rigorous support.
- Section 5.2 (deployment recommendations) is practical and well-structured.
- Section 5.3 (limitations) is honest and specific.

### Conclusion
- Conclusions are generally supported. The "comparable BER" claim needs statistical backing.

---

## Questions for Authors

1. **BER statistical significance**: Are the BER differences between LISTA and OMP statistically significant at each SNR point? Please provide paired t-tests with p-values.

2. **Support set recovery**: What is LISTA's tap-location accuracy compared to OMP? Does LISTA correctly identify the K non-zero taps more or less often than OMP?

3. **MMSE equalization**: Does the BER advantage hold with MMSE equalization? If not, how does this affect the practical relevance of the finding?

4. **NMSE saturation mechanism**: Can you experimentally validate whether the saturation is caused by the NMSE loss function, the soft-thresholding bias, or the fixed-depth architecture?

---

## Minor Issues

### Language / Grammar
- Section 4.10, paragraph 2: "This counterintuitive result" appears twice in close proximity. Vary the language.
- Table 9 footnote: "p < 0.001 (paired t-test, n=20 seeds)" — consider also reporting Wilcoxon signed-rank p-values for robustness.

### Figures and Tables
- Table 1: The ± std values are helpful. Consider adding a column for the gap with OMP (in dB) for easier comparison.
- Table 5: The ‡ footnote about N=256 divergence is important. Consider bolding or highlighting this row.

### Citation Format
- Reference format appears consistent with Elsevier style.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 52 | Weak | Contribution is systematic analysis; BER finding is novel but unvalidated |
| Methodological Rigor (25%) | 65 | Adequate | Strong ablation; BER analysis lacks statistical rigor |
| Evidence Sufficiency (25%) | 62 | Adequate | Comprehensive NMSE experiments; BER and mechanism analysis insufficient |
| Argument Coherence (15%) | 68 | Adequate | Clear structure; BER-NMSE disconnect explanation is weak |
| Writing Quality (15%) | 74 | Strong | Clear, honest, well-organized |
| **Weighted Average** | **63.6** | **Major Revision** | |
