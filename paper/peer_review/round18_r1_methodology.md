# Peer Review Report — R1 Methodology (Round 18)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation
- **Manuscript ID**: DSP-2026-ROUND18
- **Review Date**: 2026-06-01
- **Review Round**: Round 18

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology Expert

### Reviewer Identity
Dr. Kai Zhang, Associate Professor at ETH Zürich. Expertise in deep unfolding theory, optimization algorithms for sparse recovery, and statistical methodology.

### Review Focus
Research design rigor, statistical validity, reproducibility, and ablation study design.

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
The Round 18 revision addresses all methodological concerns from the previous round. The contributions are now clearly framed (Section 1), 95% CIs are added to main tables, edge-case footnotes clarify the error concentration metric, and a new threshold comparison experiment provides novel insight. The statistical methodology is rigorous throughout: 20-seed ablation with Holm–Bonferroni correction, Cohen's d effect sizes, paired t-tests for BER comparisons. The threshold comparison (hard thresholding outperforms soft by 7.1 dB, d=30.3) is a well-designed controlled experiment that isolates the thresholding function as the independent variable. The paper is ready for publication.

---

## Strengths

### S1: Threshold Comparison as Controlled Experiment
The threshold comparison (Section 4.13) is methodologically clean: same LISTA architecture, same training protocol, same seeds, only the thresholding function varies. This isolates the independent variable effectively. The large effect sizes (d=30.3, 13.1) leave no doubt about statistical significance.

### S2: 95% CIs Added to Main Tables
Tables 1–3 now include 95% confidence intervals for LISTA rows, enabling readers to assess precision. The half-width ranges in footnotes are a practical addition.

### S3: Edge-Case Metric Clarification
The footnote in Table 8 clarifies that LISTA's 100.0% arises from genuinely zero non-support error (0.01% ± 0.01%), not from the zero-total-error convention. This resolves the metric ambiguity.

### S4: Contribution Framing
The revised Section 1 explicitly states "we do not claim to discover" and lists 4 focused contributions. This is methodologically honest and positions the work accurately.

---

## Weaknesses

### W1: Threshold Comparison Seed Count
**Problem**: 5 seeds attempted, 4 converged. With n=4, the t-test has 3 degrees of freedom.
**Why it matters**: The large effect sizes (d=30.3) compensate, but n=4 is minimal.
**Suggestion**: Run with 10 seeds to get ≥8 convergent samples.
**Severity**: Minor

### W2: Straight-Through Gradient for Hard Thresholding
**Problem**: Hard thresholding is non-differentiable at |z|=θ. The straight-through estimator passes gradients through as if the mask were identity.
**Why it matters**: This approximation may affect learned parameter quality. The 7.1 dB advantage should be interpreted with this caveat.
**Suggestion**: Acknowledge this limitation explicitly in the discussion.
**Severity**: Minor

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 76 | Strong | Threshold comparison is genuinely novel |
| Methodological Rigor (25%) | 86 | Strong | Comprehensive statistical testing; clean experimental design |
| Evidence Sufficiency (25%) | 86 | Strong | Multiple experiments, seeds, baselines |
| Argument Coherence (15%) | 84 | Strong | Clear contribution structure; AMP hedged |
| Writing Quality (15%) | 85 | Strong | Professional, honest |
| **Weighted Average** | **83.6** | **Accept** | |

---

*Report submitted by Reviewer 1 (Methodology)*
