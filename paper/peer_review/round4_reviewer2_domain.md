# Peer Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 4

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain Expert)

### Reviewer Identity
Prof. Dr. Xiaohan Chen, Associate Professor of Signal Processing, Zhejiang University. Expertise in sparse channel estimation, compressed sensing for communications, and deep learning-based receiver design. Author of 20+ papers on CS-based channel estimation and LISTA variants. Deep familiarity with the theoretical foundations of LISTA, OMP, LASSO, and their communication-theoretic implications.

### Review Focus
Literature coverage completeness, theoretical framework appropriateness, domain contribution significance, and positioning within the sparse channel estimation and deep unfolding literatures. I assess whether the paper advances the field or merely applies known techniques to a known problem.

---

## Overall Assessment *

### Recommendation *
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score *
5 — Completely within my area of expertise. Sparse channel estimation and LISTA are my primary research areas.

### Summary Assessment *
This paper applies the standard LISTA architecture to sparse channel estimation and provides a comprehensive evaluation including BER validation, ablation studies, generalization analysis, and hardware complexity. The domain contribution is mixed: the BER-NMSE disconnect finding is genuinely insightful and advances our understanding of how deep-unfolded estimators behave in communication systems. The ablation study with 20 seeds provides definitive evidence about component contributions. However, the paper does not propose any architectural novelty—it applies the 2010 LISTA architecture without modification—and the comparison against recent LISTA variants is limited to LISTA-CP, which turns out to be identical.

The literature review is comprehensive and well-organized, covering deep unfolding, channel estimation, and hardware deployment. The positioning against CNN/Transformer methods is appropriate. However, the paper misses some key recent works on LISTA variants and convergence analysis that would strengthen the theoretical grounding. The domain contribution is sufficient for *Digital Signal Processing* but would be insufficient for a top-tier venue like IEEE TSP or IEEE JSAC.

---

## Strengths *

### S1: Comprehensive Literature Positioning
The Related Work section (Section 2) provides excellent coverage of four distinct areas: sparse channel estimation, deep unfolding, deep learning for channel estimation, and classical adaptive filtering. The classification of deep learning methods into CNN-based, Transformer-based, and model-driven categories (Section 2.3) is well-organized. The explicit positioning against prior work (end of Section 2.3) clearly articulates the paper's differentiation.

### S2: BER-NMSE Disconnect Provides New Domain Insight
The finding that LISTA achieves comparable or better BER despite 13–33 dB worse NMSE is a genuine contribution to the sparse channel estimation domain. The mechanism analysis (Section 4.12) showing 99.9% error concentration on true taps provides a new perspective on what makes a channel estimator "good" for communications—it is not just NMSE but the error structure that matters. This insight has implications beyond LISTA for how we evaluate channel estimators in general.

### S3: Fair Comparison with Oracle-K OMP
The paper uses OMP with known sparsity K (oracle setting), which is the strongest possible OMP configuration. Despite this advantage, LISTA achieves comparable BER. This fair comparison strengthens the practical case for LISTA, which does not require K.

### S4: ITU Channel Model Validation
Testing on ITU PedA and VehA models (Section 4.7) with baselines tuned on Gaussian data (no re-optimization) is the correct deployment scenario. The finding that LISTA generalizes to ITU channels with comparable NMSE (−23 to −27 dB) is practically important.

---

## Weaknesses *

### W1: No Comparison with Recent LISTA Variants Beyond LISTA-CP
**Problem**: The paper compares against LISTA-CP [Chen et al. 2019] but not against OCLISTA [Borgerding 2020], LISTA-AMP [Liu 2023], or ISTA-Net [He 2019]. The LISTA-CP comparison yields identical results, providing no information about whether improved LISTA variants could break the −25 dB saturation.
**Why it matters**: The deep unfolding field has evolved significantly since 2010. OCLISTA uses Onsager correction for improved convergence; LISTA-AMP bridges deep unfolding and approximate message passing. These variants may achieve better NMSE than standard LISTA, and the saturation phenomenon may be specific to the basic architecture.
**Suggestion**: (1) Add at least a brief comparison with OCLISTA or LISTA-AMP. (2) If experiments are infeasible, discuss qualitatively why the saturation might or might not affect these variants. (3) Cite and discuss the convergence guarantees of LISTA-CP and OCLISTA in the context of the observed saturation.
**Severity**: Major

### W2: Theoretical Analysis of NMSE Saturation Is Insufficient
**Problem**: The paper attributes the −25 dB saturation to three factors (Section 5.1) but provides no formal analysis. The claim about "scale-invariant loss" is intuitive but unsubstantiated. The paper does not connect to the theoretical convergence analysis of LISTA [Chen et al. 2019, Liu et al. 2023] which provides bounds on approximation error.
**Why it matters**: Without theoretical grounding, the saturation appears as an empirical observation without explanation. The deep unfolding community has developed theoretical tools (proximal operator theory, fixed-point analysis) that could provide insight.
**Suggestion**: (1) Provide a simple analysis: for the soft-thresholding operator with threshold θ, the estimation error has a bias floor of θ/2 for taps below θ. (2) Connect to LISTA convergence theory: the approximation error of a fixed-depth LISTA network scales as O(ρ^L) where ρ < 1 is the contraction rate—discuss how this relates to the observed saturation. (3) If formal analysis is infeasible, cite and discuss the relevant theoretical results more explicitly.
**Severity**: Major

### W3: Sparse Channel Model Is Simplistic
**Problem**: The paper uses i.i.d. Gaussian tap amplitudes with uniform random locations (Section 4.1). Real wireless channels have correlated tap amplitudes (exponential PDP), clustered arrivals, and frequency-dependent attenuation. The ITU model validation partially addresses this, but the training data does not reflect realistic channel statistics.
**Why it matters**: The generalization from i.i.d. Gaussian to ITU channels is a significant distribution shift. The paper's claim that "LISTA generalizes across channel types" may be overstated—the ITU results show comparable but not necessarily optimal performance.
**Suggestion**: (1) Acknowledge that the i.i.d. Gaussian model is a simplification. (2) Consider training on a mixture of Gaussian and ITU-like channels to assess whether channel-specific training improves performance. (3) Discuss the implications of the distribution shift for practical deployment.
**Severity**: Minor

### W4: Missing Comparison with Structured LISTA Variants
**Problem**: The paper identifies O(N²) per-layer complexity as a scalability limitation (Section 3.4) and suggests structured linear mappings as a solution, but does not evaluate any structured variant. The scaling analysis (Table 13) shows 1.3M parameters at N=256, but no structured alternative is tested.
**Why it matters**: Structured LISTA variants (Toeplitz, circulant, low-rank) have been proposed in the literature. Without at least a preliminary evaluation, the scalability concern remains theoretical.
**Suggestion**: (1) Add a brief experiment with a structured W^(k) (e.g., circulant or low-rank) at N=256 to demonstrate feasibility. (2) If experiments are infeasible, provide a more detailed discussion of which structured variants are most promising and why.
**Severity**: Minor

---

## Detailed Comments *

### Title & Abstract
- Title accurately reflects the paper's content. "Analysis" is appropriate given the evaluative nature.
- Abstract is comprehensive. The BER finding is appropriately highlighted.
- Keywords are appropriate and cover the key topics.

### Introduction
- The motivation is well-articulated with clear references to the sparse channel estimation literature.
- The gap identification is precise: no systematic BER validation of LISTA for channel estimation.
- The contribution list should be consolidated from 6 to 3–4 items.

### Literature Review
- Excellent coverage of four distinct areas.
- The positioning against CNN/Transformer methods is well-done.
- Missing: recent convergence analysis works [Chen 2019, Liu 2023] and OCLISTA [Borgerding 2020].
- The classical adaptive filtering subsection (Section 2.4) is appropriate but could cite PNLMS variants more extensively.

### Methodology
- The LISTA architecture is standard and clearly described.
- The FFT-based convolution implementation (Section 3.3) is a practical detail that enhances reproducibility.
- The parameter analysis (Section 3.4) correctly identifies the O(N²) scaling issue.

### Results
- Experiment 1 (NMSE vs SNR): Well-executed. The saturation analysis is the key finding.
- Experiment 5 (Ablation): The 5→20 seed progression is methodologically sound.
- Experiment 8 (LISTA-CP): The identical result is interesting but limits the comparison value.
- Experiment 10 (BER): The statistical validation is exemplary for the domain.
- Experiment 12 (Mechanism): The error sparsity analysis provides genuine domain insight.

### Discussion
- The limitations section is honest and comprehensive.
- The deployment recommendations are practical and well-reasoned.
- The future research directions are relevant and actionable.

### References
- Comprehensive coverage of deep unfolding, channel estimation, and hardware literature.
- Missing: OCLISTA [Borgerding 2020] should be discussed in the context of LISTA variants.
- The ITU reference [itut2017guidelines] is appropriate.

---

## Questions for Authors *

1. **LISTA variants**: Have you considered comparing against OCLISTA or LISTA-AMP? Do you expect the saturation phenomenon to persist with these improved architectures?
2. **Theoretical grounding**: Can you connect the observed −25 dB saturation to the LISTA convergence theory? Specifically, what is the contraction rate ρ for your configuration, and does O(ρ^L) predict the observed saturation level?
3. **Channel model**: The i.i.d. Gaussian tap model is a simplification. Have you tested whether training on ITU-like channels (with exponential PDP) improves performance on ITU test channels?
4. **LISTA-CP weight clipping**: You report that the weight clipping constraint is inactive (max ‖W^(k) − I‖₂ = 0.34). Does this mean LISTA-CP provides no practical benefit over standard LISTA in this setting?

---

## Minor Issues

### Citation Format
- Reference [chen2018lista]: The bib key says 2018 but the year field says 2019. The CVPR workshop paper was indeed 2019. Correct the key.
- Reference [borgerding2020ista]: This is the OCLISTA paper. It should be discussed in the main text, not just listed in references.

### Figures and Tables
- Table 7 footnote: "Pilot ratio M/N varies" — this is helpful but should be more prominent in the main text discussion.
- Figure 2 (NMSE vs Sparsity): The K=15 divergence should be more visually distinct (e.g., different marker).

### Layout
- No significant layout issues.

---

## Dimension Scores *

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 62 | Adequate | BER-NMSE disconnect is novel; no architectural contribution |
| Methodological Rigor (25%) | 74 | Adequate | Good practices; some theoretical gaps |
| Evidence Sufficiency (25%) | 76 | Strong | Comprehensive experiments; missing LISTA variant comparisons |
| Argument Coherence (15%) | 75 | Strong | Clear narrative; some overgeneralization |
| Writing Quality (15%) | 78 | Strong | Professional and well-organized |
| Literature Integration | 68 | Adequate | Good coverage but missing recent LISTA convergence works |
| **Weighted Average** | **72.6** | **Minor Revision** | |
