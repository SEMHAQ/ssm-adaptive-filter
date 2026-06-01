Now I have thoroughly read the paper, its references, and the implementation code. Here is my complete review report.

---

# Peer Review Report: Reviewer 2 (Domain Expert)

**Paper:** "Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation"

**Author:** Huanjie Yu, Hunan University of Technology and Business

**Target Journal:** Digital Signal Processing (Elsevier)

**Reviewer Role:** Domain Expert -- Sparse recovery, deep unfolding, compressed sensing, and wireless channel estimation

---

## 1. Summary

This paper presents a systematic empirical analysis of LISTA (Learned ISTA) applied to sparse channel estimation. The central finding is that LISTA's NMSE saturates at approximately -25 dB for SNR >= 10 dB on i.i.d. Gaussian channels, trailing OMP by 13-33 dB and FISTA by 1-27 dB. Despite this NMSE gap, the paper identifies an "error concentration" mechanism: LISTA concentrates 100.0% +/- 0.0% of estimation error on true tap locations (vs. 95.2% +/- 0.6% for OMP and 92.4% +/- 0.4% for ISTA), which provides BER advantages under ZF equalization for 16-QAM at SNR >= 15 dB. The paper includes ablation studies (20 seeds with Holm-Bonferroni correction), generalization analysis across sparsity/SNR/channel length mismatches, comparison with LISTA-CP and FISTA, SNR-specific training mitigation, and ITU channel evaluation. All experiments assume real-valued channels with BPSK pilots.

The paper is commendable for its intellectual honesty -- it openly reports that LISTA underperforms OMP and FISTA in NMSE and reframes its contribution around mechanism analysis rather than claiming state-of-the-art performance.

---

## 2. Strengths

**S1. Exceptional intellectual honesty and balanced reporting.** The paper consistently reports negative or mixed results with full transparency. For instance, Table 1 (line 293) shows LISTA at -24.25 dB vs. OMP at -37.09 dB at SNR=20 dB, and the text explicitly states "LISTA's learned parameters do not improve NMSE over standard accelerated ISTA" (line 815). The FISTA comparison (Table, lines 799-809) showing 1-27 dB disadvantage is unusual in a submission and demonstrates scientific integrity. The repeated qualification that hardware advantages are "unvalidated hypotheses" (lines 886, 900) is exemplary.

**S2. Novel mechanism analysis with ISTA control experiment.** The error concentration analysis (Section 4.12, lines 690-862) is the paper's primary intellectual contribution. The ISTA control experiment (Table at lines 750-759) elegantly disentangles the contribution of soft-thresholding (92.4% for ISTA) from LISTA's learned parameters (100.0%), providing a concrete mechanistic explanation for the BER-NMSE disconnect. The metric in Equation 12 (line 722) -- fraction of error energy on true support -- is well-defined and physically meaningful.

**S3. Rigorous statistical methodology.** The paper applies paired t-tests with Holm-Bonferroni correction, reports Cohen's d effect sizes, uses 20 seeds for ablation (addressing power concerns from the 5-seed analysis), and honestly reports when results become non-significant after correction. The progression from 5-seed ablation (Table at lines 457-468, where threshold appeared insignificant) to 20-seed ablation (Table at lines 673-685, where threshold is dominant at d=18.4) is a methodologically instructive demonstration of statistical power.

**S4. Comprehensive ablation study with clear practical implications.** The 20-seed ablation reveals that the per-layer threshold schedule is the dominant contributor (+14-18 dB degradation), while W^(k) provides a secondary but significant +1.24 dB (p < 0.001, d=1.5). This finding -- that LISTA primarily learns a threshold schedule rather than a sophisticated preconditioner -- has direct implications for architecture design.

**S5. Honest discussion of limitations.** The paper explicitly addresses the real-valued channel limitation (lines 965-966), acknowledges that LISTA-CP's convergence guarantees provide "no practical accuracy improvement" (line 564), and presents the SNR saturation as "likely a training artifact" (line 912) rather than hiding it.

---

## 3. Weaknesses

**W1. Incomplete coverage of LISTA variants and their empirical performance on channel estimation.**

*What is wrong:* The related work section (Section 2.2, lines 121-139) cites LISTA-CP, OCLISTA, ALISTA, LISTA-AMP, Elastic LISTA, and LISTA-CPSS, but only experimentally compares against LISTA-CP. The paper does not compare against OCLISTA (Borgerding et al., 2020), ALISTA (Liu et al., 2019), or LISTA-AMP (Liu et al., 2023), despite claiming that the error concentration mechanism "can be understood through the lens of approximate message passing" (line 925) and that OCLISTA and LISTA-AMP have "improved convergence properties." Given that the paper's central claim is a systematic analysis of LISTA for channel estimation, omitting empirical comparisons with these variants is a significant gap.

*Where it is:* Section 2.2 (lines 121-139), Section 5.1 (lines 923-926).

*Proposed fix:* Include at minimum OCLISTA and ALISTA as experimental baselines. OCLISTA adds Onsager correction terms that the paper hypothesizes are approximated by W^(k) (line 925) -- this hypothesis can be directly tested by comparing OCLISTA's error concentration against standard LISTA. ALISTA's analytic weight initialization would test whether the learned W^(k) matrices converge to the theoretically optimal weights. If implementing these is infeasible, the paper should explicitly state this and discuss what specific results would be expected based on prior published work.

**W2. Missing CNN/Transformer baselines weakens the paper's positioning.**

*What is wrong:* The paper justifies omitting CNN and Transformer baselines by stating the focus is "on understanding LISTA's behavior within the deep unfolding paradigm" (line 261) and provides a qualitative comparison in Section 5.2 (lines 935-941). However, the qualitative discussion (lines 939-941) claims CNNs require ">500K parameters" and Transformers require ">1M parameters" without citing specific parameter counts from published channel estimation architectures. For N=64, a simple 3-layer CNN with 64 channels has approximately 37K parameters -- fewer than LISTA's 82K. The claimed parameter advantage is not established.

*Where it is:* Section 4.1 (lines 261), Section 5.2 (lines 935-941).

*Proposed fix:* Include at least one CNN baseline (e.g., a 1D CNN mapping received signal to channel estimate, as in Ye et al. [2018]) under the same experimental conditions. Even a simple CNN baseline would significantly strengthen the positioning. If computational resources are limited, the paper should remove the parameter count claims (lines 939) that are not supported by citations to specific architectures with measured parameter counts.

**W3. The error concentration metric conflates architectural behavior with thresholding bias.**

*What is wrong:* The paper reports LISTA concentrates 100.0% +/- 0.0% of error on true taps (Table at lines 730-737). However, this result is partially an artifact of how LISTA's soft-thresholding operator works: by construction, the soft-thresholding operator (Equation 7, line 193) sets all values below theta^(k) to zero. If the learned thresholds are large enough to zero out most non-support taps, then by definition the error on non-support taps will be near zero (since both the estimate and truth are zero on those taps). The metric measures the fraction of error on true taps, but when the estimate is extremely sparse (fewer non-zero entries than the true channel), this fraction is trivially high. The paper should report the fraction of non-support taps that LISTA incorrectly estimates as non-zero (false discovery rate) alongside the error concentration metric.

*Where it is:* Table at lines 730-737, Equation 12 (line 722), interpretation at lines 740-742.

*Proposed fix:* Report the false discovery rate (fraction of estimated non-zero taps that are actually zero) and the missed detection rate (fraction of true taps that LISTA estimates as zero) alongside the error concentration metric. This would distinguish between two very different behaviors: (a) LISTA correctly identifies all true taps and concentrates error on them, vs. (b) LISTA produces an overly sparse estimate that zeros out some true taps and most non-support taps. The support recovery table (Table at lines 699-716) partially addresses this, but the Jaccard index alone does not distinguish these cases.

**W4. Channel model realism is insufficient for the target application domain.**

*What is wrong:* The paper uses i.i.d. Gaussian tap amplitudes for training and testing (line 259), with ITU channels used only for cross-distribution evaluation (lines 517-532). Real wireless channels exhibit: (1) correlated tap amplitudes (exponential PDP), (2) time variation (Doppler), (3) frequency selectivity in OFDM, and (4) complex-valued baseband signals. The paper acknowledges the real-valued limitation (lines 965-966) but does not discuss how the i.i.d. Gaussian assumption affects the generalizability of the mechanism analysis. Specifically, the 100.0% error concentration on Gaussian channels may partly result from the independence of tap amplitudes -- on channels with correlated taps (e.g., exponential PDP), the learned W^(k) may not achieve the same concentration, as evidenced by the slight decrease to 99.3-99.5% on ITU channels (Table at lines 850-858).

*Where it is:* Section 4.1 (line 259), Table at lines 850-858, Section 5.4 (lines 965-966).

*Proposed fix:* The ITU channel results are a good start, but the paper should: (1) explicitly state what fraction of real-world channel estimation scenarios are adequately represented by i.i.d. Gaussian taps, (2) discuss whether the 0.5-0.7% decrease in error concentration on ITU channels could become more significant for channels with stronger tap correlations (e.g., urban macro with many clustered reflections), and (3) consider including at least one measured channel dataset (e.g., from 3GPP channel sounder measurements) to validate the ITU model results.

**W5. The LISTA architecture does not incorporate domain-specific channel structure.**

*What is wrong:* The paper uses a generic LISTA architecture (Equation 5, lines 184-188) with full N x N weight matrices W^(k) that are initialized as identity and trained end-to-end. For channel estimation specifically, the convolution matrix X has Toeplitz structure (Equation 8, line 199), which implies that the Gram matrix X^T X is approximately banded Toeplitz. The optimal W^(k) should therefore also have structure (e.g., banded or Toeplitz). Using unstructured N x N matrices: (1) wastes parameters on entries that should be zero or structured, (2) may explain the poor scaling at N=256 (Table at lines 366-380, where 3/5 seeds diverge), and (3) limits interpretability of what W^(k) learns. The paper acknowledges scalability concerns (line 209) but does not connect them to the architectural choice.

*Where it is:* Equation 5 (lines 184-188), Table at lines 366-380, Section 3.4 (lines 204-209).

*Proposed fix:* Include an ablation comparing unstructured W^(k) against structured variants (e.g., banded, Toeplitz, or low-rank). This would: (a) reduce parameter count for scalability, (b) provide interpretability (does W^(k) learn approximately Toeplitz structure?), and (c) potentially improve generalization by encoding domain knowledge. Even analyzing the spectral structure of the learned W^(k) matrices (e.g., plotting singular values, checking for approximate Toeplitz structure) would provide valuable insight.

**W6. FISTA comparison reveals that the paper's contribution is narrower than presented.**

*What is wrong:* The FISTA comparison (Table at lines 799-809) shows that FISTA with 20 iterations and grid-searched threshold outperforms LISTA at all SNR levels by 1-27 dB, requires no training data, and has comparable computational cost. The paper honestly acknowledges this (lines 815-817) but then frames LISTA's value as lying in the "error concentration mechanism and potential hardware pipelining." However: (1) the error concentration advantage manifests only under ZF equalization (not MMSE), (2) ZF equalization is rarely used in practice (the paper itself calls MMSE "the standard in modern receivers," line 615), and (3) the hardware advantage is explicitly called an "unvalidated hypothesis" (line 886). The practical contribution therefore reduces to: LISTA achieves better 16-QAM BER under ZF equalization at SNR >= 15 dB -- a narrow finding.

*Where it is:* Table at lines 799-809, lines 815-817, lines 886, 900.

*Proposed fix:* The paper should more clearly scope its contribution in the abstract and introduction. The abstract currently presents the error concentration as a primary finding, but the practical relevance depends on ZF equalization being important. The paper's discussion of when ZF is relevant (lines 930-931) is good but could be strengthened with concrete application scenarios (e.g., low-cost IoT receivers, systems with unreliable noise estimation) and quantitative analysis of how often ZF is used in current standards.

**W7. Statistical claims about 100.0% +/- 0.0% need clarification.**

*What is wrong:* The paper reports LISTA's error concentration as "100.0% +/- 0.0%" (e.g., line 740), which appears to have zero variance across 5 seeds. This is suspicious -- either the metric has a ceiling effect (values are exactly 100.0% because the definition in Equation 12 rounds to 100% when error on non-support is very small), or the computation has a numerical artifact. The paper defines "When the total error = 0, the ratio is defined as 100% by convention" (line 724), but this applies only when the total error is exactly zero, which is unlikely. If the non-support error is 0.01% +/- 0.01% (as reported at line 740), then the support error should be 99.99% +/- 0.01%, not exactly 100.0% +/- 0.0%.

*Where it is:* Table at lines 730-737, Table at lines 750-759, abstract (line 58).

*Proposed fix:* Verify the computation of the error concentration metric. If the 100.0% value results from rounding (e.g., 99.995% rounds to 100.0%), report the unrounded value with appropriate precision. If the zero variance is genuine, explain why (e.g., the soft-thresholding operator deterministically zeros out all non-support taps for these specific parameter values).

---

## 4. Detailed Comments

### 4.1 Literature Review

**Coverage of compressed sensing for channel estimation (Section 2.1):** The coverage is adequate for the main references (Bajwa et al., 2010; Berger et al., 2010; Candes et al., 2006; Donoho, 2006). However, several important references are missing:

- **Missing: Tropp and Gilbert (2007)** is cited but the paper does not discuss the restricted isometry property (RIP) conditions under which OMP guarantees recovery -- relevant since the paper uses OMP as the primary baseline and the i.i.d. Gaussian measurement matrix satisfies RIP with high probability.

- **Missing: Needell and Tropp (2009), "CoSaMP"** -- a compressed sensing algorithm that, like OMP, requires sparsity knowledge but has stronger recovery guarantees. This would strengthen the greedy algorithm baseline set.

- **Missing: Dai and Milenkovic (2009), "Subspace Pursuit"** -- another greedy algorithm relevant to sparse channel estimation.

- **Missing: Cotter and Rao (2002), "Sparse channel estimation via matching pursuit with application to equalization"** -- an early and highly cited work on sparse channel estimation that predates the CS framework adoption.

**Coverage of deep unfolding (Section 2.2):** The section is comprehensive for LISTA variants, citing LISTA-CP (Chen et al., 2019), OCLISTA (Borgerding et al., 2020), ALISTA (Liu et al., 2019), LISTA-AMP (Liu et al., 2023), Elastic LISTA (Liu et al., 2021), and LISTA-CPSS (Chen et al., 2020). However:

- **Missing: Xin et al. (2016), "Maximum-likelihood PROMISE"** and related work on deep unfolding for MIMO detection, which shares the same mathematical structure (sparse recovery with learned iterations) and provides relevant comparison points.

- **Missing: Balatsoukas-Stimming and Studer (2019), "Deep unfolding for communications systems"** -- a tutorial-style reference that contextualizes deep unfolding specifically for communications, directly relevant to this paper's domain.

- **Missing: He et al. (2020), "ISTA-Net++"** -- an improvement over ISTA-Net (cited) that achieves better performance with fewer parameters.

**Coverage of deep learning for channel estimation (Section 2.3):** The section covers CNN, Transformer, and model-driven approaches, citing 16 references. However:

- **Missing: Gao et al. (2023)** is cited (line 260-268) as a survey but the paper does not engage with specific findings from this survey regarding which deep unfolding architectures perform best for channel estimation.

- **Missing: Honkala et al. (2021), "DeepRx and other recent DL-based channel estimation papers from Nokia/Bell Labs"** that provide practical benchmarks.

- **Missing: Tung et al. (2021), "Deep learning for MIMO detection"** and related work on unfolding for detection (not estimation), which share mathematical structure.

**Coverage of adaptive filtering (Section 2.4):** The section briefly mentions LMS, NLMS, and PNLMS. Missing:

- **Missing: Chen et al. (2009), "Sparse LMS and NLMS"** -- sparse variants of LMS/NLMS that exploit channel sparsity, directly relevant to comparing LISTA against sparsity-aware adaptive filters.

- **Missing: Aboutanios (2004)** and related work on shrinkage-based adaptive filtering.

### 4.2 Theoretical Framework

**AMP connection (Section 5.1, lines 924-926):** The paper contextualizes the error concentration within AMP theory, noting that "the connection between LISTA's learned weight matrices and the Onsager correction has been established by prior work." This is appropriate and the paper correctly does not claim new theoretical contributions. However, the connection could be made more precise:

- The paper states that "LISTA's learned per-layer threshold schedule and step sizes further refine this concentration from 92.4% to 100.0%" (line 764). This is an empirical observation, but the paper does not provide a theoretical argument for why learned thresholds achieve 100% while grid-searched thresholds achieve only 92.4%. Is the improvement due to (a) layer-specific vs. shared thresholds, (b) the interaction between W^(k) and theta^(k), or (c) the training procedure? The ablation partially addresses this (shared parameters degrade by +18.22 dB), but the connection to the error concentration metric specifically is not made.

**NMSE saturation analysis (Section 5.1, lines 913-921):** The paper provides three arguments for why the saturation is a training artifact: (1) scale-invariant loss, (2) SNR-specific training breaks it, (3) LISTA-CP constraints are naturally satisfied. These are plausible but not conclusive. Argument (1) applies to any training with NMSE loss, yet other deep unfolding works do not report similar saturation. Argument (2) shows improvement but still leaves a 6 dB gap with OMP. Argument (3) is about convergence conditions, not representational capacity. The paper should discuss whether the saturation is specific to the i.i.d. Gaussian channel model or would also occur on other sparse recovery problems.

### 4.3 Experimental Methodology

**Data generation (line 259):** Tap locations are "drawn uniformly at random" and amplitudes follow N(0,1). This is standard for compressed sensing but not representative of wireless channels, where tap amplitudes typically follow an exponential power delay profile. The paper should clarify that the i.i.d. Gaussian model represents a "best case" for sparse recovery algorithms (RIP-satisfying measurement matrix, independent taps) and that performance on more structured channels may differ.

**Baseline tuning (lines 263-269):** The baselines are tuned via grid search on the validation set, which is appropriate. However, the LASSO baseline uses ISTA with 500 iterations (line 266), while FISTA uses only 20 iterations (line 267). This asymmetry could affect the comparison: LASSO with 500 ISTA iterations is well-converged, but LASSO with 20 FISTA iterations would also be well-converged and more computationally comparable to LISTA's 20 layers. The paper should justify why LASSO uses ISTA (500 iterations) while the separate FISTA baseline uses 20 iterations.

**LISTA training (lines 271):** The paper uses mixed-SNR training with SNR in [0, 30] dB, learning rate 5e-4, batch size 256, and 200 epochs. The training generates fresh data each epoch (line 68 of train_sparse.py), which is good practice. However, the validation set is generated separately (line 69-70 of generate.py mentions 2000 validation samples) but the training script does not appear to use validation-based early stopping -- it saves the "best" model based on training loss (line 103 of train_sparse.py). This could lead to overfitting.

**Number of test samples:** The paper uses 2000 test samples (line 259) and 200 channel realizations per SNR point for BER (line 590). These are adequate for the NMSE metric but the BER analysis at low error rates (e.g., 10^-3) may have insufficient samples for reliable estimation. The paper should report confidence intervals for BER values.

### 4.4 Domain Contribution Assessment

The paper makes three distinct contributions:

1. **Mechanism analysis (error concentration):** This is the strongest contribution and is novel in the channel estimation context. The ISTA control experiment and the generalization to ITU channels strengthen the finding. However, the practical relevance is limited to ZF equalization, which is uncommon in modern receivers.

2. **Systematic empirical characterization:** The comprehensive ablation, generalization analysis, and FISTA comparison provide a clear picture of LISTA's strengths and limitations for channel estimation. This is valuable for practitioners considering LISTA deployment.

3. **Negative results with explanation:** The paper's honest reporting of LISTA's NMSE limitations, combined with the mechanistic explanation, is a valuable contribution to the literature, which tends to overstate deep learning advantages.

The contribution is appropriate for Digital Signal Processing (Elsevier) but would be strengthened by: (a) at least one CNN/Transformer baseline under identical conditions, (b) comparison with OCLISTA or ALISTA, and (c) extension to complex-valued channels.

### 4.5 Positioning

The paper positions itself as a "systematic analysis" rather than an architecture paper. This is appropriate given the negative NMSE results. However, the positioning could be clearer:

- The title says "Generalization, Error Structure, and Ablation" -- these are analysis dimensions, not contributions. The contribution is the mechanism insight (error concentration) and the practical characterization.

- The paper compares against LISTA-CP but not against OCLISTA, LISTA-AMP, or ALISTA, despite citing all of them. This creates an incomplete picture of how standard LISTA relates to the broader LISTA family.

- The paper does not position itself relative to the "when does deep learning help for sparse recovery?" literature (e.g., Li et al., 2022, cited at line 373-379). This work directly addresses that question and should engage more with the findings.

---

## 5. Minor Issues

1. **Line 125:** The citation for LISTA-CP shows year 2019 in the bib file (line 158 of references.bib) but the proceedings venue is CVPR Workshops 2019. The in-text citation at line 125 says "Chen et al. (2018)" -- this is inconsistent.

2. **Line 209:** "At N=256, the per-layer mapping alone has 65,536 parameters, yielding 1,310,740 total parameters." This should be 20 x (65,536 + 2) = 1,310,760 (the paper reports 1,310,740 in Table at line 881, which is 1,310,760 - 20 = rounding to nearest 1000?).

3. **Table at line 293:** The standard deviation at SNR=5 dB is 4.10 dB for LISTA, which is much larger than at other SNR points (0.30-0.79 dB). This suggests training instability at this SNR and should be discussed.

4. **Line 326:** At K=15, "One seed diverged (positive NMSE)" with std of 8.27 dB. The paper should report the distribution of per-seed results, not just mean +/- std, when one seed is an outlier.

5. **Code verification:** The training script (train_sparse.py) generates fresh data each epoch (line 68-74), but the evaluation script appears to use a fixed test seed (torch.manual_seed(123), line 139). This is appropriate but should be documented.

---

## 6. Questions for the Authors

1. Can you report the learned threshold values theta^(k) across layers? The ablation shows the threshold schedule is dominant (+14-18 dB), so understanding the learned schedule (e.g., does it decrease monotonically? is it layer-specific?) would provide insight into what LISTA learns.

2. What is the false discovery rate (fraction of estimated non-support taps that are actually zero) for LISTA vs. OMP? The 100% error concentration could result from LISTA producing very sparse estimates (fewer non-zero entries than K).

3. Have you tested whether the NMSE saturation occurs with other loss functions (e.g., absolute error, Huber loss)? The paper attributes the saturation to the "scale-invariant NMSE loss" -- testing with a non-scale-invariant loss would validate this hypothesis.

4. How does the error concentration mechanism behave for complex-valued channels? The soft-thresholding operator for complex signals operates on magnitude, which could produce different concentration behavior.

5. Can you report the spectral norms of the learned W^(k) - I matrices? The paper mentions max spectral norm = 0.34 for LISTA-CP (line 564), but does not report the distribution across layers for standard LISTA.

---

## 7. Overall Assessment

This paper provides a thorough, honest, and methodologically rigorous analysis of LISTA for sparse channel estimation. The error concentration mechanism analysis is novel and well-executed, and the statistical methodology (Holm-Bonferroni correction, Cohen's d, 20-seed ablation) is exemplary for this community. The paper's intellectual honesty in reporting that LISTA underperforms OMP and FISTA in NMSE is commendable and unusual.

The primary weaknesses are: (1) missing CNN/Transformer and OCLISTA/ALISTA baselines that would complete the positioning, (2) the error concentration metric needs additional diagnostics (false discovery rate) to be fully interpretable, and (3) the practical relevance is narrower than presented (ZF equalization only, unvalidated hardware advantage). The real-valued channel limitation is honestly acknowledged but limits the immediate applicability to real systems.

The paper would benefit from revision to address the missing baselines (at minimum OCLISTA and one CNN architecture) and to provide additional diagnostics for the error concentration metric. With these additions, the paper would make a solid contribution to the deep unfolding and sparse channel estimation literature.

---

## 8. Scores

| Dimension | Score (0-100) | Justification |
|-----------|:------------:|---------------|
| **Originality** | 55 | The error concentration mechanism analysis is novel in the channel estimation context. However, the LISTA architecture itself is standard (Gregor & LeCun, 2010), and the paper explicitly disclaims architectural novelty. The mechanism insight is the primary original contribution. |
| **Technical Soundness** | 70 | The experimental methodology is rigorous (multiple seeds, statistical testing, ablation). However, the error concentration metric may have ceiling effects (W3), the LISTA architecture does not exploit channel structure (W5), and the FISTA comparison reveals that the contribution scope is narrow (W6). The code is clean and reproducible. |
| **Significance/Impact** | 50 | The honest negative results are valuable but the practical impact is limited: LISTA underperforms FISTA/OMP in NMSE, the BER advantage applies only under ZF equalization (uncommon), and the hardware advantage is unvalidated. The mechanism insight is intellectually interesting but its practical utility is narrow. |
| **Literature Review** | 55 | Good coverage of LISTA variants and deep learning for channel estimation. However, missing several important references (Cotter & Rao, 2002; sparse LMS variants; CoSaMP; deep unfolding for communications surveys) and incomplete engagement with the "when does deep learning help" literature. |
| **Clarity/Presentation** | 75 | The paper is well-organized with clear section structure. Tables and figures are informative. The repeated qualifications about limitations are appropriate. However, the practical contribution is sometimes obscured by extensive analysis, and the abstract is dense. |
| **Relevance to DSP** | 70 | Directly relevant to the journal's scope (signal processing, adaptive filtering, sparse recovery). The channel estimation application is core DSP. However, the narrow practical scope (ZF-only BER advantage, unvalidated hardware) limits the impact for the DSP community. |
| **OVERALL** | 60 | A methodologically rigorous paper with a novel mechanism insight, but limited by missing baselines, narrow practical relevance, and the fundamental finding that LISTA underperforms simpler methods in NMSE. Suitable for the journal after revision to address missing baselines and metric clarifications. |

---

**Recommendation:** Revise and Resubmit. The paper has valuable contributions (mechanism analysis, honest reporting, rigorous statistics) but needs: (1) at least OCLISTA and one CNN baseline under identical conditions, (2) additional diagnostics for the error concentration metric (false discovery rate), and (3) clearer scoping of the practical contribution in the abstract and introduction.