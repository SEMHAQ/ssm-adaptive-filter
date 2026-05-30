"""
SSM-AF: State Space Model based Adaptive Filter (v2 - Stable)

Architecture (redesigned for stability and efficiency):

    1. SSM Encoder: Processes full input sequence to capture long-range dependencies
    2. Adaptive Update Network: Uses SSM features to predict filter updates
    3. FIR Filter: Standard convolution for filtering

Key insight: SSM operates on the FULL sequence (efficient parallel scan),
then the adaptive filter uses these features to learn optimal updates.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class SimpleSSM(nn.Module):
    """
    Simplified SSM block that processes full sequences.

    Uses a diagonal state space model with learnable parameters,
    avoiding the complexity of input-dependent dynamics which
    caused numerical instability in v1.
    """

    def __init__(self, d_input: int, d_state: int = 16, d_output: int = None):
        super().__init__()
        self.d_input = d_input
        self.d_state = d_state
        self.d_output = d_output or d_input

        # State space parameters (diagonal A for efficiency)
        # Initialize A as negative for stable discrete-time system
        self.A_log = nn.Parameter(torch.randn(d_state) * 0.01 - 1.0)
        self.B = nn.Parameter(torch.randn(d_input, d_state) * 0.02)
        self.C = nn.Parameter(torch.randn(d_state, self.d_output) * 0.02)
        self.D = nn.Parameter(torch.ones(d_input) * 0.1)

        # Input/output projections
        self.in_proj = nn.Linear(d_input, d_input)
        self.out_proj = nn.Linear(d_input, self.d_output)

        # Normalization
        self.norm = nn.LayerNorm(self.d_output)

        self._init_weights()

    def _init_weights(self):
        nn.init.xavier_uniform_(self.in_proj.weight)
        nn.init.xavier_uniform_(self.out_proj.weight)
        nn.init.zeros_(self.in_proj.bias)
        nn.init.zeros_(self.out_proj.bias)

    def forward(self, x):
        """
        Args:
            x: (batch, seq_len, d_input)
        Returns:
            y: (batch, seq_len, d_output)
        """
        batch, seq_len, _ = x.shape

        # Input projection
        x_proj = self.in_proj(x)  # (B, L, d_input)

        # Discretize A (using ZOH)
        A = -torch.exp(self.A_log)  # (d_state,) - negative for stability
        dt = 1.0  # Fixed dt=1 for discrete-time
        dA = torch.exp(A * dt)  # (d_state,)
        dB = self.B  # (d_input, d_state)

        # Compute state evolution: h(t) = dA * h(t-1) + dB * x(t)
        # Then output: y(t) = C * h(t) + D * x(t)

        # Vectorized scan using associative scan (more stable than loop)
        # h(t) = dA^t * h(0) + sum_{i=0}^{t-1} dA^{t-1-i} * dB * x(i)
        # For simplicity, use sequential scan with clamping

        h = torch.zeros(batch, self.d_state, device=x.device)
        states = []
        for t in range(seq_len):
            h = dA.unsqueeze(0) * h + x_proj[:, t] @ dB  # (B, d_state)
            h = h.clamp(-5.0, 5.0)  # Stability
            states.append(h)

        states = torch.stack(states, dim=1)  # (B, L, d_state)

        # Output: y(t) = C * h(t) + D * x(t)
        y_ssm = states @ self.C  # (B, L, d_output)
        y_skip = x_proj * self.D.unsqueeze(0).unsqueeze(0)  # (B, L, d_input)
        y_skip = self.out_proj(y_skip)  # (B, L, d_output)

        y = y_ssm + y_skip
        y = self.norm(y)

        return y


class StepSizePredictor(nn.Module):
    """
    Predicts input-dependent step size and direction for adaptive filtering.

    Instead of a fixed step size (like LMS), this network learns to predict
    the optimal adaptation rate based on signal characteristics.
    """

    def __init__(self, filter_length: int, hidden_dim: int = 32):
        super().__init__()
        self.filter_length = filter_length

        # SSM for temporal feature extraction
        self.ssm = SimpleSSM(d_input=filter_length, d_state=16, d_output=hidden_dim)

        # Step size prediction (bounded in [0, 1])
        self.step_net = nn.Sequential(
            nn.Linear(hidden_dim + 1, hidden_dim),  # +1 for error
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

        # Direction prediction
        self.dir_net = nn.Sequential(
            nn.Linear(hidden_dim + 1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, filter_length),
            nn.Tanh()  # Bounded direction
        )

    def forward(self, x_history, e_current):
        """
        Args:
            x_history: (batch, seq_len, filter_length) - input signal history
            e_current: (batch, 1) - current error

        Returns:
            mu: (batch, 1) - step size
            direction: (batch, filter_length) - adaptation direction
        """
        # Extract temporal features using SSM
        features = self.ssm(x_history)  # (B, L, hidden_dim)
        feat_last = features[:, -1, :]  # (B, hidden_dim) - use last timestep

        # Predict step size and direction
        inp = torch.cat([feat_last, e_current], dim=-1)
        mu = self.step_net(inp)  # (B, 1)
        direction = self.dir_net(inp)  # (B, filter_length)

        return mu, direction


class SSMAF(nn.Module):
    """
    SSM-AF: State Space Model based Adaptive Filter (v2)

    Architecture:
        1. Maintain input buffer (sliding window)
        2. SSM extracts temporal features from buffer history
        3. Step size predictor computes adaptive mu and direction
        4. Filter coefficients updated: w(n+1) = w(n) + mu * dir * e(n)

    This is a learnable adaptive filter that maintains the causal,
    sample-by-sample processing of traditional adaptive filters.
    """

    def __init__(
        self,
        filter_length: int = 64,
        hidden_dim: int = 32,
        num_layers: int = 2,
        context_len: int = 32
    ):
        super().__init__()
        self.filter_length = filter_length
        self.context_len = context_len

        # Step size predictor (uses SSM internally)
        self.predictor = StepSizePredictor(filter_length, hidden_dim)

        # Learnable initial step size
        self.init_mu = nn.Parameter(torch.tensor(0.01))

    def forward(self, x, d):
        """
        Process signal sample-by-sample.

        Args:
            x: (batch, seq_len) - input/reference signal
            d: (batch, seq_len) - desired signal

        Returns:
            y: (batch, seq_len) - filter output
            e: (batch, seq_len) - error signal
            w_history: (batch, seq_len, filter_length) - filter coefficient evolution
        """
        batch, seq_len = x.shape

        # Initialize
        w = torch.zeros(batch, self.filter_length, device=x.device)
        x_buf = torch.zeros(batch, self.filter_length, device=x.device)

        # Context buffer for SSM (keeps recent input windows)
        context = torch.zeros(batch, self.context_len, self.filter_length, device=x.device)

        y_list = []
        e_list = []
        w_list = []

        for t in range(seq_len):
            # Shift in new sample to buffer
            x_buf = torch.roll(x_buf, 1, dims=1)
            x_buf[:, 0] = x[:, t]

            # Update context (sliding window of input buffers)
            context = torch.roll(context, 1, dims=1)
            context[:, 0] = x_buf

            # Compute output and error
            y_t = (w * x_buf).sum(dim=-1, keepdim=True)
            e_t = d[:, t:t+1] - y_t

            # Predict step size and direction using SSM features
            if t < self.context_len:
                # Use available context (pad if needed)
                ctx = context[:, :t+1]
            else:
                ctx = context

            mu, direction = self.predictor(ctx, e_t)

            # Update filter coefficients
            w = w + mu * direction * e_t

            # Clamp weights for stability
            w = w.clamp(-5.0, 5.0)

            y_list.append(y_t.squeeze(-1))
            e_list.append(e_t.squeeze(-1))
            w_list.append(w)

        y = torch.stack(y_list, dim=1)
        e = torch.stack(e_list, dim=1)
        w_history = torch.stack(w_list, dim=1)

        return y, e, w_history

    def infer(self, x):
        """
        Real-time inference mode.

        Args:
            x: (seq_len,) - input signal
        Returns:
            y: (seq_len,) - filtered output
        """
        self.eval()
        seq_len = x.shape[0]
        device = x.device

        w = torch.zeros(1, self.filter_length, device=device)
        x_buf = torch.zeros(1, self.filter_length, device=device)
        context = torch.zeros(1, self.context_len, self.filter_length, device=device)
        outputs = []

        with torch.no_grad():
            for t in range(seq_len):
                x_buf = torch.roll(x_buf, 1, dims=1)
                x_buf[:, 0] = x[t]

                context = torch.roll(context, 1, dims=1)
                context[:, 0] = x_buf

                y_t = (w * x_buf).sum(dim=-1, keepdim=True)
                e_t = torch.zeros(1, 1, device=device)

                ctx = context[:, :min(t+1, self.context_len)]
                mu, direction = self.predictor(ctx, e_t)
                w = w + mu * direction * e_t
                w = w.clamp(-5.0, 5.0)

                outputs.append(y_t.squeeze())

        return torch.stack(outputs)


# ============================================================
# Baseline Implementations for Comparison
# ============================================================

class LMSFilter:
    """Standard LMS adaptive filter baseline."""

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
    """Normalized LMS adaptive filter baseline."""

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
    """Recursive Least Squares adaptive filter baseline."""

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
    # Quick sanity check
    batch_size = 2
    seq_len = 100
    filter_length = 32

    x = torch.randn(batch_size, seq_len)
    d = torch.randn(batch_size, seq_len)

    model = SSMAF(filter_length=filter_length, hidden_dim=16, context_len=16)
    y, e, w_hist = model(x, d)

    print(f"Input shape:    {x.shape}")
    print(f"Output shape:   {y.shape}")
    print(f"Error shape:    {e.shape}")
    print(f"Weights shape:  {w_hist.shape}")
    print(f"Parameters:     {sum(p.numel() for p in model.parameters()):,}")
    print(f"Output range:   [{y.min():.3f}, {y.max():.3f}]")
    print(f"Error range:    [{e.min():.3f}, {e.max():.3f}]")

    # Check for NaN
    assert not torch.isnan(y).any(), "Output contains NaN!"
    assert not torch.isnan(e).any(), "Error contains NaN!"
    print("All checks passed!")
