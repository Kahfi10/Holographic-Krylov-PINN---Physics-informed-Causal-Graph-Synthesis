import os
import json
import numpy as np
import matplotlib.pyplot as plt

def generate_krylov_figures(json_path="checkpoints/krylov_metrics.json", output_path="figure_krylov_dynamics.png"):
    if not os.path.exists(json_path):
        print(f"[ERROR] Metrics file {json_path} not found. Run run_fase3_krylov.py first.")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    meta = data["metadata"]
    time_grid = np.array(meta["time_grid"])
    regimes = data["regimes"]

    # Academic publication styling (Scopus Q1 standard)
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.dpi": 600
    })

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    colors = {
        "Integrable (Closed)": "#2ca02c",
        "Quantum Chaotic (Closed)": "#1f77b4",
        "Open Dissipative (Arrow of Time)": "#d62728"
    }
    linestyles = {
        "Integrable (Closed)": ":",
        "Quantum Chaotic (Closed)": "--",
        "Open Dissipative (Arrow of Time)": "-"
    }

    # Panel (a): Lanczos Hopping Coefficients b_n
    ax_a = axes[0]
    for name, r_data in regimes.items():
        b_vals = r_data["b_coeffs"]
        n_vals = np.arange(len(b_vals))
        ax_a.plot(n_vals, b_vals, label=name, color=colors.get(name, "black"),
                  linestyle=linestyles.get(name, "-"), marker="o", markersize=4, linewidth=1.6)
    ax_a.set_xlabel("Krylov Basis Index ($n$)")
    ax_a.set_ylabel("Lanczos Coefficients ($b_n$)")
    ax_a.set_title("(a) Operator Growth Velocity ($b_n$)", fontweight="bold")
    ax_a.grid(True, linestyle="--", alpha=0.4)
    ax_a.legend(loc="upper left", frameon=True, edgecolor="#cccccc")

    # Panel (b): Krylov Complexity K(t)
    ax_b = axes[1]
    for name, r_data in regimes.items():
        K_vals = r_data["complexity"]
        ax_b.plot(time_grid, K_vals, label=name, color=colors.get(name, "black"),
                  linestyle=linestyles.get(name, "-"), linewidth=1.8)
    ax_b.set_xlabel("Evolution Time ($t$)")
    ax_b.set_ylabel("Krylov Complexity $K(t)$")
    ax_b.set_title("(b) Circuit Complexity Spread", fontweight="bold")
    ax_b.grid(True, linestyle="--", alpha=0.4)

    # Panel (c): Emergent Arrow of Time (dK/dt)
    ax_c = axes[2]
    for name, r_data in regimes.items():
        v_vals = r_data["arrow_of_time"]
        ax_c.plot(time_grid, v_vals, label=name, color=colors.get(name, "black"),
                  linestyle=linestyles.get(name, "-"), linewidth=1.8)
    ax_c.axhline(0, color="gray", linestyle="-", linewidth=0.8, alpha=0.7)
    ax_c.set_xlabel("Evolution Time ($t$)")
    ax_c.set_ylabel("Complexity Rate ($dK/dt$)")
    ax_c.set_title("(c) Emergent Arrow of Time Vector", fontweight="bold")
    ax_c.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(output_path, dpi=600)
    plt.close()

    print(f"[SUCCESS] 600 DPI Academic Krylov Dynamics Figure saved to {output_path}")

if __name__ == "__main__":
    generate_krylov_figures()
