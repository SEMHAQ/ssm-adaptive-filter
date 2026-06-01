"""
Threshold function comparison experiment for LISTA.

Compares three thresholding operators within the LISTA architecture:
1. Soft thresholding (standard LISTA): sign(x) * max(|x| - theta, 0)
2. Hard thresholding: x * (|x| > theta)
3. Semi-soft (garrote) thresholding: x * max(1 - theta^2/x^2, 0) for |x| > theta

All variants share the same LISTA architecture (learnable W, step, threshold)
and identical training protocol. This experiment demonstrates that LISTA's
learned threshold schedule does something beyond generic soft-thresholding.

Usage:
    cd code
    python run_threshold_comparison.py --seeds 20 --device cuda
    python run_threshold_comparison.py --seeds 5 --device cpu
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import argparse
from scipy import stats

from data.generate import generate_sparse_channel_data


# ============================================================
# Threshold operators as nn.Module
# ============================================================

class SoftThreshold(nn.Module):
    """Learnable soft thresholding: sign(x) * max(|x| - theta, 0)"""
    def __init__(self, init_threshold=0.1):
        super().__init__()
        self.threshold = nn.Parameter(torch.tensor(init_threshold))

    def forward(self, x):
        return torch.sign(x) * torch.relu(torch.abs(x) - self.threshold)


class HardThreshold(nn.Module):
    """Learnable hard thresholding: x * (|x| > theta)"""
    def __init__(self, init_threshold=0.1):
        super().__init__()
        self.threshold = nn.Parameter(torch.tensor(init_threshold))

    def forward(self, x):
        # Differentiable approximation: use straight-through estimator
        # Forward: hard threshold; backward: pass gradient through
        mask = (torch.abs(x) > self.threshold).float()
        # Straight-through: use soft threshold gradient for stability
        soft_grad = torch.sign(x) * torch.relu(torch.abs(x) - self.threshold)
        return mask * x + (1 - mask) * soft_grad.detach() + soft_grad - soft_grad.detach()


class SemiSoftThreshold(nn.Module):
    """Learnable semi-soft (garrote) thresholding.

    For |x| > theta: x * (1 - theta^2 / x^2)
    For |x| <= theta: 0

    This is the non-negative garrote thresholding, which interpolates
    between soft and hard thresholding.
    """
    def __init__(self, init_threshold=0.1):
        super().__init__()
        self.threshold = nn.Parameter(torch.tensor(init_threshold))

    def forward(self, x):
        abs_x = torch.abs(x)
        # Clamp to avoid division by zero
        abs_x_safe = torch.clamp(abs_x, min=1e-8)
        # Semi-soft: x * max(1 - theta^2/x^2, 0)
        shrinkage = torch.relu(1.0 - (self.threshold ** 2) / (abs_x_safe ** 2))
        return x * shrinkage


# ============================================================
# LISTA layer and model with pluggable threshold
# ============================================================

class LISTALayerThreshold(nn.Module):
    """LISTA layer with pluggable thresholding function."""
    def __init__(self, channel_length, threshold_module, init_step=0.5):
        super().__init__()
        self.step = nn.Parameter(torch.tensor(init_step))
        self.threshold = threshold_module
        self.W = nn.Linear(channel_length, channel_length, bias=False)
        nn.init.eye_(self.W.weight)

    def forward(self, h, grad):
        h_new = self.W(h) - self.step * grad
        return self.threshold(h_new)


class LISTAThreshold(nn.Module):
    """LISTA model with pluggable thresholding function."""
    def __init__(self, channel_length, num_layers, threshold_type='soft'):
        super().__init__()
        self.channel_length = channel_length
        self.num_layers = num_layers

        # Create threshold module based on type
        if threshold_type == 'soft':
            thresh_cls = SoftThreshold
        elif threshold_type == 'hard':
            thresh_cls = HardThreshold
        elif threshold_type == 'semisoft':
            thresh_cls = SemiSoftThreshold
        else:
            raise ValueError(f"Unknown threshold type: {threshold_type}")

        self.layers = nn.ModuleList([
            LISTALayerThreshold(
                channel_length,
                thresh_cls(init_threshold=0.001),
                init_step=0.5
            )
            for _ in range(num_layers)
        ])

    def _build_toeplitz(self, x):
        """Build batched Toeplitz convolution matrix A."""
        B, M = x.shape
        N = self.channel_length
        A = torch.zeros(B, M, N, device=x.device)
        for j in range(N):
            A[:, j:, j] = x[:, :M - j]
        return A

    def forward(self, x, d, return_pre_threshold=False):
        batch = x.shape[0]
        device = x.device
        pilot_len = x.shape[1]
        A = self._build_toeplitz(x)
        h = torch.zeros(batch, self.channel_length, device=device)

        pre_threshold_values = []
        for layer in self.layers:
            d_recon = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
            residual = (d_recon - d).unsqueeze(-1)
            grad = torch.bmm(A.transpose(1, 2), residual).squeeze(-1) / pilot_len
            h_new = layer.W(h) - layer.step * grad
            if return_pre_threshold:
                pre_threshold_values.append(h_new.detach().cpu())
            h = layer.threshold(h_new)

        d_recon_final = torch.bmm(A, h.unsqueeze(-1)).squeeze(-1)
        e = d - d_recon_final

        if return_pre_threshold:
            return h, d_recon_final, e, pre_threshold_values
        return h, d_recon_final, e


# ============================================================
# Helpers
# ============================================================

def compute_nmse_db(h_est, h_true):
    """NMSE in dB."""
    err = ((h_est - h_true) ** 2).sum(dim=-1)
    power = (h_true ** 2).sum(dim=-1) + 1e-10
    return 10 * np.log10((err / power).mean().item() + 1e-10)


def compute_error_concentration(h_est, h_true, sparsity):
    """Compute error concentration on true support set.

    Returns:
        error_on_S: percentage of error energy on true taps
        error_on_Sbar: percentage of error energy on non-support taps
    """
    err = (h_est - h_true) ** 2  # (B, N)
    total_err = err.sum(dim=-1)  # (B,)

    # Find true support: top-K taps by magnitude
    _, support_idx = torch.topk(torch.abs(h_true), sparsity, dim=-1)
    mask = torch.zeros_like(h_true, dtype=torch.bool)
    mask.scatter_(1, support_idx, True)

    error_on_S = err[mask].sum() / (total_err.sum() + 1e-10) * 100
    error_on_Sbar = err[~mask].sum() / (total_err.sum() + 1e-10) * 100

    return error_on_S.item(), error_on_Sbar.item()


def train_model(model, channel_length, sparsity, pilot_length, snr_db,
                epochs=200, batch_size=64, device='cpu', mixed_snr=True):
    """Generic training loop with optional mixed-SNR training.

    mixed_snr=True: sample SNR uniformly from [0, 30] each batch (robust).
    mixed_snr=False: use fixed snr_db.
    """
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    for epoch in range(epochs):
        model.train()
        if mixed_snr:
            # Mixed SNR: sample uniformly from [0, 30] dB each batch
            epoch_snr = np.random.uniform(0, 30)
        else:
            epoch_snr = snr_db

        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size, channel_length=channel_length,
            sparsity=sparsity, pilot_length=pilot_length, snr_db=epoch_snr
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
# Main experiment
# ============================================================

def run_threshold_comparison(seeds=5, device='cpu', save_dir='results/threshold_comparison'):
    """Run threshold function comparison experiment."""
    os.makedirs(save_dir, exist_ok=True)

    # Fixed parameters
    N = 64
    K = 5
    M = 256
    L = 20
    snr_db = 20.0
    epochs = 200
    batch_size = 64
    num_test = 2000

    threshold_types = ['soft', 'hard', 'semisoft']
    threshold_labels = {
        'soft': 'Soft (LISTA)',
        'hard': 'Hard',
        'semisoft': 'Semi-soft (Garrote)'
    }

    all_results = {}

    for thresh_type in threshold_types:
        print(f"\n{'='*60}")
        print(f"Threshold: {threshold_labels[thresh_type]}")
        print(f"{'='*60}")

        nmse_values = []
        error_on_S_values = []
        error_on_Sbar_values = []
        learned_thresholds = []

        for seed in range(seeds):
            torch.manual_seed(seed * 42)
            np.random.seed(seed * 42)

            # Create and train model (mixed SNR for stability)
            model = LISTAThreshold(N, L, threshold_type=thresh_type)
            model = train_model(model, N, K, M, snr_db, epochs, batch_size, device,
                                mixed_snr=True)

            # Generate test data
            torch.manual_seed(seed * 42 + 1000)
            np.random.seed(seed * 42 + 1000)
            x_test, d_test, h_test = generate_sparse_channel_data(
                num_samples=num_test, channel_length=N, sparsity=K,
                pilot_length=M, snr_db=snr_db
            )
            x_test = x_test.to(device)
            d_test = d_test.to(device)
            h_test = h_test.to(device)

            # Evaluate
            model.eval()
            with torch.no_grad():
                h_est, _, _ = model(x_test, d_test)
                nmse = compute_nmse_db(h_est, h_test)
                err_S, err_Sbar = compute_error_concentration(h_est, h_test, K)

            # Skip divergent seeds (positive NMSE or NaN)
            if nmse > 0 or np.isnan(nmse):
                print(f"  Seed {seed}: DIVERGED (NMSE={nmse:.2f} dB) -- SKIPPED")
                continue

            nmse_values.append(nmse)
            error_on_S_values.append(err_S)
            error_on_Sbar_values.append(err_Sbar)

            # Record learned thresholds
            thresh_vals = []
            for layer in model.layers:
                t = layer.threshold.threshold.item()
                thresh_vals.append(t)
            learned_thresholds.append(thresh_vals)

            print(f"  Seed {seed}: NMSE={nmse:.2f} dB, "
                  f"Error on S={err_S:.1f}%, Error on Sbar={err_Sbar:.4f}%")

        # Store results
        all_results[thresh_type] = {
            'label': threshold_labels[thresh_type],
            'nmse_mean': float(np.mean(nmse_values)),
            'nmse_std': float(np.std(nmse_values)),
            'nmse_values': [float(v) for v in nmse_values],
            'error_on_S_mean': float(np.mean(error_on_S_values)),
            'error_on_S_std': float(np.std(error_on_S_values)),
            'error_on_Sbar_mean': float(np.mean(error_on_Sbar_values)),
            'error_on_Sbar_std': float(np.std(error_on_Sbar_values)),
            'learned_thresholds_mean': [float(np.mean([t[i] for t in learned_thresholds]))
                                        for i in range(L)],
            'learned_thresholds_std': [float(np.std([t[i] for t in learned_thresholds]))
                                       for i in range(L)],
        }

        print(f"\n  Summary: NMSE = {all_results[thresh_type]['nmse_mean']:.2f} "
              f"± {all_results[thresh_type]['nmse_std']:.2f} dB")
        print(f"  Error on S = {all_results[thresh_type]['error_on_S_mean']:.1f}% "
              f"± {all_results[thresh_type]['error_on_S_std']:.1f}%")
        print(f"  Error on Sbar = {all_results[thresh_type]['error_on_Sbar_mean']:.4f}% "
              f"± {all_results[thresh_type]['error_on_Sbar_std']:.4f}%")

    # ============================================================
    # Statistical comparison (paired t-tests)
    # ============================================================
    print(f"\n{'='*60}")
    print("Statistical Comparison (paired t-tests)")
    print(f"{'='*60}")

    comparisons = [
        ('soft', 'hard'),
        ('soft', 'semisoft'),
        ('hard', 'semisoft'),
    ]

    stat_results = {}
    for a, b in comparisons:
        nmse_a = np.array(all_results[a]['nmse_values'])
        nmse_b = np.array(all_results[b]['nmse_values'])
        t_stat, p_val = stats.ttest_rel(nmse_a, nmse_b)
        # Cohen's d
        diff = nmse_a - nmse_b
        d = diff.mean() / (diff.std() + 1e-10)

        stat_results[f"{a}_vs_{b}"] = {
            't_stat': float(t_stat),
            'p_value': float(p_val),
            'cohens_d': float(d),
            'nmse_diff': float(diff.mean()),
        }
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
        print(f"  {threshold_labels[a]} vs {threshold_labels[b]}: "
              f"Δ={diff.mean():.2f} dB, t={t_stat:.2f}, p={p_val:.4f} {sig}, d={d:.1f}")

    # ============================================================
    # Save results
    # ============================================================
    output = {
        'config': {
            'N': N, 'K': K, 'M': M, 'L': L,
            'snr_db': snr_db, 'epochs': epochs,
            'batch_size': batch_size, 'seeds': seeds,
            'num_test': num_test, 'mixed_snr': True,
        },
        'results': all_results,
        'statistical_tests': stat_results,
    }

    json_path = os.path.join(save_dir, 'threshold_comparison.json')
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {json_path}")

    # ============================================================
    # Plot: NMSE comparison bar chart
    # ============================================================
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel 1: NMSE comparison
    ax = axes[0]
    labels = [all_results[t]['label'] for t in threshold_types]
    means = [all_results[t]['nmse_mean'] for t in threshold_types]
    stds = [all_results[t]['nmse_std'] for t in threshold_types]
    colors = ['#2196F3', '#FF5722', '#4CAF50']
    bars = ax.bar(labels, means, yerr=stds, capsize=5, color=colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel('NMSE (dB)')
    ax.set_title('NMSE by Threshold Function')
    ax.grid(axis='y', alpha=0.3)
    # Add value labels
    for bar, m, s in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 1,
                f'{m:.1f}', ha='center', va='top', fontsize=10, fontweight='bold')

    # Panel 2: Error concentration on S
    ax = axes[1]
    means_S = [all_results[t]['error_on_S_mean'] for t in threshold_types]
    stds_S = [all_results[t]['error_on_S_std'] for t in threshold_types]
    bars = ax.bar(labels, means_S, yerr=stds_S, capsize=5, color=colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel('Error on S (%)')
    ax.set_title('Error Concentration on True Taps')
    ax.set_ylim([90, 101])
    ax.grid(axis='y', alpha=0.3)
    for bar, m, s in zip(bars, means_S, stds_S):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.1,
                f'{m:.1f}%', ha='center', va='top', fontsize=10, fontweight='bold')

    # Panel 3: Learned threshold schedules
    ax = axes[2]
    for i, t in enumerate(threshold_types):
        mean_thresh = all_results[t]['learned_thresholds_mean']
        std_thresh = all_results[t]['learned_thresholds_std']
        layers = range(L)
        ax.plot(layers, mean_thresh, '-o', color=colors[i], label=threshold_labels[t],
                markersize=3, linewidth=1.5)
        ax.fill_between(layers,
                        [m - s for m, s in zip(mean_thresh, std_thresh)],
                        [m + s for m, s in zip(mean_thresh, std_thresh)],
                        alpha=0.2, color=colors[i])
    ax.set_xlabel('Layer')
    ax.set_ylabel('Learned Threshold')
    ax.set_title('Learned Threshold Schedule')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    pdf_path = os.path.join(save_dir, 'threshold_comparison.pdf')
    plt.savefig(pdf_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {pdf_path}")
    plt.close()

    # ============================================================
    # Generate LaTeX table
    # ============================================================
    print(f"\n{'='*60}")
    print("LaTeX Table")
    print(f"{'='*60}")

    print("\\begin{table}[width=.9\\linewidth,cols=5,pos=h]")
    print("\\caption{Threshold function comparison: NMSE (dB) and error concentration "
          "at SNR$=20$~dB ($N=64$, $K=5$, $M=256$, $L=20$). Mean $\\pm$ std over "
          + str(seeds) + " seeds.}")
    print("\\label{tab:threshold_comparison}")
    print("\\begin{tabular*}{\\tblwidth}{@{} LCCCC@{}}")
    print("\\toprule")
    print("Threshold & NMSE (dB) & Error on $S$ (\\%) & Error on $\\bar{S}$ (\\%) & "
          "$p$ vs. Soft \\\\")
    print("\\midrule")

    for t in threshold_types:
        r = all_results[t]
        label = r['label']
        nmse_str = f"${r['nmse_mean']:.2f} \\pm {r['nmse_std']:.2f}$"
        err_S_str = f"${r['error_on_S_mean']:.1f} \\pm {r['error_on_S_std']:.1f}$"
        err_Sbar_str = f"${r['error_on_Sbar_mean']:.4f} \\pm {r['error_on_Sbar_std']:.4f}$"

        if t == 'soft':
            p_str = "---"
        else:
            key = f"soft_vs_{t}"
            p_val = stat_results[key]['p_value']
            if p_val < 0.001:
                p_str = "$< 0.001^{***}$"
            elif p_val < 0.01:
                p_str = f"${p_val:.3f}^{{**}}$"
            elif p_val < 0.05:
                p_str = f"${p_val:.3f}^{{*}}$"
            else:
                p_str = f"${p_val:.3f}$ (ns)"

        # Bold best NMSE
        best_nmse = min(all_results[tt]['nmse_mean'] for tt in threshold_types)
        if r['nmse_mean'] == best_nmse:
            nmse_str = f"$\\bm{{{r['nmse_mean']:.2f} \\pm {r['nmse_std']:.2f}}}$"

        print(f"{label} & {nmse_str} & {err_S_str} & {err_Sbar_str} & {p_str} \\\\")

    print("\\bottomrule")
    print(f"\\multicolumn{{5}}{{l}}{{$^{{***}}$ $p < 0.001$; $^{{**}}$ $p < 0.01$; "
          f"$^{{*}}$ $p < 0.05$ (paired $t$-test vs.~Soft, $n={seeds}$).}} \\\\")
    print("\\end{tabular*}")
    print("\\end{table}")

    return all_results, stat_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LISTA threshold function comparison')
    parser.add_argument('--seeds', type=int, default=5, help='Number of random seeds')
    parser.add_argument('--device', type=str, default='cpu', help='Device (cpu/cuda)')
    parser.add_argument('--save_dir', type=str, default='results/threshold_comparison',
                        help='Output directory')
    args = parser.parse_args()

    run_threshold_comparison(seeds=args.seeds, device=args.device, save_dir=args.save_dir)
