# Peer Review Report — EIC

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 12

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), Digital Signal Processing (Elsevier)

### Reviewer Identity
Prof. Elena Vasquez, Editor-in-Chief. Expertise in adaptive signal processing, compressed sensing theory, and deep learning for communications. 20+ years of editorial experience at top signal processing journals. Review preferences: methodological clarity, reproducibility, and honest assessment of limitations.

### Review Focus
Journal fit, originality, overall significance, and whether the contribution is sufficient for publication in Digital Signal Processing. This review does not go deep into methodology (Reviewer 1's domain) but assesses the paper's positioning and contribution to the field.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — Mostly within my area of expertise (signal processing, compressed sensing). Deep unfolding architectures are a secondary specialty, but the channel estimation context is core.

### Summary Assessment
This paper presents a systematic analysis of LISTA (Learned ISTA) applied to sparse channel estimation, with emphasis on understanding LISTA's behavior rather than claiming architectural novelty. The paper investigates NMSE saturation at ~-25 dB, conducts a mechanism analysis explaining LISTA's BER behavior through error concentration on true tap locations, and performs comprehensive ablation studies with statistical significance testing. The work is honest about LISTA's limitations—trailing OMP by 13–33 dB in NMSE on Gaussian channels—and reframes the contribution as mechanistic understanding rather than performance superiority. The error concentration finding (99.9% on true taps vs. 94.9% for OMP) is novel and provides genuine insight into why deep-unfolded architectures behave differently from greedy methods. However, the practical impact is limited: the BER advantage only manifests under ZF equalization (not MMSE, the standard), and the NMSE gap with OMP is substantial. The paper fits well within DSP's scope. The writing is unusually clear and self-critical. With minor revisions to address the cross-table inconsistency and strengthen the practical impact argument, this paper is suitable for publication.

---

## Strengths

### S1: Honest and Transparent Self-Assessment
The paper is refreshingly candid about LISTA's limitations. Rather than inflating results, the authors explicitly state that LISTA "trails OMP by 13–33 dB" (Abstract), acknowledge the NMSE saturation as "likely a training artifact" (Section 1, Contribution 1), and note that "the Python speedup reflects software implementation overhead, not algorithmic efficiency" (Section 4.7.1). This level of honesty is rare and builds credibility. The paper correctly identifies that the BER contribution is the mechanism analysis, not the BER equivalence under MMSE (which is "expected behavior, not a special property of LISTA").

### S2: Novel Mechanism Analysis via Error Concentration
The error concentration finding (Section 4.12) is the paper's strongest contribution. Demonstrating that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP), and that this manifests as a 1.8× noise enhancement advantage under ZF equalization, provides genuine mechanistic insight. The generalization of this mechanism to ITU channels (99.3–99.5%) strengthens the finding. This is a contribution that goes beyond incremental benchmarking.

### S3: Rigorous Statistical Methodology
The ablation study progression from 5 seeds (underpowered) to 20 seeds with paired t-tests, Wilcoxon signed-rank tests, and Cohen's $d$ effect sizes (Section 4.11) demonstrates methodological maturity. The paper transparently reports that the 5-seed ablation produced false negatives for threshold and per-layer parameters, and self-corrects with the 20-seed experiment. The BER simulations use 200 realizations per SNR point with paired statistical tests—well above the typical standard in this field.

### S4: Comprehensive Scope with Practical Deployment Guidance
The paper covers an impressive breadth: NMSE vs. SNR/sparsity/channel-length/depth, ablation, generalization, BER analysis, LISTA-CP comparison, SNR mitigation, and hardware complexity. The practical deployment recommendations (Section 5.3) provide actionable guidance for engineers.

### S5: Clear Positioning Against Prior Work
The paper explicitly states it claims "no architectural novelty" and positions itself as a "mechanism analysis" (Section 1). The Related Work section (Section 2) provides good coverage of deep unfolding, CNN/Transformer methods, and classical adaptive filtering, with a structured comparison table (Table in Section 5.2).

---

## Weaknesses

### W1: Cross-Table NMSE Inconsistency May Confuse Readers
**Problem**: Table 3 (NMSE vs SNR) reports LISTA at -24.25 dB for N=64, K=5, M=256, SNR=20 dB, while Table 4 (NMSE vs channel length) reports -32.29 dB for the same nominal configuration. The paper explains this in a footnote (Table 4, §4.3) as due to "independently trained models with different training distributions," but this 8 dB discrepancy is large and may confuse readers who compare tables directly.
**Why it matters**: Readers will inevitably compare values across tables. The footnote explanation is adequate, but the discrepancy undermines confidence in the reported numbers.
**Suggestion**: Add a consolidated table or figure showing LISTA performance under both training protocols side-by-side, making the sensitivity to training distribution a first-class result rather than a footnote caveat.
**Severity**: Minor

### W2: Practical Impact Limited to ZF Equalization
**Problem**: The BER advantage under ZF equalization (Section 4.10.2, Table 11) is the paper's key system-level finding, but ZF is not the standard equalizer in modern receivers—MMSE is. Under MMSE, all estimators converge to similar BER (as the paper correctly notes). The paper frames this as "expected behavior" but this significantly limits practical relevance.
**Why it matters**: If the primary practical contribution (BER improvement) only applies to a non-standard equalizer, the real-world impact is diminished. The paper should more clearly articulate when ZF would be preferred over MMSE.
**Suggestion**: Add a brief discussion of practical scenarios where ZF equalization is preferred (e.g., low-complexity receivers, specific modulation/coding schemes, or when MMSE noise variance estimation is unreliable). This would strengthen the practical relevance argument.
**Severity**: Minor

### W3: Hardware Complexity Claims Remain Theoretical
**Problem**: The paper makes claims about "potential hardware throughput advantage" via pipelining (Section 4.13, Abstract) but explicitly acknowledges these are "theoretical estimates; measured FPGA/ASIC results remain future work." While the honesty is appreciated, the paper devotes significant space (Section 4.13, Tables 13-14) to theoretical hardware analysis that cannot be validated.
**Why it matters**: Theoretical FLOP counts and pipeline analyses are useful but do not constitute evidence of hardware advantage. The paper's contribution would be stronger if the hardware section were more concise.
**Suggestion**: Condense the hardware analysis to a single table and 1-2 paragraphs, clearly labeling it as theoretical. Move the detailed scaling analysis to an appendix or supplementary material.
**Severity**: Minor

### W4: Single-Configuration Depth
**Problem**: Almost all experiments use N=64, K=5, M=256 as the default configuration. While the paper varies one dimension at a time (SNR, sparsity, channel length, depth), the core findings are based on a single configuration. The generalization claims (Section 4.6) are limited to two ITU channel models.
**Why it matters**: The error concentration mechanism (the paper's primary contribution) is only demonstrated at K=5, N=64, M=256. It is unclear whether this mechanism holds at different sparsity levels, channel lengths, or pilot ratios.
**Suggestion**: The paper acknowledges this in Section 4.12.5 ("Extension to different sparsity levels and pilot ratios remains future work"). Consider adding at least one additional configuration (e.g., K=8, N=128) to strengthen the generalizability claim.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title accurately reflects the paper's content: "Systematic Analysis" rather than "novel method." Good positioning.
- The abstract is dense but well-structured, covering NMSE findings, BER mechanism, ablation, and mitigation. The -25 dB saturation, 13-33 dB gap with OMP, and 99.9% error concentration are all correctly highlighted.
- Minor: The abstract is quite long (~250 words). Consider trimming 1-2 sentences.

### Introduction
- The six contributions are clearly enumerated and well-differentiated. Contribution 6 (hardware) is the weakest and could be consolidated.
- The motivation for studying LISTA (rather than proposing a new architecture) is well-articulated.
- Good use of hedging language: "likely a training artifact," "subject to implementation-dependent factors."

### Literature Review
- Comprehensive coverage of sparse channel estimation, deep unfolding, and deep learning for channel estimation.
- The structured comparison table (Section 5.2, Table 12) comparing LISTA with CNN/Transformer methods is valuable but explicitly noted as indirect.
- Some references may need verification (e.g., the FPGA survey reference appears to have placeholder page numbers: "123456--123470").

### Methodology
- Clear problem formulation (Section 3.1) and LISTA architecture description (Section 3.3).
- The parameter analysis (Section 3.4) is useful for practical deployment considerations.
- Training details are well-specified (Adam optimizer, cosine annealing, gradient clipping).

### Results
- Excellent experimental breadth covering 12 experiments.
- Statistical reporting is strong: paired t-tests, Cohen's $d$, 200 realizations for BER.
- The cross-table inconsistency (W1) is the main concern.
- The mechanism analysis (Section 4.12) is the highlight.

### Discussion
- The discussion of LISTA-CP (Section 4.8) is insightful—the finding that the clipping constraint is never activated provides genuine understanding.
- The limitations section (Section 5.4) is thorough and honest.
- The qualitative CNN/Transformer comparison (Section 5.2) could be more concise.

### Conclusion
- Accurately summarizes findings without overclaiming.
- Correctly identifies the mechanism analysis as the primary contribution.

---

## Questions for Authors

1. **Training distribution sensitivity**: The 8 dB difference between Tables 3 and 4 highlights sensitivity to training distribution. Have you investigated whether a curriculum learning approach (starting with narrow SNR range, then broadening) could achieve both good peak performance and broad-range robustness?

2. **Error concentration at different sparsity**: The error concentration mechanism is demonstrated at K=5. Do you have preliminary evidence that this mechanism holds at higher sparsity (K=10-15), where LISTA's NMSE degrades significantly? If the mechanism breaks down at high sparsity, this would limit the practical applicability.

3. **LISTA-CP spectral norm**: The paper reports that $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ never exceeded 0.35. Can you report the distribution of spectral norms across layers and seeds? This would help understand whether the constraint is close to being activated or far from it.

---

## Minor Issues

### Language / Grammar
- Generally excellent English throughout. No significant grammar issues found.
- Some sentences are quite long (e.g., the abstract). Consider breaking for readability.

### Citation Format
- The FPGA survey reference (Kim et al., 2021) appears to have placeholder page numbers ("123456--123470"). Verify and correct.
- Some references use `\citet` while others use `\citep` inconsistently, though this may be a LaTeX style issue.

### Figures and Tables
- Tables are well-formatted with clear captions and footnotes.
- Consider adding a summary figure showing the paper's main findings in a single visual (e.g., a radar chart or decision tree for deployment guidance).

### Layout
- No layout issues noted. The paper uses the Elsevier CAS template correctly.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 72 | Adequate | No architectural novelty (as acknowledged), but the error concentration mechanism analysis is a genuine contribution. The systematic analysis approach with self-correction (5→20 seeds) adds value. |
| Methodological Rigor (25%) | 78 | Strong | Strong statistical methodology with 20 seeds, paired t-tests, Cohen's $d$, 200 BER realizations. Minor concern: cross-table inconsistency and single default configuration. |
| Evidence Sufficiency (25%) | 70 | Adequate | Good evidence for main claims, but limited to one primary configuration (N=64, K=5, M=256). ITU generalization tested on only 2 channel models. Hardware claims are theoretical. |
| Argument Coherence (15%) | 82 | Strong | Excellent logical flow from problem → method → experiments → mechanism analysis → implications. The self-critical framing strengthens rather than weakens the argument. |
| Writing Quality (15%) | 85 | Strong | Unusually clear and honest writing. Good use of hedging language. Minor verbosity in some sections. |
| **Weighted Average** | **76.6** | **Minor Revision** | |

---

## Overall Score: 77/100
