import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_figure_1_chevron_structure(output_path="figure_1_system_architecture.png"):
    """
    Figure 1: High-Impact Chevron & Vertical Column Process Architecture 
    Matching User's Reference Layout in Ultra-Neat Academic Monochrome (600 DPI).
    """
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm"
    })

    fig, ax = plt.subplots(figsize=(16, 9.2), dpi=600)
    ax.set_xlim(0, 16)
    ax.set_ylim(-0.4, 9.2)
    ax.axis("off")

    # Geometry Setup
    n_stages = 4
    col_w = 3.30
    gap = 0.40
    d_chev = 0.28  # Chevron point/indent depth
    margin_x = (16.0 - (n_stages * col_w + (n_stages - 1) * gap)) / 2.0

    y_card_bot = 0.75
    card_h = 5.25
    y_card_top = y_card_bot + card_h

    gap_v = 0.12
    title_box_h = 0.72
    y_title_bot = y_card_top + gap_v
    y_title_top = y_title_bot + title_box_h

    chev_h = 0.78
    y_chev_bot = y_title_top + gap_v
    y_chev_top = y_chev_bot + chev_h
    y_chev_mid = (y_chev_bot + y_chev_top) / 2.0

    # Grayscale fills for chevron progression (UV to IR)
    chev_fills = ["#FFFFFF", "#F6F6F6", "#ECECEC", "#E0E0E0"]

    # 4 Foundational Stages
    stages = [
        {
            "num": "1",
            "title": "Quantum Microstate",
            "subtitle": "Microscopic Spin Lattice (UV)",
            "bullets": [
                r"$\bullet$ 1D Heisenberg Spin Chain ($L=6$)",
                r"$\bullet$ Mixed-Field Chaos ($h_x=1.05, h_z=0.50$)",
                r"$\bullet$ Liouvillian Super-Operator $\mathcal{L}$",
                r"$\bullet$ Non-Unitary Lindblad Dissipation",
                r"$\bullet$ Broken Time-Reversal Symmetry"
            ],
            "formula_label": "Master Equation",
            "formula": r"$\frac{dO}{dt} = i[H, O] + \sum_k \gamma_k \mathcal{D}_k(O)$"
        },
        {
            "num": "2",
            "title": "Krylov Dynamics",
            "subtitle": "Operator Complexity Growth",
            "bullets": [
                r"$\bullet$ Lanczos Orthonormal Basis $\{|O_n\rangle\}$",
                r"$\bullet$ Linear Chaotic Growth ($\alpha \approx 0.0588$)",
                r"$\bullet$ Circuit Complexity $K(t) = \sum n p_n(t)$",
                r"$\bullet$ Irreversible Entropy Plateau ($S_K \approx 3.01$)",
                r"$\bullet$ Emergent Arrow of Time $\vec{v}_{\mathrm{arrow}} > 0$"
            ],
            "formula_label": "Krylov Arrow of Time",
            "formula": r"$\vec{v}_{\mathrm{arrow}}(t) = \frac{dK(t)}{dt}\hat{e}_t > 0$"
        },
        {
            "num": "3",
            "title": "Discrete Causal Set",
            "subtitle": "Lorentzian DAG Topology",
            "bullets": [
                r"$\bullet$ $N=800$ Poisson Sprinkled Events",
                r"$\bullet$ Relativistic Lightcones ($\Delta s^2 > 0$)",
                r"$\bullet$ 91,489 Directed Timelike Edges",
                r"$\bullet$ Arrow-of-Time Edge Weight Modulation",
                r"$\bullet$ Suppression of Non-Local Links"
            ],
            "formula_label": "Lightcone Modulation",
            "formula": r"$W_{ij} = C_{ij} \left[ \frac{1 + \beta \|\vec{v}_{\mathrm{arrow}}\|}{1 + \Delta s_{ij}^2} \right]$"
        },
        {
            "num": "4",
            "title": "Hybrid GNN-PINN",
            "subtitle": "Continuum Spacetime (IR)",
            "bullets": [
                r"$\bullet$ Directed Graph Message Passing",
                r"$\bullet$ Coordinate MLP Head ($\tanh$ activations)",
                r"$\bullet$ Autograd Klein-Gordon Loss Engine",
                r"$\bullet$ Interior PDE Residual $\mathcal{L}_{\mathrm{pde}} < 10^{-3}$",
                r"$\bullet$ Emergent Differentiable Field $\phi(x, t)$"
            ],
            "formula_label": "Relativistic Residual",
            "formula": r"$(\partial_t^2 - \partial_x^2 + m^2)\phi_\theta(x, t) = 0$"
        }
    ]

    for idx, s in enumerate(stages):
        x = margin_x + idx * (col_w + gap)

        # -------------------------------------------------------------
        # 1. TOP CHEVRON ARROW
        # -------------------------------------------------------------
        chev_pts = [
            [x, y_chev_top],                    # top-left
            [x + col_w, y_chev_top],            # top-right
            [x + col_w + d_chev, y_chev_mid],   # right point
            [x + col_w, y_chev_bot],            # bottom-right
            [x, y_chev_bot],                    # bottom-left
            [x + d_chev, y_chev_mid]            # left indent
        ]
        chev_poly = patches.Polygon(
            chev_pts, closed=True,
            facecolor=chev_fills[idx],
            edgecolor="black",
            linewidth=2.2,
            zorder=3
        )
        ax.add_patch(chev_poly)

        # Step Number inside Chevron
        num_cx = x + col_w / 2.0 + d_chev / 2.0
        ax.text(num_cx, y_chev_mid, s["num"],
                ha="center", va="center", fontsize=22, fontweight="bold",
                color="black", zorder=4)

        # -------------------------------------------------------------
        # 2. TITLE BOX (Directly under Chevron)
        # -------------------------------------------------------------
        title_box = patches.FancyBboxPatch(
            (x, y_title_bot), col_w, title_box_h,
            boxstyle="round,pad=0.08",
            facecolor="#F4F4F4",
            edgecolor="black",
            linewidth=2.0,
            zorder=3
        )
        ax.add_patch(title_box)

        ax.text(x + col_w / 2.0, y_title_bot + title_box_h / 2.0, s["title"],
                ha="center", va="center", fontsize=12.5, fontweight="bold",
                color="black", zorder=4)

        # -------------------------------------------------------------
        # 3. TALL VERTICAL COLUMN CARD (Directly under Title Box)
        # -------------------------------------------------------------
        card = patches.FancyBboxPatch(
            (x, y_card_bot), col_w, card_h,
            boxstyle="round,pad=0.10",
            facecolor="white",
            edgecolor="black",
            linewidth=2.0,
            zorder=2
        )
        ax.add_patch(card)

        # Subtitle / Domain Tag inside Card
        sub_y = y_card_top - 0.35
        ax.text(x + col_w / 2.0, sub_y, s["subtitle"],
                ha="center", va="center", fontsize=9.2, style="italic",
                color="#444444")

        # Subtle divider line under subtitle
        div_y = sub_y - 0.22
        ax.plot([x + 0.30, x + col_w - 0.30], [div_y, div_y],
                color="#CCCCCC", lw=1.2, ls="-")

        # Bullet Items
        item_y = div_y - 0.38
        for b_text in s["bullets"]:
            ax.text(x + 0.20, item_y, b_text,
                    ha="left", va="center", fontsize=9.2, color="#111111",
                    linespacing=1.25)
            item_y -= 0.44

        # Formula Highlight Box at the bottom of Card
        f_box_h = 0.95
        f_box_y = y_card_bot + 0.22
        f_box_w = col_w - 0.36
        f_box = patches.FancyBboxPatch(
            (x + 0.18, f_box_y), f_box_w, f_box_h,
            boxstyle="round,pad=0.08",
            facecolor="#FAFAFA",
            edgecolor="black",
            linestyle="--",
            linewidth=1.3,
            zorder=3
        )
        ax.add_patch(f_box)

        # Formula Label
        ax.text(x + col_w / 2.0, f_box_y + f_box_h - 0.22, s["formula_label"],
                ha="center", va="center", fontsize=8.0, fontweight="bold",
                color="#555555", style="italic")

        # Formula Mathematical Expression
        ax.text(x + col_w / 2.0, f_box_y + 0.36, s["formula"],
                ha="center", va="center", fontsize=10.0, fontweight="bold",
                color="black")

    # -----------------------------------------------------------------
    # 4. BOTTOM HOLOGRAPHIC PROGRESSION BAR
    # -----------------------------------------------------------------
    prog_y = 0.22
    start_x = margin_x + 0.20
    end_x = 16.0 - margin_x - 0.20

    ax.annotate(
        "", xy=(end_x, prog_y), xytext=(start_x, prog_y),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=2.0, mutation_scale=18)
    )

    badge_text = "  HOLOGRAPHIC PROGRESSION: Microscopic Quantum Dissipation (UV) $\\longrightarrow$ Emergent Relativistic Spacetime (IR)  "
    ax.text(8.0, prog_y, badge_text,
            ha="center", va="center", fontsize=9.2, fontweight="bold", color="black",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="black", linewidth=1.3))

    # -----------------------------------------------------------------
    # 5. TITLE & SUBTITLE AT THE TOP
    # -----------------------------------------------------------------
    ax.text(8.0, 8.85, "Figure 1: Holographic Krylov-PINN (HK-PCG) System Architecture",
            ha="center", va="center", fontsize=15.5, fontweight="bold", color="black")
    ax.text(8.0, 8.48, "End-to-End Synthesis Pipeline: Unifying Open Spin Dissipation, Krylov Complexity, Causal Sets, and Differential PINNs",
            ha="center", va="center", fontsize=10.5, style="italic", color="#444444")

    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] High-resolution Chevron Process Figure 1 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_1_chevron_structure()
