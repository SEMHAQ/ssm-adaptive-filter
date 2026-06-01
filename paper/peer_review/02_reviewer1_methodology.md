# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-05-31
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology Expert

### Reviewer Identity
Dr.~James Chen, Associate Professor of Electrical Engineering, specializing in statistical signal processing and compressed sensing. Expert in experimental design for sparse recovery algorithms, reproducibility, and statistical validity. Published extensively on OMP, LASSO, and basis pursuit denoising.

### Review Focus
Research design rigor, statistical validity, reproducibility, baseline fairness, and experimental methodology. This review examines whether the experimental setup is sound, the comparisons are fair, and the statistical claims are supported.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**

### Confidence Score
5 — This paper's methodology falls directly within my area of expertise. I have published on OMP, LASSO, and sparse recovery algorithms, and I am very familiar with the experimental protocols used here.

### Summary Assessment
This paper evaluates LISTA for sparse channel estimation through a comprehensive experimental campaign covering SNR sweeps, sparsity variation, channel length scaling, depth analysis, ablation, and ITU generalization. The experimental design is generally sound, with appropriate baselines (OMP with oracle K, grid-searched LASSO/LMS/NLMS) and 5-seed averaging.

The methodology has two significant issues. First, the data consistency problem: Table 1 (SNR) and Table 2 (Sparsity) yield different LISTA values at the shared condition (SNR=20, K=5), indicating different training runs were used without acknowledgment. Second, the ablation study's statistical claims are internally inconsistent — the paper claims W contributes +2.28 dB (p < 0.001) while Table 5 shows removing W *improves* performance (p = 0.605). These issues are fixable and do not invalidate the overall findings, but they must be addressed before publication.

---

## Strengths

### S1: Appropriate Baseline Selection with Fair Hyperparameter Tuning
The paper uses grid search to optimize LMS, NLMS, and LASSO hyperparameters on a validation set, which is the correct approach for fair comparison. OMP is used with oracle K, which the paper acknowledges as an unfair advantage for OMP. This transparency is commendable. The hyperparameter grids are reasonable (e.g., LMS step size: {0.001, 0.005, 0.01, 0.02, 0.05}).

### S2: Comprehensive Experimental Coverage
The paper covers 7 experiments spanning SNR, sparsity, channel length, depth, ablation, generalization, and ITU channels. This breadth is unusual for a single paper and provides readers with a complete picture of LISTA's behavior. The 5-seed averaging provides reasonable uncertainty estimates.

### S3: Ablation Study Design
The ablation design (Full, No W, Fixed threshold, Shared params) isolates individual component contributions cleanly. Using paired t-tests with reported p-values is appropriate for comparing paired samples (same seeds). The four configurations are well-chosen to separate threshold, mapping, and per-layer effects.

### S4: Reproducibility
The paper specifies all hyperparameters (learning rate, weight decay, batch size, epochs, gradient clipping norm), data generation details (10K train, 2K val, 2K test), and random seed protocol. This enables reproduction.

---

## Weaknesses

### W1: Data Inconsistency Between Tables (Critical)
**Problem**: At the shared condition SNR=20, K=5, N=64, M=256, L=20:
- Table 1 (SNR): LISTA = -23.12 ± 0.19 dB
- Table 2 (Sparsity): LISTA = -31.16 ± 1.76 dB
- Table 3 (Channel Length, N=64): LISTA = -32.29 ± 0.85 dB

These three values differ by 8--9 dB at the *same experimental condition*. This can only be explained by different training runs producing different models. The paper does not acknowledge this inconsistency.
**Why it matters**: If the tables use different models, the cross-experiment comparisons in the Summary (Section 4.8) are invalid. The claim "LISTA saturates at ~-23 dB" depends on Table 1, but Tables 2-3 show -31 to -33 dB at the same condition.
**Suggestion**: Re-run all experiments with a single model. If the -23 dB saturation is real (from Table 1), then Tables 2-3 must be re-generated. If the -31 dB from Table 2 is real, then the SNR saturation claim is wrong. The paper cannot have both.
**Severity**: Critical

### W2: OMP Baseline Fairness Concern
**Problem**: OMP is run with oracle K (known sparsity level), while LISTA does not receive K. The paper acknowledges this but frames it as "LISTA doesn't need K" — an advantage. However, in practice, K can often be estimated from the data (e.g., via cross-validation or information criteria). Running OMP with estimated K would provide a more realistic comparison.
**Why it matters**: The oracle K gives OMP an unfair advantage that inflates the performance gap. With estimated K, OMP's performance would degrade, potentially narrowing the gap with LISTA.
**Suggestion**: Add an experiment with OMP using estimated K (e.g., via cross-validation or MDL criterion). This would strengthen the paper's practical claims.
**Severity**: Minor

### W3: No Confidence Intervals for Baselines
**Problem**: Tables 1-2 report baseline values without standard deviations (footnote says "std < 0.1 dB across seeds; omitted"). However, Table 3 reports baseline std values. This inconsistency makes it impossible to assess whether baseline differences are statistically significant.
**Why it matters**: Without baseline std, we cannot determine if LISTA's advantage over LASSO (e.g., 2 dB at K=5) is statistically significant or within noise.
**Suggestion**: Report baseline std in all tables, or at minimum report it for the key comparisons (LISTA vs LASSO, LISTA vs OMP).
**Severity**: Minor

### W4: Missing Effect Size Reporting
**Problem**: The ablation study reports p-values but not effect sizes (e.g., Cohen's d). With n=5 seeds, statistical power is low, and p-values alone can be misleading. The paper claims "p < 0.001" for the threshold contribution, but with n=5, this requires a very large effect size.
**Why it matters**: Effect sizes would help readers assess practical significance vs. statistical significance. A p < 0.001 with n=5 implies a very large effect, which should be reported explicitly.
**Suggestion**: Report Cohen's d alongside p-values in Table 5. Also consider reporting 95% confidence intervals for the deltas.
**Severity**: Minor

---

## Detailed Comments

### Methodology / Research Design
- The data generation (i.i.d. Gaussian taps, BPSK pilots, AWGN) is standard and appropriate for the research question.
- The train/val/test split (10K/2K/2K) is adequate.
- The choice of 200 epochs with cosine annealing is reasonable.

### Results / Findings
- Table 1: LISTA's saturation at -23 dB is clearly visible. The narrative correctly identifies this.
- Table 3: The N=256 divergence (3/5 seeds) is concerning but honestly reported.
- Table 4: Depth sweep is well-designed but only 5 seeds may be insufficient for detecting instability at L=8.

### Statistical Reporting
- The paper correctly uses NMSE in dB throughout.
- The use of mean ± std over 5 seeds is standard but would benefit from confidence intervals.
- The ablation's paired t-test is appropriate for the paired design.

---

## Questions for Authors

1. **Data consistency**: Please provide a table showing which JSON file / training run was used for each experiment. Are Tables 1, 2, and 3 from the same or different training runs?
2. **Statistical power**: With n=5 seeds, what is the minimum detectable effect size at α=0.05? Have you considered using more seeds (e.g., 10-20) for the ablation study?
3. **OMP with estimated K**: Have you tried running OMP with K estimated from the data? How does this affect the comparison?

---

## Minor Issues

### Figures and Tables
- Table 4: Add ± std for OMP baseline for consistency.
- Table 5: Consider adding Cohen's d column.
- All tables: Report baseline std values (even if small) for transparency.

### Statistical Reporting
- The paper should report 95% confidence intervals for key comparisons.
- Consider Bonferroni correction for multiple comparisons in the ablation study (4 comparisons → α = 0.0125).

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 60 | Adequate | Standard LISTA application; cross-distribution finding is interesting |
| Methodological Rigor (25%) | 62 | Adequate | Good design but data inconsistency is a significant methodological flaw |
| Evidence Sufficiency (25%) | 70 | Adequate | Comprehensive experiments but missing effect sizes and baseline std |
| Argument Coherence (15%) | 65 | Adequate | Generally clear but ablation contradiction weakens coherence |
| Writing Quality (15%) | 75 | Strong | Clear methodology description |
| **Weighted Average** | **66.2** | **Minor Revision** | |
