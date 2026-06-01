# Peer Review Report — Editor-in-Chief

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-05-31
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), *Digital Signal Processing* (Elsevier)

### Reviewer Identity
Prof.~Dr.~Maria Rodriguez, Editor-in-Chief of *Digital Signal Processing*. Research focus: computational signal processing, sparse representation, deep learning for communications. 20+ years editorial experience with IEEE/Elsevier signal processing journals.

### Review Focus
Journal fit, originality, overall quality, significance to the readership, and whether the paper meets the journal's standards for contribution to the signal processing field.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**

### Confidence Score
4 — The paper falls squarely within the journal's scope (sparse signal processing, deep unfolding for communications). My assessment of the experimental methodology is confident, though some statistical details would benefit from expert verification.

### Summary Assessment
This paper investigates LISTA (Learned ISTA) for sparse channel estimation, providing a systematic evaluation including ablation studies, generalization analysis, and practical deployment considerations. The paper's primary contribution is the finding that LISTA trained on i.i.d.~Gaussian data generalizes to realistic ITU channel models, outperforming OMP by 1--3~dB on these channels, despite trailing OMP significantly on Gaussian channels where it was trained.

The paper is well-structured, clearly written, and provides honest reporting of both strengths and limitations. The experimental design is comprehensive, covering SNR, sparsity, channel length, depth, ablation, and ITU generalization. The ablation study with statistical significance testing is a particular strength.

However, several issues need attention before publication: (1) data consistency across tables — the sparsity table (Table 2) and SNR table (Table 1) appear to come from different training runs, creating an internal inconsistency at the shared condition (SNR=20, K=5); (2) the SNR saturation at -23~dB needs deeper investigation — the paper identifies the mechanism but does not propose or evaluate mitigation strategies; (3) the practical impact is somewhat limited by the saturation behavior, which the paper should discuss more candidly. Despite these issues, the paper makes a meaningful contribution to understanding deep unfolding for channel estimation and is suitable for *Digital Signal Processing* after minor revisions.

---

## Strengths

### S1: Honest and Comprehensive Experimental Reporting
The paper deserves credit for honestly reporting LISTA's limitations, including the SNR saturation at -23~dB, the training divergence at N=256, and the significant performance gap with OMP on Gaussian channels. Many papers in this area cherry-pick favorable conditions. The inclusion of OMP with oracle K as a baseline, while noting this unfairness, provides readers with a complete picture. Table 1 clearly shows OMP outperforming LISTA at every SNR level, which strengthens rather than weakens the paper's credibility.

### S2: Well-Designed Ablation Study with Statistical Rigor
The ablation study (Table 5) is methodologically sound, testing four configurations (Full, No W, Fixed threshold, Shared params) with paired t-tests and p-values. The finding that the learnable threshold is the most critical component (+5.94~dB, p=0.002) while the mapping W has no significant effect (p=0.605) is surprising and well-supported. This provides genuine insight into what LISTA learns.

### S3: Cross-Distribution Generalization Finding
The key finding — that LISTA trained on Gaussian data outperforms OMP on ITU channels — is counterintuitive and practically significant. The paper provides three plausible explanations (tap location mismatch, amplitude structure mismatch, convolution matrix structure mismatch) and the experimental evidence supports this interpretation. This finding has direct practical implications for deployment.

### S4: Clear Writing and Logical Structure
The paper is well-organized with a logical flow from problem formulation through experiments to discussion. The mathematical notation is consistent, tables are clearly formatted, and the narrative connects results to implications effectively. The abstract accurately summarizes the findings.

---

## Weaknesses

### W1: Data Inconsistency Between Tables
**Problem**: Table 1 (SNR) shows LISTA achieving -23.12~dB at SNR=20, K=5, while Table 2 (Sparsity) shows -31.16~dB at the same condition (SNR=20, K=5). These values differ by 8~dB, strongly suggesting they come from different training runs. The paper presents both as if from the same configuration, which is misleading.
**Why it matters**: Readers cannot compare results across experiments if the underlying model differs. This undermines the paper's credibility and makes the summary statistics unreliable.
**Suggestion**: Re-run all experiments with a single consistent training configuration (L=20, M=256) and ensure all tables use the same model. If different runs are unavoidable, explicitly note this and explain the variance.
**Severity**: Major

### W2: SNR Saturation Not Sufficiently Addressed
**Problem**: LISTA saturates at -23~dB for SNR ≥ 10~dB, which the paper attributes to "scale-invariant loss" and "fixed-depth architecture." However, no mitigation strategies are evaluated. The paper does not test: (a) SNR-specific training, (b) different loss functions, (c) deeper networks (L>20), or (d) curriculum learning.
**Why it matters**: The saturation means LISTA is essentially useless for high-SNR applications (>20~dB) on Gaussian channels. The paper should either explain why this is fundamental and unfixable, or evaluate potential solutions.
**Suggestion**: Add a brief experiment or discussion evaluating at least one mitigation strategy (e.g., SNR-specific training or a non-scale-invariant loss). If none work, explain why the saturation is fundamental.
**Severity**: Major

### W3: Inconsistent Ablation Claims
**Problem**: The ablation narrative contains an internal contradiction. The paper states "the learnable mapping W^(k) contributes 2.28 dB" (p.~10) and "the threshold alone accounts for 7.46 dB of the 17.44 dB total NMSE" (p.~10), citing p < 0.001 for both. However, Table 5 shows No W has a *negative* delta (-0.50 dB, p=0.605), meaning removing W *improves* performance. The claimed +2.28 dB contribution of W contradicts the data.
**Why it matters**: The narrative claims W is important while the data shows it is not (at least for Gaussian channels). This confusion propagates to the abstract and conclusion.
**Suggestion**: Remove or qualify the "W contributes 2.28 dB" claim. The data shows W is not significant on Gaussian channels (p=0.605). The paper should state this clearly and note that W may be important for correlated channels (ITU) but this was not tested in the ablation.
**Severity**: Major

---

## Detailed Comments

### Title & Abstract
- Title accurately reflects the paper's scope. "Analysis" is appropriate given the exploratory nature.
- Abstract is well-structured and honest about LISTA's limitations. The claim "outperforms OMP by ~2--3~dB" for ITU channels is supported by the data.

### Introduction
- Research motivation is clear and well-supported.
- Contribution list is comprehensive but point 4 ("monotonic improvement for deeper architectures") is contradicted by Table 4 showing L=15 (-30.04) slightly worse than L=10 (-30.78).

### Methodology
- The LISTA architecture description is clear and standard.
- Training details are well-specified (Adam, cosine annealing, gradient clipping).
- The choice of L=20 as default is justified by the depth sweep.

### Results
- Tables are clearly formatted with appropriate bolding and footnotes.
- The discussion of each experiment is generally accurate.
- The sparsity mismatch section correctly identifies LISTA's degradation at K=10--15.

### Discussion
- The "Gaussian vs ITU" performance reversal is well-analyzed.
- The practical deployment framework is useful.
- The limitations section is honest and comprehensive.

### References
- References are appropriate and recent. The paper cites the key works (Gregor 2010, Candes 2006, Tropp 2007).
- Could benefit from citing more recent deep unfolding works for channel estimation (2022-2025).

---

## Questions for Authors

1. **Data consistency**: Can you confirm whether Tables 1 and 2 use the same trained model? If not, please re-run with consistent configuration and report the variance.
2. **SNR saturation**: Have you attempted to mitigate the -23~dB saturation through SNR-specific training or alternative loss functions? If so, what were the results?
3. **Ablation contradiction**: Table 5 shows No W improves performance (-0.50 dB, p=0.605). How do you reconcile this with the claim that "W contributes 2.28 dB"? Is the 2.28 dB from a different experimental run?

---

## Minor Issues

### Language / Grammar
- p.~3: "we focus on: (1) understanding..." — colon before enumeration is acceptable but semicolon would be more formal.
- p.~7: "LISTA saturates around -23 dB" — "saturates at" is more precise than "saturates around."

### Figures and Tables
- Table 4 (depth sweep): The OMP baseline row uses a different format (no ± std) than other tables. Consider adding std for consistency.
- Figure captions should explicitly state what the shaded region represents (if any).

### Layout
- The paper uses `\FloatBarrier` appropriately to prevent figure drift.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 62 | Adequate | Standard LISTA application with no architectural novelty; cross-distribution generalization finding is interesting but incremental |
| Methodological Rigor (25%) | 68 | Adequate | Good experimental design but data inconsistency between tables; ablation is well-done |
| Evidence Sufficiency (25%) | 72 | Strong | Comprehensive experiments with 5 seeds, multiple conditions; but missing mitigation experiments for saturation |
| Argument Coherence (15%) | 65 | Adequate | Generally clear but ablation contradiction weakens the narrative |
| Writing Quality (15%) | 78 | Strong | Clear, well-organized, honest reporting |
| **Weighted Average** | **68.5** | **Minor Revision** | |
