# Mathematical Notation & Equation Engineering Guidelines

This reference documents the best practices for authoring, compiling, and embedding mathematical equations into academic Word documents using LaTeX and Microsoft Office Math (`<m:oMath>`).

---

## 1. LaTeX to Word OMML Pipeline

Word stores native equations using **Office Math Markup Language (OMML)** inside `<m:oMath>` tags. To insert clean, scalable, native Word math without using slow or unreliable COM automation:

1. Write clean LaTeX expressions.
2. Convert LaTeX to MathML via `latex2mathml`.
3. Transform MathML to OMML using Microsoft's official `MML2OMML.XSL` (`C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL`) via `lxml.etree.XSLT`.
4. Append the resulting `<m:oMath>` element directly into `paragraph._p`.

---

## 2. Avoiding Common OMML Delimiter Pitfalls

`MML2OMML.XSL` converts MathML fences `<mo fence="true">` into delimiter objects `<m:d>`. In certain expressions, mathematical minus signs (`-`) or hyphens inside fences are misinterpreted as delimiter separator characters (`<m:sepChr>`), resulting in invisible or swallowed operators.

### Rule 1: Absolute Values
- ❌ **Do NOT use**: `$|a - b|$` or `\left| a - b \right|`
- ✅ **DO use**: `\lvert a - b \rvert`
  - Example: `B_a = 1.0 - \exp(-\lvert tc - ds_i \rvert)`

### Rule 2: Brackets around Expressions with Minus Signs
- ❌ **Do NOT use**: `\left[ 1.0 - \frac{\sigma}{\sigma_{\max}} \right]`
- ✅ **DO use**: `[ 1.0 - \frac{\sigma}{\sigma_{\max}} ]`
  - Example: `S_{\text{dev}} = [1.0 - \frac{\sigma}{\sigma_{\max}}] \times [1.0 - \overline{L}_{\text{bias}}] \times 100\%`

### Rule 3: Text Inside Subscripts & Math
- ❌ **Do NOT use**: `\text{resolution\_hours}` (leaves backslash visible)
- ✅ **DO use**: `\text{resolution hours}` or `\text{res\_time}`

### Rule 4: Exponential and Logarithmic Functions
- Use standard LaTeX operators: `\exp(...)`, `\ln(...)`, `\log(...)`, `\max(...)`, `\min(...)`.

---

## 3. Display Equation Layout & Numbering

For publication templates (e.g., IJEA single-column, IEEE double-column):
- Each display equation must be centered.
- The equation number `(1)`, `(2)`, ..., `(N)` must be right-aligned flush against the text margin.
- **Tab Stops implementation**:
  - Center tab at column midpoint (e.g. `4819` dxa for A4 single-column).
  - Right tab at column right edge (e.g. `9638` dxa).
  - Paragraph content: `\t` + `[OMML element]` + `\t(N)`.
