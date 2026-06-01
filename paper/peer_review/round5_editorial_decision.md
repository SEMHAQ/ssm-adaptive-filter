# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 5

---

## Decision

### Major Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC | Journal Editor-in-Chief | Minor Revision | 4 | 70/100 |
| Reviewer 1 | Methodology Expert | Major Revision | 5 | 65/100 |
| Reviewer 2 | Domain Expert (Sparse Channel Estimation) | Minor Revision | 5 | 70/100 |
| Reviewer 3 | Cross-Disciplinary (Hardware Deployment) | Minor Revision | 4 | 69/100 |
| Devil's Advocate | Stress-Test Reviewer | Major Revision | 4 | — |

**Weighted Average Score**: 68.4/100 → Major Revision (threshold: 50–64 = Major, 65–79 = Minor)

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All 4 reviewers agree):
1. **The BER-NMSE mechanism analysis is the paper's strongest contribution.** EIC: "The three-mechanism analysis is well-designed and provides genuine insight." R1: "The error sparsity analysis is the paper's most insightful result." R2: "This insight is valuable for the broader community." R3: "The BER-NMSE disconnect is a systems-level insight that changes the algorithm selection calculus."
2. **The ablation study with 20 seeds is exemplary.** EIC: "The progression from 5-seed to 20-seed ablation is commendable." R1: "This is the gold standard for ablation studies." R2: "The effect sizes are compelling." R3: "This level of ablation rigor is rare."
3. **The paper is honest about LISTA's limitations.** All reviewers commend the transparent reporting of NMSE saturation, diverged seeds, and cross-table inconsistencies.

**[CONSENSUS-3]** (3 of 4 reviewers agree):
1. **The abstract is too long and dense.** EIC, R1, and R3 recommend trimming the abstract to ~200 words. R2 does not comment on abstract length but notes the highlights are dense.
2. **The hardware claims need qualification.** EIC, R1, and R3 note that the $4.4\times$ throughput advantage is a theoretical estimate, not a measured result. R2 does not focus on hardware but agrees the claims should be qualified. R3 is the most concerned, rating this as Major severity.
3. **The MMSE equalization analysis is insufficient.** EIC and R1 explicitly request a full SNR sweep for MMSE. R3 agrees this is needed for the deployment argument. R2 does not comment on MMSE specifically but notes the ITU channel validation is limited.

### Points of Disagreement

**Disagreement 1: Overall severity — Minor vs. Major Revision**
- **EIC view**: Minor Revision. The paper's contributions (BER mechanism, ablation rigor) outweigh its weaknesses. The issues are addressable in 2–4 weeks.
- **R1 view**: Major Revision. The seed count inconsistency in BER analysis (3 vs. 5 seeds) is a Critical methodological issue that undermines the central claim. The LISTA-CP identical results are also Critical.
- **R2 view**: Minor Revision. The domain contribution is solid. The LISTA-CP issue needs investigation but is not fatal.
- **R3 view**: Minor Revision. The hardware analysis is theoretical but well-structured. The gaps are addressable.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: Major Revision. R1's methodological concerns (seed count inconsistency, LISTA-CP verification) are well-founded and affect the paper's central claims. The Devil's Advocate's CRITICAL finding about the BER advantage being ZF-specific further supports a Major Revision. The issues are addressable but require substantial additional experiments (MMSE full sweep, QPSK with 5 seeds, LISTA-CP verification).
- **Resolution Rationale**: The seed count inconsistency directly affects the paper's central claim ("comparable BER for QPSK"). With only 3 seeds, the $t$-test has $\sim$10\% power — the "comparable" claim may be a false negative. This must be resolved before publication. The LISTA-CP identical results raise implementation integrity concerns that require verification. These are not minor polish issues but fundamental to the paper's validity.

**Disagreement 2: LISTA-CP severity — Critical vs. Major vs. Minor**
- **R1 view**: Critical. The identical results are "statistically implausible" and suggest an implementation issue.
- **R2 view**: Major. The analysis needs deeper investigation but may be explainable by the problem setup.
- **DA view**: Critical. The identical results are a "data-conclusion mismatch" that undermines the finding.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: Major. While R1's concern is valid, the identical results are plausible if the weight clipping never activates (which the paper claims). The resolution requires verification (training logs showing spectral norms), not necessarily new experiments. Downgrade from Critical to Major with the requirement that the authors verify the implementation and provide training logs.

**Disagreement 3: Python speedup emphasis**
- **R3 view**: The $33\times$ Python speedup should be de-emphasized; it is misleading.
- **EIC view**: The caveat is already present; the issue is minor.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: Accept R3's recommendation. De-emphasize the Python speedup in the abstract and highlights. Replace with the hardware throughput advantage ($4.4\times$) as the primary speed metric. The Python benchmark can remain in the main text with appropriate framing.

---

## Decision Rationale

This paper provides a systematic analysis of LISTA for sparse channel estimation, with the BER-NMSE mechanism analysis as its strongest contribution. The ablation study with 20 seeds and the practical deployment framework are also valuable. The paper is honest about LISTA's limitations, which is commendable.

However, two methodological issues require resolution before publication: (1) the BER analysis uses inconsistent seed counts (3 for QPSK, 5 for 16-QAM), which affects the statistical power of the QPSK comparison — the paper's central "comparable BER" claim may be a false negative; (2) the LISTA-CP comparison shows suspiciously identical results that require implementation verification. Additionally, the Devil's Advocate correctly identifies that the BER advantage is primarily a ZF equalization artifact that largely vanishes under MMSE — this distinction must be made explicit throughout the paper.

The decision is Major Revision rather than Minor because the seed count inconsistency affects the paper's central claim and requires re-running experiments. The LISTA-CP verification requires training logs, which is a moderate effort. The MMSE full sweep requires additional experiments. These are addressable in 4–6 weeks.

The decision is not Reject because: (1) the paper's core contributions (BER mechanism, ablation rigor, deployment framework) are genuine and valuable; (2) the issues are methodological (fixable with additional experiments) rather than fundamental (invalidating the approach); (3) the paper's honesty about limitations demonstrates scientific integrity.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source | Severity | Section | Estimated Effort |
|---|--------------|--------|----------|---------|-----------------|
| R1 | Re-run QPSK BER analysis with 5 seeds (matching 16-QAM) and report updated $p$-values | R1 | Critical | Table 8, Section 4.10 | 2 days |
| R2 | Verify LISTA-CP implementation: provide training logs showing spectral norm $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ at each epoch; confirm whether clipping gradient was ever non-zero | R1, DA | Critical | Section 4.8 | 1 day |
| R3 | Add full SNR sweep (0–30 dB, step 5 dB) for MMSE equalization with both QPSK and 16-QAM; report paired $t$-tests | R1, EIC, DA | Major | Table 11, Section 4.10 | 3 days |
| R4 | Explicitly qualify the BER advantage as ZF-specific in the abstract, highlights, and conclusion; note that under MMSE, LISTA's primary advantage is throughput with no BER penalty | DA, EIC | Major | Abstract, Highlights, Conclusion | 1 day |
| R5 | Report mean $\pm$ std for all baselines (OMP, LASSO) in Tables 2–4; include paired $t$-tests for LISTA vs. OMP at each NMSE condition | R1 | Major | Tables 2–4 | 2 days |

### Required Item Details

**R1: QPSK BER with 5 Seeds**
- **Problem**: Table 8 uses 3 seeds while Table 9 uses 5 seeds, creating inconsistent statistical power. With 3 seeds, the paired $t$-test has $\sim$10% power for medium effects.
- **Source**: R1 (Critical), "this undermines the paper's central claim that LISTA achieves 'comparable BER' for QPSK"
- **Requirement**: Re-run the QPSK BER simulation with 5 seeds (same as 16-QAM). Report updated mean, std, and $p$-values.
- **Acceptance criteria**: Table 8 reports "Mean $\pm$ std over 5 seeds" and $p$-values are recalculated.

**R2: LISTA-CP Verification**
- **Problem**: LISTA and LISTA-CP show identical NMSE at all SNR points (Table 12), with "maximum per-parameter difference = 0." This is statistically implausible for independently trained models.
- **Source**: R1 (Critical), DA (Critical)
- **Requirement**: Verify the implementation by providing: (a) training logs showing $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ at each epoch for LISTA-CP, (b) confirmation of whether the clipping gradient was ever non-zero, (c) results with different random seeds.
- **Acceptance criteria**: Either (a) the identical results are confirmed with evidence (training logs), or (b) the discrepancy is identified and corrected.

**R3: MMSE Full SNR Sweep**
- **Problem**: Table 11 compares ZF and MMSE at only 2 SNR points (10 and 20 dB). This is insufficient to support claims about MMSE robustness.
- **Source**: R1 (Major), EIC (Major), DA (Major)
- **Requirement**: Provide MMSE BER for all SNR points (0–30 dB, step 5 dB) for both QPSK and 16-QAM. Report paired $t$-tests for LISTA vs. OMP under MMSE.
- **Acceptance criteria**: A complete MMSE BER table with $p$-values at each SNR point.

**R4: ZF Qualification in Abstract/Highlights**
- **Problem**: The abstract and highlights present the BER advantage as a general finding, not a ZF-specific one.
- **Source**: DA (Critical: "the BER advantage claim is ZF-specific but presented as general"), EIC (Major)
- **Requirement**: Revise the abstract and highlights to explicitly state that the BER advantage is primarily under ZF equalization. Under MMSE, LISTA's primary advantage is the 4.4$\times$ hardware throughput with no BER penalty.
- **Acceptance criteria**: The abstract contains the phrase "under ZF equalization" or equivalent when discussing BER advantage.

**R5: Baseline Error Bars in NMSE Tables**
- **Problem**: Tables 2–4 report LISTA mean $\pm$ std but not baseline error bars, preventing statistical comparison.
- **Source**: R1 (Major)
- **Requirement**: Report mean $\pm$ std for OMP and LASSO in Tables 2–4. Include paired $t$-tests for LISTA vs. OMP at each condition.
- **Acceptance criteria**: All NMSE tables report error bars for all methods and $p$-values for LISTA vs. OMP.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source | Priority | Section | Expected Improvement |
|---|--------------|--------|----------|---------|---------------------|
| S1 | Trim abstract to ~200 words; remove specific FLOP counts, parameter counts, pipeline stages | EIC | P2 | Abstract | Improved readability |
| S2 | Qualify hardware throughput as "theoretical estimate" or "projected" in abstract and highlights | EIC, R3 | P2 | Abstract, Highlights | Accurate representation |
| S3 | Add comparison with OMP using estimated $K$ (via cross-validation) to quantify practical cost of not knowing $K$ | R3 | P2 | Section 4.1 | Stronger LISTA advantage claim |
| S4 | Test on additional channel models (correlated taps, non-exponential PDP) beyond ITU PedA/VehA | R2 | P2 | Section 4.7.2 | Stronger generalization claim |
| S5 | Add brief power consumption estimate for LISTA vs. OMP on FPGA | R3 | P3 | Section 4.13 | Complete hardware analysis |
| S6 | Report LISTA output sparsity (number of non-zero taps) to support "enforces sparsity" claim | DA | P3 | Section 4.12 | Stronger mechanism claim |
| S7 | Discuss training cost and model storage requirements for SNR-specific training | R3 | P3 | Section 5.2 | Complete deployment analysis |
| S8 | Add discussion of whether findings extend to complex-valued channels | R2 | P2 | Section 5.3 | Broader applicability |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 8–10 days)
- [ ] R1: Re-run QPSK BER with 5 seeds; update Table 8 and $p$-values (2 days)
- [ ] R2: Verify LISTA-CP implementation; provide training logs (1 day)
- [ ] R3: Run MMSE full SNR sweep for QPSK and 16-QAM; create new table (3 days)
- [ ] R4: Revise abstract, highlights, and conclusion to qualify BER advantage as ZF-specific (1 day)
- [ ] R5: Add baseline error bars and $p$-values to Tables 2–4 (2 days)

### Priority 2 — Content Supplementation (Estimated total effort: 4–5 days)
- [ ] S1: Trim abstract to ~200 words (0.5 day)
- [ ] S2: Add "theoretical estimate" qualifiers to hardware claims (0.5 day)
- [ ] S3: Add OMP with estimated $K$ comparison (1 day)
- [ ] S4: Add 1–2 additional channel model experiments (2 days)
- [ ] S8: Add complex-valued channel discussion (0.5 day)

### Priority 3 — Text and Formatting (Estimated total effort: 1–2 days)
- [ ] S5: Add power consumption estimate (0.5 day)
- [ ] S6: Report LISTA output sparsity (0.5 day)
- [ ] S7: Add training cost discussion (0.5 day)
- [ ] Address minor issues from all reviewers (language, terminology, figures)

### Total Estimated Effort
- **Major Revision**: 13–17 days (approximately 3 weeks)

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01 (4 weeks from decision)
- **Basis**: Major Revision with 5 required items requiring additional experiments
- **Extension policy**: If extension is needed, notify the editor by 2026-06-22

---

## Response Letter Instructions

Please use the R→A→C (Reviewer comment → Author response → Change description) format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1–R5)
2. Response for each Suggested Revision (S1–S8) — either adopted with description, or reason for not adopting
3. Change markup: mark all changes in the revised manuscript with blue text or track changes
4. Cross-reference table: old page/paragraph → new page/paragraph for each change

---

## Closing

We encourage you to carefully consider the reviewers' comments and submit a substantially revised manuscript. The paper's core contributions — particularly the BER-NMSE mechanism analysis and the rigorous ablation study — are valuable additions to the literature. The required revisions address methodological concerns that, once resolved, will significantly strengthen the paper's claims.

We look forward to receiving your revised manuscript within the recommended deadline.

---

## Appendix: Reviewer Score Summary

| Dimension | EIC | R1 | R2 | R3 | Average |
|-----------|-----|----|----|-----|---------|
| Originality (20%) | 62 | 58 | 60 | 64 | 61.0 |
| Methodological Rigor (25%) | 74 | 62 | 72 | 70 | 69.5 |
| Evidence Sufficiency (25%) | 72 | 65 | 68 | 66 | 67.8 |
| Argument Coherence (15%) | 70 | 68 | 73 | 72 | 70.8 |
| Writing Quality (15%) | 73 | 74 | 75 | 74 | 74.0 |
| **Weighted Total** | **70.3** | **64.6** | **69.9** | **68.9** | **68.4** |

### Devil's Advocate Critical Findings

| # | Finding | EIC Assessment | Required Response |
|---|---------|---------------|-------------------|
| C1 | BER advantage is ZF-specific but presented as general | Valid — requires explicit ZF qualification | R4: Revise abstract/highlights/conclusion |
| C2 | LISTA-CP identical results suspicious | Valid — requires implementation verification | R2: Provide training logs |

**Note**: Per Checkpoint Rule #4, the Devil's Advocate found CRITICAL issues, so the Editorial Decision cannot be Accept. The decision is Major Revision, consistent with this rule.
