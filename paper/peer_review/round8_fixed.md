# Round 8 Revision Summary

**Date:** 2026-06-01
**Decision:** Minor Revision (Round 7)
**Deadline:** 2026-07-01

## Required Revisions Addressed

### R1: Qualify Hardware Claims in Abstract and Highlights ✅

**Issue:** Hardware throughput claims (4.4× advantage, 33× Python speedup) were presented without sufficient qualification that they are theoretical estimates, not measured results. The "33× faster in Python" in highlights was misleading.

**Changes made:**
- Updated highlights: removed "33× faster in Python (interpreter overhead)" from the hardware bullet; added "measured FPGA/ASIC validation remains future work"
- Updated highlights: replaced duplicate "Theoretical hardware complexity" bullet with "SNR-specific training mitigates saturation" (more informative)
- Updated abstract: removed "($33\times$ faster in Python, reflecting interpreter overhead)" parenthetical from hardware claims
- All hardware claims in abstract/highlights now include "theoretical" or "estimated" qualifiers
- The abstract retains the "measured FPGA/ASIC results remain future work" disclaimer

**Acceptance criteria met:** Every hardware claim in abstract/highlights includes a "theoretical/estimated" qualifier. The 33× Python speedup is not in the highlights.

### R2: Resolve Cross-Table Inconsistency (Table 1 vs Table 3) ✅

**Issue:** Table 1 reports LISTA at -24.25 dB and Table 3 at -32.29 dB for the same nominal configuration (N=64, K=5, M=256, L=20, SNR=20). The ~8 dB discrepancy was attributed to "different training distributions" but the explanation was insufficient.

**Changes made:**
- Updated Table 1 caption: added "LISTA trained with mixed-SNR protocol (SNR ∈ [0, 30] dB)"
- Updated Table 3 caption: added "LISTA trained with channel-length variation protocol (varying N from 32 to 256)"
- Strengthened the explanation paragraph in Section 4.3:
  - Clarified which training protocol each table uses
  - Added guidance: "The mixed-SNR model (Table 1) represents the realistic deployment scenario... and should be treated as the primary reference for LISTA's practical performance"
  - Explained that the channel-length model demonstrates LISTA can be improved when operating conditions are known at training time
  - Reframed the sensitivity as "a characteristic behavior of deep-unfolded architectures and underscores the importance of matching the training protocol to the deployment scenario"

**Acceptance criteria met:** Readers can identify which training protocol was used for each table and understand the discrepancy. The mixed-SNR model is designated as the primary reference.

### R3: Add CNN/Transformer Comparison Table ✅

**Issue:** The paper excluded CNN and Transformer baselines, providing only qualitative comparison in Section 5.2. Reviewers expected at least a structured comparison table.

**Changes made:**
- Added new Table (tab:dl_comparison) in Section 5.2 with structured comparison across 7 criteria:
  - Parameters: LISTA 82K vs CNN >500K vs Transformer >1M
  - FLOPs/estimate: LISTA 760K vs CNN 2-10M vs Transformer >50M
  - NMSE (dB): LISTA -25 vs CNN -20 to -30 vs Transformer -25 to -35
  - Requires K: LISTA No, OMP Yes
  - Interpretability: LISTA High, CNN/Transformer Low
  - Cross-distribution: LISTA Good, CNN/Transformer Limited
  - Hardware pipeline: LISTA Yes, CNN/Transformer Complex
- Added disclaimer: "this comparison is indirect---the results are drawn from different studies with varying channel models, SNR ranges, and training protocols"
- Table caption explicitly notes CNN/Transformer values are from published results on comparable (but not identical) channel models

**Acceptance criteria met:** Readers can assess LISTA's performance relative to CNN/Transformer methods across multiple dimensions.

### R4: Reframe BER Conclusion to Acknowledge MMSE Robustness ✅

**Issue:** The abstract and text stated "LISTA achieves comparable BER to OMP" which was misleading because MMSE masks estimator quality differences. The comparable BER should be attributed to MMSE's robustness, not LISTA's quality.

**Changes made across 8 locations:**
1. **Abstract:** Changed to "under MMSE equalization the NMSE gap does not translate to BER penalty (attributable to MMSE's robustness to estimation errors)"
2. **Highlights (BER bullet):** Changed to "LISTA's NMSE gap does not translate to BER penalty at SNR ≥ 5 dB, attributable to MMSE's robustness to estimation errors"
3. **Introduction contribution 2:** Changed to "attributable to MMSE's robustness to estimation errors---the equalizer, not the estimator quality, drives the BER convergence"
4. **Experiment 10 MMSE text:** Changed to "attributable to MMSE's regularization: the term 1/SNR suppresses the noise enhancement differences between estimators, rendering LISTA's NMSE gap irrelevant to BER"
5. **Experiment 10 Statistical Summary:** Changed to "MMSE's regularization term 1/SNR suppresses the noise enhancement difference between estimators---MMSE equalization is inherently robust to the estimation errors that distinguish LISTA from OMP"
6. **Discussion "Implications for MMSE":** Changed to "the comparable BER under MMSE should therefore be interpreted as evidence of MMSE's robustness to estimation errors, not as evidence that LISTA matches OMP's estimation quality"
7. **Summary of Results:** Changed to "attributable to MMSE's robustness to estimation errors"
8. **Conclusion:** Changed to "attributable to MMSE's regularization of noise enhancement differences between estimators"
9. **Limitations:** Changed to "This is attributable to MMSE's robustness to estimation errors---the equalizer's regularization suppresses the noise enhancement differences between estimators"
10. **Deployment recommendation:** Changed to "LISTA's NMSE gap does not translate to BER penalty"
11. **BER table footnote:** Changed to "attributable to MMSE's robustness to estimation errors"

**Acceptance criteria met:** All BER conclusions clearly attribute comparable BER to MMSE robustness, not LISTA quality. The framing consistently states that the equalizer masks the NMSE gap.

## Files Modified

- `paper/main.tex` — All 4 required revisions applied

## Summary of Key Framing Changes

| Aspect | Before (Round 7) | After (Round 8) |
|--------|------------------|-----------------|
| Hardware highlights | "33× faster in Python" included | Removed; replaced with "measured FPGA/ASIC validation remains future work" |
| Table consistency | Explanation paragraph only | Training protocol in captions + clearer resolution guidance |
| DL comparison | Qualitative text only | Structured comparison table (7 criteria) |
| BER framing | "LISTA achieves comparable BER" | "MMSE's robustness masks the NMSE gap" |

## Response to Reviewer Concerns

### R1 (EIC, R3, DA - Hardware Claims)
The "33× faster in Python" has been removed from highlights. All hardware claims in abstract and highlights now include explicit "theoretical" or "estimated" qualifiers. The disclaimer "measured FPGA/ASIC validation remains future work" is now in the highlights.

### R2 (EIC, R1, DA - Cross-Table Consistency)
Both Table 1 and Table 3 captions now explicitly state their training protocols. The explanation paragraph designates the mixed-SNR model (Table 1) as the primary reference for practical performance, and explains the channel-length model as demonstrating optimization potential under known conditions. The sensitivity is framed as a characteristic of deep-unfolded architectures.

### R3 (EIC, R2, DA - DL Baselines)
A new structured comparison table (Table:dl_comparison) compares LISTA against CNN and Transformer methods across 7 criteria (parameters, FLOPs, NMSE, sparsity requirement, interpretability, cross-distribution generalization, hardware pipeline). The table includes explicit caveats about the indirect nature of the comparison.

### R4 (DA - BER Framing)
All BER conclusions across the paper (abstract, highlights, introduction, experiments, discussion, summary, limitations, conclusion) now consistently attribute the comparable BER under MMSE to the equalizer's robustness to estimation errors, not to LISTA matching OMP's quality. The framing clearly states that MMSE's regularization term suppresses noise enhancement differences, rendering the NMSE gap irrelevant to BER.
