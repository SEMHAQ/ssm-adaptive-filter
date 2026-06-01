"""
Round 4 revision experiments addressing reviewer feedback.

Addresses:
- R1 (Critical): BER with 200+ realizations, paired t-test, 95% CI
- R2 (Critical): Support set recovery rate + error sparsity analysis (BER-NMSE mechanism)
- R3 (Major): MMSE equalization BER comparison
- R4 (Major): Hardware complexity analysis (FLOPs, parallelism, memory access)

Usage:
    cd code
    python run_round4_experiments.py --experiment all --seeds 5 --device cuda
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
from run_round2_experiments import train_lista_consistent, LISTACP
from run_revision_experiments import compute_nmse_db


# ============================================================
# Helper: Modulation (reused from round3)
# ============================================================

def modulate_qpsk(bits):
    """Map bit pairs to QPSK symbols."""
    bits = np.array(bits).reshape(-1, 2)
    symbols = (1 - 2 * bits[:, 0]) + 1j * (1 - 2 * bits[:, 1])
    return symbols / np.sqrt(2)


def modulate_16qam(bits):
    """Map 4-bit groups to 16-QAM symbols (Gray coded)."""
    bits = np.array(bits).reshape(-1, 4)
    def gray_map(b0, b1):
        return (2 * b0 - 1) * (2 - b1)
    real_part = gray_map(bits[:, 0], bits[:, 1])
    imag_part = gray_map(bits[:, 2], bits[:, 3])
    symbols = real_part + 1j * imag_part
    return symbols / np.sqrt(10)


# ============================================================
# R1: BER with 200 realizations + paired t-test + 95% CI
# ============================================================

def compute_ber_zf(h_true, h_est, snr_db, modulation='qpsk', num_symbols=100000):
    """Compute BER with zero-forcing equalization."""
    N = len(h_true)
    if modulation == 'qpsk':
        bits_per_symbol = 2
        modulate = modulate_qpsk
    elif modulation == '16qam':
        bits_per_symbol = 4
        modulate = modulate_16qam
    else:
        raise ValueError(f"Unknown modulation: {modulation}")

    num_bits = num_symbols * bits_per_symbol
    bits = np.random.randint(0, 2, num_bits)
    tx_symbols = modulate(bits)

    # Channel convolution
    rx_signal = np.convolve(tx_symbols, h_true)[:len(tx_symbols)]

    # AWGN
    snr_linear = 10 ** (snr_db / 10)
    signal_power = np.mean(np.abs(rx_signal) ** 2)
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(rx_signal)) + 1j * np.random.randn(len(rx_signal)))
    rx_noisy = rx_signal + noise

    # ZF equalization
    fft_len = len(tx_symbols)
    H_est = np.fft.fft(h_est, fft_len)
    H_est_safe = H_est.copy()
    H_est_safe[np.abs(H_est_safe) < 1e-10] = 1e-10
    rx_fft = np.fft.fft(rx_noisy, fft_len)
    eq_symbols = np.fft.ifft(rx_fft / H_est_safe)[:num_symbols]

    # Demodulate
    if modulation == 'qpsk':
        detected_bits = np.zeros(num_bits)
        detected_bits[0::2] = (np.real(eq_symbols) < 0).astype(int)
        detected_bits[1::2] = (np.imag(eq_symbols) < 0).astype(int)
    elif modulation == '16qam':
        eq_scaled = eq_symbols * np.sqrt(10)
        real_part = np.clip(np.round((np.real(eq_scaled) + 1) / 2) * 2 - 1, -3, 3)
        imag_part = np.clip(np.round((np.imag(eq_scaled) + 1) / 2) * 2 - 1, -3, 3)
        detected_bits = np.zeros(num_bits)
        detected_bits[0::4] = ((real_part + 3) >= 2).astype(int)
        detected_bits[1::4] = (np.abs(real_part) < 2).astype(int)
        detected_bits[2::4] = ((imag_part + 3) >= 2).astype(int)
        detected_bits[3::4] = (np.abs(imag_part) < 2).astype(int)

    return np.mean(bits != detected_bits)


def compute_ber_mmse(h_true, h_est, snr_db, modulation='qpsk', num_symbols=100000):
    """Compute BER with MMSE equalization."""
    if modulation == 'qpsk':
        bits_per_symbol = 2
        modulate = modulate_qpsk
    elif modulation == '16qam':
        bits_per_symbol = 4
        modulate = modulate_16qam
    else:
        raise ValueError(f"Unknown modulation: {modulation}")

    num_bits = num_symbols * bits_per_symbol
    bits = np.random.randint(0, 2, num_bits)
    tx_symbols = modulate(bits)

    # Channel convolution
    rx_signal = np.convolve(tx_symbols, h_true)[:len(tx_symbols)]

    # AWGN
    snr_linear = 10 ** (snr_db / 10)
    signal_power = np.mean(np.abs(rx_signal) ** 2)
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(rx_signal)) + 1j * np.random.randn(len(rx_signal)))
    rx_noisy = rx_signal + noise

    # MMSE equalization: W = H* / (|H|^2 + 1/SNR)
    fft_len = len(tx_symbols)
    H_est = np.fft.fft(h_est, fft_len)
    H_mag_sq = np.abs(H_est) ** 2
    snr_lin = 10 ** (snr_db / 10)
    # MMSE filter
    W_mmse = np.conj(H_est) / (H_mag_sq + 1.0 / snr_lin + 1e-10)

    rx_fft = np.fft.fft(rx_noisy, fft_len)
    eq_symbols = np.fft.ifft(rx_fft * W_mmse)[:num_symbols]

    # Demodulate
    if modulation == 'qpsk':
        detected_bits = np.zeros(num_bits)
        detected_bits[0::2] = (np.real(eq_symbols) < 0).astype(int)
        detected_bits[1::2] = (np.imag(eq_symbols) < 0).astype(int)
    elif modulation == '16qam':
        eq_scaled = eq_symbols * np.sqrt(10)
        real_part = np.clip(np.round((np.real(eq_scaled) + 1) / 2) * 2 - 1, -3, 3)
        imag_part = np.clip(np.round((np.imag(eq_scaled) + 1) / 2) * 2 - 1, -3, 3)
        detected_bits = np.zeros(num_bits)
        detected_bits[0::4] = ((real_part + 3) >= 2).astype(int)
        detected_bits[1::4] = (np.abs(real_part) < 2).astype(int)
        detected_bits[2::4] = ((imag_part + 3) >= 2).astype(int)
        detected_bits[3::4] = (np.abs(imag_part) < 2).astype(int)

    return np.mean(bits != detected_bits)


def exp_ber_statistical(args):
    """
    R1: BER with 200+ realizations, paired t-test, 95% CI.

    Increases channel realizations from 50 to 200 per SNR point.
    Adds paired t-tests between LISTA and OMP at each SNR.
    Reports 95% confidence intervals.
    """
    print("\n" + "=" * 60)
    print("Experiment R1: BER Statistical Validation (200 realizations)")
    print("=" * 60)

    device = args.device
    N, M, K, L = 64, 256, 5, 20
    snr_levels = [0, 5, 10, 15, 20, 25, 30]
    modulations = ['qpsk', '16qam']
    num_test = 200       # Increased from 50 to 200
    num_symbols = 50000
    num_seeds = args.seeds

    results = {
        'config': {
            'N': N, 'M': M, 'K': K, 'L': L,
            'num_test': num_test, 'num_symbols': num_symbols,
            'snr_levels': snr_levels, 'modulations': modulations,
            'num_seeds': num_seeds,
            'note': '200 realizations per SNR point (up from 50 in round3)'
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
        print(f"\n--- {mod.upper()} BER (ZF) ---")
        results['ber'][mod] = {}

        for snr in snr_levels:
            print(f"\n  SNR = {snr} dB ({num_test} realizations):")
            ber_lista_all = []
            ber_omp_all = []
            ber_lasso_all = []

            # Per-seed BER values (for paired tests)
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
                    x = x_batch.squeeze(0).numpy()
                    d = d_batch.squeeze(0).numpy()

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

                # Per-seed mean
                seed_lista = np.mean(ber_lista_realizations)
                seed_omp = np.mean(ber_omp_realizations)
                seed_lasso = np.mean(ber_lasso_realizations)
                ber_lista_seeds.append(seed_lista)
                ber_omp_seeds.append(seed_omp)
                ber_lasso_seeds.append(seed_lasso)

                ber_lista_all.extend(ber_lista_realizations)
                ber_omp_all.extend(ber_omp_realizations)
                ber_lasso_all.extend(ber_lasso_realizations)

            # Statistics
            lista_mean = np.mean(ber_lista_seeds)
            lista_std = np.std(ber_lista_seeds)
            omp_mean = np.mean(ber_omp_seeds)
            omp_std = np.std(ber_omp_seeds)
            lasso_mean = np.mean(ber_lasso_seeds)
            lasso_std = np.std(ber_lasso_seeds)

            # 95% CI (using t-distribution)
            t_crit = stats.t.ppf(0.975, num_seeds - 1)
            lista_ci = t_crit * lista_std / np.sqrt(num_seeds)
            omp_ci = t_crit * omp_std / np.sqrt(num_seeds)
            lasso_ci = t_crit * lasso_std / np.sqrt(num_seeds)

            # Paired t-test: LISTA vs OMP
            t_stat_lo, p_val_lo = stats.ttest_rel(ber_lista_seeds, ber_omp_seeds)
            # Paired t-test: LISTA vs LASSO
            t_stat_ll, p_val_ll = stats.ttest_rel(ber_lista_seeds, ber_lasso_seeds)

            # Effect size (Cohen's d) for LISTA vs OMP
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
                    'ci_95': float(lasso_ci),
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
            print(f"    LISTA: {lista_mean:.6f} ± {lista_std:.6f} (95% CI: ±{lista_ci:.6f})")
            print(f"    OMP:   {omp_mean:.6f} ± {omp_std:.6f} (95% CI: ±{omp_ci:.6f})")
            print(f"    LASSO: {lasso_mean:.6f} ± {lasso_std:.6f} (95% CI: ±{lasso_ci:.6f})")
            print(f"    LISTA vs OMP: p={p_val_lo:.4f} {sig_mark}, Cohen's d={cohens_d_lo:.3f}")

    # Save
    save_path = os.path.join(args.save_dir, 'ber_statistical.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR1 BER statistical results saved to {save_path}")
    return results


# ============================================================
# R2: BER-NMSE Mechanism Analysis
# ============================================================

def compute_support_recovery(h_true, h_est, K):
    """
    Compute support set recovery metrics.

    Returns:
        jaccard: Jaccard index |intersection|/|union|
        precision: fraction of estimated support that is correct
        recall: fraction of true support that is recovered
    """
    true_support = set(np.where(np.abs(h_true) > 1e-6)[0])
    # Top-K indices by magnitude in estimate
    est_topk = set(np.argsort(np.abs(h_est))[-K:].tolist())
    # Also consider all non-zero estimated taps
    est_nonzero = set(np.where(np.abs(h_est) > 1e-6)[0])

    # Use top-K for fair comparison (OMP also returns K taps)
    intersection = true_support & est_topk
    union = true_support | est_topk

    jaccard = len(intersection) / len(union) if len(union) > 0 else 0.0
    precision = len(intersection) / len(est_topk) if len(est_topk) > 0 else 0.0
    recall = len(intersection) / len(true_support) if len(true_support) > 0 else 0.0

    return jaccard, precision, recall


def compute_error_sparsity(h_true, h_est):
    """
    Analyze the sparsity structure of estimation error.

    Returns:
        error_on_support: fraction of total error energy on true support
        error_on_nonsupport: fraction of total error energy on non-support
        error_gini: Gini coefficient of |error| (0=uniform, 1=sparse)
        est_sparsity: fraction of |h_est| energy on top-K taps
    """
    K_true = int(np.sum(np.abs(h_true) > 1e-6))
    error = h_est - h_true
    error_mag = np.abs(error)
    error_energy = error_mag ** 2

    true_support = np.where(np.abs(h_true) > 1e-6)[0]
    all_indices = np.arange(len(h_true))
    nonsupport = np.setdiff1d(all_indices, true_support)

    total_error_energy = np.sum(error_energy) + 1e-20
    error_on_support = np.sum(error_energy[true_support]) / total_error_energy if len(true_support) > 0 else 0.0
    error_on_nonsupport = np.sum(error_energy[nonsupport]) / total_error_energy if len(nonsupport) > 0 else 0.0

    # Gini coefficient of error magnitude
    sorted_err = np.sort(error_mag)
    n = len(sorted_err)
    if np.sum(sorted_err) > 1e-20:
        gini = (2 * np.sum(np.arange(1, n + 1) * sorted_err) / (n * np.sum(sorted_err))) - (n + 1) / n
    else:
        gini = 0.0

    # Sparsity of estimate: fraction of energy in top-K
    topk_idx = np.argsort(np.abs(h_est))[-K_true:]
    est_sparsity = np.sum(np.abs(h_est[topk_idx]) ** 2) / (np.sum(np.abs(h_est) ** 2) + 1e-20)

    return float(error_on_support), float(error_on_nonsupport), float(gini), float(est_sparsity)


def compute_noise_enhancement(h_est, x_pilot, snr_db):
    """
    Compute equalizer noise enhancement factor for ZF equalization.

    The ZF equalizer applies H_est^{-1}, which amplifies noise by
    factor proportional to ||H_est^{-1}||^2.
    """
    N = len(h_est)
    M = len(x_pilot)
    fft_len = M * 2  # sufficient for linear convolution
    H_est_fft = np.fft.fft(h_est, fft_len)
    # Noise enhancement = mean of 1/|H|^2 across frequency
    H_mag_sq = np.abs(H_est_fft) ** 2
    H_mag_sq_safe = np.maximum(H_mag_sq, 1e-10)
    noise_enhancement = np.mean(1.0 / H_mag_sq_safe)
    return float(noise_enhancement)


def exp_mechanism_analysis(args):
    """
    R2: BER-NMSE mechanism analysis.

    Measures:
    1. Support set recovery (Jaccard index) for LISTA vs OMP
    2. Error sparsity analysis (where does estimation error concentrate?)
    3. Equalizer noise enhancement factor
    """
    print("\n" + "=" * 60)
    print("Experiment R2: BER-NMSE Mechanism Analysis")
    print("=" * 60)

    device = args.device
    N, M, K, L = 64, 256, 5, 20
    snr_levels = [0, 10, 20, 30]
    num_test = 200
    num_seeds = args.seeds

    results = {
        'config': {'N': N, 'M': M, 'K': K, 'L': L, 'num_test': num_test, 'num_seeds': num_seeds},
        'support_recovery': {},
        'error_sparsity': {},
        'noise_enhancement': {},
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

    for snr in snr_levels:
        print(f"\n--- SNR = {snr} dB ---")

        lista_jaccard, lista_prec, lista_recall = [], [], []
        omp_jaccard, omp_prec, omp_recall = [], [], []
        lista_err_support, lista_err_nonsupport, lista_gini, lista_est_sparsity = [], [], [], []
        omp_err_support, omp_err_nonsupport, omp_gini, omp_est_sparsity = [], [], [], []
        lista_ne, omp_ne = [], []

        for seed in range(num_seeds):
            torch.manual_seed(seed + 2000)
            np.random.seed(seed + 2000)

            for t in range(num_test):
                x_batch, d_batch, h_batch = generate_sparse_channel_data(
                    num_samples=1, channel_length=N, sparsity=K,
                    pilot_length=M, snr_db=snr
                )
                h_true = h_batch.squeeze(0).numpy()
                x = x_batch.squeeze(0).numpy()
                d = d_batch.squeeze(0).numpy()

                # LISTA estimation
                model = lista_models[seed]
                model.eval()
                with torch.no_grad():
                    h_lista, _, _ = model(x_batch.to(device), d_batch.to(device))
                h_lista_np = h_lista.squeeze(0).cpu().numpy()

                # OMP estimation
                omp = OMPFilter(channel_length=N, sparsity=K)
                h_omp = omp.estimate(x_batch.squeeze(0), d_batch.squeeze(0)).numpy()

                # Support recovery
                j_l, p_l, r_l = compute_support_recovery(h_true, h_lista_np, K)
                j_o, p_o, r_o = compute_support_recovery(h_true, h_omp, K)
                lista_jaccard.append(j_l)
                lista_prec.append(p_l)
                lista_recall.append(r_l)
                omp_jaccard.append(j_o)
                omp_prec.append(p_o)
                omp_recall.append(r_o)

                # Error sparsity
                es_l, ens_l, g_l, sp_l = compute_error_sparsity(h_true, h_lista_np)
                es_o, ens_o, g_o, sp_o = compute_error_sparsity(h_true, h_omp)
                lista_err_support.append(es_l)
                lista_err_nonsupport.append(ens_l)
                lista_gini.append(g_l)
                lista_est_sparsity.append(sp_l)
                omp_err_support.append(es_o)
                omp_err_nonsupport.append(ens_o)
                omp_gini.append(g_o)
                omp_est_sparsity.append(sp_o)

                # Noise enhancement
                ne_l = compute_noise_enhancement(h_lista_np, x, snr)
                ne_o = compute_noise_enhancement(h_omp, x, snr)
                lista_ne.append(ne_l)
                omp_ne.append(ne_o)

        snr_key = str(snr)
        results['support_recovery'][snr_key] = {
            'lista': {
                'jaccard_mean': float(np.mean(lista_jaccard)),
                'jaccard_std': float(np.std(lista_jaccard)),
                'precision_mean': float(np.mean(lista_prec)),
                'recall_mean': float(np.mean(lista_recall)),
            },
            'omp': {
                'jaccard_mean': float(np.mean(omp_jaccard)),
                'jaccard_std': float(np.std(omp_jaccard)),
                'precision_mean': float(np.mean(omp_prec)),
                'recall_mean': float(np.mean(omp_recall)),
            }
        }

        results['error_sparsity'][snr_key] = {
            'lista': {
                'error_on_support_mean': float(np.mean(lista_err_support)),
                'error_on_nonsupport_mean': float(np.mean(lista_err_nonsupport)),
                'gini_mean': float(np.mean(lista_gini)),
                'est_sparsity_mean': float(np.mean(lista_est_sparsity)),
            },
            'omp': {
                'error_on_support_mean': float(np.mean(omp_err_support)),
                'error_on_nonsupport_mean': float(np.mean(omp_err_nonsupport)),
                'gini_mean': float(np.mean(omp_gini)),
                'est_sparsity_mean': float(np.mean(omp_est_sparsity)),
            }
        }

        results['noise_enhancement'][snr_key] = {
            'lista_mean': float(np.mean(lista_ne)),
            'lista_std': float(np.std(lista_ne)),
            'omp_mean': float(np.mean(omp_ne)),
            'omp_std': float(np.std(omp_ne)),
        }

        print(f"  Support Recovery (Jaccard):")
        print(f"    LISTA: {np.mean(lista_jaccard):.4f} ± {np.std(lista_jaccard):.4f}")
        print(f"    OMP:   {np.mean(omp_jaccard):.4f} ± {np.std(omp_jaccard):.4f}")
        print(f"  Error on Support (% of total):")
        print(f"    LISTA: {np.mean(lista_err_support)*100:.1f}%")
        print(f"    OMP:   {np.mean(omp_err_support)*100:.1f}%")
        print(f"  Error Gini (higher=more sparse):")
        print(f"    LISTA: {np.mean(lista_gini):.4f}")
        print(f"    OMP:   {np.mean(omp_gini):.4f}")
        print(f"  Noise Enhancement (lower=better):")
        print(f"    LISTA: {np.mean(lista_ne):.4f}")
        print(f"    OMP:   {np.mean(omp_ne):.4f}")

    save_path = os.path.join(args.save_dir, 'mechanism_analysis.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR2 Mechanism analysis saved to {save_path}")
    return results


# ============================================================
# R3: MMSE Equalization BER
# ============================================================

def exp_ber_mmse(args):
    """
    R3: BER with MMSE equalization.

    Compares ZF vs MMSE equalization for LISTA, OMP, LASSO.
    """
    print("\n" + "=" * 60)
    print("Experiment R3: BER with MMSE Equalization")
    print("=" * 60)

    device = args.device
    N, M, K, L = 64, 256, 5, 20
    snr_levels = [0, 5, 10, 15, 20, 25, 30]
    modulations = ['qpsk', '16qam']
    num_test = 100
    num_symbols = 50000
    num_seeds = args.seeds

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
        print(f"\n--- {mod.upper()} BER (ZF vs MMSE) ---")
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

                    # ZF BER
                    zf_l_s.append(compute_ber_zf(h_true, h_lista_np, snr, mod, num_symbols))
                    zf_o_s.append(compute_ber_zf(h_true, h_omp, snr, mod, num_symbols))
                    zf_ls_s.append(compute_ber_zf(h_true, h_lasso, snr, mod, num_symbols))

                    # MMSE BER
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
            results['ber_zf'][mod][snr_key] = {
                'lista': {'mean': float(np.mean(zf_lista)), 'std': float(np.std(zf_lista))},
                'omp': {'mean': float(np.mean(zf_omp)), 'std': float(np.std(zf_omp))},
                'lasso': {'mean': float(np.mean(zf_lasso)), 'std': float(np.std(zf_lasso))},
            }
            results['ber_mmse'][mod][snr_key] = {
                'lista': {'mean': float(np.mean(mmse_lista)), 'std': float(np.std(mmse_lista))},
                'omp': {'mean': float(np.mean(mmse_omp)), 'std': float(np.std(mmse_omp))},
                'lasso': {'mean': float(np.mean(mmse_lasso)), 'std': float(np.std(mmse_lasso))},
            }

            print(f"    ZF:   LISTA={np.mean(zf_lista):.6f}  OMP={np.mean(zf_omp):.6f}  LASSO={np.mean(zf_lasso):.6f}")
            print(f"    MMSE: LISTA={np.mean(mmse_lista):.6f}  OMP={np.mean(mmse_omp):.6f}  LASSO={np.mean(mmse_lasso):.6f}")

    save_path = os.path.join(args.save_dir, 'ber_mmse.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR3 MMSE BER results saved to {save_path}")
    return results


# ============================================================
# R4: Hardware Complexity Analysis
# ============================================================

def exp_hardware_complexity(args):
    """
    R4: Hardware complexity analysis.

    Computes:
    1. FLOPs per inference for LISTA, OMP, LASSO
    2. Parallelism analysis (what can be parallelized)
    3. Memory access patterns (sequential vs random)
    4. Theoretical speedup ratios
    """
    print("\n" + "=" * 60)
    print("Experiment R4: Hardware Complexity Analysis")
    print("=" * 60)

    N, M, K, L = 64, 256, 5, 20

    results = {'config': {'N': N, 'M': M, 'K': K, 'L': L}}

    # --- LISTA FLOPs ---
    # Per layer:
    #   1. Build Toeplitz: M*N multiplications (done once, can be cached)
    #   2. Matrix-vector A @ h: M*N multiply-add
    #   3. Residual: M subtractions
    #   4. A^T @ residual: M*N multiply-add
    #   5. W @ h: N^2 multiply-add
    #   6. Step * grad: N multiply
    #   7. W*h - step*grad: N add
    #   8. Soft-threshold: 3*N compare+abs+subtract
    #
    # Per layer (after Toeplitz is built): 2*M*N + N^2 + 5*N
    # Toeplitz build (once): M*N
    # Total: M*N + L*(2*M*N + N^2 + 5*N)

    lista_flops_toeplitz = M * N
    lista_flops_per_layer = 2 * M * N + N * N + 5 * N
    lista_flops_total = lista_flops_toeplitz + L * lista_flops_per_layer

    # --- OMP FLOPs ---
    # Per iteration:
    #   1. Correlation |A^T @ r|: M*N multiply-add + N abs
    #   2. Argmax: N comparisons
    #   3. Least squares on support (k atoms): k*M*N + k^3 (QR or normal eq)
    #   4. Residual update: M*k multiply-add
    # Average: iter k has ~k*M*N for LS + M*N for correlation
    # Total for K iterations: K*M*N + sum_{k=1}^{K} (k*M*N + k^3)
    #                        ≈ K*M*N + K*(K+1)/2*M*N + K^4/4
    # For K=5: 5*256*64 + 15*256*64 + ~156 ≈ 81920 + 245760 + 156

    omp_flops = 0
    for k in range(1, K + 1):
        omp_flops += M * N  # correlation
        omp_flops += k * M * N  # least squares (simplified)
        omp_flops += M * k  # residual update
        omp_flops += k ** 3  # matrix inversion

    # --- LASSO FLOPs ---
    # Per ISTA iteration:
    #   1. A @ h: M*N
    #   2. A^T @ (A@h - d): M*N
    #   3. Step update: N
    #   4. Soft threshold: 3*N
    # Total per iter: 2*M*N + 4*N
    # 200 iterations
    lasso_iters = 200
    lasso_flops_per_iter = 2 * M * N + 4 * N
    lasso_flops_total = lasso_iters * lasso_flops_per_iter

    results['flops'] = {
        'lista': {
            'total': int(lista_flops_total),
            'per_layer': int(lista_flops_per_layer),
            'toeplitz_build': int(lista_flops_toeplitz),
            'breakdown': {
                'convolution_AX': f'{M}*{N} = {M*N} per layer',
                'gradient_ATr': f'{M}*{N} = {M*N} per layer',
                'linear_mapping_Wh': f'{N}*{N} = {N*N} per layer',
                'thresholding': f'3*{N} = {3*N} per layer',
            }
        },
        'omp': {
            'total': int(omp_flops),
            'per_iteration_avg': int(omp_flops / K),
            'breakdown': {
                'correlation': f'{M}*{N} = {M*N} per iter',
                'least_squares': f'k*{M}*{N} per iter (k grows)',
                'residual': f'{M}*k per iter',
            }
        },
        'lasso': {
            'total': int(lasso_flops_total),
            'per_iteration': int(lasso_flops_per_iter),
            'iterations': lasso_iters,
        },
        'ratios': {
            'lista_vs_omp': float(lista_flops_total / omp_flops),
            'lista_vs_lasso': float(lista_flops_total / lasso_flops_total),
            'omp_vs_lasso': float(omp_flops / lasso_flops_total),
        }
    }

    print(f"\nFLOPs Comparison (N={N}, M={M}, K={K}, L={L}):")
    print(f"  LISTA: {lista_flops_total:>12,} FLOPs ({L} layers)")
    print(f"  OMP:   {omp_flops:>12,} FLOPs ({K} iterations)")
    print(f"  LASSO: {lasso_flops_total:>12,} FLOPs ({lasso_iters} iterations)")
    print(f"  LISTA/OMP ratio: {lista_flops_total/omp_flops:.2f}x")
    print(f"  LISTA/LASSO ratio: {lista_flops_total/lasso_flops_total:.2f}x")

    # --- Parallelism Analysis ---
    results['parallelism'] = {
        'lista': {
            'description': 'Fixed-depth feedforward network',
            'layer_parallelism': 'Each layer has 3 independent matrix-vector ops (A@h, A^T@r, W@h) that can be pipelined',
            'batch_parallelism': 'Full batch parallelism across channel estimates',
            'intra_layer': [
                'A @ h: matrix-vector multiply, parallelizable across M rows',
                'A^T @ residual: matrix-vector multiply, parallelizable across N rows',
                'W @ h: N x N matrix-vector, parallelizable across N rows',
                'Soft-thresholding: element-wise, fully parallel',
            ],
            'inter_layer': 'Sequential (layer k+1 depends on layer k output)',
            'hardware_utilization': 'High — identical ops per layer, regular data flow, no branches',
            'pipeline_depth': L,
            'fpga_suitability': 'Excellent — fixed computation graph, no dynamic control flow',
        },
        'omp': {
            'description': 'Iterative greedy algorithm with dynamic support set',
            'batch_parallelism': 'Full batch parallelism across channel estimates',
            'intra_iteration': [
                'Correlation A^T @ r: parallelizable across N atoms',
                'Least squares: k x k system solve, parallelizable but small',
            ],
            'inter_iteration': 'Sequential (iteration k+1 depends on k)',
            'dynamic_behavior': 'Support set selection (argmax) requires reduction across N values',
            'hardware_utilization': 'Moderate — support set varies per iteration, irregular memory access',
            'pipeline_depth': K,
            'fpga_suitability': 'Moderate — dynamic argmax and varying LS dimension complicate pipelining',
        },
        'lasso': {
            'description': 'Iterative proximal gradient descent',
            'batch_parallelism': 'Full batch parallelism',
            'intra_iteration': 'Same as LISTA per iteration (A@h, A^T@r, soft-threshold)',
            'inter_iteration': 'Sequential',
            'hardware_utilization': 'Low — 200 iterations vs LISTA\'s 20 layers',
            'pipeline_depth': lasso_iters,
            'fpga_suitability': 'Poor — too many iterations for hardware pipelining',
        }
    }

    # --- Memory Access Patterns ---
    # Parameters
    lista_params = L * (N * N + 2)  # W matrices + step + threshold
    lista_param_bytes = lista_params * 4  # float32

    results['memory'] = {
        'lista': {
            'parameters': int(lista_params),
            'parameter_memory_bytes': int(lista_param_bytes),
            'parameter_memory_KB': float(lista_param_bytes / 1024),
            'activation_memory': f'{L} layers * {N} activations * 4 bytes = {L * N * 4} bytes',
            'access_pattern': 'Sequential — same matrix-vector ops every layer, predictable address sequence',
            'cache_behavior': 'Excellent — W^(k) matrices fit in L1/L2 cache for N=64 (16KB each)',
            'bandwidth_requirement': 'Low — parameters loaded once per inference, reused across batch',
        },
        'omp': {
            'storage': f'A matrix: {M}*{N}*4 = {M*N*4} bytes; support set: {K} indices',
            'access_pattern': 'Semi-random — argmax scans all N correlations, LS accesses support columns',
            'cache_behavior': 'Moderate — A matrix access is column-wise (stride M), support set is random',
            'bandwidth_requirement': 'Moderate — A matrix loaded every iteration, residual updated',
        },
        'lasso': {
            'storage': f'A matrix: {M}*{N}*4 = {M*N*4} bytes; h vector: {N}*4 bytes',
            'access_pattern': 'Sequential — same as LISTA per iteration',
            'cache_behavior': 'Good per iteration, but 200 iterations increase total bandwidth',
            'bandwidth_requirement': 'High — 200 iterations of full matrix-vector products',
        }
    }

    # --- Theoretical Hardware Timing ---
    # Assume: 1 DSP = 1 multiply-add per clock, clock = 500 MHz (typical FPGA)
    # LISTA: each layer has ~2*M*N + N^2 ≈ 2*256*64 + 64^2 = 32768 + 4096 = 36864 MA ops
    # With 64 DSPs in parallel: 36864/64 = 576 clocks per layer
    # 20 layers: 11520 clocks → at 500MHz = 23 us
    # With pipeline (all layers): 1 clock throughput after pipeline fills

    dsp_count = 64
    clock_mhz = 500

    lista_ops_per_layer = 2 * M * N + N * N
    lista_clocks_per_layer = lista_ops_per_layer // dsp_count + 1
    lista_total_clocks = L * lista_clocks_per_layer
    lista_latency_us = lista_total_clocks / clock_mhz
    lista_pipeline_throughput_us = lista_clocks_per_layer / clock_mhz

    omp_ops_per_iter = M * N + M * N  # correlation + LS (simplified)
    omp_total_clocks = K * (omp_ops_per_iter // dsp_count + 1)
    omp_latency_us = omp_total_clocks / clock_mhz

    results['hardware_timing_estimate'] = {
        'assumptions': {
            'DSP_count': dsp_count,
            'clock_MHz': clock_mhz,
            'precision': 'float32',
        },
        'lista': {
            'sequential_latency_us': float(lista_latency_us),
            'pipelined_throughput_us': float(lista_pipeline_throughput_us),
            'total_clocks': int(lista_total_clocks),
        },
        'omp': {
            'latency_us': float(omp_latency_us),
            'total_clocks': int(omp_total_clocks),
        },
        'speedup_sequential': float(omp_latency_us / lista_latency_us),
        'speedup_pipelined': float(omp_latency_us / lista_pipeline_throughput_us),
    }

    print(f"\nTheoretical Hardware Timing ({dsp_count} DSPs, {clock_mhz} MHz):")
    print(f"  LISTA (sequential): {lista_latency_us:.1f} μs")
    print(f"  LISTA (pipelined):  {lista_pipeline_throughput_us:.1f} μs throughput")
    print(f"  OMP:                {omp_latency_us:.1f} μs")
    print(f"  Speedup (sequential): {omp_latency_us/lista_latency_us:.1f}×")
    print(f"  Speedup (pipelined):  {omp_latency_us/lista_pipeline_throughput_us:.1f}×")

    # --- Scaling Analysis ---
    results['scaling'] = {}
    for N_val in [32, 64, 128, 256]:
        lista_params_n = L * (N_val * N_val + 2)
        lista_flops_n = M * N_val + L * (2 * M * N_val + N_val * N_val + 5 * N_val)
        omp_flops_n = 0
        for k in range(1, K + 1):
            omp_flops_n += M * N_val + k * M * N_val + M * k + k ** 3
        results['scaling'][str(N_val)] = {
            'lista_params': int(lista_params_n),
            'lista_flops': int(lista_flops_n),
            'omp_flops': int(omp_flops_n),
            'lista_omp_flops_ratio': float(lista_flops_n / omp_flops_n),
        }
        print(f"\n  N={N_val}: LISTA params={lista_params_n:,}, FLOPs ratio LISTA/OMP={lista_flops_n/omp_flops_n:.2f}x")

    save_path = os.path.join(args.save_dir, 'hardware_complexity.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nR4 Hardware complexity saved to {save_path}")
    return results


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Round 4 revision experiments')
    parser.add_argument('--experiment', type=str, default='all',
                        choices=['ber_stat', 'mechanism', 'mmse', 'hardware', 'all'],
                        help='Which experiment to run')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
    parser.add_argument('--seeds', type=int, default=5, help='Number of seeds')
    parser.add_argument('--save_dir', type=str, default='results/round4')

    args = parser.parse_args()
    os.makedirs(args.save_dir, exist_ok=True)

    print(f"Device: {args.device}")
    print(f"Seeds: {args.seeds}")
    print(f"Save dir: {args.save_dir}")

    if args.experiment in ['ber_stat', 'all']:
        exp_ber_statistical(args)

    if args.experiment in ['mechanism', 'all']:
        exp_mechanism_analysis(args)

    if args.experiment in ['mmse', 'all']:
        exp_ber_mmse(args)

    if args.experiment in ['hardware', 'all']:
        exp_hardware_complexity(args)

    print("\n\nAll Round 4 experiments complete!")


if __name__ == '__main__':
    main()
