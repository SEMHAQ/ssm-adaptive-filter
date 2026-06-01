# Perspective Review Report (Peer Reviewer 3)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-ROUND8
- **Review Date**: 2026-06-01
- **Review Round**: Round 8

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Cross-Disciplinary Perspective)

### Reviewer Identity
Dr. Aisha Okonkwo — Senior Research Scientist at a major telecommunications R&D lab, with expertise in FPGA/ASIC implementation of signal processing algorithms, real-time systems, and hardware-software co-design. 10 years of experience bridging the gap between algorithmic research and practical deployment in wireless communication systems.

### Review Focus
Practical deployment feasibility, hardware implementation realism, cross-disciplinary connections (algorithm design ↔ hardware engineering), and whether the paper's conclusions are actionable for practitioners. I bring the "implementer's perspective" — what happens when you try to actually build this system?

---

## Overall Assessment

### Recommendation
**Minor Revision**

### Confidence Score
4 — High confidence. Hardware implementation of signal processing algorithms is my core expertise. I am less familiar with the theoretical aspects of deep unfolding convergence but can strongly evaluate practical deployment claims.

### Summary Assessment
This paper provides a valuable bridge between the deep unfolding community and the channel estimation community, offering a systematic and honest assessment of LISTA's practical capabilities. The BER-NMSE disconnect finding is genuinely useful for practitioners: it tells system designers that optimizing NMSE may not be the right objective when MMSE equalization is used. However, the paper's hardware claims are its weakest aspect — they are based entirely on theoretical FLOP counts and pipeline analysis without any measured results. The paper repeatedly caveats this, which is good, but the level of detail (e.g., "1.2 μs throughput") creates an impression of precision that measured hardware would not necessarily confirm. From a deployment perspective, the paper would benefit from discussing: (1) the training infrastructure requirements, (2) the model update strategy for time-varying channels, and (3) the integration with existing receiver architectures. Overall, the paper is a solid analytical contribution with actionable insights for the DSP community.

---

## Strengths

### S1: Honest Assessment of Practical Limitations
The paper is refreshingly honest about what LISTA cannot do: it trails OMP by 13–33 dB on NMSE, training diverges at N=256, and one seed diverges at K=15. This transparency is valuable for practitioners who need to make informed deployment decisions. The explicit statement that hardware estimates are "theoretical" and that "measured FPGA/ASIC results remain future work" is appropriate.

### S2: BER-NMSE Disconnect is Actionable for System Designers
The finding that LISTA's NMSE gap does not translate to BER penalty under MMSE equalization is directly actionable: system designers can use LISTA for speed-critical applications without worrying about BER degradation, as long as MMSE equalization is employed. This is a practical insight that goes beyond academic metrics.

### S3: Decision Framework for Practitioners
Section 5.3 provides a clear decision framework: (1) speed-critical → LISTA, (2) known SNR → SNR-specific training, (3) variable SNR → broad-range training, (4) NMSE-critical → OMP/LASSO. This is exactly what practitioners need — not just performance numbers, but guidance on when to use what.

### S4: Error Structure Analysis Provides Design Insight
The mechanism analysis (Section 4.12) revealing that LISTA concentrates 99.9% of error on true taps (vs. 94.9% for OMP) provides a design insight: LISTA's soft-thresholding enforces sparsity in the estimate, which is beneficial for equalization. This insight could inform the design of other deep-unfolded architectures for communications.

### S5: Comprehensive Generalization Analysis
The multi-axis generalization analysis (sparsity, SNR, channel type) is valuable for deployment planning. The finding that Gaussian-trained LISTA generalizes to ITU channels (-23 to -27 dB) without channel-specific training is practically useful, as it eliminates the need for channel-specific training data.

---

## Weaknesses

### W1: Hardware Claims Are Purely Theoretical
**Problem**: Section 4.13 presents detailed hardware timing estimates (23 μs sequential, 1.2 μs pipelined, 4.4× speedup) based entirely on FLOP counts and pipeline analysis. The paper cites Wei et al. (2022) for FPGA validation but does not provide measured results. The theoretical estimates assume 64 parallel DSP units at 500 MHz, which is a specific FPGA configuration that may not be representative.
**Why it matters**: From an implementer's perspective, FLOP counts are a poor predictor of actual hardware performance. Memory bandwidth, pipeline stalls, clock frequency, and implementation overhead can easily change the speedup by 2–5×. The 4.4× estimate could easily be 2× or 8× in practice.
**Suggestion**: (1) Acknowledge more prominently that the 4.4× estimate has high uncertainty (±50% or more). (2) Discuss the key assumptions that could break: memory bandwidth (W^(k) matrices are 16 KB each, 328 KB total — this fits in L2 cache but not L1), pipeline stalls (data dependencies between layers), and clock frequency (500 MHz is optimistic for mid-range FPGAs). (3) If possible, provide a range estimate (e.g., "2–6× throughput advantage") rather than a point estimate.
**Severity**: Major

### W2: No Discussion of Training Infrastructure and Model Update Strategy
**Problem**: The paper discusses inference-time deployment but does not address: (1) what hardware is needed for training (GPU requirements, training time), (2) how often the model needs to be retrained (e.g., when the channel statistics change), (3) whether the trained model can be updated incrementally or requires full retraining.
**Why it matters**: For practical deployment, the total cost of ownership includes training infrastructure and maintenance, not just inference. If the channel changes frequently (e.g., vehicular scenarios), LISTA may need frequent retraining, negating its inference-time advantage.
**Suggestion**: Add a brief discussion in Section 5.3 addressing: (1) training requirements (GPU, time, data), (2) model update strategy for time-varying channels, (3) scenarios where training cost is amortized (static channels, pre-trained models) vs. scenarios where it is a limitation.
**Severity**: Minor

### W3: The 16-QAM BER Advantage Under ZF Is of Limited Practical Value
**Problem**: The paper presents LISTA's 16-QAM BER advantage under ZF equalization (Table 8) as a positive finding. However, the BER values are very high (0.29–0.32 at SNR 15–30 dB) — far above practical operating BER targets (typically 10⁻³ for 16-QAM). ZF equalization is rarely used in practice for 16-QAM precisely because of noise enhancement.
**Why it matters**: Practitioners may misinterpret this as a practical advantage. The finding is theoretically interesting for understanding error structure, but has limited practical value.
**Suggestion**: Add a sentence clarifying that the 16-QAM BER values under ZF are well above practical operating thresholds, and that the finding is primarily of theoretical interest. Consider reframing the ZF results as "error structure analysis" rather than "BER advantage."
**Severity**: Minor

### W4: No Discussion of Integration with Existing Receiver Architectures
**Problem**: The paper evaluates LISTA as a standalone channel estimator but does not discuss how it would integrate with existing receiver architectures. Specifically: (1) How does LISTA's output interface with the MMSE/ZF equalizer? (2) What is the end-to-end latency from received signal to equalized output? (3) Can LISTA be pipelined with the equalizer?
**Why it matters**: In practice, the channel estimator is part of a larger receiver chain. The latency and throughput of the entire chain matter, not just the estimator.
**Suggestion**: Add a brief discussion in Section 5.3 or Section 4.13 addressing the integration with existing receiver architectures. If possible, estimate the end-to-end latency including equalization.
**Severity**: Minor

### W5: Scalability Concerns Are Underexplored
**Problem**: The paper acknowledges that LISTA training diverges at N=256 (Table 3) and that O(N²) per-layer complexity is a scalability limitation. However, the paper does not explore mitigation strategies beyond suggesting "structured linear mappings (Toeplitz, circulant, low-rank)."
**Why it matters**: Many practical channel estimation problems involve N ≥ 128 (e.g., OFDM with long cyclic prefixes, wideband communications). Without even a proof-of-concept structured variant, the paper's practical impact is limited to short channels (N ≤ 128).
**Suggestion**: If feasible, add a brief experiment with a structured W^(k) (e.g., low-rank approximation with rank r = 8 or 16) to demonstrate that the scalability limit can be addressed. If not feasible, discuss the expected performance of structured variants based on the literature.
**Severity**: Minor

---

## Detailed Comments

### Assumption Audit

**Explicit assumptions:**
- The paper assumes BPSK-modulated pilots (±1), which is realistic for pilot signals but limits the generality of the results.
- The paper assumes AWGN noise, which is a simplification of real-world noise (which may be colored, impulsive, or non-Gaussian).
- The paper assumes the channel is static during the pilot and data transmission (quasi-static fading), which is standard but limits applicability to high-mobility scenarios.

**Implicit assumptions:**
- The paper implicitly assumes that training data is available and representative of the deployment channel. In practice, obtaining representative training data can be challenging, especially for rare channel conditions.
- The paper implicitly assumes that the computational cost of training is amortized over many inference calls. For applications with infrequent channel estimation (e.g., low-duty-cycle IoT), this assumption may not hold.

**Paradigmatic assumptions:**
- The paper assumes that NMSE is the primary metric for evaluating channel estimators. The BER analysis challenges this assumption (NMSE gap does not translate to BER penalty), which is a valuable paradigmatic contribution.

### Cross-Disciplinary Connections

**Parallel research:**
- In the FPGA/ASIC design community, there is extensive work on hardware-efficient neural network implementations (e.g., quantization, pruning, knowledge distillation). These techniques could be applied to reduce LISTA's hardware complexity.
- In the machine learning community, there is work on meta-learning for fast adaptation to new distributions. This could address the training cost concern by enabling rapid adaptation to new channel conditions.

**Borrowing opportunities:**
- **Quantization-aware training**: Training LISTA with quantized weights (e.g., 8-bit fixed-point) would reduce memory requirements and enable deployment on low-cost FPGAs.
- **Neural architecture search (NAS)**: Could be used to optimize the LISTA architecture (number of layers, layer widths) for specific hardware constraints.
- **Transfer learning**: Pre-trained LISTA models could be fine-tuned for specific channel conditions with minimal training data.

**Methodological borrowing:**
- The hardware engineering community uses cycle-accurate simulation for performance estimation. The paper's FLOP-based estimates could be validated using such tools (e.g., Vivado HLS for Xilinx FPGAs).

### Practical Impact

**Real-world application:**
- The paper's recommendations are actionable for system designers: use LISTA for speed-critical applications with MMSE equalization, use SNR-specific training when the operating SNR is known.
- The 4.4× theoretical throughput advantage, if validated, would be significant for latency-critical applications (e.g., URLLC in 5G).

**Implementation feasibility:**
- The 82K parameters (328 KB) fit comfortably in FPGA block RAM, making deployment feasible.
- The fixed-depth feedforward architecture is well-suited for FPGA implementation, as noted in the paper.
- The main implementation challenge is the O(N²) W^(k) matrices, which require significant multiply-accumulate resources.

**Stakeholders:**
- The paper addresses the needs of system designers (BER performance), hardware engineers (complexity analysis), and researchers (ablation studies).
- Missing: the perspective of standards bodies (3GPP, IEEE) who define the channel models and equalization requirements.

### Broader Implications

**Ethical dimensions:**
- No significant ethical concerns. The technology is neutral and applicable to standard wireless communications.

**Social impact:**
- Faster channel estimation could enable higher data rates and lower latency, benefiting end users.
- The energy efficiency implications are not discussed — LISTA's lower FLOP count could translate to lower power consumption, which is increasingly important for green communications.

**Future directions:**
- The most valuable follow-up research would be: (1) measured FPGA/ASIC results, (2) extension to OFDM and frequency-selective channels, (3) extension to MIMO systems, (4) integration with modern receiver architectures (e.g., iterative detection and decoding).

---

## Cross-Disciplinary Reading Recommendations

1. **Han, S., et al. (2016). "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding." *ICLR*.** — Foundational work on neural network compression; directly applicable to reducing LISTA's hardware complexity.

2. **Finn, C., et al. (2017). "Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks." *ICML*.** — Meta-learning for rapid adaptation; could address LISTA's training cost concern by enabling fast adaptation to new channel conditions.

3. **Gaudette, J., et al. (2020). "Learned Quantization for Efficient Inference in Deep Neural Networks." *IEEE JETCAS*.** — Hardware-aware quantization for neural networks; applicable to LISTA's fixed-point implementation.

4. **Shen, Y., et al. (2021). "Hardware-Aware Neural Architecture Search for Efficient Visual Wake Words." *IEEE Access*.** — NAS for hardware-efficient architectures; could optimize LISTA's architecture for specific FPGA constraints.

5. **Chen, T., et al. (2021). "Hardware-Aware Automated Machine Learning." *Springer*.** — Comprehensive treatment of hardware-aware ML; relevant to LISTA's deployment on resource-constrained platforms.

---

## Questions for Authors

1. Can you provide a range estimate (e.g., "2–6×") for the hardware throughput advantage rather than a point estimate (4.4×)? The uncertainty in theoretical estimates is typically ±50% or more.

2. Have you considered applying quantization-aware training to LISTA? Reducing weights from float32 to int8 would reduce memory by 4× and enable deployment on lower-cost FPGAs.

3. How would LISTA's performance change if the pilot signal were QPSK-modulated rather than BPSK? The BPSK assumption limits the generality of the results.

4. What is the expected performance of LISTA on frequency-selective (OFDM) channels? The current evaluation assumes single-carrier flat-fading channels.

---

## Minor Issues

### Practical Considerations
- Section 4.13: The assumption of "64 parallel DSP units at 500 MHz" is specific to mid-range FPGAs. Consider noting that high-end FPGAs (e.g., Xilinx Versal) have 1000+ DSP units and can operate at higher frequencies.
- Table 11 (Scaling): The LISTA parameters at N=256 (1.3M) would require ~5 MB of storage at float32, which exceeds typical FPGA L2 cache. Consider noting this as a deployment constraint.

### Writing
- Section 5.3: The decision framework is clear and actionable. Consider presenting it as a flowchart or decision tree figure for easier reference.
- Section 4.7.2: The ITU channel results are presented without standard deviations for LMS/NLMS/OMP/LASSO. This inconsistency should be addressed.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 60 | Adequate | Known architecture; novel systematic analysis with BER insight |
| Methodological Rigor (25%) | 75 | Strong | Comprehensive experiments; hardware claims need more caveating |
| Evidence Sufficiency (25%) | 80 | Strong | 13 experiments, ITU validation, ablation |
| Argument Coherence (15%) | 83 | Strong | Logical flow, actionable recommendations |
| Writing Quality (15%) | 82 | Strong | Clear, honest, well-organized |
| Significance & Impact | 72 | Adequate | Practical insights for speed-critical deployments; scalability limits |
| **Weighted Average** | **75.0** | **Minor Revision** | |
