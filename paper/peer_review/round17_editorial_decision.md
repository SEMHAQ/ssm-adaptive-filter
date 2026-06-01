# Editorial Decision

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-ROUND17
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 17

---

## Decision

### Minor Revision

The manuscript presents a thorough empirical analysis of LISTA for sparse channel estimation with a central finding about error concentration on true tap locations. The experimental methodology is comprehensive, the reporting is honest, and the practical deployment recommendations are actionable. After careful consideration of all five reviewer reports, I recommend **Minor Revision**. The paper requires clarification of the novelty framing (error concentration vs. known soft-thresholding properties), weakening of the unsubstantiated AMP theory claims, and a few methodological clarifications. These revisions can be completed within 3–4 weeks.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC | Journal Editor | Minor Revision | 5 | 79.6 |
| Reviewer 1 | Methodology Expert | Minor Revision | 5 | 77.4 |
| Reviewer 2 | Domain Expert | Minor Revision | 5 | 77.8 |
| Reviewer 3 | Cross-Disciplinary | Minor Revision | 4 | 76.0 |
| Devil's Advocate | Adversarial Analysis | Major Revision | — | 70.0 |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All reviewers agree):
1. **Honest reporting is a major strength**: All reviewers commend the paper's transparent reporting of LISTA's limitations (NMSE saturation, FISTA superiority, theoretical-only hardware analysis). This is consistently cited as the paper's strongest quality.
2. **The ablation study is well-designed**: The progression from 5-seed to 20-seed ablation with Holm–Bonferroni correction and Cohen's d is methodologically sound. All reviewers acknowledge this.
3. **The FISTA comparison is valuable**: All reviewers agree that the FISTA baseline (Table 12) is a significant addition that honestly positions LISTA's limitations.
4. **The AMP theory connection is unsubstantiated**: All reviewers note that the W^(k) → Onsager correction hypothesis is not empirically validated and should not be presented as a contribution.

**[CONSENSUS-3]** (3/5 reviewers agree):
1. **The 100% error concentration needs stronger novelty framing**: EIC, R1, and DA question whether the 100% concentration is a novel finding or a known property of soft-thresholding. R2 and R3 accept the characterization more readily.
2. **The 5-seed experiments have insufficient power**: R1, R2, and DA note the power limitation. EIC and R3 accept the 5-seed results as adequate for the large effect sizes observed.

### Points of Disagreement

**Disagreement 1: Severity of the novelty framing issue**
- **EIC view**: The novelty framing is a Major issue (W1) requiring strengthening of the contribution positioning.
- **DA view**: The 100% concentration is a "metric artifact" (C1) and the paper overclaims its contribution.
- **R1/R2/R3 view**: The novelty is adequate but could be better positioned.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The novelty framing is a Major issue but not a fatal flaw. The paper's contribution lies in the *quantification* of error concentration's BER impact and the *demonstration* that learned parameters improve concentration from 92.4% to 100.0%—both are novel in the channel estimation context. However, the framing must be tightened to avoid implying that error concentration itself is a new discovery.
- **Resolution Rationale**: The DA's critique that 100% is "trivial" is partially valid (soft-thresholding does produce sparse outputs), but the paper's pre-thresholding analysis (68.3% before, 100.0% after) and ISTA control (92.4% vs 100.0%) provide evidence that the learned parameters contribute meaningfully. The contribution should be framed as "quantifying and enhancing" rather than "discovering."

**Disagreement 2: Whether the paper should be Major or Minor Revision**
- **DA view**: Major Revision (score 70.0), citing C1 (metric artifact) and C2 (AMP overclaim).
- **EIC/R1/R2/R3 view**: Minor Revision (scores 76.0–79.6), citing the comprehensive methodology and honest reporting.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: Minor Revision. The DA's concerns about the metric (C1) and AMP (C2) are valid but addressable through framing changes, not fundamental restructuring. The paper's experimental methodology is sound, and the core findings (error concentration quantification, BER advantage, ablation) are valid. The revisions required are editorial (framing, AMP weakening) rather than substantive (new experiments, restructured analysis).
- **Resolution Rationale**: The DA's strongest critique—that 100% is a metric artifact—is partially addressed by the pre-thresholding analysis (68.3% before thresholding is not trivial). The AMP critique is fully valid and must be addressed by weakening the claims. However, these are framing issues, not methodological flaws.

---

## Decision Rationale

This manuscript presents a comprehensive empirical analysis of LISTA for sparse channel estimation, with particular attention to the error concentration mechanism and its BER implications. The experimental methodology is thorough: mixed-SNR training protocol, grid-searched baselines, multiple random seeds (5 for main experiments, 20 for ablation), paired t-tests with Holm–Bonferroni correction, Cohen's d effect sizes, and honest reporting of limitations. The FISTA baseline comparison (Table 12) is a significant strength that honestly positions LISTA's NMSE limitations. The BER analysis with QPSK and 16-QAM under MMSE and ZF equalization provides practical system-level context.

The central concern raised by multiple reviewers is the novelty framing of the error concentration mechanism. The Devil's Advocate argues that 100% concentration is a trivial consequence of soft-thresholding. However, the paper's pre-thresholding analysis (68.3% before thresholding) and ISTA control experiment (92.4% vs 100.0%) provide evidence that the learned parameters contribute meaningfully beyond the operator's inherent sparsity promotion. The contribution should be reframed as "quantifying and enhancing" error concentration rather than "discovering" it.

The AMP theory connection (Section 5.1) is the second major concern. All reviewers agree this is speculative and should not appear in the abstract or highlights. The authors must either add empirical validation or significantly weaken the framing.

The 5-seed experiments have limited statistical power, but the effect sizes are large enough (13–33 dB LISTA vs OMP) that 5 seeds are adequate for the main conclusions. The ablation study correctly uses 20 seeds for the smaller effects.

I recommend Minor Revision rather than Major Revision because: (1) the experimental methodology is sound and does not require rework, (2) the core findings are valid and well-supported, (3) the required changes are editorial (framing, AMP weakening) rather than substantive (new experiments), and (4) the paper's honest reporting and comprehensive analysis exceed the typical standard for the journal.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Reframe novelty of error concentration mechanism | EIC, DA | Critical | Abstract, Highlights, Section 1, Section 4.13 | 2 days |
| R2 | Remove or significantly weaken AMP theory claims from abstract/highlights | All reviewers | Critical | Abstract, Highlights, Section 5.1 | 1 day |
| R3 | Clarify error concentration metric edge cases | R1 | Major | Section 4.13.2, Eq. 6 | 1 day |
| R4 | Add confidence intervals for main experiments | R1 | Major | Tables 1, 2, 4, 5, 6, 8 | 2 days |

### Required Item Details

**R1: Reframe Novelty of Error Concentration Mechanism**
- **Problem**: The paper implies that error concentration is a novel discovery, when it is partially a known property of soft-thresholding. The DA correctly notes that ISTA achieves 92.4% with fixed thresholds.
- **Source**: EIC (W1), DA (C1)
- **Requirement**: Reframe the contribution as: (1) the first *quantification* of error concentration's BER impact in channel estimation, (2) the demonstration that learned parameters *enhance* concentration from 92.4% to 100.0% (a 379× non-support error reduction), and (3) the pre-thresholding analysis confirming this is a genuine learned property, not a trivial artifact. Add a "Contribution Summary" paragraph in Section 1 that explicitly addresses the novelty question.
- **Acceptance criteria**: The abstract, highlights, and introduction clearly frame the contribution as "quantifying and enhancing" rather than "discovering" error concentration.

**R2: Remove or Weaken AMP Theory Claims**
- **Problem**: The AMP connection (W^(k) as implicit Onsager correction) is speculative and not empirually validated. All reviewers agree this should not appear in the abstract.
- **Source**: EIC (W2), R2 (W1), DA (C2)
- **Requirement**: Remove the AMP connection from the abstract and highlights. In Section 5.1, clearly label this as a hypothesis for future work, not a finding. Remove the phrase "contextualized within AMP theory" from the abstract.
- **Acceptance criteria**: The abstract and highlights do not mention AMP or Onsager correction. Section 5.1 clearly labels the connection as a hypothesis.

**R3: Clarify Error Concentration Metric Edge Cases**
- **Problem**: The 100.0% ± 0.0% result could arise from the convention (total error = 0) or from genuinely zero non-support error. R1 correctly identifies this ambiguity.
- **Source**: R1 (W2)
- **Requirement**: Report the mean total error alongside the concentration ratio. Clarify whether the 100.0% arises from the convention or from genuinely zero non-support error. Cross-reference the pre-thresholding analysis (Table 7) as evidence that the result is not degenerate.
- **Acceptance criteria**: The paper explicitly states whether the 100.0% is from the convention or from genuine zero non-support error, with supporting data.

**R4: Add Confidence Intervals for Main Experiments**
- **Problem**: The main experiments (Tables 1, 2, 4, 5, 6, 8) report mean ± std but not confidence intervals. R1 correctly notes this limits interpretability.
- **Source**: R1 (W1)
- **Requirement**: Add 95% confidence intervals for all main experiments using t₀.₀₂₅,₄ = 2.776 for 5-seed experiments. Report CIs as [lower, upper] alongside mean ± std.
- **Acceptance criteria**: All main experiment tables include 95% confidence intervals.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Discuss threshold calibration as alternative explanation | DA | P2 | Section 4.13, Section 5.1 | Strengthens mechanistic interpretation |
| S2 | Add structured mapping parameter estimates | EIC, R3 | P2 | Section 5.4 | Addresses scalability concern |
| S3 | Clarify LISTA-CP / gradient clipping interaction | R1 | P2 | Section 4.8 | Strengthens convergence interpretation |
| S4 | Add missing key references | R2 | P3 | Section 2 | Improves literature completeness |
| S5 | Report condition number of measurement matrix | R2 | P3 | Section 4.1 | Connects pilot ratio analysis to CS theory |

---

## Revision Roadmap

### Priority 1 — Framing and Claims (Estimated total effort: 4 days)
- [ ] R1: Reframe error concentration novelty in Abstract, Highlights, Section 1, Section 4.13
- [ ] R2: Remove/weak AMP claims from Abstract, Highlights, Section 5.1
- [ ] R3: Clarify error concentration metric edge cases in Section 4.13.2
- [ ] R4: Add 95% CIs to Tables 1, 2, 4, 5, 6, 8

### Priority 2 — Content Supplementation (Estimated total effort: 3 days)
- [ ] S1: Discuss threshold calibration alternative in Section 4.13/5.1
- [ ] S2: Add structured mapping parameter estimates in Section 5.4
- [ ] S3: Clarify LISTA-CP/gradient clipping in Section 4.8
- [ ] S4: Add missing references (Candes & Plan 2011, Xu et al. 2020)
- [ ] S5: Report measurement matrix condition number

### Priority 3 — Text and Formatting (Estimated total effort: 1 day)
- [ ] Consolidate Table 6 footnotes
- [ ] Expand Table 7 header ("Non-zero non-support taps")
- [ ] Remove internal revision references ("Round 2")
- [ ] Minor language polishing

### Total Estimated Effort
- **Minor Revision**: 3–4 weeks (8 working days)

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01 (4 weeks)
- **Basis**: Minor Revision, standard 2–4 week turnaround
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1–R4)
2. Response for each Suggested Revision (S1–S5), indicating adoption or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The reviewers have provided detailed and constructive feedback, and we believe the paper will be significantly strengthened by addressing the framing issues identified. We look forward to receiving your revision within 4 weeks.

The paper's strengths—honest reporting, comprehensive methodology, and practical deployment recommendations—are commendable. The revisions required are primarily editorial (framing, claim weakening) rather than substantive (new experiments), which should make the revision process straightforward.

---

## Appendix: Full Reviewer Reports

All five reviewer reports (EIC, R1 Methodology, R2 Domain, R3 Perspective, Devil's Advocate) are attached for the author's reference.

---

*Decision issued by the Editor-in-Chief, Digital Signal Processing*
