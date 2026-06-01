# Editorial Decision

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Submission Date**: 2026-05-15
- **Decision Date**: 2026-06-01
- **Review Round**: Round 4

---

## Decision *

### Minor Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| EIC | Prof. Dr. Elena Morozova, Editor-in-Chief, *Digital Signal Processing* | Minor Revision | 4 |
| Reviewer 1 | Prof. Kai Zhang, Associate Professor, Tsinghua University (Methodology) | Minor Revision | 5 |
| Reviewer 2 | Prof. Dr. Xiaohan Chen, Associate Professor, Zhejiang University (Domain) | Minor Revision | 5 |
| Reviewer 3 | Dr. Ing. Marcus Weber, Senior Research Engineer, Nokia Bell Labs (Perspective) | Minor Revision | 4 |
| Devil's Advocate | Stress-test reviewer | N/A (challenge-only) | N/A |

---

## Consensus Analysis *

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All reviewers agree):
1. **BER-NMSE disconnect is the paper's strongest contribution.** All reviewers acknowledge that the finding—LISTA achieves comparable or better BER despite 13–33 dB worse NMSE—is genuinely insightful. The mechanism analysis (99.9% error concentration on true taps) provides new understanding of what makes channel estimators effective for equalization.
2. **Ablation study is methodologically sound.** The progression from 5-seed to 20-seed ablation with paired t-tests and Cohen's d is praised by all reviewers as exemplary statistical practice.
3. **Paper is well-written and well-organized.** All reviewers note professional prose, clear structure, and honest reporting of limitations.

**[CONSENSUS-3]** (3/4 reviewers agree):
1. **Comparison with recent LISTA variants is insufficient.** EIC, R1, and R2 all note the absence of OCLISTA and LISTA-AMP comparisons. R3 does not flag this (hardware focus). The consensus is that at least a qualitative discussion of improved LISTA variants is needed.
2. **NMSE discrepancy across tables needs explanation.** EIC and R1 flag the 8 dB difference between Table 1 and Table 7 for the same nominal configuration. R2 and R3 do not explicitly flag this but would benefit from clarification.
3. **Contribution list is too long.** EIC and R2 suggest consolidating from 6 to 3–4 contributions. R1 and R3 do not explicitly flag this.

### Points of Disagreement

**Disagreement 1: Severity of the ZF-specific BER advantage**
- **DA view**: The BER advantage is a ZF-specific artifact. MMSE equalization (Table 10) shows identical BER for all methods at SNR=20 dB, undermining the central claim. This is flagged as CRITICAL.
- **EIC/R1/R2/R3 view**: The BER advantage is a genuine finding, validated with statistical testing and mechanism analysis. The MMSE confirmation shows the *relative* advantage is preserved.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The DA raises a valid point about MMSE equalization at SNR=20 dB, but the ZF results across all SNR points and modulations are statistically significant. The paper already acknowledges that MMSE provides modest improvement and that the relative advantage is preserved. The finding is not ZF-specific—the mechanism (error concentration) is independent of equalizer type. However, the paper should more explicitly discuss the MMSE implications and avoid overstating the BER advantage for systems that use MMSE equalization.
- **Resolution Rationale**: The DA's CRITICAL finding is downgraded to MAJOR. The BER advantage is real but its practical significance depends on the equalization method used. The paper should add a paragraph discussing this nuance.

**Disagreement 2: Significance of the 33× Python speedup**
- **DA view**: The 33× speedup is misleading because it reflects Python interpreter overhead, not algorithmic superiority. The hardware estimate (4.4×) should be the headline number.
- **R3 view**: The Python speedup is useful context but should be clearly distinguished from hardware performance.
- **EIC/R1/R2 view**: The paper already acknowledges the Python caveat and provides hardware estimates.
- **Disagreement type**: Emphasis disagreement
- **Editor's Resolution**: The 33× speedup is a legitimate measurement within the Python ecosystem and is relevant for researchers prototyping in Python. However, the abstract and highlights should lead with the hardware throughput estimate (4.4×) for accuracy, with the Python speedup as supplementary context.
- **Resolution Rationale**: The paper already provides both numbers. The revision should restructure the abstract to emphasize the hardware estimate.

---

## Decision Rationale *

All four reviewers recommend Minor Revision, and I concur. The paper makes a genuine contribution to the sparse channel estimation literature through its BER-NMSE disconnect analysis, which provides new insight into how deep-unfolded estimators behave in communication systems. The ablation study with 20 seeds and the SNR saturation mitigation experiment are methodologically sound and practically useful.

The primary concerns are: (1) the NMSE discrepancy across tables needs explanation, (2) the comparison with recent LISTA variants should be expanded, (3) the abstract should lead with hardware throughput estimates rather than Python speedup, and (4) the BER advantage discussion should more explicitly address MMSE equalization implications. These are all addressable within a minor revision without requiring new experiments (except possibly a brief OCLISTA comparison or discussion).

The Devil's Advocate raised a valid concern about the ZF-specific nature of the BER advantage, but the mechanism analysis (error concentration) is independent of equalizer type, and the paper already provides MMSE confirmation. The concern is addressed by adding nuance to the discussion rather than by changing the paper's conclusions.

The paper is suitable for *Digital Signal Processing* and would be of interest to researchers working on deep unfolding, sparse recovery, and practical communication system design.

---

## Required Revisions * (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|--------------|----------------|----------|---------|-----------------|
| R1 | Explain NMSE discrepancy across tables (Table 1 vs Table 7: −24.25 vs −32.29 dB at same nominal configuration) | EIC, R1 | Critical | Section 4 | 1 day |
| R2 | Add discussion of recent LISTA variants (OCLISTA, LISTA-AMP) and whether the saturation phenomenon is architecture-specific | EIC, R2 | Major | Section 2, 5 | 2 days |
| R3 | Restructure abstract to lead with hardware throughput estimate (4.4×) rather than Python speedup (33×); add explicit caveat about Python-specific overhead | DA, R3 | Major | Abstract, Highlights | 1 day |
| R4 | Add paragraph discussing BER advantage implications for MMSE equalization; acknowledge that practical systems using MMSE may not see the same BER gap | DA | Major | Section 4.10, 5 | 1 day |

### Required Item Details

**R1: NMSE Discrepancy Across Tables**
- **Problem**: At N=64, K=5, M=256, L=20, SNR=20 dB, Table 1 reports −24.25 dB while Table 7 reports −32.29 dB. This 8 dB difference is unexplained.
- **Source**: EIC ("Table 1 vs Table 7 discrepancy"), R1 ("NMSE Discrepancy Across Tables")
- **Requirement**: Explicitly state whether each table uses the same trained model or independent training runs. If different seeds or procedures produce different results, explain the variance. Add footnotes to both tables.
- **Acceptance criteria**: The discrepancy is explained and readers can reproduce the results.

**R2: Recent LISTA Variants Discussion**
- **Problem**: The paper only compares against LISTA-CP (which yields identical results). OCLISTA and LISTA-AMP are cited but not discussed in the context of the saturation phenomenon.
- **Source**: EIC ("Missing Comparison with Recent LISTA Variants"), R2 ("No Comparison with Recent LISTA Variants Beyond LISTA-CP")
- **Requirement**: Add a paragraph in Section 2.2 and Section 5.1 discussing OCLISTA and LISTA-AMP, and whether the saturation is expected to persist with these variants. If experiments are infeasible, a qualitative discussion suffices.
- **Acceptance criteria**: The reader understands how the findings relate to the broader LISTA family.

**R3: Abstract Restructuring**
- **Problem**: The abstract leads with "33× faster inference" which is a Python-specific measurement. The hardware throughput advantage is 4.4×.
- **Source**: DA ("Data-Conclusion Mismatch"), R3 ("Python Speed Comparison May Mislead")
- **Requirement**: Restructure the abstract to state "4.4× throughput advantage in hardware" as the primary speed claim, with "33× faster in Python" as supplementary context. Add a brief caveat about Python overhead.
- **Acceptance criteria**: The abstract does not mislead readers about the speed advantage.

**R4: MMSE Equalization Discussion**
- **Problem**: The BER advantage is demonstrated primarily under ZF equalization. MMSE equalization (Table 10) shows convergence at SNR=20 dB, but the paper does not discuss the practical implications for systems using MMSE.
- **Source**: DA ("CRITICAL: BER advantage is ZF-specific")
- **Requirement**: Add a paragraph in Section 4.10 or 5.1 discussing: (1) MMSE equalization reduces the BER gap because it regularizes noise enhancement, (2) for systems using MMSE, the BER advantage may be smaller, (3) the mechanism insight (error concentration) remains valid regardless of equalizer.
- **Acceptance criteria**: The paper does not overstate the BER advantage for MMSE-based systems.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|--------------|----------------|----------|---------|---------------------|
| S1 | Consolidate contribution list from 6 to 3–4 items | EIC, R2 | P2 | Section 1 | Clearer impact narrative |
| S2 | Add LASSO convergence diagnostics (residual norm after 500 iterations) | R1 | P2 | Section 4.1 | Fairer baseline comparison |
| S3 | Add sensitivity analysis for hardware timing estimates (vary DSP count, clock frequency) | R3 | P3 | Section 4.13 | More robust hardware claims |
| S4 | Discuss practical impairment effects (QPSK pilots, frequency offset, phase noise) on LISTA vs OMP | R3 | P3 | Section 5 | Better deployment guidance |
| S5 | Consider adding "OMP + thresholding" baseline to test whether error concentration is unique to LISTA | DA | P2 | Section 4.12 | Stronger mechanism claims |

---

## Revision Roadmap *

### Priority 1 — Structural Revisions (Estimated total effort: 5 days)
- [ ] R1: Explain NMSE discrepancy across tables with footnotes and training details
- [ ] R2: Add discussion of OCLISTA, LISTA-AMP, and saturation generalization
- [ ] R3: Restructure abstract to lead with hardware throughput estimate
- [ ] R4: Add MMSE equalization discussion paragraph

### Priority 2 — Content Supplementation (Estimated total effort: 3 days)
- [ ] S1: Consolidate contribution list from 6 to 3–4 items
- [ ] S2: Add LASSO convergence diagnostics
- [ ] S5: Consider "OMP + thresholding" baseline (optional experiment)

### Priority 3 — Text and Formatting (Estimated total effort: 2 days)
- [ ] S3: Hardware timing sensitivity analysis
- [ ] S4: Practical impairment discussion
- [ ] Minor language fixes noted by reviewers
- [ ] Citation format corrections (chen2018lista year)

### Total Estimated Effort
- **Minor Revision**: 1–2 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01
- **Basis**: Minor Revision, 4 weeks
- **Extension policy**: If extension is needed, notify 1 week before the deadline

---

## Response Letter Instructions

Please use the format in `templates/revision_response_template.md` to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1–R4)
2. Response for each Suggested Revision (S1–S5) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We invite you to submit a revised version of your manuscript, addressing the points raised by the reviewers. The reviewers and I found the BER-NMSE disconnect analysis to be a genuinely valuable contribution to the sparse channel estimation literature, and the ablation study demonstrates methodological maturity. The required revisions are straightforward and do not require major new experiments.

We look forward to receiving your revision within 4 weeks.

---

## Appendix: Reviewer Dimension Score Summary

| Dimension | EIC | R1 | R2 | R3 | Mean |
|-----------|-----|----|----|----|------|
| Originality (20%) | 68 | 65 | 62 | 60 | 63.8 |
| Methodological Rigor (25%) | 78 | 72 | 74 | 70 | 73.5 |
| Evidence Sufficiency (25%) | 80 | 78 | 76 | 74 | 77.0 |
| Argument Coherence (15%) | 75 | 76 | 75 | 76 | 75.5 |
| Writing Quality (15%) | 76 | 77 | 78 | 77 | 77.0 |
| **Weighted Average** | **75.6** | **73.4** | **72.6** | **71.2** | **73.2** |
