from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "stage_b", HERE / "p1_c_3d_cat_stage_b_inspector_v1.py"
)
stage_b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stage_b)

VERSION = "P1_C_POST_R10_POSE_CORRESPONDENCE_AUDIT_V1"


def _hash_u32(values: list[int]) -> str:
    h = hashlib.sha256()
    for v in values:
        h.update(struct.pack("<I", int(v)))
    return h.hexdigest()


def _hash_f64_positions(values: list[tuple[float, ...]]) -> str:
    h = hashlib.sha256()
    for p in values:
        h.update(struct.pack("<ddd", float(p[0]), float(p[1]), float(p[2])))
    return h.hexdigest()


def _primitive_records(path: Path) -> list[dict]:
    data, _version, doc, bin_chunk, _chunks = stage_b.load_glb(path)
    records = []
    for mi, mesh in enumerate(doc.get("meshes", [])):
        for pi, prim in enumerate(mesh.get("primitives", [])):
            pos_idx = prim.get("attributes", {}).get("POSITION")
            if pos_idx is None:
                continue
            positions = stage_b.accessor_values(doc, bin_chunk, pos_idx)
            triangles, index_count, mode = stage_b.primitive_triangles(doc, bin_chunk, prim)
            if mode != 4 or not triangles:
                continue
            if "indices" in prim:
                indices = [int(x) for x in stage_b.accessor_values(doc, bin_chunk, prim["indices"])]
            else:
                indices = list(range(len(positions)))
            records.append({
                "meshIndex": mi,
                "meshName": mesh.get("name"),
                "primitiveIndex": pi,
                "positionAccessor": pos_idx,
                "vertexCount": len(positions),
                "triangleCount": len(triangles),
                "indexCount": index_count,
                "indexSha256": _hash_u32(indices),
                "positionSha256F64Canonical": _hash_f64_positions(positions),
                "positions": np.asarray([p[:3] for p in positions], dtype=np.float64),
                "indices": np.asarray(indices, dtype=np.int64),
            })
    if not records:
        raise ValueError(f"no indexed triangle primitives in {path}")
    return records


def _choose_body(records: list[dict]) -> dict:
    # Bounded audit rule: structural body candidate is the indexed triangle primitive
    # with the greatest triangle count. Facial/decorative parts are smaller separate meshes.
    return max(records, key=lambda r: (r["triangleCount"], r["vertexCount"], -r["meshIndex"], -r["primitiveIndex"]))


def _source_summary(path: Path) -> tuple[dict, dict]:
    inspection = stage_b.inspect(path)
    records = _primitive_records(path)
    body = _choose_body(records)
    return inspection, body


def _similarity_align(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, dict]:
    if source.shape != target.shape or source.ndim != 2 or source.shape[1] != 3:
        raise ValueError("source/target position shape mismatch")
    xs = source.mean(axis=0)
    yt = target.mean(axis=0)
    x = source - xs
    y = target - yt
    h = x.T @ y
    u, svals, vt = np.linalg.svd(h)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T
    denom = float(np.sum(x * x))
    scale = 1.0 if denom <= 1e-30 else float(np.sum(svals) / denom)
    aligned = scale * (x @ r.T) + yt
    return aligned, {
        "scale": scale,
        "rotationDeterminant": float(np.linalg.det(r)),
        "sourceCentroid": xs.tolist(),
        "targetCentroid": yt.tolist(),
    }


def _bbox_diag(points: np.ndarray) -> float:
    ext = points.max(axis=0) - points.min(axis=0)
    return float(np.linalg.norm(ext))


def compare_pair(name_a: str, body_a: dict, name_b: str, body_b: dict) -> dict:
    vertex_count_equal = body_a["vertexCount"] == body_b["vertexCount"]
    triangle_count_equal = body_a["triangleCount"] == body_b["triangleCount"]
    index_count_equal = body_a["indexCount"] == body_b["indexCount"]
    index_sequence_equal = (
        index_count_equal and body_a["indexSha256"] == body_b["indexSha256"]
    )
    exact_direct = vertex_count_equal and triangle_count_equal and index_sequence_equal

    if exact_direct:
        classification = "EXACT_VERTEX_TOPOLOGY_CORRESPONDENCE"
    elif vertex_count_equal and triangle_count_equal:
        classification = "COUNT_MATCH_BUT_CONNECTIVITY_DIFFERS"
    else:
        classification = "NO_DIRECT_CORRESPONDENCE"

    result = {
        "a": name_a,
        "b": name_b,
        "classification": classification,
        "vertexCountEqual": vertex_count_equal,
        "triangleCountEqual": triangle_count_equal,
        "indexCountEqual": index_count_equal,
        "indexSequenceExactlyEqual": index_sequence_equal,
        "directVertexCorrespondenceAccepted": exact_direct,
    }

    if exact_direct:
        aligned, align_meta = _similarity_align(body_a["positions"], body_b["positions"])
        displacement = np.linalg.norm(aligned - body_b["positions"], axis=1)
        diag = _bbox_diag(body_b["positions"])
        norm = displacement / diag if diag > 0 else displacement
        result["bestFitSimilarityAlignment"] = align_meta
        result["displacementNormalizedByTargetBBoxDiagonal"] = {
            "p50": float(np.percentile(norm, 50)),
            "p90": float(np.percentile(norm, 90)),
            "p95": float(np.percentile(norm, 95)),
            "p99": float(np.percentile(norm, 99)),
            "max": float(np.max(norm)),
            "rms": float(np.sqrt(np.mean(norm * norm))),
        }
    return result


def run(named_paths: dict[str, Path], out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    sources = {}
    bodies = {}
    for name, path in named_paths.items():
        inspection, body = _source_summary(path)
        bodies[name] = body
        sources[name] = {
            "fileName": path.name,
            "sha256": inspection["file"]["sha256"],
            "bytes": inspection["file"]["bytes"],
            "meshCount": inspection["structure"]["meshCount"],
            "primitiveCount": inspection["structure"]["primitiveCount"],
            "skinCount": inspection["structure"]["skinCount"],
            "animationCount": inspection["structure"]["animationCount"],
            "morphTargetSetCount": inspection["structure"]["morphTargetSetCount"],
            "structuralBodyCandidate": {
                k: body[k]
                for k in (
                    "meshIndex", "meshName", "primitiveIndex", "positionAccessor",
                    "vertexCount", "triangleCount", "indexCount", "indexSha256",
                    "positionSha256F64Canonical"
                )
            },
        }

    order = list(named_paths)
    pairs = []
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            pairs.append(compare_pair(order[i], bodies[order[i]], order[j], bodies[order[j]]))

    exact_pairs = [
        [p["a"], p["b"]] for p in pairs if p["directVertexCorrespondenceAccepted"]
    ]
    summary = {
        "version": VERSION,
        "sourceOrder": order,
        "sources": sources,
        "pairComparisons": pairs,
        "exactDirectCorrespondencePairs": exact_pairs,
        "auditConclusion": (
            "DIRECT_POSE_VERTEX_CORRESPONDENCE_AVAILABLE"
            if exact_pairs
            else "NO_DIRECT_POSE_VERTEX_CORRESPONDENCE_IN_TESTED_SOURCES"
        ),
        "interpretationFirewall": [
            "same provider or similar appearance does not imply vertex correspondence",
            "no retopology or manual matching is performed in this audit",
            "pose equations are not inferred unless exact direct correspondence is demonstrated",
        ],
    }
    (out / "pose_correspondence_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--standing", type=Path, required=True)
    ap.add_argument("--walking", type=Path, required=True)
    ap.add_argument("--sitting", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    summary = run(
        {"standing": args.standing, "walking": args.walking, "sitting": args.sitting},
        args.out,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
