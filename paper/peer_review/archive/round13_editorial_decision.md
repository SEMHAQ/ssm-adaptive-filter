# Editorial Decision Package

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Author**: Huanjie Yu, Hunan University of Technology and Business
- **Submission Date**: 2026-06-01
- **Decision Date**: 2026-06-01
- **Review Round**: Round 13

---

## Decision

### Major Revision

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC | Journal Editor | Minor Revision | 4 | 78 |
| Reviewer 1 | Methodology Expert | Minor Revision | 5 | 76 |
| Reviewer 2 | Domain Expert | Major Revision | 5 | 70 |
| Reviewer 3 | Hardware/Practical Perspective | Minor Revision | 4 | 73 |
| Devil's Advocate | Stress Test | — (no recommendation) | — | — |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All 4 reviewers agree):
1. **The 20-seed ablation study with effect sizes is methodologically excellent.** All reviewers praise the progressive approach (5-seed → 20-seed) and the consistent reporting of Cohen's d alongside p-values. This sets a good standard for the field.
2. **The paper is unusually honest about LISTA's limitations.** The transparent reporting of the 13-33 dB NMSE gap, the SNR saturation, the Python speedup as a software artifact, and the cross-table consistency issue builds credibility.
3. **The ITU channel generalization is practically valuable.** All reviewers agree that testing on ITU PedA and VehA channels with baselines tuned on Gaussian data is a fair and useful evaluation protocol.

**[CONSENSUS-3]** (3/4 reviewers agree — R1, R2, R3 agree; EIC has different emphasis):
1. **The hardware complexity discussion needs improvement.** R1 notes the FLOP analysis is adequate; R2 and R3 both flag that the "pipelining advantage" claim is unsupported and that quantization, memory bandwidth, and training infrastructure are not discussed. The EIC acknowledges this but considers it minor.

**[CONSENSUS-3]** (3/4 reviewers agree — EIC, R1, R2 agree; R3 has different emphasis):
1. **The error concentration mechanism needs an ISTA control experiment.** The EIC, R1 (implicitly), and R2 all identify this as the most critical gap. R3 does not flag this explicitly but notes the mechanism analysis is at a single configuration. The Devil's Advocate identifies this as the CRITICAL vulnerability.

### Points of Disagreement

**Disagreement 1: Severity of the missing ISTA control experiment**
- **R2 (Domain) view**: This is a Critical issue — without the ISTA comparison, the paper's primary contribution may collapse. Recommends Major Revision.
- **EIC view**: This is a Major issue — the mechanism is still valuable even if generic to soft-thresholding, but the framing needs adjustment. Recommends Minor Revision.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: R2's position is adopted. The ISTA control experiment is essential because the paper's entire contribution structure rests on the mechanism being LISTA-specific. If it turns out to be generic, the paper needs significant restructuring. This elevates the decision to Major Revision.
- **Resolution Rationale**: The domain expert (R2) has the deepest understanding of sparse recovery algorithms and correctly identifies that soft-thresholding behavior is well-studied — the paper must demonstrate novelty beyond this known behavior.

**Disagreement 2: Importance of the hardware discussion**
- **R3 (Perspective) view**: The hardware claims (pipelining advantage, FLOP analysis) are major concerns requiring significant revision.
- **EIC view**: The hardware discussion is supplementary and the paper is already honest about theoretical vs. measured results.
- **Disagreement type**: Severity disagreement
- **Editor's Resolution**: The EIC's position is adopted. The hardware discussion is clearly labeled as theoretical and supplementary. The paper's core contribution is the mechanism analysis, not hardware deployment. The hardware claims should be tightened but this is a Minor issue.
- **Resolution Rationale**: The paper's primary audience (DSP researchers) cares more about the algorithmic analysis than hardware deployment. The hardware section can be improved in a minor revision.

---

## Decision Rationale

The paper presents a comprehensive experimental analysis of LISTA for sparse channel estimation, with methodologically rigorous ablation studies and BER simulations. The writing is professional and the honesty about limitations is commendable. However, the paper's primary contribution — the "error concentration mechanism" — has a critical gap: it does not demonstrate that the mechanism is specific to LISTA rather than a generic property of soft-thresholding. The Devil's Advocate correctly identifies this as the most vulnerable point.

Three of four reviewers recommend Minor Revision, but the domain expert (R2) identifies the ISTA control experiment gap as Critical, and the Devil's Advocate flags it as the primary vulnerability. Given that the entire paper's contribution structure rests on this mechanism being LISTA-specific, and given that the domain expert has the deepest understanding of sparse recovery behavior, the decision is elevated to **Major Revision**.

The revision required is focused: (1) add an ISTA control experiment to the error concentration analysis, (2) add FISTA as a baseline, (3) apply multiple comparison corrections to hypothesis tests, and (4) tighten the hardware complexity claims. These revisions are substantial but achievable within 6-8 weeks.

The paper's strengths — comprehensive experiments, statistical rigor, honest reporting, and practical SNR mitigation analysis — provide a strong foundation. With the ISTA control experiment, the paper will either (a) demonstrate that LISTA's learned parameters produce genuinely different error concentration (strengthening the contribution) or (b) reveal that the mechanism is generic to soft-thresholding (requiring reframing but still valuable as a characterization study). Either outcome improves the paper.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source | Severity | Section | Estimated Effort |
|---|--------------|--------|----------|---------|-----------------|
| R1 | Add ISTA control experiment for error concentration | R2, DA | Critical | Section 4.12 | 3-5 days |
| R2 | Add FISTA as a baseline | R2 | Major | Section 4.2, Tables 1-2 | 3-5 days |
| R3 | Apply Holm-Bonferroni correction to multiple hypothesis tests | R1 | Major | Tables 1, 8, 9, 10, 11 | 1-2 days |
| R4 | Extend error sparsity analysis to additional configurations | R1, DA | Major | Section 4.12 | 2-3 days |
| R5 | Tighten "pipelining advantage" claims or provide supporting analysis | R3, EIC | Major | Sections 4.7.1, 4.12, 5.3 | 1-2 days |

### Required Item Details

**R1: ISTA Control Experiment for Error Concentration**
- **Problem**: The paper's primary contribution (error concentration on true taps) is not demonstrated to be LISTA-specific. Standard ISTA with fixed thresholds likely produces similar behavior due to the soft-thresholding operator.
- **Source**: R2 (Critical), DA (CRITICAL #1), EIC (Major)
- **Requirement**: Run standard ISTA with fixed thresholds (20 iterations, same configuration as Table 12) and compute the same error sparsity metrics (Error on S%, Error on S̄%, Gini coefficient). Compare with LISTA's results.
- **Acceptance criteria**: Either (a) LISTA shows qualitatively different error concentration than ISTA (e.g., 99.9% vs. 95%), supporting the "LISTA mechanism" framing, or (b) ISTA shows similar concentration (e.g., >99%), requiring the contribution to be reframed as "characterizing soft-thresholding behavior in channel estimation."

**R2: Add FISTA Baseline**
- **Problem**: The comparison is limited to OMP and LASSO (solved via basic ISTA). FISTA (Fast ISTA) is the natural comparison for LISTA and is not experimentally evaluated.
- **Source**: R2 (Major)
- **Requirement**: Add FISTA with L=20 iterations as a baseline in Tables 1 and 2. Use grid-searched hyperparameters (step size, threshold).
- **Acceptance criteria**: FISTA results are reported alongside LISTA, OMP, and LASSO, enabling direct comparison of learned vs. fixed parameters.

**R3: Multiple Comparison Correction**
- **Problem**: ~30+ hypothesis tests are conducted without correction for multiple comparisons.
- **Source**: R1 (Major)
- **Requirement**: Apply Holm-Bonferroni correction within each table's family of tests. Report corrected p-values.
- **Acceptance criteria**: Corrected p-values are reported; results that become non-significant after correction are honestly reported.

**R4: Error Sparsity Analysis at Additional Configurations**
- **Problem**: The error concentration mechanism is demonstrated at only one configuration (N=64, K=5, M=256, SNR=20 dB).
- **Source**: R1 (Major), DA (MAJOR #3)
- **Requirement**: Extend the error sparsity analysis (Table 12) to at least one additional configuration (e.g., K=10 or SNR=10 dB).
- **Acceptance criteria**: Error concentration metrics are reported at 2+ configurations, demonstrating mechanism robustness.

**R5: Tighten Hardware Claims**
- **Problem**: The "pipelining advantage" claim appears multiple times without supporting evidence.
- **Source**: R3 (Major), EIC (Minor)
- **Requirement**: Either (a) provide a brief pipeline analysis (latency, throughput estimates for LISTA vs. OMP on a hypothetical FPGA), or (b) remove the "pipelining advantage" claims and limit hardware discussion to FLOP counts and parameter counts.
- **Acceptance criteria**: Hardware claims are either supported by analysis or removed. The disclaimer "all hardware values are theoretical" is consolidated into one prominent statement.

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source | Priority | Section | Expected Improvement |
|---|--------------|--------|----------|---------|---------------------|
| S1 | Discuss quantization effects on LISTA performance | R3 | P2 | Section 5.4 | Strengthens hardware deployment story |
| S2 | Add training complexity discussion (GPU hours, convergence) | R3 | P2 | Section 3.5 | Provides complete deployment cost picture |
| S3 | Increase core experiments (Tables 1-4) to 20 seeds | R1 | P2 | Sections 4.1-4.4 | Improves statistical power and consistency |
| S4 | Restructure BER section to lead with MMSE (practical) then ZF (diagnostic) | EIC | P2 | Section 4.10 | Better framing of BER contribution |
| S5 | Add brief theoretical analysis of why soft-thresholding concentrates error on true taps | R2 | P2 | Section 4.12 | Strengthens mechanism contribution |
| S6 | Discuss LISTA's role in massive MIMO/mmWave context | DA | P3 | Section 5.4 | Broadens impact and relevance |
| S7 | Add block diagram of LISTA inference pipeline | R3 | P3 | Section 3.4 | Improves clarity for hardware readers |

---

## Revision Roadmap

### Priority 1 — Structural Revisions (Estimated total effort: 10-15 days)
- [ ] R1: Run ISTA control experiment and compute error sparsity metrics at the same configuration as Table 12. Compare with LISTA results. Reframe contribution if needed.
- [ ] R2: Add FISTA with L=20 iterations as a baseline. Grid-search hyperparameters. Update Tables 1 and 2.
- [ ] R3: Apply Holm-Bonferroni correction to all hypothesis tests. Update p-values in Tables 1, 8, 9, 10, 11.
- [ ] R4: Extend error sparsity analysis to K=10 (or SNR=10 dB). Report Error on S%, Error on S̄%, Gini.
- [ ] R5: Either provide pipeline analysis or remove "pipelining advantage" claims. Consolidate hardware disclaimers.

### Priority 2 — Content Supplementation (Estimated total effort: 5-7 days)
- [ ] S1: Add brief discussion of quantization effects (8-bit, 16-bit). Ideally include a simulation experiment.
- [ ] S2: Add paragraph on training complexity and when retraining is necessary.
- [ ] S3: Increase core experiments to 20 seeds if computationally feasible.
- [ ] S4: Restructure BER section: lead with MMSE results, then present ZF as diagnostic.
- [ ] S5: Add brief theoretical analysis of soft-thresholding error concentration.

### Priority 3 — Text and Formatting (Estimated total effort: 2-3 days)
- [ ] S6: Add paragraph on massive MIMO/mmWave relevance in Discussion.
- [ ] S7: Add LISTA inference pipeline block diagram.
- [ ] Consolidate hardware disclaimers into one statement.
- [ ] Shorten LISTA-CP subsection (Section 4.8) to 2-3 sentences.
- [ ] Minor language polishing throughout.

### Total Estimated Effort
- **Major Revision**: 3-4 weeks

---

## Revision Deadline

- **Recommended deadline**: 2026-07-01 (4 weeks)
- **Basis**: Major Revision, but the required changes are focused and achievable within the timeframe.
- **Extension policy**: If extension is needed, notify the editorial office 1 week before the deadline.

---

## Response Letter Instructions

Please use the R→A→C (Reviewer comment → Author response → Change description) format to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1-R5)
2. Response for each Suggested Revision (S1-S7) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs

---

## Closing

We encourage you to carefully consider the reviewers' comments and submit a substantially revised manuscript. The reviewers have identified a focused set of revisions — most critically, the ISTA control experiment (R1) and the FISTA baseline (R2) — that will significantly strengthen the paper's contribution. The paper's comprehensive experimental design, statistical rigor, and honest reporting are strong foundations. We look forward to receiving your revised manuscript.

---

## Appendix: Reviewer Score Summary

| Dimension | EIC | R1 (Methodology) | R2 (Domain) | R3 (Perspective) |
|-----------|-----|-------------------|-------------|-------------------|
| Originality (20%) | 68 | 65 | 58 | 65 |
| Methodological Rigor (25%) | 78 | 72 | 75 | 75 |
| Evidence Sufficiency (25%) | 80 | 78 | 70 | 72 |
| Argument Coherence (15%) | 82 | 80 | 72 | 78 |
| Writing Quality (15%) | 85 | 82 | 82 | 82 |
| Weighted Average | **78** | **76** | **70** | **73** |
| Recommendation | Minor | Minor | Major | Minor |

### Devil's Advocate Critical Issues

**DA-CRITICAL #1**: The error concentration mechanism is not demonstrated to be LISTA-specific. No ISTA control experiment is provided.
- **Corroboration**: R2 (Domain) independently identifies this as a Critical issue.
- **EIC assessment**: Valid. This is the most important revision required.
- **Required author response**: Run the ISTA control experiment (R1 in revision roadmap) and report whether the mechanism is LISTA-specific or generic to soft-thresholding.

**DA-MAJOR #2**: Selective framing — the paper emphasizes error concentration (where LISTA wins) while de-emphasizing NMSE (where LISTA loses by 13-33 dB).
- **Corroboration**: EIC notes the framing concern but considers it addressable.
- **EIC assessment**: Partially valid. The paper is honest about the NMSE gap, but the abstract and highlights could be better balanced.
- **Required author response**: Consider restructuring the abstract to lead with the comprehensive analysis framing rather than the error concentration finding.

**DA-MAJOR #5**: Stronger counter-narrative — the BER differences under ZF are small (0.006 vs. 0.010 at SNR=20 dB for QPSK) and may not matter in practice.
- **Corroboration**: EIC notes that ZF is rarely used in modern receivers.
- **EIC assessment**: Valid point. The ZF results should be presented as diagnostic, not as a practical advantage.
- **Required author response**: Restructure BER section (S4 in revision roadmap) to present ZF results as error structure diagnostics.
