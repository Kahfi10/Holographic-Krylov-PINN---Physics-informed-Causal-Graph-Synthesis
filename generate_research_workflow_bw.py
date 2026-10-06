import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil

def draw_rounded_rect(ax, center_x, center_y, width, height, text, fontsize=9.2, bold=False, double_border=False):
    x = center_x - width / 2.0
    y = center_y - height / 2.0
    
    if double_border:
        pad = 0.06
        box_out = patches.FancyBboxPatch(
            (x - pad, y - pad), width + 2 * pad, height + 2 * pad,
            boxstyle="round,pad=0.08", facecolor="none", edgecolor="black", linewidth=2.0
        )
        ax.add_patch(box_out)
    
    box = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.08", facecolor="white", edgecolor="black", linewidth=1.5
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(center_x, center_y, text, ha="center", va="center",
            fontsize=fontsize, color="black", weight=weight, linespacing=1.2)

def draw_diamond(ax, center_x, center_y, width, height, text, fontsize=8.6, bold=False):
    pts = [
        [center_x, center_y + height / 2.0],
        [center_x + width / 2.0, center_y],
        [center_x, center_y - height / 2.0],
        [center_x - width / 2.0, center_y]
    ]
    diamond = patches.Polygon(pts, closed=True, facecolor="white", edgecolor="black", linewidth=1.5)
    ax.add_patch(diamond)
    weight = "bold" if bold else "normal"
    ax.text(center_x, center_y, text, ha="center", va="center",
            fontsize=fontsize, color="black", weight=weight, linespacing=1.15)

def draw_arrow(ax, start_x, start_y, end_x, end_y, lw=1.3):
    ax.annotate(
        "", xy=(end_x, end_y), xytext=(start_x, start_y),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=lw, mutation_scale=11)
    )

def generate_research_workflow(output_path="figure_research_workflow_bw.png"):
    fig, ax = plt.subplots(figsize=(11.0, 17.0), dpi=600)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.9, 15.5)
    ax.axis("off")

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9.5
    })

    CX = 4.85     # Main vertical pipeline center
    RX = 8.55     # Rejection / Fallback boxes center
    LX = 1.35     # Iterative optimization loopback center

    # 1. Problem Formulation & Lattice Hamiltonian
    y1 = 14.8
    draw_rounded_rect(ax, CX, y1, 4.3, 0.62, "Initialize Quantum Lattice & Hamiltonian\n$H = -J\\sum Z_i Z_{i+1} - h_x\\sum X_i - h_z\\sum Z_i$", fontsize=9.2)

    # 2. Liouvillian Super-Operator
    y2 = 13.78
    draw_arrow(ax, CX, y1 - 0.31, CX, y2 + 0.31)
    draw_rounded_rect(ax, CX, y2, 4.3, 0.62, "Construct Liouvillian Super-Operator\n$\\mathcal{L}(O) = [H, O] + i\\mathcal{D}_{\\text{Lindblad}}(O)$", fontsize=9.0)

    # 3. Decision Diamond 1: Chaos & Operator Growth
    yd1 = 12.55
    draw_arrow(ax, CX, y2 - 0.31, CX, yd1 + 0.54)
    draw_diamond(ax, CX, yd1, 3.8, 1.08, "Lanczos Algorithm Evaluation:\nDoes system exhibit Universal Operator Growth?\n($b_n \\sim \\alpha n$, Non-integrable regime)", fontsize=8.3)

    # Rejection 1 (Right): Integrable / No growth
    draw_arrow(ax, CX + 1.9, yd1, RX - 1.25, yd1)
    draw_rounded_rect(ax, RX, yd1, 2.5, 0.74, "Integrable dynamics detected\n($b_n \\to \\text{const}$). Re-tune field $h_z$\nor dissipation coupling $\\gamma$", fontsize=8.0)

    # 4. Krylov Complexity Evolution
    y3 = 11.35
    draw_arrow(ax, CX, yd1 - 0.54, CX, y3 + 0.31)
    draw_rounded_rect(ax, CX, y3, 4.3, 0.62, "Evaluate Krylov Complexity Evolution\n$K(t) = \\sum_{n} n |\\phi_n(t)|^2, \\quad S_K(t) = -\\sum p_n \\ln p_n$", fontsize=9.0)

    # 5. Poisson Sprinkling
    y4 = 10.30
    draw_arrow(ax, CX, y3 - 0.31, CX, y4 + 0.31)
    draw_rounded_rect(ax, CX, y4, 4.3, 0.62, "Sample Discrete Spacetime Manifold $\\mathcal{M}^{1+1}$\nPoisson Sprinkling of $N=800$ Events $(x_i, t_i)$", fontsize=9.0)

    # 6. Decision Diamond 2: Monotonic Arrow of Time
    yd2 = 9.08
    draw_arrow(ax, CX, y4 - 0.31, CX, yd2 + 0.54)
    draw_diamond(ax, CX, yd2, 3.8, 1.08, "Dynamical Asymmetry Criterion:\nIs Krylov entropy production strictly monotonic?\n($dK/dt > 0$, Irreversible Arrow of Time)", fontsize=8.3)

    # Rejection 2 (Right): Recurrence / Periodic revival
    draw_arrow(ax, CX + 1.9, yd2, RX - 1.25, yd2)
    draw_rounded_rect(ax, RX, yd2, 2.5, 0.74, "Poincaré recurrence detected.\nIncrease lattice dimension N >= 6\nor truncate recurrence window", fontsize=8.0)

    # 7. Bifurcation into Dual Parallel Evaluators
    y5 = 7.90
    draw_arrow(ax, CX, yd2 - 0.54, CX, y5 + 0.31)
    draw_rounded_rect(ax, CX, y5, 4.3, 0.62, "Partition Relativistic Lightcone Constraints\nand Quantum Dynamical Flow", fontsize=9.0)

    # 8. Dual Parallel Evaluators (Lightcone Causality vs Krylov Arrow Vector)
    y6_a = 7.00
    y6_b = 6.60
    y_split = 7.38
    ax.plot([CX, CX], [y5 - 0.31, y_split], color="black", lw=1.3)
    ax.plot([CX - 0.85, CX + 0.85], [y_split, y_split], color="black", lw=1.3)
    draw_arrow(ax, CX - 0.85, y_split, CX - 0.85, y6_a + 0.20)
    draw_arrow(ax, CX + 0.85, y_split, CX + 0.85, y6_b + 0.20)

    draw_rounded_rect(ax, CX - 0.85, y6_a, 1.85, 0.40, "Analytic Lightcone Metric\n$C_{ij} \\in \\{0, 1\\}$ ($\\Delta s^2 \\geq 0$)", fontsize=8.0)
    draw_rounded_rect(ax, CX + 0.85, y6_b, 1.85, 0.40, "Krylov Modulation Vector\n$\\vec{v}_{\\text{arrow}}(t) = \\frac{dK}{dt} \\cdot \\hat{e}_t$", fontsize=8.0)

    # 9. Directed Causal Graph Synthesis (DAG)
    y7 = 5.50
    y_merge = 6.00
    ax.plot([CX - 0.85, CX - 0.85], [y6_a - 0.20, y_merge], color="black", lw=1.3)
    ax.plot([CX + 0.85, CX + 0.85], [y6_b - 0.20, y_merge], color="black", lw=1.3)
    ax.plot([CX - 0.85, CX + 0.85], [y_merge, y_merge], color="black", lw=1.3)
    draw_arrow(ax, CX, y_merge, CX, y7 + 0.37)

    draw_rounded_rect(ax, CX, y7, 4.4, 0.74, "Synthesize Directed Causal Set Graph (DAG)\nModulate Edge Adjacency Tensor\n$W_{ij} = C_{ij} \\cdot \\vec{v}_{\\text{arrow}}(t_j - t_i)$", fontsize=8.6)

    # 10. Decision Diamond 3: PINN Field Optimization & Residual
    yd3 = 4.15
    draw_arrow(ax, CX, y7 - 0.37, CX, yd3 + 0.54)
    draw_diamond(ax, CX, yd3, 3.8, 1.08, "Physical Field Convergence:\nDoes GNN-PINN satisfy Klein-Gordon PDE?\n($\\mathcal{R}_{\\text{PDE}} < 10^{-3}$, Loss $\\mathcal{L}_{\\text{total}} \\to 0$)", fontsize=8.3)

    # Left Branch: Residual exceeds tolerance
    draw_arrow(ax, CX - 1.9, yd3, LX + 1.25, yd3)
    draw_rounded_rect(ax, LX, yd3, 2.5, 0.68, "Field residual exceeds\ntolerance ($\\mathcal{R}_{\\text{PDE}} > 10^{-3}$)", fontsize=8.2)

    # Revision box at Left (Iterative Optimization Loop)
    y_rev = 8.5
    draw_rounded_rect(ax, LX, y_rev, 2.5, 0.82, "Backpropagate Gradients\nUpdate GNN message passing\n& Cosine Annealing rate", fontsize=8.2)

    # Vertical arrow from sent back to author revision box
    draw_arrow(ax, LX, yd3 + 0.34, LX, y_rev - 0.41)

    # Loopback arrow into y4 (Spacetime sampling & graph adjustment)
    y_turn = 10.82
    ax.plot([LX, LX], [y_rev + 0.41, y_turn], color="black", lw=1.3)
    ax.plot([LX, CX], [y_turn, y_turn], color="black", lw=1.3)
    draw_arrow(ax, CX, y_turn, CX, y4 + 0.31)

    # 11. Project Bulk Geometry
    y8 = 2.85
    draw_arrow(ax, CX, yd3 - 0.54, CX, y8 + 0.31)
    draw_rounded_rect(ax, CX, y8, 4.3, 0.62, "Forward Spacetime Projection to Bulk Geometry\nExtract Curvature Invariant $R_{\\mu\\nu}$ and Metric $g_{\\mu\\nu}$", fontsize=8.6)

    # 12. Decision Diamond 4: Global Holographic Duality
    yd4 = 1.65
    draw_arrow(ax, CX, y8 - 0.31, CX, yd4 + 0.54)
    draw_diamond(ax, CX, yd4, 3.8, 1.08, "Global Holographic Verification:\nDoes emergent geometry satisfy AdS/CFT duality?\n(Area Law & Diffeomorphism Invariance)", fontsize=8.3)

    # Rejection 3 (Right)
    draw_arrow(ax, CX + 1.9, yd4, RX - 1.25, yd4)
    draw_rounded_rect(ax, RX, yd4, 2.5, 0.74, "Diffeomorphism anomaly detected.\nRecalibrate boundary coupling\nor collocation boundary scale $z_0$", fontsize=8.0)

    # 13. Terminal Acceptance: Physical Equilibrium Validated
    # Font size 20, no "export", no filename, prominent double border
    y9 = 0.08
    w_term = 6.4
    h_term = 1.30
    draw_arrow(ax, CX, yd4 - 0.54, CX, y9 + h_term / 2.0 + 0.08)
    draw_rounded_rect(ax, CX, y9, w_term, h_term,
                      "Physical Equilibrium Reached\nEmergent Spacetime Validated",
                      fontsize=20, bold=True, double_border=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches="tight")
    plt.close()
    
    # Also overwrite figure_workflow_bw.png with this updated research workflow
    shutil.copyfile(output_path, "figure_workflow_bw.png")
    print(f"[SUCCESS] Research workflow saved to: {output_path} and copied to figure_workflow_bw.png")

if __name__ == "__main__":
    generate_research_workflow()
