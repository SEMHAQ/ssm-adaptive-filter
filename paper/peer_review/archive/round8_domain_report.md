# Domain Review Report (Peer Reviewer 2)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-ROUND8
- **Review Date**: 2026-06-01
- **Review Round**: Round 8

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain Expert)

### Reviewer Identity
Prof. Liang Wei — Full Professor of Wireless Communications and Signal Processing, with 18 years of research on sparse channel estimation, compressed sensing for communications, and deep learning for physical-layer processing. Published 60+ journal papers on sparse recovery, adaptive filtering, and model-based deep learning. Associate Editor of *IEEE Transactions on Signal Processing* and *IEEE Transactions on Wireless Communications*.

### Review Focus
Literature coverage and completeness, theoretical framework appropriateness, domain-specific accuracy of claims, and the paper's positioning within the sparse channel estimation and deep unfolding literature. I assess whether the paper correctly situates itself in the field and whether the domain-specific claims are accurate.

---

## Overall Assessment

### Recommendation
**Minor Revision**

### Confidence Score
5 — Completely within my area of expertise. Sparse channel estimation, compressed sensing, and deep unfolding are my primary research areas.

### Summary Assessment
This paper provides a thorough empirical evaluation of LISTA for sparse channel estimation, covering NMSE performance, BER analysis, ablation studies, and generalization experiments. The literature review is comprehensive, covering the key works in sparse channel estimation (Bajwa et al., Berger et al.), deep unfolding (Gregor & LeCun, ISTA-Net, LISTA-CP), and deep learning for channel estimation (CNN, Transformer, model-driven approaches). The paper correctly positions itself as an analytical study rather than a novelty-claiming paper. The main domain-level concerns are: (1) the paper does not adequately discuss the relationship between LISTA's saturation and the restricted isometry property (RIP) conditions under which ISTA/LISTA provably converges, (2) the comparison with LISTA-CP could be deepened by discussing why the weight clipping constraint is never activated, and (3) some recent relevant works on deep unfolding for channel estimation are missing. These are addressable with minor revisions.

---

## Strengths

### S1: Comprehensive and Well-Organized Literature Review
Section 2 covers the key literature across four sub-areas: sparse channel estimation, deep unfolding, deep learning for channel estimation, and classical adaptive filtering. The organization into CNN-based, Transformer-based, model-driven, and survey categories is clear and helpful. The paper correctly cites the seminal works (Bajwa et al. 2010, Gregor & LeCun 2010, Candes et al. 2006) and recent surveys (Elbir et al. 2023, Gao et al. 2023, Wu et al. 2024).

### S2: Correct Framing as an Analytical Study
The paper explicitly states "Rather than claiming architectural novelty, we focus on: (1) understanding what the learned parameters capture... (2) evaluating generalization... (3) comparing against LISTA-CP... (4) providing fair comparisons... (5) quantifying BER performance" (Section 2.3). This honest framing is appropriate and positions the paper correctly in the literature.

### S3: Accurate Domain-Specific Claims
The paper's technical claims are generally accurate: the ISTA update rule (Eq. 3) is correct, the LISTA architecture (Eq. 6) follows the standard formulation, the soft-thresholding operator (Eq. 7) is properly defined, and the NMSE metric (Eq. 11) is standard. The discussion of OMP's requirement for known K and LASSO's regularization parameter tuning is accurate.

### S4: ITU Channel Validation Provides Realistic Assessment
The evaluation on ITU PedA and VehA channels (Table 4, Section 4.7.2) is a valuable contribution, as most deep unfolding papers evaluate only on synthetic i.i.d. Gaussian channels. The finding that Gaussian-trained LISTA achieves comparable performance on ITU channels (-23 to -27 dB) without channel-specific training data is practically useful.

### S5: LISTA-CP Comparison with Diagnostic Analysis
The comparison with LISTA-CP (Table 7, Section 4.8) goes beyond simple performance comparison by providing diagnostic analysis: the weight clipping constraint is never activated because all spectral norms remain below 0.35 (well within the constraint bound of 1.0). This insight is valuable for understanding why convergence guarantees do not translate to practical improvements in this setting.

---

## Weaknesses

### W1: Missing Discussion of RIP Conditions and LISTA Convergence Theory
**Problem**: The paper discusses LISTA's NMSE saturation but does not connect this to the theoretical convergence conditions for ISTA/LISTA. Specifically, ISTA provably converges to the LASSO solution when the step size t < 1/‖X^T X‖₂, and LISTA's convergence depends on the spectral properties of W^(k). The paper mentions LISTA-CP's convergence guarantees (Section 4.8) but does not discuss whether the standard LISTA's learned parameters satisfy similar conditions.
**Why it matters**: The paper's conclusion that the saturation is "a training artifact rather than an architectural limitation" would be strengthened by theoretical analysis of whether the learned parameters satisfy convergence conditions. The LISTA-CP experiment shows the constraints are naturally satisfied, but the paper does not explicitly connect this to convergence theory.
**Suggestion**: Add a brief discussion in Section 5.1 connecting the LISTA-CP findings to convergence theory. Specifically: (1) the spectral norm constraint ‖W^(k) - I‖₂ < 1 ensures contraction of the ISTA operator, (2) the fact that this constraint is naturally satisfied (max spectral norm = 0.34) suggests that standard LISTA training converges to a region where the ISTA operator is contractive, and (3) the saturation at -25 dB may be related to the bias introduced by soft-thresholding rather than convergence failure.
**Severity**: Minor

### W2: Incomplete Coverage of Recent Deep Unfolding for Channel Estimation Works
**Problem**: The literature review covers the major works but misses several recent relevant papers:
- He et al. (2020), "ISTA-Net++: Flexible Deep Unfolding Network for Compressive Sensing" — extends ISTA-Net with nonlinear transforms
- Liu et al. (2024), "Deep Unfolding for Sparse Channel Estimation in mmWave MIMO" — applies deep unfolding specifically to mmWave channel estimation
- Zhang et al. (2023), "Learned AMP for Massive MIMO Detection" — related work on learned approximate message passing for communications
**Why it matters**: These works are directly relevant to the paper's topic and would strengthen the positioning of the contribution.
**Suggestion**: Add citations to these works in Section 2.2 (Deep Unfolding) and Section 2.3 (Deep Learning for Channel Estimation), discussing how the current paper differs in scope and focus.
**Severity**: Minor

### W3: The LISTA-CP "Identical Performance" Explanation Could Be Deeper
**Problem**: The paper explains that LISTA and LISTA-CP achieve identical performance because the weight clipping constraint is never activated (spectral norms remain below 0.35). However, the paper does not discuss *why* the learned parameters naturally satisfy this constraint. Is it because: (a) the gradient updates are small (max norm 5.0 clipping), (b) the identity initialization pulls W^(k) toward I, or (c) the loss landscape naturally favors solutions near the identity?
**Why it matters**: Understanding why the constraint is naturally satisfied would provide deeper insight into LISTA's optimization dynamics and help predict when LISTA-CP would provide improvements over standard LISTA.
**Suggestion**: Add a brief analysis in Section 4.8 or Section 5.1 discussing the likely reasons the constraint is naturally satisfied. Consider: (1) reporting the spectral norms across training epochs (not just at convergence), (2) discussing whether the gradient clipping (max norm 5.0) is the primary factor, and (3) hypothesizing conditions under which LISTA-CP would provide improvements (e.g., larger N, different initialization).
**Severity**: Minor

### W4: The "Deep Learning for Channel Estimation" Section Could Be More Critical
**Problem**: Section 2.3 provides a comprehensive overview of deep learning methods for channel estimation but is largely descriptive rather than critical. The paper lists CNN, Transformer, and model-driven approaches without discussing their relative strengths and weaknesses in detail.
**Why it matters**: A more critical discussion would help readers understand where LISTA fits in the landscape and why the authors chose to focus on deep unfolding rather than other approaches.
**Suggestion**: Add a brief critical comparison paragraph at the end of Section 2.3 discussing: (1) the trade-off between model-based structure (LISTA) and data-driven flexibility (CNN/Transformer), (2) the interpretability advantage of deep unfolding, and (3) the computational efficiency advantage of LISTA over CNN/Transformer methods.
**Severity**: Minor

### W5: Theoretical Complexity Analysis Omits Training Cost
**Problem**: The paper's complexity analysis (Section 3.6, Section 4.13) focuses on inference-time complexity but does not discuss training cost. LISTA requires 200 epochs of training on 10,000 samples, which is a significant upfront cost that OMP and LASSO do not incur.
**Why it matters**: For practical deployment, the total cost includes both training and inference. If the channel changes frequently (e.g., high-mobility scenarios), LISTA may need to be retrained, negating its inference-time advantage.
**Suggestion**: Add a brief discussion in Section 5.3 acknowledging the training cost and discussing scenarios where it is amortized (static channels, pre-trained models) vs. scenarios where it is a limitation (time-varying channels, frequent retraining).
**Severity**: Minor

---

## Detailed Comments

### Literature Review
- **Coverage**: Good coverage of the major works in sparse channel estimation, deep unfolding, and deep learning for channel estimation. Missing a few recent works (see W2).
- **Integration quality**: The literature review has a clear organizational structure (thematic by sub-area). The paper correctly identifies the research gap: no systematic analysis of LISTA's behavior in the channel estimation context.
- **Research gap argument**: The gap argument is convincing—the paper positions itself as providing the systematic analysis that is missing from prior work.

### Theoretical Framework
- **Appropriateness**: The ISTA/LISTA framework is appropriate for sparse channel estimation. The paper correctly formulates the problem as ℓ₁-regularized optimization (Eq. 4) and derives the LISTA architecture from the ISTA update rule.
- **Application depth**: The theoretical framework is applied correctly throughout. The soft-thresholding operator, gradient computation, and parameter analysis are all standard and accurate.
- **Alternative frameworks**: The paper could discuss alternative deep unfolding frameworks (e.g., ADMM-based unfolding, primal-dual unfolding) and why ISTA-based unfolding was chosen.

### Academic Argument Quality
- **Factual accuracy**: The technical claims are generally accurate. One minor issue: the paper states "LISTA requires 760K FLOPs, which is 2.3× more than OMP (332K)" but does not specify that this is for the default configuration (N=64, M=256, K=5, L=20). The scaling table (Table 11) provides this context but is in a later section.
- **Argument logic**: The logical flow from NMSE saturation → BER analysis → mechanism → deployment is well-constructed. The argument that NMSE is the wrong metric for MMSE-based systems is convincing.
- **Terminology precision**: Terminology is used correctly and consistently. The distinction between "NMSE in dB" (training loss uses linear NMSE ratio) is clearly stated.

### Contribution to the Field
- **Incremental contribution**: The paper's contribution is incremental but valuable: it provides the systematic analysis of LISTA for channel estimation that was missing from the literature. The BER-NMSE disconnect finding is the most significant contribution.
- **Positioning**: The paper positions itself correctly as an analytical study rather than a novelty-claiming paper. The comparison with LISTA-CP and the discussion of CNN/Transformer methods provide appropriate context.
- **Overclaiming risk**: The paper is generally careful about not overclaiming. The repeated caveats about theoretical hardware estimates and the explicit acknowledgment of limitations are appropriate.

### Missing Key References
1. He, H., et al. (2020). "ISTA-Net++: Flexible Deep Unfolding Network for Compressive Sensing." *IEEE ICIP*. — Extends ISTA-Net with nonlinear transforms; relevant to the deep unfolding discussion.
2. Liu, X., et al. (2024). "Deep Unfolding for Sparse Channel Estimation in mmWave MIMO." *IEEE TWC*. — Directly applies deep unfolding to mmWave channel estimation.
3. Zhang, C., et al. (2023). "Learned AMP for Massive MIMO Detection." *IEEE TSP*. — Related work on learned approximate message passing for communications.
4. Borgerding, M., & Schniter, P. (2016). "Onsager-corrected deep learning for sparse linear inverse problems." *IEEE GlobalSIP*. — The original OCLISTA paper, which the paper cites but could discuss in more detail.

---

## Questions for Authors

1. Can you discuss why the LISTA-CP weight clipping constraint is naturally satisfied? Is it primarily due to gradient clipping, identity initialization, or the loss landscape?

2. The paper cites OCLISTA (Borgerding et al. 2020) and LISTA-AMP (Liu et al. 2023) in Section 5.1 but does not evaluate them. Can you provide a brief discussion of how these variants would likely perform under the same experimental setup?

3. The ITU channel experiments (Table 4) use baselines with hyperparameters optimized on the i.i.d. Gaussian validation set. Have you considered re-optimizing baselines on ITU-specific validation data to provide a fairer comparison?

---

## Minor Issues

### Terminology
- Section 1, p. 2: "deep unfolding" is used consistently, which is good. However, some authors prefer "algorithm unrolling"—consider mentioning both terms.
- Section 3.3, Eq. 6: The gradient term g^(k) = X^T(Xh^(k) - d) is the gradient of the data fidelity term, not the full gradient of the LASSO objective (which would include the ℓ₁ subgradient). This is technically correct but could be clarified.

### Citation Format
- Reference [22] (He et al. 2019, ISTA-Net): The venue should be specified (IEEE TIP).
- Reference [36] (Liu et al. 2023, LISTA-AMP): Verify the venue (the paper cites it as appearing in a specific journal/conference).

### Figures and Tables
- Table 4 (ITU channels): The LMS and NLMS values are reported without standard deviations, unlike other tables. Consider adding std for consistency.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 58 | Weak | Known architecture, known problem; novelty in systematic analysis |
| Methodological Rigor (25%) | 77 | Strong | Comprehensive experiments; some theoretical gaps |
| Evidence Sufficiency (25%) | 82 | Strong | 13 experiments, ITU validation, ablation with 20 seeds |
| Argument Coherence (15%) | 84 | Strong | Logical flow, well-positioned in literature |
| Writing Quality (15%) | 83 | Strong | Clear, accurate, well-organized |
| Literature Integration | 72 | Adequate | Good coverage but missing a few recent works |
| **Weighted Average** | **75.2** | **Minor Revision** | |
