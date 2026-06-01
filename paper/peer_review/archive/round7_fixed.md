# Round 7 Revision Summary

**Date:** 2026-06-01  
**Decision:** Minor Revision (Round 6, avg score 70.2/100)  
**Deadline:** 2026-06-29  

## Required Revisions Addressed

### R1: Qualify Hardware Claims as Theoretical ✅

**Issue:** Hardware throughput claims (4.4× advantage, FPGA timing estimates) were presented without adequate qualification that they are theoretical estimates, not measured results.

**Changes made:**
- Updated abstract: added "theoretical estimates based on FLOP counts and pipeline analysis; measured FPGA/ASIC results remain future work"
- Updated highlights: changed "Hardware throughput" to "Theoretical hardware throughput"
- Updated Introduction contribution 6: explicitly labeled as theoretical estimates with "measured FPGA/ASIC results remain future work"
- Updated Experiment 13 title: changed to "Theoretical Hardware Complexity Analysis"
- Updated Experiment 13 text: added explicit disclaimer about theoretical nature
- Updated Discussion: added "theoretical" qualifiers to all hardware claims
- Updated Limitations: added "but actual FPGA/ASIC measurements are needed to validate the claims"
- Updated Conclusion: changed to "theoretical analysis suggests" and added "Measured FPGA/ASIC validation remains important future work"
- Updated all deployment recommendations: qualified as theoretical

### R2: Add DL Baseline Comparison ✅

**Issue:** No comparison with CNN/Transformer channel estimation methods, which is a significant gap given the extensive literature on deep learning for channel estimation.

**Changes made:**
- Added new Discussion subsection "Comparison with Deep Learning Baselines" (Section 5.3) with:
  - Model-based vs. data-driven comparison (parameter count, interpretability, generalization)
  - Expected NMSE comparison based on published results
  - Computational efficiency comparison (FLOPs)
  - Limitations of qualitative comparison acknowledged
- Updated Experiments baselines section: added note explaining why DL baselines aren't included, with cross-reference to Discussion
- Added proper label (sec:dl_comparison) for cross-referencing

### R3: Restructure BER Presentation (MMSE Primary, ZF Secondary) ✅

**Issue:** BER analysis was presented with ZF as the primary result and MMSE as secondary, but MMSE is the standard equalizer in modern receivers.

**Changes made:**
- Restructured Experiment 10:
  - Introductory paragraph now frames MMSE as the standard equalizer
  - New "MMSE Equalization (Primary Result)" subsection presented first with full table (tab:ber_mmse)
  - New "ZF Equalization (Error Structure Analysis)" subsection presented second
  - Statistical Summary now leads with MMSE finding ("no BER penalty")
- Updated abstract: leads with MMSE result ("under MMSE equalization (the standard in modern receivers), all methods converge to similar BER at SNR ≥ 5 dB")
- Updated highlights: leads with MMSE result
- Updated Introduction contribution 2: leads with MMSE
- Updated Discussion: restructured to lead with MMSE
- Updated Summary of Results: leads with MMSE
- Updated Limitations: leads with MMSE
- Updated Conclusion: leads with MMSE
- All cross-references updated (tab:ber_mmse, tab:ber_mmse_zf)

### R4: Acknowledge NMSE Saturation as Training Artifact ✅

**Issue:** The NMSE saturation at -25 dB may be caused by the scale-invariant loss and mixed-SNR training (a training artifact) rather than a fundamental architectural limitation of deep unfolding.

**Changes made:**
- Rewrote "Is the saturation architecture-specific?" section with new title "Is the saturation architecture-specific or a training artifact?"
- Added three explicit evidence points:
  1. Scale-invariant loss produces noise-floor-like saturation
  2. SNR-specific training breaks the saturation (6 dB improvement)
  3. LISTA-CP constraints naturally satisfied (not a convergence issue)
- Added explicit statement: "the saturation is primarily a training artifact rather than an architectural limitation"
- Added implication: "LISTA's NMSE can be further improved through better training strategies (e.g., curriculum learning, SNR-adaptive loss functions) without architectural changes"
- Updated abstract: added "(likely a training artifact from the scale-invariant loss and mixed-SNR training, not an architectural limitation)"
- Updated Introduction contribution 1: changed to "likely a training artifact caused by the scale-invariant loss and mixed-SNR training, rather than a fundamental architectural limitation"
- Updated Limitations: added "This saturation is likely a training artifact caused by the scale-invariant NMSE loss and mixed-SNR training distribution, rather than a fundamental architectural limitation"

## Files Modified

- `paper/main.tex` — All 4 required revisions applied

## Summary of Key Framing Changes

| Aspect | Before (Round 6) | After (Round 7) |
|--------|------------------|-----------------|
| Hardware claims | Presented as advantages | Qualified as theoretical estimates |
| DL baselines | Not addressed | Qualitative comparison in Discussion |
| BER presentation | ZF primary, MMSE secondary | MMSE primary, ZF secondary |
| NMSE saturation | Architectural limitation | Training artifact (with evidence) |

## Response to Reviewer Concerns

### R1 (Perspective Reviewer - Hardware)
The paper now consistently qualifies all hardware claims as theoretical estimates. The 4.4× throughput advantage is presented as a theoretical pipeline analysis result, with explicit acknowledgment that measured FPGA/ASIC results remain future work. This addresses the reviewer's concern about "entirely theoretical" claims.

### R2 (EIC & Domain Reviewer - DL Baselines)
A new Discussion subsection provides qualitative comparison with CNN/Transformer methods based on published results. The comparison covers parameter count, computational efficiency, interpretability, and generalization. The limitation of this qualitative approach is acknowledged, and direct experimental comparison is recommended as future work.

### R3 (Editorial Decision - BER Restructuring)
BER presentation now leads with MMSE equalization as the primary result, establishing that LISTA achieves comparable BER to OMP under the standard equalizer. ZF is presented as a secondary analysis revealing LISTA's error structure properties. This addresses the concern about "confirmation bias in selecting ZF BER as primary metric."

### R4 (Devil's Advocate - Training Artifact)
The paper now explicitly acknowledges that the NMSE saturation is likely a training artifact rather than an architectural limitation, with three supporting evidence points. This addresses the concern that the paper's claims about architectural limitations were overstated.
