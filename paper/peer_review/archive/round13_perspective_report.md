# Peer Review Report — Peer Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 13

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-disciplinary / Practical Perspective

### Reviewer Identity
FPGA/ASIC hardware engineer and systems architect with expertise in deploying neural network accelerators for real-time signal processing. Has implemented both OMP and LISTA-based estimators on FPGA platforms. Brings the "does this actually work in hardware?" perspective.

### Review Focus
Hardware deployment feasibility, throughput vs. latency trade-offs, practical deployment gaps, and real-world implementation considerations.

---

## Overall Assessment

### Recommendation
**Minor Revision**

### Confidence Score
**4** — High confidence in hardware aspects; moderate confidence in the signal processing theory.

### Summary Assessment

This paper provides a thorough experimental analysis of LISTA for sparse channel estimation, with commendable honesty about limitations. From a hardware/practical deployment perspective, the paper raises several important points — the pipelining advantage, parameter count scalability, and FLOP analysis — but the treatment has significant gaps between theoretical analysis and real hardware reality. The paper correctly identifies that Python inference time is misleading (Section 4.7.1) and that FLOP counts are more indicative of hardware cost, but then repeatedly cites the "pipelining advantage" without evidence. The theoretical hardware complexity section (Section 4.12) is the weakest part of the paper from a practical perspective: it analyzes FLOP counts but does not address memory bandwidth, data reuse, quantization effects, or actual FPGA resource utilization. With targeted improvements to the hardware discussion, the paper would be more convincing to the systems community.

---

## Strengths

### S1: Honest Python Inference Time Analysis
The paper explicitly states that the 33× Python speedup is "a software implementation artifact" (Section 4.7.1) reflecting BLAS optimization vs. Python interpreter overhead, not algorithmic efficiency. This is rare and commendable honesty — most deep learning papers would present the speedup as a genuine advantage.

### S2: Theoretical FLOP Analysis with Scaling
Table 7 provides FLOP counts across multiple channel lengths (N=32 to 256), showing the LISTA/OMP ratio increases from 2.14× to 3.06× as N grows. This scaling analysis is practically valuable for engineers evaluating LISTA for different deployment scenarios.

### S3: Parameter Count Analysis
The paper correctly identifies that the W^(k) matrices dominate parameter count (99.95%) and that at N=256, LISTA has 1.3M parameters — a potential scalability concern. The suggestion of structured linear mappings (Toeplitz, circulant, low-rank) is a practical recommendation.

### S4: SNR-Specific Training as Deployment Strategy
The finding that SNR-specific training improves NMSE by ~6 dB (Table 13) is directly actionable for hardware deployment: a LISTA accelerator could store multiple SNR-specific models and select the appropriate one based on estimated channel conditions.

---

## Weaknesses

### W1: "Pipelining Advantage" Claim Is Unsupported
**Problem**: The paper repeatedly states that "LISTA's fixed-depth feedforward architecture is more amenable to pipelining than OMP's iterative selection" (Sections 4.7.1, 4.12, 5.3). However, this is a theoretical assertion with no supporting evidence. The Wei et al. (2022) FPGA reference is cited but the paper does not analyze: (a) the actual pipeline depth and throughput, (b) memory bandwidth requirements for the W^(k) matrices, (c) the impact of the O(N^2) matrix-vector multiplication on hardware utilization.
**Why it matters**: In practice, OMP's iterative structure can also be pipelined (each iteration is a vector inner product + argmax + least-squares solve, all pipelinable). The "pipelining advantage" of LISTA is not as clear-cut as the paper suggests. Furthermore, LISTA's O(N^2) W^(k) multiplication requires N^2 multiply-accumulate operations per layer, which at N=256 is 65,536 MACs — this is a significant hardware resource requirement.
**Suggestion**: Either (a) remove the "pipelining advantage" claims and limit the hardware discussion to FLOP counts and parameter counts, or (b) provide a brief analysis of the pipeline characteristics (latency, throughput, resource utilization) for both LISTA and OMP on a hypothetical FPGA architecture. The latter would significantly strengthen the paper.
**Severity**: Major

### W2: No Discussion of Quantization Effects
**Problem**: The paper does not discuss quantization — a critical consideration for hardware deployment. LISTA's W^(k) matrices are full-precision floating-point; in hardware, these would need to be quantized (e.g., 8-bit or 16-bit fixed-point). The impact of quantization on LISTA's NMSE and BER performance is unknown.
**Why it matters**: Quantization is the primary mechanism for reducing LISTA's memory footprint and computational cost in hardware. If quantization degrades LISTA's performance significantly (e.g., the learned thresholds θ^(k) are sensitive to precision), the hardware deployment story changes dramatically.
**Suggestion**: Add a brief discussion of quantization considerations. Ideally, include a simulation experiment with quantized weights (e.g., 8-bit, 16-bit) to quantify the NMSE degradation. At minimum, acknowledge this as a limitation and future work direction.
**Severity**: Major

### W3: Memory Bandwidth Not Analyzed
**Problem**: The FLOP analysis (Table 7) counts arithmetic operations but ignores memory bandwidth. LISTA's W^(k) matrices are N×N = 4,096 elements (at N=64), stored in external memory. Each layer requires reading the full W^(k) matrix and the current estimate h^(k), computing W^(k)h^(k), and writing the result. This memory access pattern may be the bottleneck in hardware, not the arithmetic.
**Why it matters**: In FPGA implementations, memory bandwidth is often the limiting factor, not compute. A FLOP-advantageous algorithm that requires excessive memory access may be slower in practice than a FLOP-disadvantaged algorithm with good data reuse. OMP, by contrast, operates on the pilot matrix X (fixed, can be stored in BRAM) and requires minimal memory access per iteration.
**Suggestion**: Add a brief discussion of memory access patterns for LISTA vs. OMP. At minimum, note that the FLOP analysis does not account for memory bandwidth and that actual hardware performance depends on the memory-compute balance.
**Severity**: Minor

### W4: No Discussion of Training Infrastructure Requirements
**Problem**: The paper focuses on inference complexity but does not discuss training complexity. LISTA requires 200 epochs of training on 10,000 samples with backpropagation through 20 layers — this is a non-trivial computational requirement. For deployment in new channel environments, retraining may be necessary.
**Why it matters**: Practitioners need to understand the total cost of deployment, not just inference cost. If LISTA requires GPU training infrastructure and hours of training time for each new deployment scenario, the practical advantage over OMP (which requires no training) is reduced.
**Suggestion**: Add a brief paragraph on training complexity (GPU hours, convergence behavior) and discuss when retraining is necessary vs. when the Gaussian-trained model suffices.
**Severity**: Minor

---

## Detailed Comments

### Assumption Audit
- **Explicit assumptions**: The paper assumes BPSK pilot signals, AWGN noise, and sparse channels with K non-zero taps. These are standard and appropriate for the analysis.
- **Implicit assumptions**: The paper implicitly assumes that the channel statistics are stationary (same distribution in training and deployment). The cross-distribution generalization experiments partially address this.
- **Paradigmatic assumptions**: The paper assumes that NMSE is the primary metric for channel estimation quality. The BER analysis provides important context but the paper could discuss other metrics (e.g., capacity, throughput) that practitioners care about.

### Cross-Disciplinary Connections
- **Hardware-software co-design**: The paper would benefit from the hardware-software co-design perspective: how should the LISTA architecture be modified for efficient hardware implementation? (e.g., structured W^(k) matrices, reduced precision, layer fusion)
- **Edge AI deployment**: The paper's 82K parameter count is relevant to the TinyML/edge AI community. Connecting to this literature would broaden impact.

### Practical Impact
- **Real-world application**: LISTA could be deployed in 5G NR channel estimation, where low-latency inference is critical. The paper could discuss this application context more explicitly.
- **Implementation feasibility**: The 82K parameters and 760K FLOPs are feasible for FPGA deployment. However, the O(N^2) scaling limits LISTA to N ≤ 128 without structural modifications.
- **Stakeholders**: The paper addresses the DSP research community but could better serve the hardware engineering community with more practical deployment analysis.

### Broader Implications
- **Future directions**: The paper's suggestion of structured linear mappings (Toeplitz, circulant) for scalability is valuable. This connects to the broader literature on efficient neural network architectures.

---

## Cross-Disciplinary Reading Recommendations

1. **Han et al. (2016)**, "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding," *ICLR* — Foundational work on DNN compression relevant to LISTA deployment.
2. **Gholami et al. (2022)**, "A Survey of Quantization Methods for Efficient Neural Network Inference" — Comprehensive treatment of quantization techniques applicable to LISTA.
3. **Wei et al. (2022)**, "Efficient FPGA Implementation of LISTA" — Already cited but deserves deeper discussion of the actual hardware characteristics.
4. **Chen et al. (2022)**, "Hardware Implementation of Deep Unfolding Networks: Challenges and Opportunities" — Already cited but the specific challenges (memory bandwidth, quantization) should be discussed.
5. **Wang et al. (2024)**, "TinyML for Wireless Communications: Opportunities and Challenges" — Connects LISTA's small parameter count to the TinyML deployment paradigm.

---

## Questions for Authors

1. Can you provide a brief analysis of the pipeline characteristics (latency, throughput, resource utilization) for LISTA vs. OMP on a hypothetical FPGA architecture? Even a back-of-the-envelope calculation would strengthen the hardware claims.
2. Have you considered the impact of weight quantization (8-bit, 16-bit) on LISTA's performance? This is critical for practical hardware deployment.
3. The paper mentions "structured linear mappings (Toeplitz, circulant, low-rank)" for scalability. Can you provide preliminary results showing the NMSE impact of using structured W^(k) matrices?

---

## Minor Issues

- Section 4.12: "All hardware complexity values are theoretical FLOP counts; measured FPGA/ASIC latency, throughput, and power consumption remain future work" — this disclaimer appears multiple times. Consider consolidating it into one prominent statement.
- Table 7: The LISTA/OMP ratio column is helpful. Consider adding a LASSO/OMP ratio column for completeness.
- The paper's hardware discussion would benefit from a simple block diagram showing the LISTA inference pipeline (L layers, each with W^(k) multiplication + gradient computation + soft-thresholding).

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 65 | Adequate | Mechanism analysis is useful; hardware discussion is standard |
| Methodological Rigor (25%) | 75 | Strong | Comprehensive experiments; hardware analysis is theoretical only |
| Evidence Sufficiency (25%) | 72 | Adequate-Strong | Good evidence for NMSE/BER; hardware claims lack supporting evidence |
| Argument Coherence (15%) | 78 | Strong | Clear structure; hardware claims need better support |
| Writing Quality (15%) | 82 | Strong | Professional and honest |
| Significance & Impact | 68 | Adequate | Practical relevance is clear but hardware deployment story is incomplete |
| **Weighted Average** | **73** | **Minor Revision** | |
