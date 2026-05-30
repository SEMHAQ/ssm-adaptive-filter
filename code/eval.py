"""
Evaluation script for SSM-AF paper.

Generates:
1. Convergence curves (MSE vs. iteration)
2. Performance comparison tables
3. Filter coefficient evolution plots
4. Computational complexity analysis
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
import os
from pathlib import Path

from models.ssm_af import SSMAF, LMSFilter, NLMSFilter, RLSFilter, TCNFilter
from data.generate import (
    generate_echo_cancellation_data,
    generate_channel_equalization_data,
    generate_noise_reduction_data,
    generate_nonstationary_echo_data,
    generate_robust_echo_data,
    generate_nonlinear_echo_data,
    generate_loudspeaker_echo_data,
    _generate_itu_echo_path
)


def plot_convergence_curves(results: dict, save_path: str):
    """Plot MSE convergence curves for all methods."""
    plt.figure(figsize=(10, 6))

    for method, data in results.items():
        mse_curve = data['mse_curve']
        # Smooth the curve
        window = 100
        if len(mse_curve) > window:
            smoothed = np.convolve(mse_curve, np.ones(window)/window, mode='valid')
            plt.plot(smoothed, label=method, linewidth=1.5)
        else:
            plt.plot(mse_curve, label=method, linewidth=1.5)

    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('MSE (dB)', fontsize=12)
    plt.title('Convergence Comparison', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved convergence plot to {save_path}")


def plot_erle_comparison(results: dict, save_path: str):
    """Plot ERLE bar chart comparison."""
    methods = list(results.keys())
    erle_values = [results[m]['erle_db'] for m in methods]

    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']
    plt.figure(figsize=(8, 5))
    bars = plt.bar(methods, erle_values, color=colors[:len(methods)], alpha=0.8)

    # Add value labels
    for bar, val in zip(bars, erle_values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.1f}', ha='center', va='bottom', fontsize=11)

    plt.ylabel('ERLE (dB)', fontsize=12)
    plt.title('Echo Return Loss Enhancement Comparison', fontsize=14)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved ERLE plot to {save_path}")


def plot_filter_coefficients(w_history: np.ndarray, w_true: np.ndarray, save_path: str, title: str = 'Filter Coefficients'):
    """Plot filter coefficient evolution."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Coefficient evolution heatmap
    ax = axes[0]
    im = ax.imshow(w_history.T, aspect='auto', cmap='RdBu_r',
                   vmin=-np.max(np.abs(w_history)), vmax=np.max(np.abs(w_history)))
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Tap Index', fontsize=12)
    ax.set_title(f'{title} Evolution', fontsize=14)
    plt.colorbar(im, ax=ax)

    # Final coefficients vs true
    ax = axes[1]
    ax.plot(w_true, 'b-', linewidth=2, label='True', alpha=0.8)
    ax.plot(w_history[-1], 'r--', linewidth=2, label='Estimated', alpha=0.8)
    ax.set_xlabel('Tap Index', fontsize=12)
    ax.set_ylabel('Coefficient Value', fontsize=12)
    ax.set_title('Final Coefficients vs True', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved coefficient plot to {save_path}")


def compute_complexity(model: SSMAF, filter_length: int, seq_len: int) -> dict:
    """Compute computational complexity metrics."""
    device = next(model.parameters()).device

    # Count parameters
    num_params = sum(p.numel() for p in model.parameters())

    # Measure inference time
    x = torch.randn(1, seq_len).to(device)
    d = torch.randn(1, seq_len).to(device)

    # Warmup
    with torch.no_grad():
        for _ in range(3):
            model(x, d)

    # Measure
    import time
    if device.type == 'cuda':
        torch.cuda.synchronize()
    start = time.time()
    with torch.no_grad():
        for _ in range(10):
            model(x, d)
    if device.type == 'cuda':
        torch.cuda.synchronize()
    elapsed = (time.time() - start) / 10

    return {
        'num_params': num_params,
        'time_per_sample_ms': elapsed / seq_len * 1000,
        'total_time_s': elapsed,
        'throughput_samples_per_sec': seq_len / elapsed
    }


def run_evaluation(task: str, filter_length: int = 64, seq_len: int = 8000,
                   checkpoint: str = None, device: str = 'cpu', save_dir: str = 'res'):
    """Run full evaluation for a given task."""
    task_dir = os.path.join(save_dir, task)
    fig_dir = os.path.join(task_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    device = torch.device(device)

    print(f"\n{'='*60}")
    print(f"  Evaluation: {task}")
    print(f"{'='*60}")

    # Generate test data
    if task == 'echo_cancellation':
        x, d, h = generate_echo_cancellation_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length
        )
        w_true = h.squeeze().numpy()
        num_changes = 0
    elif task == 'channel_equalization':
        x, d, ch = generate_channel_equalization_data(
            num_samples=1, seq_len=seq_len
        )
        w_true = ch.squeeze().numpy()
        num_changes = 0
    elif task == 'noise_reduction':
        x, d, s = generate_noise_reduction_data(
            num_samples=1, seq_len=seq_len
        )
        w_true = None
        num_changes = 0
    elif task == 'nonstationary_echo':
        x, d, h_list = generate_nonstationary_echo_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length,
            num_changes=10
        )
        w_true = h_list[0].squeeze().numpy()  # First segment's echo path
        num_changes = 10
    elif task == 'robust_echo':
        x, d, h = generate_robust_echo_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length,
            noise_type='colored'
        )
        w_true = h.squeeze().numpy()
        num_changes = 0
    elif task == 'nonlinear_echo':
        x, d, h = generate_nonlinear_echo_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length,
            nonlinearity='pure_nonlinear'
        )
        w_true = h.squeeze().numpy()
        num_changes = 0
    elif task == 'loudspeaker_echo':
        # Use same fixed echo path as training (same seed)
        torch.manual_seed(42)
        h = _generate_itu_echo_path(1, filter_length).to(device)
        torch.manual_seed(123)  # Different seed for x (unseen data)
        x_1d = torch.randn(seq_len).to(device)
        x_conv = torch.nn.functional.conv1d(
            x_1d.unsqueeze(0).unsqueeze(0), h.squeeze().unsqueeze(0).unsqueeze(0),
            padding=filter_length - 1
        ).squeeze()[:seq_len]
        d = torch.tanh(x_conv * 3.0).unsqueeze(0)  # (1, seq_len)
        x = x_1d.unsqueeze(0)  # (1, seq_len) - 2D
        # Move to CPU for baselines (numpy requires CPU)
        x, d = x.cpu(), d.cpu()
        w_true = h.squeeze().cpu().numpy()
        num_changes = 0
    else:
        raise ValueError(f"Unknown task: {task}")

    results = {}

    # --- LMS ---
    print("\nEvaluating LMS...")
    lms = LMSFilter(filter_length, mu=0.01)
    y_lms, e_lms = lms.process(x.squeeze(), d.squeeze())
    mse_lms = 10 * np.log10(np.cumsum(e_lms.numpy()**2) / np.arange(1, seq_len+1) + 1e-10)
    erle_lms = 10 * np.log10(np.mean(d.numpy()**2) / (np.mean(e_lms.numpy()**2) + 1e-10))
    results['LMS'] = {'mse_curve': mse_lms, 'erle_db': erle_lms, 'final_mse_db': mse_lms[-1]}

    # --- NLMS ---
    print("Evaluating NLMS...")
    nlms = NLMSFilter(filter_length, mu=0.5)
    y_nlms, e_nlms = nlms.process(x.squeeze(), d.squeeze())
    mse_nlms = 10 * np.log10(np.cumsum(e_nlms.numpy()**2) / np.arange(1, seq_len+1) + 1e-10)
    erle_nlms = 10 * np.log10(np.mean(d.numpy()**2) / (np.mean(e_nlms.numpy()**2) + 1e-10))
    results['NLMS'] = {'mse_curve': mse_nlms, 'erle_db': erle_nlms, 'final_mse_db': mse_nlms[-1]}

    # --- RLS ---
    print("Evaluating RLS...")
    rls = RLSFilter(filter_length, lam=0.99)
    y_rls, e_rls = rls.process(x.squeeze(), d.squeeze())
    mse_rls = 10 * np.log10(np.cumsum(e_rls.numpy()**2) / np.arange(1, seq_len+1) + 1e-10)
    erle_rls = 10 * np.log10(np.mean(d.numpy()**2) / (np.mean(e_rls.numpy()**2) + 1e-10))
    results['RLS'] = {'mse_curve': mse_rls, 'erle_db': erle_rls, 'final_mse_db': mse_rls[-1]}

    # --- SSM-AF / NLMS+TCN ---
    if task == 'loudspeaker_echo':
        print("Evaluating NLMS + TCN residual...")
        model = TCNFilter(filter_length=filter_length, hidden_dim=32, num_blocks=3).to(device)
        method_name = 'NLMS+TCN'
    else:
        print("Evaluating SSM-AF...")
        model = SSMAF(filter_length=filter_length, hidden_dim=64).to(device)
        method_name = 'SSM-AF'
    if checkpoint and os.path.exists(checkpoint):
        ckpt = torch.load(checkpoint, map_location=device, weights_only=False)
        try:
            if 'model_state_dict' in ckpt:
                model.load_state_dict(ckpt['model_state_dict'])
            else:
                model.load_state_dict(ckpt)
            print(f"  Loaded checkpoint: {checkpoint}")
        except RuntimeError as e:
            print(f"  Warning: Checkpoint incompatible (architecture changed), using random weights")
            print(f"  {e}")

    if task == 'loudspeaker_echo':
        # Two-stage: NLMS for linear + TCN for nonlinear residual
        nlms = NLMSFilter(filter_length, mu=0.5)
        y_nlms_eval, e_nlms_eval = nlms.process(x.squeeze(), d.squeeze())
        # TCN predicts nonlinear residual
        x_dev = x.to(device)
        with torch.no_grad():
            y_tcn_res, _, _ = model(x_dev, torch.zeros_like(x_dev))  # d=0, predict residual
        # Combine: y_total = y_nlms + y_tcn_residual
        y_total = y_nlms_eval + y_tcn_res.squeeze().cpu()
        e_total = d.squeeze() - y_total
        e_np = e_total.numpy()
        mse_curve = 10 * np.log10(np.cumsum(e_np**2) / np.arange(1, seq_len+1) + 1e-10)
        erle_val = 10 * np.log10(np.mean(d.numpy()**2) / (np.mean(e_np**2) + 1e-10))
        results[method_name] = {'mse_curve': mse_curve, 'erle_db': erle_val, 'final_mse_db': mse_curve[-1]}
    else:
        x_dev, d_dev = x.to(device), d.to(device)
        with torch.no_grad():
            y_ssm, e_ssm, w_hist = model(x_dev, d_dev)
        e_ssm_np = e_ssm.squeeze().cpu().numpy()
        mse_ssm = 10 * np.log10(np.cumsum(e_ssm_np**2) / np.arange(1, seq_len+1) + 1e-10)
        erle_ssm = 10 * np.log10(np.mean(d.numpy()**2) / (np.mean(e_ssm_np**2) + 1e-10))
        results[method_name] = {'mse_curve': mse_ssm, 'erle_db': erle_ssm, 'final_mse_db': mse_ssm[-1]}

    # Print summary table
    print(f"\n{'='*60}")
    print(f"  Results Summary: {task}")
    print(f"{'='*60}")
    print(f"{'Method':<12} {'MSE (dB)':<12} {'ERLE (dB)':<12}")
    print(f"{'-'*36}")
    for method, data in results.items():
        print(f"{method:<12} {data['final_mse_db']:<12.2f} {data['erle_db']:<12.2f}")

    # Generate plots
    plot_convergence_curves(results, os.path.join(fig_dir, 'convergence.pdf'))
    plot_erle_comparison(results, os.path.join(fig_dir, 'erle.pdf'))

    if w_true is not None and 'w_hist' in locals() and w_hist is not None:
        plot_filter_coefficients(
            w_hist.squeeze().cpu().numpy(),
            w_true,
            os.path.join(fig_dir, 'coefficients.pdf'),
            title=f'{task.replace("_", " ").title()}'
        )

    # Save results
    results_save = {k: {'erle_db': v['erle_db'], 'final_mse_db': v['final_mse_db']} for k, v in results.items()}

    # For non-stationary task, compute per-segment MSE to show tracking ability
    if task == 'nonstationary_echo' and num_changes > 0:
        segment_len = seq_len // (num_changes + 1)
        segment_results = {}
        for method, data in results.items():
            mse_curve = data['mse_curve']
            segment_mse = []
            for seg_idx in range(num_changes + 1):
                start = seg_idx * segment_len
                end = min((seg_idx + 1) * segment_len, len(mse_curve))
                if start < len(mse_curve):
                    seg_mse = mse_curve[end - 1]  # Final MSE of this segment
                    segment_mse.append(float(seg_mse))
            segment_results[method] = segment_mse
        results_save['per_segment_mse'] = segment_results

    with open(os.path.join(task_dir, 'eval_results.json'), 'w') as f:
        json.dump(results_save, f, indent=2)

    # Also save to tracked results/ directory
    results_dir = os.path.join('results', task)
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, 'eval_results.json'), 'w') as f:
        json.dump(results_save, f, indent=2)

    print(f"\nResults saved to {task_dir}/ and {results_dir}/")
    return results


def main():
    parser = argparse.ArgumentParser(description='Evaluate SSM-AF model')
    parser.add_argument('--task', type=str, default='all',
                        choices=['echo_cancellation', 'channel_equalization', 'noise_reduction',
                                 'nonstationary_echo', 'robust_echo', 'nonlinear_echo', 'loudspeaker_echo', 'all'])
    parser.add_argument('--filter_length', type=int, default=64)
    parser.add_argument('--seq_len', type=int, default=8000)
    parser.add_argument('--checkpoint', type=str, default=None)
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--save_dir', type=str, default='res')

    args = parser.parse_args()

    tasks = ['echo_cancellation', 'channel_equalization', 'noise_reduction', 'nonstationary_echo', 'robust_echo', 'nonlinear_echo', 'loudspeaker_echo'] if args.task == 'all' else [args.task]

    all_results = {}
    for task in tasks:
        ckpt = args.checkpoint or os.path.join(args.save_dir, task, 'checkpoints', 'best.pt')
        all_results[task] = run_evaluation(
            task=task,
            filter_length=args.filter_length,
            seq_len=args.seq_len,
            checkpoint=ckpt,
            device=args.device,
            save_dir=args.save_dir
        )

    print("\n\nAll evaluations complete!")


if __name__ == '__main__':
    main()
