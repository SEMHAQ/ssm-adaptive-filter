"""
Round 6 revision experiments addressing Round 5 reviewer feedback.

Addresses all 5 required revisions:
- R1 (Critical): Re-run QPSK BER with 5 seeds (was 3, inconsistent with 16-QAM's 5)
- R2 (Major): Verify LISTA-CP implementation with actual weight clipping enforcement
- R3 (Major): Full MMSE SNR sweep with 5 seeds and 7 SNR points
- R4 (Major): Qualify BER advantage as ZF-specific in paper text
- R5 (Major): Add baseline error bars and p-values to NMSE tables

Usage:
    cd code
    python run_round6_experiments.py --experiment all --seeds 5 --device cuda
"""

import argparse
import json
import os
import sys
import time

import numpy as np
import torch
from scipy import stats

sys.path.insert(0, os.path.dirname(__file__))
from data.generate import generate_sparse_channel_data
from models.ssm_af import LISTA, LISTALayer, OMPFilter, LASSOFilter
from run_round2_experiments import train_lista_consistent, LISTACP, evaluate_baselines
from run_revision_experiments import compute_nmse_db
from run_round4_experiments import (
    compute_ber_zf, compute_ber_mmse, compute_support_recovery,
    compute_error_sparsity, compute_noise_enhancement,
    modulate_qpsk, modulate_16qam,
)


# ============================================================
# R2: LISTA-CP with proper weight clipping enforcement
# ============================================================

class LISTACPCorrectedLayer(torch.nn.Module):
    """LISTA-CP layer with enforced weight clipping ||W - I||_2 < 1."""
    def __init__(self, channel_length, init_step=0.5, init_threshold=0.001):
        super().__init__()
        self.step = torch.nn.Parameter(torch.tensor(init_step))
        self.threshold = torch.nn.Parameter(torch.tensor(init_threshold))
        self.W = torch.nn.Linear(channel_length, channel_length, bias=False)
        torch.nn.init.eye_(self.W.weight)

    def clip_weights(self):
        """Enforce ||W - I||_2 < 1 by spectral norm clipping."""
        with torch.no_grad():
            N = self.W.weight.shape[0]
            W_I = self.W.weight - torch.eye(N, device=self.W.weight.device)
            # Compute spectral norm via power iteration
            u = torch.randn(N, 1, device=self.W.weight.device)
            for _ in range(10):
                v = W_I.T @ u
                v = v / (v.norm() + 1e-10)
                u = W_I @ v
                u = u / (u.norm() + 1e-10)
            spectral_norm = (u.T @ W_I @ v).item()
            # Clip if spectral norm >= 1
            if abs(spectral_norm) >= 1.0:
                scale = 0.99 / (abs(spectral_norm) + 1e-10)
                W_I_clipped = W_I * scale
                self.W.weight.copy_(W_I_clipped + torch.eye(N, device=self.W.weight.device))
                return True  # clipping was applied
        return False  # no clipping needed

    def forward(self, h, grad):
        h_new = self.W(h) - self.step * grad
        return torch.sign(h_new) * torch.relu(torch.abs(h_new) - self.threshold)


class LISTACPCorrected(torch.nn.Module):
    """LISTA-CP with enforced weight clipping during training."""
    def __init__(self, channel_length, num_layers=20, init_step=0.5, init_threshold=0.001):
        super().__init__()
        self.channel_length = channel_length
        self.num_layers = num_layers
        self.layers = torch.nn.ModuleList([
            LISTACPCorrectedLayer(channel_length, init_step, init_threshold)
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

    def clip_all_weights(self):
        """Clip weights in all layers. Returns count of clipped layers."""
        clipped = 0
        for layer in self.layers:
            if layer.clip_weights():
                clipped += 1
        return clipped


def train_lista_cp_corrected(model, N, K, M, snr_range=(0, 30), epochs=200, device='cuda'):
    """Train LISTA-CP with weight clipping enforced after each optimizer step."""
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = torch.nn.MSELoss()

    clipping_log = []  # Track clipping activations per epoch

    for epoch in range(epochs):
        snr = np.random.uniform(snr_range[0], snr_range[1])
        x_batch, d_batch, h_batch = generate_sparse_channel_data(
            num_samples=256, channel_length=N, sparsity=K,
            pilot_length=M, snr_db=snr
        )
        x_batch = x_batch.to(device)
        d_batch = d_batch.to(device)
        h_batch = h_batch.to(device)

        model.train()
        optimizer.zero_grad()
        h_est, d_recon, e = model(x_batch, d_batch)
        loss = criterion(h_est, h_batch) / (torch.mean(h_batch ** 2) + 1e-10)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()

        # Enforce weight clipping after optimizer step
        clipped = model.clip_all_weights()
        clipping_log.append({'epoch': epoch, 'layers_clipped': clipped})

        scheduler.step()

    return model, clipping_log


def exp_lista_cp_verification(args):
    """
    R2: Verify LISTA-CP implementation.

    Trains LISTA and LISTA-CP with proper weight clipping enforcement.
    Reports per-layer spectral norms, clipping activations, and NMSE comparison.
    """
    print("\n" + "=" * 60)
    print("Experiment R2: LISTA-CP Verification")
    print("=" * 60)

    device = args.device
    N, M, K, L = 64, 256, 5, 20
    snr_levels = [0, 10, 20, 30]
    num_seeds = args.seeds
    num_test = 200

    results = {
        'config': {'N': N, 'M': M, 'K': K, 'L': L, 'num_seeds': num_seeds, 'num_test': num_test},
        'comparison': {},
        'diagnostics': [],
    }

    lista_nmses = {snr: [] for snr in snr_levels}
    cp_nmses = {snr: [] for snr in snr_levels}

    for seed in range(num_seeds):
        print(f"\n--- Seed {seed+1}/{num_seeds} ---")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA
        print("  Training LISTA...")
        model_lista = train_lista_consistent(LISTA(N, L), N, K, M,
                                              snr_range=(0, 30), epochs=200, device=device)
        model_lista.eval()

        # Train LISTA-CP with proper clipping
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)
        print("  Training LISTA-CP (with weight clipping)...")
        model_cp, clip_log = train_lista_cp_corrected(
            LISTACPCorrected(N, L), N, K, M,
            snr_range=(0, 30), epochs=200, device=device
        )
        model_cp.eval()

        # Count total clipping activations
        total_clips = sum(1 for entry in clip_log if entry['layers_clipped'] > 0)
        print(f"  Clipping activated in {total_clips}/{len(clip_log)} epochs")

        # Per-layer spectral norms
        spectral_norms = []
        for layer_idx, layer in enumerate(model_cp.layers):
            with torch.no_grad():
                W_I = layer.W.weight - torch.eye(N, device=device)
                s = torch.linalg.svdvals(W_I)
                spectral_norms.append({
                    'layer': layer_idx,
                    'spectral_norm_W_minus_I': float(s[0].item()),
                })

        results['diagnostics'].append({
            'seed': seed,
            'clipping_epochs': total_clips,
            'spectral_norms': spectral_norms,
        })

        for test_snr in snr_levels:
            torch.manual_seed(seed + 1000)
            np.random.seed(seed + 1000)
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=M, snr_db=test_snr
            )

            with torch.no_grad():
                h_lista, _, _ = model_lista(x_test.to(device), d_test.to(device))
                h_cp, _, _ = model_cp(x_test.to(device), d_test.to(device))

            nmse_lista = compute_nmse_db(h_lista.cpu(), h_test)
            nmse_cp = compute_nmse_db(h_cp.cpu(), h_test)
            lista_nmses[test_snr].append(nmse_lista)
            cp_nmses[test_snr].append(nmse_cp)

            print(f"    SNR={test_snr}: LISTA={nmse_lista:.2f}, LISTA-CP={nmse_cp:.2f}")

    for snr in snr_levels:
        snr_key = str(snr)
        lista_vals = lista_nmses[snr]
        cp_vals = cp_nmses[snr]

        # Paired t-test
        t_stat, p_val = stats.ttest_rel(lista_vals, cp_vals)
        diff = np.array(lista_vals) - np.array(cp_vals)

        results['comparison'][snr_key] = {
            'lista_mean': float(np.mean(lista_vals)),
            'lista_std': float(np.std(lista_vals)),
            'lista_cp_mean': float(np.mean(cp_vals)),
            'lista_cp_std': float(np.std(cp_vals)),
            'mean_diff': float(np.mean(diff)),
            'max_abs_diff': float(np.max(np.abs(diff))),
            't_statistic': float(t_stat),
            'p_value': float(p_val),
            'significant_005': bool(p_val < 0.05),
        }

    # Save
    save_path = os.path.join(args.save_dir, 'lista_cp_verification.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR2 LISTA-CP verification saved to {save_path}")
    return results


# ============================================================
# R1+R3+R5 Combined: BER and NMSE with 5 seeds
# ============================================================

def exp_ber_5seeds(args):
    """
    R1: Re-run QPSK and 16-QAM BER with 5 seeds consistently.

    Previously QPSK used 3 seeds while 16-QAM used 5.
    Now both use 5 seeds with 200 realizations per point.
    """
    print("\n" + "=" * 60)
    print("Experiment R1: BER with 5 seeds (QPSK + 16-QAM)")
    print("=" * 60)

    device = args.device
    N, M, K, L = 64, 256, 5, 20
    snr_levels = [0, 5, 10, 15, 20, 25, 30]
    modulations = ['qpsk', '16qam']
    num_test = 200
    num_symbols = 50000
    num_seeds = 5  # Fixed to 5

    results = {
        'config': {
            'N': N, 'M': M, 'K': K, 'L': L,
            'num_test': num_test, 'num_symbols': num_symbols,
            'snr_levels': snr_levels, 'modulations': modulations,
            'num_seeds': num_seeds,
            'note': 'Rerun with 5 seeds for both QPSK and 16-QAM (was 3 for QPSK)',
        },
        'ber': {}
    }

    # Train LISTA models
    print("\nTraining LISTA models...")
    lista_models = []
    for seed in range(num_seeds):
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)
        model = LISTA(channel_length=N, num_layers=L)
        model = train_lista_consistent(model, N, K, M, snr_range=(0, 30),
                                        epochs=200, device=device)
        lista_models.append(model)

    for mod in modulations:
        print(f"\n--- {mod.upper()} BER (ZF, 5 seeds) ---")
        results['ber'][mod] = {}

        for snr in snr_levels:
            print(f"\n  SNR = {snr} dB ({num_test} realizations, {num_seeds} seeds):")
            ber_lista_seeds = []
            ber_omp_seeds = []
            ber_lasso_seeds = []

            for seed in range(num_seeds):
                torch.manual_seed(seed + 1000)
                np.random.seed(seed + 1000)

                ber_lista_realizations = []
                ber_omp_realizations = []
                ber_lasso_realizations = []

                for t in range(num_test):
                    x_batch, d_batch, h_batch = generate_sparse_channel_data(
                        num_samples=1, channel_length=N, sparsity=K,
                        pilot_length=M, snr_db=snr
                    )
                    h_true = h_batch.squeeze(0).numpy()

                    # LISTA
                    model = lista_models[seed]
                    model.eval()
                    with torch.no_grad():
                        h_lista, _, _ = model(x_batch.to(device), d_batch.to(device))
                    h_lista_np = h_lista.squeeze(0).cpu().numpy()

                    # OMP
                    omp = OMPFilter(channel_length=N, sparsity=K)
                    h_omp = omp.estimate(x_batch.squeeze(0), d_batch.squeeze(0)).numpy()

                    # LASSO
                    lasso = LASSOFilter(channel_length=N, lam=0.01)
                    h_lasso = lasso.estimate(x_batch.squeeze(0), d_batch.squeeze(0)).numpy()

                    ber_lista_realizations.append(compute_ber_zf(h_true, h_lista_np, snr, mod, num_symbols))
                    ber_omp_realizations.append(compute_ber_zf(h_true, h_omp, snr, mod, num_symbols))
                    ber_lasso_realizations.append(compute_ber_zf(h_true, h_lasso, snr, mod, num_symbols))

                ber_lista_seeds.append(np.mean(ber_lista_realizations))
                ber_omp_seeds.append(np.mean(ber_omp_realizations))
                ber_lasso_seeds.append(np.mean(ber_lasso_realizations))

            # Statistics
            lista_mean = np.mean(ber_lista_seeds)
            lista_std = np.std(ber_lista_seeds)
            omp_mean = np.mean(ber_omp_seeds)
            omp_std = np.std(ber_omp_seeds)
            lasso_mean = np.mean(ber_lasso_seeds)
            lasso_std = np.std(ber_lasso_seeds)

            t_crit = stats.t.ppf(0.975, num_seeds - 1)
            lista_ci = t_crit * lista_std / np.sqrt(num_seeds)
            omp_ci = t_crit * omp_std / np.sqrt(num_seeds)

            # Paired t-test: LISTA vs OMP
            t_stat_lo, p_val_lo = stats.ttest_rel(ber_lista_seeds, ber_omp_seeds)
            t_stat_ll, p_val_ll = stats.ttest_rel(ber_lista_seeds, ber_lasso_seeds)

            diff_lo = np.array(ber_lista_seeds) - np.array(ber_omp_seeds)
            cohens_d_lo = np.mean(diff_lo) / (np.std(diff_lo, ddof=1) + 1e-10)

            results['ber'][mod][str(snr)] = {
                'lista': {
                    'mean': float(lista_mean), 'std': float(lista_std),
                    'ci_95': float(lista_ci),
                    'seeds': [float(x) for x in ber_lista_seeds]
                },
                'omp': {
                    'mean': float(omp_mean), 'std': float(omp_std),
                    'ci_95': float(omp_ci),
                    'seeds': [float(x) for x in ber_omp_seeds]
                },
                'lasso': {
                    'mean': float(lasso_mean), 'std': float(lasso_std),
                    'ci_95': float(t_crit * lasso_std / np.sqrt(num_seeds)),
                    'seeds': [float(x) for x in ber_lasso_seeds]
                },
                'lista_vs_omp': {
                    't_statistic': float(t_stat_lo),
                    'p_value': float(p_val_lo),
                    'cohens_d': float(cohens_d_lo),
                    'significant_005': bool(p_val_lo < 0.05),
                    'significant_001': bool(p_val_lo < 0.01),
                },
                'lista_vs_lasso': {
                    't_statistic': float(t_stat_ll),
                    'p_value': float(p_val_ll),
                    'significant_005': bool(p_val_ll < 0.05),
                },
            }

            sig_mark = '**' if p_val_lo < 0.01 else ('*' if p_val_lo < 0.05 else 'ns')
            print(f"    LISTA: {lista_mean:.6f} ± {lista_std:.6f}")
            print(f"    OMP:   {omp_mean:.6f} ± {omp_std:.6f}")
            print(f"    LASSO: {lasso_mean:.6f} ± {lasso_std:.6f}")
            print(f"    LISTA vs OMP: p={p_val_lo:.4f} {sig_mark}, d={cohens_d_lo:.3f}")

    save_path = os.path.join(args.save_dir, 'ber_5seeds.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR1 BER 5-seed results saved to {save_path}")
    return results


def exp_mmse_full_sweep(args):
    """
    R3: Full MMSE SNR sweep with 5 seeds.

    Previously used 3 seeds and only showed 2 SNR points in paper.
    Now 5 seeds, 7 SNR points, both QPSK and 16-QAM, both ZF and MMSE.
    """
    print("\n" + "=" * 60)
    print("Experiment R3: MMSE Full SNR Sweep (5 seeds)")
    print("=" * 60)

    device = args.device
    N, M, K, L = 64, 256, 5, 20
    snr_levels = [0, 5, 10, 15, 20, 25, 30]
    modulations = ['qpsk', '16qam']
    num_test = 200
    num_symbols = 50000
    num_seeds = 5

    results = {
        'config': {
            'N': N, 'M': M, 'K': K, 'L': L,
            'num_test': num_test, 'num_symbols': num_symbols,
            'snr_levels': snr_levels, 'modulations': modulations,
            'num_seeds': num_seeds,
        },
        'ber_mmse': {},
        'ber_zf': {},
    }

    # Train LISTA
    print("\nTraining LISTA models...")
    lista_models = []
    for seed in range(num_seeds):
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)
        model = LISTA(channel_length=N, num_layers=L)
        model = train_lista_consistent(model, N, K, M, snr_range=(0, 30),
                                        epochs=200, device=device)
        lista_models.append(model)

    for mod in modulations:
        print(f"\n--- {mod.upper()} BER (ZF vs MMSE, 5 seeds) ---")
        results['ber_mmse'][mod] = {}
        results['ber_zf'][mod] = {}

        for snr in snr_levels:
            print(f"\n  SNR = {snr} dB:")
            zf_lista, zf_omp, zf_lasso = [], [], []
            mmse_lista, mmse_omp, mmse_lasso = [], [], []

            for seed in range(num_seeds):
                torch.manual_seed(seed + 3000)
                np.random.seed(seed + 3000)

                zf_l_s, zf_o_s, zf_ls_s = [], [], []
                mmse_l_s, mmse_o_s, mmse_ls_s = [], [], []

                for t in range(num_test):
                    x_batch, d_batch, h_batch = generate_sparse_channel_data(
                        num_samples=1, channel_length=N, sparsity=K,
                        pilot_length=M, snr_db=snr
                    )
                    h_true = h_batch.squeeze(0).numpy()

                    model = lista_models[seed]
                    model.eval()
                    with torch.no_grad():
                        h_lista, _, _ = model(x_batch.to(device), d_batch.to(device))
                    h_lista_np = h_lista.squeeze(0).cpu().numpy()

                    omp = OMPFilter(channel_length=N, sparsity=K)
                    h_omp = omp.estimate(x_batch.squeeze(0), d_batch.squeeze(0)).numpy()

                    lasso = LASSOFilter(channel_length=N, lam=0.01)
                    h_lasso = lasso.estimate(x_batch.squeeze(0), d_batch.squeeze(0)).numpy()

                    zf_l_s.append(compute_ber_zf(h_true, h_lista_np, snr, mod, num_symbols))
                    zf_o_s.append(compute_ber_zf(h_true, h_omp, snr, mod, num_symbols))
                    zf_ls_s.append(compute_ber_zf(h_true, h_lasso, snr, mod, num_symbols))

                    mmse_l_s.append(compute_ber_mmse(h_true, h_lista_np, snr, mod, num_symbols))
                    mmse_o_s.append(compute_ber_mmse(h_true, h_omp, snr, mod, num_symbols))
                    mmse_ls_s.append(compute_ber_mmse(h_true, h_lasso, snr, mod, num_symbols))

                zf_lista.append(np.mean(zf_l_s))
                zf_omp.append(np.mean(zf_o_s))
                zf_lasso.append(np.mean(zf_ls_s))
                mmse_lista.append(np.mean(mmse_l_s))
                mmse_omp.append(np.mean(mmse_o_s))
                mmse_lasso.append(np.mean(mmse_ls_s))

            snr_key = str(snr)

            # Paired t-tests for ZF
            t_zf_lo, p_zf_lo = stats.ttest_rel(zf_lista, zf_omp)
            t_mmse_lo, p_mmse_lo = stats.ttest_rel(mmse_lista, mmse_omp)

            results['ber_zf'][mod][snr_key] = {
                'lista': {'mean': float(np.mean(zf_lista)), 'std': float(np.std(zf_lista)),
                          'seeds': [float(x) for x in zf_lista]},
                'omp': {'mean': float(np.mean(zf_omp)), 'std': float(np.std(zf_omp)),
                        'seeds': [float(x) for x in zf_omp]},
                'lasso': {'mean': float(np.mean(zf_lasso)), 'std': float(np.std(zf_lasso)),
                          'seeds': [float(x) for x in zf_lasso]},
                'lista_vs_omp': {
                    't_statistic': float(t_zf_lo), 'p_value': float(p_zf_lo),
                    'significant_005': bool(p_zf_lo < 0.05),
                },
            }
            results['ber_mmse'][mod][snr_key] = {
                'lista': {'mean': float(np.mean(mmse_lista)), 'std': float(np.std(mmse_lista)),
                          'seeds': [float(x) for x in mmse_lista]},
                'omp': {'mean': float(np.mean(mmse_omp)), 'std': float(np.std(mmse_omp)),
                        'seeds': [float(x) for x in mmse_omp]},
                'lasso': {'mean': float(np.mean(mmse_lasso)), 'std': float(np.std(mmse_lasso)),
                          'seeds': [float(x) for x in mmse_lasso]},
                'lista_vs_omp': {
                    't_statistic': float(t_mmse_lo), 'p_value': float(p_mmse_lo),
                    'significant_005': bool(p_mmse_lo < 0.05),
                },
            }

            print(f"    ZF:   LISTA={np.mean(zf_lista):.6f}±{np.std(zf_lista):.6f}"
                  f"  OMP={np.mean(zf_omp):.6f}±{np.std(zf_omp):.6f}"
                  f"  p={p_zf_lo:.4f}")
            print(f"    MMSE: LISTA={np.mean(mmse_lista):.6f}±{np.std(mmse_lista):.6f}"
                  f"  OMP={np.mean(mmse_omp):.6f}±{np.std(mmse_omp):.6f}"
                  f"  p={p_mmse_lo:.4f}")

    save_path = os.path.join(args.save_dir, 'mmse_full_sweep.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR3 MMSE full sweep saved to {save_path}")
    return results


def exp_nmse_error_bars(args):
    """
    R5: NMSE tables with baseline error bars and LISTA-vs-baseline p-values.

    Re-runs the SNR sweep experiment evaluating ALL methods (including baselines)
    across all seeds to obtain error bars for every method.
    """
    print("\n" + "=" * 60)
    print("Experiment R5: NMSE with Baseline Error Bars")
    print("=" * 60)

    device = args.device
    N, M, K, L = 64, 256, 5, 20
    num_seeds = args.seeds
    num_test = 200

    # --- Table 1: NMSE vs SNR ---
    snr_values = [-5, 0, 5, 10, 15, 20, 25, 30, 40]
    print("\n--- NMSE vs SNR ---")

    all_methods = {snr: {'LMS': [], 'NLMS': [], 'OMP': [], 'LASSO': [], 'LISTA': []}
                   for snr in snr_values}

    for seed in range(num_seeds):
        print(f"\n  Seed {seed+1}/{num_seeds}")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        # Train LISTA
        model = train_lista_consistent(LISTA(N, L), N, K, M,
                                        snr_range=(0, 30), epochs=200, device=device)
        model.eval()

        for test_snr in snr_values:
            # Generate test data with a seed-specific offset
            torch.manual_seed(seed + 5000)
            np.random.seed(seed + 5000)
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=M, snr_db=test_snr
            )

            # LISTA
            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_test)
            all_methods[test_snr]['LISTA'].append(nmse_lista)

            # Baselines (evaluated for each seed with different test data)
            base = evaluate_baselines(x_test, d_test, h_test, N, K)
            for method_name in ['LMS', 'NLMS', 'OMP', 'LASSO']:
                all_methods[test_snr][method_name].append(base[method_name])

        print(f"    SNR=20: LISTA={all_methods[20]['LISTA'][-1]:.2f}, "
              f"OMP={all_methods[20]['OMP'][-1]:.2f}")

    # Build table data
    table_snr = {'config': {'N': N, 'M': M, 'K': K, 'L': L,
                             'num_seeds': num_seeds, 'num_test': num_test}}
    for snr in snr_values:
        row = {}
        for method in ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']:
            vals = all_methods[snr][method]
            row[method] = {
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
                'seeds': [float(v) for v in vals],
            }
        # Paired t-tests: LISTA vs each baseline
        lista_vals = all_methods[snr]['LISTA']
        for baseline in ['LMS', 'NLMS', 'OMP', 'LASSO']:
            base_vals = all_methods[snr][baseline]
            t_stat, p_val = stats.ttest_rel(lista_vals, base_vals)
            row[f'lista_vs_{baseline.lower()}'] = {
                't_statistic': float(t_stat),
                'p_value': float(p_val),
                'significant_005': bool(p_val < 0.05),
            }
        table_snr[str(snr)] = row

    # --- Table 2: NMSE vs Sparsity ---
    sparsity_values = [2, 5, 8, 10, 15]
    print("\n--- NMSE vs Sparsity ---")

    all_methods_sparsity = {k: {'LMS': [], 'NLMS': [], 'OMP': [], 'LASSO': [], 'LISTA': []}
                            for k in sparsity_values}

    for seed in range(num_seeds):
        print(f"\n  Seed {seed+1}/{num_seeds}")
        torch.manual_seed(seed * 42)
        np.random.seed(seed * 42)

        model = train_lista_consistent(LISTA(N, L), N, K, M,
                                        snr_range=(0, 30), epochs=200, device=device)
        model.eval()

        for test_k in sparsity_values:
            torch.manual_seed(seed + 5000)
            np.random.seed(seed + 5000)
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=test_k,
                pilot_length=M, snr_db=20
            )

            with torch.no_grad():
                h_est, _, _ = model(x_test.to(device), d_test.to(device))
            nmse_lista = compute_nmse_db(h_est.cpu(), h_test)
            all_methods_sparsity[test_k]['LISTA'].append(nmse_lista)

            base = evaluate_baselines(x_test, d_test, h_test, N, K)
            for method_name in ['LMS', 'NLMS', 'OMP', 'LASSO']:
                all_methods_sparsity[test_k][method_name].append(base[method_name])

    table_sparsity = {'config': {'N': N, 'M': M, 'L': L, 'snr': 20,
                                  'num_seeds': num_seeds, 'num_test': num_test}}
    for k in sparsity_values:
        row = {}
        for method in ['LMS', 'NLMS', 'OMP', 'LASSO', 'LISTA']:
            vals = all_methods_sparsity[k][method]
            row[method] = {
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
                'seeds': [float(v) for v in vals],
            }
        lista_vals = all_methods_sparsity[k]['LISTA']
        for baseline in ['LMS', 'NLMS', 'OMP', 'LASSO']:
            base_vals = all_methods_sparsity[k][baseline]
            t_stat, p_val = stats.ttest_rel(lista_vals, base_vals)
            row[f'lista_vs_{baseline.lower()}'] = {
                't_statistic': float(t_stat),
                'p_value': float(p_val),
                'significant_005': bool(p_val < 0.05),
            }
        table_sparsity[str(k)] = row

    # Save
    results = {
        'table_snr': table_snr,
        'table_sparsity': table_sparsity,
    }
    save_path = os.path.join(args.save_dir, 'nmse_error_bars.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR5 NMSE error bars saved to {save_path}")
    return results


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Round 6 revision experiments')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['ber5', 'lista_cp', 'mmse_full', 'nmse_bars', 'all'],
                        help='Which experiment to run')
    parser.add_argument('--device', type=str,
                        default='cuda' if torch.cuda.is_available() else 'cpu')
    parser.add_argument('--seeds', type=int, default=5, help='Number of seeds')
    parser.add_argument('--save_dir', type=str, default='results/round6')

    args = parser.parse_args()
    os.makedirs(args.save_dir, exist_ok=True)

    print(f"Device: {args.device}")
    print(f"Seeds: {args.seeds}")
    print(f"Save dir: {args.save_dir}")

    if args.experiment in ['ber5', 'all']:
        exp_ber_5seeds(args)

    if args.experiment in ['lista_cp', 'all']:
        exp_lista_cp_verification(args)

    if args.experiment in ['mmse_full', 'all']:
        exp_mmse_full_sweep(args)

    if args.experiment in ['nmse_bars', 'all']:
        exp_nmse_error_bars(args)

    print("\n\nAll Round 6 experiments complete!")


if __name__ == '__main__':
    main()
