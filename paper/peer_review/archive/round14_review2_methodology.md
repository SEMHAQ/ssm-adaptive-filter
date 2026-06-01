# Peer Review Report — Reviewer 1 (Methodology)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-06-01
- **Review Round**: Round 14

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Dr.~Jie Chen, Associate Professor of Electrical Engineering, Tsinghua University. Expertise in deep unfolding architectures, optimization algorithms for signal processing, and statistical experimental design. Published extensively on LISTA variants and proximal gradient methods. Review focus: experimental design, statistical validity, reproducibility, and computational methodology.

### Review Focus
Research design rigor, statistical methodology (sample sizes, multiple comparison corrections, effect sizes), reproducibility of experimental setup, computational complexity analysis, and validity of ablation study conclusions.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
5 — Completely within my area of expertise, I am very confident in my assessment.

### Summary Assessment
This manuscript provides a systematic experimental analysis of LISTA for sparse channel estimation, with particular attention to statistical rigor. The methodology is generally sound: 20-seed ablation studies with Holm--Bonferroni correction, 200-realization BER simulations, paired $t$-tests with Cohen's $d$ effect sizes, and ISTA/FISTA control experiments. The progression from 5-seed to 20-seed ablation (Section 4.11) demonstrates awareness of statistical power limitations. However, several methodological issues warrant attention: (1) the 5-seed initial ablation (Table 4) should have been presented as a pilot study rather than a definitive result, (2) the BER simulations use only 200 realizations per SNR point which may be insufficient for rare error events at high SNR, (3) the FISTA baseline uses grid-searched threshold while LISTA uses learned parameters---an asymmetry that favors LISTA. Despite these issues, the overall methodology exceeds the typical standard in the signal processing literature, and the paper's transparency about its limitations is commendable.

---

## Strengths

### S1: Proper Statistical Power Analysis and Correction
The paper demonstrates strong statistical practice. The 20-seed ablation (Table 11) uses paired $t$-tests with Holm--Bonferroni correction ($m=3$ comparisons), reports both raw and corrected $p$-values, and includes Cohen's $d$ effect sizes. The finding that the 5-seed ablation (Table 4) produced a false negative for threshold and per-layer parameters is a valuable methodological lesson. The paper explicitly states: "The Round 2 finding that these components were 'not individually significant' was a false negative attributable to the low statistical power of $n=5$ seeds" (Section 4.11). This level of transparency is rare and commendable.

### S2: Well-Designed Control Experiments
The ISTA control experiment (Section 4.12.3, Table 15) is methodologically excellent. By comparing LISTA ($99.9\%$ error on support) against standard ISTA ($97.2\%$), the paper isolates the contribution of learned parameters from the generic soft-thresholding property. This is the correct way to attribute a mechanism: demonstrate the baseline effect, then show the incremental improvement. The FISTA comparison (Table 12) serves a similar purpose for NMSE performance.

### S3: Cross-Table Consistency and Training Protocol Transparency
The explicit discussion of cross-table inconsistency (Section 4.3, Table 3) is a methodological strength. The 8~dB difference between mixed-SNR and channel-length training models is clearly explained and attributed to the training distribution rather than random variation. This prevents readers from misinterpreting discrepancies between tables.

### S4: Reproducibility Infrastructure
The paper specifies all hyperparameters (learning rate, weight decay, gradient clipping norm, batch size, epochs), training protocols (mixed SNR, cosine annealing), and evaluation procedures (number of seeds, realizations, statistical tests). The code appears to be available (based on the experimental structure). This level of detail enables reproduction.

---

## Weaknesses

### W1: FISTA Baseline Hyperparameter Asymmetry
**Problem**: The FISTA baseline (Section 4.12.4) uses grid-searched threshold over $\{0.001, 0.005, 0.01, 0.02, 0.05, 0.1\}$ with 20 iterations, while LISTA uses learned per-layer thresholds with 20 layers. This is a fair comparison in terms of layer count, but the grid search for FISTA is limited to 6 values. A more thorough optimization (e.g., line search, or finer grid) might improve FISTA's performance further.
**Why it matters**: The paper claims "FISTA with 20 iterations outperforms LISTA at all SNR levels" (Section 4.12.4). If FISTA's threshold is suboptimal, the comparison could be more favorable to LISTA than it appears. Conversely, if FISTA's grid search is already optimal, the comparison is fair.
**Suggestion**: Report the selected FISTA threshold value at each SNR to allow readers to assess whether the grid was sufficiently fine. If the optimal threshold was at the boundary of the grid, expand the search range.
**Severity**: Minor

### W2: BER Realization Count at High SNR
**Problem**: The BER simulations use 200 channel realizations per SNR point (Section 4.10). At high SNR ($\geq 20$~dB), the BER is on the order of $10^{-3}$ to $10^{-4}$ (Table 7). With 200 realizations, the expected number of errors is 0.06--0.02 per realization (assuming ~100 bits per realization), which means many realizations will have zero errors. This makes the BER estimate noisy and the paired $t$-tests less reliable.
**Why it matters**: At the SNR points where LISTA shows its ZF advantage (SNR $\geq 15$~dB), the BER estimates may have high variance due to insufficient error counts.
**Suggestion**: Either (a) increase the number of realizations at high SNR (e.g., 1000), or (b) report the number of bit errors observed per SNR point to allow readers to assess estimation precision. Alternatively, use importance sampling or semi-analytical methods for high-SNR BER estimation.
**Severity**: Minor

### W3: Single-Seed Support Recovery Analysis
**Problem**: The support recovery analysis (Table 13, Section 4.12.1) reports results over "200 realizations, 3 seeds" without standard deviations. The error sparsity analysis (Table 14) reports results without any uncertainty quantification. This is inconsistent with the rigorous statistical treatment in the ablation study.
**Why it matters**: Without uncertainty bounds, it is impossible to assess whether the $99.9\%$ vs $94.9\%$ difference in error concentration is statistically significant.
**Suggestion**: Report mean $\pm$ std over the 3 seeds for all mechanism analysis metrics (Tables 13--16). If the variance is very small, state this explicitly.
**Severity**: Minor

### W4: LISTA-CP Clipping Threshold Justification
**Problem**: The LISTA-CP comparison (Section 4.8) uses a clipping threshold of $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2 < 1$. The paper reports that this constraint was "never activated" because spectral norms remained below 0.35. However, the choice of threshold 1.0 is not justified---a tighter threshold (e.g., 0.5) might have been activated and produced different results.
**Why it matters**: The conclusion that "LISTA-CP provides no practical benefit" depends on the specific threshold chosen. A sensitivity analysis would strengthen this claim.
**Suggestion**: Report the spectral norm values during training (e.g., at epochs 1, 50, 100, 200) to show the trajectory. Consider testing with a tighter clipping threshold (e.g., 0.5) to see if it activates and affects performance.
**Severity**: Minor

---

## Detailed Comments

### Methodology / Research Design
- The experimental design is comprehensive and well-structured. The 10 experiments cover NMSE vs.~SNR, sparsity, channel length, depth, ablation, generalization, practical deployment, LISTA-CP, SNR mitigation, and BER mechanism analysis.
- The mixed-SNR training protocol is well-motivated and consistently applied across experiments.
- The use of both parametric ($t$-tests) and non-parametric (Wilcoxon) tests in the 20-seed ablation is appropriate.

### Sampling Strategy
- Training set size (10,000) is standard for the problem scale.
- Validation set (2,000) and test set (2,000) are adequate.
- The use of independent channel realizations and noise instances for each sample is correct.

### Data Collection
- All experimental parameters are specified.
- The BPSK pilot signal choice is standard.
- The Gaussian tap amplitude model is standard but should be compared against more realistic distributions (this is partially addressed by the ITU channel experiments).

### Analysis Methods
- NMSE in dB is the standard metric.
- The Holm--Bonferroni correction is appropriate for multiple comparisons.
- Cohen's $d$ effect sizes are reported, which is excellent.
- The paired $t$-test design (same channel realizations) is correct for the BER analysis.

### Reproducibility
- All hyperparameters are specified.
- Random seed control is mentioned (5 seeds, 20 seeds).
- The training protocol (Adam, cosine annealing, gradient clipping) is fully specified.
- The only gap is that the code is not explicitly linked (though the experimental structure suggests it exists).

---

## Questions for Authors

1. In the FISTA comparison (Table 12), what threshold value was selected by grid search at each SNR? Was the optimal value at the boundary of the search range $\{0.001, 0.005, 0.01, 0.02, 0.05, 0.1\}$?

2. For the BER simulations (Section 4.10), how many bits were transmitted per channel realization? This determines the effective sample size for BER estimation at each SNR point.

3. The 20-seed ablation uses Holm--Bonferroni correction with $m=3$. Why not $m=6$ (all pairwise comparisons between the 4 configurations)? With $m=3$, you are comparing each ablated configuration against the full model, but not against each other.

4. Can you report the spectral norm $\|\mathbf{W}^{(k)} - \mathbf{I}\|_2$ at the end of training for each layer $k$? This would help readers understand whether the LISTA-CP constraint is naturally satisfied or merely happens to be inactive for these specific seeds.

---

## Minor Issues

### Language / Grammar
- Section 4.11: "The Round 2 finding that these components were 'not individually significant' was a false negative" — the term "Round 2" is internal jargon. Consider "the initial 5-seed ablation" instead.
- Table 11: The column header "Corrected $p$" could be more specific: "HB-corrected $p$" (Holm--Bonferroni).

### Figures and Tables
- Table 11: Consider adding a row for the Holm--Bonferroni significance threshold (e.g., $0.05/3 = 0.0167$ for the first test).
- Tables 13--16: Report uncertainty (mean $\pm$ std) over seeds, consistent with the ablation tables.

### Citation Format
- The paper uses \citet{} format correctly throughout.
- All references appear complete and properly formatted.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 60 | Adequate | No methodological novelty; the contribution is analytical. The mechanism analysis is the primary novel element. |
| Methodological Rigor (25%) | 85 | Strong | Excellent statistical methodology with proper corrections, effect sizes, and control experiments. Minor issues with BER sample size and support recovery uncertainty. |
| Evidence Sufficiency (25%) | 80 | Strong | Comprehensive experiments across multiple dimensions. FISTA comparison is valuable. Mechanism analysis lacks uncertainty quantification. |
| Argument Coherence (15%) | 82 | Strong | Clear logical flow from NMSE saturation to mechanism analysis to BER implications. |
| Writing Quality (15%) | 80 | Strong | Professional writing with good transparency. Minor use of internal jargon. |
| **Weighted Average** | **78.0** | **Minor Revision** | |

---

