# Peer Review Report — Domain Reviewer (R2)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 6

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert

### Reviewer Identity
Prof. Maria Santos, Professor of Wireless Communications and Deep Learning. Expertise in deep learning for channel estimation, MIMO/OFDM systems, and FPGA implementation of neural networks for communications.

### Review Focus
Literature coverage completeness (especially recent deep learning methods for channel estimation), theoretical framework appropriateness, positioning relative to state-of-the-art, and practical deployment considerations in real communication systems.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Accept**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
4 — Channel estimation and deep learning for communications are my core expertise. I am less confident about the hardware complexity analysis details.

### Summary Assessment
This paper provides a systematic analysis of LISTA for sparse channel estimation, covering performance characterization, BER validation, ablation studies, and deployment considerations. The paper is well-positioned within the deep unfolding literature and provides honest, thorough evaluation. The BER-NMSE mechanism analysis (error concentration on true taps) is a valuable contribution to understanding deep-unfolded architectures in communication systems.

The literature review is comprehensive for classical sparse recovery methods and deep unfolding, but has gaps in recent (2024–2025) deep learning channel estimation work. The comparison with ITU channel models (Section 4.7.2) demonstrates practical relevance, but the paper would benefit from comparison with at least one recent DL-based method (CNN or Transformer) to position LISTA relative to the current state of the art. The hardware complexity analysis is theoretical but well-structured.

I recommend Minor Revision. The paper's analytical contribution is solid and the statistical validation is exemplary for this field. The literature and comparison gaps are addressable.

---

## Strengths

### S1: Comprehensive Literature Taxonomy for Deep Learning Channel Estimation
Section 2.3 provides a well-organized taxonomy of DL-based channel estimation methods: CNN-based, Transformer-based, model-driven, and surveys. The explicit categorization helps readers understand LISTA's position in the broader landscape. The inclusion of hardware deployment references (Kim et al., Wei et al., Chen et al.) in Section 2.3 is particularly relevant given the paper's hardware complexity analysis.

### S2: ITU Channel Model Validation
The evaluation on ITU Pedestrian A and Vehicular A models (Section 4.7.2, Table 8) demonstrates that LISTA trained on i.i.d. Gaussian data generalizes to realistic channel models. This is a critical validation for practical deployment, as real channels have correlated tap amplitudes and exponentially decaying power delay profiles. The finding that LISTA achieves −23 to −27 dB on ITU channels (comparable to its Gaussian saturation level) is practically meaningful.

### S3: LISTA-CP Comparison with Diagnostic Analysis
The comparison with LISTA-CP (Section 4.8, Table 7) goes beyond simple performance comparison to explain why the two architectures perform identically: the weight clipping constraint is never activated because spectral norms remain below 0.35. This diagnostic analysis is valuable because it shows that the convergence guarantees of LISTA-CP provide theoretical assurance without practical accuracy improvement in this setting.

### S4: SNR-Specific Training as Practical Mitigation
The SNR saturation mitigation experiment (Section 4.9, Table 8) demonstrates that narrow-range training (e.g., [15, 25] dB) improves NMSE by ~6 dB. This is a practical and actionable finding for deployment. The recommendation to use SNR-specific training when the operating SNR is known provides clear guidance.

### S5: Honest Positioning Relative to Classical Methods
The paper does not oversell LISTA against OMP and LASSO. The NMSE gap (13–33 dB at high SNR) is clearly stated, and the paper honestly acknowledges that "when NMSE is the primary metric... OMP remains the better choice." This honest positioning strengthens credibility.

---

## Weaknesses

### W1: Missing Comparisons with Recent DL Channel Estimation Methods
**Problem**: The baselines (Section 4.1) include only classical methods: LMS, NLMS, OMP, LASSO. The literature review (Section 2.3) discusses CNN-based (Ye et al., Gao et al.), Transformer-based (Zhang et al.), and model-driven (He et al., Wei et al.) methods, but none are included in the experimental comparison. The paper's contribution would be strengthened by positioning LISTA relative to at least one modern DL baseline.
**Why it matters**: Without DL baselines, readers cannot assess whether LISTA's advantages (interpretability, hardware-friendliness) come at an accuracy cost compared to black-box methods. A CNN with comparable parameter count would clarify the trade-off.
**Suggestion**: Add at least one CNN-based baseline (e.g., a 1D ResNet or U-Net for channel estimation with ~80K parameters). If this is not feasible, add a discussion paragraph in Section 5 comparing LISTA's characteristics (fixed computation, interpretability, hardware-friendliness) with those of CNN/Transformer methods, citing relevant performance numbers from the literature.
**Severity**: Major

### W2: Literature Gap in Recent (2024–2025) DL Channel Estimation
**Problem**: The bibliography includes several 2023 surveys (Elbir et al., Gao et al., Wu et al.) but lacks recent 2024–2025 papers on learned channel estimation. Notable omissions include: (a) learned approximate message passing (LAMP) variants for channel estimation, (b) score-based generative models for sparse recovery, (c) neural ODE-based channel estimators, (d) recent work on foundation models for wireless communications.
**Why it matters**: The field is evolving rapidly. Omitting 2024–2025 work may give reviewers and readers the impression that the literature review is not current.
**Suggestion**: Add 3–5 references from 2024–2025 to demonstrate awareness of recent developments. In particular, cite any recent work on LISTA variants for channel estimation or on learned message passing for sparse recovery.
**Severity**: Minor

### W3: Limited Channel Model Diversity
**Problem**: The evaluation uses i.i.d. Gaussian channels (main experiments) and ITU PedA/VehA models (Section 4.7.2). Real communication systems also include: (a) frequency-selective channels with Doppler, (b) massive MIMO channels with spatial correlation, (c) channels with hardware impairments (IQ imbalance, phase noise). The paper does not discuss how these factors would affect LISTA's performance.
**Why it matters**: The generalization claims are limited to static, single-antenna channels. For practical deployment in modern systems (5G NR, WiFi 7), the evaluation scope is narrow.
**Suggestion**: Add a brief discussion in Section 5.3 (Limitations) acknowledging that the evaluation is limited to static, single-antenna channels. Mention that frequency-selective channels with Doppler, massive MIMO, and hardware impairments are important directions for future work.
**Severity**: Minor

### W4: BER Analysis Limited to Flat-Fading
**Problem**: The BER experiments (Section 4.10) use a single-tap equalizer (ZF or MMSE), which assumes flat-fading. Real channels are frequency-selective and require OFDM with per-subcarrier equalization. The paper does not discuss how LISTA's error concentration property would behave in OFDM systems with frequency-domain equalization.
**Why it matters**: The BER-NMSE mechanism (error concentration on true taps) may not translate directly to OFDM systems where equalization is performed in the frequency domain. The practical implications of the BER finding are limited by this assumption.
**Suggestion**: Add a discussion paragraph noting that the BER analysis assumes flat-fading with single-tap equalization. Acknowledge that OFDM systems with per-subcarrier equalization may exhibit different behavior, and that extending the BER analysis to OFDM is an important future direction.
**Severity**: Minor

---

## Detailed Comments

### Literature Review / Theoretical Framework
- Section 2.1 (Sparse Channel Estimation) is comprehensive and well-cited.
- Section 2.2 (Deep Unfolding) covers the key works: Gregor & LeCun (LISTA), Chen et al. (LISTA-CP), Borgerding et al. (OCLISTA), Liu et al. (LISTA-AMP).
- Section 2.3 (Deep Learning for Channel Estimation) provides good taxonomy but is missing recent 2024–2025 work.
- Section 2.4 (Classical Adaptive Filtering) appropriately covers LMS, NLMS, PNLMS.
- The positioning statement (end of Section 2.3) clearly differentiates this work from prior applications.

### Methodology
- The LISTA architecture (Section 3.2) is standard and well-described.
- The FFT-based convolution (Equation 8) is appropriate for the problem.
- The parameter analysis (Section 3.4) correctly identifies the O(N²) scalability concern.
- The comparison with classical methods (Section 3.6) provides useful context.

### Results
- Experiment 1 (NMSE vs SNR): Comprehensive sweep from −5 to 40 dB. The out-of-distribution points (−5 and 40 dB) test generalization boundaries.
- Experiment 6 (Generalization): The three-axis generalization testing (sparsity, SNR, cross-distribution) is thorough.
- Experiment 10 (BER): The 200-realization validation with statistical testing is exemplary.
- Experiment 12 (Mechanism): The error sparsity analysis is the paper's most valuable contribution.

### Discussion
- Section 5.1 provides good insight into the saturation mechanism.
- The deployment framework (Section 5.2) is practical.
- Limitations (Section 5.3) are honestly stated but could be expanded (see W3, W4).

### References
- Bibliography has 40+ references, mostly from 2010–2023.
- Missing: 2024–2025 papers on learned channel estimation.
- The inclusion of FPGA/hardware references (Kim, Wei, Chen) is appropriate given the paper's hardware claims.

---

## Questions for Authors

1. Can you provide a qualitative comparison of LISTA's characteristics (accuracy, computation, interpretability, hardware-friendliness) with CNN-based and Transformer-based channel estimation methods from the literature? Even without running experiments, a comparison table citing published results would help position LISTA.

2. How would LISTA's error concentration property (99.9% on true taps) behave in OFDM systems with per-subcarrier equalization? Is the BER advantage expected to hold in frequency-domain equalization?

3. Have you considered evaluating on 3GPP channel models (e.g., TDL, CDL) in addition to ITU models? These are more widely used in 5G NR standardization and would strengthen the practical relevance.

---

## Minor Issues

### Literature
- Reference [28] (Li et al., 2022) — verify that this is the correct citation for "when and why deep learning is effective for sparse channel estimation."
- Add DOIs to all references for completeness.

### Figures and Tables
- Table 8 (ITU channels): Report standard deviations for all methods, not just LISTA. The LMS, NLMS, OMP, and LASSO values lack error bars.
- Figure 3 (convergence): Add a secondary y-axis showing the improvement per additional layer to visualize diminishing returns.

### Writing
- Section 2.3: The bold formatting for method categories (CNN-based, Transformer-based, etc.) is helpful but inconsistent — some have bold labels, others do not.
- Section 4.7.2: The deployment recommendations (numbered list 1–4) could be moved to Section 5.2 for better organization.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 58 | Weak | LISTA is well-known; contribution is analytical. BER-NMSE mechanism is novel. |
| Methodological Rigor (25%) | 76 | Strong | Good experimental design. Missing DL baselines. ITU validation is valuable. |
| Evidence Sufficiency (25%) | 72 | Strong | Comprehensive experiments. Missing recent DL comparisons. ITU channel evaluation helps. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow. Mechanism analysis well-argued. |
| Writing Quality (15%) | 72 | Adequate | Generally clear. Some dense passages. |
| Literature Integration (optional) | 62 | Adequate | Good coverage of classical and deep unfolding literature. Missing 2024–2025 DL channel estimation. |
| Significance & Impact (optional) | 64 | Adequate | Useful reference. Practical deployment framework. Limited by narrow channel model scope. |
| **Weighted Average** | **70.4** | **Minor Revision** | |

---

**Decision**: Minor Revision — The paper provides solid analytical contribution with thorough statistical validation. Literature gaps (recent DL methods) and missing DL baselines are the main concerns, but are addressable.
