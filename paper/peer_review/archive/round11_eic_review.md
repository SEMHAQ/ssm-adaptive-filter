# EIC Review Report

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 11

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief

### Reviewer Identity
Prof. Elena Vasquez, Editor-in-Chief of *Digital Signal Processing*, specializing in adaptive signal processing and sparse recovery algorithms.

### Review Focus
Journal fit, originality, overall quality, structural coherence, and significance for the DSP readership.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
**4** — Mostly within my area of expertise, high confidence.

### Summary Assessment

This paper presents a systematic analysis of LISTA (Learned ISTA) for sparse channel estimation, covering NMSE performance, BER mechanism analysis, ablation studies, generalization experiments, and theoretical hardware complexity. The paper is well-structured and unusually honest about its findings — notably, it openly reports that LISTA trails OMP by 13–33 dB in NMSE and frames the contribution as mechanism analysis rather than performance superiority.

The BER mechanism analysis (error concentration on true taps) is the paper's most novel contribution, providing insight into why LISTA can achieve competitive BER despite worse NMSE. The ablation study with 20 seeds and statistical validation (paired t-tests, Cohen's d) is methodologically sound. The paper fits well within DSP's scope, addressing an active research area at the intersection of deep learning and sparse signal processing.

However, several issues prevent immediate acceptance: (1) the title promises more than the paper delivers — "Systematic Analysis" is appropriate, but the paper does not claim architectural novelty, making the scope narrower than a full system analysis; (2) some claims about hardware throughput advantage are hedged with caveats but still feel overstated for a paper with no measured hardware results; (3) the qualitative comparison with CNN/Transformer methods (Table in Section 5.2) lacks direct experimental validation and relies on published results from different experimental setups. These are addressable in a minor revision.

---

## Strengths

### S1: Honest and Transparent Presentation
The paper is remarkably transparent about LISTA's limitations. The NMSE saturation at −25 dB is explicitly attributed to "a training artifact caused by the scale-invariant loss and mixed-SNR training" (Abstract), and the authors clearly state that LISTA "trails OMP by 13–33 dB" (Section 4.1). This honesty strengthens credibility and is commendable.

### S2: Novel BER Mechanism Analysis
The error concentration analysis (Section 4.12) is the paper's most valuable contribution. The finding that LISTA concentrates 99.9% of estimation error on true taps (vs. 94.9% for OMP), with 50× less error on non-support taps, provides genuine insight into the BER–NMSE disconnect. The generalization of this mechanism to ITU channels (99.3–99.5%) further strengthens the finding.

### S3: Rigorous Ablation with Statistical Power
The progression from 5-seed ablation (insufficient power) to 20-seed ablation with paired t-tests and Cohen's d effect sizes demonstrates methodological maturity. The finding that the initial 5-seed results were "false negatives attributable to low statistical power" is an important methodological lesson.

### S4: Comprehensive Experimental Design
The paper covers SNR sweep, sparsity sweep, channel length sweep, depth analysis, generalization, ITU channels, LISTA-CP comparison, BER with MMSE/ZF, and hardware complexity — a thorough experimental characterization.

### S5: Practical Deployment Guidance
Section 4.7 provides actionable deployment recommendations (SNR-specific training, LISTA/OMP fallback framework), which is valuable for practitioners.

---

## Weaknesses

### W1: Hardware Throughput Claims Remain Theoretical
**Problem**: The paper claims "theoretical pipeline analysis suggesting potential for hardware throughput advantage over OMP" (Abstract, Conclusion) but provides no measured FPGA/ASIC results. Despite repeated caveats ("subject to implementation-dependent factors"), the claim appears in the abstract and highlights.
**Why it matters**: For DSP readers, hardware claims without measured results are a significant concern. The theoretical FLOP analysis (760K vs 332K) actually shows LISTA is 2.3× more expensive per estimate.
**Suggestion**: Either (a) remove the hardware throughput claim from the abstract/highlights and discuss it only in Section 4.13 as a theoretical possibility, or (b) add simulation results with a hardware synthesis tool (even Vivado HLS resource estimates).
**Severity**: Major

### W2: Qualitative CNN/Transformer Comparison
**Problem**: Table in Section 5.2 compares LISTA with CNN and Transformer methods using "published results on comparable (but not identical) channel models." This is acknowledged as "indirect" comparison but still presented as a structured table with specific NMSE ranges.
**Why it matters**: Comparing results across different studies with different channel models, SNR ranges, and training protocols is misleading, even with caveats.
**Suggestion**: Either (a) remove the table and keep only the qualitative textual comparison, or (b) clearly label the table as "illustrative only — not a fair benchmark" with a footnote explaining why direct comparison is impossible.
**Severity**: Minor

### W3: Abstract Length and Density
**Problem**: The abstract is excessively long (~350 words) and dense, listing many specific numbers (760K FLOPs, 2.3× OMP, 8.7× less than LASSO, 99.9%, 50×, etc.) that overwhelm the reader.
**Why it matters**: DSP's abstract guidelines typically recommend 150–250 words. The current abstract reads like a compressed version of the entire paper.
**Suggestion**: Reduce to ~200 words, focusing on the problem, approach, key findings (NMSE saturation, error concentration mechanism, BER advantage under ZF), and main conclusion. Move specific numbers to the main text.
**Severity**: Minor

---

## Detailed Comments

### Journal Fit
- Excellent fit for *Digital Signal Processing*. The paper addresses sparse channel estimation using deep unfolding, a topic at the core of the journal's scope.
- The readership (signal processing researchers and engineers) would find the mechanism analysis and practical deployment guidance valuable.

### Originality
- The paper explicitly disclaims architectural novelty, positioning itself as a "systematic analysis." This is appropriate and honest.
- The BER mechanism analysis (error concentration on true taps) is genuinely novel and provides insight not available in prior LISTA work.
- The ablation with statistical significance testing sets a new standard for deep unfolding studies.

### Significance
- The paper fills a gap in understanding LISTA's behavior for channel estimation, particularly the BER–NMSE disconnect.
- The practical deployment recommendations (SNR-specific training, LISTA/OMP fallback) are actionable.
- The significance is moderate — this is a solid analysis paper, not a breakthrough.

### Structural Coherence
- The paper flows logically: problem → method → experiments → discussion → conclusion.
- The contribution list in the introduction (6 items) is comprehensive but could be more concise.
- The cross-table consistency note (Section 4.3) is helpful but suggests the experimental design could have been more unified.

### Title & Abstract
- Title is accurate but long. Consider: "Deep-Unfolded LISTA for Sparse Channel Estimation: BER Mechanism, Ablation, and Generalization"
- Abstract needs significant compression (see W3).

### Conclusion
- Well-aligned with the findings. Appropriately acknowledges limitations.
- The conclusion is honest about the NMSE gap and theoretical nature of hardware claims.

---

## Questions for Authors

1. The SNR saturation at −25 dB is attributed to the scale-invariant loss and mixed-SNR training. Have you experimented with alternative loss functions (e.g., weighted NMSE that penalizes errors at high SNR more heavily) to see if the saturation can be broken without SNR-specific training?
2. The error concentration mechanism (99.9% on true taps) is fascinating. Is this a consequence of the soft-thresholding operator specifically, or would other sparsity-promoting activations (e.g., ReLU with bias) produce similar concentration?

---

## Minor Issues

### Language / Grammar
- Abstract: "SNR-specific training significantly mitigates the saturation, achieving −31 dB at SNR=20 dB (a 6 dB improvement)" — consider "SNR-specific training mitigates the saturation, achieving −31 dB at SNR = 20 dB (a 6 dB improvement over broad-range training)" for clarity.

### Figures and Tables
- Table 1 (NMSE vs SNR): The table is well-formatted. Consider adding a row for SNR = 35 dB to show the transition between 30 and 40 dB.
- Figure references should be checked — some experiments reference figures but the figure files may not be included in the review version.

### Layout
- The highlights section is dense. Consider reducing to 4 points maximum.

---

## Recommendation to Peer Reviewers

I ask the reviewers to pay special attention to:
1. **R1 (Methodology)**: Please verify the statistical claims in the ablation study — specifically whether 20 seeds provides sufficient power for the reported effect sizes.
2. **R2 (Domain)**: Please assess whether the BER mechanism analysis (error concentration on true taps) is a genuinely new finding or has been reported in related work.
3. **R3 (Perspective)**: Please evaluate whether the hardware throughput claims are appropriate given the theoretical nature of the analysis.
