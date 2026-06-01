# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 2

---

## Decision *

### Major Revision

The manuscript presents a systematic evaluation of LISTA for sparse channel estimation. While the experimental framework is comprehensive and the writing is clear, the reviewers have identified critical gaps that must be addressed before the paper can be considered for publication in Digital Signal Processing.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC (Prof. Vasquez) | Journal Editor | Major Revision | 4 |
| Reviewer 1 (Dr. Chen) | Methodology Expert | Major Revision | 5 |
| Reviewer 2 (Prof. Al-Dhahab) | Domain Expert | Major Revision | 5 |
| Reviewer 3 (Dr. Petrov) | Industry Perspective | Major Revision | 4 |
| Devil's Advocate | Logic Auditor | Reject (2 CRITICAL) | — |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-5]** (All reviewers agree):
1. **Missing BER analysis is a critical gap.** All five reviewers (EIC W2, R1 implicit, R2 W1 "Critical", R3 W1 "Critical", DA C1 "CRITICAL") agree that the absence of BER evaluation undermines the paper's practical claims. This is the single most important issue.
2. **The 13-33 dB gap with OMP needs honest discussion.** All reviewers note that the gap is large and its implications for practical systems are inadequately discussed.
3. **The experimental framework is comprehensive and well-designed.** All reviewers commend the breadth of experiments, fair baselines, and honest limitation disclosure.

**[CONSENSUS-4]** (4/5 reviewers agree):
1. **Statistical power is insufficient (n=5 seeds).** R1 (W1), R2 (implicit), R3 (implicit), and DA (M3) agree that the paired t-tests with n=5 have insufficient power. The EIC does not specifically flag this but notes the limited seeds.
2. **LISTA-CP identical results need explanation.** EIC (W4), R1 (W2), and DA (M4) flag this as a concern. R2 and R3 do not specifically address it.
3. **Originality is limited.** EIC (W3), R2 (W3), R3 (implicit), and DA (M1) note that the paper applies a known architecture to a known problem without architectural novelty. R1 focuses on methodology rather than originality.

### Points of Disagreement

**Disagreement 1: Severity of the speed comparison**
- **DA view**: The speed comparison is "CRITICAL" (C2) because it uses unoptimized Python implementations and is meaningless for practical deployment.
- **EIC/R1/R2/R3 view**: The speed comparison is useful as a baseline benchmark, though they acknowledge it could be strengthened with optimized implementations.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The speed comparison is acceptable as a Python-level benchmark but must be caveated. The paper should acknowledge that production implementations would differ and discuss the implications.
- **Resolution Rationale**: The DA's point about unoptimized implementations is valid but does not invalidate the comparison — both methods use the same Python framework, making it a fair relative comparison. However, the "33× faster" claim should be qualified.

**Disagreement 2: Whether SNR-specific training is a meaningful contribution**
- **DA view**: SNR-specific training is "trivially expected" (M2) — any model performs better when trained on the test distribution.
- **EIC/R1/R2/R3 view**: The 6 dB improvement is a useful quantitative finding that provides actionable deployment guidance.
- **Disagreement type**: Significance disagreement
- **Editor's Resolution**: The SNR-specific training result is a valid contribution, though the DA is correct that the mechanism is well-known. The paper should acknowledge this is an application of a known principle (distribution-matched training) and emphasize the quantitative findings (6 dB improvement, range width vs. location) as the contribution.
- **Resolution Rationale**: While the principle is known, the specific quantitative characterization for LISTA in the channel estimation context is informative.

---

## Decision Rationale

The paper presents a comprehensive evaluation of LISTA for sparse channel estimation with 9 well-designed experiments. The writing is clear, the limitations are honestly disclosed, and the ablation study with statistical testing is commendable. However, the paper has three critical issues that prevent acceptance:

1. **Missing BER analysis**: All reviewers agree that the absence of BER evaluation is the most significant gap. The paper's practical claims ("a practical alternative") cannot be substantiated without translating NMSE to BER. This is not a minor omission — it is a fundamental gap for a paper targeting a signal processing journal with a communications application.

2. **Overstated practical claims**: The 13-33 dB gap with OMP at high SNR is substantial (20-2000× in linear scale). Without BER results, the paper cannot demonstrate that LISTA's NMSE is acceptable for practical systems. The "practical alternative" claim needs either BER evidence or significant qualification.

3. **Limited originality**: The paper applies the standard LISTA architecture (2010) without modification. The contribution is analytical (ablation, generalization) rather than methodological. While the ablation insights are valuable, the paper needs to either (a) introduce an architectural contribution, or (b) clearly position itself as a benchmarking study.

The decision is Major Revision rather than Reject because: (a) the experimental framework is sound and comprehensive, (b) the ablation insights (W^(k) significance, threshold non-significance) are genuine contributions, (c) the SNR-specific training results are practically useful, and (d) the paper's honest reporting of limitations builds credibility. With BER analysis, stronger positioning, and the methodological fixes requested by Reviewer 1, the paper could make a solid contribution to DSP.

---

## Required Revisions * (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Add BER simulation (QPSK/16-QAM with MMSE equalizer) | EIC, R2, R3, DA (unanimous) | Critical | Section 4 | 5-7 days |
| R2 | Qualify speed comparison with production implementation discussion | DA (C2), EIC (W1) | Critical | Section 4.7.1 | 1-2 days |
| R3 | Increase ablation seeds to n≥20 or use non-parametric tests | R1 (W1), DA (M3) | Major | Section 4.5 | 2-3 days |
| R4 | Verify and explain LISTA-CP identical results | EIC (W4), R1 (W2), DA (M4) | Major | Section 4.8 | 2-3 days |
| R5 | Expand Related Work (CNN/transformer methods, other DL approaches) | R2 (W2), DA (m3) | Major | Section 2 | 2-3 days |

### Required Item Details

**R1: Add BER Simulation**
- **Problem**: The paper evaluates NMSE but never translates to BER, the ultimate metric for communications systems. All reviewers agree this is the most critical gap.
- **Source**: EIC (W2), R2 (W1 "Critical"), R3 (W1 "Critical"), DA (C1 "CRITICAL")
- **Requirement**: Add a BER vs. SNR simulation using QPSK and/or 16-QAM with an MMSE equalizer. Show BER curves for LISTA, OMP, LASSO, LMS, NLMS. Use the same channel setup as Experiment 1 (N=64, K=5, M=256).
- **Acceptance criteria**: BER curves are presented for at least one modulation scheme. The paper discusses whether LISTA's NMSE is acceptable for the target BER (e.g., 10⁻³ for uncoded systems).

**R2: Qualify Speed Comparison**
- **Problem**: The 33× speedup claim uses unoptimized Python implementations and may not reflect production conditions.
- **Source**: DA (C2), EIC (W1)
- **Requirement**: Add a discussion paragraph in Section 4.7.1 acknowledging that: (a) the comparison uses Python implementations, (b) production C/FPGA implementations would differ, (c) the relative speedup may be smaller or larger depending on implementation quality. Remove or qualify the "33× faster" claim in the abstract and highlights.
- **Acceptance criteria**: The speed comparison is properly caveated. The abstract does not present the 33× figure without qualification.

**R3: Increase Statistical Power**
- **Problem**: Paired t-tests with n=5 have insufficient power (~15-20% for medium effects).
- **Source**: R1 (W1), DA (M3)
- **Requirement**: Either (a) increase the number of seeds to at least 20 for the ablation study, or (b) use Wilcoxon signed-rank test and explicitly acknowledge the power limitation. Report 95% confidence intervals.
- **Acceptance criteria**: The ablation analysis uses either n≥20 seeds or a non-parametric test appropriate for small samples. Confidence intervals are reported.

**R4: Verify LISTA-CP Implementation**
- **Problem**: LISTA and LISTA-CP show identical NMSE across all SNR levels, which is surprising and unexplained.
- **Source**: EIC (W4), R1 (W2), DA (M4)
- **Requirement**: Verify the implementation by (a) printing learned W matrices and checking constraint satisfaction, (b) testing at shallower depths (L=3, 5, 8). If results are confirmed, provide a rigorous explanation. If implementation error is found, fix and re-run.
- **Acceptance criteria**: The paper either (a) provides evidence that the LISTA-CP implementation is correct with a rigorous explanation for identical results, or (b) reports corrected results.

**R5: Expand Related Work**
- **Problem**: The Related Work omits CNN/transformer-based channel estimators and other deep unfolding variants.
- **Source**: R2 (W2), DA (m3)
- **Requirement**: Add a subsection or paragraph covering: (a) CNN-based channel estimators, (b) transformer-based approaches, (c) other LISTA variants (LAMP, OCLISTA, ISTA-Net). Position LISTA within this broader landscape.
- **Acceptance criteria**: The Related Work covers the major approaches to deep learning for channel estimation, not just deep unfolding.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Add depth scaling experiment (L=30, 40, 60) to test saturation explanation | R1 (W3) | P2 | Section 4.4 | Validates/refutes saturation explanation |
| S2 | Discuss complex-valued channel extension | R2 (W4) | P2 | Section 5.3 | Addresses practical applicability |
| S3 | Report training time and data generation cost | R3 (W3), DA (m2) | P2 | Section 4 | Completes the deployment cost picture |
| S4 | Evaluate hybrid LISTA/OMP fallback framework | R3 (W4) | P2 | Section 4/5 | Provides the most promising deployment strategy |
| S5 | Compare against OMP with estimated K (not oracle) | DA (Alternative Path 2) | P3 | Section 4.2 | Fairer comparison |
| S6 | Repeat ablation with SNR-specific training | R1 (W4) | P3 | Section 4.5 | Tests whether non-significance is training-regime-dependent |

---

## Revision Roadmap

### Priority 1 — Critical Revisions (Estimated total effort: 10-15 days)
- [ ] R1: Add BER simulation with QPSK/16-QAM and MMSE equalizer
- [ ] R2: Qualify speed comparison with production implementation discussion
- [ ] R3: Increase ablation seeds to n≥20 or use non-parametric tests
- [ ] R4: Verify and explain LISTA-CP identical results
- [ ] R5: Expand Related Work to cover CNN/transformer/other DL approaches

### Priority 2 — Content Supplementation (Estimated total effort: 5-7 days)
- [ ] S1: Add depth scaling experiment (L=30, 40, 60)
- [ ] S2: Discuss complex-valued channel extension
- [ ] S3: Report training time and data generation cost
- [ ] S4: Evaluate hybrid LISTA/OMP fallback framework

### Priority 3 — Text and Formatting (Estimated total effort: 2-3 days)
- [ ] S5: Compare against OMP with estimated K
- [ ] S6: Repeat ablation with SNR-specific training
- [ ] Fix learning rate discrepancy (10⁻³ vs. 5×10⁻⁴)
- [ ] Standardize citation format
- [ ] Add ± values for deterministic baselines in tables

### Total Estimated Effort
- **Major Revision**: 3-4 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01 (4 weeks)
- **Basis**: Major Revision standard timeline for Digital Signal Processing
- **Extension policy**: If extension is needed, notify the editorial office at least 1 week before the deadline

---

## Response Letter Instructions

Please use the standard revision response format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1-R5)
2. Response for each Suggested Revision (S1-S6) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We encourage you to carefully consider the reviewers' comments and submit a substantially revised manuscript. The reviewers have identified a clear path to improvement: the addition of BER analysis (R1) and the expansion of the Related Work (R5) are the most impactful revisions. The methodological fixes (R3, R4) will strengthen the paper's rigor.

The paper's honest reporting of limitations and comprehensive experimental framework are commendable. With the required revisions, the paper has the potential to make a solid contribution to Digital Signal Processing.

Please note that the revised manuscript will undergo another round of review.

---

## Appendix: Reviewer Reports

The complete reviewer reports are attached separately:
1. `round2_reviewer1_eic.md` — EIC Report (Prof. Vasquez)
2. `round2_reviewer2_methodology.md` — Methodology Report (Dr. Chen)
3. `round2_reviewer3_domain.md` — Domain Report (Prof. Al-Dhahab)
4. `round2_reviewer4_perspective.md` — Perspective Report (Dr. Petrov)
5. `round2_reviewer5_devils_advocate.md` — Devil's Advocate Report
