# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 15

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Prof.~Jianhua Zhang, Department of Electrical Engineering, Tsinghua University. Specialization: statistical signal processing, compressed sensing theory, and experimental design for communication systems. Published extensively on sparse recovery algorithms and their statistical properties. Review philosophy: methodology must be rigorous, reproducible, and honestly reported.

### Review Focus
Research design rigor, statistical validity, experimental methodology, reproducibility, and reporting completeness. I will assess whether the experimental design supports the paper's claims, whether statistical methods are appropriate, and whether results are reproducible.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
5 — This paper is squarely within my area of expertise. The statistical methodology, experimental design, and sparse recovery algorithms are all topics I work on regularly.

### Summary Assessment
This paper presents a methodologically rigorous analysis of LISTA for sparse channel estimation. The experimental design is comprehensive (12 experiments covering NMSE, BER, ablation, generalization, and practical deployment), and the statistical methodology is generally sound. The escalation from 5-seed to 20-seed ablation with Holm--Bonferroni correction and Cohen's $d$ effect sizes demonstrates strong statistical practice. The BER simulations with 200 realizations and paired $t$-tests are well-powered.

However, several methodological issues require attention: (1) the NMSE loss function's scale-invariant property is acknowledged but not formally analyzed as a confound; (2) the error concentration metric (fraction of error energy on support) needs formal definition and confidence intervals; (3) the Holm--Bonferroni correction is applied within tables but not across the paper's 12 experiments, creating a multiple-comparisons concern at the paper level; (4) the LISTA-CP comparison lacks a formal equivalence test. These are addressable issues that do not undermine the paper's core findings but should be resolved before publication.

---

## Strengths

### S1: Escalation from 5-Seed to 20-Seed Ablation
The most impressive methodological choice is the honest escalation from 5 seeds (Table 8) to 20 seeds (Table 12). The authors discovered that their initial ablation was underpowered ($\sim$15--20% power for medium effects) and reported the false negative explicitly: "The Round 2 finding that these components were 'not individually significant' was a false negative attributable to the low statistical power of $n=5$ seeds." This level of transparency is exemplary and rarely seen in the literature.

### S2: Comprehensive BER Statistical Validation
The BER simulations use 200 independent channel realizations per SNR point with paired $t$-tests and Holm--Bonferroni correction. The paired design (same channel realizations and noise instances for all methods at each SNR point) is appropriate for reducing variance. The paper correctly reports when results become non-significant after correction (e.g., QPSK BER at SNR ≥ 5 dB).

### S3: ISTA Control Experiment Design
The ISTA control experiment (Section 4.12.3) is well-designed to disentangle generic soft-thresholding effects from LISTA-specific learned behavior. Using grid-searched ISTA thresholds as the control isolates the contribution of learned parameters. The 7.6 percentage-point difference (92.4% vs 100.0%) is interpretable and practically meaningful.

### S4: Cross-Table Consistency Transparency
The cross-table consistency note (Section 4.3) transparently explains the 8 dB difference between Tables 1 and 3 as arising from independently trained models with different training distributions. This is the kind of methodological transparency that builds reader trust.

### S5: Pilot Ratio Sensitivity Analysis
Table 6 systematically varies the pilot ratio $M/N$ from 1.5 to 4.0, providing practitioners with actionable guidance on minimum pilot requirements. The exclusion of diverged seeds is honestly reported.

---

## Weaknesses

### W1: NMSE Loss Scale-Invariance Not Formally Analyzed
**Problem**: The paper states that the NMSE loss $\|\hat{\mathbf{h}} - \mathbf{h}\|_2^2 / \|\mathbf{h}\|_2^2$ is "scale-invariant" and attributes the SNR saturation to this property (Section 5.1). However, this claim is not formally analyzed. The scale-invariance means the loss is identical for $(\hat{\mathbf{h}}, \mathbf{h})$ and $(\alpha\hat{\mathbf{h}}, \alpha\mathbf{h})$ for any $\alpha > 0$, which implies the optimizer cannot distinguish between "estimate the channel correctly" and "estimate the channel up to a scale factor." This is a significant confound that deserves formal treatment.
**Why it matters**: If the loss is truly scale-invariant, the network may learn to output $\hat{\mathbf{h}} = c \cdot \mathbf{h}$ for some constant $c \neq 1$, which would produce low NMSE during training but biased estimates at test time. The paper should verify whether the learned estimates are unbiased (i.e., $E[\hat{\mathbf{h}}] = \mathbf{h}$) or systematically scaled.
**Suggestion**: Add a diagnostic experiment: compute the mean scaling factor $\bar{c} = E[\hat{\mathbf{h}}^T \mathbf{h} / \|\mathbf{h}\|_2^2]$ across test samples. If $\bar{c} \neq 1$, this confirms the scale-invariance confound and the saturation explanation.
**Severity**: Major

### W2: Error Concentration Metric Needs Formal Definition
**Problem**: The "error on $S$ %" metric (fraction of error energy on true support) is introduced in Table 10 without formal definition. The metric is $\sum_{i \in S} (\hat{h}_i - h_i)^2 / \sum_{i=1}^N (\hat{h}_i - h_i)^2 \times 100\%$, but this is never stated. Moreover, no confidence intervals are reported for the percentages (only std over 5 seeds), and the metric has a degenerate case: if the total error is zero, the fraction is undefined.
**Why it matters**: The error concentration mechanism is the paper's primary contribution, so the metric defining it must be formally specified and its statistical properties understood.
**Suggestion**: (1) Add a formal definition equation for the error concentration metric. (2) Report 95% confidence intervals alongside the percentages. (3) Handle the degenerate case (zero total error) explicitly.
**Severity**: Major

### W3: Cross-Experiment Multiple Comparisons
**Problem**: The paper applies Holm--Bonferroni correction within individual tables (e.g., $m=7$ SNR points in Table 14, $m=3$ comparisons in Table 12) but does not address the multiple comparisons across the paper's 12 experiments. With 12 experiments, each containing multiple hypothesis tests, the family-wise error rate across the paper is substantially inflated.
**Why it matters**: Some "significant" findings may not survive a paper-level correction. For example, if Table 1 has 9 SNR points × 5 method pairs = 45 tests, and Table 14 has 7 tests, the total number of tests across the paper likely exceeds 100.
**Suggestion**: Either (a) apply a paper-level correction (e.g., Benjamini--Hochberg FDR) to all reported $p$-values, or (b) explicitly state that corrections are applied within each table's family of tests and acknowledge the paper-level inflation.
**Severity**: Minor

### W4: LISTA-CP Comparison Lacks Equivalence Test
**Problem**: Table 9 shows LISTA and LISTA-CP are "statistically indistinguishable" ($p > 0.4$), but a non-significant $p$-value does not demonstrate equivalence—it only fails to reject the null hypothesis of no difference. The paper needs a formal equivalence test (e.g., TOST: two one-sided tests) to claim equivalence.
**Why it matters**: The identical performance of LISTA and LISTA-CP is used to argue that "the weight clipping constraint is naturally satisfied." Without an equivalence test, this conclusion is not statistically supported.
**Suggestion**: Add a TOST equivalence test with a pre-specified equivalence margin (e.g., $\pm 0.5$ dB NMSE). Report the equivalence $p$-value.
**Severity**: Minor

### W5: Training Reproducibility Information Incomplete
**Problem**: The paper specifies the Adam optimizer, learning rate ($5 \times 10^{-4}$), weight decay ($10^{-5}$), batch size (256), epochs (200), and gradient clipping (max norm 5.0). However, it does not report: (1) random seed for training, (2) hardware used (GPU model), (3) training time per model, (4) validation loss trajectory, or (5) whether early stopping was used.
**Why it matters**: Reproduducibility requires complete training details. The validation loss trajectory is particularly important for understanding whether the 200-epoch training converged.
**Suggestion**: Add a reproducibility table or appendix with: GPU model, training time, final validation loss, and whether early stopping was triggered.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title accurately reflects the paper's content. The three keywords (generalization, error structure, ablation) are well-chosen.
- Abstract is dense but comprehensive. The mechanism analysis summary is clear.

### Introduction
- The 6 enumerated contributions are well-structured. Contribution 2 (BER mechanism) is the strongest.
- The introduction correctly positions this as analysis rather than novelty, which is appropriate.

### Methodology (Section 3)
- LISTA architecture is standard and well-described.
- The FFT-based convolution implementation is a practical detail that aids reproducibility.
- Training protocol is well-specified. The mixed-SNR sampling strategy is appropriate for the paper's goals.

### Experimental Design (Section 4)
- 12 experiments is comprehensive. The progression from basic NMSE comparison to mechanism analysis to practical deployment is logical.
- The experimental setup section (4.1) clearly specifies data generation, baselines, and evaluation metrics.
- The grid search for baseline hyperparameters is appropriate.

### Statistical Reporting
- The paper reports mean ± std, $p$-values, and Cohen's $d$ effect sizes, which is good practice.
- The Holm--Bonferroni correction is correctly applied within tables.
- The 200-realization BER simulations are well-powered for detecting small effects.

### Discussion (Section 5)
- The discussion is thorough and honest. The "training artifact vs. architectural limitation" analysis is well-argued.
- The AMP connection (Section 5.1) is interesting but speculative without empirical validation.

### Conclusion
- Conclusion accurately summarizes findings. The future work directions are concrete.

---

## Questions for Authors

1. **Scale-invariant loss diagnostic**: Can you report the mean scaling factor $\bar{c} = E[\hat{\mathbf{h}}^T \mathbf{h} / \|\mathbf{h}\|_2^2]$ across test samples for the mixed-SNR trained model? If $\bar{c} \neq 1$, this would formally confirm the scale-invariance confound.

2. **Error concentration confidence intervals**: Can you report 95% confidence intervals for the "Error on $S$ %" metric in Tables 10--11? The current std over 5 seeds may not capture the true uncertainty.

3. **Training convergence**: Can you provide the validation loss trajectory (loss vs. epoch) for the mixed-SNR trained model? Did training converge within 200 epochs, or would more epochs improve NMSE?

4. **Equivalence test for LISTA-CP**: Can you perform a TOST equivalence test with a $\pm 0.5$ dB margin for the LISTA vs LISTA-CP comparison in Table 9?

---

## Minor Issues

### Language / Grammar
- Section 4.1: "We generate $10{,}000$ training samples, $2{,}000$ validation samples, and $2{,}000$ test samples" — specify whether these are independent draws or if there is any overlap.
- Section 4.12.2: "The negligible standard deviations across 5 seeds ($<0.02\%$ for LISTA)" — clarify that this is for the non-support error fraction.

### Citation Format
- Reference formatting appears consistent. No issues noted.

### Figures and Tables
- Table 10: Add a column for ISTA to enable direct three-way comparison (currently ISTA appears only in Table 11).
- Table 12: The Holm--Bonferroni correction with $m=3$ is correct for 3 pairwise comparisons, but the paper should specify the family of tests.

### Layout
- No layout issues noted. Tables are well-formatted within the CAS template constraints.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | LISTA is not novel; the contribution is analytical (error concentration mechanism) |
| Methodological Rigor (25%) | 78 | Strong | Comprehensive experiments with good statistical practice; scale-invariant loss and error concentration metric need formal treatment |
| Evidence Sufficiency (25%) | 82 | Strong | 12 experiments, 200 BER realizations, 20-seed ablation; AMP connection lacks empirical support |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow from experiments to mechanism analysis; minor narrative tension |
| Writing Quality (15%) | 76 | Strong | Professional prose; some dense passages; reproducibility details incomplete |
| **Weighted Average** | **77.0** | **Minor Revision** | |
