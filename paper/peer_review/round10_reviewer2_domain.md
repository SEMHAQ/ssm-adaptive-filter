# Peer Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 10

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert

### Reviewer Identity
Senior Researcher at a national laboratory, specializing in sparse channel estimation and compressed sensing for wireless communications. 20+ years of experience with OMP, LASSO, ISTA, and their variants. Published extensively on FPGA-based channel estimators and deep unfolding for physical-layer processing. Familiar with the LISTA literature from its inception through recent variants (OCLISTA, LISTA-AMP, LISTA-CP).

### Review Focus
Completeness and accuracy of the literature review, fairness and completeness of baseline comparisons, domain contribution to the sparse channel estimation field, and positioning relative to recent LISTA variants.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
5 — Sparse channel estimation and deep unfolding are my primary research areas.

### Summary Assessment
This paper applies standard LISTA to sparse channel estimation and provides a thorough empirical characterization. The paper's main strength is its intellectual honesty in reporting that LISTA trails OMP by 13–33 dB in NMSE, and its BER mechanism analysis showing that LISTA concentrates estimation error on true tap locations. However, from a domain perspective, the paper has significant limitations: (1) the NMSE gap with OMP is so large (13–33 dB) that LISTA cannot be considered a practical alternative for applications where estimation accuracy matters, (2) the BER equivalence under MMSE is trivially expected and does not constitute a contribution, (3) the mechanism analysis, while insightful, is conducted only on i.i.d. Gaussian channels and may not generalize to realistic correlated channels, and (4) the paper does not compare against recent LISTA variants (OCLISTA, LISTA-AMP) that may achieve better performance. The paper would be strengthened by providing the mechanism analysis on ITU channels, comparing against more LISTA variants, and more clearly delineating which findings are novel versus which confirm known behavior.

---

## Strengths

### S1: Thorough Generalization Analysis Across Multiple Dimensions
The paper evaluates generalization across sparsity mismatch (Table 2), SNR mismatch (Table 1), channel length variation (Table 3), and cross-distribution transfer (Gaussian to ITU, Table 8). This multi-dimensional generalization analysis is more comprehensive than most LISTA papers, which typically evaluate only on the training distribution. The finding that LISTA generalizes to ITU channels with comparable performance (−23 to −27 dB) is practically useful.

### S2: BER Mechanism Analysis Provides Novel Domain Insight
Section 4.12 is the paper's strongest domain contribution. The finding that LISTA's soft-thresholding operator concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP) explains a non-obvious phenomenon: why a method with 13–33 dB worse NMSE can achieve comparable or better BER. The three-part analysis (support recovery, error sparsity, noise enhancement) provides a complete mechanistic explanation. This insight is novel to the best of my knowledge and has implications for equalizer design.

### S3: Comprehensive Ablation Reveals What LISTA Learns
The 20-seed ablation (Table 13) reveals that the per-layer threshold schedule is the dominant contributor (+14–18 dB degradation), not the learnable mapping W^(k) (+1.24 dB). This is an important domain insight: LISTA's primary learned behavior is a layer-specific progression of threshold values, not the preconditioning matrix. This finding has implications for designing efficient LISTA variants that share W^(k) across layers.

### S4: SNR Saturation Mitigation is Practically Actionable
The demonstration that SNR-specific training improves NMSE by ~6 dB (from −25 to −31 dB, Table 10) provides a practical deployment strategy. The finding that the improvement is consistent across different narrow-range strategies ([15,25], [18,22], [20,30]) suggests robustness to the exact range choice.

### S5: LISTA-CP Diagnostic Analysis is Informative
The analysis of why LISTA and LISTA-CP perform identically (Section 4.8)—the weight clipping constraint is never activated because spectral norms remain below 0.35—provides useful domain knowledge about the behavior of LISTA's learned parameters.

---

## Weaknesses

### W1: The 13–33 dB NMSE Gap Undermines Practical Value
**Problem**: LISTA trails OMP by 13–33 dB in NMSE at SNR ≥ 10 dB (Table 1). Even with SNR-specific training, the gap is ~6 dB (Table 10). For many practical applications (channel sounding, propagation analysis, coherent detection), this gap is unacceptable.
**Why it matters**: The paper positions LISTA as a "practical alternative for sparse channel estimation" (Abstract), but the NMSE performance does not support this claim for applications where estimation accuracy is the primary metric. The paper acknowledges this ("when NMSE is the primary metric, use OMP"), but the overall framing is still somewhat optimistic.
**Suggestion**: Reposition the paper more explicitly as a "characterization study" rather than a "LISTA is practical" paper. The contribution is understanding LISTA's behavior, not demonstrating its superiority. The deployment recommendation framework (Section 5.3) is good but should lead with "LISTA is suitable only when speed is critical and moderate accuracy is acceptable."
**Severity**: Major

### W2: BER Equivalence Under MMSE is Trivially Expected
**Problem**: The paper devotes significant space (Tables 7-8, Section 4.10.1) to demonstrating that under MMSE equalization, all estimators converge to similar BER at SNR ≥ 5 dB. The paper itself acknowledges this is "expected behavior, not a special property of LISTA" (Table 7 caption). Yet this trivially expected result is presented as a major finding.
**Why it matters**: Presenting expected behavior as a contribution inflates the paper's apparent novelty. The MMSE BER equivalence is a consequence of MMSE's design (the regularization term 1/SNR suppresses noise enhancement differences), not a finding about LISTA.
**Suggestion**: Significantly shorten the MMSE BER section (currently ~1000 words + 2 tables). A single paragraph stating the expected result with one supporting table is sufficient. Redirect the saved space to the mechanism analysis (which is the genuine contribution) and to ITU channel mechanism analysis.
**Severity**: Major

### W3: Mechanism Analysis Limited to i.i.d. Gaussian Channels
**Problem**: The error sparsity analysis (Table 15), noise enhancement analysis (Table 16), and support recovery analysis (Table 14) are all conducted on i.i.d. Gaussian channels with K=5, N=64, M=256. Real wireless channels (ITU models) have correlated tap amplitudes and non-uniform power delay profiles, which may fundamentally alter the error concentration behavior.
**Why it matters**: If LISTA's error concentration on true taps is specific to i.i.d. Gaussian channels (where taps are uncorrelated), the mechanism analysis has limited practical relevance. The soft-thresholding operator's behavior may differ when tap amplitudes are correlated.
**Suggestion**: Repeat the error sparsity analysis (Table 15) for ITU PedA and VehA channels. Even if the results are similar, explicitly confirming this significantly strengthens the contribution. If the results differ, that is also valuable information.
**Severity**: Critical

### W4: No Comparison Against Recent LISTA Variants
**Problem**: The paper compares against LISTA-CP (Section 4.8) but not against OCLISTA (Borgerding et al., 2020) or LISTA-AMP (Liu et al., 2023), which are mentioned in the related work. These variants have improved convergence properties and may achieve better NMSE.
**Why it matters**: Without comparison against state-of-the-art LISTA variants, the paper's results may be specific to the standard LISTA architecture and not representative of the deep unfolding approach's potential.
**Suggestion**: Add a comparison against at least one recent variant (OCLISTA or LISTA-AMP). If computational resources are limited, a brief discussion of expected performance differences based on the literature would be helpful.
**Severity**: Major

### W5: The "33× Speedup" Claim is Misleading
**Problem**: The paper reports a "33× faster inference" (0.21 vs 6.91 ms) in the abstract and throughout the paper. This is a Python benchmark comparing interpreted LISTA (matrix operations) vs. iterative OMP (with Python loop overhead). The speedup reflects software implementation differences, not algorithmic efficiency.
**Why it matters**: The FLOP analysis (Table 14) shows LISTA requires 2.3× more FLOPs than OMP, meaning LISTA is algorithmically slower. The 33× speedup is an artifact of Python's overhead on iterative algorithms. Presenting this as a speedup is misleading.
**Suggestion**: Reframe the runtime comparison as "LISTA's fixed-depth feedforward architecture is more amenable to efficient implementation than OMP's iterative structure" rather than claiming a "33× speedup." The FLOP comparison (2.3× OMP) should be the primary complexity reference.
**Severity**: Major

---

## Detailed Comments

### Literature Review (Section 2)
- Coverage of deep unfolding (LISTA, ISTA-Net, OCLISTA, LISTA-AMP) is comprehensive.
- CNN/Transformer comparison (Section 5.2) is useful but indirect. The paper correctly acknowledges this.
- The classical adaptive filtering section (Section 2.4) is brief but adequate.
- Missing: recent work on learned AMP (LAMP, LISTA-AMP) and their theoretical convergence properties.

### Proposed Method (Section 3)
- The LISTA architecture (Section 3.3) follows the standard formulation. No novelty here.
- The FFT-based convolution implementation (Equation 8) is a standard optimization.
- The parameter analysis (Section 3.4) is clear and useful.

### Experiments (Section 4)
- Table 1 (NMSE vs SNR): LISTA's saturation at −25 dB is clearly demonstrated.
- Table 2 (NMSE vs Sparsity): The divergence at K=15 is concerning for practical deployment.
- Table 3 (NMSE vs Channel Length): The divergence at N=256 is a significant scalability limitation.
- Table 4 (Depth Analysis): The plateau at L=10 is useful practical guidance.
- Table 8 (ITU Channels): The −23 to −27 dB performance is comparable to Gaussian saturation, indicating limited ability to exploit channel structure.

### Discussion (Section 5)
- Section 5.1 (Gaussian vs ITU) provides valuable practical guidance.
- Section 5.2 (DL comparison) is well-handled with appropriate caveats.
- Section 5.3 (Deployment framework) is actionable but somewhat optimistic given the NMSE gap.
- Section 5.4 (Limitations) is honest and thorough.

---

## Questions for Authors

1. Can you provide the error sparsity analysis (Table 15) for ITU channels? This single addition would significantly strengthen the mechanism analysis's generalizability.

2. Have you attempted to train LISTA with a non-scale-invariant loss function (e.g., absolute MSE instead of NMSE) to test whether the saturation is truly a training artifact vs. an architectural limitation?

3. The paper mentions OCLISTA and LISTA-AMP in the related work but does not compare against them. What is the expected performance difference, and could you provide at least a brief theoretical analysis?

4. For the ZF BER advantage (Table 11), the 16-QAM improvement at SNR ≥ 15 dB is statistically significant (p < 0.05) but the absolute BER difference is small (e.g., 0.305 vs 0.316 at SNR=20 dB). Is this difference practically significant for real communication systems?

---

## Minor Issues

### Literature
- Reference [liu2023listamp] should be verified for completeness (year, journal/conference).
- The paper cites [wei2022fpga] for FPGA LISTA implementation—confirm this reference exists and is correctly characterized.

### Tables
- Table 16 (noise enhancement) reverses at SNR=30 dB (OMP 6.1 vs LISTA 25.3). This reversal is noted but deserves more discussion—it suggests LISTA's advantage is SNR-dependent, not universal.

### Figures
- Figure references (Figures 1-4) are consistent with the text.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 52 | Weak | No new architecture. BER mechanism analysis is novel. Standard LISTA applied to channel estimation. |
| Methodological Rigor (25%) | 70 | Adequate | Good experimental design. Limited sample sizes in main tables. Asymmetric baseline comparison. |
| Evidence Sufficiency (25%) | 68 | Adequate | Comprehensive experiments but mechanism analysis limited to Gaussian channels. No comparison vs recent LISTA variants. |
| Argument Coherence (15%) | 78 | Strong | Clear logical flow. Some overclaiming in abstract/deployment framework. |
| Writing Quality (15%) | 80 | Strong | Professional, honest, well-structured. |
| Literature Integration | 65 | Adequate | Good coverage of LISTA/CNN/Transformer. Missing recent LISTA variants (OCLISTA, LISTA-AMP) in experiments. |
| **Weighted Average** | **69** | **Major Revision** | Domain concerns about NMSE gap, trivially expected MMSE results, and limited mechanism analysis scope. |
