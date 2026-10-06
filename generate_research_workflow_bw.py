import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil

def draw_rounded_rect(ax, center_x, center_y, width, height, text, fontsize=24, bold=True, double_border=False):
    x = center_x - width / 2.0
    y = center_y - height / 2.0
    
    pad = 0.12
    if double_border:
        box_out = patches.FancyBboxPatch(
            (x - pad, y - pad), width + 2 * pad, height + 2 * pad,
            boxstyle="round,pad=0.15", facecolor="none", edgecolor="black", linewidth=3.2
        )
        ax.add_patch(box_out)
    
    box = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.15", facecolor="white", edgecolor="black", linewidth=2.4
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(center_x, center_y, text, ha="center", va="center",
            fontsize=fontsize, color="black", weight=weight, linespacing=1.26)

def draw_diamond(ax, center_x, center_y, width, height, text, fontsize=22, bold=True):
    pts = [
        [center_x, center_y + height / 2.0],
        [center_x + width / 2.0, center_y],
        [center_x, center_y - height / 2.0],
        [center_x - width / 2.0, center_y]
    ]
    diamond = patches.Polygon(pts, closed=True, facecolor="white", edgecolor="black", linewidth=2.5)
    ax.add_patch(diamond)
    weight = "bold" if bold else "normal"
    ax.text(center_x, center_y, text, ha="center", va="center",
            fontsize=fontsize, color="black", weight=weight, linespacing=1.22)

def draw_arrow(ax, start_x, start_y, end_x, end_y, lw=2.2):
    ax.annotate(
        "", xy=(end_x, end_y), xytext=(start_x, start_y),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=lw, mutation_scale=22)
    )

def generate_research_workflow(output_path="figure_research_workflow_bw.png"):
    fig, ax = plt.subplots(figsize=(28, 40), dpi=300)
    ax.set_xlim(0, 28)
    ax.set_ylim(-5.5, 34.5)
    ax.axis("off")

    plt.rcParams.update({
        "font.family": "serif"
    })

    CX = 14.0     # Center vertical axis
    LX = 3.85     # Left loopback optimization axis
    RX = 24.15    # Right rejection / fallback axis

    W_MAIN = 12.8
    H_MAIN = 1.70
    W_DIAM = 11.8
    H_DIAM = 2.85
    W_SIDE = 6.6
    H_SIDE = 1.90

    FS_MAIN = 23.5
    FS_DIAM = 21.5
    FS_SIDE = 21.0
    FS_PAR  = 21.5
    FS_TERM = 25.0

    # -------------------------------------------------------------
    # 1. Problem Formulation & Lattice Hamiltonian
    # -------------------------------------------------------------
    y1 = 32.2
    draw_rounded_rect(ax, CX, y1, W_MAIN, H_MAIN, 
                      "Initialize Quantum Lattice & Hamiltonian\n$H = -J\\sum Z_i Z_{i+1} - h_x\\sum X_i - h_z\\sum Z_i$", 
                      fontsize=FS_MAIN, bold=True)

    # -------------------------------------------------------------
    # 2. Liouvillian Super-Operator
    # -------------------------------------------------------------
    y2 = 29.5
    draw_arrow(ax, CX, y1 - H_MAIN/2.0, CX, y2 + H_MAIN/2.0)
    draw_rounded_rect(ax, CX, y2, W_MAIN, H_MAIN, 
                      "Construct Liouvillian Super-Operator\n$\\mathcal{L}(O) = [H, O] + i\\mathcal{D}_{\\mathrm{Lindblad}}(O)$", 
                      fontsize=FS_MAIN, bold=True)

    # -------------------------------------------------------------
    # 3. Decision Diamond 1: Chaos & Operator Growth
    # -------------------------------------------------------------
    yd1 = 26.2
    draw_arrow(ax, CX, y2 - H_MAIN/2.0, CX, yd1 + H_DIAM/2.0)
    draw_diamond(ax, CX, yd1, W_DIAM, H_DIAM, 
                 "Lanczos Algorithm Evaluation:\nUniversal Operator Growth?\n($b_n \\sim \\alpha n$, Chaotic Regime)", 
                 fontsize=FS_DIAM, bold=True)

    # Rejection 1 (Right): Integrable / No growth
    draw_arrow(ax, CX + W_DIAM/2.0, yd1, RX - W_SIDE/2.0 - 0.15, yd1)
    draw_rounded_rect(ax, RX, yd1, W_SIDE, H_SIDE, 
                      "Integrable Dynamics Detected\n$b_n \\to \\mathrm{const}$ (Non-chaotic)\nRe-tune $h_z$ or dissipation $\\gamma$", 
                      fontsize=FS_SIDE, bold=True)

    # -------------------------------------------------------------
    # 4. Krylov Complexity Evolution
    # -------------------------------------------------------------
    y3 = 23.0
    draw_arrow(ax, CX, yd1 - H_DIAM/2.0, CX, y3 + H_MAIN/2.0)
    draw_rounded_rect(ax, CX, y3, W_MAIN, H_MAIN, 
                      "Evaluate Krylov Complexity Evolution\n$K(t) = \\sum n |\\phi_n(t)|^2, \\quad S_K(t) = -\\sum p_n \\ln p_n$", 
                      fontsize=FS_MAIN, bold=True)

    # -------------------------------------------------------------
    # 5. Poisson Sprinkling on Spacetime Manifold
    # -------------------------------------------------------------
    y4 = 20.3
    draw_arrow(ax, CX, y3 - H_MAIN/2.0, CX, y4 + H_MAIN/2.0)
    draw_rounded_rect(ax, CX, y4, W_MAIN, H_MAIN, 
                      "Sample Discrete Spacetime Manifold $\\mathcal{M}^{1+1}$\nPoisson Sprinkling of $N = 800$ Events $(x_i, t_i)$", 
                      fontsize=FS_MAIN, bold=True)

    # -------------------------------------------------------------
    # 6. Decision Diamond 2: Monotonic Arrow of Time
    # -------------------------------------------------------------
    yd2 = 17.1
    draw_arrow(ax, CX, y4 - H_MAIN/2.0, CX, yd2 + H_DIAM/2.0)
    draw_diamond(ax, CX, yd2, W_DIAM, H_DIAM, 
                 "Dynamical Asymmetry Criterion:\nIs entropy strictly monotonic?\n($dK/dt > 0$, Arrow of Time)", 
                 fontsize=FS_DIAM, bold=True)

    # Rejection 2 (Right): Recurrence detected
    draw_arrow(ax, CX + W_DIAM/2.0, yd2, RX - W_SIDE/2.0 - 0.15, yd2)
    draw_rounded_rect(ax, RX, yd2, W_SIDE, H_SIDE, 
                      "Poincaré Recurrence Detected\nPeriodic revival in Hilbert space\nIncrease $N \\geq 6$ or truncate window", 
                      fontsize=FS_SIDE, bold=True)

    # -------------------------------------------------------------
    # 7. Partition Relativistic Lightcone Constraints
    # -------------------------------------------------------------
    y5 = 14.0
    draw_arrow(ax, CX, yd2 - H_DIAM/2.0, CX, y5 + H_MAIN/2.0)
    draw_rounded_rect(ax, CX, y5, W_MAIN, H_MAIN, 
                      "Partition Relativistic Lightcone Constraints\nand Quantum Dynamical Flow", 
                      fontsize=FS_MAIN, bold=True)

    # -------------------------------------------------------------
    # 8. Dual Parallel Evaluators
    # -------------------------------------------------------------
    y6_a = 11.9
    y6_b = 10.9
    y_split = 12.9
    ax.plot([CX, CX], [y5 - H_MAIN/2.0, y_split], color="black", lw=2.2)
    ax.plot([CX - 3.4, CX + 3.4], [y_split, y_split], color="black", lw=2.2)
    draw_arrow(ax, CX - 3.4, y_split, CX - 3.4, y6_a + 0.65)
    draw_arrow(ax, CX + 3.4, y_split, CX + 3.4, y6_b + 0.65)

    draw_rounded_rect(ax, CX - 3.4, y6_a, 6.0, 1.35, 
                      "Analytic Lightcone Metric\n$C_{ij} \\in \\{0, 1\\}$ ($\\Delta s^2 \\geq 0$)", 
                      fontsize=FS_PAR, bold=True)
    draw_rounded_rect(ax, CX + 3.4, y6_b, 6.0, 1.35, 
                      "Krylov Modulation Vector\n$\\vec{v}_{\\mathrm{arrow}}(t) = \\frac{dK}{dt} \\cdot \\hat{e}_t$", 
                      fontsize=FS_PAR, bold=True)

    # -------------------------------------------------------------
    # 9. Directed Causal Graph Synthesis (DAG)
    # -------------------------------------------------------------
    y7 = 8.3
    y_merge = 9.7
    ax.plot([CX - 3.4, CX - 3.4], [y6_a - 0.65, y_merge], color="black", lw=2.2)
    ax.plot([CX + 3.4, CX + 3.4], [y6_b - 0.65, y_merge], color="black", lw=2.2)
    ax.plot([CX - 3.4, CX + 3.4], [y_merge, y_merge], color="black", lw=2.2)
    draw_arrow(ax, CX, y_merge, CX, y7 + 0.95)

    draw_rounded_rect(ax, CX, y7, 13.0, 1.95, 
                      "Synthesize Directed Causal Set Graph (DAG)\nModulate Edge Adjacency Tensor\n$W_{ij} = C_{ij} \\cdot \\vec{v}_{\\mathrm{arrow}}(t_j - t_i)$", 
                      fontsize=FS_MAIN, bold=True)

    # -------------------------------------------------------------
    # 10. Decision Diamond 3: PINN Field Convergence
    # -------------------------------------------------------------
    yd3 = 5.2
    draw_arrow(ax, CX, y7 - 0.95, CX, yd3 + H_DIAM/2.0)
    draw_diamond(ax, CX, yd3, W_DIAM, H_DIAM, 
                 "Physical Field Convergence:\nDoes GNN-PINN satisfy PDE?\n($\\mathcal{R}_{\\mathrm{PDE}} < 10^{-3}$, Loss $\\to 0$)", 
                 fontsize=FS_DIAM, bold=True)

    # Left Branch: Residual exceeds tolerance
    draw_arrow(ax, CX - W_DIAM/2.0, yd3, LX + W_SIDE/2.0 + 0.15, yd3)
    draw_rounded_rect(ax, LX, yd3, W_SIDE, H_SIDE, 
                      "Residual Exceeds Tolerance\n$\\mathcal{R}_{\\mathrm{PDE}} > 10^{-3}$ (Non-converged)", 
                      fontsize=FS_SIDE, bold=True)

    # Revision / Optimization Loopback Box
    y_rev = 16.4
    draw_rounded_rect(ax, LX, y_rev, W_SIDE, 2.2, 
                      "Backpropagate Gradients\nUpdate GNN Message Passing\n& Cosine Annealing Rate", 
                      fontsize=FS_SIDE, bold=True)
    draw_arrow(ax, LX, yd3 + H_SIDE/2.0, LX, y_rev - 1.1)

    # Loopback line up and entering y4 (Poisson sprinkling)
    y_turn = 21.4
    ax.plot([LX, LX], [y_rev + 1.1, y_turn], color="black", lw=2.2)
    ax.plot([LX, CX], [y_turn, y_turn], color="black", lw=2.2)
    draw_arrow(ax, CX, y_turn, CX, y4 + H_MAIN/2.0)

    # -------------------------------------------------------------
    # 11. Forward Spacetime Projection to Bulk Geometry
    # -------------------------------------------------------------
    y8 = 2.2
    draw_arrow(ax, CX, yd3 - H_DIAM/2.0, CX, y8 + H_MAIN/2.0)
    draw_rounded_rect(ax, CX, y8, W_MAIN, H_MAIN, 
                      "Forward Spacetime Bulk Projection\nExtract Curvature $R_{\\mu\\nu}$ and Metric $g_{\\mu\\nu}$", 
                      fontsize=FS_MAIN, bold=True)

    # -------------------------------------------------------------
    # 12. Decision Diamond 4: Global Holographic Duality
    # -------------------------------------------------------------
    yd4 = -0.7
    draw_arrow(ax, CX, y8 - H_MAIN/2.0, CX, yd4 + H_DIAM/2.0)
    draw_diamond(ax, CX, yd4, W_DIAM, H_DIAM, 
                 "Global Holographic Verification:\nDoes bulk geometry obey AdS/CFT?\n(Area Law & Diff-Invariance)", 
                 fontsize=FS_DIAM, bold=True)

    # Rejection 4 (Right)
    draw_arrow(ax, CX + W_DIAM/2.0, yd4, RX - W_SIDE/2.0 - 0.15, yd4)
    draw_rounded_rect(ax, RX, yd4, W_SIDE, H_SIDE, 
                      "Diffeomorphism Anomaly\nRecalibrate boundary coupling\nor collocation scale $z_0$", 
                      fontsize=FS_SIDE, bold=True)

    # -------------------------------------------------------------
    # 13. Terminal Acceptance: Physical Equilibrium Validated
    # -------------------------------------------------------------
    y9 = -3.7
    w_term = 14.0
    h_term = 2.1
    draw_arrow(ax, CX, yd4 - H_DIAM/2.0, CX, y9 + h_term/2.0 + 0.16)
    draw_rounded_rect(ax, CX, y9, w_term, h_term, 
                      "Physical Equilibrium Reached\nEmergent Spacetime Validated", 
                      fontsize=FS_TERM, bold=True, double_border=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    # Overwrite figure_workflow_bw.png with this updated figure
    shutil.copyfile(output_path, "figure_workflow_bw.png")
    print(f"[SUCCESS] Research workflow saved to: {output_path} and copied to figure_workflow_bw.png")

if __name__ == "__main__":
    generate_research_workflow()
