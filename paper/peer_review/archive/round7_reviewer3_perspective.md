# Peer Review Report — Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 7

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Cross-disciplinary Perspective)

### Reviewer Identity
Dr. Hiroshi Tanaka, Senior Research Engineer at a major telecommunications equipment manufacturer. 12+ years experience in FPGA/ASIC implementation of signal processing algorithms, hardware-software co-design, and real-time通信系统. Holds 8 patents on hardware-accelerated sparse recovery.

### Review Focus
Practical deployability, hardware complexity claims validity, real-world applicability, and the gap between theoretical analysis and measured implementation results.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
4 — Hardware implementation is my core expertise. I am very confident in assessing the hardware claims. Less confident in the pure signal processing aspects (NMSE/BER analysis), which I defer to other reviewers.

### Summary Assessment
This paper presents a comprehensive empirical analysis of LISTA for sparse channel estimation. The BER-NMSE disconnect analysis is novel and practically valuable. The ablation study is rigorous. However, from a practical deployment perspective, the paper has a fundamental issue: the hardware throughput claims (4.4× over OMP, 1.2 μs pipeline) are entirely theoretical, based on FLOP counts and pipeline analysis without any measured FPGA/ASIC results. The paper acknowledges this repeatedly but still presents these numbers prominently in the abstract and highlights. As someone who has implemented LISTA on FPGA, I know that the gap between theoretical FLOP analysis and measured performance can be 5-10× due to memory bandwidth, pipeline stalls, and control overhead. The paper's hardware analysis omits critical implementation details (memory bandwidth requirements, pipeline hazard analysis, fixed-point quantization effects). I recommend Major Revision to either provide measured FPGA results or significantly downgrade the hardware claims.

---

## Strengths

### S1: BER-NMSE Disconnect is Practically Valuable
The finding that LISTA's NMSE gap does not translate to BER penalty under MMSE equalization (Section 4.10) is genuinely useful for system designers. The mechanism analysis—error concentration on true taps reducing noise enhancement—provides actionable insight. This is the paper's strongest practical contribution.

### S2: SNR-Specific Training Finding is Deployable
The 6 dB improvement from SNR-specific training (Section 4.9) is a practical finding that can be immediately applied in deployment. The recommendation to train on a narrow SNR range around the operating point is clear and actionable.

### S3: Parameter Count Analysis is Useful
The 82K parameter count (328 KB) for N=64, L=20 is a useful data point for hardware designers. The observation that this fits in L2 cache is relevant for CPU/GPU deployment. The scaling analysis (Table 15) showing O(N²) growth is important for understanding scalability limits.

### S4: LISTA-CP Diagnostic Provides Implementation Insight
The finding that weight clipping is never activated (max spectral norm = 0.34) is useful for hardware implementers—it means the convergence constraint can be safely ignored in practice, simplifying the implementation.

---

## Weaknesses

### W1: Hardware Throughput Claims Are Entirely Theoretical
**Problem**: The paper claims "4.4× throughput advantage over OMP via 20-stage pipelining (estimated 1.2 μs on FPGA)" based on theoretical FLOP counts and pipeline analysis. No measured FPGA/ASIC results are provided. The 33× Python speedup is cited as supporting evidence but reflects interpreter overhead, not hardware capability.
**Why it matters**: As someone who has implemented LISTA on FPGA, I can attest that theoretical FLOP analysis significantly underestimates actual latency. Critical factors omitted include: (1) memory bandwidth for loading W^(k) matrices (16 KB each, 20 layers = 320 KB per estimate), (2) pipeline stalls from data dependencies between layers, (3) fixed-point quantization effects on NMSE, (4) control logic overhead for the soft-thresholding operation, (5) FFT/IFFT latency for the gradient computation. The actual throughput advantage is likely 1.5-2.5×, not 4.4×.
**Suggestion**: Either (a) provide measured FPGA results (even for a single configuration), or (b) significantly downgrade the hardware claims. Replace "4.4× throughput advantage" with "theoretical analysis suggests potential throughput improvement" and remove the 1.2 μs estimate. The 33× Python speedup should be removed from the highlights entirely.
**Severity**: Critical

### W2: No Fixed-Point Analysis
**Problem**: The paper assumes floating-point (float32) arithmetic throughout. Real FPGA implementations use fixed-point (typically 12-16 bits) to reduce resource utilization. The paper does not analyze how fixed-point quantization affects LISTA's NMSE or BER.
**Why it matters**: LISTA's soft-thresholding operation is sensitive to quantization—the learnable thresholds θ^(k) are small values (typically 0.01-0.1) that may be poorly represented in 12-bit fixed-point. The W^(k) matrices (4096 elements each) also require careful quantization to avoid overflow.
**Suggestion**: Add a fixed-point simulation study (12-bit, 16-bit) showing NMSE degradation. This is essential for any hardware deployment claim.
**Severity**: Major

### W3: Memory Bandwidth Analysis is Missing
**Problem**: The paper claims "82K parameters fit in L2 cache" (328 KB) but does not analyze the memory bandwidth requirements. Each LISTA layer requires loading W^(k) (16 KB), computing Xh and X^Tr (each requiring access to the M×N convolution matrix), and storing the intermediate result.
**Why it matters**: For a 20-stage pipeline, the memory bandwidth requirement is the bottleneck, not the compute. At 500 MHz with 64 DSP units, the compute throughput is 32 GFLOPS, but the memory bandwidth for loading W^(k) + convolution matrix at each stage is ~20 GB/s—exceeding the bandwidth of most mid-range FPGAs.
**Suggestion**: Add a memory bandwidth analysis showing the bandwidth requirements for the pipelined architecture. Compare with typical FPGA memory bandwidth (e.g., DDR4: 25.6 GB/s, HBM2: 460 GB/s).
**Severity**: Major

### W4: Pipeline Hazard Analysis is Missing
**Problem**: The paper assumes a 20-stage pipeline with no stalls. However, LISTA's architecture has data dependencies between layers: layer k+1 cannot begin until layer k produces its output. This creates a pipeline startup latency of 20 × (per-layer latency) before the pipeline is full.
**Why it matters**: For single-sample latency, the pipeline startup dominates. The 1.2 μs throughput estimate only applies to the steady-state, not to single-sample latency. For real-time applications (e.g., 5G NR with 1 ms slot duration), the startup latency matters.
**Suggestion**: Report both throughput (steady-state) and latency (single-sample) separately. The latency is 20 × 576 clocks = 23 μs, which the paper mentions but does not emphasize.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is appropriate. Abstract is too long and contains excessive hardware claims without qualification.

### Introduction
- Contribution #6 (hardware complexity) is overstated. Theoretical FLOP analysis is not "hardware complexity analysis"—it's computational complexity analysis. True hardware complexity includes memory, bandwidth, and control overhead.

### Methodology (Section 3)
- The LISTA architecture description is clear. The FFT-based convolution (Eq. 8) is a practical optimization.
- The parameter analysis (N_params = 82K) is correct and useful.

### Experiments (Section 4)
- **Experiment 7 (Practical Deployment)**: The runtime comparison (Table 7) is useful but the caveat about Python overhead is insufficient. The 33× speedup should not be presented as a primary result.
- **Experiment 13 (Hardware)**: The FLOPs comparison (Table 13) is correct but misleading. LISTA's 760K FLOPs vs OMP's 332K FLOPs does not translate to 2.3× latency difference because the operations have different parallelism characteristics. The pipeline analysis (Section 4.13.4) assumes ideal conditions.
- **Scaling Analysis (Table 15)**: The O(N²) scaling is correctly identified as a bottleneck. The recommendation for structured linear mappings is appropriate.

### Discussion
- Section 5.3 (Generalization and Practical Deployment) provides a reasonable decision framework but overstates the hardware evidence.
- Section 5.4 (Limitations) honestly acknowledges that hardware estimates are theoretical.

### References
- Good coverage of hardware implementation literature (Kim 2021, Wei 2022, Chen 2022). The Wei 2022 FPGA reference is the most relevant—did the authors contact Wei et al. for measured data?

---

## Questions for Authors

1. Have you contacted Wei et al. (2022) to obtain measured FPGA data for LISTA? Their <10 μs latency result would be directly comparable to your 23 μs sequential / 1.2 μs pipeline estimates.

2. What is the expected NMSE degradation when using 12-bit or 16-bit fixed-point arithmetic instead of float32? This is critical for FPGA deployment.

3. For the 20-stage pipeline, what is the total FPGA resource utilization (LUTs, FFs, DSP blocks, BRAM)? This determines whether the design fits on a mid-range FPGA (e.g., Xilinx Zynq UltraScale+).

---

## Minor Issues

### Hardware Claims
- Remove "33× faster in Python" from the abstract highlights—this is misleading
- Replace "4.4× throughput advantage" with "theoretical analysis suggests potential throughput improvement"
- Add "measured FPGA/ASIC results remain future work" to every hardware claim, not just the conclusion

### Figures and Tables
- Table 7 (runtime): Add a column for "Theoretical FLOPs" to help readers understand the relationship between FLOPs and measured time
- Table 13 (FLOPs): Add a column for "Memory Access" to highlight the bandwidth difference

### Practical Deployment
- The decision framework (Section 5.3) is useful but should be more conservative about hardware claims
- Consider adding a "Deployment Readiness" table showing what has been measured vs. what is theoretical

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 64 | Adequate | BER-NMSE mechanism is novel; LISTA application is incremental |
| Methodological Rigor (25%) | 68 | Adequate | Good NMSE/BER analysis, but hardware claims lack measured data |
| Evidence Sufficiency (25%) | 62 | Adequate | Comprehensive experiments but hardware evidence is theoretical |
| Argument Coherence (15%) | 78 | Strong | Clear logical flow, honest limitations |
| Writing Quality (15%) | 76 | Strong | Well-written, some verbosity |
| Significance & Impact | 66 | Adequate | Practical value limited by theoretical hardware claims |
| **Weighted Average** | **67.2** | **Minor Revision** | (Note: hardware concerns push toward Major) |
