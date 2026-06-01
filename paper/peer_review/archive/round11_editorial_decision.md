# Editorial Decision

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Author**: Huanjie Yu
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 11

---

## Decision

### Minor Revision

The manuscript presents a thorough and methodologically sound analysis of LISTA for sparse channel estimation. The BER mechanism analysis (error concentration on true taps) is a genuine contribution, and the ablation with 20 seeds sets a new standard for statistical rigor in deep unfolding studies. However, the hardware throughput claims in the abstract and highlights are not supported by measured results and should be revised. The reviewers unanimously recommend Minor Revision.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC (Prof. Vasquez) | Journal Editor | Minor Revision | 4 | 72/100 |
| Reviewer 1 (Dr. Chen) | Methodology Expert | Minor Revision | 5 | 74/100 |
| Reviewer 2 (Prof. Tanaka) | Domain Expert | Minor Revision | 5 | 73/100 |
| Reviewer 3 (Dr. Okonkwo) | Systems Perspective | Minor Revision | 4 | 70/100 |
| Devil's Advocate (Prof. Petrov) | Stress Test | N/A (issues only) | — | — |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-5]** (All reviewers agree):
1. **Error concentration mechanism is the paper's strongest contribution.** All reviewers acknowledge that the finding (LISTA concentrates 99.9% of error on true taps, 50× less on non-support taps) is novel and valuable. The generalization to ITU channels strengthens the finding.
2. **Ablation methodology is exemplary.** The progression from 5-seed to 20-seed ablation with paired t-tests and Cohen's d is praised by all reviewers as setting a new standard for deep unfolding studies.
3. **Hardware throughput claims need revision.** All reviewers agree that the abstract/highlights claim of "potential for hardware throughput advantage" is not supported by measured results and should be either removed or more strongly caveated.

**[CONSENSUS-4]** (4/5 reviewers agree):
1. **The paper is unusually honest about limitations.** EIC, R1, R2, and R3 all commend the transparent reporting of LISTA's NMSE gap with OMP, the training artifact explanation, and the theoretical nature of hardware claims.
2. **BER under MMSE is expected behavior, not a finding.** EIC, R2, and DA note that the MMSE convergence is a property of the equalizer, not of LISTA. R3 acknowledges this but focuses on the systems implications.
3. **SNR-specific training result is practically valuable.** EIC, R2, and R3 highlight the −31 dB result with narrow-range training as actionable for practitioners.

### Points of Disagreement

**Disagreement 1: Severity of hardware throughput claims**
- **EIC view**: "Major" — the claim appears in the abstract and highlights without measured results.
- **R3 view**: "Major" — from a systems perspective, the gap between theoretical FLOP analysis and measured hardware performance is substantial.
- **DA view**: "Major" — the 2.3× FLOP disadvantage is acknowledged but buried.
- **R1 view**: "Minor" — the claims are adequately hedged with caveats.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: **Major** — the claim appears in the abstract and highlights, which are the most-read parts of the paper. The caveats are present but insufficient given the prominence of the claim.
- **Resolution Rationale**: The abstract is the paper's public face. Hardware claims without measured results in the abstract could create unrealistic expectations and damage the paper's credibility. The EIC and DA both flagged this as Major, and the systems reviewer (R3) confirmed the concern from an implementation perspective.

**Disagreement 2: Practical value of ZF BER advantage**
- **DA view**: The ZF advantage applies only to an equalizer "that practitioners do not use" — limited practical value.
- **R3 view**: The error concentration mechanism has systems implications beyond BER, potentially simplifying receiver design.
- **EIC view**: The mechanism analysis is the paper's primary BER contribution, not the BER equivalence under MMSE.
- **Disagreement type**: Perspective difference
- **Editor's Resolution**: **Both views have merit.** The DA is correct that ZF is rarely used in practice. However, the mechanism insight (error concentration on true taps) is valuable regardless of the equalizer, as it reveals a fundamental property of LISTA's learned representation. The paper should frame the ZF result as illustrating the mechanism, not as a practical advantage.
- **Resolution Rationale**: The mechanism analysis is genuinely novel and should be the focus. The ZF BER result is evidence for the mechanism, not a standalone practical contribution.

---

## Decision Rationale

The manuscript makes a solid contribution to the sparse channel estimation literature through its BER mechanism analysis, rigorous ablation methodology, and practical deployment guidance. The error concentration finding (99.9% on true taps) is novel and provides insight not available in prior LISTA work. The ablation with 20 seeds and statistical significance testing sets a new standard for deep unfolding studies.

The paper's weaknesses are addressable: (1) the hardware throughput claims need to be moved from the abstract/highlights to the discussion section, with stronger caveats; (2) the abstract needs compression; (3) the qualitative CNN/Transformer comparison table should be relabeled as illustrative. None of these require new experiments.

The Devil's Advocate raised a CRITICAL issue regarding the ZF BER advantage being framed as practically relevant when ZF is rarely used. The Editorial Resolution is that the mechanism analysis is the contribution, not the ZF result per se. The paper should be revised to frame the ZF result as evidence for the mechanism, not as a practical advantage. This is a reframing issue, not a factual error, and does not require new experiments.

The unanimous Minor Revision recommendation reflects the reviewers' assessment that the paper is methodologically sound and the contributions are genuine, but the presentation needs refinement before publication.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Remove hardware throughput claims from abstract and highlights; discuss only in Section 4.13 with stronger caveats | EIC, R3, DA | Critical | Abstract, Highlights, Section 4.13 | 1 day |
| R2 | Reframe ZF BER result as evidence for error concentration mechanism, not as a practical advantage | DA, EIC | Critical | Section 4.10, Abstract | 1 day |
| R3 | Compress abstract to ~200 words; remove specific FLOP counts and hardware claims | EIC | Major | Abstract | 0.5 day |

### Required Item Details

**R1: Remove hardware throughput claims from abstract/highlights**
- **Problem**: The abstract claims "theoretical pipeline analysis suggesting potential for hardware throughput advantage over OMP" without measured results. The highlights claim "20-stage pipelining suggests potential for hardware throughput advantage."
- **Source**: EIC (W1, Major), R3 (W1, Major), DA (M1, Major)
- **Requirement**: Remove hardware throughput claims from the abstract and highlights. In Section 4.13, add a paragraph acknowledging the gap between theoretical FLOP analysis and measured hardware performance. Retain the FLOP comparison but remove the pipelining throughput claim from the abstract.
- **Acceptance criteria**: The abstract and highlights do not mention hardware throughput advantage. Section 4.13 discusses pipelining as a theoretical possibility with appropriate caveats.

**R2: Reframe ZF BER result**
- **Problem**: The paper frames the ZF BER advantage as "the primary BER contribution" when ZF is rarely used in practice. The DA correctly identifies this as a logic chain issue.
- **Source**: DA (C1, Critical), EIC (consensus)
- **Requirement**: Reframe the ZF result as evidence for the error concentration mechanism, not as a standalone practical advantage. Add a sentence: "The ZF BER advantage is used here to illustrate the error concentration mechanism; under the standard MMSE equalizer, all estimators achieve similar BER, consistent with MMSE's known robustness."
- **Acceptance criteria**: The ZF result is presented as evidence for the mechanism, not as a practical contribution.

**R3: Compress abstract**
- **Problem**: The abstract is ~350 words, exceeding typical journal guidelines.
- **Source**: EIC (W3, Minor)
- **Requirement**: Reduce to ~200 words. Focus on: problem, approach, key findings (NMSE saturation, error concentration, BER under ZF), main conclusion.
- **Acceptance criteria**: Abstract is ≤ 220 words and covers the key findings without specific FLOP counts.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Add explicit RQ list in Section 1 | R1 | P2 | Section 1 | Clarifies the paper's goals |
| S2 | Add reproducibility table (PyTorch version, GPU, seeds) | R1 | P2 | Section 4.1 | Improves reproducibility |
| S3 | Add citations to Hershey et al. (2014) and Balatsoukas-Stimming & Studer (2019) | R2 | P3 | Section 2.2 | Completes literature coverage |
| S4 | Add paragraph on memory requirements and quantization in Section 4.13 | R3 | P3 | Section 4.13 | Strengthens hardware discussion |
| S5 | Label CNN/Transformer comparison table as "illustrative only" | EIC | P3 | Section 5.2 | Prevents misleading comparison |
| S6 | Report effective degrees of freedom for BER paired t-tests | R1 | P3 | Section 4.10 | Improves statistical reporting |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 2.5 days)
- [ ] R1: Remove hardware throughput claims from abstract and highlights; strengthen caveats in Section 4.13
- [ ] R2: Reframe ZF BER result as evidence for error concentration mechanism
- [ ] R3: Compress abstract to ~200 words

### Priority 2 — Content Supplementation (Estimated total effort: 1.5 days)
- [ ] S1: Add explicit RQ list in Section 1
- [ ] S2: Add reproducibility table in Section 4.1
- [ ] S6: Report effective degrees of freedom for BER paired t-tests

### Priority 3 — Text and Formatting (Estimated total effort: 1 day)
- [ ] S3: Add missing citations (Hershey 2014, Balatsoukas-Stimming 2019)
- [ ] S4: Add memory requirements discussion in Section 4.13
- [ ] S5: Label CNN/Transformer comparison table as illustrative
- [ ] Fix terminology consistency ("deep-unfolded" vs "deep unfolding")
- [ ] Check figure references and ensure all figures are included

### Total Estimated Effort
- **Minor Revision**: 5 days

---

## Revision Deadline

- **Recommended deadline**: 2026-06-15 (2 weeks)
- **Basis**: Minor revision — the required changes are textual/reframing, not experimental
- **Extension policy**: If extension is needed, notify 1 week before the deadline

---

## Response Letter Instructions

Please use the R→A→C (Reviewer comment → Author response → Change description) format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1–R3)
2. Response for each Suggested Revision (S1–S6, adopted or reason for not adopting)
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The reviewers have identified genuine contributions (error concentration mechanism, ablation methodology) and the required revisions are primarily textual/reframing changes. We look forward to receiving your revision within 2 weeks.

---

## Appendix: Reviewer Dimension Scores

### EIC (Prof. Vasquez)

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | No architectural novelty; mechanism analysis is novel |
| Methodological Rigor (25%) | 76 | Strong | Comprehensive experiments; statistical rigor in ablation |
| Evidence Sufficiency (25%) | 75 | Strong | 12 experiments; 20 seeds for ablation; 200 realizations for BER |
| Argument Coherence (15%) | 72 | Adequate | Clear flow; ZF framing issue |
| Writing Quality (15%) | 70 | Adequate | Clear but dense; abstract too long |
| **Weighted Average** | **72.3** | **Minor Revision** | |

### Reviewer 1 — Methodology (Dr. Chen)

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | Mechanism analysis is novel; methodology is standard |
| Methodological Rigor (25%) | 80 | Strong | Exemplary ablation; paired BER design; transparent reporting |
| Evidence Sufficiency (25%) | 78 | Strong | Comprehensive; 20 seeds; 200 realizations |
| Argument Coherence (15%) | 74 | Adequate | Clear; cross-table consistency note is helpful |
| Writing Quality (15%) | 72 | Adequate | Clear; some verbosity |
| **Weighted Average** | **74.2** | **Minor Revision** | |

### Reviewer 2 — Domain (Prof. Tanaka)

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 70 | Adequate | Error concentration is novel; analysis approach is standard |
| Methodological Rigor (25%) | 75 | Strong | Sound experimental design |
| Evidence Sufficiency (25%) | 76 | Strong | Comprehensive literature; ITU channels |
| Argument Coherence (15%) | 74 | Adequate | Clear positioning; honest limitations |
| Writing Quality (15%) | 70 | Adequate | Clear; some density issues |
| Literature Integration | 72 | Adequate | Comprehensive; minor gaps (Hershey 2014) |
| **Weighted Average** | **73.4** | **Minor Revision** | |

### Reviewer 3 — Perspective (Dr. Okonkwo)

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | Mechanism analysis is novel; hardware claims are standard |
| Methodological Rigor (25%) | 74 | Strong | Sound; hardware claims need stronger caveats |
| Evidence Sufficiency (25%) | 72 | Adequate | Comprehensive; no measured hardware results |
| Argument Coherence (15%) | 70 | Adequate | Clear; hardware claims need reframing |
| Writing Quality (15%) | 70 | Adequate | Clear; abstract too long |
| Significance & Impact | 68 | Adequate | Moderate practical value; hardware claims premature |
| **Weighted Average** | **70.4** | **Minor Revision** | |

---

## Appendix: Devil's Advocate Issue Summary

| Severity | Count | Key Issues |
|----------|-------|------------|
| CRITICAL | 1 | ZF advantage framed as practical when ZF is rarely used |
| MAJOR | 4 | Hardware claims in abstract; cherry-picking in BER presentation; confirmation bias in framing; NMSE gap understated |
| MINOR | 3 | Missing AMP baseline; hardware stakeholder blind spot; premature recommendation |
| Observations | 4 | Honest presentation; exemplary ablation; clear structure; SNR-specific training value |

**DA CRITICAL Issue Resolution**: The CRITICAL issue (C1) is addressed by Required Revision R2: reframe the ZF BER result as evidence for the error concentration mechanism, not as a practical advantage. This is a presentation issue, not a factual error, and does not require new experiments.

---

*Editorial Decision prepared by the Editor-in-Chief, synthesizing 5 independent review reports.*
