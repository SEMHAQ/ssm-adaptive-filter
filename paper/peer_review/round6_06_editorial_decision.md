# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 6

---

## Decision

### Minor Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC (Prof. Marchetti) | Associate Editor | Minor Revision | 4 | 72.3 |
| Reviewer 1 (Prof. Zhang) | Methodology Expert | Minor Revision | 5 | 71.2 |
| Reviewer 2 (Prof. Santos) | Domain Expert | Minor Revision | 4 | 70.4 |
| Reviewer 3 (Prof. Thornton) | Hardware/Perspective | Minor Revision | 4 | 66.8 |
| Devil's Advocate | Stress Test | N/A (challenge only) | — | — |

**Average Score**: 70.2 / 100 → Minor Revision range (65–79)

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All reviewers agree):

1. **The BER-NMSE mechanism analysis is the paper's strongest contribution.** All four reviewers identified Section 4.12 (error concentration on true taps: 99.9% vs 94.9% for OMP) as the most valuable finding. EIC: "genuinely insightful"; R1: "non-obvious and actionable"; R2: "valuable contribution"; R3: "the strongest contribution." The Devil's Advocate also acknowledged this as "genuinely insightful."

2. **The statistical validation is exemplary.** The 20-seed ablation with paired t-tests and Cohen's d, the 200-realization BER validation, and the cross-table consistency disclosure are uniformly praised. R1 called the ablation "a model of how ablation studies should be conducted."

3. **LISTA's originality is limited.** All reviewers agree that LISTA is a well-known architecture and the contribution is analytical rather than algorithmic. The novelty lies in the systematic evaluation methodology, not in a new algorithm. EIC scored originality 58/100; R1 scored 55/100; R2 scored 58/100; R3 scored 55/100.

4. **The hardware throughput claims need qualification.** All reviewers and the Devil's Advocate flagged that the "4.4× hardware throughput advantage" claim is theoretical and should be qualified. R3 was most emphatic ("entirely theoretical — no measured FPGA or ASIC results").

**[CONSENSUS-3]** (3 of 4 reviewers agree):

1. **Missing DL baselines is a significant gap.** EIC, R2, and R3 all flagged the absence of CNN/Transformer baselines as a weakness. R1 did not explicitly flag this (focused on statistical methodology). The consensus is that at least one DL baseline would significantly strengthen the paper.

2. **The paper should lead with MMSE results, not ZF.** The Devil's Advocate and R2 noted that MMSE is the standard equalizer in modern systems, and the BER advantage is ZF-specific. The current presentation (leading with ZF results) may mislead readers.

### Points of Disagreement

**Disagreement 1: Severity of missing DL baselines**
- **EIC view**: Major weakness — "Without comparisons to recent DL methods, readers cannot assess whether LISTA is competitive with the current state of the art."
- **R1 view**: Did not explicitly flag this as a weakness (focused on statistical methodology).
- **R2 view**: Major weakness — "Without DL baselines, readers cannot assess LISTA's relative position."
- **R3 view**: Major weakness — "Positioning LISTA relative to at least one modern DL baseline would help."
- **Disagreement type**: Severity disagreement (EIC/R2/R3: Major; R1: not flagged)
- **Editor's Resolution**: This is a Major weakness. The absence of DL baselines limits the paper's ability to position LISTA in the current landscape. However, given that the paper's contribution is analytical (understanding LISTA's behavior) rather than claiming state-of-the-art performance, the absence is not fatal. The authors should add at least a qualitative comparison with DL methods.
- **Resolution Rationale**: Three of four reviewers flagged this; the paper's literature review discusses DL methods but does not compare experimentally.

**Disagreement 2: Whether NMSE saturation is a fundamental limitation or training artifact**
- **Devil's Advocate view**: The saturation may be a training artifact (scale-invariant loss) that could be broken with alternative loss functions.
- **EIC view**: The saturation is attributed to "fixed-depth architecture and scale-invariant training loss" — both are listed as causes.
- **R1 view**: Did not challenge the saturation explanation.
- **R2 view**: Accepted the explanation as presented.
- **Disagreement type**: Explanation disagreement (DA: possibly training artifact; EIC/R2: architectural + loss)
- **Editor's Resolution**: The paper's explanation (Section 5.1) is plausible but not definitive. The authors should acknowledge the Devil's Advocate's alternative explanation (training artifact) and discuss whether alternative loss functions could break the saturation.
- **Resolution Rationale**: The DA's challenge is valid — the paper does not test alternative loss functions. Acknowledging this as a limitation strengthens the paper.

---

## Decision Rationale

All four reviewers recommend Minor Revision with scores in the 66–72 range (average 70.2). The paper's core contribution — a systematic analysis of LISTA for sparse channel estimation with rigorous statistical validation — is solid and well-suited for *Digital Signal Processing*. The BER-NMSE mechanism analysis (error concentration on true taps) is a genuinely valuable finding that all reviewers identified as the strongest contribution.

The paper's weaknesses are consistent across reviewers: (1) missing DL baselines, (2) hardware claims need qualification, (3) literature gaps in recent DL channel estimation work. These are all addressable without fundamental restructuring.

The Devil's Advocate raised important challenges about the ZF-specificity of the BER advantage and the theoretical nature of hardware claims. The editorial decision incorporates these challenges by requiring the authors to: (a) qualify hardware claims as theoretical, (b) acknowledge ZF-specificity more prominently, and (c) discuss the training artifact alternative explanation for NMSE saturation.

The decision is Minor Revision (not Major) because: (a) the core contribution is solid, (b) the weaknesses are addressable within 2–4 weeks, (c) no fundamental methodological flaws were identified, and (d) the statistical validation is exemplary. The paper does not need re-review after revision — the required changes are primarily textual (qualifying claims, adding comparisons, updating literature).

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Qualify hardware throughput claims as theoretical throughout | EIC, R2, R3, DA | Critical | Abstract, Highlights, Section 4.13, Section 6 | 1 day |
| R2 | Add at least one DL baseline comparison (CNN or Transformer) or qualitative comparison table | EIC, R2, R3 | Major | Section 4.1, Section 5 | 3–5 days |
| R3 | Restructure BER presentation: lead with MMSE (realistic case), present ZF as special case | DA, R2 | Major | Section 4.10, Abstract | 2 days |
| R4 | Acknowledge NMSE saturation may be a training artifact; discuss alternative loss functions | DA | Major | Section 5.1 | 1 day |

### Required Item Details

**R1: Qualify Hardware Claims**
- **Problem**: The "4.4× hardware throughput advantage" claim appears in the abstract, highlights, and conclusion without qualification as a theoretical estimate.
- **Source**: EIC (W3), R3 (W1), DA (C1) — all flagged this.
- **Requirement**: Add "theoretical analysis suggests" or equivalent qualification to all hardware throughput claims. Remove "33× faster in Python" from the abstract (keep in results section with caveat).
- **Acceptance criteria**: Abstract and highlights do not claim measured hardware results. All throughput claims are qualified as theoretical.

**R2: Add DL Baseline Comparison**
- **Problem**: Baselines include only classical methods (LMS, NLMS, OMP, LASSO). No deep learning baselines.
- **Source**: EIC (W2), R2 (W1), R3 (W1).
- **Requirement**: Add at least one DL baseline (CNN or Transformer with comparable parameters) OR add a comparison table citing published results from the literature.
- **Acceptance criteria**: Paper includes either experimental comparison with DL baselines or a qualitative comparison table with cited performance numbers.

**R3: Restructure BER Presentation**
- **Problem**: The paper leads with ZF BER results (favorable to LISTA) rather than MMSE results (realistic case where advantage disappears).
- **Source**: DA (M1), R2 (W4).
- **Requirement**: Present MMSE BER first as the realistic case, then present ZF as a special case where LISTA has an advantage. Update abstract to lead with "under MMSE equalization, LISTA achieves comparable BER with no penalty" rather than "under ZF equalization, LISTA achieves better BER."
- **Acceptance criteria**: Abstract and Section 4.10 present MMSE as the primary case and ZF as the special case.

**R4: Acknowledge Training Artifact Alternative**
- **Problem**: The NMSE saturation explanation (Section 5.1) does not consider alternative explanations, such as the scale-invariant loss being the primary cause.
- **Source**: DA (M2).
- **Requirement**: Add a paragraph in Section 5.1 acknowledging that the saturation may be primarily a training artifact (scale-invariant loss) rather than an architectural limitation, and that alternative loss functions (e.g., weighted NMSE, support-aware loss) could potentially break the saturation.
- **Acceptance criteria**: Section 5.1 discusses the training artifact hypothesis and alternative loss functions.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Add 3–5 references from 2024–2025 on learned channel estimation | R2 | P2 | Section 2 | Literature currency |
| S2 | Report grid search details for LMS/NLMS/LASSO tuning | R1 | P2 | Section 4.1 | Reproducibility |
| S3 | Use consistent 5-seed count for support recovery (Table 10) | R1 | P3 | Section 4.12 | Consistency |
| S4 | Add energy/power discussion for hardware analysis | R3 | P3 | Section 4.13 | Completeness |
| S5 | Discuss OFDM extension for BER analysis | R2, DA | P2 | Section 5.3 | Scope clarity |
| S6 | Add equivalence testing (TOST) for QPSK BER "not significant" results | R1 | P3 | Section 4.10 | Statistical rigor |
| S7 | Condense abstract (remove statistical details, keep in methods) | EIC | P3 | Abstract | Readability |

---

## Revision Roadmap

### Priority 1 — Critical Revisions (Estimated total effort: 2–3 days)
- [ ] R1: Qualify all hardware throughput claims as theoretical (abstract, highlights, Section 4.13, Section 6)
- [ ] R3: Restructure BER presentation to lead with MMSE, present ZF as special case

### Priority 2 — Major Content Additions (Estimated total effort: 5–7 days)
- [ ] R2: Add DL baseline comparison (experimental or qualitative table with cited results)
- [ ] R4: Add training artifact alternative explanation to Section 5.1
- [ ] S1: Add 3–5 recent (2024–2025) references on learned channel estimation
- [ ] S5: Discuss OFDM extension for BER analysis in Section 5.3

### Priority 3 — Minor Improvements (Estimated total effort: 1–2 days)
- [ ] S2: Report grid search details for baseline tuning
- [ ] S3: Use consistent 5-seed count for support recovery
- [ ] S4: Add brief energy/power discussion
- [ ] S6: Consider equivalence testing for QPSK BER
- [ ] S7: Condense abstract

### Total Estimated Effort
- **Minor Revision**: 2–3 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-06-29 (4 weeks)
- **Basis**: Minor Revision — requires textual changes and possibly one additional experiment (DL baseline). 4 weeks provides adequate time.
- **Extension policy**: If extension is needed, notify the editor 1 week before the deadline.

---

## Response Letter Instructions

Please respond to every reviewer comment item by item using the standard revision response format.

**Must include**:
1. Response and revision description for each Required Revision (R1–R4)
2. Response for each Suggested Revision (S1–S7) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The paper provides a valuable analytical contribution to the deep unfolding literature, with exemplary statistical validation. The required revisions (qualifying hardware claims, adding DL comparisons, restructuring BER presentation, acknowledging alternative explanations) will strengthen the paper's positioning and honesty.

We look forward to receiving your revision within 4 weeks.

---

## Appendix: Reviewer Score Summary

| Dimension | EIC | R1 | R2 | R3 | Average |
|-----------|-----|----|----|----|---------|
| Originality (20%) | 58 | 55 | 58 | 55 | 56.5 |
| Methodological Rigor (25%) | 78 | 74 | 76 | 68 | 74.0 |
| Evidence Sufficiency (25%) | 75 | 78 | 72 | 65 | 72.5 |
| Argument Coherence (15%) | 82 | 80 | 80 | 78 | 80.0 |
| Writing Quality (15%) | 72 | 70 | 72 | 70 | 71.0 |
| **Weighted Average** | **72.3** | **71.2** | **70.4** | **66.8** | **70.2** |
