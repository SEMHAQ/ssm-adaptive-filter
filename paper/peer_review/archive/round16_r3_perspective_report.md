Now I have a comprehensive understanding of the paper. Let me produce the review report.

---

# PEER REVIEW REPORT

## Paper Information

**Title:** Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation

**Author:** Huanjie Yu, Hunan University of Technology and Business

**Target Journal:** Digital Signal Processing (Elsevier)

**Reviewer Perspective:** Cross-disciplinary (Machine Learning, Hardware Design, Information Theory)

---

## 1. SUMMARY

This paper presents a systematic empirical analysis of LISTA (Learned ISTA) applied to sparse channel estimation. The core finding is that LISTA's NMSE saturates at approximately -25 dB for SNR >= 10 dB, trailing OMP by 13-33 dB and FISTA by 1-27 dB. Despite this NMSE disadvantage, a mechanism analysis reveals that LISTA concentrates 100.0% +/- 0.0% of estimation error on true tap locations (versus 95.2% for OMP and 92.4% for ISTA), which provides tangible BER benefits under ZF equalization for 16-QAM at SNR >= 15 dB. The paper includes ablation studies (20 seeds), generalization experiments across sparsity/SNR/channel models, a FISTA comparison, LISTA-CP comparison, SNR-saturation mitigation via SNR-specific training, and theoretical hardware complexity analysis. The paper is notably honest about limitations: it acknowledges that FISTA outperforms LISTA at all SNR levels, that all hardware complexity claims are theoretical FLOP counts, and that complex-valued channels remain future work.

---

## 2. STRENGTHS

**S1. Exceptional intellectual honesty and transparency.** The paper stands out for its willingness to report negative results. The abstract leads with LISTA trailing OMP by 13-33 dB (abstract, lines 58). The FISTA comparison (Section 4.14, Table 12) explicitly shows that a non-learned algorithm outperforms LISTA at all SNR levels, and the paper states directly: "LISTA's learned parameters do not provide improvement over standard accelerated ISTA in terms of NMSE" (line 815). The cross-table consistency note (Section 4.3, Table 6) proactively explains an 8 dB discrepancy between tables rather than hiding it. This level of candor is rare and valuable for the field.

**S2. Novel mechanism analysis with practical consequences.** The error concentration analysis (Section 4.12) is the paper's primary intellectual contribution. The finding that LISTA places 267x less error energy on non-support taps than OMP (line 742), and the ISTA control experiment demonstrating this is partially generic to soft-thresholding but enhanced by learned parameters (from 92.4% to 100.0%, Table 10), provides genuine mechanistic insight into why NMSE and BER can decouple. The ZF equalization results (Table 11) provide the system-level validation.

**S3. Rigorous statistical methodology.** The paper employs paired t-tests, Holm-Bonferroni correction for multiple comparisons, Cohen's d effect sizes, 20-seed ablation studies, and confidence intervals. The progression from the initial 5-seed ablation (Table 5, where threshold appeared insignificant) to the 20-seed ablation (Table 7, revealing it as the dominant factor with d=18.4) is a textbook demonstration of statistical power awareness. The paper explicitly acknowledges the false negative at n=5 (line 688).

**S4. Comprehensive experimental design.** The paper covers NMSE vs. SNR, sparsity, channel length, network depth, pilot ratio, ITU channel models, ablation with two sample sizes, BER with two equalizers and two modulations, FISTA comparison, LISTA-CP comparison, and SNR-saturation mitigation. This breadth provides practitioners with actionable decision frameworks.

**S5. Honest treatment of hardware complexity.** Rather than claiming hardware advantages, the paper repeatedly emphasizes that "all hardware complexity values are theoretical FLOP counts; measured FPGA/ASIC latency, throughput, and power consumption remain future work" (lines 102, 868, 900). The discussion of why Python inference speedup is a software artifact (line 514) demonstrates sophisticated understanding of computational complexity.

---

## 3. WEAKNESSES

**W1. The real-valued channel assumption severely limits practical applicability.**
- What: All experiments use real-valued channels (h in R^N) with BPSK pilot signals. Real wireless channels are complex-valued, and practical systems use QAM modulations with complex baseband signals. The paper acknowledges this (lines 965-966) but does not validate the error concentration mechanism in the complex domain.
- Where: Section 3.1 (Eq. 1, line 153): "h = [h_1, ..., h_N]^T in R^N"; Section 4.1 (line 259): "Pilot signals are BPSK-modulated (+/- 1)"; Limitations section (line 965).
- Why this matters: The soft-thresholding operator (Eq. 3) and error concentration metric (Eq. 14) are defined for real-valued signals. In the complex domain, soft-thresholding operates on magnitude while preserving phase (as the paper notes at line 965). The error concentration behavior could differ fundamentally because phase errors introduce degrees of freedom that do not exist in the real case. The 100.0% error concentration finding might not hold.
- Proposed fix: At minimum, run a supplementary experiment with complex-valued channels and QPSK pilots using complex soft-thresholding S_theta(z) = z * max(1 - theta/|z|, 0). Report whether the 100% concentration holds. This is not merely a "future work" item -- it is a validity condition for the paper's main claims.

**W2. O(N^2) parameter scaling is not adequately addressed as a fundamental limitation.**
- What: The W^(k) matrices have N^2 parameters per layer. At N=256, LISTA has 1.31M parameters and 7.9M FLOPs (Table 15, line 881), and training diverges when M/N=1 (Table 4, line 374). The paper mentions structured mappings as future work (line 209) but does not explore them.
- Where: Section 3.4 (line 209): "At N=256, the per-layer mapping alone has 65,536 parameters...a potential scalability concern"; Table 4, line 374: "Training diverged (3/5 seeds yield positive NMSE)."
- Why this matters: Modern 5G NR systems use channel lengths of 256-512+ taps. A method that diverges at N=256 with M/N=1 is not deployable in realistic pilot-constrained scenarios. The paper's experiments are confined to N=64 with generous M/N=4, which is not representative of practical systems.
- Proposed fix: (a) Implement and evaluate at least one structured variant (e.g., circulant W^(k) with N parameters per layer instead of N^2, or low-rank W^(k) = UV^T with rank r << N). (b) Report results at N=128 and N=256 with M/N=2 and M/N=4. (c) If structured variants degrade accuracy, quantify the trade-off.

**W3. No CNN or Transformer baselines, even as qualitative reference points.**
- What: The paper acknowledges CNN and Transformer methods in related work (Section 2.3) but provides no experimental comparison, citing incompatible experimental setups (Section 5.2, line 937). The qualitative comparison in Section 5.2 (line 939) states that LISTA requires "far fewer parameters (82K) than typical CNN architectures (>500K parameters)" but provides no evidence for this claim.
- Where: Section 2.3 (lines 128-135); Section 5.2 (lines 935-941).
- Why this matters: The deep unfolding paradigm's value proposition is that it combines model-based interpretability with data-driven performance. Without at least one CNN baseline under identical conditions, it is impossible to assess whether LISTA's interpretability comes at a performance cost, or whether a simple CNN achieves comparable error concentration without requiring algorithm-specific architecture design. The claim that LISTA has fewer parameters is unsubstantiated.
- Proposed fix: Implement a simple 1D CNN (e.g., 3-4 conv layers with 32-64 channels, <100K parameters) trained on the same data with the same NMSE loss. Report NMSE and error concentration metrics. This does not require a comprehensive benchmark -- a single controlled comparison would significantly strengthen the paper.

**W4. The error concentration mechanism's practical significance is overstated.**
- What: The paper's primary contribution is the error concentration mechanism, which provides BER benefits only under ZF equalization with 16-QAM at SNR >= 15 dB. Under MMSE (the standard equalizer), all methods achieve similar BER (p > 0.05). The paper acknowledges this but frames the ZF results as a primary finding.
- Where: Table 8 (line 597): "all estimators converge to similar BER at SNR >= 5 dB (p > 0.05)"; Table 11 (line 643): 16-QAM ZF BER advantage at SNR >= 15 dB.
- Why this matters: MMSE equalization is used in virtually all modern receivers (LTE, 5G NR, WiFi 6+). ZF equalization is rarely used in practice because it is known to amplify noise. The paper argues ZF is relevant for "low-complexity IoT receivers" (line 931), but even IoT receivers (e.g., NB-IoT, LoRa) use MMSE or matched filtering. The error concentration mechanism, while intellectually interesting, has limited practical impact.
- Proposed fix: (a) Recenter the paper's narrative: the primary contribution is the mechanistic insight (error concentration is a property of soft-thresholding enhanced by learned parameters), with BER benefits as a secondary validation. (b) Quantify under what SNR and modulation conditions ZF is actually used in practice, citing specific standards. (c) Consider whether the error concentration insight could improve MMSE equalization through better channel estimate post-processing.

**W5. The "100.0% +/- 0.0%" claim requires deeper scrutiny.**
- What: LISTA's error concentration is reported as 100.0% +/- 0.0% across 5 seeds (Table 9, line 732). This exact value with zero variance is suspicious and warrants explanation.
- Where: Table 9 (line 732): "LISTA: 100.0 +/- 0.0"; Table 10 (line 754): "LISTA: 100.0 +/- 0.0."
- Why this matters: With N=64, K=5, and finite-precision floating point, achieving exactly 100.0% error on support taps across all realizations and all seeds is extremely unlikely unless the soft-thresholding operator forces non-support estimates to exactly zero. If S_theta maps all non-support estimates to exactly zero, then the "error concentration" is trivially true -- there is literally no error on non-support taps because the estimate is zero there. This would mean the mechanism is not about "concentration" but about hard support selection, and the finding reduces to "soft-thresholding produces sparse estimates," which is well-known.
- Proposed fix: (a) Report the actual non-support error values (e.g., 0.01% vs 0.001%) rather than just the percentage. (b) Verify whether non-support estimates are exactly zero (hard thresholding effect) or merely very small. (c) If the former, reframe the finding: LISTA's learned thresholds effectively perform oracle support selection, which is the real insight. (d) Report results with non-quantized floating point to rule out numerical artifacts.

**W6. The BPSK pilot assumption limits generalization claims.**
- What: All experiments use BPSK pilots (+/- 1). Practical systems use QAM pilots or Zadoff-Chu sequences. The convolution matrix X formed from BPSK pilots has special structure (entries in {-1, +1}) that affects the restricted isometry properties.
- Where: Section 4.1 (line 259): "Pilot signals are BPSK-modulated (+/- 1)."
- Why this matters: The measurement matrix properties directly affect sparse recovery performance. BPSK pilots produce a binary measurement matrix with specific coherence properties. QPSK or QAM pilots would produce complex-valued matrices with different properties. The generalization claims ("LISTA generalizes across channel types," line 898) may not hold with different pilot structures.
- Proposed fix: Run at least the key experiments (NMSE vs. SNR, error concentration) with QPSK or QAM pilots to validate that the findings are not artifacts of the BPSK measurement structure.

**W7. The paper does not discuss training cost or data requirements.**
- What: The paper reports inference complexity (760K FLOPs, 0.21 ms) but does not report training time, number of training samples needed, or the cost of collecting/generating training data. Mixed-SNR training requires 10,000 training samples (line 259).
- Where: Section 4.1 (line 259): "10,000 training samples"; Section 3.5 (lines 220-226): training procedure.
- Why this matters: The total cost of deploying LISTA includes training cost + inference cost. If training requires hours of GPU time and thousands of labeled channel realizations, the total cost may exceed the cost of simply running FISTA (which requires no training). For a fair comparison with training-free methods, the paper should report training wall-clock time and discuss whether training data is available in practice.
- Proposed fix: Report training wall-clock time on the specified hardware. Discuss whether 10,000 labeled channel realizations are available in practice (e.g., through channel sounding campaigns or simulation).

---

## 4. DETAILED COMMENTS

### Section 1 (Introduction)

**C1.** Line 92: "likely a training artifact caused by the scale-invariant loss and mixed-SNR training, rather than a fundamental architectural limitation." This is stated as a hypothesis but is treated as established fact throughout the paper. The SNR-specific training result (6 dB improvement) is consistent with this hypothesis but does not prove it. The improvement could also be due to reduced variance in the training distribution making optimization easier, independent of the scale-invariant loss. Consider rewording to "consistent with a training artifact hypothesis" and adding a control experiment that uses absolute MSE loss instead of NMSE loss to isolate the effect.

**C2.** Line 96: "quantifying the contribution of each learnable component." The ablation study removes components individually but does not test interactions. For example, removing W^(k) AND fixing the threshold simultaneously might show a super-additive or sub-additive effect. Consider adding a 2-way interaction ablation.

### Section 3 (Method)

**C3.** Lines 186-189: The learnable mapping W^(k) is described as "effectively learning a preconditioner that captures inter-tap dependencies." For i.i.d. Gaussian channels where taps are uncorrelated, what inter-tap dependencies is W^(k) learning? The paper does not analyze the learned W^(k) matrices. Visualizing or analyzing the spectral structure of the learned W^(k) - I matrices would provide insight into what LISTA learns and strengthen the mechanistic interpretation.

**C4.** Lines 197-201: FFT-based convolution is used for computational efficiency, reducing per-layer complexity from O(MN) to O(M log M). However, this assumes circular convolution. The channel model in Eq. 1 (line 155) uses a convolution matrix X, which implements linear (not circular) convolution. When M < 2N-1, circular and linear convolution produce different results due to wrap-around effects. With N=64 and M=256, this is likely fine (M > 2N), but the paper should explicitly verify that no boundary artifacts occur.

### Section 4 (Experiments)

**C5.** Table 1 (line 284): At SNR=5 dB, LISTA shows std=4.10 dB, which is 6-40x larger than other entries in the table. This high variance at SNR=5 dB is not discussed. Is one seed diverging? Is there a phase transition? This anomaly warrants investigation.

**C6.** Table 4 (line 374): At N=256, LISTA shows NMSE = 26.84 +/- 30.23 dB (positive NMSE), indicating training divergence. The paper reports "3/5 seeds yield positive NMSE" but does not analyze why. Is this a gradient explosion issue? An ill-conditioned measurement matrix? Understanding the failure mode would be more valuable than simply reporting it.

**C7.** Table 5 (line 457): The initial 5-seed ablation shows that fixing the threshold degrades NMSE by only -0.26 dB (p=0.455), while the 20-seed ablation (Table 7) shows +14.44 dB (p<0.001). The sign of delta is actually negative in Table 5 (-0.26) but positive in Table 7 (+14.44). This sign flip is not just a power issue -- it suggests the 5-seed result was not just underpowered but actively misleading. The paper should discuss this more prominently as a cautionary tale about small sample sizes.

**C8.** Section 4.14 (FISTA comparison, line 793): FISTA uses grid-searched threshold while LISTA uses learned thresholds. A fairer comparison would be FISTA with the same number of gradient evaluations as LISTA's training budget, or LISTA with oracle threshold initialization. The current comparison favors FISTA by giving it optimized hyperparameters while LISTA must learn them from data.

**C9.** Table 14 (line 824): The noise enhancement factor at SNR=30 dB shows LISTA at 25.3 vs OMP at 6.1, a 4.2x disadvantage. The paper explains this as "LISTA's slight support recovery errors (J = 0.93) create occasional spectral nulls" (line 837). This is a significant disadvantage that undermines the noise enhancement narrative. The paper should present the noise enhancement results more balancedly, noting that LISTA's advantage reverses at high SNR.

### Section 5 (Discussion)

**C10.** Lines 913-923: The argument that saturation is a training artifact relies on three pieces of evidence, none of which is conclusive. (1) Scale-invariant loss: This is a plausible hypothesis but not tested (no experiment with absolute MSE loss). (2) SNR-specific training breaks saturation: This shows the saturation level is training-dependent, but does not prove it is not also architecture-dependent. (3) LISTA-CP constraints naturally satisfied: This shows the architecture converges, not that it can represent the optimal solution. The paper should present this as a hypothesis with supporting evidence, not as an established finding.

**C11.** Lines 935-941: The comparison with deep learning baselines is entirely qualitative. The claim that "LISTA requires far fewer parameters (82K) than typical CNN architectures (>500K parameters)" (line 939) is unsupported. A minimal 1D CNN with 3 conv layers, 32 channels, kernel size 5, would have approximately 3 * (32*5 + 32) * 32 ~ 16K parameters -- far fewer than LISTA's 82K. The parameter count comparison should be backed by actual CNN implementations.

**C12.** Lines 947-959: The deployment recommendation framework is premature given the absence of hardware measurements. Recommending LISTA for "throughput-critical applications" (line 950) based on theoretical FLOP analysis is speculative. The paper should soften these recommendations or explicitly state they are hypotheses to be validated.

### Missing Analysis

**C13.** The paper does not analyze what the learned thresholds theta^(k) look like across layers. The ablation shows that per-layer threshold schedule is the dominant factor (+14-18 dB). Plotting theta^(k) vs. layer index k would reveal whether LISTA learns a monotonically decreasing schedule (like ISTA's convergence path), an adaptive schedule, or something else entirely. This analysis would significantly strengthen the mechanistic understanding.

**C14.** The paper does not report the condition number of the measurement matrix X or its effect on LISTA performance. For i.i.d. Gaussian X with M/N=4, the condition number is well-controlled, but the paper does not verify this. At M/N=1.5 (Table 3), the condition number may be large, explaining the training instability.

---

## 5. QUESTIONS FOR THE AUTHORS

**Q1.** Can you verify whether LISTA's non-support estimates are exactly zero or merely very small? If exactly zero, the "error concentration" finding reduces to "soft-thresholding produces sparse estimates," which is well-known. The novel claim would then be that LISTA learns thresholds that effectively perform oracle support selection.

**Q2.** Have you analyzed the learned W^(k) matrices? What spectral structure do they have? How different are they from the identity? Understanding what W^(k) learns would significantly strengthen the mechanistic interpretation.

**Q3.** Can you run a control experiment replacing the NMSE loss with absolute MSE loss to test whether the saturation is caused by scale invariance? This would directly test your primary hypothesis.

**Q4.** For the 16-QAM ZF BER advantage (Table 11): what is the absolute BER difference? At SNR=20 dB, LISTA achieves 0.305 vs OMP's 0.316 -- a difference of 0.011. Is this practically significant for a communication system?

**Q5.** What is the training wall-clock time? For practitioners considering LISTA vs. FISTA, the total cost (training + inference) matters, not just inference cost.

---

## 6. DISCUSSION (Cross-disciplinary Perspective)

### 6.1 Connections to Model-Based Deep Learning

This paper contributes to the growing body of evidence on model-based deep learning, a paradigm where domain knowledge is encoded into network architectures. The key cross-disciplinary insight is that LISTA's learned parameters do not improve NMSE over FISTA, but they do alter the error structure in ways that affect downstream tasks (BER). This finding has implications beyond channel estimation: in any inverse problem where the loss metric (NMSE) does not align with the downstream task metric (BER, classification accuracy, reconstruction quality), optimizing the loss metric may be suboptimal. This is closely related to the "task-aware" optimization literature in compressive sensing and the "end-to-end" learning paradigm.

The paper's finding that the per-layer threshold schedule dominates the ablation (+14-18 dB) is significant for the deep unfolding community. It suggests that the primary value of deep unfolding is not the learnable linear mappings (which can be expensive) but the learnable nonlinearities (which are cheap). This has implications for hardware-efficient architecture design: one could replace the N^2-parameter W^(k) matrices with fixed or structured matrices while retaining the learnable thresholds, achieving most of the benefit with far fewer parameters.

### 6.2 Practical Deployment Barriers

From a practical standpoint, the paper identifies several deployment barriers but does not adequately address them:

1. **Training data availability:** LISTA requires 10,000 labeled channel realizations. In practice, obtaining labeled training data requires either (a) channel sounding campaigns (expensive, limited to specific environments) or (b) simulation (requires accurate channel models, which may not be available for new deployments). FISTA and OMP require no training data.

2. **SNR-specific training:** The paper shows that SNR-specific training improves NMSE by 6 dB, but this requires knowing the operating SNR at training time. In variable-SNR environments, this information is not available. The paper acknowledges this (line 539) but does not provide a solution beyond using broad-range training.

3. **Online adaptation:** Unlike LMS/NLMS, LISTA cannot adapt online to changing channel conditions. The paper does not discuss this limitation, which is critical for time-varying channels.

4. **Regulatory and standardization barriers:** Deploying a neural network-based channel estimator in a standardized communication system (3GPP, IEEE 802.11) would require standardization of the network architecture, training procedure, and model parameters. This is a significant barrier that the paper does not discuss.

### 6.3 Fundamental Assumptions

The paper's assumptions -- real-valued channels, sparse CIRs, BPSK pilots, single-input single-output -- are significantly more restrictive than what modern communication systems require. The sparsity assumption (K << N) is reasonable for wideband channels but may not hold for massive MIMO or millimeter-wave systems where the channel is approximately dense. The BPSK pilot assumption excludes all practical pilot sequences (Zadoff-Chu, CAZAC, Gold codes). While the paper acknowledges these limitations, the gap between the experimental setup and practical conditions is large enough to question whether the findings would transfer.

### 6.4 Broader Implications of Error Concentration

The error concentration mechanism -- that soft-thresholding-based algorithms concentrate estimation error on true support locations -- has implications beyond channel estimation. In medical imaging (MRI, CT), sparse recovery algorithms are used to reconstruct images from undersampled measurements. If LISTA's error concentration holds in that domain, it would mean that LISTA's reconstruction errors are localized to true features rather than spread as artifacts, which could be more acceptable to clinicians. Similarly, in spectral estimation, error concentration on true frequencies would produce cleaner spectral estimates. The paper could significantly increase its impact by discussing these cross-domain implications.

### 6.5 Missing Comparison: End-to-End Learning

The paper compares LISTA against model-based methods (OMP, LASSO, FISTA) but not against end-to-end learned approaches where the entire receiver (channel estimation + equalization + decoding) is trained jointly. In such systems, the channel estimate is an intermediate representation, and optimizing it for NMSE may not be optimal for the end-to-end task. LISTA's error concentration mechanism might be discovered automatically by end-to-end training, without requiring the deep unfolding architecture. This is a fundamental question for the deep unfolding paradigm that the paper does not address.

---

## 7. SCORES

| Dimension | Score (0-100) | Justification |
|-----------|---------------|---------------|
| **Novelty/Originality** | 55 | The mechanism analysis (error concentration) is novel and insightful. However, LISTA for channel estimation is not new, and the paper explicitly disclaims architectural novelty. The finding that FISTA outperforms LISTA at all SNR levels, while honest, means the learned approach does not advance the state of the art in estimation accuracy. |
| **Technical Rigor** | 78 | Strong statistical methodology (Holm-Bonferroni, Cohen's d, 20-seed ablation). However, all experiments are on real-valued channels with BPSK pilots, which is a significant limitation. The 100.0% +/- 0.0% error concentration claim warrants deeper investigation. No hardware measurements despite deployment claims. |
| **Significance/Impact** | 50 | The error concentration insight is intellectually valuable but has limited practical impact: it only matters under ZF equalization, which is rarely used in modern systems. Under MMSE (the standard), all methods achieve similar BER. The paper does not demonstrate a scenario where LISTA is clearly the best choice for a practitioner. |
| **Clarity/Presentation** | 82 | Well-written with clear narrative structure. The honest treatment of limitations is exemplary. Tables and figures are well-designed. However, some claims are overstated relative to the evidence (e.g., deployment recommendations without hardware validation). |
| **Relevance to Journal** | 70 | Relevant to Digital Signal Processing as it concerns a signal processing algorithm (LISTA) applied to a core DSP problem (channel estimation). However, the narrow experimental setup (real-valued, BPSK, single-antenna) limits the relevance to modern communication systems. |
| **Reproducibility** | 85 | Code appears available, hyperparameters are well-documented, statistical methods are clearly described. The seed-by-seed reporting in ablation studies is commendable. |

**Overall Score: 62/100** -- The paper demonstrates strong methodological rigor and intellectual honesty, but its practical impact is limited by the narrow experimental setup, the absence of hardware validation, and the finding that FISTA (a training-free method) outperforms LISTA at all SNR levels. The error concentration mechanism is the primary contribution, but its practical relevance is confined to ZF equalization, which is rarely used in modern systems. The paper would be significantly strengthened by: (1) extending to complex-valued channels, (2) adding at least one CNN baseline, (3) analyzing the learned W^(k) matrices and threshold schedules, and (4) either validating the hardware claims or removing the deployment recommendations.

---

## 8. RECOMMENDATION

**Major Revision.** The paper has valuable contributions (error concentration mechanism, rigorous statistical methodology, honest reporting) but requires major revisions to address the real-valued channel limitation, the absence of CNN/Transformer baselines, the need for deeper analysis of what LISTA learns, and the overstatement of practical impact relative to the evidence.

---

## 9. CONFIDENCE

**4/5** -- High confidence. I have read the paper thoroughly and examined the code structure. My concerns about the real-valued assumption, the BPSK pilot limitation, and the practical relevance of ZF equalization are well-grounded in communication systems practice. The cross-disciplinary perspective highlights gaps that domain-specific reviewers might overlook.