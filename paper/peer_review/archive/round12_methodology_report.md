# Peer Review Report — Peer Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 12

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology Expert

### Reviewer Identity
Prof. Kai Zhang, Associate Professor of Electrical Engineering. Expertise in deep learning architectures for signal processing, statistical experimental design, and reproducibility in computational research. Published extensively on deep unfolding and model-based deep learning. Focus: research design rigor, statistical validity, reproducibility.

### Review Focus
Research design appropriateness, statistical methodology, experimental validity, reproducibility, and completeness of methodological reporting. This review examines whether the experimental design supports the paper's claims and whether the statistical analyses are appropriate.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
5 — Deep unfolding architectures and statistical experimental design are directly within my expertise. I have published on LISTA variants and am familiar with the methodological pitfalls in this area.

### Summary Assessment
This paper provides a methodologically sound analysis of LISTA for sparse channel estimation. The experimental design is comprehensive, covering 12 experiments with appropriate baselines and evaluation metrics. The statistical methodology is a notable strength: the progression from 5-seed to 20-seed ablation with paired t-tests, Wilcoxon signed-rank tests, and Cohen's $d$ effect sizes demonstrates awareness of statistical power issues. The BER simulations with 200 realizations and paired tests are well above the field standard. However, there are several methodological concerns: (1) the cross-table inconsistency between Tables 3 and 4, while explained, reveals sensitivity to training distribution that should be a first-class result; (2) the OMP baseline uses oracle K, which may overstate OMP's advantage in practice; (3) the LASSO baseline uses 500 ISTA iterations, which may not converge for all configurations; (4) the hardware complexity analysis is theoretical without measured results. These are addressable issues that do not invalidate the findings but should be discussed. The paper's self-critical approach—transparently reporting when initial experiments were underpowered—is commendable and sets a good example for the field.

---

## Strengths

### S1: Statistical Power Awareness and Self-Correction
The paper transparently reports that the initial 5-seed ablation (Table 5) had "limited statistical power (~15–20% for medium effects)" and self-corrects with a 20-seed experiment (Table 8). This self-correction—admitting that the Round 2 finding of "not individually significant" for threshold parameters was "a false negative attributable to low statistical power"—is rare and commendable. The 20-seed experiment includes both parametric (paired t-test) and non-parametric (Wilcoxon signed-rank) tests, with Cohen's $d$ effect sizes. The effect sizes are remarkably large ($d = 18.4$ for threshold, $d = 24.1$ for shared parameters), confirming the findings are robust.

### S2: BER Simulation Design with Paired Statistical Tests
The BER simulations (Section 4.10) use 200 independent channel realizations per SNR point with paired t-tests—significantly more rigorous than the typical 50–100 realizations in this field. The use of paired tests (same channel realizations and noise instances for all methods at each SNR point) controls for channel-to-channel variability and increases statistical power. The reporting of confidence intervals and $p$-values with significance markers follows APA 7.0 conventions.

### S3: Comprehensive Baseline Selection with Grid-Search Optimization
The baselines (LMS, NLMS, OMP, LASSO) are appropriate and well-optimized. Hyperparameters are selected via grid search on the validation set (Section 4.1), with per-SNR optimization for LMS/NLMS step sizes and LASSO regularization parameter. The OMP baseline uses oracle K (known sparsity level), which is clearly stated. This is a fair comparison setting, though it advantages OMP (see W1).

### S4: Transparent Reporting of Training Protocol Sensitivity
The paper explicitly documents the 8 dB difference between Tables 3 and 4, attributing it to different training distributions (mixed-SNR vs. channel-length variation). The footnote in Table 4 and the detailed explanation in Section 4.3 provide full transparency. The recommendation to treat the mixed-SNR model (Table 3) as "the primary reference for LISTA's practical performance" is appropriate.

### S5: Reproducibility Infrastructure
The paper reports all training details: Adam optimizer with LR $5 \times 10^{-4}$, weight decay $10^{-5}$, cosine annealing, gradient clipping (max norm 5.0), batch size 256, 200 epochs, mixed SNR $[0, 30]$ dB. The code appears to be available (based on the project structure). All results report mean $\pm$ std over seeds.

---

## Weaknesses

### W1: OMP Baseline Uses Oracle Sparsity Level
**Problem**: OMP is evaluated with known sparsity level $K$ (oracle setting, Section 4.1). In practice, $K$ is unknown and must be estimated, which introduces additional error. The paper does not evaluate OMP with estimated $K$ (e.g., via cross-validation or information criteria).
**Why it matters**: The oracle K setting overstates OMP's practical advantage. If OMP with estimated K shows degraded performance, the LISTA-OMP gap would be smaller than reported, strengthening the paper's argument for LISTA.
**Suggestion**: Add a supplementary experiment with OMP using estimated K (e.g., via cross-validation or BIC). At minimum, acknowledge this as a limitation in Section 5.4.
**Severity**: Major

### W2: LASSO Convergence Not Verified
**Problem**: LASSO is solved via ISTA with 500 iterations (Section 4.1). For some configurations (especially high SNR where the solution is very sparse), 500 iterations may not be sufficient for convergence. The paper does not report convergence diagnostics (e.g., change in solution between iterations).
**Why it matters**: If LASSO has not converged, its NMSE values may be artificially high, making LISTA look better by comparison.
**Suggestion**: Add a convergence check: report the relative change $\|\mathbf{h}^{(k)} - \mathbf{h}^{(k-1)}\| / \|\mathbf{h}^{(k)}\|$ at iteration 500 for representative configurations. If convergence is not achieved, increase iterations or switch to FISTA.
**Severity**: Major

### W3: Training-Test Data Split Not Independently Seeded
**Problem**: The paper uses 10,000 training, 2,000 validation, and 2,000 test samples (Section 4.1), but does not specify whether the data splits are independently generated or whether the same channel realizations are reused across experiments. If the same test set is used for all experiments, the results may be correlated.
**Why it matters**: Correlated test sets could inflate the apparent consistency of results across experiments.
**Suggestion**: Clarify whether test sets are independently generated for each experiment. If the same test set is used, acknowledge the potential for cross-experiment correlation.
**Severity**: Minor

### W4: No Confidence Intervals on BER Results
**Problem**: BER results in Tables 9-11 report mean $\pm$ std over 5 seeds, but the standard deviation is quite small (e.g., $\pm 0.0003$ at SNR=20). The paper reports $p$-values from paired t-tests but does not report 95% confidence intervals for the BER differences.
**Why it matters**: Confidence intervals would provide more informative error bounds than $p$-values alone, especially for the ZF equalization results where the BER differences are small.
**Suggestion**: Add 95% confidence intervals for the LISTA-OMP BER differences at each SNR point. This would help readers assess the practical significance of the statistical significance.
**Severity**: Minor

### W5: Random Seed Reporting
**Problem**: The paper reports "5 random seeds" and "20 random seeds" for different experiments but does not specify the actual seed values or whether seeds are shared across methods within an experiment.
**Why it matters**: For reproducibility, seed values should be reported or the code should be available with seed-setting functionality.
**Suggestion**: Report the seed values in the supplementary material, or confirm that the code repository includes seed-setting functionality for full reproducibility.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title accurately reflects the methodology: "Systematic Analysis" with "Generalization, Error Structure, and Ablation."
- Abstract correctly highlights the statistical methodology (200 realizations, paired t-tests, 20 seeds).

### Methodology (Section 3)
- The LISTA architecture description (Section 3.3) is clear and follows the standard formulation.
- The parameter analysis (Section 3.4) is useful: $N_{\text{params}} = L \times (N^2 + 2)$ correctly identifies the $O(N^2)$ scaling concern.
- The training details (Section 3.5) are comprehensive. The mixed-SNR training protocol is well-motivated.
- The computational complexity analysis (Section 3.6) is adequate but could be more detailed about the FFT-based convolution implementation.

### Experimental Design (Section 4)
- **Experiment 1 (NMSE vs SNR)**: Good sweep from -5 to 40 dB, covering both in-distribution and out-of-distribution SNR. The -5 and 40 dB points test generalization.
- **Experiment 2 (NMSE vs Sparsity)**: Appropriate range K=2 to 15. The divergence at K=15 is correctly reported.
- **Experiment 3 (NMSE vs Channel Length)**: The cross-table inconsistency is well-documented. The pilot ratio variation (M/N from 8 to 1) is a confound—see W1.
- **Experiment 4 (Depth Analysis)**: Good sweep from L=1 to 20. The plateau at L=10 is a useful practical finding.
- **Experiment 5 (Ablation)**: The 4-config ablation is well-designed. The progression from 5 to 20 seeds is the paper's methodological highlight.
- **Experiment 6 (Generalization)**: Sparsity and SNR mismatch are tested. Channel-length mismatch is implicit in Experiment 3.
- **Experiment 7 (Practical Deployment)**: Inference time comparison is useful but the Python vs. hardware distinction needs clearer framing.
- **Experiment 8 (LISTA-CP)**: Well-designed comparison. The diagnostic of weight clipping never being activated is insightful.
- **Experiment 9 (SNR Mitigation)**: The 3 narrow-range strategies are a good design. The finding that range width matters more than location is useful.
- **Experiment 10 (BER)**: Excellent design with 200 realizations and paired tests.
- **Experiment 11 (20-seed Ablation)**: The self-correction from Experiment 5 is commendable.
- **Experiment 12 (Mechanism Analysis)**: The error sparsity analysis is novel. The Gini coefficient and support/non-support decomposition are appropriate metrics.

### Results Reporting
- Tables are well-formatted with clear captions, footnotes, and statistical annotations.
- The use of bold for best-performing method per row is helpful.
- The paired t-test annotations ($p < 0.01$, $p < 0.05$) follow standard conventions.

### Discussion (Section 5)
- The training artifact hypothesis for NMSE saturation (Section 5.1) is well-argued with three pieces of evidence.
- The qualitative CNN/Transformer comparison (Section 5.2) is appropriately caveated as "indirect."
- The limitations section (Section 5.4) is thorough.

---

## Questions for Authors

1. **LASSO convergence**: Can you report the relative change in the LASSO solution at iteration 500 for at least the SNR=20 and SNR=40 configurations? If convergence is not achieved, the LASSO NMSE values may be artificially high.

2. **OMP with estimated K**: Have you considered evaluating OMP with an estimated sparsity level (e.g., via cross-validation or BIC)? This would provide a more realistic comparison, as K is typically unknown in practice.

3. **Pilot ratio confound in Experiment 3**: In Table 4, the pilot ratio M/N varies from 8 (N=32) to 1 (N=256). Can you disentangle the effects of channel length from pilot ratio? For example, fixing M/N=4 and varying N would isolate the channel length effect.

4. **Weight clipping distribution in LISTA-CP**: You report that $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ never exceeded 0.35. Can you report the distribution of spectral norms across all 20 layers and 5 seeds? This would help assess whether the constraint is close to activation or far from it.

---

## Minor Issues

### Language / Grammar
- Section 4.3, paragraph 2: "The channel-length training distribution is narrower and more focused" — "narrower" is ambiguous; specify that it means "covering a smaller range of N values."
- Section 4.12.4: "The NMSE metric is insensitive to error location, while BER is sensitive to it" — good insight, but consider adding a brief mathematical justification.

### Citation Format
- Reference [Kim et al., 2021] (FPGA survey) appears to have placeholder page numbers: "123456--123470." Verify and correct.
- The citation for LISTA-CP [Chen et al., 2018] uses the CVPR Workshops venue, but the paper title suggests a journal version may exist. Verify the correct citation.

### Figures and Tables
- Table 4 footnote: The cross-table explanation is good but could be moved to the main text for better visibility.
- Consider adding error bars to Figure 1 (NMSE vs SNR) to show the std across seeds.

### Layout
- No significant layout issues. The Elsevier CAS template is used correctly.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | The systematic analysis approach is valuable but not novel. The error concentration mechanism is the key original contribution. |
| Methodological Rigor (25%) | 80 | Strong | Excellent statistical methodology with self-correction. Minor concerns about LASSO convergence and oracle K for OMP. |
| Evidence Sufficiency (25%) | 72 | Adequate | Good evidence for main claims, but limited to one primary configuration. Hardware claims are theoretical. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow. The self-critical framing strengthens the argument. The mechanism analysis provides a coherent narrative. |
| Writing Quality (15%) | 82 | Strong | Clear, well-organized writing. Good use of tables and statistical annotations. Minor verbosity in some sections. |
| **Weighted Average** | **76.8** | **Minor Revision** | |

---

## Overall Score: 77/100
