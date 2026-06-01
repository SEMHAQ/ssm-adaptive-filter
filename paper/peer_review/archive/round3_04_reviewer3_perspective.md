# Peer Review Report — Reviewer 3 (Perspective / Cross-Disciplinary)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 3

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-Disciplinary Perspective

### Reviewer Identity
Dr. Sarah Kim, Senior Research Engineer, Qualcomm Research (Machine Learning for Wireless). Expertise in hardware-efficient ML architectures for communications, FPGA/ASIC deployment of neural networks, and real-time signal processing systems. Focus: practical deployability, hardware implications, cross-disciplinary connections, and whether the findings translate to real systems.

### Review Focus
Practical deployment feasibility, hardware implementation considerations, cross-disciplinary connections (ML systems ↔ communications), and whether the paper's findings have real-world impact beyond the simulation environment.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — Hardware deployment of ML for communications is my core expertise. I am confident in my assessment of practical feasibility and deployment implications.

### Summary Assessment
This manuscript evaluates LISTA for sparse channel estimation with a focus on practical deployment. The 33× speedup over OMP (Table 6) and the 82K parameter count are compelling for resource-constrained deployments. The BER analysis adds significant practical value. However, the speed comparison is Python-only and may not reflect hardware reality. The paper lacks any hardware deployment results (FPGA, ASIC, or even optimized C/C++), which is a significant gap given the emphasis on "practical deployment." The N=256 divergence and the O(N²) scalability concern are important limitations that need more discussion. Despite these gaps, the paper provides useful insights for the communications ML community and is suitable for DSP with minor revisions.

---

## Strengths

### S1: BER Analysis Bridges the Theory-Practice Gap
The BER simulation (Section 4.10) is the paper's most practically relevant contribution. In industry, NMSE is an intermediate metric—BER is what matters. The finding that LISTA achieves competitive BER despite worse NMSE is exactly the kind of insight that engineers need. The use of both QPSK and 16-QAM is appropriate (QPSK for robustness, 16-QAM for sensitivity to estimation errors).

### S2: Practical Parameter Count and Inference Time
The paper provides concrete deployment numbers: 82K parameters, 0.21 ms CPU inference. These are modest and feasible for FPGA deployment. The comparison with Wei et al. (2022) who achieved <10 μs FPGA latency for LISTA is encouraging. The authors correctly note that the relative speed advantage is expected to be preserved in hardware.

### S3: SNR-Specific Training as a Practical Mitigation
The SNR-specific training results (Section 4.9) provide a practical engineering solution to the saturation problem. The finding that narrow-range training [15, 25] dB improves NMSE by ~6 dB is actionable: if the operating SNR is known, this is a simple and effective mitigation. The decision framework in Section 5.2 is useful for practitioners.

### S4: LISTA-CP Diagnostic Analysis Informs Architecture Choice
The finding that LISTA-CP's convergence guarantees don't improve performance (because weight clipping is naturally satisfied) saves practitioners from unnecessary complexity. This is a useful negative result that prevents wasted engineering effort.

---

## Weaknesses

### W1: Speed Comparison is Python-Only — No Hardware Evidence
**Problem**: The 33× speedup (0.21 ms vs 6.91 ms) is measured in Python on a single CPU core. The paper acknowledges this caveat but the entire "practical deployment" narrative hinges on this number. No C/C++, FPGA, or ASIC measurements are provided. Python implementations are notoriously poor predictors of relative hardware performance due to interpreter overhead, memory allocation patterns, and library optimization differences.

**Why it matters**: The paper's central practical claim—"33× faster inference"—may not hold in optimized implementations. OMP in optimized C++ with BLAS may be much faster relative to LISTA than the Python comparison suggests.

**Suggestion**: (1) At minimum, provide C/C++ timing with optimized BLAS for both methods. (2) Ideally, provide a rough FPGA resource estimate (LUTs, DSP slices, latency) based on the architecture parameters. (3) If hardware results are not feasible, provide a theoretical hardware complexity analysis comparing the two methods' parallelism characteristics.

**Severity**: Major

### W2: O(N²) Scalability Not Adequately Discussed
**Problem**: The paper identifies that W^(k) has O(N²) parameters per layer, giving 1.3M parameters at N=256. The N=256 experiment diverges (all seeds). The paper briefly mentions "structured linear mappings" as a future direction but does not analyze the scalability implications.

**Why it matters**: Many practical channels have N > 64 (e.g., wideband OFDM with N=512 or 1024). If LISTA cannot scale beyond N=128, its practical applicability is severely limited.

**Suggestion**: (1) Analyze the theoretical complexity of structured alternatives (Toeplitz, circulant, low-rank) for W^(k). (2) If feasible, provide a brief experiment with a structured W^(k) at N=128 or 256. (3) Discuss the parameter-performance trade-off explicitly.

**Severity**: Major

### W3: No Discussion of Online/Incremental Deployment
**Problem**: The paper evaluates LISTA in a batch setting (train once, deploy statically). In real wireless systems, channels change over time and models may need periodic retraining or adaptation. The paper does not discuss: (a) how often LISTA needs retraining, (b) the cost of retraining, (c) whether LISTA can be fine-tuned incrementally.

**Why it matters**: LMS/NLMS adapt online; OMP/LASSO require no training. LISTA's deployment cost includes not just inference but also the training pipeline. For rapidly changing channels, this cost may be prohibitive.

**Suggestion**: Add a brief discussion (even qualitative) of: (1) retraining frequency requirements, (2) whether transfer learning or fine-tuning can reduce retraining cost, (3) the trade-off between LISTA's inference speed advantage and its training overhead.

**Severity**: Minor

### W4: Equalization Method is Simplistic
**Problem**: The BER simulation uses only zero-forcing (ZF) equalization. Modern communication systems use MMSE, decision-feedback equalization, or iterative receivers. ZF is known to amplify noise at low SNR, which may affect the LISTA vs. OMP comparison differently than MMSE would.

**Why it matters**: If the BER advantage only holds for ZF, the practical relevance is limited for modern systems.

**Suggestion**: Add MMSE equalization results. If the finding holds, it strengthens the paper. If not, discuss the limitation.

**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title correctly signals an "analysis" paper. Good.
- Abstract highlights the 33× speedup and 82K parameters—both are practical metrics that industry readers care about.

### Introduction
- The motivation is clear and the practical framing is appropriate.
- Contribution 6 (practical deployment) could be strengthened with more concrete hardware numbers.

### Literature Review
- The hardware deployment references (Wei et al., Kim et al., Chen et al.) are relevant and well-integrated.
- The comparison with CNN/Transformer methods is informative but lacks experimental validation.

### Methodology
- The experimental setup is well-specified and reproducible.
- The use of mixed-SNR training is a good engineering choice.

### Results
- Table 6 (runtime): The speedup numbers are compelling but Python-only.
- Table 7 (ITU): Encouraging generalization results.
- Tables 10–11 (BER): The most practically relevant results.

### Discussion
- Section 5.2 (deployment recommendations) is the highlight for practitioners.
- The future directions (FPGA/ASIC, MMSE equalization, MIMO) are all relevant.

### Conclusion
- The conclusion accurately summarizes the findings. The "speed-critical deployments" framing is appropriate.

---

## Questions for Authors

1. **Hardware timing**: Can you provide C/C++ timing or a theoretical hardware complexity analysis to substantiate the 33× speedup claim?

2. **Scalability**: What is the largest channel length N for which LISTA can be successfully trained with M/N ≥ 2? Can structured W^(k) matrices extend this range?

3. **Retraining cost**: In a practical deployment, how often would LISTA need retraining for time-varying channels? What is the training time relative to the inference time?

4. **MMSE equalization**: Does the BER advantage hold with MMSE equalization?

---

## Minor Issues

### Language / Grammar
- Section 4.7.2: "cross-distribution generalization" — consider clarifying that this means training on Gaussian, testing on ITU.
- Section 5.2: The numbered deployment recommendations are clear and actionable.

### Figures and Tables
- Table 6: Consider adding a "theoretical speedup" column based on operation counts, independent of Python implementation.
- Table 7: Only one SNR point for ITU. Add at least SNR=10 for context.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 50 | Weak | BER finding is novel; overall contribution is analysis |
| Methodological Rigor (25%) | 70 | Adequate | Good experiments; hardware claims unsupported |
| Evidence Sufficiency (25%) | 64 | Adequate | Comprehensive NMSE; BER and hardware evidence insufficient |
| Argument Coherence (15%) | 68 | Adequate | Clear structure; practical claims need more support |
| Writing Quality (15%) | 74 | Strong | Clear, practical framing, honest limitations |
| Significance & Impact | 62 | Adequate | Practical value is real but limited by Python-only evidence |
| **Weighted Average** | **65.0** | **Minor Revision** | |
