# Peer Review Report — Peer Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 9

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Prof. Kai Zhang, Department of Electrical Engineering, Tsinghua University. Expertise in statistical signal processing, experimental design in machine learning, and reproducibility standards. 15 years of experience reviewing for IEEE and Elsevier signal processing journals.

### Review Focus
Research design rigor, statistical validity of experimental results, ablation methodology, BER simulation design, and reproducibility. I specifically evaluate whether the statistical claims are properly supported by the experimental evidence.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
5 — Completely within my area of expertise, I am very confident in my assessment

### Summary Assessment
This paper presents a comprehensive analysis of LISTA for sparse channel estimation, with particular emphasis on statistical rigor. The authors conduct 13 experiments covering NMSE performance, ablation studies, generalization analysis, BER simulations, and hardware complexity. The methodological approach is generally sound, with notable strengths in the ablation study design (20 seeds with paired t-tests and Cohen's d) and BER validation (200 realizations per SNR point).

However, I have identified several methodological concerns that should be addressed. The most significant is the inconsistent use of seed counts across experiments: the initial ablation uses 5 seeds while the follow-up uses 20, but other experiments (BER, generalization) also use 5 seeds without justification for why this is sufficient. The BER simulation design has some issues with the paired t-test methodology that need clarification. The hardware complexity analysis, while thorough in its FLOP counting, makes throughput claims that go beyond what the analysis supports. These issues are addressable and do not fundamentally undermine the paper's contributions.

---

## Strengths

### S1: Exemplary Ablation Study Progression
The progression from 5-seed to 20-seed ablation (Sections 4.5 and 4.11) demonstrates exceptional methodological awareness. The authors correctly identify that n=5 seeds provides only ~15-20% statistical power for medium effects and follow up with a properly powered study. The 20-seed study reports paired t-tests, Cohen's d effect sizes, and reveals that the initial finding (threshold and per-layer parameters "not individually significant") was a false negative. This is exactly how science should work — initial findings are checked with adequate power.

### S2: BER Simulation Statistical Validation
The BER simulation design (Section 4.10) uses 200 channel realizations per SNR point with paired t-tests and 95% confidence intervals. This is significantly better than the typical practice in the channel estimation literature, which often reports single-seed results without error bars. The use of 5 random seeds for the BER experiments provides reasonable confidence in the reported means.

### S3: Transparent Reporting of Training Protocol
The paper clearly documents the training procedure: Adam optimizer, learning rate 5×10⁻⁴, weight decay 10⁻⁵, cosine annealing, gradient clipping (max norm 5.0), mixed SNR sampling from [0, 30] dB, 200 epochs, batch size 256. This level of detail enables reproducibility. The cross-table consistency note (Section 4.3) explaining why Tables 1 and 3 show different NMSE values for the same nominal configuration is a particularly nice touch.

### S4: Effect Size Reporting
The ablation study reports Cohen's d alongside p-values, which is best practice. The effect sizes are substantial: d=1.5 for W^(k), d=18.4 for threshold, d=24.1 for shared parameters. This allows readers to assess practical significance, not just statistical significance.

---

## Weaknesses

### W1: Inconsistent Seed Counts Across Experiments
**Problem**: The paper uses different numbers of seeds for different experiments: 5 seeds for NMSE vs. SNR (Table 1), 5 seeds for sparsity (Table 2), 5 seeds for channel length (Table 3), 5 seeds for depth (Table 4), 5 seeds for initial ablation (Table 5), 20 seeds for follow-up ablation (Table 9), 5 seeds for BER (Tables 6-8), and 5 seeds for LISTA-CP (Table 10). The 20-seed ablation is motivated by the need for higher statistical power, but this same argument applies to other experiments.

**Why it matters**: If 5 seeds is insufficient for the ablation study (as the authors acknowledge), it may also be insufficient for other experiments where differences between methods are smaller. For example, the LISTA vs. LISTA-CP comparison (Table 10) reports p > 0.4 with 5 seeds, but this could be a false negative due to low power.

**Suggestion**: Provide a brief justification for why 5 seeds is sufficient for the non-ablation experiments. Ideally, include a power analysis showing that 5 seeds provides adequate power for the effect sizes of interest. Alternatively, increase the seed count for at least the BER experiments to match the ablation study.

**Severity**: Major

### W2: Paired t-test Methodology for BER Comparisons
**Problem**: The BER experiments use paired t-tests to compare LISTA vs. OMP across 5 seeds. However, the pairing is not clearly defined. Are the same 5 random seeds used for both LISTA and OMP? If so, what is being paired — the same channel realizations with the same noise instances? The paper states "200 channel realizations per SNR point" but does not clarify whether the same 200 realizations are used for all methods.

**Why it matters**: Paired t-tests require that the paired observations share the same random variation (e.g., same noise instances). If different noise instances are used for LISTA and OMP, an unpaired test would be more appropriate. Using a paired test on unpaired data inflates the significance level.

**Suggestion**: Clarify the pairing structure. If the same channel realizations and noise instances are used for all methods (which should be the case for a fair comparison), state this explicitly. If different noise instances are used, switch to unpaired t-tests or Welch's t-test.

**Severity**: Major

### W3: Hardware Throughput Claims Exceed Analysis Scope
**Problem**: The paper claims "2-6× hardware throughput advantage over OMP" based on FLOP counts and theoretical pipeline analysis (Section 4.13). However, FLOP counts do not directly translate to throughput because: (1) memory bandwidth is often the bottleneck, not compute; (2) the analysis assumes 64 parallel DSP units at 500 MHz without justification for this configuration; (3) pipeline stall analysis is omitted.

**Why it matters**: Hardware throughput is a key practical claim. The analysis provides FLOP counts (which are valid) but the throughput extrapolation involves assumptions that are not validated. The 2-6× range is presented as a finding rather than an estimate.

**Suggestion**: Reframe the hardware analysis as "FLOP comparison and qualitative parallelism analysis" rather than "throughput advantage." Remove specific throughput estimates (4.4×) unless supported by actual hardware implementation. Keep the FLOP counts and parallelism characteristics, which are valid contributions.

**Severity**: Major

### W4: Missing Confidence Intervals for NMSE Results
**Problem**: Tables 1-4 report mean ± standard deviation over 5 seeds, but do not report 95% confidence intervals. Standard deviation describes variability across seeds, while confidence intervals describe uncertainty in the estimated mean. With n=5, the confidence interval width depends heavily on the assumption of normality.

**Why it matters**: Confidence intervals are more interpretable for assessing uncertainty in the reported means. The standard deviation of 5 samples has high uncertainty itself (the true SD could be 0.5× to 2× the reported value).

**Suggestion**: Report 95% confidence intervals (mean ± t_{0.025,4} × SD/√5) alongside or instead of standard deviations. For n=5, t_{0.025,4} = 2.776, so the confidence interval is approximately ±1.24 × SD.

**Severity**: Minor

### W5: No Multiple Comparison Correction
**Problem**: The paper reports many paired t-tests across multiple SNR levels, sparsity levels, and ablation configurations without correcting for multiple comparisons. For example, Table 1 reports LISTA vs. OMP at 9 SNR levels, Table 2 at 5 sparsity levels, and Table 9 at 3 ablation configurations. With α = 0.05, the expected number of false positives across all tests is non-negligible.

**Why it matters**: Without correction, the family-wise error rate is inflated. A Bonferroni correction would change some p < 0.05 results to non-significant.

**Suggestion**: Either (a) apply Bonferroni or Holm-Bonferroni correction to the reported p-values, or (b) explicitly state that no multiple comparison correction was applied and discuss the implications. The ablation study (Table 9) has only 3 comparisons, so the impact is minimal, but the SNR sweep (Table 1) has 9 comparisons.

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is appropriate and descriptive.
- Abstract is comprehensive but very long (~400 words). Consider condensing.
- The abstract's statistical claims are well-formulated (p-values, confidence intervals mentioned).

### Introduction
- Six contributions are clearly enumerated.
- Contribution 2 (BER mechanism analysis) could be more clearly separated from the BER equivalence finding.

### Methodology (Section 3)
- LISTA architecture description is standard and clear.
- Parameter analysis is helpful (82K parameters).
- Training procedure is well-documented.
- Missing: learning rate schedule details (cosine annealing parameters), data split ratios.

### Experiments (Section 4)
- **4.1 Setup**: Clear documentation of data generation, baselines, and LISTA configuration.
- **4.2 NMSE vs SNR**: Results are clear. The mixed-SNR training protocol is well-explained.
- **4.3 Channel Length**: The cross-table consistency note is excellent. Training divergence at N=256 is well-documented.
- **4.4 Depth Analysis**: Results are clear. The practical recommendation of L=10-20 is reasonable.
- **4.5 Ablation (5 seeds)**: The initial ablation is honest about its limitations.
- **4.6 Generalization**: The three mismatch scenarios are well-chosen.
- **4.7 Practical Deployment**: Inference time comparison is useful but caveated appropriately.
- **4.8 LISTA-CP**: The diagnostic analysis of why clipping is never activated is insightful.
- **4.9 SNR Mitigation**: Results are clear and practically useful.
- **4.10 BER**: The 200-realization design is strong. The MMSE vs. ZF distinction is well-motivated.
- **4.11 Ablation (20 seeds)**: Exemplary methodology.
- **4.12 Mechanism Analysis**: The error sparsity analysis is novel and insightful.
- **4.13 Hardware**: FLOP counts are valid; throughput estimates are speculative.

### Discussion (Section 5)
- Section 5.1 (saturation analysis) is thorough.
- Section 5.2 (deep learning comparison) is the weakest — qualitative only.
- Section 5.3 (deployment framework) is practical.
- Section 5.4 (limitations) is honest.

### Conclusion
- Well-structured summary.
- Hardware claims appropriately hedged.

---

## Questions for Authors

1. Can you clarify the pairing structure for the BER paired t-tests? Are the same noise instances used for all methods at each SNR point?

2. Given that the 20-seed ablation revealed false negatives in the 5-seed study, have you considered whether the 5-seed BER experiments (where LISTA vs. OMP differences are small) might also contain false negatives?

3. The hardware analysis assumes 64 parallel DSP units at 500 MHz. What is the basis for this specific configuration? How would the throughput estimates change with different configurations?

---

## Minor Issues

### Language / Grammar
- Section 4.12: "the NMSE metric is agnostic to error location" — "insensitive to" is more precise
- Throughout: consider using "estimate" instead of "advantage" for hardware claims

### Statistical Reporting
- Table 1: Consider adding 95% CI alongside mean ± SD
- Table 9: The Cohen's d values are very large (d=18.4, d=24.1) — these indicate near-perfect separation, which is expected given the large effect sizes
- Tables 6-8: The BER p-values should be interpreted with caution given the multiple comparisons

### Figures and Tables
- All tables are well-formatted
- Consider adding error bars to figures where applicable
- Table 8 (16-QAM BER) is particularly well-designed with clear significance markers

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 60 | Adequate | BER mechanism analysis is novel; rest is comprehensive but incremental |
| Methodological Rigor (25%) | 68 | Adequate | Good practices overall, but inconsistent seed counts and pairing issues need addressing |
| Evidence Sufficiency (25%) | 72 | Strong | Comprehensive experiments with 200 realizations for BER; 20 seeds for ablation |
| Argument Coherence (15%) | 74 | Strong | Clear logical flow; honest about limitations |
| Writing Quality (15%) | 70 | Adequate | Generally clear; some repetition; abstract too long |
| **Weighted Average** | **69.2** | **Minor Revision** | |

---

## Final Assessment

The paper demonstrates strong methodological awareness, particularly in the ablation study progression and BER validation. The main concerns are: (1) inconsistent seed counts across experiments, (2) unclear paired t-test methodology for BER, and (3) hardware claims that exceed the analysis scope. These are addressable with minor revisions. The BER mechanism analysis and error sparsity analysis are genuine methodological contributions to the field.

**Overall Score: 69/100 — Minor Revision**
