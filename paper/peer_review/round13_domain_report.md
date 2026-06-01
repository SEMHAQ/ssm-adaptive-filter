# Peer Review Report — Peer Reviewer 2 (Domain)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 13

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert

### Reviewer Identity
Senior researcher in sparse channel estimation and compressed sensing for wireless communications, with 15+ years of experience. Published seminal work on CS-based channel estimation. Deep familiarity with OMP, LASSO, ISTA, and their variants in the channel estimation context. Regular reviewer for IEEE TSP, TWC, and DSP journals.

### Review Focus
Literature coverage completeness, theoretical framework accuracy, domain-specific contribution assessment, and positioning within the sparse channel estimation field.

---

## Overall Assessment

### Recommendation
**Major Revision**

### Confidence Score
**5** — Completely within my area of expertise.

### Summary Assessment

This paper applies the standard LISTA architecture to sparse channel estimation and provides a systematic experimental analysis covering NMSE performance, BER implications, error structure, ablation, and generalization. The paper is well-written and the experiments are comprehensive. However, I have significant concerns about the domain contribution: (1) the paper does not demonstrate that the "error concentration mechanism" is specific to LISTA rather than a generic property of soft-thresholding, which undermines the primary contribution claim; (2) the comparison baseline is limited to OMP and LASSO, omitting several important sparse channel estimation algorithms (SAMP, CoSaMP, SP, OBOOMP); (3) the i.i.d. Gaussian channel model is simplistic for drawing conclusions about "sparse channel estimation" in general; (4) the paper's positioning as an "analysis" paper rather than a "method" paper requires a higher bar for insight generation, which is not fully met. With substantial revision to address these concerns, the paper could make a meaningful contribution.

---

## Strengths

### S1: Comprehensive Ablation with Statistical Rigor
The 20-seed ablation study (Table 11) with paired t-tests and Cohen's d is the most rigorous ablation I have seen in the deep unfolding for channel estimation literature. The finding that the per-layer threshold schedule is the dominant contributor (+14-18 dB) is a genuine insight into what LISTA learns.

### S2: ITU Channel Generalization
Testing on ITU PedA and VehA channels (Table 6) with baselines tuned on i.i.d. Gaussian data is a fair and practical evaluation protocol. The finding that LISTA generalizes to ITU channels without retraining is practically valuable.

### S3: LISTA-CP Diagnostic Analysis
The comparison with LISTA-CP (Table 8) is technically sound. The diagnostic finding that the weight clipping constraint is never activated (max spectral norm = 0.34 < 1.0) provides genuine insight: standard LISTA training naturally satisfies the convergence conditions that LISTA-CP enforces.

### S4: SNR Mitigation Strategy
The SNR-specific training experiment (Table 13) is practically valuable. The finding that narrow-range training improves NMSE by ~6 dB is actionable for practitioners deploying LISTA in known-SNR environments.

---

## Weaknesses

### W1: Error Concentration May Be Generic to Soft-Thresholding, Not LISTA-Specific
**Problem**: The paper's primary contribution is the finding that LISTA concentrates 99.9% of estimation error on true tap locations. However, this is likely a generic property of the soft-thresholding operator, not a learned property of LISTA. Any estimator using soft-thresholding — including standard ISTA with fixed thresholds — would enforce sparsity in the estimate, pushing residual error onto the true tap locations. The paper does not compare LISTA's error concentration against ISTA's, making it impossible to determine whether the learned parameters contribute to the mechanism.
**Why it matters**: If ISTA with fixed thresholds achieves 99.5% error concentration on true taps, then the "mechanism analysis" is simply characterizing soft-thresholding behavior, not discovering a LISTA-specific property. The contribution would need to be reframed significantly.
**Suggestion**: Add a control experiment: run standard ISTA (fixed thresholds, 20 iterations) and compute the same error sparsity metrics. If ISTA shows similar concentration (e.g., >99%), reframe the contribution as "characterizing the error structure of soft-thresholding-based sparse recovery in the channel estimation context" rather than "LISTA's mechanism."
**Severity**: Critical

### W2: Limited Baseline Comparison
**Problem**: The comparison is limited to OMP, LASSO, LMS, and NLMS. Several important sparse channel estimation algorithms are missing:
- **SAMP (Sparsity Adaptive Matching Pursuit)**: Does not require sparsity knowledge, like LISTA
- **CoSaMP (Compressive Sampling Matching Pursuit)**: More robust than OMP to correlated atoms
- **Subspace Pursuit (SP)**: Good performance with moderate complexity
- **FISTA (Fast ISTA)**: Accelerated ISTA variant that is the natural comparison for LISTA
**Why it matters**: OMP is the simplest greedy algorithm and LASSO uses basic ISTA. Comparing only against these baselines may overstate LISTA's relative performance. FISTA, in particular, is the direct comparison — LISTA is supposed to accelerate ISTA convergence, so comparing against FISTA (with the same iteration count) would directly test this claim.
**Suggestion**: Add FISTA as a baseline with L=20 iterations (same as LISTA layers). This directly tests whether LISTA's learned parameters provide improvement over standard accelerated ISTA. If FISTA with 20 iterations matches LISTA, the value of learning is diminished.
**Severity**: Major

### W3: i.i.d. Gaussian Channel Model Is Simplistic
**Problem**: The primary experiments use i.i.d. Gaussian tap amplitudes with uniform random tap locations. Real wireless channels have: (1) correlated tap amplitudes (exponential PDP), (2) correlated tap locations (clustered multipath), (3) frequency selectivity, (4) time variation. The ITU channel experiments partially address this, but the core mechanism analysis (Table 12) is only on i.i.d. Gaussian channels.
**Why it matters**: The error concentration mechanism may behave differently on channels with correlated taps or non-uniform PDP. The ITU generalization (Table 14) is encouraging (99.3-99.5% vs. 99.9%) but the analysis is limited to a single SNR and configuration.
**Suggestion**: Acknowledge more prominently that the i.i.d. Gaussian model is a simplification. Consider adding a correlated-tap channel model (e.g., exponential PDP with random tap locations) as an intermediate step between i.i.d. Gaussian and ITU channels.
**Severity**: Minor

### W4: Theoretical Analysis of Error Concentration Is Missing
**Problem**: The paper empirically demonstrates error concentration but provides no theoretical analysis. Why does soft-thresholding concentrate error on true taps? Can this be proven analytically? The ISTA convergence theory (e.g., Beck & Teboulle 2009) provides convergence guarantees but does not characterize the error distribution across support vs. non-support taps.
**Why it matters**: A theoretical analysis would significantly strengthen the mechanism contribution. Even a simple analysis showing that the soft-thresholding operator's proximal mapping property implies error concentration on the support would be valuable.
**Suggestion**: Consider adding a brief theoretical analysis (even informal/the sketch-level) explaining why soft-thresholding concentrates error on true taps. This could be based on the proximal mapping interpretation of ISTA.
**Severity**: Major

---

## Detailed Comments

### Literature Review
- **Coverage**: Good coverage of deep unfolding (Gregor 2010, Chen 2018, Borgerding 2020, Liu 2023) and classical methods (OMP, LASSO, LMS/NLMS). The CNN/Transformer comparison section is comprehensive.
- **Missing**: FISTA (Beck & Teboulle 2009) is cited but not compared against experimentally. SAMP, CoSaMP, and SP are not mentioned. The deep unfolding literature for channel estimation (Gao 2023 survey) could be more extensively discussed.
- **Integration quality**: The literature review is well-organized with clear thematic structure.

### Theoretical Framework
- **Appropriateness**: The ISTA/LISTA formulation is standard and correct. The proximal gradient descent interpretation is appropriate.
- **Application depth**: The theoretical framework is used to motivate the LISTA architecture but is not deeply applied to analyze the experimental findings.
- **Alternative frameworks**: The paper could benefit from discussing the AMP (Approximate Message Passing) framework as an alternative to ISTA for sparse recovery, particularly since LISTA-AMP (Liu 2023) is mentioned.

### Academic Argument Quality
- **Factual accuracy**: Technical claims are generally accurate. The ISTA formulation (Eq. 3-6) is correct. The parameter count formula (Eq. 8) is correct.
- **Argument logic**: The logical flow is clear. However, the argument that error concentration is a "LISTA mechanism" (rather than a soft-thresholding mechanism) is not adequately supported — see W1.
- **Terminology precision**: "Deep unfolding" and "LISTA" are used correctly. The distinction between "NMSE" (linear ratio) and "NMSE in dB" is properly maintained.

### Contribution to the Field
- **Incremental contribution**: The ablation study and SNR mitigation analysis are genuine incremental contributions. The mechanism analysis is potentially more significant but needs the ISTA control experiment.
- **Positioning**: The paper positions itself well as an "analysis" paper rather than a "method" paper. However, this positioning requires deeper insights than a methods paper.
- **Overclaiming**: The abstract's claim that error concentration "provides direct evidence explaining LISTA's BER behavior" is slightly overstated — the evidence is correlational (error concentration co-occurs with BER advantage), not causal.

### Missing Key References
1. **Beck & Teboulle (2009)**, "A Fast Iterative Shrinkage-Thresholding Algorithm for Linear Inverse Problems," *SIAM J. Imaging Sciences* — FISTA is the natural comparison for LISTA and should be experimentally compared.
2. **Dai & Milenkovic (2009)**, "Subspace Pursuit for Compressive Sensing Signal Reconstruction," *IEEE TIT* — SP is an important sparse recovery baseline.
3. **Do & Gan (2008)**, "Fast Subspace Tracking Algorithm for Sparse Channel Estimation" — relevant for adaptive sparse channel estimation context.
4. **Huang & Bhatt (2023)**, "Deep Unfolding for Sparse Channel Estimation: A Survey" — recent survey directly relevant to this work's positioning.

---

## Questions for Authors

1. Can you run standard ISTA (fixed thresholds, 20 iterations) and compute the error sparsity metrics (Table 12) to determine whether the error concentration is LISTA-specific or generic to soft-thresholding?
2. Can you add FISTA as a baseline with L=20 iterations? This directly tests whether LISTA's learned parameters provide improvement over standard accelerated ISTA.
3. The abstract claims LISTA "requiring no sparsity knowledge" — but OMP requires K as input while LISTA's training data is generated with K=5. If the test sparsity differs from training (Table 2), LISTA degrades. How robust is this "no sparsity knowledge" claim?

---

## Minor Issues

- Table 6: The LMS and NLMS values for ITU channels appear to be single values (not mean ± std). Please clarify whether these are from a single seed or averaged.
- Section 2.1: The sentence "OMP iteratively selects the atom most correlated with the residual" could be more precise: OMP selects the atom with the largest absolute inner product with the residual.
- Table 8: The p-values (0.42-0.62) suggest that LISTA and LISTA-CP are indistinguishable. This is expected but the table could be shortened to a single sentence in the text.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 58 | Weak-Adequate | Mechanism analysis framing is useful but may not be LISTA-specific; limited baseline comparison |
| Methodological Rigor (25%) | 75 | Strong | Comprehensive experiments; 20-seed ablation is excellent; missing FISTA comparison |
| Evidence Sufficiency (25%) | 70 | Adequate-Strong | Good evidence for ablation and generalization; mechanism analysis needs ISTA control |
| Argument Coherence (15%) | 72 | Adequate-Strong | Clear structure but the "LISTA mechanism" argument has a logical gap |
| Writing Quality (15%) | 82 | Strong | Professional, well-organized, honest about limitations |
| Literature Integration | 65 | Adequate | Good coverage but missing key baselines (FISTA, SAMP, CoSaMP) |
| **Weighted Average** | **70** | **Major Revision** | |
