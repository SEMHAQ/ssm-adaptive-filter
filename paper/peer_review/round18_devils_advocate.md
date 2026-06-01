# Devil's Advocate Report (Round 18)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation
- **Manuscript ID**: DSP-2026-ROUND18
- **Review Date**: 2026-06-01
- **Review Round**: Round 18

---

## Reviewer Role
Devil's Advocate — Challenges core arguments, detects logical fallacies, identifies strongest counter-arguments.

## Reviewer Identity
Prof. Marcus Blackwell, Professor of Statistical Signal Processing at Imperial College London.

---

## Strongest Counter-Argument (200 words)

**The threshold comparison experiment, while interesting, actually undermines LISTA's value proposition.**

The paper shows that hard thresholding outperforms soft thresholding by 7.1 dB within the same LISTA architecture (Table 13). But this raises a fundamental question: if hard thresholding is better, why does LISTA use soft thresholding at all? The answer is that LISTA was designed to unroll ISTA, which uses soft thresholding. The 7.1 dB gap suggests that LISTA's architecture is suboptimal—it should have been designed with hard thresholding from the start.

Moreover, the paper's central claim—that LISTA's learned threshold schedule "adapts thresholding behavior beyond default soft-thresholding"—is speculative. The paper does not show that LISTA's learned thresholds produce hard-thresholding-like decisions. It only shows that hard thresholding is better when you replace LISTA's soft thresholding with hard thresholding. These are different claims.

The paper's value proposition is now confused: LISTA is worse than FISTA (NMSE), worse than hard-thresholding LISTA (NMSE), and only provides BER benefits under ZF equalization for 16-QAM at SNR ≥ 15 dB—a narrow operating regime. For most practical systems using MMSE equalization, LISTA provides no advantage.

---

## Issue List

### MAJOR Issues

**M1: Threshold Comparison Does Not Validate LISTA's Adaptation**
- **Dimension**: Argument Coherence
- **Location**: Section 4.13, Table 13
- **Problem**: The paper claims "the learned threshold schedule adapts the thresholding behavior beyond default soft-thresholding" but the experiment shows only that hard thresholding is better when substituted. It does not show that LISTA's learned thresholds produce hard-thresholding-like behavior.
- **Impact**: The interpretation overreaches the evidence.
- **Suggestion**: Add a diagnostic comparing the effective thresholding behavior of learned LISTA vs. ideal hard thresholding (e.g., compare the sparsity patterns of intermediate representations).

**M2: Narrow BER Advantage Regime**
- **Dimension**: Significance
- **Location**: Section 4.14, Table 11
- **Problem**: LISTA's BER advantage over OMP is significant only for 16-QAM under ZF equalization at SNR ≥ 15 dB. Under MMSE (the standard equalizer), all methods converge. The BER advantage is real but narrow.
- **Impact**: For most practical systems, LISTA provides no BER advantage.
- **Suggestion**: Acknowledge the narrow regime more prominently in the abstract.

### MINOR Issues

**m1: Straight-Through Gradient for Hard Thresholding**
- **Location**: Table 13 footnote
- **Problem**: Hard thresholding uses a straight-through gradient estimator. The paper does not discuss whether this approximation affects the 7.1 dB result.

**m2: Convergent Seed Count**
- **Location**: Table 13
- **Problem**: 4 convergent seeds is minimal. One diverged seed per variant suggests training instability.

---

## Observations (Non-Defects)

1. **The contribution framing is now honest.** The "we do not claim to discover" statement and the 4-contribution structure are well-done.
2. **The AMP connection is appropriately hedged.** "Consistent with" and "direct validation remains future work" is the correct framing.
3. **The threshold comparison is a genuine addition.** While my critique above notes the interpretation overreach, the experiment itself is well-designed and the result (7.1 dB) is compelling.

---

## Devil's Advocate Score Summary

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 72 | Adequate | Threshold comparison adds novelty but interpretation overreaches |
| Methodological Rigor (25%) | 80 | Strong | Comprehensive; n=4 is minimal |
| Evidence Sufficiency (25%) | 82 | Strong | Multiple experiments; threshold comparison well-designed |
| Argument Coherence (15%) | 78 | Strong | Clear but interpretation slightly overreaches |
| Writing Quality (15%) | 83 | Strong | Professional, honest |
| **Weighted Average** | **79.0** | **Minor Revision** | |

---

*Report submitted by Devil's Advocate*
