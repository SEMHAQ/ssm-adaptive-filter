# Peer Review Report — R3 Perspective (Round 18)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation
- **Manuscript ID**: DSP-2026-ROUND18
- **Review Date**: 2026-06-01
- **Review Round**: Round 18

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-Disciplinary Perspective

### Reviewer Identity
Dr. Sarah Chen, Senior Research Scientist at Nokia Bell Labs. Expertise in FPGA/ASIC design for wireless communications and practical deployment of ML at the physical layer.

### Review Focus
Practical deployment implications, hardware feasibility, cross-disciplinary connections.

---

## Overall Assessment

### Recommendation
- [x] **Accept**
- [ ] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
4

### Summary Assessment
The Round 18 revision improves the practical contribution. The threshold comparison experiment has direct hardware implications: hard thresholding is simpler to implement in hardware than soft thresholding (a comparator vs. a subtractor + comparator), and its 7.1 dB advantage means hardware designers can choose the simpler implementation with better performance. The contribution framing is now honest, the AMP claims are appropriately hedged, and the deployment framework (Section 5.3) remains actionable. The paper is ready for publication.

---

## Strengths

### S1: Hardware Implications of Threshold Comparison
The threshold comparison (Section 4.13) has direct hardware relevance: hard thresholding is both simpler to implement (comparator only, no subtractor) and 7.1 dB better than soft thresholding. For FPGA/ASIC implementations, this means the better algorithm is also the cheaper one—a rare win-win.

### S2: Honest Hardware Analysis
The paper correctly states "All hardware complexity values are theoretical FLOP counts; measured FPGA/ASIC latency, throughput, and power consumption remain future work." This honesty is appropriate.

### S3: Deployment Framework
Section 5.3 provides a clear decision framework: throughput-critical → LISTA, known SNR → SNR-specific training, variable SNR → broad-range training, NMSE-critical → OMP/FISTA.

---

## Weaknesses

### W1: Hardware Implications of Threshold Comparison Not Discussed
**Problem**: The threshold comparison (Section 4.13) does not discuss the hardware implications of hard vs. soft thresholding. Hard thresholding is simpler to implement in hardware.
**Why it matters**: This is a missed opportunity to strengthen the practical contribution.
**Suggestion**: Add a sentence noting that hard thresholding is hardware-friendlier.
**Severity**: Minor

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 74 | Strong | Threshold comparison adds practical novelty |
| Methodological Rigor (25%) | 83 | Strong | Comprehensive; hardware analysis theoretical |
| Evidence Sufficiency (25%) | 84 | Strong | Multiple experiments and baselines |
| Argument Coherence (15%) | 83 | Strong | Clear narrative; practical recommendations |
| Writing Quality (15%) | 84 | Strong | Professional, honest |
| Significance & Impact | 76 | Strong | Practical deployment guidance; threshold comparison has HW implications |
| **Weighted Average** | **81.0** | **Accept** | |

---

*Report submitted by Reviewer 3 (Perspective)*
