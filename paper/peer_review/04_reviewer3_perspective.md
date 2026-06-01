# Peer Review Report — Reviewer 3 (Perspective)

## Manuscript Information
- **Title**: Analysis of Deep-Unfolded LISTA for Sparse Channel Estimation: Generalization, Ablation, and Practical Limitations
- **Manuscript ID**: DSP-2026-XXXX
- **Review Date**: 2026-05-31
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 — Cross-Disciplinary Perspective

### Reviewer Identity
Prof.~Dr.~Sarah Kim, Professor of Machine Learning and Wireless Systems, with expertise spanning deep learning, optimization theory, and practical wireless system deployment. Research focus: model-based deep learning, hardware-efficient AI, and real-world deployment of learned systems.

### Review Focus
Cross-disciplinary connections, practical deployment considerations, real-world impact, hardware efficiency, and whether the findings are relevant beyond the narrow sparse channel estimation community.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision**

### Confidence Score
4 — I am confident in the machine learning and practical deployment aspects. My assessment of the wireless communications specifics is moderate.

### Summary Assessment
This paper evaluates LISTA for sparse channel estimation with a focus on practical deployment. The paper's strength is its honest reporting of both capabilities and limitations, including the SNR saturation behavior and training divergence at large channel lengths. The cross-distribution generalization finding (Gaussian training → ITU outperformance) is practically significant and challenges conventional wisdom.

From a practical deployment perspective, the paper provides useful guidance: LISTA is fast (0.21 ms), compact (82K parameters), and generalizes across channel types. However, the SNR saturation at -23 dB is a serious practical limitation that the paper should address more thoroughly. The paper also lacks discussion of: (1) real-time implementation considerations, (2) model update/retraining strategies, (3) robustness to model mismatch in practice, and (4) comparison with industry-standard methods.

---

## Strengths

### S1: Practical Speed Advantage with Quantified Trade-offs
The paper provides concrete inference time comparisons (LISTA: 0.21 ms vs OMP: 6.91 ms, 33× speedup) and parameter counts (82K). This enables practitioners to assess whether the speed-accuracy trade-off is acceptable for their application. The paper honestly reports that LISTA trails OMP on Gaussian channels, which is important for informed deployment decisions.

### S2: Cross-Distribution Generalization Has Real-World Impact
The finding that Gaussian-trained LISTA outperforms OMP on ITU channels is practically significant because:
- Training data for specific channel models may be scarce or proprietary
- Channel statistics change over time (mobility, environment)
- Gaussian training data can be generated synthetically at no cost
This eliminates a major barrier to deployment: the need for channel-specific training data.

### S3: Ablation Provides Design Insights
The ablation finding that the threshold is the most critical component (not the mapping W) has practical implications:
- Hardware implementations can prioritize threshold learning over matrix multiplication
- Simplified architectures (without W) may be viable for resource-constrained deployments
- The threshold's importance suggests LISTA's advantage comes from sparsity enforcement, not inter-tap correlation exploitation

### S4: Honest Limitations Discussion
The paper's limitations section is unusually honest for this field. Acknowledging the -23 dB saturation, the N=256 divergence, and the L=8 instability shows scientific integrity and helps practitioners make informed decisions.

---

## Weaknesses

### W1: No Real-World Implementation Considerations
**Problem**: The paper evaluates inference time in a controlled Python/PyTorch environment but does not discuss:
- FPGA/ASIC implementation latency
- Quantization effects (INT8, INT4)
- Model compression/pruning for edge deployment
- Power consumption comparison
**Why it matters**: The paper's target audience includes practitioners deploying on real hardware. The 0.21 ms CPU time may not translate to FPGA/ASIC implementations. The 82K parameters may be too large for some edge devices.
**Suggestion**: Add a brief discussion of hardware implementation considerations, or at minimum, note that the reported times are for Python/PyTorch and may differ on dedicated hardware.
**Severity**: Minor

### W2: No Discussion of Model Maintenance
**Problem**: The paper does not discuss:
- How often the model needs retraining
- Whether the model degrades gracefully as channel statistics drift
- How to detect when retraining is needed
- Online/fine-tuning strategies
**Why it matters**: Real wireless channels are non-stationary. A model trained on static channel statistics may degrade in time-varying environments. The paper's practical deployment framework would be strengthened by addressing model maintenance.
**Suggestion**: Add a brief discussion of model maintenance strategies and the paper's recommendations for handling non-stationary channels.
**Severity**: Minor

### W3: Comparison Only Against Classical Methods
**Problem**: The paper compares LISTA only against classical methods (OMP, LASSO, LMS, NLMS). Missing comparisons include:
- Other deep unfolding methods for channel estimation
- End-to-end learned channel estimators (e.g., DeepSAGE, MMNet)
- Hybrid model-based/data-driven methods
**Why it matters**: Practitioners need to know how LISTA compares against the state-of-the-art, not just classical baselines. If a simple CNN outperforms LISTA, the paper's contribution is diminished.
**Suggestion**: Add at least one comparison with a modern learned method (e.g., a simple CNN or transformer-based estimator) to contextualize LISTA's performance.
**Severity**: Minor

### W4: Scalability Concerns Not Fully Addressed
**Problem**: The paper reports training divergence at N=256 (3/5 seeds) but does not:
- Investigate the cause of divergence
- Propose mitigation strategies (e.g., gradient normalization, learning rate scheduling)
- Test whether the divergence is fixable with architectural changes
**Why it matters**: N=256 is a realistic channel length for 5G NR. If LISTA cannot handle N=256, its practical applicability is limited to shorter channels.
**Suggestion**: Investigate the cause of divergence at N=256 and propose at least one mitigation strategy. If the divergence is fundamental, state this clearly.
**Severity**: Minor

---

## Detailed Comments

### Practical Impact
- The 33× speedup over OMP is significant and well-quantified.
- The 82K parameter count is modest but may be large for some edge devices.
- The cross-distribution generalization eliminates the need for channel-specific training data.

### Broader Implications
- The finding that Gaussian training generalizes to ITU channels has implications beyond LISTA: it suggests that generic training data may be sufficient for other learned channel estimators.
- The ablation finding (threshold is most important) suggests that simpler architectures (e.g., learned thresholding without the W matrix) may be viable.
- The SNR saturation behavior suggests fundamental limitations of the deep unfolding paradigm for high-SNR applications.

### Missing Perspectives
- **Hardware designers**: Would benefit from FPGA/ASIC implementation considerations.
- **System integrators**: Would benefit from model maintenance and retraining strategies.
- **Standards bodies**: Would benefit from comparison with 3GPP-standardized methods.

---

## Questions for Authors

1. **Hardware implementation**: Have you considered FPGA/ASIC implementation? What would the latency be?
2. **Model maintenance**: How often would the model need retraining in a real deployment? Can the model be fine-tuned online?
3. **N=256 divergence**: What causes the training divergence at N=256? Is it fixable?

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 60 | Adequate | Cross-distribution finding is interesting |
| Methodological Rigor (25%) | 66 | Adequate | Good experiments |
| Evidence Sufficiency (25%) | 68 | Adequate | Missing comparisons with modern learned methods |
| Argument Coherence (15%) | 72 | Strong | Clear narrative |
| Writing Quality (15%) | 76 | Strong | Well-written |
| Significance & Impact | 68 | Adequate | Practical speed advantage; limited by saturation |
| **Weighted Average** | **67.4** | **Minor Revision** | |
