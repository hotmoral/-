from __future__ import annotations

from xml.sax.saxutils import escape

import p1_fr5_core_mass_silhouette_v2 as v2
import run_p1_fr5_core_mass_silhouette_v1 as base


RUN_VERSION = "P1_FR5_CORE_MASS_SILHOUETTE_EVIDENCE_V2_FINAL_COEFFICIENT"


def _comparison_sheet_v2(samples, title: str):
    cell_w = 190.0
    cell_h = 125.0
    left = 82.0
    top = 30.0
    width = left + len(samples) * cell_w
    height = top + 2 * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
        f'<text x="6" y="{top + 16:.4f}" font-family="sans-serif" font-size="8">FR3 V5</text>',
        f'<text x="6" y="{top + cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR5 V2</text>',
    ]
    for col, (label, fixture, result) in enumerate(samples):
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 4:.4f}" y="17" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(base._normalized_control_group(
            fixture, result.control, x0 + cell_w * 0.50, top + cell_h * 0.52
        ))
        parts.append(base._normalized_fr5_group(
            fixture, result, x0 + cell_w * 0.50, top + cell_h * 1.52
        ))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    # Reuse the already-validated V1 matrix/evidence harness. Only the candidate
    # geometry module and display label/version are replaced for final V2.
    base.fr5 = v2
    base.RUN_VERSION = RUN_VERSION
    base._comparison_sheet = _comparison_sheet_v2
    base.main()


if __name__ == "__main__":
    main()
