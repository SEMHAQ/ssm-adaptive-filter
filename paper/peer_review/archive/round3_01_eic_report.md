# Peer Review Report — Editor-in-Chief

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 3

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), Digital Signal Processing

### Reviewer Identity
Prof. Elena Vasquez, Associate Editor, Digital Signal Processing (Elsevier). Expertise in adaptive filtering, sparse signal processing, and computational methods for communications. 15 years of editorial experience in signal processing journals. Review preferences: practical relevance, methodological soundness, clear positioning against existing work.

### Review Focus
Journal fit, originality, overall quality, significance to the DSP readership, and whether the contribution warrants publication in this venue.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — The paper falls squarely within my area of expertise (adaptive filtering and sparse signal processing). I am highly confident in my assessment of journal fit and contribution significance.

### Summary Assessment
This manuscript presents a systematic analysis of LISTA (Learned ISTA) applied to sparse channel estimation, covering NMSE performance, BER analysis, ablation studies, generalization experiments, and practical deployment considerations. The paper is well-structured and honestly reports both strengths and limitations of the approach.

The most significant contribution is the BER analysis (Section 4.10), which reveals that LISTA's 13–33 dB NMSE gap with OMP does *not* translate to a BER penalty—LISTA achieves competitive BER for QPSK and better BER for 16-QAM. This counterintuitive finding, if rigorously substantiated, has genuine practical value. The ablation study with 20 seeds and proper statistical testing (Cohen's d, paired t-tests) represents good experimental practice.

However, the paper has two notable weaknesses: (1) the originality is limited—applying LISTA to channel estimation is not new, and the contribution is primarily an empirical characterization rather than a methodological advance; (2) the BER-NMSE disconnect explanation lacks theoretical grounding and relies on post-hoc rationalization. These issues are addressable and do not preclude publication in DSP with appropriate revisions.

---

## Strengths

### S1: BER Analysis Provides System-Level Context
The BER simulation in Section 4.10 is the paper's strongest contribution. By demonstrating that LISTA's NMSE disadvantage does not carry over to BER (Tables 10–11), the authors provide the practical justification that the NMSE-only analysis cannot. The finding that LISTA outperforms OMP on 16-QAM BER is particularly noteworthy and counterintuitive. This reframes LISTA from a "worse OMP" to a "different trade-off" and is exactly the kind of insight the DSP readership values.

### S2: Rigorous Ablation with Adequate Statistical Power
The 20-seed ablation study (Section 4.11, Table 9) with paired t-tests and Cohen's d effect sizes is commendable. The authors transparently acknowledge that the initial 5-seed ablation lacked statistical power (~15–20% for medium effects) and proactively conducted the follow-up study. The finding that the per-layer threshold schedule is the dominant contributor (+14–18 dB) while W^(k) provides a secondary but significant improvement (+1.24 dB, d=1.5) is well-supported and insightful.

### S3: Honest Reporting of Limitations
The authors do not oversell LISTA. They clearly state the 13–33 dB NMSE gap with OMP, the N=256 divergence issue, the Python-only speed comparison caveat, and the saturation behavior. Section 5.3 (Limitations) is forthright and specific. This honesty strengthens credibility and helps readers make informed deployment decisions.

### S4: Comprehensive Experimental Design
The experimental matrix covers SNR, sparsity, channel length, depth, generalization, ITU channels, LISTA-CP comparison, SNR mitigation, and BER—11 experiments in total. The use of mixed-SNR training to eliminate training-procedure-induced inconsistencies between tables is a good methodological choice.

---

## Weaknesses

### W1: Limited Originality — Contribution is Empirical Characterization, Not Methodological Advance
**Problem**: The paper applies the standard LISTA architecture (Gregor & LeCun, 2010) to sparse channel estimation without architectural novelty. The authors explicitly acknowledge this ("Rather than claiming architectural novelty," Related Work, p. 5), but the contribution positioning needs strengthening. The related work section lists numerous prior works applying deep learning to channel estimation (Ye et al., Gao et al., Dong et al., Zhang et al.), making the incremental contribution unclear to readers unfamiliar with the deep unfolding specificities.

**Why it matters**: DSP reviewers will ask "what is new here?" The answer is the systematic analysis methodology (ablation, BER, generalization), but this needs to be foregrounded more explicitly.

**Suggestion**: Strengthen the introduction's positioning by explicitly stating: "Our contribution is not architectural novelty but rather the first systematic characterization of LISTA's behavior in the channel estimation context, including the counterintuitive BER-NMSE disconnect." Add a brief comparison table summarizing what prior deep-learning-for-channel-estimation works did vs. what this paper does differently.

**Severity**: Major

### W2: BER-NMSE Disconnect Explanation Lacks Theoretical Grounding
**Problem**: The explanation for why LISTA achieves better BER despite worse NMSE—"LISTA's learned soft-thresholding produces channel estimates whose error structure is more favorable for zero-forcing equalization" (Section 4.10, Section 5.1)—is a post-hoc rationalization without formal analysis. The paper does not characterize what "more favorable error structure" means quantitatively. No analysis of the equalizer's noise enhancement, no comparison of the channel estimate's condition number, no examination of tap-location accuracy vs. tap-amplitude accuracy.

**Why it matters**: This is the paper's most important claim and its weakest link. Without rigorous analysis, reviewers may dismiss it as speculation.

**Suggestion**: Add a diagnostic analysis: (1) measure tap-location accuracy (how often does LISTA identify the correct support set?) vs. OMP; (2) compute the condition number of X^T * diag(h_hat) * X for LISTA vs. OMP estimates; (3) analyze the equalizer's noise enhancement factor. This would transform a hand-wavy explanation into a rigorous finding.

**Severity**: Critical

### W3: BER Simulation Limited to i.i.d. Gaussian Channels
**Problem**: The BER analysis (Section 4.10) uses only i.i.d. Gaussian channels, while the NMSE analysis includes ITU channels (Section 4.7.2). The paper claims "cross-distribution generalization" for NMSE but provides no BER evidence on ITU channels.

**Why it matters**: If the BER advantage does not hold on ITU channels, the practical value of the finding is significantly reduced.

**Suggestion**: Add BER results on ITU PedA and VehA channels. Even a single SNR point (e.g., 20 dB) would be valuable.

**Severity**: Major

---

## Detailed Comments

### Title & Abstract
- The title is descriptive and accurate. "Analysis" correctly signals that this is a characterization paper, not an architectural contribution.
- The abstract is comprehensive but dense. Consider splitting the NMSE saturation finding and the BER finding into clearer separate sentences.
- The highlights are well-chosen and summarize the key findings effectively.

### Introduction
- The six contributions are clearly enumerated. However, contribution 2 (BER analysis) should be elevated—it is the most novel finding.
- The motivation for studying LISTA specifically (vs. other deep-unfolded architectures) could be strengthened. Why LISTA and not ISTA-Net or OCLISTA?

### Literature Review / Theoretical Framework
- Good coverage of deep unfolding and channel estimation literature.
- The positioning against CNN-based and Transformer-based methods is helpful but could be more explicit about the trade-offs.

### Methodology / Research Design
- The experimental design is sound. Mixed-SNR training is a good choice.
- The LISTA-CP comparison with diagnostic analysis of weight clipping is well-executed.

### Results / Findings
- Tables are clear and well-formatted. The use of bold for best-performing method per row is helpful.
- Figure references are present but I cannot verify the figures themselves.
- The statistical reporting (mean ± std, p-values, Cohen's d) is appropriate.

### Discussion
- Section 5.1 provides good synthesis but the BER explanation needs strengthening (see W2).
- The deployment recommendation framework (Section 5.2, items 1–5) is practical and useful.

### Conclusion
- Conclusions are supported by the evidence. No over-claiming detected.

### References
- References are comprehensive and recent. The inclusion of hardware deployment references (Wei et al., Kim et al.) is appropriate given the practical focus.

---

## Questions for Authors

1. **BER-NMSE disconnect**: Can you provide a quantitative analysis of *why* LISTA achieves better BER despite worse NMSE? Specifically, what is the tap-location accuracy (correct support set identification rate) for LISTA vs. OMP, and how does this relate to the equalizer's noise enhancement?

2. **LISTA vs. other deep-unfolded architectures**: Why was LISTA chosen over ISTA-Net (He et al., 2019) or OCLISTA (Borgerding et al., 2020)? Would the BER advantage hold for these variants?

3. **Practical deployment**: The 33× speedup is measured in Python. Can you provide C/C++ or FPGA timing estimates, even rough ones, to substantiate the hardware deployment claims?

---

## Minor Issues

### Language / Grammar
- Abstract, line 4: "LISTA's NMSE saturates at approximately −25 dB" — consider "plateaus" for variety.
- Section 4.10, paragraph 2: "This counterintuitive result" — this phrase appears multiple times; consider varying the language.

### Figures and Tables
- Table 5 (channel length): The ‡ footnote about N=256 divergence is important but easy to miss. Consider adding a visual indicator in the table.
- Table 8 (LISTA-CP): The identical values for LISTA and LISTA-CP at all SNR levels could be presented more compactly.

### Layout
- The paper is well-structured. No significant layout issues.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | Contribution is systematic analysis, not architectural novelty; BER finding is novel |
| Methodological Rigor (25%) | 72 | Adequate | Good ablation and statistical testing; BER analysis needs more rigor |
| Evidence Sufficiency (25%) | 68 | Adequate | Comprehensive experiments but BER limited to Gaussian channels |
| Argument Coherence (15%) | 70 | Adequate | Clear structure; BER-NMSE disconnect explanation needs strengthening |
| Writing Quality (15%) | 75 | Strong | Well-written, clear, honest reporting |
| **Weighted Average** | **67.6** | **Minor Revision** | |
