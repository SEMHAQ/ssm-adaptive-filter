# Peer Review Report — Reviewer 2 (Domain Expert)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 5

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert (Sparse Channel Estimation & Deep Unfolding)

### Reviewer Identity
Prof.~Dr.~Li Wei, School of Information and Communication Engineering, Beijing University of Posts and Telecommunications. 18 years of research experience in sparse channel estimation, compressed sensing for wireless communications, and deep learning for physical layer processing. Author of >80 journal papers on compressed sensing-based channel estimation and model-driven deep learning. Associate Editor of *IEEE Transactions on Wireless Communications*. Familiar with the full landscape of LISTA variants (LISTA-CP, OCLISTA, LISTA-AMP) and their theoretical properties.

### Review Focus
Literature coverage completeness, theoretical framework appropriateness, domain contribution, positioning relative to existing work, and whether the paper advances the state-of-the-art in sparse channel estimation. I particularly assess: (1) whether the literature review captures the relevant body of work, (2) whether the theoretical framing is correct, (3) whether the contribution is incremental or substantive.

---

## Overall Assessment

### Recommendation
- [ ] **Accept**
- [x] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
5 — This is my primary area of expertise. I have published extensively on compressed sensing for channel estimation and am familiar with all cited works and many uncited ones.

### Summary Assessment

This manuscript provides a thorough analysis of LISTA for sparse channel estimation, with particular strength in the BER-NMSE disconnect analysis and the comprehensive ablation study. The paper correctly identifies that LISTA's NMSE saturation at $\sim$$-25$~dB is a significant limitation and provides honest, well-quantified analysis of when LISTA is and is not preferable to classical methods. The literature review is comprehensive, covering the key works in deep unfolding, sparse channel estimation, and hardware deployment. The main domain contribution is the mechanism analysis explaining why LISTA achieves competitive BER despite worse NMSE — this is a genuinely useful insight for the community.

However, the paper has several domain-specific gaps: (1) the comparison with LISTA-CP needs deeper analysis, as the identical results are more likely due to the specific problem setup (i.i.d.~Gaussian channels, $N=64$) than a general finding; (2) the paper does not discuss the relationship between LISTA's saturation and the restricted isometry property (RIP) of the sensing matrix; (3) the ITU channel experiments use only 2 models (PedA, VehA), which is insufficient to claim "cross-distribution generalization"; (4) the paper does not compare against recent LISTA variants (OCLISTA, LISTA-AMP) despite citing them. These are addressable with additional experiments and discussion.

---

## Strengths

### S1: Honest and Comprehensive NMSE Saturation Analysis
The paper's honest characterization of LISTA's $-25$~dB NMSE saturation is refreshing. Rather than hiding this limitation, the paper dedicates significant space to understanding it (Section 5.1), proposing mitigations (Section 4.9), and analyzing its system-level impact (Section 4.10). The three-factor explanation (fixed-depth architecture, scale-invariant loss, soft-thresholding bias floor) is plausible and well-reasoned. The SNR-specific training mitigation (Table 13, $-31$~dB with narrow-range training) provides a practical solution.

### S2: BER-NMSE Mechanism Analysis
The error sparsity analysis (Table 13) is the paper's most significant domain contribution. The finding that LISTA concentrates 99.9\% of estimation error on true taps (vs.~94.9\% for OMP) with $50\times$ less non-support error provides a clear, interpretable mechanism for the BER-NMSE disconnect. This insight is valuable for the broader community because it shows that NMSE alone is insufficient for evaluating channel estimators — the error structure matters for equalization.

### S3: Comprehensive Generalization Analysis
The generalization experiments (Section 4.6) cover sparsity mismatch, SNR mismatch, and cross-distribution (ITU channels). The explicit acknowledgment that LISTA's performance on ITU channels ($-23$ to $-27$~dB) is comparable to its Gaussian saturation level ($\sim$$-25$~dB) — rather than claiming superior generalization — is honest and informative.

### S4: Ablation Study with Statistical Rigor
The 20-seed ablation (Table 10) with paired $t$-tests and Cohen's $d$ effect sizes is exemplary. The finding that the per-layer threshold schedule is the dominant contributor ($d = 18.4$) while $\mathbf{W}^{(k)}$ is secondary ($d = 1.5$) provides genuine insight into what LISTA learns. This level of ablation rigor is rare in the deep unfolding literature.

### S5: Practical Deployment Framework
The decision framework in Section 5.2 is actionable and well-justified by the experimental results. The recommendation to use LISTA for speed-critical applications with moderate accuracy requirements, and OMP/LASSO when NMSE is the primary metric, is a useful practical guideline.

---

## Weaknesses

### W1: LISTA-CP Analysis Needs Deeper Investigation
**Problem**: The paper reports that LISTA and LISTA-CP achieve "identical performance" with "maximum per-parameter difference = 0" (Section 4.8). The explanation that the weight clipping constraint is "naturally satisfied" (spectral norm 0.34 < 1.0) is plausible but incomplete. The paper does not discuss why this occurs — is it because (a) the i.i.d.~Gaussian channel model produces a well-conditioned sensing matrix $\mathbf{X}$ that naturally keeps $\mathbf{W}^{(k)}$ close to $\mathbf{I}$, (b) the Adam optimizer with weight decay penalizes large deviations from $\mathbf{I}$, or (c) the specific $N=64$, $M=256$ configuration is particularly benign?
**Why it matters**: If the identical performance is specific to the i.i.d.~Gaussian setup, the finding does not generalize to more challenging channel models (e.g., correlated taps, frequency-selective fading). The paper presents this as a general finding ("the convergence guarantees of LISTA-CP provide theoretical assurance but no practical accuracy improvement in this setting") without sufficient qualification.
**Suggestion**: (1) Analyze whether the spectral norm $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ remains below 1.0 across different channel models (ITU, correlated taps). (2) Discuss whether the finding generalizes to larger $N$ where the optimization landscape may be different. (3) Consider comparing against OCLISTA or LISTA-AMP, which use different convergence mechanisms.
**Severity**: Major

### W2: Limited ITU Channel Validation
**Problem**: The cross-distribution generalization claim is based on only 2 ITU channel models (PedA and VehA). These are both relatively simple exponentially decaying profiles with $N=64$. The paper does not test on: (a) more complex channel models (e.g., 3GPP TDL or CDL models with clustered delays), (b) frequency-selective channels with correlated tap amplitudes, or (c) channels with different delay spreads.
**Why it matters**: "Cross-distribution generalization" is a strong claim that requires testing across a diverse set of channel models. With only 2 ITU models, the generalization claim is limited to "LISTA works on exponentially decaying channels," which is a narrow form of generalization.
**Suggestion**: Test on at least 2 additional channel models: (a) a channel with correlated tap amplitudes (e.g., correlated Rayleigh fading), and (b) a channel with non-exponential power delay profile. If the paper cannot add more experiments, weaken the generalization claim to "cross-model generalization within the ITU framework."
**Severity**: Minor

### W3: Missing Comparison with Recent LISTA Variants
**Problem**: The paper cites OCLISTA \citep{borgerding2020ista} and LISTA-AMP \citep{liu2023listamp} in Section 5.1 but does not compare against them. The discussion speculates that "OCLISTA and LISTA-AMP would exhibit similar saturation under broad-range mixed-SNR training" but this is untested. Given that these variants have improved convergence properties, they may achieve better NMSE even under broad-range training.
**Why it matters**: The paper's contribution is an analysis of LISTA, but the reader needs to know whether the findings generalize to improved variants. Without this comparison, the paper's conclusions may be specific to the standard LISTA architecture.
**Suggestion**: Add a comparison with at least one LISTA variant (OCLISTA is the most accessible). If this is not feasible, add a more explicit discussion of why the findings may or may not generalize to improved variants, and recommend this as a concrete future work direction.
**Severity**: Minor

### W4: Real-Valued Channel Assumption
**Problem**: The paper uses real-valued channels ($\mathbf{h} \in \mathbb{R}^N$) and BPSK pilot signals throughout. Real wireless channels are complex-valued ($\mathbf{h} \in \mathbb{C}^N$) with QPSK/QAM pilot signals. The paper does not discuss whether the findings extend to complex-valued channels.
**Why it matters**: The real-valued assumption simplifies the problem significantly. The soft-thresholding operator (Eq.~5) needs modification for complex-valued inputs (typically using the complex sign function). The BER analysis with QPSK/16-QAM is performed at the equalization stage, but the channel estimation itself operates on real-valued signals, which is inconsistent with practical systems.
**Suggestion**: Either (a) extend the experiments to complex-valued channels, or (b) add a discussion explaining why the real-valued results are expected to extend to the complex case. The latter is acceptable if the argument is well-reasoned (e.g., the soft-thresholding operator applies element-wise and the FFT-based convolution works for complex signals).
**Severity**: Major

### W5: Scalability Discussion Insufficient
**Problem**: The paper reports that LISTA training diverges at $N=256$ (Table 4) and mentions that structured linear mappings could help (Section 5.3), but does not provide any experiments or analysis of structured mappings. The $O(N^2)$ parameter scaling is a known limitation of LISTA, and the paper does not advance the state-of-the-art on this front.
**Why it matters**: For practical channel estimation, $N=256$ or larger is common (e.g., 5G NR with 273 resource blocks). The paper's analysis is limited to $N=64$, which is a relatively short channel.
**Suggestion**: Add a brief experiment or analysis with structured mappings (e.g., Toeplitz, low-rank) for $N=128$ and $N=256$. If this is not feasible, explicitly acknowledge that the analysis is limited to short channels ($N \leq 128$) and that structured mappings are essential for practical deployment at larger $N$.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title accurately reflects the paper's scope. "Analysis" is appropriate.
- The abstract claims "cross-distribution generalization: Gaussian-trained LISTA achieves comparable performance on ITU channels" — this should be qualified as "2 ITU channel models" rather than implying broad generalization.

### Literature Review
- Comprehensive coverage of deep unfolding \citep{monga2021algorithm}, LISTA \citep{gregor2010learning}, and recent variants \citep{chen2018lista, borgerding2020ista, liu2023listamp}.
- The CNN-based, Transformer-based, and model-driven deep learning sections provide good context.
- The hardware deployment section \citep{kim2021fpga, wei2022fpga, chen2022survey} is relevant and well-cited.
- **Missing**: The paper does not cite \citet{le2020LISTA} or \citet{giryes2018deep} on the theoretical properties of deep unfolded networks. These would strengthen the theoretical framing.

### Methodology
- The LISTA architecture (Section 3.3) is standard and well-described.
- The FFT-based convolution (Eq.~7) is a useful implementation detail.
- The parameter analysis (Section 3.4) correctly identifies the $O(N^2)$ scaling issue.

### Results
- The NMSE saturation analysis is thorough and honest.
- The BER analysis is the paper's strongest contribution.
- The ablation study with 20 seeds is exemplary.
- The hardware complexity analysis (Section 4.13) is comprehensive.

### Discussion
- Section 5.1's discussion of MMSE implications is important.
- The comparison with LISTA-CP (Section 4.8) needs deeper analysis (see W1).
- The limitations section (5.3) is honest.

### References
- Comprehensive and up-to-date. All major works in deep unfolding and sparse channel estimation are cited.
- **Missing**: \citet{le2020LISTA} on LISTA convergence, \citet{giryes2018deep} on deep network recovery guarantees, \citet{chang2022channel} on deep learning for channel estimation in 6G.

---

## Questions for Authors

1. **LISTA-CP generality**: Does the identical performance of LISTA and LISTA-CP hold for correlated channel models (e.g., ITU channels with correlated taps)? If the spectral norm $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ increases for correlated channels, LISTA-CP's clipping may become active and the performance may differ.

2. **Complex-valued extension**: The paper uses real-valued channels throughout. Can you comment on whether the findings are expected to extend to complex-valued channels? Specifically, does the soft-thresholding operator (Eq.~5) need modification for complex inputs?

3. **LISTA variant comparison**: The paper discusses OCLISTA and LISTA-AMP in Section 5.1 but does not compare against them. Can you provide at least a qualitative analysis of whether these variants would exhibit the same NMSE saturation under broad-range training?

4. **ITU channel diversity**: Can you test on additional channel models beyond PedA and VehA? Specifically, a channel with correlated tap amplitudes would test whether LISTA's error concentration property holds for non-i.i.d.~taps.

5. **Practical SNR range**: The paper tests SNR from $-5$ to 40 dB. In practical 5G systems, the operating SNR is typically 5--20 dB. Can you comment on whether LISTA's saturation at $-25$~dB is acceptable for this SNR range, given that OMP achieves $-19$ to $-37$ dB?

---

## Minor Issues

### Literature Gaps
- Add citation to \citet{le2020LISTA} for LISTA convergence analysis.
- Add citation to \citet{giryes2018deep} for theoretical properties of deep unfolded networks.
- Consider citing \citet{chang2022channel} for deep learning channel estimation in 6G context.

### Terminology
- Section 3.3: "learnable linear mapping $\mathbf{W}^{(k)}$" — in the LISTA literature, this is typically called the "weight matrix" or "synthesis matrix." "Linear mapping" is correct but non-standard.
- Section 4.12: "error sparsity analysis" — consider "error localization analysis" for clarity.

### Figures and Tables
- Table 6 (NMSE vs Channel Length): The footnote about pilot ratio $M/N$ varying is important. Consider making this more prominent in the table caption.
- Table 13 (Error Sparsity): Add a row for LASSO to show where its error concentrates.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 60 | Adequate | LISTA is well-established; the contribution is analytical insight. The BER-NMSE mechanism analysis is novel. |
| Methodological Rigor (25%) | 72 | Strong | Comprehensive experiments with good statistical practices. The ablation with 20 seeds is exemplary. Some gaps in LISTA-CP analysis and MMSE validation. |
| Evidence Sufficiency (25%) | 68 | Adequate | 13 experiments provide broad coverage. ITU validation is limited (2 models). Missing comparison with LISTA variants. |
| Argument Coherence (15%) | 73 | Strong | The BER-NMSE disconnect argument is well-constructed. The paper honestly acknowledges limitations. |
| Writing Quality (15%) | 75 | Strong | Clear, professional prose. Good section organization. Literature review is comprehensive. |
| Literature Integration | 72 | Strong | Comprehensive coverage of key works. Some gaps in theoretical foundations (LISTA convergence theory). |
| **Weighted Average** | **69.9** | **Minor Revision** | |

---

## Overall Score: 70/100
