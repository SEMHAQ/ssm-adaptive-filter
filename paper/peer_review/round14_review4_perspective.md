# Peer Review Report — Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 14

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Cross-disciplinary Perspective)

### Reviewer Identity
Dr.~Mehmet Akçakaya, Associate Professor of Electrical and Computer Engineering, University of Pittsburgh. Expertise in compressed sensing for MRI, deep learning for inverse problems, and hardware-efficient inference architectures. Cross-disciplinary perspective bridging medical imaging, communications, and machine learning. Review focus: cross-disciplinary connections, practical deployment implications, and broader impact of the findings.

### Review Focus
Cross-disciplinary applicability of the error concentration mechanism, practical deployment considerations, hardware implementation feasibility, and broader impact on the deep unfolding paradigm beyond channel estimation.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
4 — Mostly within my area of expertise, high confidence.

### Summary Assessment
This manuscript provides a detailed analysis of LISTA for sparse channel estimation, with the novel finding that LISTA concentrates estimation error on true tap locations ($99.9\%$). The paper is well-written and methodologically sound, with comprehensive experiments and honest reporting of limitations. From a cross-disciplinary perspective, the error concentration mechanism has potential implications beyond channel estimation---in compressed sensing MRI, radar, and other sparse recovery applications---but the paper does not explore these connections. The hardware complexity analysis (Section 4.13) is theoretical only, which limits the practical deployment claims. The paper would benefit from: (1) discussing whether the error concentration mechanism generalizes to other sparse recovery domains, (2) providing more concrete hardware deployment guidance, and (3) addressing the scalability limitations more thoroughly. Despite these gaps, the paper makes a valuable contribution to understanding deep-unfolded architectures and is suitable for *Digital Signal Processing* with minor revisions.

---

## Strengths

### S1: Mechanism Analysis with Cross-Domain Implications
The error concentration finding (Section 4.12) has implications beyond channel estimation. In compressed sensing MRI, where reconstruction errors on non-support locations can create artifacts that are clinically significant, a network that concentrates errors on true support locations would be highly desirable. The paper's finding that this property generalizes to ITU channels ($99.3$--$99.5\%$) and higher sparsity ($K=10$, $99.2\%$) suggests it may be a general property of soft-thresholding-based deep unfolding, which could benefit multiple application domains.

### S2: Practical Deployment Decision Framework
Section 5.3 provides a clear, actionable decision framework for practitioners: (1) throughput-critical applications should consider LISTA, (2) known operating SNR should use SNR-specific training, (3) variable SNR should use broad-range training, (4) when NMSE is primary metric, use OMP/FISTA. This practical guidance is valuable and often missing from academic papers.

### S3: Honest Assessment of Hardware Claims
The paper is commendably transparent about the gap between theoretical FLOP analysis and actual hardware performance. The statement "All hardware complexity values are theoretical FLOP counts; measured FPGA/ASIC latency, throughput, and power consumption remain future work" (Section 4.13) is repeated multiple times. The discussion of why the Python speedup ($33\times$) does not reflect algorithmic efficiency is particularly important for preventing misinterpretation.

### S4: SNR Saturation Mitigation as Practical Contribution
The SNR-specific training results (Table 9) are practically valuable. The finding that training on $[15, 25]$~dB achieves $-31$~dB (vs.~$-25$~dB with broad-range training) provides a concrete, actionable recommendation for practitioners who know their operating SNR.

---

## Weaknesses

### W1: No Discussion of Cross-Domain Generalizability
**Problem**: The error concentration mechanism is presented solely in the context of channel estimation. However, the same mechanism would apply to any sparse recovery problem where soft-thresholding is used (e.g., compressed sensing MRI, radar imaging, spectroscopy). The paper does not discuss whether these findings generalize to other domains.
**Why it matters**: The paper's contribution would be significantly strengthened if the mechanism analysis were framed as a general property of deep-unfolded soft-thresholding architectures, rather than a channel-estimation-specific finding.
**Suggestion**: Add a brief discussion in Section 5.1 or 5.3 noting that the error concentration mechanism may generalize to other sparse recovery domains (MRI, radar, etc.) and that this is an interesting direction for future work. If possible, cite relevant work from these domains.
**Severity**: Minor

### W2: Hardware Complexity Analysis Lacks Concrete Guidance
**Problem**: The hardware analysis (Section 4.13) provides FLOP counts but no concrete deployment guidance. The paper states that LISTA's "regular computation graph may facilitate hardware pipelining" but acknowledges this is "an unvalidated hypothesis." Without measured results, the hardware section reads as speculative.
**Why it matters**: For practitioners considering LISTA deployment, FLOP counts alone are insufficient. They need guidance on memory requirements, latency, throughput, and power consumption.
**Suggestion**: Either (a) provide a more detailed theoretical analysis of memory bandwidth, latency, and throughput based on the FLOP counts and typical FPGA/ASIC specifications, or (b) significantly shorten the hardware section and reframe it as "complexity analysis" rather than "hardware deployment."
**Severity**: Minor

### W3: Scalability Concerns Not Adequately Addressed
**Problem**: The paper reports training divergence at $N=256$ (Table 2) and notes that the $O(N^2)$ parameter count of $\mathbf{W}^{(k)}$ is a scalability concern (Section 3.4). However, it does not provide concrete solutions or even estimates of when structured mappings (Toeplitz, circulant, low-rank) would be needed.
**Why it matters**: Many practical channel estimation problems involve $N \geq 128$ (e.g., 5G NR with large delay spreads). The paper's analysis is limited to $N \leq 128$, which may not cover all practical scenarios.
**Suggestion**: Add a brief analysis of parameter scaling with structured mappings. For example, a Toeplitz $\mathbf{W}^{(k)}$ would have $2N-1$ parameters instead of $N^2$, reducing the total from $82$K to $\sim$2.6K for $N=64$. Discuss the expected accuracy tradeoff.
**Severity**: Minor

### W4: Limited Discussion of Online/Adaptive Deployment
**Problem**: The paper focuses on batch training and static deployment. However, many practical channel estimation scenarios require online adaptation to time-varying channels. The paper does not discuss whether LISTA can be adapted online (e.g., via fine-tuning on recent observations) or whether it is inherently a batch method.
**Why it matters**: For time-varying channels (e.g., vehicular communications), a static LISTA model may be inadequate. The classical LMS/NLMS baselines adapt online, which is a practical advantage not captured by the NMSE comparison.
**Suggestion**: Add a brief discussion in Section 5.3 noting that LISTA requires offline training and does not adapt online, unlike LMS/NLMS. Discuss whether incremental fine-tuning is feasible and what the expected latency would be.
**Severity**: Minor

---

## Detailed Comments

### Cross-Disciplinary Connections
- The paper does not explicitly connect to compressed sensing in other domains (MRI, radar, spectroscopy). This is a missed opportunity.
- The error concentration mechanism could be framed as a general property of learned soft-thresholding, with implications for any sparse recovery application.
- The hardware analysis could connect to the FPGA/ML accelerator literature beyond channel estimation.

### Practical Applications
- The deployment decision framework (Section 5.3) is practical and well-reasoned.
- The SNR-specific training recommendation is actionable.
- The FISTA comparison provides clear guidance: "for NMSE, use FISTA; for error concentration, use LISTA."

### Broader Impact
- The paper's honest assessment of LISTA's limitations is a positive contribution to the field.
- The mechanism analysis advances understanding of deep-unfolded architectures.
- The practical deployment guidance benefits practitioners.

### Fundamental Assumptions
- The paper assumes BPSK pilots and real-valued channels. Extension to complex-valued channels (standard in communications) is mentioned as future work but not discussed.
- The paper assumes perfect synchronization and no inter-symbol interference. These are standard assumptions but should be acknowledged.

---

## Questions for Authors

1. Does the error concentration mechanism generalize to other sparse recovery domains (e.g., compressed sensing MRI, radar imaging)? If so, this would significantly broaden the paper's impact.

2. For the hardware analysis, can you estimate the latency and throughput of LISTA on a typical FPGA (e.g., Xilinx UltraScale+) based on the FLOP counts and memory bandwidth? Even a rough estimate would be more informative than FLOP counts alone.

3. The paper focuses on static channels. For time-varying channels (e.g., vehicular communications at 100~km/h), how frequently would LISTA need to be re-trained? Is online fine-tuning feasible?

4. Have you considered using structured linear mappings (Toeplitz, circulant, low-rank) for $\mathbf{W}^{(k)}$ to improve scalability to $N \geq 256$? What accuracy tradeoff would you expect?

---

## Minor Issues

### Literature
- Consider citing recent work on hardware-efficient deep unfolding (e.g., quantized LISTA, binary LISTA) for resource-constrained deployment.
- The paper cites \citet{wei2022fpga} for FPGA implementation but does not discuss the specific hardware architecture used.

### Figures and Tables
- Table 2 (channel length): The divergence at $N=256$ is important but buried in a footnote. Consider highlighting it more prominently.
- The deployment decision framework (Section 5.3) would benefit from a flowchart or decision tree figure.

### Writing
- Section 5.1 is long and could be restructured. Consider splitting into "Saturation Analysis" and "BER Implications" subsections.
- The repeated caveat about theoretical FLOP counts is appreciated but becomes verbose. Consider stating it once prominently and referencing it subsequently.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 66 | Adequate | Mechanism analysis is novel; no architectural innovation. Cross-domain potential not explored. |
| Methodological Rigor (25%) | 80 | Strong | Sound experimental design with comprehensive baselines. Hardware analysis is theoretical only. |
| Evidence Sufficiency (25%) | 76 | Strong | Comprehensive experiments within channel estimation. No cross-domain validation. |
| Argument Coherence (15%) | 80 | Strong | Clear logical flow. The BER-NMSE disconnect is well-explained. |
| Writing Quality (15%) | 80 | Strong | Professional prose. Some verbosity in hardware caveats. |
| Significance & Impact | 72 | Adequate | Impact limited to channel estimation domain. Cross-domain implications not explored. |
| **Weighted Average** | **76.4** | **Minor Revision** | |

---

