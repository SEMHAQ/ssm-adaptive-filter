# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-ROUND17
- **Review Date**: 2026-06-01
- **Review Round**: Round 17

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology Expert

### Reviewer Identity
Dr. Kai Zhang, Associate Professor at ETH Zürich. Expertise in deep unfolding theory, optimization algorithms for sparse recovery, and statistical methodology for experimental validation. Published extensively on LISTA variants and convergence analysis. Review focuses on experimental design rigor, statistical validity, and reproducibility.

### Review Focus
Research design appropriateness, statistical methodology (power analysis, multiple comparisons, effect sizes), reproducibility of experimental procedures, and validity of the ablation study design.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Accept**
- [ ] **Reject**

### Confidence Score
5 — Deep unfolding and statistical methodology are squarely within my expertise.

### Summary Assessment
This paper presents a comprehensive experimental evaluation of LISTA for sparse channel estimation, with particular attention to the error concentration mechanism. The methodology is generally sound: mixed-SNR training protocol, grid-searched baselines, multiple random seeds, paired t-tests with Holm–Bonferroni correction, and Cohen's d effect sizes. The progression from 5-seed to 20-seed ablation demonstrates methodological awareness of statistical power issues. However, several methodological concerns remain: (1) the 5-seed experiments throughout the paper have insufficient power for the claims made, (2) the NMSE loss function choice deserves deeper justification, and (3) the error concentration metric (Eq. 6) has edge-case behavior that needs clarification. These are addressable in revision and do not undermine the core findings.

---

## Strengths

### S1: Statistical Rigor with Holm–Bonferroni Correction
The paper consistently applies Holm–Bonferroni correction for multiple comparisons (Tables 1, 10, 11). The 20-seed ablation (Table 10) reports both parametric (paired t-test) and non-parametric (Wilcoxon signed-rank) results, with Cohen's d effect sizes. This level of statistical rigor is commendable and exceeds what is typically seen in the signal processing literature.

### S2: Honest Reporting of Statistical Power Limitations
The authors transparently acknowledge that the initial 5-seed ablation had insufficient power (15–20% for medium effects) and that the threshold/per-layer results were false negatives (Section 4.5, Section 4.12). This self-correction strengthens methodological credibility.

### S3: Multiple Baseline Comparison with Fair Hyperparameter Optimization
All baselines (LMS, NLMS, OMP, LASSO, FISTA) use grid-searched hyperparameters on the validation set, ensuring fair comparison. The FISTA baseline with 20 iterations is a natural comparison for LISTA. The LASSO convergence verification (relative change < 10⁻⁴ at iteration 500) is appropriately documented.

### S4: Pre-Thresholding Diagnostic Analysis
The pre-thresholding analysis (Section 4.13.4) is methodologically sophisticated. By computing error concentration on the intermediate representation (before soft-thresholding), the authors rule out the trivial explanation that 100% concentration is simply due to sparse outputs. The 68.3% → 100.0% jump is compelling evidence.

### S5: Cross-Table Consistency Transparency
The explicit discussion of the 8 dB difference between Tables 1 and 5 (Section 4.3) is excellent methodological practice. The consolidated Table 3 makes the training-distribution sensitivity visible as a first-class result rather than a footnote.

---

## Weaknesses

### W1: Insufficient Seed Count in Main Experiments
**Problem**: The main experiments (Tables 1, 2, 4, 5, 6, 8) use only 5 seeds. For the effect sizes observed (e.g., LISTA vs OMP differences of 13–33 dB), 5 seeds may provide adequate power. However, for smaller effects (e.g., LISTA vs FISTA at low SNR: ~1 dB), 5 seeds yields very wide confidence intervals. The paper reports "mean ± std over 5 seeds" but does not report confidence intervals or power analysis for the main experiments.
**Why it matters**: Without confidence intervals, readers cannot assess whether the 1 dB LISTA vs FISTA difference at SNR=−5 dB (Table 1) is statistically distinguishable from zero.
**Suggestion**: Report 95% confidence intervals for all main experiments (not just the ablation). For the 5-seed experiments, use t₀.₀₂₅,₄ = 2.776 for CI computation. Consider reporting power for key comparisons.
**Severity**: Major

### W2: Error Concentration Metric Edge Cases
**Problem**: The error concentration ratio (Eq. 6) is defined as ∑ᵢ∈S (ĥᵢ−hᵢ)² / ∑ᵢ₌₁ᴺ (ĥᵢ−hᵢ)². When the total error is zero (perfect recovery), the ratio is defined as 100% "by convention." However, the paper also reports 100.0% ± 0.0% for LISTA, which could mean either (a) perfect recovery on support taps with zero non-support error, or (b) the convention being triggered. The paper does not clarify which interpretation applies.
**Why it matters**: If LISTA achieves 100% because total error ≈ 0 on some seeds, the metric is degenerate. If LISTA achieves 100% because non-support error is truly zero, the result is meaningful.
**Suggestion**: Report the mean total error alongside the concentration ratio. Clarify whether the 100.0% ± 0.0% arises from the convention or from genuinely zero non-support error. The pre-thresholding analysis (Table 7) partially addresses this but should be cross-referenced.
**Severity**: Major

### W3: NMSE Loss Function Justification
**Problem**: The paper uses NMSE loss (Eq. 5) which is scale-invariant. The authors attribute the −25 dB saturation to this loss function and mixed-SNR training (Section 5.1). However, the alternative of using MSE loss or SNR-adaptive loss is not experimentally evaluated. The claim that saturation is "a training artifact" is supported by the SNR-specific training experiment (Table 9) but not by loss function comparison.
**Why it matters**: If the saturation is caused by the loss function choice, this is a methodological limitation that should be explicitly acknowledged as a design decision with consequences.
**Suggestion**: Add a brief experiment or discussion comparing NMSE loss vs. MSE loss. If infeasible, explicitly state that the loss function choice is a design decision and discuss its implications.
**Severity**: Minor

### W4: Training Data Independence
**Problem**: The paper generates 10,000 training, 2,000 validation, and 2,000 test samples with "independent channel realizations and noise" (Section 4.1). However, the pilot signals are BPSK-modulated (±1), which means the measurement matrix X has entries in {−1, +1}. The paper does not discuss whether the training/validation/test splits share pilot sequences or use independent ones.
**Why it matters**: If pilot sequences are shared, the test set is not fully independent of training, potentially inflating performance estimates.
**Suggestion**: Clarify whether pilot sequences are independent across splits. If shared, discuss the implications.
**Severity**: Minor

### W5: LISTA-CP Experiment Interpretation
**Problem**: The LISTA-CP comparison (Section 4.8) reports identical performance because "the clipping was never activated" (spectral norms remained below 0.35). The authors interpret this as evidence that standard LISTA training already satisfies convergence conditions. However, an alternative interpretation is that the gradient clipping (max norm 5.0) implicitly enforces the weight constraint, making the explicit LISTA-CP constraint redundant.
**Why it matters**: If gradient clipping is the actual mechanism, the conclusion should attribute the convergence satisfaction to gradient clipping, not to "natural" training behavior.
**Suggestion**: Run LISTA-CP without gradient clipping to test whether the weight constraint becomes active. If it does, the interpretation changes significantly.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is accurate and descriptive. "Systematic Analysis" is appropriate.
- Abstract reports "mean ± std over 20 seeds" for the error concentration but "mean ± std over 5 seeds" for other results—this inconsistency should be noted.

### Methodology / Research Design
- The experimental design is comprehensive: SNR sweep, sparsity sweep, channel length sweep, pilot ratio sweep, depth analysis, ablation, generalization, BER, and mechanism analysis.
- The mixed-SNR training protocol is well-justified and consistently applied.
- The grid search for baselines is appropriate but the search ranges could be wider for LASSO (λ up to 0.5 may be insufficient for high SNR).

### Results / Findings
- Table 1: At SNR=5 dB, LISTA std = 4.10 dB—this is unusually high and suggests one outlier seed. Consider reporting median ± IQR or investigating the outlier.
- Table 2: At K=15, LISTA std = 8.27 dB with one diverged seed. The paper notes this but does not discuss whether excluding the diverged seed changes the conclusion.
- Table 6: The pilot ratio analysis is valuable but uses mixed-SNR training. A pilot-ratio-specific training experiment would strengthen the analysis.

### Statistical Reporting
- The paper reports p-values but not confidence intervals for main experiments. Adding CIs would improve interpretability.
- The Holm–Bonferroni correction is appropriate. The paper correctly notes when results become non-significant after correction.
- Cohen's d values in Table 10 are very large (d = 18.4, 24.1), indicating massive effect sizes. This is appropriate for the threshold/per-layer ablation.

---

## Questions for Authors

1. Can you clarify the edge-case behavior of the error concentration metric? Specifically, for LISTA at SNR=20 dB, what is the mean total error ∑ᵢ₌₁ᴺ (ĥᵢ−hᵢ)²? If this value is near zero, the 100% concentration is trivially true.

2. The 5-seed experiments report "mean ± std" but not confidence intervals. For the LISTA vs FISTA comparison at SNR=−5 dB (Δ = 0.69 dB, Table 1), what is the 95% CI for the difference? Is this difference statistically significant?

3. In the LISTA-CP experiment (Section 4.8), did you monitor whether gradient clipping (max norm 5.0) was the mechanism keeping spectral norms below 0.35? What would happen with gradient clipping disabled?

4. For Table 1 at SNR=5 dB, LISTA std = 4.10 dB is much higher than at adjacent SNR points (0.35 at SNR=0, 0.69 at SNR=10). Can you explain this outlier?

---

## Minor Issues

### Language / Grammar
- Section 4.13.2, Eq. 6: "When the total error ... = 0, the ratio is defined as 100% by convention" — this should be stated in the main text, not just in a parenthetical.
- Section 4.12, p. 14: "The Round 2 finding that these components were 'not individually significant' was a false negative" — "Round 2" refers to internal revision history; consider "the initial 5-seed experiment" for the published version.

### Citation Format
- Reference formatting is consistent. No issues noted.

### Figures and Tables
- Table 10: Consider adding a column for the non-parametric (Wilcoxon) p-values alongside the parametric ones.
- Table 7: The "Non-zero S̄ taps" column header uses S̄ which may confuse readers; consider "Non-zero non-support taps."

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | Error concentration analysis is novel but builds on known soft-thresholding properties |
| Methodological Rigor (25%) | 78 | Strong | Comprehensive design with statistical testing; 5-seed limitation in main experiments; edge-case metric behavior |
| Evidence Sufficiency (25%) | 82 | Strong | Multiple experiments, seeds, baselines, statistical tests; some gaps in power analysis |
| Argument Coherence (15%) | 80 | Strong | Clear narrative; AMP connection weakens slightly |
| Writing Quality (15%) | 82 | Strong | Clear, professional; minor internal reference issues |
| **Weighted Average** | **77.4** | **Minor Revision** | |

---

*Report submitted by Reviewer 1 (Methodology)*
