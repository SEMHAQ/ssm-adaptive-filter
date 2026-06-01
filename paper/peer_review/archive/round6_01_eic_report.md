# Peer Review Report — EIC

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 6

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (Associate Editor)

### Reviewer Identity
Prof. Elena Marchetti, Associate Editor, *Digital Signal Processing* (Elsevier). Expertise in model-based deep learning for signal processing and algorithm-hardware co-design.

### Review Focus
Journal fit, overall contribution significance, clarity of presentation, and whether the paper advances the state of the art sufficiently for the DSP readership. I assess whether the paper bridges theory and practice effectively.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Accept**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
4 — The paper's core topic (deep unfolding for channel estimation) is well within my editorial scope. Hardware complexity analysis is slightly outside my primary expertise, but I am confident in the overall assessment.

### Summary Assessment
This paper presents a systematic analysis of LISTA (Learned ISTA) for sparse channel estimation, covering NMSE performance, BER validation with statistical rigor, ablation studies, generalization across channel models, and hardware complexity analysis. The paper is well-structured and addresses a relevant topic for the DSP community: understanding when and why deep-unfolded architectures are practical alternatives to classical sparse recovery methods.

The paper's strongest contribution is the BER-NMSE mechanism analysis (Section 4.12), which explains why LISTA's NMSE saturation does not translate to a BER penalty under ZF equalization. This is a genuinely insightful finding with practical implications. The ablation study with 20 seeds and proper statistical testing (paired t-tests, Cohen's d) is methodologically sound and addresses prior concerns about statistical power.

However, the paper has notable weaknesses: (1) the originality claim is somewhat overstated — LISTA is a well-known architecture and the paper's contribution is more analytical than algorithmic; (2) some comparisons are only against classical baselines (OMP, LASSO, LMS/NLMS) without including recent deep learning methods; (3) the hardware complexity claims rely on theoretical analysis rather than measured results. These issues are addressable and do not fundamentally undermine the paper's value.

I recommend Minor Revision. The paper provides a useful reference for the community on the practical characteristics of LISTA for channel estimation, with unusually thorough statistical validation.

---

## Strengths

### S1: Rigorous Statistical Validation of BER Claims
The BER experiments use 200 channel realizations per SNR point with 5 random seeds, paired t-tests, and 95% confidence intervals (Section 4.10). This level of statistical rigor is uncommon in the deep learning for communications literature and significantly strengthens the central BER claims. The explicit reporting of p-values and significance levels (Tables 7–9) allows readers to independently assess the evidence.

### S2: Insightful BER-NMSE Mechanism Analysis
The mechanism analysis (Section 4.12) is the paper's most valuable contribution. The finding that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP), resulting in 50× less non-support error and 1.8× lower noise enhancement, provides a clear and actionable explanation for the BER-NMSE disconnect. This insight is non-obvious and has practical implications for algorithm selection in communication systems.

### S3: Comprehensive Ablation with Proper Power
The 20-seed ablation study (Section 4.11) with paired t-tests and Cohen's d effect sizes correctly identifies the per-layer threshold schedule as the dominant contributor (+14–18 dB degradation). The paper honestly acknowledges that the initial 5-seed ablation produced false negatives due to low statistical power — this transparency is commendable and strengthens credibility.

### S4: Honest Treatment of Limitations
The paper does not oversell LISTA's capabilities. The NMSE saturation at −25 dB, the divergence at N=256, and the ZF-specificity of the BER advantage are all clearly stated. The Discussion section (Section 5.3) provides an honest assessment of limitations. This balanced presentation is appropriate for a methods-oriented journal like DSP.

### S5: Practical Deployment Framework
The decision framework in Section 5.2 (speed-critical → LISTA, known SNR → SNR-specific training, high NMSE → OMP/LASSO) provides actionable guidance for practitioners. The hardware complexity analysis with FLOPs, parallelism characteristics, and memory access patterns (Section 4.13) complements the algorithmic contribution.

---

## Weaknesses

### W1: Limited Novelty in the Architecture Itself
**Problem**: LISTA is a well-known architecture (Gregor & LeCun, 2010), and the paper applies it to channel estimation without architectural modifications. The contribution is analytical (understanding behavior) rather than algorithmic (new method). The title says "Analysis of Deep-Unfolded LISTA" which is accurate, but the abstract and introduction sometimes imply a stronger contribution.
**Why it matters**: DSP readers may expect more than an analysis paper. The novelty lies in the systematic evaluation methodology (BER validation, ablation, mechanism analysis) rather than in a new algorithm.
**Suggestion**: Strengthen the positioning as an analytical/contributions paper. Explicitly state in the abstract that the contribution is "a systematic analysis framework for evaluating deep-unfolded architectures" rather than implying algorithmic novelty. Consider adding a brief comparison with LISTA-CP, OCLISTA, and LISTA-AMP in the abstract to show awareness of variants.
**Severity**: Minor

### W2: Missing Comparisons with Recent DL Channel Estimation Methods
**Problem**: The baselines (Section 4.1) include only classical methods (LMS, NLMS, OMP, LASSO). Recent deep learning approaches (CNN-based, Transformer-based) are discussed in Section 2.3 but not compared experimentally. Table 1 in Section 2.3 lists several methods (Ye et al., Gao et al., Zhang et al.) that could serve as additional baselines.
**Why it matters**: Without comparisons to recent DL methods, readers cannot assess whether LISTA is competitive with the current state of the art. A CNN or Transformer baseline would clarify LISTA's relative position.
**Suggestion**: Add at least one CNN-based baseline (e.g., a 1D-CNN for channel estimation) to the comparison. If computational resources are limited, at least discuss qualitatively why LISTA's advantages (interpretability, fixed computation, hardware-friendliness) justify its use despite potentially lower accuracy than black-box DL methods.
**Severity**: Major

### W3: Hardware Claims Lack Measured Results
**Problem**: Section 4.13 provides theoretical FLOPs analysis and pipelining estimates (4.4× throughput advantage), but no measured FPGA or ASIC results. The 1.2 μs throughput estimate is based on assumptions (64 DSP units at 500 MHz) that may not reflect real implementations.
**Why it matters**: Hardware complexity claims are a key selling point of the paper (abstract highlights "4.4× hardware throughput advantage"). Without measured results, these claims are aspirational rather than demonstrated.
**Suggestion**: Either (a) tone down the hardware claims to "theoretical analysis suggests" rather than "enables 4.4× throughput advantage," or (b) provide at least a reference implementation (e.g., HLS code or pseudo-RTL) that validates the estimates. The citation of Wei et al. (2022) helps, but the paper's specific architecture (with W^(k) matrices) differs from that reference.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is accurate and descriptive. "Analysis" correctly positions the contribution.
- Abstract is comprehensive but dense (350+ words). Consider condensing the statistical details (200 realizations, 5 seeds, p-values) to improve readability — these belong in the methods section, not the abstract.
- The abstract's claim of "4.4× hardware throughput advantage" should be qualified as theoretical.

### Introduction
- Well-structured with clear enumeration of 6 contributions.
- Contribution 1 (NMSE saturation analysis) and Contribution 2 (BER validation) are the strongest. Contribution 6 (hardware complexity) is weakest due to lack of measured results.
- The research gap is clearly articulated: prior work either claims novelty without understanding, or applies LISTA without systematic analysis.

### Literature Review
- Comprehensive coverage of sparse channel estimation, deep unfolding, and DL for channel estimation.
- The categorization (CNN-based, Transformer-based, model-driven, surveys) is helpful.
- Missing: comparison with recent learned denoising-based methods (e.g., Learned AMP, denoising score matching for sparse recovery).

### Methodology
- Problem formulation (Section 3.1) is standard and clear.
- LISTA architecture (Section 3.2) follows the standard formulation with appropriate citations.
- Training details (Section 3.5) are well-specified: Adam optimizer, cosine annealing, gradient clipping.
- The mixed-SNR training protocol is well-justified for producing a single model across conditions.

### Results
- 13 experiments with clear structure. Each experiment addresses a specific question.
- Tables and figures are well-designed. The inclusion of p-values and effect sizes is commendable.
- The cross-table consistency note (Section 4.3) is unusually transparent and helpful.

### Discussion
- Section 5.1 provides good insight into the SNR saturation mechanism.
- The deployment framework (Section 5.2) is practical and actionable.
- Limitations (Section 5.3) are honestly stated.

### References
- Bibliography is comprehensive (40+ references) and reasonably current.
- Missing some 2024–2025 papers on learned channel estimation.

---

## Questions for Authors

1. The abstract claims "4.4× hardware throughput advantage over OMP on FPGA." Given that this is a theoretical estimate based on 64 DSP units at 500 MHz, should this claim be softened to "theoretical analysis suggests 4.4× throughput advantage" in the abstract and highlights?

2. Have you considered comparing against a simple CNN baseline (e.g., 1D-CNN with comparable parameter count) to position LISTA relative to black-box deep learning methods? Even a brief comparison would strengthen the paper.

3. The NMSE saturation at −25 dB is attributed to "scale-invariant training loss" and "broad SNR range." Could you provide a more formal analysis of why the saturation occurs at this specific level? Is −25 dB related to the channel parameters (N=64, K=5) or is it a property of the architecture?

---

## Minor Issues

### Language / Grammar
- Abstract: "LISTA's NMSE saturates at approximately −25 dB for SNR ≥ 10 dB" — consider "for SNR ≥ 10 dB" → "when SNR ≥ 10 dB" for clarity.
- Section 4.10: "200 independent channel realizations per SNR point (increased from 50 in the initial study)" — the parenthetical is helpful but could be moved to a footnote.

### Figures and Tables
- Table 1 (NMSE vs SNR): The bold formatting is inconsistent — LISTA is bolded in some rows but not others.
- Figure 1 (NMSE vs SNR): Consider adding a horizontal dashed line at −25 dB to visually highlight the saturation level.

### Layout
- The paper is 25+ pages in the CAS template, which is long for DSP. Consider whether some experiments (e.g., Experiment 3 channel length, Experiment 8 LISTA-CP) could be moved to a supplementary document.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 58 | Weak | LISTA is well-known; contribution is analytical rather than algorithmic. The BER-NMSE mechanism analysis is novel. |
| Methodological Rigor (25%) | 78 | Strong | Excellent statistical validation (20 seeds, paired t-tests, Cohen's d). Missing DL baselines and measured hardware results. |
| Evidence Sufficiency (25%) | 75 | Strong | 13 experiments with comprehensive coverage. BER validation is thorough. Missing comparison with recent DL methods. |
| Argument Coherence (15%) | 82 | Strong | Clear logical flow from problem → method → experiments → mechanism → deployment. Well-structured. |
| Writing Quality (15%) | 72 | Adequate | Generally clear and professional. Some dense passages in the abstract and mechanism analysis. |
| Literature Integration (optional) | 68 | Adequate | Good coverage of sparse recovery and deep unfolding literature. Missing some 2024–2025 DL channel estimation papers. |
| Significance & Impact (optional) | 65 | Adequate | Useful reference for practitioners, but impact limited by lack of architectural novelty. |
| **Weighted Average** | **72.3** | **Minor Revision** | |

---

**Decision**: Minor Revision — The paper provides a thorough and honest analysis of LISTA for channel estimation with strong statistical validation. The BER-NMSE mechanism analysis is a genuine contribution. Issues (missing DL baselines, hardware claims) are addressable.
