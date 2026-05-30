"""
SSM-AF: State Space Model based Adaptive Filter (v6 - Context-Aware)

NLMS with learned step size using error history context.
The network observes a window of recent errors to detect:
- Convergence state (steady decreasing error -> small step)
- Echo path change (sudden error increase -> large step)
- Noise level (error variance -> optimal tradeoff)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class StepSizeNet(nn.Module):
    """
    Predicts adaptive step size from signal context and error history.

    Key insight: By looking at recent error trends, the network can detect
    when the echo path has changed and increase step size accordingly.

    Input: x_buf (filter_length), e_history (context_len), x_power (1)
    Output: step size mu in (0, 1)
    """

    def __init__(self, filter_length: int, context_len: int = 16, hidden_dim: int = 32):
        super().__init__()
        self.context_len = context_len

        # Error history encoder (captures temporal patterns)
        self.error_encoder = nn.Sequential(
            nn.Linear(context_len, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
        )

        # Signal features encoder
        self.signal_encoder = nn.Sequential(
            nn.Linear(filter_length + 1, hidden_dim),  # x_buf + current error
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
        )

        # Combine and predict step size
        self.predictor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )

        # Initialize to output ~0.5 initially
        nn.init.zeros_(self.predictor[-2].weight)
        nn.init.constant_(self.predictor[-2].bias, 0.0)

    def forward(self, x_buf, e_current, e_history):
        """
        Args:
            x_buf: (B, filter_length) - current input buffer
            e_current: (B, 1) - current error
            e_history: (B, context_len) - recent error history
        Returns:
            mu: (B, 1) - step size in (0, 1)
        """
        # Encode error history (temporal patterns)
        e_feat = self.error_encoder(e_history)

        # Encode current signal state
        sig_feat = self.signal_encoder(torch.cat([x_buf, e_current], dim=-1))

        # Combine and predict
        combined = torch.cat([e_feat, sig_feat], dim=-1)
        return self.predictor(combined)


class SSMAF(nn.Module):
    """
    SSM-AF v6: Context-Aware NLMS with Learned Step Size

    Key innovation: Step size prediction conditioned on error history,
    enabling the model to detect and adapt to non-stationary changes.

    Update rule:
        direction = x_buf / (||x_buf||^2 + eps)   [NLMS direction]
        mu = sigmoid(MLP(x_buf, e, e_history))      [context-aware step size]
        w = w + mu * direction * e
    """

    def __init__(self, filter_length: int = 64, hidden_dim: int = 32,
                 context_len: int = 16, **kwargs):
        super().__init__()
        self.filter_length = filter_length
        self.context_len = context_len

        # Context-aware step size predictor
        self.step_net = StepSizeNet(filter_length, context_len, hidden_dim)

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

            # NLMS direction (normalized)
            x_norm_sq = (x_buf ** 2).sum(dim=-1, keepdim=True) + 1e-8
            direction = x_buf / x_norm_sq

            # Context-aware step size
            mu = self.step_net(x_buf, e_t, e_history) + self.base_mu

            # Update filter coefficients
            w = w + mu * direction * e_t

            # Update error history buffer
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

    model = SSMAF(filter_length=filter_length, hidden_dim=16)
    y, e, w_hist = model(x, d)

    print(f"Input:   {x.shape}")
    print(f"Output:  {y.shape}")
    print(f"Error:   {e.shape}")
    print(f"Params:  {sum(p.numel() for p in model.parameters()):,}")
    assert not torch.isnan(y).any(), "NaN!"
    print("OK!")
