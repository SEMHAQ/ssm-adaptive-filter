# Round 12 Revision Summary

**Date**: 2026-06-01
**Based on**: Round 11 review reports (8 files)

---

## Issues Addressed

### R1: Remove Hardware Throughput Claims from Abstract/Highlights ✅

**Problem**: The abstract and highlights contained theoretical hardware throughput claims ("20-stage pipelining suggests potential for hardware throughput advantage over OMP") that are entirely theoretical with no measured validation. The devil's advocate review and other reviewers flagged this as overclaiming.

**Changes**:
- **Abstract**: Removed all hardware throughput, FLOP count, and pipelining claims. The abstract now focuses on LISTA's performance, error concentration mechanism, ablation, and SNR mitigation only.
- **Highlights**: Removed the second highlight item entirely ("Theoretical hardware complexity: 760K FLOPs..."). The remaining highlights focus on error concentration, ablation, generalization, and SNR mitigation.

**Rationale**: Hardware throughput advantage is entirely theoretical (no FPGA/ASIC measurements) and should not appear in the abstract/highlights, which set reader expectations. The theoretical complexity analysis remains in Section 4.13 (Theoretical Hardware Complexity) and the Discussion/Limitations for readers interested in deployment considerations.

---

### R2: Reframe ZF BER Results as Evidence of Error Concentration Mechanism ✅

**Problem**: The ZF BER results were presented as a standalone performance advantage, which reviewers found misleading since ZF is rarely used in practice. The framing needed to clarify that ZF BER results serve as *evidence* for the error concentration mechanism, not as a practical advantage.

**Changes**:
- **Abstract**: Changed from "The error structure advantage is masked under MMSE...but manifests under ZF equalization, where LISTA achieves comparable QPSK BER and statistically significantly better 16-QAM BER" to "This error concentration...provides direct evidence explaining LISTA's BER behavior: the advantage is masked under MMSE but manifests under ZF equalization, where LISTA achieves significantly better 16-QAM BER at SNR ≥ 15 dB (p < 0.05), reducing noise enhancement by 1.8×."
- **Highlights**: Changed from "providing tangible BER benefit under ZF equalization for 16-QAM" to "this mechanism provides direct evidence for LISTA's BER behavior, manifesting as significantly better 16-QAM BER under ZF equalization."

**Rationale**: The ZF results are valuable not as a practical deployment scenario but as experimental evidence that LISTA's error concentration on true taps has measurable consequences. Under MMSE (the practical equalizer), the advantage is masked — this is expected. Under ZF (which is sensitive to error location), the advantage manifests, confirming the mechanism. The reframing positions ZF BER as diagnostic evidence rather than a performance claim.

---

### R3: Compress Abstract to ~200 Words ✅

**Problem**: The original abstract was ~350 words — far too long for a journal paper. The target is ~200 words.

**Changes**: Compressed from ~350 words to ~208 words by:
- Removing hardware throughput/FLOP/pipelining claims (saves ~50 words)
- Removing redundant statistical methodology details ("validated with 200 channel realizations per SNR point, paired t-tests, and 95% confidence intervals across 5 random seeds" → "200 realizations, paired t-tests")
- Removing LISTA-CP evaluation from abstract (secondary result)
- Condensing the opening ("Sparse channel estimation is a fundamental problem..." → direct entry with LISTA)
- Removing noise enhancement detail from ZF section
- Keeping all core contributions: NMSE performance, error concentration mechanism, ablation, SNR mitigation

**Final word count**: ~208 words

---

## Files Modified

| File | Changes |
|------|---------|
| `paper/main.tex` | Abstract rewritten (~208 words), highlights reworded |
| `paper/main.abs` | Synchronized with new abstract |

## Verification

- Abstract: ~208 words (target ~200) ✅
- No hardware throughput claims in abstract or highlights ✅
- ZF BER framed as mechanism evidence, not performance claim ✅
- All technical content in main paper body preserved unchanged
- Theoretical hardware complexity section (4.13) and Discussion (5.4) retained for interested readers
