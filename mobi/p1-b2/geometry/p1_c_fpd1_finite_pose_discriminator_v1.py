from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

VERSION = "P1_C_FPD1_FINITE_POSE_DISCRIMINATOR_V1"
DECISION_TOKEN = "P1_C_SMALL_FINITE_POSE_NECK_YAW_SELECTED"
CONTRACT_TOKEN = "P1_C_SMALL_FINITE_POSE_NECK_YAW_CONTRACT_FROZEN"
PREFLIGHT_TOKEN = "P1_C_SMALL_FINITE_POSE_NECK_YAW_PREFLIGHT_PASS"
POSE_ID = "FPD1_FOREQUARTER_PIVOT_NECK_HEAD_YAW_LEFT_8DEG"

EXPECTED_DAR1_SHA256 = "2ed9eac016c32a29a855eb26e0006c6e299a9b25d4a843b6cb4f398e6c356450"
EXPECTED_DAR1_GIT_BLOB_SHA1 = "d13d191499b6d734845051ba428323fdcf37dabd"
EXPECTED_DAR1_VERSION = "P1_C_DAR1_DIAGNOSTIC_AXIS_REVISION_V1"
EXPECTED_V3125_SHA256 = "839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77"
EXPECTED_STAGE_D_GIT_BLOB_SHA1 = "5c8820fb7270e7727ececb1bb37d3a24331b24ab"

PIVOT_ROLE = "FOREQUARTER_CTRL"
SELECTED_ROLES = ("NECK_BASE_CTRL", "HEAD_CTRL")
AXIS_R10 = np.asarray([0.0, 1.0, 0.0], dtype=np.float64)
ANGLE_DEG = 8.0
ANGLE_RAD = 0.13962634015954636

EXPECTED_COORDS = {
    "FOREQUARTER_CTRL": np.asarray([0.0, 0.3042532245235634, 0.11311978860491462], dtype=np.float64),
    "NECK_BASE_CTRL": np.asarray([0.0008915510202294848, 0.44389076654214477, 0.27701027738751116], dtype=np.float64),
    "HEAD_CTRL": np.asarray([0.019503411828433556, 0.4524791544196584, 0.27694844796375645], dtype=np.float64),
}
EXPECTED_TRANSFORMED_REFERENCE = {
    "NECK_BASE_CTRL": np.asarray([0.02369202204872201, 0.44389076654214477, 0.2752912264966191], dtype=np.float64),
    "HEAD_CTRL": np.asarray([0.04211414851431466, 0.4524791544196584, 0.2726397284092512], dtype=np.float64),
}
EXPECTED_REFERENCE_DISPLACEMENT = {
    "NECK_BASE_CTRL": 0.022865183469340536,
    "HEAD_CTRL": 0.023017612336591848,
}
EXPECTED_PITCH = 0.0039006823656867104
EXPECTED_SUPPORT_UNION_COUNT = 626
EXPECTED_SUPPORT_DOMAIN_COUNTS = {
    "CORE": 612,
    "FORE_L": 10,
    "FORE_R": 4,
    "HIND_L": 0,
    "HIND_R": 0,
    "TAIL": 0,
}
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def array_bytes_f64(a: np.ndarray) -> bytes:
    return np.asarray(a, dtype="<f8", order="C").tobytes(order="C")


def array_bytes_i64(a: np.ndarray) -> bytes:
    return np.asarray(a, dtype="<i8", order="C").tobytes(order="C")


def load_dar1(geometry_dir: Path):
    path = geometry_dir / "p1_c_dar1_diagnostic_axis_revision_v1.py"
    if not path.is_file():
        raise RuntimeError("frozen DAR1 adapter missing")
    if sha256_file(path) != EXPECTED_DAR1_SHA256:
        raise RuntimeError("DAR1 adapter SHA drift")
    if git_blob_sha1(path) != EXPECTED_DAR1_GIT_BLOB_SHA1:
        raise RuntimeError("DAR1 adapter blob drift")
    spec = importlib.util.spec_from_file_location("mobi_dar1_frozen_for_fpd1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen DAR1 adapter")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if getattr(mod, "VERSION", None) != EXPECTED_DAR1_VERSION:
        raise RuntimeError("DAR1 version drift")
    return mod


def load_stage_d(geometry_dir: Path, r11):
    path = geometry_dir / "p1_c_3d_cat_stage_d_projection_v1.py"
    if git_blob_sha1(path) != EXPECTED_STAGE_D_GIT_BLOB_SHA1:
        raise RuntimeError("Stage-D projector blob drift")
    return r11._load_module(path, "fpd1_frozen_stage_d")


def rotation_matrix() -> np.ndarray:
    c = math.cos(ANGLE_RAD)
    s = math.sin(ANGLE_RAD)
    return np.asarray([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]], dtype=np.float64)


def rigid_transform(points: np.ndarray, pivot: np.ndarray) -> np.ndarray:
    p = np.asarray(points, dtype=np.float64)
    pivot = np.asarray(pivot, dtype=np.float64)
    return pivot + (p - pivot) @ rotation_matrix().T


def validate_pose_contract(role_order) -> dict:
    roles = tuple(role_order)
    if len(roles) != 30:
        raise RuntimeError(f"FPD1 role count drift: {len(roles)}")
    if PIVOT_ROLE not in roles:
        raise RuntimeError("FPD1 pivot role missing")
    if any(r not in roles for r in SELECTED_ROLES):
        raise RuntimeError("FPD1 selected role missing")
    if len(set(SELECTED_ROLES)) != 2:
        raise RuntimeError("FPD1 selected-role set invalid")
    if not np.array_equal(AXIS_R10, np.asarray([0.0, 1.0, 0.0], dtype=np.float64)):
        raise RuntimeError("FPD1 axis drift")
    if ANGLE_DEG != 8.0 or ANGLE_RAD != 0.13962634015954636:
        raise RuntimeError("FPD1 angle drift")
    return {
        "poseId": POSE_ID,
        "frame": "R10",
        "pivotRole": PIVOT_ROLE,
        "axisR10": AXIS_R10.tolist(),
        "angleDeg": ANGLE_DEG,
        "angleRad": ANGLE_RAD,
        "rightHanded": True,
        "anatomicalMeaning": "NECK_HEAD_YAW_TOWARD_ANATOMICAL_LEFT",
        "selectedRoles": list(SELECTED_ROLES),
        "identityRoleCount": 28,
        "bodyRootTranslationR10": [0.0, 0.0, 0.0],
    }


def finite_weighted_evaluate(
    bind_vertices: np.ndarray,
    indices: np.ndarray,
    weights: np.ndarray,
    role_order,
    pivot: np.ndarray,
) -> np.ndarray:
    """Exact bounded FPD1 weighted evaluator.

    Both selected roles share the same rigid transform. Grouping equal transforms is
    algebraically identical to the frozen per-slot blend. Vertices with exactly zero
    selected-role weight are copied bit-for-bit from bind state; this is the exact
    identity branch implied by the contract, not a corrective post-process.
    """
    v = np.asarray(bind_vertices, dtype=np.float64, order="C")
    idx = np.asarray(indices)
    w = np.asarray(weights, dtype=np.float64, order="C")
    if v.ndim != 2 or v.shape[1] != 3:
        raise RuntimeError("FPD1 bind vertex shape drift")
    if idx.shape != w.shape or idx.ndim != 2 or idx.shape[0] != v.shape[0] or idx.shape[1] != 4:
        raise RuntimeError("FPD1 top-4 array shape drift")
    if not np.isfinite(v).all() or not np.isfinite(w).all():
        raise RuntimeError("FPD1 non-finite input")
    contract = validate_pose_contract(role_order)
    role_index = {role: i for i, role in enumerate(tuple(role_order))}
    selected_indices = np.asarray([role_index[r] for r in SELECTED_ROLES], dtype=idx.dtype)
    selected_slot = np.isin(idx, selected_indices)
    selected_total = np.sum(np.where(selected_slot, w, 0.0), axis=1, dtype=np.float64)
    identity_total = np.sum(np.where(selected_slot, 0.0, w), axis=1, dtype=np.float64)
    total = selected_total + identity_total
    if not np.allclose(total, 1.0, rtol=0.0, atol=1e-12):
        raise RuntimeError("FPD1 weight normalization drift")
    rigid = rigid_transform(v, pivot)
    out = identity_total[:, None] * v + selected_total[:, None] * rigid
    zero_selected = selected_total == 0.0
    out[zero_selected] = v[zero_selected]
    if not np.isfinite(out).all():
        raise RuntimeError("FPD1 produced non-finite vertex")
    if contract["identityRoleCount"] != 28:
        raise RuntimeError("FPD1 identity-role count drift")
    return np.asarray(out, dtype=np.float64, order="C")


def reconstruct_frozen_state(source_glb: Path, geometry_dir: Path) -> dict:
    dar1 = load_dar1(geometry_dir)
    r12 = dar1.load_r12(geometry_dir)
    r11 = r12.load_r11(geometry_dir)
    validate_pose_contract(r11.ROLE_ORDER)

    v, f, identity = r11.reproduce_v3125(source_glb, geometry_dir)
    if str(identity.get("meshArraySha256", "")) != EXPECTED_V3125_SHA256:
        raise RuntimeError("FPD1 V3125 identity drift")
    frame = r11.frame_sign_audit(v, geometry_dir)
    if frame.get("anatomicalLeftSign") != "+X_R10":
        raise RuntimeError("FPD1 frame/sign drift")

    skel, transform, pitch = r11.voxel_skeleton(v, f)
    raw_graph = r11.graph_from_skeleton(skel)
    graph, _snapped, nodes, paths = r11.derive_semantic_graph(v, raw_graph, transform, pitch)
    r11_controls, path_worlds = r11.make_controls(transform, nodes, paths)
    aliases = r12.derive_surface_terminal_aliases(v, r11)
    controls = r12.replace_paw_bind_controls(r11, r11_controls, aliases)
    r12_delta = r12.delta_audit(r11, r11_controls, controls, path_worlds, aliases)
    if r12_delta.get("changedRoleCount") != 4 or r12_delta.get("unchangedNonPawRoleCount") != 26:
        raise RuntimeError("FPD1 inherited R12 delta drift")

    domains, interfaces, domain_info, _polylines = r11.derive_domains(v, path_worlds, pitch)
    indices, weights = r11.build_weights(v, controls, domains, interfaces, pitch)
    weight_audit = r11.weight_audit(indices, weights, domains, interfaces)
    if weight_audit.get("domainBleedCount") != 0 or weight_audit.get("unweightedVertexCount") != 0:
        raise RuntimeError("FPD1 inherited weight audit drift")
    axis_audit = dar1.axis_isolation_audit(r11, controls)
    if axis_audit.get("changedDiagnosticAxisRoles") != ["TAIL_ROOT_CTRL"]:
        raise RuntimeError("FPD1 DAR1 isolation drift")

    rest = r11.rest_lbs(v, controls, indices, weights)
    rest_delta = np.linalg.norm(rest - v, axis=1)
    h = float(r11.body_metrics(v)["height"])
    rest_max = float(rest_delta.max() / h)
    rest_rms = float(math.sqrt(float(np.mean(rest_delta * rest_delta))) / h)
    if rest_max > r11.REST_MAX_NORMALIZED or rest_rms > r11.REST_RMS_NORMALIZED:
        raise RuntimeError("FPD1 neutral rest regression")

    return {
        "dar1": dar1,
        "r12": r12,
        "r11": r11,
        "vertices": np.asarray(v, dtype=np.float64, order="C"),
        "faces": np.asarray(f, dtype=np.int64, order="C"),
        "identity": identity,
        "frame": frame,
        "pitch": float(pitch),
        "controls": controls,
        "aliases": aliases,
        "domains": np.asarray(domains),
        "interfaces": np.asarray(interfaces),
        "domainInfo": domain_info,
        "indices": np.asarray(indices),
        "weights": np.asarray(weights, dtype=np.float64, order="C"),
        "weightAudit": weight_audit,
        "axisAudit": axis_audit,
        "restMaxNormalized": rest_max,
        "restRmsNormalized": rest_rms,
    }


def control_map(controls) -> dict:
    return {c.role: np.asarray(c.position, dtype=np.float64) for c in controls}


def support_isolation_report(state: dict) -> dict:
    r11 = state["r11"]
    r12 = state["r12"]
    indices = state["indices"]
    weights = state["weights"]
    domains = state["domains"]
    role_index = {role: int(r11.ROLE_INDEX[role]) for role in r11.ROLE_ORDER}
    selected_idx = np.asarray([role_index[r] for r in SELECTED_ROLES], dtype=indices.dtype)
    selected_slots = np.isin(indices, selected_idx)
    positive = selected_slots & (weights > 0.0)
    union = np.any(positive, axis=1)
    union_count = int(np.count_nonzero(union))
    domain_counts = {d: int(np.count_nonzero(union & (domains == d))) for d in r11.DOMAIN_ORDER}
    if union_count != EXPECTED_SUPPORT_UNION_COUNT:
        raise RuntimeError(f"FPD1 support union drift: {union_count}")
    if domain_counts != EXPECTED_SUPPORT_DOMAIN_COUNTS:
        raise RuntimeError(f"FPD1 support-domain drift: {domain_counts}")

    paw = {}
    for role, expected_index in EXPECTED_PAW_VERTEX_INDEX.items():
        anchor = r12.PAW_ROLE_TO_ANCHOR[role]
        actual_index = int(state["aliases"][anchor]["surfaceBindIndex"])
        if actual_index != expected_index:
            raise RuntimeError(f"FPD1 paw alias index drift {role}: {actual_index}")
        selected_weight = float(np.sum(np.where(selected_slots[actual_index], weights[actual_index], 0.0), dtype=np.float64))
        if selected_weight != 0.0:
            raise RuntimeError(f"FPD1 selected-role weight at paw anchor {role}: {selected_weight}")
        paw[role] = {
            "surfaceBindIndex": actual_index,
            "selectedRoleWeight": selected_weight,
            "selectedRolesAbsentFromTop4": True,
        }
    return {
        "selectedRoles": list(SELECTED_ROLES),
        "positiveSupportUnionCount": union_count,
        "positiveSupportDomainCounts": domain_counts,
        "noSelectedSupportInHindOrTail": all(domain_counts[x] == 0 for x in ("HIND_L", "HIND_R", "TAIL")),
        "pawAnchors": paw,
        "selectedSupportMaskSha256": sha256_bytes(np.asarray(union, dtype=np.uint8).tobytes()),
    }


def pre_evidence_audit(source_glb: Path, geometry_dir: Path, out_file: Path) -> dict:
    state = reconstruct_frozen_state(source_glb, geometry_dir)
    r11 = state["r11"]
    controls = control_map(state["controls"])
    for role, expected in EXPECTED_COORDS.items():
        if not np.array_equal(controls[role], expected):
            raise RuntimeError(f"FPD1 frozen control coordinate drift {role}: {controls[role].tolist()}")
    if not math.isclose(state["pitch"], EXPECTED_PITCH, rel_tol=0.0, abs_tol=IDENTITY_ATOL):
        raise RuntimeError(f"FPD1 pitch drift: {state['pitch']}")

    pivot = controls[PIVOT_ROLE]
    transformed_reference = {}
    for role in SELECTED_ROLES:
        transformed = rigid_transform(controls[role][None, :], pivot)[0]
        if not np.allclose(transformed, EXPECTED_TRANSFORMED_REFERENCE[role], rtol=0.0, atol=IDENTITY_ATOL):
            raise RuntimeError(f"FPD1 transformed reference drift {role}: {transformed.tolist()}")
        disp = float(np.linalg.norm(transformed - controls[role]))
        if not math.isclose(disp, EXPECTED_REFERENCE_DISPLACEMENT[role], rel_tol=0.0, abs_tol=IDENTITY_ATOL):
            raise RuntimeError(f"FPD1 reference displacement drift {role}: {disp}")
        transformed_reference[role] = {
            "bindR10": controls[role].tolist(),
            "expectedTransformedR10": transformed.tolist(),
            "displacement": disp,
            "displacementInPitch": disp / state["pitch"],
        }

    support = support_isolation_report(state)
    weight_bytes = r11.serialize_weights(state["indices"], state["weights"])
    report = {
        "version": VERSION,
        "decisionToken": DECISION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "preflightToken": PREFLIGHT_TOKEN,
        "pose": validate_pose_contract(r11.ROLE_ORDER),
        "actualFinitePoseEvidenceExecuted": False,
        "deformedV3125Produced": False,
        "rasterEvidenceExecuted": False,
        "perceptualReviewExecuted": False,
        "identity": state["identity"],
        "frame": state["frame"],
        "pitch": state["pitch"],
        "controlCount": len(state["controls"]),
        "frozenCoordinates": {k: v.tolist() for k, v in EXPECTED_COORDS.items()},
        "transformedReferenceOnly": transformed_reference,
        "supportIsolation": support,
        "weightSha256": sha256_bytes(weight_bytes),
        "bindVertexSha256": sha256_bytes(array_bytes_f64(state["vertices"])),
        "faceIndexSha256": sha256_bytes(array_bytes_i64(state["faces"])),
        "rest": {
            "maxNormalized": state["restMaxNormalized"],
            "rmsNormalized": state["restRmsNormalized"],
        },
        "dar1Isolation": {
            "changedDiagnosticAxisRoles": state["axisAudit"]["changedDiagnosticAxisRoles"],
            "allNonTailRootAxesExactInherited": state["axisAudit"]["allNonTailRootAxesExactInherited"],
        },
    }
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(stable_json(report))
    return report


def _distribution(x: np.ndarray) -> dict:
    a = np.asarray(x, dtype=np.float64)
    if a.size == 0:
        return {"count": 0}
    q = np.quantile(a, [0.0, 0.01, 0.05, 0.5, 0.95, 0.99, 1.0])
    return {
        "count": int(a.size),
        "min": float(q[0]),
        "p01": float(q[1]),
        "p05": float(q[2]),
        "median": float(q[3]),
        "p95": float(q[4]),
        "p99": float(q[5]),
        "max": float(q[6]),
        "mean": float(np.mean(a)),
        "rms": float(math.sqrt(float(np.mean(a * a)))),
    }


def geometry_health(bind: np.ndarray, deformed: np.ndarray, faces: np.ndarray, domains: np.ndarray, selected_union: np.ndarray) -> dict:
    if bind.shape != deformed.shape or bind.shape[1] != 3:
        raise RuntimeError("FPD1 deformed vertex shape drift")
    if not np.isfinite(deformed).all():
        raise RuntimeError("FPD1 deformed vertices contain NaN/Inf")
    displacement = np.linalg.norm(deformed - bind, axis=1)
    by_domain = {d: _distribution(displacement[domains == d]) for d in EXPECTED_SUPPORT_DOMAIN_COUNTS}

    tri = np.asarray(faces, dtype=np.int64)
    a0, b0, c0 = bind[tri[:, 0]], bind[tri[:, 1]], bind[tri[:, 2]]
    a1, b1, c1 = deformed[tri[:, 0]], deformed[tri[:, 1]], deformed[tri[:, 2]]
    n0 = np.cross(b0 - a0, c0 - a0)
    n1 = np.cross(b1 - a1, c1 - a1)
    len0 = np.linalg.norm(n0, axis=1)
    len1 = np.linalg.norm(n1, axis=1)
    area0 = 0.5 * len0
    area1 = 0.5 * len1
    valid0 = len0 > 0.0
    ratio = np.full(len(area0), np.nan, dtype=np.float64)
    ratio[valid0] = area1[valid0] / area0[valid0]
    both = (len0 > 0.0) & (len1 > 0.0)
    dots = np.sum(n0[both] * n1[both], axis=1) / (len0[both] * len1[both])
    dots = np.clip(dots, -1.0, 1.0)

    return {
        "finiteVertexCount": int(np.isfinite(deformed).all(axis=1).sum()),
        "vertexCount": int(len(bind)),
        "displacement": _distribution(displacement),
        "displacementByDomain": by_domain,
        "selectedSupportDisplacement": _distribution(displacement[selected_union]),
        "outsideSelectedSupportDisplacement": _distribution(displacement[~selected_union]),
        "triangleAreaRatio": _distribution(ratio[np.isfinite(ratio)]),
        "neutralExactZeroAreaFaceCount": int(np.count_nonzero(area0 == 0.0)),
        "deformedExactZeroAreaFaceCount": int(np.count_nonzero(area1 == 0.0)),
        "nonFiniteAreaFaceCount": int(np.count_nonzero(~np.isfinite(area1))),
        "faceNormalDot": _distribution(dots),
    }


def _yaw_name(deg: float) -> str:
    if deg == 0.0:
        return "p000"
    return ("p" if deg > 0 else "m") + f"{abs(deg):05.1f}".replace(".", "p")


def render_mask(stage_d, vertices: np.ndarray, faces: np.ndarray, deg: float) -> bytes:
    projected = [stage_d.project_point(tuple(map(float, p)), float(deg)) for p in vertices]
    triangles = [tuple(map(int, t)) for t in faces]
    return bytes(stage_d.rasterize(projected, triangles))


def write_visual_evidence(stage_d, bind: np.ndarray, deformed: np.ndarray, faces: np.ndarray, out: Path) -> dict:
    direct_dir = out / "direct_deformed_only"
    direct_dir.mkdir(parents=True, exist_ok=True)
    direct_rows = []
    direct_grays = []
    for deg in DIRECT_VIEWS:
        mask = render_mask(stage_d, deformed, faces, deg)
        gray = stage_d.mask_to_gray(mask)
        direct_grays.append(gray)
        name = _yaw_name(deg)
        native = direct_dir / f"FPD1_DEFORMED_{name}_96.png"
        enlarged = direct_dir / f"FPD1_DEFORMED_{name}_96_8X.png"
        native.write_bytes(stage_d.png_gray(stage_d.CANVAS, stage_d.CANVAS, gray))
        bw, bh, bgray = stage_d.upscale_nearest(gray, stage_d.CANVAS, stage_d.CANVAS, 8)
        enlarged.write_bytes(stage_d.png_gray(bw, bh, bgray))
        direct_rows.append({
            "yawDeg": deg,
            "maskSha256": sha256_bytes(mask),
            "metrics": stage_d.mask_metrics(mask),
            "nativePng": native.name,
            "enlargedPng": enlarged.name,
        })
    sw, sh, strip = stage_d.combine_horizontal(direct_grays, stage_d.CANVAS, stage_d.CANVAS)
    (direct_dir / "FPD1_DEFORMED_DIRECT_9VIEW_STRIP_96.png").write_bytes(stage_d.png_gray(sw, sh, strip))
    ew, eh, estrip = stage_d.upscale_nearest(strip, sw, sh, 8)
    (direct_dir / "FPD1_DEFORMED_DIRECT_9VIEW_STRIP_96_8X.png").write_bytes(stage_d.png_gray(ew, eh, estrip))

    dense = []
    for deg in DENSE_VIEWS:
        neutral_mask = render_mask(stage_d, bind, faces, deg)
        deformed_mask = render_mask(stage_d, deformed, faces, deg)
        xor_count = sum(1 for a, b in zip(neutral_mask, deformed_mask) if a != b)
        dense.append({
            "yawDeg": deg,
            "neutralMaskSha256": sha256_bytes(neutral_mask),
            "deformedMaskSha256": sha256_bytes(deformed_mask),
            "xorPixelCount": int(xor_count),
            "deformedMetrics": stage_d.mask_metrics(deformed_mask),
        })
    return {"directViewCount": len(direct_rows), "directViews": direct_rows, "denseViewCount": len(dense), "denseYaw": dense}


def run_finite_pose_evidence(source_glb: Path, geometry_dir: Path, out: Path) -> dict:
    state = reconstruct_frozen_state(source_glb, geometry_dir)
    r11 = state["r11"]
    v = state["vertices"]
    f = state["faces"]
    controls = control_map(state["controls"])
    support = support_isolation_report(state)
    role_index = {role: int(r11.ROLE_INDEX[role]) for role in r11.ROLE_ORDER}
    selected_idx = np.asarray([role_index[r] for r in SELECTED_ROLES], dtype=state["indices"].dtype)
    selected_slots = np.isin(state["indices"], selected_idx)
    selected_union = np.any(selected_slots & (state["weights"] > 0.0), axis=1)

    bind_before = array_bytes_f64(v)
    weights_before = r11.serialize_weights(state["indices"], state["weights"])
    deformed = finite_weighted_evaluate(v, state["indices"], state["weights"], r11.ROLE_ORDER, controls[PIVOT_ROLE])
    if array_bytes_f64(v) != bind_before:
        raise RuntimeError("FPD1 evaluator mutated bind vertices")
    if r11.serialize_weights(state["indices"], state["weights"]) != weights_before:
        raise RuntimeError("FPD1 evaluator mutated frozen weights")

    paw_report = {}
    for role, index in EXPECTED_PAW_VERTEX_INDEX.items():
        before = np.asarray(v[index], dtype=np.float64)
        after = np.asarray(deformed[index], dtype=np.float64)
        if not np.array_equal(before, after):
            raise RuntimeError(f"FPD1 moved frozen paw anchor {role}")
        paw_report[role] = {
            "surfaceBindIndex": index,
            "beforeR10": before.tolist(),
            "afterR10": after.tolist(),
            "exactByteNumericIdentity": True,
            "displacement": 0.0,
        }

    out.mkdir(parents=True, exist_ok=True)
    pose = validate_pose_contract(r11.ROLE_ORDER)
    (out / "pose_parameters.json").write_bytes(stable_json(pose))
    (out / "support_isolation.json").write_bytes(stable_json(support))
    (out / "paw_anchor_report.json").write_bytes(stable_json(paw_report))
    (out / "deformed_vertices.f64le.bin").write_bytes(array_bytes_f64(deformed))
    (out / "faces.i64le.bin").write_bytes(array_bytes_i64(f))

    health = geometry_health(v, deformed, f, state["domains"], selected_union)
    (out / "geometry_health.json").write_bytes(stable_json(health))
    stage_d = load_stage_d(geometry_dir, r11)
    visual = write_visual_evidence(stage_d, v, deformed, f, out)
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
        "bindVertexSha256": sha256_bytes(bind_before),
        "deformedVertexSha256": sha256_bytes(array_bytes_f64(deformed)),
        "faceIndexSha256": sha256_bytes(array_bytes_i64(f)),
        "weightSha256": sha256_bytes(weights_before),
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
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--pre-evidence-audit", action="store_true")
    mode.add_argument("--evaluate-pose", action="store_true")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.pre_evidence_audit:
        result = pre_evidence_audit(a.source_glb, a.geometry_dir, a.out)
    else:
        result = run_finite_pose_evidence(a.source_glb, a.geometry_dir, a.out)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
