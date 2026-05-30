"""
SSM-AF: State Space Model based Adaptive Filter (v4 - Block Adaptive)

Key innovation: Instead of learning step size (marginal improvement),
use SSM to predict filter coefficients directly from signal history.

Architecture:
    1. Divide input into blocks of N samples
    2. SSM processes the block history to predict optimal filter coefficients
    3. Apply filter, compute error, update state

This is fundamentally different from LMS/NLMS which update sample-by-sample.
Our approach can adapt faster by leveraging temporal structure.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class SSMBlockPredictor(nn.Module):
    """
    Predicts filter coefficients from signal block history using SSM.

    Input: Recent signal blocks [x(n-N+1), ..., x(n)]
    Output: Filter coefficients w(n)

    The SSM captures temporal dynamics across blocks, enabling
    faster adaptation than sample-by-sample methods.
    """

    def __init__(self, block_size: int, filter_length: int, d_state: int = 16, context_blocks: int = 4):
        super().__init__()
        self.block_size = block_size
        self.filter_length = filter_length
        self.d_state = d_state
        self.context_blocks = context_blocks

        # SSM parameters (diagonal A for stability)
        self.A_log = nn.Parameter(torch.randn(d_state) * 0.01 - 1.0)
        self.B = nn.Linear(block_size, d_state, bias=False)
        self.C = nn.Linear(d_state, filter_length, bias=False)
        self.D = nn.Linear(block_size, filter_length, bias=False)

        # Layer norm
        self.norm = nn.LayerNorm(filter_length)

        self._init_weights()

    def _init_weights(self):
        nn.init.xavier_uniform_(self.B.weight)
        nn.init.xavier_uniform_(self.C.weight)
        nn.init.xavier_uniform_(self.D.weight)

    def forward(self, blocks):
        """
        Args:
            blocks: (batch, num_blocks, block_size) - signal blocks
        Returns:
            w: (batch, filter_length) - predicted filter coefficients
        """
        batch, num_blocks, _ = blocks.shape

        # Discretize A
        A = -torch.exp(self.A_log)  # (d_state,)
        dA = torch.exp(A)  # (d_state,)

        # Process blocks through SSM
        h = torch.zeros(batch, self.d_state, device=blocks.device)
        for t in range(num_blocks):
            h = dA.unsqueeze(0) * h + self.B(blocks[:, t])
            h = h.clamp(-5.0, 5.0)

        # Output: filter coefficients
        w_ssm = self.C(h)  # (B, filter_length)
        w_skip = self.D(blocks[:, -1])  # (B, filter_length) - skip from last block
        w = w_ssm + w_skip
        w = self.norm(w)

        return w


class SSMAF(nn.Module):
    """
    SSM-AF v4: Block-Adaptive Filter with SSM

    Unlike LMS/NLMS which update sample-by-sample, this model:
    1. Processes signal in blocks
    2. Uses SSM to predict optimal filter coefficients from block history
    3. Applies filter and computes error

    This enables faster adaptation by leveraging temporal structure
    across blocks, which classical methods cannot do.
    """

    def __init__(
        self,
        filter_length: int = 64,
        block_size: int = 16,
        d_state: int = 16,
        context_blocks: int = 4,
    ):
        super().__init__()
        self.filter_length = filter_length
        self.block_size = block_size
        self.context_blocks = context_blocks

        # SSM-based filter predictor
        self.predictor = SSMBlockPredictor(
            block_size=block_size,
            filter_length=filter_length,
            d_state=d_state,
            context_blocks=context_blocks
        )

    def forward(self, x, d):
        """
        Args:
            x: (batch, seq_len) - input signal
            d: (batch, seq_len) - desired signal
        Returns:
            y: (batch, seq_len) - filter output
            e: (batch, seq_len) - error signal
            w_history: (batch, num_blocks, filter_length)
        """
        batch, seq_len = x.shape
        device = x.device

        # Pad to multiple of block_size
        pad_len = (self.block_size - seq_len % self.block_size) % self.block_size
        if pad_len > 0:
            x = F.pad(x, (0, pad_len))
            d = F.pad(d, (0, pad_len))
        total_len = x.shape[1]
        num_blocks = total_len // self.block_size

        # Reshape into blocks
        x_blocks = x.reshape(batch, num_blocks, self.block_size)
        d_blocks = d.reshape(batch, num_blocks, self.block_size)

        # Process
        y_list = []
        e_list = []
        w_list = []

        # Buffer of recent blocks for SSM context
        block_buf = torch.zeros(batch, self.context_blocks, self.block_size, device=device)

        for b in range(num_blocks):
            # Update block buffer
            block_buf = torch.roll(block_buf, 1, dims=1)
            block_buf[:, 0] = x_blocks[:, b]

            # Predict filter coefficients from block history
            w = self.predictor(block_buf)

            # Apply filter to current block (convolution)
            # For each sample in block, compute y = w^T * x_buf
            x_block = x_blocks[:, b]  # (B, block_size)
            d_block = d_blocks[:, b]  # (B, block_size)

            # Compute output for each sample in block
            y_block = torch.zeros(batch, self.block_size, device=device)
            for i in range(self.block_size):
                # Build input buffer for this sample
                # Current block samples + previous block samples
                x_buf = torch.zeros(batch, self.filter_length, device=device)

                # Fill buffer from current block (samples 0..i)
                for j in range(min(i + 1, self.filter_length)):
                    if i - j >= 0:
                        x_buf[:, j] = x_block[:, i - j]

                # Fill remaining from previous blocks
                if i + 1 < self.filter_length:
                    remaining = self.filter_length - (i + 1)
                    # Flatten previous blocks
                    prev = block_buf[:, 1:].reshape(batch, -1)  # previous blocks
                    if prev.shape[1] >= remaining:
                        x_buf[:, i+1:] = prev[:, :remaining]
                    else:
                        x_buf[:, i+1:i+1+prev.shape[1]] = prev

                y_block[:, i] = (w * x_buf).sum(dim=-1)

            e_block = d_block - y_block

            y_list.append(y_block)
            e_list.append(e_block)
            w_list.append(w)

        # Concatenate blocks
        y = torch.cat(y_list, dim=1)[:, :seq_len]
        e = torch.cat(e_list, dim=1)[:, :seq_len]
        w_history = torch.stack(w_list, dim=1)

        return y, e, w_history

    def infer(self, x):
        """Real-time inference."""
        self.eval()
        seq_len = x.shape[0]
        device = x.device

        pad_len = (self.block_size - seq_len % self.block_size) % self.block_size
        if pad_len > 0:
            x = F.pad(x, (0, pad_len))
        total_len = x.shape[0]
        num_blocks = total_len // self.block_size

        x_blocks = x.reshape(1, num_blocks, self.block_size)
        block_buf = torch.zeros(1, self.context_blocks, self.block_size, device=device)

        outputs = []

        with torch.no_grad():
            for b in range(num_blocks):
                block_buf = torch.roll(block_buf, 1, dims=1)
                block_buf[:, 0] = x_blocks[:, b]

                w = self.predictor(block_buf)
                x_block = x_blocks[:, b]

                y_block = torch.zeros(1, self.block_size, device=device)
                for i in range(self.block_size):
                    x_buf = torch.zeros(1, self.filter_length, device=device)
                    for j in range(min(i + 1, self.filter_length)):
                        if i - j >= 0:
                            x_buf[:, j] = x_block[:, i - j]
                    if i + 1 < self.filter_length:
                        remaining = self.filter_length - (i + 1)
                        prev = block_buf[:, 1:].reshape(1, -1)
                        if prev.shape[1] >= remaining:
                            x_buf[:, i+1:] = prev[:, :remaining]
                        else:
                            x_buf[:, i+1:i+1+prev.shape[1]] = prev
                    y_block[:, i] = (w * x_buf).sum(dim=-1)

                outputs.append(y_block)

        return torch.cat(outputs, dim=1).squeeze()[:seq_len]


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
    seq_len = 256
    filter_length = 32
    block_size = 16

    x = torch.randn(batch_size, seq_len)
    d = torch.randn(batch_size, seq_len)

    model = SSMAF(filter_length=filter_length, block_size=block_size, d_state=8, context_blocks=4)
    y, e, w_hist = model(x, d)

    print(f"Input shape:    {x.shape}")
    print(f"Output shape:   {y.shape}")
    print(f"Error shape:    {e.shape}")
    print(f"Weights shape:  {w_hist.shape}")
    print(f"Parameters:     {sum(p.numel() for p in model.parameters()):,}")
    assert not torch.isnan(y).any(), "NaN!"
    print("All checks passed!")
