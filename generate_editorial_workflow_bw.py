import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rounded_rect(ax, center_x, center_y, width, height, text, fontsize=8.8, bold=False, double_border=False):
    x = center_x - width / 2.0
    y = center_y - height / 2.0
    
    if double_border:
        pad = 0.045
        box_out = patches.FancyBboxPatch(
            (x - pad, y - pad), width + 2 * pad, height + 2 * pad,
            boxstyle="round,pad=0.06", facecolor="none", edgecolor="black", linewidth=1.8
        )
        ax.add_patch(box_out)
    
    box = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.06", facecolor="white", edgecolor="black", linewidth=1.4
    )
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(center_x, center_y, text, ha="center", va="center",
            fontsize=fontsize, color="black", weight=weight, linespacing=1.2)

def draw_diamond(ax, center_x, center_y, width, height, text, fontsize=8.4, bold=False):
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

def generate_editorial_workflow(output_path="figure_editorial_workflow_bw.png"):
    fig, ax = plt.subplots(figsize=(10.5, 16.0), dpi=600)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.4, 15.5)
    ax.axis("off")

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9
    })

    CX = 4.85     # Main vertical pipeline center
    RX = 8.55     # Rejection boxes center
    LX = 1.35     # Revision loopback center

    # 1. Author submits manuscript
    y1 = 14.8
    draw_rounded_rect(ax, CX, y1, 4.0, 0.58, "Author submits manuscript\nto PMR journal", fontsize=9.2)

    # 2. EiC evaluates
    y2 = 13.8
    draw_arrow(ax, CX, y1 - 0.29, CX, y2 + 0.29)
    draw_rounded_rect(ax, CX, y2, 4.0, 0.58, "Editor-in-Chief evaluates manuscript\ntaking into account basic criteria", fontsize=9.0)

    # 3. EiC decision diamond 1
    yd1 = 12.6
    draw_arrow(ax, CX, y2 - 0.29, CX, yd1 + 0.52)
    draw_diamond(ax, CX, yd1, 3.6, 1.04, "Editor-in-Chief\nmakes decision based on basic criteria for\nPMR journal", fontsize=8.3)

    # Rejection 1 (Right)
    draw_arrow(ax, CX + 1.8, yd1, RX - 1.25, yd1)
    draw_rounded_rect(ax, RX, yd1, 2.5, 0.72, "Manuscript is rejected due to\nnot meeting basic criteria for\nPMR journal", fontsize=8.2)

    # 4. EiC assigns Associate Editor
    y3 = 11.4
    draw_arrow(ax, CX, yd1 - 0.52, CX, y3 + 0.29)
    draw_rounded_rect(ax, CX, y3, 4.0, 0.58, "Editor-in-Chief assigns Associate Editor\nbased on subject matter expertise", fontsize=8.8)

    # 5. AE evaluates
    y4 = 10.35
    draw_arrow(ax, CX, y3 - 0.29, CX, y4 + 0.29)
    draw_rounded_rect(ax, CX, y4, 4.0, 0.58, "Associate Editor evaluates manuscript\ntaking into account assessment criteria", fontsize=8.8)

    # 6. AE decision diamond 2
    yd2 = 9.15
    draw_arrow(ax, CX, y4 - 0.29, CX, yd2 + 0.52)
    draw_diamond(ax, CX, yd2, 3.6, 1.04, "Associate Editor\nmakes decision based on assessment\ncriteria", fontsize=8.3)

    # Rejection 2 (Right)
    draw_arrow(ax, CX + 1.8, yd2, RX - 1.25, yd2)
    draw_rounded_rect(ax, RX, yd2, 2.5, 0.72, "Manuscript is rejected due to\nnot meeting assessment criteria\nfor PMR journal", fontsize=8.2)

    # 7. AE assigns at least two Reviewers
    y5 = 7.95
    draw_arrow(ax, CX, yd2 - 0.52, CX, y5 + 0.29)
    draw_rounded_rect(ax, CX, y5, 4.0, 0.58, "Associate Editor assigns at least two\nReviewers", fontsize=9.0)

    # 8. Staggered Reviewer boxes with proper bifurcation lines
    y6_a = 7.05
    y6_b = 6.65
    y_split = 7.42
    
    # Line down from y5 to y_split, then branch left and right
    ax.plot([CX, CX], [y5 - 0.29, y_split], color="black", lw=1.3)
    ax.plot([CX - 0.7, CX + 0.7], [y_split, y_split], color="black", lw=1.3)
    draw_arrow(ax, CX - 0.7, y_split, CX - 0.7, y6_a + 0.18)
    draw_arrow(ax, CX + 0.7, y_split, CX + 0.7, y6_b + 0.18)

    draw_rounded_rect(ax, CX - 0.7, y6_a, 1.6, 0.36, "Reviewer", fontsize=8.8)
    draw_rounded_rect(ax, CX + 0.7, y6_b, 1.6, 0.36, "Reviewer", fontsize=8.8)

    # 9. Reviewers complete form
    y7 = 5.55
    y_merge = 6.05
    ax.plot([CX - 0.7, CX - 0.7], [y6_a - 0.18, y_merge], color="black", lw=1.3)
    ax.plot([CX + 0.7, CX + 0.7], [y6_b - 0.18, y_merge], color="black", lw=1.3)
    ax.plot([CX - 0.7, CX + 0.7], [y_merge, y_merge], color="black", lw=1.3)
    draw_arrow(ax, CX, y_merge, CX, y7 + 0.36)

    draw_rounded_rect(ax, CX, y7, 4.2, 0.72, "Reviewers complete Manuscript Review\nForm and submit it together with\ncomments and recommendations to\nAssociate Editor", fontsize=8.6)

    # 10. AE decision diamond 3 (Reviewer evaluation)
    yd3 = 4.20
    draw_arrow(ax, CX, y7 - 0.36, CX, yd3 + 0.52)
    draw_diamond(ax, CX, yd3, 3.6, 1.04, "Associate Editor\nevaluates manuscript based on Reviewer\ncomments and recommendations", fontsize=8.3)

    # Left Branch: Manuscript sent back to Author for revision
    draw_arrow(ax, CX - 1.8, yd3, LX + 1.25, yd3)
    draw_rounded_rect(ax, LX, yd3, 2.5, 0.68, "Manuscript is sent back to\nAuthor for revision", fontsize=8.3)

    # Revision box at Left (aligned with upper flow)
    y_rev = 8.5
    draw_rounded_rect(ax, LX, y_rev, 2.5, 0.82, "Author revises manuscript\nbased on Reviewer(s)\nsuggestions and resubmits to\nAssociate Editor", fontsize=8.0)

    # Vertical arrow from sent back to author revision box
    draw_arrow(ax, LX, yd3 + 0.34, LX, y_rev - 0.41)

    # Loopback arrow: from Author revises up, right, and into line entering AE evaluation (y4)
    y_turn = 10.88
    ax.plot([LX, LX], [y_rev + 0.41, y_turn], color="black", lw=1.3)
    ax.plot([LX, CX], [y_turn, y_turn], color="black", lw=1.3)
    draw_arrow(ax, CX, y_turn, CX, y4 + 0.29)

    # 11. AE submits to EiC
    y8 = 2.90
    draw_arrow(ax, CX, yd3 - 0.52, CX, y8 + 0.29)
    draw_rounded_rect(ax, CX, y8, 4.0, 0.58, "Associate Editor submits manuscript\ntogether with his recommendations to\nEditor-in-Chief", fontsize=8.6)

    # 12. EiC decision diamond 4
    yd4 = 1.70
    draw_arrow(ax, CX, y8 - 0.29, CX, yd4 + 0.52)
    draw_diamond(ax, CX, yd4, 3.6, 1.04, "Editor-in-Chief\nmakes decision based on Associate Editor\nrecommendations", fontsize=8.3)

    # Rejection 3 (Right)
    draw_arrow(ax, CX + 1.8, yd4, RX - 1.25, yd4)
    draw_rounded_rect(ax, RX, yd4, 2.5, 0.72, "Manuscript is rejected due to\nnot meeting criteria for\npublication in PMR journal", fontsize=8.2)

    # 13. Terminal Acceptance (Bottom)
    y9 = 0.50
    draw_arrow(ax, CX, yd4 - 0.52, CX, y9 + 0.32)
    draw_rounded_rect(ax, CX, y9, 4.0, 0.60, "Manuscript is accepted for publication\nin PMR journal", fontsize=9.2, bold=True, double_border=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] High-fidelity editorial workflow saved to: {output_path}")

if __name__ == "__main__":
    generate_editorial_workflow()
