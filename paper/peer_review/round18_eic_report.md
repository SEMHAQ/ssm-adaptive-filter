# Peer Review Report — EIC (Round 18)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-ROUND18
- **Review Date**: 2026-06-01
- **Review Round**: Round 18

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), *Digital Signal Processing* (Elsevier)

### Reviewer Identity
Prof. Maria Rodriguez, Editor-in-Chief of *Digital Signal Processing*. 20+ years of editorial experience in sparse signal processing, deep unfolding architectures, and adaptive signal processing.

### Review Focus
Journal fit, originality, significance to the DSP readership, coherence of the contribution narrative, and whether the paper advances the field.

---

## Overall Assessment

### Recommendation
- [x] **Accept**
- [ ] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
5

### Summary Assessment
This manuscript presents a systematic analysis of LISTA for sparse channel estimation, with contributions centered on quantifying error concentration on true tap locations and its BER implications. The revised manuscript (Round 18) substantially improves over the previous round: the contributions are now clearly framed as "quantifying and contextualizing" rather than "discovering," the AMP theory connection is appropriately hedged, and a new threshold function comparison experiment (Section 4.13) provides genuinely novel insight. The threshold comparison—showing hard thresholding outperforms soft by 7.1 dB (p < 0.001) within the same LISTA architecture—is a substantive finding that strengthens the paper's originality beyond mere characterization. The experimental methodology is comprehensive (20-seed ablation, Holm–Bonferroni correction, Cohen's d, 200 realizations for BER), the writing is professional, and the honest reporting of LISTA's limitations (NMSE saturation, FISTA superiority) is commendable. This paper is ready for publication.

---

## Strengths

### S1: Clear, Honest Contribution Framing
The revised Section 1 explicitly states "we do not claim to discover this phenomenon" and lists four focused contributions. This framing eliminates the overclaiming critique and positions the work accurately as quantification and contextualization.

### S2: Threshold Comparison Experiment (New)
The threshold function comparison (Section 4.13) is a significant addition. The 7.1 dB advantage of hard thresholding over soft (p < 0.001, d = 30.3) demonstrates that LISTA's learned threshold schedule adapts the thresholding behavior, not just parameters. This goes beyond characterization.

### S3: Comprehensive Statistical Methodology
20-seed ablation with Holm–Bonferroni correction, Cohen's d effect sizes, paired t-tests, 95% CIs in main tables. The statistical rigor exceeds typical DSP journal standards.

### S4: Honest Limitation Reporting
The paper consistently reports LISTA's limitations: NMSE saturation at −25 dB, FISTA superiority by 1–27 dB, theoretical-only hardware analysis. This honesty strengthens credibility.

### S5: Practical Deployment Framework
Section 5.3 provides an actionable decision framework for practitioners. The SNR-specific training results (−31 dB) and pilot ratio analysis (M/N ≥ 2) have immediate practical value.

---

## Weaknesses

### W1: Threshold Comparison Seeding
**Problem**: The threshold comparison (Table 13) uses 5 seeds but reports 4 convergent seeds (1 diverged per variant). With n=4, the statistical power is limited.
**Why it matters**: The large effect sizes (d=30.3) compensate, but n=4 is at the minimum for parametric tests.
**Suggestion**: Run with 10 seeds to confirm the results with more convergent samples.
**Severity**: Minor

### W2: Hard Thresholding Gradient Estimation
**Problem**: Hard thresholding uses a straight-through gradient estimator, which is an approximation. The paper acknowledges this in a footnote but does not discuss the implications.
**Why it matters**: The straight-through estimator may bias the learned parameters. The 7.1 dB advantage could partly reflect the gradient approximation rather than the thresholding function itself.
**Suggestion**: Add a brief discussion of the straight-through estimator's limitations and potential impact.
**Severity**: Minor

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 76 | Strong | Threshold comparison adds genuine novelty; honest framing strengthens contribution |
| Methodological Rigor (25%) | 85 | Strong | 20-seed ablation, Holm–Bonferroni, CIs, comprehensive baselines |
| Evidence Sufficiency (25%) | 86 | Strong | Multiple experiments, seeds, baselines, statistical tests |
| Argument Coherence (15%) | 84 | Strong | Clear 4-contribution structure; AMP appropriately hedged |
| Writing Quality (15%) | 85 | Strong | Professional, honest, well-structured |
| **Weighted Average** | **83.4** | **Accept** | |

---

*Report submitted by EIC, Digital Signal Processing*
