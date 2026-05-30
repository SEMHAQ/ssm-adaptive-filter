"""
Generate publication-quality PDF figures and LaTeX tables for DSP journal paper.
LISTA sparse channel estimation experiments.

Figures:
  - fig_nmse_vs_snr.pdf
  - fig_nmse_vs_sparsity.pdf
  - fig_nmse_vs_channellen.pdf
  - fig_convergence.pdf

LaTeX tables are printed to stdout.
"""

import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results" / "sparse_channel"
FIGURES_DIR = RESULTS_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Publication style
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.size": 12,
    "font.family": "serif",
    "text.usetex": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "legend.framealpha": 0.9,
    "legend.edgecolor": "0.8",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "pdf.fonttype": 42,       # TrueType fonts for LaTeX embedding
    "ps.fonttype": 42,
})

# ---------------------------------------------------------------------------
# Method styles
# ---------------------------------------------------------------------------
METHOD_STYLES = {
    "LMS":   {"color": "#2196F3", "marker": "o", "lw": 2.0, "label": "LMS"},
    "NLMS":  {"color": "#4CAF50", "marker": "s", "lw": 2.0, "label": "NLMS"},
    "OMP":   {"color": "#FF9800", "marker": "^", "lw": 2.0, "label": "OMP"},
    "LASSO": {"color": "#9C27B0", "marker": "D", "lw": 2.0, "label": "LASSO"},
    "LISTA": {"color": "#F44336", "marker": "v", "lw": 2.5, "label": "LISTA"},
}

METHODS = ["LMS", "NLMS", "OMP", "LASSO", "LISTA"]

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
def load_json(name: str) -> dict:
    with open(RESULTS_DIR / name, "r") as f:
        return json.load(f)

data_snr = load_json("exp_snr.json")
data_sparsity = load_json("exp_sparsity.json")
data_chlen = load_json("exp_channel_length.json")
data_conv = load_json("exp_convergence.json")

# ---------------------------------------------------------------------------
# Helper: extract sorted (x, y) from a results dict
# ---------------------------------------------------------------------------
def extract_xy(results: dict, method: str):
    keys_sorted = sorted(results.keys(), key=lambda k: int(k))
    x = [int(k) for k in keys_sorted]
    y = [results[k][method] for k in keys_sorted]
    return np.array(x), np.array(y)


def plot_nmse_vs_x(data: dict, x_label: str, title_suffix: str, filename: str,
                   legend_loc: str = "best", y_pad: float = 0.0):
    """Generic NMSE-vs-something plot for all 5 methods."""
    fig, ax = plt.subplots(figsize=(8, 5))

    for method in METHODS:
        x, y = extract_xy(data["results"], method)
        s = METHOD_STYLES[method]
        ax.plot(
            x, y,
            color=s["color"],
            marker=s["marker"],
            linewidth=s["lw"],
            markersize=7,
            markerfacecolor=s["color"],
            markeredgecolor="white",
            markeredgewidth=0.6,
            label=s["label"],
        )

    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel("NMSE (dB)", fontsize=13)
    ax.grid(True, alpha=0.3, linestyle="--")
    if y_pad > 0:
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(ymin, ymax + y_pad)
    ax.legend(loc=legend_loc, fontsize=11)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / filename, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {filename}")


# ---------------------------------------------------------------------------
# Figure 1: NMSE vs SNR
# ---------------------------------------------------------------------------
plot_nmse_vs_x(
    data_snr,
    x_label="SNR (dB)",
    title_suffix="SNR",
    filename="fig_nmse_vs_snr.pdf",
)

# ---------------------------------------------------------------------------
# Figure 2: NMSE vs Sparsity K
# ---------------------------------------------------------------------------
plot_nmse_vs_x(
    data_sparsity,
    x_label="Sparsity K",
    title_suffix="Sparsity",
    filename="fig_nmse_vs_sparsity.pdf",
    legend_loc="upper right",
    y_pad=0.5,
)

# ---------------------------------------------------------------------------
# Figure 3: NMSE vs Channel Length N
# ---------------------------------------------------------------------------
plot_nmse_vs_x(
    data_chlen,
    x_label="Channel Length N",
    title_suffix="Channel Length",
    filename="fig_nmse_vs_channellen.pdf",
)

# ---------------------------------------------------------------------------
# Figure 4: LISTA Convergence
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

layers = np.array(data_conv["layers"])
lista_nmse = np.array(data_conv["lista_nmse"])
omp_nmse = data_conv["omp_nmse"]

ax.plot(
    layers, lista_nmse,
    color=METHOD_STYLES["LISTA"]["color"],
    marker=METHOD_STYLES["LISTA"]["marker"],
    linewidth=METHOD_STYLES["LISTA"]["lw"],
    markersize=7,
    markerfacecolor=METHOD_STYLES["LISTA"]["color"],
    markeredgecolor="white",
    markeredgewidth=0.6,
    label="LISTA",
    linestyle="-",
)
ax.axhline(
    y=omp_nmse,
    color=METHOD_STYLES["OMP"]["color"],
    linestyle="--",
    linewidth=1.8,
    label=f"OMP ({omp_nmse:.2f} dB)",
)

ax.set_xlabel("Number of Layers", fontsize=13)
ax.set_ylabel("NMSE (dB)", fontsize=13)
ax.grid(True, alpha=0.3, linestyle="--")
ax.legend(loc="best", fontsize=11)

fig.tight_layout()
fig.savefig(FIGURES_DIR / "fig_convergence.pdf", bbox_inches="tight")
plt.close(fig)
print("  Saved fig_convergence.pdf")

# ---------------------------------------------------------------------------
# LaTeX Tables
# ---------------------------------------------------------------------------

def make_latex_table(data: dict, x_label: str, table_caption: str, table_label: str) -> str:
    """Generate a booktabs-style LaTeX table from a results dict."""
    keys_sorted = sorted(data["results"].keys(), key=lambda k: int(k))
    x_vals = [int(k) for k in keys_sorted]

    # Find best (lowest) NMSE per row
    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"  \centering")
    lines.append(r"  \caption{" + table_caption + r"}")
    lines.append(r"  \label{" + table_label + r"}")

    ncols = len(METHODS) + 1  # x column + methods
    col_spec = "l" + "c" * len(METHODS)
    lines.append(r"  \begin{tabular}{" + col_spec + "}")
    lines.append(r"    \toprule")

    # Header
    header_cells = [x_label] + METHODS
    lines.append("    " + " & ".join(header_cells) + r" \\")
    lines.append(r"    \midrule")

    # Data rows
    for key in keys_sorted:
        x = int(key)
        vals = {m: data["results"][key][m] for m in METHODS}
        best_method = min(vals, key=vals.get)
        cells = [str(x)]
        for m in METHODS:
            v = f"{vals[m]:.2f}"
            if m == best_method:
                v = r"\textbf{" + v + "}"
            cells.append(v)
        lines.append("    " + " & ".join(cells) + r" \\")

    lines.append(r"    \bottomrule")
    lines.append(r"  \end{tabular}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


def make_convergence_table(data: dict) -> str:
    """LaTeX table for LISTA convergence."""
    layers = data["layers"]
    lista_nmse = data["lista_nmse"]
    omp_nmse = data["omp_nmse"]

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"  \centering")
    lines.append(r"  \caption{LISTA Convergence: NMSE vs. Number of Layers}")
    lines.append(r"  \label{tab:convergence}")

    lines.append(r"  \begin{tabular}{lcc}")
    lines.append(r"    \toprule")
    lines.append(r"    Layers & LISTA NMSE (dB) & OMP NMSE (dB) \\")
    lines.append(r"    \midrule")

    # Bold the best LISTA row
    best_idx = int(np.argmin(lista_nmse))
    for i, (l, v) in enumerate(zip(layers, lista_nmse)):
        lista_str = f"{v:.2f}"
        if i == best_idx:
            lista_str = r"\textbf{" + lista_str + "}"
        lines.append(f"    {l} & {lista_str} & {omp_nmse:.2f} \\")

    lines.append(r"    \bottomrule")
    lines.append(r"  \end{tabular}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


# Print LaTeX tables to stdout
print("\n" + "=" * 70)
print("LATEX TABLES (copy-paste into paper)")
print("=" * 70 + "\n")

print("% Table 1: NMSE vs SNR")
print(make_latex_table(
    data_snr,
    x_label="SNR (dB)",
    table_caption="NMSE (dB) vs. SNR for different methods ($N=64$, $K=5$)",
    table_label="tab:snr",
))

print("\n% Table 2: NMSE vs Sparsity")
print(make_latex_table(
    data_sparsity,
    x_label="$K$",
    table_caption="NMSE (dB) vs. Sparsity $K$ for different methods ($N=64$, SNR=20 dB)",
    table_label="tab:sparsity",
))

print("\n% Table 3: NMSE vs Channel Length")
print(make_latex_table(
    data_chlen,
    x_label="$N$",
    table_caption="NMSE (dB) vs. Channel Length $N$ for different methods ($K/N=8\\%$, SNR=20 dB)",
    table_label="tab:channellen",
))

print("\n% Table 4: LISTA Convergence")
print(make_convergence_table(data_conv))

print("\n" + "=" * 70)
print(f"Figures saved to: {FIGURES_DIR}")
print("=" * 70)
