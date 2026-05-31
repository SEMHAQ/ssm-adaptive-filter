"""
Training script for LISTA (deep-unfolded ISTA) sparse channel estimation.

Compares against OMP, LASSO, LMS, NLMS baselines.
"""

import torch
import torch.optim as optim
import numpy as np
import argparse
import os
import json
import time

from models.ssm_af import LISTA, OMPFilter, LASSOFilter, LMSFilter, NLMSFilter
from data.generate import generate_sparse_channel_data


def compute_nmse(h_est: torch.Tensor, h_true: torch.Tensor) -> float:
    """Normalized MSE: ||h_est - h_true||^2 / ||h_true||^2"""
    err = ((h_est - h_true) ** 2).sum(dim=-1)
    power = (h_true ** 2).sum(dim=-1) + 1e-10
    return (err / power).mean().item()


def compute_nmse_db(h_est: torch.Tensor, h_true: torch.Tensor) -> float:
    """NMSE in dB."""
    return 10 * np.log10(compute_nmse(h_est, h_true) + 1e-10)


def train_lista(
    channel_length: int = 64,
    sparsity: int = 5,
    num_layers: int = 20,
    pilot_length: int = 256,
    snr_db: float = 20.0,
    epochs: int = 200,
    batch_size: int = 64,
    lr: float = 1e-3,
    device: str = 'cuda',
    save_dir: str = 'res'
):
    """Train LISTA model."""
    task_dir = os.path.join(save_dir, 'sparse_channel')
    ckpt_dir = os.path.join(task_dir, 'checkpoints')
    os.makedirs(ckpt_dir, exist_ok=True)
    device = torch.device(device if torch.cuda.is_available() else 'cpu')

    # Model
    model = LISTA(channel_length=channel_length, num_layers=num_layers).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Training on: {device}")
    print(f"Config: N={channel_length}, K={sparsity}, L={num_layers}, "
          f"pilot={pilot_length}, SNR={snr_db}dB, epochs={epochs}, batch={batch_size}")
    print(f"{'='*60}")

    best_loss = float('inf')
    history = {'train_loss': [], 'val_loss': []}

    for epoch in range(epochs):
        model.train()
        t_start = time.time()

        # Generate training data
        x, d, h = generate_sparse_channel_data(
            num_samples=batch_size,
            channel_length=channel_length,
            sparsity=sparsity,
            pilot_length=pilot_length,
            snr_db=snr_db
        )
        x, d, h = x.to(device), d.to(device), h.to(device)

        # Forward
        h_est, d_recon, e = model(x, d)

        # Loss: NMSE on channel estimation
        loss = torch.mean((h_est - h) ** 2) / (torch.mean(h ** 2) + 1e-10)

        # Check NaN
        if torch.isnan(loss):
            print(f"Epoch {epoch+1:3d}/{epochs} | NaN loss, skipping")
            continue

        # Backward
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()
        scheduler.step()

        nmse_db = 10 * torch.log10(loss + 1e-10).item()
        history['train_loss'].append(nmse_db)

        elapsed = time.time() - t_start
        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"Epoch {epoch+1:3d}/{epochs} | NMSE: {nmse_db:7.2f} dB | {elapsed:.1f}s")

        # Save best
        if loss.item() < best_loss:
            best_loss = loss.item()
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'loss': best_loss,
            }, os.path.join(ckpt_dir, 'best.pt'))

    # Save final
    torch.save(model.state_dict(), os.path.join(ckpt_dir, 'final.pt'))

    # Save metrics
    summary = {
        'task': 'sparse_channel',
        'config': {
            'channel_length': channel_length, 'sparsity': sparsity,
            'num_layers': num_layers, 'pilot_length': pilot_length,
            'snr_db': snr_db, 'epochs': epochs, 'lr': lr,
        },
        'final_nmse_db': history['train_loss'][-1] if history['train_loss'] else None,
        'best_loss': best_loss,
        'history': history,
    }
    os.makedirs(os.path.join('results', 'sparse_channel'), exist_ok=True)
    with open(os.path.join('results', 'sparse_channel', 'metrics.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nTraining complete. Best NMSE: {10*np.log10(best_loss+1e-10):.2f} dB")
    return model, history


def evaluate_baselines(channel_length=64, sparsity=5, pilot_length=128,
                       snr_db=20.0, num_test=100):
    """Evaluate classical baselines on test data."""
    from data.generate import generate_sparse_channel_data

    torch.manual_seed(123)
    x, d, h = generate_sparse_channel_data(
        num_samples=num_test, channel_length=channel_length,
        sparsity=sparsity, pilot_length=pilot_length, snr_db=snr_db
    )

    results = {}

    # LMS (online, run per sample)
    lms = LMSFilter(channel_length, mu=0.01)
    h_lms_list = []
    for i in range(num_test):
        _, e_lms = lms.process(x[i], d[i])
        # LMS final weights as channel estimate
        # Run again to get weights (hack: use the error to reconstruct)
        w = np.zeros(channel_length)
        x_buf = np.zeros(channel_length)
        x_np = x[i].numpy()
        d_np = d[i].numpy()
        for n in range(len(x_np)):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x_np[n]
            y_n = np.dot(w, x_buf)
            e_n = d_np[n] - y_n
            w = w + 0.01 * e_n * x_buf
        h_lms_list.append(torch.tensor(w))
    h_lms = torch.stack(h_lms_list)
    nmse_lms = compute_nmse_db(h_lms, h)
    results['LMS'] = nmse_lms
    print(f"LMS:     NMSE = {nmse_lms:.2f} dB")

    # NLMS
    h_nlms_list = []
    for i in range(num_test):
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
            w = w + (0.5 / norm) * e_n * x_buf
        h_nlms_list.append(torch.tensor(w))
    h_nlms = torch.stack(h_nlms_list)
    nmse_nlms = compute_nmse_db(h_nlms, h)
    results['NLMS'] = nmse_nlms
    print(f"NLMS:    NMSE = {nmse_nlms:.2f} dB")

    # OMP
    omp = OMPFilter(channel_length, sparsity)
    h_omp_list = [omp.estimate(x[i], d[i]) for i in range(num_test)]
    h_omp = torch.stack(h_omp_list)
    nmse_omp = compute_nmse_db(h_omp, h)
    results['OMP'] = nmse_omp
    print(f"OMP:     NMSE = {nmse_omp:.2f} dB")

    # LASSO
    lasso = LASSOFilter(channel_length, lam=0.01)
    h_lasso_list = [lasso.estimate(x[i], d[i]) for i in range(num_test)]
    h_lasso = torch.stack(h_lasso_list)
    nmse_lasso = compute_nmse_db(h_lasso, h)
    results['LASSO'] = nmse_lasso
    print(f"LASSO:   NMSE = {nmse_lasso:.2f} dB")

    return results


def main():
    parser = argparse.ArgumentParser(description='Train LISTA for sparse channel estimation')
    parser.add_argument('--channel_length', type=int, default=64)
    parser.add_argument('--sparsity', type=int, default=5)
    parser.add_argument('--num_layers', type=int, default=20)
    parser.add_argument('--pilot_length', type=int, default=256)
    parser.add_argument('--snr_db', type=float, default=20.0)
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--save_dir', type=str, default='res')

    args = parser.parse_args()

    # Train LISTA
    model, history = train_lista(
        channel_length=args.channel_length,
        sparsity=args.sparsity,
        num_layers=args.num_layers,
        pilot_length=args.pilot_length,
        snr_db=args.snr_db,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
        save_dir=args.save_dir
    )

    # Evaluate baselines
    baseline_results = evaluate_baselines(
        channel_length=args.channel_length,
        sparsity=args.sparsity,
        pilot_length=args.pilot_length,
        snr_db=args.snr_db,
        num_test=100
    )

    # Evaluate LISTA on test data
    torch.manual_seed(123)
    from data.generate import generate_sparse_channel_data
    x_test, d_test, h_test = generate_sparse_channel_data(
        num_samples=100, channel_length=args.channel_length,
        sparsity=args.sparsity, pilot_length=args.pilot_length,
        snr_db=args.snr_db
    )
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    model.eval()
    with torch.no_grad():
        h_lista, _, _ = model(x_test.to(device), d_test.to(device))
    nmse_lista = compute_nmse_db(h_lista.cpu(), h_test)
    print(f"LISTA:   NMSE = {nmse_lista:.2f} dB")
    baseline_results['LISTA'] = nmse_lista

    # Save all results
    all_results = {
        'task': 'sparse_channel',
        'config': vars(args),
        'results': baseline_results,
    }
    os.makedirs(os.path.join('results', 'sparse_channel'), exist_ok=True)
    with open(os.path.join('results', 'sparse_channel', 'eval_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults: {baseline_results}")


if __name__ == '__main__':
    main()
