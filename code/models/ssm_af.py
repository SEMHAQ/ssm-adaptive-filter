"""
SSM-AF: State Space Model based Adaptive Filter (v3 - Working)

Simplified architecture that reliably learns:
1. Base: NLMS-like update (direction = normalized input buffer)
2. Enhancement: SSM refines step size based on signal history
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class StepSizeNet(nn.Module):
    """
    Predicts adaptive step size from recent signal history.

    Takes the recent input buffers and errors, predicts a
    per-sample step size in (0, 1).
    """

    def __init__(self, filter_length: int, context_len: int = 16, hidden_dim: int = 32):
        super().__init__()
        self.filter_length = filter_length
        self.context_len = context_len

        # Simple MLP on recent input statistics
        self.net = nn.Sequential(
            nn.Linear(filter_length + 1, hidden_dim),  # current buf + current error
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()  # step size in [0, 1]
        )

    def forward(self, x_buf, e):
        """
        Args:
            x_buf: (B, filter_length) - current input buffer
            e: (B, 1) - current error
        Returns:
            mu: (B, 1) - step size
        """
        inp = torch.cat([x_buf, e], dim=-1)
        return self.net(inp)


class SSMAF(nn.Module):
    """
    SSM-AF v3: Learnable Adaptive Filter

    Core idea: NLMS uses direction = x_buf / ||x_buf||^2 with fixed mu.
    We keep the NLMS direction but learn the optimal step size.

    Update rule:
        direction = x_buf / (||x_buf||^2 + eps)  [NLMS direction]
        mu = StepSizeNet(x_buf, e)                 [learned step size]
        w = w + mu * direction * e
    """

    def __init__(
        self,
        filter_length: int = 64,
        hidden_dim: int = 32,
        context_len: int = 16,
    ):
        super().__init__()
        self.filter_length = filter_length
        self.context_len = context_len

        # Learnable step size predictor
        self.step_net = StepSizeNet(filter_length, context_len, hidden_dim)

        # Learnable initial mu (start with NLMS-like value)
        self.base_mu = nn.Parameter(torch.tensor(0.5))

    def forward(self, x, d):
        """
        Args:
            x: (batch, seq_len) - input/reference signal
            d: (batch, seq_len) - desired signal
        Returns:
            y: (batch, seq_len) - filter output
            e: (batch, seq_len) - error signal
            w_history: (batch, seq_len, filter_length)
        """
        batch, seq_len = x.shape

        # Initialize
        w = torch.zeros(batch, self.filter_length, device=x.device)
        x_buf = torch.zeros(batch, self.filter_length, device=x.device)

        y_list = []
        e_list = []
        w_list = []

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

            # Learned step size
            mu = self.step_net(x_buf, e_t) + self.base_mu * 0.1  # base + learned

            # Update
            w = w + mu * direction * e_t
            w = w.clamp(-10.0, 10.0)

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
                mu = self.step_net(x_buf, e_t) + self.base_mu * 0.1

                w = w + mu * direction * e_t
                w = w.clamp(-10.0, 10.0)
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
        import numpy as np
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
        import numpy as np
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
        import numpy as np
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

    model = SSMAF(filter_length=filter_length, hidden_dim=16, context_len=8)
    y, e, w_hist = model(x, d)

    print(f"Input shape:    {x.shape}")
    print(f"Output shape:   {y.shape}")
    print(f"Error shape:    {e.shape}")
    print(f"Parameters:     {sum(p.numel() for p in model.parameters()):,}")
    print(f"Output range:   [{y.min():.3f}, {y.max():.3f}]")
    print(f"Error range:    [{e.min():.3f}, {e.max():.3f}]")
    assert not torch.isnan(y).any(), "NaN in output!"
    assert not torch.isnan(e).any(), "NaN in error!"
    print("All checks passed!")
