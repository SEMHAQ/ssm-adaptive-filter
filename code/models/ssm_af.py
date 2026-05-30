"""
SSM-AF: State Space Model based Adaptive Filter (v7 - Change Detection)

NLMS with explicit change detection + learned step size.

Key innovation: Two-tier adaptation:
1. Change detector monitors error variance ratio (recent vs long-term)
2. When change detected, step size increases dramatically for fast re-convergence
3. When converged, learned step size minimizes steady-state error

This directly addresses the non-stationary tracking problem.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class ChangeDetector(nn.Module):
    """
    Detects echo path changes by monitoring error statistics.

    Computes ratio of short-term to long-term error power.
    When echo path changes, short-term error spikes -> ratio > 1.

    This is differentiable and can be trained end-to-end.
    """

    def __init__(self, short_window: int = 8, long_window: int = 64):
        super().__init__()
        self.short_window = short_window
        self.long_window = long_window

        # Learnable thresholds and sensitivities
        self.sensitivity = nn.Parameter(torch.tensor(2.0))
        self.threshold = nn.Parameter(torch.tensor(1.5))

    def forward(self, e_history):
        """
        Args:
            e_history: (B, long_window) - error history
        Returns:
            change_score: (B, 1) - change probability in [0, 1]
        """
        # Short-term power (recent errors)
        short_power = (e_history[:, :self.short_window] ** 2).mean(dim=-1, keepdim=True)

        # Long-term power (all errors)
        long_power = (e_history ** 2).mean(dim=-1, keepdim=True) + 1e-8

        # Ratio: >1 means error is increasing (possible change)
        ratio = short_power / long_power

        # Soft thresholding with learnable parameters
        change_score = torch.sigmoid(self.sensitivity * (ratio - self.threshold))

        return change_score


class StepSizeNet(nn.Module):
    """
    Predicts adaptive step size from signal context and error history.

    Combines:
    - Change detection (explicit ratio-based)
    - Learned patterns (MLP on error history)
    - Current signal state
    """

    def __init__(self, filter_length: int, context_len: int = 64, hidden_dim: int = 32):
        super().__init__()
        self.context_len = context_len

        # Change detector (explicit)
        self.change_detector = ChangeDetector(
            short_window=8,
            long_window=context_len
        )

        # Error pattern encoder
        self.error_encoder = nn.Sequential(
            nn.Linear(context_len, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
        )

        # Signal features encoder
        self.signal_encoder = nn.Sequential(
            nn.Linear(filter_length + 1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
        )

        # Step size predictor (takes all features + change score)
        self.predictor = nn.Sequential(
            nn.Linear(hidden_dim + 1, hidden_dim // 2),  # +1 for change_score
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )

        # Initialize predictor to output moderate values
        nn.init.zeros_(self.predictor[-2].weight)
        nn.init.constant_(self.predictor[-2].bias, 0.0)

    def forward(self, x_buf, e_current, e_history):
        """
        Args:
            x_buf: (B, filter_length)
            e_current: (B, 1)
            e_history: (B, context_len)
        Returns:
            mu: (B, 1) - step size in (0, 1)
            change_score: (B, 1) - detected change probability
        """
        # Change detection
        change_score = self.change_detector(e_history)

        # Error patterns
        e_feat = self.error_encoder(e_history)

        # Signal state
        sig_feat = self.signal_encoder(torch.cat([x_buf, e_current], dim=-1))

        # Combine all features
        combined = torch.cat([e_feat, sig_feat, change_score], dim=-1)
        mu = self.predictor(combined)

        return mu, change_score


class SSMAF(nn.Module):
    """
    SSM-AF v7: Change Detection + Learned Step Size

    Two-tier adaptation strategy:
    1. Change detector identifies when echo path shifts
    2. Base step size scales with change score for fast re-convergence
    3. Learned component fine-tunes for steady-state performance

    Update rule:
        direction = x_buf / (||x_buf||^2 + eps)   [NLMS direction]
        mu_base = base_mu * (1 + alpha * change_score)  [adaptive base]
        mu_learned = sigmoid(MLP(...))                   [fine-tuning]
        mu = mu_base + mu_learned
        w = w + mu * direction * e
    """

    def __init__(self, filter_length: int = 64, hidden_dim: int = 32,
                 context_len: int = 64, **kwargs):
        super().__init__()
        self.filter_length = filter_length
        self.context_len = context_len

        # Step size predictor with change detection
        self.step_net = StepSizeNet(filter_length, context_len, hidden_dim)

        # Learnable base step size
        self.base_mu = nn.Parameter(torch.tensor(0.1))

        # Learnable change response factor
        self.alpha = nn.Parameter(torch.tensor(1.0))

    def forward(self, x, d):
        """
        Args:
            x: (B, seq_len) - input signal
            d: (B, seq_len) - desired signal
        Returns:
            y: (B, seq_len) - filter output
            e: (B, seq_len) - error signal
            w_history: (B, seq_len, filter_length)
        """
        batch, seq_len = x.shape

        # Initialize
        w = torch.zeros(batch, self.filter_length, device=x.device)
        x_buf = torch.zeros(batch, self.filter_length, device=x.device)
        e_history = torch.zeros(batch, self.context_len, device=x.device)

        y_list, e_list, w_list = [], [], []

        for t in range(seq_len):
            # Shift in new sample
            x_buf = torch.roll(x_buf, 1, dims=1)
            x_buf[:, 0] = x[:, t]

            # Filter output
            y_t = (w * x_buf).sum(dim=-1, keepdim=True)
            e_t = d[:, t:t+1] - y_t

            # NLMS direction
            x_norm_sq = (x_buf ** 2).sum(dim=-1, keepdim=True) + 1e-8
            direction = x_buf / x_norm_sq

            # Step size with change detection
            mu_learned, change_score = self.step_net(x_buf, e_t, e_history)

            # Adaptive base: larger when change detected
            mu_adaptive_base = self.base_mu * (1 + self.alpha * change_score)

            # Total step size
            mu = mu_adaptive_base + mu_learned

            # Update filter coefficients
            w = w + mu * direction * e_t

            # Update error history
            e_history = torch.roll(e_history, 1, dims=1)
            e_history[:, 0] = e_t.squeeze(-1)

            y_list.append(y_t.squeeze(-1))
            e_list.append(e_t.squeeze(-1))
            w_list.append(w)

        y = torch.stack(y_list, dim=1)
        e = torch.stack(e_list, dim=1)
        w_history = torch.stack(w_list, dim=1)

        return y, e, w_history


# ============================================================
# Baselines
# ============================================================

class LMSFilter:
    def __init__(self, filter_length: int, mu: float = 0.01):
        self.filter_length = filter_length
        self.mu = mu

    def process(self, x, d):
        if isinstance(x, torch.Tensor):
            x, d = x.cpu().numpy(), d.cpu().numpy()
        seq_len = len(x)
        w = np.zeros(self.filter_length)
        x_buf = np.zeros(self.filter_length)
        y = np.zeros(seq_len)
        e = np.zeros(seq_len)
        for n in range(seq_len):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x[n]
            y[n] = np.dot(w, x_buf)
            e[n] = d[n] - y[n]
            w = w + self.mu * e[n] * x_buf
        return torch.tensor(y), torch.tensor(e)


class NLMSFilter:
    def __init__(self, filter_length: int, mu: float = 0.5, epsilon: float = 1e-8):
        self.filter_length = filter_length
        self.mu = mu
        self.epsilon = epsilon

    def process(self, x, d):
        if isinstance(x, torch.Tensor):
            x, d = x.cpu().numpy(), d.cpu().numpy()
        seq_len = len(x)
        w = np.zeros(self.filter_length)
        x_buf = np.zeros(self.filter_length)
        y = np.zeros(seq_len)
        e = np.zeros(seq_len)
        for n in range(seq_len):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x[n]
            y[n] = np.dot(w, x_buf)
            e[n] = d[n] - y[n]
            norm = np.dot(x_buf, x_buf) + self.epsilon
            w = w + (self.mu / norm) * e[n] * x_buf
        return torch.tensor(y), torch.tensor(e)


class RLSFilter:
    def __init__(self, filter_length: int, lam: float = 0.99, delta: float = 0.01):
        self.filter_length = filter_length
        self.lam = lam
        self.delta = delta

    def process(self, x, d):
        if isinstance(x, torch.Tensor):
            x, d = x.cpu().numpy(), d.cpu().numpy()
        seq_len = len(x)
        w = np.zeros(self.filter_length)
        P = np.eye(self.filter_length) / self.delta
        x_buf = np.zeros(self.filter_length)
        y = np.zeros(seq_len)
        e = np.zeros(seq_len)
        for n in range(seq_len):
            x_buf = np.roll(x_buf, 1)
            x_buf[0] = x[n]
            y[n] = np.dot(w, x_buf)
            e[n] = d[n] - y[n]
            k = P @ x_buf / (self.lam + x_buf @ P @ x_buf)
            w = w + k * e[n]
            P = (P - np.outer(k, x_buf @ P)) / self.lam
        return torch.tensor(y), torch.tensor(e)


if __name__ == "__main__":
    batch_size = 2
    seq_len = 500
    filter_length = 32

    x = torch.randn(batch_size, seq_len)
    d = torch.randn(batch_size, seq_len)

    model = SSMAF(filter_length=filter_length, hidden_dim=16, context_len=32)
    y, e, w_hist = model(x, d)

    print(f"Input:   {x.shape}")
    print(f"Output:  {y.shape}")
    print(f"Error:   {e.shape}")
    print(f"Params:  {sum(p.numel() for p in model.parameters()):,}")
    assert not torch.isnan(y).any(), "NaN!"
    print("OK!")
