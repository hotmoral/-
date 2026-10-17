from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import struct
import sys
from pathlib import Path

import numpy as np

VERSION = "P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_V1"
SELECTION_TOKEN = "P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_SELECTED"
CONTRACT_TOKEN = "P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_CONTRACT_FROZEN"
POSE_ID = "FPD1_FOREQUARTER_PIVOT_NECK_HEAD_YAW_LEFT_8DEG"

EXPECTED_FPD1_SHA256 = "157ca0408f27e67330d10e49dff8b91446c0d674d4c106ec548bfbe001b8f097"
EXPECTED_FPD1_GIT_BLOB_SHA1 = "b76d4034cc23555c382d2508aaaa31e7578797ec"
EXPECTED_FPD1_VERSION = "P1_C_FPD1_FINITE_POSE_DISCRIMINATOR_V1"
EXPECTED_V3125_SHA256 = "839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77"

CANONICAL_WEIGHTS_BYTES = 112_532
CANONICAL_PREFIX = b"MOBI_R11_WEIGHTS_V1\0"
CANONICAL_VERTEX_COUNT = 3125
CANONICAL_ROLE_COUNT = 30
CANONICAL_MAX_INFLUENCES = 4
CANONICAL_SERIALIZED_SHA256 = "171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c"
CANONICAL_INDICES_SHA256 = "1907a206446b8da3497cb1e6adba4f59120f3af41bd5b003fabe513db64f871b"
CANONICAL_WEIGHT_FLOATS_SHA256 = "aa3569c6d2c3350bf21493d8c4fc8acc8d15db366cdcf51c8c81c7cdafa57411"
CANONICAL_SOURCE_ARTIFACT_ID = 12088123879
CANONICAL_SOURCE_ARTIFACT_DIGEST = "sha256:a395cf71206d3459c9ed052c37ff51ad1c0be097bc66fb5ebb02f7e208b97c84"
CANONICAL_SOURCE_MEMBER = "neutral_stage1_regression/weights.bin"


def stable_json(obj) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, separators=(",", ": ")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def load_fpd1(geometry_dir: Path):
    path = geometry_dir / "p1_c_fpd1_finite_pose_discriminator_v1.py"
    if not path.is_file():
        raise RuntimeError("frozen FPD1 evaluator missing")
    if sha256_file(path) != EXPECTED_FPD1_SHA256:
        raise RuntimeError("FPD1 evaluator SHA drift")
    if git_blob_sha1(path) != EXPECTED_FPD1_GIT_BLOB_SHA1:
        raise RuntimeError("FPD1 evaluator blob drift")
    spec = importlib.util.spec_from_file_location("mobi_fpd1_frozen_for_canonical_replay", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen FPD1 evaluator")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if getattr(mod, "VERSION", None) != EXPECTED_FPD1_VERSION:
        raise RuntimeError("FPD1 evaluator version drift")
    if getattr(mod, "POSE_ID", None) != POSE_ID:
        raise RuntimeError("FPD1 pose identity drift")
    return mod


def parse_canonical_weights_bytes(data: bytes) -> tuple[np.ndarray, np.ndarray, dict]:
    if len(data) != CANONICAL_WEIGHTS_BYTES:
        raise RuntimeError(f"canonical weights byte length drift: {len(data)}")
    serialized_sha = sha256_bytes(data)
    if serialized_sha != CANONICAL_SERIALIZED_SHA256:
        raise RuntimeError(f"canonical weights SHA drift: {serialized_sha}")
    if not data.startswith(CANONICAL_PREFIX):
        raise RuntimeError("canonical weights prefix drift")
    off = len(CANONICAL_PREFIX)
    vertex_count, role_count = struct.unpack("<QI", data[off:off + 12])
    if (vertex_count, role_count) != (CANONICAL_VERTEX_COUNT, CANONICAL_ROLE_COUNT):
        raise RuntimeError(f"canonical weights header drift: {(vertex_count, role_count)}")
    off += 12
    index_bytes_len = CANONICAL_VERTEX_COUNT * CANONICAL_MAX_INFLUENCES
    weight_bytes_len = index_bytes_len * 8
    index_bytes = data[off:off + index_bytes_len]
    weight_bytes = data[off + index_bytes_len:off + index_bytes_len + weight_bytes_len]
    if len(index_bytes) != index_bytes_len or len(weight_bytes) != weight_bytes_len:
        raise RuntimeError("canonical weights payload truncation")
    if sha256_bytes(index_bytes) != CANONICAL_INDICES_SHA256:
        raise RuntimeError("canonical top-4 indices SHA drift")
    if sha256_bytes(weight_bytes) != CANONICAL_WEIGHT_FLOATS_SHA256:
        raise RuntimeError("canonical float64 weights SHA drift")
    indices = np.frombuffer(index_bytes, dtype=np.uint8).copy().reshape(CANONICAL_VERTEX_COUNT, CANONICAL_MAX_INFLUENCES)
    weights = np.frombuffer(weight_bytes, dtype="<f8").copy().reshape(CANONICAL_VERTEX_COUNT, CANONICAL_MAX_INFLUENCES)
    if not np.isfinite(weights).all() or (weights < 0.0).any():
        raise RuntimeError("canonical weights contain invalid numeric values")
    meta = {
        "bytes": len(data),
        "prefixAscii": "MOBI_R11_WEIGHTS_V1\\0",
        "vertexCount": int(vertex_count),
        "roleCount": int(role_count),
        "maxInfluences": CANONICAL_MAX_INFLUENCES,
        "serializedSha256": serialized_sha,
        "indicesSha256": sha256_bytes(index_bytes),
        "weightFloatsSha256": sha256_bytes(weight_bytes),
        "sourceArtifactId": CANONICAL_SOURCE_ARTIFACT_ID,
        "sourceArtifactDigest": CANONICAL_SOURCE_ARTIFACT_DIGEST,
        "sourceMember": CANONICAL_SOURCE_MEMBER,
    }
    return indices, weights, meta


def load_canonical_weights(path: Path) -> tuple[np.ndarray, np.ndarray, dict]:
    if not path.is_file():
        raise RuntimeError("canonical weights.bin missing")
    return parse_canonical_weights_bytes(path.read_bytes())


def ulp_drift_stats(canonical: np.ndarray, fresh: np.ndarray) -> dict:
    a = np.asarray(canonical, dtype="<f8", order="C")
    b = np.asarray(fresh, dtype="<f8", order="C")
    if a.shape != b.shape:
        raise RuntimeError("weight drift comparison shape mismatch")
    if not np.isfinite(a).all() or not np.isfinite(b).all() or (a < 0).any() or (b < 0).any():
        raise RuntimeError("weight drift comparison requires finite nonnegative floats")
    au = a.view(np.uint64)
    bu = b.view(np.uint64)
    ulp = np.maximum(au, bu) - np.minimum(au, bu)
    bitdiff = ulp > 0
    diff = b - a
    changed = ulp[bitdiff]
    return {
        "bitwiseDifferentSlots": int(np.count_nonzero(bitdiff)),
        "slots": int(a.size),
        "verticesWithAnyDifference": int(np.count_nonzero(np.any(bitdiff, axis=1))) if a.ndim == 2 else None,
        "maxAbsoluteDifference": float(np.max(np.abs(diff))) if a.size else 0.0,
        "maxRelativeDifference": float(np.max(np.abs(diff) / np.maximum(np.abs(a), 1e-300))) if a.size else 0.0,
        "maxUlp": int(ulp.max()) if a.size else 0,
        "medianChangedUlp": float(np.median(changed)) if changed.size else 0.0,
    }


def reconstruct_canonical_replay_state(source_glb: Path, geometry_dir: Path, canonical_weights_bin: Path) -> dict:
    fpd1 = load_fpd1(geometry_dir)
    fresh = fpd1.reconstruct_frozen_state(source_glb, geometry_dir)
    if fresh["identity"].get("meshArraySha256") != EXPECTED_V3125_SHA256:
        raise RuntimeError("canonical replay V3125 identity drift")

    canonical_indices, canonical_weights, canonical_meta = load_canonical_weights(canonical_weights_bin)
    fresh_indices = np.asarray(fresh["indices"], dtype=np.uint8, order="C")
    if not np.array_equal(canonical_indices, fresh_indices):
        raise RuntimeError("fresh top-4 indices differ from canonical frozen indices")

    r11 = fresh["r11"]
    fresh_serial = r11.serialize_weights(fresh_indices, fresh["weights"])
    canonical_serial = r11.serialize_weights(canonical_indices, canonical_weights)
    if sha256_bytes(canonical_serial) != CANONICAL_SERIALIZED_SHA256:
        raise RuntimeError("R11 serializer does not reproduce canonical weight bytes")

    state = dict(fresh)
    state["indices"] = canonical_indices
    state["weights"] = canonical_weights
    canonical_audit = r11.weight_audit(canonical_indices, canonical_weights, state["domains"], state["interfaces"])
    if canonical_audit.get("domainBleedCount") != 0 or canonical_audit.get("unweightedVertexCount") != 0:
        raise RuntimeError("canonical replay weight audit failed")

    support = fpd1.support_isolation_report(state)
    if support.get("positiveSupportUnionCount") != 626:
        raise RuntimeError("canonical replay selected support drift")
    if support.get("positiveSupportDomainCounts") != {
        "CORE": 612, "FORE_L": 10, "FORE_R": 4, "HIND_L": 0, "HIND_R": 0, "TAIL": 0
    }:
        raise RuntimeError("canonical replay support-domain drift")
    for role, row in support["pawAnchors"].items():
        if row["selectedRoleWeight"] != 0.0:
            raise RuntimeError(f"canonical replay paw isolation fail {role}")

    rest = r11.rest_lbs(state["vertices"], state["controls"], canonical_indices, canonical_weights)
    rest_delta = np.linalg.norm(rest - state["vertices"], axis=1)
    h = float(r11.body_metrics(state["vertices"])["height"])
    rest_max = float(rest_delta.max() / h)
    rest_rms = float(math.sqrt(float(np.mean(rest_delta * rest_delta))) / h)
    if rest_max > r11.REST_MAX_NORMALIZED or rest_rms > r11.REST_RMS_NORMALIZED:
        raise RuntimeError("canonical replay neutral rest regression")

    state["canonicalReplay"] = {
        "selectionToken": SELECTION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "canonicalWeightIdentity": canonical_meta,
        "freshIndicesByteIdenticalToCanonical": True,
        "freshSerializedWeightsSha256": sha256_bytes(fresh_serial),
        "freshVsCanonicalFloatDrift": ulp_drift_stats(canonical_weights, fresh["weights"]),
        "canonicalWeightAudit": canonical_audit,
        "canonicalSupportIsolation": support,
        "canonicalRest": {"maxNormalized": rest_max, "rmsNormalized": rest_rms},
    }
    return state


def pre_evidence_audit(source_glb: Path, geometry_dir: Path, canonical_weights_bin: Path, out_file: Path) -> dict:
    state = reconstruct_canonical_replay_state(source_glb, geometry_dir, canonical_weights_bin)
    fpd1 = state["dar1"] and load_fpd1(geometry_dir)
    report = {
        "version": VERSION,
        "selectionToken": SELECTION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "poseId": POSE_ID,
        "actualFinitePoseEvidenceExecuted": False,
        "deformedV3125Produced": False,
        "rasterEvidenceExecuted": False,
        "perceptualReviewExecuted": False,
        "identity": state["identity"],
        "frame": state["frame"],
        "pose": fpd1.validate_pose_contract(state["r11"].ROLE_ORDER),
        "controlCount": len(state["controls"]),
        "canonicalReplay": state["canonicalReplay"],
    }
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(stable_json(report))
    return report


def run_canonical_replay_evidence(source_glb: Path, geometry_dir: Path, canonical_weights_bin: Path, out: Path) -> dict:
    state = reconstruct_canonical_replay_state(source_glb, geometry_dir, canonical_weights_bin)
    fpd1 = load_fpd1(geometry_dir)
    r11 = state["r11"]
    v = state["vertices"]
    f = state["faces"]
    controls = fpd1.control_map(state["controls"])
    indices = state["indices"]
    weights = state["weights"]
    support = state["canonicalReplay"]["canonicalSupportIsolation"]

    role_index = {role: int(r11.ROLE_INDEX[role]) for role in r11.ROLE_ORDER}
    selected_idx = np.asarray([role_index[r] for r in fpd1.SELECTED_ROLES], dtype=indices.dtype)
    selected_slots = np.isin(indices, selected_idx)
    selected_union = np.any(selected_slots & (weights > 0.0), axis=1)

    bind_before = fpd1.array_bytes_f64(v)
    canonical_serial_before = r11.serialize_weights(indices, weights)
    deformed = fpd1.finite_weighted_evaluate(v, indices, weights, r11.ROLE_ORDER, controls[fpd1.PIVOT_ROLE])
    if fpd1.array_bytes_f64(v) != bind_before:
        raise RuntimeError("canonical replay evaluator mutated bind vertices")
    if r11.serialize_weights(indices, weights) != canonical_serial_before:
        raise RuntimeError("canonical replay evaluator mutated canonical weights")

    paw_report = {}
    for role, index in fpd1.EXPECTED_PAW_VERTEX_INDEX.items():
        before = np.asarray(v[index], dtype=np.float64)
        after = np.asarray(deformed[index], dtype=np.float64)
        if not np.array_equal(before, after):
            raise RuntimeError(f"canonical replay moved frozen paw anchor {role}")
        paw_report[role] = {
            "surfaceBindIndex": int(index),
            "beforeR10": before.tolist(),
            "afterR10": after.tolist(),
            "exactByteNumericIdentity": True,
            "displacement": 0.0,
        }

    out.mkdir(parents=True, exist_ok=True)
    pose = fpd1.validate_pose_contract(r11.ROLE_ORDER)
    (out / "pose_parameters.json").write_bytes(stable_json(pose))
    (out / "canonical_weight_replay.json").write_bytes(stable_json(state["canonicalReplay"]))
    (out / "support_isolation.json").write_bytes(stable_json(support))
    (out / "paw_anchor_report.json").write_bytes(stable_json(paw_report))
    (out / "deformed_vertices.f64le.bin").write_bytes(fpd1.array_bytes_f64(deformed))
    (out / "faces.i64le.bin").write_bytes(fpd1.array_bytes_i64(f))

    health = fpd1.geometry_health(v, deformed, f, state["domains"], selected_union)
    (out / "geometry_health.json").write_bytes(stable_json(health))
    stage_d = fpd1.load_stage_d(geometry_dir, r11)
    visual = fpd1.write_visual_evidence(stage_d, v, deformed, f, out)
    (out / "visual_evidence.json").write_bytes(stable_json(visual))

    summary = {
        "version": VERSION,
        "selectionToken": SELECTION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "poseId": POSE_ID,
        "actualFinitePoseEvidenceExecuted": True,
        "deformedV3125Produced": True,
        "rasterEvidenceExecuted": True,
        "perceptualReviewExecuted": False,
        "identity": state["identity"],
        "canonicalWeightSerializedSha256": CANONICAL_SERIALIZED_SHA256,
        "canonicalIndicesSha256": CANONICAL_INDICES_SHA256,
        "bindVertexSha256": fpd1.sha256_bytes(bind_before),
        "deformedVertexSha256": fpd1.sha256_bytes(fpd1.array_bytes_f64(deformed)),
        "faceIndexSha256": fpd1.sha256_bytes(fpd1.array_bytes_i64(f)),
        "supportIsolation": support,
        "pawAnchorsExact": True,
        "geometryHealth": health,
        "directViewCount": visual["directViewCount"],
        "denseViewCount": visual["denseViewCount"],
        "productAcceptance": "REQUIRES_SEPARATE_DIRECT_UNSTYLED_HUMAN_REVIEW",
    }
    (out / "summary.json").write_bytes(stable_json(summary))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_glb", type=Path)
    ap.add_argument("--geometry-dir", type=Path, required=True)
    ap.add_argument("--canonical-weights-bin", type=Path, required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--pre-evidence-audit", action="store_true")
    mode.add_argument("--evaluate-pose-canonical-replay", action="store_true")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.pre_evidence_audit:
        result = pre_evidence_audit(a.source_glb, a.geometry_dir, a.canonical_weights_bin, a.out)
    else:
        result = run_canonical_replay_evidence(a.source_glb, a.geometry_dir, a.canonical_weights_bin, a.out)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
