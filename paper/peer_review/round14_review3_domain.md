# Peer Review Report — Reviewer 2 (Domain)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 14

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain Expert)

### Reviewer Identity
Prof.~Philip Schniter, Department of Electrical and Computer Engineering, The Ohio State University. Expertise in sparse signal recovery, approximate message passing (AMP), deep unfolding for communications, and compressed sensing theory. Author of seminal works on learned AMP and structured sparsity models. Review focus: literature coverage, theoretical framework, domain contribution, and positioning within the sparse recovery and deep unfolding communities.

### Review Focus
Completeness of literature review in sparse channel estimation and deep unfolding, accuracy of theoretical claims, novelty of the contribution relative to prior LISTA/channel estimation work, and significance of findings for the compressed sensing and communications communities.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
5 — Completely within my area of expertise, I am very confident in my assessment.

### Summary Assessment
This manuscript presents a thorough empirical analysis of LISTA applied to sparse channel estimation, with the primary contribution being the "error concentration mechanism"---the finding that LISTA concentrates $99.9\%$ of estimation error on true tap locations. The paper is well-positioned within the deep unfolding literature and provides honest, comprehensive comparisons against classical baselines. The literature review is extensive, covering sparse channel estimation, deep unfolding, and deep learning for channel estimation. However, several domain-specific concerns should be addressed: (1) the paper does not discuss the relationship between LISTA's learned $\mathbf{W}^{(k)}$ matrices and the Bethe Hessian / Onsager corrections from AMP theory, which would provide theoretical grounding for the mechanism analysis; (2) the ITU channel experiments use a fixed $M=256$ pilot length, which is not standard for ITU channel evaluation; (3) the comparison with LISTA-AMP and OCLISTA is only qualitative. Despite these gaps, the paper makes a solid contribution to understanding deep-unfolded sparse recovery in the channel estimation context.

---

## Strengths

### S1: Honest and Comprehensive Baseline Comparisons
The paper compares against a remarkably complete set of baselines: LMS, NLMS, OMP (oracle $K$), LASSO (grid-searched $\lambda$), FISTA (grid-searched threshold), ISTA (control), and LISTA-CP. The FISTA comparison (Table 12) is particularly important---many LISTA papers omit this natural baseline, and the finding that FISTA outperforms LISTA by 1--27~dB is a significant contribution to the field's understanding of deep unfolding's value proposition.

### S2: Error Concentration as a Mechanism, Not Just a Metric
The paper's key insight is reframing the BER-NMSE disconnect as an error *location* problem rather than an error *magnitude* problem. The ISTA control experiment (Table 15) elegantly separates the generic soft-thresholding effect ($97.2\%$) from LISTA's learned enhancement ($99.9\%$). The $50\times$ reduction in non-support error (vs.~OMP) and $28\times$ reduction (vs.~ISTA) are clean, interpretable results that advance understanding of why deep-unfolded networks behave differently from their algorithmic counterparts.

### S3: Cross-Distribution Generalization to ITU Channels
The evaluation on ITU PedA and VehA channel models (Table 6) is a valuable addition. The finding that LISTA trained on i.i.d.~Gaussian data achieves comparable performance on ITU channels ($-23$ to $-27$~dB) demonstrates practical generalizability. The error concentration mechanism also generalizes ($99.3$--$99.5\%$ on ITU vs.~$99.9\%$ on Gaussian), suggesting it is an architectural property rather than a distribution-specific artifact.

### S4: SNR Saturation Analysis with Training Distribution Sensitivity
The cross-table consistency analysis (Table 3) and the SNR mitigation experiments (Table 9) provide important practical insights. The 8~dB sensitivity to training distribution is a finding that practitioners need to know, and the paper presents it transparently rather than hiding it.

---

## Weaknesses

### W1: Missing Connection to AMP Theory
**Problem**: The paper does not discuss the relationship between LISTA's learned parameters and the Onsager correction terms from approximate message passing (AMP) theory. \citet{liu2023listamp} demonstrated that LISTA-AMP achieves near-oracle performance by incorporating AMP corrections. The paper's finding that LISTA's $\mathbf{W}^{(k)}$ captures "inter-tap dependencies" (Section 4.5) could be theoretically grounded by connecting to the Bethe Hessian or state evolution frameworks.
**Why it matters**: Without this connection, the mechanism analysis remains empirical. Understanding *why* LISTA concentrates error on true taps (beyond "soft-thresholding does this") would strengthen the contribution significantly.
**Suggestion**: Add a brief discussion in Section 5.1 connecting the error concentration mechanism to AMP theory. Specifically, discuss whether LISTA's learned $\mathbf{W}^{(k)}$ approximates the Onsager correction that prevents noise amplification in AMP.
**Severity**: Major

### W2: Fixed Pilot Length Across Channel Models
**Problem**: All experiments use $M=256$ pilots, regardless of channel length $N$. For ITU channels (Table 6), the pilot ratio $M/N = 4$ (with $N=64$), which is generous. In practice, pilot overhead is a critical constraint, and the paper does not evaluate how LISTA performs under tighter pilot budgets (e.g., $M/N = 1.5$ or $M/N = 2$).
**Why it matters**: The practical value of LISTA depends on its performance under realistic pilot constraints. The training divergence at $N=256$ (Table 2, $M/N = 1$) hints at sensitivity to pilot ratio, but this is not systematically explored.
**Suggestion**: Add an experiment varying $M/N$ ratio (e.g., $M \in \{96, 128, 192, 256\}$ for $N=64$) to characterize LISTA's pilot efficiency. This would also connect to the compressed sensing literature on measurement complexity.
**Severity**: Major

### W3: No Comparison with LISTA-AMP or OCLISTA
**Problem**: The paper mentions LISTA-AMP~\citep{liu2023listamp} and OCLISTA~\citep{borgerding2020ista} in the Related Work and Discussion but does not compare against them experimentally. The paper hypothesizes that "these variants would exhibit similar saturation under broad-range mixed-SNR training" (Section 5.1), but this is not validated.
**Why it matters**: LISTA-AMP and OCLISTA are the state-of-the-art LISTA variants. Without experimental comparison, the paper cannot claim to provide a complete analysis of deep-unfolded sparse channel estimation.
**Suggestion**: If implementing these variants is infeasible, at least provide a more detailed theoretical argument for why they would behave similarly. Alternatively, cite published results on these variants under comparable conditions.
**Severity**: Minor

### W4: Sparse Channel Model Limitations
**Problem**: The i.i.d.~Gaussian tap amplitude model ($\mathcal{N}(0, 1)$) is standard but simplistic. Real channels have correlated tap amplitudes (partially addressed by ITU models), frequency-dependent path loss, and non-Gaussian statistics (e.g., Rayleigh/Rician fading). The paper does not discuss how these factors might affect the error concentration mechanism.
**Why it matters**: The generalizability claims are based on two ITU models, which is a limited sample. The paper should acknowledge this limitation more explicitly.
**Suggestion**: Add a paragraph in Section 5.4 (Limitations) acknowledging that the i.i.d.~Gaussian model does not capture all real-world channel characteristics, and that the generalizability to frequency-selective fading, time-varying channels, and MIMO systems remains unverified.
**Severity**: Minor

---

## Detailed Comments

### Literature Review
- The coverage of sparse channel estimation (Section 2.1) is comprehensive, citing the seminal works of \citet{bajwa2010compressed} and \citet{berger2010application}.
- The deep unfolding section (Section 2.2) covers the key variants: LISTA, ISTA-Net, LISTA-CP, OCLISTA, and LISTA-AMP. However, it omits recent works on learned approximate message passing (LAMP) and denoising-based AMP (D-AMP), which are relevant to the mechanism analysis.
- The deep learning section (Section 2.3) is thorough, covering CNN, Transformer, and model-driven approaches.
- The classical adaptive filtering section (Section 2.4) is brief but adequate.

### Theoretical Framework
- The problem formulation (Section 3.1) is standard and correct.
- The ISTA/LISTA derivation (Sections 3.2--3.3) is clear and well-presented.
- The parameter analysis (Section 3.4) is useful for understanding scalability.
- The computational complexity analysis (Section 3.6) is thorough.

### Academic Argument Accuracy
- The claim that "LISTA concentrates $99.9\%$ of estimation error on true tap locations" is well-supported by Table 14.
- The claim that "this provides direct evidence explaining LISTA's BER behavior" (Abstract) is supported by the ZF BER results (Table 10).
- The claim that "error concentration is partially generic to soft-thresholding" (Section 4.12.3) is supported by the ISTA control experiment.

### Incremental Contribution
- The paper's contribution is primarily analytical rather than methodological. The mechanism analysis is novel and valuable, but the lack of architectural novelty limits the contribution.
- The FISTA comparison and LISTA-CP comparison are valuable additions that clarify LISTA's position in the algorithmic landscape.

---

## Questions for Authors

1. Can you provide a theoretical explanation for *why* LISTA's learned parameters enhance error concentration from $97.2\%$ (ISTA) to $99.9\%$? Specifically, does the learned $\mathbf{W}^{(k)}$ approximate the Onsager correction from AMP theory?

2. How does LISTA perform under tighter pilot budgets (e.g., $M/N = 1.5$ or $M/N = 2$)? The current experiments only test $M/N = 4$ for $N=64$.

3. The ITU channel models (PedA, VehA) have specific power delay profiles. Have you tested on other standardized channel models (e.g., EPA, EVA from 3GPP) to assess generalizability across a broader range of channel types?

4. The paper states that "LISTA's support recovery ($J = 0.78$) is lower than OMP's ($J = 0.97$)" (Section 5.4). Where does this $J = 0.78$ value come from? It is not present in Table 13, which reports $J = 0.90$--$0.93$ for LISTA at SNR $\geq 10$~dB.

---

## Minor Issues

### Literature Gaps
- Missing citation to \citet{sprechmann2015learning} in the context of learned proximal operators (mentioned in Related Work but not discussed).
- The paper cites \citet{liu2023listamp} but does not compare against LISTA-AMP. Consider either removing the citation or adding a more detailed discussion of why comparison is deferred.

### Figures and Tables
- Table 6 (ITU channels): The LMS and NLMS values lack standard deviations. Are these single-seed results?
- Table 12 (FISTA comparison): The $\Delta$ column is helpful but consider also reporting the relative improvement percentage.

### Terminology
- The paper uses "error concentration" and "error sparsity" somewhat interchangeably. Consider standardizing terminology: "error concentration on support" (the fraction of error on true taps) vs.~"error sparsity" (the Gini coefficient of the error distribution).

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 64 | Adequate | Mechanism analysis is novel; no architectural innovation. |
| Methodological Rigor (25%) | 78 | Strong | Sound experimental design with minor gaps (pilot ratio, BER sample size). |
| Evidence Sufficiency (25%) | 76 | Strong | Comprehensive baselines but missing LISTA-AMP/OCLISTA comparison. Literature gaps in AMP theory. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow from NMSE saturation to mechanism to BER implications. |
| Writing Quality (15%) | 82 | Strong | Professional prose, good transparency. |
| Literature Integration | 72 | Adequate | Good coverage of deep unfolding and channel estimation literature; missing AMP-theory connection. |
| **Weighted Average** | **76.0** | **Minor Revision** | |

---

