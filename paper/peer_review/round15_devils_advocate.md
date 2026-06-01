# Devil's Advocate Review

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 15

---

## Reviewer Information

### Reviewer Role
Devil's Advocate Reviewer

### Reviewer Identity
The Devil's Advocate does not have a fixed identity. My role is to stress-test the paper's core arguments, find the strongest counter-arguments, and identify vulnerabilities that other reviewers may miss.

### Review Focus
Core argument challenges, logical fallacy detection, cherry-picking detection, confirmation bias detection, and the strongest possible case against the paper's conclusions.

---

## Strongest Counter-Argument

The paper's central thesis is that LISTA's "error concentration mechanism" — concentrating 100.0% of estimation error on true tap locations — is a meaningful contribution that justifies LISTA's existence despite its 13--33 dB NMSE deficit relative to OMP and 1--27 dB deficit relative to FISTA. This thesis has three critical vulnerabilities.

**First, the error concentration is a trivial consequence of soft-thresholding, not a discovery.** The soft-thresholding operator $\mathcal{S}_\theta(\mathbf{z}) = \text{sign}(\mathbf{z}) \odot \text{ReLU}(|\mathbf{z}| - \theta)$ sets all components below the threshold to zero. By construction, the output is sparse, and the residual error is concentrated on the locations where the output is non-zero — which are, by design, the locations with the largest input magnitudes. On sparse channels, these locations coincide with the true taps. The ISTA control experiment confirms this: ISTA achieves 92.4% concentration without any learned parameters. The paper's "mechanism analysis" is therefore rediscovering a known property of proximal operators and presenting it as a new finding. The 7.6 percentage-point improvement from LISTA's learned parameters (92.4% to 100.0%) is real but marginal, and the paper's claim that this constitutes a "primary contribution" is overstated.

**Second, the BER advantage is an artifact of the equalizer choice, not a property of LISTA.** The paper shows that under MMSE equalization (the standard in modern receivers), all estimators achieve similar BER at SNR ≥ 5 dB. The ZF advantage only manifests for 16-QAM at SNR ≥ 15 dB. But ZF equalization is rarely used in practice precisely because it amplifies noise — the paper itself acknowledges this (Section 5.1: "ZF is included to reveal LISTA's error structure properties, which are masked under MMSE"). Using a deliberately inferior equalizer to reveal a property of the channel estimator is a valid diagnostic technique, but presenting it as a "BER advantage" is misleading. A practitioner reading the highlights box would conclude that LISTA has BER advantages, when in fact the advantage only exists under conditions (ZF + 16-QAM + high SNR) that are rarely encountered in practice.

**Third, the paper's own results argue against using LISTA.** The paper shows: (1) LISTA trails OMP by 13--33 dB in NMSE; (2) LISTA trails FISTA by 1--27 dB in NMSE; (3) FISTA requires no training data; (4) LISTA requires 2.3x more FLOPs than OMP; (5) the hardware pipelining advantage is "an unvalidated hypothesis"; (6) the error concentration advantage only matters under ZF equalization. The honest conclusion from these facts is: **do not use LISTA for sparse channel estimation**. Use FISTA if you want fast convergence, OMP if you know the sparsity level, or LASSO if you want robustness. The paper's attempt to find a silver lining (error concentration) does not change this conclusion.

---

## Issue List

#### CRITICAL

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| C1 | Core Thesis | The paper's central contribution (error concentration) is a trivial consequence of soft-thresholding, not a new discovery. The ISTA control (92.4%) confirms this is generic to proximal operators. The 7.6 pp improvement from learned parameters is marginal and does not constitute a "primary contribution." | Abstract, Section 4.12 |
| C2 | Data-Conclusion Mismatch | The paper presents the ZF/16-QAM BER advantage as a major finding, but this only exists under conditions (ZF equalization) that the paper itself acknowledges are rarely used in practice. The highlights box overstates the practical significance. | Highlights box, Section 4.10 |

#### MAJOR

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| M1 | Strongest Counter-Narrative | The paper's own results provide a stronger argument for not using LISTA than for using it. FISTA outperforms LISTA at all SNR levels, requires no training, and has lower computational cost. The paper should acknowledge this more prominently. | Tables 1, 13; Section 4.12 |
| M2 | Cherry-Picking | The highlights box selects favorable findings (error concentration, SNR mitigation) while de-emphasizing unfavorable ones (13--33 dB NMSE gap, FISTA superiority). This creates an unbalanced impression. | Highlights box |
| M3 | Overgeneralization | The error concentration analysis uses only $N=64$, $K=5$, $M=256$, real-valued channels, and BPSK pilots. Generalizing to complex-valued channels, larger $N$, or different modulations is not supported by the data. | Section 4.12 |
| M4 | Logic Chain Break | The paper argues that error concentration "explains" the BER behavior, but the causal chain is: soft-thresholding → sparse output → error on support → lower noise enhancement under ZF → better BER for 16-QAM. Each link is plausible but the paper does not formally prove the causal chain (e.g., by showing that a synthetic estimator with the same error concentration but different error distribution achieves the same BER). | Section 4.12.5 |

#### MINOR

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| m1 | Confirmation Bias | The paper frames LISTA's saturation at -25 dB as a "training artifact" rather than a limitation. While SNR-specific training improves to -31 dB, this still trails OMP by 6 dB. The "training artifact" framing suggests the problem is fixable, when it may be fundamental. | Section 5.1 |
| m2 | Missing Alternative | The paper does not consider whether a simple post-processing step (e.g., hard thresholding OMP's output to enforce sparsity) could achieve the same error concentration as LISTA without the training overhead. | Section 4.12 |
| m3 | Overclaim on AMP | The AMP connection (Section 5.1) is presented as a theoretical contribution but is speculative. The Onsager correction connection has been made by Liu et al. (2023) and Borgerding et al. (2020). | Section 5.1 |

---

## Ignored Alternative Explanations/Paths

1. **Hard-thresholded OMP**: OMP could be post-processed to enforce sparsity in the estimate (setting all non-selected taps to zero), which would achieve 100% error concentration by construction. This would be simpler than LISTA and achieve the same BER advantage under ZF equalization. The paper does not consider this alternative.

2. **FISTA with learned threshold**: Instead of full LISTA training, one could simply learn the optimal threshold for FISTA (a single scalar parameter) while keeping the Nesterov momentum fixed. This would capture most of LISTA's benefit (the per-layer threshold is the dominant ablation component) with far less complexity.

3. **Direct BER optimization**: Instead of training with NMSE loss and hoping for BER benefits, one could train directly with a BER-aware loss function. This would likely achieve better BER performance than LISTA's indirect approach.

4. **Ensemble of OMP with different sparsity levels**: Running OMP with $K \in \{3, 5, 7\}$ and selecting the best estimate (by cross-validation) might achieve better NMSE than LISTA without any training.

---

## Missing Stakeholder Perspectives

- **Hardware designers**: The paper discusses theoretical FLOP counts but does not engage with the hardware design community's concerns (memory bandwidth, power consumption, area constraints). The pipelining hypothesis needs validation from this community.
- **Standards bodies**: 3GPP channel estimation standards (e.g., for NR) use specific pilot structures and channel models. The paper's BPSK pilot assumption does not match these standards.
- **Practical system designers**: The paper assumes perfect knowledge of the pilot signal $\mathbf{x}$ at the receiver. In practice, pilot overhead is a critical resource, and the paper's $M/N = 4$ ratio is generous by modern standards.

---

## Observations (Non-Defects)

- The paper's honesty about LISTA's limitations is commendable and rare. Most papers on deep learning for communications overstate their contributions.
- The ISTA control experiment is well-designed and provides genuine insight into the role of learned parameters.
- The 20-seed ablation with Holm--Bonferroni correction is exemplary statistical practice.
- The FISTA comparison is a valuable addition that honestly positions LISTA's value.

---

## Dimension Scores

The Devil's Advocate does not score the paper. My role is to challenge, not to evaluate. The scoring is the other reviewers' responsibility.

---

## Editorial Impact Assessment

If the CRITICAL issues (C1, C2) are not addressed, the paper's core contribution is undermined. The paper would need to either: (a) demonstrate that the error concentration improvement (92.4% to 100.0%) has practical consequences beyond the narrow ZF/16-QAM scenario, or (b) reframe the contribution as "quantifying the properties of soft-thresholding in the channel estimation context" rather than "discovering a new mechanism."
