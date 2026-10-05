import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rounded_rect(ax, center_x, center_y, width, height, text, fontsize=10, bold=False):
    x = center_x - width / 2.0
    y = center_y - height / 2.0
    box = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.08",
        facecolor="white",
        edgecolor="black",
        linewidth=1.6
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(center_x, center_y, text, ha="center", va="center",
            fontsize=fontsize, color="black", weight=weight, linespacing=1.25)

def draw_diamond(ax, center_x, center_y, width, height, text, fontsize=9.5, bold=False):
    # Diamond coordinates: top, right, bottom, left
    pts = [
        [center_x, center_y + height / 2.0],
        [center_x + width / 2.0, center_y],
        [center_x, center_y - height / 2.0],
        [center_x - width / 2.0, center_y]
    ]
    diamond = patches.Polygon(pts, closed=True, facecolor="white", edgecolor="black", linewidth=1.6)
    ax.add_patch(diamond)
    weight = "bold" if bold else "normal"
    ax.text(center_x, center_y, text, ha="center", va="center",
            fontsize=fontsize, color="black", weight=weight, linespacing=1.2)

def draw_arrow(ax, start_x, start_y, end_x, end_y, label=None, label_pos="right"):
    ax.annotate(
        "", xy=(end_x, end_y), xytext=(start_x, start_y),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5, mutation_scale=14)
    )
    if label:
        mid_x = (start_x + end_x) / 2.0
        mid_y = (start_y + end_y) / 2.0
        if label_pos == "right":
            ax.text(mid_x + 0.15, mid_y, label, ha="left", va="center", fontsize=9.5, fontweight="bold", color="black")
        elif label_pos == "top":
            ax.text(mid_x, mid_y + 0.15, label, ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="black")
        elif label_pos == "left":
            ax.text(mid_x - 0.15, mid_y, label, ha="right", va="center", fontsize=9.5, fontweight="bold", color="black")

def generate_black_white_workflow(output_path="figure_workflow_bw.png"):
    fig, ax = plt.subplots(figsize=(10, 14.5), dpi=600)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    ax.axis("off")

    # Font setup
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10
    })

    CX = 4.2   # Main vertical center axis
    RX = 8.1   # Right branch center axis
    LX = 1.3   # Left loopback axis

    # -------------------------------------------------------------
    # 1. Step 1: Quantum Microstate Initialization
    # -------------------------------------------------------------
    y1 = 14.2
    draw_rounded_rect(ax, CX, y1, 4.4, 0.75, "Initialize N-Spin Quantum Lattice & Hamiltonian\n$H = -J\\sum Z_i Z_{i+1} - h_x\\sum X_i - h_z\\sum Z_i$", fontsize=9.5)

    y2 = 13.0
    draw_arrow(ax, CX, y1 - 0.375, CX, y2 + 0.375)
    draw_rounded_rect(ax, CX, y2, 4.4, 0.75, "Construct Liouvillian Super-Operator\n$\\mathcal{L}(O) = [H, O] + i\\mathcal{D}_{Lindblad}(O)$", fontsize=9.5)

    # -------------------------------------------------------------
    # 2. Step 2: Krylov Space & Lanczos Tridiagonalization
    # -------------------------------------------------------------
    y3 = 11.8
    draw_arrow(ax, CX, y2 - 0.375, CX, y3 + 0.375)
    draw_rounded_rect(ax, CX, y3, 4.4, 0.75, "Execute Lanczos Algorithm with Full Re-orthogonalization\nCompute Hopping Elements $b_n$ and Amplitudes $\\phi_n(t)$", fontsize=9.2)

    # Decision 1: Chaos & Operator Growth
    y_d1 = 10.45
    draw_arrow(ax, CX, y3 - 0.375, CX, y_d1 + 0.6)
    draw_diamond(ax, CX, y_d1, 3.8, 1.2, "Does system exhibit\nUniversal Operator Growth?\n($b_n \\sim n$ and $dK/dt > 0$)", fontsize=9.0)

    # Branch Right: Reject / Re-tune
    draw_arrow(ax, CX + 1.9, y_d1, RX - 1.4, y_d1, label="No", label_pos="top")
    draw_rounded_rect(ax, RX, y_d1, 2.8, 0.85, "Re-tune Hamiltonian parameters\n$h_z$ or dissipation coupling $\\gamma$\n(System remains integrable)", fontsize=8.5)

    # -------------------------------------------------------------
    # 3. Step 3: Extract Arrow of Time & Causal Sets
    # -------------------------------------------------------------
    y4 = 9.1
    draw_arrow(ax, CX, y_d1 - 0.6, CX, y4 + 0.375, label="Yes", label_pos="right")
    draw_rounded_rect(ax, CX, y4, 4.4, 0.75, "Extract Emergent Arrow of Time Vector\n$\\vec{v}_{\\text{arrow}}(t) = \\frac{d K(t)}{dt}$ (Irreversible Asymmetry)", fontsize=9.5)

    y5 = 7.9
    draw_arrow(ax, CX, y4 - 0.375, CX, y5 + 0.375)
    draw_rounded_rect(ax, CX, y5, 4.4, 0.75, "Poisson Sprinkling of 800 Spacetime Events $(x_i, t_i)$\nGenerate Lightcone Causal Order $(\\Delta t > 0, \\Delta s^2 > 0)$", fontsize=9.2)

    y6 = 6.7
    draw_arrow(ax, CX, y5 - 0.375, CX, y6 + 0.375)
    draw_rounded_rect(ax, CX, y6, 4.4, 0.75, "Synthesize Directed Causal Set Graph (DAG)\nModulate Edge Weights $W_{ij}$ using $\\vec{v}_{\\text{arrow}}$", fontsize=9.2)

    # -------------------------------------------------------------
    # 4. Step 4: Hybrid GNN-PINN Architecture & Field Loss
    # -------------------------------------------------------------
    y7 = 5.5
    draw_arrow(ax, CX, y6 - 0.375, CX, y7 + 0.375)
    draw_rounded_rect(ax, CX, y7, 4.4, 0.75, "Forward Pass: Directed Causal Message Passing\nProject Graph State to Continuous Field $\\phi(x, t)$", fontsize=9.2)

    y8 = 4.3
    draw_arrow(ax, CX, y7 - 0.375, CX, y8 + 0.375)
    draw_rounded_rect(ax, CX, y8, 4.4, 0.75, "Autograd Optimization of Klein-Gordon Residual:\n$\\mathcal{R}_{\\text{PDE}} = \\frac{\\partial^2 \\phi}{\\partial t^2} - \\frac{\\partial^2 \\phi}{\\partial x^2} + m^2 \\phi$", fontsize=9.2)

    # Decision 2: Convergence
    y_d2 = 2.9
    draw_arrow(ax, CX, y8 - 0.375, CX, y_d2 + 0.6)
    draw_diamond(ax, CX, y_d2, 3.8, 1.2, "Has Spacetime Equilibrium\nconverged?\n($\\mathcal{L}_{\\text{total}} \\to 0$, Residual $< 10^{-3}$)", fontsize=9.0)

    # Branch Left: Loop back for Optimization
    draw_arrow(ax, CX - 1.9, y_d2, LX + 1.2, y_d2, label="No", label_pos="top")
    draw_rounded_rect(ax, LX, y_d2, 2.4, 0.85, "Backpropagate Gradients\nAdam / Cosine Annealing\nUpdate GNN-PINN weights", fontsize=8.5)
    
    # Loop back arrow from LX up to y7 (Message Passing)
    ax.plot([LX, LX], [y_d2 + 0.425, y7], color="black", lw=1.5)
    draw_arrow(ax, LX, y7, CX - 2.2, y7)

    # Branch Right: Divergence / Failure
    draw_arrow(ax, CX + 1.9, y_d2, RX - 1.4, y_d2, label="Diverged", label_pos="top")
    draw_rounded_rect(ax, RX, y_d2, 2.8, 0.85, "Gradient Explodes / OOM\nAdjust Collocation Sampling\nor Learning Rate", fontsize=8.5)

    # -------------------------------------------------------------
    # 5. Final Terminal Step: Acceptance / Physical Equilibrium
    # -------------------------------------------------------------
    y9 = 1.3
    draw_arrow(ax, CX, y_d2 - 0.6, CX, y9 + 0.45, label="Yes", label_pos="right")
    
    # Terminal double-bordered box
    x_end = CX - 2.4
    y_end = y9 - 0.45
    w_end = 4.8
    h_end = 0.9
    box_outer = patches.FancyBboxPatch((x_end - 0.05, y_end - 0.05), w_end + 0.1, h_end + 0.1,
                                       boxstyle="round,pad=0.08", facecolor="none", edgecolor="black", linewidth=2.0)
    box_inner = patches.FancyBboxPatch((x_end, y_end), w_end, h_end,
                                       boxstyle="round,pad=0.08", facecolor="white", edgecolor="black", linewidth=1.2)
    ax.add_patch(box_outer)
    ax.add_patch(box_inner)
    ax.text(CX, y9, "Physical Equilibrium Reached: Emergent Spacetime Validated\nSave Model Weights (`hk_pcg_best.pt`) & Generate 600 DPI Suite",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="black", linespacing=1.25)

    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Black-and-white workflow diagram saved to: {output_path}")

if __name__ == "__main__":
    generate_black_white_workflow()
