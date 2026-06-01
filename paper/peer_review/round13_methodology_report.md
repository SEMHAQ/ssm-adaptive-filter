# Peer Review Report — Peer Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 13

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology

### Reviewer Identity
Associate Professor specializing in statistical signal processing and experimental design for machine learning systems. Expertise in paired hypothesis testing, effect size reporting, power analysis, and reproducibility in computational experiments. Has published on ablation study methodology and the pitfalls of underpowered experiments.

### Review Focus
Statistical rigor of experimental design, adequacy of sample sizes and power analysis, fairness of baseline comparisons, and reproducibility of computational experiments.

---

## Overall Assessment

### Recommendation
**Minor Revision**

### Confidence Score
**5** — Completely within my area of expertise.

### Summary Assessment

This paper presents a comprehensive experimental evaluation of LISTA for sparse channel estimation, covering SNR sweeps, sparsity sweeps, channel length analysis, depth analysis, ablation studies, generalization tests, BER simulations, and hardware complexity analysis. The methodology is generally sound: the 20-seed ablation with paired t-tests and Cohen's d is well-designed, the 200-realization BER simulations provide adequate statistical power, and the baseline comparisons use grid-searched hyperparameters.

However, several methodological concerns should be addressed: (1) the core experiments (Tables 1-4) use only 5 seeds, which the authors acknowledge is underpowered but still report strong conclusions from; (2) the cross-table consistency issue (8 dB difference at the same nominal configuration) introduces potential confounds that are explained but not fully resolved; (3) the mixed-SNR training protocol, while practical, makes it difficult to separate training effects from architectural properties; (4) multiple comparison corrections are not applied despite numerous hypothesis tests. These issues are addressable and do not fundamentally undermine the paper's conclusions, but they should be explicitly discussed.

---

## Strengths

### S1: Progressive Statistical Validation
The paper demonstrates methodological awareness by initially running 5-seed ablation (Table 5), identifying the power limitation, and then conducting a 20-seed follow-up (Table 11) with both parametric and non-parametric tests. This progressive approach to statistical validation is commendable and sets a good example for the field.

### S2: Effect Size Reporting
The consistent reporting of Cohen's d alongside p-values in the ablation study (Table 11) is excellent. The effect sizes are large (d = 1.5 to 24.1), providing strong evidence that the ablation effects are practically significant, not just statistically significant. This addresses the common criticism of deep learning papers that rely solely on p-values.

### S3: Paired Experimental Design for BER
The BER simulations use 200 independent channel realizations per SNR point with all methods evaluated on the *same* channel realizations and noise instances. This paired design enables paired t-tests that control for channel-to-channel variability, which is a significant methodological strength over independent-sample comparisons.

### S4: Baseline Fairness
The baselines (OMP, LASSO, LMS, NLMS) are tuned via grid search on the validation set, which is the correct procedure. The LASSO convergence is explicitly verified (relative change < 10^-4 at iteration 500). The oracle K for OMP is stated. This transparency about baseline tuning is important for fair comparison.

### S5: Cross-Table Consistency Disclosure
The paper explicitly discloses the ~8 dB difference between Tables 1 and 3 at the same nominal configuration (Section 4.3), attributes it to different training protocols, and provides a consolidated comparison table (Table 3a). This is excellent transparency that many papers would hide.

---

## Weaknesses

### W1: Underpowered Core Experiments (5 Seeds)
**Problem**: Tables 1, 2, 3, and 4 use only 5 seeds. With n=5, a paired t-test has approximately 15-20% power to detect medium effects (Cohen's d = 0.5). The authors acknowledge this for the ablation study but do not apply the same standard to the core NMSE experiments. The reported standard deviations in Table 1 are small (0.05-0.79 dB), suggesting low variance, but 5 seeds may not capture the full distribution of training outcomes.
**Why it matters**: Conclusions drawn from 5-seed experiments may not be robust. The "all LISTA vs. OMP differences are significant (p < 0.01)" claim in Table 1 caption is based on 5 paired observations — with such small n, even large real differences may not reach significance, and the p-values may be unstable.
**Suggestion**: Either (a) increase the core experiments to 20 seeds (consistent with the ablation), or (b) add a power analysis showing that 5 seeds provide adequate power for the effect sizes observed, or (c) explicitly caveat that the 5-seed results are preliminary and the 20-seed ablation provides the definitive statistical evidence.
**Severity**: Major

### W2: Multiple Comparisons Not Addressed
**Problem**: The paper conducts numerous hypothesis tests: Table 1 (9 SNR points × LISTA vs. OMP), Table 9 (7 SNR points), Table 10 (7 SNR points × LISTA vs. OMP), Table 11 (3 ablation comparisons), Table 8 (4 SNR points). No correction for multiple comparisons (e.g., Bonferroni, Holm-Bonferroni, FDR) is applied.
**Why it matters**: With ~30+ hypothesis tests, the probability of at least one false positive is high (family-wise error rate ≈ 1 - 0.95^30 ≈ 0.78 at α = 0.05 per test). Some reported "significant" results may be false positives.
**Suggestion**: Apply Holm-Bonferroni correction within each table (family of tests). At minimum, report the number of tests conducted and note that no correction was applied, so readers can interpret p-values with appropriate caution.
**Severity**: Major

### W3: Mixed-SNR Training Confounds NMSE Interpretation
**Problem**: LISTA is trained with mixed SNR sampling (SNR ∈ [0, 30] dB), producing a single model evaluated across all SNR levels. This is practical but confounds the interpretation: when LISTA saturates at -25 dB for SNR ≥ 10 dB, is this because (a) the architecture cannot represent finer details, (b) the scale-invariant loss compromises across noise levels, or (c) the optimizer settles at a local minimum? The paper argues (b) but does not definitively rule out (a) and (c).
**Why it matters**: The distinction matters for the paper's argument that the saturation is a "training artifact" rather than an "architectural limitation." The SNR-specific training experiment (Table 13) supports (b), but a control experiment training with MSE loss (not scale-invariant) would strengthen the argument.
**Suggestion**: Consider adding a control experiment with MSE loss (not NMSE) to test whether the scale-invariant property is indeed the cause of saturation. If MSE-trained LISTA does not saturate, the "training artifact" argument is strongly supported.
**Severity**: Minor

### W4: Error Structure Analysis at Single Configuration Only
**Problem**: The error sparsity analysis (Table 12) is conducted at a single configuration (N=64, K=5, M=256, SNR=20 dB). The paper acknowledges this limitation in Section 4.12 ("Extension to different sparsity levels and pilot ratios remains future work") but the mechanism analysis — which is the paper's primary contribution — rests entirely on this single configuration.
**Why it matters**: The error concentration (99.9% vs. 94.9%) may not hold at different sparsity levels, SNR values, or channel lengths. The ITU generalization (Table 14) is helpful but still uses the same N, K, M configuration.
**Suggestion**: Add error sparsity analysis at one or two additional configurations (e.g., K=2 and K=10, or SNR=10 dB) to demonstrate that the mechanism is robust. This would significantly strengthen the "mechanism analysis" contribution.
**Severity**: Major

---

## Detailed Comments

### Research Questions & Hypotheses
- The paper does not state explicit hypotheses but presents 6 clear contributions. The research questions are implicit: "What does LISTA learn?", "Why does LISTA achieve competitive BER despite worse NMSE?", "How does LISTA generalize?" These are clear and answerable.

### Research Design
- The experimental design is comprehensive and well-structured. The progression from basic NMSE comparison to mechanism analysis to ablation to generalization is logical.
- The use of independent training/test splits with different random seeds is appropriate.

### Sampling Strategy
- 10,000 training / 2,000 validation / 2,000 test samples is adequate for the channel estimation task.
- 200 channel realizations per BER SNR point is sufficient for reliable BER estimation.

### Data Collection
- Synthetic data generation is well-described with clear parameter specifications.
- The ITU channel models are properly referenced and implemented.

### Analysis Methods
- Paired t-tests are appropriate for the paired experimental design.
- Cohen's d is correctly computed and interpreted.
- The NMSE metric is standard for channel estimation evaluation.

### Results Presentation
- Tables are well-formatted with mean ± std notation.
- The "Bold = best per row" convention is clear.
- Footnotes explaining cross-table differences are helpful.

### Reproducibility
- Code availability is not explicitly stated. The paper should include a data/code availability statement.
- Hyperparameter specifications are detailed enough for replication.
- Random seed specifications (5 or 20 seeds) enable reproducibility.

### Methodological Fallacies Detected
- **Survivorship bias (minor)**: The ablation study reports the best-performing configuration but does not report failed training runs (e.g., how many seeds diverged for each ablation configuration).
- **Multiple comparisons (moderate)**: As noted in W2, numerous hypothesis tests without correction.

---

## Questions for Authors

1. How many seeds (out of 5 or 20) diverged or produced anomalous results for each ablation configuration? Reporting failed runs would strengthen the ablation analysis.
2. Have you considered applying Holm-Bonferroni correction to the p-values in Tables 1, 9, 10, and 11? If not, please either apply corrections or explicitly note that no correction was applied.
3. For the cross-table consistency issue: can you provide a single experiment that evaluates LISTA under both training protocols (mixed-SNR and channel-length variation) at the same configuration, with the same number of seeds, to isolate the training distribution effect?
4. Can the error sparsity analysis (Table 12) be extended to at least one additional configuration (e.g., K=10 or SNR=10 dB) to demonstrate mechanism robustness?

---

## Minor Issues

- Table 1 caption: "all LISTA vs. OMP differences are significant (p < 0.01) except SNR=5 dB (p = 0.24)" — with n=5, these p-values should be interpreted cautiously. Consider adding a caveat.
- Table 2: "One seed diverged (positive NMSE)" at K=15 — please report which seed and whether this affected the mean ± std calculation.
- Section 4.4: "Training is stable at all depths (std < 0.8 dB)" — this is based on 5 seeds. With 20 seeds, the std may be larger.
- The NMSE loss equation (Eq. 7) uses ε = 10^-10; consider reporting whether results are sensitive to this choice.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | The mechanism analysis framing is useful but the core finding may be inherent to soft-thresholding |
| Methodological Rigor (25%) | 72 | Adequate-Strong | Good paired design and effect sizes; 5-seed core experiments and missing multiple comparisons are concerns |
| Evidence Sufficiency (25%) | 78 | Strong | Comprehensive experiments; error structure analysis at single configuration is a gap |
| Argument Coherence (15%) | 80 | Strong | Clear logical structure; conclusions generally follow from evidence |
| Writing Quality (15%) | 82 | Strong | Professional and well-organized; minor verbosity |
| **Weighted Average** | **76** | **Minor Revision** | |
