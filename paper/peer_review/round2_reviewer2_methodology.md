# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 2

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Dr. Marcus Chen, Associate Professor, Department of Electrical and Computer Engineering, University of Toronto. Specialization: deep unfolding architectures, algorithm unrolling for inverse problems, statistical methodology in machine learning research. Author of 40+ papers on learned optimization. Reviewer for IEEE TSP, IEEE JSTSP, NeurIPS, ICML.

### Review Focus
Research design rigor, statistical validity, reproducibility, and methodological soundness. I evaluate whether the experimental design supports the claims, whether the statistical analysis is appropriate, and whether the results are reproducible from the information provided.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
5 — Deep unfolding and statistical methodology are squarely within my expertise. I have published on LISTA variants and am very familiar with the methodological standards expected in this area.

### Summary Assessment
This paper provides a systematic experimental evaluation of LISTA for sparse channel estimation, covering 9 experiments with ablation, generalization, and practical deployment analyses. The methodological framework is generally sound: baselines are grid-searched, multiple seeds are used, and the ablation includes statistical significance testing with effect sizes. However, several methodological issues weaken the paper: (1) the statistical power with n=5 seeds is insufficient for the paired t-tests claimed, (2) the LISTA-CP comparison yields identical results which raises implementation concerns, (3) the NMSE saturation analysis lacks a rigorous theoretical explanation, and (4) the scale-invariant loss explanation is asserted but not validated experimentally. The paper would benefit from deeper methodological analysis of the saturation phenomenon and stronger statistical evidence. I recommend Major Revision.

---

## Strengths

### S1: Fair Baseline Comparison with Grid Search
The paper optimizes baseline hyperparameters (LMS step size, NLMS step size, LASSO λ) via grid search on the validation set (Section 4.1). This is the correct approach and avoids the common pitfall of comparing against poorly tuned baselines. The grid ranges are reasonable and the per-SNR optimization ensures fairness.

### S2: Ablation Design with Controlled Variables
The ablation study (Section 4.5) uses four well-chosen configurations that isolate individual components: No W (identity mapping), Fixed threshold, and Shared parameters. Each configuration changes exactly one factor, enabling clean attribution of performance differences. This is textbook ablation design.

### S3: Statistical Reporting with Effect Sizes
The use of paired t-tests with Cohen's d effect sizes (Table 5) is commendable and sets a positive example for the field. The reporting of exact p-values (not just significance stars) and the inclusion of effect sizes allows readers to assess both statistical and practical significance.

### S4: Cross-Distribution Generalization Testing
Testing on ITU channel models (Section 4.7.2) with baselines optimized on i.i.d. Gaussian data is a rigorous evaluation of generalization. The decision not to re-optimize baselines for ITU channels ensures a fair comparison under realistic deployment conditions.

---

## Weaknesses

### W1: Insufficient Statistical Power (n=5 Seeds)
**Problem**: The paired t-tests in the ablation study (Table 5) use n=5 seeds. With only 5 paired observations, the t-test has very low statistical power — approximately 15-20% power to detect a medium effect size (d = 0.5) at α = 0.05. The paper reports p = 0.455 for the threshold ablation and p = 0.338 for shared parameters, but these non-significant results may simply reflect insufficient power rather than true null effects.
**Why it matters**: The paper concludes that "threshold and per-layer parameters show no individually significant effects," but this conclusion is not supported by the statistical test given the sample size. A type II error is highly likely.
**Suggestion**: Increase the number of seeds to at least 20-30 for the ablation study. Alternatively, use a more appropriate statistical test for small samples (e.g., Wilcoxon signed-rank test) and explicitly acknowledge the limited power. Report confidence intervals alongside p-values.
**Severity**: Major

### W2: LISTA-CP Identical Results Raise Implementation Concerns
**Problem**: Table 7 shows LISTA and LISTA-CP achieve identical NMSE values to the reported precision across all SNR levels. The paper claims "LISTA-CP weight constraints do not alter the learned parameters when training converges within L=20 layers," but this is an extraordinary claim that requires extraordinary evidence. LISTA-CP imposes specific weight constraints (W = I - κA^T A) that should produce different parameter trajectories during training, even if final performance is similar.
**Why it matters**: If the implementation is incorrect, the comparison is meaningless. If correct, the result needs a rigorous explanation — why do the constraints have zero effect?
**Suggestion**: (1) Verify the LISTA-CP implementation by printing the learned W matrices and checking whether they satisfy the CP constraints. (2) Test at shallower depths (L=3, 5, 8) where convergence differences should manifest. (3) Report the actual weight norms and constraint violations during training. (4) If the results are confirmed, provide a formal argument for why the constraints are inactive.
**Severity**: Major

### W3: NMSE Saturation Explanation Lacks Experimental Validation
**Problem**: The paper attributes the NMSE saturation at ~-25 dB to three factors (Section 5.1): (1) fixed-depth architecture, (2) scale-invariant NMSE loss, (3) soft-thresholding bias floor. However, none of these explanations are experimentally validated. The paper does not test: (a) whether deeper networks (>20 layers) break the saturation, (b) whether a non-scale-invariant loss (e.g., MSE without normalization) changes the saturation level, (c) whether the soft-thresholding operator is the bottleneck.
**Why it matters**: Without experimental validation, the saturation explanation is speculative. If the true cause is different, the proposed mitigation (SNR-specific training) may be addressing a symptom rather than the root cause.
**Suggestion**: Add targeted experiments: (1) train with L=40, 60 to test depth scaling; (2) compare NMSE loss vs. MSE loss; (3) replace soft-thresholding with ReLU or hard-thresholding and measure the effect. These experiments would either validate or refute the proposed explanations.
**Severity**: Major

### W4: Mixed-SNR Training Creates Confounded Ablation Results
**Problem**: The ablation study (Section 4.5) uses mixed-SNR training (SNR ∈ [0, 30] dB), but the evaluation is at a single SNR (20 dB). The paper concludes that threshold and per-layer parameters are "not individually significant," but this may be an artifact of the mixed-SNR training: the learned parameters must compromise across SNR levels, potentially washing out per-component effects that would be visible with SNR-specific training.
**Why it matters**: The ablation conclusions are training-regime-dependent. If the same ablation were conducted with SNR-specific training, the results might differ significantly.
**Suggestion**: Repeat the ablation study with SNR-specific training (e.g., SNR ∈ [18, 22]) to determine whether the threshold and per-layer parameters become significant when the training objective is not diluted across SNR levels.
**Severity**: Minor

### W5: No Confidence Intervals for NMSE Estimates
**Problem**: The paper reports mean ± std over 5 seeds but does not report confidence intervals. For n=5, the standard error is std/√5 ≈ 0.45 × std, meaning the 95% CI (using t-distribution with 4 df) is approximately mean ± 2.78 × SE. This makes many of the reported differences statistically indistinguishable.
**Why it matters**: Without confidence intervals, readers cannot assess whether observed differences (e.g., -24.96 vs. -23.96 dB in the ablation) are statistically meaningful.
**Suggestion**: Report 95% confidence intervals for all NMSE estimates. Use overlapping CI visualizations in figures where applicable.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title is descriptive. "Analysis of" correctly signals a characterization study rather than a novelty paper.
- The abstract is well-structured with quantitative results. The honest reporting of the saturation behavior is appreciated.

### Introduction
- The five contributions are clearly stated. However, contribution (1) ("systematic analysis") is not a traditional contribution — it describes the paper's methodology, not its findings.
- The research gap could be sharper. What do existing surveys leave unanswered?

### Methodology / Research Design
- The data generation (Section 4.1) is standard and well-described. The use of BPSK pilots and Gaussian tap amplitudes is appropriate for a baseline study.
- The training setup (Adam optimizer, cosine annealing, gradient clipping) is standard. The learning rate of 5×10⁻⁴ differs from the 10⁻³ mentioned in Section 3.5 — clarify which is correct.
- The mixed-SNR training protocol is well-justified for producing a single model across conditions.

### Results / Findings
- Experiment 1 (SNR sweep): The saturation is clearly demonstrated. The out-of-distribution test at SNR = -5 and 40 dB is appropriate.
- Experiment 2 (Sparsity): The divergence at K=15 is honestly reported. The std = 8.27 dB at K=15 should be discussed further.
- Experiment 3 (Channel Length): The divergence at N=256 is a significant scalability limitation. The paper should discuss this more prominently.
- Experiment 4 (Depth): The plateau at L=10 is interesting. What happens at L=30, 40?
- Experiment 5 (Ablation): The statistical analysis needs strengthening (see W1).
- Experiment 6 (Generalization): Reusing Experiment 2 results is efficient but limits the analysis.
- Experiment 7 (Practical): Good inference time analysis. The ITU channel results are informative.
- Experiment 8 (LISTA-CP): Identical results need explanation (see W2).
- Experiment 9 (SNR Mitigation): The SNR-specific training results are the most practically useful finding.

### Discussion
- Section 5.1 provides plausible explanations for the saturation but lacks experimental validation (see W3).
- Section 5.2's practical deployment framework is useful.
- Section 5.3's limitations are honestly stated.

### Conclusion
- The conclusion accurately summarizes the findings. The positioning as "when speed is prioritized" is appropriate given the results.

### References
- References are comprehensive. The inclusion of both seminal works and recent surveys is appropriate.

---

## Questions for Authors

1. **Statistical Power**: With n=5 seeds, the paired t-tests in the ablation study have very low power. Can you increase the number of seeds to at least 20 for the ablation, or alternatively use a non-parametric test and explicitly acknowledge the power limitation?

2. **LISTA-CP Implementation**: Can you verify the LISTA-CP implementation by (a) printing the learned W matrices and checking constraint satisfaction, and (b) testing at shallower depths (L=3, 5) where convergence differences should be visible?

3. **Saturation Validation**: Can you provide experimental evidence for the three proposed explanations of the NMSE saturation? Specifically: (a) does L=40 break the saturation? (b) does MSE loss (without normalization) change the saturation level? (c) does hard-thresholding instead of soft-thresholding affect the saturation?

4. **Learning Rate Discrepancy**: Section 3.5 states learning rate 10⁻³, but Section 4.1 states 5×10⁻⁴. Which is correct? Please reconcile.

---

## Minor Issues

### Language / Grammar
- Section 3.5: "learning rate 10⁻³" contradicts Section 4.1 "learning rate 5×10⁻⁴"
- Table 3: "Training diverged (3/5 seeds yield positive NMSE)" — specify which seeds

### Figures and Tables
- Table 1: The ± values are missing for most methods (only LISTA has them). Are the other methods deterministic?
- Table 5: Consider adding a column for statistical power or confidence interval width

### Layout
- No significant layout issues. The Elsevier CAS template is used correctly.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | Application of known architecture to known problem; contribution is analytical |
| Methodological Rigor (25%) | 62 | Adequate | Good design but insufficient statistical power (n=5); unvalidated saturation explanation |
| Evidence Sufficiency (25%) | 65 | Adequate | Comprehensive experiments but missing depth scaling, loss comparison, BER analysis |
| Argument Coherence (15%) | 68 | Adequate | Clear structure; saturation explanation plausible but unvalidated |
| Writing Quality (15%) | 72 | Strong | Clear, professional; minor LR discrepancy |
| **Weighted Average** | **63.8** | **Adequate** | **Major Revision recommended** |
