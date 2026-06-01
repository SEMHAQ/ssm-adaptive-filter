# SSM-Adaptive-Filter

Sparse channel estimation using deep-unfolded LISTA (Learned ISTA) and adaptive filtering baselines.

Target journal: **Digital Signal Processing** (Elsevier).

## Project Structure

```text
code/
├── models/
│   └── ssm_af.py          # LISTA, OMP, LASSO, LMS, NLMS implementations
├── data/
│   └── generate.py         # Synthetic sparse channel data generation
├── run_experiments.py       # Original experiments (SNR, sparsity, channel length, convergence)
├── run_revision_experiments.py  # Revision experiments (ablation, generalization, runtime, ITU)
├── train.py                 # Training script for SSM-AF model
├── train_sparse.py          # Sparse channel training
├── eval.py                  # Evaluation utilities
└── generate_paper_figures.py  # Figure generation for paper
```

## Quick Start

```bash
pip install -r requirements.txt
```

## Running Experiments

### Original experiments (Tables 1-4 in paper)

```bash
cd code
python run_experiments.py --experiment all --device cuda --num_test 100
```

Individual experiments:

```bash
python run_experiments.py --experiment snr          # NMSE vs SNR
python run_experiments.py --experiment sparsity     # NMSE vs Sparsity
python run_experiments.py --experiment channellen   # NMSE vs Channel Length
python run_experiments.py --experiment convergence  # NMSE vs Layers
```

### Revision experiments (ablation, generalization, runtime, ITU)

```bash
cd code
python run_revision_experiments.py --experiment all --seeds 5 --device cuda
```

Individual revision experiments:

```bash
python run_revision_experiments.py --experiment ablation       # Ablation study
python run_revision_experiments.py --experiment gen_sparsity   # Sparsity mismatch
python run_revision_experiments.py --experiment gen_snr        # SNR mismatch
python run_revision_experiments.py --experiment runtime        # Inference time
python run_revision_experiments.py --experiment itu            # ITU channel models
python run_revision_experiments.py --experiment depth          # Depth sweep (Table 4)
python run_revision_experiments.py --experiment channellen     # Channel length sweep (Table 3)
python run_revision_experiments.py --experiment generalization # All generalization
```

Output is saved to `code/results/revision/` (JSON + PDF).

## Methods

| Method | Type | Sparsity-aware | Requires training |
| --- | --- | :-: | :-: |
| LMS | Adaptive filter | No | No |
| NLMS | Adaptive filter | No | No |
| OMP | Greedy CS | Yes | No |
| LASSO | Convex relaxation | Yes | No |
| LISTA | Deep unfolding | Yes | Yes |
