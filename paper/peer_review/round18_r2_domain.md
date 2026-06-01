# Peer Review Report — R2 Domain (Round 18)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation
- **Manuscript ID**: DSP-2026-ROUND18
- **Review Date**: 2026-06-01
- **Review Round**: Round 18

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert

### Reviewer Identity
Prof. Li Wei, Professor at Tsinghua University, Department of Electronic Engineering. Expertise in compressed sensing for wireless communications, sparse channel estimation, and AMP algorithms.

### Review Focus
Literature coverage, theoretical framework accuracy, domain contribution.

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
The Round 18 revision strengthens the domain contribution substantially. The threshold comparison experiment (Section 4.13) connects LISTA's learned behavior to the well-studied soft/hard/garrote thresholding literature in statistics, providing a bridge between deep unfolding and classical sparse recovery theory. The AMP connection is now appropriately hedged as "consistent with" rather than claimed as a finding. The contributions are honestly framed as quantification and contextualization. The paper's comprehensive evaluation (ITU channels, complex-valued extension, pilot ratio analysis) covers the practical dimensions that matter for the DSP readership. Ready for publication.

---

## Strengths

### S1: Bridge Between Deep Unfolding and Classical Thresholding Theory
The threshold comparison (Section 4.13) connects LISTA's learned behavior to the garrote thresholding literature (Antoniadis et al., 2001). The 7.1 dB advantage of hard over soft thresholding is consistent with known results in sparse recovery: hard thresholding avoids the shrinkage bias of soft thresholding on large coefficients.

### S2: AMP Connection Appropriately Hedged
The AMP discussion now states "our findings are consistent with this framework" and "direct validation remains future work." This is the correct framing for an empirical observation about a theoretical connection.

### S3: Comprehensive Channel Model Coverage
The paper evaluates i.i.d. Gaussian, ITU PedA, ITU VehA, and complex-valued channels. The cross-distribution generalization results (Table 10) and error concentration on ITU channels (Table 15) provide practical confidence in LISTA's deployment.

### S4: Honest Positioning vs. FISTA
The FISTA comparison (Table 12) honestly demonstrates that LISTA's learned parameters do not improve NMSE over standard accelerated ISTA. This clarity helps practitioners make informed choices.

---

## Weaknesses

### W1: Missing Discussion of Threshold Shrinkage Bias
**Problem**: The paper notes that hard thresholding outperforms soft by 7.1 dB but does not connect this to the well-known shrinkage bias of soft thresholding in the sparse recovery literature.
**Why it matters**: The shrinkage bias (soft thresholding shrinks all coefficients by θ, including large true taps) is the theoretical explanation for the 7.1 dB gap. Citing this connection would strengthen the domain contribution.
**Suggestion**: Add a brief discussion of shrinkage bias and cite relevant sparse recovery theory (e.g., Donoho & Johnstone, 1994).
**Severity**: Minor

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 76 | Strong | Threshold comparison bridges deep unfolding and classical theory |
| Methodological Rigor (25%) | 84 | Strong | Comprehensive experiments; statistical validation |
| Evidence Sufficiency (25%) | 85 | Strong | Multiple channel models, seeds, baselines |
| Argument Coherence (15%) | 84 | Strong | Clear narrative; AMP hedged |
| Writing Quality (15%) | 84 | Strong | Professional, honest |
| Literature Integration | 78 | Strong | Good coverage; threshold theory connection is new |
| **Weighted Average** | **82.4** | **Accept** | |

---

*Report submitted by Reviewer 2 (Domain Expert)*
