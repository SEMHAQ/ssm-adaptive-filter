# Peer Review Report — Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-ROUND17
- **Review Date**: 2026-06-01
- **Review Round**: Round 17

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-Disciplinary Perspective

### Reviewer Identity
Dr. Sarah Chen, Senior Research Scientist at Nokia Bell Labs. Expertise spans hardware implementation of signal processing algorithms, FPGA/ASIC design for wireless communications, and practical deployment of machine learning at the physical layer. Brings a systems-level perspective: how do algorithmic choices translate to hardware cost, latency, and power consumption?

### Review Focus
Practical deployment implications, hardware feasibility, cross-disciplinary connections (signal processing ↔ hardware design ↔ machine learning), and the paper's relevance to real-world communication systems.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Accept**
- [ ] **Reject**

### Confidence Score
4 — Hardware deployment and practical systems are my expertise; the deep unfolding theory is partially outside my core area.

### Summary Assessment
This paper provides a valuable systems-level analysis of LISTA for channel estimation, with particular strength in the BER analysis, practical deployment recommendations, and honest assessment of hardware complexity. The error concentration mechanism has practical relevance for ZF equalization in low-complexity receivers. The paper's recommendation framework (Section 5.3) is actionable for practitioners. However, the hardware complexity analysis is entirely theoretical (FLOP counts) with no measured results, and the claim about "pipelined throughput" advantage is explicitly acknowledged as unvalidated. The paper would benefit from a more honest framing of the hardware contribution and a discussion of alternative deployment strategies (e.g., quantized LISTA, pruning).

---

## Strengths

### S1: Practical Deployment Decision Framework
Section 5.3 provides a clear, actionable decision framework for practitioners: (1) throughput-critical → LISTA, (2) known SNR → SNR-specific training, (3) variable SNR → broad-range training, (4) NMSE-critical → OMP/FISTA. This framework directly addresses the "so what?" question and has immediate practical value.

### S2: BER Analysis with Realistic Modulations
The BER simulations (Section 4.11) use QPSK and 16-QAM—modulations relevant to practical systems. The MMSE vs. ZF comparison is well-motivated: MMSE convergence is expected (honestly noted), while ZF reveals the error structure advantage. The 16-QAM results (Table 11) demonstrate tangible BER improvement at SNR ≥ 15 dB, which is a practical operating range for many wireless systems.

### S3: Honest Hardware Complexity Assessment
The paper is commendably honest about the hardware analysis: "All hardware estimates below are derived from FLOP counting and analytical pipeline modeling; no measured FPGA/ASIC results are presented" (Section 4.14). The acknowledgment that "a fair hardware comparison would require implementing both algorithms on the same FPGA platform" is refreshing. The FLOP analysis (Table 13) correctly shows LISTA requires 2.3× more FLOPs than OMP, contradicting any claim of computational advantage.

### S4: ZF Equalization Justification
The discussion of when ZF equalization is relevant (Section 5.1) is well-reasoned. The three scenarios—low-complexity IoT receivers, unreliable noise variance estimation, and theoretical analysis—are practical and convincing. The framing of ZF as a "diagnostic tool for understanding error structure" is insightful.

### S5: ITU Channel Model Evaluation
Testing on ITU PedA and VehA channels (Section 4.7.2) demonstrates cross-distribution generalization. The finding that LISTA achieves −23 to −27 dB on ITU channels without channel-specific training is practically important, as it eliminates the need for channel-specific training data in deployment.

---

## Weaknesses

### W1: Hardware Analysis is Purely Theoretical
**Problem**: The hardware complexity analysis (Section 4.14) is entirely based on FLOP counting. The paper claims LISTA's "regular computation graph may facilitate hardware pipelining" but explicitly acknowledges this is "an unvalidated hypothesis." The reference to Wei et al. (2022) FPGA implementation is cited but not compared against OMP under identical conditions.
**Why it matters**: For *Digital Signal Processing* readers interested in hardware deployment, theoretical FLOP counts are insufficient. The pipelining advantage claim—central to the hardware argument—is unsubstantiated.
**Suggestion**: Either (a) add a brief FPGA implementation comparison (even a preliminary one), or (b) remove the pipelining claim from the abstract and conclusions, replacing it with a clear statement that hardware advantages are theoretical predictions requiring validation.
**Severity**: Major

### W2: Missing Quantization and Pruning Analysis
**Problem**: The paper does not discuss quantization or pruning of LISTA parameters, which are standard techniques for deploying neural networks on resource-constrained hardware. The 82K parameters could be significantly reduced through pruning, and the W^(k) matrices could be quantized to 8-bit or even 4-bit precision.
**Why it matters**: For practical FPGA/ASIC deployment, parameter quantization and pruning are essential for reducing memory footprint and computational cost. The paper's hardware analysis would be significantly strengthened by including these techniques.
**Suggestion**: Add a brief analysis of LISTA's robustness to parameter quantization (e.g., 8-bit, 4-bit). Even a simulation-based analysis would be valuable.
**Severity**: Minor

### W3: No Comparison with Lightweight Deep Learning Methods
**Problem**: The paper compares against CNN (Section 4.10) but not against other lightweight deep learning methods suitable for hardware deployment, such as binary neural networks, knowledge distillation, or neural architecture search (NAS) optimized models.
**Why it matters**: Practitioners choosing between LISTA and other deep learning approaches need to know how LISTA compares against hardware-optimized alternatives.
**Suggestion**: Add a brief discussion of how LISTA's hardware characteristics compare against lightweight deep learning alternatives. A full comparison is not required, but a qualitative discussion would be valuable.
**Severity**: Minor

### W4: Scalability Discussion Lacks Concrete Solutions
**Problem**: The paper identifies the O(N²) parameter scaling as a scalability limitation (N=256 diverges) and mentions "structured linear mappings (Toeplitz, circulant, low-rank)" as potential solutions. However, no concrete analysis or implementation is provided.
**Why it matters**: For wideband systems with N ≥ 128, the scalability limitation is a practical barrier. Without concrete solutions, the paper's applicability is limited to narrowband channels.
**Suggestion**: Provide parameter count estimates for structured mapping alternatives (e.g., Toeplitz: O(N) parameters per layer; low-rank: O(rN) parameters). Even without implementation, these estimates would help practitioners assess scalability.
**Severity**: Minor

### W5: Power Consumption Not Discussed
**Problem**: The paper discusses computational complexity (FLOPs) and inference time (Python benchmarks) but not power consumption, which is a critical constraint for battery-powered devices and base stations.
**Why it matters**: For practical deployment, power consumption often matters more than raw throughput. LISTA's fixed-depth architecture may have power advantages over iterative methods, but this is not discussed.
**Suggestion**: Add a brief discussion of expected power consumption characteristics, even if only at the theoretical level (e.g., energy per FLOP estimates).
**Severity**: Minor

---

## Detailed Comments

### Introduction
- The six contributions are clearly enumerated. The practical deployment contribution (item 6) is particularly relevant to my review focus.
- The statement "LISTA requires 2.3× more computation per estimate" (Section 1) is honest and important.

### Methodology
- The LISTA architecture (Section 3.3) is standard. The FFT-based convolution (Eq. 8) is a practical implementation choice.
- The parameter analysis (Section 3.4) correctly identifies the 82K parameter count and O(N²) scaling.

### Results
- Table 8 (runtime): The 33× Python speedup is correctly attributed to "software implementation artifact" rather than algorithmic advantage. This honesty is commendable.
- Table 13 (FLOPs): The 2.3× OMP disadvantage is clearly shown. The scaling from N=32 to N=256 is informative.
- Table 9 (SNR mitigation): The 6 dB improvement from SNR-specific training is practically valuable.

### Discussion
- Section 5.3 (deployment framework): Excellent practical guidance. The five-point decision framework is actionable.
- Section 5.1 (ZF relevance): Well-reasoned justification for the ZF analysis.
- Section 5.4 (limitations): Honest and comprehensive.

### Hardware Discussion
- The acknowledgment that "measured FPGA/ASIC latency, throughput, and power consumption remain future work" is appropriate.
- The reference to Wei et al. (2022) is relevant but the lack of OMP comparison is a gap.

---

## Questions for Authors

1. The paper claims LISTA's "regular computation graph may facilitate hardware pipelining" but acknowledges this is unvalidated. Can you provide a theoretical analysis of the pipeline depth and throughput for LISTA vs. OMP, even without FPGA implementation?

2. For the 82K parameters, what is the expected memory footprint at different quantization levels (32-bit, 16-bit, 8-bit)? This would help practitioners assess deployment feasibility.

3. The paper recommends LISTA for "throughput-critical applications" (Section 5.3). Given that LISTA requires 2.3× more FLOPs than OMP, under what conditions would LISTA's pipelining advantage overcome this per-estimate cost deficit?

4. For the complex-valued extension (Appendix A), the weight matrices double (real + imaginary). What is the total parameter count for the complex LISTA? Does this affect the hardware deployment recommendation?

---

## Minor Issues

### Language / Grammar
- Section 4.14, p. 15: "LISTA's regular computation graph may facilitate hardware pipelining" — "may" is appropriately hedged, but consider "has the potential to" for stronger academic register.

### Figures and Tables
- Table 8: The footnote about Python speedup being a "software implementation artifact" is important. Consider making this more prominent.
- Table 13: Consider adding a column for memory bandwidth requirements (bytes per estimate).

### Layout
- Section 4.14 could be expanded into a separate "Hardware Deployment Analysis" section for better visibility.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 64 | Adequate | Error concentration is novel; hardware analysis is standard |
| Methodological Rigor (25%) | 78 | Strong | Comprehensive experiments; hardware analysis is theoretical only |
| Evidence Sufficiency (25%) | 80 | Strong | Multiple experiments and baselines; hardware evidence is weak |
| Argument Coherence (15%) | 80 | Strong | Clear narrative; practical recommendations well-motivated |
| Writing Quality (15%) | 82 | Strong | Clear, professional; honest reporting |
| Significance & Impact | 72 | Adequate | Practical relevance clear but limited by NMSE gap and theoretical hardware analysis |
| **Weighted Average** | **76.0** | **Minor Revision** | |

---

*Report submitted by Reviewer 3 (Perspective)*
