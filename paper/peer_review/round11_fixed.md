# Round 11 Revision Summary

**Date:** 2026-06-01
**Decision:** Major Revision (Round 10 editorial decision)
**Revisions addressed:** 5 required revisions (R1–R5)

---

## R1: Add ITU Channel Error Sparsity Analysis ✅

**Reviewer concern:** R2 (Domain) Critical — mechanism analysis limited to i.i.d. Gaussian channels; generalizability to correlated-tap channels unknown.

**Changes:**
- Added new subsection "Generalizability to ITU Channel Models" (Section 4.12) with Table `tab:error_sparsity_itu`
- Error sparsity analysis on ITU PedA and VehA at SNR=20 dB:
  - PedA: LISTA 99.3% on true taps vs OMP 95.8% (6.0× less non-support error)
  - VehA: LISTA 99.5% on true taps vs OMP 96.1% (7.8× less non-support error)
- Mechanism generalizes: slightly less extreme than Gaussian (99.9% vs 94.9%, 50×) but qualitative pattern preserved
- Updated abstract, highlights, and conclusion to mention ITU generalization
- Updated scope paragraph to note ITU support for the generalizability hypothesis

**Acceptance criterion:** Error concentration mechanism tested on at least one non-Gaussian channel model → ✅ (tested on both PedA and VehA)

---

## R2: Shorten MMSE BER Section ✅

**Reviewer concern:** R2 (Domain) W2 — MMSE BER equivalence is trivially expected; section ~2000 words inflates a non-contribution.

**Changes:**
- Section 4.10.1 (MMSE Equalization): reduced from ~800 words to ~60 words (kept table, removed verbose explanation)
- Removed redundant paragraph explaining why MMSE convergence is expected
- Shortened ZF equalization explanation paragraph
- Shortened Statistical Summary to 2 sentences
- Shortened Discussion "Implications for MMSE-based systems" from 3 paragraphs to 1 paragraph
- Removed the long "Does LISTA's error structure provide BER advantage over a generic estimator under MMSE?" paragraph (this was 400+ words explaining a non-result)
- Total MMSE-related text reduced by ~60%

**Acceptance criterion:** MMSE BER section reduced to <800 words → ✅

---

## R3: Reframe 33× Speedup as Implementation Efficiency ✅

**Reviewer concern:** R2 W5, R3 W2 — 33× speedup is a Python software artifact, not an algorithmic advantage; misleading.

**Changes:**
- Runtime table (Table `tab:runtime`): changed column header from "Speedup vs OMP" to "FLOPs (×10³)"; table caption now explicitly states "reflects software implementation overhead, not algorithmic efficiency"
- Table description paragraph: reframed to explain that LISTA requires 2.3× MORE FLOPs than OMP; the Python speedup reflects BLAS optimization of feedforward operations vs Python interpreter overhead in iterative greedy selection
- Introduction contribution #6: changed from "Python benchmarks confirm 33× faster inference" to "Python benchmarks show 33× faster LISTA inference, but this reflects interpreter overhead differences... not algorithmic efficiency"
- Added explicit "Interpretation" paragraph explaining that FLOP count is the relevant metric for hardware, and LISTA's advantage is in pipelined throughput, not per-estimate cost
- Hardware section: removed "relative speed advantage of LISTA over OMP may be preserved in hardware" claim
- Discussion: reframed to "LISTA's potential hardware advantage lies in pipelined throughput via its fixed-depth feedforward architecture, not per-estimate computational cost"

**Acceptance criterion:** 33× speedup consistently presented as software artifact, not algorithmic advantage → ✅

---

## R4: Reposition Narrative to "Systematic Analysis" ✅

**Reviewer concern:** R2 W1, Devil's Advocate C1 — paper frames negative results as "practical alternative" despite 13–33 dB NMSE gap.

**Changes:**
- Title: changed from "Generalization, Ablation, and Practical Limitations" to "Generalization, Error Structure, and Ablation"
- Abstract: changed "establish LISTA as a practical alternative" to "provide a systematic characterization of LISTA"
- Introduction: changed "with emphasis on practical deployment advantages" to "focusing on understanding its behavior, generalization properties, and error structure rather than claiming architectural novelty"
- Conclusion: changed "establish LISTA as a practical tool" to "provide a systematic characterization of deep-unfolded sparse channel estimation"
- Discussion: changed "Use LISTA for speed" to "Use LISTA for throughput"; changed "LISTA is the preferred choice" to "LISTA is a viable choice"
- All instances of "practical alternative" and "practical tool" removed

**Acceptance criterion:** Paper framing consistently positions contribution as analysis, not as advocacy → ✅

---

## R5: Shorten Hardware Section ✅

**Reviewer concern:** R3 W1 — no measured hardware validation; section is entirely theoretical and speculative.

**Changes:**
- Section 4.13: condensed from 5 subsections (~2500 words) to 1 section (~400 words)
- Removed: detailed Parallelism Characteristics subsection (intra-layer, batch, pipeline parallelism)
- Removed: detailed Memory Access Patterns subsection (cache analysis, L1/L2 estimates)
- Removed: Hardware Timing Estimates subsection (23 μs sequential, 1.2 μs pipelined, 5 μs OMP)
- Kept: FLOPs table (Table `tab:flops`) — essential quantitative comparison
- Kept: Scaling table (Table `tab:scaling`) — demonstrates N² problem
- Kept: Key insight about pipelining as LISTA's potential hardware advantage
- Added explicit "All hardware estimates are theoretical; measured FPGA/ASIC results remain future work"
- Updated summary and discussion to match condensed hardware content

**Acceptance criterion:** Hardware section reduced to <1000 words with no speculative timing estimates → ✅

---

## Summary of All Changes

| Revision | Status | Key Change |
|----------|--------|------------|
| R1 | ✅ | Added ITU PedA/VehA error sparsity analysis (99.3–99.5% on true taps) |
| R2 | ✅ | MMSE BER section reduced ~60%; removed verbose non-result explanations |
| R3 | ✅ | 33× speedup reframed as software artifact; FLOP count emphasized |
| R4 | ✅ | Narrative repositioned from "practical alternative" to "systematic analysis" |
| R5 | ✅ | Hardware section reduced from 5 subsections to 1; removed speculative timing |

## Files Modified

- `paper/main.tex` — all 5 revisions
- `paper/main.abs` — R1 (ITU mention), R4 (narrative repositioning)
- `paper/peer_review/round11_fixed.md` — this summary
