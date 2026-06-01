"""
Generate publication-quality figures for the LISTA channel estimation paper.

Follows nature-figure skill guidelines:
- Python backend (matplotlib)
- Professional palette (Nature Machine Intelligence style)
- 300+ DPI PDF output
- Editable TrueType text (pdf.fonttype = 42)

Usage:
    cd paper
    python generate_figures.py
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ============================================================
# Nature-figure skill: rcParams quick-start
# ============================================================
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "figure.dpi": 150,
})

# Color palette (nature-figure skill)
BLUE_MAIN = "#0F4D92"
BLUE_SEC = "#3775BA"
GREEN = "#2E9E44"
RED_STRONG = "#B64342"
TEAL = "#42949E"
VIOLET = "#9A4D8E"
NEUTRAL = "#767676"
NEUTRAL_LIGHT = "#CFCECE"
ORANGE = "#E67E22"

# Method colors
COLOR_LISTA = BLUE_MAIN
COLOR_OMP = RED_STRONG
COLOR_ISTA = TEAL
COLOR_FISTA = VIOLET
COLOR_LMS = NEUTRAL
COLOR_NLMS = NEUTRAL_LIGHT
COLOR_LASSO = ORANGE

OUTDIR = os.path.dirname(os.path.abspath(__file__))


def save_pub(fig, name, dpi=300):
    """Save figure as PDF (primary) and PNG (preview)."""
    fig.savefig(os.path.join(OUTDIR, f"{name}.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(OUTDIR, f"{name}.png"), dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {name}.pdf / .png")


# ============================================================
# Figure 1: Architecture Diagram
# ============================================================
def fig_architecture():
    """LISTA architecture schematic."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(5, 3.2, 'LISTA Architecture for Sparse Channel Estimation',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # Input block
    rect = mpatches.FancyBboxPatch((-0.3, 0.5), 1.6, 2, boxstyle="round,pad=0.1",
                                    facecolor=BLUE_SEC, edgecolor=BLUE_MAIN, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(0.5, 1.8, 'Input', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(0.5, 1.2, r'$\mathbf{x}, \mathbf{d}$', ha='center', va='center', fontsize=9, color='white')

    # Arrow from input to first layer
    ax.annotate('', xy=(1.8, 1.5), xytext=(1.3, 1.5),
                arrowprops=dict(arrowstyle='->', color=BLUE_MAIN, lw=1.5))

    # Layer blocks (show 3 representative layers out of L=20)
    layer_labels = ['Layer 1', 'Layer 2', r'$\cdots$', r'Layer $L$']
    layer_x = [2.2, 4.2, 6.0, 7.8]

    for i, (x, label) in enumerate(zip(layer_x, layer_labels)):
        if label == r'$\cdots$':
            # Dots
            for dx in [-0.15, 0, 0.15]:
                ax.plot(x + dx, 1.5, 'o', color=NEUTRAL, markersize=4)
            continue

        # Layer box
        rect = mpatches.FancyBboxPatch((x - 0.5, 0.3), 2.0, 2.4,
                                        boxstyle="round,pad=0.1",
                                        facecolor='#E8F0FE', edgecolor=BLUE_MAIN, linewidth=1.2)
        ax.add_patch(rect)

        # Layer label
        ax.text(x + 0.5, 2.35, label, ha='center', va='center', fontsize=8,
                fontweight='bold', color=BLUE_MAIN)

        # W^(k) block
        rect_w = mpatches.FancyBboxPatch((x - 0.3, 1.5), 0.7, 0.6,
                                          boxstyle="round,pad=0.05",
                                          facecolor=BLUE_MAIN, edgecolor=BLUE_MAIN, linewidth=0.8)
        ax.add_patch(rect_w)
        ax.text(x + 0.05, 1.8, r'$\mathbf{W}^{(k)}$', ha='center', va='center',
                fontsize=7, color='white', fontweight='bold')

        # mu^(k) block
        rect_mu = mpatches.FancyBboxPatch((x + 0.5, 1.5), 0.7, 0.6,
                                           boxstyle="round,pad=0.05",
                                           facecolor=ORANGE, edgecolor=ORANGE, linewidth=0.8)
        ax.add_patch(rect_mu)
        ax.text(x + 0.85, 1.8, r'$\mu^{(k)}$', ha='center', va='center',
                fontsize=7, color='white', fontweight='bold')

        # Gradient block
        ax.text(x + 0.5, 1.2, r'$\mathbf{g}^{(k)}$', ha='center', va='center',
                fontsize=7, color=NEUTRAL)

        # Soft thresholding
        rect_s = mpatches.FancyBboxPatch((x + 0.1, 0.4), 0.8, 0.6,
                                          boxstyle="round,pad=0.05",
                                          facecolor=GREEN, edgecolor=GREEN, linewidth=0.8)
        ax.add_patch(rect_s)
        ax.text(x + 0.5, 0.7, r'$\mathcal{S}_{\theta^{(k)}}$', ha='center', va='center',
                fontsize=7, color='white', fontweight='bold')

    # Arrows between layers
    for x1, x2 in [(1.8, 1.7), (3.7, 3.7), (5.5, 5.5), (7.3, 7.3)]:
        if x1 == 1.8:
            ax.annotate('', xy=(1.7, 1.5), xytext=(1.3, 1.5),
                        arrowprops=dict(arrowstyle='->', color=BLUE_MAIN, lw=1.2))
        elif x1 == 3.7:
            ax.annotate('', xy=(3.7, 1.5), xytext=(3.7, 1.5),
                        arrowprops=dict(arrowstyle='->', color=BLUE_MAIN, lw=1.2))

    # Arrows between layer blocks
    for x1, x2 in [(3.7, 3.7), (5.5, 5.5), (7.3, 7.3)]:
        pass  # The layer boxes are close enough

    # Output block
    rect = mpatches.FancyBboxPatch((9.0, 0.5), 1.6, 2, boxstyle="round,pad=0.1",
                                    facecolor=GREEN, edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(9.8, 1.8, 'Output', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    ax.text(9.8, 1.2, r'$\hat{\mathbf{h}}$', ha='center', va='center', fontsize=11, color='white')

    # Arrow to output
    ax.annotate('', xy=(9.0, 1.5), xytext=(8.5, 1.5),
                arrowprops=dict(arrowstyle='->', color=BLUE_MAIN, lw=1.5))

    # Legend at bottom
    legend_elements = [
        mpatches.Patch(facecolor=BLUE_MAIN, label=r'Linear mapping $\mathbf{W}^{(k)}$'),
        mpatches.Patch(facecolor=ORANGE, label=r'Step size $\mu^{(k)}$'),
        mpatches.Patch(facecolor=GREEN, label=r'Thresholding $\mathcal{S}_{\theta^{(k)}}$'),
    ]
    ax.legend(handles=legend_elements, loc='lower center', ncol=3,
              fontsize=8, bbox_to_anchor=(0.5, -0.15))

    save_pub(fig, 'fig_architecture')


# ============================================================
# Figure 2: Error Concentration Visualization
# ============================================================
def fig_error_concentration():
    """Bar chart of error concentration on true taps."""
    fig, ax = plt.subplots(figsize=(5, 4))

    methods = ['LISTA', 'OMP', 'ISTA', 'LISTA\n(pre-thresh)']
    means = [100.0, 95.2, 92.4, 68.3]
    stds = [0.0, 0.6, 0.4, 2.1]
    colors = [COLOR_LISTA, COLOR_OMP, COLOR_ISTA, BLUE_SEC]

    bars = ax.bar(methods, means, yerr=stds, capsize=4, color=colors,
                  alpha=0.9, edgecolor='black', linewidth=0.5, width=0.6)

    # Value labels
    for bar, m, s in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{m:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_ylabel('Error on true taps (%)', fontsize=10)
    ax.set_ylim([50, 108])
    ax.axhline(y=100, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.grid(axis='y', alpha=0.3)

    # Annotation
    ax.annotate('LISTA enhances from\n92.4% (ISTA) to 100.0%',
                xy=(0, 100), xytext=(1.5, 80),
                fontsize=8, ha='center',
                arrowprops=dict(arrowstyle='->', color=BLUE_MAIN, lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

    save_pub(fig, 'fig_error_concentration')


# ============================================================
# Figure 3: BER-NMSE Disconnect
# ============================================================
def fig_ber_nmse_disconnect():
    """Dual-panel: NMSE vs SNR and BER vs SNR under ZF."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))

    snr = np.array([-5, 0, 5, 10, 15, 20, 25, 30, 40])

    # Panel A: NMSE vs SNR
    lista_nmse = np.array([-3.83, -11.01, -15.98, -22.80, -24.36, -24.25, -25.08, -25.02, -25.02])
    omp_nmse = np.array([-6.43, -13.23, -19.10, -25.65, -30.62, -37.09, -42.21, -48.51, -58.04])
    fista_nmse = np.array([-4.52, -11.87, -17.24, -23.91, -28.14, -33.85, -38.67, -43.12, -52.45])

    ax1.plot(snr, omp_nmse, '-s', color=COLOR_OMP, label='OMP', markersize=4, linewidth=1.5)
    ax1.plot(snr, fista_nmse, '-^', color=COLOR_FISTA, label='FISTA', markersize=4, linewidth=1.5)
    ax1.plot(snr, lista_nmse, '-o', color=COLOR_LISTA, label='LISTA', markersize=5, linewidth=2)

    ax1.set_xlabel('SNR (dB)', fontsize=10)
    ax1.set_ylabel('NMSE (dB)', fontsize=10)
    ax1.set_title('(a) NMSE vs SNR', fontsize=10, fontweight='bold')
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    # Highlight the gap
    ax1.annotate('', xy=(20, -24.25), xytext=(20, -37.09),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    ax1.text(22, -31, '12.8 dB\ngap', fontsize=7, ha='left', va='center', color='gray')

    # Panel B: 16-QAM BER under ZF
    snr_ber = np.array([0, 5, 10, 15, 20, 25, 30])
    lista_ber = np.array([0.425, 0.380, 0.343, 0.318, 0.305, 0.297, 0.292])
    omp_ber = np.array([0.426, 0.383, 0.346, 0.325, 0.316, 0.314, 0.313])

    ax2.plot(snr_ber, omp_ber, '-s', color=COLOR_OMP, label='OMP', markersize=4, linewidth=1.5)
    ax2.plot(snr_ber, lista_ber, '-o', color=COLOR_LISTA, label='LISTA', markersize=5, linewidth=2)

    # Shade the LISTA advantage region
    ax2.fill_between(snr_ber, omp_ber, lista_ber,
                     where=(lista_ber < omp_ber), alpha=0.15, color=GREEN, label='LISTA advantage')

    ax2.set_xlabel('SNR (dB)', fontsize=10)
    ax2.set_ylabel('16-QAM BER', fontsize=10)
    ax2.set_title('(b) BER under ZF equalization', fontsize=10, fontweight='bold')
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)

    # Mark significance
    for snr_val, p_str in [(15, '*'), (20, '**'), (25, '**'), (30, '**')]:
        idx = np.where(snr_ber == snr_val)[0][0]
        ax2.text(snr_val, lista_ber[idx] - 0.008, p_str, ha='center', fontsize=9,
                fontweight='bold', color=RED_STRONG)

    plt.tight_layout()
    save_pub(fig, 'fig_ber_nmse_disconnect')


# ============================================================
# Figure 4: Threshold Comparison
# ============================================================
def fig_threshold_comparison():
    """Grouped bar: soft vs hard vs semi-soft thresholding."""
    fig, ax = plt.subplots(figsize=(4.5, 4))

    methods = ['Soft\n(LISTA)', 'Hard', 'Semi-soft\n(garrote)']
    nmse = [-24.59, -31.72, -27.85]
    std = [0.18, 0.11, 0.08]
    colors = [COLOR_LISTA, RED_STRONG, ORANGE]

    bars = ax.bar(methods, nmse, yerr=std, capsize=4, color=colors,
                  alpha=0.9, edgecolor='black', linewidth=0.5, width=0.5)

    # Value labels
    for bar, m in zip(bars, nmse):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.5,
                f'{m:.1f}', ha='center', va='top', fontsize=9, fontweight='bold', color='white')

    # Annotation for the gap
    ax.annotate('', xy=(0, -24.59), xytext=(1, -31.72),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1.2))
    ax.text(0.5, -28.5, '7.1 dB\n$p < 0.001$', ha='center', fontsize=8, color='gray')

    ax.set_ylabel('NMSE (dB)', fontsize=10)
    ax.set_ylim([-35, -22])
    ax.grid(axis='y', alpha=0.3)
    ax.set_title('Threshold Function Comparison', fontsize=10, fontweight='bold')

    save_pub(fig, 'fig_threshold_comparison')


# ============================================================
# Figure 5: Learned Threshold Schedule
# ============================================================
def fig_threshold_schedule():
    """Per-layer learned threshold values with error bands."""
    fig, ax = plt.subplots(figsize=(5, 4))

    layers = np.arange(20)
    # From the paper: Table 9 learned thresholds (mean)
    theta_mean = [0.0234, 0.0221, 0.0209, 0.0198, 0.0187,
                  0.0177, 0.0168, 0.0159, 0.0152, 0.0145,
                  0.0139, 0.0133, 0.0128, 0.0124, 0.0120,
                  0.0117, 0.0115, 0.0113, 0.0112, 0.0110]
    # Approximate std (from 20 seeds)
    theta_std = [0.0018, 0.0017, 0.0016, 0.0015, 0.0015,
                 0.0014, 0.0013, 0.0013, 0.0012, 0.0012,
                 0.0011, 0.0011, 0.0010, 0.0010, 0.0010,
                 0.0009, 0.0009, 0.0009, 0.0009, 0.0009]

    theta_mean = np.array(theta_mean)
    theta_std = np.array(theta_std)

    ax.plot(layers, theta_mean * 1000, '-o', color=BLUE_MAIN, markersize=4, linewidth=2,
            label=r'Learned $\theta^{(k)}$')
    ax.fill_between(layers,
                    (theta_mean - theta_std) * 1000,
                    (theta_mean + theta_std) * 1000,
                    alpha=0.2, color=BLUE_MAIN)

    # Step sizes on secondary axis
    ax2 = ax.twinx()
    mu_mean = [0.482, 0.474, 0.466, 0.458, 0.456,
               0.448, 0.440, 0.434, 0.431, 0.424,
               0.418, 0.413, 0.408, 0.404, 0.400,
               0.397, 0.395, 0.393, 0.392, 0.390]
    ax2.plot(layers, mu_mean, '--s', color=ORANGE, markersize=3, linewidth=1.5,
             label=r'Learned $\mu^{(k)}$')
    ax2.set_ylabel(r'Step size $\mu^{(k)}$', fontsize=10, color=ORANGE)
    ax2.tick_params(axis='y', labelcolor=ORANGE)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(ORANGE)

    ax.set_xlabel('Layer $k$', fontsize=10)
    ax.set_ylabel(r'Threshold $\theta^{(k)}$ ($\times 10^{-3}$)', fontsize=10)
    ax.set_xticks(layers[::2])
    ax.grid(alpha=0.3)

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper right')

    # Annotation
    ax.annotate('Decreasing schedule:\naggressive early, gentle late',
                xy=(15, theta_mean[15]*1000), xytext=(10, 22),
                fontsize=8, ha='center',
                arrowprops=dict(arrowstyle='->', color='gray', lw=1),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

    save_pub(fig, 'fig_threshold_schedule')


# ============================================================
# Figure 6: Summary / Contribution Overview
# ============================================================
def fig_summary():
    """Conceptual summary figure of LISTA's value proposition."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Title
    ax.text(5, 5.6, 'LISTA for Sparse Channel Estimation: Key Findings',
            ha='center', va='center', fontsize=12, fontweight='bold')

    # Box 1: NMSE Performance
    rect = mpatches.FancyBboxPatch((0.3, 3.5), 4.2, 1.8, boxstyle="round,pad=0.15",
                                    facecolor='#FFF3E0', edgecolor=ORANGE, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(2.4, 5.0, 'NMSE Performance', ha='center', fontsize=10, fontweight='bold', color=ORANGE)
    ax.text(2.4, 4.5, 'LISTA: $-25$ dB (saturates)', ha='center', fontsize=9, color=RED_STRONG)
    ax.text(2.4, 4.1, 'OMP: $-37$ dB | FISTA: $-34$ dB', ha='center', fontsize=9, color=NEUTRAL)
    ax.text(2.4, 3.7, r'$\Rightarrow$ LISTA trails by 12--27 dB', ha='center', fontsize=9,
            fontweight='bold', color=RED_STRONG)

    # Box 2: BER Performance
    rect = mpatches.FancyBboxPatch((5.5, 3.5), 4.2, 1.8, boxstyle="round,pad=0.15",
                                    facecolor='#E8F5E9', edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7.6, 5.0, 'BER Performance (ZF, 16-QAM)', ha='center', fontsize=10,
            fontweight='bold', color=GREEN)
    ax.text(7.6, 4.5, 'LISTA matches or beats OMP', ha='center', fontsize=9, color=GREEN)
    ax.text(7.6, 4.1, 'at SNR $\\geq 15$ dB ($p < 0.05$)', ha='center', fontsize=9, color=NEUTRAL)
    ax.text(7.6, 3.7, r'$\Rightarrow$ BER advantage despite worse NMSE',
            ha='center', fontsize=9, fontweight='bold', color=GREEN)

    # Arrow connecting them
    ax.annotate('', xy=(5.4, 4.4), xytext=(4.6, 4.4),
                arrowprops=dict(arrowstyle='->', color='gray', lw=2))

    # Box 3: Mechanism
    rect = mpatches.FancyBboxPatch((0.3, 1.2), 9.4, 2.0, boxstyle="round,pad=0.15",
                                    facecolor='#E3F2FD', edgecolor=BLUE_MAIN, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(5, 2.9, 'Mechanism: Error Concentration', ha='center',
            fontsize=11, fontweight='bold', color=BLUE_MAIN)
    ax.text(5, 2.4, 'LISTA concentrates 100.0% of estimation error on true tap locations',
            ha='center', fontsize=9)
    ax.text(5, 2.0, '(vs. 95.2% OMP, 92.4% ISTA) → $267\\times$ less non-support error',
            ha='center', fontsize=9, color=NEUTRAL)
    ax.text(5, 1.5, 'Learned threshold schedule is dominant ($+14$--$18$ dB); '
            'hard thresholding outperforms soft by 7.1 dB',
            ha='center', fontsize=8, color=NEUTRAL)

    # Bottom: Practical recommendation
    rect = mpatches.FancyBboxPatch((1.5, 0.1), 7.0, 0.9, boxstyle="round,pad=0.1",
                                    facecolor='#F3E5F5', edgecolor=VIOLET, linewidth=1)
    ax.add_patch(rect)
    ax.text(5, 0.55, 'Use LISTA for throughput-critical ZF systems; OMP/FISTA for NMSE-critical tasks',
            ha='center', fontsize=9, fontweight='bold', color=VIOLET)

    save_pub(fig, 'fig_summary')


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating figures...")
    fig_architecture()
    fig_error_concentration()
    fig_ber_nmse_disconnect()
    fig_threshold_comparison()
    fig_threshold_schedule()
    fig_summary()
    print("Done!")
