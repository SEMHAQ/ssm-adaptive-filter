# Peer Review Report — EIC

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 14

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC)

### Reviewer Identity
Prof.~Andreas Spanias, Editor-in-Chief, *Digital Signal Processing* (Elsevier). Expertise in adaptive signal processing, sparse recovery, and deep learning for communications. 25+ years editorial experience in signal processing journals. Review focus: journal fit, originality, significance to the DSP readership, and overall quality.

### Review Focus
Journal fit and scope alignment with *Digital Signal Processing*, originality of the contribution within the deep unfolding literature, significance of findings for the signal processing community, and overall manuscript quality and readiness for publication.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
4 — Mostly within my area of expertise, high confidence.

### Summary Assessment
This manuscript presents a systematic analysis of LISTA (Learned ISTA) applied to sparse channel estimation, focusing on understanding the mechanism behind LISTA's behavior rather than claiming architectural novelty. The paper reports that LISTA's NMSE saturates at approximately $-25$~dB on i.i.d.~Gaussian channels, trailing OMP by 13--33~dB and FISTA by 1--27~dB, but identifies an error concentration mechanism where LISTA places $99.9\%$ of estimation error on true tap locations (vs.~$94.9\%$ for OMP). The methodological approach is sound: 20-seed ablation studies with Holm--Bonferroni correction, 200-realization BER simulations with paired $t$-tests, and ISTA/FISTA control experiments provide rigorous evidence. The paper's honesty about LISTA's limitations is commendable and unusual. However, the originality is limited---LISTA is a well-known architecture, and the paper explicitly states it does not claim novelty. The contribution is primarily analytical (mechanism characterization) rather than methodological. The error concentration finding is interesting but its practical relevance is confined to ZF equalization scenarios, which are uncommon in modern receivers. The paper is well-suited for *Digital Signal Processing* as a thorough analytical study, but the incremental nature of the contribution warrants minor revision to strengthen the positioning and clarify the practical implications.

---

## Strengths

### S1: Exemplary Scientific Honesty and Transparency
The paper is remarkably transparent about LISTA's limitations. Rather than inflating the contribution, it explicitly states: "LISTA's value lies not in NMSE superiority... but in the error concentration mechanism" (Section 1, Contribution 2). Table 1 honestly reports LISTA trailing OMP by 13--33~dB. The FISTA comparison (Table 12) demonstrates that FISTA outperforms LISTA at all SNR levels. This level of honesty strengthens the paper's credibility and sets a positive example for the field.

### S2: Rigorous Statistical Methodology
The experimental methodology exceeds typical standards in the signal processing literature. The paper employs: (1) 20-seed ablation with paired $t$-tests and Cohen's $d$ effect sizes (Table 11), (2) Holm--Bonferroni correction for multiple comparisons, (3) 200 channel realizations per SNR point for BER analysis, (4) both parametric and non-parametric tests. The progression from 5-seed to 20-seed ablation (Section 4.11) demonstrates intellectual honesty about statistical power limitations.

### S3: Mechanism Analysis with ISTA Control Experiment
The error concentration mechanism (Section 4.12) is the paper's most novel contribution. The ISTA control experiment (Table 15) is particularly well-designed: it distinguishes LISTA-specific learning from generic soft-thresholding properties, showing LISTA enhances concentration from $97.2\%$ (ISTA) to $99.9\%$. The $50\times$ reduction in non-support error compared to OMP is a clean, interpretable result.

### S4: Comprehensive Baseline Comparisons
The paper compares against LMS, NLMS, OMP, LASSO, FISTA, ISTA, and LISTA-CP---a thorough set of baselines covering adaptive filtering, greedy, convex relaxation, and accelerated proximal methods. The FISTA comparison is particularly important as it is the natural "accelerated ISTA" baseline that prior LISTA papers often omit.

---

## Weaknesses

### W1: Limited Novelty in Architecture and Problem Setting
**Problem**: The paper explicitly states it does not claim architectural novelty (Section 2: "Rather than claiming architectural novelty, we focus on..."). LISTA was introduced in 2010, and its application to channel estimation has been explored in prior work (e.g., \citet{liu2020learned}). The problem setting (sparse channel estimation with i.i.d.~Gaussian channels) is standard.
**Why it matters**: For *Digital Signal Processing*, some degree of novelty is expected. The analytical contribution must compensate for the lack of methodological novelty.
**Suggestion**: Strengthen the positioning by emphasizing the mechanism analysis as the primary contribution. Consider adding a paragraph in the Introduction explicitly framing this as a "lessons learned" or "retrospective analysis" paper that provides insights unavailable from prior work. The ITU channel generalization and FISTA comparison are differentiators that should be foregrounded.
**Severity**: Minor

### W2: Practical Relevance of ZF Equalization Results
**Problem**: The error concentration mechanism provides BER benefits primarily under ZF equalization (Table 10), which the paper acknowledges is uncommon in modern receivers (Section 5.1: "MMSE is the standard equalizer in modern receivers"). Under MMSE---the practical equalizer---all estimators converge to similar BER. The paper devotes significant space (Sections 4.10, 4.12) to a result that applies to a niche scenario.
**Why it matters**: Readers may question the practical value of a mechanism that only manifests under ZF equalization.
**Suggestion**: The paper already partially addresses this by framing ZF as a "diagnostic tool for understanding error structure" (Section 5.1). Strengthen this framing further. Additionally, consider discussing whether the error concentration mechanism has implications for other equalization/detection scenarios beyond ZF (e.g., successive interference cancellation, maximum likelihood detection).
**Severity**: Minor

### W3: Deep Learning Comparison is Qualitative Only
**Problem**: The comparison with CNN and Transformer methods (Section 5.2, Table 13) is based on published results rather than direct experiments. The paper acknowledges this ("this comparison is indirect... drawn from different studies with varying channel models").
**Why it matters**: For a journal paper, an indirect comparison weakens the positioning against the broader deep learning literature. The NMSE ranges cited ($-20$ to $-35$~dB for Transformers) are too wide to be informative.
**Suggestion**: Either (a) conduct at least one direct comparison with a simple CNN baseline under identical conditions, or (b) narrow the scope of Table 13 to only include methods with directly comparable experimental settings, and remove speculative entries.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title accurately reflects the paper's content. "Systematic Analysis" is appropriate.
- The abstract is dense but complete. The $-25$~dB saturation, FISTA comparison, error concentration, and ablation findings are all mentioned. Consider slightly expanding the abstract to mention the LISTA-CP comparison.

### Introduction
- The six contributions are clearly enumerated. However, Contribution 5 (SNR-specific training) is a relatively minor finding that could be merged with Contribution 1.
- The motivation for studying LISTA specifically (rather than newer variants like OCLISTA or LISTA-AMP) could be strengthened. The paper mentions these variants in Section 5.1 but does not justify why LISTA is the right starting point.

### Literature Review
- Comprehensive coverage of sparse channel estimation, deep unfolding, and deep learning for channel estimation.
- The classical adaptive filtering subsection (Section 2.4) is brief but adequate.
- The paper correctly positions itself as an analytical study rather than a methods paper.

### Methodology
- Well-structured with clear parameter choices (N=64, K=5, M=256, L=20).
- The mixed-SNR training protocol is well-motivated and consistently applied.
- The computational complexity analysis (Section 3.6) is thorough.

### Results
- Tables and figures are well-designed and informative.
- The cross-table consistency note (Section 4.3) is an excellent addition that prevents confusion.
- The progression from 5-seed to 20-seed ablation demonstrates methodological maturity.

### Discussion
- Section 5.1 provides a nuanced discussion of the saturation mechanism.
- The "Is the saturation architecture-specific or a training artifact?" analysis is compelling.
- The deployment decision framework (Section 5.3) is practical and well-reasoned.

### Conclusion
- Accurately summarizes findings without overclaiming.
- Future research directions are concrete and actionable.

---

## Questions for Authors

1. The paper claims LISTA's error concentration provides "tangible BER benefits" under ZF equalization. Given that MMSE is the standard equalizer, can you quantify how often ZF equalization is used in practice (e.g., in 5G NR, Wi-Fi 7, or IoT standards)? This would help readers assess the practical relevance.

2. The SNR saturation is attributed to the "scale-invariant loss" and "mixed-SNR training." Have you experimented with alternative loss functions (e.g., weighted NMSE, SNR-conditioned loss) that might mitigate the saturation without requiring SNR-specific training?

3. Table 5 shows training divergence at $N=256$ (all seeds). Is this a fundamental scalability limit of LISTA with dense $\mathbf{W}^{(k)}$ matrices, or could it be addressed with better initialization or regularization?

---

## Minor Issues

### Language / Grammar
- The writing is generally of high quality. A few minor points:
  - Section 1, Contribution 2: "the advantage is masked under MMSE but manifests under ZF" — consider "is obscured" instead of "masked" for clarity.
  - Section 4.12: "LISTA's soft-thresholding operator enforces sparsity in the estimate" — repeated several times; consider varying phrasing.

### Figures and Tables
- Table 10 (16-QAM BER): The column headers "Sig." with asterisks/asterisks could be clearer. Consider adding a footnote explaining the significance notation.
- Figure references (e.g., "Fig.~\ref{fig:snr}") are used but the actual figure files are not included in the LaTeX source provided. Ensure all figures are present in the final submission.

### Layout
- The paper is well-structured for the CAS template. No layout issues observed.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 62 | Adequate | No architectural novelty; analytical contribution (mechanism analysis) is the primary novelty. Incremental over prior LISTA work. |
| Methodological Rigor (25%) | 82 | Strong | Excellent statistical methodology with 20-seed ablation, Holm--Bonferroni correction, effect sizes, and ISTA/FISTA control experiments. |
| Evidence Sufficiency (25%) | 78 | Strong | Comprehensive baselines, multiple experimental scenarios, ITU channel validation. Deep learning comparison is qualitative only. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow from problem to mechanism analysis. The BER-NMSE disconnect is well-explained. |
| Writing Quality (15%) | 82 | Strong | Professional academic prose. Transparent about limitations. Minor verbosity in some sections. |
| **Weighted Average** | **76.5** | **Minor Revision** | |

---

