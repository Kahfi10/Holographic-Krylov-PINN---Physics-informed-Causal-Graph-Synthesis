import os
import json
import matplotlib.pyplot as plt

def generate_publication_figure(json_path="checkpoints/training_metrics.json", output_path="figure_convergence.png"):
    if not os.path.exists(json_path):
        print(f"[ERROR] Metrics file {json_path} not found. Run train_poc.py first.")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    history = data.get("history", [])
    if not history:
        print("[ERROR] No history entries found in metrics.")
        return

    epochs = [entry["epoch"] for entry in history]
    total_loss = [entry["total_loss"] for entry in history]
    pde_loss = [entry["pde_loss"] for entry in history]
    init_loss = [entry["init_loss"] for entry in history]

    # Academic publication styling (IEEE / Elsevier / Scopus standard)
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 12,
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "figure.dpi": 600
    })

    fig, ax = plt.subplots(figsize=(7, 4.5))

    ax.semilogy(epochs, total_loss, label="Total Objective Loss", color="#1f77b4", linewidth=2.0, linestyle="-")
    ax.semilogy(epochs, pde_loss, label="Schrödinger PDE Residual", color="#d62728", linewidth=1.8, linestyle="--")
    ax.semilogy(epochs, init_loss, label="Initial State Discrepancy", color="#2ca02c", linewidth=1.5, linestyle=":")

    ax.set_xlabel("Training Epochs")
    ax.set_ylabel("Physics Loss Residual (Log Scale)")
    ax.set_title("HK-PCG: Convergence Telemetry in 1+1D Spacetime", pad=12, fontweight="bold")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", frameon=True, edgecolor="#cccccc")

    plt.tight_layout()
    plt.savefig(output_path, dpi=600)
    plt.close()

    print(f"[SUCCESS] 600 DPI Academic Figure saved to {output_path}")

if __name__ == "__main__":
    generate_publication_figure()
