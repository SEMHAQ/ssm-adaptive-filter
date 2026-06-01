# Peer Review Report — Reviewer 3 (Cross-Disciplinary Perspective)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 5

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-Disciplinary Perspective

### Reviewer Identity
Prof.~Dr.~Sarah Kim, Department of Computer Science & Engineering, Seoul National University. Expert in hardware-aware neural architecture design, FPGA/ASIC acceleration of deep learning, and edge AI systems. 12 years of experience bridging machine learning algorithm design with hardware deployment constraints. Has implemented >15 neural network architectures on FPGA, including several compressed sensing decoders. Brings a systems-level perspective: algorithm design must be evaluated not just by accuracy but by deployability, power efficiency, and real-world constraints.

### Review Focus
Cross-disciplinary connections between algorithm design and hardware deployment, practical impact and deployability, broader implications for the deep unfolding community, and whether the paper's claims hold from a systems perspective. I assess: (1) whether the hardware claims are realistic, (2) whether the practical deployment recommendations are actionable, (3) whether the paper bridges the algorithm-hardware gap effectively.

---

## Overall Assessment

### Recommendation
- [ ] **Accept**
- [x] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
4 — High confidence on hardware deployment aspects (my primary expertise). Moderate confidence on the signal processing details (adjacent to my field).

### Summary Assessment

This paper provides a valuable bridge between the sparse recovery and hardware deployment communities by analyzing LISTA not just as an algorithm but as a deployable system. The hardware complexity analysis (Section 4.13) is well-structured, covering FLOPs, parallelism, memory access, and pipeline timing. The practical deployment framework (Section 5.2) is actionable and reflects real-world constraints. The BER-NMSE disconnect analysis is particularly important for hardware designers who need to choose between estimators based on system-level metrics (BER) rather than algorithm-level metrics (NMSE).

However, the paper's hardware analysis has a significant gap: it provides only theoretical estimates without measured FPGA results. The $4.4\times$ throughput advantage and $1.2$~$\mu$s latency are projections that may not account for memory bandwidth bottlenecks, control overhead, or resource sharing in real FPGA implementations. Additionally, the paper does not discuss power consumption, which is a critical constraint in mobile and IoT deployments. The Python speedup claim ($33\times$) is misleading if taken out of context, as the paper acknowledges. These gaps are addressable and the paper is suitable for publication after revision.

---

## Strengths

### S1: Systems-Level Thinking in Algorithm Evaluation
The paper evaluates LISTA from a systems perspective, not just an algorithm perspective. The combination of NMSE accuracy, BER performance, hardware complexity (FLOPs), memory access patterns, and pipeline throughput provides a multi-dimensional evaluation that is rare in the sparse recovery literature. Table 14's FLOPs comparison and Table 15's scaling analysis are exactly what hardware designers need to make deployment decisions.

### S2: BER-NMSE Disconnect as a Systems Insight
The finding that LISTA's 13--33~dB NMSE gap with OMP does not translate to a BER penalty is a systems-level insight that changes the algorithm selection calculus. For hardware designers choosing between LISTA and OMP, the BER result is more relevant than the NMSE result. The mechanism analysis (error concentration on true taps) provides a physical explanation that hardware designers can reason about.

### S3: Practical Deployment Framework
The 5-point deployment recommendation in Section 5.2 is actionable:
1. Speed-critical → LISTA (4.4$\times$ throughput)
2. Known SNR → SNR-specific training ($-31$~dB)
3. Variable SNR → broad-range training ($-25$~dB)
4. NMSE-critical → OMP/LASSO
5. Architecture choice → $L=10$--$20$ layers

This framework directly addresses the "when should I use LISTA?" question that practitioners ask.

### S4: Pipeline Architecture Analysis
The analysis of LISTA's 20-stage pipeline potential (Section 4.13.2) is well-reasoned. The identification of three levels of parallelism (intra-layer, batch, pipeline) and the comparison with OMP's irregular control flow is insightful. The memory access pattern analysis (sequential vs.~semi-random) is particularly relevant for FPGA implementations where memory bandwidth is often the bottleneck.

### S5: Honest Python Speedup Caveat
The explicit caveat that the $33\times$ Python speedup "reflects the relative efficiency of LISTA's fixed-depth feedforward computation versus OMP's iterative greedy selection within the same software ecosystem" (Section 4.7.1) is commendable. Many papers present Python speedups as if they predict hardware performance.

---

## Weaknesses

### W1: Hardware Claims Lack Measured Results
**Problem**: The $4.4\times$ throughput advantage and $1.2$~$\mu$s FPGA latency are theoretical estimates based on "64 parallel DSP units at 500 MHz" (Section 4.13.4). No actual FPGA implementation or measurement is provided. The estimates assume ideal conditions: no memory bandwidth bottlenecks, no control overhead, no resource sharing, and perfect pipelining.
**Why it matters**: Real FPGA implementations typically achieve 50--70\% of theoretical peak utilization due to memory bandwidth limitations, control logic overhead, and resource sharing. The $4.4\times$ advantage may shrink to $2$--$3\times$ in practice. The $1.2$~$\mu$s latency does not account for data transfer overhead between FPGA fabric and memory.
**Suggestion**: Either (a) provide measured FPGA results (even a prototype), or (b) include a more realistic utilization estimate (e.g., 60\% of peak) and explicitly state that the numbers are theoretical projections. Citing \citet{wei2022fpga}'s measured $< 10$~$\mu$s latency as evidence is appropriate, but the paper should not claim $1.2$~$\mu$s without measurement.
**Severity**: Major

### W2: Power Consumption Not Discussed
**Problem**: The paper does not discuss power consumption, which is a critical constraint for mobile and IoT deployments. LISTA's $760$K FLOPs per estimate translates to approximately $0.1$--$1$~mW on a modern FPGA (depending on clock frequency and voltage), but the paper does not provide this analysis.
**Why it matters**: For edge devices and mobile terminals, power consumption may be more important than throughput. A LISTA implementation that achieves $4.4\times$ throughput but consumes $3\times$ more power than OMP may not be preferable for battery-constrained devices.
**Suggestion**: Add a brief power consumption estimate based on the FLOP count and typical FPGA power efficiency (e.g., $10$--$50$~GFLOPs/W for mid-range FPGAs). Compare with OMP's power consumption. This would complete the hardware deployment analysis.
**Severity**: Minor

### W3: Python Speedup Comparison Methodology
**Problem**: The $33\times$ Python speedup (Table 6) is measured using Python (NumPy/PyTorch) implementations on a single CPU core. The paper acknowledges this reflects "interpreter overhead rather than algorithmic complexity," but the number is still prominently featured in the abstract and highlights. This risks being quoted out of context by readers who do not read the caveat.
**Why it matters**: The Python speedup is not a meaningful metric for hardware deployment decisions. A fair comparison would use optimized C/C++ implementations on the same platform. The paper's own hardware analysis (Section 4.13) shows a more modest $4.4\times$ advantage, which is the deployment-relevant metric.
**Suggestion**: De-emphasize the Python speedup in the abstract and highlights. Replace with the hardware throughput advantage ($4.4\times$) as the primary speed metric. Keep the Python benchmark in the main text but frame it as "software implementation comparison" rather than "speedup."
**Severity**: Minor

### W4: No Discussion of Training Cost
**Problem**: The paper does not discuss the training cost of LISTA. Training a LISTA model requires generating 10,000 training samples, running 200 epochs of backpropagation, and repeating for 5 seeds. This training cost is a one-time expense, but it is relevant for: (a) practitioners who need to retrain for different channel conditions, (b) SNR-specific training (Section 4.9) which requires separate models for each SNR range.
**Why it matters**: The paper's deployment recommendation includes SNR-specific training, which requires training and storing multiple models. For a system that operates across a wide SNR range, this multiplies the training cost and model storage requirements.
**Suggestion**: Add a brief discussion of training cost (time, compute, storage) and how it affects the deployment recommendation. If SNR-specific training requires 4 separate models (one per SNR range), this should be acknowledged.
**Severity**: Minor

### W5: Comparison Fairness — OMP with Oracle K
**Problem**: The paper compares LISTA against OMP with oracle sparsity level $K$ (Section 4.1). This gives OMP an unfair advantage in practice, where $K$ is unknown. The paper acknowledges this ("LISTA does not require explicit sparsity knowledge") but does not quantify the cost of estimating $K$ for OMP.
**Why it matters**: In practical deployments, $K$ must be estimated (e.g., via cross-validation or information criteria), which adds computational cost and may degrade OMP's performance. A fairer comparison would include OMP with estimated $K$ (e.g., using the Akaike Information Criterion or cross-validation).
**Suggestion**: Add a comparison with OMP using estimated $K$ (e.g., via cross-validation on the validation set). This would quantify the practical cost of not knowing $K$ and strengthen LISTA's advantage in the "no sparsity knowledge" scenario.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title is descriptive but long. Consider shortening to "Deep-Unfolded LISTA for Sparse Channel Estimation: BER Analysis, Ablation, and Hardware Deployment."
- The abstract's hardware claims should be qualified as theoretical estimates.

### Introduction
- The 6 contributions are comprehensive. Contribution 6 (hardware complexity) is particularly relevant for my review focus.
- The motivation for studying LISTA (rather than newer variants) is adequately justified.

### Methodology
- The LISTA architecture is standard and well-described.
- The training procedure is well-specified.

### Results
- The NMSE and BER analyses are thorough.
- The hardware complexity analysis (Section 4.13) is well-structured but lacks measured results.
- The scaling analysis (Table 15) correctly identifies the $O(N^2)$ bottleneck.

### Discussion
- The deployment framework (Section 5.2) is actionable and well-justified.
- The limitations section (5.3) is honest.
- The future research directions include hardware implementation, which is appropriate.

### References
- The hardware deployment references \citep{kim2021fpga, wei2022fpga, chen2022survey} are relevant.
- **Missing**: \citet{han2016deep} on hardware-aware deep learning, \citet{venkataramani2017deep} on scalable deep learning hardware.

---

## Questions for Authors

1. **FPGA utilization**: The $4.4\times$ throughput estimate assumes 64 DSP units at 500 MHz. What utilization rate did you assume? Real FPGA implementations typically achieve 50--70\% of peak. Can you provide a more conservative estimate?

2. **Power consumption**: Can you estimate the power consumption of LISTA vs.~OMP on a mid-range FPGA (e.g., Xilinx Zynq UltraScale+)? This would complete the hardware deployment analysis.

3. **Training cost for SNR-specific models**: The deployment recommendation includes SNR-specific training. How many separate models would be needed to cover the 0--30 dB range? What is the training cost per model?

4. **OMP with estimated K**: Can you compare LISTA against OMP with $K$ estimated via cross-validation? This would quantify the practical cost of not knowing $K$.

5. **Memory bandwidth**: The pipeline analysis assumes sufficient memory bandwidth to feed 64 DSP units. For $N=64$, each $\mathbf{W}^{(k)}$ matrix is 16 KB. Can the FPGA's memory bandwidth sustain 20 pipeline stages at 500 MHz?

---

## Minor Issues

### Hardware Analysis
- Table 14: Add a column for "Memory (KB)" to show the storage requirements for each method.
- Table 15: Add a row for $N=512$ to show the scaling trend more clearly.
- Section 4.13.4: Clarify whether the 64 DSP units assumption is for a mid-range or high-end FPGA.

### Figures and Tables
- Figure 1 (NMSE vs SNR): Add a horizontal line at $-25$~dB to visually highlight the saturation level.
- Table 6 (Runtime): Add a column for "FLOPs per estimate" to connect with the theoretical analysis in Table 14.

### Terminology
- Section 4.13.2: "intra-layer parallelism" — consider "within-layer parallelism" for clarity.
- Section 4.13.4: "pipeline steady-state" — define this term for readers unfamiliar with pipeline architecture.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 64 | Adequate | The BER-NMSE mechanism analysis is novel. The hardware analysis is comprehensive but based on theoretical estimates. |
| Methodological Rigor (25%) | 70 | Strong | Comprehensive experiments with good statistical practices. Hardware analysis lacks measured results. |
| Evidence Sufficiency (25%) | 66 | Adequate | NMSE and BER evidence is strong. Hardware evidence is theoretical. Power consumption not discussed. |
| Argument Coherence (15%) | 72 | Strong | The systems-level argument (BER > NMSE for deployment decisions) is well-constructed. |
| Writing Quality (15%) | 74 | Strong | Clear, professional prose. Hardware analysis is well-organized. |
| Significance & Impact | 70 | Adequate | Practical deployment framework is actionable. Hardware claims need measured validation. |
| **Weighted Average** | **68.9** | **Minor Revision** | |

---

## Overall Score: 69/100
