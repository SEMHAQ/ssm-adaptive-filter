# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-06-01
- **Decision Date**: 2026-06-01
- **Review Round**: Round 9

---

## Decision *

### Minor Revision

The manuscript presents a comprehensive analysis of LISTA for sparse channel estimation with a genuine contribution in the BER mechanism analysis. The paper is well-structured, honest about limitations, and uses rigorous statistical practices. However, several issues need to be addressed before publication: hardware throughput claims require significant reframing, the BER mechanism analysis scope should be clarified, and the excessive repetition should be reduced. These are all addressable with minor revisions.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC | Prof. Elena Marchetti (DSP Editor) | Minor Revision | 4 | 69 |
| Reviewer 1 | Prof. Kai Zhang (Methodology) | Minor Revision | 5 | 69 |
| Reviewer 2 | Prof. Maria Rodriguez (Domain) | Minor Revision | 5 | 70 |
| Reviewer 3 | Prof. Hiroshi Tanaka (Perspective) | Minor Revision | 4 | 69 |
| Devil's Advocate | Prof. James Whitfield (Challenge) | N/A (2 CRITICAL, 4 MAJOR) | 5 | — |

**Average Score: 69.3/100 — Minor Revision**

---

## Consensus Analysis *

### Points of Agreement (Consensus)

**[CONSENSUS-5]** (All reviewers agree):
1. **BER mechanism analysis is the paper's primary contribution.** All five reviewers (EIC S2, R1 S2, R2 S2, R3 S1, DA Observations) identify the error concentration finding (99.9% on true taps vs. 94.9% for OMP) as the most valuable contribution. The Devil's Advocate acknowledges this as a "genuine contribution" despite challenging its generalizability.

2. **The paper is honest about its limitations.** All reviewers commend the transparent reporting of LISTA's NMSE saturation, the 13-33 dB gap with OMP, and the theoretical nature of hardware claims. The limitations section (Section 5.4) is consistently praised.

3. **Hardware throughput claims require reframing.** All five reviewers (EIC W1, R1 W3, R2 W1, R3 W2, DA M1) agree that the "2-6× hardware throughput advantage" claim is overstated and needs to be clearly framed as theoretical.

4. **The ablation study methodology is exemplary.** The progression from 5-seed to 20-seed ablation is praised by all reviewers as demonstrating methodological maturity and proper statistical practice.

**[CONSENSUS-4]** (4/5 reviewers agree):
1. **The deep learning comparison (Section 5.2, Table 8) is inadequate.** EIC (W4), R1, R2 (W4), and R3 (W1) all note that the qualitative comparison with CNN/Transformer methods is insufficient. The Devil's Advocate (M4) calls it "not fair or informative." R2 suggests including at least one modern deep learning baseline.

2. **Excessive repetition weakens the paper.** EIC (W3), R3, DA (m1) note that the BER mechanism findings are repeated at least 6 times. R1 also notes the abstract is too long.

### Points of Disagreement

**Disagreement 1: Severity of the NMSE gap with OMP**
- **EIC view**: The 13-33 dB NMSE gap is a "notable weakness" (W2) that raises questions about practical value, but the BER analysis partially addresses this.
- **DA view**: The NMSE gap fundamentally undermines the "practical alternative" claim. The paper's narrative is "built on a foundation of shifting goalposts."
- **R2 view**: The gap is substantial but the BER mechanism analysis provides genuine insight into when LISTA is preferred.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The NMSE gap is a legitimate concern but does not prevent publication. The paper's contribution is the mechanism analysis, not the claim that LISTA outperforms OMP. The framing should be tightened to avoid overstating practical relevance.
- **Resolution Rationale**: The paper's primary contribution (BER mechanism analysis) is valid regardless of the NMSE gap. The paper should clearly state when LISTA is preferred (speed-critical, ZF equalization, higher-order modulations) and when OMP is preferred (NMSE-critical applications).

**Disagreement 2: Generalizability of the BER mechanism finding**
- **DA view** (C2): The error concentration finding (99.9% on true taps) is based on a single configuration and its generalizability is not established. This is a CRITICAL issue.
- **R1/R2/R3 view**: The finding is novel and valuable, though its scope should be clarified.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The DA's concern about generalizability is valid but does not rise to CRITICAL. The paper should add a paragraph discussing the scope of the finding and identifying conditions under which it may not hold. The finding is still valuable as a first analysis of this phenomenon.
- **Resolution Rationale**: The paper presents the finding as an analysis of LISTA's behavior on i.i.d. Gaussian channels, not as a universal property. The scope is implicitly limited by the experimental setup. Adding an explicit scope statement addresses the concern without requiring additional experiments.

**Disagreement 3: Whether the saturation is a training artifact or architectural limitation**
- **R2 view** (W4): The paper should compare with OCLISTA and LISTA-AMP to test the hypothesis.
- **DA view** (M2): The "training artifact" explanation is post-hoc and not experimentally verified.
- **EIC/R1/R3 view**: The evidence presented (SNR-specific training breaks saturation, LISTA-CP constraints naturally satisfied) is sufficient for the hypothesis.
- **Disagreement type**: Evidence disagreement
- **Editor's Resolution**: The paper's evidence is sufficient to support the hypothesis, but it should be clearly labeled as a hypothesis. The comparison with OCLISTA/LISTA-AMP is valuable future work but not required for publication.
- **Resolution Rationale**: The three lines of evidence (scale-invariant loss, SNR-specific training, LISTA-CP diagnostics) provide reasonable support for the "training artifact" hypothesis. Requiring comparison with additional LISTA variants would significantly expand the paper's scope.

---

## Decision Rationale *

The paper makes a solid contribution to the sparse channel estimation literature through its BER mechanism analysis, which reveals that LISTA's soft-thresholding operator produces an error structure (concentrated on true taps) that is favorable for equalization. This insight is novel, well-validated (200 realizations, 5 seeds, paired t-tests), and has implications beyond channel estimation. The ablation study progression (5 seeds → 20 seeds) demonstrates methodological maturity, and the honest limitations discussion strengthens the paper's credibility.

The main concerns are: (1) hardware throughput claims need significant reframing as theoretical estimates, (2) the BER mechanism analysis scope should be explicitly stated, (3) excessive repetition should be reduced, and (4) the deep learning comparison should be more clearly positioned as qualitative. The Devil's Advocate raised two CRITICAL issues: the practical value proposition and mechanism generalizability. I do not consider these CRITICAL because (a) the paper's primary contribution is the mechanism analysis, not the claim that LISTA is a practical alternative to OMP, and (b) the finding's scope is implicitly limited by the experimental setup.

The decision is Minor Revision rather than Major Revision because all concerns are addressable with text changes (reframing, scope clarification, repetition reduction) without requiring additional experiments. The paper's scientific contributions are sound, and the revisions are editorial in nature.

---

## Required Revisions * (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Reframe hardware throughput claims as theoretical estimates | EIC, R1, R2, R3, DA | Critical | Abstract, Intro, Sec 4.13, Conclusion | 1 day |
| R2 | Clarify scope of BER mechanism analysis | DA (C2), R2 | Major | Sec 4.12, Discussion | 0.5 day |
| R3 | Reduce excessive repetition of BER mechanism findings | EIC (W3), DA (m1) | Major | Abstract, Intro, Sec 4.10, 4.12, Discussion, Conclusion | 1 day |
| R4 | Clarify paired t-test methodology for BER experiments | R1 (W2) | Major | Sec 4.10 | 0.5 day |

### Required Item Details

**R1: Reframe hardware throughput claims as theoretical estimates**
- **Problem**: The "2-6× hardware throughput advantage" is presented as a finding but is a theoretical estimate based on unvalidated assumptions. All 5 reviewers flagged this.
- **Source**: EIC W1, R1 W3, R2 W1, R3 W2, DA M1
- **Requirement**: Replace "2-6× throughput advantage" with "theoretical analysis suggests potential for pipelining advantage" consistently throughout. Remove the 4.4× point estimate. Keep FLOP counts and parallelism analysis. Add a clear disclaimer near the first hardware claim.
- **Acceptance criteria**: The word "advantage" should not appear without "theoretical" or "estimated" qualifier in any hardware claim. No specific throughput multiplier should be stated without "theoretical" qualifier.

**R2: Clarify scope of BER mechanism analysis**
- **Problem**: The error concentration finding (99.9% on true taps) is presented as a general property but is demonstrated only for i.i.d. Gaussian channels with K=5, N=64, M=256.
- **Source**: DA C2, R2 W3
- **Requirement**: Add a paragraph in Section 4.12 or Section 5.1 explicitly stating the scope: "These findings are based on i.i.d. Gaussian channels with K=5, N=64, M=256. The generalizability to channels with correlated taps, different sparsity levels, or different pilot ratios is an open question."
- **Acceptance criteria**: The scope limitation is explicitly stated in at least one location.

**R3: Reduce excessive repetition of BER mechanism findings**
- **Problem**: The 99.9% error concentration, 50× less non-support error, and 1.8× noise enhancement findings are repeated at least 6 times across the paper.
- **Source**: EIC W3, DA m1
- **Requirement**: Present the full analysis in Section 4.12. Summarize briefly in Section 5.1. Reference back from Abstract, Introduction, and Conclusion. Remove redundant detailed explanations in Sections 4.10 and 4.12's summary paragraphs.
- **Acceptance criteria**: The detailed mechanism analysis appears in full only once (Section 4.12). Other locations reference it with 1-2 sentences.

**R4: Clarify paired t-test methodology for BER experiments**
- **Problem**: The pairing structure for BER paired t-tests is unclear. Are the same noise instances used for all methods?
- **Source**: R1 W2
- **Requirement**: Add a sentence in Section 4.10 clarifying: "All methods are evaluated on the same channel realizations and noise instances at each SNR point, enabling paired statistical tests."
- **Acceptance criteria**: The pairing structure is explicitly stated.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Add justification for 5-seed experiments | R1 (W1) | P2 | Sec 4.1 | Addresses seed count inconsistency |
| S2 | Add 95% confidence intervals to NMSE tables | R1 (W4) | P3 | Tables 1-4 | Better uncertainty quantification |
| S3 | Discuss multiple comparison correction | R1 (W5) | P3 | Sec 4 | Statistical rigor |
| S4 | Discuss structured W^(k) alternatives | R2 (W2) | P2 | Sec 5.4 | Addresses scalability concern |
| S5 | Discuss channel model limitations | R2 (W3) | P3 | Sec 5.4 | Scope clarification |
| S6 | Discuss practical deployment constraints | R3 (W2) | P3 | Sec 5.3 | Practical relevance |
| S7 | Shorten abstract to 250-300 words | EIC, R1, R3 | P3 | Abstract | Readability |

---

## Revision Roadmap *

### Priority 1 — Structural Revisions (Estimated total effort: 3 days)
- [ ] R1: Reframe all hardware throughput claims as theoretical estimates throughout the paper
- [ ] R2: Add scope clarification paragraph for BER mechanism analysis
- [ ] R3: Consolidate BER mechanism findings — full analysis in Section 4.12 only, brief references elsewhere
- [ ] R4: Add pairing structure clarification to Section 4.10

### Priority 2 — Content Supplementation (Estimated total effort: 2 days)
- [ ] S1: Add brief justification for why 5 seeds suffices for non-ablation experiments
- [ ] S4: Add discussion paragraph on structured W^(k) alternatives for scalability
- [ ] S7: Condense abstract to 250-300 words

### Priority 3 — Text and Formatting (Estimated total effort: 1 day)
- [ ] S2: Add 95% confidence intervals to NMSE tables (or justify use of SD)
- [ ] S3: Add statement about multiple comparison correction approach
- [ ] S5: Add brief acknowledgment of channel model limitations
- [ ] S6: Add brief discussion of practical deployment constraints
- [ ] Minor language fixes noted by reviewers

### Total Estimated Effort
- **Minor Revision**: 4-6 days

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01 (4 weeks)
- **Basis**: Minor Revision — text changes only, no additional experiments required
- **Extension policy**: If extension is needed, notify 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1-R4)
2. Response for each Suggested Revision (S1-S7) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The paper makes a valuable contribution through its BER mechanism analysis and the honest assessment of LISTA's capabilities and limitations. The revisions required are primarily editorial in nature — reframing hardware claims, clarifying scope, and reducing repetition.

We look forward to receiving your revision within 4 weeks.

---

## Appendix: Reviewer Score Summary

| Dimension | EIC | R1 | R2 | R3 | Average |
|-----------|-----|----|----|-----|---------|
| Originality (20%) | 62 | 60 | 65 | 68 | 63.8 |
| Methodological Rigor (25%) | 72 | 68 | 70 | 70 | 70.0 |
| Evidence Sufficiency (25%) | 70 | 72 | 72 | 65 | 69.8 |
| Argument Coherence (15%) | 75 | 74 | 74 | 74 | 74.3 |
| Writing Quality (15%) | 68 | 70 | 68 | 68 | 68.5 |
| **Weighted Average** | **69.4** | **69.2** | **69.8** | **68.5** | **69.3** |

**Decision Threshold**: ≥80 Accept, 65-79 Minor Revision, 50-64 Major Revision, <50 Reject

**Result**: 69.3 → **Minor Revision** ✓

---

## Appendix: Devil's Advocate Issue Summary

| Severity | Count | Issues |
|----------|-------|--------|
| CRITICAL | 2 | C1 (practical value proposition), C2 (mechanism generalizability) |
| MAJOR | 4 | M1 (hardware claims), M2 (saturation explanation), M3 (mechanism depth), M4 (DL comparison) |
| MINOR | 2 | m1 (repetition), m2 (abstract length) |

**Editorial Resolution**: C1 is addressed by reframing the paper's contribution as the mechanism analysis, not the claim that LISTA is a practical alternative. C2 is addressed by adding scope clarification. M1-M4 are addressed by the Required Revisions. The DA's issues do not prevent publication but the revisions should address the core concerns.
