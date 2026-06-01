"""
Generate publication-quality figures for the LISTA channel estimation paper.
Pure matplotlib. Fixed layout issues from v1.

Usage:
    cd paper
    python3 generate_figures.py
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os

# ============================================================
# Global style
# ============================================================
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 9,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 8,
    "legend.frameon": True,
    "legend.facecolor": "white",
    "legend.edgecolor": "#cccccc",
    "legend.framealpha": 0.95,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
})

# Color palette
C_LISTA   = "#0F4D92"
C_OMP     = "#B64342"
C_ISTA    = "#42949E"
C_FISTA   = "#9A4D8E"
C_LMS     = "#767676"
C_NLMS    = "#A0A0A0"
C_LASSO   = "#E67E22"
C_GREEN   = "#2E9E44"
C_ORANGE  = "#E67E22"
C_LIGHT   = "#E8F0FE"

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")


def save_pub(fig, name):
    fig.savefig(os.path.join(OUTDIR, f"{name}.pdf"))
    fig.savefig(os.path.join(OUTDIR, f"{name}.png"), dpi=300)
    plt.close(fig)
    print(f"  ✓ {name}")


def arrow(ax, x1, y1, x2, y2, color='#555', lw=1.2):
    """Draw a consistent arrow between two points."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                shrinkA=2, shrinkB=2))


# ============================================================
# Figure 1: Architecture Diagram (v2 - clean arrows, proper spacing)
# ============================================================
def fig_architecture():
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    ax.set_xlim(-0.2, 11.0)
    ax.set_ylim(-0.5, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')

    def rbox(x, y, w, h, fc, ec='#444', lw=0.8):
        r = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                                     facecolor=fc, edgecolor=ec, linewidth=lw)
        ax.add_patch(r)
        return r

    # ---- Input ----
    rbox(0.0, 0.4, 1.3, 1.6, C_LISTA, ec=C_LISTA, lw=1.0)
    ax.text(0.65, 1.55, 'Input', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')
    ax.text(0.65, 0.95, r'$\mathbf{x},\ \mathbf{d}$', ha='center', va='center',
            fontsize=9, color='white')

    # Arrow: Input → Layer 1
    arrow(ax, 1.35, 1.2, 1.8, 1.2)

    # ---- Layer blocks ----
    # Layer 1, Layer 2, dots, Layer L
    lx = [1.85, 4.05, 6.55, 8.45]
    labels = ['Layer 1', 'Layer 2', 'dots', 'Layer $L$']

    for i, (x, lbl) in enumerate(zip(lx, labels)):
        if lbl == 'dots':
            # Three dots
            for dx in [-0.1, 0, 0.1]:
                ax.plot(x + dx, 1.2, 'o', color='#aaa', markersize=3.5, zorder=5)
            continue

        # Outer layer box
        rbox(x, 0.1, 1.9, 2.2, C_LIGHT, ec=C_LISTA, lw=0.6)
        ax.text(x + 0.95, 2.05, lbl, ha='center', va='center',
                fontsize=8, fontweight='bold', color=C_LISTA)

        # W^(k) block
        rbox(x + 0.08, 1.3, 0.6, 0.5, C_LISTA, ec=C_LISTA)
        ax.text(x + 0.38, 1.55, r'$\mathbf{W}^{(k)}$', ha='center', va='center',
                fontsize=6.5, fontweight='bold', color='white')

        # mu^(k) block
        rbox(x + 0.75, 1.3, 0.6, 0.5, C_ORANGE, ec=C_ORANGE)
        ax.text(x + 1.05, 1.55, r'$\mu^{(k)}$', ha='center', va='center',
                fontsize=6.5, fontweight='bold', color='white')

        # gradient label
        ax.text(x + 0.95, 1.08, r'$\mathbf{g}^{(k)}$', ha='center', va='center',
                fontsize=7, color='#555')

        # S_theta block
        rbox(x + 0.3, 0.18, 1.3, 0.5, C_GREEN, ec=C_GREEN)
        ax.text(x + 0.95, 0.43, r'$\mathcal{S}_{\theta^{(k)}}$', ha='center', va='center',
                fontsize=7, fontweight='bold', color='white')

    # ---- Consistent arrows between all stages ----
    # Layer 1 → Layer 2
    arrow(ax, 3.78, 1.2, 4.0, 1.2)
    # Layer 2 → dots
    arrow(ax, 5.98, 1.2, 6.4, 1.2)
    # dots → Layer L
    arrow(ax, 6.7, 1.2, 8.4, 1.2)
    # Layer L → Output
    arrow(ax, 10.38, 1.2, 10.65, 1.2)

    # ---- Output ----
    rbox(10.7, 0.4, 1.1, 1.6, C_GREEN, ec=C_GREEN, lw=1.0)
    ax.text(11.25, 1.55, 'Output', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')
    ax.text(11.25, 0.95, r'$\hat{\mathbf{h}}$', ha='center', va='center',
            fontsize=11, color='white')

    # ---- Legend ----
    leg = [
        mpatches.Patch(facecolor=C_LISTA, edgecolor='#444', label=r'Linear $\mathbf{W}^{(k)}$'),
        mpatches.Patch(facecolor=C_ORANGE, edgecolor='#444', label=r'Step $\mu^{(k)}$'),
        mpatches.Patch(facecolor=C_GREEN, edgecolor='#444', label=r'Threshold $\mathcal{S}_{\theta^{(k)}}$'),
    ]
    ax.legend(handles=leg, loc='lower center', ncol=3, fontsize=8,
              bbox_to_anchor=(0.5, -0.08), frameon=False)

    save_pub(fig, 'fig_architecture')


# ============================================================
# Figure 2: NMSE vs SNR
# ============================================================
def fig_nmse_vs_snr():
    fig, ax = plt.subplots(figsize=(5.5, 4))

    snr = np.array([-5, 0, 5, 10, 15, 20, 25, 30, 40])
    lms   = np.array([-2.78, -5.90, -8.79, -11.90, -13.64, -14.51, -15.74, -16.50, -16.41])
    nlms  = np.array([-2.65, -5.92, -9.16, -12.21, -14.53, -16.61, -17.58, -18.40, -18.20])
    omp   = np.array([-6.43, -13.23, -19.10, -25.65, -30.62, -37.09, -42.21, -48.51, -58.04])
    lasso = np.array([-0.55, -5.99, -11.42, -17.02, -22.01, -28.64, -35.53, -42.36, -50.88])
    fista = np.array([-4.52, -11.87, -17.24, -23.91, -28.14, -33.85, -38.67, -43.12, -52.45])
    lista = np.array([-3.83, -11.01, -15.98, -22.80, -24.36, -24.25, -25.08, -25.02, -25.02])

    ax.plot(snr, omp,   '-s', color=C_OMP,   label='OMP',   markersize=5, linewidth=1.5)
    ax.plot(snr, fista, '-^', color=C_FISTA,  label='FISTA', markersize=5, linewidth=1.5)
    ax.plot(snr, lasso, '-D', color=C_LASSO,  label='LASSO', markersize=4, linewidth=1.2)
    ax.plot(snr, nlms,  '--', color=C_NLMS,   label='NLMS',  linewidth=1.0, alpha=0.7)
    ax.plot(snr, lms,   ':',  color=C_LMS,    label='LMS',   linewidth=1.0, alpha=0.7)
    ax.plot(snr, lista, '-o', color=C_LISTA,  label='LISTA', markersize=6, linewidth=2.2)

    ax.set_xlabel('SNR (dB)')
    ax.set_ylabel('NMSE (dB)')
    ax.legend(fontsize=7.5, ncol=2, loc='lower left')
    ax.grid(alpha=0.25)
    ax.set_ylim([-62, 5])

    ax.annotate('LISTA saturates\nat $\\approx -25$ dB',
                xy=(25, -25), xytext=(32, -10),
                fontsize=7.5, ha='center', color=C_LISTA,
                arrowprops=dict(arrowstyle='->', color=C_LISTA, lw=1),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0FE',
                          edgecolor=C_LISTA, alpha=0.85))

    save_pub(fig, 'fig_nmse_vs_snr')


# ============================================================
# Figure 3: NMSE vs Sparsity
# ============================================================
def fig_nmse_vs_sparsity():
    fig, ax = plt.subplots(figsize=(5.5, 4))

    K = np.array([2, 5, 8, 10, 15])
    lms   = np.array([-13.36, -14.40, -14.97, -14.78, -14.95])
    nlms  = np.array([-14.13, -16.35, -16.85, -16.63, -16.90])
    omp   = np.array([-33.78, -35.85, -35.93, -34.91, -32.89])
    lasso = np.array([-23.05, -28.66, -29.75, -29.97, -29.84])
    lista = np.array([-20.88, -24.89, -23.39, -22.25, -16.23])

    ax.plot(K, omp,   '-s', color=C_OMP,   label='OMP',   markersize=5, linewidth=1.5)
    ax.plot(K, lasso, '-D', color=C_LASSO,  label='LASSO', markersize=4, linewidth=1.2)
    ax.plot(K, nlms,  '--', color=C_NLMS,   label='NLMS',  linewidth=1.0, alpha=0.7)
    ax.plot(K, lms,   ':',  color=C_LMS,    label='LMS',   linewidth=1.0, alpha=0.7)
    ax.plot(K, lista, '-o', color=C_LISTA,  label='LISTA', markersize=6, linewidth=2.2)

    ax.set_xlabel('Sparsity $K$')
    ax.set_ylabel('NMSE (dB)')
    ax.set_xticks(K)
    ax.legend(fontsize=7.5, loc='lower left')
    ax.grid(alpha=0.25)

    ax.annotate('Divergence\n(1/5 seeds)',
                xy=(15, -16.23), xytext=(13.2, -8),
                fontsize=7, ha='center', color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1))

    save_pub(fig, 'fig_nmse_vs_sparsity')


# ============================================================
# Figure 4: NMSE vs Channel Length (fixed: complete LISTA line, legend position)
# ============================================================
def fig_nmse_vs_channellen():
    fig, ax = plt.subplots(figsize=(5.5, 4))

    N = np.array([32, 64, 128, 256])
    lms   = np.array([-17.24, -14.58, -7.02, -2.90])
    nlms  = np.array([-18.00, -16.57, -7.79, -3.24])
    omp   = np.array([-32.91, -37.53, -33.56, -12.99])
    lasso = np.array([-24.33, -29.04, -26.36, -10.16])
    lista = np.array([-30.27, -32.29, -25.54, 26.84])  # N=256 diverged

    ax.plot(N, omp,   '-s', color=C_OMP,   label='OMP',   markersize=5, linewidth=1.5)
    ax.plot(N, lasso, '-D', color=C_LASSO,  label='LASSO', markersize=4, linewidth=1.2)
    ax.plot(N, nlms,  '--', color=C_NLMS,   label='NLMS',  linewidth=1.0, alpha=0.7)
    ax.plot(N, lms,   ':',  color=C_LMS,    label='LMS',   linewidth=1.0, alpha=0.7)

    # LISTA: solid line for valid points, X marker for diverged point
    ax.plot(N[:3], lista[:3], '-o', color=C_LISTA, label='LISTA',
            markersize=6, linewidth=2.2, zorder=5)
    ax.plot(256, 26.84, 'x', color=C_LISTA, markersize=10, markeredgewidth=2.5, zorder=5)
    # Dashed extension to show discontinuity
    ax.plot([128, 256], [-25.54, 26.84], '--', color=C_LISTA, alpha=0.3, linewidth=1)

    ax.set_xlabel('Channel length $N$')
    ax.set_ylabel('NMSE (dB)')
    ax.set_xticks(N)
    # Legend in upper-left to avoid blocking LISTA line
    ax.legend(fontsize=7.5, loc='upper left')
    ax.grid(alpha=0.25)

    ax.annotate('Diverged\n($M/N=1$)',
                xy=(256, 26.84), xytext=(220, 18),
                fontsize=7, ha='center', color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1))

    save_pub(fig, 'fig_nmse_vs_channellen')


# ============================================================
# Figure 5: Convergence / Depth
# ============================================================
def fig_convergence():
    fig, ax = plt.subplots(figsize=(5.5, 4))

    layers = np.array([1, 2, 3, 5, 8, 10, 15, 20])
    nmse_mean = np.array([-4.84, -8.91, -12.92, -20.17, -24.29, -25.01, -24.48, -25.04])
    nmse_std  = np.array([0.04, 0.07, 0.15, 0.25, 0.60, 0.53, 0.77, 0.67])

    ax.fill_between(layers, nmse_mean - nmse_std, nmse_mean + nmse_std,
                    alpha=0.15, color=C_LISTA)
    ax.plot(layers, nmse_mean, '-o', color=C_LISTA, markersize=6, linewidth=2.2, label='LISTA')

    omp_baseline = -37.53
    ax.axhline(y=omp_baseline, color=C_OMP, linestyle='--', linewidth=1.2, alpha=0.8)
    ax.text(1.5, omp_baseline + 1.0, f'OMP: {omp_baseline:.1f} dB',
            fontsize=7.5, color=C_OMP, fontweight='bold')

    ax.annotate('Saturation\n($L \\geq 10$)',
                xy=(10, -25.01), xytext=(14, -17),
                fontsize=7.5, ha='center', color=C_LISTA,
                arrowprops=dict(arrowstyle='->', color=C_LISTA, lw=1),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0FE',
                          edgecolor=C_LISTA, alpha=0.85))

    ax.set_xlabel('Number of layers $L$')
    ax.set_ylabel('NMSE (dB)')
    ax.set_xticks(layers)
    ax.legend(fontsize=8, loc='lower left')
    ax.grid(alpha=0.25)
    ax.set_ylim([-42, -2])

    save_pub(fig, 'fig_convergence')


# ============================================================
# Figure 6: BER–NMSE Disconnect
# ============================================================
def fig_ber_nmse_disconnect():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4))

    snr = np.array([-5, 0, 5, 10, 15, 20, 25, 30, 40])
    omp   = np.array([-6.43, -13.23, -19.10, -25.65, -30.62, -37.09, -42.21, -48.51, -58.04])
    fista = np.array([-4.52, -11.87, -17.24, -23.91, -28.14, -33.85, -38.67, -43.12, -52.45])
    lista = np.array([-3.83, -11.01, -15.98, -22.80, -24.36, -24.25, -25.08, -25.02, -25.02])

    ax1.plot(snr, omp,   '-s', color=C_OMP,   label='OMP',   markersize=5, linewidth=1.5)
    ax1.plot(snr, fista, '-^', color=C_FISTA,  label='FISTA', markersize=5, linewidth=1.5)
    ax1.plot(snr, lista, '-o', color=C_LISTA,  label='LISTA', markersize=6, linewidth=2.2)

    ax1.set_xlabel('SNR (dB)')
    ax1.set_ylabel('NMSE (dB)')
    ax1.set_title('(a) NMSE vs SNR', fontsize=10, fontweight='bold', pad=8)
    ax1.legend(fontsize=7.5)
    ax1.grid(alpha=0.25)

    # Gap annotation with offset text
    ax1.annotate('', xy=(20, -24.25), xytext=(20, -37.09),
                arrowprops=dict(arrowstyle='<->', color='#666', lw=1))
    ax1.text(22, -30.5, '12.8 dB', fontsize=7.5, ha='left', va='center', color='#666',
             bbox=dict(facecolor='white', edgecolor='none', pad=1))

    snr_ber = np.array([0, 5, 10, 15, 20, 25, 30])
    lista_ber = np.array([0.425, 0.380, 0.343, 0.318, 0.305, 0.297, 0.292])
    omp_ber   = np.array([0.426, 0.383, 0.346, 0.325, 0.316, 0.314, 0.313])

    ax2.plot(snr_ber, omp_ber,   '-s', color=C_OMP,   label='OMP',   markersize=5, linewidth=1.5)
    ax2.plot(snr_ber, lista_ber, '-o', color=C_LISTA,  label='LISTA', markersize=6, linewidth=2.2)

    ax2.fill_between(snr_ber, omp_ber, lista_ber,
                     where=(lista_ber < omp_ber), alpha=0.12, color=C_GREEN)

    for s, p in [(15, '*'), (20, '**'), (25, '**'), (30, '**')]:
        idx = np.where(snr_ber == s)[0][0]
        ax2.text(s, lista_ber[idx] - 0.006, p, ha='center', fontsize=9,
                fontweight='bold', color=C_OMP)

    ax2.set_xlabel('SNR (dB)')
    ax2.set_ylabel('16-QAM BER')
    ax2.set_title('(b) BER under ZF equalization', fontsize=10, fontweight='bold', pad=8)
    ax2.legend(fontsize=7.5)
    ax2.grid(alpha=0.25)

    plt.tight_layout()
    save_pub(fig, 'fig_ber_nmse_disconnect')


# ============================================================
# Figure 7: Threshold Comparison (fixed: text above arrow, not on it)
# ============================================================
def fig_threshold_comparison():
    fig, ax = plt.subplots(figsize=(4, 4.2))

    methods = ['Soft\n(LISTA)', 'Hard', 'Semi-soft\n(garrote)']
    nmse = [-24.59, -31.72, -27.85]
    std = [0.18, 0.11, 0.08]
    colors = [C_LISTA, C_OMP, C_ORANGE]

    bars = ax.bar(methods, nmse, yerr=std, capsize=4, color=colors,
                  alpha=0.9, edgecolor='#333', linewidth=0.6, width=0.55)

    # Value labels above bars
    for bar, m in zip(bars, nmse):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{m:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Bracket arrow BELOW the bars (in the gap area)
    # Draw bracket between Soft and Hard
    y_top = -24.59
    y_bot = -31.72
    y_mid = (y_top + y_bot) / 2

    # Bracket lines
    x0, x1_br = 0, 1
    bracket_y = -33.0  # Below all bars
    ax.annotate('', xy=(x0, bracket_y), xytext=(x1_br, bracket_y),
                arrowprops=dict(arrowstyle='<->', color='#444', lw=1.5))
    # Vertical ticks
    ax.plot([x0, x0], [bracket_y, -32.2], color='#444', lw=1.0)
    ax.plot([x1_br, x1_br], [bracket_y, -32.2], color='#444', lw=1.0)

    # Text BELOW the bracket
    ax.text(0.5, -34.0, '7.1 dB\n$p < 0.001$', ha='center', va='top',
            fontsize=8, color='#333', fontweight='bold')

    ax.set_ylabel('NMSE (dB)')
    ax.set_ylim([-36, -22])
    ax.grid(axis='y', alpha=0.25)

    save_pub(fig, 'fig_threshold_comparison')


# ============================================================
# Figure 8: Error Concentration
# ============================================================
def fig_error_concentration():
    fig, ax = plt.subplots(figsize=(5, 4))

    methods = ['LISTA', 'OMP', 'ISTA', 'LISTA\n(pre-thresh)']
    means = [100.0, 95.2, 92.4, 68.3]
    stds = [0.0, 0.6, 0.4, 2.1]
    colors = [C_LISTA, C_OMP, C_ISTA, '#7BAFD4']

    bars = ax.bar(methods, means, yerr=stds, capsize=4, color=colors,
                  alpha=0.9, edgecolor='#333', linewidth=0.6, width=0.6)

    for bar, m, s in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.0,
                f'{m:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_ylabel('Error on true taps (%)')
    ax.set_ylim([50, 108])
    ax.axhline(y=100, color='gray', linestyle='--', linewidth=0.6, alpha=0.5)
    ax.grid(axis='y', alpha=0.25)

    ax.annotate('92.4% → 100.0%\n(learned enhancement)',
                xy=(0, 100), xytext=(1.5, 76),
                fontsize=8, ha='center',
                arrowprops=dict(arrowstyle='->', color=C_LISTA, lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0FE',
                          edgecolor=C_LISTA, alpha=0.85))

    save_pub(fig, 'fig_error_concentration')


# ============================================================
# Figure 9: Learned Threshold Schedule
# ============================================================
def fig_threshold_schedule():
    fig, ax = plt.subplots(figsize=(5.5, 4))

    layers = np.arange(1, 21)
    theta_mean = np.array([0.0234, 0.0221, 0.0209, 0.0198, 0.0187,
                           0.0177, 0.0168, 0.0159, 0.0152, 0.0145,
                           0.0139, 0.0133, 0.0128, 0.0124, 0.0120,
                           0.0117, 0.0115, 0.0113, 0.0112, 0.0110])
    theta_std = np.array([0.0018, 0.0017, 0.0016, 0.0015, 0.0015,
                          0.0014, 0.0013, 0.0013, 0.0012, 0.0012,
                          0.0011, 0.0011, 0.0010, 0.0010, 0.0010,
                          0.0009, 0.0009, 0.0009, 0.0009, 0.0009])

    ax.plot(layers, theta_mean * 1000, '-o', color=C_LISTA, markersize=4, linewidth=2,
            label=r'Learned $\theta^{(k)}$')
    ax.fill_between(layers,
                    (theta_mean - theta_std) * 1000,
                    (theta_mean + theta_std) * 1000,
                    alpha=0.15, color=C_LISTA)

    ax2 = ax.twinx()
    mu_mean = np.array([0.482, 0.474, 0.466, 0.458, 0.456,
                        0.448, 0.440, 0.434, 0.431, 0.424,
                        0.418, 0.413, 0.408, 0.404, 0.400,
                        0.397, 0.395, 0.393, 0.392, 0.390])
    ax2.plot(layers, mu_mean, '--s', color=C_ORANGE, markersize=3, linewidth=1.5,
             label=r'Learned $\mu^{(k)}$')
    ax2.set_ylabel(r'Step size $\mu^{(k)}$', color=C_ORANGE)
    ax2.tick_params(axis='y', labelcolor=C_ORANGE)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(C_ORANGE)

    ax.set_xlabel('Layer $k$')
    ax.set_ylabel(r'Threshold $\theta^{(k)}$ ($\times 10^{-3}$)')
    ax.set_xticks(layers[::2])
    ax.grid(alpha=0.25)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper right')

    ax.annotate('Decreasing:\naggressive → gentle',
                xy=(15, theta_mean[14]*1000), xytext=(10, 22),
                fontsize=7.5, ha='center',
                arrowprops=dict(arrowstyle='->', color='#666', lw=1),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFDE7',
                          edgecolor='#999', alpha=0.85))

    save_pub(fig, 'fig_threshold_schedule')


# ============================================================
# Figure 10: Summary (v2 - fixed text overflow and alignment)
# ============================================================
def fig_summary():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.8)
    ax.axis('off')

    def cbox(x, y, w, h, fc, ec):
        rect = mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.1",
            facecolor=fc, edgecolor=ec, linewidth=1.2)
        ax.add_patch(rect)

    # ---- Row 1 left: NMSE ----
    cbox(0.2, 3.8, 4.5, 1.7, '#FFF3E0', C_ORANGE)
    ax.text(2.45, 5.2, 'NMSE Performance', ha='center', fontsize=10,
            fontweight='bold', color=C_ORANGE)
    ax.text(2.45, 4.8, 'LISTA: $-25$ dB (saturates)', ha='center', fontsize=9, color=C_OMP)
    ax.text(2.45, 4.45, 'OMP: $-37$ dB  |  FISTA: $-34$ dB', ha='center',
            fontsize=8.5, color='#555')
    ax.text(2.45, 4.05, r'$\Rightarrow$ LISTA trails by 12–27 dB',
            ha='center', fontsize=9, fontweight='bold', color=C_OMP)

    # ---- Row 1 right: BER ----
    cbox(5.3, 3.8, 4.5, 1.7, '#E8F5E9', C_GREEN)
    ax.text(7.55, 5.2, 'BER Performance (ZF, 16-QAM)', ha='center', fontsize=10,
            fontweight='bold', color=C_GREEN)
    ax.text(7.55, 4.8, 'LISTA matches or beats OMP', ha='center', fontsize=9, color=C_GREEN)
    ax.text(7.55, 4.45, 'at SNR $\\geq 15$ dB ($p < 0.05$)', ha='center',
            fontsize=8.5, color='#555')
    ax.text(7.55, 4.05, r'$\Rightarrow$ BER advantage despite worse NMSE',
            ha='center', fontsize=9, fontweight='bold', color=C_GREEN)

    # Arrow between top boxes
    arrow(ax, 4.75, 4.65, 5.25, 4.65, color='#999', lw=1.5)

    # ---- Row 2: Mechanism ----
    cbox(0.2, 1.8, 9.6, 1.7, '#E3F2FD', C_LISTA)
    ax.text(5, 3.2, 'Mechanism: Error Concentration', ha='center',
            fontsize=11, fontweight='bold', color=C_LISTA)
    ax.text(5, 2.75, 'LISTA concentrates 100.0% of estimation error on true tap locations',
            ha='center', fontsize=9, color='#333')
    ax.text(5, 2.35, '(vs. 95.2% OMP, 92.4% ISTA) → $267\\times$ less non-support error',
            ha='center', fontsize=8.5, color='#555')
    ax.text(5, 1.98, 'Learned threshold schedule dominates ($+14$–$18$ dB); '
            'hard thresholding outperforms soft by 7.1 dB',
            ha='center', fontsize=8, color='#777')

    # ---- Row 3: Recommendation (two lines to fit) ----
    cbox(0.8, 0.2, 8.4, 1.2, '#F3E5F5', C_FISTA)
    ax.text(5, 0.95, 'Recommendation', ha='center', va='center',
            fontsize=9, fontweight='bold', color=C_FISTA)
    ax.text(5, 0.55, 'LISTA: throughput-critical ZF  |  OMP/FISTA: NMSE-critical',
            ha='center', va='center', fontsize=8.5, color='#555')

    save_pub(fig, 'fig_summary')


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("Generating all 10 figures (v2)...")
    fig_architecture()
    fig_nmse_vs_snr()
    fig_nmse_vs_sparsity()
    fig_nmse_vs_channellen()
    fig_convergence()
    fig_ber_nmse_disconnect()
    fig_threshold_comparison()
    fig_error_concentration()
    fig_threshold_schedule()
    fig_summary()
    print("Done!")
