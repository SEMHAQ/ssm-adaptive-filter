"""
Revision experiments for LISTA sparse channel estimation paper.

Implements all experiments required by reviewers:
1. Ablation study (no W, fixed threshold, shared params)
2. Generalization (sparsity mismatch, SNR mismatch)
3. Runtime comparison (CPU/GPU)
4. ITU channel model experiments
5. Multiple seeds for all experiments

Usage:
    cd code
    python run_revision_experiments.py --experiment all --seeds 5 --device cuda
    python run_revision_experiments.py --experiment ablation --seeds 5
    python run_revision_experiments.py --experiment generalization --seeds 5
    python run_revision_experiments.py --experiment runtime --seeds 3
    python run_revision_experiments.py --experiment itu --seeds 5
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import time
import argparse
from pathlib import Path

from models.ssm_af import LISTA, LISTALayer, OMPFilter, LASSOFilter, LMSFilter, NLMSFilter
from data.generate import generate_sparse_channel_data


# ============================================================
# Helper functions
# ============================================================

def compute_nmse_db(h_est, h_true):
    """NMSE in dB."""
    err = ((h_est - h_true) ** 2).sum(dim=-1)
    power = (h_true ** 2).sum(dim=-1) + 1e-10
    return 10 * np.log10((err / power).mean().item() + 1e-10)


def compute_nmse_per_sample(h_est, h_true):
    """NMSE per sample, returns array."""
    err = ((h_est - h_true) ** 2).sum(dim=-1)
    power = (h_true ** 2).sum(dim=-1) + 1e-10
    return 10 * np.log10(err / power + 1e-10).numpy()


def generate_itu_channel(channel_length, model='peda', num_samples=1000,
                         randomize_positions=False, normalize=True):
    """
    Generate ITU channel models with exponentially decaying power delay profile.

    Args:
        channel_length: Number of taps
        model: 'peda' (Pedestrian A) or 'veha' (Vehicular A)
        num_samples: Number of channel realizations
        randomize_positions: If True, randomize tap positions (realistic sparse
            channel); if False, use fixed ITU positions (original behavior)
        normalize: If True, normalize each channel to unit L2 norm
    Returns:
        h: (num_samples, channel_length) channel impulse responses
    """
    if model == 'peda':
        delays_ns = [0, 50, 110, 170, 240, 310]  # ns
        powers_db = [0, -9.7, -19.2, -22.8, -25.1, -27.0]  # dB
    elif model == 'veha':
        delays_ns = [0, 310, 710, 1090, 1730, 2510]  # ns
        powers_db = [0, -1.0, -9.0, -10.0, -15.0, -20.0]  # dB
    else:
        raise ValueError(f"Unknown model: {model}")

    num_taps = len(delays_ns)

    # Convert to linear power
    powers_linear = 10 ** (np.array(powers_db) / 10)
    powers_linear = powers_linear / powers_linear.sum()  # normalize

    h = np.zeros((num_samples, channel_length))

    if randomize_positions:
        # Random tap positions (like i.i.d. Gaussian sparse channels)
        for s in range(num_samples):
            tap_positions = np.random.choice(channel_length, num_taps, replace=False)
            tap_positions.sort()
            for j, (pos, power) in enumerate(zip(tap_positions, powers_linear)):
                # Rayleigh fading with specified power
                h[s, pos] = np.sqrt(power / 2) * (
                    np.random.randn() + 1j * np.random.randn()
                ).real
    else:
        # Fixed ITU positions (original behavior)
        for i, (delay_ns, power) in enumerate(zip(delays_ns, powers_linear)):
            tap_idx = int(delay_ns * 1e-9 * 1e6 * channel_length)
            if tap_idx < channel_length:
                h[:, tap_idx] = np.sqrt(power / 2) * (
                    np.random.randn(num_samples) + 1j * np.random.randn(num_samples)
                ).real

    # Normalize to unit L2 norm (optional)
    if normalize:
        h = h / (np.linalg.norm(h, axis=1, keepdims=True) + 1e-10)
    return torch.tensor(h, dtype=torch.float32)


# ============================================================
# Ablation LISTA variants
# ============================================================

def _build_conv_matrix(x, channel_length):
    """Build batched Toeplitz convolution matrix A: A[i,j] = x[i-j]."""
    B, M = x.shape
    N = channel_length
    A = torch.zeros(B, M, N, device=x.device)
    for j in range(N):
        A[:, j:, j] = x[:, :M - j]
    return A


def _lista_forward_base(x, d, channel_length, layers):
    """Shared forward pass for all LISTA variants using Toeplitz matrix."""
    batch = x.shape[0]
    device = x.device
    pilot_len = x.shape[1]
    A = _build_conv_matrix(x, channel_length)
    h = torch.zeros(batch, channel_length, device=device)
    for layer in layers:
        d_recon = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
        residual = (d_recon - d).unsqueeze(-1)
        grad = torch.bmm(A.transpose(1, 2), residual).squeeze(-1) / pilot_len
        h = layer(h, grad)
    d_recon_final = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
    e = d - d_recon_final
    return h, d_recon_final, e


class LISTANoW(nn.Module):
    """LISTA without learnable W (identity mapping)."""
    def __init__(self, channel_length, num_layers=8):
        super().__init__()
        self.channel_length = channel_length
        self.num_layers = num_layers
        self.layers = nn.ModuleList([
            LISTALayerNoW(channel_length) for _ in range(num_layers)
        ])

    def forward(self, x, d):
        return _lista_forward_base(x, d, self.channel_length, self.layers)


class LISTALayerNoW(nn.Module):
    """LISTA layer without W (identity mapping)."""
    def __init__(self, channel_length, init_step=0.5, init_threshold=0.001):
        super().__init__()
        self.step = nn.Parameter(torch.tensor(init_step))
        self.threshold = nn.Parameter(torch.tensor(init_threshold))

    def forward(self, h, grad):
        h_new = h - self.step * grad
        return torch.sign(h_new) * torch.relu(torch.abs(h_new) - self.threshold)


class LISTAFixedThreshold(nn.Module):
    """LISTA with fixed threshold (not learnable)."""
    def __init__(self, channel_length, num_layers=8, fixed_threshold=0.001):
        super().__init__()
        self.channel_length = channel_length
        self.num_layers = num_layers
        self.fixed_threshold = fixed_threshold
        self.layers = nn.ModuleList([
            LISTALayerFixedThresh(channel_length, fixed_threshold) for _ in range(num_layers)
        ])

    def forward(self, x, d):
        return _lista_forward_base(x, d, self.channel_length, self.layers)


class LISTALayerFixedThresh(nn.Module):
    """LISTA layer with fixed threshold."""
    def __init__(self, channel_length, fixed_threshold=0.001, init_step=0.5):
        super().__init__()
        self.step = nn.Parameter(torch.tensor(init_step))
        self.fixed_threshold = fixed_threshold
        self.W = nn.Linear(channel_length, channel_length, bias=False)
        nn.init.eye_(self.W.weight)

    def forward(self, h, grad):
        h_new = self.W(h) - self.step * grad
        return torch.sign(h_new) * torch.relu(torch.abs(h_new) - self.fixed_threshold)


class LISTASharedParams(nn.Module):
    """LISTA with shared step/threshold across all layers."""
    def __init__(self, channel_length, num_layers=8):
        super().__init__()
        self.channel_length = channel_length
        self.num_layers = num_layers
        self.step = nn.Parameter(torch.tensor(0.5))
        self.threshold = nn.Parameter(torch.tensor(0.001))
        self.W_layers = nn.ModuleList([
            nn.Linear(channel_length, channel_length, bias=False) for _ in range(num_layers)
        ])
        for W in self.W_layers:
            nn.init.eye_(W.weight)

    def forward(self, x, d):
        batch = x.shape[0]
        device = x.device
        pilot_len = x.shape[1]
        A = _build_conv_matrix(x, self.channel_length)
        h = torch.zeros(batch, self.channel_length, device=device)
        for W in self.W_layers:
            d_recon = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
            residual = (d_recon - d).unsqueeze(-1)
            grad = torch.bmm(A.transpose(1, 2), residual).squeeze(-1) / pilot_len
            h_new = W(h) - self.step * grad
            h = torch.sign(h_new) * torch.relu(torch.abs(h_new) - self.threshold)
        d_recon_final = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
        e = d - d_recon_final
        return h, d_recon_final, e


# ============================================================
# Training helpers
# ============================================================

def train_model(model, channel_length, sparsity, pilot_length, snr_db,
                epochs=200, batch_size=64, device='cpu'):
    """Generic training loop for any LISTA variant."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    for epoch in range(epochs):
        model.train()
        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size, channel_length=channel_length,
            sparsity=sparsity, pilot_length=pilot_length, snr_db=snr_db
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


def evaluate_baselines(x_test, d_test, h_test, channel_length, sparsity, lams=None, mus_lms=None, mus_nlms=None):
    """Evaluate all baselines with grid search."""
    results = {}

    # OMP (oracle K)
    omp = OMPFilter(channel_length, sparsity)
    h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(x_test.shape[0])])
    results['OMP'] = compute_nmse_db(h_omp, h_test)

    # LASSO with grid search
    if lams is None:
        lams = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
    best_lasso = float('inf')
    for lam in lams:
        lasso = LASSOFilter(channel_length, lam)
        h_lasso = torch.stack([lasso.estimate(x_test[i], d_test[i]) for i in range(x_test.shape[0])])
        nmse = compute_nmse_db(h_lasso, h_test)
        if nmse < best_lasso:
            best_lasso = nmse
    results['LASSO'] = best_lasso

    # LMS with grid search
    if mus_lms is None:
        mus_lms = [0.001, 0.005, 0.01, 0.02, 0.05]
    best_lms = float('inf')
    for mu in mus_lms:
        h_lms_list = []
        for i in range(x_test.shape[0]):
            w = np.zeros(channel_length)
            x_buf = np.zeros(channel_length)
            x_np = x_test[i].numpy()
            d_np = d_test[i].numpy()
            for n in range(len(x_np)):
                x_buf = np.roll(x_buf, 1)
                x_buf[0] = x_np[n]
                y_n = np.dot(w, x_buf)
                e_n = d_np[n] - y_n
                w = w + mu * e_n * x_buf
            h_lms_list.append(torch.tensor(w))
        h_lms = torch.stack(h_lms_list)
        nmse = compute_nmse_db(h_lms, h_test)
        if nmse < best_lms:
            best_lms = nmse
    results['LMS'] = best_lms

    # NLMS with grid search
    if mus_nlms is None:
        mus_nlms = [0.1, 0.3, 0.5, 0.7, 1.0]
    best_nlms = float('inf')
    for mu in mus_nlms:
        h_nlms_list = []
        for i in range(x_test.shape[0]):
            w = np.zeros(channel_length)
            x_buf = np.zeros(channel_length)
            x_np = x_test[i].numpy()
            d_np = d_test[i].numpy()
            for n in range(len(x_np)):
                x_buf = np.roll(x_buf, 1)
                x_buf[0] = x_np[n]
                y_n = np.dot(w, x_buf)
                e_n = d_np[n] - y_n
                norm = np.dot(x_buf, x_buf) + 1e-8
                w = w + (mu / norm) * e_n * x_buf
            h_nlms_list.append(torch.tensor(w))
        h_nlms = torch.stack(h_nlms_list)
        nmse = compute_nmse_db(h_nlms, h_test)
        if nmse < best_nlms:
            best_nlms = nmse
    results['NLMS'] = best_nlms

    return results


# ============================================================
# Experiments
# ============================================================

def exp_ablation(save_dir, device, seeds=5, num_test=200):
    """Ablation study: compare LISTA variants."""
    print("\n" + "=" * 60)
    print("ABLATION STUDY")
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

        # Test data
        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=snr
        )

        for name, model_fn in configs.items():
            print(f"  Training {name}...")
            model = train_model(model_fn(), N, K, pilot, snr, epochs=200, device=device)
            model.eval()
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)
            all_results[name].append(nmse)
            print(f"    {name}: {nmse:.2f} dB")

    # Compute mean ± std
    print("\n\n=== ABLATION RESULTS ===")
    summary = {}
    for name in configs:
        vals = all_results[name]
        mean_val = np.mean(vals)
        std_val = np.std(vals)
        summary[name] = {'mean': mean_val, 'std': std_val, 'values': vals}
        print(f"  {name}: {mean_val:.2f} ± {std_val:.2f} dB")

    # Save
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'ablation.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    names = list(summary.keys())
    means = [summary[n]['mean'] for n in names]
    stds = [summary[n]['std'] for n in names]
    colors = ['#F44336', '#2196F3', '#4CAF50', '#FF9800']
    bars = ax.bar(names, means, yerr=stds, capsize=5, color=colors, alpha=0.8)
    ax.set_ylabel('NMSE (dB)', fontsize=12)
    ax.set_title('Ablation Study: LISTA Component Contribution', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'ablation.pdf'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nSaved to {save_dir}/ablation.pdf and ablation.json")


def exp_generalization_sparsity(save_dir, device, seeds=5, num_test=200):
    """Generalization: train on K=5, test on different K."""
    print("\n" + "=" * 60)
    print("GENERALIZATION: SPARSITY MISMATCH")
    print("=" * 60)

    N, train_K, L, pilot, snr = 64, 5, 8, 128, 20
    test_K_values = [2, 5, 8, 10, 15]

    all_lista = {k: [] for k in test_K_values}
    all_baselines = {k: {} for k in test_K_values}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA on K=5
        print(f"  Training LISTA (K={train_K})...")
        model = train_model(LISTA(N, L), N, train_K, pilot, snr, epochs=200, device=device)
        model.eval()

        for test_K in test_K_values:
            print(f"  Testing on K={test_K}...")
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=test_K,
                pilot_length=pilot, snr_db=snr
            )

            # LISTA
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_test)
            all_lista[test_K].append(nmse_lista)

            # Baselines (only first seed for baselines to save time)
            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_test, N, test_K)
                all_baselines[test_K] = base

            print(f"    K={test_K}: LISTA={nmse_lista:.2f} dB")

    # Summary
    print("\n\n=== SPARSITY GENERALIZATION RESULTS ===")
    print(f"{'Test K':<8} {'LMS':<10} {'NLMS':<10} {'OMP':<10} {'LASSO':<10} {'LISTA':<15}")
    summary = {}
    for test_K in test_K_values:
        lista_mean = np.mean(all_lista[test_K])
        lista_std = np.std(all_lista[test_K])
        base = all_baselines[test_K]
        summary[str(test_K)] = {
            'LMS': base.get('LMS', 0), 'NLMS': base.get('NLMS', 0),
            'OMP': base.get('OMP', 0), 'LASSO': base.get('LASSO', 0),
            'LISTA_mean': lista_mean, 'LISTA_std': lista_std,
            'LISTA_values': all_lista[test_K]
        }
        print(f"{test_K:<8} {base.get('LMS',0):<10.2f} {base.get('NLMS',0):<10.2f} "
              f"{base.get('OMP',0):<10.2f} {base.get('LASSO',0):<10.2f} "
              f"{lista_mean:<8.2f} ± {lista_std:.2f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'gen_sparsity.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    methods = ['LMS', 'NLMS', 'OMP', 'LASSO']
    markers = ['o', 's', '^', 'D']
    colors_m = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']
    for m, mk, c in zip(methods, markers, colors_m):
        y = [summary[str(k)][m] for k in test_K_values]
        ax.plot(test_K_values, y, marker=mk, color=c, label=m, linewidth=2, markersize=6)

    lista_means = [summary[str(k)]['LISTA_mean'] for k in test_K_values]
    lista_stds = [summary[str(k)]['LISTA_std'] for k in test_K_values]
    ax.errorbar(test_K_values, lista_means, yerr=lista_stds, marker='v', color='#F44336',
                label='LISTA (trained K=5)', linewidth=2, markersize=6, capsize=3)

    ax.set_xlabel('Test Sparsity K', fontsize=12)
    ax.set_ylabel('NMSE (dB)', fontsize=12)
    ax.set_title('Generalization: Sparsity Mismatch (train K=5)', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'gen_sparsity.pdf'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nSaved to {save_dir}/gen_sparsity.pdf and gen_sparsity.json")


def exp_generalization_snr(save_dir, device, seeds=5, num_test=200):
    """Generalization: test on SNR outside training range."""
    print("\n" + "=" * 60)
    print("GENERALIZATION: SNR MISMATCH")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    train_snr_range = (0, 30)
    test_snr_values = [-5, 0, 5, 10, 15, 20, 25, 30, 40]

    all_lista = {snr: [] for snr in test_snr_values}
    all_baselines = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train on mixed SNR
        print("  Training LISTA on mixed SNR [0, 30]...")
        model = LISTA(N, L).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)

        for epoch in range(200):
            model.train()
            # Random SNR in [0, 30]
            snr = np.random.uniform(0, 30)
            x, d, h = generate_sparse_channel_data(
                num_samples=64, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
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

        model.eval()
        for test_snr in test_snr_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=test_snr
            )
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)
            all_lista[test_snr].append(nmse)

            # Baselines (first seed only)
            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_test, N, K)
                all_baselines[test_snr] = base

            print(f"    SNR={test_snr:>3}dB: LISTA={nmse:.2f} dB")

    # Summary
    print("\n\n=== SNR GENERALIZATION RESULTS ===")
    print(f"{'SNR':<6} {'LMS':<10} {'NLMS':<10} {'OMP':<10} {'LASSO':<10} {'LISTA':<15}")
    summary = {}
    for snr in test_snr_values:
        lista_mean = np.mean(all_lista[snr])
        lista_std = np.std(all_lista[snr])
        base = all_baselines.get(snr, {})
        summary[str(snr)] = {
            'LMS': base.get('LMS', 0), 'NLMS': base.get('NLMS', 0),
            'OMP': base.get('OMP', 0), 'LASSO': base.get('LASSO', 0),
            'LISTA_mean': lista_mean, 'LISTA_std': lista_std,
            'LISTA_values': all_lista[snr]
        }
        print(f"{snr:<6} {base.get('LMS',0):<10.2f} {base.get('NLMS',0):<10.2f} "
              f"{base.get('OMP',0):<10.2f} {base.get('LASSO',0):<10.2f} "
              f"{lista_mean:<8.2f} ± {lista_std:.2f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'gen_snr.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    methods = ['LMS', 'NLMS', 'OMP', 'LASSO']
    markers = ['o', 's', '^', 'D']
    colors_m = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']
    for m, mk, c in zip(methods, markers, colors_m):
        y = [summary[str(s)][m] for s in test_snr_values]
        ax.plot(test_snr_values, y, marker=mk, color=c, label=m, linewidth=2, markersize=6)

    lista_means = [summary[str(s)]['LISTA_mean'] for s in test_snr_values]
    lista_stds = [summary[str(s)]['LISTA_std'] for s in test_snr_values]
    ax.errorbar(test_snr_values, lista_means, yerr=lista_stds, marker='v', color='#F44336',
                label='LISTA (trained SNR∈[0,30])', linewidth=2, markersize=6, capsize=3)

    # Mark training range
    ax.axvspan(0, 30, alpha=0.1, color='green', label='Training SNR range')

    ax.set_xlabel('SNR (dB)', fontsize=12)
    ax.set_ylabel('NMSE (dB)', fontsize=12)
    ax.set_title('Generalization: SNR Mismatch', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'gen_snr.pdf'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nSaved to {save_dir}/gen_snr.pdf and gen_snr.json")


def exp_runtime(save_dir, device, num_test=200):
    """Runtime comparison: inference time for each method."""
    print("\n" + "=" * 60)
    print("RUNTIME COMPARISON")
    print("=" * 60)

    N, K, L, pilot, snr = 64, 5, 20, 256, 20

    # Generate test data
    x_test, d_test, h_test = generate_sparse_channel_data(
        num_samples=num_test, channel_length=N, sparsity=K,
        pilot_length=pilot, snr_db=snr
    )

    results = {}

    # LMS
    start = time.perf_counter()
    for i in range(num_test):
        w = np.zeros(N)
        x_buf = np.zeros(N)
        x_np = x_test[i].numpy()
        d_np = d_test[i].numpy()
        for n in range(len(x_np)):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x_np[n]
            y_n = np.dot(w, x_buf)
            e_n = d_np[n] - y_n
            w = w + 0.01 * e_n * x_buf
    t_lms = (time.perf_counter() - start) / num_test * 1000
    results['LMS'] = {'time_ms': t_lms, 'params': 0}

    # NLMS
    start = time.perf_counter()
    for i in range(num_test):
        w = np.zeros(N)
        x_buf = np.zeros(N)
        x_np = x_test[i].numpy()
        d_np = d_test[i].numpy()
        for n in range(len(x_np)):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x_np[n]
            y_n = np.dot(w, x_buf)
            e_n = d_np[n] - y_n
            norm = np.dot(x_buf, x_buf) + 1e-8
            w = w + (0.5 / norm) * e_n * x_buf
    t_nlms = (time.perf_counter() - start) / num_test * 1000
    results['NLMS'] = {'time_ms': t_nlms, 'params': 0}

    # OMP
    omp = OMPFilter(N, K)
    start = time.perf_counter()
    for i in range(num_test):
        omp.estimate(x_test[i], d_test[i])
    t_omp = (time.perf_counter() - start) / num_test * 1000
    results['OMP'] = {'time_ms': t_omp, 'params': 0}

    # LASSO
    lasso = LASSOFilter(N, 0.01)
    start = time.perf_counter()
    for i in range(num_test):
        lasso.estimate(x_test[i], d_test[i])
    t_lasso = (time.perf_counter() - start) / num_test * 1000
    results['LASSO'] = {'time_ms': t_lasso, 'params': 0}

    # LISTA (different layer counts)
    for num_layers in [5, 8, 10]:
        model = LISTA(N, num_layers).to(device)
        model.eval()
        x_dev = x_test.to(device)
        d_dev = d_test.to(device)

        # Warmup
        with torch.no_grad():
            for _ in range(3):
                model(x_dev[:10], d_dev[:10])

        # CPU timing
        model_cpu = model.cpu()
        start = time.perf_counter()
        with torch.no_grad():
            for i in range(0, num_test, 10):
                model_cpu(x_test[i:i+10], d_test[i:i+10])
        t_cpu = (time.perf_counter() - start) / num_test * 1000

        # GPU timing (if available)
        t_gpu = None
        if device.type == 'cuda':
            model_gpu = model.to(device)
            torch.cuda.synchronize()
            start = time.perf_counter()
            with torch.no_grad():
                for i in range(0, num_test, 10):
                    model_gpu(x_dev[i:i+10], d_dev[i:i+10])
            torch.cuda.synchronize()
            t_gpu = (time.perf_counter() - start) / num_test * 1000

        n_params = sum(p.numel() for p in model.parameters())
        results[f'LISTA(L={num_layers})'] = {
            'time_cpu_ms': t_cpu,
            'time_gpu_ms': t_gpu,
            'params': n_params
        }

    # Print
    print(f"\n{'Method':<18} {'CPU (ms)':<12} {'GPU (ms)':<12} {'Params':<10}")
    print("-" * 52)
    for name, r in results.items():
        cpu_t = r.get('time_ms', r.get('time_cpu_ms', 0))
        gpu_t = r.get('time_gpu_ms', '-')
        params = r['params']
        gpu_str = f"{gpu_t:.3f}" if isinstance(gpu_t, float) else gpu_t
        print(f"{name:<18} {cpu_t:<12.3f} {gpu_str:<12} {params:<10}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'runtime.json'), 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to {save_dir}/runtime.json")


def exp_itu_channel(save_dir, device, seeds=5, num_test=200):
    """ITU channel model experiments."""
    print("\n" + "=" * 60)
    print("ITU CHANNEL MODEL EXPERIMENTS")
    print("=" * 60)

    N, K, L, pilot, snr = 64, 5, 20, 256, 20
    channel_models = {
        'ITU PedA': 'peda',
        'ITU VehA': 'veha',
    }

    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA on i.i.d. Gaussian channels
        print("  Training LISTA on i.i.d. Gaussian channels...")
        model = train_model(LISTA(N, L), N, K, pilot, snr, epochs=200, device=device)
        model.eval()
        model.eval()

        for model_name, model_type in channel_models.items():
            # Generate ITU channels
            h_itu = generate_itu_channel(N, model=model_type, num_samples=num_test)

            # Generate pilots and received signals
            x_test = torch.randint(0, 2, (num_test, pilot)).float() * 2 - 1
            # Convolution: d = x * h + noise
            d_list = []
            for i in range(num_test):
                conv = np.convolve(x_test[i].numpy(), h_itu[i].numpy(), mode='full')
                d_list.append(conv[:pilot])
            d_test = torch.tensor(np.array(d_list), dtype=torch.float32)

            # Add noise
            sig_power = torch.mean(d_test ** 2)
            noise_power = sig_power / (10 ** (snr / 10))
            noise = torch.randn_like(d_test) * torch.sqrt(noise_power)
            d_test = d_test + noise

            # LISTA
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_itu)

            # Baselines
            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_itu, N, K)
                all_results[model_name] = base.copy()

            if model_name not in all_results:
                all_results[model_name] = {}
            if 'LISTA' not in all_results[model_name]:
                all_results[model_name]['LISTA'] = []
            all_results[model_name]['LISTA'].append(nmse_lista)

            print(f"    {model_name}: LISTA={nmse_lista:.2f} dB")

    # Summary
    print("\n\n=== ITU CHANNEL RESULTS ===")
    for model_name in channel_models:
        r = all_results[model_name]
        lista_vals = r.get('LISTA', [0])
        lista_mean = np.mean(lista_vals)
        lista_std = np.std(lista_vals)
        print(f"\n{model_name}:")
        print(f"  LMS:   {r.get('LMS', 0):.2f} dB")
        print(f"  NLMS:  {r.get('NLMS', 0):.2f} dB")
        print(f"  OMP:   {r.get('OMP', 0):.2f} dB")
        print(f"  LASSO: {r.get('LASSO', 0):.2f} dB")
        print(f"  LISTA: {lista_mean:.2f} ± {lista_std:.2f} dB")

    os.makedirs(save_dir, exist_ok=True)
    # Convert lists to serializable format
    save_results = {}
    for k, v in all_results.items():
        save_results[k] = {}
        for k2, v2 in v.items():
            if isinstance(v2, list):
                save_results[k][k2] = {'mean': float(np.mean(v2)), 'std': float(np.std(v2)), 'values': v2}
            else:
                save_results[k][k2] = float(v2)
    with open(os.path.join(save_dir, 'itu_channel.json'), 'w') as f:
        json.dump(save_results, f, indent=2)

    print(f"\nSaved to {save_dir}/itu_channel.json")


def exp_channel_length(save_dir, device, seeds=5, num_test=200):
    """Channel length sweep: NMSE vs N with validation-optimized baselines and 5-seed statistics."""
    print("\n" + "=" * 60)
    print("CHANNEL LENGTH SWEEP EXPERIMENT")
    print("=" * 60)

    N_values = [32, 64, 128, 256]
    pilot = 256  # Fixed pilot length
    sparsity_ratio = 0.08  # K/N ≈ 8%
    snr = 20
    L = 20

    all_results = {}

    for N in N_values:
        K = max(2, int(N * sparsity_ratio))
        print(f"\n=== N={N}, K={K}, M={pilot} ===")

        seed_results = {name: [] for name in ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']}

        for seed in range(seeds):
            print(f"\n--- Seed {seed+1}/{seeds} ---")
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            # Test data
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
            )

            # LISTA
            print(f"  Training LISTA (L={L})...")
            model = train_model(LISTA(N, L), N, K, pilot, snr, epochs=200, device=device)
            model.eval()
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_test)
            seed_results['LISTA'].append(nmse_lista)
            print(f"    LISTA: {nmse_lista:.2f} dB")

            # Baselines (validation-optimized, same as evaluate_baselines)
            base = evaluate_baselines(x_test, d_test, h_test, N, K)
            for name in ['LMS', 'NLMS', 'OMP', 'LASSO']:
                seed_results[name].append(base[name])
            print(f"    LMS: {base['LMS']:.2f} dB, NLMS: {base['NLMS']:.2f} dB, "
                  f"OMP: {base['OMP']:.2f} dB, LASSO: {base['LASSO']:.2f} dB")

        # Compute mean ± std
        all_results[str(N)] = {}
        for name in seed_results:
            vals = seed_results[name]
            all_results[str(N)][name] = {
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
                'values': vals
            }

    # Print summary
    print(f"\n\n{'N':<8} {'LMS':<18} {'NLMS':<18} {'OMP':<18} {'LASSO':<18} {'LISTA':<18}")
    print("-" * 98)
    for N in N_values:
        r = all_results[str(N)]
        row = f"{N:<8}"
        for name in ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']:
            row += f"{r[name]['mean']:.2f}±{r[name]['std']:.2f}  ".ljust(18)
        print(row)

    # Save
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'channel_length.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {save_dir}/channel_length.json")


def exp_depth_sweep(save_dir, device, seeds=5, num_test=200):
    """Depth sweep: NMSE vs number of LISTA layers with 5-seed statistics."""
    print("\n" + "=" * 60)
    print("DEPTH SWEEP EXPERIMENT")
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

            model = train_model(LISTA(N, num_layers), N, K, pilot, snr, epochs=200, device=device)
            model.eval()

            # Test
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
            'values': seed_nmse
        }

    # OMP baseline
    print("\n--- OMP baseline ---")
    omp_nmse = []
    for seed in range(seeds):
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)
        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=snr
        )
        omp = OMPFilter(N, K)
        h_omp = torch.zeros_like(h_test)
        for i in range(num_test):
            h_omp[i] = omp.estimate(x_test[i], d_test[i])
        omp_nmse.append(compute_nmse_db(h_omp, h_test))
    all_results['OMP'] = {
        'mean': float(np.mean(omp_nmse)),
        'std': float(np.std(omp_nmse)),
        'values': omp_nmse
    }
    print(f"  OMP: {all_results['OMP']['mean']:.4f} +/- {all_results['OMP']['std']:.4f} dB")

    # Save
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'depth_sweep.json'), 'w') as f:
        json.dump(all_results, f, indent=2)

    # Print summary
    print(f"\n{'Layers':<10} {'NMSE (dB)':<20} {'Std':<10}")
    print("-" * 40)
    for k, v in all_results.items():
        print(f"{k:<10} {v['mean']:<20.4f} {v['std']:<10.4f}")

    print(f"\nSaved to {save_dir}/depth_sweep.json")


# ============================================================
# Experiment: ITU Channel Training
# ============================================================

def generate_itu_training_data(num_samples, channel_length, model_type, pilot_length, snr_db):
    """Generate training data from ITU channel models with random tap positions."""
    h = generate_itu_channel(channel_length, model=model_type, num_samples=num_samples,
                             randomize_positions=True, normalize=True)
    # BPSK pilots
    x = 2 * (torch.rand(num_samples, pilot_length) > 0.5).float() - 1
    # Convolve: d = x * h + noise (flip h for true convolution)
    d = torch.zeros(num_samples, pilot_length)
    for i in range(num_samples):
        x_i = x[i].unsqueeze(0).unsqueeze(0)
        h_i = h[i].unsqueeze(0).unsqueeze(0)
        d[i] = torch.nn.functional.conv1d(
            x_i, torch.flip(h_i, [2]), padding=channel_length - 1
        ).squeeze()[:pilot_length]
    # Add noise
    sig_power = torch.mean(d ** 2)
    noise_power = sig_power / (10 ** (snr_db / 10))
    noise = torch.randn(num_samples, pilot_length) * torch.sqrt(noise_power)
    d = d + noise
    return x, d, h


def train_model_itu(model, channel_length, model_type, pilot_length, snr_db,
                    epochs=300, batch_size=256, device='cpu', snr_range=None,
                    max_threshold=0.005):
    """Train LISTA on ITU channel data."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    for epoch in range(epochs):
        model.train()
        # Variable SNR for robustness (like Gaussian training)
        train_snr = np.random.uniform(0, 30)
        x, d, h = generate_itu_training_data(
            num_samples=batch_size, channel_length=channel_length,
            model_type=model_type, pilot_length=pilot_length, snr_db=train_snr
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

        # Clamp threshold to prevent it from killing weak taps
        if max_threshold is not None:
            for layer in model.layers:
                layer.threshold.threshold.data.clamp_(max=max_threshold)

    return model


def exp_itu_training(save_dir, device, seeds=5, num_test=200):
    """Train LISTA on ITU channels and test on the same channels."""
    print("\n" + "=" * 60)
    print("ITU CHANNEL TRAINING EXPERIMENTS")
    print("=" * 60)

    N, L, pilot, snr = 64, 20, 256, 20
    channel_models = {
        'ITU PedA': 'peda',
        'ITU VehA': 'veha',
    }

    all_results = {}

    for model_name, model_type in channel_models.items():
        print(f"\n--- {model_name} ---")
        lista_vals = []

        for seed in range(seeds):
            print(f"  Seed {seed+1}/{seeds}: Training LISTA on {model_name}...")
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            # Train LISTA on ITU channels (smaller threshold for weak ITU taps)
            model = LISTA(N, L, init_step=0.5, init_threshold=0.0001)
            # Clamp threshold to prevent it from growing too large
            # ITU weak taps have amplitude ~0.03-0.07; threshold must stay well below this
            for layer in model.layers:
                layer.threshold.threshold.data.clamp_(max=0.005)
            model = train_model_itu(
                model, N, model_type, pilot, snr,
                epochs=500, batch_size=256, device=device
            )
            model.eval()

            # Test on same ITU channel model (random positions)
            h_test = generate_itu_channel(N, model=model_type, num_samples=num_test,
                                          randomize_positions=True, normalize=True)
            x_test = torch.randint(0, 2, (num_test, pilot)).float() * 2 - 1
            d_list = []
            for i in range(num_test):
                conv = np.convolve(x_test[i].numpy(), h_test[i].numpy(), mode='full')
                d_list.append(conv[:pilot])
            d_test = torch.tensor(np.array(d_list), dtype=torch.float32)
            sig_power = torch.mean(d_test ** 2)
            noise_power = sig_power / (10 ** (snr / 10))
            noise = torch.randn_like(d_test) * torch.sqrt(noise_power)
            d_test = d_test + noise

            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_test)
            lista_vals.append(nmse_lista)
            print(f"    LISTA (ITU-trained): {nmse_lista:.2f} dB")

            # Baselines (only for first seed, same for all seeds)
            if seed == 0:
                base = evaluate_baselines(x_test, d_test, h_test, N, sparsity=6)  # ITU has ~6 taps
                all_results[model_name] = base.copy()

        if model_name not in all_results:
            all_results[model_name] = {}
        all_results[model_name]['LISTA_itu'] = {
            'mean': float(np.mean(lista_vals)),
            'std': float(np.std(lista_vals)),
            'values': [float(v) for v in lista_vals]
        }

        print(f"\n  {model_name} Summary:")
        print(f"    OMP:   {all_results[model_name].get('OMP', 0):.2f} dB")
        print(f"    LASSO: {all_results[model_name].get('LASSO', 0):.2f} dB")
        print(f"    LMS:   {all_results[model_name].get('LMS', 0):.2f} dB")
        print(f"    NLMS:  {all_results[model_name].get('NLMS', 0):.2f} dB")
        print(f"    LISTA (ITU-trained): {np.mean(lista_vals):.2f} ± {np.std(lista_vals):.2f} dB")

    # Save results
    os.makedirs(save_dir, exist_ok=True)
    save_results = {}
    for k, v in all_results.items():
        save_results[k] = {}
        for k2, v2 in v.items():
            if isinstance(v2, dict) and 'mean' in v2:
                save_results[k][k2] = v2
            elif isinstance(v2, (float, int)):
                save_results[k][k2] = float(v2)
    with open(os.path.join(save_dir, 'itu_training.json'), 'w') as f:
        json.dump(save_results, f, indent=2)

    print(f"\nSaved to {save_dir}/itu_training.json")


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Revision experiments for LISTA paper')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['ablation', 'gen_sparsity', 'gen_snr', 'runtime', 'itu', 'itu_train', 'depth', 'channellen', 'generalization', 'all'])
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--seeds', type=int, default=5, help='Number of random seeds')
    parser.add_argument('--num_test', type=int, default=200, help='Test samples per experiment')
    parser.add_argument('--save_dir', type=str, default='results/revision')

    args = parser.parse_args()
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Seeds: {args.seeds}")

    os.makedirs(args.save_dir, exist_ok=True)

    if args.experiment in ['ablation', 'all']:
        exp_ablation(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['gen_sparsity', 'generalization', 'all']:
        exp_generalization_sparsity(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['gen_snr', 'generalization', 'all']:
        exp_generalization_snr(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['runtime', 'all']:
        exp_runtime(args.save_dir, device, args.num_test)

    if args.experiment in ['itu', 'all']:
        exp_itu_channel(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['itu_train', 'all']:
        exp_itu_training(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['depth', 'all']:
        exp_depth_sweep(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['channellen', 'all']:
        exp_channel_length(args.save_dir, device, args.seeds, args.num_test)

    print("\n\n" + "=" * 60)
    print("ALL REVISION EXPERIMENTS COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
