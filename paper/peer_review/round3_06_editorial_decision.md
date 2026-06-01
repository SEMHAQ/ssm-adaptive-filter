# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 3

---

## Decision *

### Minor Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC (Prof. Vasquez) | Journal Editor | Minor Revision | 4/5 |
| Reviewer 1 (Dr. Chen) | Methodology Expert | Major Revision | 5/5 |
| Reviewer 2 (Prof. Wei) | Domain Expert | Minor Revision | 4/5 |
| Reviewer 3 (Dr. Kim) | Cross-Disciplinary / Hardware | Minor Revision | 4/5 |
| Devil's Advocate (Dr. Torres) | Core Argument Challenge | — (see DA report) | — |

**Score Summary:**

| Reviewer | Weighted Score | Decision Mapping |
|----------|---------------|-----------------|
| EIC | 67.6 | Minor Revision |
| Reviewer 1 | 63.6 | Major Revision |
| Reviewer 2 | 67.6 | Minor Revision |
| Reviewer 3 | 65.0 | Minor Revision |
| **Panel Average** | **66.0** | **Minor Revision** |

---

## Consensus Analysis *

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All 4 reviewers + DA agree):
1. **The ablation study with 20 seeds is excellent.** EIC: "commends the statistical rigor"; R1: "sets a good standard"; R2: "exemplary"; R3: "the best-validated part of the paper"; DA: "genuinely excellent." All reviewers agree this is the paper's methodological highlight.
2. **The BER-NMSE disconnect is the most important finding but needs more rigorous support.** EIC: "the paper's most important claim and its weakest link"; R1: "lacks mechanism analysis"; R2: "needs strengthening"; R3: "bridges the theory-practice gap but needs validation"; DA: "statistically unvalidated and mechanismally unexplained." Unanimous agreement that this finding is valuable but insufficiently substantiated.
3. **The paper honestly reports limitations.** All reviewers commend the transparent reporting of N=256 divergence, Python-only speed caveat, and 13–33 dB NMSE gap.

**[CONSENSUS-3]** (3/4 reviewers agree):
1. **The 33× speedup claim needs hardware validation.** R1, R3, and DA flag this as a significant concern; R2 notes it but considers it less critical. The consensus is that Python-only timing is insufficient for a paper emphasizing practical deployment.
2. **MMSE equalization results are needed.** EIC, R1, and DA request MMSE results; R2 and R3 note it as minor. The consensus is that ZF-only BER is a limitation.

### Points of Disagreement

**Disagreement 1: Severity of the BER statistical gap**
- **R1 view**: Critical—the BER analysis "lacks the methodological rigor of the NMSE experiments" and the "better BER" claim may be noise. Recommends Major Revision.
- **EIC/R2/R3 view**: Important but addressable—the BER finding is novel and valuable; with statistical testing it can be substantiated. Recommend Minor Revision.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The BER gap is important but not fatal. The finding is plausible (LISTA's soft-thresholding does enforce sparsity, which should help ZF equalization), and the statistical testing required is straightforward (paired t-tests, more seeds). Minor Revision is appropriate.
- **Resolution Rationale**: R1's expertise in statistical validation is acknowledged, but the required fix is concrete and achievable within a minor revision timeframe.

**Disagreement 2: Importance of hardware validation**
- **R3 view**: Major—the "entire practical deployment narrative hinges on" the Python speed number.
- **R2 view**: Minor—the paper already cites Wei et al. (2022) for FPGA evidence.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The Python caveat is already acknowledged in the paper. The authors should add a theoretical hardware complexity analysis (operation counts, parallelism characteristics) but are not required to provide FPGA measurements. This is a Major suggestion, not a required revision.

---

## Decision Rationale *

The panel reaches a consensus that this manuscript makes a genuine contribution to the understanding of deep unfolding for sparse channel estimation. The ablation study with 20 seeds and proper statistical testing is methodologically exemplary. The BER-NMSE disconnect finding is novel and practically significant, though it requires additional validation.

The decision is Minor Revision rather than Major Revision for the following reasons: (1) The required changes are concrete and achievable—statistical testing of BER results, mechanism analysis of the BER-NMSE disconnect, and MMSE equalization experiments. (2) The paper's core contribution (systematic analysis of LISTA) is sound and well-executed. (3) The limitations are honestly reported and do not undermine the paper's validity. (4) The Devil's Advocate's CRITICAL issues (BER statistical significance, BER-NMSE mechanism) are addressable within the revision scope.

The decision is Minor Revision rather than Accept because: (1) The DA's CRITICAL issues must be addressed before publication—the BER claim is the paper's centerpiece and must be statistically validated. (2) The MMSE equalization gap is a significant omission for a paper claiming practical relevance. (3) The "33× faster" claim needs at least theoretical hardware analysis.

---

## Required Revisions * (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | BER statistical validation | R1, DA (C1) | Critical | Section 4.10 | 3–5 days |
| R2 | BER-NMSE mechanism analysis | EIC (W2), DA (C2) | Critical | Section 4.10, 5.1 | 5–7 days |
| R3 | MMSE equalization results | EIC, R1 (W4) | Major | Section 4.10 | 2–3 days |
| R4 | Hardware complexity analysis | R3 (W1), DA (M1) | Major | Section 4.7.1 | 2–3 days |

### Required Item Details

**R1: BER Statistical Validation**
- **Problem**: BER results (Tables 10–11) report mean ± std over 5 seeds but no statistical tests. The "competitive" and "better" BER claims are not statistically validated. At high SNR, LISTA and OMP BER values overlap within 1 standard deviation.
- **Source**: R1 (W1, Critical): "The BER analysis is the paper's most novel finding. If the 'better BER' claim is not statistically significant, the paper's main contribution collapses." DA (C1): "Without paired t-tests or confidence intervals, the reader cannot distinguish signal from noise."
- **Requirement**: (1) Add paired t-tests between LISTA and OMP BER at each SNR point for both QPSK and 16-QAM. (2) Increase channel realizations per SNR point from 50 to at least 200. (3) Report 95% confidence intervals. (4) If differences are not statistically significant, revise claims accordingly (e.g., "LISTA achieves BER comparable to OMP" instead of "better BER").
- **Acceptance criteria**: All BER comparison claims are supported by p-values. If "better BER" cannot be substantiated, the claim is downgraded to "comparable BER."

**R2: BER-NMSE Mechanism Analysis**
- **Problem**: The explanation for the BER-NMSE disconnect—"more favorable error structure"—is an untested hypothesis. No quantitative analysis of what makes LISTA's error structure "more favorable."
- **Source**: EIC (W2, Critical): "The paper's most important claim and its weakest link." DA (C2): "The reader learns *that* LISTA has better BER but not *why*."
- **Requirement**: Add a diagnostic section that measures: (1) Support set recovery accuracy (Jaccard index or F1 score between estimated and true non-zero tap locations) for LISTA vs. OMP. (2) The sparsity of estimation errors (what fraction of LISTA's error energy is on true tap locations vs. spread across all taps). (3) If feasible, the equalizer's noise enhancement factor. Present as a new subsection (e.g., "4.11 Diagnostic Analysis of BER-NMSE Disconnect").
- **Acceptance criteria**: The paper provides at least two quantitative metrics explaining why LISTA achieves better BER despite worse NMSE.

**R3: MMSE Equalization Results**
- **Problem**: All BER results use zero-forcing equalization. Modern systems use MMSE. The BER advantage may not hold for MMSE.
- **Source**: R1 (W4): "If the BER advantage only holds for ZF equalization, the practical relevance is limited." EIC (W3): "Add BER results with MMSE equalization for at least QPSK."
- **Requirement**: Add BER results with MMSE equalization for QPSK (and 16-QAM if feasible) at the same SNR points as Tables 10–11. Compare LISTA, OMP, and LASSO.
- **Acceptance criteria**: MMSE BER results are reported. If the advantage does not hold for MMSE, this is discussed as a limitation.

**R4: Hardware Complexity Analysis**
- **Problem**: The "33× faster" claim is Python-only. The paper's practical deployment narrative is built on this number without hardware evidence.
- **Source**: R3 (W1): "The entire practical deployment narrative hinges on this number." DA (M1): "In optimized C++ or hardware, the gap may be much smaller."
- **Requirement**: Add a theoretical hardware complexity analysis comparing LISTA and OMP: (1) Operation counts per inference (FLOPs). (2) Parallelism characteristics (LISTA's fixed computation graph vs. OMP's dynamic support set). (3) Memory access patterns. (4) Reference to Wei et al. (2022) FPGA results for LISTA and any available FPGA OMP results. Present as a paragraph in Section 4.7.1 or a new subsection.
- **Acceptance criteria**: The paper provides a complexity analysis that supports or qualifies the "33× faster" claim with operation counts, not just Python timing.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | ITU BER results | R1, R2, DA (M3) | P2 | Section 4.10 | Confirms BER advantage on realistic channels |
| S2 | Pilot overhead analysis | R2 (W2) | P2 | New experiment | Characterizes M/N trade-off |
| S3 | Correlated tap channel experiments | R2 (W1) | P2 | Section 4.6 | Strengthens generalization claims |
| S4 | Positioning table vs. prior work | EIC (W1) | P3 | Introduction | Clarifies novelty |
| S5 | Online/incremental deployment discussion | R3 (W3) | P3 | Section 5.3 | Addresses retraining cost |

---

## Revision Roadmap *

### Priority 1 — Critical Revisions (Estimated total effort: 12–18 days)
- [ ] R1: BER statistical validation — add paired t-tests, increase realizations, report CIs (3–5 days)
- [ ] R2: BER-NMSE mechanism analysis — support set recovery, error sparsity analysis (5–7 days)
- [ ] R3: MMSE equalization results — add MMSE BER for QPSK and 16-QAM (2–3 days)
- [ ] R4: Hardware complexity analysis — FLOPs, parallelism, memory access (2–3 days)

### Priority 2 — Content Supplementation (Estimated total effort: 5–7 days)
- [ ] S1: ITU BER results at SNR=20 dB (1–2 days)
- [ ] S2: Pilot overhead analysis (M=64, 128, 256, 512) (2–3 days)
- [ ] S3: Correlated tap channel experiments (exponential PDP) (2–3 days)

### Priority 3 — Text and Formatting (Estimated total effort: 2–3 days)
- [ ] S4: Add positioning table vs. prior deep-learning-for-channel-estimation work
- [ ] S5: Add brief discussion of retraining cost and online deployment
- [ ] Revise "33× faster" claims to include "Python" qualifier or theoretical analysis
- [ ] Vary "counterintuitive" phrasing (appears multiple times)
- [ ] Add DOIs to references where available

### Total Estimated Effort
- **Minor Revision**: 3–4 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01 (4 weeks)
- **Basis**: Minor revision with 4 required items, all achievable within the timeframe
- **Extension policy**: If extension is needed, notify the editor 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to address every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1–R4)
2. Response for each Suggested Revision (S1–S5: adopted or reason for not adopting)
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs for each revision

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The panel agrees that the paper makes a genuine contribution to understanding deep unfolding for sparse channel estimation, particularly the ablation study and the BER-NMSE disconnect finding. The required revisions focus on strengthening the BER analysis with statistical validation and mechanism explanation, which will significantly enhance the paper's impact.

We look forward to receiving your revision within 4 weeks.

---

## Appendix: Score Summary by Dimension

| Dimension | EIC | R1 (Methodology) | R2 (Domain) | R3 (Perspective) |
|-----------|-----|-------------------|-------------|-------------------|
| Originality (20%) | 55 | 52 | 55 | 50 |
| Methodological Rigor (25%) | 72 | 65 | 70 | 70 |
| Evidence Sufficiency (25%) | 68 | 62 | 68 | 64 |
| Argument Coherence (15%) | 70 | 68 | 70 | 68 |
| Writing Quality (15%) | 75 | 74 | 76 | 74 |
| Literature Integration | — | — | 70 | — |
| Significance & Impact | — | — | — | 62 |
| **Weighted Average** | **67.6** | **63.6** | **67.6** | **65.0** |
| **Decision Mapping** | Minor | Major | Minor | Minor |
