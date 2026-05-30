"""
SSM-AF: State Space Model based Adaptive Filter (v5 - Final)

Simple and reliable: NLMS with learned step size.
The network learns when to take big/small steps based on signal context.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class StepSizeNet(nn.Module):
    """
    Predicts adaptive step size from current signal context.

    Input: input buffer x_buf and current error e
    Output: step size mu in (0, 1)

    The network learns that:
    - Large error -> larger step (fast convergence)
    - Small error -> smaller step (low steady-state error)
    - Signal power affects optimal step size
    """

    def __init__(self, filter_length: int, hidden_dim: int = 32):
        super().__init__()
        # Simple 2-layer MLP
        self.net = nn.Sequential(
            nn.Linear(filter_length + 1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )
        # Initialize to output ~0.5 (moderate step size)
        nn.init.zeros_(self.net[-2].weight)
        nn.init.constant_(self.net[-2].bias, 0.0)

    def forward(self, x_buf, e):
        """
        Args:
            x_buf: (B, filter_length)
            e: (B, 1)
        Returns:
            mu: (B, 1)
        """
        inp = torch.cat([x_buf, e], dim=-1)
        return self.net(inp)


class SSMAF(nn.Module):
    """
    SSM-AF v5: NLMS with Learned Step Size

    Update rule:
        direction = x_buf / (||x_buf||^2 + eps)   [NLMS direction]
        mu = sigmoid(MLP(x_buf, e))                 [learned step size]
        w = w + mu * direction * e

    This is a direct improvement over NLMS: same proven direction,
    but the step size adapts to signal conditions.
    """

    def __init__(self, filter_length: int = 64, hidden_dim: int = 32, **kwargs):
        super().__init__()
        self.filter_length = filter_length

        # Step size predictor
        self.step_net = StepSizeNet(filter_length, hidden_dim)

        # Learnable base step size (initialized to NLMS-like value)
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

        y_list, e_list, w_list = [], [], []

        for t in range(seq_len):
            # Shift in new sample
            x_buf = torch.roll(x_buf, 1, dims=1)
            x_buf[:, 0] = x[:, t]

            # Filter output
            y_t = (w * x_buf).sum(dim=-1, keepdim=True)
            e_t = d[:, t:t+1] - y_t

            # NLMS direction (normalized)
            x_norm_sq = (x_buf ** 2).sum(dim=-1, keepdim=True) + 1e-8
            direction = x_buf / x_norm_sq

            # Learned step size (base + learned)
            mu = self.step_net(x_buf, e_t) + self.base_mu

            # Update filter coefficients
            w = w + mu * direction * e_t

            y_list.append(y_t.squeeze(-1))
            e_list.append(e_t.squeeze(-1))
            w_list.append(w)

        y = torch.stack(y_list, dim=1)
        e = torch.stack(e_list, dim=1)
        w_history = torch.stack(w_list, dim=1)

        return y, e, w_history

    def infer(self, x):
        """Real-time inference."""
        self.eval()
        seq_len = x.shape[0]
        device = x.device

        w = torch.zeros(1, self.filter_length, device=device)
        x_buf = torch.zeros(1, self.filter_length, device=device)
        outputs = []

        with torch.no_grad():
            for t in range(seq_len):
                x_buf = torch.roll(x_buf, 1, dims=1)
                x_buf[:, 0] = x[t]

                y_t = (w * x_buf).sum(dim=-1, keepdim=True)
                e_t = torch.zeros(1, 1, device=device)

                x_norm_sq = (x_buf ** 2).sum(dim=-1, keepdim=True) + 1e-8
                direction = x_buf / x_norm_sq
                mu = self.step_net(x_buf, e_t) + self.base_mu

                w = w + mu * direction * e_t
                outputs.append(y_t.squeeze())

        return torch.stack(outputs)


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

    model = SSMAF(filter_length=filter_length, hidden_dim=16)
    y, e, w_hist = model(x, d)

    print(f"Input:   {x.shape}")
    print(f"Output:  {y.shape}")
    print(f"Error:   {e.shape}")
    print(f"Params:  {sum(p.numel() for p in model.parameters()):,}")
    assert not torch.isnan(y).any(), "NaN!"
    print("OK!")
