# Peer Review Report — Peer Reviewer 2 (Domain Expert)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 12

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert (Sparse Channel Estimation & Compressed Sensing)

### Reviewer Identity
Prof. Marcus Wei, Full Professor of Wireless Communications. Expertise in sparse channel estimation, compressed sensing for communications, OFDM systems, and MIMO signal processing. Published 80+ papers on compressed channel estimation and its applications to 5G/6G systems. Deep knowledge of OMP, LASSO, ISTA, and their theoretical recovery guarantees.

### Review Focus
Literature coverage completeness, theoretical framework appropriateness, domain contribution significance, and positioning within the sparse channel estimation literature. This review assesses whether the paper makes a meaningful contribution to the channel estimation community.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
5 — Sparse channel estimation and compressed sensing for communications are directly within my core expertise. I have published on OMP, LASSO, and ISTA-based channel estimation methods.

### Summary Assessment
This paper applies LISTA to sparse channel estimation and provides a systematic analysis of its behavior, focusing on understanding rather than novelty. The paper correctly identifies that LISTA's NMSE saturates at ~-25 dB, trailing OMP by 13-33 dB on Gaussian channels, and provides a mechanism analysis explaining LISTA's BER behavior through error concentration on true tap locations. The literature review is comprehensive, covering sparse channel estimation, deep unfolding, CNN/Transformer methods, and classical adaptive filtering. The domain contribution is primarily the error concentration mechanism (99.9% on true taps), which provides new insight into how deep-unfolded architectures differ from greedy methods in their error structure. However, the paper's positioning within the channel estimation literature could be strengthened: (1) the comparison with recent LISTA variants (OCLISTA, LISTA-AMP) is only qualitative; (2) the ITU channel evaluation is limited to two models; (3) the paper does not discuss the relationship to structured sparsity models (e.g., block sparsity, joint sparsity) that are important in practical channels. The writing is clear and the references are generally appropriate, though some may need verification. With minor revisions to strengthen the literature positioning and address the missing references, this paper is suitable for publication in DSP.

---

## Strengths

### S1: Comprehensive and Well-Organized Literature Review
The Related Work section (Section 2) provides excellent coverage across four areas: sparse channel estimation (Bajwa, Berger), deep unfolding (Gregor, Monga, Chen, Borgerding, Liu), deep learning for channel estimation (CNN, Transformer, model-driven), and classical adaptive filtering (LMS, NLMS, PNLMS). The structured comparison table in Section 5.2 positions LISTA against CNN/Transformer methods across 7 criteria. The paper correctly identifies the gap: no systematic analysis of LISTA's behavior, generalization, and error structure exists for channel estimation.

### S2: Error Concentration Mechanism — Novel Domain Insight
The finding that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP) is a genuine contribution to the channel estimation literature. This is not just a benchmarking result—it provides mechanistic understanding of why deep-unfolded architectures behave differently from greedy methods. The generalization to ITU channels (99.3–99.5%) strengthens the finding. The connection to equalizer noise enhancement (1.8× advantage) provides a clear bridge from the signal processing mechanism to the system-level BER impact.

### S3: Honest Assessment of LISTA's Limitations
The paper does not oversell LISTA's performance. It correctly states that LISTA "trails OMP by 13–33 dB" (Abstract), that the BER advantage is specific to ZF equalization, and that the hardware claims are theoretical. This honest assessment is valuable for the community—it prevents practitioners from deploying LISTA with unrealistic expectations.

### S4: Cross-Distribution Generalization Testing
Testing LISTA trained on i.i.d. Gaussian data on ITU PedA and VehA channels (Section 4.7.2) is important for practical relevance. The finding that LISTA achieves -23 to -27 dB on ITU channels (comparable to its Gaussian saturation level) without channel-specific training is useful for deployment strategy.

### S5: SNR Saturation Mitigation with Practical Guidance
The SNR-specific training experiments (Section 4.9) provide actionable guidance. The finding that narrow-range training improves NMSE by ~6 dB (from -25 to -31 dB) is practically useful. The recommendation to deploy LISTA trained on a narrow SNR range around the operating point is clear and implementable.

---

## Weaknesses

### W1: Missing Comparison with Recent LISTA Variants
**Problem**: The paper compares against LISTA-CP (Section 4.8) but does not experimentally compare against OCLISTA [Borgerding 2020] or LISTA-AMP [Liu 2023], which are mentioned in the Related Work. The paper hypothesizes that "these variants would exhibit similar saturation under broad-range mixed-SNR training" (Section 5.1) but does not verify this.
**Why it matters**: OCLISTA and LISTA-AMP are the most relevant recent LISTA variants. If they achieve better NMSE under the same training protocol, the paper's findings about LISTA's saturation may not generalize to the state-of-the-art.
**Suggestion**: At minimum, add a qualitative discussion of why the saturation findings should or should not apply to OCLISTA/LISTA-AMP. Ideally, include at least one experimental comparison with OCLISTA.
**Severity**: Major

### W2: Limited ITU Channel Evaluation
**Problem**: The ITU channel evaluation uses only PedA and VehA models (Section 4.7.2). These are relatively simple channel models with exponential power delay profiles. More challenging models (e.g., ITU Extended Pedestrian A, TDL models from 3GPP TR 38.901, or measured channel data) would better test generalization.
**Why it matters**: The paper claims "cross-distribution generalization" but only tests on two similar channel models. The error concentration mechanism may not generalize to channels with more complex delay profiles or non-exponential decay.
**Suggestion**: Add at least one additional channel model (e.g., TDL-C or TDL-D from 3GPP) to strengthen the generalization claim. If data is unavailable, acknowledge the limitation explicitly.
**Severity**: Minor

### W3: No Discussion of Structured Sparsity
**Problem**: The paper treats sparsity as purely random (uniform tap locations, Gaussian amplitudes). In practical channels, sparsity has structure: taps are clustered (block sparsity), correlated across antennas (joint sparsity), or have specific decay patterns. The paper does not discuss how LISTA's error concentration mechanism interacts with structured sparsity.
**Why it matters**: Structured sparsity is the norm in practical wireless channels. If LISTA's mechanism relies on the i.i.d. tap assumption, its practical applicability is limited.
**Suggestion**: Add a brief discussion of structured sparsity and its potential impact on LISTA's error concentration mechanism. If possible, add a supplementary experiment with block-sparse channels.
**Severity**: Minor

### W4: Incomplete Discussion of Recovery Guarantees
**Problem**: The paper mentions that LASSO has "theoretical recovery guarantees under certain conditions" (Section 3.7) and that LISTA-CP has "convergence guarantees" (Section 4.8), but does not discuss the specific conditions (e.g., RIP, mutual coherence) or how they relate to the channel estimation setting.
**Why it matters**: The channel estimation matrix $\mathbf{X}$ has specific structure (convolution matrix from BPSK pilots) that affects recovery guarantees. The paper should discuss whether the theoretical conditions are satisfied in the experimental setup.
**Suggestion**: Add a brief discussion of the recovery conditions (e.g., RIP constants, mutual coherence of $\mathbf{X}$) and whether they are satisfied for the experimental parameters. This would strengthen the theoretical positioning.
**Severity**: Minor

### W5: Reference Quality Concerns
**Problem**: Some references appear to have issues:
- Kim et al. (2021) — FPGA survey has placeholder page numbers ("123456--123470").
- The LISTA-CP citation (Chen et al., 2018) is listed as CVPR Workshops, but the paper title suggests a stronger venue may exist.
- Some references (e.g., Soltani 2019, Guo 2020, Farsad 2021, Liu 2020) are cited in the bibliography but not directly referenced in the text.
**Why it matters**: Reference quality affects the paper's credibility. Unreferenced bibliography entries suggest incomplete revision.
**Suggestion**: Verify all references. Remove unreferenced entries or add citations in the text. Correct the Kim et al. page numbers.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is appropriate for the domain: "Systematic Analysis" correctly positions the contribution.
- Abstract mentions all key findings: -25 dB saturation, 13-33 dB gap, 99.9% error concentration, ablation with 20 seeds.
- The abstract correctly states "trailing OMP by 13–33 dB"—honest positioning.

### Related Work (Section 2)
- **Sparse Channel Estimation**: Good coverage of Bajwa (2010) and Berger (2010). The discussion of OMP limitations (atom correlations) and LASSO limitations (regularization parameter tuning) is accurate.
- **Deep Unfolding**: Comprehensive coverage from Gregor (2010) through Liu (2023). The inclusion of OCLISTA and LISTA-AMP is appropriate.
- **Deep Learning for Channel Estimation**: Good structured coverage of CNN, Transformer, and model-driven methods. The surveys (Elbir 2023, Gao 2023, Wu 2024, Ma 2022) are appropriate.
- **Classical Adaptive Filtering**: Brief but adequate coverage of LMS, NLMS, PNLMS.
- **Gap identification**: The paper correctly identifies that no systematic analysis of LISTA's behavior exists for channel estimation.

### Methodology (Section 3)
- Problem formulation (Section 3.1) is standard and correct.
- LISTA architecture (Section 3.3) follows the standard Gregor (2010) formulation. The FFT-based convolution (Eq. 8) is a practical implementation detail.
- The comparison with classical methods (Section 3.7) is well-structured: vs. OMP, vs. LASSO/ISTA, vs. LMS/NLMS.

### Results (Section 4)
- The 12 experiments provide comprehensive coverage.
- The mechanism analysis (Section 4.12) is the domain contribution highlight.
- The error sparsity analysis (Table 9) with Gini coefficient is a novel metric for this domain.
- The noise enhancement analysis (Table 10) provides a clear bridge to BER performance.

### Discussion (Section 5)
- The training artifact hypothesis (Section 5.1) is well-argued.
- The qualitative CNN/Transformer comparison (Section 5.2) is useful but could be more concise.
- The practical deployment recommendations (Section 5.3) are actionable.
- The limitations (Section 5.4) are thorough.

### References
- Generally good coverage of the field.
- Some references may need verification (see W5).
- The paper cites 36 references, which is adequate for DSP.

---

## Questions for Authors

1. **OCLISTA comparison**: You hypothesize that OCLISTA would exhibit similar saturation (Section 5.1). Can you provide experimental evidence or at least a more detailed theoretical argument for why the Onsager correction terms would not break the saturation?

2. **Recovery conditions**: For your experimental setup (BPSK pilots, N=64, M=256), what is the mutual coherence of the convolution matrix $\mathbf{X}$? Does it satisfy the conditions for OMP/LASSO recovery guarantees?

3. **Structured sparsity**: Have you considered testing on channels with block sparsity (e.g., clustered taps as in urban macro cells)? The error concentration mechanism may behave differently when taps are correlated.

4. **LISTA-AMP**: The paper mentions LISTA-AMP [Liu 2023] but does not compare against it. Given that LISTA-AMP achieves "near-oracle performance on synthetic sparse recovery," how do you expect it to perform on channel estimation?

---

## Minor Issues

### Literature Positioning
- The paper's positioning as "mechanism analysis" rather than "novel architecture" is appropriate and well-executed.
- Consider adding a brief comparison with deep unfolding for other signal processing tasks (e.g., image reconstruction, source separation) to broaden the context.

### Citation Format
- Some bibliography entries are not cited in the text: Soltani (2019), Guo (2020), Farsad (2021), Liu (2020). Either cite them or remove them.
- The Kim et al. (2021) reference needs page number correction.

### Figures and Tables
- Table 9 (Error Sparsity) is the paper's key domain contribution. Consider making it more prominent (e.g., in the main text rather than a subsection).
- The comparison table in Section 5.2 is useful but relies on published results from different studies. Acknowledge the limitations of indirect comparison more prominently.

### Writing
- Section 2.3 (Deep Learning for Channel Estimation) is quite long. Consider condensing the CNN/Transformer descriptions.
- The notation is generally consistent. One minor issue: the paper uses both $\mathbf{W}^{(k)}$ and $\mathbf{W}_k$ in different places—standardize.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 70 | Adequate | No architectural novelty, but the error concentration mechanism is a genuine domain contribution. The systematic analysis approach adds value. |
| Methodological Rigor (25%) | 75 | Strong | Good experimental design with appropriate baselines. Minor concerns about LASSO convergence and oracle K for OMP. |
| Evidence Sufficiency (25%) | 68 | Adequate | Good evidence for main claims, but limited to one primary configuration and two ITU models. Missing comparison with OCLISTA/LISTA-AMP. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow from problem to mechanism analysis. The self-critical framing strengthens the argument. |
| Writing Quality (15%) | 82 | Strong | Clear, well-organized writing. Good use of tables and statistical annotations. |
| Literature Integration | 72 | Adequate | Comprehensive coverage but some gaps: missing OCLISTA/LISTA-AMP comparison, structured sparsity discussion. Some reference quality issues. |
| **Weighted Average** | **74.6** | **Minor Revision** | |

---

## Overall Score: 75/100
