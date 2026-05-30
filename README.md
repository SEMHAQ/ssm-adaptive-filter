# SSM-AdaptiveFilter

Adaptive Filtering Meets Deep Learning: A Lightweight State Space Model Approach for Signal Enhancement

**Target Journal:** Digital Signal Processing (Elsevier)

## Overview

This repository contains the implementation of SSM-AF, a novel adaptive filtering framework that integrates State Space Models (SSMs) with traditional adaptive filtering theory for signal enhancement tasks.

## Project Structure

```
ssm-adaptive-filter/
├── main.tex                # Paper LaTeX source
├── references.bib          # Bibliography
├── figures/                # Paper figures
├── code/                   # Experiment code
│   ├── models/             # Model implementations
│   ├── data/               # Data generation/loading
│   └── utils/              # Utility functions
├── els-cas-templates/      # Elsevier CAS LaTeX template
└── README.md
```

## Tasks

- Echo Cancellation
- Channel Equalization
- Noise Reduction

## Baselines

| Method | Type |
|--------|------|
| LMS / NLMS | Classical Adaptive |
| RLS | Classical Adaptive |
| Kalman Filter | Optimal Estimation |
| DeepFilterNet | Deep Learning SOTA |

## Requirements

- Python 3.9+
- PyTorch 2.0+
- NumPy
- SciPy
- Matplotlib
- pesq, pystoi (for audio evaluation)

## Usage

```bash
# Train SSM-AF model
python code/train.py --task echo_cancellation

# Evaluate
python code/eval.py --task echo_cancellation --checkpoint checkpoints/best.pt
```

## License

For academic research use only.
