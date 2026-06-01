# Peer Review Report — Perspective Reviewer (R3)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 6

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-Disciplinary Perspective

### Reviewer Identity
Prof. James Thornton, Professor of Hardware Acceleration for Machine Learning. Expertise in FPGA/ASIC design for communications, real-time ML systems, and algorithm-hardware co-optimization.

### Review Focus
Hardware complexity claims, scalability analysis, practical deployment feasibility, and cross-disciplinary impact (ML + hardware + communications). I assess whether theoretical complexity claims are realistic and whether the paper provides sufficient evidence for hardware deployment.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**
- [ ] **Accept**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
4 — Hardware acceleration and FPGA design are my core expertise. I am confident in assessing the hardware complexity claims. The signal processing aspects are within my broader knowledge.

### Summary Assessment
This paper analyzes LISTA for sparse channel estimation with emphasis on practical deployment, including hardware complexity analysis, pipelining estimates, and memory access patterns. The paper's cross-disciplinary contribution lies in bridging deep unfolding theory with hardware implementation considerations. The theoretical FLOPs analysis (Section 4.13) and the scaling analysis (Table 13) provide useful guidance for hardware designers.

However, the hardware claims are entirely theoretical — no measured FPGA or ASIC results are provided. The 4.4× throughput advantage and 1.2 μs throughput estimates are based on idealized assumptions (64 DSP units, 500 MHz, perfect pipelining) that may not hold in practice. The paper cites Wei et al. (2022) for FPGA validation, but the specific architecture analyzed here (with W^(k) matrices) differs from that reference. The Python speed comparison (33× faster) is acknowledged as reflecting interpreter overhead, which is honest but limits the practical value of the claim.

I recommend Minor Revision. The hardware analysis is well-structured and provides a useful theoretical framework, but the claims should be tempered or supplemented with measured results.

---

## Strengths

### S1: Structured Hardware Complexity Analysis
Section 4.13 provides a well-organized hardware complexity analysis covering FLOPs (Table 12), parallelism characteristics (intra-layer, batch, pipeline), memory access patterns, and timing estimates. The breakdown of LISTA's per-layer complexity into FFT convolution (O(M log M)), linear mapping (O(N²)), and thresholding (O(N)) is clear and useful for hardware designers.

### S2: Scaling Analysis with Practical Implications
Table 13 (scaling analysis) shows how LISTA's parameters and FLOPs scale with channel length N, from 32 to 256. The finding that LISTA/OMP FLOPs ratio grows from 2.14× to 3.06× as N increases highlights the O(N²) bottleneck of the W^(k) matrices. The explicit recommendation for structured linear mappings (Toeplitz, circulant, low-rank) at N > 128 is actionable.

### S3: Memory Access Pattern Characterization
The characterization of LISTA's memory access as "sequential and predictable" (Section 4.13.3) with W^(k) matrices fitting in L1 cache (16 KB per matrix) and total parameters fitting in L2 cache (328 KB) is valuable for hardware designers. The contrast with OMP's "semi-random memory access patterns" due to dynamic support set selection is well-argued.

### S4: Pipeline Throughput Analysis
The 20-stage pipeline analysis (Section 4.13.4) estimating 1.2 μs throughput is a useful reference point. The alignment with Wei et al.'s measured < 10 μs FPGA latency provides external validation. The distinction between latency (23 μs) and throughput (1.2 μs per estimate) is important and correctly explained.

### S5: Cross-Disciplinary Deployment Framework
Section 5.2 provides a practical decision framework bridging algorithm and hardware considerations: speed-critical → LISTA (4.4× throughput), known SNR → SNR-specific training, variable SNR → broad-range training. The recommendation to "use LISTA for speed, OMP for accuracy" is a useful practical guideline.

---

## Weaknesses

### W1: Hardware Claims Entirely Theoretical
**Problem**: The paper's key hardware claim — "4.4× hardware throughput advantage over OMP via 20-stage pipelining (1.2 μs on FPGA)" — is based entirely on theoretical analysis. No measured FPGA, ASIC, or even HLS-synthesized results are provided. The assumptions (64 DSP units at 500 MHz, perfect pipelining, zero pipeline stalls) are idealized.
**Why it matters**: Hardware designers need measured results, not theoretical estimates. The 4.4× advantage could be significantly different in practice due to: (a) memory bandwidth bottlenecks, (b) pipeline stalls from data dependencies, (c) resource utilization inefficiencies, (d) clock frequency limitations. The abstract highlights this claim prominently, which may mislead readers.
**Suggestion**: Either (a) provide at least an HLS implementation or synthesis results to validate the estimates, or (b) qualify the claims as "theoretical analysis suggests" throughout the paper (abstract, highlights, conclusion). The current wording ("enables 4.4× throughput advantage") implies measured results.
**Severity**: Major

### W2: Python Speed Comparison Limited Value
**Problem**: The paper reports LISTA is "33× faster in Python (0.21 vs 6.91 ms)" (Table 4) and correctly notes this "reflects interpreter overhead rather than algorithmic complexity." However, this caveat is sometimes lost in the abstract and highlights, where "33× faster" appears without qualification.
**Why it matters**: The 33× speedup is a software artifact, not an algorithmic property. OMP's iterative nature involves Python loops that are slow in interpreted code, while LISTA's feedforward computation maps to matrix operations that are efficiently handled by NumPy/PyTorch. In optimized C++ implementations, the gap would be much smaller.
**Suggestion**: Remove the "33× faster" claim from the abstract and highlights, or clearly qualify it as "Python implementation speedup reflecting interpreter overhead." The hardware throughput claim (4.4×) is the deployment-relevant metric and should be the primary speed claim.
**Severity**: Minor

### W3: No Energy/Power Analysis
**Problem**: The hardware complexity analysis (Section 4.13) focuses on FLOPs and throughput but does not discuss energy consumption or power dissipation. For mobile and IoT communications (a key application domain), energy efficiency is often more important than throughput.
**Why it matters**: LISTA's W^(k) matrix-vector multiplications require O(N²) MAC operations per layer, which consume significant energy. OMP's greedy selection involves fewer MAC operations but with irregular access patterns. The energy comparison could be very different from the throughput comparison.
**Suggestion**: Add a brief discussion of energy complexity, even if only at the FLOP-count level. Note that LISTA's regular computation pattern may enable better energy efficiency per FLOP due to reduced memory access overhead, but the higher FLOP count (2.3× OMP) means total energy may be comparable.
**Severity**: Minor

### W4: Scalability Concern Understated
**Problem**: The paper reports LISTA training diverges at N=256 (Table 3, 3/5 seeds yield positive NMSE) and notes this as a "practical scalability limit." However, the Discussion section (Section 5.3) treats this as a minor limitation, suggesting structured linear mappings as a solution without evaluating whether they actually work.
**Why it matters**: N=256 is not an unusually large channel length — 5G NR systems can have channel lengths of 256–1024 taps. If LISTA cannot handle N=256, its practical applicability is significantly limited. The suggestion of structured mappings (Toeplitz, circulant) is speculative without experimental validation.
**Suggestion**: Either (a) evaluate LISTA with structured linear mappings (Toeplitz or low-rank) at N=128 and 256 to demonstrate that the approach works, or (b) explicitly state that LISTA is limited to N ≤ 128 without architectural modifications, and that the structured mapping approach is unvalidated.
**Severity**: Minor

---

## Detailed Comments

### Hardware Complexity Analysis (Section 4.13)
- FLOPs comparison (Table 12): Well-structured. The per-iteration breakdown is helpful.
- Parallelism characteristics: Good coverage of intra-layer, batch, and pipeline parallelism.
- Memory access patterns: The L1/L2 cache analysis is practical and useful.
- Timing estimates: The 64 DSP units at 500 MHz assumption is reasonable for mid-range FPGA but should be stated as an assumption.
- Scaling analysis (Table 13): The O(N²) bottleneck is correctly identified. The structured mapping recommendation is appropriate but unvalidated.

### BER Analysis (Section 4.10)
- From a hardware perspective, the BER results are interesting because they suggest that LISTA's "worse" NMSE is not actually worse for the end metric (BER). This has implications for hardware designers who might choose LISTA for speed without BER penalty.
- The ZF vs MMSE distinction is important for hardware: ZF equalizers are simpler to implement than MMSE, so the ZF-specific BER advantage is relevant for low-complexity receivers.

### Practical Deployment (Section 5.2)
- The decision framework is useful but could be expanded with hardware-specific considerations: (a) what FPGA resources are needed? (b) what is the power consumption? (c) what is the latency budget?

### References
- The hardware references (Kim et al., Wei et al., Chen et al.) are appropriate.
- Missing: recent (2024–2025) FPGA implementations of deep-unfolded networks for communications.

---

## Questions for Authors

1. Can you provide at least a high-level resource utilization estimate (LUTs, FFs, DSPs, BRAMs) for implementing LISTA on a mid-range FPGA (e.g., Xilinx Zynq UltraScale+)? Even a rough estimate would be valuable for hardware designers.

2. The 4.4× throughput advantage assumes perfect pipelining with zero stalls. In practice, data dependencies between pipeline stages (e.g., the gradient computation g^(k) = X^T(Xh^(k) - d) depends on h^(k)) may introduce stalls. Have you analyzed the actual pipeline utilization?

3. For the structured linear mappings (Toeplitz, circulant, low-rank) suggested in Section 5.3 for N > 128: have you validated this approach experimentally? If not, this should be stated as a future direction rather than a recommendation.

---

## Minor Issues

### Hardware Claims
- Abstract: "4.4× hardware throughput advantage" → add "theoretical analysis suggests" or provide measured results.
- Highlights: "4.4× hardware throughput advantage over OMP via 20-stage pipelining" → qualify as theoretical.
- Table 4: Add a footnote explaining that the Python speedup reflects interpreter overhead, not algorithmic complexity.

### Figures
- Consider adding a diagram of the 20-stage pipeline architecture to help hardware designers understand the data flow.
- Figure for scaling analysis (Table 13): Plot FLOPs vs N on log-log scale to visualize the O(N²) scaling.

### Writing
- Section 4.13.4: The timing estimates should explicitly state the assumptions (64 DSP units, 500 MHz, zero pipeline stalls) in the text, not just in the surrounding discussion.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 55 | Weak | LISTA is well-known. Hardware analysis is theoretical. BER-NMSE mechanism is novel. |
| Methodological Rigor (25%) | 68 | Adequate | Good experimental design. Hardware claims unvalidated. Missing DL baselines. |
| Evidence Sufficiency (25%) | 65 | Adequate | Comprehensive experiments. Hardware claims lack measured results. |
| Argument Coherence (15%) | 78 | Strong | Clear logical flow. Hardware analysis well-structured. |
| Writing Quality (15%) | 70 | Adequate | Generally clear. Hardware claims sometimes overstated. |
| Literature Integration (optional) | 64 | Adequate | Good coverage. Missing recent FPGA implementation papers. |
| Significance & Impact (optional) | 62 | Adequate | Useful for hardware designers. Limited by lack of measured results. |
| **Weighted Average** | **66.8** | **Minor Revision** | |

---

**Decision**: Minor Revision — The paper provides useful hardware complexity analysis as a theoretical framework, but claims should be tempered without measured results. The BER-NMSE mechanism analysis is the strongest contribution. Hardware-specific concerns are addressable.
