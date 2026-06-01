# Methodology Review Report (Peer Reviewer 1)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-ROUND8
- **Review Date**: 2026-06-01
- **Review Round**: Round 8

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Dr. Marcus Chen — Associate Professor of Electrical Engineering, specializing in statistical signal processing, experimental design for machine learning systems, and reproducible research methodology. 12 years of experience evaluating empirical studies in signal processing and communications. Published extensively on experimental methodology for deep learning in physical-layer communications.

### Review Focus
Research design rigor, statistical validity, reproducibility, and whether the experimental methodology supports the paper's conclusions. I focus on whether the experiments are well-designed, whether statistical claims are properly validated, and whether the results are reproducible.

---

## Overall Assessment

### Recommendation
**Minor Revision**

### Confidence Score
5 — Completely within my area of expertise. Statistical methodology, experimental design for ML systems, and reproducibility are my core research areas.

### Summary Assessment
This paper presents a comprehensive experimental evaluation of LISTA for sparse channel estimation across 13 experiments. The methodology is generally sound: the authors use appropriate metrics (NMSE in dB), report mean ± standard deviation over multiple seeds, conduct paired t-tests with effect sizes (Cohen's d), and validate BER results with 200 channel realizations per SNR point. The progression from 5-seed to 20-seed ablation (addressing statistical power concerns) is commendable. However, several methodological issues warrant attention: (1) the theoretical hardware complexity analysis makes strong claims based on FLOP counts without measured validation, (2) the BER analysis uses only 5 seeds for the primary MMSE results while claiming statistical rigor, and (3) the mixed-SNR training protocol creates potential confounds in interpreting the NMSE saturation. These are addressable with minor revisions.

---

## Strengths

### S1: Proper Statistical Validation with Effect Sizes and Confidence Intervals
The paper reports paired t-tests, p-values, Cohen's d effect sizes, and 95% confidence intervals for the BER experiments (Section 4.10). The ablation study (Table 9) reports both p-values and Cohen's d, with effect sizes ranging from d = 1.5 (No W) to d = 24.1 (Shared parameters). This is exemplary statistical reporting for the signal processing community, where effect sizes are often omitted.

### S2: Self-Correcting Experimental Design (5-Seed → 20-Seed Ablation)
The paper explicitly identifies the low statistical power of the initial 5-seed ablation (Table 5: "with only n=5 seeds, the statistical power is limited (~15–20% for medium effects)") and conducts a follow-up 20-seed ablation (Table 9) that reveals the threshold and per-layer parameters as dominant contributors. This self-correction strengthens the paper's credibility and provides a methodological lesson for the community.

### S3: Cross-Table Consistency Transparency
Section 4.3 explicitly explains why Table 2 and Table 3 report different NMSE values at the same nominal configuration (N=64, K=5, M=256, L=20, SNR=20 dB): the two experiments use independently trained models with different training distributions. This level of transparency is rare and valuable.

### S4: BER Validation with Adequate Realizations
The BER experiments use 200 independent channel realizations per SNR point (Section 4.10), which is adequate for BER estimation. The use of paired t-tests for LISTA vs. OMP comparisons is appropriate given that both methods are evaluated on the same channel realizations.

### S5: Comprehensive Generalization Analysis
The paper evaluates generalization across three axes: sparsity mismatch (Section 4.6.1), SNR mismatch (Section 4.6.2), and cross-distribution (ITU channels, Section 4.7.2). This multi-axis generalization analysis is more thorough than typical deep unfolding papers.

---

## Weaknesses

### W1: Theoretical Hardware Claims Without Measured Validation
**Problem**: Section 4.13 presents detailed hardware timing estimates (23 μs sequential latency, 1.2 μs pipelined throughput, 4.4× speedup over OMP) based on FLOP counts and pipeline analysis. While the paper repeatedly states these are "theoretical estimates," the level of specificity (e.g., "1.2 μs") creates an impression of precision that may not hold in practice. The paper cites Wei et al. (2022) for FPGA validation, but does not provide measured results.
**Why it matters**: Readers may interpret the 4.4× throughput advantage as a validated claim rather than a theoretical estimate. FLOP counts alone do not predict hardware performance—memory bandwidth, pipeline stalls, and implementation overhead can significantly alter the actual speedup.
**Suggestion**: (1) Add a prominent caveat in the abstract and highlights that hardware timing estimates are theoretical. (2) Consider reducing the specificity of timing claims (e.g., "estimated 1–3 μs" rather than "1.2 μs"). (3) If possible, provide a brief sensitivity analysis showing how the 4.4× estimate changes under different assumptions (e.g., memory-bound vs. compute-bound).
**Severity**: Major

### W2: BER Analysis Uses Only 5 Seeds for Primary MMSE Results
**Problem**: The BER MMSE results (Table 6) report "Mean over 5 seeds, 200 realizations per point." While 200 realizations per seed is adequate for BER estimation, using only 5 seeds means the reported mean BER is based on 5 independent estimates of the true BER. The standard deviation across seeds is reported for some entries but not all, and the paired t-tests use n=5 as the sample size.
**Why it matters**: With n=5 seeds, the paired t-test has limited power to detect small but meaningful BER differences. The paper claims "no BER penalty at SNR ≥ 5 dB (p > 0.05)," but p > 0.05 with n=5 does not establish equivalence—it only fails to reject the null hypothesis of no difference.
**Suggestion**: (1) Add a power analysis showing what BER difference could be detected with n=5 seeds at 80% power. (2) Consider reporting equivalence tests (TOST) or confidence intervals for the BER difference rather than relying solely on p > 0.05. (3) If feasible, increase to 10–20 seeds for the primary MMSE BER results.
**Severity**: Major

### W3: Mixed-SNR Training Creates Confounds in NMSE Saturation Interpretation
**Problem**: LISTA is trained with mixed-SNR sampling (SNR ∈ [0, 30] dB, Section 4.1), and the paper attributes the NMSE saturation at ~-25 dB to "the scale-invariant loss and mixed-SNR training" (Abstract). However, the paper does not disentangle these two factors: is the saturation caused by (a) the scale-invariant loss function, (b) the mixed-SNR training distribution, or (c) both?
**Why it matters**: The interpretation affects the paper's conclusion that the saturation is "a training artifact rather than an architectural limitation." If the saturation is primarily caused by the loss function (which is inherent to LISTA's design), it may be more accurately described as an architectural property.
**Suggestion**: Add a control experiment training LISTA with (i) MSE loss instead of NMSE loss, and/or (ii) SNR-specific training with MSE loss, to disentangle the contributions of the loss function and training distribution. The existing SNR-specific training experiment (Table 10) partially addresses this, but uses NMSE loss, so the two factors remain confounded.
**Severity**: Minor

### W4: No Confidence Intervals for NMSE Results in Tables 1–4
**Problem**: Tables 1–4 report NMSE as "mean ± std" over 5 seeds, but do not report 95% confidence intervals. The BER tables (Tables 6–8) report confidence intervals, creating an inconsistency in statistical reporting across the paper.
**Why it matters**: Standard deviation describes variability across seeds, while confidence intervals describe uncertainty in the estimated mean. For n=5, the difference is substantial (95% CI is approximately ±2.78 × std/√5).
**Suggestion**: Report 95% confidence intervals for all NMSE tables (Tables 1–4, 9, 10) to maintain consistency with the BER tables and provide a more interpretable measure of uncertainty.
**Severity**: Minor

### W5: Reproducibility Concerns — No Code or Data Availability Statement
**Problem**: The paper does not include a code or data availability statement. While the experimental setup is described in sufficient detail for replication, the absence of released code makes independent verification difficult.
**Why it matters**: Reproducibility is a cornerstone of empirical research. The signal processing community increasingly expects code availability for ML-based methods.
**Suggestion**: Add a Data Availability Statement indicating whether the code and trained models will be released. If code will be released, provide a repository URL or DOI.
**Severity**: Minor

---

## Detailed Comments

### Research Questions & Hypotheses
The research questions are implicit rather than explicitly stated as hypotheses. The paper investigates: (1) How does LISTA compare to classical methods for channel estimation? (2) Why does LISTA's NMSE gap not translate to BER penalty? (3) What are the practical deployment considerations? These are clear and answerable, though framing them as explicit hypotheses would strengthen the paper.

### Research Design
The experimental design is comprehensive, covering 13 experiments across multiple dimensions (SNR, sparsity, channel length, depth, ablation, generalization, BER, hardware). The use of mixed-SNR training for the primary model ensures consistency across experiments. The independent training for Table 3 (channel-length variation) is explicitly acknowledged.

### Sampling Strategy
The data generation uses i.i.d. Gaussian taps with uniform random locations, which is appropriate for the synthetic evaluation. The ITU channel experiments (Section 4.7.2) provide validation on more realistic channels. The sample sizes (10,000 training, 2,000 validation, 2,000 test) are adequate.

### Data Collection
The experimental setup is well-documented: N=64, K=5, M=256, L=20, BPSK pilots, AWGN noise. The baseline hyperparameters are optimized via grid search on the validation set, which is appropriate. The LISTA training uses Adam optimizer with cosine annealing and gradient clipping.

### Analysis Methods
The analysis methods are appropriate: NMSE in dB for channel estimation accuracy, BER for system-level performance, Jaccard index for support recovery, Gini coefficient for error sparsity. The use of paired t-tests for LISTA vs. OMP comparisons is correct given the paired experimental design.

### Results Presentation
The results are presented clearly with 13 tables and figures. The cross-table consistency note (Section 4.3) is excellent. The progression from 5-seed to 20-seed ablation is well-motivated. However, the theoretical hardware analysis (Section 4.13) could benefit from more prominent caveating.

### Reproducibility
The experimental setup is described in sufficient detail for replication. However, no code or data availability statement is provided. The random seeds are mentioned but not specified.

### Methodological Fallacies Detected
- **Confounding**: The NMSE saturation analysis confounds the effects of the loss function and training distribution (W3).
- **Overgeneralization risk**: The theoretical hardware timing estimates (Section 4.13) are presented with a level of specificity that may not hold in practice (W1).

---

## Questions for Authors

1. Can you provide a power analysis for the BER paired t-tests with n=5 seeds? What is the minimum detectable BER difference at 80% power?

2. The NMSE saturation is attributed to "the scale-invariant loss and mixed-SNR training." Can you disentangle these two factors with a control experiment using MSE loss?

3. Will the code and trained models be released for reproducibility?

4. For the theoretical hardware analysis (Section 4.13), can you provide a sensitivity analysis showing how the 4.4× throughput estimate changes under different assumptions (e.g., memory-bound vs. compute-bound)?

---

## Minor Issues

### Statistical Reporting
- Tables 1–4 report "mean ± std" but not 95% confidence intervals. Consider adding CIs for consistency with the BER tables.
- Table 5 (5-seed ablation): The p-values for "Fixed threshold" (p=0.455) and "Shared parameters" (p=0.338) are non-significant, but the paper correctly notes this is due to low power. Consider adding a footnote explaining that the non-significance is a power issue, not evidence of no effect.

### Figures and Tables
- Figure 4 (NMSE vs layers): The y-axis range is very wide (-4.84 to -25.04 dB), making it hard to distinguish performance at L=10–20. Consider a secondary zoomed-in plot.
- Table 11 (Scaling): The LISTA/OMP FLOPs ratio increases from 2.14× at N=32 to 3.06× at N=256. This trend is worth noting in the text.

### Language
- Section 4.10.1: "all three methods converge to nearly identical BER at SNR ≥ 15 dB (~0.0003 for QPSK)" — the BER 0.0003 is the same at SNR 15, 20, 25, and 30 dB for LISTA, which seems suspicious. Is this a reporting artifact (e.g., floor effect from limited realizations)?

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | Known architecture, known problem; novelty in systematic analysis |
| Methodological Rigor (25%) | 76 | Strong | Comprehensive experiments; some concerns about hardware claims and BER power |
| Evidence Sufficiency (25%) | 80 | Strong | 13 experiments, multiple seeds, effect sizes; code not released |
| Argument Coherence (15%) | 83 | Strong | Logical flow, self-correcting design |
| Writing Quality (15%) | 82 | Strong | Clear, transparent, well-organized |
| **Weighted Average** | **74.4** | **Minor Revision** | |
