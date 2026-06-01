# Peer Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 10

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-disciplinary / Practical Deployment

### Reviewer Identity
Principal Engineer at a semiconductor company, with a PhD in Electrical Engineering and 12 years of experience in FPGA/ASIC design for wireless communication systems. Specializes in deploying neural network accelerators on resource-constrained platforms. Published on hardware implementation of deep learning for physical-layer processing, including FPGA-based LISTA implementations.

### Review Focus
Validity of hardware complexity claims (FLOPs, pipelining, throughput), practical deployability (parameter count, memory footprint, latency), and the gap between theoretical estimates and measured hardware results.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
4 — Hardware implementation of neural networks is my core expertise. The signal processing aspects are within my broader competence.

### Summary Assessment
This paper provides a theoretical hardware complexity analysis of LISTA for sparse channel estimation, comparing FLOP counts, parallelism characteristics, and memory access patterns against OMP and LASSO. The analysis is technically sound but fundamentally incomplete: all hardware claims are theoretical estimates with no measured validation. The paper repeatedly acknowledges this ("measured FPGA/ASIC results remain future work"), yet the hardware section (Section 4.13) constitutes approximately 2000 words and 4 tables—substantial real estate for unvalidated claims. The theoretical FLOP analysis is straightforward arithmetic that any reader can compute; it does not constitute a research contribution. The pipelining analysis (20-stage pipeline, 1.2 μs throughput) makes assumptions about memory bandwidth, pipeline stalls, and clock frequency that are not validated. The "33× speedup" is a Python benchmark that reflects interpreter overhead, not algorithmic efficiency. The paper would be significantly strengthened by either (a) providing at least a prototype FPGA implementation, or (b) dramatically shortening the hardware section and positioning it as brief future-work outlook.

---

## Strengths

### S1: Honest and Transparent Caveating
The paper consistently hedges all hardware claims with appropriate caveats: "theoretical estimates," "subject to implementation-dependent factors," "measured FPGA/ASIC results remain future work." This transparency is commendable and prevents the reader from being misled. The paper explicitly states in Section 4.13: "We emphasize that all hardware timing estimates in this section are theoretical; measured FPGA/ASIC results remain future work."

### S2: FLOP Analysis Provides Useful Complexity Reference
Table 14 (FLOPs comparison) provides a clear, quantitative comparison: LISTA requires 760K FLOPs (2.3× OMP, 8.7× less than LASSO). While this is straightforward arithmetic, it provides a useful reference for readers evaluating LISTA's computational requirements. The breakdown of per-layer FLOPs (matrix-vector products, FFT convolution, soft-thresholding) is informative.

### S3: Scaling Analysis Highlights the N² Problem
Table 17 (scaling analysis) shows that LISTA's parameter count grows as O(N²), reaching 1.3M parameters at N=256. The paper correctly identifies this as "a potential scalability concern" and suggests structured linear mappings (Toeplitz, circulant, low-rank) as a mitigation. This is practically useful guidance.

### S4: Memory Access Pattern Analysis is Informative
The analysis of LISTA's sequential, predictable memory access patterns (Section 4.13.3) versus OMP's semi-random column selection provides useful hardware design insight. The observation that LISTA's W^(k) matrices (16 KB each, 328 KB total) fit in L2 cache is a practical deployment consideration.

### S5: Comparison with Published FPGA Results
The paper cites Wei et al. (2022) who demonstrated < 10 μs LISTA latency on FPGA, and notes that the theoretical estimates are "consistent with" this measured result. This anchoring to published hardware results adds credibility to the theoretical estimates.

---

## Weaknesses

### W1: No Measured Hardware Validation
**Problem**: All hardware complexity claims (760K FLOPs, 20-stage pipelining, 1.2 μs throughput, 33× speedup) are theoretical estimates. The paper provides no measured FPGA/ASIC results—no latency measurements, no power consumption, no resource utilization.
**Why it matters**: The hardware section (Section 4.13) is approximately 2000 words with 4 tables, yet provides no empirical validation. The theoretical FLOP analysis is trivial arithmetic. The pipelining analysis makes assumptions about memory bandwidth and pipeline stalls that can only be validated through implementation. Without measured results, the hardware claims are unverifiable.
**Suggestion**: Either (a) provide a prototype FPGA implementation with measured latency, power, and resource utilization (this would be a significant contribution), or (b) dramatically shorten the hardware section to a brief paragraph in the Discussion, positioning it as future work. Option (b) is more realistic for a single-author paper.
**Severity**: Critical

### W2: The "33× Speedup" is a Software Artifact
**Problem**: The paper claims "33× faster inference (0.21 vs 6.91 ms)" throughout the abstract and main text. This speedup is measured in Python (NumPy/PyTorch) and reflects the difference between LISTA's fixed-depth matrix operations (efficiently handled by BLAS libraries) and OMP's iterative greedy selection (slow Python loops). The FLOP analysis shows LISTA actually requires 2.3× more FLOPs than OMP.
**Why it matters**: Presenting a software implementation artifact as a speedup is misleading. The speedup would not exist in optimized C/C++ implementations, where OMP's iterative operations can be efficiently compiled. The paper's own FLOP analysis contradicts the speedup claim.
**Suggestion**: Replace the "33× speedup" framing with: "LISTA's fixed-depth feedforward architecture enables more efficient software implementation than OMP's iterative structure, as reflected in the Python benchmark (0.21 vs 6.91 ms). However, LISTA requires 2.3× more FLOPs, indicating that the speedup is an implementation efficiency gain, not an algorithmic advantage."
**Severity**: Major

### W3: Pipelining Analysis Ignores Critical Practical Factors
**Problem**: The 20-stage pipelining analysis (Section 4.13.2) assumes ideal conditions: "64 parallel DSP units at 500 MHz," no memory bandwidth contention, no pipeline stalls, no inter-layer data dependencies. In practice, each pipeline stage requires reading W^(k) from memory (16 KB), and with 20 stages active simultaneously, the total working set is 20 × 16 KB = 320 KB of weight matrices plus intermediate activations.
**Why it matters**: Real FPGA implementations face memory bandwidth limitations that can significantly reduce throughput. The paper's theoretical 1.2 μs throughput assumes all data is available when needed, which may not hold in practice.
**Suggestion**: Add a brief discussion of memory bandwidth requirements for the pipelined architecture. Specifically, estimate the memory bandwidth needed to sustain 1.2 μs throughput and compare it to typical FPGA memory bandwidth. If the bandwidth requirement exceeds typical capabilities, acknowledge this as a limitation.
**Severity**: Major

### W4: Comparison with Wei et al. (2022) is Superficial
**Problem**: The paper cites Wei et al. (2022) who demonstrated < 10 μs LISTA latency on FPGA, and states that the theoretical estimates are "consistent with" this result. However, the paper does not provide a detailed comparison: what FPGA was used? What clock frequency? How many DSP units? What was the channel configuration?
**Why it matters**: Without a detailed comparison, the reader cannot assess whether the theoretical estimates are realistic or optimistic.
**Suggestion**: Provide a brief comparison table showing Wei et al.'s measured parameters alongside the paper's theoretical estimates. If the parameters differ significantly, discuss the implications.
**Severity**: Minor

### W5: Power Consumption Analysis is Missing
**Problem**: The paper does not discuss power consumption, which is a critical consideration for hardware deployment. LISTA's 20-stage pipeline with 64 DSP units would consume significant dynamic power due to the continuous data flow.
**Why it matters**: For mobile and embedded applications (the paper's target deployment scenarios), power consumption is often the binding constraint, not latency.
**Suggestion**: Add a brief theoretical power estimate based on the FLOP count and typical FPGA power per FLOP. Even a rough estimate would be useful.
**Severity**: Minor

---

## Detailed Comments

### Hardware Complexity Analysis (Section 4.13)
- FLOPs comparison (Table 14): Straightforward but useful. The 760K vs 332K comparison is clear.
- Parallelism characteristics (Section 4.13.2): The intra-layer parallelism analysis is correct. The batch parallelism point is valid. The pipeline analysis is theoretically sound but unvalidated.
- Memory access patterns (Section 4.13.3): The L2 cache analysis is useful. The comparison with OMP's irregular access patterns is informative.
- Hardware timing estimates (Section 4.13.4): The 23 μs sequential latency and 1.2 μs pipelined throughput are theoretical. The comparison with Wei et al. (2022) is superficial.
- Scaling analysis (Table 17): Useful for understanding the N² bottleneck.

### Python Runtime Comparison (Section 4.7.1)
- Table 4 (runtime): The 33× speedup is a Python artifact. The paper should reframe this more carefully.
- The caveat paragraph is good but should be more prominent.

### Deployment Recommendations (Section 5.3)
- The recommendation framework is actionable but should lead with LISTA's limitations.
- The statement "LISTA's fixed-depth feedforward architecture theoretically enables hardware throughput advantage over OMP via pipelining" is overly optimistic without measured validation.

---

## Questions for Authors

1. Have you considered implementing a minimal FPGA prototype (even on a low-cost board like Xilinx Artix-7) to validate the theoretical timing estimates? Even a non-optimized implementation would provide valuable data.

2. For the pipelined architecture, what is the estimated memory bandwidth requirement to sustain 1.2 μs throughput? Does this exceed typical FPGA memory bandwidth capabilities?

3. The paper states that LISTA's parameters (328 KB for N=64) "fit in L2 cache." For the pipelined architecture with 20 active stages, what is the total working set size? Does it still fit in L2 cache?

4. Have you estimated the power consumption of the pipelined LISTA architecture? How does it compare to OMP's power consumption?

---

## Minor Issues

### Hardware Claims
- The paper should consistently use "theoretical" or "estimated" before all hardware numbers, not just in caveats.
- Table 14 (FLOPs) should include a footnote stating that these are theoretical counts, not measured values.

### References
- The paper cites [wei2022fpga] and [chen2022survey] for hardware results. Verify these references are correctly characterized.

### Figures
- No hardware-related figures are provided. A block diagram of the pipelined architecture would be helpful.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 50 | Weak | No hardware implementation. Theoretical analysis is trivial. |
| Methodological Rigor (25%) | 60 | Adequate | FLOP analysis is correct. Pipelining analysis makes unvalidated assumptions. |
| Evidence Sufficiency (25%) | 45 | Weak | No measured hardware results. All claims are theoretical. |
| Argument Coherence (15%) | 75 | Strong | Logical flow from FLOPs → parallelism → pipelining. Consistent hedging. |
| Writing Quality (15%) | 80 | Strong | Clear, professional, well-caveated. |
| Significance & Impact | 55 | Weak | Hardware section provides no empirical contribution. Theoretical estimates are useful but not novel. |
| **Weighted Average** | **61** | **Major Revision** | Hardware claims lack measured validation. Section is too long for unvalidated theoretical estimates. |
