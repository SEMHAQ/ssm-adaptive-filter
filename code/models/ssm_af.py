"""
SSM-AF: State Space Model based Adaptive Filter (v8 - Learned Correction)

NLMS with learned correction vector.

Key insight: Instead of just learning a scalar step size,
learn a full correction vector that can adjust each filter coefficient
independently based on signal context.

Update rule:
    w = w + mu * direction * e + correction(context)

This gives the model much more flexibility:
- Can correct specific taps that need adjustment
- Can use context to predict how each coefficient should change
- NLMS provides stable base, correction handles non-stationarity
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class CorrectionNet(nn.Module):
    """
    Predicts correction vector for filter coefficients.

    Input: signal context (x_buf, e_history, current e)
    Output: correction vector of dimension filter_length

    The network learns to predict how each filter coefficient
    should be adjusted based on recent signal statistics.
    """

    def __init__(self, filter_length: int, context_len: int = 32, hidden_dim: int = 64):
        super().__init__()
        self.filter_length = filter_length

        # Context encoder (processes error history and current state)
        self.context_encoder = nn.Sequential(
            nn.Linear(context_len + 1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

        # Correction predictor
        self.corrector = nn.Sequential(
            nn.Linear(hidden_dim + filter_length, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, filter_length),
            nn.Tanh()  # Bounded correction
        )

        # Scale factor (learnable)
        self.scale = nn.Parameter(torch.tensor(0.01))

        # Initialize to small corrections
        nn.init.zeros_(self.corrector[-2].weight)
        nn.init.zeros_(self.corrector[-2].bias)

    def forward(self, x_buf, e_current, e_history):
        """
        Args:
            x_buf: (B, filter_length) - current input buffer
            e_current: (B, 1) - current error
            e_history: (B, context_len) - recent error history
        Returns:
            correction: (B, filter_length) - correction vector
        """
        # Encode context
        context = torch.cat([e_history, e_current], dim=-1)
        ctx_feat = self.context_encoder(context)

        # Predict correction
        combined = torch.cat([ctx_feat, x_buf], dim=-1)
        correction = self.corrector(combined)

        return correction * self.scale


class SSMAF(nn.Module):
    """
    SSM-AF v8: NLMS + Learned Correction Vector

    Update rule:
        direction = x_buf / (||x_buf||^2 + eps)   [NLMS direction]
        mu = sigmoid(MLP(context)) + base_mu        [adaptive step size]
        correction = MLP(x_buf, context)             [learned correction]
        w = w + mu * direction * e + correction

    This combines:
    1. NLMS for stable, proven convergence
    2. Adaptive step size for overall scaling
    3. Learned correction for fine-grained adjustment
    """

    def __init__(self, filter_length: int = 64, hidden_dim: int = 32,
                 context_len: int = 32, **kwargs):
        super().__init__()
        self.filter_length = filter_length
        self.context_len = context_len

        # Step size predictor
        self.step_net = nn.Sequential(
            nn.Linear(context_len + 1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

        # Correction predictor
        self.correction_net = CorrectionNet(filter_length, context_len, hidden_dim)

        # Learnable base step size
        self.base_mu = nn.Parameter(torch.tensor(0.1))

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

            # Adaptive step size
            mu_input = torch.cat([e_history, e_t], dim=-1)
            mu = self.step_net(mu_input) + self.base_mu

            # Learned correction
            correction = self.correction_net(x_buf, e_t, e_history)

            # Update: NLMS + correction
            w = w + mu * direction * e_t + correction

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
