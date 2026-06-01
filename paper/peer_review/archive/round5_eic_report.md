# Peer Review Report — Editor-in-Chief

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 5

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC), Digital Signal Processing (Elsevier)

### Reviewer Identity
Prof.~Dr.~Maria Schmidt, Editor-in-Chief of *Digital Signal Processing*, with 25 years of experience in adaptive signal processing, compressed sensing, and sparse recovery algorithms. Specialist in bridging theoretical signal processing with practical communication system design. Has edited >200 papers on deep unfolding and model-based deep learning for physical-layer processing.

### Review Focus
Journal fit, originality, overall quality, significance to the DSP readership, and whether the paper advances the field in a meaningful way. I do not go deep into methodology (that is Reviewer 1's job) but assess whether the contribution is substantial enough for publication.

---

## Overall Assessment

### Recommendation
- [ ] **Accept**
- [x] **Minor Revision**
- [ ] **Major Revision**
- [ ] **Reject**

### Confidence Score
4 — Mostly within my area of expertise. Deep unfolding for channel estimation is squarely within DSP's scope, and I have high confidence in assessing the contribution level, though some of the BER analysis details are better evaluated by the methodology reviewer.

### Summary Assessment

This manuscript provides a systematic analysis of LISTA applied to sparse channel estimation, with emphasis on practical deployment characteristics. The paper is well-structured and addresses a relevant topic for the DSP readership. The most notable contribution is the BER-NMSE disconnect analysis (Experiment 12), which demonstrates that LISTA's 13--33~dB NMSE gap with OMP does not translate to a BER penalty, with mechanism analysis showing LISTA concentrates 99.9\% of estimation error on true tap locations. This is a genuinely useful finding for the communications community.

However, the paper has a fundamental positioning tension: it simultaneously acknowledges LISTA's significant NMSE disadvantage while arguing for practical relevance through BER performance. The argument is convincing for QPSK and 16-QAM under ZF equalization, but the MMSE results (Table 11) show the advantage largely vanishes under the more practical equalizer. The paper's hardware throughput claims ($4.4\times$) are theoretically sound but lack measured FPGA results. The ablation study with 20 seeds is commendable for statistical rigor. The paper is suitable for DSP after addressing several clarifications requested by the reviewers.

---

## Strengths

### S1: BER-NMSE Disconnect Analysis with Mechanism Insight
The paper's strongest contribution is the systematic analysis of why LISTA achieves competitive BER despite worse NMSE. The three-mechanism analysis (support recovery, error sparsity, noise enhancement) in Experiment 12 is well-designed and provides genuine insight. Table 13's finding that LISTA concentrates 99.9\% of error on true taps (vs.~94.9\% for OMP) with $50\times$ less non-support error is a clean, interpretable result that explains the BER-NMSE disconnect. This mechanism analysis elevates the paper beyond a simple benchmarking exercise.

### S2: Statistical Rigor in BER Validation
The use of 200 channel realizations per SNR point with paired $t$-tests and 95\% confidence intervals (Section 4.10) represents a significant improvement over typical signal processing papers that report BER without statistical validation. The explicit reporting of $p$-values and significance levels (Tables 8--9) allows readers to assess the reliability of the BER claims. This level of statistical rigor should be a model for the field.

### S3: Comprehensive Ablation with Sufficient Statistical Power
The progression from 5-seed to 20-seed ablation (Sections 4.5 and 4.11) is commendable. The paper honestly reports that the 5-seed analysis produced false negatives for the threshold and per-layer parameters, and corrects this with the 20-seed study. The Cohen's $d$ effect sizes ($d = 18.4$ for threshold, $d = 24.1$ for shared parameters) leave no doubt about the significance of these components. This transparency about statistical power limitations is rare and valuable.

### S4: Practical Deployment Analysis
The combination of FLOPs analysis (Table 14), memory access patterns, pipeline timing estimates, and scaling analysis (Table 15) provides a comprehensive practical assessment. The explicit caveat about Python speedup vs.~hardware throughput (Section 4.7.1) shows intellectual honesty. The recommendation framework in Section 5.2 is actionable for practitioners.

---

## Weaknesses

### W1: Positioning Tension — NMSE Gap Acknowledgment vs.~Practical Claims
**Problem**: The paper simultaneously acknowledges a 13--33~dB NMSE gap with OMP and argues for LISTA's practical relevance. While the BER analysis convincingly shows no BER penalty for QPSK, the MMSE results (Table 11) demonstrate that the advantage largely vanishes under MMSE equalization, which is the standard in modern receivers. The paper acknowledges this but then continues to emphasize the ZF-based BER advantage in the abstract and highlights.
**Why it matters**: Readers may be confused about when LISTA is actually preferable to OMP. The paper's practical recommendation (Section 5.2) is nuanced, but the abstract and highlights present a simpler picture.
**Suggestion**: Revise the abstract and highlights to explicitly state that the BER advantage is primarily under ZF equalization, and that under MMSE, LISTA's primary advantage is the $4.4\times$ hardware throughput with no BER penalty (rather than better BER). This is already discussed in Section 5.1 but needs to propagate to the abstract.
**Severity**: Major

### W2: Hardware Claims Lack Measured Results
**Problem**: The $4.4\times$ throughput advantage and $1.2$~$\mu$s FPGA latency are theoretical estimates based on 64 DSP units at 500~MHz (Section 4.13.4). No actual FPGA implementation or measurement is provided. While the estimates align with \citet{wei2022fpga}'s results, the paper presents these as established facts in the abstract ("enables 20-stage pipelining with an estimated 4.4$\times$ throughput advantage") without sufficient qualification.
**Why it matters**: Hardware claims based on theoretical estimates carry less weight than measured results. Reviewers and readers may question the practical achievability of these numbers.
**Suggestion**: Either (a) add "theoretical estimate" or "projected" qualifiers to all hardware claims in the abstract and highlights, or (b) soften the claims by noting that actual FPGA implementation may differ due to memory bandwidth, control overhead, and resource sharing. The current phrasing "enables 20-stage pipelining" sounds like a demonstrated capability.
**Severity**: Minor

### W3: Abstract Length and Density
**Problem**: The abstract is 298 words (excluding LaTeX commands), which exceeds the typical 150--200 word limit for DSP papers. It contains excessive numerical detail (e.g., "760K FLOPs ($2.3\times$ OMP, $8.7\times$ less than LASSO)", "82K parameters fit in L2 cache") that belongs in the main text rather than the abstract.
**Why it matters**: Dense abstracts reduce readability and may violate journal formatting guidelines. Key findings get buried in numbers.
**Suggestion**: Reduce the abstract to ~200 words by removing specific numerical details (FLOP counts, parameter counts, pipeline stages) and focusing on the key findings: LISTA's BER comparability, the mechanism insight, and the hardware throughput advantage.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- The title is accurate and descriptive. "Analysis" correctly positions this as an analytical study rather than a methodological contribution.
- The abstract needs trimming (see W3). The highlights section is also dense; consider reducing from 6 to 4 items.

### Introduction
- Well-structured with clear contributions listed. The 6 contributions are comprehensive but may overwhelm readers. Consider grouping into 3--4 higher-level contributions.
- The motivation for studying LISTA specifically (rather than newer variants) is adequately justified in Section 2.

### Literature Review
- Comprehensive coverage of deep unfolding, sparse channel estimation, and hardware deployment literature. The differentiation from prior work (Section 2, paragraph before Section 2.4) is clear.
- The paper correctly positions itself as an analytical study rather than claiming architectural novelty.

### Methodology
- The LISTA architecture is standard and well-described. The FFT-based convolution detail (Eq.~7) is a useful implementation note.
- The training procedure (mixed SNR, cosine annealing, gradient clipping) is well-specified and reproducible.

### Results
- The 13 experiments are comprehensive, covering NMSE, BER, ablation, generalization, and hardware analysis.
- The cross-table consistency note (Section 4.3) is an excellent addition that addresses a common reviewer concern.
- Table 7's footnote about the diverged seed at $K=15$ is honest reporting.

### Discussion
- Section 5.1's discussion of MMSE implications is important and well-reasoned.
- The limitation section (5.3) is honest and comprehensive.
- Future research directions are concrete and actionable.

### Conclusion
- The conclusion accurately summarizes findings without overclaiming.
- The final sentence about "speed-critical deployments" appropriately qualifies the practical recommendation.

---

## Questions for Authors

1. **On the MMSE equalization results**: Table 11 shows only 2 SNR points (10 and 20 dB) for the ZF vs.~MMSE comparison. Can you provide a full SNR sweep (0--30 dB) for MMSE equalization to clarify at which SNR regimes LISTA's BER advantage persists under MMSE? This would significantly strengthen the practical deployment argument.

2. **On LISTA-CP identical performance**: You report that LISTA and LISTA-CP achieve identical performance because the weight clipping constraint is naturally satisfied (spectral norm 0.34 < 1.0). Did you verify this across all training seeds, or only the final trained model? If the constraint is always satisfied, what does this imply about the tightness of LISTA-CP's convergence guarantees for this problem class?

3. **On the abstract's hardware claims**: The abstract states "enables 20-stage pipelining with an estimated 4.4$\times$ throughput advantage." Given that no FPGA implementation is provided, would you consider qualifying this as a "theoretical estimate" or "projected advantage" in the abstract?

---

## Minor Issues

### Language / Grammar
- Section 4.3, p.~8: "The channel-length training distribution is narrower and more focused" — "narrower" is ambiguous (narrower in what dimension?). Suggest: "The channel-length training distribution covers a narrower range of $N$ values."
- Section 5.1, p.~14: "the BER advantage should be interpreted with care for systems employing MMSE equalization" — "with care" is vague. Suggest: "the BER advantage is attenuated under MMSE equalization."

### Figures and Tables
- Table 5 (Ablation, 5 seeds): The "Fixed threshold" row shows $\Delta = -0.26$~dB (improvement), which is counterintuitive. Add a footnote explaining that this is within noise and the 20-seed study (Table 10) corrects this.
- Table 11 (ZF vs.~MMSE): Expand to include more SNR points for completeness.

### Layout
- The highlights section has 6 items; DSP typically expects 3--5. Consider consolidating.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 62 | Adequate | LISTA is well-known; the contribution is analytical insight, not architectural novelty. The BER-NMSE mechanism analysis is novel. |
| Methodological Rigor (25%) | 74 | Strong | Comprehensive experiments with statistical validation. The 200-realization BER study and 20-seed ablation are commendable. Some concerns about hardware claims lacking measurements. |
| Evidence Sufficiency (25%) | 72 | Strong | 13 experiments cover NMSE, BER, ablation, generalization, and hardware. ITU channel validation adds realism. MMSE results are limited (2 SNR points). |
| Argument Coherence (15%) | 70 | Adequate | The BER-NMSE disconnect argument is well-constructed. The positioning tension between acknowledging NMSE gap and claiming practical relevance creates some narrative friction. |
| Writing Quality (15%) | 73 | Strong | Clear, professional academic prose. Some density in abstract and highlights. Section organization is logical. |
| **Weighted Average** | **70.3** | **Minor Revision** | |

---

## Overall Score: 70/100
