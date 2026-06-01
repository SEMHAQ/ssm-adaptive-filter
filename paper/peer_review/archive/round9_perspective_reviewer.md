# Peer Review Report — Peer Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 9

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Perspective / Cross-disciplinary)

### Reviewer Identity
Prof. Hiroshi Tanaka, Department of Computer Science, University of Tokyo. Expertise in deep learning for communications, model-driven AI, and cross-disciplinary applications of machine learning. 12 years of experience bridging machine learning and wireless communications research.

### Review Focus
Cross-disciplinary connections between deep learning and signal processing, practical deployment implications, comparison with modern deep learning approaches, and broader impact of the findings. I evaluate whether the paper's contributions extend beyond the narrow channel estimation domain.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
4 — Mostly within my area of expertise, high confidence

### Summary Assessment
This paper provides a comprehensive analysis of LISTA for sparse channel estimation, with particular emphasis on understanding what the learned parameters capture and how LISTA's error structure affects system-level BER performance. From a cross-disciplinary perspective, the paper's most valuable contribution is the BER mechanism analysis, which reveals that LISTA's soft-thresholding operator produces an error structure (concentrated on true taps) that is favorable for equalization. This insight has implications beyond channel estimation — it suggests that deep-unfolded architectures may learn problem-specific error structures that are not captured by traditional metrics like NMSE.

However, the paper has a significant blind spot: it does not adequately engage with the modern deep learning literature for channel estimation. The qualitative comparison with CNN/Transformer methods (Section 5.2) is insufficient for a paper that claims to provide a "systematic analysis" of deep-unfolded channel estimation. Additionally, the practical deployment analysis, while thorough in its FLOP counting, does not address the real-world constraints that practitioners face (latency requirements, power budgets, integration with existing systems). These concerns are addressable and the paper makes a solid contribution.

---

## Strengths

### S1: BER Mechanism Analysis — Cross-disciplinary Insight
The finding that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP) is a genuinely novel insight with cross-disciplinary implications. This suggests that deep-unfolded architectures learn problem-specific error structures that are not captured by NMSE — a finding that could influence how we evaluate deep learning methods for signal processing more broadly. The error sparsity analysis (Gini coefficient, support vs. non-support error distribution) provides a new analytical framework that could be applied to other deep-unfolded architectures (e.g., LISTA for image reconstruction, deep-unfolded radar processing).

### S2: Honest Limitations Discussion
The paper's limitations section (Section 5.4) is remarkably honest and thorough. The authors explicitly acknowledge: (1) the 13-33 dB NMSE gap with OMP, (2) the theoretical nature of hardware claims, (3) the N² scalability limitation, (4) training instability at high sparsity, and (5) the qualitative nature of the deep learning comparison. This level of transparency is unusual and commendable — it allows readers to make informed decisions about the paper's applicability to their work.

### S3: Practical Deployment Framework
Section 5.3 provides a clear decision framework for practitioners: (1) speed-critical applications → LISTA with pipelining, (2) known operating SNR → SNR-specific training, (3) variable SNR → broad-range training, (4) when NMSE matters → OMP/LASSO, (5) architecture choice → L=10-20 layers. This framework, while simple, is practically useful and demonstrates the authors' understanding of real-world deployment constraints.

### S4: Ablation Study Methodology
The progression from 5-seed to 20-seed ablation (Sections 4.5 and 4.11) demonstrates methodological maturity. The finding that the per-layer threshold schedule is the dominant contributor (+14-18 dB) while W^(k) provides a secondary +1.24 dB contribution provides genuine insight into what LISTA learns. This has implications for designing more efficient deep-unfolded architectures — the threshold schedule is the critical component, not the linear mapping.

---

## Weaknesses

### W1: Insufficient Engagement with Modern Deep Learning Literature
**Problem**: The paper provides only a qualitative comparison with CNN and Transformer methods (Section 5.2, Table 8) based on published results rather than direct experimental comparison. The table compares LISTA against "1D-CNN" and "ResNet-CNN" using NMSE ranges from different studies with different experimental setups. This is insufficient for a paper that claims to provide a "systematic analysis" of deep-unfolded channel estimation.

**Why it matters**: The deep learning community has moved beyond simple CNNs. Modern approaches include attention mechanisms, graph neural networks, and hybrid model-driven/data-driven architectures. The paper's comparison is against outdated baselines and does not reflect the current state of the art.

**Suggestion**: Either (a) include at least one modern deep learning baseline in the experiments (e.g., a Transformer-based channel estimator trained under the same conditions), or (b) more clearly state that the comparison is qualitative and that the paper's contribution is understanding LISTA's behavior, not benchmarking against all possible architectures. The current framing suggests the comparison is more comprehensive than it actually is.

**Severity**: Major

### W2: Practical Deployment Constraints Not Addressed
**Problem**: The hardware analysis (Section 4.13) focuses on FLOP counts and theoretical pipeline analysis but does not address real-world deployment constraints: (1) latency requirements for 5G NR (1 ms slot duration), (2) power budgets for mobile devices, (3) integration with existing receiver architectures, (4) training data requirements for deployment, (5) model update frequency for time-varying channels.

**Why it matters**: Practitioners evaluating LISTA for deployment need to understand these constraints. The paper's hardware analysis is too abstract to be practically useful.

**Suggestion**: Add a brief discussion of practical deployment constraints, even if only qualitative. For example, discuss how LISTA's 82K parameters and 0.21 ms inference time relate to 5G NR latency requirements, or how the training data requirement (10,000 samples) affects deployment in new environments.

**Severity**: Minor

### W3: Error Structure Analysis Limited to i.i.d. Gaussian Channels
**Problem**: The BER mechanism analysis (Section 4.12) is conducted on i.i.d. Gaussian channels with K=5, N=64, M=256. The finding that LISTA concentrates error on true taps may not generalize to: (1) channels with correlated tap amplitudes, (2) channels with different sparsity levels, (3) channels with different pilot ratios, (4) time-varying channels.

**Why it matters**: The error structure analysis is the paper's primary contribution, but its generalizability is not established. The ITU channel experiments (Section 4.7) show comparable NMSE but do not analyze error structure.

**Suggestion**: If possible, extend the error structure analysis to ITU channels or at least discuss how correlated tap amplitudes might affect the error concentration behavior. The current analysis is a strong starting point but its scope should be clearly stated.

**Severity**: Minor

### W4: Missing Analysis of Training Data Requirements
**Problem**: The paper uses 10,000 training samples but does not analyze how training data size affects LISTA's performance. This is a practical concern for deployment in new environments where training data may be limited.

**Why it matters**: Practitioners need to know how much training data is required to achieve the reported performance. If LISTA requires 10,000 samples but a CNN-based method achieves similar performance with 1,000 samples, the practical advantage may be smaller than suggested.

**Suggestion**: Add a brief experiment or discussion of training data requirements. How does LISTA's performance degrade with fewer training samples? Is there a minimum data requirement?

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title accurately describes the paper's scope.
- Abstract is comprehensive but very long (~400 words). The repeated caveats about hardware estimates create a defensive tone.
- The abstract correctly positions the BER mechanism analysis as the primary contribution.

### Introduction (Section 1)
- Six contributions are clearly enumerated.
- The positioning is honest: "Rather than claiming architectural novelty, we focus on understanding LISTA's behavior."
- Contribution 6 (hardware complexity) feels disconnected from the others.

### Literature Review (Section 2)
- Good coverage of sparse channel estimation, deep unfolding, and deep learning for channel estimation.
- The comparison framework (vs. OMP, LASSO, LMS, NLMS) is standard and appropriate.
- Missing: recent work on model-driven deep learning for communications (He et al., 2019 is cited but not deeply engaged with).

### Methodology (Section 3)
- Standard LISTA architecture, well-described.
- Parameter analysis is helpful.
- Missing: discussion of why LISTA was chosen over other deep-unfolded architectures (e.g., LISTA-CP, OCLISTA) for this analysis.

### Experiments (Section 4)
- Comprehensive experimental design covering 13 experiments.
- The BER mechanism analysis (Section 4.12) is the highlight.
- The hardware analysis (Section 4.13) is thorough but speculative.
- The ITU channel experiments (Section 4.7) add practical relevance.

### Discussion (Section 5)
- Section 5.1 (saturation analysis) is thorough and well-argued.
- Section 5.2 (deep learning comparison) is the weakest section.
- Section 5.3 (deployment framework) is practical and useful.
- Section 5.4 (limitations) is honest and comprehensive.

### Conclusion
- Well-structured summary of findings.
- Hardware claims appropriately hedged.
- Future research directions are relevant and specific.

### References
- 42 references, mostly peer-reviewed, recent (2018-2024), appropriate for the field.
- Good coverage of both classical and modern methods.
- Missing some recent deep learning for communications references.

---

## Questions for Authors

1. How does LISTA's error structure (concentrated on true taps) compare with other deep-unfolded architectures? Is this a general property of soft-thresholding-based architectures, or specific to LISTA's training?

2. For practical deployment, how would LISTA handle time-varying channels? Would the model need to be retrained periodically, or does the broad-range training provide sufficient robustness?

3. The paper focuses on single-antenna SISO channels. How would the findings extend to MIMO systems, where the channel estimation problem is significantly more complex?

---

## Minor Issues

### Cross-disciplinary Connections
- The paper could benefit from discussing connections to other deep-unfolded architectures (e.g., LISTA for image reconstruction, deep-unfolded radar processing).
- The error structure analysis has implications for how we evaluate deep learning methods in signal processing more broadly — this could be discussed.

### Practical Implications
- The deployment framework (Section 5.3) is useful but could be more specific about real-world constraints.
- The training data requirement (10,000 samples) should be discussed in the context of practical deployment.

### Writing
- The paper is generally well-written but excessively repetitive.
- The abstract is too long.
- The hardware section (4.13) is too long and could be split.

### Figures and Tables
- All tables are well-formatted.
- Table 8 (deep learning comparison) is useful but should be more clearly labeled as qualitative.
- Consider adding a figure showing the error structure (support vs. non-support error) visually.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | BER mechanism analysis is novel; rest is comprehensive but incremental |
| Methodological Rigor (25%) | 70 | Strong | Good experimental design; hardware claims need reframing |
| Evidence Sufficiency (25%) | 65 | Adequate | Comprehensive for LISTA; insufficient for deep learning comparison |
| Argument Coherence (15%) | 74 | Strong | Clear logical flow; honest about limitations |
| Writing Quality (15%) | 68 | Adequate | Generally clear; some repetition; abstract too long |
| Significance & Impact | 66 | Adequate | BER mechanism insight has cross-disciplinary potential; practical impact limited by NMSE gap |
| **Weighted Average** | **68.5** | **Minor Revision** | |

---

## Final Assessment

The paper makes a solid contribution to understanding LISTA's behavior for sparse channel estimation. The BER mechanism analysis is the standout contribution, with potential cross-disciplinary implications for how we evaluate deep-unfolded architectures. The main concerns are: (1) insufficient engagement with modern deep learning literature, (2) practical deployment constraints not addressed, and (3) error structure analysis scope should be clarified. These are addressable with minor revisions. The paper's honest approach to limitations is commendable and strengthens its credibility.

**Overall Score: 69/100 — Minor Revision**
