---
name: academic-research
description: >-
  Comprehensive academic research, scientific methodology formalization, and manuscript engineering guide.
  Use this skill whenever conducting literature reviews, empirical experiment design, mathematical modeling,
  manuscript drafting/revision for international and national journals (IEEE, ACM, Elsevier, Springer, IJEA, JANAPATI),
  converting equations to native Word Office Math (<m:oMath>), generating publication-grade 600 DPI figures,
  structuring point-by-point response to peer-reviewers, and auditing academic integrity.
---

# Academic Research & Scientific Publishing Skill

This skill guides the end-to-end lifecycle of academic research and scientific manuscript preparation, ensuring rigorous methodology, empirical reproducibility, flawless mathematical typesetting, high-impact data visualization, and successful peer-review navigation.

---

## 1. Core Workflow & Research Lifecycle

```text
1. Conceptualization & State-of-the-Art Review
   └── Map scientific gap vs. baseline literature (Related Works Synthesis Table)
2. Mathematical Modeling & Problem Formulation
   └── Formalize state/action/objective functions (MDP, combinatorial optimization, Pareto)
3. Empirical Telemetry & Reproducibility Setup
   └── Data mining, feature schema definition, preprocessing, train/eval split, random seed control
4. Computational Implementation & Baseline Benchmarking
   └── State-of-the-art models vs. classical metaheuristics vs. unconstrained control baselines
5. Rigorous Multi-Objective Evaluation & Statistical Validation
   └── Quantitative metric tables, trade-off Pareto curves, convergence speed, variance analysis
6. Academic Manuscript Writing (Publisher Format)
   └── Flowing prose (zero bullet points in body), dual table/figure mentions, native Office Math
7. Peer-Review Revision & Point-by-Point Rebuttal
   └── Structured reviewer response matrix, polite evidence-based argumentation, manuscript cross-referencing
```

---

## 2. Mathematical Formalization & Native Word Office Math (`<m:oMath>`)

Scientific papers require professional, numbered mathematical expressions. When drafting or modifying Word (`.docx`) manuscripts:

### A. Display Equations
- **Alignment**: Centered equation with right-aligned numbering `(1)`–`(N)`.
- **Implementation**: Use two tab stops on the paragraph:
  - Center tab at middle of text column (e.g. `4819` dxa for single-column A4 or `4500` dxa).
  - Right tab at right margin (e.g. `9638` dxa or `9000` dxa).
- **Run structure**: `add_run("\t")` + `omml_element` + `add_run(f"\t({eq_num})")`.

### B. LaTeX to Native Office Math Pipeline
In Python `python-docx`, never leave raw text equations like `B_a = 1.0 - exp(-|tc - ds_i|)`. Convert them via:
1. `latex2mathml.converter.convert(latex_code)` $\rightarrow$ MathML.
2. Transform MathML to OMML using Microsoft's official `MML2OMML.XSL` (`C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL`) via `lxml.etree.XSLT`.
3. Append root `<m:oMath>` element directly to `paragraph._p`.

### C. Critical LaTeX Delimiter Rules for Word OMML
- **Absolute Value**: Avoid bare `$|a - b|$` or `\left| a - b \right|` because `MML2OMML.XSL` interprets the minus sign inside fences as a delimiter separator (`<m:sepChr>`), which can drop or hide the minus sign. **Always use `\lvert a - b \rvert`**.
- **Square Brackets with Minus Signs**: Avoid `\left[ 1.0 - \frac{a}{b} \right]`. Use standard brackets `[ 1.0 - \frac{a}{b} ]` to prevent minus operator absorption into delimiter attributes.
- **Text in Subscripts & Formulas**: Use `\text{variable}` without underscores, e.g., `\text{resolution hours}` or `\text{success}`.

Refer to [`references/equation_guidelines.md`](./references/equation_guidelines.md) for complete equation patterns.

---

## 3. Scientific Visualization Standards (600 DPI Figures)

All figures submitted to peer-reviewed journals must meet strict publication standards:

1. **Resolution & Format**: Minimum **600 DPI**, PNG/TIFF format, lossless compression.
2. **Typography**:
   - Font family must match manuscript typography (Times New Roman or Cambria).
   - Label font size: **12pt to 14pt** (must remain completely legible when scaled down to column width).
   - Bold panel markers: **(a)**, **(b)**, **(c)**.
3. **Color & Contrast**:
   - Professional, accessible palettes (e.g., ColorBrewer, Seaborn 'deep', 'muted', viridis).
   - Distinct linestyles (`-`, `--`, `-.`, `:`) and markers (`o`, `s`, `^`, `D`) for grayscale printing readability.
4. **Layout**:
   - Zero label clipping; use `plt.tight_layout()` or `bbox_inches='tight'`.
   - Gridlines: subtle dashed gray (`alpha=0.3` to `0.5`).

---

## 4. Academic Rhetoric, Manuscript Structure & Dual-Mention Rule

### A. Zero Bullet Point Constraint
In standard academic journal bodies (Introduction, Methodology, Results, Discussion, Conclusion), avoid informal bulleted lists. Restructure all itemized descriptions into **continuous academic prose** with discourse markers (*First, ... Second, ... Furthermore, ... Finally, ...*).

### B. Mandatory Dual-Mention Rule
Every single table and figure must be referenced at least **twice** in the manuscript body:
1. **Pre-Mention (Introductory Callout)**: Immediately before the figure/table, explicitly directing the reader (e.g., *"To contextualize the experimental workflow, Figure 1 delineates the end-to-end architecture..."*).
2. **Post-Mention (Analytical Discussion)**: In the paragraph immediately following the figure/table, providing in-depth scientific interpretation of the observed trends, trade-offs, and empirical findings.

### C. Empirical Numerical Consistency
Every metric stated in the Abstract, Introduction, Results Tables, Discussion, and Conclusion must match 100% with the latest retrained experimental data. Never leave stale or conflicting metrics across sections.

---

## 5. Peer-Review Response Strategy (Response to Reviewers)

When preparing rebuttal documents:
1. **Point-by-Point Matrix**: Structure every reviewer query with:
   - Reviewer Comment (verbatim quote, italicized).
   - Author's Response (appreciative, objective, evidence-driven, citing exact equations and numbers).
   - Exact Location in Revised Manuscript (Section, Paragraph, Equation number, Table number).
2. **Native Math in Responses**: All formulas and variables mentioned in the response document must be rendered in native Office Math `<m:oMath>`—never raw plain text.
3. **Addressing Reviewer Confusion on Trade-offs**: When heuristics (like PSO) appear to win on one narrow metric (e.g., single-step throughput) but cause severe systemic failure (e.g., extreme burnout, workload skew), explain the **behavioral economics and Pareto optimality trade-offs** clearly.

Refer to [`references/peer_review_response_guide.md`](./references/peer_review_response_guide.md) for rebuttal strategies.

---

## 6. Automated Manuscript Verification Scripts

Always verify document integrity using the provided automation scripts:
- **`scripts/verify_manuscript.py`**: Audits paragraphs, tables, dual mentions, bullet counts, and scans for any unformatted plain text equations.
- **`scripts/latex_to_word_omml.py`**: Standalone helper for converting LaTeX strings to native Word Office Math XML.
