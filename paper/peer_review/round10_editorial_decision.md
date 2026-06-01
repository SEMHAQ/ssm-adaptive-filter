# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 10

---

## Decision *

### Major Revision

The manuscript presents a thorough empirical analysis of LISTA for sparse channel estimation. While the paper demonstrates intellectual honesty, statistical maturity, and a genuinely novel BER mechanism analysis, several significant concerns must be addressed before the paper can be considered for publication in *Digital Signal Processing*.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC | Associate Editor, DSP | Minor Revision | 4 |
| Reviewer 1 | Methodology Expert | Minor Revision | 5 |
| Reviewer 2 | Domain Expert (Sparse Channel Estimation) | Major Revision | 5 |
| Reviewer 3 | Hardware/Deployment Expert | Major Revision | 4 |
| Devil's Advocate | Skeptical Deep Learning Researcher | Major Revision (implicit) | 4 |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All reviewers agree):
1. **The BER mechanism analysis (error concentration on true taps) is the paper's strongest contribution.** All five reviewers identify Section 4.12 as novel and valuable. The EIC calls it "the paper's strongest contribution" (S2); R1 highlights its "mechanistic explanation" (S2); R2 calls it "novel domain insight" (S2); R3 acknowledges its intellectual merit; the Devil's Advocate concedes it is "genuinely new insight."
2. **The paper's intellectual honesty is commendable.** All reviewers praise the transparent reporting of LISTA's limitations, the explicit acknowledgment of statistical power issues, and the appropriate hedging of hardware claims. The EIC notes "this level of transparency is rare" (S1); R1 calls it "commendable" (S3); R2 agrees; R3 praises the "consistent hedging" (S1).
3. **The ablation study with 20 seeds is methodologically strong.** All reviewers agree that Table 13 (20-seed ablation with Cohen's d and paired t-tests) is a highlight. R1 calls it "methodologically exemplary" (S1); the EIC identifies it as the "statistical highlight" (S3); R2 calls it "important domain insight" (S3).

**[CONSENSUS-3]** (3/4 reviewers agree):
1. **The MMSE BER equivalence is trivially expected and should be shortened.** R2 (Major, W2), Devil's Advocate (Critical, C2), and EIC (Minor, implicit) agree that the MMSE BER results are presented at excessive length for a trivially expected finding. R1 does not comment on this. *Editor's resolution*: The MMSE section should be condensed to one paragraph + one table, redirecting space to the mechanism analysis.
2. **The "33× speedup" claim is misleading.** R2 (Major, W5), R3 (Major, W2), and Devil's Advocate (Major, M2) all identify the Python speedup as a software artifact. R1 does not comment. *Editor's resolution*: The speedup claim must be reframed as an implementation efficiency gain, not an algorithmic advantage.
3. **The hardware section lacks measured validation.** R3 (Critical, W1), Devil's Advocate (Major, M3), and EIC (Major, W2) agree that the hardware section is too long for unvalidated theoretical estimates. R2 does not comment. *Editor's resolution*: The hardware section should be significantly shortened and positioned as theoretical analysis with future-work validation.

### Points of Disagreement

**Disagreement 1: Severity of the NMSE gap with OMP**
- **R2 view**: The 13–33 dB NMSE gap "undermines practical value" (W1) and the paper should be repositioned as a "characterization study" rather than claiming LISTA is "practical."
- **EIC view**: The gap is acknowledged but the paper's honest reporting and mechanism analysis compensate. The contribution is analytical, not architectural.
- **Disagreement type**: Severity disagreement — R2 sees the NMSE gap as disqualifying for a "practical alternative" claim; the EIC sees it as acceptable given the paper's honest framing.
- **Editor's Resolution**: The EIC's view is correct that the paper's contribution is analytical, not architectural. However, R2 is correct that the abstract's concluding sentence ("establish LISTA as a practical alternative") overclaims. The paper should be repositioned as a "systematic analysis" rather than a "practical alternative" recommendation.
- **Resolution Rationale**: The data supports the analysis but not the "practical alternative" claim. The mechanism analysis is the genuine contribution.

**Disagreement 2: Whether the paper is Minor or Major Revision**
- **EIC and R1**: Minor Revision — the concerns are addressable and the paper's strengths (honesty, mechanism analysis, ablation) are substantial.
- **R2 and R3**: Major Revision — the NMSE gap, trivially expected MMSE results, unvalidated hardware claims, and limited mechanism analysis scope require substantial revision.
- **Disagreement type**: Severity disagreement.
- **Editor's Resolution**: Major Revision. The convergence of R2 and R3 on Major Revision, combined with the Devil's Advocate's critical findings (C1: data-narrative gap, C2: inflated MMSE contribution), indicates that substantial revision is needed. The required revisions (shortening MMSE section, reframing speedup claims, adding ITU mechanism analysis, shortening hardware section) are substantive but achievable.
- **Resolution Rationale**: The paper has genuine strengths but the gap between the evidence and the narrative requires correction. The mechanism analysis on ITU channels is essential for validating the paper's primary contribution.

---

## Decision Rationale

The paper provides a thorough empirical analysis of LISTA for sparse channel estimation. Its primary contributions—the BER mechanism analysis showing error concentration on true taps, the comprehensive 20-seed ablation, and the multi-dimensional generalization analysis—are valuable additions to the literature. The paper's intellectual honesty in reporting LISTA's limitations is commendable and sets a positive example for the field.

However, several significant concerns must be addressed. First, the paper's narrative overclaims relative to its evidence: the abstract concludes that "these findings establish LISTA as a practical alternative," but the data shows LISTA trails OMP by 13–33 dB in NMSE and achieves BER equivalence only under MMSE (trivially expected) with marginal improvement under ZF (deprecated). Second, the MMSE BER section is inflated for a trivially expected result. Third, the "33× speedup" is a Python software artifact, not an algorithmic advantage. Fourth, the hardware section lacks measured validation. Fifth, the mechanism analysis is limited to i.i.d. Gaussian channels and may not generalize to realistic ITU channels.

These concerns are substantial but addressable. The paper's core contribution—the mechanism analysis—is sound and novel. With appropriate revision (shortening the MMSE section, reframing the speedup and hardware claims, adding ITU mechanism analysis, and repositioning the narrative), this paper can make a valuable contribution to *Digital Signal Processing*.

---

## Required Revisions * (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Add error sparsity analysis (Table 15 equivalent) for ITU channels | R2 (W3), Devil's Advocate (m4) | Critical | Section 4.12 | 3-5 days |
| R2 | Shorten MMSE BER section to 1 paragraph + 1 table | R2 (W2), Devil's Advocate (C2) | Critical | Section 4.10.1 | 1 day |
| R3 | Reframe "33× speedup" as implementation efficiency, not algorithmic advantage | R2 (W5), R3 (W2), Devil's Advocate (M2) | Major | Abstract, Section 4.7.1 | 1 day |
| R4 | Reposition narrative from "practical alternative" to "systematic analysis" | R2 (W1), Devil's Advocate (C1) | Major | Abstract, Introduction, Conclusion | 1-2 days |
| R5 | Shorten hardware section; position pipelining/throughput as theoretical future work | EIC (W2), R3 (W1) | Major | Section 4.13 | 2-3 days |

### Required Item Details

**R1: Error Sparsity Analysis on ITU Channels**
- **Problem**: The mechanism analysis (error concentration on true taps) is the paper's primary contribution but is validated only on i.i.d. Gaussian channels. Real channels (ITU models) have correlated tap amplitudes.
- **Source**: R2 (W3, "Critical"): "If LISTA's error concentration on true taps is specific to i.i.d. Gaussian channels, the mechanism analysis has limited practical relevance." Devil's Advocate (m4): "If the error concentration is specific to i.i.d. Gaussian channels, the mechanism analysis has limited practical relevance."
- **Requirement**: Repeat the error sparsity analysis (Table 15) for ITU PedA and VehA channels. Report the percentage of error on true taps vs non-support taps for LISTA and OMP.
- **Acceptance criteria**: Table 15 equivalent for ITU channels is present in the revised manuscript.

**R2: Condense MMSE BER Section**
- **Problem**: Section 4.10.1 devotes ~2000 words and 2 tables to demonstrating a trivially expected result (BER convergence under MMSE).
- **Source**: R2 (W2, "Major"): "Presenting expected behavior as a contribution inflates the paper's apparent novelty." Devil's Advocate (C2, "Critical"): "Approximately 20% of the results section is devoted to a trivially expected result."
- **Requirement**: Condense Section 4.10.1 to one paragraph (stating the expected result) and one table (Table 7). Remove Table 8 (ZF vs MMSE comparison) and integrate key data into the ZF section.
- **Acceptance criteria**: Section 4.10.1 is ≤ 500 words with 1 table.

**R3: Reframe Speedup Claims**
- **Problem**: "33× faster inference" is a Python benchmark reflecting interpreter overhead, not algorithmic efficiency. LISTA requires 2.3× more FLOPs than OMP.
- **Source**: R2 (W5, "Major"), R3 (W2, "Major"), Devil's Advocate (M2, "Major").
- **Requirement**: Replace all instances of "33× speedup" with language that distinguishes software implementation efficiency from algorithmic complexity. The FLOP comparison (2.3× OMP) should be the primary complexity reference.
- **Acceptance criteria**: No unqualified "33× speedup" claims remain. All speedup references include appropriate context.

**R4: Reposition Narrative**
- **Problem**: The abstract concludes "these findings establish LISTA as a practical alternative," but the data shows LISTA trails OMP by 13–33 dB in NMSE.
- **Source**: R2 (W1, "Major"), Devil's Advocate (C1, "Critical").
- **Requirement**: Reposition the paper as a "systematic analysis" or "characterization study" rather than a "practical alternative" recommendation. The conclusion should lead with the mechanism analysis contribution, not the deployment recommendation.
- **Acceptance criteria**: The abstract and conclusion do not claim LISTA is a "practical alternative" without qualifying the conditions.

**R5: Shorten Hardware Section**
- **Problem**: Section 4.13 is ~2000 words with 4 tables, all based on theoretical estimates with no measured validation.
- **Source**: EIC (W2, "Major"): "Either provide at least a prototype FPGA implementation or significantly shorten the hardware section." R3 (W1, "Critical"): "All hardware claims are theoretical estimates with no measured validation."
- **Requirement**: Shorten Section 4.13 to ~1000 words. Keep the FLOP comparison (Table 14) and scaling analysis (Table 17). Move the pipelining analysis and hardware timing estimates to a brief paragraph in the Discussion or Future Work.
- **Acceptance criteria**: Section 4.13 is ≤ 1000 words with 2 tables.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Expand main NMSE tables to 10-20 seeds | R1 (W1) | P2 | Tables 1-4 | Improved statistical power |
| S2 | Add comparison against OCLISTA or LISTA-AMP | R2 (W4) | P2 | Section 4 | Stronger positioning vs recent variants |
| S3 | Clarify mixed-SNR training asymmetry | R1 (W2) | P2 | Section 4.1 | Fairer comparison framing |
| S4 | Add power consumption estimate | R3 (W5) | P3 | Section 4.13 | More complete hardware analysis |
| S5 | Report exact p-values for all pairwise comparisons | R1 (W4) | P3 | Tables 1-4 | Better statistical transparency |

---

## Revision Roadmap

### Priority 1 — Critical Revisions (Estimated total effort: 8-12 days)
- [ ] R1: Add ITU channel error sparsity analysis (3-5 days)
- [ ] R2: Condense MMSE BER section to ≤ 500 words (1 day)
- [ ] R3: Reframe all speedup claims (1 day)
- [ ] R4: Reposition narrative in abstract/introduction/conclusion (1-2 days)
- [ ] R5: Shorten hardware section to ≤ 1000 words (2-3 days)

### Priority 2 — Content Supplementation (Estimated total effort: 5-7 days)
- [ ] S1: Expand main NMSE tables to more seeds (3-5 days, computationally expensive)
- [ ] S2: Add OCLISTA or LISTA-AMP comparison (3-5 days)
- [ ] S3: Add explicit note about mixed-SNR training asymmetry (0.5 days)

### Priority 3 — Text and Formatting (Estimated total effort: 1-2 days)
- [ ] S4: Add theoretical power consumption estimate (0.5 days)
- [ ] S5: Report exact p-values for all pairwise comparisons (0.5 days)
- [ ] Add cross-table reference box explaining training protocols
- [ ] Verify all reference completeness and accuracy
- [ ] Final language polish

### Total Estimated Effort
- **Major Revision**: 2-3 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-07-15 (6 weeks)
- **Basis**: Major Revision, 2-3 weeks of estimated effort with buffer for computational experiments (ITU mechanism analysis, expanded seeds)
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1-R5)
2. Response for each Suggested Revision (S1-S5, adopted or reason for not adopting)
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We encourage you to carefully consider the reviewers' comments and submit a substantially revised manuscript. The reviewers have identified genuine strengths in your work—particularly the BER mechanism analysis and the comprehensive ablation study—but have also raised significant concerns about the gap between the evidence and the narrative, the scope of the mechanism analysis, and the hardware claims.

The revised manuscript will undergo another round of review, with particular attention to:
1. Whether the ITU mechanism analysis confirms the error concentration finding
2. Whether the narrative appropriately reflects the evidence
3. Whether the hardware section has been appropriately scoped

We look forward to receiving your revision.

---

## Appendix: Reviewer Score Summary

| Reviewer | Originality | Methodology | Evidence | Argument | Writing | Weighted Avg | Decision |
|----------|------------|-------------|----------|----------|---------|-------------|----------|
| EIC | 58 | 78 | 75 | 82 | 80 | 74 | Minor |
| R1 (Methodology) | 55 | 72 | 75 | 80 | 82 | 72 | Minor |
| R2 (Domain) | 52 | 70 | 68 | 78 | 80 | 69 | Major |
| R3 (Deployment) | 50 | 60 | 45 | 75 | 80 | 61 | Major |
| Devil's Advocate | 45 | 68 | 55 | 60 | 78 | 58 | — |
| **Consensus** | **52** | **70** | **64** | **75** | **80** | **67** | **Major** |

**Score interpretation**: The paper scores well on writing quality (80) and argument coherence (75) but lower on evidence sufficiency (64) and originality (52). The primary gaps are in the hardware claims (unvalidated) and the mechanism analysis scope (limited to Gaussian channels). These are addressable through the required revisions.
