# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 5

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology Expert

### Reviewer Identity
Prof.~Dr.~James Chen, Department of Electrical and Computer Engineering, University of Toronto. Expert in statistical signal processing, experimental design for machine learning systems, and reproducibility in computational research. 15 years of experience in sparse recovery algorithms with particular focus on rigorous benchmarking methodology and statistical validation. Author of "Best Practices for Benchmarking Sparse Recovery Algorithms" (IEEE SPM, 2022).

### Review Focus
Research design rigor, statistical validity, experimental methodology, reproducibility, and whether the experimental evidence supports the paper's claims. I particularly focus on: (1) whether baseline comparisons are fair, (2) whether statistical testing is appropriate and adequately powered, (3) whether results are reproducible from the provided information.

---

## Overall Assessment

### Recommendation
- [ ] **Accept**
- [ ] **Minor Revision**
- [x] **Major Revision**
- [ ] **Reject**

### Confidence Score
5 — This is squarely within my expertise. Experimental methodology for sparse recovery benchmarking and statistical validation of machine learning claims are my primary research areas.

### Summary Assessment

This paper presents a systematic evaluation of LISTA for sparse channel estimation across 13 experiments. The methodology is generally sound, with several commendable practices: the 200-realization BER study with paired $t$-tests, the 20-seed ablation with effect size reporting, and the honest acknowledgment of cross-table inconsistencies. However, there are significant methodological concerns that must be addressed before publication: (1) the BER analysis uses only 3 seeds for QPSK (Table 8) but 5 seeds for 16-QAM (Table 9), creating an inconsistency in statistical power; (2) the MMSE equalization analysis (Table 11) is limited to 2 SNR points, insufficient to support the paper's claims about MMSE robustness; (3) the LISTA-CP comparison (Table 12) shows suspiciously identical values across all conditions, suggesting a possible implementation issue rather than the claimed "naturally satisfied constraints"; (4) the training-validation-test split is not clearly specified for all experiments. These issues are addressable but require substantial additional experiments and clarification.

---

## Strengths

### S1: Commendable Statistical Rigor in BER Analysis
The use of 200 channel realizations per SNR point with paired $t$-tests and 95\% confidence intervals (Section 4.10) represents a significant improvement over standard practice in the signal processing community. The explicit reporting of $p$-values in Tables 8--9 allows readers to assess claim reliability. The progression from 50 to 200 realizations (mentioned in Section 4.10) demonstrates iterative improvement of the experimental design.

### S2: Honest Reporting of Statistical Power Limitations
The paper transparently reports that the 5-seed ablation (Table 5) had insufficient statistical power ($\sim$15--20\% for medium effects) and that this produced false negatives for the threshold and per-layer parameters. The correction with 20 seeds (Table 10) and the explicit statement "the Round 2 finding that these components were 'not individually significant' was a false negative" is exemplary scientific honesty. This transparency is rare and valuable.

### S3: Cross-Table Consistency Explanation
The explicit note in Section 4.3 explaining the $\sim$8~dB discrepancy between Table 2 ($-24.25$~dB) and Table 4 ($-32.29$~dB) at the same nominal configuration is excellent. The explanation (independently trained models with different training distributions) is correct and demonstrates careful experimental bookkeeping. Many papers would silently ignore such discrepancies.

### S4: Comprehensive Baseline Optimization
The grid search for baseline hyperparameters (LMS step size, NLMS step size, LASSO $\lambda$) with per-SNR optimization (Section 4.1) ensures fair comparison. The use of validation set for hyperparameter selection and test set for evaluation follows proper experimental protocol.

### S5: Reproducibility Information
The paper provides sufficient detail for reproduction: training hyperparameters (Adam, lr $5 \times 10^{-4}$, weight decay $10^{-5}$, 200 epochs, batch size 256), data generation procedure (10K train, 2K val, 2K test), and network architecture ($L=20$, $N=64$, $M=256$). The code appears to be available (based on the project structure).

---

## Weaknesses

### W1: Inconsistent Seed Count in BER Analysis
**Problem**: Table 8 (QPSK BER) reports "Mean $\pm$ std over 3 seeds" while Table 9 (16-QAM BER) reports "Mean $\pm$ std over 5 seeds." This inconsistency in the number of seeds between the two modulation schemes is unexplained and creates different statistical power for the two analyses. The paired $t$-tests for QPSK (with $n=3$) have much lower power than for 16-QAM ($n=5$), potentially masking real differences.
**Why it matters**: With only 3 seeds, the QPSK paired $t$-test has $\sim$10\% power to detect a medium effect size ($d = 0.5$). The reported "ns" (not significant) results for QPSK may be false negatives due to insufficient power, not genuine equivalence. This undermines the paper's central claim that LISTA achieves "comparable BER" for QPSK.
**Suggestion**: Re-run the QPSK BER analysis with 5 seeds (matching 16-QAM) and report the updated $p$-values. If the results remain non-significant, the claim is strengthened. If they become significant, the paper's narrative needs revision.
**Severity**: Critical

### W2: LISTA-CP Suspiciously Identical Results
**Problem**: Table 12 shows LISTA and LISTA-CP achieving identical NMSE values at all 4 SNR points (0, 10, 20, 30 dB), with the paper claiming "maximum per-parameter difference = 0." This is statistically implausible: even with identical architectures and the same training procedure, different random seeds should produce slightly different results. The claim that the weight clipping constraint is "naturally satisfied" (spectral norm 0.34 < 1.0) does not explain why the trained parameters are bit-for-bit identical.
**Why it matters**: This raises a red flag about the experimental setup. Possible explanations: (a) the LISTA-CP implementation shares the same random seed and does not actually apply the weight clipping (implementation bug), (b) the weight clipping is applied but never activates (which would mean the architectures are truly identical and the comparison is trivial), or (c) the results are copied from the same source.
**Suggestion**: Verify the LISTA-CP implementation by: (1) checking that the weight clipping is actually applied during training (print the spectral norms at each epoch), (2) running with different random seeds to confirm the results are not seed-dependent, (3) explicitly reporting whether the clipping gradient was ever non-zero during training. If the clipping truly never activates, this should be stated as a limitation of the comparison rather than presented as a finding.
**Severity**: Critical

### W3: MMSE Equalization Analysis Insufficient
**Problem**: Table 11 compares ZF and MMSE BER at only 2 SNR points (10 and 20 dB) for QPSK. This is insufficient to support the paper's claims about MMSE robustness. The paper states "MMSE equalization confirms this is not a ZF-specific artifact" (abstract), but the evidence is limited. At SNR=20 dB, all three methods achieve identical BER (0.0003) under MMSE, which actually undermines the claim of LISTA's BER advantage.
**Why it matters**: The paper's central practical claim hinges on LISTA's BER advantage. If this advantage vanishes under MMSE (which is the standard equalizer), the practical relevance is limited to ZF-based systems. The current 2-point comparison cannot determine at which SNR the MMSE advantage persists or vanishes.
**Suggestion**: Provide a full SNR sweep (0--30 dB, step 5 dB) for MMSE equalization with both QPSK and 16-QAM. Report paired $t$-tests for LISTA vs.~OMP under MMSE at each SNR point. This is essential for the paper's practical deployment argument.
**Severity**: Major

### W4: Training-Test Split Ambiguity
**Problem**: The paper states "10,000 training samples, 2,000 validation samples, and 2,000 test samples" (Section 4.1), but it is unclear whether the same test set is used across all experiments. For the channel length experiment (Table 4), the test set must have different $N$ values; for the sparsity experiment (Table 3), different $K$ values. Are these separate test sets, or is the same 2,000-sample set reused?
**Why it matters**: Reusing the same test set across multiple experiments inflates the risk of overfitting to the test set, especially when hyperparameters are tuned on validation data that may share distributional properties with the test set.
**Suggestion**: Clarify whether each experiment uses an independently generated test set. If the same test set is reused, acknowledge this as a limitation.
**Severity**: Minor

### W5: Error Bars Missing from Some Tables
**Problem**: Tables 2 (NMSE vs SNR) and 3 (NMSE vs Sparsity) report LISTA mean $\pm$ std but do not report error bars for the baselines (LMS, NLMS, OMP, LASSO). Since the baselines are deterministic algorithms (given fixed data), their "std" across seeds comes only from the randomness in data generation. However, for a fair comparison, the baseline std should also be reported to show whether the LISTA-baseline differences exceed the baseline's own variance.
**Why it matters**: Without baseline error bars, readers cannot assess whether the LISTA-OMP gap is statistically significant for the NMSE experiments. The BER experiments report $p$-values, but the NMSE experiments do not.
**Suggestion**: Report mean $\pm$ std for all methods in all tables, and include paired $t$-tests for LISTA vs.~OMP at each condition in the NMSE experiments (as done for BER).
**Severity**: Major

---

## Detailed Comments

### Title & Abstract
- The title accurately describes the paper's scope. "Analysis" is appropriate given the paper's focus on understanding rather than proposing a new method.
- The abstract claims "LISTA achieves comparable BER with OMP for QPSK ($p > 0.05$ at all SNR points)" — but this is based on only 3 seeds (Table 8). With 3 seeds, the $t$-test has very low power, so "comparable" should be qualified as "not statistically distinguishable with the current sample size."

### Introduction
- The 6 contributions are comprehensive. Contribution 2 (BER analysis) is the strongest and most novel.
- The claim "LISTA achieves comparable BER with OMP for QPSK" in the introduction should reference the seed count limitation.

### Methodology
- The LISTA architecture description (Section 3.3) is clear and standard.
- The training procedure (Section 3.5) is well-specified. The mixed-SNR training is a reasonable choice.
- The NMSE loss function (Eq.~8) is appropriate for channel estimation.

### Results
- Experiment 1 (NMSE vs SNR): The saturation at $-25$~dB is well-characterized. The explanation (scale-invariant loss + mixed-SNR training) is plausible.
- Experiment 5 (Ablation, 5 seeds): The initial ablation is underpowered. The paper acknowledges this, which is good.
- Experiment 10 (BER): The statistical validation is commendable but undermined by the seed count inconsistency (W1).
- Experiment 11 (Ablation, 20 seeds): This is the gold standard for ablation studies. The effect sizes are compelling.
- Experiment 12 (Mechanism): The error sparsity analysis (Table 13) is the paper's most insightful result.

### Discussion
- The MMSE implications discussion (Section 5.1) is important but relies on the insufficient Table 11 data.
- The limitations section (5.3) is honest and comprehensive.

### References
- Comprehensive and up-to-date. The inclusion of recent surveys (\citet{elbir2023deep}, \citet{gao2023deep}, \citet{wu2024deep}) is appropriate.

---

## Questions for Authors

1. **Seed count inconsistency**: Why does Table 8 (QPSK) use 3 seeds while Table 9 (16-QAM) uses 5 seeds? Was this intentional or an oversight? If intentional, what is the justification for the different statistical power?

2. **LISTA-CP implementation verification**: Can you provide training logs showing the spectral norm $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ at each epoch for LISTA-CP? If the clipping gradient was never non-zero, this should be explicitly stated.

3. **MMSE full sweep**: Can you provide MMSE BER for all SNR points (0--30 dB) for both QPSK and 16-QAM? This is essential for the paper's practical deployment argument.

4. **Baseline error bars**: Can you report mean $\pm$ std for OMP and LASSO in Tables 2--4, and include paired $t$-tests for LISTA vs.~OMP at each condition?

5. **LISTA variance at high SNR**: In Table 2, LISTA's std is $0.40$--$0.79$~dB at SNR $\geq 10$~dB, while the NMSE is nearly constant ($-24.25$ to $-25.08$~dB). Is this variance across seeds, or across test samples within a single seed? Clarify the source of variance.

---

## Minor Issues

### Language / Grammar
- Section 4.5, p.~9: "the statistical power is limited ($\sim$15--20\% for medium effects)" — specify what "medium effects" means (Cohen's $d = 0.5$?).
- Section 4.12, p.~16: "LISTA concentrates 99.9\% of its estimation error energy on the true tap locations" — "error energy" should be "error power" for consistency with signal processing terminology.

### Citation Format
- Reference \citet{liu2023listamp}: Verify that this is the correct citation for LISTA-AMP. The paper lists it as "liu2023listamp" but the actual publication may have a different year.

### Figures and Tables
- Table 12: Add a column showing the per-parameter difference between LISTA and LISTA-CP to support the "identical" claim.
- Table 13: The "Est.~sparsity" column shows 100.0\% for both methods. Explain what this metric means and why it is relevant.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 58 | Weak | LISTA is well-established; the contribution is analytical insight. The BER-NMSE mechanism analysis is novel but the method is not. |
| Methodological Rigor (25%) | 62 | Adequate | Generally sound methodology with commendable statistical practices. However, the seed count inconsistency (W1), LISTA-CP identical results (W2), and insufficient MMSE analysis (W3) are significant methodological gaps. |
| Evidence Sufficiency (25%) | 65 | Adequate | 13 experiments provide broad coverage. However, the MMSE analysis is insufficient (2 SNR points), and some tables lack error bars for baselines. |
| Argument Coherence (15%) | 68 | Adequate | The BER-NMSE disconnect argument is well-constructed. The positioning tension between NMSE gap and BER advantage creates some friction. |
| Writing Quality (15%) | 74 | Strong | Clear, professional prose. Good section organization. Some density in the abstract. |
| **Weighted Average** | **64.6** | **Major Revision** | |

---

## Overall Score: 65/100
