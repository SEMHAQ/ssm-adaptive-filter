# Peer Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 10

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology

### Reviewer Identity
Associate Professor in Statistical Signal Processing at a research university, specializing in experimental design and statistical validation for computational methods. Expertise in paired hypothesis testing, effect size reporting, power analysis, and reproducibility standards for machine learning experiments. Published on statistical methodology for comparing iterative algorithms.

### Review Focus
Statistical rigor of the experimental design, appropriateness of hypothesis tests and sample sizes, fairness of baseline comparisons, and reproducibility of the training and evaluation protocols.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
5 — Statistical methodology and experimental design for computational methods are squarely within my expertise.

### Summary Assessment
This paper provides a systematic empirical analysis of LISTA for sparse channel estimation. From a methodological standpoint, the paper demonstrates clear growth during its revision history: the progression from 5-seed experiments (Tables 1-4) to 20-seed ablation (Table 13) with proper paired t-tests and Cohen's d effect sizes reflects genuine engagement with statistical best practices. The BER experiments use 200 channel realizations per SNR point with paired tests, which is appropriate. However, several methodological concerns remain: (1) the 5-seed experiments underlying the main NMSE tables have limited statistical power (~15-20% for medium effects), (2) the mixed-SNR training protocol creates a systematic comparison issue where LISTA is evaluated on conditions it was not specifically optimized for, while baselines are grid-searched per SNR, and (3) the LISTA-CP comparison conflates "constraint not activated" with "constraint not needed." These are addressable concerns that do not fundamentally undermine the paper's contributions but should be discussed transparently.

---

## Strengths

### S1: 20-Seed Ablation with Proper Statistical Testing
The 20-seed ablation study (Section 4.11, Table 13) is methodologically exemplary. The use of paired t-tests with Cohen's d effect sizes, combined with the explicit acknowledgment that the initial 5-seed experiment lacked statistical power, demonstrates mature statistical practice. The effect sizes are dramatic (d = 18.4 for threshold, d = 24.1 for shared parameters), leaving no doubt about the significance of the findings. The inclusion of both parametric (paired t-test) and non-parametric (Wilcoxon signed-rank test) results would further strengthen confidence, but the large effect sizes make this less critical.

### S2: BER Experiments with Adequate Sample Size and Paired Design
The BER experiments (Section 4.10) use 200 channel realizations per SNR point with paired t-tests across 5 random seeds. The paired design—where all methods are evaluated on the same channel realizations and noise instances—is appropriate for controlling channel-to-channel variability. The reporting of 95% confidence intervals alongside p-values follows current best practices.

### S3: Honest Reporting of Statistical Limitations
The paper explicitly acknowledges the statistical power limitation of the 5-seed experiments (Section 4.5): "with only n=5 seeds, the statistical power is limited (~15–20% for medium effects)." This transparency is commendable and rare. The paper then addresses this limitation by conducting the 20-seed follow-up, demonstrating responsive revision.

### S4: Fair Baseline Optimization Protocol
The baselines (LMS, NLMS, OMP, LASSO) use grid-searched hyperparameters on the validation set (Section 4.1), which is a fair comparison protocol. The paper explicitly states that baselines use the "same hyperparameters optimized on the i.i.d. Gaussian validation set" for ITU channel experiments, ensuring no channel-specific re-optimization.

### S5: Cross-Table Consistency Explanation
The paper proactively explains the ~8 dB discrepancy between Table 1 and Table 3 at the same nominal configuration (Section 4.3), attributing it to different training distributions. This preemptive explanation prevents reader confusion and demonstrates awareness of cross-experiment consistency.

---

## Weaknesses

### W1: 5-Seed Experiments Have Insufficient Statistical Power
**Problem**: Tables 1-4 (NMSE vs SNR, Sparsity, Channel Length, Depth) use only 5 random seeds. For the typical effect sizes observed (differences of 1-3 dB with standard deviations of 0.3-0.8 dB), n=5 yields approximately 15-20% statistical power for medium effects (d = 0.5). This means the experiments have an 80-85% chance of missing real differences.
**Why it matters**: The main NMSE comparison tables—the paper's primary results—have limited ability to detect statistically significant differences between methods. The paper reports "paired t-tests: all LISTA vs OMP differences are significant (p < 0.01)" in Table 1, but with n=5, only very large effects (d > 2) can be reliably detected.
**Suggestion**: Report exact p-values for all comparisons (not just "p < 0.01"), and add a brief power analysis note. Alternatively, increase to 10-20 seeds for the main NMSE tables, consistent with the ablation study. If this is impractical due to computational cost, state this explicitly.
**Severity**: Major

### W2: Mixed-SNR Training Creates Asymmetric Comparison
**Problem**: LISTA is trained with mixed-SNR sampling (SNR ∈ [0, 30] dB) and evaluated across all SNR levels with a single model. However, the baselines (LMS, NLMS, LASSO) are grid-searched per SNR—"best selected per SNR" (Section 4.1). This means baselines have SNR-specific optimization while LISTA does not.
**Why it matters**: This asymmetry makes the comparison unfair at each individual SNR point. LISTA's "saturation" at −25 dB may partly reflect the compromise across SNR levels, while baselines are optimized for each operating point. The paper acknowledges this indirectly (Section 4.9 shows SNR-specific training improves to −31 dB), but does not explicitly frame the main comparison as unfair.
**Suggestion**: Add a sentence in Section 4.1 explicitly noting this asymmetry: "We note that LMS/NLMS/LASSO hyperparameters are optimized per SNR, while LISTA uses a single mixed-SNR model. This reflects a practical deployment scenario (one model for all conditions) but means LISTA is at a disadvantage at any specific SNR." The SNR-specific training results (Table 10) then serve as the fair apples-to-apples comparison.
**Severity**: Major

### W3: LISTA-CP Comparison Logic is Circular
**Problem**: Section 4.8 reports that LISTA and LISTA-CP achieve "statistically indistinguishable performance" because "the weight clipping constraint was never activated" (spectral norms remained below 0.35, well within the constraint bound of 1.0). The paper concludes that "the convergence guarantees of LISTA-CP provide theoretical assurance but no practical accuracy improvement."
**Why it matters**: The conclusion that LISTA-CP's constraints are "not needed" is valid only for this specific training configuration (gradient clipping max norm 5.0, Adam optimizer, 200 epochs). Under different training conditions (larger learning rates, longer training, different optimizers), the constraint might activate and provide benefit. The current framing implies LISTA-CP is generally unnecessary, which overgeneralizes from a single training setup.
**Suggestion**: Soften the conclusion to: "Under our training configuration, the LISTA-CP constraints are naturally satisfied, suggesting that standard LISTA training with gradient clipping already achieves the convergence conditions. Whether this holds under different training protocols remains an open question."
**Severity**: Minor

### W4: Missing Confidence Intervals in Main NMSE Tables
**Problem**: Tables 1-4 report "mean ± std" but do not report confidence intervals or exact p-values for all comparisons. The paper reports p-values only for LISTA vs OMP, not for LISTA vs LASSO or LISTA vs LMS/NLMS.
**Why it matters**: Without confidence intervals, readers cannot assess the precision of the estimates. Without p-values for all pairwise comparisons, the statistical significance of LISTA's advantage over LMS/NLMS (which is claimed but not statistically tested) is uncertain.
**Suggestion**: Add 95% confidence intervals (mean ± t_{0.025, n-1} × std/√n) to the main tables, or at least report exact p-values for LISTA vs all baselines.
**Severity**: Minor

### W5: Training-Test Data Leakage Not Explicitly Addressed
**Problem**: The paper generates 10,000 training, 2,000 validation, and 2,000 test samples with "independent channel realizations and noise" (Section 4.1). However, the validation set is used for hyperparameter selection (learning rate, weight decay, etc.), and the test set results are reported. The paper does not explicitly confirm that the test set was never used during training or hyperparameter tuning.
**Why it matters**: In machine learning experiments, subtle data leakage can inflate test performance. While the paper's protocol appears sound, explicit confirmation would strengthen confidence.
**Suggestion**: Add a sentence: "The test set was held out and never used during training or hyperparameter selection. All hyperparameters were selected using the validation set only."
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title accurately reflects the paper's content. "Analysis" correctly positions the work.
- The abstract reports p-values and confidence intervals, which is good statistical practice.

### Methodology (Section 3)
- The LISTA architecture (Section 3.3) is standard and well-documented.
- The NMSE loss function (Equation 6) is appropriate for channel estimation.
- The training protocol (Adam, cosine annealing, gradient clipping) is well-documented.

### Results (Section 4)
- Table 1 (NMSE vs SNR): The inclusion of "mean ± std" is good. The footnote about paired t-tests is useful but should include exact p-values.
- Table 5 (LISTA vs LISTA-CP): The diagnostic analysis of weight clipping activation is a strength.
- Table 10 (SNR mitigation): The comparison across training ranges is well-designed.
- Table 13 (20-seed ablation): Excellent statistical rigor. This should be the model for the other experiments.

### Statistical Reporting
- The paper follows APA 7.0 conventions for reporting p-values (asterisks for significance levels).
- Cohen's d is reported for the ablation study but not for the main NMSE comparisons. Consistent effect size reporting throughout would improve the paper.

---

## Questions for Authors

1. What is the exact computational cost of running 20 seeds vs 5 seeds for the main NMSE experiments? If feasible, would you consider expanding Tables 1-4 to 10-20 seeds for consistency with the ablation study?

2. For the BER experiments (Section 4.10), you report "mean over 5 seeds" in the table captions but conduct paired t-tests. How are the paired tests structured—across seeds, across realizations, or across both? Please clarify the exact statistical test design.

3. The paper reports that LISTA training diverges at K=15 (one seed, Table 2) and N=256 (all seeds, Table 3). Have you investigated whether these divergences are due to gradient explosion, numerical overflow, or optimization failure? Understanding the failure mode would strengthen the generalization analysis.

---

## Minor Issues

### Language / Grammar
- No significant language issues. The paper is well-written.

### Figures and Tables
- All tables include appropriate statistical annotations.
- Consider adding error bars to the figures (Figures 1-4) for visual consistency with the tables.

### Citation Format
- Citations follow the journal's author-year format correctly.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | No new method; analytical contribution. BER mechanism is novel insight. |
| Methodological Rigor (25%) | 72 | Adequate | Good ablation methodology. Main NMSE tables have limited power (n=5). Asymmetric baseline comparison. |
| Evidence Sufficiency (25%) | 75 | Strong | Comprehensive experiments. Hardware claims lack measured validation. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow. Appropriate hedging. |
| Writing Quality (15%) | 82 | Strong | Professional, honest, well-structured. |
| **Weighted Average** | **72** | **Minor Revision** | Methodological concerns are addressable. The 20-seed ablation demonstrates capability for rigorous statistics. |

---

## Questions for Authors (Summary)
1. Expand main NMSE tables to more seeds for statistical power?
2. Clarify BER paired test design (across seeds vs realizations)?
3. Investigate training divergence failure modes at K=15 and N=256?
