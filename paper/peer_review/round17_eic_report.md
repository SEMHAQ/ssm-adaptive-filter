# Peer Review Report — EIC

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-ROUND17
- **Review Date**: 2026-06-01
- **Review Round**: Round 17

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), *Digital Signal Processing* (Elsevier)

### Reviewer Identity
Prof. Maria Rodriguez, Editor-in-Chief of *Digital Signal Processing*. Research expertise spans sparse signal recovery, deep unfolding architectures, and adaptive signal processing. 20+ years of editorial experience in signal processing journals. Particular interest in papers that bridge theoretical analysis with practical deployment insights.

### Review Focus
Overall journal fit, originality, significance to the DSP readership, coherence of the contribution narrative, and whether the paper advances the field beyond incremental extension.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Accept**
- [ ] **Reject**

### Confidence Score
5 — This paper falls squarely within my editorial expertise in sparse signal processing and deep unfolding for communications.

### Summary Assessment
This manuscript presents a systematic analysis of LISTA applied to sparse channel estimation, with a central finding that LISTA concentrates 100.0% ± 0.0% of estimation error on true tap locations—a mechanism the authors term "error concentration." The paper is methodologically thorough, with ablation studies across 20 seeds, BER simulations with statistical validation, and honest reporting of LISTA's limitations (NMSE saturation at −25 dB, trailing OMP by 13–33 dB). The pre-thresholding analysis and ISTA control experiment strengthen the mechanistic claim. The writing is clear and the contribution narrative is well-structured. However, the paper's central contribution—the error concentration mechanism—needs stronger positioning relative to the well-known sparsity-promoting property of soft-thresholding. The AMP theory connection, while interesting, remains speculative (noted by the authors themselves). The paper is suitable for *Digital Signal Processing* after minor revisions addressing the novelty framing and a few methodological clarifications.

---

## Strengths

### S1: Honest and Transparent Reporting of Limitations
The manuscript is commendably honest about LISTA's performance limitations. The authors clearly state that LISTA saturates at −25 dB, trailing OMP by 13–33 dB and FISTA by 1–27 dB (Table 1, Table 12). The cross-table consistency note (Section 4.3) transparently explains the 8 dB difference between training protocols. This level of honesty strengthens credibility and is refreshing in a field where negative results are often obscured.

### S2: Mechanism Analysis with Multiple Validation Layers
The error concentration analysis (Section 4.13) is well-designed with three complementary validations: (1) the ISTA control experiment (92.4% vs 100.0%) demonstrates the contribution of learned parameters over fixed thresholds, (2) the pre-thresholding analysis (68.3% before, 100.0% after) rules out trivial artifact explanations, and (3) the extension to K=10 and ITU channels demonstrates generalizability. The 267× and 379× non-support error reduction ratios are compelling quantitative metrics.

### S3: Comprehensive Ablation with Adequate Statistical Power
The progression from 5-seed to 20-seed ablation (Section 4.12) is methodologically sound. The authors honestly report that the 5-seed experiment produced false negatives for threshold and per-layer parameters, and the 20-seed experiment with Holm–Bonferroni correction reveals the full picture. The Cohen's d effect sizes (d = 1.5, 18.4, 24.1) are appropriately reported.

### S4: FISTA Baseline Comparison
Adding FISTA as a baseline (Table 12) is a significant strength. It directly demonstrates that LISTA's learned parameters do not improve NMSE over standard accelerated ISTA, clarifying that LISTA's value lies elsewhere (error concentration, potential hardware pipelining). This honest positioning strengthens the paper's contribution claims.

### S5: BER Analysis with Proper Statistical Validation
The BER simulations (Section 4.11) use 200 channel realizations per SNR point, paired t-tests, and Holm–Bonferroni correction. The MMSE vs. ZF comparison is well-motivated: MMSE convergence is expected behavior (honestly noted), while ZF reveals the error structure advantage. The 16-QAM results with corrected p-values at SNR ≥ 15 dB are convincing.

---

## Weaknesses

### W1: Novelty Framing Needs Strengthening
**Problem**: The paper's central contribution is the error concentration mechanism, but this is closely related to the well-known sparsity-promoting property of soft-thresholding. The authors acknowledge that ISTA already achieves 92.4% concentration (Section 4.13.3), and the paper explicitly states LISTA provides no NMSE improvement over FISTA. The question "what is the novel contribution beyond characterizing a known property?" is not fully answered.
**Why it matters**: For *Digital Signal Processing*, the contribution must go beyond characterization of known phenomena. The 7.6 percentage-point improvement (92.4% → 100.0%) and the BER implications need stronger framing as a contribution.
**Suggestion**: Strengthen the introduction to position the contribution as: (1) the first quantification of error concentration's BER impact in channel estimation, (2) the demonstration that learned parameters provide a 379× improvement over fixed-threshold ISTA, and (3) the AMP-theoretic interpretation connecting W^(k) to Onsager correction. Consider adding a "Contribution Summary" paragraph in Section 1.
**Severity**: Major

### W2: AMP Theory Connection Remains Speculative
**Problem**: The discussion of W^(k) as an implicit Onsager correction (Section 5.1) is interesting but unsubstantiated. The authors themselves note "we have not empirically validated this by comparing W^(k) against the theoretical Onsager correction matrix" (Section 5.1). This speculative framing weakens the theoretical contribution.
**Why it matters**: Claims about connections to established theory (AMP) require either empirical validation or formal proof. Without either, the connection remains a hypothesis.
**Suggestion**: Either (a) add an experiment comparing W^(k) against the theoretical Onsager correction matrix, or (b) significantly weaken the framing to clearly label this as a hypothesis for future work, removing it from the abstract and highlights.
**Severity**: Major

### W3: Missing Deep Learning Baselines in Main Text
**Problem**: The paper compares against OMP, LASSO, FISTA, LMS, NLMS but not against CNN or Transformer baselines in the main experiments. The CNN comparison appears only in Section 4.10 as a supplementary experiment. The related work section (Section 2.3) extensively discusses CNN and Transformer methods but the paper does not compare against them.
**Why it matters**: The readership of *Digital Signal Processing* would expect comparison against representative deep learning baselines, especially since the paper claims LISTA is a deep learning method.
**Suggestion**: Move the CNN baseline to the main comparison table (Table 1) or explicitly justify its placement as a supplementary experiment. Consider adding a brief Transformer baseline or citing a fair comparison from the literature.
**Severity**: Minor

### W4: Scalability Concerns Not Fully Addressed
**Problem**: The paper shows LISTA training diverges at N=256 (Table 5) and requires M/N ≥ 2 for stable operation (Table 6). However, the proposed solutions (structured linear mappings) are mentioned only in passing without implementation or analysis.
**Why it matters**: For practical deployment, scalability to N ≥ 128 is important for wideband systems. The O(N^2) parameter scaling is a fundamental limitation that deserves deeper treatment.
**Suggestion**: Add a brief analysis of structured mapping alternatives (Toeplitz, low-rank) with parameter count estimates, even if full implementation is deferred to future work.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title accurately reflects the paper's content. "Systematic Analysis" is appropriate given the breadth of experiments.
- The abstract is dense but well-structured. The central finding (100.0% ± 0.0% error concentration) is prominently placed. The abstract honestly notes LISTA's NMSE limitations.
- The highlights section effectively summarizes key contributions.

### Introduction
- The six contributions are clearly enumerated. However, contribution (1) could be strengthened by more explicitly stating what is novel about the analysis versus prior LISTA work.
- The research gap is well-articulated: prior work focused on NMSE performance without understanding the error structure.

### Literature Review / Theoretical Framework
- Comprehensive coverage of deep unfolding, sparse channel estimation, and deep learning for channel estimation. The hardware deployment subsection is a nice addition.
- The positioning relative to LISTA-CP, OCLISTA, LISTA-AMP, and ALISTA is appropriate.

### Methodology / Research Design
- The experimental design is sound: mixed-SNR training, grid-searched baselines, multiple seeds, statistical testing.
- The LISTA architecture description (Section 3.3) is clear and standard.
- The loss function discussion (NMSE, scale-invariant) is important for understanding the saturation.

### Results / Findings
- Tables are well-formatted and results are clearly presented.
- The pilot ratio analysis (Table 6) and channel length analysis (Table 5) provide practical insights.
- The SNR mitigation experiment (Table 9) is valuable for practitioners.

### Discussion
- The discussion is thorough, covering performance comparison, deep learning baselines, generalization, and limitations.
- The "When is ZF equalization relevant?" discussion (Section 5.1) is well-reasoned.
- The AMP theory discussion needs tightening (see W2).

### Conclusion
- The conclusion accurately summarizes findings without overclaiming. The FISTA comparison is appropriately highlighted.
- Future work directions are reasonable and specific.

---

## Questions for Authors

1. The abstract claims LISTA's error concentration is "a learned property enhanced by W^(k)." Given that ISTA achieves 92.4% with fixed thresholds, can you quantify more precisely what fraction of the 7.6 percentage-point improvement is attributable to W^(k) versus the learned threshold schedule? The ablation (Table 10) shows threshold is dominant (+14.44 dB) while W^(k) contributes +1.24 dB—does this imply the threshold schedule drives most of the 92.4% → 100.0% improvement?

2. The pre-thresholding analysis (Table 7) shows 68.3% concentration before thresholding. Can you clarify whether this 68.3% is for the *last* layer's intermediate representation? If so, how does the concentration evolve across layers? A per-layer analysis would strengthen the mechanistic understanding.

3. For the complex-valued extension (Appendix A), the error concentration drops from 100.0% to 97.8%. Is this difference statistically significant given 5 seeds? The paper reports 97.8% ± 0.3% but does not report the corresponding test for the real case (100.0% ± 0.0%).

---

## Minor Issues

### Language / Grammar
- Section 4.3, p. 8: "The channel-length training distribution is narrower and more focused" — consider "more constrained" for precision.
- Section 5.1, p. 16: "we hypothesize that these variants would exhibit similar saturation" — this is stated as opinion; consider "we conjecture" for academic register.

### Figures and Tables
- Table 1: The footnote about FISTA convergence could be shortened.
- Table 6: The multiple footnotes are somewhat cluttered; consider consolidating.
- Figure captions could include the key numerical result (e.g., "LISTA saturates at −25 dB").

### Layout
- The paper is well-formatted for the CAS template. No layout issues noted.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | Error concentration characterization is novel in channel estimation context, but closely related to known soft-thresholding properties |
| Methodological Rigor (25%) | 82 | Strong | Comprehensive experiments with statistical validation, ablation, and multiple baselines; minor gaps in power analysis |
| Evidence Sufficiency (25%) | 85 | Strong | Multiple experiments, seeds, statistical tests, effect sizes; FISTA and CNN baselines added |
| Argument Coherence (15%) | 80 | Strong | Clear narrative from NMSE limitation → error concentration → BER advantage; AMP connection weakens coherence slightly |
| Writing Quality (15%) | 83 | Strong | Clear, professional prose; honest reporting; minor verbose passages |
| **Weighted Average** | **79.6** | **Minor Revision** | |

---

*Report submitted by EIC, Digital Signal Processing*
