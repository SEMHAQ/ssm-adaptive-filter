"""
Round 15 experiments: address all 3 required reviewer fixes.

R1: (Paper only - AMP theory discussion, no experiment needed)
R2: Pilot ratio experiment (M in {96, 128, 192, 256} for N=64)
R3: Mechanism analysis with 5 seeds for uncertainty quantification

Usage:
    cd code
    python run_round15_experiments.py --experiment all --device cuda --seeds 5
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


def train_lista(model, N, K, pilot, snr, epochs=200, batch_size=256, device='cpu', mixed_snr=True):
    """Train LISTA model. If mixed_snr=True, use random SNR in [0, 30] per batch (paper protocol).
    If mixed_snr=False, use fixed snr parameter."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    for epoch in range(epochs):
        model.train()
        if mixed_snr:
            snr_train = np.random.uniform(0, 30)
        else:
            snr_train = snr
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


def compute_error_sparsity(h_est, h_true, K):
    """Compute error concentration metrics for a batch of estimates."""
    batch = h_est.shape[0]
    N = h_est.shape[1]
    _, true_support = torch.topk(h_true.abs(), K, dim=1)

    results = []
    for i in range(batch):
        err = h_est[i] - h_true[i]
        err_energy = err ** 2
        total_err = err_energy.sum().item() + 1e-20

        S = true_support[i]
        err_on_S = err_energy[S].sum().item()
        err_on_Sbar = total_err - err_on_S

        err_abs = err.abs().sort()[0].float()
        n = len(err_abs)
        cumsum = err_abs.cumsum(0)
        gini = (2 * (torch.arange(1, n + 1).float() * err_abs).sum() / (n * cumsum[-1])) - (n + 1) / n

        results.append({
            'error_on_S_pct': err_on_S / total_err * 100,
            'error_on_Sbar_pct': err_on_Sbar / total_err * 100,
            'gini': gini.item(),
        })

    avg = {}
    for key in results[0]:
        vals = [r[key] for r in results]
        avg[key] = {'mean': float(np.mean(vals)), 'std': float(np.std(vals))}
    return avg


def compute_support_recovery(h_est, h_true, K):
    """Compute Jaccard index, precision, recall for support recovery."""
    batch = h_est.shape[0]
    _, true_support = torch.topk(h_true.abs(), K, dim=1)
    _, est_support = torch.topk(h_est.abs(), K, dim=1)

    jaccards, precisions, recalls = [], [], []
    for i in range(batch):
        S_true = set(true_support[i].tolist())
        S_est = set(est_support[i].tolist())
        intersection = len(S_true & S_est)
        union = len(S_true | S_est)
        jaccard = intersection / union if union > 0 else 0
        precision = intersection / K if K > 0 else 0
        recall = intersection / K if K > 0 else 0
        jaccards.append(jaccard)
        precisions.append(precision)
        recalls.append(recall)

    return {
        'jaccard': {'mean': float(np.mean(jaccards)), 'std': float(np.std(jaccards))},
        'precision': {'mean': float(np.mean(precisions)), 'std': float(np.std(precisions))},
        'recall': {'mean': float(np.mean(recalls)), 'std': float(np.std(recalls))},
    }


# ============================================================
# R2: Pilot Ratio Experiment
# ============================================================

def exp_pilot_ratio(save_dir, device, seeds=5, num_test=200):
    """R2: Vary pilot ratio M/N for N=64.
    M in {96, 128, 192, 256} giving ratios {1.5, 2.0, 3.0, 4.0}.
    """
    print("\n" + "=" * 60)
    print("R2: PILOT RATIO EXPERIMENT (varying M/N)")
    print("=" * 60)

    N, K, L, snr = 64, 5, 20, 20
    M_values = [96, 128, 192, 256]
    ratios = {M: M / N for M in M_values}

    all_results = {}

    for seed in range(seeds):
        print(f"\n--- Seed {seed+1}/{seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        for M in M_values:
            ratio = ratios[M]
            print(f"\n  M={M} (M/N={ratio:.1f})")

            # Train LISTA with this pilot length
            print(f"    Training LISTA...")
            lista = train_lista(LISTA(N, L), N, K, M, snr, epochs=200, device=device)
            lista.eval()

            # Test data
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=M, snr_db=snr
            )

            # LISTA
            with torch.no_grad():
                h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
            h_lista = h_lista.cpu()
            nmse_lista = compute_nmse_db(h_lista, h_test)

            # Baselines (first seed only for OMP/LASSO/LMS/NLMS to save time)
            if seed == 0:
                omp = OMPFilter(N, K)
                h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])
                nmse_omp = compute_nmse_db(h_omp, h_test)

                # LASSO grid search
                best_lasso_nmse = float('inf')
                for lam in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5]:
                    lasso = LASSOFilter(N, lam)
                    h_lasso = torch.stack([lasso.estimate(x_test[j], d_test[j]) for j in range(num_test)])
                    nmse_l = compute_nmse_db(h_lasso, h_test)
                    if nmse_l < best_lasso_nmse:
                        best_lasso_nmse = nmse_l

                # FISTA
                best_fista_nmse = float('inf')
                for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
                    fista = FISTAFilter(N, num_iterations=20, threshold=thresh)
                    h_fista = torch.stack([fista.estimate(x_test[j], d_test[j]) for j in range(num_test)])
                    nmse_f = compute_nmse_db(h_fista, h_test)
                    if nmse_f < best_fista_nmse:
                        best_fista_nmse = nmse_f

                all_results[M] = {
                    'OMP': nmse_omp,
                    'LASSO': best_lasso_nmse,
                    'FISTA': best_fista_nmse,
                    'LISTA': [],
                }

            if M not in all_results:
                all_results[M] = {'LISTA': []}
            all_results[M]['LISTA'].append(nmse_lista)

            print(f"    NMSE: LISTA={nmse_lista:.2f} dB")
            if seed == 0:
                print(f"    NMSE: OMP={all_results[M]['OMP']:.2f}, "
                      f"LASSO={all_results[M]['LASSO']:.2f}, "
                      f"FISTA={all_results[M]['FISTA']:.2f}")

    # Summary
    print("\n\n=== PILOT RATIO RESULTS ===")
    print(f"{'M':<6} {'M/N':<6} {'OMP':<10} {'LASSO':<10} {'FISTA':<10} {'LISTA':<20}")
    print("-" * 62)
    summary = {}
    for M in M_values:
        r = all_results[M]
        lista_mean = np.mean(r['LISTA'])
        lista_std = np.std(r['LISTA'])
        summary[str(M)] = {
            'ratio': ratios[M],
            'OMP': r.get('OMP', None),
            'LASSO': r.get('LASSO', None),
            'FISTA': r.get('FISTA', None),
            'LISTA_mean': float(lista_mean),
            'LISTA_std': float(lista_std),
            'LISTA_seeds': [float(v) for v in r['LISTA']],
        }
        omp_str = f"{r['OMP']:.2f}" if 'OMP' in r else '---'
        lasso_str = f"{r['LASSO']:.2f}" if 'LASSO' in r else '---'
        fista_str = f"{r['FISTA']:.2f}" if 'FISTA' in r else '---'
        print(f"{M:<6} {ratios[M]:<6.1f} {omp_str:<10} {lasso_str:<10} {fista_str:<10} "
              f"{lista_mean:.2f}±{lista_std:.2f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'pilot_ratio.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved to {save_dir}/pilot_ratio.json")
    return summary


# ============================================================
# R3: Mechanism Analysis with 5 seeds (uncertainty quantification)
# ============================================================

def exp_mechanism_5seeds(save_dir, device, seeds=5, num_test=500):
    """R3: Re-run mechanism analysis with 5 seeds to get mean±std.
    Covers: support recovery, error sparsity, ISTA control, extended sparsity.
    """
    print("\n" + "=" * 60)
    print("R3: MECHANISM ANALYSIS WITH 5 SEEDS (uncertainty quantification)")
    print("=" * 60)

    N, K, L, pilot = 64, 5, 20, 256
    snr_values = [10, 20, 30]

    # ---- Part A: Support recovery + Error sparsity at multiple SNRs ----
    print("\n--- Part A: Support Recovery + Error Sparsity ---")
    support_results = {snr: {m: {'jaccard': [], 'precision': [], 'recall': []}
                            for m in ['LISTA', 'OMP']} for snr in snr_values}
    sparsity_results = {snr: {m: {'error_on_S': [], 'error_on_Sbar': [], 'gini': []}
                              for m in ['LISTA', 'OMP']} for snr in snr_values}

    for seed in range(seeds):
        print(f"\n  Seed {seed+1}/{seeds}")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA once per seed
        print("    Training LISTA...")
        lista = train_lista(LISTA(N, L), N, K, pilot, 20, epochs=200, device=device)
        lista.eval()

        for snr in snr_values:
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=snr
            )

            # LISTA
            with torch.no_grad():
                h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
            h_lista = h_lista.cpu()

            # OMP
            omp = OMPFilter(N, K)
            h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])

            for method, h_est in [('LISTA', h_lista), ('OMP', h_omp)]:
                # Support recovery
                sr = compute_support_recovery(h_est, h_test, K)
                for metric in ['jaccard', 'precision', 'recall']:
                    support_results[snr][method][metric].append(sr[metric]['mean'])

                # Error sparsity
                es = compute_error_sparsity(h_est, h_test, K)
                sparsity_results[snr][method]['error_on_S'].append(es['error_on_S_pct']['mean'])
                sparsity_results[snr][method]['error_on_Sbar'].append(es['error_on_Sbar_pct']['mean'])
                sparsity_results[snr][method]['gini'].append(es['gini']['mean'])

            print(f"    SNR={snr}: LISTA error_on_S={sparsity_results[snr]['LISTA']['error_on_S'][-1]:.1f}%, "
                  f"OMP error_on_S={sparsity_results[snr]['OMP']['error_on_S'][-1]:.1f}%")

    # ---- Part B: ISTA control at SNR=20 ----
    print("\n--- Part B: ISTA Control Experiment (SNR=20) ---")
    ista_results = {m: {'error_on_S': [], 'error_on_Sbar': [], 'gini': [], 'nmse': []}
                    for m in ['LISTA', 'OMP', 'ISTA']}

    for seed in range(seeds):
        print(f"\n  Seed {seed+1}/{seeds}")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        x_test, d_test, h_test = generate_sparse_channel_data(
            num_samples=num_test, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=20
        )

        # Train LISTA
        lista = train_lista(LISTA(N, L), N, K, pilot, 20, epochs=200, device=device)
        lista.eval()
        with torch.no_grad():
            h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
        h_lista = h_lista.cpu()

        # OMP
        omp = OMPFilter(N, K)
        h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])

        # ISTA (grid search threshold)
        x_val, d_val, h_val = generate_sparse_channel_data(
            num_samples=200, channel_length=N, sparsity=K,
            pilot_length=pilot, snr_db=20
        )
        best_thresh = 0.01
        best_nmse = float('inf')
        for thresh in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
            ista = ISTAFilter(N, num_iterations=20, threshold=thresh)
            h_val_est = torch.stack([ista.estimate(x_val[j], d_val[j]) for j in range(200)])
            nmse_val = compute_nmse_db(h_val_est, h_val)
            if nmse_val < best_nmse:
                best_nmse = nmse_val
                best_thresh = thresh

        ista = ISTAFilter(N, num_iterations=20, threshold=best_thresh)
        h_ista = torch.stack([ista.estimate(x_test[i], d_test[i]) for i in range(num_test)])

        for method, h_est in [('LISTA', h_lista), ('OMP', h_omp), ('ISTA', h_ista)]:
            nmse = compute_nmse_db(h_est, h_test)
            es = compute_error_sparsity(h_est, h_test, K)
            ista_results[method]['nmse'].append(nmse)
            ista_results[method]['error_on_S'].append(es['error_on_S_pct']['mean'])
            ista_results[method]['error_on_Sbar'].append(es['error_on_Sbar_pct']['mean'])
            ista_results[method]['gini'].append(es['gini']['mean'])

        print(f"    LISTA NMSE={ista_results['LISTA']['nmse'][-1]:.2f}, "
              f"OMP NMSE={ista_results['OMP']['nmse'][-1]:.2f}, "
              f"ISTA NMSE={ista_results['ISTA']['nmse'][-1]:.2f}")

    # ---- Part C: Extended sparsity (K=5 and K=10) ----
    print("\n--- Part C: Extended Error Sparsity (K=5 and K=10) ---")
    K_values = [5, 10]
    extended_results = {K: {m: {'error_on_S': [], 'error_on_Sbar': [], 'gini': [], 'nmse': []}
                           for m in ['LISTA', 'OMP', 'ISTA']} for K in K_values}

    for K in K_values:
        print(f"\n  K={K}")
        for seed in range(seeds):
            print(f"    Seed {seed+1}/{seeds}")
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=pilot, snr_db=20
            )

            # Train LISTA on K=5 (always)
            lista = train_lista(LISTA(N, L), N, 5, pilot, 20, epochs=200, device=device)
            lista.eval()
            with torch.no_grad():
                h_lista, _, _ = lista(x_test.to(device), d_test.to(device))
            h_lista = h_lista.cpu()

            omp = OMPFilter(N, K)
            h_omp = torch.stack([omp.estimate(x_test[i], d_test[i]) for i in range(num_test)])

            ista = ISTAFilter(N, num_iterations=20, threshold=0.01)
            h_ista = torch.stack([ista.estimate(x_test[i], d_test[i]) for i in range(num_test)])

            for method, h_est in [('LISTA', h_lista), ('OMP', h_omp), ('ISTA', h_ista)]:
                nmse = compute_nmse_db(h_est, h_test)
                es = compute_error_sparsity(h_est, h_test, K)
                extended_results[K][method]['nmse'].append(nmse)
                extended_results[K][method]['error_on_S'].append(es['error_on_S_pct']['mean'])
                extended_results[K][method]['error_on_Sbar'].append(es['error_on_Sbar_pct']['mean'])
                extended_results[K][method]['gini'].append(es['gini']['mean'])

            print(f"      LISTA error_on_S={extended_results[K]['LISTA']['error_on_S'][-1]:.1f}%, "
                  f"OMP error_on_S={extended_results[K]['OMP']['error_on_S'][-1]:.1f}%")

    # ---- Compile and save all results ----
    def stats(vals):
        return {'mean': float(np.mean(vals)), 'std': float(np.std(vals)),
                'seeds': [float(v) for v in vals]}

    final = {
        'config': {'N': N, 'K': K, 'L': L, 'pilot': pilot, 'seeds': seeds, 'num_test': num_test},
        'support_recovery': {},
        'error_sparsity': {},
        'ista_control': {},
        'extended_sparsity': {},
    }

    # Support recovery
    for snr in snr_values:
        final['support_recovery'][str(snr)] = {}
        for method in ['LISTA', 'OMP']:
            final['support_recovery'][str(snr)][method] = {
                metric: stats(support_results[snr][method][metric])
                for metric in ['jaccard', 'precision', 'recall']
            }

    # Error sparsity
    for snr in snr_values:
        final['error_sparsity'][str(snr)] = {}
        for method in ['LISTA', 'OMP']:
            final['error_sparsity'][str(snr)][method] = {
                metric: stats(sparsity_results[snr][method][metric])
                for metric in ['error_on_S', 'error_on_Sbar', 'gini']
            }

    # ISTA control
    for method in ['LISTA', 'OMP', 'ISTA']:
        final['ista_control'][method] = {
            metric: stats(ista_results[method][metric])
            for metric in ['nmse', 'error_on_S', 'error_on_Sbar', 'gini']
        }

    # Extended sparsity
    for K in K_values:
        final['extended_sparsity'][str(K)] = {}
        for method in ['LISTA', 'OMP', 'ISTA']:
            final['extended_sparsity'][str(K)][method] = {
                metric: stats(extended_results[K][method][metric])
                for metric in ['nmse', 'error_on_S', 'error_on_Sbar', 'gini']
            }

    # Print summary
    print("\n\n=== MECHANISM ANALYSIS SUMMARY (mean ± std over {} seeds) ===".format(seeds))

    print("\n--- Support Recovery ---")
    for snr in snr_values:
        for method in ['LISTA', 'OMP']:
            j = final['support_recovery'][str(snr)][method]['jaccard']
            p = final['support_recovery'][str(snr)][method]['precision']
            r = final['support_recovery'][str(snr)][method]['recall']
            print(f"  SNR={snr}, {method}: J={j['mean']:.3f}±{j['std']:.3f}, "
                  f"P={p['mean']:.3f}±{p['std']:.3f}, R={r['mean']:.3f}±{r['std']:.3f}")

    print("\n--- Error Sparsity ---")
    for snr in snr_values:
        for method in ['LISTA', 'OMP']:
            es = final['error_sparsity'][str(snr)][method]['error_on_S']
            esb = final['error_sparsity'][str(snr)][method]['error_on_Sbar']
            g = final['error_sparsity'][str(snr)][method]['gini']
            print(f"  SNR={snr}, {method}: Error on S={es['mean']:.1f}±{es['std']:.1f}%, "
                  f"Error on S̄={esb['mean']:.2f}±{esb['std']:.2f}%, "
                  f"Gini={g['mean']:.3f}±{g['std']:.3f}")

    print("\n--- ISTA Control (SNR=20) ---")
    for method in ['LISTA', 'OMP', 'ISTA']:
        m = final['ista_control'][method]
        print(f"  {method}: NMSE={m['nmse']['mean']:.2f}±{m['nmse']['std']:.2f}, "
              f"Error on S={m['error_on_S']['mean']:.1f}±{m['error_on_S']['std']:.1f}%, "
              f"Error on S̄={m['error_on_Sbar']['mean']:.2f}±{m['error_on_Sbar']['std']:.2f}%, "
              f"Gini={m['gini']['mean']:.3f}±{m['gini']['std']:.3f}")

    print("\n--- Extended Sparsity ---")
    for K in K_values:
        for method in ['LISTA', 'OMP', 'ISTA']:
            m = final['extended_sparsity'][str(K)][method]
            print(f"  K={K}, {method}: NMSE={m['nmse']['mean']:.2f}±{m['nmse']['std']:.2f}, "
                  f"Error on S={m['error_on_S']['mean']:.1f}±{m['error_on_S']['std']:.1f}%, "
                  f"Gini={m['gini']['mean']:.3f}±{m['gini']['std']:.3f}")

    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, 'mechanism_5seeds.json'), 'w') as f:
        json.dump(final, f, indent=2)
    print(f"\nSaved to {save_dir}/mechanism_5seeds.json")
    return final


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Round 15 experiments')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['pilot_ratio', 'mechanism', 'all'])
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--seeds', type=int, default=5)
    parser.add_argument('--num_test', type=int, default=500)
    parser.add_argument('--save_dir', type=str, default='results/round15')
    args = parser.parse_args()

    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Seeds: {args.seeds}")

    os.makedirs(args.save_dir, exist_ok=True)

    if args.experiment in ['pilot_ratio', 'all']:
        exp_pilot_ratio(args.save_dir, device, args.seeds, min(args.num_test, 200))

    if args.experiment in ['mechanism', 'all']:
        exp_mechanism_5seeds(args.save_dir, device, args.seeds, args.num_test)

    print("\n\n" + "=" * 60)
    print("ROUND 15 EXPERIMENTS COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
