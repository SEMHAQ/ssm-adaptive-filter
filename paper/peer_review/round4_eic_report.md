# EIC Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 4

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), *Digital Signal Processing* (Elsevier)

### Reviewer Identity
Prof. Dr. Elena Morozova, Editor-in-Chief of *Digital Signal Processing*. Expertise in model-based deep learning for signal processing, algorithm unrolling, and computational efficiency analysis. 20+ years of editorial experience in signal processing journals. Preference for papers that bridge theory and practice with clear deployment pathways.

### Review Focus
Overall quality, journal fit, originality, structural coherence, and strategic value to the DSP readership. I assess whether the paper makes a meaningful contribution to the intersection of deep learning and signal processing, and whether the findings are presented with sufficient clarity and rigor for the journal's audience.

---

## Overall Assessment *

### Recommendation *
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score *
4 — Mostly within my area of expertise, high confidence. The deep unfolding and sparse recovery aspects are squarely in my domain; the hardware deployment analysis is adjacent but I have sufficient familiarity.

### Summary Assessment *
This paper investigates LISTA (Learned ISTA) for sparse channel estimation, providing a systematic analysis of generalization, ablation, BER performance, and practical deployment characteristics. The paper is well-structured and addresses a legitimate gap: while LISTA has been extensively studied in the compressed sensing literature, its application to sparse channel estimation with rigorous BER validation and hardware complexity analysis is underexplored.

The paper's strongest contribution is the BER-NMSE disconnect analysis (Section 4.10), which reveals that LISTA's 13–33 dB NMSE gap with OMP does not translate to a BER penalty—indeed, LISTA achieves *better* BER for 16-QAM at high SNR. The mechanism analysis (99.9% error concentration on true taps) is insightful and well-validated with 200 realizations and paired t-tests. The ablation study with 20 seeds and the SNR saturation mitigation experiment are also valuable.

However, the paper has some structural issues: the title promises "Analysis" but the contribution list reads more like a system paper with 6 enumerated claims. The Related Work section is comprehensive but could be tighter. The NMSE saturation at −25 dB is honestly reported but the paper sometimes overstates the practical significance of LISTA when OMP is clearly superior on NMSE. Overall, this is a solid contribution suitable for *Digital Signal Processing* after minor revision.

---

## Strengths *

### S1: BER-NMSE Disconnect Analysis with Mechanism Insight
The paper's central contribution is the demonstration that LISTA's NMSE disadvantage does not translate to BER degradation. The mechanism analysis (Section 4.12) showing that LISTA concentrates 99.9% of estimation error on true tap locations (vs. 94.9% for OMP), with 50× less non-support error, provides genuine insight into *why* NMSE is the wrong metric for equalization quality. This is validated with 200 realizations, paired t-tests, and MMSE equalization confirmation—a level of statistical rigor uncommon in the deep unfolding literature.

### S2: Comprehensive Ablation with Proper Statistical Power
The progression from 5-seed ablation (Table 5) to 20-seed ablation (Table 11) with paired t-tests and Cohen's d effect sizes is exemplary. The finding that the threshold schedule is the dominant contributor (+14–18 dB degradation) while W^(k) provides a secondary +1.24 dB (d=1.5) is well-supported and provides actionable insight for practitioners.

### S3: Honest Reporting of Limitations
The paper honestly reports LISTA's NMSE saturation at −25 dB, the divergence at N=256, and the instability at K=15. The discussion of when to prefer OMP/LASSO over LISTA (Section 5.2) is balanced and practical. This honesty strengthens rather than weakens the paper.

### S4: Practical Deployment Analysis
The combination of Python runtime benchmarks (33× speedup), FLOP analysis (760K vs. 332K for OMP), hardware complexity estimation (20-stage pipeline, 1.2 μs throughput), and the SNR-specific training mitigation strategy provides a complete picture for practitioners considering LISTA deployment.

---

## Weaknesses *

### W1: Inconsistent Parameter Reporting Across Experiments
**Problem**: The paper reports L=20 layers throughout, but Table 7 (Channel Length) shows different NMSE values for N=64 than Table 1 (SNR sweep) at SNR=20 dB: Table 1 reports −24.25 dB while Table 7 reports −32.29 dB for the same N=64, K=5, M=256, L=20, SNR=20 configuration. This discrepancy is not explained.
**Why it matters**: Inconsistent results across tables undermine reproducibility and suggest different training procedures were used despite the paper's claim of a "single model."
**Suggestion**: Clarify whether the same trained model is used across all experiments. If different seeds or training runs produce different results, explain the variance. Add a footnote to Table 7 explaining the discrepancy.
**Severity**: Major

### W2: Title Mismatch with Content
**Problem**: The title says "Analysis of Deep-Unfolded LISTA" suggesting an analytical study, but the paper is structured as a system evaluation with 13 experiments, 6 contribution claims, and deployment recommendations. The title undersells the practical contributions.
**Why it matters**: Title-content mismatch can confuse readers and reviewers about the paper's positioning.
**Suggestion**: Consider a title that better reflects the practical evaluation angle, e.g., "LISTA for Sparse Channel Estimation: BER Performance, Ablation, and Deployment Analysis."
**Severity**: Minor

### W3: Overcrowded Contribution List
**Problem**: The introduction lists 6 contributions (Section 1, items 1–6), which dilutes the impact. Some items overlap (items 1 and 2 both discuss NMSE/BER; items 4 and 6 both discuss generalization and hardware).
**Why it matters**: A crowded contribution list makes it hard for readers to identify the paper's core message. Reviewers may perceive the paper as trying to do too much.
**Suggestion**: Consolidate to 3–4 crisp contributions: (1) BER-NMSE disconnect with mechanism analysis, (2) comprehensive ablation with statistical rigor, (3) SNR saturation mitigation, (4) practical deployment characterization.
**Severity**: Minor

### W4: Missing Comparison with Recent LISTA Variants
**Problem**: The paper compares against LISTA-CP (Section 4.8) but does not compare against OCLISTA [Borgerding 2020], ISTA-Net [He 2019], or LISTA-AMP [Liu 2023]. The LISTA-CP comparison shows identical performance, which is interesting but limited.
**Why it matters**: The deep unfolding field has evolved significantly since the original LISTA (2010). Without comparison against more recent variants, the reader cannot assess whether the findings are specific to the basic LISTA architecture or generalize to improved variants.
**Suggestion**: Add at least a brief comparison or discussion of OCLISTA and LISTA-AMP. If experiments are infeasible, a qualitative discussion of expected differences would suffice.
**Severity**: Major

---

## Detailed Comments *

### Title & Abstract
- The title is descriptive but could be more impactful. Consider emphasizing the BER finding.
- The abstract is dense (250+ words) but well-structured. The key findings are clearly stated.
- The highlights section effectively captures the main contributions.

### Introduction
- The motivation is clear and well-supported with references.
- The 6-contribution list is too long—consolidate to 3–4.
- The paper organization paragraph is standard and appropriate.

### Literature Review / Theoretical Framework
- Comprehensive coverage of deep unfolding, channel estimation, and hardware deployment literature.
- The positioning against CNN/Transformer methods is appropriate.
- The gap identification is clear: no systematic BER validation of LISTA for channel estimation.

### Methodology / Research Design
- The LISTA architecture description is clear and standard.
- The experimental design is sound with proper controls.
- The statistical methodology (200 realizations, paired t-tests, Cohen's d) is rigorous.

### Results / Findings
- Results are well-presented with clear tables and figures.
- The BER-NMSE disconnect finding is the paper's highlight.
- The ablation study progression (5→20 seeds) demonstrates methodological maturity.

### Discussion
- The discussion honestly addresses limitations.
- The deployment recommendations are practical and actionable.
- The future research directions are relevant.

### Conclusion
- Conclusion accurately summarizes findings without over-claiming.
- The closing statement about LISTA as a "practical tool" is well-supported.

### References
- References are comprehensive and recent (up to 2024).
- Citation format is consistent with Elsevier style.

---

## Questions for Authors *

1. **Table 1 vs Table 7 discrepancy**: At N=64, K=5, M=256, L=20, SNR=20 dB, Table 1 reports LISTA NMSE = −24.25 ± 0.40 dB while Table 7 reports −32.29 ± 0.85 dB. These differ by ~8 dB. Which is correct? Were different training procedures used?
2. **LISTA-CP identical results**: You report that LISTA and LISTA-CP have identical parameters (max per-parameter difference = 0). Does this mean the weight clipping constraint never activates during training? If so, why does LISTA-CP exist as a separate architecture?
3. **Practical deployment gap**: The 33× speedup is measured in Python. For hardware deployment, you estimate 4.4× throughput advantage. Can you comment on the gap between these numbers and what accounts for it?

---

## Minor Issues

### Language / Grammar
- Abstract: "LISTA's NMSE saturates at approximately −25 dB" — consider "plateaus" for precision.
- Section 4.10: "LISTA consistently *outperforms* OMP" should be "LISTA achieves competitive BER with OMP" for QPSK.

### Figures and Tables
- All figures are clear and well-labeled.
- Table 4 (Ablation 5-seed) could include a footnote about statistical power limitations.

### Layout
- No significant layout issues detected.

---

## Dimension Scores *

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | BER-NMSE disconnect analysis is novel; LISTA for channel estimation is not new |
| Methodological Rigor (25%) | 78 | Strong | Good statistical practices; some inconsistency across tables |
| Evidence Sufficiency (25%) | 80 | Strong | 200 realizations, multiple seeds, effect sizes reported |
| Argument Coherence (15%) | 75 | Strong | Clear narrative with minor structural issues |
| Writing Quality (15%) | 76 | Strong | Professional prose; some density in abstract |
| **Weighted Average** | **75.6** | **Minor Revision** | |

---

## Recommendation to Peer Reviewers

I recommend the reviewers pay particular attention to:
1. The NMSE discrepancy across tables (R1 focus)
2. The completeness of the related work and comparison with recent LISTA variants (R2 focus)
3. The practical significance of the findings for the DSP community (R3 focus)
4. The validity of the BER-NMSE disconnect claim (DA focus)
