# EIC Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-ROUND8
- **Review Date**: 2026-06-01
- **Review Round**: Round 8

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief, *Digital Signal Processing* (Elsevier)

### Reviewer Identity
Prof. Elena Marchetti — Editor-in-Chief of *Digital Signal Processing*, with 20+ years of experience in adaptive signal processing, compressed sensing, and hardware-efficient algorithm design. Expertise in evaluating whether manuscripts meet the journal's standards for methodological clarity, practical relevance to signal processing practitioners, and contribution to the DSP literature.

### Review Focus
Journal fit, originality, overall significance, structural coherence, and alignment with the readership of *Digital Signal Processing*. I do not dive deep into statistical methodology (Reviewer 1's domain) or literature completeness (Reviewer 2's domain), but assess whether the paper as a whole merits publication in this venue.

---

## Overall Assessment

### Recommendation
**Minor Revision**

### Confidence Score
4 — High confidence. The paper falls squarely within signal processing and compressed sensing, which is my core area of editorial expertise. The deep unfolding aspect is adjacent to my primary specialization but well within my evaluation competence.

### Summary Assessment
This manuscript presents a systematic analysis of LISTA (Learned ISTA) applied to sparse channel estimation, covering NMSE performance, BER simulations, ablation studies, generalization analysis, and theoretical hardware complexity. The paper's primary contribution is not architectural novelty—LISTA is a well-known architecture—but rather a thorough, honest characterization of its behavior in the channel estimation context, including the important finding that LISTA's NMSE gap with OMP does not translate to BER penalty under MMSE equalization. The writing is clear, the experimental design is comprehensive, and the paper is commendably transparent about limitations (e.g., the NMSE saturation, the theoretical nature of hardware estimates). The main weakness is that the core architecture is not novel, which limits the originality score, and the qualitative comparison with CNN/Transformer baselines (Table 7) relies on indirect comparisons from different studies. Overall, the paper provides valuable engineering insights for the DSP community and, with minor revisions, would be a solid contribution to the journal.

---

## Strengths

### S1: Honest and Transparent Reporting of Negative Results
The paper does not shy away from reporting that LISTA trails OMP by 13–33 dB on Gaussian channels. This honesty is refreshing and valuable—the paper frames the NMSE gap as a starting point for deeper analysis rather than hiding it. The explicit statement that the saturation is "likely a training artifact" (Abstract, p. 1) and the acknowledgment that hardware estimates are theoretical demonstrate scientific integrity.

### S2: BER-NMSE Disconnect Analysis is a Genuine Insight
The finding that LISTA's NMSE gap does not translate to BER penalty under MMSE equalization, validated with 200 realizations and paired t-tests, is the paper's most impactful contribution. The mechanism analysis (99.9% error on true taps vs. 94.9% for OMP, Section 4.12) provides a principled explanation. This insight—that NMSE is the wrong metric for evaluating channel estimators when MMSE equalization is used—has practical implications beyond LISTA itself.

### S3: Comprehensive Ablation with Adequate Statistical Power
The progression from 5-seed ablation (Table 5, where threshold/per-layer effects appeared insignificant) to 20-seed ablation (Table 9, revealing all components as highly significant with Cohen's d = 18.4 and 24.1) demonstrates methodological self-correction. The paper explicitly acknowledges the false negative from low statistical power, which strengthens credibility.

### S4: Practical Deployment Framework
Section 4.7 and the Discussion provide actionable deployment recommendations (when to use SNR-specific training, when to prefer OMP/LASSO, the decision framework in Section 5.3). This goes beyond typical academic exercises and addresses what practitioners actually need.

### S5: Clear Writing and Well-Structured Experiments
The paper is well-organized with 13 clearly labeled experiments, each with its own table and figure. The cross-table consistency note (Section 4.3) explaining why Table 2 and Table 3 values differ at the same nominal configuration is a model of transparency.

---

## Weaknesses

### W1: Limited Originality — LISTA is a Well-Known Architecture
**Problem**: The paper applies a known architecture (LISTA, from Gregor & LeCun 2010) to a known problem (sparse channel estimation) without architectural novelty. The Related Work section (Section 2) acknowledges this, but the paper's contribution rests on "systematic analysis" rather than methodological innovation.
**Why it matters**: *Digital Signal Processing* publishes both novel algorithms and thorough analyses, but reviewers and readers may question whether the contribution is sufficient for a full paper.
**Suggestion**: Strengthen the framing in the Introduction by more explicitly positioning this as a "lessons learned" or "practical guide" paper for deep unfolding in channel estimation. Consider adding a brief comparison with at least one recent LISTA variant (e.g., OCLISTA or LISTA-AMP) beyond LISTA-CP to demonstrate awareness of the state of the art.
**Severity**: Major

### W2: Qualitative Comparison with CNN/Transformer Baselines (Table 7)
**Problem**: Table 7 compares LISTA with CNN and Transformer methods using values "from published results on comparable (but not identical) channel models." The paper acknowledges this is "indirect" comparison, but the table presents it alongside direct experimental results without clear visual differentiation.
**Why it matters**: Indirect comparisons can be misleading—different channel models, SNR ranges, and training protocols make apples-to-apples comparison impossible. Readers may misinterpret these as direct experimental findings.
**Suggestion**: Either (a) remove Table 7 and replace with a narrative discussion in Section 5.2, or (b) add a prominent footnote/caption making clear that CNN/Transformer values are from different experimental setups and cannot be directly compared. Option (a) is preferred.
**Severity**: Minor

### W3: The 16-QAM BER Advantage Under ZF Needs Stronger Caveating
**Problem**: The paper presents LISTA's statistically significant 16-QAM BER advantage under ZF equalization (Table 8) as a positive finding. However, ZF equalization is rarely used in practice precisely because of noise enhancement, and the BER values themselves are very high (0.29–0.32 at SNR 15–30 dB)—far above practical operating BER targets.
**Why it matters**: Framing a result at impractical BER levels as an "advantage" may overstate practical relevance.
**Suggestion**: Add a sentence clarifying that the 16-QAM BER values under ZF are well above practical operating thresholds (typically 10⁻³), and that the finding is primarily of theoretical interest for understanding error structure rather than a practical deployment recommendation.
**Severity**: Minor

### W4: No Comparison with Structured LISTA Variants
**Problem**: The paper identifies O(N²) per-layer complexity as a scalability limitation (Section 4.13, Table 11) and suggests "structured linear mappings (Toeplitz, circulant, low-rank)" as a solution, but does not implement or evaluate any structured variant.
**Why it matters**: The scalability concern is real (training diverges at N=256), and without even a proof-of-concept structured variant, the paper's claim that LISTA is "practical" for channel estimation is weakened.
**Suggestion**: If feasible, add a brief experiment with a structured W^(k) (e.g., low-rank approximation) to demonstrate that the scalability limit can be addressed. If not feasible, acknowledge this more prominently as a critical limitation.
**Severity**: Major

---

## Detailed Comments

### Journal Fit
The paper is an excellent fit for *Digital Signal Processing*. It addresses a core DSP problem (sparse channel estimation), uses well-established signal processing tools (compressed sensing, deep unfolding), and provides practical insights (BER analysis, hardware complexity). The methodology and writing style align with the journal's readership.

### Originality
The originality is adequate but not exceptional. The LISTA architecture is well-known, and the application to channel estimation has been explored before (cited in Section 2). The paper's novelty lies in: (1) the BER-NMSE disconnect analysis, (2) the systematic ablation with statistical rigor, and (3) the practical deployment framework. These are valuable contributions but are incremental rather than transformative.

### Significance
The BER-NMSE disconnect finding has broad significance for the channel estimation community—it challenges the assumption that NMSE is the right metric for evaluating estimators in MMSE-based systems. The practical deployment framework is also useful. However, the impact is limited by the fact that LISTA itself is not state-of-the-art for sparse recovery (OMP and LASSO outperform it on NMSE).

### Structural Coherence
Excellent. The paper flows logically from problem formulation → method → experiments → discussion → conclusion. Each experiment builds on the previous one. The cross-table consistency note (Section 4.3) is a model of transparency.

### Title & Abstract
The title accurately reflects the paper's content. The abstract is comprehensive but long (~350 words)—consider trimming by 50–100 words for readability. The highlights are well-written and capture the key findings.

### Conclusion
The conclusion accurately summarizes the findings without overclaiming. The explicit acknowledgment that "measured FPGA/ASIC validation remains future work" is appropriate.

---

## Questions for Authors

1. The paper reports that LISTA training diverges at N=256 (Table 3, Section 4.3). Have you investigated whether reducing the number of layers L (e.g., L=5 or L=10) at N=256 prevents divergence? This would help clarify whether the divergence is due to insufficient oversampling or network depth.

2. Table 7 presents indirect comparisons with CNN/Transformer methods. Would you consider removing this table and replacing it with a narrative discussion to avoid potential misinterpretation?

3. The 20-seed ablation (Table 9) uses only 5 seeds per configuration in the initial ablation (Table 5). Have you considered running the 20-seed ablation with non-parametric tests (Wilcoxon signed-rank) in addition to the paired t-tests, given the small sample sizes?

---

## Minor Issues

### Language / Grammar
- Abstract, p. 1: "attributable to LISTA's error concentration on true taps" — this phrase appears 3 times in the abstract; consider varying the phrasing.
- Section 4.1, p. 6: "LISTA consistently outperforms LMS and NLMS across all SNR levels by ~1–17 dB" — the range "1–17 dB" is very wide; consider narrowing to a more typical range.

### Figures and Tables
- Table 1 (NMSE vs SNR): The table has 6 columns but the header alignment could be improved for readability.
- Figure 1: Consider adding a horizontal dashed line at -25 dB to visually highlight the LISTA saturation level.

### Layout
- The paper uses `\FloatBarrier` after each figure, which is good practice but may cause formatting issues with some LaTeX configurations.

---

## Recommendation to Peer Reviewers

I recommend that Reviewer 1 (Methodology) pay special attention to:
- The statistical validation of the BER results (200 realizations, 5 seeds, paired t-tests)
- The ablation study design and the progression from 5-seed to 20-seed experiments
- The theoretical hardware complexity analysis and whether the assumptions are justified

I recommend that Reviewer 2 (Domain) pay special attention to:
- The positioning of LISTA relative to recent LISTA variants (OCLISTA, LISTA-AMP)
- The completeness of the deep unfolding and channel estimation literature
- The qualitative comparison with CNN/Transformer methods

I recommend that Reviewer 3 (Perspective) pay special attention to:
- The practical deployment implications and whether the recommendations are realistic
- The scalability limitations and their impact on real-world applicability

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 58 | Weak | Known architecture applied to known problem; novelty lies in systematic analysis rather than methodological innovation |
| Methodological Rigor (25%) | 78 | Strong | Comprehensive experiments with statistical validation; some concerns about indirect comparisons |
| Evidence Sufficiency (25%) | 82 | Strong | 13 experiments, multiple seeds, paired t-tests, effect sizes; ITU channel validation |
| Argument Coherence (15%) | 85 | Strong | Logical flow from NMSE saturation → BER analysis → mechanism → deployment |
| Writing Quality (15%) | 83 | Strong | Clear, well-organized, transparent about limitations |
| **Weighted Average** | **76.3** | **Minor Revision** | |
