# Peer Review Report — EIC

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 7

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC)

### Reviewer Identity
Prof. Elena Marchetti, Associate Editor for *Digital Signal Processing*. Expertise in adaptive signal processing, compressed sensing, and deep learning for communications. 15+ years editing experience in signal processing journals.

### Review Focus
Journal fit, originality, overall quality, significance for the DSP readership, and whether the contribution claims are appropriately scoped.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — The paper falls well within my area of expertise. I am confident in my assessment of journal fit and contribution significance.

### Summary Assessment
This paper presents a systematic analysis of LISTA (Learned ISTA) applied to sparse channel estimation, with emphasis on BER performance, ablation studies, generalization, and theoretical hardware complexity. The paper is well-structured and addresses a relevant problem in the DSP community. The key finding—that LISTA's NMSE gap with OMP does not translate to BER penalty under MMSE equalization—is novel and practically significant. The ablation study with 20 seeds and proper statistical testing (paired t-tests, Cohen's d) is methodologically sound. However, the paper's central weakness is the persistent gap between theoretical hardware claims and measured results: all FPGA/ASIC throughput estimates remain theoretical, and the paper repeatedly hedges on this point. The writing quality is generally strong, though the abstract is excessively long and the paper could benefit from tighter prose in the Discussion. The contribution is incremental within the deep unfolding literature but provides genuinely useful system-level insights for the channel estimation community. I recommend Minor Revision, primarily to tighten the hardware claims and reduce abstract length.

---

## Strengths

### S1: Novel BER-NMSE Disconnect Analysis
The paper's strongest contribution is the systematic analysis showing that LISTA's NMSE disadvantage does not translate to BER penalty under MMSE equalization (Section 4.10, Tables 10-12). The mechanism analysis—LISTA concentrates 99.9% of error on true taps vs. 94.9% for OMP—is well-supported by 200 channel realizations per SNR point with paired t-tests. This finding is genuinely useful for practitioners deciding between estimators.

### S2: Rigorous Ablation with Statistical Power
The progression from 5-seed ablation (Table 5) to 20-seed ablation (Table 11) with proper statistical testing is commendable. The paper transparently acknowledges that the initial 5-seed result was a false negative due to low power, and the 20-seed experiment reveals the true picture (threshold schedule is dominant at +14-18 dB). This level of statistical rigor is uncommon in the deep unfolding literature.

### S3: Honest Treatment of Limitations
The paper is refreshingly honest about LISTA's limitations: the -25 dB saturation, the NMSE gap with OMP, and the theoretical nature of hardware estimates. The Discussion section (Section 5) appropriately scopes the claims and identifies the saturation as likely a training artifact rather than architectural limitation.

### S4: Comprehensive Experimental Design
The paper covers 13 experiments spanning NMSE vs. SNR, sparsity, channel length, depth analysis, ablation, generalization, ITU channels, LISTA-CP comparison, SNR mitigation, BER performance, mechanism analysis, and hardware complexity. This breadth provides a thorough characterization of LISTA's behavior.

---

## Weaknesses

### W1: Hardware Claims Remain Theoretical
**Problem**: The paper's hardware throughput claims (4.4× advantage over OMP, 1.2 μs pipeline throughput) are entirely theoretical, based on FLOP counts and pipeline analysis. The paper acknowledges this repeatedly but the highlights and abstract still present these as primary contributions. The 33× Python speedup reflects interpreter overhead, not hardware capability.
**Why it matters**: For a signal processing journal, hardware claims carry significant weight. Presenting theoretical estimates alongside measured Python results risks misleading readers about actual performance.
**Suggestion**: Either (a) reduce the prominence of hardware claims in the abstract/highlights, or (b) clearly label all hardware numbers as "theoretical estimates" in every table and figure caption. Consider removing the 33× Python speedup from the highlights entirely.
**Severity**: Major

### W2: Abstract Exceeds Reasonable Length
**Problem**: The abstract is approximately 350 words—far exceeding the typical 150-250 word limit for Elsevier journals. It contains excessive detail about statistical methodology (200 realizations, paired t-tests, 95% CI, 5 seeds) that belongs in the Methods section.
**Why it matters**: Long abstracts reduce readability and may violate journal formatting requirements.
**Suggestion**: Reduce to 200 words. Focus on: problem, approach, key finding (BER-NMSE disconnect), and main practical implication. Move statistical validation details to the body.
**Severity**: Minor

### W3: Cross-Table Consistency Issue Undermines Reproducibility
**Problem**: Table 3 (NMSE vs channel length) reports LISTA at -32.29 dB for N=64, SNR=20, while Table 1 (NMSE vs SNR) reports -24.25 dB for the same nominal configuration. The paper explains this as "independently trained models with different training distributions," but this raises concerns about the robustness of the reported numbers.
**Why it matters**: Readers cannot reproduce results without knowing which training protocol was used for each table. The ~8 dB discrepancy is substantial.
**Suggestion**: Either unify the training protocol across all experiments, or add a clear "Training Protocol" column to every results table specifying the training distribution used.
**Severity**: Major

### W4: Missing CNN/Transformer Baseline Comparison
**Problem**: The paper explicitly excludes CNN and Transformer baselines, providing only a qualitative comparison in Section 5.2 based on published results. For a journal submission, this weakens the positioning.
**Why it matters**: Reviewers at DSP will expect at least one deep learning baseline for direct comparison, given that the paper claims practical advantages.
**Suggestion**: Add at least one CNN baseline (e.g., a simple 1D-CNN) trained under identical conditions. If space is limited, provide the comparison in a supplementary document.
**Severity**: Major

---

## Detailed Comments

### Title & Abstract
- Title accurately reflects the paper's scope. The "Analysis" framing is appropriate given the non-novel architecture.
- Abstract needs significant trimming (see W2). The highlights are well-crafted but the hardware claims need qualification.

### Introduction
- Well-structured with clear enumeration of 6 contributions. The research motivation is persuasive.
- Contribution list is comprehensive but could be more concise. Some contributions (e.g., #6 hardware analysis) overlap with #4 (generalization).

### Literature Review
- Good coverage of deep unfolding, channel estimation, and adaptive filtering. The comparison table in Section 2.3 is helpful.
- The positioning relative to CNN/Transformer methods is acknowledged but deferred to Discussion (see W4).

### Methodology
- LISTA architecture description is clear and well-formulated.
- Training protocol is well-specified (mixed SNR, Adam optimizer, cosine annealing).
- The scale-invariant loss discussion is insightful.

### Results
- 13 experiments provide comprehensive coverage. Tables and figures are well-formatted.
- The BER analysis (Section 4.10) is the paper's highlight—rigorous and well-validated.
- Cross-table consistency issue (W3) needs resolution.

### Discussion
- Honest and well-scoped. The "training artifact vs. architectural limitation" discussion is particularly strong.
- Section 5.2 (CNN/Transformer comparison) is reasonable but would benefit from direct comparison.

### Conclusion
- Accurately summarizes findings without overclaiming. Appropriately hedges hardware results.

### References
- Good coverage (~45 references). Recent works (2022-2024) are included. Citation format is consistent.

---

## Questions for Authors

1. The cross-table consistency issue (Table 1 vs. Table 3 at N=64, SNR=20) shows an ~8 dB difference attributed to different training distributions. Can you provide a unified experiment with a single training protocol to resolve this discrepancy? If not, can you add a training protocol identifier to each table?

2. The hardware throughput claim of 4.4× is based on theoretical pipeline analysis. Given that Wei et al. (2022) reported <10 μs FPGA latency for LISTA, can you provide any preliminary FPGA measurement results, even for a single configuration?

3. For the BER analysis, the paper uses 200 realizations per SNR point. What is the confidence interval width for the BER estimates at SNR=20 dB? Is 200 sufficient for the claimed p-value precision?

---

## Minor Issues

### Language / Grammar
- Abstract, line 3: "likely a training artifact from the scale-invariant loss" — reword to "likely attributable to the scale-invariant loss"
- Section 4.10, Table 10 caption: "200 realizations per point" — should be "200 channel realizations per SNR point"

### Figures and Tables
- Table 1: Consider adding a column for LISTA-CP results to reduce table count
- Figure 2 (NMSE vs sparsity): The y-axis range should be consistent with Figure 1 for visual comparison

### Layout
- The highlights section contains 6 items; consider reducing to 5 per journal guidelines

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | BER-NMSE disconnect analysis is novel; LISTA for channel estimation is incremental |
| Methodological Rigor (25%) | 78 | Strong | Good statistical testing, but cross-table inconsistency and missing baselines |
| Evidence Sufficiency (25%) | 75 | Strong | Comprehensive experiments, but hardware claims lack measured data |
| Argument Coherence (15%) | 82 | Strong | Clear logical flow, honest treatment of limitations |
| Writing Quality (15%) | 76 | Strong | Generally well-written, abstract too long |
| **Weighted Average** | **75.4** | **Minor Revision** | |
