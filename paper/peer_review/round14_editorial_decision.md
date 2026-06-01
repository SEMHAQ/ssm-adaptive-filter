# Editorial Decision

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 14

---

## Decision *

### Minor Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC (Prof.~Spanias) | Editor-in-Chief | Minor Revision | 4 | 76.5 |
| Reviewer 1 (Dr.~Chen) | Methodology Expert | Minor Revision | 5 | 78.0 |
| Reviewer 2 (Prof.~Schniter) | Domain Expert | Minor Revision | 5 | 76.0 |
| Reviewer 3 (Dr.~Akçakaya) | Cross-disciplinary Perspective | Minor Revision | 4 | 76.4 |
| Devil's Advocate | Adversarial Reviewer | Minor Revision | — | 71.2 |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-5]** (All reviewers agree):
1. **Excellent statistical methodology.** All five reviewers commend the paper's statistical rigor: 20-seed ablation with Holm--Bonferroni correction, Cohen's $d$ effect sizes, 200-realization BER simulations with paired $t$-tests, and the ISTA/FISTA control experiments. The progression from 5-seed to 20-seed ablation demonstrates methodological maturity and transparency.
2. **Exemplary honesty about limitations.** All reviewers note the paper's transparent reporting of LISTA's NMSE saturation, FISTA superiority, and the ZF-only scope of the BER advantage. This honesty strengthens the paper's credibility.
3. **FISTA comparison is a valuable addition.** The finding that FISTA outperforms LISTA by 1--27~dB at all SNR levels is considered an important contribution that clarifies LISTA's position in the algorithmic landscape.

**[CONSENSUS-4]** (4/5 reviewers agree):
1. **The error concentration mechanism is the paper's primary novel contribution.** EIC, R1, R2, and R3 agree that the $99.9\%$ error concentration on true taps (vs.~$94.9\%$ for OMP and $97.2\%$ for ISTA) is the most interesting finding. The Devil's Advocate challenges this as a "minor refinement" of a known property, but the majority view is that the quantification and ISTA control experiment provide genuine insight.
2. **The practical relevance of ZF equalization results is limited.** EIC, R2, R3, and DA note that ZF is not the standard equalizer and that the error concentration advantage has limited practical scope. R1 does not emphasize this issue.

### Points of Disagreement

**Disagreement 1: Severity of the originality limitation**
- **EIC view**: Originality is "Adequate" (62)---the mechanism analysis compensates for lack of architectural novelty. Minor revision to strengthen positioning.
- **DA view**: Originality is "Weak" (58)---the mechanism is a "minor refinement" of a known property. The framing inflates a modest contribution.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The EIC's assessment is more accurate. The paper does not claim architectural novelty, and the mechanism analysis---while building on known properties of soft-thresholding---provides quantitative insight (ISTA control, $50\times$ comparison with OMP) that goes beyond prior work. The originality is adequate but not exceptional.
- **Resolution Rationale**: The paper's contribution is analytical, not methodological. For an analytical paper, the novelty lies in the depth and rigor of the analysis, not in the architecture itself. The mechanism analysis meets this bar.

**Disagreement 2: Importance of the FISTA comparison**
- **DA view**: The FISTA comparison "essentially demonstrates that LISTA is dominated by a simpler, more effective method" (M3). This undermines the paper's value proposition.
- **EIC/R1/R2/R3 view**: The FISTA comparison is a valuable contribution that clarifies LISTA's position. It strengthens the paper by providing an honest assessment.
- **Disagreement type**: Perspective difference
- **Editor's Resolution**: Both views have merit. The FISTA comparison does demonstrate LISTA's NMSE inferiority, but the paper correctly reframes LISTA's value as lying in the error concentration mechanism and potential hardware pipelining. The comparison strengthens rather than weakens the paper, because it provides the complete picture that readers need.
- **Resolution Rationale**: A paper that honestly reports negative results (FISTA superiority) and explains why the studied method still has value (error concentration) is more useful than one that hides the comparison.

---

## Decision Rationale

This manuscript presents a thorough, methodologically rigorous analysis of LISTA for sparse channel estimation. The five reviewers unanimously recommend Minor Revision, with scores ranging from 71.2 (Devil's Advocate) to 78.0 (Methodology Reviewer), averaging 76.0---solidly in the Minor Revision range.

The paper's primary strengths are: (1) exemplary statistical methodology with proper corrections, effect sizes, and control experiments; (2) honest and transparent reporting of LISTA's limitations; (3) the error concentration mechanism as a novel analytical contribution; and (4) comprehensive baseline comparisons including FISTA and LISTA-CP.

The primary concerns are: (1) the practical relevance of the ZF equalization results is limited (noted by EIC, R2, R3, DA); (2) the connection to AMP theory is missing (R2); (3) the hardware analysis is theoretical only (R3); and (4) the pilot ratio sensitivity is not systematically explored (R2). None of these are critical flaws---they are areas where the paper can be strengthened within the current scope.

The Devil's Advocate raised the concern that the error concentration mechanism is a "minor refinement" of a known property. While this perspective has some merit, the majority view (EIC, R1, R2, R3) is that the quantification, ISTA control experiment, and BER analysis provide genuine insight that goes beyond prior work. The DA did not identify any CRITICAL issues that would warrant rejection.

I recommend Minor Revision to address: (1) the missing AMP theory connection (R2, Major); (2) the pilot ratio experiment (R2, Major); (3) the support recovery uncertainty quantification (R1, Minor); and (4) the ZF relevance framing (EIC, Minor). These revisions are achievable within 2--3 weeks and do not require re-review.

---

## Required Revisions * (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Add discussion connecting error concentration to AMP theory (Onsager corrections, Bethe Hessian) | R2 (Domain) | Major | Section 5.1 | 2 days |
| R2 | Add pilot ratio experiment varying $M/N$ | R2 (Domain) | Major | Section 4.3 or new Section | 3 days |
| R3 | Report mean $\pm$ std over seeds for mechanism analysis metrics (Tables 13--16) | R1 (Methodology) | Minor | Section 4.12 | 1 day |

### Required Item Details

**R1: AMP Theory Connection**
- **Problem**: The paper does not discuss the relationship between LISTA's learned parameters and the Onsager correction terms from AMP theory. This leaves the mechanism analysis without theoretical grounding.
- **Source**: R2 (Domain), W1: "The paper does not discuss the relationship between LISTA's learned $\mathbf{W}^{(k)}$ matrices and the Bethe Hessian / Onsager corrections from AMP theory."
- **Requirement**: Add a paragraph in Section 5.1 connecting the error concentration mechanism to AMP theory. Specifically, discuss whether LISTA's learned $\mathbf{W}^{(k)}$ approximates the Onsager correction that prevents noise amplification in AMP. Cite \citet{liu2023listamp} and discuss the relationship.
- **Acceptance criteria**: The revised Section 5.1 includes a discussion of AMP theory connections with appropriate citations.

**R2: Pilot Ratio Experiment**
- **Problem**: All experiments use $M=256$ pilots, which is a generous budget ($M/N = 4$ for $N=64$). The paper does not evaluate performance under tighter pilot constraints.
- **Source**: R2 (Domain), W2: "The paper does not evaluate how LISTA performs under tighter pilot budgets."
- **Requirement**: Add an experiment varying $M/N$ ratio (e.g., $M \in \{96, 128, 192, 256\}$ for $N=64$) to characterize LISTA's pilot efficiency. This can be a small table or figure added to Section 4.3 or as a new subsection.
- **Acceptance criteria**: The revised paper includes a table or figure showing LISTA performance as a function of $M/N$ ratio.

**R3: Mechanism Analysis Uncertainty**
- **Problem**: Tables 13--16 report mechanism analysis metrics without standard deviations, inconsistent with the paper's statistical standards.
- **Source**: R1 (Methodology), W3: "Without uncertainty bounds, it is impossible to assess whether the $99.9\%$ vs $94.9\%$ difference is statistically significant."
- **Requirement**: Report mean $\pm$ std over the 3 seeds for all mechanism analysis metrics. If variance is very small, state this explicitly.
- **Acceptance criteria**: All mechanism analysis tables include uncertainty quantification.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Strengthen positioning as analytical/"lessons learned" paper | EIC | P2 | Introduction | Clarifies contribution framing |
| S2 | Discuss cross-domain generalizability of error concentration | R3 (Perspective) | P2 | Section 5.1 | Broadens impact |
| S3 | Report FISTA selected threshold values at each SNR | R1 (Methodology) | P3 | Section 4.12.4 | Transparency |
| S4 | Add brief discussion of online/adaptive deployment limitations | R3 (Perspective) | P3 | Section 5.3 | Completeness |
| S5 | Discuss whether LASSO also exhibits error concentration on support | DA | P2 | Section 4.12 | Mechanism attribution |
| S6 | Add discussion of structured linear mappings for scalability | R3 (Perspective) | P3 | Section 5.4 | Scalability guidance |

---

## Revision Roadmap

### Priority 1 — Content Revisions (Estimated total effort: 6 days)
- [ ] R1: Add AMP theory connection discussion in Section 5.1 (2 days)
- [ ] R2: Add pilot ratio experiment ($M \in \{96, 128, 192, 256\}$) with table/figure (3 days)
- [ ] R3: Add uncertainty quantification to Tables 13--16 (1 day)

### Priority 2 — Positioning and Framing (Estimated total effort: 2 days)
- [ ] S1: Strengthen Introduction positioning as analytical paper (0.5 day)
- [ ] S2: Add cross-domain generalizability discussion (0.5 day)
- [ ] S5: Add LASSO error concentration analysis or discussion (1 day)

### Priority 3 — Minor Improvements (Estimated total effort: 1 day)
- [ ] S3: Report FISTA threshold values in Table 12 caption (0.25 day)
- [ ] S4: Add online deployment limitations paragraph (0.25 day)
- [ ] S6: Add structured mappings discussion (0.5 day)
- [ ] Address remaining minor issues from all reviewers (review terminology, figure captions, etc.)

### Total Estimated Effort
- **Minor Revision**: 2--3 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-06-22 (3 weeks from decision)
- **Basis**: Minor revision with content additions (pilot ratio experiment, AMP discussion)
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1--R3)
2. Response for each Suggested Revision (S1--S6): adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The reviewers have provided constructive feedback that should strengthen the paper without requiring substantial changes to the core analysis. We look forward to receiving your revision within 3 weeks.

---

## Appendix: Reviewer Score Summary

| Reviewer | Originality | Methodology | Evidence | Coherence | Writing | Weighted Avg |
|----------|------------|-------------|----------|-----------|---------|-------------|
| EIC | 62 | 82 | 78 | 80 | 82 | 76.5 |
| R1 (Methodology) | 60 | 85 | 80 | 82 | 80 | 78.0 |
| R2 (Domain) | 64 | 78 | 76 | 80 | 82 | 76.0 |
| R3 (Perspective) | 66 | 80 | 76 | 80 | 80 | 76.4 |
| DA | 58 | 78 | 72 | 70 | 80 | 71.2 |
| **Average** | **62.0** | **80.6** | **76.4** | **78.4** | **80.8** | **76.0** |

**Decision threshold**: Minor Revision requires weighted average 65--79. This manuscript scores 76.0, well within the Minor Revision range.

---

