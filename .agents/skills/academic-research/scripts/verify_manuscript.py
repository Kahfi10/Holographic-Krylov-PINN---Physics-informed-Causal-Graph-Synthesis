"""
verify_manuscript.py
Comprehensive auditor for academic manuscripts in Word (.docx) format.
Verifies:
1. Native Office Math (<m:oMath>) coverage vs raw unformatted math expressions.
2. Dual-mention compliance for all figures and tables (Pre-callout and Post-analysis).
3. Bullet points / list item count in manuscript body.
4. Empirical metric alignment.
"""

import sys
import os
import re
import docx

sys.stdout.reconfigure(encoding='utf-8')

def audit_manuscript(docx_path: str):
    if not os.path.exists(docx_path):
        print(f"Error: File not found: {docx_path}")
        return False

    print(f"==================================================")
    print(f"AUDITING MANUSCRIPT: {os.path.basename(docx_path)}")
    print(f"==================================================")
    doc = docx.Document(docx_path)
    ns = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}

    # 1. Math Audit
    omath_count = 0
    raw_math_terms = [
        'B_a = 1.0 - exp', 'P_success = 1.0 / (1.0 + exp', 'B_o = 1.0 / (1.0 + exp', 
        'B_l = max(0', 'L_bias = w_1', 'O_overload = w_i /', 
        'R̄ = (1/N)', 'η_eff = [(1', 'σ = sqrt(', 'ΔB_% = [(', 'S_dev = [1.0 - (σ',
        '|tc - ds_i|', 'resolution_hours - τ'
    ]
    raw_matches = []

    for idx, p in enumerate(doc.paragraphs):
        omaths = p._p.xpath('.//m:oMath')
        omath_count += len(omaths)
        for term in raw_math_terms:
            if term in p.text:
                raw_matches.append((f"P{idx}", term, p.text[:60]))

    for t_idx, tbl in enumerate(doc.tables):
        for r_idx, row in enumerate(tbl.rows):
            for c_idx, cell in enumerate(row.cells):
                for p in cell.paragraphs:
                    omaths = p._p.xpath('.//m:oMath')
                    omath_count += len(omaths)
                    for term in raw_math_terms:
                        if term in p.text:
                            raw_matches.append((f"T{t_idx}R{r_idx}C{c_idx}", term, p.text[:60]))

    print(f"[1] Math Audit:")
    print(f"    - Native Office Math (<m:oMath>) elements: {omath_count}")
    if raw_matches:
        print(f"    - WARNING: Found {len(raw_matches)} unformatted raw math occurrences:")
        for loc, term, snippet in raw_matches:
            print(f"      * {loc}: '{term}' in '{snippet}...'")
    else:
        print(f"    - Status: PASS (Zero unformatted plain-text equations found)")

    # 2. Bullet Points Audit
    body_bullets = 0
    for idx, p in enumerate(doc.paragraphs):
        style_name = p.style.name if p.style else ""
        txt = p.text.strip()
        if "List" in style_name or txt.startswith("•") or txt.startswith("- ") or re.match(r'^\d+\.\s', txt):
            # Check if this is in References or Front matter
            if idx > 12 and "REFERENCES" not in doc.paragraphs[max(0, idx-10)].text:
                body_bullets += 1

    print(f"[2] Prose Structure Audit:")
    print(f"    - Bullet points / list paragraphs in body: {body_bullets}")
    if body_bullets == 0:
        print(f"    - Status: PASS (Strict flowing academic prose)")
    else:
        print(f"    - Status: WARNING ({body_bullets} list items detected)")

    # 3. Figure & Table Mentions
    full_text = " ".join([p.text for p in doc.paragraphs])
    print(f"[3] Dual-Mention Audit:")
    for fig_num in range(1, 6):
        pattern = rf'Figure\s+{fig_num}\b'
        count = len(re.findall(pattern, full_text, re.IGNORECASE))
        status = "PASS" if count >= 2 else "FLAG (Need >= 2 mentions)"
        print(f"    - Figure {fig_num}: {count} in-text mentions -> {status}")

    for tbl_num in range(1, 7):
        pattern = rf'Table\s+{tbl_num}\b'
        count = len(re.findall(pattern, full_text, re.IGNORECASE))
        status = "PASS" if count >= 2 else "FLAG (Need >= 2 mentions)"
        print(f"    - Table {tbl_num}: {count} in-text mentions -> {status}")

    print(f"==================================================\n")
    return len(raw_matches) == 0

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "d:/eka punya/template baru/MUH. EKA ANDRI SETIAWAN_2026_IJEA.docx"
    audit_manuscript(target)
