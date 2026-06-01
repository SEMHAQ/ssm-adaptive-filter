# Phase 0: Field Analysis & Reviewer Configuration

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Author**: Huanjie Yu (Hunan University of Technology and Business)
- **Target Journal**: Digital Signal Processing (Elsevier)
- **Review Date**: 2026-06-01
- **Review Round**: Round 6

---

## Field Analysis

### Primary Discipline
**Signal Processing / Wireless Communications**

### Secondary Discipline
**Machine Learning / Deep Learning for Communications**

### Research Paradigm
Empirical / Computational — combines theoretical analysis with extensive experimental validation

### Methodology Type
- Algorithm design and evaluation
- Deep unfolding (model-based deep learning)
- Monte Carlo simulation with statistical validation
- Hardware complexity analysis (theoretical FLOPs + pipelining estimates)

### Target Journal Tier
Mid-to-upper tier — *Digital Signal Processing* (Elsevier) is a well-regarded journal in the signal processing community, impact factor ~3.0–3.5. Not top-tier (IEEE TSP, JSTSP) but solid.

### Paper Maturity
**Late-stage revision** — The paper has undergone multiple rounds of revision (Round 6), with extensive statistical validation (20 seeds for ablation, 200 realizations for BER, paired t-tests, Cohen's d), cross-distribution generalization tests, and hardware complexity analysis. The authors have clearly addressed prior review concerns about statistical rigor.

---

## Reviewer Configuration

### EIC: Prof. Elena Marchetti
- **Journal**: Associate Editor, *Digital Signal Processing* (Elsevier)
- **Expertise**: Model-based deep learning for signal processing, algorithm-hardware co-design
- **Review Preferences**: Focuses on journal fit, practical relevance, clarity of presentation, and whether the contribution is sufficient for DSP readership. Values papers that bridge theory and practice. Expects clear positioning relative to existing work.

### Reviewer 1 (Methodology): Prof. Kai Zhang
- **Expertise**: Statistical signal processing, compressed sensing theory, optimization algorithms for sparse recovery
- **Particular Focus**: Experimental design rigor, statistical validity (power analysis, effect sizes, multiple comparisons), reproducibility of computational experiments, fairness of baseline comparisons
- **Known tendencies**: Strict about statistical reporting standards; will flag underpowered experiments or missing confidence intervals

### Reviewer 2 (Domain): Prof. Maria Santos
- **Expertise**: Deep learning for wireless communications, channel estimation in MIMO/OFDM systems, FPGA implementation of neural networks
- **Particular Focus**: Literature completeness (especially recent 2023–2025 deep learning channel estimation papers), positioning relative to state-of-the-art, practical deployment considerations
- **Known tendencies**: Will check for missing comparisons with recent DL-based channel estimation methods

### Reviewer 3 (Perspective): Prof. James Thornton
- **Expertise**: Hardware acceleration of ML algorithms, FPGA/ASIC design for communications, real-time systems
- **Particular Focus**: Hardware complexity claims, scalability analysis, practical deployment feasibility, cross-disciplinary impact (ML + hardware + communications)
- **Known tendencies**: Skeptical of theoretical FLOPs claims without measured hardware results; values real implementation data

### Devil's Advocate: Unnamed (stress-test role)
- **Focus**: Challenge core arguments, detect logical gaps, find strongest counter-arguments
- **Particular Attack Surface**: NMSE-BER disconnect claim, saturation explanation, generalization claims, hardware throughput estimates
