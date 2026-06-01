# Peer Review Report

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 4

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Cross-Disciplinary Perspective)

### Reviewer Identity
Dr. Ing. Marcus Weber, Senior Research Engineer, Nokia Bell Labs (Germany). Expertise in FPGA/ASIC implementation of signal processing algorithms, hardware-software co-design, and real-time communication systems. 12 years of industry experience deploying deep learning models on embedded platforms. Brings the practitioner's perspective: can this actually be deployed?

### Review Focus
Practical deployment feasibility, hardware implementation considerations, cross-disciplinary connections (signal processing ↔ hardware design ↔ ML systems), and real-world impact. I assess whether the paper's claims translate from Python simulations to production hardware, and whether the findings matter for engineers building actual communication systems.

---

## Overall Assessment *

### Recommendation *
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score *
4 — Mostly within my area of expertise. Hardware deployment and practical systems are my core domain; the sparse recovery theory is adjacent but I have sufficient familiarity.

### Summary Assessment *
This paper evaluates LISTA for sparse channel estimation with a focus on BER performance and practical deployment. From a practitioner's perspective, the most valuable contribution is the BER analysis showing that LISTA achieves comparable or better BER than OMP despite worse NMSE—this is the metric that matters for system designers. The hardware complexity analysis (760K FLOPs, 20-stage pipeline, 1.2 μs throughput) provides useful ballpark estimates.

However, the hardware analysis is entirely theoretical—no actual FPGA or ASIC implementation is presented. The FLOP counts and timing estimates are reasonable but unvalidated. The Python speed comparison (33×) is not directly relevant to hardware deployment, and the paper appropriately acknowledges this. The 82K parameter count is modest and fits modern FPGA block RAM, which is a genuine advantage. Overall, the paper provides a useful feasibility analysis for practitioners but falls short of a hardware implementation paper.

---

## Strengths *

### S1: BER-Centric Evaluation Instead of NMSE
From a system designer's perspective, BER is what matters—not NMSE. The paper's central finding that LISTA achieves comparable BER with 33× faster inference is directly actionable for engineers designing receivers. The 16-QAM advantage (p < 0.05 at SNR ≥ 15 dB) is particularly relevant for modern high-order modulation systems.

### S2: Honest Hardware Complexity Analysis
The paper provides FLOP counts, parameter memory, pipeline estimates, and scaling analysis without overclaiming. The distinction between Python speedup (33×) and hardware throughput advantage (4.4×) is important and honestly presented. The reference to [Wei 2022] FPGA results (< 10 μs latency) grounds the estimates in measured data.

### S3: Practical Deployment Recommendations
Section 5.2 provides a clear decision framework: use LISTA for speed-critical applications, use SNR-specific training when operating SNR is known, fall back to OMP for accuracy-critical scenarios. This is exactly what practitioners need.

### S4: Parameter Efficiency
The 82K parameter count (328 KB at float32) fitting in L2 cache is a genuine hardware advantage. The sequential memory access pattern enabling efficient caching is well-analyzed. This makes LISTA deployable on resource-constrained platforms where OMP's dynamic memory patterns would be problematic.

---

## Weaknesses *

### W1: Hardware Analysis Is Purely Theoretical
**Problem**: The paper provides FLOP counts and timing estimates (Section 4.13) but no actual FPGA or ASIC implementation. The timing estimates assume 64 DSP units at 500 MHz—specific hardware assumptions that may not reflect real implementations.
**Why it matters**: Practitioners need measured latency, throughput, and power consumption—not theoretical estimates. The gap between theoretical FLOP counts and actual hardware performance can be 2–10× due to memory bandwidth, pipeline stalls, and control overhead.
**Suggestion**: (1) Acknowledge more prominently that the hardware analysis is theoretical. (2) If possible, cite or collaborate with an FPGA implementation group to provide measured results. (3) At minimum, provide a sensitivity analysis: how do the timing estimates change with different DSP counts or clock frequencies?
**Severity**: Minor

### W2: Python Speed Comparison May Mislead
**Problem**: The paper reports 33× speedup in Python (Section 4.7.1) and uses this as a headline number in the abstract and highlights. However, Python performance is dominated by interpreter overhead, not algorithmic complexity. A C++ implementation of OMP might be only 2–5× slower than LISTA.
**Why it matters**: Practitioners reading the abstract may overestimate LISTA's speed advantage. The 4.4× hardware throughput estimate is more realistic but less prominently featured.
**Suggestion**: (1) Lead with the hardware throughput estimate (4.4×) rather than the Python speedup (33×) in the abstract and highlights. (2) Explicitly state that the 33× reflects Python-specific overhead and is not representative of optimized implementations. (3) Consider providing C++ benchmarks if feasible.
**Severity**: Minor

### W3: No Power Consumption Analysis
**Problem**: The paper analyzes FLOPs, memory, and throughput but not power consumption—a critical metric for embedded and mobile deployments. LISTA's fixed computation graph should enable lower power than OMP's dynamic scheduling, but this is not quantified.
**Why it matters**: For 5G/6G base stations and mobile devices, power consumption is often the binding constraint, not throughput.
**Suggestion**: (1) Provide a theoretical power estimate based on FLOP count and typical energy per FLOP on FPGA (e.g., ~10 pJ/FLOP for modern FPGAs). (2) Compare with OMP and LASSO power estimates. (3) Discuss implications for battery-powered devices.
**Severity**: Minor

### W4: Missing Real-World Channel Considerations
**Problem**: The paper uses BPSK pilots (±1) and AWGN noise. Real systems use QPSK or higher-order pilot symbols, have frequency offsets, phase noise, and non-linear distortions. The impact of these practical impairments on LISTA's performance is not discussed.
**Why it matters**: Practitioners need to know whether LISTA's advantages survive in realistic operating conditions.
**Suggestion**: (1) Discuss expected impact of practical impairments on LISTA vs. OMP. (2) At minimum, test with QPSK pilots to assess sensitivity to pilot modulation. (3) Discuss whether LISTA's training can incorporate impairments as data augmentation.
**Severity**: Minor

---

## Detailed Comments *

### Title & Abstract
- Title is appropriate for the paper's evaluative nature.
- Abstract clearly states the key practical findings (33× speedup, comparable BER).
- The highlights section effectively communicates deployment-relevant information.

### Introduction
- The motivation for speed-critical deployment is well-articulated.
- The contribution list is comprehensive but could be more focused on practical implications.

### Literature Review
- The hardware deployment subsection (Section 2.3) appropriately covers FPGA accelerators and deep unfolding implementations.
- The reference to [Wei 2022] FPGA results is important for grounding the estimates.

### Methodology
- The LISTA architecture description is clear enough for hardware engineers to understand the implementation requirements.
- The FFT-based convolution (Section 3.3) is a practical implementation detail that enhances reproducibility.

### Results
- Experiment 7 (Runtime): The Python speedup is useful but should be contextualized for hardware.
- Experiment 13 (Hardware): The FLOP analysis is thorough. The pipeline estimate (1.2 μs) is reasonable but unvalidated.
- The BER results (Section 4.10) are the most deployment-relevant findings.

### Discussion
- The deployment recommendations (Section 5.2) are practical and actionable.
- The limitations section honestly addresses hardware deployment gaps.
- The future research directions include FPGA implementation, which is the natural next step.

### References
- The hardware deployment references [Kim 2021, Wei 2022, Chen 2022] are appropriate and recent.

---

## Questions for Authors *

1. **C++ benchmarks**: Have you considered providing C++ or optimized NumPy benchmarks? The Python speedup (33×) may not reflect optimized implementation performance.
2. **Power consumption**: Can you provide a rough power estimate for LISTA vs. OMP on FPGA? Even a theoretical estimate based on FLOP count would be useful.
3. **Pilot modulation**: All experiments use BPSK pilots. Have you tested with QPSK or higher-order pilots to assess sensitivity?
4. **Real-time constraint**: For a 5G NR slot (0.5 ms), can LISTA process all subcarriers within the slot? What is the maximum channel length N that meets this constraint?

---

## Minor Issues

### Language / Grammar
- Section 4.13.4: "20-stage pipeline with ~1.2 μs throughput per estimate at 500 MHz with 64 DSP units" — the "~" should be removed or the estimate range given.

### Figures and Tables
- Table 12 (FLOPs): The LASSO FLOP count (6.6M) should include a note about the iteration count (200 vs. 500 for convergence).
- Table 13 (Scaling): The LISTA/OMP FLOPs ratio column is useful for practitioners.

### Layout
- No significant layout issues.

---

## Dimension Scores *

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 60 | Adequate | No architectural novelty; novel BER analysis |
| Methodological Rigor (25%) | 70 | Adequate | Good simulation practices; hardware analysis is theoretical |
| Evidence Sufficiency (25%) | 74 | Adequate | Comprehensive experiments; hardware claims unvalidated |
| Argument Coherence (15%) | 76 | Strong | Clear practical narrative |
| Writing Quality (15%) | 77 | Strong | Professional and accessible |
| Significance & Impact | 72 | Adequate | Useful for practitioners; no measured hardware results |
| **Weighted Average** | **71.2** | **Minor Revision** | |
