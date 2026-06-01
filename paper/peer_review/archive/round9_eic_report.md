# Peer Review Report — Editor-in-Chief

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 9

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC)

### Reviewer Identity
Prof. Elena Marchetti, Associate Editor for *Digital Signal Processing*. Expertise in sparse signal recovery, compressed sensing, and adaptive filtering. 20+ years editorial experience with focus on bridging theory and practice in signal processing.

### Review Focus
Journal fit, originality, overall significance, clarity of presentation, and relevance to the DSP readership. I assess whether the paper makes a meaningful contribution to the sparse channel estimation literature and whether it meets the standards of *Digital Signal Processing*.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
4 — Mostly within my area of expertise, high confidence

### Summary Assessment
This paper provides a systematic analysis of LISTA (Learned ISTA) applied to sparse multipath channel estimation. The authors investigate generalization behavior, component contributions via ablation studies, BER performance with statistical validation, and practical deployment characteristics including theoretical hardware complexity. The paper is well-structured and addresses a legitimate research question: understanding the behavior of deep-unfolded architectures in the channel estimation context.

The paper's primary strength is its honesty about LISTA's limitations—the NMSE saturation at ~-25 dB is explicitly acknowledged and analyzed as a training artifact rather than hidden. The BER mechanism analysis (error concentration on true taps) is a genuine contribution that explains the NMSE-BER disconnect. The ablation study with 20 seeds and proper statistical testing (paired t-tests, Cohen's d) meets modern reproducibility standards.

However, the paper has a notable weakness: the core claim of "2-6× hardware throughput advantage" is entirely theoretical with no measured FPGA/ASIC results. While the authors are transparent about this, the repeated emphasis on hardware advantages without empirical validation weakens the practical contribution. The NMSE gap with OMP (13-33 dB) is substantial and raises questions about whether LISTA is truly competitive for this application. I recommend Minor Revision to address the hardware claims framing and strengthen the positioning.

---

## Strengths

### S1: Honest and Transparent Reporting of Limitations
The paper explicitly acknowledges LISTA's NMSE saturation at ~-25 dB and the 13-33 dB gap with OMP. Rather than hiding these limitations, the authors provide a detailed analysis attributing the saturation to the scale-invariant loss and mixed-SNR training (Section 5.1). This level of transparency is commendable and strengthens the paper's credibility. The statement "the saturation is likely a training artifact rather than a fundamental architectural limitation" (p. 15) is well-supported by the SNR-specific training experiments.

### S2: BER Mechanism Analysis as Primary Contribution
The BER-NMSE disconnect analysis (Section 4.12) is the paper's most valuable contribution. The finding that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP), validated with 200 channel realizations and proper statistical testing, provides genuine insight into why deep-unfolded architectures may be suitable for BER-critical applications despite worse NMSE. The distinction between MMSE and ZF equalization contexts is well-articulated.

### S3: Rigorous Ablation Study Design
The progression from 5-seed to 20-seed ablation (Sections 4.5 and 4.11) demonstrates methodological maturity. The authors correctly identify that the initial 5-seed experiment had insufficient statistical power (~15-20% for medium effects) and follow up with a properly powered study. Reporting both parametric (paired t-tests) and effect sizes (Cohen's d) with the 20-seed results is exemplary. The finding that the per-layer threshold schedule is the dominant contributor (+14-18 dB) while W^(k) provides a secondary +1.24 dB contribution is well-supported.

### S4: Comprehensive Experimental Design
The paper covers 13 experiments spanning NMSE vs. SNR, sparsity, channel length, depth analysis, ablation, generalization, LISTA-CP comparison, SNR mitigation, BER performance, error mechanism analysis, and hardware complexity. This breadth provides a thorough characterization of LISTA's behavior. The inclusion of ITU channel models (PedA, VehA) adds practical relevance.

---

## Weaknesses

### W1: Hardware Throughput Claims Lack Empirical Validation
**Problem**: The paper repeatedly claims "2-6× hardware throughput advantage over OMP" (Abstract, Introduction, Conclusion) based entirely on theoretical FLOP counts and pipeline analysis. No measured FPGA or ASIC results are provided. The Python speedup of 33× reflects software overhead differences, not hardware performance.

**Why it matters**: Hardware throughput claims are a significant practical selling point of the paper. Without measured results, these claims remain speculative and may mislead readers about LISTA's actual deployment readiness.

**Suggestion**: Either (a) tone down the hardware claims significantly, replacing "2-6× throughput advantage" with "theoretical analysis suggests potential for pipelining advantage" consistently throughout, or (b) add a clear disclaimer box near the first hardware claim stating that all hardware estimates are theoretical and unvalidated. The current text does include caveats, but they are often buried in lengthy paragraphs.

**Severity**: Major

### W2: NMSE Gap with OMP Undermines Practical Value Proposition
**Problem**: LISTA trails OMP by 13-33 dB on i.i.d. Gaussian channels. While the BER analysis shows convergence under MMSE, the NMSE gap means LISTA is unsuitable for applications where channel estimation accuracy matters directly (e.g., channel sounding, propagation analysis). The paper acknowledges this but does not adequately address whether the 13-33 dB gap is acceptable for the target application domain.

**Why it matters**: Reviewers and readers will question why a method with 13-33 dB worse NMSE should be published. The BER mechanism analysis partially addresses this, but the practical relevance needs stronger framing.

**Suggestion**: Add a clearer decision framework early in the paper (not just in Section 5.3) that specifies when LISTA is preferred vs. when OMP/LASSO should be used. The current framework in Section 5.3 is good but comes too late.

**Severity**: Minor

### W3: Repetition of Key Claims
**Problem**: The BER mechanism analysis findings (99.9% error concentration, 50× less non-support error, 1.8× noise enhancement advantage) are repeated at least 6 times: Abstract, Introduction, Experiments (Section 4.10, 4.12), Discussion (Section 5.1), and Conclusion. While some repetition is expected in academic papers, this level of redundancy is excessive.

**Why it matters**: Excessive repetition makes the paper feel padded and may irritate reviewers. It also dilutes the impact of the finding by making it seem like the paper has only one contribution.

**Suggestion**: Consolidate the BER mechanism findings. Present the full analysis in Section 4.12, summarize in Section 5.1, and reference back from the Abstract/Introduction/Conclusion. Remove the redundant detailed explanations in Sections 4.10 and 4.12's summary paragraphs.

**Severity**: Minor

### W4: Missing Comparison with Modern Deep Learning Methods
**Problem**: The paper provides only a qualitative comparison with CNN and Transformer methods (Section 5.2, Table 8) based on published results rather than direct experimental comparison. The rationale ("our focus is on understanding LISTA's behavior within the deep unfolding paradigm") is reasonable but insufficient for a comprehensive analysis paper.

**Why it matters**: Readers will naturally want to know how LISTA compares with current state-of-the-art deep learning approaches. A qualitative comparison based on different studies with varying experimental setups is not convincing.

**Suggestion**: At minimum, add a paragraph in the Discussion acknowledging this as a significant limitation and specifying what a fair comparison would require (same channel models, SNR ranges, training protocols). If possible, include at least one CNN baseline in the experiments.

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title is accurate and descriptive. "Analysis" correctly positions this as an analytical study rather than a novel architecture paper.
- The abstract is comprehensive but excessively long (~400 words). Consider condensing to 250-300 words for readability.
- The abstract's repeated caveats ("subject to implementation-dependent factors", "measured FPGA/ASIC results remain future work") are honest but create a defensive tone.

### Introduction
- The six contributions are clearly enumerated and well-described.
- The positioning is honest: "Rather than claiming architectural novelty, we focus on understanding LISTA's behavior."
- Contribution 6 (hardware complexity) could be better integrated with the others rather than feeling like an afterthought.

### Literature Review
- Comprehensive coverage of sparse channel estimation, deep unfolding, and deep learning for channel estimation.
- The comparison framework (vs. OMP, vs. LASSO/ISTA, vs. LMS/NLMS) is well-structured.
- Missing recent work on state-of-the-art LISTA variants (OCLISTA, LISTA-AMP) — these are mentioned but not compared against experimentally.

### Methodology
- The LISTA architecture description is clear and follows the standard formulation.
- The parameter analysis (82K parameters for N=64) is helpful.
- The training procedure is well-documented (Adam, cosine annealing, gradient clipping).

### Results
- The 13 experiments provide comprehensive coverage.
- Tables and figures are well-formatted.
- The cross-table consistency note (Section 4.3) is a nice touch showing methodological awareness.
- The 20-seed ablation is a strength.

### Discussion
- Section 5.1 (saturation analysis) is thorough and well-argued.
- Section 5.2 (comparison with deep learning) is the weakest section — qualitative only.
- Section 5.3 (deployment framework) is practical and useful.
- Section 5.4 (limitations) is honest and comprehensive.

### Conclusion
- Well-structured summary of findings.
- The conclusion appropriately hedges hardware claims with "subject to implementation-dependent factors."

### References
- 42 references, mostly peer-reviewed, recent (2018-2024), appropriate for the field.
- Good coverage of both classical (OMP, LASSO, ISTA) and modern (LISTA-CP, OCLISTA) methods.

---

## Questions for Authors

1. The NMSE saturation at ~-25 dB is attributed to the scale-invariant loss and mixed-SNR training. Have you investigated whether a *weighted* NMSE loss (e.g., emphasizing high-SNR samples during training) could break the saturation while maintaining broad-range generalization?

2. The BER mechanism analysis shows LISTA concentrates 99.9% of error on true taps. Is this a consequence of the soft-thresholding operator specifically, or would any sparse-inducing activation function produce similar error concentration? Have you tested alternative thresholding functions (e.g., hard thresholding, smooth approximation)?

3. For the hardware complexity claims, what is the estimated timeline for FPGA validation? The theoretical analysis is reasonable, but measured results would significantly strengthen the paper's practical contribution.

---

## Minor Issues

### Language / Grammar
- Abstract: "likely a training artifact from the scale-invariant loss" — "likely" weakens the claim; consider "primarily attributable to"
- Section 4.12: "the NMSE metric is agnostic to error location" — "agnostic" is slightly informal; consider "insensitive to"
- Throughout: excessive use of em-dashes for parenthetical statements; consider using parentheses for some

### Citation Format
- Consistent use of natbib author-year format throughout
- No formatting issues detected

### Figures and Tables
- All tables follow CAS template formatting
- Figure references are consistent
- Consider adding a summary table comparing all methods across all experiments

### Layout
- The paper is well-structured with clear section headings
- FloatBarrier commands appropriately placed
- Table widths are consistent

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 62 | Adequate | Applies existing LISTA to channel estimation; BER mechanism analysis is novel but incremental |
| Methodological Rigor (25%) | 72 | Strong | Good statistical practices (20 seeds, t-tests, Cohen's d), but hardware claims lack validation |
| Evidence Sufficiency (25%) | 70 | Strong | Comprehensive experiments, but missing direct CNN/Transformer comparison and FPGA results |
| Argument Coherence (15%) | 75 | Strong | Clear logical flow, honest about limitations, well-structured contributions |
| Writing Quality (15%) | 68 | Adequate | Generally clear but excessively repetitive; abstract too long |
| **Weighted Average** | **69.4** | **Minor Revision** | |

---

## Final Assessment

The paper makes a solid contribution to understanding LISTA's behavior for sparse channel estimation. The BER mechanism analysis is the standout contribution. The paper is honest about limitations, which is refreshing. The main concerns are: (1) hardware claims need stronger framing as theoretical, (2) excessive repetition of key findings, and (3) missing direct comparison with modern deep learning baselines. These are addressable with minor revisions.

**Overall Score: 69/100 — Minor Revision**
