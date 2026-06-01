# Peer Review Report — Peer Reviewer 2 (Domain Expert)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 9

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain Expert)

### Reviewer Identity
Prof. Maria Rodriguez, Department of Telecommunications, Universidad Politécnica de Madrid. Expertise in sparse channel estimation, OFDM systems, and FPGA implementation of signal processing algorithms. 18 years of experience in wireless communications research.

### Review Focus
Literature completeness and positioning, domain-specific claims about channel estimation, validity of channel models used, and hardware complexity analysis accuracy. I evaluate whether the paper correctly positions itself within the sparse channel estimation literature and whether the domain-specific claims are well-supported.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
5 — Completely within my area of expertise, I am very confident in my assessment

### Summary Assessment
This paper provides a thorough analysis of LISTA applied to sparse multipath channel estimation, covering NMSE performance, BER analysis, ablation studies, generalization, and hardware complexity. The domain-specific contributions are solid: the BER mechanism analysis (error concentration on true taps) provides genuine insight, the ITU channel experiments add practical relevance, and the SNR-specific training mitigation offers a practical solution to the saturation problem.

The literature review is comprehensive, covering sparse channel estimation, deep unfolding, and deep learning for channel estimation. However, I have concerns about the hardware complexity claims (which go beyond what FLOP analysis can support), the scalability analysis (which doesn't address structured alternatives to the full W^(k) matrix), and the channel model validity (i.i.d. Gaussian taps are a significant simplification). These concerns are addressable and the paper makes a solid contribution to the DSP literature.

---

## Strengths

### S1: Comprehensive Literature Positioning
The paper positions itself well within three distinct literatures: sparse channel estimation (Section 2.1), deep unfolding (Section 2.2), and deep learning for channel estimation (Section 2.3). The comparison framework against OMP, LASSO, LMS, and NLMS is standard and appropriate. The inclusion of recent LISTA variants (LISTA-CP, OCLISTA, LISTA-AMP) shows awareness of the current state of the art. The explicit statement "Rather than claiming architectural novelty, we focus on understanding LISTA's behavior" (Section 2.3) is honest and well-positioned.

### S2: BER Mechanism Analysis — Novel Domain Insight
The finding that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP) is a genuine contribution to the channel estimation literature. This explains the NMSE-BER disconnect that has been observed but not previously analyzed in detail. The error sparsity analysis (Gini coefficient, support vs. non-support error distribution) provides a new analytical framework that could be applied to other sparse recovery algorithms. The distinction between MMSE and ZF equalization contexts is well-motivated and correctly identifies when LISTA's error structure provides tangible benefits.

### S3: Practical Deployment Analysis
The paper goes beyond NMSE reporting to address practical deployment considerations: inference time (0.21 ms for LISTA vs. 6.91 ms for OMP), parameter count (82K), FLOP counts (760K for LISTA vs. 332K for OMP), memory access patterns, and scalability analysis. While the hardware throughput claims are overstated (see W1), the qualitative analysis of parallelism characteristics and memory access patterns is valuable for practitioners considering LISTA deployment.

### S4: ITU Channel Model Experiments
The inclusion of ITU PedA and VehA channel models (Section 4.7) adds significant practical relevance. These models feature exponentially decaying power delay profiles with correlated tap amplitudes, unlike the i.i.d. Gaussian taps used for training. The finding that LISTA generalizes across channel types (achieving -23 to -27 dB on ITU channels) is practically important and demonstrates the robustness of the mixed-SNR training approach.

---

## Weaknesses

### W1: Hardware Throughput Claims Are Overstated
**Problem**: The paper claims "2-6× hardware throughput advantage over OMP" based on FLOP counts and theoretical pipeline analysis (Section 4.13). However, this analysis makes several assumptions that are not validated: (1) 64 parallel DSP units at 500 MHz — this is a specific mid-range FPGA configuration, not a general result; (2) the analysis ignores memory bandwidth, which is often the bottleneck for matrix-vector multiplications; (3) pipeline stall analysis from inter-layer data dependencies is omitted; (4) the 4.4× point estimate is presented with unwarranted precision.

**Why it matters**: Hardware throughput is a key practical claim for the channel estimation community. Practitioners reading this paper may make deployment decisions based on the 2-6× claim. Without measured results, this could be misleading.

**Suggestion**: Reframe as "FLOP comparison suggests potential for pipelining advantage" and remove the specific 4.4× point estimate. Keep the FLOP counts (which are valid) and the qualitative parallelism analysis (which is useful). Add a table comparing FLOP counts, memory requirements, and parallelism characteristics without extrapolating to throughput.

**Severity**: Major

### W2: Scalability Analysis Missing Structured Alternatives
**Problem**: The scalability analysis (Table 11) shows that LISTA's parameters grow as O(N²), reaching 1.3M at N=256. The paper notes that "structured linear mappings (Toeplitz, circulant, low-rank) are essential for scaling LISTA to longer channels" but does not analyze any structured alternatives. The training divergence at N=256 (Table 3) is presented as a fundamental limitation without exploring whether structured W^(k) could resolve it.

**Why it matters**: The N² scaling is a known limitation of standard LISTA. The paper should either (a) experiment with at least one structured alternative, or (b) more clearly position the N=256 failure as a limitation of the specific architecture variant used, not of LISTA in general.

**Suggestion**: Add a brief experiment or discussion of structured W^(k) alternatives (e.g., Toeplitz, circulant, low-rank factorization). At minimum, cite the relevant literature on structured LISTA variants and discuss how they would affect the scalability analysis.

**Severity**: Major

### W3: Channel Model Validity Concerns
**Problem**: The primary experiments use i.i.d. Gaussian tap amplitudes, which is a significant simplification of real wireless channels. While the ITU channel experiments (Section 4.7) partially address this, the i.i.d. Gaussian model ignores several important channel characteristics: (1) tap correlation arising from the physical propagation environment, (2) frequency-dependent path loss, (3) Doppler effects in time-varying channels, (4) non-Gaussian tap distributions (e.g., Rayleigh, Rician).

**Why it matters**: The paper's conclusions about LISTA's generalization behavior are based primarily on i.i.d. Gaussian channels. The ITU experiments show comparable performance, but these are still simplified models. Practitioners may overestimate LISTA's robustness based on these results.

**Suggestion**: Add a discussion paragraph acknowledging the channel model limitations and identifying specific scenarios where the i.i.d. Gaussian assumption may fail (e.g., correlated multipath, non-stationary channels). The ITU experiments are a good start; consider adding at least one experiment with correlated tap amplitudes.

**Severity**: Minor

### W4: Missing Comparison with State-of-the-Art LISTA Variants
**Problem**: The paper compares against LISTA-CP (Section 4.8) but not against OCLISTA (Borgerding et al., 2020) or LISTA-AMP (Liu et al., 2023), which are mentioned in the related work as having improved convergence properties. The discussion hypothesizes that "these variants would exhibit similar saturation under broad-range mixed-SNR training" (Section 5.1) but this is not experimentally verified.

**Why it matters**: OCLISTA and LISTA-AMP represent the current state of the art for LISTA variants. Without comparison, readers cannot assess whether the findings are specific to standard LISTA or apply to the broader class of deep-unfolded architectures.

**Suggestion**: Either (a) include experimental comparison with at least one state-of-the-art LISTA variant (OCLISTA is relatively easy to implement), or (b) more clearly state that the analysis is specific to standard LISTA and that the behavior of improved variants is an open question.

**Severity**: Minor

### W5: Oversampling Ratio Not Systematically Studied
**Problem**: The paper uses M=256 (pilot length) with N=64 (channel length), giving an oversampling ratio M/N=4. The channel length experiment (Table 3) varies N while fixing M=256, so the oversampling ratio changes from 8 (N=32) to 1 (N=256). The training divergence at N=256 is attributed to insufficient oversampling, but this is not systematically studied.

**Why it matters**: The oversampling ratio is a critical parameter for sparse recovery. The paper's conclusions about LISTA's scalability are confounded by the changing oversampling ratio. A systematic study varying M/N would provide more insight.

**Suggestion**: Add a brief experiment varying M/N at fixed N=64 to isolate the effect of oversampling ratio from channel length. This would strengthen the scalability analysis.

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title accurately describes the paper's scope.
- Abstract is comprehensive but very long. The repeated caveats about hardware estimates create a defensive tone.
- The abstract's BER mechanism claims are well-formulated.

### Literature Review (Section 2)
- Excellent coverage of sparse channel estimation (Bajwa, Berger, OMP, LASSO).
- Good coverage of deep unfolding (Gregor, Sprechmann, Wisdom, He, Chen, Borgerding, Liu).
- Comprehensive coverage of deep learning for channel estimation (CNN, Transformer, model-driven).
- Missing: recent work on structured LISTA variants and hardware-efficient deep unfolding.

### Methodology (Section 3)
- Standard LISTA architecture, well-described.
- Parameter analysis is helpful.
- FFT-based convolution implementation is practical.
- Missing: discussion of complex-valued extensions (real-valued model is a limitation for practical systems).

### Experiments (Section 4)
- Comprehensive experimental design covering 13 experiments.
- NMSE vs. SNR (Table 1): Results are clear. The 13-33 dB gap with OMP is substantial.
- Sparsity (Table 2): Results are clear. Training instability at K=15 is noted.
- Channel length (Table 3): Cross-table consistency note is helpful. Training divergence at N=256 is well-documented.
- Depth (Table 4): Practical recommendation of L=10-20 is reasonable.
- Ablation (Tables 5, 9): The 20-seed study is exemplary.
- Generalization (Section 4.6): The three mismatch scenarios are well-chosen.
- ITU channels (Table 11): Important practical contribution.
- LISTA-CP (Table 10): Diagnostic analysis of why clipping is never activated is insightful.
- SNR mitigation (Table 12): Practical and useful.
- BER (Tables 6-8): 200 realizations is strong. MMSE vs. ZF distinction is well-motivated.
- Mechanism (Tables 13-15): Novel analysis framework.
- Hardware (Tables 16-17): FLOP counts are valid; throughput estimates are speculative.

### Discussion (Section 5)
- Section 5.1 (saturation analysis) is thorough and well-argued.
- Section 5.2 (deep learning comparison) is qualitative — the weakest section.
- Section 5.3 (deployment framework) is practical and useful.
- Section 5.4 (limitations) is honest and comprehensive.

### Conclusion
- Well-structured summary of findings.
- Hardware claims appropriately hedged.
- Future research directions are relevant and specific.

---

## Questions for Authors

1. Have you considered testing LISTA with structured W^(k) matrices (Toeplitz, circulant, low-rank) to address the N² scalability limitation? This would significantly strengthen the scalability analysis.

2. The paper uses real-valued channel models. How would the findings extend to complex-valued channels, which are standard in practical wireless systems? Are there any fundamental differences in LISTA's behavior for complex-valued signals?

3. The BER mechanism analysis shows LISTA concentrates error on true taps. Is this behavior preserved for channels with correlated tap amplitudes (e.g., ITU models), or does it depend on the i.i.d. Gaussian assumption?

---

## Minor Issues

### Literature
- Missing reference to structured LISTA variants (e.g., circulant LISTA, low-rank LISTA).
- The comparison with CNN/Transformer (Table 8) should note that NMSE values are from different studies with different experimental setups.

### Channel Model
- The i.i.d. Gaussian tap model is standard but simplified. Consider adding a sentence acknowledging this.
- The ITU channel experiments use only SNR=20 dB. A brief SNR sweep on ITU channels would be more informative.

### Hardware Analysis
- The FLOP comparison (Table 16) is well-done.
- The scaling analysis (Table 11) is useful.
- The parallelism characteristics discussion is valuable.
- The throughput estimates should be reframed as theoretical bounds.

### Writing
- Section 4.13 is very long (almost 3 pages). Consider splitting into separate FLOP and pipeline sections.
- The repeated hardware caveats are honest but excessive. Consider consolidating.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | BER mechanism analysis is novel; rest is comprehensive but incremental |
| Methodological Rigor (25%) | 70 | Strong | Good experimental design; hardware claims need reframing |
| Evidence Sufficiency (25%) | 72 | Strong | Comprehensive experiments; missing structured LISTA variants |
| Argument Coherence (15%) | 74 | Strong | Clear logical flow; honest about limitations |
| Writing Quality (15%) | 68 | Adequate | Generally clear; some repetition; hardware section too long |
| Literature Integration | 70 | Good | Comprehensive coverage; missing some recent structured LISTA work |
| **Weighted Average** | **69.8** | **Minor Revision** | |

---

## Final Assessment

The paper makes a solid contribution to the sparse channel estimation literature. The BER mechanism analysis is the standout contribution, providing genuine insight into why deep-unfolded architectures may be suitable for BER-critical applications. The main concerns are: (1) hardware throughput claims need significant reframing, (2) scalability analysis should address structured alternatives, and (3) channel model validity could be strengthened. These are addressable with minor revisions. The paper is well-suited for publication in *Digital Signal Processing* after addressing these concerns.

**Overall Score: 70/100 — Minor Revision**
