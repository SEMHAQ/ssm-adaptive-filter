# Peer Review Report — Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 2

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Cross-Disciplinary Perspective)

### Reviewer Identity
Dr. Sofia Petrov, Senior Research Scientist, Nokia Bell Labs. Specialization: real-time signal processing for 5G/6G systems, hardware-efficient algorithms, FPGA/ASIC implementation of deep learning for physical layer. 15 years of industry experience deploying signal processing algorithms in commercial wireless systems. Reviewer for IEEE JSAC, IEEE COMST.

### Review Focus
Practical deployment feasibility, hardware implementation considerations, cross-disciplinary connections (ML systems, edge computing), and real-world applicability. I evaluate whether the paper's claims hold from an industry deployment perspective.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
4 — My expertise in hardware deployment and real-time signal processing gives me a strong perspective on the practical claims, though the theoretical compressed sensing aspects are slightly outside my primary domain.

### Summary Assessment
This paper evaluates LISTA for sparse channel estimation with a focus on practical deployment. From an industry perspective, the paper identifies the right trade-offs (speed vs. accuracy, training cost vs. inference cost) and provides useful benchmarks (33× speedup, 82K parameters, 0.21 ms inference). However, the paper falls short of the practical deployment story it aims to tell: (1) the 13-33 dB NMSE gap with OMP is likely unacceptable for commercial systems, (2) the missing BER analysis prevents assessment of system-level impact, (3) the O(N²) scalability concern is not addressed with practical solutions, and (4) the training infrastructure requirements are not discussed. The paper would benefit from an honest reframing: LISTA is useful as a fast initial estimate in a hybrid system, not as a standalone replacement for OMP. I recommend Major Revision.

---

## Strengths

### S1: Practical Inference Time Benchmarks
The inference time comparison (Table 6) is exactly what industry practitioners need. The 33× speedup over OMP (0.21 vs. 6.91 ms on CPU) and the 82K parameter count are concrete, actionable numbers. The comparison across different LISTA depths (L=5, 10, 20) provides a speed-accuracy trade-off curve that is useful for deployment decisions.

### S2: SNR-Specific Training as a Deployment Strategy
The SNR-specific training results (Table 8) provide a clear deployment recommendation: when the operating SNR is approximately known, narrow-range training improves NMSE by ~6 dB. This is a practical insight that directly translates to deployment decisions. The finding that the range width matters more than the exact location is also practically useful.

### S3: Cross-Distribution Generalization to ITU Channels
The ITU channel results (Table 6) are important for industry. The finding that Gaussian-trained LISTA generalizes to ITU channels without retraining eliminates a major deployment concern (needing channel-specific training data). The 4-5 dB gap with OMP on ITU channels is more acceptable than the 13-33 dB gap on Gaussian channels.

### S4: Honest Limitations Disclosure
The paper honestly discloses the saturation behavior, the divergence at N=256, and the instability at K=15. This transparency is appreciated and builds credibility with industry readers who need to assess deployment risks.

---

## Weaknesses

### W1: No System-Level Impact Assessment (BER, Throughput, Latency)
**Problem**: The paper evaluates NMSE in isolation. For industry deployment, what matters is the system-level impact: BER, throughput, and end-to-end latency. A 33× inference speedup is meaningless if the NMSE gap with OMP causes unacceptable BER degradation.
**Why it matters**: Industry decisions are made based on system-level metrics, not intermediate signal processing metrics. Without BER results, the paper cannot inform deployment decisions.
**Suggestion**: Add a system-level evaluation: BER vs. SNR for QPSK/16-QAM with MMSE equalization, using LISTA/OMP/LASSO-estimated channels. Include end-to-end latency (channel estimation + equalization + decoding). This would make the paper directly useful for industry.
**Severity**: Critical

### W2: O(N²) Scalability Not Addressed with Practical Solutions
**Problem**: The paper acknowledges that LISTA's W^(k) matrix has O(N²) parameters (Section 3.4) and that training diverges at N=256 (Table 3). However, no practical solution is proposed. For 5G NR with N=256-512, this is a blocking limitation.
**Why it matters**: Industry systems require scalability to larger channel lengths. Without a solution, LISTA is limited to small-scale channels.
**Suggestion**: Propose or evaluate structured linear mappings (e.g., Toeplitz, circulant, sparse) to reduce the O(N²) complexity. Alternatively, discuss the applicability of LISTA to sub-band processing where N is smaller.
**Severity**: Major

### W3: Training Infrastructure Requirements Not Discussed
**Problem**: The paper reports inference time but not training time, data generation cost, or infrastructure requirements. For industry, the total cost of ownership (training + deployment + maintenance) matters.
**Why it matters**: If LISTA requires days of GPU training and 10,000 samples, the cost may not justify the 33× inference speedup over OMP (which requires no training).
**Suggestion**: Report training time, data generation cost, and GPU requirements. Discuss whether the training overhead is justified for different deployment scenarios (one-time vs. frequent retraining).
**Severity**: Major

### W4: Hybrid LISTA/OMP Framework Only Described, Not Evaluated
**Problem**: Section 5.2 mentions a "hybrid LISTA/OMP fallback framework" but never evaluates it. This is the most promising deployment strategy (use LISTA for speed, fall back to OMP when accuracy is insufficient), but without experimental results, it remains a concept.
**Why it matters**: The hybrid approach could resolve the speed-accuracy trade-off. Without evaluation, the reader cannot assess its effectiveness.
**Suggestion**: Implement and evaluate the hybrid framework: use LISTA as an initial estimate, detect when the residual exceeds a threshold, and fall back to OMP. Report the speedup and accuracy trade-off.
**Severity**: Major

### W5: No Discussion of Real-Time Constraints and Latency Budgets
**Problem**: The paper reports 0.21 ms inference time but does not discuss real-time constraints. In 5G NR, the channel estimation latency budget is typically 0.1-1 ms depending on the slot structure. The paper does not discuss whether 0.21 ms fits within these budgets.
**Why it matters**: The practical utility of LISTA depends on whether its inference time fits within the system's latency budget. Without this context, the 0.21 ms number is uninterpretable.
**Suggestion**: Discuss the latency requirements for 5G NR and compare LISTA's inference time against these requirements. If GPU inference is used, discuss the additional latency of CPU-GPU data transfer.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title is appropriate. "Analysis of" correctly signals a characterization study.
- The abstract is clear and honest. The quantitative results are well-presented.

### Introduction
- The introduction correctly identifies the speed-accuracy trade-off as the key motivation.
- The five contributions are clearly stated but could be reorganized to lead with the most impactful findings.

### Literature Review / Theoretical Framework
- The literature review covers the compressed sensing and deep unfolding literature adequately.
- Missing: discussion of hardware implementation of deep unfolding (FPGA/ASIC), which is directly relevant to the deployment claims.

### Methodology / Research Design
- The experimental setup is standard and well-described.
- The mixed-SNR training protocol is practical and well-justified.
- The CPU inference time benchmarking is appropriate for comparison, though GPU benchmarking would also be useful.

### Results / Findings
- The SNR saturation (Table 1) is the key finding. The paper correctly identifies this as a limitation.
- The inference time comparison (Table 6) is the most practically useful result.
- The ITU channel results (Table 6) are important for generalization claims.
- The SNR-specific training (Table 8) provides actionable deployment guidance.

### Discussion
- Section 5.1's saturation explanation is plausible.
- Section 5.2's practical framework is useful but incomplete without BER and hybrid evaluation.
- Section 5.3's limitations are honestly stated.

### Conclusion
- The conclusion is appropriate. The positioning as "when speed is prioritized" is correct but needs BER evidence.

### References
- References are adequate. The inclusion of both theoretical and practical works is appropriate.

---

## Questions for Authors

1. **BER Impact**: Can you add BER simulations? From an industry perspective, this is the single most important missing piece.

2. **Hybrid Framework**: Can you evaluate the hybrid LISTA/OMP fallback framework? This seems like the most promising deployment strategy and deserves experimental validation.

3. **Training Cost**: What is the total training cost (time, data, GPU)? How does this compare against the lifetime inference savings from the 33× speedup?

4. **Scalability Solution**: Do you have any preliminary results on structured linear mappings (Toeplitz, circulant) to reduce the O(N²) complexity for larger N?

---

## Minor Issues

### Language / Grammar
- Overall writing quality is good. No significant issues.

### Figures and Tables
- Table 6: Add GPU inference times if available. Industry practitioners often deploy on GPU.
- Table 8: Consider adding a row for "OMP" baseline in each training condition for easier comparison.

### Layout
- No significant layout issues.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 52 | Weak | Standard LISTA applied to known problem; contribution is analytical |
| Methodological Rigor (25%) | 64 | Adequate | Good experimental design; fair baselines; limited statistical power |
| Evidence Sufficiency (25%) | 55 | Weak | Missing BER, system-level evaluation, training cost, hybrid framework |
| Argument Coherence (15%) | 67 | Adequate | Clear structure; practical claims need BER support |
| Writing Quality (15%) | 72 | Strong | Clear, professional; well-organized |
| Significance & Impact | 58 | Weak | Practical impact unquantified without BER; deployment story incomplete |
| **Weighted Average** | **61.6** | **Adequate** | **Major Revision recommended** |
