# SSM-Adaptive-Filter Project

Deep-unfolded LISTA (Learned ISTA) for sparse channel estimation.
Target journal: **Digital Signal Processing** (Elsevier).
Author: Huanjie Yu, Hunan University of Technology and Business.

## Project Layout

```
code/
├── models/ssm_af.py          # LISTA, OMP, LASSO, LMS, NLMS implementations
├── data/generate.py           # Synthetic sparse channel data generation
├── run_experiments.py         # Original experiments (Tables 1-4)
├── run_revision_experiments.py # Revision experiments (ablation, generalization, runtime, ITU)
├── train_sparse.py            # LISTA training script
├── train.py                   # General training (echo cancellation, etc.)
└── eval.py                    # Evaluation utilities
paper/
├── main.tex                   # LaTeX paper
├── main.abs                   # Abstract
├── references.bib             # Bibliography
└── cas-sc-template.tex        # Elsevier CAS template
```

## Key Parameters
- Channel length N=64, sparsity K=5, pilot M=128, LISTA layers L=8
- Metrics: NMSE (dB) = 10*log10(||h_est - h_true||^2 / ||h_true||^2)
- Baselines: LMS, NLMS (grid-searched step sizes), OMP (oracle K), LASSO (grid-searched λ)

## Running Experiments
```bash
cd code
python run_experiments.py --experiment all --device cuda --num_test 100      # Original
python run_revision_experiments.py --experiment all --seeds 5 --device cuda  # Revision
```

## Installed Skills (in .claude/skills/)

### academic-research/ (4 skills)
- `academic-paper-reviewer/SKILL.md` — 5-reviewer paper simulation
- `academic-paper/SKILL.md` — 12-agent paper writing pipeline
- `academic-pipeline/SKILL.md` — Full research-to-publication pipeline
- `deep-research/SKILL.md` — 13-agent deep research

### nature-skills/ (10 skills)
- `nature-writing/SKILL.md` — Nature-style manuscript writing
- `nature-polishing/SKILL.md` — Academic English polishing
- `nature-reviewer/SKILL.md` — Nature-style reviewer simulation
- `nature-response/SKILL.md` — Reviewer response letters
- `nature-citation/SKILL.md` — CNS citation management
- `nature-figure/SKILL.md` — Publication-grade figures (Python/R)
- `nature-reader/SKILL.md` — CN-EN side-by-side paper reading
- `nature-paper2ppt/SKILL.md` — Paper to PPT
- `nature-data/SKILL.md` — Data availability statements
- `nature-academic-search/SKILL.md` — Multi-source literature search

### andrej-karpathy-skills/
- `skills/andrej-karpathy-skill/SKILL.md` — Karpathy coding guidelines

## How to Use Skills
Read the relevant SKILL.md file from `.claude/skills/` before starting a task.
For example, to review the paper: read `.claude/skills/academic-research/academic-paper-reviewer/SKILL.md`.
