Now I have thoroughly read the paper and all relevant source code. Let me compile the complete peer review report.

---

# Peer Review Report -- Reviewer 1 (Methodology Expert)

**Paper:** "Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation"

**Author:** Huanjie Yu, Hunan University of Technology and Business

**Target Journal:** Digital Signal Processing (Elsevier)

**Recommendation:** Accept with Minor Revisions

---

## 1. Summary

This paper provides a systematic empirical analysis of LISTA (Learned ISTA) applied to sparse channel estimation. Rather than claiming architectural novelty, the paper focuses on understanding LISTA's behavior through: (1) comprehensive NMSE benchmarking against OMP, LASSO, FISTA, LMS, and NLMS; (2) a mechanism analysis explaining why LISTA achieves competitive BER despite worse NMSE -- namely, that LISTA concentrates 100.0% of estimation error on true tap locations; (3) a 20-seed ablation study with Holm-Bonferroni correction; and (4) generalization experiments across sparsity, SNR, channel length, and ITU channel models. The paper is notably honest about LISTA's limitations: NMSE saturates at approximately -25 dB, FISTA outperforms LISTA at all SNR levels, and the error concentration mechanism is partially generic to soft-thresholding.

---

## 2. Strengths

**S1. Exceptional statistical rigor.** The paper is one of the better examples of empirical methodology I have reviewed in the deep unfolding literature. The use of paired t-tests with Holm-Bonferroni correction, Cohen's d effect sizes, 200 channel realizations per BER point, and the explicit escalation from 5-seed to 20-seed ablation to address power concerns (Section 4.11) demonstrates mature experimental practice. The paper honestly reports when corrections render results non-significant (e.g., Table 4, SNR=5 dB, p=0.24).

**S2. Novel mechanism analysis.** The error concentration analysis (Section 4.12, Eq. 11) is a genuine contribution. The finding that LISTA concentrates 100.0% +/- 0.0% of error on true taps versus 95.2% +/- 0.6% for OMP and 92.4% +/- 0.4% for ISTA provides interpretable insight into why NMSE and BER can diverge. The ISTA control experiment (Section 4.12.3) correctly identifies that the mechanism is partially generic to soft-thresholding while quantifying the incremental benefit of learned parameters.

**S3. Transparent reporting of negative results.** The paper reports that FISTA outperforms LISTA by 1-27 dB (Table 12), that LISTA-CP shows identical performance because weight clipping is never activated (Table 9), and that LISTA training diverges at N=256 (Table 5). This level of honesty strengthens credibility.

**S4. Fair baseline treatment.** OMP uses oracle K, LASSO uses grid-searched lambda, and LMS/NLMS use grid-searched step sizes -- all optimized per SNR. This is fairer than many deep unfolding papers that compare against poorly tuned baselines.

**S5. Cross-table consistency explanation.** The paper proactively addresses the 8 dB discrepancy between Table 1 and Table 5 at the same nominal configuration (N=64, K=5, M=256, L=20, SNR=20 dB), attributing it to different training protocols (mixed-SNR vs. channel-length variation) and dedicating Table 6 to consolidate this finding.

**S6. Reproducibility infrastructure.** The code is well-structured with clear separation between model definitions (`ssm_af.py`), data generation (`generate.py`), and experiment scripts. The ablation variants (`LISTANoW`, `LISTAFixedThreshold`, `LISTASharedParams`) are cleanly implemented with shared forward pass logic.

---

## 3. Weaknesses

### Methodology

**W1. Zero standard deviation in the error concentration metric raises degenerate statistics concerns.**

Location: Tables 10, 11, 13, Section 4.12.

The paper reports LISTA's error on true taps as "100.0% +/- 0.0%" with 95% CI [100.0, 100.0]. This arises because the metric (Eq. 11) is defined as 100% when total error is zero (perfect recovery), and near-zero non-support errors produce ratios at or above 100% due to floating-point arithmetic. With zero variance, the standard deviation, confidence interval, and any parametric test comparing this quantity are degenerate. The paper does not report a formal statistical test comparing LISTA's 100.0% to OMP's 95.2% or ISTA's 92.4%, likely because the zero-variance LISTA distribution invalidates a standard t-test.

Proposed fix: Report the complementary metric (error on non-support taps, in dB or log scale) as the primary comparison quantity, since this has non-degenerate variance (LISTA: 0.01% +/- 0.01%, OMP: 4.81% +/- 0.59%). A Wilcoxon rank-sum test or a permutation test on the non-support error fraction would provide valid p-values for the LISTA-vs-OMP and LISTA-vs-ISTA comparisons. Additionally, report the per-sample NMSE alongside the error concentration to verify that 100% concentration does not merely reflect zero total estimation error (which would trivially produce any concentration ratio).

**W2. The training/test split description in the paper does not match the code.**

Location: Section 4.1 ("Data Generation") vs. `train_sparse.py` and `run_revision_experiments.py`.

The paper states "We generate 10,000 training samples, 2,000 validation samples, and 2,000 test samples" (Section 4.1). However, the training code (`run_revision_experiments.py`, line 237-256) generates fresh training data each epoch via `generate_sparse_channel_data(num_samples=batch_size)`, meaning training uses 64 samples per epoch with no persistent dataset. The test set in the revision experiments uses 200 samples (`num_test=200`), not 2,000. The 10,000/2,000/2,000 split described in the paper appears to apply only to the original experiments (`run_experiments.py`), not to the revision experiments that constitute the bulk of the reported results.

Proposed fix: Clarify in Section 4.1 which experiments use which data generation protocol. State explicitly that LISTA training generates fresh data each epoch (a form of data augmentation), and report the actual test set sizes used in each experiment. This distinction matters for reproducibility: a reader attempting to reproduce Table 11 (ablation) would need to know that test data is 200 samples, not 2,000.

**W3. Baseline hyperparameters are optimized on test data, not a held-out validation set.**

Location: `run_revision_experiments.py`, `evaluate_baselines()` function (lines 260-330).

The grid search for LASSO lambda, LMS mu, and NLMS mu is performed directly on the test set (`x_test, d_test, h_test`). This means baselines are optimized on the same data used for evaluation, which introduces optimistic bias. The paper mentions "optimizing hyperparameters via grid search on the validation set" (Section 4.1), but the code does not implement a separate validation set for baseline tuning.

Proposed fix: Generate a separate validation set (e.g., 500 samples) for baseline hyperparameter selection, then evaluate on the held-out test set. Alternatively, if the test-set optimization is intentional (e.g., to give baselines the best possible chance against LISTA), state this explicitly and note that it biases results in favor of baselines.

**W4. The 200 BER realizations per SNR point may be insufficient for reliable paired tests at low error rates.**

Location: Section 4.10, Tables 7, 8.

At SNR=30 dB, the reported BER is approximately 0.0003. With 200 realizations, the expected number of bit errors is approximately 0.06, meaning most realizations will observe zero errors. The paired t-test on proportions with many zero-error observations has reduced power and may produce unreliable p-values. The paper reports p=0.10 at SNR=30 dB for LISTA vs. OMP under MMSE, but the confidence in this non-significance is limited by the low error count.

Proposed fix: For high-SNR points (>= 25 dB), increase the number of bits per realization (e.g., by simulating longer transmissions) to ensure at least 100 bit errors per realization, or use an exact binomial test rather than a paired t-test. Alternatively, acknowledge in the text that BER comparisons at SNR >= 25 dB have limited statistical power due to low error counts.

**W5. The paper does not report the number of bits simulated per realization.**

Location: Section 4.10.

The BER tables report results over "200 channel realizations per SNR point" but do not specify how many bits are transmitted per realization. If each realization uses a single OFDM symbol with N=64 subcarriers, this would be only 64 bits per realization -- far too few for reliable BER estimation at moderate-to-high SNR. The code is not available for the BER simulation, so this cannot be verified from the repository.

Proposed fix: State explicitly in Section 4.10 how many bits are simulated per channel realization and per SNR point in total.

**W6. The LISTA code uses a different gradient normalization than standard ISTA.**

Location: `ssm_af.py`, line 641; paper Eq. (3).

The LISTA implementation divides the gradient by `pilot_len` (line 641: `grad = torch.bmm(A.transpose(1, 2), residual).squeeze(-1) / pilot_len`), while the standard ISTA formulation (Eq. 3) does not include this normalization. The step size mu^(k) absorbs this factor, but it means that LISTA's learned step sizes are not directly comparable to the theoretical ISTA step size (1/Lipschitz constant). This is not necessarily wrong -- it is a common implementation choice -- but it should be documented because it affects the interpretation of the ablation results. When the step size is fixed (ablation "Fixed threshold" variant), the remaining learnable step size still absorbs the pilot-length normalization, making the comparison with standard ISTA's fixed step size (which uses the un-normalized gradient) potentially unfair.

Proposed fix: Note in Section 3.3 that the gradient is normalized by pilot length M, and discuss how this affects the interpretation of the learned step sizes relative to theoretical ISTA. Consider whether the ISTA baseline in Section 4.12.3 uses the same normalization for a fair comparison.

### Experimental Design

**W7. The FISTA baseline uses a grid-searched threshold while LISTA uses a learned threshold, creating an asymmetric comparison.**

Location: Section 4.1 ("Baselines"), Table 12.

FISTA's threshold is grid-searched over {0.001, 0.005, 0.01, 0.02, 0.05, 0.1} on the test set, while LISTA's threshold is learned during training. This means FISTA benefits from test-set optimization while LISTA does not. A fairer comparison would either: (a) grid-search FISTA's threshold on a validation set, or (b) also report LISTA's performance with grid-searched parameters. As stated, the comparison may overstate FISTA's advantage.

Proposed fix: Report FISTA with both validation-optimized and test-optimized thresholds. Note in the text that FISTA's grid search is performed on the test set.

**W8. The pilot ratio analysis (Table 6) uses a different training protocol than the main experiments.**

Location: Section 4.3, Table 6.

Table 6 reports LISTA results with mixed-SNR training but does not specify whether the training data uses the same pilot length as the test data at each M/N ratio. If LISTA is always trained with M=256 and tested at smaller M, the comparison is unfair. If LISTA is retrained for each M, this should be stated explicitly.

Proposed fix: Clarify in the Table 6 caption or Section 4.3 whether LISTA is retrained for each pilot ratio M/N or uses a single model trained at M=256.

### Reproducibility

**W9. Non-determinism in training due to fresh data generation each epoch.**

Location: `run_revision_experiments.py`, `train_model()` function (line 237).

While random seeds are set (`torch.manual_seed(seed * 42)`), the training loop generates fresh data each epoch via `generate_sparse_channel_data()`. This means that even with the same seed, the exact training trajectory depends on the order of random number consumption, which can vary across PyTorch versions, GPU architectures, or even CUDA library versions. The paper reports results over 5 or 20 seeds, which mitigates this for aggregate statistics, but individual seed results may not be exactly reproducible.

Proposed fix: Acknowledge in Section 4.1 that exact reproducibility requires specifying the PyTorch version, CUDA version, and GPU model. Consider pre-generating and saving all training data to ensure full determinism.

**W10. Missing BER simulation code.**

The repository contains code for NMSE experiments (`run_experiments.py`, `run_revision_experiments.py`) but does not include the BER simulation code. The BER results (Tables 7, 8, 9) cannot be independently verified from the provided codebase.

Proposed fix: Include the BER simulation script in the repository.

---

## 4. Detailed Comments on Specific Claims

**C1. "LISTA concentrates 100.0% +/- 0.0% of error on true taps" (Abstract).** As noted in W1, this claim is technically correct but the zero standard deviation makes it impossible to construct a valid confidence interval or perform a statistical test. The claim would be strengthened by reporting the non-support error fraction (0.01% +/- 0.01%) with a formal test against OMP (4.81% +/- 0.59%).

**C2. "Placing 267x less error on non-support taps than OMP" (Abstract).** This ratio (5.33%/0.02%) is computed from Table 11 means. However, the 0.02% denominator has std=0.02%, meaning some seeds may have near-zero non-support error, inflating the ratio. Reporting the ratio with a bootstrap confidence interval would be more informative.

**C3. "SNR-specific training mitigates saturation: -31 dB at SNR=20 dB (6 dB improvement)" (Section 4.9, Table 14).** This is a strong result. However, the improvement comes at the cost of losing robustness across SNR levels -- the narrow-range model would perform poorly outside its training range. The paper acknowledges this tradeoff (Section 4.9, paragraph 3), which is appropriate.

**C4. "All three components are significant" in the 20-seed ablation (Table 11).** The reported p-values are all < 0.001 after Holm-Bonferroni correction (m=3). With n=20 paired observations and the reported effect sizes (d=1.5, 18.4, 24.1), these results are credible. The escalation from the 5-seed ablation (where threshold and per-layer appeared insignificant) to the 20-seed ablation (where all are highly significant) is a textbook example of statistical power analysis in practice.

**C5. "FISTA with 20 iterations outperforms LISTA at all SNR levels" (Table 12).** This is an important negative result. The gap widening from ~1 dB at SNR=-5 dB to ~27 dB at SNR=40 dB is consistent with LISTA's saturation at -25 dB versus FISTA's continued improvement. The paper correctly notes that this means "LISTA's learned parameters do not provide improvement over standard accelerated ISTA in terms of NMSE" (Section 4.12.4).

---

## 5. Questions for the Authors

Q1. Can you provide the BER simulation code and specify the number of bits per realization?

Q2. In Table 11 (ablation), what is the NMSE distribution for the "Shared parameters" configuration? The std of 0.31 dB with mean -6.69 dB suggests very tight clustering. Is this because all 20 seeds converge to nearly identical local minima?

Q3. The error concentration metric reports 100.0% for LISTA at K=5. What happens at K=1 and K=2, where the channel is even sparser? Does the metric remain at 100%?

Q4. Have you verified that the FISTA implementation (Eq. 3 + Nesterov momentum) matches the standard FISTA algorithm (Beck & Teboulle, 2009)? The code in `ssm_af.py` lines 801-829 implements the momentum correctly, but the threshold grid search uses a fixed threshold rather than the lambda*step product that LASSO uses.

Q5. The paper mentions "200 channel realizations per SNR point" for BER. How many bits are transmitted per channel realization? This is critical for interpreting the BER statistical power.

---

## 6. Minor Issues

M1. Table 5 footnote says "Pilot ratio M/N varies: 8 (N=32), 4 (N=64), 2 (N=128), 1 (N=256)" but the paper text says "fixed M=256." These are consistent but the footnote could be clearer.

M2. The paper uses both "5 seeds" and "20 seeds" for different experiments. A summary table listing which experiments use how many seeds would aid readability.

M3. The code sets `torch.manual_seed(seed * 42)` rather than `torch.manual_seed(seed)`. This is fine but unconventional. Documenting the rationale (e.g., to avoid seed 0 producing degenerate results) would help.

M4. In `run_revision_experiments.py`, the ITU channel experiment (line 748) calls `model.eval()` twice. This is harmless but suggests copy-paste.

M5. The paper's Table 1 footnote says "LASSO convergence verified: relative change < 10^{-4} at iteration 500 across all SNR levels" but the code (`ssm_af.py`, LASSOFilter) uses only 200 iterations (line 744: `for _ in range(200)`). This discrepancy should be reconciled.

---

## 7. Scores

| Dimension | Score (0-100) | Justification |
|---|---|---|
| **Originality** | 68 | No architectural novelty, but the error concentration mechanism analysis and the systematic ablation with statistical rigor are genuine contributions to the deep unfolding literature. The ISTA control experiment is a thoughtful design choice. |
| **Significance** | 72 | The finding that LISTA's NMSE saturates and FISTA outperforms it is important for the field. The error concentration mechanism provides interpretable insight. However, the practical impact is limited by the real-valued-only setting and the lack of hardware validation. |
| **Rigor** | 82 | Strong statistical methodology (paired tests, effect sizes, multiple comparison correction, power analysis). The escalation from 5-seed to 20-seed ablation is exemplary. Deductions for the baseline hyperparameter optimization on test data (W3), the degenerate statistics on the error concentration metric (W1), and the missing BER simulation code (W10). |
| **Clarity** | 80 | The paper is well-structured with clear section organization. The cross-table consistency explanation (Section 4.3) and the explicit discussion of limitations (Section 5.4) are commendable. Some tables are dense and the paper could benefit from a summary figure showing the key takeaways. |
| **Reproducibility** | 70 | Code is available and well-structured, but the training/test split discrepancy (W2), the missing BER code (W10), and the non-determinism from fresh data generation (W9) limit full reproducibility. The paper would benefit from a requirements.txt or environment specification. |
| **Methodology** | 79 | Excellent statistical framework with appropriate corrections and effect sizes. Deductions for test-set baseline optimization (W3), insufficient BER samples at high SNR (W4), and the asymmetric FISTA comparison (W7). The experimental design is generally sound with good coverage of operating conditions. |

**Overall Score: 76/100**

---

## 8. Final Assessment

This is a methodologically strong paper that makes a genuine contribution to understanding deep-unfolded sparse channel estimation. Its primary strengths are the rigorous statistical framework, the novel error concentration mechanism analysis, and the honest reporting of LISTA's limitations. The primary weaknesses are technical issues in the statistical treatment of the error concentration metric (degenerate zero-variance statistics), the baseline optimization on test data, and missing details in the BER simulation methodology.

The paper is well-suited for Digital Signal Processing, which values both algorithmic contributions and rigorous empirical analysis. With the minor revisions addressing the specific issues identified above (particularly W1, W2, W3, and W4), this would be a solid publication that advances the community's understanding of when and why deep-unfolded architectures work for channel estimation.