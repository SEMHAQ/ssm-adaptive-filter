"""
Round 14 experiments: address all 5 required reviewer fixes.

R1: ISTA control experiment for error concentration
R2: FISTA baseline (L=20 iterations)
R4: Error sparsity analysis at K=10

Usage:
    cd code
    python run_round14_experiments.py --device cuda --seeds 5
"""

import torch
import numpy as np
import json
import os
import argparse
from pathlib import Path

from models.ssm_af import (
    LISTA, OMPFilter, LASSOFilter, ISTAFilter, FISTAFilter
)
from data.generate import generate_sparse_channel_data


# ============================================================
# Helpers
# ============================================================

def compute_nmse_db(h_est, h_true):
    err = ((h_est - h_true) ** 2).sum(dim=-1)
    power = (h_true ** 2).sum(dim=-1) + 1e-10
    return 10 * np.log10((err / power).mean().item() + 1e-10)


def build_conv_matrix(x, channel_length):
    B, M = x.shape
    N = channel_length
    A = torch.zeros(B, M, N)
    for j in range(N):
        A[:, j:, j] = x[:, :M - j]
    return A


def train_lista(model, N, K, pilot, snr, epochs=200, batch_size=256, device='cpu'):
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    for epoch in range(epochs):
        model.train()
        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size, channel_length=N,
            sparsity=K, pilot_length=pilot, snr_db=snr
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
# Error sparsity analysis
# ============================================================

def compute_error_sparsity(h_est, h_true, K):
    """Compute error concentration metrics for a batch of estimates."""
    batch = h_est.shape[0]
    N = h_est.shape[1]

    # Determine true support set (top-K by magnitude)
    _, true_support = torch.topk(h_true.abs(), K, dim=1)

    results = []
    for i in range(batch):
        err = h_est[i] - h_true[i]
        err_energy = err ** 2
        total_err = err_energy.sum().item() + 1e-20

        # Error on true support
        S = true_support[i]
        err_on_S = err_energy[S].sum().item()
        err_on_Sbar = total_err - err_on_S

        # Gini coefficient of error magnitude
        err_abs = err.abs().sort()[0].float()
        n = len(err_abs)
        cumsum = err_abs.cumsum(0)
        gini = (2 * (torch.arange(1, n + 1).float() * err_abs).sum() / (n * cumsum[-1])) - (n + 1) / n

        # Estimated sparsity (fraction of near-zero entries)
        est_sparsity = (err_abs < 1e-3).float().mean().item() * 100

        results.append({
            'error_on_S_pct': err_on_S / total_err * 100,
            'error_on_Sbar_pct': err_on_Sbar / total_err * 100,
            'gini': gini.item(),
            'est_sparsity_pct': est_sparsity,
        })

    # Average over batch
    avg = {}
    for key in results[0]:
        vals = [r[key] for r in results]
        avg[key] = {'mean': float(np.mean(vals)), 'std': float(np.std(vals))}
    return avg


# ============================================================
# R1: ISTA Control Experiment
# ============================================================

def exp_ista_control(save_dir, device, seeds=5, num_test=500):
    """R1: ISTA control experiment for error concentration.
    Run standard ISTA (fixed thresholds, 20 iterations) and compute
    error sparsity metrics to compare with LISTA."""
    print("\n" + "=" * 60)
    print("R1: ISTA CONTROL EXPERIMENT FOR ERROR CONCENTRATION")
    print("=" * 60)

    N, K, L, pilot, snr = 64, 5, 20, 256, 20
    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Test data
        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=snr
        )

        # Train LISTA
        print("  Training LISTA...")
        lista = train_lista(LISTA(N, L), N, K, pilot, snr, epochs=200, device=device)
        lista.eval()
        with torch.no_grad():
            h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
        h_lista = h_lista.cpu()

        # OMP
        omp = OMPFilter(N, K)
        h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])

        # ISTA (fixed thresholds, 20 iterations)
        # Grid search threshold on a small validation set
        print("  Grid-searching ISTA threshold...")
        x_val, d_val, h_val = generate_sparse_channel_data(
            num_samples=200, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=snr
        )
        best_ista_thresh = 0.01
        best_ista_nmse = float('inf')
        for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
            ista = ISTAFilter(N, num_iterations=20, threshold=thresh)
            h_ista_val = torch.stack([ista.estimate(x_val[j], d_val[j]) for j in range(200)])
            nmse_val = compute_nmse_db(h_ista_val, h_val)
            if nmse_val < best_ista_nmse:
                best_ista_nmse = nmse_val
                best_ista_thresh = thresh
        print(f"  Best ISTA threshold: {best_ista_thresh} ({best_ista_nmse:.2f} dB)")

        ista = ISTAFilter(N, num_iterations=20, threshold=best_ista_thresh)
        h_ista = torch.stack([ista.estimate(x_test[i], d_test[i]) for i in range(num_test)])

        # NMSE
        nmse_lista = compute_nmse_db(h_lista, h_test)
        nmse_omp = compute_nmse_db(h_omp, h_test)
        nmse_ista = compute_nmse_db(h_ista, h_test)

        # Error sparsity
        sparsity_lista = compute_error_sparsity(h_lista, h_test, K)
        sparsity_omp = compute_error_sparsity(h_omp, h_test, K)
        sparsity_ista = compute_error_sparsity(h_ista, h_test, K)

        print(f"  NMSE: LISTA={nmse_lista:.2f}, OMP={nmse_omp:.2f}, ISTA={nmse_ista:.2f}")
        print(f"  Error on S%: LISTA={sparsity_lista['error_on_S_pct']['mean']:.1f}, "
              f"OMP={sparsity_omp['error_on_S_pct']['mean']:.1f}, "
              f"ISTA={sparsity_ista['error_on_S_pct']['mean']:.1f}")

        seed_data = {
            'nmse': {'LISTA': nmse_lista, 'OMP': nmse_omp, 'ISTA': nmse_ista},
            'sparsity': {'LISTA': sparsity_lista, 'OMP': sparsity_omp, 'ISTA': sparsity_ista},
            'ista_threshold': best_ista_thresh,
        }

        for method in ['LISTA', 'OMP', 'ISTA']:
            if method not in all_results:
                all_results[method] = {'nmse': [], 'error_on_S': [], 'error_on_Sbar': [], 'gini': []}
            all_results[method]['nmse'].append(seed_data['nmse'][method])
            all_results[method]['error_on_S'].append(seed_data['sparsity'][method]['error_on_S_pct']['mean'])
            all_results[method]['error_on_Sbar'].append(seed_data['sparsity'][method]['error_on_Sbar_pct']['mean'])
            all_results[method]['gini'].append(seed_data['sparsity'][method]['gini']['mean'])

    # Summary
    print("\n\n=== ISTA CONTROL EXPERIMENT RESULTS ===")
    summary = {}
    for method in ['LISTA', 'OMP', 'ISTA']:
        r = all_results[method]
        summary[method] = {
            'nmse_mean': float(np.mean(r['nmse'])),
            'nmse_std': float(np.std(r['nmse'])),
            'error_on_S_mean': float(np.mean(r['error_on_S'])),
            'error_on_S_std': float(np.std(r['error_on_S'])),
            'error_on_Sbar_mean': float(np.mean(r['error_on_Sbar'])),
            'error_on_Sbar_std': float(np.std(r['error_on_Sbar'])),
            'gini_mean': float(np.mean(r['gini'])),
            'gini_std': float(np.std(r['gini'])),
        }
        s = summary[method]
        print(f"  {method}: NMSE={s['nmse_mean']:.2f}±{s['nmse_std']:.2f} dB, "
              f"Error on S={s['error_on_S_mean']:.1f}±{s['error_on_S_std']:.1f}%, "
              f"Error on S̄={s['error_on_Sbar_mean']:.2f}±{s['error_on_Sbar_std']:.2f}%, "
              f"Gini={s['gini_mean']:.3f}±{s['gini_std']:.3f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'ista_control.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/ista_control.json")
    return summary


# ============================================================
# R2: FISTA Baseline
# ============================================================

def exp_fista_baseline(save_dir, device, seeds=5, num_test=200):
    """R2: Add FISTA as a baseline with L=20 iterations."""
    print("\n" + "=" * 60)
    print("R2: FISTA BASELINE EXPERIMENT")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    snr_values = [-5, 0, 5, 10, 15, 20, 25, 30, 40]

    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA (mixed SNR)
        print("  Training LISTA on mixed SNR [0, 30]...")
        lista = LISTA(N, L).to(device)
        optimizer = torch.optim.Adam(lista.parameters(), lr=1e-3, weight_decay=1e-5)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)
        for epoch in range(200):
            lista.train()
            snr_train = np.random.uniform(0, 30)
            x, d, h = generate_sparse_channel_data(
                num_samples=256, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr_train
            )
            x, d, h = x.to(device), d.to(device), h.to(device)
            h_est, _, _ = lista(x, d)
            loss = torch.mean((h_est - h) ** 2) / (torch.mean(h ** 2) + 1e-10)
            if torch.isnan(loss):
                continue
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(lista.parameters(), max_norm=5.0)
            optimizer.step()
            scheduler.step()
        lista.eval()

        # Grid search FISTA threshold on validation set
        if seed == 0:
            print("  Grid-searching FISTA hyperparameters...")
            x_val, d_val, h_val = generate_sparse_channel_data(
                num_samples=200, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=20
            )
            best_fista_thresh = 0.01
            best_fista_nmse = float('inf')
            for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
                fista = FISTAFilter(N, num_iterations=20, threshold=thresh)
                h_fista_val = torch.stack([fista.estimate(x_val[j], d_val[j]) for j in range(200)])
                nmse_val = compute_nmse_db(h_fista_val, h_val)
                if nmse_val < best_fista_nmse:
                    best_fista_nmse = nmse_val
                    best_fista_thresh = thresh
            print(f"  Best FISTA threshold: {best_fista_thresh} ({best_fista_nmse:.2f} dB)")

        for snr in snr_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
            )

            # LISTA
            with torch.no_grad():
                h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_lista.cpu(), h_test)

            # FISTA
            fista = FISTAFilter(N, num_iterations=20, threshold=best_fista_thresh)
            h_fista = torch.stack([fista.estimate(x_test[i], d_test[i]) for i in range(num_test)])
            nmse_fista = compute_nmse_db(h_fista, h_test)

            # Baselines (first seed only)
            if seed == 0:
                omp = OMPFilter(N, K)
                h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])
                nmse_omp = compute_nmse_db(h_omp, h_test)

                lasso = LASSOFilter(N, 0.01)
                h_lasso = torch.stack([lasso.estimate(x_test[i], d_test[i]) for i in range(num_test)])
                nmse_lasso = compute_nmse_db(h_lasso, h_test)

                all_results[snr] = {'OMP': nmse_omp, 'LASSO': nmse_lasso}

            if snr not in all_results:
                all_results[snr] = all_results.get(snr, {})
            if 'LISTA' not in all_results[snr]:
                all_results[snr]['LISTA'] = []
            if 'FISTA' not in all_results[snr]:
                all_results[snr]['FISTA'] = []
            all_results[snr]['LISTA'].append(nmse_lista)
            all_results[snr]['FISTA'].append(nmse_fista)

            print(f"    SNR={snr:>3}dB: LISTA={nmse_lista:.2f}, FISTA={nmse_fista:.2f}")

    # Summary
    print("\n\n=== FISTA BASELINE RESULTS ===")
    print(f"{'SNR':<6} {'OMP':<10} {'LASSO':<10} {'FISTA':<15} {'LISTA':<15}")
    print("-" * 56)
    summary = {}
    for snr in snr_values:
        r = all_results[snr]
        lista_mean = np.mean(r['LISTA'])
        lista_std = np.std(r['LISTA'])
        fista_mean = np.mean(r['FISTA'])
        fista_std = np.std(r['FISTA'])
        summary[str(snr)] = {
            'OMP': r['OMP'], 'LASSO': r['LASSO'],
            'FISTA_mean': float(fista_mean), 'FISTA_std': float(fista_std),
            'LISTA_mean': float(lista_mean), 'LISTA_std': float(lista_std),
        }
        print(f"{snr:<6} {r['OMP']:<10.2f} {r['LASSO']:<10.2f} "
              f"{fista_mean:.2f}±{fista_std:.2f}  {lista_mean:.2f}±{lista_std:.2f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'fista_baseline.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/fista_baseline.json")
    return summary


# ============================================================
# R4: Error Sparsity at K=10
# ============================================================

def exp_error_sparsity_k10(save_dir, device, seeds=5, num_test=500):
    """R4: Extend error sparsity analysis to K=10."""
    print("\n" + "=" * 60)
    print("R4: ERROR SPARSITY ANALYSIS AT K=10")
    print("=" * 60)

    N, L, pilot, snr = 64, 20, 256, 20
    K_values = [5, 10]
    all_results = {}

    for K in K_values:
        print(f"\n=== K={K} ===")
        all_results[K] = {}

        for seed in range(seeds):
            print(f"\n--- Seed {seed+1}/{seeds} ---")
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            # Test data
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
            )

            # Train LISTA on K=5 (default) -- use pretrained if K=5
            # For K=10, we still train on K=5 to test generalization
            train_K = 5
            print(f"  Training LISTA (train K={train_K}, test K={K})...")
            lista = train_lista(LISTA(N, L), N, train_K, pilot, snr, epochs=200, device=device)
            lista.eval()
            with torch.no_grad():
                h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
            h_lista = h_lista.cpu()

            # OMP (oracle K)
            omp = OMPFilter(N, K)
            h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])

            # ISTA (fixed thresholds, 20 iterations)
            ista = ISTAFilter(N, num_iterations=20, threshold=0.01)
            h_ista = torch.stack([ista.estimate(x_test[i], d_test[i]) for i in range(num_test)])

            # Error sparsity for each method
            for method, h_est in [('LISTA', h_lista), ('OMP', h_omp), ('ISTA', h_ista)]:
                sparsity = compute_error_sparsity(h_est, h_test, K)
                if method not in all_results[K]:
                    all_results[K][method] = {'error_on_S': [], 'error_on_Sbar': [], 'gini': []}
                all_results[K][method]['error_on_S'].append(sparsity['error_on_S_pct']['mean'])
                all_results[K][method]['error_on_Sbar'].append(sparsity['error_on_Sbar_pct']['mean'])
                all_results[K][method]['gini'].append(sparsity['gini']['mean'])

            nmse_lista = compute_nmse_db(h_lista, h_test)
            nmse_omp = compute_nmse_db(h_omp, h_test)
            nmse_ista = compute_nmse_db(h_ista, h_test)
            print(f"  NMSE: LISTA={nmse_lista:.2f}, OMP={nmse_omp:.2f}, ISTA={nmse_ista:.2f}")
            print(f"  Error on S%: LISTA={all_results[K]['LISTA']['error_on_S'][-1]:.1f}, "
                  f"OMP={all_results[K]['OMP']['error_on_S'][-1]:.1f}, "
                  f"ISTA={all_results[K]['ISTA']['error_on_S'][-1]:.1f}")

    # Summary
    print("\n\n=== ERROR SPARSITY RESULTS (K=5 and K=10) ===")
    summary = {}
    for K in K_values:
        summary[K] = {}
        for method in ['LISTA', 'OMP', 'ISTA']:
            r = all_results[K][method]
            summary[K][method] = {
                'error_on_S_mean': float(np.mean(r['error_on_S'])),
                'error_on_S_std': float(np.std(r['error_on_S'])),
                'error_on_Sbar_mean': float(np.mean(r['error_on_Sbar'])),
                'error_on_Sbar_std': float(np.std(r['error_on_Sbar'])),
                'gini_mean': float(np.mean(r['gini'])),
                'gini_std': float(np.std(r['gini'])),
            }
            s = summary[K][method]
            print(f"  K={K}, {method}: Error on S={s['error_on_S_mean']:.1f}±{s['error_on_S_std']:.1f}%, "
                  f"Error on S̄={s['error_on_Sbar_mean']:.2f}±{s['error_on_Sbar_std']:.2f}%, "
                  f"Gini={s['gini_mean']:.3f}±{s['gini_std']:.3f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'error_sparsity_extended.json'), 'w') as f:
        json.dump({str(k): v for k, v in summary.items()}, f, indent=2)
    print(f"\nSaved to {save_dir}/error_sparsity_extended.json")
    return summary


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Round 14 experiments')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['ista_control', 'fista', 'error_sparsity', 'all'])
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--seeds', type=int, default=5)
    parser.add_argument('--num_test', type=int, default=500)
    parser.add_argument('--save_dir', type=str, default='results/round14')
    args = parser.parse_args()

    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Seeds: {args.seeds}")

    os.makedirs(args.save_dir, exist_ok=True)

    if args.experiment in ['ista_control', 'all']:
        exp_ista_control(args.save_dir, device, args.seeds, args.num_test)

    if args.experiment in ['fista', 'all']:
        exp_fista_baseline(args.save_dir, device, args.seeds, min(args.num_test, 200))

    if args.experiment in ['error_sparsity', 'all']:
        exp_error_sparsity_k10(args.save_dir, device, args.seeds, args.num_test)

    print("\n\n" + "=" * 60)
    print("ROUND 14 EXPERIMENTS COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
