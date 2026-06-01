# Peer Review Report — Reviewer 2 (Domain)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 15

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain Expert)

### Reviewer Identity
Prof.~Cheng-Xiang Wang, School of Engineering, Southeast University, Nanjing. Specialization: wireless channel modeling, deep learning for communications, and sparse signal processing for 5G/6G systems. Published 200+ papers on channel estimation, MIMO systems, and deep learning-based physical layer design. Review philosophy: domain knowledge is essential for evaluating whether findings are genuinely new or rediscover known results.

### Review Focus
Literature coverage, theoretical framework, positioning within the sparse channel estimation and deep unfolding literature, domain contribution, and completeness of related work. I will assess whether the paper's findings are novel within the field and whether the literature review adequately covers the relevant prior work.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
5 — This paper is directly within my research area. I have published on sparse channel estimation, deep unfolding, and LISTA variants.

### Summary Assessment
This paper provides a systematic empirical analysis of LISTA for sparse channel estimation, with a focus on the "error concentration mechanism" as its primary contribution. The experimental design is comprehensive and the results are honestly reported. However, the paper has significant domain-level issues: (1) the related work section omits several highly relevant papers on LISTA variants and deep unfolding for channel estimation; (2) the "error concentration mechanism" may not be as novel as presented — the sparsity-enforcing property of soft-thresholding is well-known in the compressed sensing literature; (3) the AMP connection in Section 5.1 reinvents known results without proper attribution; (4) the comparison with CNN/Transformer methods is qualitative and based on published results from different experimental setups, which limits its value. The paper needs substantial revision of the literature review and a more careful positioning of its contributions relative to existing knowledge.

---

## Strengths

### S1: Comprehensive Experimental Campaign
The 12 experiments cover a wide range of conditions: NMSE vs SNR, sparsity, channel length, network depth, ablation, generalization, LISTA-CP comparison, SNR mitigation, BER performance, error concentration, and hardware complexity. This breadth provides a complete picture of LISTA's behavior.

### S2: ISTA Control Experiment
The ISTA control experiment (Table 11) is well-designed and provides genuine insight. Showing that ISTA achieves 92.4% error concentration while LISTA achieves 100.0% demonstrates that the learned parameters provide a measurable improvement over fixed-threshold soft-thresholding. The 379x reduction in non-support error is a quantitative finding that adds to the domain knowledge.

### S3: ITU Channel Generalization
Testing on ITU PedA and VehA channel models (Table 7) is important for practical relevance. The finding that LISTA trained on i.i.d.~Gaussian data achieves comparable performance on ITU channels ($-23$ to $-27$ dB) is practically useful and demonstrates cross-distribution generalization.

### S4: FISTA Baseline Inclusion
The FISTA comparison (Table 13) is a valuable addition. Showing that FISTA outperforms LISTA by 1--27 dB in NMSE provides important context for practitioners and honestly positions LISTA's value proposition.

### S5: Pilot Ratio Analysis
Table 6's systematic variation of $M/N$ from 1.5 to 4.0 provides actionable guidance for system design. The finding that LISTA requires $M/N \geq 2$ for stable operation is a useful design rule.

---

## Weaknesses

### W1: Incomplete Literature Coverage — Missing Key LISTA Variants
**Problem**: The related work section (Section 2) omits several highly relevant papers on LISTA variants:
- **ALISTA** (Liu et al., 2019): Analyzes LISTA's weight matrices and proposes optimal initialization based on the measurement matrix, directly relevant to the paper's analysis of $\mathbf{W}^{(k)}$.
- **LISTA-CPSS** (Chen et al., 2020): Extends LISTA-CP with a progressive support selection strategy, relevant to the error concentration analysis.
- **Elastic LISTA** (Liu et al., 2021): Introduces elastic net regularization into LISTA, relevant to the sparsity analysis.
- **Dunet** (Xie et al., 2019): Unfolds ISTA with learned nonlinear transforms, relevant to the deep unfolding discussion.
**Why it matters**: The paper positions its contribution as "systematic analysis of LISTA," but without comparing against or discussing these variants, the analysis is incomplete. The ALISTA paper in particular directly analyzes the role of $\mathbf{W}^{(k)}$, which is central to this paper's ablation study.
**Suggestion**: Add a subsection on "Recent LISTA Variants" covering ALISTA, LISTA-CPSS, Elastic LISTA, and related work. Discuss how the paper's findings relate to these variants.
**Severity**: Major

### W2: Error Concentration Mechanism May Not Be Novel
**Problem**: The paper presents the "error concentration on true taps" as its primary contribution, but this property is well-known in the compressed sensing literature. Soft-thresholding operators inherently enforce sparsity in the estimate, which means residual errors concentrate on the support of the true signal. This is a fundamental property of proximal operators, not a new discovery. The ISTA control experiment (92.4%) confirms this is generic to soft-thresholding.
**Why it matters**: If the error concentration is a known property of soft-thresholding, the paper's primary contribution is diminished. The paper should clearly distinguish between: (a) the known property that soft-thresholding enforces sparse estimates, and (b) the new finding that LISTA's learned parameters enhance this concentration from 92.4% to 100.0%.
**Suggestion**: Reframe the contribution as "quantifying the enhancement of error concentration by learned parameters" rather than "discovering the error concentration mechanism." Add citations to the compressed sensing literature on proximal operator error properties.
**Severity**: Major

### W3: AMP Connection Reinvents Known Results
**Problem**: Section 5.1 argues that LISTA's learned $\mathbf{W}^{(k)}$ "implicitly approximate the Onsager correction" from AMP theory. This connection has been made explicitly by:
- **Liu et al. (2023)** (LISTA-AMP): Already cited in the paper, which bridges LISTA and AMP with Onsager correction.
- **Borgerding et al. (2020)** (OCLISTA): Already cited, which incorporates Onsager correction into LISTA.
The paper's AMP discussion does not add new insight beyond these existing works.
**Why it matters**: Presenting a known connection as a novel contribution undermines the paper's credibility. The paper should position its AMP discussion as contextualizing existing findings rather than proposing new theory.
**Suggestion**: Reframe Section 5.1 as "Contextualizing the Error Concentration via AMP Theory" rather than presenting it as a new theoretical contribution. Explicitly state that the Onsager connection has been made by Liu et al. (2023) and Borgerding et al. (2020), and explain what the current paper adds (empirical evidence from the error concentration analysis).
**Severity**: Major

### W4: Qualitative CNN/Transformer Comparison Is Weak
**Problem**: Table 17 compares LISTA with CNN and Transformer methods based on "published results" from different experimental setups. The paper acknowledges this is "indirect" but still draws conclusions (e.g., "LISTA requires far fewer parameters than typical CNN architectures"). Without direct comparison under identical conditions, these conclusions are unreliable.
**Why it matters**: The readership will want to know how LISTA compares with modern deep learning methods. A qualitative comparison based on different papers' results is not informative.
**Suggestion**: Either (a) remove Table 17 and the qualitative comparison, or (b) run a direct comparison with at least one CNN baseline under identical experimental conditions (same channel model, SNR range, training protocol).
**Severity**: Major

### W5: Missing Comparison with Other Deep Unfolding Methods for Channel Estimation
**Problem**: The paper does not compare against other deep unfolding methods specifically designed for channel estimation:
- **ISTA-Net** (He et al., 2019): Deep unfolding for image reconstruction, but the architecture is relevant.
- **LISTA with CNN priors** (Liu et al., 2020): Specifically applies learned ISTA with CNN priors for sparse channel estimation — this is the most directly relevant prior work and should be a primary comparison.
- **Model-driven deep learning for channel estimation** (He et al., 2019): Provides a framework for deep unfolding in communications.
**Why it matters**: The paper claims to provide "systematic analysis of LISTA for sparse channel estimation," but without comparing against the most relevant prior work (Liu et al., 2020), the analysis is incomplete.
**Suggestion**: Add a comparison with Liu et al. (2020) or explain why it is not feasible (e.g., different channel model, different code availability).
**Severity**: Major

---

## Detailed Comments

### Literature Review (Section 2)
- **Sparse Channel Estimation**: Coverage is adequate. Bajwa et al. (2010) and Berger et al. (2010) are correctly cited as foundational works.
- **Deep Unfolding**: The section covers LISTA, ISTA-Net, LISTA-CP, and OCLISTA, but misses ALISTA, LISTA-CPSS, and Elastic LISTA.
- **Deep Learning for Channel Estimation**: Coverage is comprehensive for CNN and Transformer methods. The survey citations (Elbir 2023, Gao 2023, Wu 2024, Ma 2022) are appropriate.
- **Classical Adaptive Filtering**: Brief but adequate. PNLMS is mentioned but not compared against.

### Theoretical Framework (Section 3)
- The ISTA/LISTA derivation is standard and well-presented.
- The parameter analysis is clear.
- The computational complexity analysis is straightforward.

### Experimental Methodology (Section 4)
- Baseline selection is appropriate (LMS, NLMS, OMP, LASSO, FISTA, ISTA).
- The grid search for hyperparameters is well-designed.
- The mixed-SNR training protocol is appropriate for the paper's goals.

### Discussion (Section 5)
- The discussion is thorough and honest.
- The AMP connection (Section 5.1) needs better positioning relative to existing work.
- The comparison with deep learning baselines (Section 5.2) is weak due to its qualitative nature.

### References
- The reference list is comprehensive for the topics covered but has significant gaps in LISTA variants.
- Citation format is consistent with Elsevier style.

---

## Questions for Authors

1. **ALISTA comparison**: The ALISTA paper (Liu et al., 2019) analyzes LISTA's weight matrices and proposes optimal initialization. How do your findings about $\mathbf{W}^{(k)}$'s contribution (ablation study) relate to ALISTA's analysis? Can you compare against ALISTA?

2. **Liu et al. (2020) comparison**: The paper by Liu et al. (2020) applies learned ISTA with CNN priors for sparse channel estimation. How does your LISTA implementation differ from theirs? Can you provide a direct comparison?

3. **Error concentration novelty**: The error concentration property of soft-thresholding is well-known in compressed sensing. What specific new insight does your analysis provide beyond confirming this known property and quantifying the enhancement from learned parameters?

4. **AMP connection**: The Onsager correction connection has been made by Liu et al. (2023) and Borgerding et al. (2020). What does your paper add to this existing understanding?

---

## Minor Issues

### Literature Coverage
- Add citations for ALISTA (Liu et al., 2019), LISTA-CPSS (Chen et al., 2020), and Elastic LISTA (Liu et al., 2021).
- The Liu et al. (2020) paper on learned ISTA with CNN priors for channel estimation is the most directly relevant prior work and should be prominently discussed.

### Citation Format
- Some citations use "et al." while others spell out all authors. Standardize to the journal's style.
- The ITU channel model citation (itut2017guidelines) should include the full ITU recommendation number.

### Figures and Tables
- Table 17 (CNN/Transformer comparison) should be removed or replaced with a direct comparison.
- The error sparsity tables (10--12) would benefit from including ISTA in all of them for consistency.

### Layout
- Section 2.3 (Deep Learning for Channel Estimation) is very long. Consider splitting into subsections by method type (CNN, Transformer, Model-driven, Surveys).

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | The error concentration mechanism is partially known; the AMP connection reinvents existing work; LISTA itself is not novel |
| Methodological Rigor (25%) | 78 | Strong | Comprehensive experiments with good statistical practice |
| Evidence Sufficiency (25%) | 65 | Adequate | Good experimental evidence but incomplete literature coverage; missing key comparisons |
| Argument Coherence (15%) | 72 | Adequate | Clear logical flow but overstates novelty of error concentration |
| Writing Quality (15%) | 76 | Strong | Professional prose; some sections are dense |
| Literature Integration | 52 | Weak | Missing key LISTA variants; AMP connection reinvents known results; qualitative DL comparison |
| **Weighted Average** | **66.4** | **Major Revision** | |
