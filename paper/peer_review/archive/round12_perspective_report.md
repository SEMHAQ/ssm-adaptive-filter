# Peer Review Report — Peer Reviewer 3 (Cross-Disciplinary Perspective)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 12

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-Disciplinary Perspective

### Reviewer Identity
Prof. Aisha Rahman, Associate Professor of Electrical and Computer Engineering. Expertise in FPGA/ASIC implementation of deep learning accelerators, hardware-software co-design for wireless systems, and practical deployment of ML models at the edge. Published on hardware-efficient neural network architectures and real-time signal processing systems.

### Review Focus
Cross-disciplinary connections (hardware implementation, practical deployment), practical impact, broader implications for the deep unfolding community, and whether the findings are actionable for practitioners. This review assesses the paper from the perspective of someone who would implement and deploy these algorithms.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — Hardware implementation and practical deployment are my core expertise. Deep unfolding architectures are a secondary specialty, but the hardware complexity analysis and deployment considerations are directly relevant to my work.

### Summary Assessment
This paper provides a systematic analysis of LISTA for sparse channel estimation, with particular value for practitioners considering deployment. The paper's honesty about LISTA's limitations—trailing OMP by 13–33 dB in NMSE—is refreshing and helps practitioners make informed decisions. The error concentration mechanism (99.9% on true taps) is a novel finding with practical implications: it explains why LISTA may be preferred under ZF equalization despite worse NMSE. The hardware complexity analysis (760K FLOPs, 2.3× OMP) and the theoretical pipeline throughput discussion are useful starting points, though they remain theoretical. The practical deployment recommendations (Section 5.3) provide a clear decision framework. However, the paper has significant gaps from a deployment perspective: (1) the hardware analysis is entirely theoretical with no measured results; (2) the paper does not discuss memory bandwidth, power consumption, or latency in real hardware; (3) the $O(N^2)$ scaling of $\mathbf{W}^{(k)}$ is acknowledged but not addressed with concrete solutions; (4) the paper does not discuss online adaptation or time-varying channels. These gaps limit the paper's practical impact but are addressable in a revision. The paper is suitable for publication with minor revisions to strengthen the practical deployment discussion.

---

## Strengths

### S1: Clear Practical Deployment Decision Framework
Section 5.3 provides a well-structured decision framework for practitioners: (1) throughput-critical → LISTA with pipelining, (2) known SNR → SNR-specific training, (3) variable SNR → broad-range training, (4) NMSE-critical → OMP/LASSO. This is actionable guidance that goes beyond typical academic papers. The recommendation to "use LISTA for throughput, OMP for accuracy" is a clear, honest positioning.

### S2: Error Concentration Mechanism — Practical Implications
The finding that LISTA concentrates 99.9% of error on true taps has direct practical implications for equalizer design. The 1.8× noise enhancement advantage under ZF (Section 4.12.3) translates to tangible BER improvements for 16-QAM. This is valuable for practitioners designing receivers with ZF equalization (e.g., low-complexity IoT receivers).

### S3: Parameter Count and Complexity Analysis
The parameter analysis (Section 3.4: 82K parameters for N=64) and FLOP analysis (Table 13: 760K FLOPs) are useful for resource-constrained deployment. The scaling analysis (Table 14) showing the $O(N^2)$ growth is important for practitioners considering larger channel lengths. The comparison with CNN/Transformer methods (Section 5.2, Table 12) contextualizes LISTA's computational cost.

### S4: LISTA-CP Comparison with Diagnostic Insight
The LISTA-CP comparison (Section 4.8) is valuable from a deployment perspective. The finding that the weight clipping constraint is never activated (max spectral norm = 0.34 < 1.0) means practitioners can use standard LISTA without the additional complexity of constraint enforcement. This simplifies hardware implementation.

### S5: SNR-Specific Training as Deployment Strategy
The SNR mitigation experiments (Section 4.9) provide a concrete deployment strategy. The finding that narrow-range training improves NMSE by ~6 dB (from -25 to -31 dB) with minimal additional training cost is practically useful. The recommendation to train on a narrow SNR range around the operating point is easy to implement.

---

## Weaknesses

### W1: Hardware Analysis Entirely Theoretical
**Problem**: The paper devotes significant space (Section 4.13, Tables 13-14) to theoretical hardware complexity analysis—FLOP counts, pipeline stages, theoretical throughput—but explicitly acknowledges "measured FPGA/ASIC results remain future work." The paper cites Wei et al. (2022) for FPGA LISTA implementation but does not reproduce or validate those results.
**Why it matters**: Theoretical FLOP counts do not account for memory bandwidth, data reuse, pipeline stalls, clock frequency, or power consumption—all critical for real hardware. The claim of "potential hardware throughput advantage" (Abstract) is unsubstantiated without measured results.
**Suggestion**: Either (a) add measured FPGA/ASIC results (even preliminary), or (b) significantly condense the hardware section to a single table and 1-2 paragraphs, clearly labeling everything as theoretical. The current level of detail for theoretical-only analysis is excessive.
**Severity**: Major

### W2: No Discussion of Memory Bandwidth Bottleneck
**Problem**: The paper analyzes FLOP counts but does not discuss memory bandwidth. For LISTA with $L=20$ layers and $\mathbf{W}^{(k)} \in \mathbb{R}^{64 \times 64}$, each layer requires reading 4096 parameters and writing 64 results. At 500 MHz, this requires ~40 GB/s bandwidth—far exceeding typical FPGA on-chip memory capacity.
**Why it matters**: Memory bandwidth, not FLOP count, is often the bottleneck for hardware accelerators. The paper's theoretical throughput claims may not hold when memory bandwidth is considered.
**Suggestion**: Add a brief discussion of memory bandwidth requirements and how they affect the theoretical throughput analysis. Consider mentioning weight reuse strategies (e.g., layer-wise weight sharing) as potential mitigations.
**Severity**: Major

### W3: No Discussion of Online Adaptation or Time-Varying Channels
**Problem**: The paper evaluates LISTA on static channels (independent realizations, no temporal correlation). In practical wireless systems, channels are time-varying, and estimators must adapt. The paper does not discuss whether LISTA can be fine-tuned online or whether its error concentration mechanism holds for time-varying channels.
**Why it matters**: Practical channel estimation requires tracking channel variations over time. A method that only works on static channels has limited practical applicability.
**Suggestion**: Add a brief discussion of LISTA's potential for online adaptation (e.g., fine-tuning the last few layers on recent pilot data). If this is outside the paper's scope, acknowledge it as a limitation.
**Severity**: Minor

### W4: Scalability Concern Not Addressed
**Problem**: The paper acknowledges that LISTA training diverges at N=256 (Table 4) and that the $O(N^2)$ parameter count limits scalability (Section 3.4). The paper suggests "structured linear mappings (Toeplitz, circulant, low-rank)" as potential solutions but does not evaluate them.
**Why it matters**: Many practical channels (e.g., wideband OFDM, massive MIMO) have N > 128. Without concrete solutions for the scalability issue, LISTA's practical applicability is limited to short channels.
**Suggestion**: At minimum, add a brief analysis of the potential of structured linear mappings (e.g., estimate the parameter reduction from Toeplitz structure). Ideally, include a preliminary experiment with structured $\mathbf{W}^{(k)}$.
**Severity**: Minor

### W5: Power Consumption Not Discussed
**Problem**: The paper does not discuss power consumption, which is critical for edge deployment (e.g., IoT devices, mobile terminals). LISTA's 760K FLOPs may translate to different power consumption depending on the hardware platform.
**Why it matters**: For battery-constrained devices, power consumption is often more important than throughput. The paper's deployment recommendations would be stronger with power estimates.
**Suggestion**: Add a brief discussion of expected power consumption based on published hardware implementations (e.g., Wei et al. 2022). If data is unavailable, acknowledge the gap.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title correctly positions the paper as an analysis rather than a new method.
- Abstract mentions hardware complexity (760K FLOPs, 2.3× OMP) but correctly labels it as theoretical.

### Introduction
- Contribution 6 (hardware complexity) is the weakest contribution and could be condensed.
- The deployment recommendations in the introduction are useful but premature (results come later).

### Methodology (Section 3)
- The parameter analysis (Section 3.4) is valuable for practitioners.
- The computational complexity analysis (Section 3.6) could include memory access counts.
- The comparison with classical methods (Section 3.7) is well-structured.

### Results (Section 4)
- The inference time comparison (Table 7) is useful but the Python caveat is important.
- The ITU channel evaluation (Section 4.7.2) tests cross-distribution generalization.
- The hardware complexity analysis (Section 4.13) is detailed but theoretical.

### Discussion (Section 5)
- The deployment recommendations (Section 5.3) are the highlight from a practical perspective.
- The limitations (Section 5.4) are thorough but should include memory bandwidth and online adaptation.
- The qualitative CNN/Transformer comparison (Section 5.2) is useful but could be more concise.

### Practical Impact Assessment
- **Throughput**: Theoretical pipeline analysis suggests potential advantage, but no measured results.
- **Latency**: Python benchmarks (0.21 ms) are not representative of hardware latency.
- **Power**: Not discussed.
- **Memory**: Not discussed beyond parameter count.
- **Adaptability**: Not discussed (static channels only).

---

## Questions for Authors

1. **Memory bandwidth**: For N=64, L=20, what is the total memory bandwidth required per channel estimate? Have you considered weight reuse strategies to reduce bandwidth?

2. **Online adaptation**: Have you considered fine-tuning LISTA's last few layers on recent pilot data for time-varying channels? This would be a natural extension for practical deployment.

3. **Structured $\mathbf{W}^{(k)}$**: You suggest Toeplitz/circulant/low-rank structures for scalability (Section 3.4). Can you estimate the parameter reduction and expected NMSE impact for at least one of these structures?

4. **Power consumption**: Based on Wei et al. (2022)'s FPGA implementation, what is the expected power consumption per channel estimate for LISTA vs. OMP?

---

## Minor Issues

### Cross-Disciplinary Connections
- The paper could benefit from citing more hardware-focused references (e.g., systolic array designs for matrix-vector multiplication, weight stationary dataflow for deep unfolding).
- The comparison with CNN/Transformer methods (Section 5.2) should mention that these methods have been implemented on FPGA (cite relevant work).

### Practical Deployment
- The inference time comparison (Table 7) should include a footnote explaining why Python benchmarks are not representative of hardware performance.
- The pipeline throughput analysis (Section 4.13) should mention the assumption of sufficient memory bandwidth.

### Writing
- Section 4.13 is too long for a theoretical analysis. Consider condensing to 1-2 paragraphs with a single table.
- The deployment recommendations (Section 5.3) are well-written and actionable.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | No architectural novelty. The error concentration mechanism is the key contribution. The deployment framework adds practical value. |
| Methodological Rigor (25%) | 72 | Adequate | Good experimental design, but hardware analysis is entirely theoretical. Missing memory bandwidth and power analysis. |
| Evidence Sufficiency (25%) | 65 | Adequate | Good evidence for NMSE/BER claims. Hardware claims lack measured evidence. Limited to static channels. |
| Argument Coherence (15%) | 78 | Strong | Clear logical flow. The mechanism analysis provides a coherent narrative. Deployment recommendations are well-structured. |
| Writing Quality (15%) | 80 | Strong | Clear writing. Good use of tables. Some sections are verbose (hardware analysis). |
| Significance & Impact | 70 | Adequate | Practical deployment framework is valuable. Hardware analysis is theoretical. Limited to static channels and short channel lengths. |
| **Weighted Average** | **71.4** | **Minor Revision** | |

---

## Overall Score: 71/100
