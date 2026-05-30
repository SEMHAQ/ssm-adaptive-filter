"""
SSM-AF: State Space Model based Adaptive Filter

Core idea: Replace the fixed step-size in traditional LMS/NLMS with a
selective state space model that dynamically adjusts the adaptation
process based on input signal characteristics.

Architecture:
    Input x(n) --> SSM Encoder --> State h(n)
    State h(n) + Error e(n) --> Adaptive Update --> Filter Coefficients w(n)
    Filter Coefficients w(n) + Input x(n) --> Output y(n) = w^T * x(n)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class SelectiveSSM(nn.Module):
    """
    Selective State Space Model block inspired by Mamba.

    Key innovation: Input-dependent A, B, C matrices enable
    the model to selectively process different signal patterns,
    analogous to how a Kalman filter adjusts its gain based on
    the innovation sequence.
    """

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv

        # Input projection
        self.in_proj = nn.Linear(d_model, d_model * 2, bias=False)

        # Convolution for local context
        self.conv1d = nn.Conv1d(
            d_model, d_model, kernel_size=d_conv,
            padding=d_conv - 1, groups=d_model
        )

        # SSM parameters (input-dependent via projection)
        self.x_proj = nn.Linear(d_model, d_state * 2 + d_model, bias=False)  # B, C, dt

        # A parameter (log space for stability)
        A = torch.arange(1, d_state + 1, dtype=torch.float32).unsqueeze(0).expand(d_model, -1)
        self.A_log = nn.Parameter(torch.log(A))

        # D parameter (skip connection)
        self.D = nn.Parameter(torch.ones(d_model))

        # Output projection
        self.out_proj = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):
        """
        Args:
            x: (batch, seq_len, d_model)
        Returns:
            y: (batch, seq_len, d_model)
        """
        batch, seq_len, _ = x.shape

        # Input projection and split
        xz = self.in_proj(x)  # (B, L, 2*D)
        x_proj, z = xz.chunk(2, dim=-1)  # each (B, L, D)

        # Convolution (causal)
        x_conv = self.conv1d(x_proj.transpose(1, 2))[:, :, :seq_len].transpose(1, 2)
        x_conv = F.silu(x_conv)

        # Compute input-dependent SSM parameters
        x_dbl = self.x_proj(x_conv)  # (B, L, 2*d_state + D)
        B_param = x_dbl[..., :self.d_state]  # (B, L, d_state)
        C_param = x_dbl[..., self.d_state:2*self.d_state]  # (B, L, d_state)
        dt = F.softplus(x_dbl[..., 2*self.d_state:])  # (B, L, D) - discretization step

        # Discretize A
        A = -torch.exp(self.A_log)  # (D, d_state)
        dA = torch.exp(dt.unsqueeze(-1) * A)  # (B, L, D, d_state)
        dB = dt.unsqueeze(-1) * B_param.unsqueeze(2)  # (B, L, D, d_state)

        # Selective scan (sequential for clarity, can be parallelized)
        h = torch.zeros(batch, self.d_model, self.d_state, device=x.device)
        outputs = []
        for t in range(seq_len):
            h = dA[:, t] * h + dB[:, t] * x_conv[:, t].unsqueeze(-1)
            y_t = (h * C_param[:, t].unsqueeze(1)).sum(-1)  # (B, D)
            outputs.append(y_t)

        y = torch.stack(outputs, dim=1)  # (B, L, D)

        # Skip connection
        y = y + x_conv * self.D.unsqueeze(0).unsqueeze(0)

        # Gating
        y = y * F.silu(z)

        return self.out_proj(y)


class AdaptiveFilterLayer(nn.Module):
    """
    Core adaptive filter layer that combines SSM state with
    filter coefficient estimation.

    The SSM captures temporal dynamics of the signal, while
    the adaptive filter layer computes the actual filtering
    and coefficient updates.
    """

    def __init__(self, filter_length: int, d_state: int = 16):
        super().__init__()
        self.filter_length = filter_length

        # SSM for modeling filter dynamics
        self.ssm = SelectiveSSM(d_model=filter_length, d_state=d_state)

        # Step size network (input-dependent step size)
        self.step_size_net = nn.Sequential(
            nn.Linear(filter_length * 2, filter_length),
            nn.ReLU(),
            nn.Linear(filter_length, filter_length),
            nn.Sigmoid()  # Step size in [0, 1]
        )

        # Direction network (adaptation direction)
        self.direction_net = nn.Sequential(
            nn.Linear(filter_length * 2, filter_length),
            nn.ReLU(),
            nn.Linear(filter_length, filter_length)
        )

    def forward(self, x_buf, error, w_prev):
        """
        Args:
            x_buf: (batch, filter_length) - current input buffer
            error: (batch, 1) - current estimation error
            w_prev: (batch, filter_length) - previous filter coefficients

        Returns:
            w_new: (batch, filter_length) - updated filter coefficients
            y: (batch, 1) - filter output
        """
        # Filter output
        y = (w_prev * x_buf).sum(dim=-1, keepdim=True)  # (B, 1)

        # SSM processes the input buffer to capture temporal context
        ssm_input = x_buf.unsqueeze(1)  # (B, 1, L)
        ssm_out = self.ssm(ssm_input).squeeze(1)  # (B, L)

        # Compute input-dependent step size
        step_input = torch.cat([ssm_out, error.expand(-1, self.filter_length)], dim=-1)
        mu = self.step_size_net(step_input)  # (B, L)

        # Compute adaptation direction
        direction = self.direction_net(step_input)  # (B, L)

        # Update filter coefficients
        w_new = w_prev + mu * direction * error

        return w_new, y


class SSMAF(nn.Module):
    """
    SSM-AF: State Space Model based Adaptive Filter

    Full model that performs sample-by-sample adaptive filtering,
    similar to LMS/NLMS but with learned, input-dependent dynamics.

    This maintains the causal, real-time processing capability of
    traditional adaptive filters while leveraging SSM for better
    convergence and steady-state performance.
    """

    def __init__(
        self,
        filter_length: int = 64,
        d_state: int = 16,
        num_layers: int = 2,
        normalize: bool = True
    ):
        super().__init__()
        self.filter_length = filter_length
        self.normalize = normalize

        # Stack of adaptive filter layers
        self.layers = nn.ModuleList([
            AdaptiveFilterLayer(filter_length, d_state)
            for _ in range(num_layers)
        ])

        # Final output projection
        self.output_proj = nn.Linear(filter_length, 1)

    def forward(self, x, d):
        """
        Process signal sample-by-sample (training mode with parallel simulation).

        Args:
            x: (batch, seq_len) - input/reference signal
            d: (batch, seq_len) - desired signal

        Returns:
            y: (batch, seq_len) - filter output
            e: (batch, seq_len) - error signal
            w_history: (batch, seq_len, filter_length) - filter coefficient evolution
        """
        batch, seq_len = x.shape

        # Initialize filter coefficients
        w = torch.zeros(batch, self.filter_length, device=x.device)

        # Buffers for outputs
        y_list = []
        e_list = []
        w_list = []

        # Input buffer (shift register)
        x_buf = torch.zeros(batch, self.filter_length, device=x.device)

        for t in range(seq_len):
            # Shift in new sample
            x_buf = torch.roll(x_buf, 1, dims=1)
            x_buf[:, 0] = x[:, t]

            # Normalize input buffer
            if self.normalize:
                norm = torch.norm(x_buf, dim=1, keepdim=True) + 1e-8
                x_buf_norm = x_buf / norm
            else:
                x_buf_norm = x_buf

            # Compute current output and error
            y_t = (w * x_buf).sum(dim=-1, keepdim=True)  # (B, 1)
            e_t = d[:, t:t+1] - y_t  # (B, 1)

            # Update filter coefficients through layers
            w_current = w
            for layer in self.layers:
                w_current, _ = layer(x_buf_norm, e_t, w_current)

            w = w_current

            y_list.append(y_t.squeeze(-1))
            e_list.append(e_t.squeeze(-1))
            w_list.append(w)

        y = torch.stack(y_list, dim=1)
        e = torch.stack(e_list, dim=1)
        w_history = torch.stack(w_list, dim=1)

        return y, e, w_history

    def infer(self, x):
        """
        Real-time inference mode: process sample by sample.

        Args:
            x: (seq_len,) - input signal (single channel)

        Returns:
            y: (seq_len,) - filtered output
        """
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

                if self.normalize:
                    norm = torch.norm(x_buf, dim=1, keepdim=True) + 1e-8
                    x_buf_norm = x_buf / norm
                else:
                    x_buf_norm = x_buf

                y_t = (w * x_buf).sum(dim=-1, keepdim=True)

                # For inference, use the last error estimate
                e_t = torch.zeros(1, 1, device=device)  # No desired signal in inference

                for layer in self.layers:
                    w, _ = layer(x_buf_norm, e_t, w)

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
        self.w = None

    def process(self, x, d):
        """
        Process entire signal.

        Args:
            x: (seq_len,) - input signal
            d: (seq_len,) - desired signal

        Returns:
            y: (seq_len,) - output
            e: (seq_len,) - error
        """
        seq_len = len(x)
        device = x.device if isinstance(x, torch.Tensor) else 'cpu'

        if isinstance(x, torch.Tensor):
            x = x.cpu().numpy()
            d = d.cpu().numpy()

        import numpy as np
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

        self.w = w
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
            x = x.cpu().numpy()
            d = d.cpu().numpy()

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
            x = x.cpu().numpy()
            d = d.cpu().numpy()

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
    # Quick test
    batch_size = 2
    seq_len = 1000
    filter_length = 32

    # Generate test signals
    x = torch.randn(batch_size, seq_len)
    d = torch.randn(batch_size, seq_len)

    # Test SSM-AF
    model = SSMAF(filter_length=filter_length, d_state=8, num_layers=2)
    y, e, w_hist = model(x, d)

    print(f"Input shape:    {x.shape}")
    print(f"Output shape:   {y.shape}")
    print(f"Error shape:    {e.shape}")
    print(f"Weights shape:  {w_hist.shape}")
    print(f"Parameters:     {sum(p.numel() for p in model.parameters()):,}")
