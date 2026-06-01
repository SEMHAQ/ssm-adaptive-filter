# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-31
- **Decision Date**: 2026-05-31
- **Review Round**: Round 1

---

## Decision

### Major Revision

The manuscript presents a systematic evaluation of LISTA for sparse channel estimation with several notable strengths: honest reporting of limitations, comprehensive experimental coverage, and the counterintuitive finding that Gaussian-trained LISTA outperforms OMP on ITU channels. However, three critical issues must be resolved before the paper can be considered for publication.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC | Editor-in-Chief, DSP | Minor Revision | 4 |
| Reviewer 1 | Methodology Expert | Minor Revision | 5 |
| Reviewer 2 | Domain Expert | Minor Revision | 5 |
| Reviewer 3 | Cross-Disciplinary | Minor Revision | 4 |
| Devil's Advocate | Stress Test | N/A (challenges only) | — |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All reviewers agree):
1. **Data inconsistency is a critical flaw.** All four reviewers identified that Tables 1, 2, and 3 report different LISTA values at the same experimental condition (SNR=20, K=5, N=64). R1 calls it "Critical," EIC calls it "Major," R2 and R3 note it as a concern. The Devil's Advocate flags it as C1. This must be resolved.
2. **The cross-distribution generalization finding is the paper's main contribution.** All reviewers agree that the ITU outperformance result is interesting and practically significant.
3. **The ablation study is well-designed.** All reviewers commend the ablation with statistical significance testing.

**[CONSENSUS-3]** (3/4 reviewers agree):
1. **Missing comparison with LISTA variants.** R2, R3, and DA note the absence of comparisons with LISTA-CP, OCLISTA, or other learned methods. EIC does not flag this as strongly but acknowledges it.
2. **SNR saturation needs more investigation.** EIC, R1, and DA note that the -23 dB saturation is not adequately addressed. R3 notes it but frames it as a limitation rather than a weakness.

### Points of Disagreement

**Disagreement 1: Severity of the SNR saturation issue**
- **EIC view**: The saturation is a limitation that should be discussed more thoroughly but does not invalidate the paper. The ITU outperformance compensates.
- **DA view**: The saturation is a "fatal flaw" that undermines the paper's central claim. A method with 15-34 dB worse accuracy is not a "practical alternative" regardless of speed.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The saturation is a significant limitation but not fatal. The paper honestly reports it and the ITU outperformance provides a legitimate use case. However, the paper must either (a) evaluate at least one mitigation strategy or (b) provide stronger theoretical justification for why the saturation is fundamental. The framing must be adjusted to acknowledge that LISTA is not competitive on Gaussian channels.
- **Resolution Rationale**: The DA's concern about framing is valid — the paper's language ("practical alternative") overstates the case for Gaussian channels. But the ITU results provide a genuine use case where LISTA outperforms OMP, which justifies publication with appropriate framing.

**Disagreement 2: Ablation contradiction severity**
- **R1 view**: The ablation contradiction (claimed W contribution of +2.28 dB vs Table 5 showing -0.50 dB) is a "Critical" methodological flaw.
- **EIC view**: The contradiction is "Major" — it weakens the narrative but does not invalidate the ablation's main finding (threshold importance).
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The contradiction is Major. The ablation's main finding (threshold is most important) is well-supported regardless of the W claim. The paper must remove or qualify the W contribution claim to match the data.
- **Resolution Rationale**: The threshold finding (p=0.002) is robust. The W issue appears to be a narrative error (citing old data) rather than a methodological flaw. Correcting the narrative resolves the issue.

---

## Decision Rationale

The paper makes a meaningful contribution to the sparse channel estimation literature through its cross-distribution generalization finding, comprehensive experimental design, and honest reporting. The ablation study provides genuine insight into LISTA's components. The practical deployment framework (Gaussian training → ITU deployment) is actionable.

However, three issues prevent acceptance: (1) the data inconsistency between tables must be resolved by re-running experiments with a consistent configuration; (2) the ablation narrative contradiction must be corrected to match the data; (3) the framing must be adjusted to honestly acknowledge that LISTA is not competitive on Gaussian channels while emphasizing the ITU outperformance as the key contribution.

The decision is Major Revision rather than Minor Revision because the data inconsistency affects multiple tables and requires re-running experiments. The revision is tractable and the paper's core contribution remains valid.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Resolve data inconsistency: Re-run all experiments with consistent L=20, M=256 configuration. All tables must use the same model. | EIC, R1, R2, DA | Critical | Tables 1-3, Section 4 | 3-5 days |
| R2 | Fix ablation narrative: Remove or qualify the "W contributes +2.28 dB" claim. Table 5 shows W is not significant (p=0.605). Update abstract, highlights, and conclusion accordingly. | EIC, R1, DA | Critical | Table 5, Abstract, Conclusion | 1 day |
| R3 | Reframe the paper's claims: Acknowledge that LISTA is not competitive on Gaussian channels (15-34 dB gap with OMP). Emphasize ITU outperformance as the key contribution. Adjust abstract, highlights, and conclusion language. | DA, EIC | Major | Abstract, Highlights, Conclusion | 1 day |

### Required Item Details

**R1: Resolve Data Inconsistency**
- **Problem**: Tables 1, 2, and 3 report different LISTA values (-23.12, -31.16, -32.29 dB) at the same condition (SNR=20, K=5, N=64).
- **Source**: All reviewers identified this issue independently.
- **Requirement**: Re-run all experiments with a single consistent configuration (L=20, M=256). Document which training run produced each table. If variance across runs is expected, report it explicitly.
- **Acceptance criteria**: All tables show consistent LISTA values at shared conditions, or the paper explicitly acknowledges and explains any differences.

**R2: Fix Ablation Narrative**
- **Problem**: The paper claims "W contributes +2.28 dB (p < 0.001)" while Table 5 shows removing W improves performance by 0.50 dB (p=0.605).
- **Source**: EIC (W3), R1, DA (M1).
- **Requirement**: Remove the "+2.28 dB" claim. State that W is not significant on Gaussian channels (p=0.605). Note that W may be important for correlated channels (ITU) but this was not tested in the ablation.
- **Acceptance criteria**: The ablation narrative matches Table 5 data. No unsupported claims about W's contribution.

**R3: Reframe Paper Claims**
- **Problem**: The paper claims LISTA is a "practical alternative to OMP" while reporting 15-34 dB worse performance on Gaussian channels.
- **Source**: DA (C2, C3), EIC.
- **Requirement**: Reframe as: "LISTA is a practical alternative for ITU-like channels where Gaussian training data is sufficient and fast inference is required." Remove or qualify claims about Gaussian channel competitiveness.
- **Acceptance criteria**: The abstract and conclusion accurately reflect LISTA's strengths (ITU outperformance, speed) and weaknesses (Gaussian saturation).

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Add comparison with at least one LISTA variant (LISTA-CP, OCLISTA) or model-based deep learning method | R2, R3, DA | P2 | Section 4 | Positions contribution relative to state-of-the-art |
| S2 | Evaluate at least one SNR saturation mitigation strategy (SNR-specific training, alternative loss) | EIC, DA | P2 | Section 4/5 | Addresses the key limitation |
| S3 | Add 5-10 recent references (2023-2025) on deep unfolding for channel estimation | R2 | P3 | Section 2 | Improves literature coverage |
| S4 | Report baseline standard deviations in all tables | R1 | P3 | Tables 1-4 | Improves transparency |
| S5 | Investigate N=256 training divergence cause and mitigation | R3 | P2 | Section 4/5 | Addresses scalability concern |
| S6 | Add effect sizes (Cohen's d) to ablation study | R1 | P3 | Table 5 | Improves statistical reporting |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 5-7 days)
- [ ] R1: Re-run all experiments with consistent L=20, M=256 configuration. Update all tables with new results.
- [ ] R2: Fix ablation narrative. Remove W contribution claim. Update abstract, highlights, conclusion.
- [ ] R3: Reframe paper claims. Adjust abstract, highlights, introduction contributions, conclusion to honestly report Gaussian saturation and emphasize ITU outperformance.

### Priority 2 — Content Supplementation (Estimated total effort: 3-5 days)
- [ ] S1: Add comparison with LISTA-CP or OCLISTA on at least one experiment (e.g., SNR sweep or ITU).
- [ ] S2: Evaluate SNR-specific training (e.g., train on [15, 25] only) and report whether saturation persists.
- [ ] S5: Investigate N=256 divergence. Try gradient clipping, learning rate warmup, or architectural changes.

### Priority 3 — Text and Formatting (Estimated total effort: 1-2 days)
- [ ] S3: Add recent references (2023-2025) to Section 2.
- [ ] S4: Report baseline std in all tables.
- [ ] S6: Add Cohen's d to Table 5.
- [ ] Fix minor language issues noted by reviewers.

### Total Estimated Effort
- **Major Revision**: 9-14 days

---

## Revision Deadline

- **Recommended deadline**: 2026-07-15 (6 weeks)
- **Basis**: Major Revision with experimental re-runs required
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline

---

## Response Letter Instructions

Please use the standard R→A→C format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1-R3)
2. Response for each Suggested Revision (S1-S6) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs
5. Updated tables showing consistent data across all experiments

---

## Closing

We encourage you to carefully consider the reviewers' comments and submit a substantially revised manuscript. The paper's core contribution — the cross-distribution generalization finding — is valuable and worth publishing. However, the data inconsistency and framing issues must be resolved. Please note that the revised manuscript will undergo another round of review, with particular attention to the data consistency issue (R1).

We look forward to receiving your revision.

---

*Editorial Decision prepared by the Editor-in-Chief, Digital Signal Processing*
