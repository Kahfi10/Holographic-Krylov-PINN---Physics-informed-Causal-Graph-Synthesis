import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_figure_1_bw(output_path="figure_1_system_architecture.png"):
    """
    Figure 1: Clean, Minimalist, High-Impact Monochrome (Black & White) 
    System Architecture of the HK-PCG Framework (600 DPI).
    """
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm"
    })

    fig, ax = plt.subplots(figsize=(16, 6.2), dpi=600)
    ax.set_xlim(0, 16)
    ax.set_ylim(-0.6, 6.2)
    ax.axis("off")

    # 4 Modular Stages: (x, y, w, h, stage_num, title, tag, items, formula_box)
    stages = [
        {
            "x": 0.6, "y": 0.8, "w": 3.0, "h": 4.3,
            "stage": "STAGE 1",
            "title": "Quantum Microstate",
            "tag": "Microscopic Lattice (UV)",
            "items": [
                r"$\bullet$ 1D Heisenberg Spin Chain ($L=6$)",
                r"$\bullet$ Mixed-Field Chaos ($h_x=1.05, h_z=0.5$)",
                r"$\bullet$ Non-Unitary Lindblad Dissipation",
                r"$\bullet$ Broken Time-Reversal Symmetry"
            ],
            "formula": r"$\frac{dO}{dt} = \mathcal{L}(O) = i[H, O] + \mathcal{D}(O)$"
        },
        {
            "x": 4.5, "y": 0.8, "w": 3.0, "h": 4.3,
            "stage": "STAGE 2",
            "title": "Krylov Dynamics",
            "tag": "Operator Complexity Growth",
            "items": [
                r"$\bullet$ Lanczos Orthonormal Basis $\{|O_n\rangle\}$",
                r"$\bullet$ Linear Chaotic Slope ($\alpha \approx 0.0588$)",
                r"$\bullet$ Suppressed Poincaré Revivals",
                r"$\bullet$ Unidirectional Entropy Plateau"
            ],
            "formula": r"$\vec{v}_{\mathrm{arrow}} = \frac{dK(t)}{dt}\hat{e}_t > 0$"
        },
        {
            "x": 8.4, "y": 0.8, "w": 3.0, "h": 4.3,
            "stage": "STAGE 3",
            "title": "Discrete Causal Set",
            "tag": "Lorentzian DAG Topology",
            "items": [
                r"$\bullet$ 800 Poisson-Sprinkled Events",
                r"$\bullet$ Relativistic Lightcones ($\Delta s^2 > 0$)",
                r"$\bullet$ 91,489 Directed Causal Links",
                r"$\bullet$ Arrow-of-Time Edge Modulation"
            ],
            "formula": r"$W_{ij} = C_{ij} \left[ \frac{1 + \beta \|\vec{v}_{\mathrm{arrow}}\|}{1 + \Delta s_{ij}^2} \right]$"
        },
        {
            "x": 12.3, "y": 0.8, "w": 3.0, "h": 4.3,
            "stage": "STAGE 4",
            "title": "Hybrid GNN-PINN",
            "tag": "Continuum Spacetime (IR)",
            "items": [
                r"$\bullet$ Directed Graph Message Passing",
                r"$\bullet$ Second-Order Autograd Residual",
                r"$\bullet$ Klein-Gordon Loss ($\mathcal{L}_{\mathrm{pde}} < 10^{-3}$)",
                r"$\bullet$ Holographic Bulk Duality"
            ],
            "formula": r"$(\partial_t^2 - \partial_x^2 + m^2)\phi_\theta = 0$"
        }
    ]

    for s in stages:
        x, y, w, h = s["x"], s["y"], s["w"], s["h"]

        # Main Card Body (Pure White with crisp black border)
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.12",
            facecolor="white",
            edgecolor="black",
            linewidth=2.2
        )
        ax.add_patch(card)

        # Header Banner (Light gray shading with black outline)
        hdr_h = 1.05
        hdr = patches.FancyBboxPatch(
            (x, y + h - hdr_h), w, hdr_h,
            boxstyle="round,pad=0.10",
            facecolor="#F4F4F4",
            edgecolor="black",
            linewidth=1.8
        )
        ax.add_patch(hdr)

        # Header Stage Tag
        ax.text(x + w / 2.0, y + h - 0.28, s["stage"],
                ha="center", va="center", fontsize=9.5, fontweight="bold",
                color="#444444")

        # Header Title
        ax.text(x + w / 2.0, y + h - 0.58, s["title"],
                ha="center", va="center", fontsize=12.5, fontweight="bold",
                color="black")

        # Header Subtitle Tag
        ax.text(x + w / 2.0, y + h - 0.86, s["tag"],
                ha="center", va="center", fontsize=8.8, style="italic",
                color="#555555")

        # Bullet Items
        item_y = y + h - 1.35
        for item in s["items"]:
            ax.text(x + 0.18, item_y, item,
                    ha="left", va="center", fontsize=9.2, color="#111111")
            item_y -= 0.42

        # Formula Highlight Box (Dashed black border, subtle off-white fill)
        f_box_h = 0.72
        f_box_y = y + 0.22
        f_box = patches.FancyBboxPatch(
            (x + 0.16, f_box_y), w - 0.32, f_box_h,
            boxstyle="round,pad=0.08",
            facecolor="#FAFAFA",
            edgecolor="black",
            linestyle="--",
            linewidth=1.2
        )
        ax.add_patch(f_box)
        ax.text(x + w / 2.0, f_box_y + f_box_h / 2.0, s["formula"],
                ha="center", va="center", fontsize=10.0, fontweight="bold", color="black")

    # Clean Connecting Arrows between Stages with enhanced spacing
    arrow_props = dict(
        arrowstyle="-|>",
        color="black",
        lw=2.2,
        mutation_scale=18
    )

    connectors = [
        {"start": (3.68, 2.70), "end": (4.42, 2.70), "label": "Super-Operator\nEvolution"},
        {"start": (7.58, 2.70), "end": (8.32, 2.70), "label": "Arrow-of-Time\nBias $\\vec{v}_{\\mathrm{arrow}}$"},
        {"start": (11.48, 2.70), "end": (12.22, 2.70), "label": "Directed DAG\n$(\\mathcal{C}, W_{ij})$"}
    ]

    for c in connectors:
        sx, sy = c["start"]
        ex, ey = c["end"]
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy), arrowprops=arrow_props)
        # Connector Label placed cleanly above arrow
        mid_x = (sx + ex) / 2.0
        ax.text(mid_x, sy + 0.35, c["label"],
                ha="center", va="bottom", fontsize=8.0, fontweight="bold",
                color="#111111", linespacing=1.15,
                bbox=dict(boxstyle="square,pad=0.18", facecolor="white", edgecolor="none"))

    # Bottom Progression Banner (Holographic Axis)
    prog_y = 0.20
    ax.annotate(
        "", xy=(15.2, prog_y), xytext=(0.8, prog_y),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8, mutation_scale=16)
    )
    # Background badge for progression text
    ax.text(8.0, prog_y, "  HOLOGRAPHIC PROGRESSION: Microscopic Quantum Dissipation (UV) $\\longrightarrow$ Emergent Relativistic Spacetime (IR)  ",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="black",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="black", linewidth=1.2))

    # Title & Subtitle at the Top
    ax.text(8.0, 5.85, "Figure 1: Holographic Krylov-PINN (HK-PCG) System Architecture",
            ha="center", va="center", fontsize=15, fontweight="bold", color="black")
    ax.text(8.0, 5.50, "End-to-End Synthesis Pipeline: Unifying Open Spin Dissipation, Krylov Complexity, Causal Sets, and Differential PINNs",
            ha="center", va="center", fontsize=10.5, style="italic", color="#444444")

    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] High-resolution monochrome Figure 1 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_1_bw()
