# Editorial Decision

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 12

---

## Decision

### Minor Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC (Prof. Vasquez) | Editor-in-Chief | Minor Revision | 4/5 | 77/100 |
| Reviewer 1 (Prof. Zhang) | Methodology Expert | Minor Revision | 5/5 | 77/100 |
| Reviewer 2 (Prof. Wei) | Domain Expert | Minor Revision | 5/5 | 75/100 |
| Reviewer 3 (Prof. Rahman) | Cross-Disciplinary Perspective | Minor Revision | 4/5 | 71/100 |
| Devil's Advocate (Prof. Novak) | Stress-Test | N/A (challenge only) | — | — |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All reviewers agree):
1. **Error concentration mechanism is the paper's primary contribution.** All reviewers identify the finding that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP) as the paper's most significant contribution. EIC calls it "the paper's strongest contribution," R1 highlights the "novel domain insight," R2 calls it "genuine domain contribution," and R3 notes its "practical implications for equalizer design." The DA acknowledges it as "a genuinely novel finding" while challenging its practical relevance.

2. **Honest self-assessment is commendable.** All reviewers praise the paper's transparent reporting: admitting LISTA trails OMP by 13–33 dB, acknowledging the NMSE saturation as "likely a training artifact," and self-correcting the 5-seed ablation with 20 seeds. This level of honesty is rare in the field.

3. **BER advantage is limited to ZF equalization.** All reviewers (and the DA) agree that the BER advantage under ZF equalization is the paper's key system-level finding, but that it does not apply under MMSE (the standard). The DA frames this as a critical flaw; the other reviewers view it as a limitation to be acknowledged.

4. **Statistical methodology is strong.** R1 highlights the "statistical power awareness and self-correction," EIC praises the "20 seeds with paired t-tests, Cohen's $d$," and R2 notes the BER simulations use "200 realizations per SNR point—well above the field standard."

**[CONSENSUS-3]** (3/4 reviewers agree):
1. **Hardware claims need measured validation.** R1, R3, and the DA all flag the hardware analysis as theoretical. R3 calls it "entirely theoretical" and rates it Major; the DA calls it "unsubstantiated." EIC acknowledges the concern but rates it Minor. The consensus is that the hardware section should be condensed and clearly labeled as theoretical.

2. **Cross-table inconsistency should be addressed more prominently.** EIC and R1 both flag the 8 dB discrepancy between Tables 3 and 4. EIC suggests "a consolidated table or figure"; R1 suggests "making the sensitivity to training distribution a first-class result." R2 and the DA view it as a methodological concern.

### Points of Disagreement

**Disagreement 1: Severity of ZF-only BER advantage**
- **DA view**: The BER advantage under ZF is a CRITICAL flaw—it renders the paper's primary system-level contribution "practically irrelevant" because no modern system uses ZF equalization.
- **EIC/R1/R2/R3 view**: The ZF-only limitation is a Minor concern to be acknowledged. The mechanism analysis provides genuine insight regardless of the equalizer used.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The DA's challenge is well-argued but overstated. The paper correctly frames the BER contribution as a "mechanism analysis" rather than a practical advantage. The error concentration finding has value independent of the ZF BER results—it explains why deep-unfolded architectures behave differently from greedy methods. The paper should strengthen its discussion of when ZF is relevant (e.g., low-complexity receivers) but need not treat this as a critical flaw.
- **Resolution Rationale**: The paper's contribution is the mechanism insight, not the BER advantage per se. The DA's strongest counter-argument—that no practical system uses ZF—is valid but does not invalidate the mechanism analysis.

**Disagreement 2: LASSO convergence concern**
- **R1 view**: LASSO convergence should be verified (Major concern). 500 ISTA iterations may not converge for all configurations.
- **EIC/R2/R3 view**: LASSO convergence is not flagged as a significant concern.
- **Disagreement type**: Existence disagreement
- **Editor's Resolution**: R1's concern is valid and should be addressed. Adding a convergence check (relative change at iteration 500) is a minor revision that strengthens the methodology.
- **Resolution Rationale**: R1 has the strongest methodological expertise (confidence 5/5) and the concern is easy to address.

---

## Decision Rationale

This paper presents a systematic analysis of LISTA for sparse channel estimation, with the primary contribution being a mechanism analysis demonstrating that LISTA concentrates 99.9% of estimation error on true tap locations. The paper is unusually honest about LISTA's limitations (13–33 dB NMSE gap with OMP) and provides rigorous statistical methodology (20 seeds, paired t-tests, 200 BER realizations).

All four reviewers recommend Minor Revision. The Devil's Advocate raises valid challenges (ZF-only BER advantage, theoretical hardware claims) but these are better characterized as limitations to be acknowledged rather than critical flaws. The DA's strongest counter-argument—that the BER advantage is practically irrelevant under MMSE—is valid but does not invalidate the mechanism analysis, which is the paper's primary contribution.

The key revision items are: (1) condense the hardware analysis and clearly label it as theoretical, (2) add LASSO convergence verification, (3) address the cross-table inconsistency more prominently, (4) discuss when ZF equalization is relevant, and (5) verify reference quality. These are all achievable within a minor revision.

The paper is well-suited for Digital Signal Processing. Its focus on understanding LISTA's behavior (rather than claiming novelty) aligns with the journal's emphasis on rigorous signal processing analysis. The error concentration mechanism is a genuine contribution to the deep unfolding literature.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Condense hardware analysis; clearly label all claims as theoretical | EIC, R3, DA | Major | Section 4.13 | 1 day |
| R2 | Add LASSO convergence verification (relative change at iteration 500) | R1 | Major | Section 4.1 | 0.5 days |
| R3 | Add discussion of when ZF equalization is relevant in practice | EIC, DA | Major | Section 5.1 | 0.5 days |
| R4 | Address cross-table inconsistency more prominently (consolidated table or figure) | EIC, R1 | Major | Section 4.3 | 1 day |
| R5 | Verify and correct reference quality issues (placeholder page numbers, unreferenced entries) | R2 | Major | References | 0.5 days |

### Required Item Details

**R1: Condense Hardware Analysis**
- **Problem**: The hardware analysis (Section 4.13) devotes significant space to theoretical FLOP counts and pipeline analysis without measured results. The DA and R3 both flag this as insufficiently substantiated.
- **Source**: R3 (Major), DA (Major), EIC (Minor)
- **Requirement**: Condense to a single table (FLOP counts) and 1-2 paragraphs. Remove the detailed pipeline throughput analysis. Add a clear disclaimer that all hardware claims are theoretical.
- **Acceptance criteria**: The hardware section should be no longer than 1 page, with all claims explicitly labeled as theoretical.

**R2: LASSO Convergence Verification**
- **Problem**: LASSO uses 500 ISTA iterations (Section 4.1) without convergence verification. R1 (methodology expert, confidence 5/5) flags this as a potential validity concern.
- **Source**: R1 (Major)
- **Requirement**: Report the relative change $\|\mathbf{h}^{(k)} - \mathbf{h}^{(k-1)}\| / \|\mathbf{h}^{(k)}\|$ at iteration 500 for representative configurations (e.g., SNR=20, SNR=40). If convergence is not achieved, increase iterations or switch to FISTA.
- **Acceptance criteria**: The paper either confirms LASSO convergence or reports results with a converged solver.

**R3: Discuss ZF Equalization Relevance**
- **Problem**: The DA's strongest counter-argument is that ZF equalization is not used in practice. The paper should address this directly.
- **Source**: DA (CRITICAL), EIC (Minor)
- **Requirement**: Add 1-2 paragraphs in Section 5.1 discussing practical scenarios where ZF is relevant: (1) low-complexity IoT receivers, (2) when MMSE noise variance estimation is unreliable, (3) as a theoretical baseline for understanding error structure. Acknowledge that MMSE is the standard and the BER advantage is specific to ZF.
- **Acceptance criteria**: The discussion should be balanced—acknowledging ZF's limited practical use while explaining why the mechanism analysis is still valuable.

**R4: Address Cross-Table Inconsistency**
- **Problem**: Tables 3 and 4 report LISTA NMSE of -24.25 and -32.29 dB for the same nominal configuration, differing by 8 dB. While explained in a footnote, this may confuse readers.
- **Source**: EIC (Minor), R1 (Minor)
- **Requirement**: Add a consolidated figure or table showing LISTA performance under both training protocols side-by-side. Make the sensitivity to training distribution a first-class result rather than a footnote caveat.
- **Acceptance criteria**: The cross-table inconsistency should be visible in a figure or consolidated table, with clear explanation in the main text.

**R5: Verify Reference Quality**
- **Problem**: Several references have issues: Kim et al. (2021) has placeholder page numbers ("123456--123470"); some bibliography entries (Soltani 2019, Guo 2020, Farsad 2021, Liu 2020) are not cited in the text.
- **Source**: R2 (Minor), EIC (Minor)
- **Requirement**: Verify all references. Correct the Kim et al. page numbers. Either cite unreferenced entries in the text or remove them from the bibliography.
- **Acceptance criteria**: All bibliography entries should be cited in the text, and all page numbers should be verified.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Add OMP with estimated K (e.g., cross-validation or BIC) | R1 | P2 | Section 4.1 | Strengthens comparison fairness |
| S2 | Discuss memory bandwidth implications for hardware | R3 | P2 | Section 4.13 | Addresses deployment concerns |
| S3 | Add at least one additional ITU channel model | R2, DA | P2 | Section 4.7.2 | Strengthens generalization claim |
| S4 | Add brief discussion of online adaptation for time-varying channels | R3, DA | P3 | Section 5.4 | Addresses practical deployment gap |
| S5 | Report 95% confidence intervals for BER differences | R1 | P3 | Section 4.10 | Improves statistical reporting |
| S6 | Add discussion of structured sparsity (block sparsity) | R2 | P3 | Section 5.4 | Broadens applicability discussion |
| S7 | Report spectral norm distribution across layers for LISTA-CP | R1, EIC | P3 | Section 4.8 | Strengthens LISTA-CP analysis |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 3-4 days)
- [ ] R1: Condense hardware analysis to 1 page, label as theoretical
- [ ] R2: Add LASSO convergence verification
- [ ] R3: Add discussion of ZF equalization relevance
- [ ] R4: Add consolidated figure for cross-table inconsistency
- [ ] R5: Verify and correct all references

### Priority 2 — Content Supplementation (Estimated total effort: 2-3 days)
- [ ] S1: Add OMP with estimated K
- [ ] S2: Discuss memory bandwidth implications
- [ ] S3: Add additional ITU channel model (if feasible)

### Priority 3 — Text and Formatting (Estimated total effort: 1-2 days)
- [ ] S4: Add discussion of online adaptation
- [ ] S5: Add 95% confidence intervals for BER
- [ ] S6: Add discussion of structured sparsity
- [ ] S7: Report spectral norm distribution for LISTA-CP
- [ ] Minor language and formatting issues from all reviewers

### Total Estimated Effort
- **Minor Revision**: 6-9 days

---

## Revision Deadline

- **Recommended deadline**: 2026-07-15 (6 weeks)
- **Basis**: Minor Revision — 4-6 weeks standard for DSP
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1-R5)
2. Response for each Suggested Revision (S1-S7) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The reviewers have identified the error concentration mechanism as the paper's primary contribution and have praised the honest, self-critical approach. The revisions focus on strengthening the hardware analysis claims, verifying LASSO convergence, and addressing the practical relevance of the ZF equalization results.

We look forward to receiving your revision within 6 weeks.

---

## Appendix: Reviewer Dimension Scores Summary

| Dimension | EIC | R1 | R2 | R3 | Average |
|-----------|-----|----|----|-----|---------|
| Originality (20%) | 72 | 68 | 70 | 68 | 69.5 |
| Methodological Rigor (25%) | 78 | 80 | 75 | 72 | 76.3 |
| Evidence Sufficiency (25%) | 70 | 72 | 68 | 65 | 68.8 |
| Argument Coherence (15%) | 82 | 80 | 80 | 78 | 80.0 |
| Writing Quality (15%) | 85 | 82 | 82 | 80 | 82.3 |
| **Weighted Average** | **76.6** | **76.8** | **74.6** | **71.4** | **74.9** |

**Decision Threshold**: Weighted average 65-79 → Minor Revision ✓

---

## Appendix: Devil's Advocate Challenge Summary

| Severity | Count | Key Issues |
|----------|-------|------------|
| CRITICAL | 2 | BER advantage limited to ZF; generalization claim based on only 2 ITU models |
| MAJOR | 5 | Selective emphasis on ZF; training sensitivity; hardware claims unsubstantiated; LISTA-CP straw man; saturation may be architectural |
| MINOR | 5 | Single configuration; no time-varying channels; SNR mitigation overstated; ablation design concern; Python speedup misleading |

**DA CRITICAL Issues Resolution**:
- **C1 (ZF-only BER advantage)**: Addressed by Required Revision R3 — add discussion of ZF relevance. The mechanism analysis has value independent of the ZF BER results.
- **C2 (Generalization from 2 ITU models)**: Addressed by Suggested Revision S3 — add additional ITU channel model. The paper already acknowledges this limitation in Section 4.12.5.

Per Checkpoint Rule #4, the DA CRITICAL issues prevent an Accept decision. The Minor Revision decision appropriately reflects these concerns.

---

## Appendix: Full Reviewer Reports

The complete reviewer reports are attached separately:
1. `round12_eic_report.md` — EIC Review (Prof. Vasquez)
2. `round12_methodology_report.md` — Methodology Review (Prof. Zhang)
3. `round12_domain_report.md` — Domain Review (Prof. Wei)
4. `round12_perspective_report.md` — Perspective Review (Prof. Rahman)
5. `round12_devils_advocate_report.md` — Devil's Advocate Review (Prof. Novak)
