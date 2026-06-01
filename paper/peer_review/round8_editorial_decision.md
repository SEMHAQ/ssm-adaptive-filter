# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-ROUND8
- **Submission Date**: 2026-06-01
- **Decision Date**: 2026-06-01
- **Review Round**: Round 8

---

## Decision

### Minor Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC (Prof. Marchetti) | Journal Editor-in-Chief | Minor Revision | 4 |
| Reviewer 1 (Dr. Chen) | Methodology Expert | Minor Revision | 5 |
| Reviewer 2 (Prof. Wei) | Domain Expert (Sparse Channel Estimation) | Minor Revision | 5 |
| Reviewer 3 (Dr. Okonkwo) | Hardware/Deployment Perspective | Minor Revision | 4 |
| Devil's Advocate | Adversarial Challenger | N/A (challenge-only) | — |

**Consensus**: All four scoring reviewers recommend Minor Revision with high confidence (4–5). The Devil's Advocate raised two CRITICAL issues that require editorial resolution.

---

## Consensus Analysis

### Points of Agreement (Consensus-4)

**[CONSENSUS-4] All 4 reviewers agree:**
1. **The paper is well-written and transparent about limitations.** EIC (S1), R1 (S3), R2 (S3), R3 (S1) all praise the paper's honesty about LISTA's NMSE gap, theoretical hardware estimates, and training divergence.
2. **The BER-NMSE disconnect analysis is the paper's primary contribution.** EIC (S2), R1 (S4), R2 (S3), R3 (S2) all identify this as the most impactful finding, though the DA challenges its interpretation.
3. **The ablation study progression (5-seed → 20-seed) is methodologically sound.** EIC (S3), R1 (S2), R2 (S5), R3 (S4) all commend the self-correcting experimental design.
4. **The theoretical hardware claims need stronger caveating.** EIC (W1), R1 (W1), R2 (W5), R3 (W1) all note that the 4.4× throughput estimate is presented with false precision.

**[CONSENSUS-3] 3/4 reviewers agree:**
1. **The qualitative CNN/Transformer comparison (Table 7) should be removed or restructured.** EIC (W2), R2 (W4), R3 (W5) agree; R1 does not specifically mention it. The indirect comparison across different experimental setups is potentially misleading.
2. **The paper lacks code/data availability.** R1 (W5), R2 (W5), R3 (W2) mention reproducibility concerns; EIC does not specifically address this.

### Points of Disagreement

**Disagreement 1: Severity of the "trivially true under MMSE" challenge**
- **DA view (C1)**: The BER-NMSE disconnect is trivially true for *any* estimator under MMSE, not a special property of LISTA. The paper fails to show LISTA's error structure provides BER advantage over a generic -25 dB NMSE estimator.
- **EIC/R1/R2/R3 view**: The finding is valuable because it quantifies the specific mechanism (error concentration on true taps) and provides actionable deployment guidance.
- **Disagreement type**: Severity disagreement — DA sees this as CRITICAL; the other reviewers see it as a genuine insight.
- **Editor's Resolution**: The DA's point is partially valid — MMSE does suppress estimation quality differences. However, the paper's contribution is not just "no BER penalty under MMSE" but also the mechanism analysis (99.9% vs 94.9% error on true taps) and the ZF results showing LISTA's error structure advantage. The finding is non-trivial because: (a) it quantifies the specific threshold at which NMSE gaps become irrelevant to BER, (b) the mechanism analysis explains *why*, and (c) the ZF results provide a complementary perspective where LISTA's error structure matters. **Resolution: Downgrade from CRITICAL to MAJOR.** The paper should strengthen the MMSE discussion by noting that the "no BER penalty" finding is expected under MMSE's design, and reframe the contribution as the mechanism analysis rather than the BER equivalence per se.

**Disagreement 2: Practical value of the ZF 16-QAM results**
- **DA view (M2)**: The ZF 16-QAM BER values (0.29–0.32) are far above practical operating thresholds; presenting this as an "advantage" is misleading.
- **R3 view (W3)**: The finding is of limited practical value but theoretical interest.
- **EIC view (W3)**: Needs stronger caveating but is still valuable.
- **Disagreement type**: Severity disagreement — DA sees this as MAJOR; R3 and EIC see it as MINOR.
- **Editor's Resolution**: The DA and R3 are correct that the BER values are impractical. However, the finding is valuable for understanding error structure mechanics. **Resolution: MINOR.** Add a sentence clarifying that the BER values are above practical thresholds and the finding is primarily of theoretical interest.

---

## Decision Rationale

This paper presents a systematic analysis of LISTA for sparse channel estimation, with the BER-NMSE disconnect finding as its primary contribution. All four reviewers recommend Minor Revision, and I concur. The paper's strengths — comprehensive experimental design, transparent reporting, actionable deployment framework — outweigh its weaknesses.

The Devil's Advocate raised two CRITICAL issues. After careful consideration, I downgrade both to MAJOR:

1. **The "trivially true under MMSE" challenge (DA C1)**: Partially valid. The paper should acknowledge that MMSE's design inherently suppresses estimation quality differences, and reframe the contribution as the mechanism analysis (error concentration on true taps) rather than the BER equivalence per se. However, the mechanism analysis and ZF results provide genuine insight beyond the trivial observation.

2. **The 4.4× hardware estimate (DA C2)**: Valid concern about false precision, but not a fatal flaw. The paper repeatedly caveats the estimates as theoretical. The fix is to provide uncertainty ranges rather than point estimates.

The required revisions are:
- R1: Reframe the MMSE BER contribution to acknowledge that "no BER penalty under MMSE" is expected by design, and emphasize the mechanism analysis as the primary contribution.
- R2: Add uncertainty ranges to the hardware throughput estimates (e.g., "2–6×" rather than "4.4×").
- R3: Address the DA's point about comparing LISTA's BER with a generic -25 dB estimator under MMSE (even a brief theoretical argument would suffice).

These are achievable within 2–3 weeks and do not require additional experiments.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Reframe MMSE BER contribution: acknowledge that "no BER penalty under MMSE" is expected by MMSE's design; reframe primary contribution as mechanism analysis | DA (C1), EIC | Critical | Abstract, Section 4.10, Section 5.1, Conclusion | 2 days |
| R2 | Add uncertainty ranges to hardware throughput estimates | EIC (W1), R1 (W1), R3 (W1), DA (C2) | Critical | Abstract, Section 4.13, Conclusion | 1 day |
| R3 | Add theoretical argument for why LISTA's error structure provides BER advantage over generic -25 dB estimator under MMSE (or acknowledge the limitation) | DA (C1) | Major | Section 4.10.1 | 1 day |

### Required Item Details

**R1: Reframe MMSE BER Contribution**
- **Problem**: The paper presents "no BER penalty under MMSE" as a finding about LISTA, when it is actually a property of MMSE equalization that applies to any estimator with reasonable NMSE.
- **Source**: DA (C1): "The BER-NMSE disconnect finding is trivially true for any estimator under MMSE." EIC: "The comparable BER under MMSE should be interpreted as evidence of MMSE's robustness to estimation errors."
- **Requirement**: In the Abstract, Introduction, and Conclusion, reframe the contribution: instead of "LISTA's NMSE gap does not translate to BER penalty under MMSE," say "under MMSE equalization, the NMSE gap between LISTA and OMP does not affect BER, consistent with MMSE's known robustness to estimation errors; the mechanism analysis reveals LISTA's error concentration on true taps."
- **Acceptance criteria**: The paper no longer implies that "no BER penalty under MMSE" is a special property of LISTA.

**R2: Add Uncertainty Ranges to Hardware Estimates**
- **Problem**: The 4.4× throughput estimate is a point estimate with no uncertainty quantification.
- **Source**: EIC (W1), R1 (W1), R3 (W1), DA (C2).
- **Requirement**: Replace "4.4× throughput advantage" with "estimated 2–6× throughput advantage (point estimate 4.4×, subject to implementation-dependent factors including memory bandwidth, pipeline stalls, and clock frequency)."
- **Acceptance criteria**: All hardware throughput claims include uncertainty ranges.

**R3: Address Generic Estimator Comparison**
- **Problem**: The paper does not demonstrate that LISTA's specific error structure provides BER advantage over a generic -25 dB NMSE estimator under MMSE.
- **Source**: DA (C1): "A random channel estimator with -25 dB NMSE would also show no BER penalty under MMSE."
- **Requirement**: Add a brief argument (1–2 paragraphs) in Section 4.10.1 or Section 5.1 explaining whether LISTA's error concentration on true taps provides any BER advantage over a generic estimator with the same NMSE under MMSE. If no advantage exists under MMSE, state this explicitly and note that the error concentration advantage is specific to ZF equalization.
- **Acceptance criteria**: The paper explicitly addresses whether LISTA's error structure matters under MMSE, or clearly states it does not.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Remove or restructure Table 7 (qualitative CNN/Transformer comparison) | EIC (W2), R2 (W4) | P2 | Section 5.2 | Avoids misleading indirect comparisons |
| S2 | Add code/data availability statement | R1 (W5), R2 (W5) | P2 | Before References | Improves reproducibility |
| S3 | Add 95% confidence intervals to all NMSE tables | R1 (W4) | P3 | Tables 1–4, 9, 10 | Consistency with BER tables |
| S4 | Discuss training cost and model update strategy | R3 (W2), R2 (W5) | P2 | Section 5.3 | Addresses practical deployment concerns |
| S5 | Discuss LISTA-CP constraint activation reasons in more depth | R2 (W3) | P3 | Section 4.8 | Deeper insight into optimization dynamics |
| S6 | Cite missing recent works (ISTA-Net++, mmWave LISTA, Learned AMP) | R2 (W2) | P3 | Section 2 | Stronger literature positioning |
| S7 | Clarify that ZF 16-QAM BER advantage is theoretical interest only | DA (M2), EIC (W3), R3 (W3) | P3 | Section 4.10.2 | Prevents misinterpretation |
| S8 | Add power analysis for BER paired t-tests (n=5 seeds) | R1 (W2) | P2 | Section 4.10 | Strengthens statistical claims |
| S9 | Discuss scalability mitigation (structured W^(k)) more prominently | EIC (W4), R3 (W5) | P2 | Section 5.3 | Addresses practical limitation |
| S10 | Reframe "LISTA requires no sparsity knowledge" with caveat about training distribution | DA (m1) | P3 | Abstract | More accurate framing |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 4 days)
- [ ] R1: Reframe MMSE BER contribution in Abstract, Section 4.10, Section 5.1, and Conclusion
- [ ] R2: Add uncertainty ranges to hardware throughput estimates in Abstract, Section 4.13, and Conclusion
- [ ] R3: Add theoretical argument comparing LISTA's BER with generic -25 dB estimator under MMSE

### Priority 2 — Content Supplementation (Estimated total effort: 3 days)
- [ ] S1: Remove or restructure Table 7
- [ ] S2: Add code/data availability statement
- [ ] S4: Discuss training cost and model update strategy in Section 5.3
- [ ] S8: Add power analysis for BER paired t-tests
- [ ] S9: Discuss scalability mitigation more prominently

### Priority 3 — Text and Formatting (Estimated total effort: 2 days)
- [ ] S3: Add 95% confidence intervals to NMSE tables
- [ ] S5: Expand LISTA-CP discussion
- [ ] S6: Add missing references
- [ ] S7: Clarify ZF 16-QAM BER framing
- [ ] S10: Reframe sparsity knowledge claim

### Total Estimated Effort
- **Minor Revision**: 1–2 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-06-15 (2 weeks)
- **Basis**: Minor Revision, 3 required items achievable in 4 days, suggested items add ~5 days
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1–R3)
2. Response for each Suggested Revision (S1–S10) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The reviewers found the paper well-written and the BER-NMSE mechanism analysis genuinely insightful. The required revisions are focused: reframing the MMSE contribution, adding uncertainty to hardware estimates, and addressing the "generic estimator" comparison. These are achievable within the 2-week deadline.

We look forward to receiving your revision.

---

## Appendix: Full Reviewer Reports

### EIC Review (Prof. Marchetti)
- **Recommendation**: Minor Revision
- **Confidence**: 4/5
- **Dimension Scores**: Originality 58, Methodology 78, Evidence 82, Coherence 85, Writing 83 → Weighted 76.3
- **Key Strengths**: Transparent reporting, BER-NMSE insight, comprehensive ablation, deployment framework
- **Key Weaknesses**: Limited originality, qualitative CNN comparison, ZF 16-QAM caveating, no structured variant

### Methodology Review (Dr. Chen)
- **Recommendation**: Minor Revision
- **Confidence**: 5/5
- **Dimension Scores**: Originality 55, Methodology 76, Evidence 80, Coherence 83, Writing 82 → Weighted 74.4
- **Key Strengths**: Proper statistical validation, self-correcting design, cross-table transparency, BER validation
- **Key Weaknesses**: Theoretical hardware claims, BER power (n=5), NMSE saturation confound, no CIs in NMSE tables

### Domain Review (Prof. Wei)
- **Recommendation**: Minor Revision
- **Confidence**: 5/5
- **Dimension Scores**: Originality 58, Methodology 77, Evidence 82, Coherence 84, Writing 83, Literature 72 → Weighted 75.2
- **Key Strengths**: Comprehensive literature, correct framing, accurate claims, ITU validation, LISTA-CP diagnostics
- **Key Weaknesses**: Missing RIP discussion, incomplete recent coverage, LISTA-CP depth, descriptive literature section

### Perspective Review (Dr. Okonkwo)
- **Recommendation**: Minor Revision
- **Confidence**: 4/5
- **Dimension Scores**: Originality 60, Methodology 75, Evidence 80, Coherence 83, Writing 82, Impact 72 → Weighted 75.0
- **Key Strengths**: Honest limitations, BER insight, decision framework, error structure analysis, generalization
- **Key Weaknesses**: Theoretical hardware claims, no training cost discussion, ZF practical value, no integration discussion

### Devil's Advocate
- **CRITICAL Issues**: 2 (BER-NMSE trivially true under MMSE; 4.4× estimate false precision) — both downgraded to MAJOR after editorial resolution
- **MAJOR Issues**: 5 (overgeneralization, ZF cherry-picking, confirmation bias, missing alternatives, scalability)
- **MINOR Issues**: 5 (sparsity knowledge claim, absolute error comparison, noise enhancement framing, missing stakeholders, MMSE triviality)
- **Strongest Counter-Argument**: The BER-NMSE disconnect is trivially true for any estimator under MMSE; the paper's contribution is the mechanism analysis, not the BER equivalence.
