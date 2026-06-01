# Round 16 — Revision Summary

## Date: 2026-06-01

### Overview
Addressed all 6 required revisions from Round 15 peer review (EIC, R1-Methodology, R2-Domain, R3-Perspective, Devil's Advocate).

---

## R1: Rewrite Abstract and Highlights ✅

**Source**: EIC (W1), Devil's Advocate (C2, M2) — Narrative tension between honest limitations and highlights positioning.

**Changes**:
- **Abstract** (`main.tex` lines 57-59, `main.abs`): Restructured to lead with NMSE limitations ("LISTA trails OMP by 13–33 dB and FISTA by 1–27 dB") before presenting the error concentration mechanism. Added explicit mention that FISTA outperforms LISTA at all SNR levels without training data, and that under MMSE equalization all estimators converge to similar BER. Error concentration is now positioned as "Despite these NMSE limitations, a mechanism analysis reveals..." rather than as the primary lead.
- **Highlights** (`main.tex` lines 62-67): Restructured with the first bullet now stating the NMSE gap and FISTA superiority. Error concentration moved to second bullet. Added note about real-valued channel assumption in the last bullet.

**Acceptance criteria met**: A reader scanning only the abstract and highlights now forms an accurate impression of LISTA's practical limitations before learning about the error concentration finding.

---

## R2: Add Missing LISTA Variant References ✅

**Source**: R2-Domain (W1) — Incomplete literature coverage of ALISTA, LISTA-CPSS, Elastic LISTA.

**Changes**:
- **`references.bib`**: Added 3 new entries:
  - `liu2019alista` — ALISTA (Analytic LISTA with optimal weight initialization)
  - `chen2020lista_cpss` — LISTA-CPSS (progressive support selection)
  - `liu2021elastic_lista` — Elastic LISTA (elastic net regularization)
- **Section 2.2** (`main.tex`): Added discussion paragraph covering all three variants and their relevance to the paper's analysis of $\mathbf{W}^{(k)}$.

**Acceptance criteria met**: The related work section now covers the major LISTA variants published through 2024.

---

## R3: Reframe AMP Connection ✅

**Source**: EIC (W4), R2-Domain (W3), Devil's Advocate (m3) — AMP connection presented as new theory but reinvents existing work.

**Changes**:
- **Section 5.1** (`main.tex`): Renamed subsection heading to "Contextualizing the error concentration via AMP theory." Added explicit statement: "We do not claim new theoretical contributions here but instead contextualize our empirical findings within this existing framework." Cited Borgerding et al. (2020) and Liu et al. (2023) as prior work that established the Onsager connection. Added honest caveat: "we have not empirically validated this by comparing $\mathbf{W}^{(k)}$ against the theoretical Onsager correction matrix---this remains an important direction for future work."
- **Conclusion** (`main.tex`): Updated to say "contextualize" rather than "connect/argue" and cite prior work.

**Acceptance criteria met**: The AMP discussion is clearly positioned as contextualizing existing theory, not proposing new theory.

---

## R4: Formalize Error Concentration Metric ✅

**Source**: R1-Methodology (W2) — Error concentration metric needs formal definition and confidence intervals.

**Changes**:
- **Section 4.12.2** (`main.tex`): Added formal definition equation:
  $$\text{Error on } S = \frac{\sum_{i \in S} (\hat{h}_i - h_i)^2}{\sum_{i=1}^N (\hat{h}_i - h_i)^2} \times 100\%$$
  with degenerate case handling (zero total error → 100% by convention).
- **Table 10** (error sparsity): Added 95% CI footnote for "Error on S" metric.
- **Table 11** (ISTA control): Added 95% CI footnote for "Error on S" metric.
- CIs computed as $\bar{x} \pm t_{0.025,4} \cdot s / \sqrt{5}$ with $t_{0.025,4} = 2.776$.

**Acceptance criteria met**: The metric is formally defined with an equation, degenerate case handling, and 95% confidence intervals.

---

## R5: Discuss Real-Valued Channel Limitation ✅

**Source**: R3-Perspective (W1) — Real-valued channel assumption limits generalizability.

**Changes**:
- **Section 5.4** (`main.tex`): Added new paragraph "Real-valued channel assumption" that:
  - States all experiments use real-valued channels and BPSK pilots
  - Explains the complex-valued soft-thresholding extension ($\mathcal{S}_\theta(\mathbf{z}) = \mathbf{z} \cdot \max(1 - \theta/|\mathbf{z}|, 0)$)
  - Acknowledges the error concentration mechanism may behave differently for complex channels due to phase degrees of freedom
  - Identifies extension to complex-valued channels and MIMO as important future work
- **Highlights** (`main.tex`): Added note "All results assume real-valued channels; extension to complex-valued channels remains future work."

**Acceptance criteria met**: The limitation is clearly stated with discussion of how findings might change for complex-valued channels.

---

## R6: Remove Qualitative CNN/Transformer Comparison ✅

**Source**: R2-Domain (W4), Devil's Advocate — Table 17 draws conclusions from incomparable experimental results.

**Changes**:
- **Section 5.2** (`main.tex`): Removed Table 17 (qualitative comparison) and all quantitative claims drawn from published results (parameter counts, FLOP ranges, NMSE ranges for CNN/Transformer). Replaced with:
  - Retained the qualitative "Model-based vs. data-driven" discussion (structural distinctions are valid without direct comparison)
  - Added "Why we do not provide a quantitative comparison" paragraph explaining that published results use different experimental configurations and drawing conclusions would be misleading
  - Explicitly states: "A comprehensive benchmark comparing LISTA, CNN, and Transformer methods under identical experimental conditions... is important future work"

**Acceptance criteria met**: The paper no longer draws conclusions from incomparable experimental results.

---

## Summary of Files Modified

| File | Changes |
|------|---------|
| `paper/main.tex` | Abstract, highlights, Section 2.2 (new LISTA variants), Section 4.12.2 (formal definition + CIs), Section 5.1 (AMP reframe), Section 5.2 (DL comparison replacement), Section 5.4 (real-valued limitation), Conclusion |
| `paper/main.abs` | Complete rewrite to match new abstract |
| `paper/references.bib` | Added 3 new entries (ALISTA, LISTA-CPSS, Elastic LISTA) |
| `paper/peer_review/round16_fixed.md` | This file |
