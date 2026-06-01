# Peer Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 10

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC)

### Reviewer Identity
Associate Editor of *Digital Signal Processing* (Elsevier), specializing in model-based deep learning for communications and signal processing. 15 years of editorial experience in the signal processing domain, familiar with the deep unfolding literature from Gregor & LeCru (2010) through recent LISTA variants.

### Review Focus
Journal fit, originality, significance to the readership, and overall structural coherence. I do not dive deep into statistical methodology (Reviewer 1's domain) or hardware implementation details (Reviewer 3's domain).

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — The paper falls squarely within signal processing and deep unfolding, which is my core area. The BER equalization analysis touches on communications theory where I have moderate but not deep expertise.

### Summary Assessment
This paper investigates LISTA (Learned ISTA) for sparse channel estimation, providing a systematic analysis of generalization, ablation, BER performance, and practical deployment characteristics. The paper is notable for its intellectual honesty: it explicitly reports that LISTA trails OMP by 13–33 dB in NMSE and saturates at approximately −25 dB for SNR ≥ 10 dB, and attributes this to a training artifact rather than an architectural limitation. The BER mechanism analysis—showing that LISTA concentrates 99.9% of estimation error on true tap locations—is a genuinely insightful contribution that explains why LISTA achieves competitive BER despite worse NMSE under ZF equalization. The ablation study with 20 seeds and proper statistical testing (paired t-tests, Cohen's d) demonstrates methodological maturity. However, the paper's contribution is primarily analytical/empirical rather than architectural—it does not propose a new method, but rather provides a thorough characterization of an existing one. The extensive hedging of hardware claims (all marked as "theoretical estimates") is appropriate but weakens the practical deployment narrative. Overall, this is a solid analytical contribution that fits well within *Digital Signal Processing* and will interest readers working on deep unfolding for communications.

---

## Strengths

### S1: Intellectual Honesty in Reporting Negative Results
The paper explicitly and prominently reports that LISTA trails OMP by 13–33 dB in NMSE (Table 1, Section 4.2), rather than burying this finding. The title itself includes "Practical Limitations." This level of transparency is rare and valuable—it provides practitioners with realistic expectations for deep-unfolded channel estimators. The paper correctly reframes the contribution from "LISTA beats OMP" to "understanding LISTA's behavior and error structure," which is a more honest and ultimately more useful contribution.

### S2: BER Mechanism Analysis Provides Genuine Insight
Section 4.12 (Experiment 12) is the paper's strongest contribution. The finding that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP), with 50× less error on non-support taps (Table 15), provides a mechanistic explanation for the BER-NMSE disconnect. This is not trivially obvious and has practical implications for equalizer design. The three-part mechanism analysis (support recovery, error sparsity, noise enhancement) is well-structured and convincing.

### S3: Comprehensive Ablation with Statistical Rigor
The progression from 5-seed ablation (Table 6, where threshold and per-layer parameters appeared insignificant) to 20-seed ablation (Table 13, revealing all components are highly significant with p < 0.001) demonstrates methodological growth during the revision process. The inclusion of Cohen's d effect sizes, paired t-tests, and the explicit acknowledgment that the initial 5-seed experiment lacked statistical power (Section 4.11) is commendable.

### S4: Well-Structured Paper with Clear Contributions
The six enumerated contributions in the Introduction (Section 1) are clearly stated and each maps to a specific experiment. The paper follows a logical progression: baseline comparison → ablation → generalization → BER → hardware analysis. The Discussion section (Section 5) thoughtfully addresses the "so what?" question and provides a practical deployment framework.

### S5: SNR Saturation Mitigation is Practically Useful
Section 4.9 (Experiment 9) demonstrates that SNR-specific training mitigates the saturation, achieving −31 dB at SNR=20 dB (a 6 dB improvement). This is a practical, actionable finding for engineers deploying LISTA in known-SNR environments.

---

## Weaknesses

### W1: Contribution is Analytical, Not Architectural
**Problem**: The paper does not propose any architectural innovation—it applies standard LISTA (Gregor & LeCru, 2010) to channel estimation and characterizes its behavior. The "contribution" is primarily a thorough empirical analysis.
**Why it matters**: *Digital Signal Processing* readers expect methodological or algorithmic contributions. A purely analytical paper on a 15-year-old architecture may be seen as insufficiently novel.
**Suggestion**: The authors should more clearly position the paper as a "lessons learned" or "practical guide" contribution, and emphasize the BER mechanism analysis (which is genuinely novel insight) over the NMSE comparisons (which confirm what is already known about LISTA's limitations).
**Severity**: Major

### W2: Hardware Claims Lack Measured Validation
**Problem**: All hardware complexity claims (760K FLOPs, 20-stage pipelining, 33× speedup) are theoretical estimates. The paper acknowledges this repeatedly ("measured FPGA/ASIC results remain future work"), but the absence of any measured hardware results weakens the practical deployment narrative significantly.
**Why it matters**: Section 4.13 (Experiment 13) constitutes a substantial portion of the paper (approximately 2000 words), yet provides no empirical hardware validation. The theoretical FLOP analysis is straightforward arithmetic, not a research contribution.
**Suggestion**: Either (a) provide at least a prototype FPGA implementation with measured latency/power, or (b) significantly shorten the hardware section and position it as brief future-work outlook rather than a full experiment. Option (b) is more realistic given the single-author scope.
**Severity**: Major

### W3: Cross-Table Inconsistency Requires Reader Effort
**Problem**: Table 3 (NMSE vs Channel Length) reports LISTA NMSE of −32.29 dB at N=64, SNR=20 dB, while Table 1 (NMSE vs SNR) reports −24.25 dB at the same nominal configuration. The explanation (different training distributions) is provided in a footnote and in Section 4.3, but the inconsistency is confusing on first read.
**Why it matters**: Readers comparing tables may be confused or may question the validity of the results.
**Suggestion**: Add a prominent "Cross-Table Reference" box in Section 4.1 that explicitly explains the two training protocols and which table uses which. Alternatively, use different column headers (e.g., "LISTA (mixed-SNR)" vs "LISTA (channel-trained)") to make the distinction immediately visible.
**Severity**: Minor

### W4: Limited Generalizability of BER Mechanism Analysis
**Problem**: The mechanism analysis (Section 4.12) is conducted only on i.i.d. Gaussian channels with K=5, N=64, M=256. The paper acknowledges this in the "Scope and generalizability" paragraph at the end of Section 4.12, but the finding that LISTA concentrates error on true taps may not generalize to correlated channels (e.g., ITU models).
**Why it matters**: If the error concentration is specific to i.i.d. Gaussian channels, the mechanism analysis has limited practical value, since real channels have correlated tap amplitudes.
**Suggestion**: At minimum, report the error sparsity analysis (Table 15) for ITU channels as well, even if briefly. If the finding holds, it significantly strengthens the contribution.
**Severity**: Major

---

## Detailed Comments

### Title & Abstract
- The title is accurate and informative. "Analysis" correctly positions the paper as empirical rather than architectural. "Practical Limitations" signals honesty.
- The abstract is comprehensive but dense (~350 words). Consider trimming the BER mechanism details slightly to improve readability.

### Introduction
- The six enumerated contributions are clear and well-mapped to experiments. Good structure.
- The phrase "likely a training artifact from the scale-invariant loss" (contribution 1) is appropriately hedged.

### Literature Review
- Coverage is thorough, covering deep unfolding (LISTA, ISTA-Net, OCLISTA, LISTA-AMP), CNN/Transformer methods, and hardware deployment.
- The qualitative comparison with CNN/Transformer methods (Section 5.2, Table 17) is useful but indirect. The paper correctly acknowledges this limitation.

### Methodology
- The LISTA architecture description (Section 3.3) is clear and follows the standard formulation.
- The training protocol (mixed SNR, cosine annealing, gradient clipping) is well-documented.

### Results
- Tables 1–4 provide a comprehensive NMSE comparison across SNR, sparsity, channel length, and depth.
- The BER experiments (Tables 7–12) are well-designed with 200 realizations per point.
- Table 13 (20-seed ablation) is the statistical highlight of the paper.

### Discussion
- Section 5.1 (Gaussian vs ITU channels) provides valuable practical guidance.
- The deployment recommendation framework (Section 5.3) is actionable and useful.
- The limitations section (Section 5.4) is honest and thorough.

### Conclusion
- Conclusions are appropriately scoped and do not overclaim.
- The paper correctly emphasizes the mechanism analysis as the primary contribution.

---

## Questions for Authors

1. The error sparsity analysis (Table 15) shows LISTA concentrates 99.9% of error on true taps at SNR=20 dB on i.i.d. Gaussian channels. Does this finding hold on ITU channel models? A single supplementary table would significantly strengthen the mechanism analysis's generalizability claim.

2. The SNR saturation is attributed to the scale-invariant NMSE loss (Section 5.1). Have you experimented with alternative loss functions (e.g., absolute NMSE, weighted NMSE that penalizes high-SNR errors more) that might mitigate the saturation without requiring SNR-specific training?

3. Table 3 shows LISTA training diverges at N=256 (all seeds yield positive NMSE). Is this a fundamental scalability limit, or could it be addressed with more training data, longer training, or architectural modifications (e.g., structured weight matrices)?

---

## Minor Issues

### Language / Grammar
- The paper is generally well-written in academic English. No significant language issues.
- Some sentences are excessively long (e.g., the abstract has sentences exceeding 80 words). Consider breaking these up.

### Figures and Tables
- All tables are well-formatted and include appropriate statistical annotations (p-values, confidence intervals).
- Figure references are consistent.

### Layout
- The paper uses the Elsevier CAS template correctly.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 58 | Weak | No architectural novelty; analytical contribution on a 15-year-old method. BER mechanism analysis provides novel insight. |
| Methodological Rigor (25%) | 78 | Strong | Good experimental design, proper statistical testing with 20 seeds, effect sizes. 5-seed experiments are weaker but acknowledged. |
| Evidence Sufficiency (25%) | 75 | Strong | Comprehensive experiments across multiple conditions. Hardware claims lack measured validation. |
| Argument Coherence (15%) | 82 | Strong | Clear logical flow from NMSE analysis → BER mechanism → practical deployment. Hedging is appropriate. |
| Writing Quality (15%) | 80 | Strong | Well-structured, honest reporting, professional tone. Some overly long sentences. |
| **Weighted Average** | **74** | **Minor Revision** | Solid analytical contribution with clear strengths in mechanism analysis and statistical rigor. |

---

## Recommendation to Peer Reviewers

I recommend the following areas of focus for the peer reviewers:

- **Reviewer 1 (Methodology)**: Please scrutinize the statistical power of the 5-seed experiments (Tables 1-4) and the adequacy of the mixed-SNR training protocol. The 20-seed ablation (Table 13) is much stronger—please evaluate whether the initial experiments should have used larger sample sizes.

- **Reviewer 2 (Domain)**: Please evaluate whether the BER mechanism analysis (error concentration on true taps) is genuinely novel in the channel estimation literature, and whether the NMSE gap with OMP undermines the paper's practical value.

- **Reviewer 3 (Practical Deployment)**: Please assess the hardware complexity claims critically. The FLOP analysis is straightforward, but the pipelining and throughput claims need scrutiny. Are the theoretical estimates adequately caveated?

- **Devil's Advocate**: Please challenge whether the paper's extensive hedging is honest reporting or an attempt to make weak results look acceptable. Is the BER equivalence under MMSE a genuine finding or a trivial consequence of MMSE's design?
