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


def generate_nonstationary_echo_data(
    num_samples: int = 10000,
    seq_len: int = 8000,
    filter_length: int = 64,
    snr_db: float = 20.0,
    num_changes: int = 3
) -> Tuple[torch.Tensor, torch.Tensor, list]:
    """
    Generate non-stationary echo cancellation data.

    The echo path changes abruptly `num_changes` times during the signal.
    This simulates real scenarios like:
    - Speaker moves during a call
    - Room acoustics change (door opens/closes)
    - Network path changes

    Traditional LMS/NLMS struggle to track these changes.
    A learned model can potentially adapt faster.

    Args:
        num_samples: Number of sequences
        seq_len: Sequence length
        filter_length: Filter length
        snr_db: Signal-to-noise ratio
        num_changes: Number of echo path changes

    Returns:
        x: (num_samples, seq_len) - input signal
        d: (num_samples, seq_len) - desired signal (with changing echo)
        h_list: list of (num_samples, filter_length) - echo paths at each segment
    """
    x = torch.randn(num_samples, seq_len)

    # Generate multiple echo paths
    h_list = [_generate_itu_echo_path(num_samples, filter_length) for _ in range(num_changes + 1)]

    # Determine change points (evenly spaced)
    segment_len = seq_len // (num_changes + 1)
    change_points = [i * segment_len for i in range(1, num_changes + 1)]

    # Generate desired signal with changing echo path
    d = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        segments = []
        start = 0
        for seg_idx, end in enumerate(change_points + [seq_len]):
            x_seg = x[i, start:end].unsqueeze(0).unsqueeze(0)
            h_seg = h_list[seg_idx][i].unsqueeze(0).unsqueeze(0)
            echo_seg = torch.nn.functional.conv1d(x_seg, h_seg, padding=filter_length - 1)
            segments.append(echo_seg.squeeze()[:end - start])
            start = end
        d[i] = torch.cat(segments)

    # Add noise
    noise_power = 10 ** (-snr_db / 10)
    d = d + torch.randn(num_samples, seq_len) * np.sqrt(noise_power)

    return x, d, h_list


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


def generate_nonlinear_echo_data(
    num_samples: int = 10000,
    seq_len: int = 8000,
    filter_length: int = 64,
    snr_db: float = 20.0,
    nonlinearity: str = 'tanh',
    nl_strength: float = 0.5
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate nonlinear echo cancellation data.

    Real-world echo paths often contain nonlinearities:
    - Loudspeaker distortion (saturation/clipping)
    - Acoustic nonlinearity
    - Amplifier distortion

    Traditional linear adaptive filters (LMS/NLMS/RLS) cannot model
    these nonlinearities, leading to poor performance.

    A neural network can learn the nonlinear mapping, providing
    a clear advantage over classical methods.

    Args:
        num_samples: Number of sequences
        seq_len: Sequence length
        filter_length: Filter length
        snr_db: Signal-to-noise ratio
        nonlinearity: Type of nonlinearity ('tanh', 'clip', 'poly', 'sigmoid')
        nl_strength: Strength of nonlinearity (0=linear, 1=strong)

    Returns:
        x: (num_samples, seq_len) - input signal
        d: (num_samples, seq_len) - desired signal (nonlinear echo + noise)
        h: (num_samples, filter_length) - true linear component of echo path
    """
    x = torch.randn(num_samples, seq_len)
    h = _generate_itu_echo_path(num_samples, filter_length)

    # Linear convolution
    d_linear = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        x_i = x[i].unsqueeze(0).unsqueeze(0)
        h_i = h[i].unsqueeze(0).unsqueeze(0)
        echo = torch.nn.functional.conv1d(x_i, h_i, padding=filter_length - 1)
        d_linear[i] = echo.squeeze()[:seq_len]

    # Apply nonlinearity
    if nonlinearity == 'tanh':
        # Soft saturation (like loudspeaker)
        d = (1 - nl_strength) * d_linear + nl_strength * torch.tanh(d_linear * 2)
    elif nonlinearity == 'clip':
        # Hard clipping
        clip_level = 1.0 - nl_strength * 0.5
        d = torch.clamp(d_linear, -clip_level, clip_level)
    elif nonlinearity == 'poly':
        # Polynomial nonlinearity: y = x + a*x^2 + b*x^3
        d = d_linear + nl_strength * 0.3 * d_linear**2 + nl_strength * 0.1 * d_linear**3
    elif nonlinearity == 'sigmoid':
        # Sigmoid saturation
        d = (1 - nl_strength) * d_linear + nl_strength * torch.sigmoid(d_linear * 3) - 0.5
    elif nonlinearity == 'pure_nonlinear':
        # Pure nonlinear mapping (no linear component)
        # NLMS cannot handle this at all
        d = torch.tanh(x * 3) * 0.5 + torch.sin(x * 5) * 0.3
    else:
        d = d_linear

    # Add noise
    noise_power = 10 ** (-snr_db / 10)
    d = d + torch.randn(num_samples, seq_len) * np.sqrt(noise_power)

    return x, d, h


def generate_robust_echo_data(
    num_samples: int = 10000,
    seq_len: int = 8000,
    filter_length: int = 64,
    snr_db: float = 20.0,
    outlier_prob: float = 0.01,
    noise_type: str = 'colored'
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate echo cancellation data with challenging conditions.

    This creates scenarios where traditional methods struggle:
    1. Colored noise (violates white noise assumption of NLMS/RLS)
    2. Outliers/spikes (impulse干扰)
    3. Non-Gaussian noise

    Args:
        num_samples: Number of sequences
        seq_len: Sequence length
        filter_length: Filter length
        snr_db: Signal-to-noise ratio
        outlier_prob: Probability of outlier at each sample
        noise_type: 'white', 'colored', or 'impulsive'

    Returns:
        x: (num_samples, seq_len) - input signal
        d: (num_samples, seq_len) - desired signal
        h: (num_samples, filter_length) - true echo path
    """
    x = torch.randn(num_samples, seq_len)
    h = _generate_itu_echo_path(num_samples, filter_length)

    # Convolve with echo path
    d = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        x_i = x[i].unsqueeze(0).unsqueeze(0)
        h_i = h[i].unsqueeze(0).unsqueeze(0)
        echo = torch.nn.functional.conv1d(x_i, h_i, padding=filter_length - 1)
        d[i] = echo.squeeze()[:seq_len]

    # Generate challenging noise
    if noise_type == 'colored':
        # Colored noise (low-pass filtered white noise)
        noise = torch.randn(num_samples, seq_len)
        # Simple low-pass filter
        kernel = torch.ones(1, 1, 11) / 11
        for i in range(num_samples):
            noise[i] = torch.nn.functional.conv1d(
                noise[i].unsqueeze(0).unsqueeze(0),
                kernel, padding=5
            ).squeeze()[:seq_len]
    elif noise_type == 'impulsive':
        # Impulsive noise (sparse large spikes)
        noise = torch.randn(num_samples, seq_len) * 0.1
        mask = torch.rand(num_samples, seq_len) < outlier_prob
        noise[mask] = torch.randn(mask.sum()) * 10  # Large spikes
    else:
        noise = torch.randn(num_samples, seq_len)

    # Scale noise to desired SNR
    noise_power = 10 ** (-snr_db / 10)
    signal_power = (d ** 2).mean()
    noise = noise * torch.sqrt(signal_power * noise_power / (noise.var() + 1e-10))

    d = d + noise

    return x, d, h


def generate_loudspeaker_echo_data(
    num_samples: int = 10000,
    seq_len: int = 8000,
    filter_length: int = 64,
    snr_db: float = 20.0,
    nl_type: str = 'hard_clip',
    nl_params: dict = None
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate loudspeaker echo cancellation data with severe nonlinearity.

    Signal path: x(n) -> linear echo path h -> nonlinear distortion f(.) -> d(n)

    Real loudspeakers exhibit:
    - Hard clipping at saturation
    - Soft saturation (tanh-like)
    - Harmonic distortion
    - Intermodulation

    Linear adaptive filters (LMS/NLMS/RLS) CANNOT model the nonlinear part.
    The residual error after linear cancellation contains the nonlinear component.
    A neural network can learn this nonlinear residual.

    Args:
        num_samples: Number of sequences
        seq_len: Sequence length
        filter_length: Filter length
        snr_db: Signal-to-noise ratio
        nl_type: Type of nonlinearity ('hard_clip', 'soft_clip', 'poly5', 'crossover')
        nl_params: Additional parameters for nonlinearity

    Returns:
        x: (num_samples, seq_len) - input signal
        d: (num_samples, seq_len) - desired signal (nonlinear echo + noise)
        h: (num_samples, filter_length) - true linear echo path
    """
    if nl_params is None:
        nl_params = {}

    x = torch.randn(num_samples, seq_len) * 0.8
    h = _generate_itu_echo_path(num_samples, filter_length)

    # Linear convolution
    d_linear = torch.zeros(num_samples, seq_len)
    for i in range(num_samples):
        x_i = x[i].unsqueeze(0).unsqueeze(0)
        h_i = h[i].unsqueeze(0).unsqueeze(0)
        echo = torch.nn.functional.conv1d(x_i, h_i, padding=filter_length - 1)
        d_linear[i] = echo.squeeze()[:seq_len]

    # Apply severe nonlinearity
    if nl_type == 'hard_clip':
        # Hard clipping - loudspeaker saturation
        threshold = nl_params.get('threshold', 0.3)
        d = torch.clamp(d_linear, -threshold, threshold)
    elif nl_type == 'soft_clip':
        # Soft clipping with very steep tanh
        gain = nl_params.get('gain', 10.0)
        d = torch.tanh(d_linear * gain)
    elif nl_type == 'poly5':
        # 5th-order polynomial (common loudspeaker model)
        # y = x + a2*x^2 + a3*x^3 + a5*x^5
        a2 = nl_params.get('a2', 0.5)
        a3 = nl_params.get('a3', -0.3)
        a5 = nl_params.get('a5', 0.1)
        d = d_linear + a2 * d_linear**2 + a3 * d_linear**3 + a5 * d_linear**5
    elif nl_type == 'crossover':
        # Crossover distortion (class-B amplifier)
        dead_zone = nl_params.get('dead_zone', 0.2)
        d = torch.where(
            torch.abs(d_linear) < dead_zone,
            torch.zeros_like(d_linear),
            d_linear - torch.sign(d_linear) * dead_zone
        )
    elif nl_type == 'mixed':
        # Mixed: linear + nonlinear components
        alpha = nl_params.get('alpha', 0.6)  # Linear fraction
        d = alpha * d_linear + (1 - alpha) * torch.tanh(d_linear * 5)
    else:
        d = d_linear

    # Add noise
    noise_power = 10 ** (-snr_db / 10)
    d = d + torch.randn(num_samples, seq_len) * np.sqrt(noise_power)

    return x, d, h


def generate_sparse_channel_data(
    num_samples: int = 10000,
    channel_length: int = 64,
    sparsity: int = 5,
    snr_db: float = 20.0,
    pilot_length: int = None
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate sparse multipath channel estimation data.

    Setup: Pilot signal x passes through sparse channel h to produce
    received signal d = x * h + noise. Goal: estimate h from (x, d).

    The channel h has only K non-zero taps out of N total (sparse).
    Classical LMS/NLMS ignores sparsity -> suboptimal.
    Deep-unfolded ISTA (LISTA) learns to exploit sparsity -> better.

    Args:
        num_samples: Number of channel realizations
        channel_length: Length of channel impulse response (N)
        sparsity: Number of non-zero taps (K)
        snr_db: Signal-to-noise ratio
        pilot_length: Length of pilot signal (default: 2 * channel_length)

    Returns:
        x: (num_samples, pilot_length) - pilot/reference signal
        d: (num_samples, pilot_length) - received signal (y = x * h + noise)
        h: (num_samples, channel_length) - true sparse channel
    """
    if pilot_length is None:
        pilot_length = 2 * channel_length

    # Generate sparse channels
    h = torch.zeros(num_samples, channel_length)
    for i in range(num_samples):
        # Random tap positions
        tap_positions = torch.randperm(channel_length)[:sparsity]
        # Random tap values (exponentially decaying)
        tap_values = torch.randn(sparsity) * torch.exp(
            -torch.arange(sparsity).float() * 0.2
        )
        h[i, tap_positions] = tap_values

    # Generate pilot signals (BPSK)
    x = 2 * (torch.rand(num_samples, pilot_length) > 0.5).float() - 1

    # Convolve: d = x * h + noise
    # Note: torch.conv1d does cross-correlation, not convolution.
    # Flip h to get true convolution: y[n] = sum_k x[n-k]*h[k]
    d = torch.zeros(num_samples, pilot_length)
    for i in range(num_samples):
        x_i = x[i].unsqueeze(0).unsqueeze(0)
        h_i = h[i].unsqueeze(0).unsqueeze(0)
        d[i] = torch.nn.functional.conv1d(
            x_i, torch.flip(h_i, [2]), padding=channel_length - 1
        ).squeeze()[:pilot_length]

    # Add noise
    noise_power = 10 ** (-snr_db / 10)
    noise = torch.randn(num_samples, pilot_length) * np.sqrt(noise_power)
    d = d + noise

    return x, d, h


def generate_sparse_channel_test(
    channel_length: int = 64,
    sparsity: int = 5,
    snr_db: float = 20.0,
    num_test: int = 100
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Generate test data with fixed seed for reproducibility."""
    torch.manual_seed(42)
    return generate_sparse_channel_data(
        num_samples=num_test,
        channel_length=channel_length,
        sparsity=sparsity,
        snr_db=snr_db
    )


def generate_complex_sparse_channel_data(
    num_samples: int = 10000,
    channel_length: int = 64,
    sparsity: int = 5,
    snr_db: float = 20.0,
    pilot_length: int = None
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate complex-valued sparse channel estimation data.

    Uses QPSK pilots and complex-valued channels.
    Soft-thresholding operates on magnitude while preserving phase.

    Args:
        num_samples: Number of channel realizations
        channel_length: Length of channel impulse response (N)
        sparsity: Number of non-zero taps (K)
        snr_db: Signal-to-noise ratio
        pilot_length: Length of pilot signal (default: 2 * channel_length)

    Returns:
        x: (num_samples, pilot_length) complex - QPSK pilot signal
        d: (num_samples, pilot_length) complex - received signal
        h: (num_samples, channel_length) complex - true sparse channel
    """
    if pilot_length is None:
        pilot_length = 2 * channel_length

    # Generate complex sparse channels
    h = torch.zeros(num_samples, channel_length, dtype=torch.cfloat)
    for i in range(num_samples):
        tap_positions = torch.randperm(channel_length)[:sparsity]
        # Complex tap values with exponential decay
        tap_real = torch.randn(sparsity) * torch.exp(
            -torch.arange(sparsity).float() * 0.2
        )
        tap_imag = torch.randn(sparsity) * torch.exp(
            -torch.arange(sparsity).float() * 0.2
        )
        h[i, tap_positions] = torch.complex(tap_real, tap_imag)

    # Generate QPSK pilot signals: (±1±j)/√2
    x_real = 2 * (torch.rand(num_samples, pilot_length) > 0.5).float() - 1
    x_imag = 2 * (torch.rand(num_samples, pilot_length) > 0.5).float() - 1
    x = torch.complex(x_real, x_imag) / np.sqrt(2)

    # Convolve: d = x * h + noise (complex)
    d = torch.zeros(num_samples, pilot_length, dtype=torch.cfloat)
    for i in range(num_samples):
        x_i = x[i].unsqueeze(0).unsqueeze(0)
        h_i = h[i].unsqueeze(0).unsqueeze(0)
        d[i] = torch.nn.functional.conv1d(
            x_i, torch.flip(h_i, [2]), padding=channel_length - 1
        ).squeeze()[:pilot_length]

    # Add complex AWGN
    sig_power = torch.mean(torch.abs(d) ** 2).item()
    noise_power = sig_power / (10 ** (snr_db / 10))
    noise = (torch.randn(num_samples, pilot_length) +
             1j * torch.randn(num_samples, pilot_length)) * np.sqrt(noise_power / 2)
    d = d + noise

    return x, d, h


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
