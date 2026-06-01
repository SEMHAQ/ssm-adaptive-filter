# Cover Letter

Dear Editor,

We would like to submit our manuscript entitled "Deep-unfolded LISTA for sparse channel estimation: Error concentration and BER implications" for consideration for publication in Digital Signal Processing.

## Summary

This paper provides a mechanism analysis of the Learned Iterative Shrinkage-Thresholding Algorithm (LISTA) applied to sparse multipath channel estimation. Rather than proposing a new architecture, we investigate a counter-intuitive finding: LISTA's NMSE saturates 12--33 dB behind classical methods (OMP, FISTA), yet it delivers competitive BER performance under certain equalization conditions.

## Key Contributions

1. **Error concentration mechanism**: We quantify how LISTA's learned parameters concentrate 100% of estimation error on true tap locations (vs. 95% for OMP and 92% for ISTA), placing 379x less error on non-support taps.

2. **Ablation with statistical rigor**: Ablation studies (20 seeds, Holm--Bonferroni corrected) identify the per-layer threshold schedule as the dominant learned component (+14--18 dB).

3. **Practical deployment guidance**: We provide a decision framework for practitioners: use LISTA when inference speed (25x faster batched inference) and BER under ZF equalization matter; use OMP/FISTA when NMSE accuracy is paramount.

4. **Generalization**: The error concentration mechanism transfers to ITU channel models (99.5%) and complex-valued pilots (97.8%).

## Significance

This paper addresses a gap between the deep unfolding literature's claims and practical performance. By honestly characterizing LISTA's limitations (NMSE saturation) and strengths (error concentration, inference speed), we provide guidance that helps practitioners choose the right tool for their specific deployment scenario. This type of mechanism analysis is valuable to the signal processing community.

## Fit with DSP

This work aligns with DSP's scope in adaptive filtering, sparse signal processing, and deep learning for communications. The paper emphasizes reproducibility (20 seeds, corrected statistics, code available at https://github.com/SEMHAQ/ssm-adaptive-filter).

## Declarations

- **Conflict of Interest**: None.
- **Funding**: None.
- **Ethical Approval**: Not applicable (no human subjects or sensitive data).
- **Data Availability**: All code and experimental data are publicly available at https://github.com/SEMHAQ/ssm-adaptive-filter.
- **AI Disclosure**: Claude (Anthropic, Inc.) was used for text editing, figure generation scripts, code review, citation verification, and simulated peer review. The author reviewed and edited all content and takes full responsibility.

This manuscript has not been published elsewhere and is not under consideration by another journal. All authors have approved the manuscript and agree with its submission to Digital Signal Processing.

We look forward to your decision.

Sincerely,
Huanjie Yu
School of Computer Science
Hunan University of Technology and Business
Changsha, Hunan 410205, China
Email: semhaqx@gmail.com
ORCID: 0009-0008-9824-1801
