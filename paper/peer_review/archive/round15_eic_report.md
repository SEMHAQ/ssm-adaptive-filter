# Peer Review Report — EIC

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 15

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC)

### Reviewer Identity
Prof.~Dr.~Maria Torres, Editor-in-Chief, *Digital Signal Processing* (Elsevier). Specialization: computational methods for signal processing, sparse representation, and deep learning for communications. 20+ years of editorial experience in signal processing journals. Review philosophy: prioritize papers that provide genuine insight into *why* methods work (or fail), not just benchmark comparisons.

### Review Focus
Journal fit, originality, overall significance, structural coherence, and strategic value for the DSP readership. I will not delve into deep methodological details (Reviewer 1's domain) but will assess whether the paper tells a compelling story.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 — This paper falls squarely within signal processing and sparse recovery, areas I know well. The deep unfolding and channel estimation components are within my expertise, though some of the AMP-theoretic connections are at the boundary.

### Summary Assessment
This manuscript presents a systematic analysis of LISTA (Learned ISTA) applied to sparse channel estimation, with a focus on understanding *why* LISTA behaves as it does rather than claiming architectural novelty. The paper is well-structured and unusually honest about LISTA's limitations: it clearly states that LISTA trails OMP by 13--33 dB in NMSE and FISTA by 1--27 dB, and that the primary value lies in the "error concentration mechanism" rather than raw estimation accuracy. The ablation study with 20 seeds and Holm--Bonferroni correction is methodologically sound, and the mechanism analysis connecting error concentration to BER performance under ZF equalization is genuinely insightful. The FISTA comparison and LISTA-CP analysis add valuable context.

However, the paper has a narrative tension: it positions LISTA as useful for channel estimation while simultaneously showing it is outperformed by simpler methods on the primary metric (NMSE). The error concentration story is interesting but narrow in scope (ZF + 16-QAM only). The paper would benefit from a tighter framing that honestly acknowledges this tension in the abstract and introduction rather than burying it. The target journal (Digital Signal Processing) is appropriate, and the paper's analytical approach fits the journal's emphasis on understanding signal processing methods. I recommend Minor Revision.

---

## Strengths

### S1: Exemplary Honesty About Limitations
The paper is remarkably transparent about LISTA's shortcomings. Table 1 clearly shows LISTA trailing OMP by 13--33 dB at high SNR, and the authors explicitly state: "LISTA's value lies not in NMSE superiority... but in the error concentration mechanism" (Section 4.12). The FISTA comparison (Table 13) further strengthens this honesty by showing FISTA outperforms LISTA at all SNR levels. This level of candor is rare and commendable.

### S2: Mechanism Analysis with ISTA Control Experiment
The error concentration analysis (Section 4.12) is the paper's strongest contribution. The ISTA control experiment (Table 11) is particularly well-designed: it disentangles the contribution of soft-thresholding (generic, 92.4%) from LISTA's learned parameters (enhanced to 100.0%). The quantitative characterization (267x less non-support error than OMP, 379x less than ISTA) is compelling and provides genuine insight into deep unfolding behavior.

### S3: Rigorous Statistical Methodology
The ablation study escalation from 5 seeds to 20 seeds (Section 4.11) demonstrates intellectual integrity. The authors discovered that their initial 5-seed ablation was underpowered (15--20% power for medium effects) and honestly reported the false negative. The 20-seed follow-up with Holm--Bonferroni correction and Cohen's $d$ effect sizes meets high statistical standards. The BER simulations with 200 realizations and paired $t$-tests are similarly rigorous.

### S4: Comprehensive Generalization Analysis
The paper systematically evaluates generalization across sparsity mismatch, SNR mismatch, channel length variation, ITU channel models, and pilot ratio sensitivity. The cross-table consistency note (Section 4.3) transparently explains the 8 dB difference between independently trained models. This thoroughness provides practitioners with actionable deployment guidance.

### S5: Practical Deployment Framework
Section 5.3 provides a clear decision framework for practitioners: when to use LISTA (throughput-critical, known SNR), when to prefer OMP/FISTA (NMSE-critical), and how to configure training. The SNR-specific training mitigation (6 dB improvement) is practically valuable.

---

## Weaknesses

### W1: Narrative Tension Between Title/Abstract and Actual Findings
**Problem**: The title ("Systematic Analysis of Deep-Unfolded LISTA") and abstract position LISTA as a method worth analyzing for channel estimation, yet the paper's own results show it is consistently outperformed by both OMP (13--33 dB) and FISTA (1--27 dB) on the primary metric. The abstract leads with the error concentration mechanism, which is interesting but narrow in practical scope (ZF equalization + 16-QAM only).
**Why it matters**: Readers scanning the abstract may form an inflated impression of LISTA's practical value. The "error concentration" finding, while insightful, has limited practical impact since MMSE equalization (the standard) masks the advantage entirely.
**Suggestion**: Restructure the abstract to lead with a more balanced framing: "We show that LISTA trails OMP and FISTA in NMSE but exhibits a distinctive error concentration mechanism that provides BER benefits under specific equalization conditions." This sets accurate expectations upfront.
**Severity**: Major

### W2: Limited Practical Impact of the Error Concentration Finding
**Problem**: The error concentration mechanism is the paper's primary contribution, but its practical scope is narrow. Under MMSE equalization (the standard in modern receivers), all estimators achieve similar BER at SNR ≥ 5 dB ($p > 0.05$). The ZF advantage applies only to 16-QAM at SNR ≥ 15 dB. The paper acknowledges this but the highlights box still presents it as a major finding.
**Why it matters**: The readership of *Digital Signal Processing* will want to know: "Should I use LISTA for my channel estimation problem?" The honest answer, based on the paper's own results, is "probably not, unless you have a specific throughput requirement and are using ZF equalization with 16-QAM."
**Suggestion**: Add a concise "Practical Implications" box or paragraph early in the paper that clearly states the conditions under which LISTA is (and is not) advantageous. Move the ZF/16-QAM finding from a "highlights" position to a "nuance" position.
**Severity**: Major

### W3: Missing Hardware Validation
**Problem**: The theoretical hardware complexity analysis (Section 4.13) correctly notes that all FLOP counts are theoretical and no FPGA/ASIC measurements are presented. The pipelining advantage is explicitly called "an unvalidated hypothesis." Yet the highlights box lists "potential hardware pipelining" as a value proposition.
**Why it matters**: Without measured hardware results, the complexity comparison is incomplete. The paper's own analysis shows LISTA requires 2.3x more FLOPs than OMP, so the pipelining hypothesis needs to overcome a per-estimate cost deficit.
**Suggestion**: Either (a) remove hardware pipelining from the highlights and relegate it to future work, or (b) add a brief theoretical argument quantifying the pipelining throughput advantage (e.g., pipeline depth × clock rate comparison) to make the hypothesis more concrete.
**Severity**: Minor

### W4: The AMP Connection Is Speculative
**Problem**: Section 5.1 argues that LISTA's learned $\mathbf{W}^{(k)}$ "implicitly approximate the Onsager correction" from AMP theory. This is an interesting hypothesis but is presented without formal derivation or empirical validation (e.g., comparing the learned $\mathbf{W}^{(k)}$ against the theoretical Onsager correction matrix).
**Why it matters**: The AMP connection elevates the paper from empirical analysis to theoretical contribution, but only if substantiated. In its current form, it reads as post-hoc rationalization.
**Suggestion**: Either (a) add an experiment comparing learned $\mathbf{W}^{(k)}$ against the theoretical Onsager correction, or (b) soften the language to "we hypothesize that" and present it as future work rather than a finding.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is accurate but long. Consider: "Deep-Unfolded LISTA for Sparse Channel Estimation: Error Concentration, Generalization, and Ablation" (shorter, punchier).
- Abstract is dense (250+ words in a single paragraph). Consider breaking into structured segments or trimming by 20%.
- The highlights box items 1 and 2 present the same finding (error concentration) from different angles; consolidate.

### Introduction
- The 6 enumerated contributions are comprehensive but overlap. Contributions 1 (NMSE saturation), 2 (BER mechanism), and 5 (SNR mitigation) could be merged into a tighter narrative.
- The introduction correctly positions this as "understanding behavior" rather than "claiming novelty," which is appropriate.

### Literature Review
- Coverage is thorough. The deep unfolding, CNN/Transformer, and classical adaptive filtering sections are well-organized.
- The qualitative comparison with CNN/Transformer (Table 17) is useful but could be strengthened with a sentence acknowledging the limitations of indirect comparison.

### Methodology
- LISTA architecture description is clear and well-formulated.
- The parameter analysis ($N_{\text{params}} = L \times (N^2 + 2)$) is straightforward.
- Training protocol is well-specified (mixed SNR, cosine annealing, gradient clipping).

### Results
- 12 experiments is comprehensive, perhaps overly so. Some experiments (e.g., Experiment 3 channel length) could be consolidated.
- Tables and figures are well-formatted. The cross-table consistency note is a nice touch.
- The pilot ratio analysis (Table 6) is particularly useful for practitioners.

### Discussion
- The discussion is thorough and honest. The "When is ZF equalization relevant?" paragraph is well-argued.
- The comparison with deep learning baselines (Section 5.2) is appropriately qualified as indirect.

### Conclusion
- Conclusion accurately summarizes findings without over-claiming.
- The future work directions are concrete and actionable.

### References
- References are comprehensive and current (up to 2024).
- Citation format appears consistent with Elsevier style.

---

## Questions for Authors

1. **On the AMP connection**: Can you provide empirical evidence that the learned $\mathbf{W}^{(k)}$ matrices approximate the Onsager correction? For example, computing $\|\mathbf{W}^{(k)} - \mathbf{W}_{\text{Onsager}}^{(k)}\|_2$ at each layer would significantly strengthen Section 5.1.

2. **On practical deployment**: Given that LISTA trails OMP by 13--33 dB and FISTA by 1--27 dB in NMSE, and that the BER advantage only manifests under ZF equalization with 16-QAM, what is the realistic deployment scenario where a practitioner should choose LISTA over FISTA? Can you quantify the pipelining throughput advantage more precisely?

3. **On the SNR saturation**: You argue the saturation is a training artifact. Have you tried training with a curriculum learning strategy (e.g., starting with low SNR and gradually increasing)? This would provide additional evidence for or against the training artifact hypothesis.

---

## Minor Issues

### Language / Grammar
- Abstract, line 1: The sentence "LISTA's NMSE saturates at approximately $-25$ dB for SNR $\geq 10$ dB, trailing OMP by 13--33 dB and FISTA by 1--27 dB" is grammatically correct but could be clearer: "LISTA's NMSE saturates at approximately $-25$ dB for SNR $\geq 10$ dB; OMP outperforms it by 13--33 dB and FISTA by 1--27 dB."
- Section 4.12, paragraph 3: "The negligible standard deviations across 5 seeds ($<0.02\%$ for LISTA)" — specify that this is for the "Error on $\bar{S}$" metric.

### Figures and Tables
- Table 1: Consider adding a column for FISTA to enable direct comparison with the FISTA-focused results later.
- Figure 1: The NMSE vs SNR plot would benefit from a zoomed inset showing the high-SNR region where LISTA saturates.

### Layout
- The paper is well-formatted for the CAS template. No layout issues noted.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 68 | Adequate | The error concentration mechanism is a genuine insight, but LISTA itself is not novel; the contribution is analytical, not architectural |
| Methodological Rigor (25%) | 82 | Strong | Excellent statistical methodology (20 seeds, Holm--Bonferroni, effect sizes, 200 BER realizations); minor gap in hardware validation |
| Evidence Sufficiency (25%) | 80 | Strong | 12 experiments, comprehensive generalization analysis; AMP connection lacks empirical support |
| Argument Coherence (15%) | 75 | Strong | Clear logical flow but narrative tension between honest limitations and "highlights" positioning |
| Writing Quality (15%) | 78 | Strong | Professional academic prose; some dense passages in abstract and mechanism analysis |
| **Weighted Average** | **77.0** | **Minor Revision** | |

---

## Recommendation to Peer Reviewers

I ask Reviewers 1--3 to pay particular attention to:
1. The statistical methodology — is the 20-seed ablation with Holm--Bonferroni correction sufficient? Are there additional robustness checks needed?
2. The AMP theoretical connection — is the argument in Section 5.1 substantiated or speculative?
3. The practical deployment guidance — is the decision framework in Section 5.3 actionable and complete?
