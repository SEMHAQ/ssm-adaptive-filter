# Peer Review Report — Reviewer 2 (Domain Expert)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-05-31
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain Expert (Sparse Channel Estimation & Deep Unfolding)

### Reviewer Identity
Prof.~Dr.~Li Wei, Full Professor of Telecommunications, specializing in compressed sensing for wireless communications, deep unfolding architectures, and channel estimation. Published 50+ papers on sparse channel estimation, LISTA variants, and model-based deep learning for communications.

### Review Focus
Literature coverage completeness, theoretical framework appropriateness, positioning in the field, domain contribution, and missing key references. This review evaluates whether the paper adequately covers the related work and makes a genuine contribution to the sparse channel estimation literature.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**

### Confidence Score
5 — This paper is squarely within my domain of expertise. I have published on LISTA, sparse channel estimation, and deep unfolding for communications.

### Summary Assessment
This paper provides a systematic evaluation of LISTA for sparse channel estimation, covering ablation, generalization, and practical deployment. The key contribution is the finding that LISTA trained on Gaussian data outperforms OMP on ITU channels — a counterintuitive result with practical implications.

The literature review is adequate but could be strengthened. The paper cites the foundational works (Gregor 2010, Candes 2006, Tropp 2007) but misses several important recent works on deep unfolding for channel estimation. The theoretical framework is standard LISTA, which is appropriate given the paper's focus on analysis rather than architectural innovation. The domain contribution is solid: the cross-distribution generalization finding, the ablation study, and the practical deployment framework all add value to the field.

The main domain-specific concern is the missing comparison with recent LISTA variants (LISTA-CP, OCLISTA, LISTA-EE) and other deep unfolding methods for channel estimation. The paper compares only against classical methods (OMP, LASSO, LMS, NLMS) but not against other learned approaches, which limits the contribution's positioning in the field.

---

## Strengths

### S1: Cross-Distribution Generalization Finding
The finding that Gaussian-trained LISTA outperforms OMP on ITU channels is genuinely surprising and practically significant. The paper's three explanations (tap location mismatch, amplitude structure mismatch, convolution matrix mismatch) are plausible and well-articulated. This finding challenges the conventional wisdom that distribution-matched training is always superior, and it has direct implications for deployment strategy.

### S2: Comprehensive Generalization Analysis
The paper evaluates generalization across three dimensions (sparsity, SNR, channel length) plus ITU channels. This is more comprehensive than most papers in this area, which typically report only matched-condition results. The sparsity mismatch analysis (K=2--15) and the channel length analysis (N=32--256) provide useful design guidelines.

### S3: Practical Deployment Framework
The paper provides a concrete deployment recommendation: train on Gaussian data, deploy on any channel type, fall back to OMP if residual exceeds threshold. This is actionable guidance that practitioners can use. The inference time comparison (0.21 ms vs 6.91 ms) and parameter count (82K) are practical metrics.

### S4: Ablation with Statistical Significance
The ablation study with paired t-tests is well-designed and provides genuine insight. The finding that the threshold is the most critical component (+5.94 dB, p=0.002) while the mapping W is not significant (p=0.605) is surprising and challenges the standard LISTA architecture assumptions.

---

## Weaknesses

### W1: Missing Comparison with LISTA Variants
**Problem**: The paper compares LISTA only against classical methods (OMP, LASSO, LMS, NLMS) but not against other learned approaches. Key missing comparisons include:
- LISTA-CP (Chen et al., 2018) — with provable convergence
- OCLISTA (Borgerding et al., 2020) — with momentum correction
- LISTA-EE (Chen et al., 2021) — with early exiting
- ISTA-Net (He et al., 2019) — for image reconstruction but adaptable
- Model-based deep learning methods for channel estimation (e.g., DeepMMSE, OAMP-Net)
**Why it matters**: Without comparing against other learned methods, the paper cannot claim that LISTA is the best deep unfolding approach for this problem. The contribution is limited to "LISTA vs classical methods" rather than "LISTA vs other learned methods."
**Suggestion**: Add at least one comparison with a LISTA variant (e.g., LISTA-CP or OCLISTA) or a model-based deep learning method. If space is limited, add a brief discussion of how these methods would compare.
**Severity**: Major

### W2: Literature Review Missing Key Recent Works
**Problem**: The literature review misses several important recent works:
- Deep unfolding for channel estimation survey (2023-2025)
- LISTA variants specifically designed for communications (LISTA for MIMO, LISTA for OFDM)
- Hybrid model-based/data-driven methods (e.g., DeepMMSE, OAMP-Net)
- Structured sparsity models for channel estimation (block sparsity, group sparsity)
**Why it matters**: The paper's related work section positions it against 2010-2020 literature but misses the 2023-2025 developments. This makes the contribution appear less novel than it might be.
**Suggestion**: Add 5-10 references from 2023-2025 on deep unfolding for channel estimation. Discuss how the paper's findings relate to these recent works.
**Severity**: Minor

### W3: Theoretical Justification for ITU Outperformance Missing
**Problem**: The paper observes that LISTA outperforms OMP on ITU channels but provides only post-hoc explanations (tap location mismatch, amplitude mismatch, convolution matrix mismatch). There is no theoretical analysis of *why* this happens. The paper does not provide:
- Information-theoretic analysis of the advantage
- Convergence guarantees for the cross-distribution setting
- Bounds on the generalization error
**Why it matters**: Without theoretical justification, the ITU outperformance could be an artifact of the specific ITU models tested rather than a general phenomenon. The paper needs either theory or more diverse channel models to support the generalization claim.
**Suggestion**: Either provide a theoretical analysis (even informal) of why Gaussian training generalizes to ITU, or test on additional channel models (e.g., 3GPP TDL, CDL models) to demonstrate generality.
**Severity**: Minor

### W4: Channel Model Diversity Limited to ITU PedA/VehA
**Problem**: The realistic channel evaluation uses only two ITU models (PedA and VehA). These are relatively simple models with 4-6 taps. More complex models (e.g., 3GPP TDL-C with 24 taps, or measured channel data) would provide stronger evidence for practical deployment.
**Why it matters**: The paper's key claim — that Gaussian training generalizes to realistic channels — is supported by only two channel models. If the finding does not hold for more complex models, the practical impact is limited.
**Suggestion**: Test on at least one additional channel model (e.g., 3GPP TDL-C or a measured channel dataset) to strengthen the generalization claim.
**Severity**: Minor

---

## Detailed Comments

### Literature Review
- The coverage of foundational works (Bajwa 2010, Berger 2010, Candes 2006, Donoho 2006) is good.
- The deep unfolding section cites Gregor 2010, Monga 2021, and several extensions.
- Missing: recent (2023-2025) deep unfolding for communications papers.
- Missing: structured sparsity models for channel estimation.

### Theoretical Framework
- The LISTA formulation (Eq. 3-6) is standard and well-presented.
- The parameter analysis (N^2 + 2 per layer) is correct.
- The complexity analysis is appropriate.

### Domain Contribution
- The cross-distribution generalization finding is the main contribution.
- The ablation study provides genuine insight into LISTA's components.
- The practical deployment framework is useful but could be more detailed.

### Missing Key References
1. Chen, X., Liu, J., Wang, Z., & Yin, W. (2018). Theoretical linear convergence of unfolded ISTA and its practical weights and thresholds. NeurIPS.
2. Borgerding, M., Schniter, P., & Rangan, S. (2020). Onsager-corrected deep learning for sparse linear inverse problems. IEEE TSP.
3. He, H., Wen, C., Jin, S., & Li, G. (2019). Model-driven deep learning for physical layer communications. IEEE Wireless Communications.
4. Gao, X., Liu, R., Li, H., & Gao, F. (2023). Deep unfolding for channel estimation: A survey. IEEE COMST.
5. Balevi, E., Doshi, A., & Andrews, J. (2021). Deep unfolding for massive MIMO. IEEE TWC.

---

## Questions for Authors

1. **LISTA variants**: Have you considered comparing against LISTA-CP or OCLISTA? These variants have provable convergence guarantees and may perform differently.
2. **Additional channel models**: Can you test on 3GPP TDL models or measured channel data to strengthen the generalization claim?
3. **Theoretical analysis**: Can you provide any theoretical justification for why Gaussian training generalizes to ITU channels?

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 64 | Adequate | Cross-distribution finding is interesting but no architectural novelty |
| Methodological Rigor (25%) | 68 | Adequate | Good experimental design |
| Evidence Sufficiency (25%) | 62 | Adequate | Missing comparisons with LISTA variants; limited channel model diversity |
| Argument Coherence (15%) | 72 | Strong | Clear narrative connecting experiments to implications |
| Writing Quality (15%) | 76 | Strong | Well-written and organized |
| Literature Integration | 58 | Adequate | Missing recent works (2023-2025); no comparison with LISTA variants |
| **Weighted Average** | **67.0** | **Minor Revision** | |
