# Editorial Decision (Round 18)

## Manuscript Information
- **Title**: Systematic Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Error Structure, and Ablation
- **Manuscript ID**: DSP-2026-ROUND18
- **Decision Date**: 2026-06-01
- **Review Round**: Round 18

---

## Decision

### Accept

The manuscript presents a comprehensive, honestly framed analysis of LISTA for sparse channel estimation. The Round 18 revision successfully addresses all issues from Round 17: contributions are clearly stated as quantification (not discovery), the AMP connection is appropriately hedged, 95% CIs are added to main tables, edge-case metric behavior is clarified, and a new threshold function comparison experiment provides genuinely novel insight. The paper is ready for publication in *Digital Signal Processing*.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Score |
|----------|------|---------------|------------|-------|
| EIC | Journal Editor | Accept | 5 | 83.4 |
| Reviewer 1 | Methodology Expert | Accept | 5 | 83.6 |
| Reviewer 2 | Domain Expert | Accept | 5 | 82.4 |
| Reviewer 3 | Cross-Disciplinary | Accept | 4 | 81.0 |
| Devil's Advocate | Adversarial Analysis | Minor Revision | — | 79.0 |

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-5]** (All reviewers including DA agree):
1. **The contribution framing is now honest and appropriate.** The "we do not claim to discover" statement and 4-contribution structure are well-received by all reviewers.
2. **The AMP connection is correctly hedged.** All reviewers agree the "consistent with" framing is appropriate.
3. **The statistical methodology is rigorous.** 20-seed ablation, Holm–Bonferroni, Cohen's d, CIs.

**[CONSENSUS-4]** (EIC, R1, R2, R3 agree):
1. **The threshold comparison is a genuine contribution.** The 7.1 dB result is compelling and adds novelty beyond characterization.
2. **The paper is ready for publication.** All four score ≥ 81.

### Points of Disagreement

**Disagreement 1: Whether threshold comparison interpretation overreaches**
- **DA view**: The paper claims LISTA "adapts thresholding behavior" but only shows hard thresholding is better when substituted—different claims.
- **EIC/R1/R2/R3 view**: The result is consistent with the interpretation that the learned schedule adapts toward harder thresholding.
- **Disagreement type**: Interpretation disagreement
- **Editor's Resolution**: The DA's point is valid—the paper could strengthen the interpretation by adding a diagnostic (e.g., comparing effective sparsity patterns). However, the current interpretation is presented as a hypothesis ("suggests," "may be implicitly adapting"), not a claim. The hedging language is appropriate.
- **Resolution Rationale**: The paper uses "suggests" and "may be implicitly adapting," which are appropriately cautious. The diagnostic would strengthen the paper but is not required for acceptance.

---

## Decision Rationale

This manuscript has undergone substantial improvement through the revision process. The Round 17 issues (R1: novelty framing, R2: AMP overclaiming, R3: metric edge cases, R4: missing CIs) are all resolved. The Round 18 additions—a threshold function comparison experiment and reframed 4-contribution structure—strengthen the paper's originality from "characterization" to "quantification with novel experimental insight."

The threshold comparison (Section 4.13) is the key addition: hard thresholding outperforms soft by 7.1 dB (p < 0.001, d=30.3) within the same LISTA architecture. This result has implications for both understanding LISTA's learned behavior and practical hardware deployment. While the DA correctly notes that the interpretation could be strengthened with a diagnostic, the paper's hedging language ("suggests," "may be") is appropriate.

The paper's other contributions—error concentration quantification, BER-NMSE disconnect analysis, ISTA/FISTA control experiments—remain well-supported. The honest reporting of LISTA's limitations (NMSE saturation, FISTA superiority, narrow BER advantage regime) is commendable and strengthens credibility.

I recommend Accept. The paper is ready for publication.

---

## Suggested Revisions (Non-Blocking)

These are suggestions for improvement, not requirements for publication:

| # | Suggestion | Source | Priority |
|---|-----------|--------|----------|
| S1 | Add diagnostic comparing LISTA's effective thresholding behavior to hard thresholding | DA (M1) | P3 |
| S2 | Discuss shrinkage bias as explanation for hard vs. soft gap | R2 (W1) | P3 |
| S3 | Note hardware simplicity of hard thresholding | R3 (W1) | P3 |
| S4 | Run threshold comparison with 10 seeds for robustness | R1 (W1) | P3 |

---

## Closing

We are pleased to accept your manuscript for publication in *Digital Signal Processing*. The paper provides a comprehensive, honestly framed analysis of LISTA for sparse channel estimation, with particular strength in the error concentration quantification, threshold comparison experiment, and practical deployment recommendations. The reviewers commend the transparent reporting of limitations and the rigorous statistical methodology.

Please incorporate the suggested revisions (S1–S4) if possible before the final version, though these are not required for acceptance.

---

## Appendix: Full Reviewer Reports

All five reviewer reports (EIC, R1 Methodology, R2 Domain, R3 Perspective, Devil's Advocate) are attached for the author's reference.

---

*Decision issued by the Editor-in-Chief, Digital Signal Processing*
