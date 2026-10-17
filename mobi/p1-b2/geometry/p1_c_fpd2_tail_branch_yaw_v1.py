from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

VERSION = "P1_C_FPD2_TAIL_BRANCH_YAW_V1"
DECISION_TOKEN = "P1_C_POST_FPD1_TAIL_BRANCH_YAW_SELECTED"
CONTRACT_TOKEN = "P1_C_FPD2_TAIL_BRANCH_YAW_CONTRACT_FROZEN"
PREFLIGHT_TOKEN = "P1_C_FPD2_TAIL_BRANCH_YAW_PREFLIGHT_PASS"
POSE_ID = "FPD2_TAIL_ROOT_PIVOT_FULL_TAIL_YAW_RIGHT_8DEG"

EXPECTED_REPLAY_SHA256 = "76c7fad97ad7820b59b4935b4206fb67e74c866a12d0097bd7b11e70bbddeb41"
EXPECTED_REPLAY_GIT_BLOB_SHA1 = "d91b434172ee30cd233b5647ba52295a89e1a925"
EXPECTED_REPLAY_VERSION = "P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_V1"
EXPECTED_V3125_SHA256 = "839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77"

CANONICAL_WEIGHTS_BYTES = 112_532
CANONICAL_SERIALIZED_SHA256 = "171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c"
CANONICAL_INDICES_SHA256 = "1907a206446b8da3497cb1e6adba4f59120f3af41bd5b003fabe513db64f871b"
CANONICAL_WEIGHT_FLOATS_SHA256 = "aa3569c6d2c3350bf21493d8c4fc8acc8d15db366cdcf51c8c81c7cdafa57411"

PIVOT_ROLE = "TAIL_ROOT_CTRL"
SELECTED_ROLES = (
    "TAIL_ROOT_CTRL",
    "TAIL_1_CTRL",
    "TAIL_2_CTRL",
    "TAIL_3_CTRL",
    "TAIL_4_CTRL",
    "TAIL_TIP_CTRL",
)
AXIS_R10 = np.asarray([0.0, 1.0, 0.0], dtype=np.float64)
ANGLE_DEG = 8.0
ANGLE_RAD = 0.13962634015954636

EXPECTED_COORDS = {
    "TAIL_ROOT_CTRL": np.asarray([0.0, 0.2925511774265033, -0.08581501204510761], dtype=np.float64),
    "TAIL_1_CTRL": np.asarray([0.0, 0.30161730034676437, -0.16988316452705254], dtype=np.float64),
    "TAIL_2_CTRL": np.asarray([0.00225761216498044, 0.34892587392237023, -0.22100673764892909], dtype=np.float64),
    "TAIL_3_CTRL": np.asarray([0.015602729462746837, 0.4259644026954308, -0.33538722077218913], dtype=np.float64),
    "TAIL_4_CTRL": np.asarray([0.021714148267661493, 0.5153225764802215, -0.37810626667608743], dtype=np.float64),
    "TAIL_TIP_CTRL": np.asarray([0.019503411828433556, 0.5812016724873199, -0.3861675542029843], dtype=np.float64),
}
EXPECTED_TRANSFORMED_REFERENCE = {
    "TAIL_ROOT_CTRL": np.asarray([0.0, 0.2925511774265033, -0.08581501204510761], dtype=np.float64),
    "TAIL_1_CTRL": np.asarray([-0.011700025472895899, 0.30161730034676437, -0.16906501904607507], dtype=np.float64),
    "TAIL_2_CTRL": np.asarray([-0.016579410437843455, 0.34892587392237023, -0.2200052599544097], dtype=np.float64),
    "TAIL_3_CTRL": np.asarray([-0.019282853429829133, 0.4259644026954308, -0.3351298814356142], dtype=np.float64),
    "TAIL_4_CTRL": np.asarray([-0.019176252621116288, 0.5153225764802215, -0.3782837336276957], dtype=np.float64),
    "TAIL_TIP_CTRL": np.asarray([-0.022487388708136092, 0.5812016724873199, -0.3859588942128736], dtype=np.float64),
}
EXPECTED_REFERENCE_DISPLACEMENT = {
    "TAIL_ROOT_CTRL": 0.0,
    "TAIL_1_CTRL": 0.011728595742647828,
    "TAIL_2_CTRL": 0.01886362579442028,
    "TAIL_3_CTRL": 0.03488653203299144,
    "TAIL_4_CTRL": 0.04089078599591688,
    "TAIL_TIP_CTRL": 0.041991318968251645,
}
EXPECTED_PITCH = 0.0039006823656867104
EXPECTED_SUPPORT_UNION_COUNT = 619
EXPECTED_SUPPORT_DOMAIN_COUNTS = {
    "CORE": 0,
    "FORE_L": 0,
    "FORE_R": 0,
    "HIND_L": 0,
    "HIND_R": 0,
    "TAIL": 619,
}
EXPECTED_SUPPORT_MASK_SHA256 = "72565b6b1a7db89aaa11c37097463ccbde45dd1540c524313dcdc9074e9b530e"
EXPECTED_MIXED_ROOT_INTERFACE_COUNT = 19
EXPECTED_MIXED_SELECTED_MIN = 0.2606796033855258
EXPECTED_MIXED_SELECTED_MAX = 0.7507989280093238
EXPECTED_PAW_VERTEX_INDEX = {
    "FORE_L_PAW_CTRL": 1338,
    "FORE_R_PAW_CTRL": 146,
    "HIND_L_PAW_CTRL": 2277,
    "HIND_R_PAW_CTRL": 826,
}
DIRECT_VIEWS = (-90.0, -67.5, -45.0, -22.5, 0.0, 22.5, 45.0, 67.5, 90.0)
DENSE_VIEWS = tuple(float(x) for x in np.arange(-90.0, 90.0 + 1e-9, 2.5))
IDENTITY_ATOL = 1e-15


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


def load_replay(geometry_dir: Path):
    path = geometry_dir / "p1_c_fpd1_canonical_weight_replay_v1.py"
    if not path.is_file():
        raise RuntimeError("frozen canonical-weight replay adapter missing")
    if sha256_file(path) != EXPECTED_REPLAY_SHA256:
        raise RuntimeError("canonical replay adapter SHA drift")
    if git_blob_sha1(path) != EXPECTED_REPLAY_GIT_BLOB_SHA1:
        raise RuntimeError("canonical replay adapter blob drift")
    spec = importlib.util.spec_from_file_location("mobi_fpd1_replay_frozen_for_fpd2", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen canonical replay adapter")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if getattr(mod, "VERSION", None) != EXPECTED_REPLAY_VERSION:
        raise RuntimeError("canonical replay adapter version drift")
    if mod.CANONICAL_WEIGHTS_BYTES != CANONICAL_WEIGHTS_BYTES:
        raise RuntimeError("canonical weight byte-count authority drift")
    if mod.CANONICAL_SERIALIZED_SHA256 != CANONICAL_SERIALIZED_SHA256:
        raise RuntimeError("canonical serialized weight authority drift")
    if mod.CANONICAL_INDICES_SHA256 != CANONICAL_INDICES_SHA256:
        raise RuntimeError("canonical index authority drift")
    if mod.CANONICAL_WEIGHT_FLOATS_SHA256 != CANONICAL_WEIGHT_FLOATS_SHA256:
        raise RuntimeError("canonical float64 weight authority drift")
    return mod


def rotation_matrix() -> np.ndarray:
    c = math.cos(ANGLE_RAD)
    s = math.sin(ANGLE_RAD)
    return np.asarray([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]], dtype=np.float64)


def rigid_transform(points: np.ndarray, pivot: np.ndarray) -> np.ndarray:
    p = np.asarray(points, dtype=np.float64)
    q = np.asarray(pivot, dtype=np.float64)
    return q + (p - q) @ rotation_matrix().T


def validate_pose_contract(role_order) -> dict:
    roles = tuple(role_order)
    if len(roles) != 30:
        raise RuntimeError(f"FPD2 role count drift: {len(roles)}")
    if PIVOT_ROLE not in roles:
        raise RuntimeError("FPD2 pivot role missing")
    if tuple(r for r in roles if r in SELECTED_ROLES) != SELECTED_ROLES:
        raise RuntimeError("FPD2 selected role ordering drift")
    if len(set(SELECTED_ROLES)) != 6:
        raise RuntimeError("FPD2 selected-role set invalid")
    if not np.array_equal(AXIS_R10, np.asarray([0.0, 1.0, 0.0], dtype=np.float64)):
        raise RuntimeError("FPD2 axis drift")
    if ANGLE_DEG != 8.0 or ANGLE_RAD != 0.13962634015954636:
        raise RuntimeError("FPD2 angle drift")
    return {
        "poseId": POSE_ID,
        "frame": "R10",
        "pivotRole": PIVOT_ROLE,
        "pivotR10": EXPECTED_COORDS[PIVOT_ROLE].tolist(),
        "axisR10": AXIS_R10.tolist(),
        "angleDeg": ANGLE_DEG,
        "angleRad": ANGLE_RAD,
        "rightHanded": True,
        "anatomicalMeaning": "FULL_TAIL_YAW_TOWARD_ANATOMICAL_RIGHT",
        "selectedRoles": list(SELECTED_ROLES),
        "identityRoleCount": 24,
        "bodyRootTranslationR10": [0.0, 0.0, 0.0],
        "ikApplied": False,
        "rootCompensationApplied": False,
    }


def finite_weighted_evaluate(
    bind_vertices: np.ndarray,
    indices: np.ndarray,
    weights: np.ndarray,
    role_order,
    pivot: np.ndarray,
) -> np.ndarray:
    """Exact bounded FPD2 discriminator evaluator using canonical top-4 weights.

    All six tail roles share the same rigid transform. Grouping equal transforms is
    algebraically identical to slot-wise LBS. Vertices with zero selected-tail
    weight are copied bit-for-bit from bind state; no smoothing or correction is
    applied.
    """
    v = np.asarray(bind_vertices, dtype=np.float64, order="C")
    idx = np.asarray(indices)
    w = np.asarray(weights, dtype=np.float64, order="C")
    if v.ndim != 2 or v.shape[1] != 3:
        raise RuntimeError("FPD2 bind vertex shape drift")
    if idx.shape != w.shape or idx.ndim != 2 or idx.shape != (v.shape[0], 4):
        raise RuntimeError("FPD2 top-4 array shape drift")
    if not np.isfinite(v).all() or not np.isfinite(w).all() or (w < 0.0).any():
        raise RuntimeError("FPD2 invalid numeric input")
    contract = validate_pose_contract(role_order)
    role_index = {role: i for i, role in enumerate(tuple(role_order))}
    selected_indices = np.asarray([role_index[r] for r in SELECTED_ROLES], dtype=idx.dtype)
    selected_slot = np.isin(idx, selected_indices)
    selected_total = np.sum(np.where(selected_slot, w, 0.0), axis=1, dtype=np.float64)
    identity_total = np.sum(np.where(selected_slot, 0.0, w), axis=1, dtype=np.float64)
    total = selected_total + identity_total
    if not np.allclose(total, 1.0, rtol=0.0, atol=1e-12):
        raise RuntimeError("FPD2 weight normalization drift")
    rigid = rigid_transform(v, pivot)
    out = identity_total[:, None] * v + selected_total[:, None] * rigid
    zero_selected = selected_total == 0.0
    out[zero_selected] = v[zero_selected]
    if not np.isfinite(out).all():
        raise RuntimeError("FPD2 produced non-finite vertex")
    if contract["identityRoleCount"] != 24:
        raise RuntimeError("FPD2 identity-role count drift")
    return np.asarray(out, dtype=np.float64, order="C")


def control_map(controls) -> dict[str, np.ndarray]:
    return {c.role: np.asarray(c.position, dtype=np.float64) for c in controls}


def reference_control_report(state: dict) -> dict:
    controls = control_map(state["controls"])
    pitch = float(state["pitch"])
    if abs(pitch - EXPECTED_PITCH) > IDENTITY_ATOL:
        raise RuntimeError(f"FPD2 pitch drift: {pitch}")
    pivot = controls[PIVOT_ROLE]
    if not np.allclose(pivot, EXPECTED_COORDS[PIVOT_ROLE], rtol=0.0, atol=IDENTITY_ATOL):
        raise RuntimeError("FPD2 tail-root pivot coordinate drift")
    rows = {}
    for role in SELECTED_ROLES:
        bind = controls[role]
        expected_bind = EXPECTED_COORDS[role]
        if not np.allclose(bind, expected_bind, rtol=0.0, atol=IDENTITY_ATOL):
            raise RuntimeError(f"FPD2 bind control drift {role}: {bind.tolist()}")
        transformed = rigid_transform(bind[None, :], pivot)[0]
        expected_transformed = EXPECTED_TRANSFORMED_REFERENCE[role]
        if not np.allclose(transformed, expected_transformed, rtol=0.0, atol=IDENTITY_ATOL):
            raise RuntimeError(f"FPD2 transformed reference drift {role}: {transformed.tolist()}")
        displacement = float(np.linalg.norm(transformed - bind))
        if abs(displacement - EXPECTED_REFERENCE_DISPLACEMENT[role]) > IDENTITY_ATOL:
            raise RuntimeError(f"FPD2 reference displacement drift {role}: {displacement}")
        rows[role] = {
            "bindR10": bind.tolist(),
            "transformedR10": transformed.tolist(),
            "displacement": displacement,
            "displacementPitch": displacement / pitch,
        }
    return {
        "pitch": pitch,
        "pivotRole": PIVOT_ROLE,
        "pivotR10": pivot.tolist(),
        "roles": rows,
    }


def support_isolation_report(state: dict) -> dict:
    r11 = state["r11"]
    r12 = state["r12"]
    indices = np.asarray(state["indices"])
    weights = np.asarray(state["weights"], dtype=np.float64)
    domains = np.asarray(state["domains"])
    role_index = {role: int(r11.ROLE_INDEX[role]) for role in r11.ROLE_ORDER}
    selected_idx = np.asarray([role_index[r] for r in SELECTED_ROLES], dtype=indices.dtype)
    selected_slots = np.isin(indices, selected_idx)
    selected_total = np.sum(np.where(selected_slots, weights, 0.0), axis=1, dtype=np.float64)
    union = selected_total > 0.0
    union_count = int(np.count_nonzero(union))
    domain_counts = {d: int(np.count_nonzero(union & (domains == d))) for d in r11.DOMAIN_ORDER}
    if union_count != EXPECTED_SUPPORT_UNION_COUNT:
        raise RuntimeError(f"FPD2 support union drift: {union_count}")
    if domain_counts != EXPECTED_SUPPORT_DOMAIN_COUNTS:
        raise RuntimeError(f"FPD2 support-domain drift: {domain_counts}")
    tail_domain = domains == "TAIL"
    if int(np.count_nonzero(tail_domain)) != EXPECTED_SUPPORT_UNION_COUNT:
        raise RuntimeError("FPD2 TAIL-domain count drift")
    if not np.array_equal(union, tail_domain):
        raise RuntimeError("FPD2 selected support no longer equals TAIL domain")
    support_mask_sha = sha256_bytes(np.asarray(union, dtype=np.uint8, order="C").tobytes(order="C"))
    if support_mask_sha != EXPECTED_SUPPORT_MASK_SHA256:
        raise RuntimeError(f"FPD2 support mask SHA drift: {support_mask_sha}")

    tol = float(r11.FLOAT_SUM_TOLERANCE)
    mixed = union & (selected_total < (1.0 - tol))
    mixed_count = int(np.count_nonzero(mixed))
    if mixed_count != EXPECTED_MIXED_ROOT_INTERFACE_COUNT:
        raise RuntimeError(f"FPD2 mixed root-interface count drift: {mixed_count}")
    mixed_values = selected_total[mixed]
    mixed_min = float(mixed_values.min())
    mixed_max = float(mixed_values.max())
    if abs(mixed_min - EXPECTED_MIXED_SELECTED_MIN) > IDENTITY_ATOL:
        raise RuntimeError(f"FPD2 mixed selected min drift: {mixed_min}")
    if abs(mixed_max - EXPECTED_MIXED_SELECTED_MAX) > IDENTITY_ATOL:
        raise RuntimeError(f"FPD2 mixed selected max drift: {mixed_max}")
    full_tail = union & ~mixed
    if int(np.count_nonzero(full_tail)) != 600:
        raise RuntimeError("FPD2 full-tail selected count drift")
    if float(np.max(np.abs(selected_total[full_tail] - 1.0))) > tol:
        raise RuntimeError("FPD2 full-tail selected totals drift")

    paw = {}
    for role, expected_index in EXPECTED_PAW_VERTEX_INDEX.items():
        anchor = r12.PAW_ROLE_TO_ANCHOR[role]
        actual_index = int(state["aliases"][anchor]["surfaceBindIndex"])
        if actual_index != expected_index:
            raise RuntimeError(f"FPD2 paw alias index drift {role}: {actual_index}")
        selected_weight = float(np.sum(np.where(selected_slots[actual_index], weights[actual_index], 0.0), dtype=np.float64))
        if selected_weight != 0.0:
            raise RuntimeError(f"FPD2 selected-tail weight at paw anchor {role}: {selected_weight}")
        paw[role] = {
            "surfaceBindIndex": actual_index,
            "selectedTailRoleWeight": selected_weight,
        }

    return {
        "selectedRoles": list(SELECTED_ROLES),
        "positiveSupportUnionCount": union_count,
        "positiveSupportDomainCounts": domain_counts,
        "tailDomainCount": int(np.count_nonzero(tail_domain)),
        "selectedSupportEqualsTailDomain": True,
        "supportMaskSha256": support_mask_sha,
        "mixedRootInterfaceCount": mixed_count,
        "mixedSelectedTailWeightMin": mixed_min,
        "mixedSelectedTailWeightMax": mixed_max,
        "fullTailSelectedCount": int(np.count_nonzero(full_tail)),
        "pawAnchors": paw,
        "selectedTotal": selected_total,
        "selectedUnionMask": union,
    }


def reconstruct_fpd2_state(source_glb: Path, geometry_dir: Path, canonical_weights_bin: Path) -> dict:
    replay = load_replay(geometry_dir)
    state = replay.reconstruct_canonical_replay_state(source_glb, geometry_dir, canonical_weights_bin)
    if state["identity"].get("meshArraySha256") != EXPECTED_V3125_SHA256:
        raise RuntimeError("FPD2 V3125 identity drift")
    validate_pose_contract(state["r11"].ROLE_ORDER)
    refs = reference_control_report(state)
    support = support_isolation_report(state)
    state["fpd2ReferenceControls"] = refs
    state["fpd2SupportIsolation"] = support
    return state


def _jsonable_support(report: dict) -> dict:
    return {k: v for k, v in report.items() if k not in ("selectedTotal", "selectedUnionMask")}


def pre_evidence_audit(source_glb: Path, geometry_dir: Path, canonical_weights_bin: Path, out_file: Path) -> dict:
    state = reconstruct_fpd2_state(source_glb, geometry_dir, canonical_weights_bin)
    replay = load_replay(geometry_dir)
    canonical = state["canonicalReplay"]["canonicalWeightIdentity"]
    report = {
        "version": VERSION,
        "decisionToken": DECISION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "preflightToken": PREFLIGHT_TOKEN,
        "poseId": POSE_ID,
        "actualFinitePoseEvidenceExecuted": False,
        "deformedV3125Produced": False,
        "rasterEvidenceExecuted": False,
        "perceptualReviewExecuted": False,
        "identity": state["identity"],
        "frame": state["frame"],
        "pose": validate_pose_contract(state["r11"].ROLE_ORDER),
        "controlCount": len(state["controls"]),
        "canonicalWeightIdentity": canonical,
        "canonicalReplayNeutralRest": state["canonicalReplay"]["canonicalRest"],
        "freshIndicesByteIdenticalToCanonical": state["canonicalReplay"]["freshIndicesByteIdenticalToCanonical"],
        "referenceControls": state["fpd2ReferenceControls"],
        "supportIsolation": _jsonable_support(state["fpd2SupportIsolation"]),
        "inheritedReplayVersion": replay.VERSION,
    }
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(stable_json(report))
    return report


def run_fpd2_canonical_replay_evidence(source_glb: Path, geometry_dir: Path, canonical_weights_bin: Path, out: Path) -> dict:
    state = reconstruct_fpd2_state(source_glb, geometry_dir, canonical_weights_bin)
    replay = load_replay(geometry_dir)
    fpd1 = replay.load_fpd1(geometry_dir)
    r11 = state["r11"]
    v = np.asarray(state["vertices"], dtype=np.float64, order="C")
    f = np.asarray(state["faces"], dtype=np.int64, order="C")
    indices = state["indices"]
    weights = state["weights"]
    controls = control_map(state["controls"])
    support_full = state["fpd2SupportIsolation"]
    selected_union = support_full["selectedUnionMask"]

    bind_before = fpd1.array_bytes_f64(v)
    canonical_serial_before = r11.serialize_weights(indices, weights)
    deformed = finite_weighted_evaluate(v, indices, weights, r11.ROLE_ORDER, controls[PIVOT_ROLE])
    if fpd1.array_bytes_f64(v) != bind_before:
        raise RuntimeError("FPD2 evaluator mutated bind vertices")
    if r11.serialize_weights(indices, weights) != canonical_serial_before:
        raise RuntimeError("FPD2 evaluator mutated canonical weights")

    paw_report = {}
    for role, index in EXPECTED_PAW_VERTEX_INDEX.items():
        before = np.asarray(v[index], dtype=np.float64)
        after = np.asarray(deformed[index], dtype=np.float64)
        if not np.array_equal(before, after):
            raise RuntimeError(f"FPD2 moved frozen paw anchor {role}")
        paw_report[role] = {
            "surfaceBindIndex": int(index),
            "beforeR10": before.tolist(),
            "afterR10": after.tolist(),
            "exactByteNumericIdentity": True,
            "displacement": 0.0,
        }

    out.mkdir(parents=True, exist_ok=True)
    pose = validate_pose_contract(r11.ROLE_ORDER)
    support = _jsonable_support(support_full)
    (out / "pose_parameters.json").write_bytes(stable_json(pose))
    (out / "canonical_weight_identity.json").write_bytes(stable_json(state["canonicalReplay"]["canonicalWeightIdentity"]))
    (out / "support_isolation.json").write_bytes(stable_json(support))
    (out / "reference_controls.json").write_bytes(stable_json(state["fpd2ReferenceControls"]))
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
        "decisionToken": DECISION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "preflightToken": PREFLIGHT_TOKEN,
        "poseId": POSE_ID,
        "actualFinitePoseEvidenceExecuted": True,
        "deformedV3125Produced": True,
        "rasterEvidenceExecuted": True,
        "perceptualReviewExecuted": False,
        "identity": state["identity"],
        "pose": pose,
        "canonicalWeightIdentity": state["canonicalReplay"]["canonicalWeightIdentity"],
        "supportIsolation": support,
        "referenceControls": state["fpd2ReferenceControls"],
        "pawAnchors": paw_report,
        "geometryHealth": health,
        "visualEvidence": visual,
        "bindVertexSha256": sha256_bytes(fpd1.array_bytes_f64(v)),
        "deformedVertexSha256": sha256_bytes(fpd1.array_bytes_f64(deformed)),
        "faceIndexSha256": sha256_bytes(fpd1.array_bytes_i64(f)),
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
    mode.add_argument("--evaluate-fpd2-canonical-replay", action="store_true")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.pre_evidence_audit:
        result = pre_evidence_audit(a.source_glb, a.geometry_dir, a.canonical_weights_bin, a.out)
    else:
        result = run_fpd2_canonical_replay_evidence(a.source_glb, a.geometry_dir, a.canonical_weights_bin, a.out)
    print(json.dumps(result, indent=2, sort_keys=True, default=lambda x: "<ndarray>" if isinstance(x, np.ndarray) else x))


if __name__ == "__main__":
    main()
