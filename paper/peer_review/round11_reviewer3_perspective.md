# Perspective Review Report (Peer Reviewer 3)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 11

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Perspective)

### Reviewer Identity
Dr. Sarah Okonkwo, Research Scientist in Machine Learning Systems, specializing in hardware-efficient neural network architectures and model compression. Experience in FPGA acceleration and edge computing deployment.

### Review Focus
Cross-disciplinary connections between algorithmic research and hardware implementation, practical deployment feasibility, and systems-level implications.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
**4** — High confidence on hardware and systems aspects; moderate on pure signal processing theory.

### Summary Assessment

This paper provides a comprehensive analysis of LISTA for sparse channel estimation, with particular strength in the BER mechanism analysis and ablation studies. From a systems perspective, the paper's most valuable contribution is the practical deployment guidance (Section 4.7) and the honest assessment of hardware complexity.

However, the hardware throughput claims warrant careful scrutiny. The paper repeatedly mentions "potential for hardware throughput advantage via pipelining" while acknowledging that all hardware estimates are theoretical. From my experience deploying neural networks on FPGAs, the gap between theoretical FLOP analysis and measured hardware performance is often 5–10× due to memory bandwidth, data movement, and control overhead. The paper's hardware claims, while hedged, may create unrealistic expectations.

The cross-disciplinary connection to the neural architecture search (NAS) and hardware-aware optimization communities is largely unexplored. LISTA's fixed-depth feedforward architecture is precisely the type of network that benefits from hardware-aware design, and the paper could strengthen its contribution by connecting to this literature.

---

## Strengths

### S1: Honest Assessment of Hardware Complexity
The paper explicitly states: "The FLOP count (760K vs 332K) shows LISTA requires 2.3× more computation per estimate" (Section 4.7). This honesty about LISTA being more computationally expensive per estimate, while arguing for pipelined throughput, is commendable and rare in the deep learning literature.

### S2: Practical Deployment Framework
Section 4.7 provides a clear decision framework: "Use LISTA for throughput, OMP for accuracy" (Section 4.7). The recommendation to use SNR-specific training when the operating SNR is known is actionable and practical.

### S3: Error Concentration Mechanism has Systems Implications
The finding that LISTA concentrates error on true taps (Section 4.12) has practical implications beyond BER: it suggests that LISTA's estimates are "compatible" with equalization algorithms that expect sparse channels, potentially simplifying receiver design.

### S4: Scalability Analysis
Table 13 (scaling with N) is valuable for systems designers. The identification of O(N²) as the bottleneck and the suggestion of structured linear mappings shows awareness of practical constraints.

---

## Weaknesses

### W1: Hardware Throughput Claims Need Stronger Caveats
**Problem**: The abstract states "theoretical pipeline analysis suggesting potential for hardware throughput advantage over OMP" and the highlights mention "20-stage pipelining suggests potential for hardware throughput advantage." While caveats are present ("subject to implementation-dependent factors"), the abstract/highlights position creates an impression of demonstrated hardware advantage.
**Why it matters**: In my experience, the gap between theoretical FLOP analysis and measured FPGA/ASIC performance is substantial. Memory bandwidth, data movement, control logic, and clock frequency often dominate over raw FLOP count. A 20-stage pipeline with 82K parameters requires significant on-chip memory, which may not be available on resource-constrained FPGAs.
**Suggestion**: (a) Remove hardware throughput claims from the abstract and highlights, discussing them only in Section 4.13; (b) add a paragraph acknowledging the gap between theoretical FLOP analysis and measured hardware performance; (c) cite Wei et al. (2022) more prominently as evidence that LISTA can be implemented on FPGA, while noting that throughput comparison with OMP requires matched implementation.
**Severity**: Major

### W2: Missing Connection to Hardware-Aware Neural Architecture Design
**Problem**: The paper does not connect to the hardware-aware NAS and model compression literature. LISTA's fixed-depth feedforward architecture is precisely the type of network that benefits from hardware-aware design (e.g., quantization-aware training, structured pruning, operator fusion).
**Why it matters**: The DSP readership includes researchers working on hardware implementation. Connecting to this literature would broaden the paper's impact.
**Suggestion**: Add a paragraph in Section 5.4 (Future Work) discussing how techniques from hardware-aware NAS (e.g., MCUNet, TinyML) could be applied to LISTA deployment.
**Severity**: Minor

### W3: Parameter Count vs. Practical Memory
**Problem**: The paper reports 82K parameters for L = 20, N = 64 (Section 3.4) but does not discuss the practical memory implications. In FPGA deployment, each parameter requires storage, and 82K × 32-bit = 328 KB, which is significant for small FPGAs.
**Why it matters**: Memory constraints often dominate FLOP constraints in hardware deployment.
**Suggestion**: Add a brief discussion of memory requirements and potential quantization strategies (e.g., 8-bit or 16-bit quantization) in Section 4.13.
**Severity**: Minor

### W4: Python Benchmark Interpretation
**Problem**: The paper reports LISTA inference at 0.21 ms vs. OMP at 6.91 ms (Table 7), a 33× speedup, but then correctly notes this is "a software implementation artifact" due to BLAS optimization. However, this number may still mislead readers who skim the paper.
**Why it matters**: The 33× speedup claim is likely to be cited out of context, despite the paper's caveats.
**Suggestion**: Consider removing the Python inference time comparison entirely, or replacing it with a more meaningful metric (e.g., FLOP-normalized throughput).
**Severity**: Minor

---

## Detailed Comments

### Assumption Audit
- **Explicit assumptions**: The paper assumes i.i.d. Gaussian tap amplitudes, BPSK pilots, and AWGN noise. These are standard and appropriate for the analysis.
- **Implicit assumptions**: The paper implicitly assumes that the training distribution (mixed SNR) is representative of deployment conditions. This is addressed in the generalization experiments but could be discussed more explicitly.
- **Paradigmatic assumptions**: The paper assumes that NMSE is a meaningful metric for channel estimation quality. The BER analysis (Section 4.10) challenges this assumption by showing that NMSE does not directly predict BER, which is a valuable paradigmatic insight.

### Cross-Disciplinary Connections
- **Parallel research**: The hardware-aware NAS community (MCUNet, TinyML) faces similar challenges in deploying learned algorithms on resource-constrained platforms. The paper could benefit from this connection.
- **Borrowing opportunities**: Quantization-aware training, a technique from the model compression literature, could be applied to LISTA to reduce memory requirements.
- **Methodological borrowing**: The paper's ablation methodology (20 seeds, paired t-tests, Cohen's d) could serve as a model for other deep unfolding studies.

### Practical Impact
- **Real-world application**: The paper's deployment recommendations (SNR-specific training, LISTA/OMP fallback) are practical and actionable.
- **Implementation feasibility**: The 82K parameter count is feasible for FPGA deployment, but the O(N²) scaling limits applicability to N > 128 without structured mappings.
- **Stakeholders**: The paper primarily addresses algorithm designers and communication systems engineers. Hardware designers are acknowledged but not fully engaged.

### Broader Implications
- **Ethical dimensions**: No significant ethical concerns. The technology is for physical layer communications and does not raise privacy or fairness issues.
- **Social impact**: Improved channel estimation could improve wireless connectivity in underserved areas, but this is not discussed.
- **Future directions**: The most valuable follow-up would be measured FPGA/ASIC results comparing LISTA and OMP throughput under matched conditions.

---

## Cross-Disciplinary Reading Recommendations

1. **Lin, J., et al. (2021). MCUNet: Tiny Deep Learning on IoT Devices. *Neural Information Processing Systems*.** — Demonstrates hardware-aware design for deploying neural networks on microcontrollers. Relevant to LISTA deployment on resource-constrained platforms.
2. **Wang, K., et al. (2020). HAQ: Hardware-Aware Automated Quantization. *CVPR*.** — Quantization strategies for hardware deployment. Could be applied to LISTA's W^(k) matrices.
3. **Balatsoukas-Stimming, A., & Studer, C. (2019). Deep Unfolding for Communications Systems. *IEEE SiPS*.** — FPGA implementation of deep unfolding networks. Directly relevant to the hardware claims.
4. **Han, S., et al. (2016). Deep Compression. *ICLR*.** — Model compression techniques (pruning, quantization, Huffman coding) applicable to LISTA deployment.

---

## Questions for Authors

1. The paper claims "20-stage pipelining could enable hardware throughput advantage" (Section 4.13). Have you estimated the on-chip memory required for a 20-stage pipeline with 82K parameters? This would help assess practical feasibility.
2. For the SNR-specific training (Section 4.9), the improvement is 6 dB. In a practical system where the SNR varies within a 10 dB range, would you recommend training on the full range or using multiple SNR-specific models with a switching mechanism?
3. The error concentration mechanism (Section 4.12) is analyzed for i.i.d. Gaussian and ITU channels. Have you investigated whether the mechanism holds for channels with different sparsity structures (e.g., block-sparse channels)?

---

## Minor Issues

### Figures and Tables
- Table 13 (scaling analysis) would benefit from a column showing the memory requirement in KB or MB.
- The hardware complexity discussion (Section 4.13) would benefit from a figure showing the pipeline architecture.

### Layout
- The highlights section mentions "hardware throughput advantage" — consider rewording to "potential for hardware throughput advantage (theoretical analysis, measured validation remains future work)."
