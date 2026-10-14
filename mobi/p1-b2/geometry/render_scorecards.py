from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from candidates_v2 import solve_pose
from model import M0, M1, M2
from motions_v2 import sample_motion
from turn_2p5d import solve_turn_2p5d

CANDIDATES = ("BM_A", "BM_B", "BM_C")
MORPHOLOGIES = (M0, M1, M2)
SIZES = (48, 64, 80, 96, 112)
KEY_T = (0.0, 0.25, 0.50, 0.75, 1.0)

ROWS = (
    ("H1_NEUTRAL", lambda c, m, s, t: solve_pose(c, m, "H1_NEUTRAL_SUPPORT", s, 0.0)),
    ("H2_WALK", lambda c, m, s, t: sample_motion(c, m, "H2_SLOW_WALK", s, t)),
    ("H4_SIT_STAND", lambda c, m, s, t: sample_motion(c, m, "H4_SIT_TO_STAND", s, t)),
    ("H5_CROUCH", lambda c, m, s, t: solve_pose(c, m, "H5_CROUCH", s, 0.0)),
    ("H6_TURN_2P5D", lambda c, m, s, t: solve_turn_2p5d(c, _orientation_morph(m), s, t)),
    ("H7_NARROW", lambda c, m, s, t: sample_motion(c, m, "H7_NARROW_SHORT_STEP", s, t)),
)


def _orientation_morph(morphology):
    from orientation_v2 import M0_V2, M1_V2, M2_V2

    return {
        M0.id: M0_V2,
        M1.id: M1_V2,
        M2.id: M2_V2,
    }[morphology.id]


def _points(points):
    return " ".join(f"{p.x:.4f},{p.y:.4f}" for p in points)


def _shape_svg(shape):
    kind = shape["type"]
    role = escape(str(shape.get("role", "")))
    common = f'data-role="{role}" fill="black" stroke="black"'
    if kind == "ellipse":
        return (
            f'<ellipse {common} cx="{shape["cx"]:.4f}" cy="{shape["cy"]:.4f}" '
            f'rx="{shape["rx"]:.4f}" ry="{shape["ry"]:.4f}" stroke="none"/>'
        )
    if kind == "line":
        return (
            f'<line data-role="{role}" x1="{shape["p0"].x:.4f}" y1="{shape["p0"].y:.4f}" '
            f'x2="{shape["p1"].x:.4f}" y2="{shape["p1"].y:.4f}" '
            f'stroke="black" stroke-width="{shape["width"]:.4f}" stroke-linecap="round"/>'
        )
    if kind == "polyline":
        return (
            f'<polyline data-role="{role}" points="{_points(shape["points"])}" fill="none" '
            f'stroke="black" stroke-width="{shape["width"]:.4f}" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    if kind == "polygon":
        return f'<polygon {common} points="{_points(shape["points"])}" stroke="none"/>'
    raise ValueError(kind)


def _rect_svg(rect, stroke, dash=""):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<rect x="{rect.left:.4f}" y="{rect.top:.4f}" width="{rect.width:.4f}" height="{rect.height:.4f}" '
        f'fill="none" stroke="{stroke}" stroke-width="0.8"{dash_attr}/>'
    )


def _state_group(state, mode):
    parts = []
    if mode == "QA_OVERLAY":
        ground_y = state.size_dp * 1.38
        parts.append(f'<line x1="0" y1="{ground_y:.4f}" x2="{state.size_dp * 3.1:.4f}" y2="{ground_y:.4f}" stroke="#777" stroke-width="0.6"/>')
    parts.extend(_shape_svg(shape) for shape in state.shapes)
    if mode == "QA_OVERLAY":
        parts.append(_rect_svg(state.visual_bounds, "#555", "2,2"))
        parts.append(_rect_svg(state.window_bounds, "#999", "4,2"))
        for name, point in state.anchors.items():
            r = 1.0 if "PAW" in name else 0.8
            parts.append(f'<circle cx="{point.x:.4f}" cy="{point.y:.4f}" r="{r:.4f}" fill="#444"/>')
    return "".join(parts)


def render_sheet(candidate, morphology, size_dp, mode):
    cell_w = size_dp * 3.15
    cell_h = size_dp * 1.82
    left_label = max(72.0, size_dp * 0.72)
    top_label = 24.0
    width = left_label + cell_w * len(KEY_T)
    height = top_label + cell_h * len(ROWS)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="8" y="16" font-family="sans-serif" font-size="11">{escape(candidate)} | {escape(morphology.id)} | S{size_dp} | {mode}</text>',
    ]

    for col, t in enumerate(KEY_T):
        x = left_label + col * cell_w
        parts.append(f'<text x="{x + 4:.4f}" y="16" font-family="sans-serif" font-size="9">t={t:.2f}</text>')

    for row_index, (row_name, solver) in enumerate(ROWS):
        y0 = top_label + row_index * cell_h
        parts.append(
            f'<text x="5" y="{y0 + 15:.4f}" font-family="sans-serif" font-size="9">{escape(row_name)}</text>'
        )
        for col, t in enumerate(KEY_T):
            state = solver(candidate, morphology, size_dp, t)
            errors = state.validate()
            if errors:
                raise RuntimeError((candidate, morphology.id, size_dp, row_name, t, errors))
            x0 = left_label + col * cell_w
            parts.append(f'<g transform="translate({x0:.4f},{y0:.4f})">')
            parts.append(_state_group(state, mode))
            parts.append('</g>')

    parts.append('</svg>')
    return "".join(parts)


def render_all(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for candidate in CANDIDATES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for mode in ("SILHOUETTE", "QA_OVERLAY"):
                    filename = f'{candidate}_{morphology.id}_S{size_dp}_{mode}.svg'
                    text = render_sheet(candidate, morphology, size_dp, mode)
                    (output_dir / filename).write_text(text, encoding="utf-8")
                    manifest.append(filename)
    (output_dir / "MANIFEST.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    args = parser.parse_args()
    files = render_all(Path(args.output_dir))
    print(f"generated={len(files)}")
