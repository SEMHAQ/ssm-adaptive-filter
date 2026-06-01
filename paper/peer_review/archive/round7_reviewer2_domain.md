# Peer Review Report — Reviewer 2 (Domain)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 7

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain Expert)

### Reviewer Identity
Prof. Maria Santos, Full Professor of Telecommunications at Instituto Superior Técnico, University of Lisbon. 20+ years research in sparse channel estimation, compressed sensing for communications, and OFDM systems. Published 80+ papers on compressed sensing-based channel estimation. Member of ITU-R Study Group 3.

### Review Focus
Literature coverage and positioning, theoretical framework appropriateness, domain contribution significance, and validity of experimental assumptions against real wireless channel models.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
5 — This paper falls directly within my core expertise area. I have published extensively on sparse channel estimation and compressed sensing for communications.

### Summary Assessment
This paper provides a thorough empirical analysis of LISTA for sparse channel estimation, covering NMSE performance, BER analysis, ablation studies, generalization, and hardware complexity. The literature review is comprehensive and well-organized, covering deep unfolding, CNN/Transformer-based methods, and classical adaptive filtering. The key contribution—the BER-NMSE disconnect analysis showing LISTA's error concentration on true taps—is novel and practically relevant. The ITU channel experiments demonstrate reasonable cross-distribution generalization. However, the paper's positioning is somewhat awkward: it applies a well-known architecture (LISTA) to a well-studied problem (sparse channel estimation) without architectural novelty, relying instead on the depth of empirical analysis. While the analysis is valuable, the domain contribution is incremental. The missing CNN/Transformer baseline comparison is a significant gap for a journal submission. I recommend Minor Revision to address the baseline gap and strengthen the domain positioning.

---

## Strengths

### S1: Comprehensive Literature Coverage with Clear Positioning
The paper provides excellent coverage of the literature across three streams: sparse channel estimation (Bajwa 2010, Berger 2010), deep unfolding (Gregor 2010, Chen 2018, Borgerding 2020, Liu 2023), and deep learning for channel estimation (Ye 2018, Gao 2019, Zhang 2020). The qualitative comparison in Section 5.2 positions LISTA against CNN/Transformer methods across three dimensions (parameters, interpretability, generalization). This is well-organized and helpful for readers.

### S2: BER-NMSE Mechanism Analysis is Domain-Significant
The error sparsity analysis (Section 4.12) reveals that LISTA concentrates 99.9% of error on true taps vs. 94.9% for OMP. This is a genuinely new insight for the channel estimation community. The connection to equalizer noise enhancement (1.8× advantage at SNR=20) provides a concrete mechanism explanation. This finding has implications beyond LISTA—it suggests that sparsity-enforcing estimators may have inherent BER advantages regardless of NMSE.

### S3: ITU Channel Experiments Validate Practical Relevance
The ITU PedA and VehA experiments (Section 4.7) demonstrate that LISTA trained on i.i.d. Gaussian data achieves -23 to -27 dB on realistic channels. The paper correctly notes that baselines use the same hyperparameters (no re-optimization for ITU), ensuring fair comparison. This cross-distribution generalization is important for practical deployment.

### S4: Honest Comparison with LISTA-CP
The LISTA-CP comparison (Section 4.8) with diagnostic analysis showing that weight clipping is never activated (max spectral norm = 0.34 < 1.0) provides genuine insight. The conclusion that convergence guarantees provide theoretical assurance but no practical improvement is honest and informative.

---

## Weaknesses

### W1: No Direct CNN/Transformer Baseline Comparison
**Problem**: The paper excludes CNN and Transformer baselines, providing only qualitative comparison in Section 5.2. The paper states: "our focus is on understanding LISTA's behavior within the deep unfolding paradigm and comparing against well-established model-based methods."
**Why it matters**: For DSP readers, the practical question is "which method should I use?" Without direct comparison, readers cannot assess whether LISTA's 4.4× throughput advantage comes with a performance penalty vs. CNN/Transformer methods. The qualitative comparison cites published NMSE ranges (-20 to -30 dB for CNNs) but these are on different channel models and SNR ranges.
**Suggestion**: Add at least one CNN baseline (e.g., a 1D-CNN with comparable parameter count) trained under identical conditions. If space is limited, provide in supplementary material. Alternatively, provide a detailed table comparing published results across methods on the same channel model and SNR range.
**Severity**: Major

### W2: i.i.d. Gaussian Channel Model is Oversimplified
**Problem**: The paper uses i.i.d. Gaussian tap amplitudes with uniform random locations for training and most experiments. Real wireless channels have correlated tap amplitudes (exponential decay), correlated tap locations (clustered multipath), and time-varying characteristics.
**Why it matters**: The i.i.d. Gaussian model does not capture the correlation structure that makes sparse channel estimation challenging in practice. LISTA's learned W^(k) matrices may be exploiting the independence assumption, which would not hold on real channels.
**Suggestion**: Add an experiment training and testing on correlated channels (e.g., exponentially decaying taps with correlated locations). The ITU experiments partially address this, but a controlled experiment varying correlation strength would be more informative.
**Severity**: Major

### W3: Sparsity Level K=5 is Low Relative to N=64
**Problem**: The default configuration uses K=5 non-zero taps out of N=64 (7.8% sparsity). Many practical channels have higher sparsity levels (K=10-20 for N=64). The K=15 experiment shows instability (one seed diverges), suggesting LISTA's practical range is limited.
**Why it matters**: If LISTA only works reliably for K ≤ 10 (15.6% sparsity), its practical applicability is narrower than implied.
**Suggestion**: Provide a more detailed sparsity sweep (K = 2, 4, 6, 8, 10, 12, 15) with stability analysis (how many seeds diverge at each K). Report the maximum reliable sparsity level.
**Severity**: Minor

### W4: Pilot Length M=256 is Fixed Across All Experiments
**Problem**: The paper fixes M=256 (4× oversampling for N=64) across all experiments. In practice, pilot overhead is a critical resource, and the M/N tradeoff significantly affects spectral efficiency.
**Why it matters**: LISTA's performance may degrade differently than OMP/LASSO as M decreases (lower oversampling ratio). The M/N=1 case at N=256 shows divergence, but the M/N tradeoff for N=64 is not explored.
**Suggestion**: Add an experiment varying M (e.g., M = 64, 128, 256, 512) for fixed N=64 to characterize the pilot efficiency tradeoff. This would strengthen the practical deployment analysis.
**Severity**: Minor

---

## Detailed Comments

### Title & Abstract
- Title is accurate but long. Consider: "LISTA for Sparse Channel Estimation: BER Analysis, Ablation, and Hardware Complexity"
- Abstract is too long (~350 words). Reduce to 200 words focusing on the BER-NMSE disconnect.

### Introduction
- Good motivation. The 6 contributions are well-organized but could be more concise.
- The sparsity motivation (wideband communications, underwater acoustics, radar) is appropriate.

### Related Work (Section 2)
- Excellent coverage across three streams. The hardware deployment subsection (Kim 2021, Wei 2022, Chen 2022) is a nice addition.
- Missing: recent work on learned AMP (Liu 2023 is cited but not deeply discussed), and any work on LISTA for channel estimation specifically (if it exists).
- The classical adaptive filtering subsection (LMS, NLMS, PNLMS) is appropriate.

### Methodology (Section 3)
- Standard LISTA architecture. The FFT-based convolution (Eq. 8) is a practical optimization.
- The parameter analysis (N_params = 82K for N=64, L=20) is correct.
- The comparison with classical methods (OMP, LASSO, LMS/NLMS) is well-structured.

### Experiments (Section 4)
- **NMSE vs SNR (Table 1)**: LISTA's saturation at -25 dB is clearly demonstrated. The gap with OMP (13-33 dB at high SNR) is substantial.
- **NMSE vs Sparsity (Table 2)**: The K=15 divergence is concerning. Need more detail on stability.
- **NMSE vs Channel Length (Table 3)**: N=256 divergence at M/N=1 is correctly diagnosed. The cross-table inconsistency needs resolution.
- **Depth Analysis (Table 4)**: Clean results. L=10-20 recommendation is well-supported.
- **Ablation (Tables 5, 11)**: The 5→20 seed progression is excellent. The threshold dominance finding is important.
- **Generalization**: Adequate but could be more systematic.
- **ITU Channels (Table 8)**: Important for practical relevance. -23 to -27 dB on ITU channels is reasonable.
- **LISTA-CP (Table 9)**: Diagnostic analysis is a strength.
- **SNR Mitigation (Table 10)**: Well-designed. The 6 dB improvement from SNR-specific training is significant.
- **BER (Tables 10-12)**: The standout experiment. The mechanism analysis is novel.
- **Hardware (Tables 13-15)**: Theoretical analysis is useful but needs clearer labeling.

### Discussion
- The "training artifact vs. architectural limitation" discussion is well-reasoned.
- Section 5.2 (CNN/Transformer comparison) is reasonable but would benefit from direct comparison.
- The generalization discussion (Section 5.3) is practical and helpful.
- Limitations (Section 5.4) are honestly stated.

### Conclusion
- Accurately summarizes findings. The "measured FPGA/ASIC validation remains future work" caveat is appropriate.

### References
- Good coverage (~45 references). Recent works (2022-2024) are included.
- Missing: any paper specifically applying LISTA to channel estimation (if one exists). Also missing: learned AMP papers beyond Liu 2023.

---

## Questions for Authors

1. Are there any published works applying LISTA or LISTA variants specifically to channel estimation? If so, how does your analysis compare? If not, this should be explicitly stated as a gap your paper fills.

2. The paper uses BPSK pilot signals (±1). Would the results hold for QPSK or higher-order pilot modulations? The pilot modulation affects the convolution matrix properties.

3. For the ITU channel experiments, did you verify that the ITU channel sparsity (number of significant taps) is within LISTA's reliable operating range (K ≤ 10 based on the sparsity analysis)?

---

## Minor Issues

### Citation Format
- Reference [30] (Liu 2023 LISTA-AMP): Verify that this is the correct citation for LISTA-AMP. The description mentions "Onsager correction terms" which is typically associated with OCLISTA (Borgerding 2020).
- Reference [36] (Ma 2022): Ensure this is the correct deep-learning channel estimation survey.

### Figures and Tables
- Table 8 (ITU channels): Missing std for LMS, NLMS, OMP, LASSO. Were these run with multiple seeds?
- Figure 1 (NMSE vs SNR): Add LISTA-CP curve for visual comparison with Table 9 results.

### Literature
- Consider citing: Berger et al. "Sparse channel estimation for multicarrier underwater acoustic communication" (2008) for the underwater acoustics motivation.
- Consider citing: Candes et al. "Robust uncertainty principles" (2006) for the compressed sensing theoretical foundation (already cited but could be discussed more).

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 62 | Adequate | BER-NMSE mechanism is novel; LISTA application is incremental |
| Methodological Rigor (25%) | 76 | Strong | Good experiments, but cross-table inconsistency and missing baselines |
| Evidence Sufficiency (25%) | 74 | Strong | Comprehensive but missing CNN/Transformer direct comparison |
| Argument Coherence (15%) | 82 | Strong | Clear logical flow, honest limitations |
| Writing Quality (15%) | 77 | Strong | Well-written, some verbosity |
| Literature Integration | 78 | Strong | Good coverage, minor gaps |
| **Weighted Average** | **74.2** | **Minor Revision** | |
