# Editorial Decision Package

**Paper:** "Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation"
**Author:** Huanjie Yu, Hunan University of Technology and Business
**Journal:** Digital Signal Processing (Elsevier)
**Date:** 2026-06-01

---

## 1. Decision

**Major Revision**

The paper presents a methodologically rigorous analysis with genuine contributions (error concentration mechanism, exemplary statistical methodology, honest reporting of limitations). However, the paper's central claim -- that the 100.0% error concentration on true taps constitutes a meaningful mechanism insight -- has been challenged by multiple reviewers as potentially a trivial consequence of the soft-thresholding operator. Resolving this challenge requires substantive new experiments (pre-thresholding analysis, learned threshold reporting, verification of zero non-support entries) that go beyond text revisions. Additionally, the absence of any deep learning baselines, the real-valued-only channel model, and the narrow practical scope (ZF-only BER advantage) require either new experiments or significant narrowing of claims. Two of four substantive reviewers (R2, R3) recommend Major Revision. The Devil's Advocate identified critical issues with the core finding that must be addressed before the paper's contribution can be properly evaluated.

---

## 2. Reviewer Summary Table

| Reviewer | Role | Recommendation | Score | Confidence |
|----------|------|---------------|:-----:|:----------:|
| EIC | Editor-in-Chief | Minor Revision | 73/100 | 4/5 |
| R1 | Methodology Expert | Accept with Minor Revisions | 76/100 | Not stated |
| R2 | Domain Expert (Sparse Recovery, Deep Unfolding) | Revise and Resubmit | 60/100 | Not stated |
| R3 | Cross-disciplinary (ML, HW, Info Theory) | Major Revision | 62/100 | 4/5 |
| Devil's Advocate | Critical Analysis | Implicit Reject | N/A | N/A |

**Weighted Recommendation:** Major Revision (2 Minor, 2 Major, 1 Implicit Reject)

---

## 3. Consensus Analysis

### Points of Agreement (CONSENSUS-4: 4 or 5 reviewers agree)

**CA-1. The paper's intellectual honesty and statistical rigor are exemplary.**
All four substantive reviewers commend the transparent reporting of negative results (LISTA trailing OMP/FISTA), the use of Holm-Bonferroni correction, Cohen's d effect sizes, and the escalation from 5-seed to 20-seed ablation. The Devil's Advocate acknowledges this as well (O1, O2). This is the paper's uncontested strength.
*Sources: EIC S1-S3, R1 S1-S3, R2 S1-S3, R3 S1-S3, DA O1-O4.*

**CA-2. The 100.0% +/- 0.0% error concentration claim requires verification.**
Four reviewers independently flagged the zero-variance, exact-100% metric as suspicious. EIC (W4) notes it could be a numerical artifact of aggressive thresholding. R1 (W1) identifies degenerate statistics that prevent valid confidence intervals or hypothesis tests. R2 (W7) questions whether the metric has a ceiling effect. DA (C1) argues it is likely a trivial consequence of soft-thresholding producing near-zero non-support estimates. The convergence of these concerns from reviewers with different expertise (methodology, domain, cross-disciplinary, adversarial) makes this the highest-priority revision item.
*Sources: EIC W4/Q1, R1 W1, R2 W3/W7, R3 W5, DA C1.*

**CA-3. The real-valued channel model severely limits practical relevance.**
Four reviewers identify this as a significant constraint. EIC (W1) notes the error concentration metric, soft-thresholding operator, and NMSE loss are all defined for real-valued signals. R2 (W4) argues the i.i.d. Gaussian model is not representative of wireless channels. R3 (W1) states the complex-valued extension is "a validity condition for the paper's main claims." DA (M4) notes phase errors could reverse the core finding.
*Sources: EIC W1, R2 W4, R3 W1/W6, DA M4.*

**CA-4. The ZF-only BER advantage limits the practical significance of the mechanism analysis.**
Four reviewers note that LISTA's BER advantage manifests only under ZF equalization, which is rarely used in modern receivers. EIC acknowledges MMSE is standard. R2 (W6) quantifies this as a narrow finding. R3 (W4) states ZF is not used even in IoT receivers. DA (C3) notes the BER levels (0.29-0.32) are completely unusable in practice.
*Sources: EIC (implicitly), R2 W6, R3 W4, DA C3.*

**CA-5. Missing CNN/Transformer baselines weaken the paper's positioning.**
Four reviewers request at least one deep learning baseline under identical conditions. EIC (W3) argues this would contextualize LISTA's limitations. R2 (W2) notes a simple 1D CNN could have fewer parameters than LISTA's 82K. R3 (W3) states the parameter count claim (">500K for CNNs") is unsupported. DA notes the absence makes it impossible to assess whether deep unfolding offers any advantage.
*Sources: EIC W3, R2 W2, R3 W3, DA (implicitly).*

### Points of Disagreement with Resolution

**DA-1. Whether the paper requires Minor or Major Revision.**
EIC and R1 recommend Minor Revision; R2 and R3 recommend Major Revision. The Devil's Advocate implicitly rejects.
*Resolution:* Major Revision is warranted because (a) the paper's central contribution (error concentration mechanism) has been challenged as potentially trivial by multiple reviewers, and resolving this challenge requires new experiments, not text edits; (b) R2 and R3 provide detailed, substantive concerns that cannot be addressed by minor changes; (c) the DA's critical issues (C1, C4) are shared by other reviewers and require analytical work to resolve.

**DA-2. Whether the error concentration mechanism is a genuine finding or a trivial artifact.**
R1 (S2) and R3 (S2) view it as a genuine contribution. DA (C1) and R2 (W3) view it as potentially trivial.
*Resolution:* The finding is potentially valuable but unverified. The revision must include pre-thresholding error concentration analysis and reporting of learned thresholds to determine whether the mechanism is genuine. If pre-thresholding concentration is already high, the finding is less novel; if it is low and only becomes 100% after thresholding, the finding is an artifact of the operator, not the learned parameters. The paper cannot be accepted until this is resolved.

**DA-3. Whether the FISTA comparison is fair.**
R1 (W7) and DA (C4) argue FISTA's per-SNR grid search gives it an unfair advantage over LISTA's mixed-SNR training. R2 (W6) and EIC (W2) view the comparison as informative but note it undermines the paper's premise.
*Resolution:* The comparison is informative but asymmetric. The revision should include a fairer comparison mode (e.g., LISTA with SNR-specific training vs. FISTA with single fixed threshold) or explicitly acknowledge the asymmetry and its implications.

**DA-4. Whether the statistical power concern applies beyond the ablation.**
R1 (W4) and DA (M1) note that 5 seeds are insufficient for most experiments, not just the ablation. EIC and R2 do not flag this for non-ablation experiments.
*Resolution:* The concern is valid but secondary. The paper correctly escalated the ablation to 20 seeds. For other experiments, 5 seeds with paired tests may be sufficient if effect sizes are large (as they appear to be for NMSE vs. OMP). However, the BER experiments at high SNR (low error rates) do need more realizations per point, as R1 (W4) notes.

---

## 4. Decision Rationale

This paper makes a genuine contribution through its rigorous statistical methodology and its novel attempt to explain the BER-NMSE disconnect in deep-unfolded sparse channel estimation. The intellectual honesty in reporting that LISTA underperforms OMP and FISTA in NMSE is commendable and unusual. The experimental design is comprehensive, covering SNR, sparsity, channel length, depth, pilot ratio, ITU channels, ablation, BER with two equalizers, and FISTA comparison.

However, the paper's central intellectual contribution -- the 100.0% error concentration mechanism -- has been challenged by four of five reviewers as potentially a trivial consequence of the soft-thresholding operator. The zero-variance, exact-100% metric is statistically degenerate and cannot support formal hypothesis testing. Resolving whether this finding is genuine or an artifact requires new analytical work (pre-thresholding analysis, learned threshold reporting, verification of zero non-support entries) that constitutes a substantive revision. Additionally, the paper's practical scope is narrower than presented: the BER advantage operates only under ZF equalization at unusable BER levels (0.29-0.32), and the absence of any deep learning baselines makes it impossible to assess LISTA's position in the broader landscape. The real-valued-only channel model further limits direct applicability to wireless systems. These issues, collectively, require Major Revision to validate the core claims and properly scope the contribution.

---

## 5. Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer(s) | Severity | Section(s) | Estimated Effort |
|---|--------------|-------------------|----------|-----------|-----------------|
| R1 | **Verify error concentration mechanism:** (a) Report learned threshold values theta^(k) for each layer. (b) Compute error concentration on the pre-thresholding intermediate representation (after W^(k)h^(k) - mu^(k)g^(k) but before soft-thresholding). (c) Report the number of non-zero non-support taps in LISTA's estimates to verify whether the 100% is trivially produced by exact-zero outputs. If pre-thresholding concentration is already high, reframe the finding as a generic property of soft-thresholding; if low, demonstrate it is a learned property. | EIC W4/Q1, R1 W1, R2 W3/W7, R3 W5/Q1, DA C1 | Critical | Section 4.12, Tables 10-13 | 1-2 weeks (new experiments + analysis) |
| R2 | **Report the complementary metric as primary:** Present the non-support error fraction (0.01% vs 4.81% for OMP) in log scale or dB as the primary comparison quantity, with a valid statistical test (Wilcoxon rank-sum or permutation test) since the 100% metric has zero variance. Report bootstrap confidence intervals for the 267x ratio. | R1 W1/C1, R2 W7 | High | Section 4.12, Abstract | 3-5 days |
| R3 | **Add at least one CNN baseline:** Implement a 1D CNN (3-4 conv layers, 32-64 channels, <100K parameters) trained on the same data with the same NMSE loss. Report NMSE and error concentration metrics. If implementing a CNN is infeasible, remove the unsupported parameter count claims (line 939: ">500K parameters") and replace with a qualitative discussion citing specific architectures with measured parameter counts. | EIC W3, R2 W2, R3 W3, DA (implicitly) | High | Section 4 (new experiment), Section 5.2 | 2-3 weeks (implementation + training + evaluation) |
| R4 | **Add a complex-valued channel estimation result:** At minimum, provide a supplementary experiment with complex-valued channels and QPSK pilots using magnitude-based soft-thresholding (S_theta(z) = z * max(1 - theta/|z|, 0)). Report whether the error concentration mechanism transfers. This can be in an appendix or supplementary material. | EIC W1, R2 W4, R3 W1, DA M4 | High | Appendix or Supplementary | 1-2 weeks |
| R5 | **Fix data generation description mismatch:** Clarify in Section 4.1 which experiments use which data generation protocol. State explicitly that LISTA training generates fresh data each epoch. Report actual test set sizes (200 for revision experiments, 2000 for original experiments). Also verify and correct the tap amplitude distribution: paper states N(0,1) but code applies exponential decay (`torch.exp(-torch.arange(sparsity).float() * 0.2)`). | R1 W2/M5, DA M5 | Medium | Section 4.1 | 2-3 days |
| R6 | **Fix baseline hyperparameter optimization:** Either (a) generate a separate validation set for baseline hyperparameter selection and evaluate on held-out test data, or (b) state explicitly that baselines are optimized on test data and note this biases results in favor of baselines. | R1 W3 | Medium | Section 4.1, code | 3-5 days |
| R7 | **Specify bits per BER realization:** State explicitly in Section 4.10 how many bits are simulated per channel realization and per SNR point. For high-SNR points (>=25 dB), ensure sufficient bit errors for reliable estimation (at least 100 bit errors per realization). | R1 W4/W5, DA M1 | Medium | Section 4.10 | 1-2 days |
| R8 | **Tighten framing around FISTA's superiority:** Reframe the paper to more clearly acknowledge that FISTA's superiority over LISTA is a central finding, not just a comparison point. Integrate FISTA into all main tables for consistent three-way comparison. Revise the title and abstract to reflect this positioning. | EIC W2/Q2, R2 W6, DA C2 | Medium | Title, Abstract, all Tables | 1 week |
| R9 | **Fix Jaccard index discrepancy:** Line 963 states J=0.78 for LISTA vs J=0.97 for OMP, but Table 7 reports J=0.929 vs J=0.968 at SNR=20 dB. Verify and correct. | EIC (minor issue 6) | Low | Section 5.4 | 1 day |

---

## 6. Suggested Revisions (Should Fix)

| # | Revision Item | Source | Priority | Section(s) | Expected Improvement |
|---|--------------|--------|----------|-----------|---------------------|
| S1 | **Include OCLISTA and/or ALISTA as experimental baselines.** OCLISTA tests whether W^(k) approximates Onsager correction (paper's hypothesis at line 925). ALISTA tests whether learned weights converge to analytically optimal weights. | R2 W1, R3 (Section 6.4) | High | Section 4 (new experiment) | Strengthens positioning within deep unfolding family; tests paper's theoretical hypotheses |
| S2 | **Analyze learned W^(k) matrices:** Report spectral norms, singular value distributions, and check for approximate Toeplitz/banded structure. Visualize how W^(k) - I evolves across layers. | R2 W5, R3 Q2, R3 C3 | High | Section 4 (new analysis) | Significantly strengthens mechanistic interpretation; addresses what LISTA learns |
| S3 | **Report the learned threshold schedule:** Plot theta^(k) vs. layer index k. Determine whether it decreases monotonically, is adaptive, or follows another pattern. | EIC Q1, R1 Q2, R2 Q1, R3 C13 | High | Section 4 (new figure/analysis) | Core insight into what LISTA learns; directly addresses ablation finding |
| S4 | **Add fairer FISTA comparison:** Report LISTA with SNR-specific training vs. FISTA with single fixed threshold for all SNR. This addresses the asymmetry where FISTA gets per-SNR optimization while LISTA uses mixed-SNR training. | R1 W7, DA C4 | Medium | Section 4.12 | Fairer comparison; may narrow the FISTA-LISTA gap |
| S5 | **Implement MSE loss control experiment:** Train LISTA with absolute MSE loss instead of NMSE loss to test whether the saturation is caused by scale invariance. This directly tests the paper's primary hypothesis (line 913). | R3 Q3/C1, DA M2 | Medium | Section 4 (new experiment) | Validates or refutes the "training artifact" hypothesis |
| S6 | **Report false discovery rate and missed detection rate:** Alongside error concentration, report FDR (fraction of estimated non-zero taps that are actually zero) and MDR (fraction of true taps estimated as zero). | R2 W3 | Medium | Section 4.12 | Distinguishes between oracle support selection and aggressive sparsification |
| S7 | **Discuss FISTA in LASSO comparison:** Justify why LASSO uses 500 ISTA iterations while the FISTA baseline uses only 20 iterations. Consider running LASSO with 20 FISTA iterations for consistency. | R2 (Section 4.3) | Low | Section 4.1 | Fairer baseline comparison |
| S8 | **Report training wall-clock time:** State training duration on the specified hardware. Discuss whether 10,000 labeled channel realizations are available in practice. | R3 W7/Q5 | Low | Section 3.5 | Completes cost-benefit analysis for practitioners |
| S9 | **Add LISTA results at deeper configurations (L=50, L=100):** Test whether the FISTA-LISTA gap narrows with more layers, as EIC Q2 suggests. | EIC Q2 | Medium | Section 4.4 | Addresses whether saturation is architectural or depth-limited |
| S10 | **Discuss BER at operationally meaningful levels:** Note that the ZF BER advantage occurs at BER levels (0.29-0.32) that are unusable in practice. If possible, extend BER simulation to lower error rates. | DA C3 | Low | Section 4.10 | More honest assessment of practical significance |
| S11 | **Include BER simulation code in repository.** | R1 W10 | Low | Code repository | Reproducibility |
| S12 | **Add control for BPSK pilot structure:** Run at least the key experiments with QPSK pilots to validate that findings are not artifacts of the binary measurement matrix. | R3 W6 | Medium | Section 4 (new experiment) | Strengthens generalizability claims |
| S13 | **Strengthen the generalizability discussion:** Theoretically analyze whether the error concentration mechanism would apply to other soft-thresholding-based deep-unfolded architectures (ISTA-Net, LISTA-AMP). | EIC W5 | Low | Section 5.1 | Extends mechanism insight beyond LISTA |

---

## 7. Revision Roadmap

### Phase 1: Core Mechanism Validation (Weeks 1-3) -- HIGHEST PRIORITY

**Objective:** Resolve whether the error concentration finding is genuine or an artifact.

1. **Week 1:** Implement pre-thresholding error concentration computation. Extract learned threshold values theta^(k) from trained LISTA models. Count non-zero non-support entries in LISTA's estimates.
2. **Week 2:** Run the pre-thresholding analysis across all seeds. Implement the complementary metric (non-support error fraction in dB) with Wilcoxon rank-sum test and bootstrap confidence intervals.
3. **Week 3:** Analyze results. If pre-thresholding concentration is already high, reframe the finding as generic to soft-thresholding. If low and only 100% after thresholding, reframe as thresholding artifact. If genuinely learned, strengthen the claim with the new evidence.
4. **Deliverable:** Revised Section 4.12 with verified error concentration analysis, learned threshold table/figure, and properly powered statistical tests.

### Phase 2: Missing Baselines (Weeks 2-5) -- HIGH PRIORITY

**Objective:** Add CNN baseline and (if feasible) OCLISTA/ALISTA.

1. **Weeks 2-3:** Implement 1D CNN baseline (3-4 conv layers, 32-64 channels). Train on same data with same NMSE loss.
2. **Week 4:** Evaluate CNN across SNR sweep. Compute error concentration for CNN.
3. **Week 5 (if feasible):** Implement OCLISTA. Compare error concentration against standard LISTA.
4. **Deliverable:** New experiment section with CNN baseline; optional OCLISTA comparison.

### Phase 3: Complex-Valued Extension (Weeks 3-5) -- HIGH PRIORITY

**Objective:** Validate mechanism in complex domain.

1. **Week 3:** Implement complex-valued LISTA with magnitude-based soft-thresholding. Modify data generation for complex channels and QPSK pilots.
2. **Week 4:** Train and evaluate. Run error concentration analysis for complex case.
3. **Week 5:** Analyze results. Determine whether mechanism transfers.
4. **Deliverable:** Appendix or supplementary material with complex-valued results.

### Phase 4: Framing and Presentation (Weeks 5-6) -- MEDIUM PRIORITY

**Objective:** Tighten framing, fix inconsistencies, improve presentation.

1. Revise title and abstract to reflect FISTA's superiority as a central finding.
2. Integrate FISTA into all main tables.
3. Fix data generation description, Jaccard index discrepancy, parameter count arithmetic.
4. Add bits-per-realization specification to BER section.
5. Fix baseline optimization description (test-set vs. validation-set).
6. Add W^(k) analysis (spectral norms, structure).
7. **Deliverable:** Revised manuscript with all text corrections.

### Phase 5: Additional Experiments (Weeks 4-7) -- MEDIUM PRIORITY

**Objective:** Address suggested revisions.

1. MSE loss control experiment (tests scale-invariance hypothesis).
2. Fairer FISTA comparison (SNR-specific LISTA vs. single-threshold FISTA).
3. Deeper LISTA configurations (L=50, L=100).
4. QPSK pilot experiments.
5. Training time reporting.
6. **Deliverable:** Additional tables and analysis as needed.

---

## 8. Revision Deadline

**Deadline:** 2026-09-01 (3 months from decision date)

The 3-month window accounts for the scope of required experiments (new CNN baseline, complex-valued extension, pre-thresholding analysis) and the need for careful statistical analysis. Authors who need additional time should contact the editor before the deadline.

---

## 9. Response Letter Instructions

The response letter must address every Required Revision (R1-R9) and every Suggested Revision (S1-S13) that the authors choose to address. For each item:

1. **State the reviewer concern** in one sentence.
2. **Describe the specific action taken** (new experiment, text change, analysis, etc.).
3. **Provide the evidence** (table, figure, statistical test result, or page/line reference to revised text).
4. **If the concern is not addressed**, explain why and what alternative action was taken.

For the critical revision item R1 (error concentration verification), the response must include:
- The learned threshold values theta^(k) for each layer.
- The pre-thresholding error concentration results.
- The count of non-zero non-support entries in LISTA's estimates.
- A revised interpretation of the error concentration mechanism based on these findings.

For R3 (CNN baseline), if the authors choose not to implement a CNN, they must provide a detailed justification and remove all unsupported parameter count claims.

The response letter should be organized by revision item (R1, R2, ..., R9, S1, S2, ..., S13) with page/line references to the revised manuscript.

---

## 10. Closing

This paper demonstrates commendable intellectual honesty and statistical rigor in its analysis of LISTA for sparse channel estimation. The experimental methodology is among the best I have seen in the deep unfolding literature, and the willingness to report negative results (LISTA trailing OMP and FISTA) strengthens the field's credibility. The error concentration mechanism analysis has the potential to be a genuine contribution to understanding deep-unfolded architectures, but this potential cannot be realized until the finding is verified through the pre-thresholding analysis requested in R1.

The Major Revision decision reflects the gap between the paper's current evidence and its claims, not a judgment of the paper's ultimate merit. If the authors can demonstrate that the error concentration mechanism is genuinely learned (not an artifact of thresholding), and can contextualize LISTA's position relative to at least one CNN baseline, this paper will make a solid contribution to Digital Signal Processing. I look forward to receiving the revised manuscript.

---

*Editorial Decision rendered by the Editorial Synthesizer for Digital Signal Processing (Elsevier), 2026-06-01.*