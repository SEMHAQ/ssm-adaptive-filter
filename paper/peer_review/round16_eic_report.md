Here is the complete EIC review report.

---

# Peer Review Report -- Digital Signal Processing (Elsevier)

---

## Manuscript Information

- **Title:** Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Author:** Huanjie Yu, Hunan University of Technology and Business
- **Manuscript Type:** Research Article
- **Target Journal:** Digital Signal Processing (Elsevier)
- **Date of Review:** 2026-06-01

---

## Reviewer Information

- **Role:** Editor-in-Chief (EIC)
- **Expertise:** Deep learning for signal processing, sparse recovery, communication system design
- **Conflicts of Interest:** None declared

---

## Overall Assessment

**Recommendation:** Minor Revision

**Confidence Score:** 4 / 5

**Summary:** This paper presents a systematic empirical analysis of LISTA applied to sparse channel estimation. Rather than claiming architectural novelty, the paper honestly characterizes LISTA's limitations (NMSE saturation at -25 dB, trailing OMP by 13-33 dB and FISTA by 1-27 dB) while identifying a genuinely interesting mechanism: LISTA concentrates 100% of estimation error on true tap locations, providing tangible BER benefits under ZF equalization for 16-QAM. The statistical methodology is unusually rigorous for this domain (Holm-Bonferroni correction, Cohen's d, 20-seed ablation). The paper is well-suited for Digital Signal Processing, as it addresses the intersection of deep unfolding and sparse channel estimation with practical system-level analysis. However, the contribution is constrained by the real-valued-only channel model, the absence of CNN/Transformer baselines, and the fact that FISTA outperforms LISTA at every SNR point without any training. The paper's value lies primarily in the mechanism analysis and the honest assessment of deep-unfolded architectures, not in demonstrating a new state-of-the-art method.

---

## Strengths

**Strength 1: Honest and rigorous characterization of LISTA's limitations.**
The paper transparently reports that LISTA saturates at approximately -25 dB for SNR >= 10 dB (Table 1, lines 283-301), trailing OMP by 13-33 dB and FISTA by 1-27 dB (Table in Section 4.12, lines 796-813). This level of honesty is rare and valuable. The paper does not obscure these findings but instead investigates their causes, attributing the saturation to the scale-invariant loss and mixed-SNR training (Section 5.1, lines 913-923), and demonstrating that SNR-specific training breaks the saturation to achieve -31 dB (Table 10, lines 571-584). This approach -- presenting a method's limitations as findings rather than hiding them -- is a model for the field.

**Strength 2: Novel mechanism analysis connecting error structure to BER.**
The error concentration analysis (Section 4.12, lines 718-764) is the paper's most significant intellectual contribution. The finding that LISTA concentrates 100.0% +/- 0.0% of estimation error on true tap locations (vs. 95.2% +/- 0.6% for OMP and 92.4% +/- 0.4% for ISTA) with 267x less error on non-support taps than OMP provides a mechanistic explanation for the BER-NMSE disconnect. The ISTA control experiment (Table 13, lines 749-762) correctly identifies that this concentration is partially generic to soft-thresholding (92.4% for ISTA) but enhanced by LISTA's learned parameters (100.0%). The generalization of this mechanism to K=10 (99.9%) and ITU channels (99.3-99.5%) strengthens the finding. This is a genuine contribution to understanding deep-unfolded architectures for sparse recovery.

**Strength 3: Exemplary statistical methodology.**
The paper employs Holm-Bonferroni correction for multiple comparisons (lines 277, 644, 673), reports Cohen's d effect sizes (Tables 3 and 11), uses both parametric and non-parametric tests (Section 4.11, line 670), and conducts the ablation study with 20 random seeds to address the statistical power limitation of the initial 5-seed experiment (Section 4.11, lines 668-688). The honest reporting that the 5-seed ablation produced false negatives for threshold and per-layer parameters (line 688: "The Round 2 finding that these components were 'not individually significant' was a false negative attributable to the low statistical power of n=5 seeds") demonstrates methodological integrity that strengthens the entire paper.

**Strength 4: Clear practical deployment guidance.**
The paper provides actionable recommendations for practitioners: SNR-specific training for known operating points (-31 dB vs -25 dB, Section 4.9), L=10-20 layers for optimal depth-efficiency tradeoff (Table 6, lines 416-443), M/N >= 2 for stable operation (Table 5, lines 396-410), and a decision framework for choosing between LISTA, OMP, and FISTA based on the deployment scenario (Section 5.3, lines 947-959). The discussion of when ZF equalization is relevant (Section 5.1, lines 930-931) adds practical context.

**Strength 5: Comprehensive experimental design.**
The experimental scope is broad and systematic: SNR sweep (-5 to 40 dB), sparsity sweep (K=2 to 15), channel length sweep (N=32 to 256), pilot ratio analysis (M/N = 1.5 to 4.0), depth analysis (L=1 to 20), ITU channel models, LISTA-CP comparison, FISTA comparison, MMSE and ZF BER with QPSK and 16-QAM, and a 20-seed ablation. Each experiment is well-motivated and the cross-table consistency discussion (lines 345-363) demonstrates awareness of experimental pitfalls.

---

## Weaknesses

**Weakness 1: Real-valued channel model severely limits practical relevance.**

- **Problem:** All experiments use real-valued channel impulse responses (h in R^N) with BPSK pilot signals (lines 153, 259). Real wireless channels are complex-valued, and practical systems use QAM modulations with complex baseband signals. The paper acknowledges this limitation (lines 965-966) but does not provide even preliminary results for the complex case.

- **Why it matters:** The soft-thresholding operator (Eq. 5, line 176), the error concentration metric (Eq. 17, line 721-723), and the NMSE loss (Eq. 8, line 222) are all defined for real-valued signals. The paper's central finding -- 100% error concentration on true taps -- may not hold for complex-valued channels, where the phase component introduces additional degrees of freedom that could affect error distribution. The BER results (Section 4.10) use QPSK and 16-QAM but only for the equalizer simulation; the channel estimation itself remains real-valued. This creates a disconnect: the paper's practical recommendations are for communication system designers who work with complex baseband signals.

- **Suggested fix:** At minimum, provide a brief appendix or supplementary material with complex-valued channel estimation results for QPSK pilot signals and complex-valued LISTA (using magnitude-based soft-thresholding: S_theta(z) = z * max(1 - theta/|z|, 0)). The qualitative findings may well transfer, but this needs to be demonstrated, not assumed.

- **Severity:** Moderate. The real-valued model is acceptable for a focused mechanism analysis paper, but it limits the paper's direct applicability to the DSP readership.

**Weakness 2: FISTA with 20 iterations outperforms LISTA at every SNR point, undermining the paper's core premise.**

- **Problem:** Table in Section 4.12 (lines 796-813) shows that FISTA with 20 iterations and grid-searched threshold outperforms LISTA by 1-27 dB across all SNR levels, with the gap widening from ~1 dB at SNR=-5 dB to ~27 dB at SNR=40 dB. FISTA requires no training data, no GPU computation, and has the same iteration count as LISTA's layer count.

- **Why it matters:** LISTA's original premise (Gregor and LeCun, 2010) is that learned parameters accelerate convergence beyond fixed-parameter ISTA. If FISTA with the same iteration count and simple grid-searched threshold outperforms LISTA at every operating point, the fundamental motivation for LISTA in channel estimation is weakened. The paper acknowledges this (line 815-816: "LISTA's learned parameters do not provide improvement over standard accelerated ISTA in terms of NMSE") but then pivots to the error concentration mechanism as the primary contribution. While the mechanism analysis is valuable, the paper should more clearly frame itself as an analysis of why LISTA fails to outperform FISTA, rather than as a study of LISTA for channel estimation.

- **Suggested fix:** Reframe the paper's positioning. The title and abstract currently suggest a systematic analysis of LISTA for channel estimation. A more accurate framing would emphasize that the paper demonstrates FISTA's superiority over LISTA for channel estimation while discovering a previously uncharacterized error concentration mechanism that provides BER benefits under ZF equalization. Additionally, include FISTA in all tables (currently it appears only in Table 8 and the pilot ratio analysis) so readers can see the three-way comparison throughout.

- **Severity:** Moderate. The paper is honest about this limitation, but the framing could be tightened.

**Weakness 3: No CNN or Transformer baselines for the deep learning channel estimation problem.**

- **Problem:** The paper does not include any CNN (Ye et al., 2018; Gao et al., 2019) or Transformer (Zhang et al., 2020) baselines (line 261: "We do not include CNN or Transformer baselines, as our focus is on understanding LISTA's behavior within the deep unfolding paradigm"). Section 5.2 (lines 935-941) provides only a qualitative discussion, citing different NMSE ranges from published papers with incompatible experimental setups.

- **Why it matters:** For the Digital Signal Processing readership, practitioners need to know whether deep unfolding is competitive with other deep learning approaches. The paper's argument that "drawing quantitative conclusions from such incomparable results would be misleading" (line 941) is valid, but it also means the paper cannot answer the most practical question: should I use LISTA, a CNN, or a Transformer for my channel estimation problem? The paper's own results show LISTA trailing FISTA (a non-learning method) by 1-27 dB, which raises the question of whether any deep learning approach is justified here.

- **Suggested fix:** Implement at least one CNN baseline (e.g., a 1D-CNN with comparable parameter count, ~80K parameters) under the same experimental protocol (N=64, K=5, M=256, same training data). This would provide a direct comparison and significantly strengthen the paper's practical value. If the CNN also trails FISTA, that strengthens the paper's message about the limitations of deep learning for this problem. If the CNN outperforms LISTA, that contextualizes LISTA's limitations within the broader deep learning landscape.

- **Severity:** Moderate. The paper's focus on mechanism analysis partially compensates, but the absence of deep learning baselines limits its utility as a benchmark.

**Weakness 4: The 100% error concentration finding raises a potential numerical artifact concern.**

- **Problem:** LISTA achieves "100.0% +/- 0.0%" error concentration on true taps (Table 12, line 732), meaning that across 5 seeds, the fraction of error on non-support taps is exactly 0.01% +/- 0.01% with zero variance. The 95% confidence interval is [100.0, 100.0] (line 736). This perfect reproducibility across seeds is suspicious and could indicate a numerical artifact of the soft-thresholding operator rather than a genuine learned property.

- **Why it matters:** If the threshold theta^(k) is larger than the typical magnitude of non-support tap estimates, the soft-thresholding operator will zero out all non-support taps by construction, making 100% error concentration a trivial consequence of aggressive thresholding rather than a meaningful learned behavior. The paper does not report the learned threshold values or verify that non-support taps are being zeroed by thresholding rather than by some other mechanism.

- **Suggested fix:** Report the learned threshold values theta^(k) for each layer (Table 11 ablation already shows that fixing the threshold at 0.1 degrades NMSE by 14 dB, but the actual learned values are not shown). Additionally, compute the error concentration for the pre-thresholding intermediate representation (after the W^(k) h^(k) - mu^(k) g^(k) step but before soft-thresholding) to distinguish between thresholding-induced and genuinely learned concentration. If pre-thresholding concentration is already high, the finding is less novel; if it is low and only becomes 100% after thresholding, the finding is an artifact of the operator, not the learned parameters.

- **Severity:** Moderate. This does not invalidate the paper but requires clarification to ensure the finding is genuine.

**Weakness 5: The paper's scope is narrow relative to the journal's readership.**

- **Problem:** The paper analyzes a single method (LISTA) on a single problem (sparse channel estimation) with a single channel model (real-valued, i.i.d. Gaussian taps) and a single pilot configuration (BPSK). The DSP journal covers a broad range of signal processing topics, and the paper's findings -- while rigorous -- are specific to this narrow experimental setting.

- **Why it matters:** The paper's primary contribution is the mechanism analysis (error concentration on true taps), which is an interesting finding about deep-unfolded architectures in general. However, the paper does not generalize this finding to other deep-unfolded methods (e.g., LISTA-CP, OCLISTA, ALISTA) or to other sparse recovery problems (e.g., image reconstruction, source separation). The LISTA-CP comparison (Section 4.8) shows identical performance, which is informative but does not extend the mechanism analysis.

- **Suggested fix:** Strengthen the generalizability discussion by at least theoretically analyzing whether the error concentration mechanism would apply to other soft-thresholding-based deep-unfolded architectures (ISTA-Net, LISTA-AMP). The paper already mentions AMP theory (Section 5.1, lines 925-926) but does not develop this connection into a generalizable insight.

- **Severity:** Low. The paper's depth compensates for its narrow scope, and the mechanism analysis has broader implications for the deep unfolding paradigm.

---

## Detailed Comments

### Abstract (Lines 57-59)
The abstract is well-written and comprehensive. It honestly states all major findings including LISTA's limitations. The statistical reporting (p-values, confidence intervals) in the abstract is appropriate and sets the right expectations.

### Introduction (Section 1, Lines 79-106)
The introduction is clear and well-structured. The six enumerated contributions (lines 91-103) are specific and well-scoped. The explicit statement "rather than claiming architectural novelty" (line 89) correctly positions the paper as an analysis study. However, the introduction could better motivate why LISTA analysis is still relevant given that FISTA outperforms it: what does LISTA's error structure teach us about deep unfolding in general?

### Related Work (Section 2, Lines 111-144)
The related work section is comprehensive, covering sparse channel estimation, deep unfolding, deep learning for channel estimation, classical adaptive filtering, and hardware deployment. The bibliography includes 35 references spanning the key areas. The distinction between model-driven and data-driven approaches (line 139) is well-articulated. One gap: the paper does not discuss recent work on learned ISTA variants specifically designed for channel estimation (e.g., Liu et al., 2020 is mentioned but not compared against).

### Method (Section 3, Lines 149-248)
The method section is clearly written with standard notation. The LISTA architecture (Eq. 7, line 185) follows the canonical formulation. The parameter analysis (lines 206-209) is useful: 82K parameters for N=64, scaling as O(N^2). The FFT-based convolution (Eq. 10, line 198-199) is a reasonable implementation choice. One issue: the paper states "The learnable mapping W^(k) is a standard component of LISTA" (line 189) but does not discuss whether structured alternatives (Toeplitz, circulant) could reduce the O(N^2) parameter count -- this is mentioned only in the discussion (line 870).

### Experiments (Section 4, Lines 253-901)
The experimental section is extensive and well-organized. Key observations:
- The cross-table consistency discussion (lines 345-363) is excellent and demonstrates awareness of experimental pitfalls.
- The pilot ratio analysis (Table 5) is a valuable addition that characterizes LISTA's operating envelope.
- The 20-seed ablation (Section 4.11) appropriately addresses the statistical power concern from the 5-seed experiment.
- The BER analysis (Section 4.10) with 200 realizations per SNR point is statistically sound.
- The FISTA comparison (Section 4.12) is critical and appropriately placed as a reality check.

### Discussion (Section 5, Lines 907-969)
The discussion is thoughtful and well-structured. The analysis of whether the saturation is architecture-specific or a training artifact (lines 913-923) is convincing. The AMP theory contextualization (lines 925-926) is appropriate and correctly attributes the LISTA-AMP connection to prior work. The deployment decision framework (lines 947-959) is practical. The limitations section (lines 961-969) is honest and comprehensive.

### Conclusion (Section 6, Lines 975-981)
The conclusion accurately summarizes the findings without overstating contributions. The emphasis on the mechanism analysis as the primary contribution is appropriate.

---

## Questions for Authors

**Question 1:** What are the learned threshold values theta^(k) for each layer in the trained LISTA? If these values are consistently larger than the typical magnitude of non-support tap estimates, the 100% error concentration may be a trivial consequence of aggressive soft-thresholding rather than a genuinely learned property. Please report the threshold values and compute error concentration on the pre-thresholding intermediate representation.

**Question 2:** The FISTA comparison (Table 8) shows that FISTA outperforms LISTA by 1-27 dB at all SNR levels. Did you try increasing LISTA's layer count beyond 20 to see if the gap narrows? If LISTA with L=50 or L=100 layers could match FISTA with 20 iterations, that would change the interpretation of the depth analysis (Table 6).

**Question 3:** The paper claims the NMSE saturation is a training artifact rather than an architectural limitation (Section 5.1). Have you verified this by training LISTA on a single SNR point (e.g., SNR=20 dB only) and checking whether the NMSE improves beyond -31 dB? If it does not, the saturation may have an architectural component after all.

**Question 4:** The error concentration metric (Eq. 17) is defined for real-valued signals. For complex-valued channels, would you define it over the magnitude squared |h_est - h_true|^2, or would you also consider phase errors separately? This is important for extending the mechanism to practical systems.

---

## Minor Issues

1. **Line 209:** "At N=256, the per-layer mapping alone has 65,536 parameters, yielding 1,310,740 total parameters" -- verify this arithmetic: 20 * (256^2 + 2) = 20 * 65538 = 1,310,760, not 1,310,740. The discrepancy is 20 (the 2 parameter count per layer was dropped).

2. **Table 2 (line 326):** At K=15, LISTA shows std of 8.27 dB with one seed diverging. Consider reporting median +/- MAD instead of mean +/- std for robustness, or explicitly excluding the diverged seed and reporting on 4 seeds.

3. **Table 5 (line 402):** At M/N=1.5, OMP and LASSO values lack standard deviations, while LISTA reports mean +/- std. For consistency, report std for all methods or explain why only LISTA has variability.

4. **Line 563:** The text states "training log diagnostics confirm that the weight clipping constraint was properly implemented and monitored: across all 5 seeds (1,000 total training epochs)" -- clarify: 5 seeds x 200 epochs = 1,000, which is correct, but the phrasing could be clearer.

5. **Line 742:** "OMP's slightly higher non-support error (4.81% vs 0.01%) and higher noise enhancement (13.7 vs 7.8) degrade equalization quality" -- the noise enhancement values are from SNR=20 dB (Table 14), but the error sparsity values are also at SNR=20 dB. The cross-reference should be explicit.

6. **Line 963:** "LISTA's support recovery (J = 0.78) is lower than OMP's (J = 0.97)" -- Table 7 reports Jaccard of 0.929 vs 0.968 at SNR=20 dB, not 0.78 vs 0.97. Verify which SNR point the 0.78 refers to; it may be from SNR=0 dB where J is not reported in the paper.

7. **References:** The bibliography includes 35 entries, which is appropriate for this journal. However, several references use inconsistent formatting (e.g., some NeurIPS proceedings are listed as "journal" entries rather than "inproceedings"). This should be standardized.

8. **AI Disclosure (line 994):** The declaration states Claude was used for "conducting simulated peer review to identify potential weaknesses." This is a commendable level of transparency but raises a question: were the statistical analyses and experimental code also AI-assisted? The declaration should be more specific about which computational results were human-verified.

---

## Dimension Scores

| Dimension | Score (0-100) | Comments |
|-----------|:---:|----------|
| **Originality** | 62 | The paper does not propose a new method but provides a novel mechanism analysis (error concentration on true taps) and a comprehensive empirical characterization. The LISTA-CP comparison, FISTA comparison, and ISTA control experiment add original insights. However, the core method (LISTA) is 14 years old and the application to channel estimation is not new. |
| **Significance** | 65 | The mechanism analysis (error concentration) is a genuine contribution to understanding deep-unfolded architectures. The practical deployment guidance is useful. However, the finding that FISTA outperforms LISTA at every SNR point limits the practical significance for channel estimation specifically. The real-valued-only model further limits direct applicability. |
| **Rigor** | 85 | The experimental methodology is unusually rigorous: 20-seed ablation, Holm-Bonferroni correction, Cohen's d effect sizes, paired t-tests, 200 BER realizations per SNR point, ISTA control experiment, and cross-table consistency analysis. The honest reporting of limitations and false negatives strengthens credibility. Minor concerns about the 100% error concentration finding and the lack of pre-thresholding analysis. |
| **Clarity** | 82 | The paper is well-organized with clear section structure. The abstract honestly summarizes all findings. Tables and figures are well-formatted. The cross-table consistency discussion (Section 4.3) is a model of transparent reporting. Some sections are verbose (the Discussion could be condensed). The decision framework (Section 5.3) is clear and actionable. |
| **Relevance to DSP** | 72 | The paper addresses sparse channel estimation, which is core to the DSP readership. The BER analysis with MMSE and ZF equalization connects to practical communication systems. However, the real-valued-only model and the absence of complex baseband analysis limit direct relevance to modern wireless systems. The mechanism analysis has broader implications for deep-unfolded signal processing. |
| **Completeness** | 70 | The experimental scope is broad (12 experiments covering SNR, sparsity, channel length, depth, ablation, generalization, BER, ITU channels, LISTA-CP, FISTA, SNR mitigation, mechanism analysis). However, the absence of complex-valued channels, CNN/Transformer baselines, and hardware measurements leaves important gaps. The FISTA comparison is present but not integrated into all tables. |
| **Presentation** | 78 | The paper is well-written with professional LaTeX formatting using the Elsevier CAS template. Tables are clear and well-annotated. The statistical reporting is exemplary. Some figures are referenced but not included in the LaTeX source (e.g., Figure 1 references `figures/fig_nmse_vs_snr.pdf`). The paper could benefit from a summary figure or table consolidating all key findings. |

**Overall Weighted Score: 73 / 100**

---

**Final Recommendation: Minor Revision**

The paper makes a meaningful contribution through its mechanism analysis of error concentration on true taps and its honest, rigorous characterization of LISTA's limitations for channel estimation. The statistical methodology is exemplary. The paper is suitable for Digital Signal Processing after addressing the following minor revisions:

1. Add a brief complex-valued channel estimation result (even in an appendix) to validate the mechanism's generalizability.
2. Report learned threshold values and pre-thresholding error concentration to verify the 100% finding is genuine.
3. Tighten the framing to acknowledge that FISTA's superiority over LISTA is a central finding, not just a comparison point.
4. Integrate FISTA into all main tables for consistent three-way comparison.
5. Correct the Jaccard index discrepancy in the Discussion (line 963).