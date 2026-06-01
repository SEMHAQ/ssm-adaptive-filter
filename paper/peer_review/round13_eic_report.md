# Peer Review Report — EIC

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 13

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief

### Reviewer Identity
Senior Associate Editor of *Digital Signal Processing* (Elsevier), specializing in model-based and data-driven signal processing algorithms, with expertise in sparse recovery and adaptive filtering.

### Review Focus
Journal fit, originality of the "mechanism analysis" framing, overall quality and coherence of the manuscript, and significance for the DSP readership.

---

## Overall Assessment

### Recommendation
**Minor Revision**

### Confidence Score
**4** — High confidence; well within my area of editorial expertise.

### Summary Assessment

This paper presents a systematic investigation of LISTA (Learned ISTA) applied to sparse multipath channel estimation. Rather than claiming architectural novelty, the paper positions itself as an "analysis" paper, focusing on understanding LISTA's behavior, error structure, and generalization properties. The key finding is that LISTA concentrates 99.9% of its estimation error on true tap locations (vs. 94.9% for OMP), which provides tangible BER benefits under ZF equalization for 16-QAM — though this advantage is masked under standard MMSE equalization.

The paper is well-structured, methodologically rigorous (20-seed ablation with effect sizes, 200-realization BER simulations with paired t-tests), and commendably honest about LISTA's limitations (13-33 dB NMSE gap with OMP, SNR saturation at -25 dB). The writing is clear and professional. However, the core contribution — the "mechanism analysis" — needs stronger justification as to why this constitutes a meaningful advance beyond what is already known about soft-thresholding behavior. Additionally, some claims about hardware deployment need qualification. These issues are addressable in a minor revision, and the paper would make a solid contribution to *Digital Signal Processing*.

---

## Strengths

### S1: Honest and Transparent Reporting of Limitations
The paper is unusually transparent about LISTA's shortcomings. It explicitly reports the 13-33 dB NMSE gap with OMP (Table 1), the SNR saturation at -25 dB, training divergence at N=256, and the fact that Python speedup reflects interpreter overhead rather than algorithmic efficiency. This honesty strengthens credibility and is commendable for a deep learning paper.

### S2: Comprehensive Statistical Validation
The 20-seed ablation study with paired t-tests and Cohen's d effect sizes (Table 11) is well-designed. The progression from 5-seed (underpowered) to 20-seed experiments demonstrates methodological awareness. The 200-realization BER simulations with paired statistical tests are appropriate for the claims made.

### S3: Mechanism Analysis Provides Genuine Insight
The error sparsity analysis (Table 12) revealing that LISTA concentrates 99.9% of error on true taps vs. 94.9% for OMP is a concrete, measurable finding. The generalization of this mechanism to ITU channels (Table 14) strengthens the result. This goes beyond simple benchmarking.

### S4: Well-Structured Experimental Design
The paper covers a comprehensive experimental space: SNR sweep, sparsity sweep, channel length sweep, depth analysis, generalization (sparsity/SNR/channel mismatch), ITU channels, LISTA-CP comparison, SNR mitigation, and BER analysis. The experiments are logically ordered and each builds on previous findings.

---

## Weaknesses

### W1: Contribution Framing Needs Strengthening
**Problem**: The paper positions itself as a "mechanism analysis" paper, but the core finding — that soft-thresholding concentrates error on true taps — may be considered an inherent property of the soft-thresholding operator rather than a novel insight about LISTA specifically. Any estimator using soft-thresholding (including standard ISTA) would likely exhibit similar error concentration.
**Why it matters**: If the mechanism is generic to soft-thresholding rather than specific to LISTA's learned parameters, the contribution is diminished. The paper does not demonstrate that LISTA's *learned* thresholds produce qualitatively different error concentration than fixed ISTA thresholds.
**Suggestion**: Add an experiment comparing LISTA's error concentration against standard ISTA with fixed thresholds. If ISTA shows similar concentration, reframe the contribution as characterizing the mechanism in the channel estimation context rather than discovering a LISTA-specific property.
**Severity**: Major

### W2: ZF Equalization Results May Overstate Practical Relevance
**Problem**: The BER advantage under ZF equalization (Tables 9-10) is presented as a key finding, but ZF equalization is rarely used in modern receivers. The paper acknowledges this but still devotes significant space to ZF results. Under MMSE (the practical standard), all estimators converge — which the paper correctly notes but frames as "expected behavior."
**Why it matters**: If the primary BER finding is "LISTA works as well as OMP under MMSE" and "LISTA is better under ZF (which nobody uses)," the practical contribution is limited. The ZF results are valuable as diagnostic tools but should not be over-emphasized.
**Suggestion**: Restructure the BER section to lead with MMSE results as the primary practical finding, then present ZF results explicitly as a diagnostic tool for understanding error structure. Reduce the emphasis on ZF BER "advantages" in the abstract and highlights.
**Severity**: Minor

### W3: Hardware Complexity Claims Need Tighter Qualification
**Problem**: While the paper is generally honest about theoretical vs. measured hardware results, the statement "LISTA's fixed-depth feedforward architecture is more amenable to pipelining" appears multiple times without sufficient qualification. The FLOP analysis (Table 7) actually shows LISTA requires 2.3× more FLOPs than OMP, contradicting the narrative of LISTA being computationally advantageous.
**Why it matters**: Readers may misinterpret the pipelining claim as a demonstrated advantage rather than a theoretical possibility. The Wei et al. (2022) FPGA reference is cited but the paper's own experiments do not validate hardware performance.
**Suggestion**: Consolidate hardware discussion into a single section with clear "theoretical analysis" vs. "measured results" labels. Add a brief paragraph explicitly stating that the pipelining advantage is hypothesis-generating, not demonstrated, and that per-estimate FLOP cost favors OMP.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is accurate and descriptive. "Systematic Analysis" is appropriate given the breadth of experiments.
- Abstract is comprehensive but slightly long (~250 words). The 4 highlights are well-chosen.

### Introduction
- Well-structured with clear enumeration of 6 contributions. However, contribution (1) ("systematic analysis") is somewhat generic — every paper claims systematic analysis. The specific findings should be front-loaded.
- The distinction between "mechanism analysis" and "performance benchmarking" is important but could be made more sharply.

### Literature Review
- Good coverage of deep unfolding, CNN/Transformer methods, and classical adaptive filtering.
- The qualitative comparison with CNN/Transformer (Table 6) is reasonable but acknowledges its limitations appropriately.

### Experiments
- Comprehensive and well-organized. The cross-table consistency note (Section 4.3) is a good addition.
- The LISTA-CP comparison (Section 4.8) is somewhat anticlimactic — the result (identical performance) is expected given that the constraint is never activated. This could be shortened.

### Discussion
- The "Is the saturation architecture-specific or a training artifact?" discussion is valuable.
- The "When is ZF equalization relevant?" subsection is well-argued.

### Conclusion
- Accurately summarizes findings without overclaiming. Good.

---

## Questions for Authors

1. Can you demonstrate that LISTA's error concentration is qualitatively different from what standard ISTA (with fixed thresholds) would achieve? If ISTA shows similar concentration (e.g., 99% on true taps), the mechanism is generic to soft-thresholding and the contribution framing should be adjusted.
2. The abstract states LISTA "requiring no sparsity knowledge" — but the training data is generated with known K=5. How does the model behave when the training sparsity distribution is broader (e.g., K uniformly sampled from 2-10)?

---

## Minor Issues

- Section 4.8 (LISTA-CP): The result that clipping is never activated could be summarized in 2-3 sentences rather than a full subsection.
- Table 6 (DL comparison): The caption should more explicitly state that CNN/Transformer values are from different studies with different experimental setups.
- The "Python benchmarks show 33× faster LISTA inference" claim in the abstract could be qualified to avoid misleading readers about computational efficiency.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | Mechanism analysis is a useful framing but the core finding (soft-thresholding concentrates error) may be considered inherent to the operator |
| Methodological Rigor (25%) | 78 | Strong | 20-seed ablation with effect sizes, 200-realization BER with paired t-tests; 5-seed experiments underpowered but acknowledged |
| Evidence Sufficiency (25%) | 80 | Strong | Comprehensive experiments across multiple dimensions; ITU channel validation strengthens claims |
| Argument Coherence (15%) | 82 | Strong | Clear logical flow from problem to mechanism to implications |
| Writing Quality (15%) | 85 | Strong | Professional, honest, well-organized; minor verbosity in some sections |
| **Weighted Average** | **78** | **Minor Revision** | |

---

## Recommendation to Peer Reviewers

I ask the methodology reviewer (R1) to pay particular attention to: (1) whether the 5-seed experiments have adequate statistical power for the claims made, and (2) whether the cross-table consistency issue (8 dB difference between Tables 1 and 3) is adequately explained. I ask the domain reviewer (R2) to evaluate whether the mechanism analysis contribution is genuinely novel or an expected consequence of soft-thresholding. I ask R3 to assess the hardware deployment claims for practical realism.
