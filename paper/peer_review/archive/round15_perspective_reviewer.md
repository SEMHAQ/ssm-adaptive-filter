# Peer Review Report — Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 15

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Cross-disciplinary Perspective)

### Reviewer Identity
Prof.~Dr.~Stefan Schwarz, Institute of Telecommunications, TU Wien, Vienna. Specialization: machine learning for wireless systems, resource allocation, and cross-disciplinary applications of optimization theory to communications. Published on deep learning for physical layer, model-based learning, and hardware-efficient signal processing. Review philosophy: evaluate papers from the perspective of practical impact and cross-disciplinary connections.

### Review Focus
Cross-disciplinary connections, practical deployment implications, broader impact on related fields, and whether the findings generalize beyond the specific experimental setup. I will assess the paper's value for practitioners and researchers in adjacent fields.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — My expertise covers machine learning for wireless systems and hardware-efficient signal processing. The deep unfolding and channel estimation components are within my domain, though the compressed sensing theory is at the boundary.

### Summary Assessment
This paper provides a thorough empirical analysis of LISTA for sparse channel estimation, with a focus on understanding its behavior rather than claiming novelty. The error concentration mechanism is an insightful finding that connects deep unfolding behavior to equalization performance. The paper is unusually honest about LISTA's limitations, clearly stating it trails OMP and FISTA in NMSE. The practical deployment framework (Section 5.3) is useful for practitioners.

From a cross-disciplinary perspective, the paper's findings have implications for: (1) the broader deep unfolding community (the error concentration mechanism may generalize to other unfolded architectures), (2) hardware design (the theoretical complexity analysis provides design guidelines), and (3) the compressed sensing community (the ISTA control experiment provides new quantitative data on soft-thresholding properties). However, the paper would benefit from: (a) discussing how the error concentration findings apply to complex-valued channels (real-valued only is a significant limitation), (b) connecting to the broader model-based deep learning literature, and (c) discussing implications for MIMO systems where the channel matrix structure is different.

---

## Strengths

### S1: Honest and Actionable Deployment Guidance
Section 5.3 provides a clear decision framework for practitioners: when to use LISTA (throughput-critical, known SNR), when to prefer OMP/FISTA (NMSE-critical), and how to configure training. The SNR-specific training mitigation (6 dB improvement) is a practical contribution that can be immediately applied. This kind of honest, actionable guidance is rare in the deep learning literature.

### S2: Error Concentration as a Cross-Architecture Insight
The finding that LISTA concentrates 100.0% of error on true taps (vs. 92.4% for ISTA) has implications beyond LISTA. If this property generalizes to other deep-unfolded architectures (e.g., unfolded ADMM, unfolded primal-dual), it could explain why these architectures often achieve good BER despite mediocre NMSE. The paper should discuss this cross-architectural potential.

### S3: Comprehensive Generalization Analysis
The generalization experiments (sparsity mismatch, SNR mismatch, channel length, ITU models, pilot ratio) provide a complete picture of LISTA's operating envelope. The pilot ratio analysis (Table 6) is particularly useful for system design, establishing $M/N \geq 2$ as a minimum requirement.

### S4: LISTA-CP Diagnostic Analysis
The LISTA-CP comparison (Section 4.8) goes beyond simple performance comparison to provide diagnostic insight: the weight clipping constraint is never activated because spectral norms remain below 0.35. This kind of diagnostic analysis adds genuine understanding and is more valuable than a simple "no significant difference" statement.

### S5: FISTA Comparison Clarifies LISTA's Value
The FISTA comparison (Table 13) is crucial for positioning LISTA's value. By showing FISTA outperforms LISTA by 1--27 dB in NMSE, the paper honestly clarifies that LISTA's value lies in the error concentration mechanism and potential hardware pipelining, not NMSE accuracy. This is valuable guidance for practitioners choosing between methods.

---

## Weaknesses

### W1: Real-Valued Channel Assumption Limits Generalizability
**Problem**: The entire analysis assumes real-valued channels ($\mathbf{h} \in \mathbb{R}^N$) and real-valued pilot signals (BPSK-modulated, $\pm 1$). Real wireless channels are complex-valued, and practical systems use QAM modulations with complex baseband signals. The soft-thresholding operator (Eq. 7) and the error concentration metric are defined for real-valued signals only.
**Why it matters**: The complex-valued case introduces phase ambiguity and the soft-thresholding operator must be extended to the complex domain (typically by thresholding the magnitude). The error concentration mechanism may behave differently for complex-valued channels because the phase component introduces additional degrees of freedom. This significantly limits the practical applicability of the findings.
**Suggestion**: Either (a) extend the analysis to complex-valued channels with QAM pilots, or (b) add a prominent disclaimer that all results are for real-valued channels and discuss how the findings might change for complex-valued channels.
**Severity**: Major

### W2: No Discussion of Time-Varying Channels
**Problem**: The analysis assumes static channels (each realization is independent). Real wireless channels are time-varying, and adaptive filtering methods (LMS/NLMS) are designed to track these variations. LISTA, being a feedforward network, cannot adapt to channel changes without retraining.
**Why it matters**: The comparison with LMS/NLMS is somewhat unfair because LMS/NLMS can track time-varying channels while LISTA cannot. The paper should discuss this limitation and assess whether LISTA's error concentration mechanism holds for time-varying channels (e.g., by testing on channels with Doppler spread).
**Suggestion**: Add a discussion paragraph on time-varying channels and the limitations of feedforward LISTA compared to adaptive filters. If possible, add a simple experiment with time-varying channels.
**Severity**: Minor

### W3: Missing Connection to Model-Based Deep Learning Literature
**Problem**: The paper discusses LISTA within the deep unfolding paradigm but does not connect to the broader model-based deep learning literature (e.g., He et al., 2019 "Model-Driven Deep Learning for Physical Layer Communications"). This literature provides a broader framework for understanding why deep-unfolded architectures work and offers design principles that could enhance the paper's analysis.
**Why it matters**: The model-based deep learning community has developed general principles for designing deep-unfolded architectures (e.g., physics-informed constraints, interpretable layers, provable convergence). Connecting to this literature would position the paper's findings within a broader context and potentially suggest architectural improvements.
**Suggestion**: Add a paragraph in Section 5 connecting the error concentration findings to the model-based deep learning literature. Discuss whether the error concentration property is a general consequence of physics-informed architecture design.
**Severity**: Minor

### W4: Scalability Analysis Incomplete
**Problem**: The scalability analysis (Table 4, Section 4.13) shows that LISTA training diverges at $N=256$ when $M/N = 1$, and the parameter count grows as $O(N^2)$. The paper mentions "structured linear mappings (Toeplitz, circulant, low-rank)" as potential solutions but does not evaluate them.
**Why it matters**: For practical 5G/6G systems, channel lengths can be $N = 256$--$1024$ (e.g., for mmWave channels with long delay spreads). The $O(N^2)$ scaling makes LISTA impractical for these scenarios without structured mappings.
**Suggestion**: Either (a) evaluate at least one structured mapping (e.g., circulant approximation of $\mathbf{W}^{(k)}$) and report the impact on NMSE and parameter count, or (b) add a more detailed discussion of which structured mappings are most promising and why.
**Severity**: Minor

### W5: Practical Deployment Missing Power Consumption Analysis
**Problem**: The hardware complexity analysis (Section 4.13) focuses on FLOP counts and theoretical latency but does not discuss power consumption. For IoT and mobile devices, power consumption is often the binding constraint, not latency.
**Why it matters**: LISTA's feedforward architecture may have different power characteristics than OMP's iterative architecture. The regular computation graph of LISTA may enable better power management (e.g., clock gating, voltage scaling) than OMP's irregular control flow.
**Suggestion**: Add a brief discussion of power consumption implications, even if only qualitative. Reference any existing work on power-efficient deep unfolding implementations.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title accurately reflects the paper's content. The three focus areas (generalization, error structure, ablation) are well-chosen.
- Abstract is comprehensive but dense. The highlights box is informative.

### Introduction
- The introduction is well-structured and positions the paper appropriately as analysis rather than novelty.
- The 6 enumerated contributions are comprehensive.

### Related Work (Section 2)
- Coverage is broad but has gaps in LISTA variants (as noted by Reviewer 2).
- The deep learning for channel estimation section is comprehensive.

### Methodology (Section 3)
- The LISTA architecture description is clear.
- The computational complexity analysis is straightforward.
- The training protocol is well-specified.

### Experiments (Section 4)
- 12 experiments is comprehensive. The progression from basic comparison to mechanism analysis is logical.
- The pilot ratio analysis (Table 6) is particularly useful.
- The FISTA comparison (Table 13) is a valuable addition.

### Discussion (Section 5)
- The discussion is thorough and honest.
- The deployment guidance (Section 5.3) is practical and actionable.
- The AMP connection (Section 5.1) needs better positioning.

### Conclusion
- Conclusion accurately summarizes findings.
- Future work directions are concrete and actionable.

### References
- Reference list is comprehensive for the topics covered.
- Missing key LISTA variants (ALISTA, LISTA-CPSS, Elastic LISTA).

---

## Questions for Authors

1. **Complex-valued channels**: How would the error concentration mechanism change for complex-valued channels? The soft-thresholding operator would need to be extended to the complex domain (thresholding magnitude while preserving phase). Would the error concentration percentage change?

2. **Time-varying channels**: LISTA is a feedforward network and cannot track time-varying channels without retraining. How does this limitation affect the practical deployment guidance in Section 5.3?

3. **Structured mappings**: Can you evaluate at least one structured mapping (e.g., circulant approximation of $\mathbf{W}^{(k)}$) to assess whether the $O(N^2)$ scaling can be reduced without significant NMSE degradation?

4. **Cross-architecture generalization**: Do you expect the error concentration mechanism to generalize to other deep-unfolded architectures (e.g., unfolded ADMM)? Have you tested this?

---

## Minor Issues

### Cross-disciplinary Connections
- The paper would benefit from connecting to the model-based deep learning literature (He et al., 2019; Wei et al., 2021).
- The error concentration finding has implications for the broader deep unfolding community that should be discussed.

### Practical Implications
- Add a brief discussion of power consumption implications for hardware deployment.
- The deployment guidance (Section 5.3) could be enhanced with a decision flowchart.

### Figures and Tables
- Figure 1: Consider adding a marker for the "LISTA saturation region" to highlight the key finding visually.
- Table 17 (CNN/Transformer comparison): Should be removed or replaced with a direct comparison.

### Layout
- Section 5.1 (AMP connection) is long and somewhat tangential. Consider moving some content to an appendix or supplementary material.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 62 | Adequate | Error concentration is insightful but partially known; LISTA itself is not novel |
| Methodological Rigor (25%) | 80 | Strong | Comprehensive experiments with good statistical practice |
| Evidence Sufficiency (25%) | 78 | Strong | 12 experiments, good generalization analysis; real-valued channels only |
| Argument Coherence (15%) | 78 | Strong | Clear logical flow; some narrative tension |
| Writing Quality (15%) | 76 | Strong | Professional prose; dense in places |
| Significance & Impact | 68 | Adequate | Practical deployment guidance is valuable; real-valued channels limit applicability; error concentration has cross-architectural potential |
| **Weighted Average** | **73.8** | **Minor Revision** | |
