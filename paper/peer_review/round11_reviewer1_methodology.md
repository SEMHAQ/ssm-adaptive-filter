# Methodology Review Report (Peer Reviewer 1)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 11

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Dr. Marcus Chen, Associate Professor of Electrical Engineering, specializing in compressed sensing, sparse recovery algorithms, and deep learning for communications.

### Review Focus
Research design rigor, statistical validity, reproducibility, and experimental methodology for algorithm comparison studies.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
**5** — Completely within my area of expertise.

### Summary Assessment

This paper provides a methodologically sound experimental evaluation of LISTA for sparse channel estimation. The experimental design is comprehensive, covering NMSE vs. SNR, sparsity, channel length, depth analysis, ablation, generalization, BER performance, and hardware complexity. The use of paired t-tests and Cohen's d effect sizes in the ablation study (Section 4.11) is commendable and represents best practice for computational studies.

The key methodological strengths include: (1) the progression from underpowered 5-seed ablation to properly powered 20-seed ablation, with transparent reporting of the statistical power issue; (2) the BER simulation with 200 channel realizations per SNR point; (3) the paired experimental design where all methods are evaluated on the same channel realizations. The methodology is appropriate for the research questions posed.

However, several methodological concerns remain: (1) the cross-table inconsistency between Tables 1 and 3 (−24.25 vs. −32.29 dB at the same nominal configuration) is confusing and should be better explained; (2) the BER experiments report 5 seeds but the confidence intervals suggest this may be insufficient for the effect sizes observed; (3) the LISTA-CP comparison does not include a formal equivalence test. These are minor issues that do not fundamentally undermine the findings.

---

## Strengths

### S1: Statistical Rigor in Ablation Study
The 20-seed ablation (Section 4.11) with paired t-tests, Cohen's d effect sizes, and transparent reporting of the 5-seed power limitation is exemplary. The finding that the 5-seed ablation produced "false negatives" (Section 4.5) due to low power (~15–20% for medium effects) is an important methodological lesson. The effect sizes are large (d = 1.5 to 24.1), confirming that the findings are not artifacts of multiple testing.

### S2: Paired Experimental Design for BER
The BER simulation uses 200 channel realizations per SNR point with all methods evaluated on the *same* realizations (Section 4.10), enabling paired statistical tests that control for channel-to-channel variability. This is a strong design choice that increases statistical power and reduces confounding.

### S3: Transparent Reporting of Training Protocol Effects
The cross-table consistency note (Section 4.3) explicitly explains why LISTA values differ between tables (different training distributions). This transparency allows readers to correctly interpret the results and is more valuable than hiding the inconsistency.

### S4: Comprehensive Baseline Comparison
The baselines (LMS, NLMS, OMP, LASSO) are well-chosen and hyperparameters are optimized via grid search on the validation set (Section 4.1). The OMP oracle-K setting is appropriate for an upper-bound comparison.

---

## Weaknesses

### W1: BER Confidence Intervals May Be Insufficient
**Problem**: The BER experiments report results over 5 seeds (Table 10), but the standard deviations reported are very small (e.g., ±0.0003 at SNR = 15). With only 5 seeds and 200 realizations per seed, the effective sample size for the paired t-test is n = 5 (seeds), not n = 1000 (realizations).
**Why it matters**: With n = 5, the paired t-test has limited power for small effect sizes. The p = 0.09 at SNR = 15 (Table 10) could be a Type II error.
**Suggestion**: Report the effective degrees of freedom more clearly. Consider running 10+ seeds for the BER experiments, or using a mixed-effects model that accounts for both seed and realization variability.
**Severity**: Minor

### W2: Cross-Table Inconsistency Needs Clearer Framing
**Problem**: Table 1 reports LISTA NMSE = −24.25 dB at SNR = 20, while Table 3 reports −32.29 dB at the same nominal configuration. The explanation in Section 4.3 is helpful but buried in a footnote.
**Why it matters**: Readers comparing tables will be confused. The 8 dB difference is large and could undermine confidence in the results.
**Suggestion**: Add a prominent callout box or a dedicated paragraph in Section 4.1 explaining that LISTA results are training-distribution-dependent, and that the mixed-SNR model (Table 1) is the primary reference.
**Severity**: Minor

### W3: LISTA-CP Comparison Lacks Equivalence Testing
**Problem**: Table 8 reports LISTA vs. LISTA-CP differences < 0.2 dB with p > 0.4, and the authors conclude "statistically indistinguishable." However, non-significance does not prove equivalence — it only fails to reject the null hypothesis of no difference.
**Why it matters**: With n = 5 seeds, the test has limited power. The authors should either report an equivalence test (TOST procedure) or explicitly acknowledge that the sample size may be insufficient to detect small differences.
**Suggestion**: Add a sentence: "While the non-significant p-values are consistent with equivalence, the small sample size (n = 5) limits our ability to detect differences < 0.5 dB. Formal equivalence testing with larger samples would strengthen this conclusion."
**Severity**: Minor

### W4: Training Reproducibility Details
**Problem**: The paper reports training hyperparameters (learning rate, weight decay, batch size, epochs) but does not report the random seeds used for training, the hardware used, or the training time.
**Why it matters**: Reproducibility requires complete reporting of the experimental environment.
**Suggestion**: Add a reproducibility table in Section 4.1 listing: PyTorch version, CUDA version, GPU model, training time per model, and the 5 random seeds used.
**Severity**: Minor

---

## Detailed Comments

### Research Questions & Hypotheses
- The research questions are implicit rather than explicitly stated. The paper would benefit from a clear RQ list: RQ1: How does LISTA compare to classical methods in NMSE? RQ2: What is LISTA's BER performance? RQ3: What components contribute to LISTA's performance? RQ4: How does LISTA generalize?

### Research Design
- The experimental design is comprehensive and well-structured. The use of 12 experiments with clear separation of concerns is appropriate.
- The decision to use mixed-SNR training as the default and report it consistently is a good design choice.

### Sampling Strategy
- Training: 10,000 samples; validation: 2,000; test: 2,000. These are reasonable for the problem complexity.
- The 200 channel realizations per BER SNR point is adequate.

### Data Collection
- Synthetic data generation is well-described (Section 4.1). The use of BPSK pilots, Gaussian tap amplitudes, and uniform tap locations is standard.
- The ITU channel models (PedA, VehA) provide a realistic test.

### Analysis Methods
- NMSE in dB is the standard metric. BER simulation with MMSE and ZF equalization is appropriate.
- The paired t-test is the correct choice for seed-level comparisons. Cohen's d is reported for all ablation comparisons.

### Results Presentation
- Tables are well-formatted with mean ± std, p-values, and significance markers.
- The bold marking of best results per row is helpful.
- Figure references are included but figures were not available in the review version.

### Reproducibility
- Code availability is not mentioned. The authors should state whether code and data will be released.
- The experimental setup is described in sufficient detail for replication.

### Methodological Fallacies Detected
- No major fallacies detected. The authors appropriately acknowledge limitations and avoid overclaiming.

---

## Questions for Authors

1. Can you confirm that the 5 random seeds used for training are independent of the 200 channel realizations used for BER evaluation? If seeds are reused, this could introduce correlation.
2. For the 20-seed ablation (Section 4.11), were all 20 seeds used for both training and evaluation, or were different seeds used for each? Please clarify the experimental protocol.
3. The paper reports gradient clipping with max norm 5.0 (Section 4.1). Have you verified that gradients are not consistently hitting this limit, which could indicate training instability?

---

## Minor Issues

### Statistical Reporting
- Table 1: Consider reporting 95% confidence intervals in addition to mean ± std.
- Table 10: The "Sig." column could include the actual p-value range (e.g., "p < 0.01" instead of just "**").

### Figures
- Figure references are included but figures were not available. Please ensure all figures are included in the submission.
