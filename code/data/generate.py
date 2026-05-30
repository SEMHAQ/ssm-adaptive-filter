"""
Data generation for adaptive filtering experiments.

Three canonical tasks:
1. Echo Cancellation - ITU-T G.168 echo path
2. Channel Equalization - Frequency-selective channel
3. Noise Reduction - Adaptive noise cancellation
"""

import torch
import numpy as np
from typing import Tuple, Optional


def generate_echo_cancellation_data(
    num_samples: int = 10000,
    seq_len: int = 8000,
    filter_length: int = 128,
    snr_db: float = 20.0,
    echo_path_type: str = 'itu_g168'
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate echo cancellation training data.

    Setup: Far-end signal x(n) passes through echo path h to produce
    echo d(n) = h * x(n) + noise. Adaptive filter estimates h.

    Args:
        num_samples: Number of training sequences
        seq_len: Length of each sequence (samples)
        filter_length: Length of the echo path
        snr_db: Signal-to-noise ratio in dB
        echo_path_type: Type of echo path ('itu_g168' or 'random')

    Returns:
        x: (num_samples, seq_len) - reference/far-end signal
        d: (num_samples, seq_len) - near-end signal (echo + noise)
        h: (num_samples, filter_length) - true echo path
    """
    # Generate random speech-like signal (colored noise)
    x = torch.randn(num_samples, seq_len)

    # Generate echo path
    if echo_path_type == 'itu_g168':
        h = _generate_itu_echo_path(num_samples, filter_length)
    else:
        h = torch.randn(num_samples, filter_length) * 0.5

    # Convolve with echo path
    d = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        x_i = x[i].unsqueeze(0).unsqueeze(0)   # (1, 1, seq_len)
        h_i = h[i].unsqueeze(0).unsqueeze(0)   # (1, 1, filter_length)
        echo = torch.nn.functional.conv1d(x_i, h_i, padding=filter_length - 1)
        d[i] = echo.squeeze()[:seq_len]

    # Add noise
    noise_power = 10 ** (-snr_db / 10)
    noise = torch.randn(num_samples, seq_len) * np.sqrt(noise_power)
    d = d + noise

    return x, d, h


def generate_channel_equalization_data(
    num_samples: int = 10000,
    seq_len: int = 8000,
    channel_length: int = 11,
    snr_db: float = 30.0
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate channel equalization data.

    Setup: Signal s(n) passes through channel c(n) to produce
    received signal x(n) = c * s(n) + noise. Equalizer w estimates
    the inverse channel.

    Args:
        num_samples: Number of sequences
        seq_len: Sequence length
        channel_length: Channel impulse response length
        snr_db: Signal-to-noise ratio

    Returns:
        x: (num_samples, seq_len) - received signal
        d: (num_samples, seq_len) - desired signal (delayed original)
        channel: (num_samples, channel_length) - true channel
    """
    # BPSK source signal
    s = 2 * (torch.rand(num_samples, seq_len) > 0.5).float() - 1

    # Generate frequency-selective channels
    channel = _generate_random_channel(num_samples, channel_length)

    # Pass through channel
    x = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        s_i = s[i].unsqueeze(0).unsqueeze(0)       # (1, 1, seq_len)
        ch_i = channel[i].unsqueeze(0).unsqueeze(0) # (1, 1, channel_length)
        x[i] = torch.nn.functional.conv1d(s_i, ch_i, padding=channel_length - 1).squeeze()[:seq_len]

    # Add noise
    noise_power = 10 ** (-snr_db / 10)
    x = x + torch.randn(num_samples, seq_len) * np.sqrt(noise_power)

    # Desired output: delayed version of original signal
    delay = channel_length // 2
    d = torch.zeros(num_samples, seq_len)
    d[:, delay:] = s[:, :seq_len - delay]

    return x, d, channel


def generate_noise_reduction_data(
    num_samples: int = 10000,
    seq_len: int = 8000,
    snr_db: float = 5.0,
    noise_type: str = 'white'
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate adaptive noise cancellation data.

    Setup: Clean signal s(n) corrupted by noise v1(n).
    Reference noise v2(n) correlated with v1(n) is available.
    Adaptive filter estimates the noise path.

    Args:
        num_samples: Number of sequences
        seq_len: Sequence length
        snr_db: Signal-to-noise ratio
        noise_type: Type of noise ('white', 'colored')

    Returns:
        x: (num_samples, seq_len) - reference noise signal
        d: (num_samples, seq_len) - noisy signal (clean + noise)
        s: (num_samples, seq_len) - clean signal
    """
    # Generate clean signal (sum of sinusoids - speech-like)
    t = torch.linspace(0, 1, seq_len)
    s = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        freqs = torch.rand(5) * 500 + 100  # Random frequencies
        for f in freqs:
            s[i] += torch.sin(2 * np.pi * f * t + torch.rand(1) * 2 * np.pi)
        s[i] = s[i] / s[i].std()

    # Generate correlated noise
    if noise_type == 'white':
        v2 = torch.randn(num_samples, seq_len)
    else:  # colored noise
        v2 = torch.randn(num_samples, seq_len)
        # Simple low-pass filter
        for i in range(num_samples):
            v2[i] = torch.nn.functional.conv1d(
                v2[i].unsqueeze(0).unsqueeze(0),
                torch.ones(1, 1, 5) / 5,
                padding=2
            ).squeeze()

    # Generate correlated noise for the primary channel
    noise_path = torch.randn(num_samples, 11) * 0.3
    v1 = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        v2_i = v2[i].unsqueeze(0).unsqueeze(0)           # (1, 1, seq_len)
        np_i = noise_path[i].unsqueeze(0).unsqueeze(0)   # (1, 1, 11)
        v1[i] = torch.nn.functional.conv1d(v2_i, np_i, padding=5).squeeze()[:seq_len]

    # Mix signal and noise
    noise_power = 10 ** (-snr_db / 10)
    d = s + v1 * np.sqrt(noise_power)

    return v2, d, s


def _generate_itu_echo_path(num_samples: int, length: int) -> torch.Tensor:
    """Generate ITU-T G.168-like echo path impulse responses."""
    h = torch.zeros(num_samples, length)
    for i in range(num_samples):
        # Typical echo path: sparse with a few dominant taps
        h[i, 0] = 1.0
        h[i, length // 4] = 0.5 + torch.rand(1).item() * 0.3
        h[i, length // 2] = 0.2 + torch.rand(1).item() * 0.2
        h[i, 3 * length // 4] = 0.1 + torch.rand(1).item() * 0.1

        # Add some random small taps
        num_small = np.random.randint(5, 15)
        for _ in range(num_small):
            idx = np.random.randint(0, length)
            h[i, idx] = torch.randn(1).item() * 0.05

        # Normalize
        h[i] = h[i] / torch.norm(h[i])
    return h


def _generate_random_channel(num_samples: int, length: int) -> torch.Tensor:
    """Generate random frequency-selective channels."""
    channel = torch.randn(num_samples, length)
    # Exponential decay
    decay = torch.exp(-torch.arange(length).float() * 0.3)
    channel = channel * decay.unsqueeze(0)
    # Normalize
    channel = channel / torch.norm(channel, dim=1, keepdim=True)
    return channel


if __name__ == "__main__":
    # Test data generation
    print("Generating echo cancellation data...")
    x, d, h = generate_echo_cancellation_data(num_samples=2, seq_len=1000)
    print(f"  x: {x.shape}, d: {d.shape}, h: {h.shape}")

    print("Generating channel equalization data...")
    x, d, ch = generate_channel_equalization_data(num_samples=2, seq_len=1000)
    print(f"  x: {x.shape}, d: {d.shape}, channel: {ch.shape}")

    print("Generating noise reduction data...")
    x, d, s = generate_noise_reduction_data(num_samples=2, seq_len=1000)
    print(f"  x: {x.shape}, d: {d.shape}, s: {s.shape}")
