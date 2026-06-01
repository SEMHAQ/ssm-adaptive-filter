# Peer Review Report — Reviewer 2 (Domain Expert)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 3

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert (Sparse Channel Estimation & Compressed Sensing)

### Reviewer Identity
Prof. Li Wei, Full Professor, Department of Electronic Engineering, Tsinghua University. Expertise in compressed sensing for wireless communications, sparse channel estimation, and pilot design for OFDM systems. Published extensively on OMP-based and LASSO-based channel estimation. Focus: literature completeness, theoretical positioning, domain contribution, and practical relevance to the communications community.

### Review Focus
Literature coverage and positioning, theoretical framework appropriateness, domain-specific contribution, missing references, and whether the findings advance the state of the art in sparse channel estimation.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — Sparse channel estimation is my primary research area. I am confident in my assessment of the domain contribution and literature positioning.

### Summary Assessment
This manuscript provides a thorough empirical evaluation of LISTA for sparse channel estimation, covering performance, generalization, ablation, and practical deployment. The literature review is comprehensive, covering compressed sensing, deep unfolding, and deep learning for channel estimation. The paper's key contribution is the BER analysis showing that LISTA's NMSE disadvantage does not translate to BER penalty, and the ablation study identifying the per-layer threshold schedule as the dominant learned component.

The main domain-specific concern is the limited scope of the channel model evaluation: all primary experiments use i.i.d. Gaussian taps, and only two ITU models are tested. Real wireless channels exhibit more complex structures (correlated taps, time variation, frequency selectivity). Additionally, the paper does not discuss the relationship between pilot overhead and estimation quality in sufficient depth—a critical practical consideration. The positioning against recent deep learning methods (Transformers, CNNs) could be sharper. These issues are addressable and the paper is suitable for DSP with minor revisions.

---

## Strengths

### S1: Comprehensive Baseline Comparison with Fair Tuning
The paper compares LISTA against LMS, NLMS, OMP, and LASSO with grid-searched hyperparameters (Section 4.1). This is the correct approach—many papers compare against poorly tuned baselines, making the comparison unfair. The use of oracle K for OMP is noted and appropriate (it gives OMP an advantage, making LISTA's competitive BER even more noteworthy).

### S2: ITU Channel Model Evaluation
The inclusion of ITU PedA and VehA channel models (Section 4.7.2) is important for practical relevance. The finding that LISTA trained on i.i.d. Gaussian data achieves comparable performance on ITU channels (−23 to −27 dB) demonstrates reasonable cross-distribution generalization. The honest reporting that baselines use the same hyperparameters (no re-optimization for ITU) strengthens the comparison.

### S3: LISTA-CP Comparison with Diagnostic Insight
The comparison with LISTA-CP (Section 4.8) is well-positioned within the deep unfolding literature. The diagnostic finding that the weight clipping constraint is naturally satisfied (spectral norm 0.34 < 1.0) provides genuine insight into why convergence guarantees don't translate to practical improvement in this setting.

### S4: Practical Deployment Discussion
Section 5.2 provides a clear decision framework for practitioners: when to use LISTA vs. OMP, how to handle SNR-specific training, and the speed-accuracy trade-off. This is exactly the kind of practical guidance that DSP readers value.

---

## Weaknesses

### W1: Limited Channel Model Diversity
**Problem**: The primary experiments (Sections 4.2–4.6, 4.9–4.11) all use i.i.d. Gaussian taps. The ITU evaluation (Section 4.7.2) covers only two models (PedA, VehA) at a single SNR point. Real wireless channels exhibit: (a) correlated tap amplitudes (exponential PDP), (b) time variation (Doppler), (c) frequency selectivity, (d) non-Gaussian tap distributions (e.g., Nakagami-m, Ricean).

**Why it matters**: The i.i.d. Gaussian assumption is the simplest possible channel model. The paper's conclusions about generalization may not hold for more realistic channels. The ITU results are encouraging but insufficient.

**Suggestion**: Add experiments with: (1) correlated tap channels (exponential PDP with varying decay rates); (2) at least one frequency-selective channel model beyond ITU; (3) BER results on ITU channels (currently only NMSE is reported for ITU). This would significantly strengthen the generalization claims.

**Severity**: Major

### W2: Insufficient Discussion of Pilot Overhead
**Problem**: The paper uses M=256 pilots for N=64 (pilot ratio M/N=4). The channel length experiment (Table 3) shows divergence at N=256 (M/N=1). However, the paper does not systematically study the pilot overhead vs. accuracy trade-off, which is a fundamental consideration in practical systems where pilots consume bandwidth.

**Why it matters**: In practical systems, pilot overhead directly impacts spectral efficiency. A method that requires M/N=4 may not be practical for high-rate communications. The paper should characterize LISTA's performance as a function of M/N.

**Suggestion**: Add an experiment varying M (e.g., M = 64, 128, 256, 512) for fixed N=64 and K=5, showing how LISTA's NMSE and BER degrade as pilot overhead decreases. Compare against OMP and LASSO under the same conditions.

**Severity**: Major

### W3: Positioning Against Recent Deep Learning Methods
**Problem**: The Related Work section lists CNN-based (Ye et al., Gao et al.), Transformer-based (Zhang et al., Shen et al.), and model-driven (He et al., Wei et al.) methods but does not compare against any of them experimentally. The paper only compares against classical methods (LMS, NLMS, OMP, LASSO).

**Why it matters**: Readers will wonder how LISTA compares to these alternatives. If a simple CNN achieves similar performance with less training data, LISTA's value proposition weakens.

**Suggestion**: Add at least one deep learning baseline (e.g., a simple CNN or DNN-based estimator from Ye et al., 2018). Even a brief comparison would help position LISTA within the broader landscape.

**Severity**: Minor

### W4: Missing References on LISTA for Channel Estimation
**Problem**: The paper does not cite or discuss prior work that has applied LISTA or similar deep-unfolded architectures specifically to channel estimation. While the Related Work section covers deep learning for channel estimation broadly, the specific niche of deep unfolding for channel estimation (as covered in Gao et al., 2023 survey) should be more thoroughly discussed.

**Why it matters**: If prior work has already applied LISTA to channel estimation with similar findings, the paper's novelty claim weakens.

**Suggestion**: Add a paragraph in Related Work specifically discussing prior applications of deep unfolding (not just LISTA) to channel estimation, and clearly state what this paper adds beyond those works.

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is appropriate. "Analysis" correctly signals the paper's nature.
- Abstract mentions "33× faster inference" — this is a strong practical claim that is well-supported by Table 6.

### Introduction
- The motivation for sparse channel estimation is well-established with appropriate references (Bajwa et al., Berger et al.).
- The research gap is clearly articulated: prior work lacks systematic characterization of deep unfolding for channel estimation.

### Literature Review / Theoretical Framework
- Coverage of compressed sensing (Candes, Donoho), greedy algorithms (OMP), and convex relaxation (LASSO) is comprehensive.
- Deep unfolding coverage includes seminal (Gregor & LeCun) and recent (Liu et al., 2023) works.
- The hardware deployment references (Wei et al., Kim et al.) are a nice addition.
- Missing: more specific discussion of prior deep-unfolded channel estimation work.

### Methodology / Research Design
- Data generation is well-specified and reproducible.
- The BPSK pilot signal choice is standard but could be extended to QPSK pilots for completeness.

### Results / Findings
- Table 1 (NMSE vs SNR): Clear and informative. The saturation behavior is well-demonstrated.
- Table 2 (NMSE vs sparsity): Good coverage of K=2 to 15. The K=15 divergence is noted.
- Table 4 (depth analysis): The plateau at L=10 is a useful practical finding.
- Table 7 (ITU): Encouraging results but limited to one SNR point.

### Discussion
- Section 5.1 provides good synthesis. The BER discussion is the highlight.
- Section 5.2 (deployment recommendations) is practical and well-structured.
- The future research directions in Section 5.3 are relevant and actionable.

### Conclusion
- Conclusions are well-supported. The "33× faster inference with comparable BER" summary is accurate.

### References
- 40+ references, mostly peer-reviewed, recent, and relevant. Good coverage of both classical and deep learning approaches.

---

## Questions for Authors

1. **Pilot overhead**: How does LISTA perform as a function of pilot ratio M/N? Can you provide results for M/N ∈ {1, 2, 4, 8}?

2. **ITU BER**: Can you provide BER results on ITU channels? Even a single SNR point (e.g., 20 dB) would be valuable to confirm the BER advantage holds on realistic channels.

3. **Prior deep-unfolded channel estimation**: Has LISTA or a similar architecture been applied to channel estimation before? If so, how does your analysis differ?

4. **Correlated channels**: Does LISTA's performance change when tap amplitudes are correlated (e.g., exponential PDP) rather than i.i.d.?

---

## Minor Issues

### Language / Grammar
- Section 2.3, paragraph on surveys: "Several comprehensive surveys have been published recently" — consider integrating these into the narrative rather than listing them separately.
- Section 4.7.2: "cross-distribution generalization" — this term is used loosely; consider defining it more precisely.

### Citation Format
- All citations appear consistent with Elsevier authoryear style.
- Consider adding DOIs where available (Elsevier best practice).

### Figures and Tables
- Table 7 (ITU): Only one SNR point. Consider adding SNR=10 and SNR=30 for completeness.
- Table 6 (runtime): The "Speedup vs OMP" column is helpful. Consider adding a "Speedup vs LASSO" column.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | Contribution is systematic analysis; BER finding is novel |
| Methodological Rigor (25%) | 70 | Adequate | Good experimental design; some gaps in BER and channel diversity |
| Evidence Sufficiency (25%) | 68 | Adequate | Comprehensive NMSE experiments; BER and channel model coverage limited |
| Argument Coherence (15%) | 70 | Adequate | Clear structure; BER explanation needs strengthening |
| Writing Quality (15%) | 76 | Strong | Well-written, clear, appropriate technical depth |
| Literature Integration | 70 | Adequate | Good coverage but missing some domain-specific prior work |
| **Weighted Average** | **67.6** | **Minor Revision** | |
