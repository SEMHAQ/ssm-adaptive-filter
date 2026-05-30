"""
SSM-AF: State Space Model based Adaptive Filter (v9 - Nonlinear)

Hybrid linear-nonlinear adaptive filter for nonlinear echo cancellation.

Key innovation:
- Linear component: NLMS filter for linear echo path
- Nonlinear component: Neural network for nonlinear distortion
- Joint optimization of both components

Traditional LMS/NLMS/RLS assume linear echo paths and CANNOT handle
nonlinearities (loudspeaker distortion, clipping, saturation).

SSM-AF can model both linear AND nonlinear components, providing
a fundamental advantage in real-world scenarios.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class NonlinearCorrection(nn.Module):
    """
    Neural network that models nonlinear distortion.

    Takes the input buffer and predicts a nonlinear correction
    that captures effects like:
    - Loudspeaker saturation
    - Amplifier clipping
    - Acoustic nonlinearities
    """

    def __init__(self, filter_length: int, hidden_dim: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(filter_length, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Tanh()  # Bounded output for stability
        )

        # Initialize to small outputs
        nn.init.zeros_(self.net[-2].weight)
        nn.init.zeros_(self.net[-2].bias)

    def forward(self, x_buf):
        """
        Args:
            x_buf: (B, filter_length) - input buffer
        Returns:
            nl_output: (B, 1) - nonlinear correction
        """
        return self.net(x_buf)


class SSMAF(nn.Module):
    """
    SSM-AF v9: Hybrid Linear-Nonlinear Adaptive Filter

    Architecture:
    1. Linear component: NLMS filter (proven, stable)
    2. Nonlinear component: Neural network (models distortion)
    3. Adaptive mixing: learns when to trust which component

    Update rule:
        y_linear = w^T * x_buf                    [NLMS output]
        y_nonlinear = MLP(x_buf)                   [nonlinear correction]
        y = y_linear + alpha * y_nonlinear          [mixed output]
        e = d - y                                   [error]
        w = w + mu * (x_buf / ||x_buf||^2) * e     [NLMS update]

    Advantages:
    - Handles nonlinear echo paths (LMS/NLMS/RLS cannot)
    - Stable convergence (NLMS base)
    - Learns optimal linear-nonlinear balance
    """

    def __init__(self, filter_length: int = 64, hidden_dim: int = 32,
                 context_len: int = 32, **kwargs):
        super().__init__()
        self.filter_length = filter_length

        # Nonlinear correction network
        self.nl_net = NonlinearCorrection(filter_length, hidden_dim * 2)

        # Learnable mixing factor (how much nonlinear correction to apply)
        self.alpha = nn.Parameter(torch.tensor(0.1))

        # Learnable step size for NLMS
        self.base_mu = nn.Parameter(torch.tensor(0.1))

        # Step size predictor
        self.step_net = nn.Sequential(
            nn.Linear(context_len + 1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

        self.context_len = context_len

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

            # Linear component (NLMS)
            y_linear = (w * x_buf).sum(dim=-1, keepdim=True)

            # Nonlinear component
            y_nonlinear = self.nl_net(x_buf)

            # Mixed output
            y_t = y_linear + self.alpha * y_nonlinear

            # Error
            e_t = d[:, t:t+1] - y_t

            # NLMS direction
            x_norm_sq = (x_buf ** 2).sum(dim=-1, keepdim=True) + 1e-8
            direction = x_buf / x_norm_sq

            # Adaptive step size
            mu_input = torch.cat([e_history, e_t], dim=-1)
            mu = self.step_net(mu_input) + self.base_mu

            # Update linear filter only (NLMS)
            # Nonlinear network learns via backprop through the loss
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

    model = SSMAF(filter_length=filter_length, hidden_dim=16, context_len=16)
    y, e, w_hist = model(x, d)

    print(f"Input:   {x.shape}")
    print(f"Output:  {y.shape}")
    print(f"Error:   {e.shape}")
    print(f"Params:  {sum(p.numel() for p in model.parameters()):,}")
    assert not torch.isnan(y).any(), "NaN!"
    print("OK!")
