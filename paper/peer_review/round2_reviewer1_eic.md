# Peer Review Report — EIC

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 2

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), Digital Signal Processing (Elsevier)

### Reviewer Identity
Prof. Dr. Elena Vasquez, Editor-in-Chief, Digital Signal Processing. Specialization: sparse signal processing, compressed sensing, and deep learning for communications. 20+ years of editorial experience in signal processing journals. Review preferences: methodological clarity, fair baselines, reproducibility, and practical relevance to the DSP community.

### Review Focus
Journal fit, originality, overall significance, and relevance to the DSP readership. I assess whether the paper makes a meaningful contribution to the journal's scope and whether the claims are supported by the evidence presented.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
4 — The paper falls squarely within my editorial domain (sparse signal processing, deep unfolding for communications). I am highly confident in my assessment of journal fit and contribution level.

### Summary Assessment
This paper investigates the Learned Iterative Shrinkage-Thresholding Algorithm (LISTA) for sparse channel estimation, providing ablation studies, generalization analysis, and practical deployment benchmarks. The experimental framework is comprehensive, covering SNR sweeps, sparsity variations, channel length scaling, depth analysis, ITU channel models, and SNR-specific training strategies. The writing is clear and the limitations are honestly reported.

However, the paper faces a fundamental tension: it claims LISTA as a "practical alternative" while simultaneously demonstrating that LISTA trails OMP by 13--33 dB on Gaussian channels and saturates at ~-25 dB. The SNR-specific training mitigation (achieving -31 dB) is promising but still leaves a 6 dB gap with OMP. The originality is limited — this is an application of a well-known architecture (LISTA, 2010) to a well-studied problem (sparse channel estimation), with the main contribution being the systematic analysis rather than methodological novelty. The paper needs to either (a) strengthen the practical case with BER/throughput results, or (b) reposition more clearly as an analysis/characterization paper with weaker deployment claims. I recommend Major Revision.

---

## Strengths

### S1: Comprehensive and Honest Experimental Framework
The paper presents 9 well-designed experiments covering the key dimensions relevant to practical deployment: SNR sensitivity, sparsity robustness, channel length scalability, network depth, ablation with statistical testing, cross-distribution generalization, ITU channel performance, inference time, and SNR mitigation strategies. The experimental setup is clearly described with sufficient detail for reproducibility (Section 4.1). The use of 5 random seeds with mean ± std reporting is appropriate, and the grid-searched baselines ensure fair comparison.

### S2: Rigorous Ablation with Effect Size Reporting
The ablation study (Section 4.5) stands out for its use of paired t-tests and Cohen's d effect sizes, which is uncommon in the deep unfolding literature. The finding that W^(k) provides a statistically significant contribution (+1.0 dB, p = 0.003, d = 2.8) while threshold and per-layer parameters show no individually significant effects provides genuine insight into what LISTA learns. This level of statistical rigor should be a model for the field.

### S3: Honest Reporting of Limitations
The paper does not oversell its results. The NMSE saturation at ~-25 dB is clearly reported with a plausible explanation (scale-invariant loss, fixed-depth architecture). The divergence at N=256 and K=15 is honestly disclosed. The conclusion correctly positions LISTA as useful "when speed is prioritized over maximum accuracy." This transparency builds credibility.

### S4: Practical Deployment Analysis
The inference time comparison (Table 6) and the SNR-specific training results (Table 8) provide actionable guidance for practitioners. The 33× speedup over OMP and the 6 dB improvement from SNR-specific training are concrete, quantifiable benefits that address real deployment needs.

---

## Weaknesses

### W1: Overstated Practical Claims Despite 13--33 dB Gap with OMP
**Problem**: The abstract and conclusion claim LISTA is "a practical alternative for sparse channel estimation when speed is prioritized," but the results show a 13--33 dB gap with OMP at SNR ≥ 10 dB (Table 1). At SNR = 20 dB, LISTA achieves -24.25 dB while OMP achieves -37.09 dB — a 12.84 dB difference that translates to a ~19× error ratio in linear scale. For communications systems, this gap directly impacts BER.
**Why it matters**: Reviewers and readers will question whether a -25 dB NMSE is acceptable for practical systems. Without BER results, the paper cannot substantiate its deployment claims.
**Suggestion**: Either (a) add BER simulations showing that LISTA's -25 dB NMSE is sufficient for acceptable BER in specific scenarios, or (b) weaken the practical claims and reposition as a characterization/analysis paper.
**Severity**: Major

### W2: Missing BER/Throughput Analysis
**Problem**: The paper evaluates NMSE but never translates this to bit error rate (BER) or throughput — the metrics that ultimately matter for communications systems. The practical deployment section (4.7) discusses inference time and ITU channels but never asks: "Does LISTA's NMSE advantage over LMS/NLMS translate to a BER advantage?"
**Why it matters**: NMSE is an intermediate metric. A 10 dB NMSE improvement may or may not translate to a meaningful BER improvement depending on the modulation, coding, and detection scheme. Without BER results, the practical impact is unquantified.
**Suggestion**: Add a BER simulation section using a standard modulation scheme (e.g., QPSK or 16-QAM) with the estimated channels. This would immediately clarify whether LISTA's NMSE is "good enough" for practical use.
**Severity**: Major

### W3: Originality Is Limited — Application Paper Without Architectural Contribution
**Problem**: The paper applies the standard LISTA architecture (Gregor & LeCun, 2010) to sparse channel estimation without any architectural modification. The "contributions" listed in the Introduction are analysis-oriented (systematic evaluation, ablation, generalization) rather than methodological. The Related Work (Section 2) acknowledges this but does not adequately address what gap in the existing literature this paper fills — prior work on deep unfolding for channel estimation already exists (Elbir 2023, Gao 2023, Wu 2024 surveys).
**Why it matters**: DSP publishes papers with clear methodological or analytical novelty. An application of a 15-year-old architecture to a well-studied problem needs a stronger novelty argument.
**Suggestion**: Either (a) introduce a meaningful architectural modification (e.g., structured W^(k) to address the O(N²) scalability issue), or (b) clearly position the paper as a rigorous benchmarking/characterization study and emphasize the ablation insights as the primary contribution.
**Severity**: Major

### W4: LISTA-CP Comparison Shows Identical Performance — Raises Questions
**Problem**: Table 7 shows that LISTA and LISTA-CP achieve identical NMSE across all SNR levels (differences = 0 dB to the reported precision). The paper explains this as "LISTA-CP weight constraints do not alter the learned parameters when training converges within L=20 layers," but this raises a concern: if the convergence guarantees of LISTA-CP have no practical effect, why include this comparison?
**Why it matters**: The identical results suggest either (a) the implementation is incorrect, (b) the training setup does not stress-test the convergence difference, or (c) the comparison is not meaningful at this depth.
**Suggestion**: Verify the LISTA-CP implementation and test at shallower depths (L=3-5) where convergence differences should be more pronounced. If the results are confirmed, explain more clearly why the comparison is still informative.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title is accurate and descriptive, though "Analysis of" is somewhat generic. Consider a more specific title that highlights the key finding (e.g., "Deep-Unfolded LISTA for Sparse Channel Estimation: When Speed Matters More Than Accuracy").
- The abstract is well-structured and honest. The saturation behavior is clearly stated. However, the phrase "practical alternative" in the final sentence is not fully supported by the 13--33 dB gap with OMP.

### Introduction
- The five contributions are clearly enumerated. However, contribution (1) ("systematic analysis") is not a traditional contribution — it's the paper's methodology. Consider leading with the ablation insights (contribution 2) as the primary contribution.
- The research gap is identified but could be sharper. What specifically do the existing surveys (Elbir 2023, Gao 2023, Wu 2024) leave unanswered that this paper addresses?

### Literature Review / Theoretical Framework
- Coverage is adequate for the compressed sensing and deep unfolding literature. The distinction from prior work (Section 2.2, last paragraph) is clear.
- Missing: comparison with other deep learning approaches for channel estimation (e.g., CNN-based, transformer-based) that do not use deep unfolding.

### Methodology / Research Design
- The experimental setup (Section 4.1) is well-described. The grid search for baselines ensures fairness.
- The mixed-SNR training protocol is well-justified and eliminates training-procedure-induced inconsistencies.
- Concern: only 5 seeds for statistical testing. With paired t-tests on n=5, the statistical power is limited. Consider 10+ seeds for the ablation study.

### Results / Findings
- Tables and figures are clear and well-formatted. The use of bold for best results and footnotes for diverged seeds is good practice.
- The SNR saturation is well-documented but the explanation (Section 5.1) could be deeper. What specific aspect of the scale-invariant loss causes saturation?

### Discussion
- The limitations section (5.3) is honest and comprehensive. The future research directions are appropriate.
- The practical deployment framework (Section 5.2) is useful but would be stronger with BER results.

### Conclusion
- The conclusion accurately summarizes the findings. The positioning as "when speed is prioritized" is appropriate.

### References
- References are comprehensive and current. The mix of seminal works (Candes, Donoho, Tibshirani) and recent surveys is appropriate.

---

## Questions for Authors

1. **BER Impact**: Have you evaluated whether LISTA's -25 dB NMSE (or -31 dB with SNR-specific training) translates to acceptable BER for standard modulation schemes (e.g., QPSK, 16-QAM)? This would significantly strengthen the practical deployment claims.

2. **LISTA-CP Verification**: The identical performance of LISTA and LISTA-CP (Table 7) is surprising. Can you verify the implementation by testing at shallower depths (L=3-5) where convergence differences should be more pronounced? Can you confirm that the LISTA-CP weight constraints are actually applied during training?

3. **Computational Cost of Training**: The paper reports inference time but not training time. For practical deployment, the training cost (data generation + training) is important. Can you provide training time estimates and discuss whether the training overhead is justified by the inference speedup?

4. **Comparison with CNN/Transformer Methods**: How does LISTA compare with non-unfolded deep learning approaches (e.g., CNN-based channel estimators) that have been proposed for similar tasks? This would help position LISTA within the broader landscape.

---

## Minor Issues

### Language / Grammar
- Overall writing quality is good. Minor polish needed in a few places:
  - Section 4.1: "each training batch uses a randomly sampled SNR" — clarify whether this is per-sample or per-batch.
  - Table 3 caption: "Pilot ratio M/N varies" — this should be noted more prominently as it affects interpretability.

### Figures and Tables
- Table 3 (Channel Length): The diverged result at N=256 (+26.84 dB) makes the table hard to read. Consider using "Diverged" or "N/A" instead of a positive NMSE value.
- Figure 2 (NMSE vs Sparsity): The K=15 point with std = 8.27 dB makes the y-axis scale awkward. Consider a separate inset or footnote.

### Layout
- The paper uses the Elsevier CAS template correctly. No layout issues noted.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | Application of well-known LISTA to well-studied problem; contribution is analytical, not methodological |
| Methodological Rigor (25%) | 68 | Adequate | Good experimental design, fair baselines, statistical testing; limited by n=5 seeds |
| Evidence Sufficiency (25%) | 63 | Adequate | Comprehensive experiments but missing BER analysis; 13-33 dB gap with OMP weakens claims |
| Argument Coherence (15%) | 70 | Adequate | Clear structure, honest limitations, but practical claims not fully supported |
| Writing Quality (15%) | 74 | Strong | Clear, professional academic writing; well-organized |
| **Weighted Average** | **65.2** | **Adequate** | **Major Revision recommended** |
