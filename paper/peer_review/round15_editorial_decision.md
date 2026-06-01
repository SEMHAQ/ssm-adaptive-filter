# Editorial Decision

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 15

---

## Decision *

### Major Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC (Prof.~Torres) | Journal Editor | Minor Revision | 4/5 |
| Reviewer 1 (Prof.~Zhang) | Methodology Expert | Minor Revision | 5/5 |
| Reviewer 2 (Prof.~Wang) | Domain Expert | Major Revision | 5/5 |
| Reviewer 3 (Prof.~Schwarz) | Cross-disciplinary | Minor Revision | 4/5 |
| Devil's Advocate | Stress Test | N/A (challenge only) | N/A |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All reviewers agree):
1. **Statistical methodology is strong.** The 20-seed ablation with Holm--Bonferroni correction, 200-realization BER simulations, and paired $t$-tests are exemplary. The honest escalation from 5 seeds to 20 seeds demonstrates intellectual integrity. (EIC: S3, R1: S1, R2: S1, R3: S1)
2. **LISTA trails OMP and FISTA in NMSE.** All reviewers acknowledge the 13--33 dB gap with OMP and 1--27 dB gap with FISTA. The paper is honest about this limitation. (EIC: W1, R1: noted, R2: noted, R3: S5)
3. **The ISTA control experiment is well-designed.** Disentangling soft-thresholding effects (92.4%) from LISTA's learned parameters (100.0%) provides genuine insight. (EIC: S2, R1: S3, R2: S2, R3: noted)
4. **FISTA comparison is valuable.** Including FISTA as a baseline honestly positions LISTA's value proposition. (EIC: noted, R1: noted, R2: S4, R3: S5)

**[CONSENSUS-3]** (3/4 reviewers agree):
1. **The error concentration mechanism needs better positioning.** R2 argues it is partially known (soft-thresholding property), DA argues it is trivial, while EIC and R1 find it insightful but narrow. *Resolution: The contribution is the quantification of the enhancement (92.4% → 100.0%) and the BER connection, not the discovery of the mechanism itself.*
2. **The AMP connection is speculative.** EIC, R2, and DA note that the Onsager correction connection has been made by Liu et al. (2023) and Borgerding et al. (2020). R1 does not flag this. *Resolution: Reframe as contextualizing existing theory, not proposing new theory.*

### Points of Disagreement

**Disagreement 1: Severity of the narrative tension**
- **EIC view**: The narrative tension between honest limitations and "highlights" positioning is Major — the abstract should set accurate expectations.
- **DA view**: The highlights box cherry-picks favorable findings (CRITICAL issue).
- **R2 view**: The paper overstates novelty of error concentration (Major).
- **R3 view**: The deployment guidance is honest and actionable (Minor).
- **Disagreement type**: Severity disagreement — all agree the tension exists, but disagree on how serious it is.
- **Editor's Resolution**: The tension is a Major issue. The abstract and highlights box should be revised to lead with the honest limitations before presenting the error concentration finding.
- **Resolution Rationale**: The EIC's assessment is most authoritative on framing issues. The DA's cherry-picking concern is valid but can be addressed by restructuring rather than removing content.

**Disagreement 2: Novelty of the error concentration mechanism**
- **R2 view**: The mechanism is partially known in the compressed sensing literature (Major).
- **DA view**: The mechanism is a trivial consequence of soft-thresholding (CRITICAL).
- **EIC view**: The mechanism is the paper's strongest contribution (S2).
- **R1 view**: The ISTA control experiment provides genuine insight (S3).
- **Disagreement type**: Existence disagreement — is the contribution novel or not?
- **Editor's Resolution**: The contribution is the quantification and BER connection, not the discovery. The ISTA control experiment (92.4% → 100.0%) adds genuine value beyond the known soft-thresholding property.
- **Resolution Rationale**: R1's methodology expertise supports the value of the quantification. The DA's "trivial" assessment is too strong — the 7.6 pp improvement and 379x error reduction are measurable and interpretable. However, R2's concern about literature positioning is valid.

**Disagreement 3: Practical significance of the BER finding**
- **EIC view**: The BER advantage is narrow (ZF + 16-QAM only) — Major.
- **DA view**: Presenting ZF BER as a "major finding" is misleading — CRITICAL.
- **R3 view**: The error concentration has cross-architectural potential — Minor.
- **R1 view**: The BER methodology is sound — not a concern.
- **Disagreement type**: Severity disagreement.
- **Editor's Resolution**: The BER finding is valid but narrow. It should be presented as a nuanced insight, not a major advantage. The DA's CRITICAL assessment is too strong — the finding is real, just narrow.
- **Resolution Rationale**: R1's methodology assessment supports the BER analysis's validity. The practical limitation (ZF only) should be clearly stated but does not invalidate the finding.

---

## Decision Rationale

This paper presents a comprehensive and methodologically rigorous analysis of LISTA for sparse channel estimation. The statistical methodology is exemplary (20-seed ablation, Holm--Bonferroni correction, 200-realization BER simulations), and the paper is unusually honest about LISTA's limitations. The error concentration mechanism, while partially known, is quantified with precision (92.4% → 100.0%, 379x error reduction) and connected to BER performance through a well-designed ISTA control experiment.

However, the paper has significant issues that prevent acceptance: (1) the narrative framing overstates the practical significance of the error concentration finding, particularly in the highlights box and abstract; (2) the literature review omits key LISTA variants (ALISTA, LISTA-CPSS, Elastic LISTA); (3) the AMP connection is presented as a theoretical contribution when it contextualizes existing work; (4) the real-valued channel assumption limits generalizability; and (5) the qualitative CNN/Transformer comparison is weak. The Devil's Advocate raises valid concerns about the core thesis — the error concentration is a known property of soft-thresholding, and the BER advantage only exists under conditions (ZF equalization) that are rarely used in practice.

I recommend Major Revision because the issues are addressable but require substantial changes to the framing, literature review, and positioning. The core experimental work is solid, but the paper's narrative needs to be tightened to accurately represent the contributions.

---

## Required Revisions * (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Reframe abstract and highlights to lead with honest limitations (NMSE gap) before presenting error concentration | EIC, DA | Critical | Abstract, Highlights | 1 day |
| R2 | Add missing LISTA variant references (ALISTA, LISTA-CPSS, Elastic LISTA) and discuss relation to paper's findings | R2 | Critical | Section 2 | 2 days |
| R3 | Reframe AMP connection as contextualizing existing theory (Liu et al. 2023, Borgerding et al. 2020), not proposing new theory | EIC, R2, DA | Critical | Section 5.1 | 1 day |
| R4 | Add formal definition equation for error concentration metric with confidence intervals | R1 | Major | Section 4.12 | 0.5 days |
| R5 | Discuss real-valued channel limitation and its impact on generalizability | R3 | Major | Section 5.4 | 0.5 days |
| R6 | Remove or replace qualitative CNN/Transformer comparison (Table 17) with honest acknowledgment of incomparability | R2, DA | Major | Section 5.2 | 1 day |

### Required Item Details

**R1: Reframe Abstract and Highlights**
- **Problem**: The abstract and highlights box present the error concentration mechanism as the primary contribution without adequately contextualizing LISTA's NMSE limitations. The DA identifies this as cherry-picking.
- **Source**: EIC (W1), DA (C2, M2)
- **Requirement**: Restructure the abstract to lead with: "LISTA trails OMP by 13--33 dB and FISTA by 1--27 dB in NMSE, but exhibits an error concentration mechanism..." The highlights box should be similarly restructured.
- **Acceptance criteria**: A reader scanning only the abstract and highlights should form an accurate impression of LISTA's practical limitations.

**R2: Add Missing LISTA Variants**
- **Problem**: The related work section omits ALISTA (Liu et al., 2019), LISTA-CPSS (Chen et al., 2020), and Elastic LISTA (Liu et al., 2021), which are directly relevant to the paper's analysis of $\mathbf{W}^{(k)}$.
- **Source**: R2 (W1)
- **Requirement**: Add a subsection on "Recent LISTA Variants" covering these works. Discuss how the paper's findings relate to ALISTA's analysis of weight matrices.
- **Acceptance criteria**: The related work section covers the major LISTA variants published through 2024.

**R3: Reframe AMP Connection**
- **Problem**: Section 5.1 presents the Onsager correction connection as a new theoretical contribution, but this connection has been made by Liu et al. (2023) and Borgerding et al. (2020).
- **Source**: EIC (W4), R2 (W3), DA (m3)
- **Requirement**: Reframe Section 5.1 as "Contextualizing the Error Concentration via AMP Theory." Explicitly cite the prior work and explain what the current paper adds (empirical evidence from error concentration analysis).
- **Acceptance criteria**: The AMP discussion is clearly positioned as contextualizing existing theory, not proposing new theory.

**R4: Formalize Error Concentration Metric**
- **Problem**: The "Error on $S$ %" metric is used without formal definition.
- **Source**: R1 (W2)
- **Requirement**: Add equation: $\text{Error on } S = \frac{\sum_{i \in S} (\hat{h}_i - h_i)^2}{\sum_{i=1}^N (\hat{h}_i - h_i)^2} \times 100\%$. Report 95% CIs.
- **Acceptance criteria**: The metric is formally defined with an equation and confidence intervals.

**R5: Discuss Real-Valued Limitation**
- **Problem**: All experiments use real-valued channels and BPSK pilots. Real wireless channels are complex-valued.
- **Source**: R3 (W1)
- **Requirement**: Add a paragraph in Section 5.4 (Limitations) discussing the real-valued assumption and its impact on generalizability.
- **Acceptance criteria**: The limitation is clearly stated with a discussion of how findings might change for complex-valued channels.

**R6: Remove Qualitative DL Comparison**
- **Problem**: Table 17 compares LISTA with CNN/Transformer methods based on different papers' results, which is unreliable.
- **Source**: R2 (W4), DA (noted)
- **Requirement**: Remove Table 17 or replace with an honest statement: "Direct comparison with CNN/Transformer methods under identical conditions is left to future work."
- **Acceptance criteria**: The paper does not draw conclusions from incomparable experimental results.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Add scale-invariant loss diagnostic ($\bar{c}$ metric) | R1 | P2 | Section 4.1 | Strengthens the training artifact argument |
| S2 | Add TOST equivalence test for LISTA-CP comparison | R1 | P2 | Section 4.8 | Statistical rigor |
| S3 | Discuss time-varying channel limitations | R3 | P3 | Section 5.4 | Completeness |
| S4 | Evaluate structured mappings for scalability | R3 | P3 | Section 4.13 | Practical guidance |
| S5 | Add hard-thresholded OMP as a baseline | DA | P2 | Section 4.1 | Tests whether error concentration can be achieved without LISTA |
| S6 | Consolidate contributions 1, 2, 5 in introduction | EIC | P3 | Section 1 | Tighter narrative |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 5 days)
- [ ] R1: Reframe abstract and highlights to lead with honest limitations
- [ ] R2: Add missing LISTA variant references and discussion
- [ ] R3: Reframe AMP connection as contextualizing existing theory
- [ ] R4: Formalize error concentration metric with equation and CIs
- [ ] R5: Discuss real-valued channel limitation
- [ ] R6: Remove or replace qualitative CNN/Transformer comparison

### Priority 2 — Content Supplementation (Estimated total effort: 3 days)
- [ ] S1: Add scale-invariant loss diagnostic
- [ ] S2: Add TOST equivalence test for LISTA-CP
- [ ] S5: Add hard-thresholded OMP baseline

### Priority 3 — Text and Formatting (Estimated total effort: 2 days)
- [ ] S3: Discuss time-varying channel limitations
- [ ] S4: Evaluate structured mappings
- [ ] S6: Consolidate introduction contributions
- [ ] Language polishing (minor grammar issues from all reviewers)
- [ ] Citation format standardization

### Total Estimated Effort
- **Major Revision**: 2--3 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-06-22 (3 weeks)
- **Basis**: Major Revision, 6 required items with moderate effort
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline

---

## Response Letter Instructions

Please use the standard R→A→C (Reviewer comment → Author response → Change description) format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1--R6)
2. Response for each Suggested Revision (S1--S6) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We appreciate the thorough and honest analysis presented in this manuscript. The experimental methodology is exemplary, and the error concentration mechanism provides genuine insight into LISTA's behavior. However, the framing and literature positioning need substantial revision to accurately represent the contributions and properly contextualize the findings within the existing literature.

We encourage you to carefully consider the reviewers' comments — particularly the consensus issues around framing (R1), literature coverage (R2), and the AMP connection (R3) — and submit a substantially revised manuscript. The revised manuscript will undergo another round of review, focused on whether the required revisions have been adequately addressed.

We look forward to receiving your revised manuscript.

---

## Appendix: Reviewer Score Summary

| Reviewer | Originality | Methodology | Evidence | Coherence | Writing | Weighted Avg | Decision |
|----------|------------|-------------|----------|-----------|---------|-------------|----------|
| EIC | 68 | 82 | 80 | 75 | 78 | 77.0 | Minor |
| R1 (Methodology) | 65 | 78 | 82 | 80 | 76 | 77.0 | Minor |
| R2 (Domain) | 55 | 78 | 65 | 72 | 76 | 66.4 | Major |
| R3 (Perspective) | 62 | 80 | 78 | 78 | 76 | 73.8 | Minor |
| **Panel Average** | **62.5** | **79.5** | **76.3** | **76.3** | **76.5** | **73.6** | **Major Revision** |
