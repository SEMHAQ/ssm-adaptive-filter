# Peer Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 4

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Prof. Kai Zhang, Associate Professor of Electrical Engineering, Tsinghua University. Expertise in deep unfolding architectures, proximal optimization, and statistical validation methodology for signal processing. Author of 15+ papers on LISTA variants and algorithm unrolling. Strong focus on reproducibility, statistical power, and fair baseline comparisons.

### Review Focus
Research design rigor, statistical validity, experimental methodology, reproducibility, and fair comparison protocols. I particularly scrutinize whether baselines are properly tuned, whether statistical tests are appropriate, and whether claims are supported by the evidence presented.

---

## Overall Assessment *

### Recommendation *
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score *
5 — Completely within my area of expertise. Deep unfolding methodology and statistical validation are my core research areas.

### Summary Assessment *
This paper provides a systematic evaluation of LISTA for sparse channel estimation, with particular emphasis on BER validation, ablation studies, and practical deployment. The methodology is generally sound: baselines are grid-searched, statistical tests are used (paired t-tests, Cohen's d), and the ablation study is conducted with adequate sample sizes (20 seeds). The BER analysis with 200 realizations per SNR point represents a significant improvement over typical evaluations in this literature.

However, I have concerns about the NMSE discrepancy across tables, the fairness of the LASSO baseline (500 ISTA iterations may be insufficient), and the lack of confidence intervals for some BER results. The SNR saturation analysis is insightful but the mechanism explanation could be more rigorous. These issues are addressable and do not fundamentally undermine the paper's contributions.

---

## Strengths *

### S1: Rigorous BER Validation with Statistical Testing
The BER experiment (Section 4.10) uses 200 channel realizations per SNR point with paired t-tests and 95% confidence intervals—far exceeding the typical 50–100 realizations in the literature. The distinction between QPSK (p > 0.05, comparable) and 16-QAM (p < 0.05 at SNR ≥ 15 dB, better) is well-supported. The MMSE equalization confirmation (Table 10) strengthens the finding.

### S2: Progressive Ablation with Power Analysis
The ablation study demonstrates methodological maturity: the initial 5-seed experiment (Table 5) is honestly reported as underpowered, and the follow-up 20-seed experiment (Table 11) with parametric and non-parametric tests provides definitive results. The Cohen's d effect sizes (1.5, 18.4, 24.1) clearly communicate practical significance.

### S3: Fair Baseline Comparison Protocol
The paper grid-searches hyperparameters for all baselines (LMS step size, NLMS step size, LASSO regularization) on the validation set, which is the correct protocol. The oracle-K setting for OMP is acknowledged, and the implications are discussed.

### S4: Comprehensive Generalization Analysis
The paper tests generalization across sparsity, SNR, channel length, and channel type (ITU). The SNR-specific training mitigation experiment (Section 4.9) is well-designed and provides actionable guidance.

---

## Weaknesses *

### W1: NMSE Discrepancy Across Tables
**Problem**: At the nominal configuration (N=64, K=5, M=256, L=20, SNR=20 dB), Table 1 reports LISTA NMSE = −24.25 ± 0.40 dB, Table 7 (Channel Length, N=64 row) reports −32.29 ± 0.85 dB, and Table 9 (SNR Mitigation, baseline row) reports −25.04 ± 0.67 dB. These differ by up to 8 dB.
**Why it matters**: If the same training procedure and configuration are used, these values should be identical. The discrepancy suggests different training runs, seeds, or procedures were used, contradicting the paper's claim of "a single model that is evaluated across all experimental conditions."
**Suggestion**: (1) Explicitly state whether each table uses the same trained model or independent training runs. (2) If different seeds produce different results, report the inter-seed variance. (3) Add a "Training Details" column or footnote to each table specifying the training run used.
**Severity**: Major

### W2: LASSO Baseline May Be Underpowered
**Problem**: LASSO is solved via ISTA with 500 iterations (Section 4.1). For ill-conditioned problems or small regularization parameters, 500 iterations may not converge. The paper does not report convergence diagnostics (residual norm, objective value trajectory).
**Why it matters**: If LASSO has not converged, the comparison is unfair—LISTA's 20 forward passes are compared against an unconverged LASSO. This could inflate LISTA's relative advantage.
**Suggestion**: (1) Report the convergence status of LASSO (e.g., final residual norm). (2) Consider using FISTA instead of ISTA for faster convergence. (3) Test with 1000+ iterations to verify that 500 is sufficient.
**Severity**: Major

### W3: Missing Confidence Intervals for Some BER Results
**Problem**: Table 8 (QPSK BER) reports mean ± std over 3 seeds, while Table 9 (16-QAM BER) reports over 5 seeds. The MMSE comparison (Table 10) reports only means without uncertainty. The statistical tests are applied inconsistently.
**Why it matters**: Without consistent uncertainty quantification, readers cannot assess the reliability of the BER comparisons, particularly the MMSE results.
**Suggestion**: (1) Use the same number of seeds (preferably 5) for all BER experiments. (2) Report confidence intervals for all BER results, including MMSE. (3) Apply paired t-tests consistently across all comparisons.
**Severity**: Minor

### W4: SNR Saturation Mechanism Lacks Formal Analysis
**Problem**: The paper attributes the SNR saturation to three factors (Section 5.1): fixed-depth architecture, scale-invariant loss, and soft-thresholding bias. However, no formal analysis or ablation isolates these factors. The claim that "the scale-invariant NMSE loss produces parameters that compromise across noise levels" is intuitive but unsubstantiated.
**Why it matters**: Without isolating the causes, it is unclear which mitigation strategy is most effective and why.
**Suggestion**: (1) Provide a formal analysis of the soft-thresholding bias floor. (2) Consider an ablation that isolates the loss function effect (e.g., train with MSE instead of NMSE). (3) If formal analysis is infeasible, soften the claims to "hypothesized factors" rather than presenting them as established causes.
**Severity**: Minor

---

## Detailed Comments *

### Title & Abstract
- Title is descriptive but could emphasize the BER finding more prominently.
- Abstract is comprehensive and well-structured. The key quantitative findings are clearly stated.

### Introduction
- The research gap is well-identified: no systematic BER validation of LISTA for channel estimation.
- The 6-contribution list is excessive—consolidate to 3–4 core contributions.

### Methodology
- LISTA architecture (Section 3.3) is standard and clearly described.
- Training details (Section 3.5) are complete: Adam optimizer, cosine annealing, gradient clipping.
- The mixed-SNR training protocol (Section 4.1) is well-designed for fair evaluation.

### Results
- Experiment 1 (NMSE vs SNR): Clear and well-presented. The saturation at −25 dB is honestly reported.
- Experiment 5 (Ablation): The 5→20 seed progression is exemplary.
- Experiment 10 (BER): The statistical validation is the paper's strongest methodological contribution.
- Experiment 12 (Mechanism): The error sparsity analysis is insightful but could benefit from formal analysis.

### Discussion
- The limitations section is honest and comprehensive.
- The deployment recommendations are practical.

### References
- Comprehensive and up-to-date. The inclusion of hardware deployment references is appropriate.

---

## Questions for Authors *

1. **Table discrepancy**: Please explain the 8 dB difference between Table 1 (−24.25 dB) and Table 7 (−32.29 dB) for the same nominal configuration. Were different training runs used?
2. **LASSO convergence**: Did LASSO converge within 500 ISTA iterations? Please report convergence diagnostics (e.g., relative change in objective value over the last 100 iterations).
3. **SNR saturation**: Can you provide evidence that the scale-invariant loss is a primary cause of saturation? For example, does training with MSE loss (instead of NMSE) change the saturation behavior?

---

## Minor Issues

### Language / Grammar
- Section 4.1: "each training batch uses a randomly sampled SNR from [0, 30] dB" — clarify whether this is per-sample or per-batch.
- Table 3 caption: "Pilot ratio M/N varies: 8 (N=32), 4 (N=64), 2 (N=128), 1 (N=256)" — this is helpful context.

### Citation Format
- Reference [chen2018lista]: The year in the bib entry is 2019 but the citation key says 2018. Verify the correct year.

### Figures and Tables
- All tables are well-formatted and clear.
- Figure 1 (NMSE vs SNR) would benefit from a log-scale x-axis for the high-SNR region.

---

## Dimension Scores *

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | BER-NMSE disconnect is novel; LISTA application is incremental |
| Methodological Rigor (25%) | 72 | Adequate | Good practices but table discrepancy and LASSO convergence concerns |
| Evidence Sufficiency (25%) | 78 | Strong | 200 realizations, 20 seeds, effect sizes; some missing CIs |
| Argument Coherence (15%) | 76 | Strong | Clear narrative with minor inconsistencies |
| Writing Quality (15%) | 77 | Strong | Professional prose; some density |
| **Weighted Average** | **73.4** | **Minor Revision** | |
