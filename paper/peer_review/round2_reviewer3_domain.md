# Peer Review Report — Reviewer 2 (Domain)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 2

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain Expert)

### Reviewer Identity
Prof. Dr. Ahmed Al-Dhahab, Professor of Wireless Communications, King Fahd University of Petroleum and Minerals. Specialization: sparse channel estimation, compressed sensing for communications, MIMO systems, and pilot design. Author of 60+ papers on channel estimation. Associate Editor for IEEE Transactions on Wireless Communications. Reviewer for IEEE TCOM, IEEE TVT, Signal Processing (Elsevier).

### Review Focus
Literature coverage, theoretical framework, domain contribution, and positioning within the sparse channel estimation field. I evaluate whether the paper correctly understands and advances the state-of-the-art in sparse channel estimation.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
5 — Sparse channel estimation and compressed sensing for communications are my primary research areas. I have published extensively on OMP, LASSO, and deep learning approaches for channel estimation.

### Summary Assessment
This paper evaluates LISTA for sparse channel estimation through 9 experiments covering SNR, sparsity, channel length, depth, ablation, generalization, ITU channels, runtime, and SNR mitigation. The domain knowledge is adequate, and the paper correctly identifies the key trade-offs (speed vs. accuracy, training distribution vs. generalization). However, the paper has significant domain-level issues: (1) the 13-33 dB gap with OMP is inadequately discussed in the context of communications system requirements, (2) the missing BER analysis leaves the practical impact unquantified, (3) the literature review omits several important recent works on deep learning for channel estimation, and (4) the paper does not discuss the fundamental limits of deep unfolding for sparse recovery. The paper is a competent application study but needs deeper domain engagement. I recommend Major Revision.

---

## Strengths

### S1: Correct Problem Formulation and Sparse Recovery Framework
The paper correctly formulates the sparse channel estimation problem (Section 3.1) and presents the ISTA/LISTA framework accurately. The connection between ISTA iterations and neural network layers (Section 3.2) is clearly explained. The FFT-based convolution implementation (Section 3.3) is a practical optimization that shows domain awareness.

### S2: Fair Comparison with Properly Tuned Baselines
The comparison with OMP (oracle K), LASSO (grid-searched λ), LMS, and NLMS (grid-searched step sizes) is fair and well-designed. The use of oracle sparsity for OMP is acknowledged, and the per-SNR optimization ensures that baselines are not unfairly disadvantaged. This level of baseline care is often missing in deep learning papers.

### S3: ITU Channel Model Evaluation
Testing on ITU PedA and VehA models (Section 4.7.2) is a significant strength. These models feature exponentially decaying power delay profiles and correlated tap amplitudes, which are more realistic than i.i.d. Gaussian taps. The finding that LISTA generalizes to ITU channels without channel-specific training is practically useful.

### S4: SNR-Specific Training as Mitigation Strategy
The SNR-specific training results (Section 4.9) are the most practically valuable finding. The 6 dB improvement from narrow-range training addresses the most significant limitation (NMSE saturation) and provides a clear deployment strategy.

---

## Weaknesses

### W1: Missing BER Analysis — The Most Critical Gap
**Problem**: The paper evaluates NMSE but never translates to BER. For communications systems, BER is the ultimate metric. A -25 dB NMSE may or may not be acceptable depending on the modulation, coding rate, and detection scheme. The paper claims LISTA is "a practical alternative" but cannot substantiate this without BER results.
**Why it matters**: The sparse channel estimation literature (Bajwa 2010, Berger 2010, Elbir 2023) typically evaluates BER alongside NMSE. Omitting BER makes the paper incomplete for the target journal.
**Suggestion**: Add a BER simulation using QPSK or 16-QAM with a standard receiver (e.g., MMSE equalizer). Show BER vs. SNR curves for all methods. This single addition would significantly strengthen the paper's contribution.
**Severity**: Critical

### W2: Literature Gaps — Missing Key Recent Works
**Problem**: The Related Work (Section 2) omits several important works:
- Deep learning-based channel estimators (CNN, transformer) that do not use deep unfolding but compete in the same space
- Learned denoising-based approaches (e.g., LISTA variants with learned denoisers)
- Recent works on adaptive step-size ISTA that share LISTA's motivation
- Papers on computational complexity analysis of deep unfolding for real-time systems
**Why it matters**: The paper positions itself against OMP/LASSO/LMS but not against the broader landscape of deep learning approaches for channel estimation. This makes the contribution appear more novel than it is.
**Suggestion**: Expand the Related Work to include (a) CNN/transformer-based channel estimators, (b) other LISTA variants (LISTA-CP, OCLISTA, LISTA-SS), and (c) computational complexity analyses for real-time deployment. Position LISTA within this broader landscape.
**Severity**: Major

### W3: Inadequate Discussion of the 13-33 dB Gap with OMP
**Problem**: The paper reports that LISTA trails OMP by 13-33 dB at SNR ≥ 10 dB (Table 1) but does not adequately discuss the implications. In linear scale, a 13 dB gap means OMP has ~20× lower error, and a 33 dB gap means ~2000× lower error. For communications, this translates directly to BER degradation.
**Why it matters**: The paper's main claim is that LISTA is a "practical alternative" to OMP, but the gap is so large that this claim is questionable without BER evidence. The paper should either (a) show that the gap doesn't matter for BER in specific scenarios, or (b) honestly acknowledge that LISTA is not a replacement for OMP when accuracy matters.
**Suggestion**: Add a frank discussion of what the 13-33 dB gap means in practice. Quantify the BER impact. Discuss scenarios where the gap is acceptable (e.g., low-order modulation, high coding gain) vs. unacceptable (e.g., high-order modulation, low coding gain).
**Severity**: Major

### W4: Channel Model Limitations — Only Real-Valued, Single-Antenna
**Problem**: The paper uses only real-valued channels and single-antenna systems. Real wireless channels are complex-valued, and modern systems use MIMO. The BPSK pilot assumption (Section 4.1) is simplistic — real systems use QAM pilots.
**Why it matters**: The generalization claims may not hold for complex-valued channels or MIMO systems. The BPSK restriction limits the practical applicability.
**Suggestion**: (1) Extend to complex-valued channels and QAM pilots. (2) Discuss how the framework would extend to MIMO. (3) If restricted to real-valued for simplicity, explicitly state this limitation and its implications.
**Severity**: Major

### W5: No Comparison with Learned AMP or Other Deep Unfolding Variants
**Problem**: The paper compares LISTA against OMP, LASSO, and LMS/NLMS but not against other deep unfolding approaches for sparse recovery, such as:
- Learned Approximate Message Passing (LAMP)
- LISTA-CP (only compared in Section 4.8 with identical results)
- OCLISTA (Onsager-corrected LISTA)
- ISTA-Net
**Why it matters**: Without comparison against other deep unfolding variants, the reader cannot assess whether LISTA is the best choice within its family.
**Suggestion**: Add comparisons with at least LAMP and OCLISTA. If the implementations are not available, discuss the expected differences based on the literature.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title accurately reflects the paper's content. "Analysis of" correctly signals a characterization study.
- The abstract is well-structured and honest. The quantitative results are clearly stated.

### Introduction
- The introduction correctly identifies the research problem and motivation. The five contributions are clearly enumerated.
- Contribution (1) is methodology, not a finding. Consider restructuring to lead with the ablation insights.

### Literature Review / Theoretical Framework
- Coverage of compressed sensing and deep unfolding is adequate but incomplete (see W2).
- The distinction from prior work (Section 2.2, last paragraph) is clear but could be sharper.
- Missing: discussion of fundamental limits of deep unfolding for sparse recovery (e.g., sample complexity, recovery guarantees).

### Methodology / Research Design
- The problem formulation (Section 3.1) is standard and correct.
- The LISTA architecture (Section 3.3) is the standard formulation with no modifications. This is both a strength (simplicity) and a weakness (no novelty).
- The computational complexity analysis (Section 3.6) is useful but incomplete — it doesn't account for the training cost.

### Results / Findings
- The SNR saturation (Table 1) is the key finding. The paper correctly identifies this as a limitation.
- The sparsity robustness (Table 2) is well-analyzed. The divergence at K=15 is honestly reported.
- The channel length scalability (Table 3) reveals a practical limit (N=256 diverges). This is important for deployment.
- The depth analysis (Table 4) shows diminishing returns beyond L=10. This is useful for practitioners.
- The ITU channel results (Table 6) are practically relevant. The cross-distribution generalization is a genuine finding.

### Discussion
- Section 5.1's saturation explanation is plausible but needs experimental validation.
- Section 5.2's practical framework is useful but incomplete without BER.
- Section 5.3's limitations are honestly stated.

### Conclusion
- The conclusion is accurate and appropriately modest. The positioning as "when speed is prioritized" is correct.

### References
- References are adequate but incomplete (see W2). The mix of seminal and recent works is appropriate for what is cited.

---

## Questions for Authors

1. **BER Results**: Can you add BER simulations using QPSK or 16-QAM with an MMSE equalizer? This would immediately clarify whether LISTA's NMSE is acceptable for practical systems.

2. **Complex-Valued Extension**: Can you extend the framework to complex-valued channels? Real wireless channels are complex-valued, and the restriction to real-valued channels limits the practical applicability.

3. **Training Cost**: What is the training time for LISTA? For practical deployment, the total cost (training + inference) should be compared against OMP/LASSO (which require no training).

4. **Comparison with LAMP/OCLISTA**: Can you compare against other deep unfolding variants (LAMP, OCLISTA) to position LISTA within its family?

---

## Minor Issues

### Citation Format
- Some citations use \citet and others use \citet* inconsistently. Standardize.
- The ITU reference (itut2017guidelines) should include the full ITU document number.

### Figures and Tables
- Table 1: Missing ± values for LMS, NLMS, OMP, LASSO. Are these deterministic? If so, state this explicitly.
- Figure 2: The K=15 outlier makes the figure hard to read. Consider a separate panel or inset.

### Layout
- No significant layout issues.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 52 | Weak | Standard LISTA applied to known problem; no architectural contribution |
| Methodological Rigor (25%) | 65 | Adequate | Good experimental design; fair baselines; limited statistical power |
| Evidence Sufficiency (25%) | 58 | Weak | Missing BER, complex-valued channels, comparison with other DL methods |
| Argument Coherence (15%) | 68 | Adequate | Clear structure; practical claims not fully supported |
| Writing Quality (15%) | 72 | Strong | Clear, professional; minor citation inconsistencies |
| Literature Integration | 58 | Weak | Missing key recent works on DL for channel estimation |
| **Weighted Average** | **62.4** | **Adequate** | **Major Revision recommended** |
