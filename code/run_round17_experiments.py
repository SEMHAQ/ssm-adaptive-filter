"""
Round 17 experiments: address all critical/high reviewer issues.

R1: Pre-thresholding error concentration analysis + learned threshold reporting
R3: CNN baseline comparison
R4: Complex-valued channel estimation
R8: Fairer FISTA comparison (SNR-specific LISTA vs single-threshold FISTA)

Usage:
    cd code
    python run_round17_experiments.py --experiment all --device cuda --seeds 20
    python run_round17_experiments.py --experiment pre_threshold --device cuda --seeds 20
    python run_round17_experiments.py --experiment cnn --device cuda --seeds 5
    python run_round17_experiments.py --experiment complex --device cuda --seeds 5
    python run_round17_experiments.py --experiment fista_fair --device cuda --seeds 5
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import argparse
from scipy import stats

from models.ssm_af import (
    LISTA, LISTALayer, OMPFilter, LASSOFilter, FISTAFilter,
    ISTAFilter, CNNChannelEstimator, ComplexLISTA
)
from data.generate import generate_sparse_channel_data, generate_complex_sparse_channel_data


# ============================================================
# Helpers
# ============================================================

def compute_nmse_db(h_est, h_true):
    """NMSE in dB."""
    if h_est.is_complex():
        err = (torch.abs(h_est - h_true) ** 2).sum(dim=-1)
        power = (torch.abs(h_true) ** 2).sum(dim=-1) + 1e-10
    else:
        err = ((h_est - h_true) ** 2).sum(dim=-1)
        power = (h_true ** 2).sum(dim=-1) + 1e-10
    return 10 * np.log10((err / power).mean().item() + 1e-10)


def compute_error_sparsity(h_est, h_true, K):
    """Compute error concentration metrics for a batch of estimates."""
    batch = h_est.shape[0]
    if h_est.is_complex():
        h_est_abs = h_est.abs()
        h_true_abs = h_true.abs()
    else:
        h_est_abs = h_est.abs()
        h_true_abs = h_true.abs()

    _, true_support = torch.topk(h_true_abs, K, dim=1)

    results = []
    for i in range(batch):
        if h_est.is_complex():
            err_energy = (torch.abs(h_est[i] - h_true[i]) ** 2).float()
        else:
            err_energy = (h_est[i] - h_true[i]) ** 2
        total_err = err_energy.sum().item() + 1e-20

        S = true_support[i]
        err_on_S = err_energy[S].sum().item()
        err_on_Sbar = total_err - err_on_S

        # Count non-zero non-support entries
        non_support_mask = torch.ones(h_est.shape[1], dtype=torch.bool)
        non_support_mask[S] = False
        if h_est.is_complex():
            nonzero_non_support = (torch.abs(h_est[i][non_support_mask]) > 1e-6).sum().item()
        else:
            nonzero_non_support = (torch.abs(h_est[i][non_support_mask]) > 1e-6).sum().item()

        results.append({
            'error_on_S_pct': err_on_S / total_err * 100,
            'error_on_Sbar_pct': err_on_Sbar / total_err * 100,
            'gini': 0.0,  # simplified
            'nonzero_non_support': nonzero_non_support,
        })

    avg = {}
    for key in results[0]:
        vals = [r[key] for r in results]
        avg[key] = {'mean': float(np.mean(vals)), 'std': float(np.std(vals)),
                     'values': [float(v) for v in vals]}
    return avg


def train_lista_mixed_snr(model, N, K, pilot, epochs=200, batch_size=256, device='cpu'):
    """Train LISTA with mixed-SNR protocol (paper standard)."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    for epoch in range(epochs):
        model.train()
        snr_train = np.random.uniform(0, 30)
        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size, channel_length=N,
            sparsity=K, pilot_length=pilot, snr_db=snr_train
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


def train_lista_snr_specific(model, N, K, pilot, snr_range, epochs=200, batch_size=256, device='cpu'):
    """Train LISTA with SNR-specific protocol."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    for epoch in range(epochs):
        model.train()
        snr_train = np.random.uniform(snr_range[0], snr_range[1])
        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size, channel_length=N,
            sparsity=K, pilot_length=pilot, snr_db=snr_train
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


def train_cnn(model, N, K, pilot, epochs=200, batch_size=256, device='cpu'):
    """Train CNN baseline with same mixed-SNR protocol as LISTA."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    for epoch in range(epochs):
        model.train()
        snr_train = np.random.uniform(0, 30)
        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size, channel_length=N,
            sparsity=K, pilot_length=pilot, snr_db=snr_train
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


def train_complex_lista(model, N, K, pilot, epochs=200, batch_size=256, device='cpu'):
    """Train complex LISTA with mixed-SNR protocol."""
    model = model.to(device)
    # Use float parameters for the real/imag linear layers
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    for epoch in range(epochs):
        model.train()
        snr_train = np.random.uniform(0, 30)
        x, d, h = generate_complex_sparse_channel_data(
            num_samples=batch_size, channel_length=N,
            sparsity=K, pilot_length=pilot, snr_db=snr_train
        )
        x, d, h = x.to(device), d.to(device), h.to(device)
        h_est, _, _ = model(x, d)
        # NMSE loss for complex: |h_est - h|^2 / |h|^2
        loss = (torch.abs(h_est - h) ** 2).mean() / (torch.abs(h) ** 2).mean().clamp(min=1e-10)
        if torch.isnan(loss):
            continue
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()
        scheduler.step()
    return model


def extract_learned_thresholds(model):
    """Extract learned threshold values from each LISTA layer."""
    thresholds = []
    for i, layer in enumerate(model.layers):
        thresholds.append({
            'layer': i,
            'threshold': float(layer.threshold.threshold.data.item()),
            'step': float(layer.step.data.item()),
        })
    return thresholds


def extract_complex_thresholds(model):
    """Extract learned threshold values from complex LISTA layers."""
    thresholds = []
    for i, layer in enumerate(model.layers):
        thresholds.append({
            'layer': i,
            'threshold': float(layer.threshold.threshold.data.item()),
            'step': float(layer.step.data.item()),
        })
    return thresholds


# ============================================================
# R1: Pre-thresholding error concentration analysis
# ============================================================

def exp_pre_thresholding(save_dir, device, seeds=20, num_test=500):
    """
    R1: Verify error concentration mechanism.
    - Compute error concentration on pre-thresholding intermediate
    - Report learned threshold values θ^(k) for each layer
    - Count non-zero non-support taps
    - Use 20 seeds for statistical power
    """
    print("\n" + "=" * 60)
    print("R1: PRE-THRESHOLDING ERROR CONCENTRATION ANALYSIS")
    print("=" * 60)

    N, K, L, pilot, snr = 64, 5, 20, 256, 20

    all_results = {
        'post_threshold': {'lista': [], 'omp': [], 'ista': []},
        'pre_threshold': {'lista': []},
        'thresholds': [],
        'nonzero_non_support': {'lista': [], 'omp': []},
    }

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA
        print("  Training LISTA...")
        model = train_lista_mixed_snr(LISTA(N, L), N, K, pilot, epochs=200, device=device)
        model.eval()

        # Test data
        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=snr
        )

        # Extract learned thresholds
        thresholds = extract_learned_thresholds(model)
        all_results['thresholds'].append(thresholds)
        if seed == 0:
            print(f"  Learned thresholds (seed 0):")
            for t in thresholds:
                print(f"    Layer {t['layer']}: θ={t['threshold']:.6f}, μ={t['step']:.6f}")

        # Post-thresholding error concentration (LISTA)
        with torch.no_grad():
            h_lista, _, _ = model(x_test.to(device), d_test.to(device))
        h_lista = h_lista.cpu()
        post_lista = compute_error_sparsity(h_lista, h_test, K)
        all_results['post_threshold']['lista'].append(post_lista)

        # Pre-thresholding error concentration (LISTA)
        # Run forward pass manually to capture pre-thresholding intermediates
        with torch.no_grad():
            A = model._build_toeplitz(x_test.to(device))
            h = torch.zeros(x_test.shape[0], N, device=device)
            pre_threshold_errors = []
            for layer_idx, layer in enumerate(model.layers):
                d_recon = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
                residual = (d_recon - x_test.to(device)[:, :pilot] if False else d_recon - d_test.to(device)).unsqueeze(-1)
                grad = torch.bmm(A.transpose(1, 2), residual).squeeze(-1) / pilot
                h_new = layer.W(h) - layer.step * grad
                # Compute error concentration on pre-thresholding h_new
                pre_conc = compute_error_sparsity(h_new.cpu(), h_test, K)
                h = layer(h, grad)  # apply threshold for next iteration
            # Use last layer's pre-thresholding result
            all_results['pre_threshold']['lista'].append(pre_conc)

        # OMP baseline
        omp = OMPFilter(N, K)
        h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])
        post_omp = compute_error_sparsity(h_omp, h_test, K)
        all_results['post_threshold']['omp'].append(post_omp)

        # ISTA baseline (grid-searched threshold)
        best_ista_nmse = float('inf')
        best_ista_h = None
        for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
            ista = ISTAFilter(N, num_iterations=20, threshold=thresh)
            h_ista = torch.stack([ista.estimate(x_test[i], d_test[i]) for i in range(num_test)])
            nmse_ista = compute_nmse_db(h_ista, h_test)
            if nmse_ista < best_ista_nmse:
                best_ista_nmse = nmse_ista
                best_ista_h = h_ista
        post_ista = compute_error_sparsity(best_ista_h, h_test, K)
        all_results['post_threshold']['ista'].append(post_ista)

        print(f"  Post-threshold LISTA: error_on_S={post_lista['error_on_S_pct']['mean']:.2f}%, "
              f"non_support_nz={post_lista['nonzero_non_support']['mean']:.1f}")
        print(f"  Pre-threshold LISTA:  error_on_S={pre_conc['error_on_S_pct']['mean']:.2f}%")
        print(f"  Post-threshold OMP:   error_on_S={post_omp['error_on_S_pct']['mean']:.2f}%")
        print(f"  Post-threshold ISTA:  error_on_S={post_ista['error_on_S_pct']['mean']:.2f}%")

    # Aggregate results
    print("\n\n=== PRE-THRESHOLDING ANALYSIS RESULTS ===")

    # Compute aggregate statistics
    def aggregate_metric(all_seed_results, key):
        """Aggregate a metric across seeds."""
        means = [r[key]['mean'] for r in all_seed_results]
        return {
            'mean': float(np.mean(means)),
            'std': float(np.std(means)),
            'seeds': [float(m) for m in means],
        }

    summary = {}

    # Post-thresholding
    summary['post_threshold_lista'] = {
        'error_on_S': aggregate_metric(all_results['post_threshold']['lista'], 'error_on_S_pct'),
        'error_on_Sbar': aggregate_metric(all_results['post_threshold']['lista'], 'error_on_Sbar_pct'),
        'nonzero_non_support': aggregate_metric(all_results['post_threshold']['lista'], 'nonzero_non_support'),
    }
    summary['post_threshold_omp'] = {
        'error_on_S': aggregate_metric(all_results['post_threshold']['omp'], 'error_on_S_pct'),
        'error_on_Sbar': aggregate_metric(all_results['post_threshold']['omp'], 'error_on_Sbar_pct'),
        'nonzero_non_support': aggregate_metric(all_results['post_threshold']['omp'], 'nonzero_non_support'),
    }
    summary['post_threshold_ista'] = {
        'error_on_S': aggregate_metric(all_results['post_threshold']['ista'], 'error_on_S_pct'),
        'error_on_Sbar': aggregate_metric(all_results['post_threshold']['ista'], 'error_on_Sbar_pct'),
        'nonzero_non_support': aggregate_metric(all_results['post_threshold']['ista'], 'nonzero_non_support'),
    }

    # Pre-thresholding
    summary['pre_threshold_lista'] = {
        'error_on_S': aggregate_metric(all_results['pre_threshold']['lista'], 'error_on_S_pct'),
        'error_on_Sbar': aggregate_metric(all_results['pre_threshold']['lista'], 'error_on_Sbar_pct'),
    }

    # Learned thresholds (average across seeds)
    if all_results['thresholds']:
        avg_thresholds = []
        for layer_idx in range(L):
            ths = [s[layer_idx]['threshold'] for s in all_results['thresholds']]
            stps = [s[layer_idx]['step'] for s in all_results['thresholds']]
            avg_thresholds.append({
                'layer': layer_idx,
                'threshold_mean': float(np.mean(ths)),
                'threshold_std': float(np.std(ths)),
                'step_mean': float(np.mean(stps)),
                'step_std': float(np.std(stps)),
            })
        summary['learned_thresholds'] = avg_thresholds

    # Print summary
    print(f"\nPost-threshold LISTA:")
    print(f"  Error on S:   {summary['post_threshold_lista']['error_on_S']['mean']:.2f}% ± "
          f"{summary['post_threshold_lista']['error_on_S']['std']:.2f}%")
    print(f"  Error on S̄:   {summary['post_threshold_lista']['error_on_Sbar']['mean']:.4f}% ± "
          f"{summary['post_threshold_lista']['error_on_Sbar']['std']:.4f}%")
    print(f"  Non-zero S̄:   {summary['post_threshold_lista']['nonzero_non_support']['mean']:.1f} ± "
          f"{summary['post_threshold_lista']['nonzero_non_support']['std']:.1f}")

    print(f"\nPre-threshold LISTA (last layer):")
    print(f"  Error on S:   {summary['pre_threshold_lista']['error_on_S']['mean']:.2f}% ± "
          f"{summary['pre_threshold_lista']['error_on_S']['std']:.2f}%")
    print(f"  Error on S̄:   {summary['pre_threshold_lista']['error_on_Sbar']['mean']:.2f}% ± "
          f"{summary['pre_threshold_lista']['error_on_Sbar']['std']:.2f}%")

    print(f"\nPost-threshold OMP:")
    print(f"  Error on S:   {summary['post_threshold_omp']['error_on_S']['mean']:.2f}% ± "
          f"{summary['post_threshold_omp']['error_on_S']['std']:.2f}%")

    print(f"\nPost-threshold ISTA:")
    print(f"  Error on S:   {summary['post_threshold_ista']['error_on_S']['mean']:.2f}% ± "
          f"{summary['post_threshold_ista']['error_on_S']['std']:.2f}%")

    # Wilcoxon rank-sum test: LISTA non-support error vs OMP non-support error
    lista_ns = summary['post_threshold_lista']['error_on_Sbar']['seeds']
    omp_ns = summary['post_threshold_omp']['error_on_Sbar']['seeds']
    if len(lista_ns) >= 5 and len(omp_ns) >= 5:
        stat, p_val = stats.ranksums(lista_ns, omp_ns)
        summary['wilcoxon_lista_vs_omp'] = {'statistic': float(stat), 'p_value': float(p_val)}
        print(f"\nWilcoxon rank-sum (LISTA vs OMP non-support error): p={p_val:.6f}")

    # Print learned thresholds
    if 'learned_thresholds' in summary:
        print(f"\nLearned thresholds (averaged over {seeds} seeds):")
        print(f"{'Layer':<8} {'θ (mean±std)':<25} {'μ (mean±std)':<25}")
        print("-" * 58)
        for t in summary['learned_thresholds']:
            print(f"{t['layer']:<8} {t['threshold_mean']:.6f}±{t['threshold_std']:.6f}  "
                  f"{t['step_mean']:.6f}±{t['step_std']:.6f}")

    # Save
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'pre_threshold.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/pre_threshold.json")


# ============================================================
# R3: CNN baseline
# ============================================================

def exp_cnn_baseline(save_dir, device, seeds=5, num_test=200):
    """
    R3: Compare LISTA against 1D CNN baseline.
    Train CNN with same protocol, report NMSE and error concentration.
    """
    print("\n" + "=" * 60)
    print("R3: CNN BASELINE COMPARISON")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    snr_values = [-5, 0, 5, 10, 15, 20, 25, 30, 40]

    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA
        print("  Training LISTA...")
        lista = train_lista_mixed_snr(LISTA(N, L), N, K, pilot, epochs=200, device=device)
        lista.eval()

        # Train CNN
        print("  Training CNN...")
        cnn = CNNChannelEstimator(N, pilot, hidden_channels=96, num_layers=4, kernel_size=5)
        n_cnn_params = sum(p.numel() for p in cnn.parameters())
        print(f"    CNN parameters: {n_cnn_params:,}")
        cnn = train_cnn(cnn, N, K, pilot, epochs=200, device=device)
        cnn.eval()

        for test_snr in snr_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=test_snr
            )

            # LISTA
            with torch.no_grad():
                h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_lista.cpu(), h_test)

            # CNN
            with torch.no_grad():
                h_cnn, _, _ = cnn(x_test.to(device), d_test.to(device))
            nmse_cnn = compute_nmse_db(h_cnn.cpu(), h_test)

            # OMP
            omp = OMPFilter(N, K)
            h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])
            nmse_omp = compute_nmse_db(h_omp, h_test)

            # FISTA (grid-searched)
            best_fista_nmse = float('inf')
            for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
                fista = FISTAFilter(N, num_iterations=20, threshold=thresh)
                h_fista = torch.stack([fista.estimate(x_test[j], d_test[j]) for j in range(num_test)])
                nmse_f = compute_nmse_db(h_fista, h_test)
                if nmse_f < best_fista_nmse:
                    best_fista_nmse = nmse_f

            if str(test_snr) not in all_results:
                all_results[str(test_snr)] = {
                    'LISTA': [], 'CNN': [], 'OMP': [], 'FISTA': []
                }
            all_results[str(test_snr)]['LISTA'].append(nmse_lista)
            all_results[str(test_snr)]['CNN'].append(nmse_cnn)
            all_results[str(test_snr)]['OMP'].append(nmse_omp)
            all_results[str(test_snr)]['FISTA'].append(best_fista_nmse)

            print(f"    SNR={test_snr:>3}dB: LISTA={nmse_lista:.2f}, CNN={nmse_cnn:.2f}, "
                  f"OMP={nmse_omp:.2f}, FISTA={best_fista_nmse:.2f}")

    # Error concentration for CNN at SNR=20
    print("\n  Computing error concentration for CNN at SNR=20...")
    torch.manual_seed(0)
    np.random.seed(0)
    x_test, d_test, h_test = generate_sparse_channel_data(
        num_samples=num_test, channel_length=N, sparsity=K,
        pilot_length=pilot, snr_db=20
    )
    # Retrain CNN for error concentration
    torch.manual_seed(0)
    cnn_ec = CNNChannelEstimator(N, pilot, hidden_channels=96, num_layers=4, kernel_size=5)
    cnn_ec = train_cnn(cnn_ec, N, K, pilot, epochs=200, device=device)
    cnn_ec.eval()
    with torch.no_grad():
        h_cnn_ec, _, _ = cnn_ec(x_test.to(device), d_test.to(device))
    ec_cnn = compute_error_sparsity(h_cnn_ec.cpu(), h_test, K)

    # LISTA error concentration
    torch.manual_seed(0)
    lista_ec = train_lista_mixed_snr(LISTA(N, L), N, K, pilot, epochs=200, device=device)
    lista_ec.eval()
    with torch.no_grad():
        h_lista_ec, _, _ = lista_ec(x_test.to(device), d_test.to(device))
    ec_lista = compute_error_sparsity(h_lista_ec.cpu(), h_test, K)

    # Summary
    summary = {'snr_sweep': {}, 'error_concentration': {}, 'cnn_params': n_cnn_params}
    for snr in snr_values:
        s = str(snr)
        summary['snr_sweep'][s] = {}
        for method in ['LISTA', 'CNN', 'OMP', 'FISTA']:
            vals = all_results[s][method]
            summary['snr_sweep'][s][method] = {
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
            }

    summary['error_concentration'] = {
        'CNN': {
            'error_on_S': ec_cnn['error_on_S_pct'],
            'error_on_Sbar': ec_cnn['error_on_Sbar_pct'],
        },
        'LISTA': {
            'error_on_S': ec_lista['error_on_S_pct'],
            'error_on_Sbar': ec_lista['error_on_Sbar_pct'],
        },
    }

    print(f"\n\n=== CNN BASELINE RESULTS ===")
    print(f"CNN parameters: {n_cnn_params:,}")
    print(f"\n{'SNR':<6} {'LISTA':<15} {'CNN':<15} {'OMP':<15} {'FISTA':<15}")
    print("-" * 66)
    for snr in snr_values:
        s = str(snr)
        l = summary['snr_sweep'][s]
        print(f"{snr:<6} {l['LISTA']['mean']:<8.2f}±{l['LISTA']['std']:<5.2f} "
              f"{l['CNN']['mean']:<8.2f}±{l['CNN']['std']:<5.2f} "
              f"{l['OMP']['mean']:<8.2f}±{l['OMP']['std']:<5.2f} "
              f"{l['FISTA']['mean']:<8.2f}±{l['FISTA']['std']:<5.2f}")

    print(f"\nError concentration at SNR=20:")
    print(f"  CNN:   S={ec_cnn['error_on_S_pct']['mean']:.2f}%, "
          f"S̄={ec_cnn['error_on_Sbar_pct']['mean']:.4f}%")
    print(f"  LISTA: S={ec_lista['error_on_S_pct']['mean']:.2f}%, "
          f"S̄={ec_lista['error_on_Sbar_pct']['mean']:.4f}%")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'cnn_baseline.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/cnn_baseline.json")


# ============================================================
# R4: Complex-valued channel estimation
# ============================================================

def exp_complex_channel(save_dir, device, seeds=5, num_test=200):
    """
    R4: Complex-valued channel estimation with QPSK pilots.
    Test whether error concentration mechanism transfers to complex domain.
    """
    print("\n" + "=" * 60)
    print("R4: COMPLEX-VALUED CHANNEL ESTIMATION")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    snr_values = [0, 5, 10, 15, 20, 25, 30]

    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train complex LISTA
        print("  Training Complex LISTA...")
        model = ComplexLISTA(N, L)
        model = train_complex_lista(model, N, K, pilot, epochs=200, device=device)
        model.eval()

        for test_snr in snr_values:
            x_test, d_test, h_test = generate_complex_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=test_snr
            )

            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse = compute_nmse_db(h_est.cpu(), h_test)

            if str(test_snr) not in all_results:
                all_results[str(test_snr)] = {'lista': [], 'omp': []}
            all_results[str(test_snr)]['lista'].append(nmse)

            # Complex OMP baseline (use real part for OMP)
            omp = OMPFilter(N, K)
            h_omp_list = []
            for i in range(num_test):
                # Use real part for OMP (simplified)
                h_omp_real = omp.estimate(x_test[i].real, d_test[i].real)
                h_omp_imag = omp.estimate(x_test[i].imag, d_test[i].imag)
                h_omp_list.append(torch.complex(h_omp_real, h_omp_imag))
            h_omp = torch.stack(h_omp_list)
            nmse_omp = compute_nmse_db(h_omp, h_test)
            all_results[str(test_snr)]['omp'].append(nmse_omp)

            print(f"    SNR={test_snr:>3}dB: Complex LISTA={nmse:.2f}, OMP={nmse_omp:.2f}")

    # Error concentration for complex LISTA at SNR=20
    print("\n  Computing error concentration for complex LISTA at SNR=20...")
    torch.manual_seed(0)
    np.random.seed(0)
    x_test, d_test, h_test = generate_complex_sparse_channel_data(
        num_samples=num_test, channel_length=N, sparsity=K,
        pilot_length=pilot, snr_db=20
    )
    torch.manual_seed(0)
    model_ec = ComplexLISTA(N, L)
    model_ec = train_complex_lista(model_ec, N, K, pilot, epochs=200, device=device)
    model_ec.eval()
    with torch.no_grad():
        h_est_ec, _, _ = model_ec(x_test.to(device), d_test.to(device))
    ec_complex = compute_error_sparsity(h_est_ec.cpu(), h_test, K)

    # Complex OMP error concentration
    omp_ec = OMPFilter(N, K)
    h_omp_ec_list = []
    for i in range(num_test):
        h_omp_real = omp_ec.estimate(x_test[i].real, d_test[i].real)
        h_omp_imag = omp_ec.estimate(x_test[i].imag, d_test[i].imag)
        h_omp_ec_list.append(torch.complex(h_omp_real, h_omp_imag))
    h_omp_ec = torch.stack(h_omp_ec_list)
    ec_omp_complex = compute_error_sparsity(h_omp_ec, h_test, K)

    # Extract complex LISTA thresholds
    thresholds = extract_complex_thresholds(model_ec)

    # Summary
    summary = {'snr_sweep': {}, 'error_concentration': {}, 'thresholds': thresholds}
    for snr in snr_values:
        s = str(snr)
        lista_vals = all_results[s]['lista']
        omp_vals = all_results[s]['omp']
        summary['snr_sweep'][s] = {
            'Complex_LISTA': {'mean': float(np.mean(lista_vals)), 'std': float(np.std(lista_vals))},
            'Complex_OMP': {'mean': float(np.mean(omp_vals)), 'std': float(np.std(omp_vals))},
        }

    summary['error_concentration'] = {
        'Complex_LISTA': {
            'error_on_S': ec_complex['error_on_S_pct'],
            'error_on_Sbar': ec_complex['error_on_Sbar_pct'],
            'nonzero_non_support': ec_complex['nonzero_non_support'],
        },
        'Complex_OMP': {
            'error_on_S': ec_omp_complex['error_on_S_pct'],
            'error_on_Sbar': ec_omp_complex['error_on_Sbar_pct'],
            'nonzero_non_support': ec_omp_complex['nonzero_non_support'],
        },
    }

    print(f"\n\n=== COMPLEX-VALUED RESULTS ===")
    print(f"\n{'SNR':<6} {'Complex LISTA':<20} {'Complex OMP':<20}")
    print("-" * 46)
    for snr in snr_values:
        s = str(snr)
        l = summary['snr_sweep'][s]
        print(f"{snr:<6} {l['Complex_LISTA']['mean']:<10.2f}±{l['Complex_LISTA']['std']:<8.2f} "
              f"{l['Complex_OMP']['mean']:<10.2f}±{l['Complex_OMP']['std']:<8.2f}")

    print(f"\nError concentration at SNR=20 (complex):")
    print(f"  Complex LISTA: S={ec_complex['error_on_S_pct']['mean']:.2f}%, "
          f"S̄={ec_complex['error_on_Sbar_pct']['mean']:.4f}%")
    print(f"  Complex OMP:   S={ec_omp_complex['error_on_S_pct']['mean']:.2f}%, "
          f"S̄={ec_omp_complex['error_on_Sbar_pct']['mean']:.4f}%")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'complex_channel.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/complex_channel.json")


# ============================================================
# R8: Fairer FISTA comparison
# ============================================================

def exp_fista_fair_comparison(save_dir, device, seeds=5, num_test=200):
    """
    R8: Fairer comparison: SNR-specific LISTA vs single-threshold FISTA.
    Addresses the asymmetry where FISTA gets per-SNR optimization.
    """
    print("\n" + "=" * 60)
    print("R8: FAIRER FISTA COMPARISON")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    snr_values = [-5, 0, 5, 10, 15, 20, 25, 30, 40]

    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train SNR-specific LISTA at SNR=20
        print("  Training SNR-specific LISTA (SNR∈[15,25])...")
        lista_specific = train_lista_snr_specific(
            LISTA(N, L), N, K, pilot, snr_range=(15, 25), epochs=200, device=device
        )
        lista_specific.eval()

        # Train mixed-SNR LISTA (standard)
        print("  Training mixed-SNR LISTA (SNR∈[0,30])...")
        lista_mixed = train_lista_mixed_snr(LISTA(N, L), N, K, pilot, epochs=200, device=device)
        lista_mixed.eval()

        # Find best single FISTA threshold across all SNR (instead of per-SNR)
        print("  Finding best single FISTA threshold...")
        best_thresh = None
        best_total_nmse = float('inf')
        for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
            total_nmse = 0
            for val_snr in [0, 10, 20, 30]:
                x_val, d_val, h_val = generate_sparse_channel_data(
                    num_samples=100, channel_length=N, sparsity=K,
                    pilot_length=pilot, snr_db=val_snr
                )
                fista = FISTAFilter(N, num_iterations=20, threshold=thresh)
                h_fista = torch.stack([fista.estimate(x_val[i], d_val[i]) for i in range(100)])
                total_nmse += compute_nmse_db(h_fista, h_val)
            if total_nmse < best_total_nmse:
                best_total_nmse = total_nmse
                best_thresh = thresh
        print(f"    Best single threshold: {best_thresh}")

        for test_snr in snr_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=test_snr
            )

            # SNR-specific LISTA
            with torch.no_grad():
                h_ls, _, _ = lista_specific(x_test.to(device), d_test.to(device))
            nmse_ls = compute_nmse_db(h_ls.cpu(), h_test)

            # Mixed-SNR LISTA
            with torch.no_grad():
                h_lm, _, _ = lista_mixed(x_test.to(device), d_test.to(device))
            nmse_lm = compute_nmse_db(h_lm.cpu(), h_test)

            # Single-threshold FISTA
            fista = FISTAFilter(N, num_iterations=20, threshold=best_thresh)
            h_fista = torch.stack([fista.estimate(x_test[i], d_test[i]) for i in range(num_test)])
            nmse_fista_single = compute_nmse_db(h_fista, h_test)

            # Per-SNR best FISTA (for reference)
            best_fista_per_snr = float('inf')
            for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
                fista_p = FISTAFilter(N, num_iterations=20, threshold=thresh)
                h_fp = torch.stack([fista_p.estimate(x_test[j], d_test[j]) for j in range(num_test)])
                nmse_fp = compute_nmse_db(h_fp, h_test)
                if nmse_fp < best_fista_per_snr:
                    best_fista_per_snr = nmse_fp

            if str(test_snr) not in all_results:
                all_results[str(test_snr)] = {
                    'lista_snr_specific': [], 'lista_mixed': [],
                    'fista_single': [], 'fista_per_snr': [],
                }
            all_results[str(test_snr)]['lista_snr_specific'].append(nmse_ls)
            all_results[str(test_snr)]['lista_mixed'].append(nmse_lm)
            all_results[str(test_snr)]['fista_single'].append(nmse_fista_single)
            all_results[str(test_snr)]['fista_per_snr'].append(best_fista_per_snr)

            print(f"    SNR={test_snr:>3}dB: LISTA_snr={nmse_ls:.2f}, LISTA_mix={nmse_lm:.2f}, "
                  f"FISTA_single={nmse_fista_single:.2f}, FISTA_per={best_fista_per_snr:.2f}")

    # Summary
    summary = {'best_fista_threshold': best_thresh, 'snr_sweep': {}}
    for snr in snr_values:
        s = str(snr)
        summary['snr_sweep'][s] = {}
        for method in ['lista_snr_specific', 'lista_mixed', 'fista_single', 'fista_per_snr']:
            vals = all_results[s][method]
            summary['snr_sweep'][s][method] = {
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
            }

    print(f"\n\n=== FAIRER FISTA COMPARISON RESULTS ===")
    print(f"Best single FISTA threshold: {best_thresh}")
    print(f"\n{'SNR':<6} {'LISTA_snr':<18} {'LISTA_mix':<18} {'FISTA_single':<18} {'FISTA_per':<18}")
    print("-" * 78)
    for snr in snr_values:
        s = str(snr)
        r = summary['snr_sweep'][s]
        print(f"{snr:<6} {r['lista_snr_specific']['mean']:<10.2f}±{r['lista_snr_specific']['std']:<5.2f} "
              f"{r['lista_mixed']['mean']:<10.2f}±{r['lista_mixed']['std']:<5.2f} "
              f"{r['fista_single']['mean']:<10.2f}±{r['fista_single']['std']:<5.2f} "
              f"{r['fista_per_snr']['mean']:<10.2f}±{r['fista_per_snr']['std']:<5.2f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'fista_fair.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/fista_fair.json")


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Round 17 experiments')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['pre_threshold', 'cnn', 'complex', 'fista_fair', 'all'])
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--seeds', type=int, default=20)
    parser.add_argument('--num_test', type=int, default=500)
    parser.add_argument('--save_dir', type=str, default='results/round17')

    args = parser.parse_args()
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Seeds: {args.seeds}")

    os.makedirs(args.save_dir, exist_ok=True)

    if args.experiment in ['pre_threshold', 'all']:
        exp_pre_thresholding(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['cnn', 'all']:
        exp_cnn_baseline(args.save_dir, device, min(args.seeds, 5), min(args.num_test, 200))

    if args.experiment in ['complex', 'all']:
        exp_complex_channel(args.save_dir, device, min(args.seeds, 5), min(args.num_test, 200))

    if args.experiment in ['fista_fair', 'all']:
        exp_fista_fair_comparison(args.save_dir, device, min(args.seeds, 5), min(args.num_test, 200))

    print("\n\n" + "=" * 60)
    print("ALL ROUND 17 EXPERIMENTS COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
