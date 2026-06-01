# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 7

---

## Decision

### Minor Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC (Prof. Marchetti) | Journal Editor | Minor Revision | 4 |
| Reviewer 1 (Dr. Zhang) | Methodology | Minor Revision | 5 |
| Reviewer 2 (Prof. Santos) | Domain Expert | Minor Revision | 5 |
| Reviewer 3 (Dr. Tanaka) | Perspective (Hardware) | Major Revision | 4 |
| Devil's Advocate (Prof. Volkov) | Stress Test | — (Issues flagged) | — |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All 4 reviewers + DA agree):
1. **The BER-NMSE disconnect analysis is the paper's strongest contribution.** EIC (S1), R1 (noted), R2 (S2), R3 (S1), and DA all agree that the finding—LISTA's NMSE gap does not translate to BER penalty under MMSE—is novel and practically valuable. The mechanism analysis (error concentration on true taps) provides genuine insight.

2. **The ablation study methodology is exemplary.** EIC (S2), R1 (S1), R2 (S3), and DA (Observations) all commend the 5→20 seed progression with transparent power analysis. The paper's acknowledgment of the initial false negative demonstrates good scientific practice.

3. **The hardware throughput claims require significant qualification.** EIC (W1), R3 (W1—CRITICAL), R2 (W1), and DA (C2) all identify the theoretical nature of hardware claims as a problem. R3 provides specific technical reasons (memory bandwidth, pipeline hazards, fixed-point effects) why the 4.4× estimate is likely optimistic.

**[CONSENSUS-3]** (3/4 reviewers agree):
1. **Cross-table inconsistency (Table 1 vs Table 3) undermines reproducibility.** EIC (W3), R1 (W1), and DA (M3) flag this as a significant issue. R2 notes it but considers it less critical. **Editor's resolution**: This is a legitimate concern that must be addressed. The 8 dB discrepancy at the same nominal configuration is too large to ignore.

2. **Missing CNN/Transformer baseline is a gap.** EIC (W4), R2 (W1), and DA (M4) identify this as a weakness. R3 focuses on hardware but agrees the positioning is incomplete. **Editor's resolution**: At minimum, a qualitative comparison table with published results on comparable channel models should be added. A direct comparison is preferred but may be deferred to supplementary material.

### Points of Disagreement

**Disagreement 1: Severity of hardware claims issue**
- **R3 view**: CRITICAL — hardware claims are "unsupported speculation" and should be downgraded to "theoretical analysis suggests potential improvement"
- **EIC/R1/R2 view**: MAJOR — hardware claims need qualification but do not invalidate the paper
- **DA view**: CRITICAL — hardware claims are overgeneralization from computational complexity to hardware performance
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The issue is MAJOR, not CRITICAL. The paper already includes appropriate caveats ("these are theoretical estimates; measured FPGA/ASIC results remain future work") in the Discussion and Conclusion. The problem is that the abstract and highlights present the numbers without sufficient qualification. Revising the abstract/highlights to add "theoretical" qualifiers resolves this without requiring new experiments.
- **Resolution Rationale**: The paper's caveats are present but buried. Prominent qualification in the abstract/highlights is sufficient.

**Disagreement 2: Whether the BER "no penalty" claim is misleading**
- **DA view**: The BER claim is "vacuous under MMSE" because MMSE masks estimator quality, not because LISTA is good
- **EIC/R1/R2 view**: The BER claim is valid and practically useful—system designers care about BER, not NMSE
- **Disagreement type**: Perspective difference
- **Editor's Resolution**: The BER claim is valid but the framing should be adjusted. The paper should state more clearly that LISTA's BER advantage comes from the equalizer's robustness, not from LISTA being a better estimator. The current framing ("LISTA achieves comparable BER") is technically correct but could be more precise.
- **Resolution Rationale**: The BER result is genuinely useful for practitioners. The DA's critique is theoretically valid but the practical implication (no BER penalty) remains true.

**Disagreement 3: Whether the NMSE saturation is proven to be a training artifact**
- **DA view**: Not proven—three evidence points are suggestive but not conclusive
- **EIC/R1/R2 view**: Reasonably supported by the evidence (SNR-specific training breaks saturation)
- **Disagreement type**: Evidence sufficiency disagreement
- **Editor's Resolution**: The paper's evidence is suggestive but not conclusive. The current language ("likely a training artifact") is appropriately hedged. No change required, but the paper should acknowledge the DA's alternative explanation (architectural capacity limit) in the Discussion.
- **Resolution Rationale**: The paper already hedges appropriately. Adding a sentence acknowledging the alternative interpretation strengthens the Discussion.

---

## Decision Rationale

This paper presents a comprehensive analysis of LISTA for sparse channel estimation with several genuine contributions: the BER-NMSE disconnect analysis, the rigorous ablation study, and the error concentration mechanism analysis. The paper is well-written, honestly treats its limitations, and provides useful practical recommendations (SNR-specific training, deployment decision framework).

The primary concerns are: (1) the hardware throughput claims require more prominent qualification, (2) the cross-table inconsistency must be resolved, and (3) a CNN/Transformer baseline comparison should be added or the positioning clarified. These are addressable through text revisions and do not require new experiments (except possibly a supplementary CNN baseline).

The DA raises valid concerns about the BER claim's framing and the NMSE saturation interpretation, but these are matters of perspective rather than factual errors. The paper's hedging language ("likely a training artifact," "theoretical estimates") is appropriate.

I recommend Minor Revision because the core contributions are sound and the issues are addressable through writing revisions. The hardware claims need prominent qualification in the abstract and highlights. The cross-table inconsistency needs a clear explanation or resolution. A CNN/Transformer comparison table (even from published results) would strengthen the positioning.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Qualify hardware claims in abstract and highlights | EIC (W1), R3 (W1), DA (C2) | Critical | Abstract, Highlights | 1 day |
| R2 | Resolve cross-table inconsistency (Table 1 vs Table 3) | EIC (W3), R1 (W1), DA (M3) | Major | Section 4.1, 4.3 | 2 days |
| R3 | Add CNN/Transformer comparison table | EIC (W4), R2 (W1), DA (M4) | Major | Section 5.2 | 2 days |
| R4 | Reframe BER conclusion to acknowledge MMSE robustness | DA (C1) | Major | Abstract, Section 4.10, 6 | 1 day |

### Required Item Details

**R1: Qualify Hardware Claims in Abstract and Highlights**
- **Problem**: The abstract and highlights present "4.4× hardware throughput advantage" and "33× faster in Python" without sufficient qualification. These numbers appear as measured results rather than theoretical estimates.
- **Source**: EIC W1 ("the paper's hardware claims remain theoretical"), R3 W1 ("hardware throughput claims are entirely theoretical"), DA C2 ("hardware claims extrapolated from theoretical analysis")
- **Requirement**: Add "theoretical" or "estimated" qualifiers to all hardware claims in the abstract and highlights. Remove "33× faster in Python" from the highlights (keep in body with caveat). Add "measured FPGA/ASIC results remain future work" to the abstract.
- **Acceptance criteria**: Every hardware claim in the abstract/highlights includes a "theoretical/estimated" qualifier. The 33× Python speedup is not in the highlights.

**R2: Resolve Cross-Table Inconsistency**
- **Problem**: Table 1 reports LISTA at -24.25 dB and Table 3 at -32.29 dB for the same nominal configuration (N=64, K=5, M=256, L=20, SNR=20).
- **Source**: EIC W3 ("an ~8 dB discrepancy between tables"), R1 W1 ("undermines reproducibility"), DA M3 ("data-conclusion mismatch")
- **Requirement**: Either (a) rerun Table 3 with the mixed-SNR model for direct comparison, (b) add a "Training Protocol" column to all tables, or (c) consolidate under a single training protocol. The explanation must be in the main text, not just a footnote.
- **Acceptance criteria**: Readers can identify which training protocol was used for each table and understand the discrepancy.

**R3: Add CNN/Transformer Comparison Table**
- **Problem**: The paper excludes CNN/Transformer baselines, providing only qualitative comparison.
- **Source**: EIC W4, R2 W1 ("missing CNN/Transformer baseline"), DA M4
- **Requirement**: Add a table in Section 5.2 comparing published NMSE/BER results for CNN, Transformer, and LISTA on comparable channel models and SNR ranges. If direct comparison is not possible, provide a structured qualitative comparison table with specific numbers from cited papers.
- **Acceptance criteria**: Readers can assess LISTA's performance relative to CNN/Transformer methods.

**R4: Reframe BER Conclusion**
- **Problem**: The abstract states "LISTA achieves comparable BER to OMP" which the DA argues is misleading because MMSE masks estimator quality.
- **Source**: DA C1 ("BER 'no penalty' claim is vacuous under MMSE")
- **Requirement**: Reframe to: "Under MMSE equalization, LISTA's NMSE gap does not translate to BER penalty (all methods converge at SNR ≥ 5 dB)." This acknowledges that the equalizer, not the estimator, drives the BER result.
- **Acceptance criteria**: The BER conclusion clearly attributes the comparable BER to MMSE robustness.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Reduce abstract to ~200 words | EIC (W2) | P2 | Abstract | Improved readability |
| S2 | Add 95% CIs to BER tables | R1 (W3) | P2 | Section 4.10 | Better statistical reporting |
| S3 | Acknowledge DA's alternative explanation for NMSE saturation | DA (M1) | P2 | Section 5.1 | Stronger Discussion |
| S4 | Add sparsity stability analysis (seeds diverging at each K) | R2 (W3) | P3 | Section 4.2 | Better characterization |
| S5 | Add memory bandwidth analysis for hardware | R3 (W3) | P3 | Section 4.13 | More complete hardware analysis |
| S6 | Add fixed-point quantization analysis | R3 (W2) | P3 | Section 4.13 | Hardware deployment readiness |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 3 days)
- [ ] R1: Qualify all hardware claims in abstract and highlights with "theoretical/estimated"
- [ ] R2: Resolve cross-table inconsistency by adding training protocol identifiers or rerunning with unified protocol
- [ ] R3: Add CNN/Transformer comparison table in Section 5.2
- [ ] R4: Reframe BER conclusion to acknowledge MMSE robustness

### Priority 2 — Content Supplementation (Estimated total effort: 2 days)
- [ ] S1: Trim abstract to 200 words
- [ ] S2: Add 95% CIs to BER tables
- [ ] S3: Add sentence acknowledging alternative NMSE saturation explanation

### Priority 3 — Text and Formatting (Estimated total effort: 1 day)
- [ ] S4: Add sparsity stability analysis
- [ ] S5: Add memory bandwidth analysis (optional)
- [ ] S6: Add fixed-point analysis (optional, can be future work)
- [ ] Minor language fixes identified by reviewers

### Total Estimated Effort
- **Minor Revision**: 5-7 days

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01 (4 weeks)
- **Basis**: Minor Revision, primarily writing revisions with limited new experiments
- **Extension policy**: If extension is needed, notify 1 week before the deadline

---

## Response Letter Instructions

Please use the format in `templates/revision_response_template.md` to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1-R4)
2. Response for each Suggested Revision (S1-S6, adopted or reason for not adopting)
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The paper's core contributions—the BER-NMSE disconnect analysis, the rigorous ablation study, and the error concentration mechanism analysis—are valuable additions to the literature. The revisions required are primarily editorial (qualifying hardware claims, resolving cross-table inconsistency, adding baseline comparison) and do not require fundamental changes to the experimental design.

We look forward to receiving your revision within 4 weeks.

---

## Appendix: Reviewer Score Summary

| Dimension | EIC | R1 | R2 | R3 | Weighted Avg |
|-----------|-----|----|----|----|--------------|
| Originality (20%) | 68 | 65 | 62 | 64 | 64.8 |
| Methodological Rigor (25%) | 78 | 82 | 76 | 68 | 76.0 |
| Evidence Sufficiency (25%) | 75 | 80 | 74 | 62 | 72.8 |
| Argument Coherence (15%) | 82 | 84 | 82 | 78 | 81.5 |
| Writing Quality (15%) | 76 | 78 | 77 | 76 | 76.8 |
| **Overall** | **75.4** | **78.0** | **74.2** | **67.2** | **73.7** |

**Decision**: Minor Revision (weighted average 73.7 falls in the 65-79 range)
