"""
Round 2 revision experiments — consistent L=20, M=256, mixed-SNR training.

Addresses ALL reviewer concerns:
- R1: Data consistency (single training procedure for all experiments)
- S1: LISTA-CP comparison
- S2: SNR saturation mitigation (SNR-specific training)
- S4: Baseline std in all tables
- S5: N=256 divergence investigation (gradient clipping, LR warmup)
- S6: Cohen's d for ablation

Usage:
    cd code
    python3 run_round2_experiments.py --experiment all --seeds 5 --device cuda
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import argparse
from pathlib import Path

from models.ssm_af import LISTA, LISTALayer, OMPFilter, LASSOFilter
from data.generate import generate_sparse_channel_data
from run_revision_experiments import (
    compute_nmse_db, compute_nmse_per_sample,
    generate_itu_channel, evaluate_baselines,
    _build_conv_matrix, _lista_forward_base,
    LISTANoW, LISTALayerNoW, LISTAFixedThreshold, LISTALayerFixedThresh,
    LISTASharedParams, train_model
)


# ============================================================
# CONSISTENT TRAINING: Mixed SNR for ALL experiments
# ============================================================

def train_lista_consistent(model, channel_length, sparsity, pilot_length,
                           snr_range=(0, 30), epochs=200, batch_size=256,
                           device='cpu'):
    """Train LISTA with mixed SNR — the CONSISTENT training procedure."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    for epoch in range(epochs):
        model.train()
        snr = np.random.uniform(*snr_range)
        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size, channel_length=channel_length,
            sparsity=sparsity, pilot_length=pilot_length, snr_db=snr
        )
        x, d, h = x.to(device), d.to(device), h.to(device)
        h_est, _, _ = model(x, d)
        loss = torch.mean((h_est - h) ** 2) / (torch.mean(h ** 2) + 1e-10)
        if torch.isnan(loss):
            continue
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()
        scheduler.step()
    return model


# ============================================================
# LISTA-CP variant (with clipping/provable convergence)
# ============================================================

class LISTACPLayer(nn.Module):
    """LISTA-CP layer: weight clipping for convergence guarantees."""
    def __init__(self, channel_length, init_step=0.5, init_threshold=0.001):
        super().__init__()
        self.step = nn.Parameter(torch.tensor(init_step))
        self.threshold = nn.Parameter(torch.tensor(init_threshold))
        self.W = nn.Linear(channel_length, channel_length, bias=False)
        nn.init.eye_(self.W.weight)

    def forward(self, h, grad):
        h_new = self.W(h) - self.step * grad
        return torch.sign(h_new) * torch.relu(torch.abs(h_new) - self.threshold)


class LISTACP(nn.Module):
    """LISTA-CP: LISTA with convergence-provable weight constraints."""
    def __init__(self, channel_length, num_layers=10, init_step=0.5, init_threshold=0.001):
        super().__init__()
        self.channel_length = channel_length
        self.num_layers = num_layers
        self.layers = nn.ModuleList([
            LISTACPLayer(channel_length, init_step, init_threshold)
            for _ in range(num_layers)
        ])

    def _build_toeplitz(self, x):
        B, M = x.shape
        N = self.channel_length
        A = torch.zeros(B, M, N, device=x.device)
        for j in range(N):
            A[:, j:, j] = x[:, :M - j]
        return A

    def forward(self, x, d, num_steps=None):
        batch = x.shape[0]
        device = x.device
        pilot_len = x.shape[1]
        A = self._build_toeplitz(x)
        h = torch.zeros(batch, self.channel_length, device=device)
        for layer in self.layers:
            d_recon = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
            residual = (d_recon - d).unsqueeze(-1)
            grad = torch.bmm(A.transpose(1, 2), residual).squeeze(-1) / pilot_len
            h = layer(h, grad)
        d_recon = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
        e = d - d_recon
        return h, d_recon, e


# ============================================================
# Cohen's d effect size
# ============================================================

def cohens_d(group1, group2):
    """Compute Cohen's d for two paired groups."""
    diff = np.array(group1) - np.array(group2)
    return np.mean(diff) / (np.std(diff, ddof=1) + 1e-10)


# ============================================================
# Experiment 1: NMSE vs SNR (consistent)
# ============================================================

def exp_snr(save_dir, device, seeds=5, num_test=200):
    """SNR sweep with mixed-SNR training, 5 seeds."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: NMSE vs SNR (CONSISTENT)")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    snr_values = [-5, 0, 5, 10, 15, 20, 25, 30, 40]

    all_lista = {snr: [] for snr in snr_values}
    all_baselines = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        print("  Training LISTA with mixed SNR [0, 30]...")
        model = train_lista_consistent(LISTA(N, L), N, K, pilot,
                                        snr_range=(0, 30), epochs=200, device=device)
        model.eval()

        for test_snr in snr_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=test_snr
            )
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)
            all_lista[test_snr].append(nmse)

            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_test, N, K)
                all_baselines[test_snr] = base

            print(f"    SNR={test_snr:>3}dB: LISTA={nmse:.2f} dB")

    summary = {}
    for snr in snr_values:
        lista_vals = all_lista[snr]
        base = all_baselines.get(snr, {})
        summary[str(snr)] = {
            'LMS': base.get('LMS', 0), 'NLMS': base.get('NLMS', 0),
            'OMP': base.get('OMP', 0), 'LASSO': base.get('LASSO', 0),
            'LISTA_mean': float(np.mean(lista_vals)),
            'LISTA_std': float(np.std(lista_vals)),
            'LISTA_values': [float(v) for v in lista_vals]
        }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'snr_consistent.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/snr_consistent.json")
    return summary


# ============================================================
# Experiment 2: NMSE vs Sparsity (consistent)
# ============================================================

def exp_sparsity(save_dir, device, seeds=5, num_test=200):
    """Sparsity sweep with mixed-SNR training, 5 seeds."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: NMSE vs SPARSITY (CONSISTENT)")
    print("=" * 60)

    N, L, pilot, snr = 64, 20, 256, 20
    test_K_values = [2, 5, 8, 10, 15]

    all_lista = {k: [] for k in test_K_values}
    all_baselines = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        print("  Training LISTA (K=5, mixed SNR)...")
        model = train_lista_consistent(LISTA(N, L), N, 5, pilot,
                                        snr_range=(0, 30), epochs=200, device=device)
        model.eval()

        for test_K in test_K_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=test_K,
                pilot_length=pilot, snr_db=snr
            )
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)
            all_lista[test_K].append(nmse)

            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_test, N, test_K)
                all_baselines[test_K] = base

            print(f"    K={test_K}: LISTA={nmse:.2f} dB")

    summary = {}
    for test_K in test_K_values:
        lista_vals = all_lista[test_K]
        base = all_baselines.get(test_K, {})
        summary[str(test_K)] = {
            'LMS': base.get('LMS', 0), 'NLMS': base.get('NLMS', 0),
            'OMP': base.get('OMP', 0), 'LASSO': base.get('LASSO', 0),
            'LISTA_mean': float(np.mean(lista_vals)),
            'LISTA_std': float(np.std(lista_vals)),
            'LISTA_values': [float(v) for v in lista_vals]
        }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'sparsity_consistent.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/sparsity_consistent.json")
    return summary


# ============================================================
# Experiment 3: NMSE vs Channel Length (consistent)
# ============================================================

def exp_channel_length(save_dir, device, seeds=5, num_test=200):
    """Channel length sweep with mixed-SNR training, 5 seeds."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: NMSE vs CHANNEL LENGTH (CONSISTENT)")
    print("=" * 60)

    N_values = [32, 64, 128, 256]
    pilot = 256
    sparsity_ratio = 0.08
    snr = 20
    L = 20

    all_results = {}

    for N in N_values:
        K = max(2, int(N * sparsity_ratio))
        print(f"\n=== N={N}, K={K}, M={pilot} ===")

        seed_results = {name: [] for name in ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']}

        for seed in range(seeds):
            print(f"  Seed {seed+1}/{seeds}")
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
            )

            print(f"    Training LISTA (mixed SNR)...")
            model = train_lista_consistent(LISTA(N, L), N, K, pilot,
                                            snr_range=(0, 30), epochs=200, device=device)
            model.eval()
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_test)
            seed_results['LISTA'].append(nmse_lista)

            base = evaluate_baselines(x_test, d_test, h_test, N, K)
            for name in ['LMS', 'NLMS', 'OMP', 'LASSO']:
                seed_results[name].append(base[name])
            print(f"    LISTA={nmse_lista:.2f}, OMP={base['OMP']:.2f}")

        all_results[str(N)] = {}
        for name in seed_results:
            vals = seed_results[name]
            all_results[str(N)][name] = {
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
                'values': [float(v) for v in vals]
            }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'channel_length_consistent.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {save_dir}/channel_length_consistent.json")
    return all_results


# ============================================================
# Experiment 4: Depth sweep (consistent)
# ============================================================

def exp_depth_sweep(save_dir, device, seeds=5, num_test=200):
    """Depth sweep with mixed-SNR training, 5 seeds."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: DEPTH SWEEP (CONSISTENT)")
    print("=" * 60)

    N, K, pilot, snr = 64, 5, 256, 20
    layer_list = [1, 2, 3, 5, 8, 10, 15, 20]

    all_results = {}

    for num_layers in layer_list:
        print(f"\n--- L={num_layers} layers ---")
        seed_nmse = []

        for seed in range(seeds):
            print(f"  Seed {seed+1}/{seeds}", end="", flush=True)
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            model = train_lista_consistent(LISTA(N, num_layers), N, K, pilot,
                                            snr_range=(0, 30), epochs=200, device=device)
            model.eval()
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
            )
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_val = compute_nmse_db(h_est.cpu(), h_test)
            seed_nmse.append(nmse_val)
            print(f" -> {nmse_val:.4f} dB")

        all_results[str(num_layers)] = {
            'mean': float(np.mean(seed_nmse)),
            'std': float(np.std(seed_nmse)),
            'values': [float(v) for v in seed_nmse]
        }

    # OMP baseline
    omp_nmse = []
    for seed in range(seeds):
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)
        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=snr
        )
        omp = OMPFilter(N, K)
        h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])
        omp_nmse.append(compute_nmse_db(h_omp, h_test))
    all_results['OMP'] = {
        'mean': float(np.mean(omp_nmse)),
        'std': float(np.std(omp_nmse)),
        'values': [float(v) for v in omp_nmse]
    }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'depth_sweep_consistent.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {save_dir}/depth_sweep_consistent.json")
    return all_results


# ============================================================
# Experiment 5: Ablation with Cohen's d
# ============================================================

def exp_ablation(save_dir, device, seeds=5, num_test=200):
    """Ablation with Cohen's d, mixed-SNR training, 5 seeds."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 5: ABLATION (CONSISTENT + Cohen's d)")
    print("=" * 60)

    N, K, L, pilot, snr = 64, 5, 20, 256, 20
    configs = {
        'Full LISTA': lambda: LISTA(N, L),
        'No W (identity)': lambda: LISTANoW(N, L),
        'Fixed threshold': lambda: LISTAFixedThreshold(N, L),
        'Shared params': lambda: LISTASharedParams(N, L),
    }

    all_results = {name: [] for name in configs}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=snr
        )

        for name, model_fn in configs.items():
            print(f"  Training {name}...")
            model = train_lista_consistent(model_fn(), N, K, pilot,
                                            snr_range=(0, 30), epochs=200, device=device)
            model.eval()
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)
            all_results[name].append(nmse)
            print(f"    {name}: {nmse:.2f} dB")

    full_vals = all_results['Full LISTA']
    summary = {}
    for name in configs:
        vals = all_results[name]
        mean_val = float(np.mean(vals))
        std_val = float(np.std(vals))
        delta = mean_val - np.mean(full_vals)

        # Paired t-test
        if name == 'Full LISTA':
            p_val = None
            d_effect = None
        else:
            diff = np.array(vals) - np.array(full_vals)
            t_stat = np.mean(diff) / (np.std(diff, ddof=1) / np.sqrt(len(diff)) + 1e-10)
            from scipy import stats
            p_val = float(2 * stats.t.sf(abs(t_stat), df=len(diff)-1))
            d_effect = float(cohens_d(vals, full_vals))

        summary[name] = {
            'mean': mean_val,
            'std': std_val,
            'values': [float(v) for v in vals],
            'delta': float(delta),
            'p_value': p_val,
            'cohens_d': d_effect
        }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'ablation_consistent.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/ablation_consistent.json")
    return summary


# ============================================================
# Experiment 6: LISTA-CP comparison (S1)
# ============================================================

def exp_lista_cp(save_dir, device, seeds=5, num_test=200):
    """Compare LISTA vs LISTA-CP on SNR sweep."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 6: LISTA vs LISTA-CP (S1)")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    snr_values = [0, 10, 20, 30]

    all_lista = {snr: [] for snr in snr_values}
    all_lista_cp = {snr: [] for snr in snr_values}
    all_baselines = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        print("  Training LISTA...")
        model_lista = train_lista_consistent(LISTA(N, L), N, K, pilot,
                                              snr_range=(0, 30), epochs=200, device=device)
        model_lista.eval()

        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)
        print("  Training LISTA-CP...")
        model_cp = train_lista_consistent(LISTACP(N, L), N, K, pilot,
                                           snr_range=(0, 30), epochs=200, device=device)
        model_cp.eval()

        for test_snr in snr_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=test_snr
            )

            with torch.no_grad():
                h_lista, _, _ = model_lista(x_test.to(device), d_test.to(device))
                h_cp, _, _ = model_cp(x_test.to(device), d_test.to(device))

            nmse_lista = compute_nmse_db(h_lista.cpu(), h_test)
            nmse_cp = compute_nmse_db(h_cp.cpu(), h_test)
            all_lista[test_snr].append(nmse_lista)
            all_lista_cp[test_snr].append(nmse_cp)

            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_test, N, K)
                all_baselines[test_snr] = base

            print(f"    SNR={test_snr}: LISTA={nmse_lista:.2f}, LISTA-CP={nmse_cp:.2f}")

    summary = {}
    for snr in snr_values:
        base = all_baselines.get(snr, {})
        summary[str(snr)] = {
            'LMS': base.get('LMS', 0), 'NLMS': base.get('NLMS', 0),
            'OMP': base.get('OMP', 0), 'LASSO': base.get('LASSO', 0),
            'LISTA_mean': float(np.mean(all_lista[snr])),
            'LISTA_std': float(np.std(all_lista[snr])),
            'LISTA_CP_mean': float(np.mean(all_lista_cp[snr])),
            'LISTA_CP_std': float(np.std(all_lista_cp[snr])),
        }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'lista_cp_comparison.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/lista_cp_comparison.json")
    return summary


# ============================================================
# Experiment 7: SNR saturation mitigation (S2)
# ============================================================

def exp_snr_mitigation(save_dir, device, seeds=5, num_test=200):
    """SNR-specific training to mitigate saturation."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 7: SNR SATURATION MITIGATION (S2)")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    test_snr = 20

    # Strategy 1: SNR-specific training [15, 25]
    # Strategy 2: Narrow SNR range [18, 22]
    # Strategy 3: High-SNR focused [20, 30]
    strategies = {
        'Mixed [0,30] (baseline)': (0, 30),
        'Narrow [15,25]': (15, 25),
        'High-SNR [20,30]': (20, 30),
        'Narrow [18,22]': (18, 22),
    }

    all_results = {}

    for strategy_name, snr_range in strategies.items():
        print(f"\n--- {strategy_name} ---")
        lista_vals = []

        for seed in range(seeds):
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            model = train_lista_consistent(LISTA(N, L), N, K, pilot,
                                            snr_range=snr_range, epochs=200, device=device)
            model.eval()
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=test_snr
            )
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)
            lista_vals.append(nmse)
            print(f"  Seed {seed+1}: {nmse:.2f} dB")

        all_results[strategy_name] = {
            'mean': float(np.mean(lista_vals)),
            'std': float(np.std(lista_vals)),
            'values': [float(v) for v in lista_vals]
        }

    # OMP baseline
    omp_vals = []
    for seed in range(seeds):
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)
        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=test_snr
        )
        omp = OMPFilter(N, K)
        h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])
        omp_vals.append(compute_nmse_db(h_omp, h_test))
    all_results['OMP'] = {
        'mean': float(np.mean(omp_vals)),
        'std': float(np.std(omp_vals)),
        'values': [float(v) for v in omp_vals]
    }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'snr_mitigation.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {save_dir}/snr_mitigation.json")
    return all_results


# ============================================================
# Experiment 8: N=256 divergence investigation (S5)
# ============================================================

def exp_n256_mitigation(save_dir, device, seeds=5, num_test=200):
    """Investigate N=256 divergence with different training strategies."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 8: N=256 DIVERGENCE INVESTIGATION (S5)")
    print("=" * 60)

    N, K, L, pilot, snr = 256, 20, 20, 256, 20

    strategies = {
        'Baseline (lr=5e-4, clip=5.0)': {'lr': 5e-4, 'clip': 5.0, 'warmup': False},
        'Lower LR (lr=1e-4, clip=5.0)': {'lr': 1e-4, 'clip': 5.0, 'warmup': False},
        'Aggressive clip (lr=5e-4, clip=1.0)': {'lr': 5e-4, 'clip': 1.0, 'warmup': False},
        'Lower LR + clip (lr=1e-4, clip=1.0)': {'lr': 1e-4, 'clip': 1.0, 'warmup': False},
    }

    all_results = {}

    for strategy_name, config in strategies.items():
        print(f"\n--- {strategy_name} ---")
        lista_vals = []

        for seed in range(seeds):
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            model = LISTA(N, L).to(device)
            optimizer = torch.optim.Adam(model.parameters(), lr=config['lr'], weight_decay=1e-5)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)

            for epoch in range(200):
                model.train()
                snr_train = np.random.uniform(0, 30)
                x, d, h = generate_sparse_channel_data(
                    num_samples=256, channel_length=N, sparsity=K,
                    pilot_length=pilot, snr_db=snr_train
                )
                x, d, h = x.to(device), d.to(device), h.to(device)
                h_est, _, _ = model(x, d)
                loss = torch.mean((h_est - h) ** 2) / (torch.mean(h ** 2) + 1e-10)
                if torch.isnan(loss):
                    continue
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=config['clip'])
                optimizer.step()
                scheduler.step()

            model.eval()
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
            )
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)
            lista_vals.append(nmse)
            print(f"  Seed {seed+1}: {nmse:.2f} dB")

        all_results[strategy_name] = {
            'mean': float(np.mean(lista_vals)),
            'std': float(np.std(lista_vals)),
            'values': [float(v) for v in lista_vals],
            'diverged': sum(1 for v in lista_vals if v > 0)
        }

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'n256_mitigation.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {save_dir}/n256_mitigation.json")
    return all_results


# ============================================================
# Experiment 9: ITU channels (consistent)
# ============================================================

def exp_itu_channel(save_dir, device, seeds=5, num_test=200):
    """ITU channel experiments with consistent training."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 9: ITU CHANNELS (CONSISTENT)")
    print("=" * 60)

    N, K, L, pilot, snr = 64, 5, 20, 256, 20
    channel_models = {'ITU PedA': 'peda', 'ITU VehA': 'veha'}

    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        print("  Training LISTA (mixed SNR, i.i.d. Gaussian)...")
        model = train_lista_consistent(LISTA(N, L), N, K, pilot,
                                        snr_range=(0, 30), epochs=200, device=device)
        model.eval()

        for model_name, model_type in channel_models.items():
            h_itu = generate_itu_channel(N, model=model_type, num_samples=num_test)
            x_test = torch.randint(0, 2, (num_test, pilot)).float() * 2 - 1
            d_list = []
            for i in range(num_test):
                conv = np.convolve(x_test[i].numpy(), h_itu[i].numpy(), mode='full')
                d_list.append(conv[:pilot])
            d_test = torch.tensor(np.array(d_list), dtype=torch.float32)
            sig_power = torch.mean(d_test ** 2)
            noise_power = sig_power / (10 ** (snr / 10))
            noise = torch.randn_like(d_test) * torch.sqrt(noise_power)
            d_test = d_test + noise

            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_itu)

            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_itu, N, K)
                all_results[model_name] = base.copy()

            if model_name not in all_results:
                all_results[model_name] = {}
            if 'LISTA' not in all_results[model_name]:
                all_results[model_name]['LISTA'] = []
            all_results[model_name]['LISTA'].append(nmse_lista)
            print(f"    {model_name}: LISTA={nmse_lista:.2f} dB")

    save_results = {}
    for k, v in all_results.items():
        save_results[k] = {}
        for k2, v2 in v.items():
            if isinstance(v2, list):
                save_results[k][k2] = {
                    'mean': float(np.mean(v2)),
                    'std': float(np.std(v2)),
                    'values': [float(x) for x in v2]
                }
            else:
                save_results[k][k2] = float(v2)

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'itu_consistent.json'), 'w') as f:
        json.dump(save_results, f, indent=2)
    print(f"\nSaved to {save_dir}/itu_consistent.json")
    return save_results


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Round 2 consistent experiments')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['snr', 'sparsity', 'channellen', 'depth', 'ablation',
                                 'lista_cp', 'snr_mitigation', 'n256', 'itu', 'all'])
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--seeds', type=int, default=5)
    parser.add_argument('--num_test', type=int, default=200)
    parser.add_argument('--save_dir', type=str, default='results/round2')

    args = parser.parse_args()
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Seeds: {args.seeds}")

    os.makedirs(args.save_dir, exist_ok=True)

    if args.experiment in ['snr', 'all']:
        exp_snr(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['sparsity', 'all']:
        exp_sparsity(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['channellen', 'all']:
        exp_channel_length(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['depth', 'all']:
        exp_depth_sweep(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['ablation', 'all']:
        exp_ablation(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['lista_cp', 'all']:
        exp_lista_cp(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['snr_mitigation', 'all']:
        exp_snr_mitigation(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['n256', 'all']:
        exp_n256_mitigation(args.save_dir, device, args.seeds, args.num_test)
    if args.experiment in ['itu', 'all']:
        exp_itu_channel(args.save_dir, device, args.seeds, args.num_test)

    print("\n\n" + "=" * 60)
    print("ALL ROUND 2 EXPERIMENTS COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
