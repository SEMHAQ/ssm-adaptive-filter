# Peer Review Report — Reviewer 2 (Domain Expert)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-ROUND17
- **Review Date**: 2026-06-01
- **Review Round**: Round 17

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert (Sparse Channel Estimation / Compressed Sensing)

### Reviewer Identity
Prof. Li Wei, Professor at Tsinghua University, Department of Electronic Engineering. Expertise in compressed sensing for wireless communications, sparse channel estimation, and approximate message passing algorithms. Published 80+ papers on sparse recovery theory and applications. Review focuses on literature completeness, theoretical framework accuracy, and domain contribution.

### Review Focus
Literature coverage completeness, accuracy of compressed sensing and AMP theory references, positioning relative to existing LISTA variants, and the paper's contribution to the sparse channel estimation field.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Accept**
- [ ] **Reject**

### Confidence Score
5 — Sparse channel estimation and AMP theory are my primary research areas.

### Summary Assessment
This paper provides a thorough empirical analysis of LISTA applied to sparse channel estimation, with a central finding about error concentration on true tap locations. The literature review is comprehensive, covering deep unfolding, sparse channel estimation, and deep learning for channel estimation. The comparison against LISTA-CP, FISTA, and ISTA control experiments positions the work well within the LISTA variant landscape. However, the paper's treatment of AMP theory (Section 5.1) is superficial—the connection between W^(k) and the Onsager correction is hypothesized but not validated, and the paper does not engage with the rich AMP literature on state evolution and phase transitions. The contribution to the sparse channel estimation field is primarily empirical characterization rather than theoretical advance, which is appropriate for *Digital Signal Processing* but should be honestly framed.

---

## Strengths

### S1: Comprehensive Literature Coverage
The related work section (Section 2) covers sparse channel estimation, deep unfolding, deep learning for channel estimation, and classical adaptive filtering. The inclusion of recent LISTA variants (LISTA-CP, OCLISTA, LISTA-AMP, ALISTA, LISTA-CPSS, Elastic LISTA) demonstrates thorough engagement with the literature. The hardware deployment subsection (Section 2.3) is a valuable addition.

### S2: Appropriate Positioning Relative to LISTA Variants
The comparison against LISTA-CP (Section 4.8) and the discussion of OCLISTA, LISTA-AMP, and ALISTA (Section 5.1) appropriately position the work within the LISTA variant landscape. The finding that LISTA-CP achieves identical performance because the weight constraint is naturally satisfied is a useful contribution to understanding LISTA behavior.

### S3: ITU Channel Model Evaluation
Testing on ITU PedA and VehA channels (Section 4.7.2) is important for practical relevance. The finding that LISTA generalizes to ITU channels with comparable performance (−23 to −27 dB) without channel-specific training is practically useful. The error concentration analysis on ITU channels (Table 15) extends the mechanism beyond i.i.d. Gaussian assumptions.

### S4: Honest Assessment of LISTA vs. FISTA
The FISTA comparison (Table 12) is a significant strength. By demonstrating that FISTA with 20 iterations outperforms LISTA by 1–27 dB, the paper honestly positions LISTA's value as lying in error concentration and potential hardware pipelining, not NMSE accuracy. This clarity is refreshing and helps practitioners make informed choices.

### S5: Pilot Ratio Analysis
The pilot ratio analysis (Table 6) characterizes LISTA's measurement efficiency, showing that M/N ≥ 2 is required for stable operation. This is important for practical deployment where pilot overhead is a concern. The finding that LISTA's NMSE degrades gracefully (−25.3 to −17.6 dB as M/N decreases from 4.0 to 1.5) is useful.

---

## Weaknesses

### W1: AMP Theory Treatment is Superficial
**Problem**: Section 5.1 discusses the connection between LISTA's W^(k) and the Onsager correction from AMP theory, citing Borgerding et al. (2020) and Liu et al. (2023). However, the paper does not engage with the AMP literature on state evolution, phase transitions, or Bayes-optimal recovery. The claim that "W^(k) implicitly approximate a decorrelation function similar to the Onsager correction" is unsubstantiated.
**Why it matters**: AMP theory provides precise predictions about sparse recovery performance (e.g., state evolution equations, phase transition curves). The paper's AMP discussion is at the level of analogy rather than rigorous connection.
**Suggestion**: Either (a) add a quantitative comparison between W^(k) and the theoretical Onsager correction matrix, or (b) significantly weaken the AMP framing and cite it only as motivation for future work. Remove the AMP connection from the abstract and highlights if not empirically validated.
**Severity**: Major

### W2: Missing References on Error Concentration in Sparse Recovery
**Problem**: The paper's central finding—that LISTA concentrates error on true support—is related to known results in sparse recovery theory. The debiasing property of LASSO (where support-set errors dominate) and the support recovery guarantees of OMP are well-studied. The paper does not connect its findings to this existing body of theory.
**Why it matters**: Without this connection, the paper's contribution appears more novel than it may actually be. The 100% concentration finding should be contextualized against theoretical predictions.
**Suggestion**: Add a discussion connecting the error concentration findings to LASSO debiasing theory and OMP support recovery guarantees. This would strengthen the theoretical positioning.
**Severity**: Major

### W3: Sparsity Assumption Discussion
**Problem**: The paper assumes K is known for OMP (oracle setting) but not for LISTA. This is a fair comparison choice, but the paper does not discuss how LISTA performs when the sparsity level is unknown and must be estimated—a common practical scenario. The pilot ratio analysis (Table 6) touches on this indirectly but a direct experiment would strengthen the practical contribution.
**Why it matters**: In practice, K is rarely known exactly. LISTA's advantage of not requiring K as input is mentioned (Section 3.6) but not experimentally validated.
**Suggestion**: Add a brief experiment comparing LISTA against OMP with estimated K (e.g., using cross-validation or information criteria). This would validate the claimed advantage.
**Severity**: Minor

### W4: Complex-Valued Channel Extension is Incomplete
**Problem**: The complex-valued extension (Appendix A) uses magnitude-based soft-thresholding and separate real/imaginary weight matrices. However, the error concentration drops from 100.0% to 97.8%, and the paper does not discuss whether this drop is statistically significant (5 seeds). The NMSE saturation persists at −22 dB, and the paper does not compare against complex OMP's NMSE trend.
**Why it matters**: Practical wireless systems use complex-valued channels. The 2.2% non-support error in the complex case may have different BER implications than the 0.01% in the real case.
**Suggestion**: Report statistical significance of the 100.0% vs 97.8% difference. Add the complex OMP NMSE trend to Table 16 for comparison. Discuss BER implications of the 2.2% non-support error.
**Severity**: Minor

### W5: Measurement Matrix Properties Not Discussed
**Problem**: The paper uses BPSK pilot signals (±1) forming the measurement matrix X. The paper does not discuss the coherence or restricted isometry properties (RIP) of this matrix, which are fundamental to compressed sensing recovery guarantees. The condition number of X affects all methods' performance.
**Why it matters**: The measurement matrix properties determine the theoretical recovery limits. Without this analysis, the NMSE saturation cannot be properly attributed to the method versus the measurement setup.
**Suggestion**: Report the condition number or mutual coherence of X for the default configuration. Discuss whether the M/N ratio analysis (Table 6) is related to measurement matrix conditioning.
**Severity**: Minor

---

## Detailed Comments

### Literature Review / Theoretical Framework
- Section 2.1: Good coverage of Bajwa (2010), Berger (2010), OMP, LASSO, ISTA/FISTA. Missing: Candes & Plan (2011) on near-ideal model selection, which is relevant to the sparsity mismatch analysis.
- Section 2.2: Comprehensive LISTA variant coverage. The inclusion of ALISTA, LISTA-CPSS, and Elastic LISTA is commendable. Missing: Xu et al. (2020) on ISTA-Net++ which is a major deep unfolding work for image reconstruction.
- Section 2.3: Good coverage of CNN, Transformer, and model-driven methods. The hardware deployment subsection is valuable.
- Section 2.4: Brief but adequate coverage of LMS/NLMS/PNLMS.

### Methodology / Research Design
- The LISTA architecture (Section 3.3) is standard and well-described. The FFT-based convolution (Eq. 8) is a practical implementation detail.
- The parameter analysis (Section 3.4) correctly identifies the O(N²) scaling issue. The 82K parameter count at N=64 is modest.
- The computational complexity analysis (Section 3.5) is fair and honest.

### Results / Findings
- Table 1: The FISTA comparison is a major strength. The 1–27 dB gap clearly demonstrates LISTA's NMSE limitation.
- Table 9: SNR-specific training results are practically valuable. The 6 dB improvement is significant.
- Table 12: The LISTA-CP comparison is well-interpreted.
- Table 15: ITU error concentration results extend the mechanism analysis convincingly.

### Discussion
- Section 5.1: The AMP discussion needs strengthening (see W1). The connection to Onsager correction is interesting but unsubstantiated.
- Section 5.2: The CNN comparison is appropriate and well-interpreted.
- Section 5.3: The deployment framework is practical and useful.

### References
- The reference list is comprehensive (40+ citations). Recent papers (2020–2024) are well-represented.
- Missing key references: Candes & Plan (2011), Xu et al. (2020) ISTA-Net++, Donoho et al. (2009) AMP original paper (cited but could be more prominently discussed).

---

## Questions for Authors

1. The paper claims W^(k) "implicitly approximate a decorrelation function similar to the Onsager correction" (Section 5.1). Have you computed the actual Onsager correction matrix for your experimental setup and compared it to the learned W^(k)? If not, how strong is this claim?

2. For the error concentration metric, how does the 100.0% result change if you use a different definition of the support set (e.g., taps above a threshold rather than top-K)? The current definition assumes K is known.

3. The paper reports LISTA's NMSE on ITU channels (−23 to −27 dB) but does not report the error concentration for the complex-valued ITU case. Can you provide these results?

4. The pilot ratio analysis (Table 6) shows LISTA diverges at M/N=1.5 with 1/5 seeds. Is this divergence related to the measurement matrix becoming ill-conditioned? Can you report the condition number of X at each M/N ratio?

---

## Minor Issues

### Citation Format
- Reference [22] (liu2023listamp) and [25] (liu2021elastic_lista) are recent additions; verify they are correctly formatted for the CAS template.
- Reference [32] (wu2024deep) is listed as 2024; verify this is published, not in press.

### Figures and Tables
- Table 12: The Δ column header should specify "FISTA − LISTA" more clearly.
- Table 15: The "Ratio" column is ambiguous—specify "OMP non-support error / LISTA non-support error."

### Layout
- Section 4.13 has many subsections (4.13.1–4.13.7). Consider consolidating some into a single "Mechanism Analysis" section with clearer structure.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 66 | Adequate | Error concentration characterization is novel in channel estimation; AMP connection unsubstantiated |
| Methodological Rigor (25%) | 80 | Strong | Comprehensive experiments; statistical validation; minor power issues |
| Evidence Sufficiency (25%) | 83 | Strong | Multiple experiments, baselines, seeds; literature coverage comprehensive |
| Argument Coherence (15%) | 78 | Strong | Clear narrative; AMP connection weakens coherence |
| Writing Quality (15%) | 82 | Strong | Clear, professional; minor verbose passages |
| Literature Integration | 75 | Strong | Comprehensive coverage; missing a few key references |
| **Weighted Average** | **77.8** | **Minor Revision** | |

---

*Report submitted by Reviewer 2 (Domain Expert)*
