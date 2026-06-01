# Devil's Advocate Review

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 5

---

## Reviewer Information

### Reviewer Role
Devil's Advocate — Stress-Test Reviewer

### Reviewer Identity
The Devil's Advocate does not have a fixed identity. I exist to challenge the paper's core arguments, find logical gaps, and construct the strongest possible counter-arguments. I am the "stress test" before submission.

---

## Overall Assessment

### Recommendation
- [ ] **Accept**
- [ ] **Minor Revision**
- [x] **Major Revision**
- [ ] **Reject**

### Confidence Score
4 — High confidence in identifying logical vulnerabilities. My role is adversarial, not evaluative.

### Summary Assessment

This paper presents LISTA as a "practical alternative for sparse channel estimation" based primarily on BER comparability with OMP. The BER-NMSE disconnect analysis is genuinely insightful. However, the paper's core argument has a critical vulnerability: the BER advantage is demonstrated primarily under ZF equalization and largely vanishes under MMSE (Table 11). Since MMSE is the standard equalizer in modern receivers, the paper's central practical claim is weaker than presented. Additionally, the LISTA-CP comparison (identical results) raises implementation integrity concerns that must be resolved. The paper is honest about its limitations, which is commendable, but the abstract and highlights present a more optimistic picture than the full results support.

---

### Strongest Counter-Argument

The paper's central thesis is that LISTA is a "practical alternative for sparse channel estimation" because it achieves "comparable BER" with OMP despite 13--33~dB worse NMSE. This argument has a fatal weakness: **the BER advantage is an artifact of ZF equalization, not a property of LISTA itself.**

Under ZF equalization, LISTA's error concentration on true taps (99.9\% vs.~94.9\% for OMP) reduces noise enhancement, producing better BER despite worse NMSE. But under MMSE equalization — which is the standard in every modern wireless receiver (4G LTE, 5G NR, Wi-Fi 6/7) — this advantage vanishes. Table 11 shows that at SNR=20 dB, all three methods (OMP, LASSO, LISTA) achieve identical BER (0.0003) under MMSE. The paper acknowledges this: "MMSE's regularization term $1/\text{SNR}$ suppresses the noise enhancement difference that drives LISTA's BER advantage under ZF."

This means the paper's central practical claim — "LISTA provides 4.4$\times$ hardware throughput advantage over OMP with comparable BER performance" — is only true for ZF-based systems. For MMSE-based systems (which is the vast majority of practical deployments), LISTA provides 4.4$\times$ hardware throughput but **no BER advantage**, and its BER is comparable to OMP only because MMSE equalizes away the differences. The paper's abstract and highlights do not make this distinction clear, presenting the BER advantage as a general finding rather than a ZF-specific artifact.

Furthermore, the paper's mechanism analysis — while insightful — actually undermines its own practical claim. The finding that LISTA concentrates error on true taps is a property of the soft-thresholding operator, which enforces sparsity in the estimate. But this same sparsity enforcement causes LISTA's NMSE to saturate at $-25$~dB: the soft-thresholding operator introduces a bias floor that prevents further NMSE improvement. Thus, LISTA's BER advantage (from error concentration) and NMSE disadvantage (from thresholding bias) are two sides of the same coin — you cannot have one without the other. The paper presents these as separate findings but they are mechanistically linked.

A practical engineer reading this paper would conclude: "LISTA gives me 4.4$\times$ throughput with no BER penalty under MMSE, but 13--33~dB worse NMSE. For my 5G NR system using MMSE equalization, I should use OMP because NMSE matters for channel sounding and link adaptation, and MMSE already handles the BER." The paper's recommendation framework (Section 5.2) partially acknowledges this, but the abstract and highlights do not.

---

### Issue List

#### CRITICAL
| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| C1 | Logic Chain | The BER advantage claim is ZF-specific but presented as general. Table 11 shows the advantage vanishes under MMSE at SNR=20 dB, yet the abstract claims "comparable BER" without qualifying the equalizer. The paper's central practical claim is weaker than presented. | Abstract, Highlights, Section 4.10 |
| C2 | Data-Conclusion Mismatch | LISTA-CP shows "maximum per-parameter difference = 0" with standard LISTA (Table 12). This is statistically implausible for independently trained models and suggests either an implementation issue or trivial comparison. The conclusion that "convergence guarantees provide no practical improvement" may be invalid if the comparison is flawed. | Section 4.8, Table 12 |

#### MAJOR
| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| M1 | Confirmation Bias | The paper emphasizes the ZF BER advantage in the abstract and highlights but buries the MMSE result (Table 11, only 2 SNR points) in the main text. This framing creates a more optimistic impression than the full results support. | Abstract, Highlights, Table 11 |
| M2 | Overgeneralization | The "cross-distribution generalization" claim is based on only 2 ITU channel models (PedA, VehA). Both have exponentially decaying profiles similar to the training distribution. This is "cross-model" generalization within a narrow class, not "cross-distribution" generalization. | Section 4.7.2, Abstract |
| M3 | Alternative Explanation | The NMSE saturation at $-25$~dB is attributed to "fixed-depth architecture and scale-invariant training loss" (Section 5.1). An alternative explanation is that the soft-thresholding operator's bias floor is the primary cause, and the fixed-depth architecture merely prevents iterative refinement beyond this floor. The paper does not disentangle these two factors. | Section 5.1 |
| M4 | Cherry-Picking | The paper reports LISTA's BER advantage for 16-QAM at SNR $\geq 15$ dB ($p < 0.05$) but does not emphasize that this advantage is smaller in absolute terms (e.g., 0.305 vs 0.316 at SNR=20 dB, a 3.5\% relative improvement). The statistical significance is driven by low variance (200 realizations), not large effect size. | Table 9 |
| M5 | Missing Stakeholder | The paper does not discuss the perspective of standards bodies (3GPP, IEEE) who define the channel estimation requirements for wireless systems. LISTA's applicability depends on whether it meets 3GPP NR channel estimation specifications, which the paper does not address. | Section 5 |

#### MINOR
| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| m1 | Overgeneralization | The abstract claims "LISTA provides 4.4$\times$ hardware throughput advantage" without the "theoretical estimate" qualifier. This is presented as a measured result. | Abstract |
| m2 | Logic Gap | The paper states "LISTA does not require explicit sparsity knowledge" (Section 3.6) but uses $K=5$ for training data generation. The training distribution implicitly encodes sparsity knowledge. | Section 3.6 |
| m3 | Imprecision | The $33\times$ Python speedup is prominently featured but the paper acknowledges it "reflects interpreter overhead rather than algorithmic complexity." This number should be de-emphasized. | Abstract, Table 6 |
| m4 | Missing Evidence | The paper claims "LISTA's soft-thresholding enforces sparsity in the estimate" (Section 4.12.3) but does not report the actual sparsity of LISTA's output (number of non-zero taps). Does LISTA output exactly $K=5$ non-zero taps, or more/less? | Section 4.12 |

---

### Ignored Alternative Explanations/Paths

1. **AMP-based methods**: Approximate Message Passing (AMP) and its variants (GAMP, VAMP) achieve near-oracle performance on i.i.d.~Gaussian sensing matrices with $O(MN)$ complexity. The paper does not compare against AMP, which may outperform both LISTA and OMP on the i.i.d.~Gaussian channels used in this study. AMP's Onsager correction term provides faster convergence than ISTA, and its denoiser can be learned (LDAMP), creating a direct competitor to LISTA.

2. **Learned OMP**: Rather than unfolding ISTA, one could learn the atom selection rule of OMP, creating a "Learned OMP" that retains OMP's greedy structure but with learned selection criteria. This would combine OMP's low per-iteration complexity with data-driven adaptation, potentially achieving better NMSE than LISTA with comparable BER.

3. **Hybrid LISTA/OMP**: The paper recommends LISTA for speed and OMP for accuracy (Section 5.2), but does not consider a hybrid approach: use LISTA for initial estimation and OMP for refinement. This could achieve LISTA's speed with OMP's accuracy.

4. **SNR-adaptive LISTA**: Rather than training separate models for different SNR ranges, one could add SNR as an input to the network (e.g., via conditional batch normalization), creating a single model that adapts to the operating SNR. This would eliminate the need for multiple SNR-specific models.

---

### Missing Stakeholder Perspectives

- **Standards bodies (3GPP, IEEE)**: Do not define channel estimation algorithms but specify performance requirements (e.g., BLER targets). LISTA's applicability depends on meeting these requirements, which the paper does not assess.
- **FPGA/ASIC designers**: The paper's hardware estimates assume ideal conditions. Real designers face memory bandwidth bottlenecks, clock domain crossing, and resource sharing constraints that the paper does not address.
- **System integrators**: Need to consider training data availability, model retraining frequency, and deployment complexity. The paper's SNR-specific training recommendation multiplies the deployment burden.

---

### Unexamined Premise

The paper assumes that NMSE is the appropriate metric for evaluating channel estimators, and then argues that BER is more relevant for practical systems. But there is a third metric that the paper ignores: **channel estimation latency**. In real-time communication systems, the channel estimator must complete within a strict deadline (e.g., one slot duration in 5G NR = 0.5 ms). The paper's Python benchmarks (0.21 ms for LISTA) suggest this is feasible, but the analysis does not account for: (a) data transfer overhead, (b) preprocessing (FFT of pilot signal), (c) post-processing (thresholding, clipping). A complete latency analysis would strengthen the deployment argument.

---

### Observations (Non-Defects)

- The paper's honesty about LISTA's limitations is commendable. Many papers would hide the NMSE saturation; this paper dedicates significant space to understanding and mitigating it.
- The progression from 5-seed to 20-seed ablation with transparent reporting of false negatives is exemplary scientific practice.
- The BER-NMSE mechanism analysis (error concentration on true taps) is a genuinely novel insight that contributes to the community's understanding of deep-unfolded architectures.
- The paper correctly identifies that LISTA's primary advantage is speed (4.4$\times$ throughput), not accuracy, and positions it accordingly in the deployment framework.

---

## Devil's Advocate Score (Not Applicable)

As the Devil's Advocate, I do not score the paper. My role is to challenge, not evaluate. The scoring is the responsibility of the EIC and peer reviewers.

---

## Summary of DA Findings

| Severity | Count | Key Issues |
|----------|-------|------------|
| CRITICAL | 2 | BER advantage is ZF-specific (presented as general); LISTA-CP identical results suspicious |
| MAJOR | 5 | Confirmation bias in framing; overgeneralization of cross-distribution claims; missing alternative explanations; missing stakeholder perspectives |
| MINOR | 4 | Unqualified hardware claims; sparsity knowledge implicit in training; Python speedup emphasis; LISTA output sparsity not reported |
| Observations | 4 | Commendable honesty; exemplary ablation practice; novel mechanism insight; correct speed positioning |

**DA Verdict**: The paper has 2 CRITICAL findings that must be addressed. The BER advantage claim needs explicit ZF qualification throughout the paper (abstract, highlights, conclusion). The LISTA-CP comparison needs verification. After addressing these, the paper is suitable for publication.
