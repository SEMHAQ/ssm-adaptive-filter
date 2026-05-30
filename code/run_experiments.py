"""
Comprehensive experiments for LISTA sparse channel estimation paper.

Experiments:
1. NMSE vs SNR (fixed N=64, K=5)
2. NMSE vs Sparsity (fixed N=64, SNR=20)
3. NMSE vs Channel Length (fixed K/N ratio, SNR=20)
4. Convergence curves (NMSE vs LISTA layers)
5. Computational complexity comparison

Generates:
- PDF figures for LaTeX
- JSON results for tables
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import time
import argparse

from models.ssm_af import LISTA, OMPFilter, LASSOFilter, LMSFilter, NLMSFilter
from data.generate import generate_sparse_channel_data


def compute_nmse_db(h_est, h_true):
    """NMSE in dB."""
    err = ((h_est - h_true) ** 2).sum(dim=-1)
    power = (h_true ** 2).sum(dim=-1) + 1e-10
    return 10 * np.log10((err / power).mean().item() + 1e-10)


def evaluate_omp(x, d, channel_length, sparsity):
    """Evaluate OMP baseline."""
    omp = OMPFilter(channel_length, sparsity)
    h_list = [omp.estimate(x[i], d[i]) for i in range(x.shape[0])]
    return torch.stack(h_list)


def evaluate_lasso(x, d, channel_length, lam=0.01):
    """Evaluate LASSO baseline."""
    lasso = LASSOFilter(channel_length, lam)
    h_list = [lasso.estimate(x[i], d[i]) for i in range(x.shape[0])]
    return torch.stack(h_list)


def evaluate_lms(x, d, channel_length, mu=0.01):
    """Evaluate LMS baseline (final weights as channel estimate)."""
    h_list = []
    for i in range(x.shape[0]):
        w = np.zeros(channel_length)
        x_buf = np.zeros(channel_length)
        x_np = x[i].numpy()
        d_np = d[i].numpy()
        for n in range(len(x_np)):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x_np[n]
            y_n = np.dot(w, x_buf)
            e_n = d_np[n] - y_n
            w = w + mu * e_n * x_buf
        h_list.append(torch.tensor(w))
    return torch.stack(h_list)


def evaluate_nlms(x, d, channel_length, mu=0.5):
    """Evaluate NLMS baseline."""
    h_list = []
    for i in range(x.shape[0]):
        w = np.zeros(channel_length)
        x_buf = np.zeros(channel_length)
        x_np = x[i].numpy()
        d_np = d[i].numpy()
        for n in range(len(x_np)):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x_np[n]
            y_n = np.dot(w, x_buf)
            e_n = d_np[n] - y_n
            norm = np.dot(x_buf, x_buf) + 1e-8
            w = w + (mu / norm) * e_n * x_buf
        h_list.append(torch.tensor(w))
    return torch.stack(h_list)


def train_lista_model(channel_length, sparsity, num_layers, pilot_length,
                      snr_db, epochs=200, batch_size=64, device='cpu'):
    """Train LISTA model and return it."""
    model = LISTA(channel_length=channel_length, num_layers=num_layers).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
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
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()

    return model


def run_single_experiment(channel_length, sparsity, pilot_length, snr_db,
                          num_layers, num_test, device, epochs=200):
    """Run one full experiment: train LISTA, evaluate all methods."""
    # Generate test data
    torch.manual_seed(42)
    x_test, d_test, h_test = generate_sparse_channel_data(
        num_samples=num_test, channel_length=channel_length,
        sparsity=sparsity, pilot_length=pilot_length, snr_db=snr_db
    )

    results = {}

    # LMS
    h_lms = evaluate_lms(x_test, d_test, channel_length)
    results['LMS'] = compute_nmse_db(h_lms, h_test)

    # NLMS
    h_nlms = evaluate_nlms(x_test, d_test, channel_length)
    results['NLMS'] = compute_nmse_db(h_nlms, h_test)

    # OMP
    h_omp = evaluate_omp(x_test, d_test, channel_length, sparsity)
    results['OMP'] = compute_nmse_db(h_omp, h_test)

    # LASSO
    h_lasso = evaluate_lasso(x_test, d_test, channel_length)
    results['LASSO'] = compute_nmse_db(h_lasso, h_test)

    # LISTA (train fresh for each config)
    print(f"  Training LISTA (N={channel_length}, K={sparsity}, SNR={snr_db})...")
    model = train_lista_model(
        channel_length, sparsity, num_layers, pilot_length, snr_db,
        epochs=epochs, device=device
    )
    model.eval()
    with torch.no_grad():
        h_lista, _, _ = model(x_test.to(device), d_test.to(device))
    results['LISTA'] = compute_nmse_db(h_lista.cpu(), h_test)

    return results


def exp_snr(save_dir, device, num_test=100):
    """Experiment 1: NMSE vs SNR."""
    print("\n=== Experiment 1: NMSE vs SNR ===")
    snr_values = [0, 5, 10, 15, 20, 25, 30]
    N, K, L, pilot = 64, 5, 10, 128

    all_results = {}
    for snr in snr_values:
        print(f"\nSNR = {snr} dB")
        res = run_single_experiment(N, K, pilot, snr, L, num_test, device)
        all_results[snr] = res
        print(f"  LMS={res['LMS']:.2f} NLMS={res['NLMS']:.2f} "
              f"OMP={res['OMP']:.2f} LASSO={res['LASSO']:.2f} LISTA={res['LISTA']:.2f}")

    # Save
    with open(os.path.join(save_dir, 'exp_snr.json'), 'w') as f:
        json.dump({'config': {'N': N, 'K': K, 'L': L, 'pilot': pilot},
                   'results': {str(k): v for k, v in all_results.items()}}, f, indent=2)

    # Plot
    methods = ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']
    markers = ['o', 's', '^', 'D', 'v']
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']

    plt.figure(figsize=(8, 5))
    for m, mk, c in zip(methods, markers, colors):
        y = [all_results[snr][m] for snr in snr_values]
        plt.plot(snr_values, y, marker=mk, color=c, label=m, linewidth=2, markersize=6)
    plt.xlabel('SNR (dB)', fontsize=12)
    plt.ylabel('NMSE (dB)', fontsize=12)
    plt.title('Channel Estimation vs SNR', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'nmse_vs_snr.pdf'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {save_dir}/nmse_vs_snr.pdf")


def exp_sparsity(save_dir, device, num_test=100):
    """Experiment 2: NMSE vs Sparsity."""
    print("\n=== Experiment 2: NMSE vs Sparsity ===")
    sparsity_values = [2, 4, 6, 8, 10, 12, 15]
    N, L, pilot, snr = 64, 10, 128, 20

    all_results = {}
    for K in sparsity_values:
        print(f"\nK = {K}")
        res = run_single_experiment(N, K, pilot, snr, L, num_test, device)
        all_results[K] = res
        print(f"  LMS={res['LMS']:.2f} NLMS={res['NLMS']:.2f} "
              f"OMP={res['OMP']:.2f} LASSO={res['LASSO']:.2f} LISTA={res['LISTA']:.2f}")

    with open(os.path.join(save_dir, 'exp_sparsity.json'), 'w') as f:
        json.dump({'config': {'N': N, 'L': L, 'pilot': pilot, 'snr': snr},
                   'results': {str(k): v for k, v in all_results.items()}}, f, indent=2)

    methods = ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']
    markers = ['o', 's', '^', 'D', 'v']
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']

    plt.figure(figsize=(8, 5))
    for m, mk, c in zip(methods, markers, colors):
        y = [all_results[K][m] for K in sparsity_values]
        plt.plot(sparsity_values, y, marker=mk, color=c, label=m, linewidth=2, markersize=6)
    plt.xlabel('Sparsity K', fontsize=12)
    plt.ylabel('NMSE (dB)', fontsize=12)
    plt.title('Channel Estimation vs Sparsity', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'nmse_vs_sparsity.pdf'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {save_dir}/nmse_vs_sparsity.pdf")


def exp_channel_length(save_dir, device, num_test=100):
    """Experiment 3: NMSE vs Channel Length."""
    print("\n=== Experiment 3: NMSE vs Channel Length ===")
    N_values = [32, 64, 128, 256]
    K_ratio = 0.08  # ~8% sparsity
    L, pilot_ratio, snr = 10, 2, 20

    all_results = {}
    for N in N_values:
        K = max(2, int(N * K_ratio))
        pilot = N * pilot_ratio
        print(f"\nN = {N}, K = {K}, pilot = {pilot}")
        res = run_single_experiment(N, K, pilot, snr, L, num_test, device)
        all_results[N] = res
        print(f"  LMS={res['LMS']:.2f} NLMS={res['NLMS']:.2f} "
              f"OMP={res['OMP']:.2f} LASSO={res['LASSO']:.2f} LISTA={res['LISTA']:.2f}")

    with open(os.path.join(save_dir, 'exp_channel_length.json'), 'w') as f:
        json.dump({'config': {'K_ratio': K_ratio, 'L': L, 'pilot_ratio': pilot_ratio, 'snr': snr},
                   'results': {str(k): v for k, v in all_results.items()}}, f, indent=2)

    methods = ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']
    markers = ['o', 's', '^', 'D', 'v']
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']

    plt.figure(figsize=(8, 5))
    for m, mk, c in zip(methods, markers, colors):
        y = [all_results[N][m] for N in N_values]
        plt.plot(N_values, y, marker=mk, color=c, label=m, linewidth=2, markersize=6)
    plt.xlabel('Channel Length N', fontsize=12)
    plt.ylabel('NMSE (dB)', fontsize=12)
    plt.title('Channel Estimation vs Channel Length', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'nmse_vs_channellen.pdf'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {save_dir}/nmse_vs_channellen.pdf")


def exp_convergence(save_dir, device, num_test=100):
    """Experiment 4: NMSE vs Number of LISTA Layers."""
    print("\n=== Experiment 4: LISTA Convergence ===")
    layer_values = [1, 2, 3, 5, 8, 10, 15, 20]
    N, K, pilot, snr = 64, 5, 128, 20

    # Generate test data
    torch.manual_seed(42)
    x_test, d_test, h_test = generate_sparse_channel_data(
        num_samples=num_test, channel_length=N, sparsity=K,
        pilot_length=pilot, snr_db=snr
    )

    # Baselines (fixed)
    h_omp = evaluate_omp(x_test, d_test, N, K)
    nmse_omp = compute_nmse_db(h_omp, h_test)

    lista_results = []
    for L in layer_values:
        print(f"\nL = {L} layers")
        model = train_lista_model(N, K, L, pilot, snr, epochs=200, device=device)
        model.eval()
        with torch.no_grad():
            h_lista, _, _ = model(x_test.to(device), d_test.to(device))
        nmse = compute_nmse_db(h_lista.cpu(), h_test)
        lista_results.append(nmse)
        print(f"  LISTA({L}) = {nmse:.2f} dB")

    with open(os.path.join(save_dir, 'exp_convergence.json'), 'w') as f:
        json.dump({'config': {'N': N, 'K': K, 'pilot': pilot, 'snr': snr},
                   'layers': layer_values,
                   'lista_nmse': lista_results,
                   'omp_nmse': nmse_omp}, f, indent=2)

    plt.figure(figsize=(8, 5))
    plt.plot(layer_values, lista_results, 'rv-', label='LISTA', linewidth=2, markersize=6)
    plt.axhline(y=nmse_omp, color='#FF9800', linestyle='--', label=f'OMP ({nmse_omp:.1f} dB)', linewidth=1.5)
    plt.xlabel('Number of Layers (Iterations)', fontsize=12)
    plt.ylabel('NMSE (dB)', fontsize=12)
    plt.title('LISTA Convergence', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'lista_convergence.pdf'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {save_dir}/lista_convergence.pdf")


def main():
    parser = argparse.ArgumentParser(description='Run all sparse channel experiments')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['snr', 'sparsity', 'channellen', 'convergence', 'all'])
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--num_test', type=int, default=100)
    parser.add_argument('--save_dir', type=str, default='res/sparse_channel/figures')

    args = parser.parse_args()
    os.makedirs(args.save_dir, exist_ok=True)
    os.makedirs('results/sparse_channel', exist_ok=True)

    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    if args.experiment in ['snr', 'all']:
        exp_snr(args.save_dir, device, args.num_test)
    if args.experiment in ['sparsity', 'all']:
        exp_sparsity(args.save_dir, device, args.num_test)
    if args.experiment in ['channellen', 'all']:
        exp_channel_length(args.save_dir, device, args.num_test)
    if args.experiment in ['convergence', 'all']:
        exp_convergence(args.save_dir, device, args.num_test)

    print("\n\nAll experiments complete!")


if __name__ == '__main__':
    main()
