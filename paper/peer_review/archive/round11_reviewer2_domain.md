# Domain Review Report (Peer Reviewer 2)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 11

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain)

### Reviewer Identity
Prof. Akiko Tanaka, Professor of Communications Engineering, specializing in channel estimation, OFDM systems, and compressed sensing for wireless communications.

### Review Focus
Literature coverage, theoretical framework, domain-specific accuracy, and contribution to the sparse channel estimation field.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
**5** — Completely within my area of expertise.

### Summary Assessment

This paper provides a thorough analysis of LISTA for sparse channel estimation, covering a wide range of experimental conditions. The literature review is comprehensive, covering compressed sensing, deep unfolding, CNN/Transformer-based channel estimation, and classical adaptive filtering. The positioning within the field is clear — the paper claims no architectural novelty and focuses on systematic analysis.

The domain contribution is solid: (1) the error concentration mechanism (99.9% on true taps) is a new finding that explains the BER–NMSE disconnect; (2) the ablation study with statistical significance testing quantifies what LISTA learns; (3) the cross-distribution generalization to ITU channels is practically relevant. The paper correctly identifies LISTA's limitations (NMSE saturation, OMP gap) and provides mitigation strategies (SNR-specific training).

However, the literature review could be strengthened in two areas: (1) the comparison with recent LISTA variants (OCLISTA, LISTA-AMP) is only qualitative; (2) the discussion of structured linear mappings for scaling to larger N is brief. These are minor issues.

---

## Strengths

### S1: Comprehensive Literature Coverage
The related work section (Section 2) covers four major areas: sparse channel estimation, deep unfolding, deep learning for channel estimation, and classical adaptive filtering. Key references are well-cited: Gregor & LeCun (2010) for LISTA, Chen et al. (2018) for LISTA-CP, Bajwa et al. (2010) for compressed sensing channel estimation. Recent surveys (Elbir 2023, Gao 2023, Wu 2024) are included.

### S2: Clear Positioning in the Field
The paper explicitly states: "Rather than claiming architectural novelty, we focus on: (1) understanding what the learned parameters capture, (2) evaluating generalization, (3) comparing against LISTA-CP, (4) providing fair comparisons, and (5) quantifying BER performance" (Section 2.3). This honest positioning is appropriate and avoids overclaiming.

### S3: Error Concentration Mechanism is Novel
The finding that LISTA concentrates 99.9% of estimation error on true taps (Section 4.12) is, to my knowledge, a new result in the sparse channel estimation literature. The generalization to ITU channels (99.3–99.5%) and the 50× advantage over OMP on non-support taps provide genuine domain insight.

### S4: Practical ITU Channel Evaluation
The evaluation on ITU PedA and VehA channel models (Section 4.7) with baselines optimized on Gaussian data (no re-optimization for ITU) is a fair and practically relevant test. The finding that LISTA achieves −23 to −27 dB on ITU channels is valuable for deployment decisions.

---

## Weaknesses

### W1: Incomplete Comparison with Recent LISTA Variants
**Problem**: The paper compares against LISTA-CP (Section 4.8) but only qualitatively discusses OCLISTA and LISTA-AMP (Section 5.1). The claim that "these variants would exhibit similar saturation under broad-range mixed-SNR training" (Section 5.1) is a hypothesis, not a finding.
**Why it matters**: The deep unfolding field has evolved significantly since LISTA-CP. OCLISTA and LISTA-AMP have demonstrated improved convergence properties, and readers would benefit from quantitative comparison.
**Suggestion**: Either (a) include a brief experimental comparison with OCLISTA or LISTA-AMP (even at a single SNR point), or (b) clearly state that this comparison is future work and explain why it was not included.
**Severity**: Major

### W2: Structured Linear Mappings Discussion is Brief
**Problem**: The paper identifies the O(N²) scaling of W^(k) as a scalability limitation (Section 4.13, Table 13) and mentions "structured linear mappings (Toeplitz, circulant, low-rank)" as potential solutions (Section 4.13), but does not explore this direction.
**Why it matters**: For the DSP readership, scaling to N = 256–1024 is practically important. The brief mention of structured mappings is insufficient.
**Suggestion**: Add a paragraph in Section 5.4 (Future Work) discussing which structured mappings would be most appropriate for channel estimation and why. Reference relevant work on structured LISTA variants.
**Severity**: Minor

### W3: Missing Reference to Key Deep Unfolding Work
**Problem**: The paper cites Monga et al. (2021) for deep unfolding but does not cite the earlier comprehensive survey by Hershey et al. (2014, "Deep unfolding") or the more recent work by Balatsoukas-Stimming & Studer (2019) on deep unfolding for MIMO detection.
**Why it matters**: These are seminal works in the deep unfolding literature that readers would expect to see.
**Suggestion**: Add citations to Hershey et al. (2014) and Balatsoukas-Stimming & Studer (2019) in Section 2.2.
**Severity**: Minor

### W4: NMSE vs. BER Disconnect Explanation Could Be Deeper
**Problem**: The paper explains the BER–NMSE disconnect through error concentration (Section 4.12), but the theoretical connection between error location and equalizer noise enhancement could be more formally developed. The noise enhancement analysis (Table 12) is empirical, not analytical.
**Why it matters**: A formal derivation showing how non-support errors affect ZF equalization would strengthen the mechanism analysis.
**Suggestion**: Consider adding a brief analytical derivation in Section 4.12 or an appendix showing how the ZF noise enhancement factor depends on the error support.
**Severity**: Minor

---

## Detailed Comments

### Literature Review
- **Coverage**: Comprehensive. Key works in compressed sensing (Candès 2006, Donoho 2006), greedy algorithms (Tropp 2007), LASSO (Tibshirani 1996), ISTA (Daubechies 2004, Beck 2009), and LISTA (Gregor 2010) are all cited. Recent deep learning methods (CNN, Transformer) and surveys are covered.
- **Integration quality**: The literature review is organized thematically and provides critical synthesis rather than mere enumeration. The positioning of the paper within the deep unfolding literature is clear.
- **Research gap argument**: The gap is well-identified: "Rather than claiming architectural novelty, we focus on understanding what the learned parameters capture." This is a valid and well-argued gap.

### Theoretical Framework
- **Appropriateness**: The ISTA/soft-thresholding framework is the correct theoretical foundation for LISTA. The connection to compressed sensing theory is well-established.
- **Application depth**: The paper applies the framework correctly, with appropriate initialization and training procedures.
- **Alternative frameworks**: The paper could discuss the connection to approximate message passing (AMP) theory, which provides a different theoretical lens for understanding LISTA's behavior.

### Academic Argument Quality
- **Factual accuracy**: Technical claims are accurate. The NMSE calculations, BER simulations, and FLOP counts appear correct.
- **Argument logic**: The logical flow from NMSE saturation → BER analysis → mechanism analysis → practical deployment is sound.
- **Terminology precision**: Terminology is used correctly and consistently. The distinction between "scale-invariant loss" and "noise-floor saturation" is well-articulated.

### Contribution to the Field
- **Incremental contribution**: The paper's contribution is analytical rather than architectural. The error concentration mechanism, ablation with statistical rigor, and practical deployment guidance are valuable additions to the field.
- **Positioning**: The paper positions itself clearly as a systematic analysis paper, not a method paper. This is appropriate.
- **Overclaiming**: The authors generally avoid overclaiming, with appropriate caveats on hardware and NMSE gap claims.

### Missing Key References
1. Hershey, J. R., Roux, J. L., & Weninger, F. (2014). Deep unfolding: Model-based inspiration of novel deep architectures. *arXiv:1409.2574*. — Seminal deep unfolding survey.
2. Balatsoukas-Stimming, A., & Studer, C. (2019). Deep unfolding for communications systems: A survey and some new directions. *IEEE Int. Workshop on Signal Processing Systems*. — Recent deep unfolding survey for communications.
3. Liu, Y., et al. (2023). LISTA-AMP: Bridging deep unfolding and approximate message passing. — The paper cites this but could discuss its relationship to the current findings more explicitly.

---

## Questions for Authors

1. The error concentration mechanism (99.9% on true taps) is fascinating. Have you investigated whether this is a consequence of the soft-thresholding operator specifically, or whether other sparsity-promoting activations would produce similar concentration? This would help determine if the mechanism is architectural or operator-specific.
2. The paper reports that LISTA training diverges at N = 256 (Table 3). Is this a fundamental limitation of the O(N²) architecture, or could it be addressed with better training techniques (e.g., gradient normalization, learning rate scheduling)?
3. For the ITU channel experiments, the baselines use hyperparameters optimized on Gaussian data. Have you also tested with hyperparameters optimized on ITU data? This would help determine how much of LISTA's ITU performance is due to generalization vs. the baselines being suboptimal.

---

## Minor Issues

### Terminology
- Section 2.2: "Deep unfolding" should be consistently hyphenated ("deep-unfolded" in some places, "deep unfolding" in others).
- Section 4.12: "Gini coefficient" is correctly used but should be briefly defined for readers unfamiliar with the metric.

### Citation Format
- Some citations use "et al." while others list all authors. Please ensure consistency with the journal's citation style.
- The citation to Liu et al. (2023) on LISTA-AMP should include the journal/conference name.
