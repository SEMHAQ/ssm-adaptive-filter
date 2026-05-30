"""
Training script for SSM-AF model.

Trains on echo cancellation, channel equalization, or noise reduction tasks.
Compares against LMS, NLMS, RLS baselines.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import argparse
import os
import json
import time
from pathlib import Path

from models.ssm_af import SSMAF, LMSFilter, NLMSFilter, RLSFilter, HybridNLMSNN, TCNFilter
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


def compute_metrics(y_pred: torch.Tensor, y_true: torch.Tensor, d: torch.Tensor) -> dict:
    """Compute evaluation metrics."""
    # MSE in dB
    mse = torch.mean((y_true - y_pred) ** 2)
    mse_db = 10 * torch.log10(mse + 1e-10)

    # Misadjustment
    excess_mse = mse - torch.min(torch.mean(y_true ** 2), torch.mean(d ** 2))

    return {
        'mse_db': mse_db.item(),
        'mse_linear': mse.item(),
    }


def compute_erle(d: torch.Tensor, e: torch.Tensor) -> float:
    """Compute Echo Return Loss Enhancement."""
    erle = 10 * torch.log10(
        torch.mean(d ** 2) / (torch.mean(e ** 2) + 1e-10) + 1e-10
    )
    return erle.item()


def train_ssm_af(
    task: str,
    filter_length: int = 64,
    hidden_dim: int = 32,
    epochs: int = 100,
    batch_size: int = 4,
    seq_len: int = 1000,
    lr: float = 3e-4,
    device: str = 'cuda',
    save_dir: str = 'res'
):
    """Train SSM-AF model."""
    task_dir = os.path.join(save_dir, task)
    fig_dir = os.path.join(task_dir, 'figures')
    ckpt_dir = os.path.join(task_dir, 'checkpoints')
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(ckpt_dir, exist_ok=True)
    device = torch.device(device if torch.cuda.is_available() else 'cpu')

    # Initialize model
    if task == 'loudspeaker_echo':
        model = TCNFilter(
            filter_length=filter_length,
            hidden_dim=hidden_dim,
            num_blocks=3,
            kernel_size=3
        ).to(device)
    else:
        model = SSMAF(
            filter_length=filter_length,
            hidden_dim=hidden_dim
        ).to(device)

    if task == 'loudspeaker_echo':
        # Higher LR for NN component - it needs to learn fast before NLMS adapts
        optimizer = optim.Adam(model.parameters(), lr=1e-2, weight_decay=1e-4)
    else:
        optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)

    # Learning rate scheduler with warmup
    warmup_epochs = min(10, epochs // 5)
    def lr_lambda(epoch):
        if epoch < warmup_epochs:
            return (epoch + 1) / warmup_epochs  # Linear warmup
        else:
            progress = (epoch - warmup_epochs) / (epochs - warmup_epochs)
            return 0.5 * (1 + np.cos(np.pi * progress))  # Cosine decay
    scheduler = optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Training on: {device}")
    print(f"Task: {task}")
    print(f"Config: epochs={epochs}, batch={batch_size}, seq_len={seq_len}, filter_len={filter_length}")
    print(f"{'='*60}")

    best_loss = float('inf')
    history = {'train_loss': [], 'val_loss': []}

    # For loudspeaker_echo: fixed echo path + fixed dataset
    # Real scenario: one room, one device, offline training
    if task == 'loudspeaker_echo':
        num_train_samples = 32
        # Generate ONE fixed echo path (deterministic seed)
        torch.manual_seed(42)
        h_fixed = _generate_itu_echo_path(1, filter_length).to(device)
        # Generate data with the SAME echo path every time
        x_fixed_list, d_fixed_list = [], []
        for _ in range(num_train_samples):
            x_i = torch.randn(1, seq_len).to(device)
            # Linear convolution with fixed path
            x_conv = torch.nn.functional.conv1d(
                x_i.unsqueeze(0), h_fixed.unsqueeze(0), padding=filter_length - 1
            ).squeeze()[:seq_len]
            # Nonlinear: soft clipping
            d_i = torch.tanh(x_conv * 10.0)
            x_fixed_list.append(x_i.squeeze())
            d_fixed_list.append(d_i)
        x_fixed = torch.stack(x_fixed_list)
        d_fixed = torch.stack(d_fixed_list)
        print(f"Fixed echo path, {num_train_samples} samples, soft_clip gain=10")

    for epoch in range(epochs):
        model.train()
        t_start = time.time()

        # Generate training data (on-the-fly)
        if task == 'echo_cancellation':
            x, d, h = generate_echo_cancellation_data(
                num_samples=batch_size, seq_len=seq_len,
                filter_length=filter_length
            )
        elif task == 'channel_equalization':
            x, d, ch = generate_channel_equalization_data(
                num_samples=batch_size, seq_len=seq_len
            )
        elif task == 'noise_reduction':
            x, d, s = generate_noise_reduction_data(
                num_samples=batch_size, seq_len=seq_len
            )
        elif task == 'nonstationary_echo':
            x, d, h_list = generate_nonstationary_echo_data(
                num_samples=batch_size, seq_len=seq_len,
                filter_length=filter_length, num_changes=10
            )
        elif task == 'robust_echo':
            x, d, h = generate_robust_echo_data(
                num_samples=batch_size, seq_len=seq_len,
                filter_length=filter_length, noise_type='colored'
            )
        elif task == 'nonlinear_echo':
            x, d, h = generate_nonlinear_echo_data(
                num_samples=batch_size, seq_len=seq_len,
                filter_length=filter_length, nonlinearity='pure_nonlinear'
            )
        elif task == 'loudspeaker_echo':
            # Use random subset from fixed dataset
            idx = torch.randperm(num_train_samples)[:batch_size]
            x, d = x_fixed[idx], d_fixed[idx]
        else:
            raise ValueError(f"Unknown task: {task}")

        x, d = x.to(device), d.to(device)

        # Forward pass
        y, e, w_history = model(x, d)

        # Check for NaN in output
        if torch.isnan(y).any() or torch.isnan(e).any():
            print(f"Epoch {epoch+1:3d}/{epochs} | NaN detected in output, skipping update")
            continue

        # Loss: MSE of error signal
        loss = torch.mean(e ** 2)

        # Check for NaN loss
        if torch.isnan(loss):
            print(f"Epoch {epoch+1:3d}/{epochs} | NaN loss, skipping update")
            continue

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
        optimizer.step()
        scheduler.step()

        # Compute metrics
        with torch.no_grad():
            mse_db = 10 * torch.log10(loss + 1e-10).item()
            erle = compute_erle(d, e)

        elapsed = time.time() - t_start
        history['train_loss'].append(mse_db)

        # Print every epoch so user can see progress
        print(f"Epoch {epoch+1:3d}/{epochs} | MSE: {mse_db:7.2f} dB | ERLE: {erle:7.2f} dB | {elapsed:.1f}s")

        # Save best model
        if loss.item() < best_loss:
            best_loss = loss.item()
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': best_loss,
            }, os.path.join(ckpt_dir, 'best.pt'))

    # Save final model
    torch.save(model.state_dict(), os.path.join(ckpt_dir, 'final.pt'))

    # Save training config and final metrics
    summary = {
        'task': task,
        'config': {
            'filter_length': filter_length, 'hidden_dim': hidden_dim,
            'epochs': epochs, 'batch_size': batch_size, 'seq_len': seq_len, 'lr': lr,
        },
        'final_mse_db': history['train_loss'][-1] if history['train_loss'] else None,
        'best_loss': best_loss,
        'history': history,
    }
    with open(os.path.join(task_dir, 'metrics.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Save lightweight results to tracked directory (no checkpoints)
    results_dir = os.path.join('results', task)
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, 'metrics.json'), 'w') as f:
        json.dump({
            'task': task,
            'final_mse_db': summary['final_mse_db'],
            'best_loss': best_loss,
            'history': history,
        }, f, indent=2)

    print(f"\nTraining complete. Results saved to {task_dir}/")
    return model, history


def evaluate_baselines(task: str, filter_length: int = 64, seq_len: int = 4000):
    """Evaluate classical adaptive filter baselines."""
    print("\n=== Baseline Evaluation ===")

    # Generate test data
    if task == 'echo_cancellation':
        x, d, h = generate_echo_cancellation_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length
        )
    elif task == 'channel_equalization':
        x, d, ch = generate_channel_equalization_data(
            num_samples=1, seq_len=seq_len
        )
    elif task == 'noise_reduction':
        x, d, s = generate_noise_reduction_data(
            num_samples=1, seq_len=seq_len
        )
    elif task == 'nonstationary_echo':
        x, d, h_list = generate_nonstationary_echo_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length,
            num_changes=3
        )
    elif task == 'robust_echo':
        x, d, h = generate_robust_echo_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length,
            noise_type='colored'
        )
    elif task == 'nonlinear_echo':
        x, d, h = generate_nonlinear_echo_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length,
            nonlinearity='pure_nonlinear'
        )
    elif task == 'loudspeaker_echo':
        x, d, h = generate_loudspeaker_echo_data(
            num_samples=1, seq_len=seq_len, filter_length=filter_length,
            nl_type='soft_clip', nl_params={'gain': 10.0}
        )
    else:
        raise ValueError(f"Unknown task: {task}")

    x_np = x.squeeze().numpy()
    d_np = d.squeeze().numpy()

    results = {}

    # LMS
    lms = LMSFilter(filter_length, mu=0.01)
    y_lms, e_lms = lms.process(x.squeeze(), d.squeeze())
    mse_lms = 10 * np.log10(np.mean(e_lms.numpy() ** 2) + 1e-10)
    erle_lms = 10 * np.log10(np.mean(d_np ** 2) / (np.mean(e_lms.numpy() ** 2) + 1e-10))
    results['LMS'] = {'mse_db': mse_lms, 'erle_db': erle_lms}
    print(f"LMS:     MSE = {mse_lms:.2f} dB, ERLE = {erle_lms:.2f} dB")

    # NLMS
    nlms = NLMSFilter(filter_length, mu=0.5)
    y_nlms, e_nlms = nlms.process(x.squeeze(), d.squeeze())
    mse_nlms = 10 * np.log10(np.mean(e_nlms.numpy() ** 2) + 1e-10)
    erle_nlms = 10 * np.log10(np.mean(d_np ** 2) / (np.mean(e_nlms.numpy() ** 2) + 1e-10))
    results['NLMS'] = {'mse_db': mse_nlms, 'erle_db': erle_nlms}
    print(f"NLMS:    MSE = {mse_nlms:.2f} dB, ERLE = {erle_nlms:.2f} dB")

    # RLS
    rls = RLSFilter(filter_length, lam=0.99)
    y_rls, e_rls = rls.process(x.squeeze(), d.squeeze())
    mse_rls = 10 * np.log10(np.mean(e_rls.numpy() ** 2) + 1e-10)
    erle_rls = 10 * np.log10(np.mean(d_np ** 2) / (np.mean(e_rls.numpy() ** 2) + 1e-10))
    results['RLS'] = {'mse_db': mse_rls, 'erle_db': erle_rls}
    print(f"RLS:     MSE = {mse_rls:.2f} dB, ERLE = {erle_rls:.2f} dB")

    return results


def main():
    parser = argparse.ArgumentParser(description='Train SSM-AF model')
    parser.add_argument('--task', type=str, default='echo_cancellation',
                        choices=['echo_cancellation', 'channel_equalization', 'noise_reduction',
                                 'nonstationary_echo', 'robust_echo', 'nonlinear_echo', 'loudspeaker_echo'],
                        help='Adaptive filtering task')
    parser.add_argument('--filter_length', type=int, default=64, help='Filter length')
    parser.add_argument('--hidden_dim', type=int, default=32, help='Hidden dimension')
    parser.add_argument('--epochs', type=int, default=100, help='Training epochs')
    parser.add_argument('--batch_size', type=int, default=4, help='Batch size')
    parser.add_argument('--seq_len', type=int, default=1000, help='Sequence length')
    parser.add_argument('--lr', type=float, default=3e-4, help='Learning rate')
    parser.add_argument('--device', type=str, default='cuda', help='Device')
    parser.add_argument('--save_dir', type=str, default='res', help='Save directory')

    args = parser.parse_args()

    # Train SSM-AF
    model, history = train_ssm_af(
        task=args.task,
        filter_length=args.filter_length,
        hidden_dim=args.hidden_dim,
        epochs=args.epochs,
        batch_size=args.batch_size,
        seq_len=args.seq_len,
        lr=args.lr,
        device=args.device,
        save_dir=args.save_dir
    )

    # Evaluate baselines
    baseline_results = evaluate_baselines(
        task=args.task,
        filter_length=args.filter_length,
        seq_len=args.seq_len
    )

    # Save all results
    all_results = {
        'task': args.task,
        'baselines': baseline_results,
        'config': vars(args)
    }
    with open(os.path.join(args.save_dir, f'results_{args.task}.json'), 'w') as f:
        json.dump(all_results, f, indent=2)


if __name__ == '__main__':
    main()
