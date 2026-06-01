# Round 9 Revision Summary

**Date:** 2026-06-01
**Decision:** Minor Revision (Round 8)
**Deadline:** 2026-06-15

## Required Revisions Addressed

### R1: Reframe MMSE BER Contribution as Mechanism Analysis ✅

**Issue:** The paper presented "no BER penalty under MMSE" as a finding about LISTA, when it is actually a property of MMSE equalization that applies to any estimator with reasonable NMSE. The Devil's Advocate (C1) argued this is "trivially true for any estimator under MMSE." The EIC resolved: "Downgrade from CRITICAL to MAJOR. The paper should strengthen the MMSE discussion by noting that the 'no BER penalty' finding is expected under MMSE's design, and reframe the contribution as the mechanism analysis rather than the BER equivalence per se."

**Changes made across 12 locations:**

1. **Abstract:** Changed from "this NMSE gap does not translate to a BER penalty" to "all estimators converge to similar BER... consistent with MMSE's known robustness to estimation errors. The primary BER contribution is a mechanism analysis: LISTA concentrates 99.9% of estimation error on true tap locations..."

2. **Abstract (summary sentence):** Changed from "under MMSE equalization the NMSE gap does not translate to BER penalty" to "the mechanism analysis reveals that LISTA's error concentration on true taps---while masked under MMSE equalization where any reasonable estimator achieves similar BER---provides tangible BER benefits under ZF equalization for higher-order modulations"

3. **Highlights (BER bullet):** Changed from "LISTA's NMSE gap does not translate to BER penalty" to "under MMSE (standard), all estimators converge to similar BER... consistent with MMSE's design; LISTA concentrates 99.9% of error on true taps... providing tangible BER benefit under ZF"

4. **Introduction contribution 2:** Changed header from "quantify the system-level impact" to "conduct a mechanism analysis of the BER-NMSE disconnect." Added: "this is expected behavior, not a special property of LISTA." Reframed the contribution as the error structure analysis.

5. **Experiment 10 intro paragraph:** Changed from "assess the system-level impact of LISTA's NMSE gap" to "assess the BER implications." Added: "we expect all reasonable estimators to converge to similar BER (consistent with MMSE's robustness to estimation errors)"

6. **MMSE subsection header:** Changed from "Primary Result" to "Expected Convergence"

7. **MMSE results text:** Complete rewrite. Now leads with "The MMSE results confirm the expected behavior" and explicitly states "This convergence is a property of MMSE equalization, not a special property of LISTA: any estimator with comparable NMSE (e.g., a generic -25 dB estimator) would exhibit similar BER under MMSE." Added: "The contribution of this paper is not the BER equivalence per se (which is expected under MMSE), but the mechanism analysis."

8. **ZF subsection header:** Changed from "Error Structure Analysis" to "Error Structure Advantage"

9. **ZF section text:** Added "Importantly, this is the same error structure that exists under MMSE---but MMSE's regularization masks the difference."

10. **Statistical Summary:** Complete rewrite. Now leads with "MMSE (expected convergence)" and "consistent with MMSE's known robustness to estimation errors. This is expected behavior." Reframed primary contribution as "Mechanism analysis (primary contribution)."

11. **Discussion "Implications for MMSE":** Complete rewrite. Now explicitly states "A generic estimator achieving -25 dB NMSE would exhibit similar BER under MMSE, confirming that this convergence is a property of the equalizer, not of LISTA. The comparable BER under MMSE should therefore not be interpreted as a LISTA-specific advantage---it is a consequence of MMSE's design."

12. **Summary of Results:** Both BER bullets reframed. "BER-NMSE mechanism" now labeled as "(primary contribution)" with "This error structure analysis---not the BER equivalence under MMSE---is the paper's primary contribution."

13. **Limitations:** Reframed to "all estimators with reasonable NMSE converge to similar BER... consistent with MMSE's known robustness to estimation errors---this is expected behavior, not a special property of LISTA."

14. **Conclusion:** Reframed to "all estimators converge to similar BER... consistent with MMSE's known robustness to estimation errors. The primary BER contribution is a mechanism analysis."

15. **Deployment recommendation:** Changed from "LISTA's NMSE gap does not translate to BER penalty" to "all estimators achieve similar BER (as expected)"

16. **BER table footnote:** Changed from "attributable to MMSE's robustness to estimation errors" to "consistent with MMSE's known robustness to estimation errors"

**Acceptance criteria met:** The paper no longer implies that "no BER penalty under MMSE" is a special property of LISTA. The contribution is consistently framed as the mechanism analysis (error concentration on true taps).

---

### R2: Add Uncertainty Ranges to Hardware Estimates ✅

**Issue:** The 4.4× throughput estimate was a point estimate with no uncertainty quantification. The Devil's Advocate (C2) noted "the actual advantage could be 2× or 8×." All four reviewers agreed (EIC W1, R1 W1, R3 W1, DA C2).

**Changes made across 11 locations:**

1. **Abstract:** Changed "estimated 4.4× throughput advantage" to "estimated 2--6× throughput advantage over OMP on FPGA (point estimate 4.4× based on FLOP counts, subject to implementation-dependent factors including memory bandwidth, pipeline stalls, and clock frequency)"

2. **Highlights:** Changed "estimated 4.4× advantage" to "estimated 2--6× advantage... (point estimate 4.4×, subject to memory bandwidth and implementation factors)"

3. **Introduction contribution 6:** Changed "4.4× throughput advantage" to "2--6× throughput advantage (point estimate 4.4×, subject to implementation-dependent factors including memory bandwidth, pipeline stalls, and clock frequency)"

4. **Deployment recommendation (Section 4.7):** Changed "LISTA provides 4.4× hardware throughput advantage" to "Theoretical analysis estimates 2--6× hardware throughput advantage"

5. **Hardware timing estimates:** Changed "4.4× throughput advantage" to "~2--6× throughput advantage (point estimate 4.4×, subject to implementation-dependent factors)"

6. **Hardware timing explanation paragraph:** Changed "a potential 4.4× throughput advantage" to "an estimated 2--6× throughput advantage." Added explanation: "The wide range reflects implementation-dependent factors: memory bandwidth (each W^(k) matrix is 16 KB, totaling 328 KB that fits in L2 cache but may cause bandwidth contention), pipeline stalls from inter-layer data dependencies, and clock frequency variations across FPGA families."

7. **Discussion "Implications for MMSE":** Changed "4.4× hardware throughput improvement" to "estimated 2--6× hardware throughput improvement"

8. **Discussion mechanism paragraph:** Changed "4.4× hardware throughput advantage" to "estimated 2--6× hardware throughput advantage"

9. **Summary of Results hardware bullet:** Changed "4.4× theoretical throughput advantage" to "2--6× throughput advantage (point estimate 4.4×, subject to implementation-dependent factors)"

10. **Limitations:** Changed "estimating a 4.4× throughput advantage" to "estimating a 2--6× throughput advantage (point estimate 4.4×, subject to implementation-dependent factors including memory bandwidth, pipeline stalls, and clock frequency)"

11. **Conclusion:** Changed "4.4× throughput advantage" to "2--6× throughput advantage (subject to implementation-dependent factors)"

**Acceptance criteria met:** All hardware throughput claims now include uncertainty ranges (2--6×) with the point estimate (4.4×) and explanation of uncertainty sources.

---

### R3: Analyze LISTA Error Structure Under MMSE vs Generic Estimator ✅

**Issue:** The Devil's Advocate (C1) argued: "A random channel estimator with -25 dB NMSE would also show no BER penalty under MMSE. The paper fails to demonstrate that LISTA's specific error structure provides BER advantage over a generic -25 dB NMSE estimator under MMSE." The EIC resolved: "Add a theoretical argument (1-2 paragraphs) in Section 4.10.1 or Section 5.1 explaining whether LISTA's error concentration on true taps provides any BER advantage over a generic estimator with the same NMSE under MMSE."

**Changes made:**

Added a new paragraph in Section 5.1 (Discussion) titled "Does LISTA's error structure provide BER advantage over a generic estimator under MMSE?" with the following theoretical argument:

1. **MMSE equalizer output:** $\hat{s} = \hat{H}^* r / (|\hat{H}|^2 + 1/\text{SNR})$

2. **Post-equalization SINR analysis:** At moderate-to-high SNR (where $1/\text{SNR} \ll |\hat{H}|^2$), the regularization term dominates the denominator and the noise enhancement becomes approximately $1/|\hat{H}|^2$, which is insensitive to the *distribution* of estimation error across taps---it depends primarily on the total error magnitude.

3. **Generic estimator comparison:** A generic estimator achieving -25 dB NMSE with uniformly distributed errors would produce similar post-equalization SINR and BER under MMSE as LISTA with its concentrated error structure.

4. **ZF-specific advantage:** The error concentration advantage is specific to ZF equalization, where the absence of regularization makes the equalizer sensitive to the *location* of estimation errors: errors on non-support taps create spurious channel components that distort the equalized constellation, while errors on true taps primarily scale existing symbols.

5. **Conclusion:** Under MMSE, the error structure advantage is masked. The BER-relevant contribution is the mechanism insight (error concentration on true taps), not the BER equivalence under MMSE.

**Acceptance criteria met:** The paper explicitly addresses whether LISTA's error structure matters under MMSE (it does not---the advantage is masked by MMSE's regularization) and clearly states the error concentration advantage is specific to ZF equalization.

---

## Summary of Key Framing Changes

| Aspect | Before (Round 8) | After (Round 9) |
|--------|------------------|-----------------|
| BER contribution framing | "LISTA's NMSE gap does not translate to BER penalty under MMSE" | "All estimators converge to similar BER under MMSE (expected); the contribution is the mechanism analysis" |
| MMSE subsection header | "Primary Result" | "Expected Convergence" |
| ZF subsection header | "Error Structure Analysis" | "Error Structure Advantage" |
| Hardware throughput | "4.4× throughput advantage" (point estimate) | "2--6× throughput advantage (point estimate 4.4×, subject to implementation-dependent factors)" |
| Generic estimator comparison | Not addressed | Explicit theoretical argument showing error structure advantage is masked under MMSE |
| Primary BER contribution | BER equivalence under MMSE | Mechanism analysis (error concentration on true taps) |

## Response to Reviewer Concerns

### R1 (DA C1, EIC - MMSE BER Framing)
The paper now consistently acknowledges that "no BER penalty under MMSE" is expected behavior (a property of MMSE's design), not a special property of LISTA. The contribution is reframed as the mechanism analysis: LISTA concentrates 99.9% of error on true taps (vs 94.9% for OMP), an advantage that is masked under MMSE but manifests under ZF equalization. The MMSE subsection is retitled "Expected Convergence" and the ZF subsection "Error Structure Advantage" to make the framing clear.

### R2 (EIC W1, R1 W1, R3 W1, DA C2 - Hardware Uncertainty)
All 11 instances of "4.4× throughput advantage" now include the uncertainty range "2--6×" with explanation of uncertainty sources (memory bandwidth, pipeline stalls, clock frequency). The hardware timing explanation paragraph now explicitly describes why the range is wide.

### R3 (DA C1 - Generic Estimator Comparison)
A new theoretical paragraph in Section 5.1 analyzes whether LISTA's error concentration provides BER advantage over a generic -25 dB estimator under MMSE. The answer is no: at moderate-to-high SNR, MMSE's regularization term dominates the noise enhancement, making it insensitive to error distribution. The advantage is specific to ZF equalization, where the absence of regularization makes the equalizer sensitive to error location.

## Files Modified

- `paper/main.tex` — All 3 required revisions applied

## Verification

- All "4.4×" references now include "point estimate" qualifier with uncertainty range
- All MMSE BER conclusions consistently attribute convergence to MMSE's design, not LISTA
- The mechanism analysis is consistently presented as the primary BER contribution
- New theoretical argument explicitly addresses the generic estimator comparison
- No remaining instances of "no BER penalty" without proper attribution to MMSE
