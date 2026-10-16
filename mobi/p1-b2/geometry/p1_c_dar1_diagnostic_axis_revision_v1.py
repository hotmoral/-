from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

VERSION = "P1_C_DAR1_DIAGNOSTIC_AXIS_REVISION_V1"
DECISION_TOKEN = "POST_R12_DIAGNOSTIC_AXIS_SINGLE_CHILD_CONTINUATION_SELECTED"
CONTRACT_TOKEN = "POST_R12_DIAGNOSTIC_AXIS_REVISION_CONTRACT_FROZEN"
PREFLIGHT_TOKEN = "POST_R12_DIAGNOSTIC_AXIS_REVISION_PREFLIGHT_PASS"
VARIANT = "DAR1_HIERARCHY_CONTINUATION_ON_EXACT_PARENT_DEGENERACY"

EXPECTED_R12_SHA256 = "fc4096162607dbf59859749562ec5ab9ea7d0e09551aa7cd3cd1ad05e9f5594c"
EXPECTED_R12_GIT_BLOB_SHA1 = "837f4abe7ff474a527893b099be8087a104f7aaa"
EXPECTED_R12_VERSION = "P1_C_R12_SURFACE_TERMINAL_BIND_ALIAS_V1"
EXPECTED_R11_SHA256 = "af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87"
EXPECTED_V3125_SHA256 = "839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77"

DEGENERATE_THRESHOLD = 1e-15
EXPECTED_EDGE_COUNT = 29
EXPECTED_DEGENERATE_EDGE = ("PELVIS_CTRL", "TAIL_ROOT_CTRL")
EXPECTED_FALLBACK_ROLE = "TAIL_ROOT_CTRL"
EXPECTED_DIRECT_CHILD = "TAIL_1_CTRL"
EXPECTED_TANGENT = np.asarray([0.0, 0.0090661229202611, -0.08406815248194494], dtype=np.float64)
EXPECTED_TANGENT_NORM = 0.08455559618696346
EXPECTED_AXIS = np.asarray([0.0, -0.9942352283349678, -0.10722085029374898], dtype=np.float64)
IDENTITY_ATOL = 1e-15


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def stable_json(obj) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, separators=(",", ": ")) + "\n").encode("utf-8")


def load_r12(geometry_dir: Path):
    path = geometry_dir / "p1_c_r12_surface_terminal_bind_alias_v1.py"
    if not path.is_file():
        raise RuntimeError("frozen R12 adapter missing")
    actual_sha = sha256_file(path)
    actual_blob = git_blob_sha1(path)
    if actual_sha != EXPECTED_R12_SHA256:
        raise RuntimeError(f"R12 adapter SHA drift: {actual_sha}")
    if actual_blob != EXPECTED_R12_GIT_BLOB_SHA1:
        raise RuntimeError(f"R12 adapter blob drift: {actual_blob}")
    spec = importlib.util.spec_from_file_location("mobi_r12_frozen_for_dar1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen R12 adapter")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if getattr(mod, "VERSION", None) != EXPECTED_R12_VERSION:
        raise RuntimeError(f"R12 version drift: {getattr(mod, 'VERSION', None)}")
    if getattr(mod, "EXPECTED_R11_IMPLEMENTATION_SHA256", None) != EXPECTED_R11_SHA256:
        raise RuntimeError("R12 inherited R11 SHA drift")
    if getattr(mod, "EXPECTED_V3125_MESH_SHA256", None) != EXPECTED_V3125_SHA256:
        raise RuntimeError("R12 inherited V3125 identity drift")
    return mod


def controls_by_role(controls) -> dict:
    return {c.role: c for c in controls}


def axis_from_tangent(tangent: np.ndarray) -> np.ndarray:
    tangent = np.asarray(tangent, dtype=np.float64)
    n = float(np.linalg.norm(tangent))
    if n <= DEGENERATE_THRESHOLD:
        raise RuntimeError("zero diagnostic tangent")
    t = tangent / n
    basis = min(np.eye(3), key=lambda b: abs(float(np.dot(t, b))))
    axis = np.cross(t, basis)
    an = float(np.linalg.norm(axis))
    if an <= DEGENERATE_THRESHOLD:
        raise RuntimeError("zero diagnostic axis")
    return axis / an


def hierarchy_activation_audit(r11, controls_by_role_map: dict) -> dict:
    if set(controls_by_role_map) != set(r11.ROLE_ORDER):
        raise RuntimeError("DAR1 control-role set drift")

    edges = []
    degenerate = []
    for role in r11.ROLE_ORDER:
        c = controls_by_role_map[role]
        if c.parent != r11.PARENT[role]:
            raise RuntimeError(f"DAR1 parent metadata drift {role}: {c.parent} != {r11.PARENT[role]}")
        if c.domain != r11.ROLE_DOMAIN[role]:
            raise RuntimeError(f"DAR1 domain metadata drift {role}: {c.domain} != {r11.ROLE_DOMAIN[role]}")
        if c.parent is None:
            continue
        parent = controls_by_role_map[c.parent]
        vector = np.asarray(c.position, dtype=np.float64) - np.asarray(parent.position, dtype=np.float64)
        length = float(np.linalg.norm(vector))
        row = {
            "parent": c.parent,
            "role": role,
            "length": length,
            "degenerateLE1e15": bool(length <= DEGENERATE_THRESHOLD),
        }
        edges.append(row)
        if row["degenerateLE1e15"]:
            degenerate.append((c.parent, role))

    if len(edges) != EXPECTED_EDGE_COUNT:
        raise RuntimeError(f"DAR1 hierarchy edge count drift: {len(edges)}")
    if tuple(degenerate) != (EXPECTED_DEGENERATE_EDGE,):
        raise RuntimeError(f"DAR1 degenerate edge set drift: {degenerate}")

    children = tuple(
        role for role in r11.ROLE_ORDER
        if controls_by_role_map[role].parent == EXPECTED_FALLBACK_ROLE
    )
    if children != (EXPECTED_DIRECT_CHILD,):
        raise RuntimeError(f"DAR1 direct-child identity/count drift: {children}")

    root = np.asarray(controls_by_role_map[EXPECTED_FALLBACK_ROLE].position, dtype=np.float64)
    child = np.asarray(controls_by_role_map[EXPECTED_DIRECT_CHILD].position, dtype=np.float64)
    tangent = child - root
    tangent_norm = float(np.linalg.norm(tangent))
    if tangent_norm <= DEGENERATE_THRESHOLD:
        raise RuntimeError("DAR1 direct-child continuation tangent is degenerate")

    return {
        "edgeCount": len(edges),
        "degenerateThreshold": DEGENERATE_THRESHOLD,
        "degenerateEdgeCount": len(degenerate),
        "degenerateEdges": [list(x) for x in degenerate],
        "fallbackRole": EXPECTED_FALLBACK_ROLE,
        "directChildren": list(children),
        "selectedDirectChild": EXPECTED_DIRECT_CHILD,
        "selectedTangentR10": tangent.tolist(),
        "selectedTangentNorm": tangent_norm,
    }


def diagnostic_axis_dar1(r11, inherited_axis, role: str, controls_by_role_map: dict) -> np.ndarray:
    c = controls_by_role_map[role]
    if c.parent is None:
        return np.asarray(inherited_axis(role, controls_by_role_map), dtype=np.float64)

    incoming = np.asarray(c.position, dtype=np.float64) - np.asarray(
        controls_by_role_map[c.parent].position, dtype=np.float64
    )
    if float(np.linalg.norm(incoming)) > DEGENERATE_THRESHOLD:
        return np.asarray(inherited_axis(role, controls_by_role_map), dtype=np.float64)

    if role != EXPECTED_FALLBACK_ROLE or c.parent != EXPECTED_DEGENERATE_EDGE[0]:
        raise RuntimeError(f"DAR1 unexpected degenerate incoming edge {c.parent}->{role}")

    audit = hierarchy_activation_audit(r11, controls_by_role_map)
    tangent = np.asarray(audit["selectedTangentR10"], dtype=np.float64)
    return axis_from_tangent(tangent)


def axis_isolation_audit(r11, controls) -> dict:
    by = controls_by_role(controls)
    hierarchy = hierarchy_activation_audit(r11, by)
    inherited = r11.diagnostic_axis
    rows = {}
    changed = []

    for role in r11.ROLE_ORDER:
        inherited_axis_value = None
        inherited_error = None
        try:
            inherited_axis_value = np.asarray(inherited(role, by), dtype=np.float64)
        except RuntimeError as exc:
            inherited_error = str(exc)

        revised = diagnostic_axis_dar1(r11, inherited, role, by)
        if role == EXPECTED_FALLBACK_ROLE:
            if inherited_error is None or "zero diagnostic tangent" not in inherited_error:
                raise RuntimeError(f"DAR1 expected inherited tail-root singularity missing: {inherited_error}")
            changed.append(role)
        else:
            if inherited_error is not None:
                raise RuntimeError(f"DAR1 unexpected inherited axis failure {role}: {inherited_error}")
            if not np.array_equal(revised, inherited_axis_value):
                raise RuntimeError(f"DAR1 changed non-tail-root diagnostic axis {role}")

        rows[role] = {
            "inheritedDefined": inherited_error is None,
            "inheritedError": inherited_error,
            "revisedAxisR10": revised.tolist(),
            "exactlyInheritedForNonTailRoot": bool(
                role == EXPECTED_FALLBACK_ROLE or np.array_equal(revised, inherited_axis_value)
            ),
        }

    if changed != [EXPECTED_FALLBACK_ROLE]:
        raise RuntimeError(f"DAR1 changed-role set drift: {changed}")

    selected_tangent = np.asarray(hierarchy["selectedTangentR10"], dtype=np.float64)
    selected_axis = np.asarray(rows[EXPECTED_FALLBACK_ROLE]["revisedAxisR10"], dtype=np.float64)
    if not np.allclose(selected_tangent, EXPECTED_TANGENT, rtol=0.0, atol=IDENTITY_ATOL):
        raise RuntimeError(f"DAR1 frozen tangent identity drift: {selected_tangent.tolist()}")
    if not math.isclose(float(hierarchy["selectedTangentNorm"]), EXPECTED_TANGENT_NORM, rel_tol=0.0, abs_tol=IDENTITY_ATOL):
        raise RuntimeError(f"DAR1 frozen tangent norm drift: {hierarchy['selectedTangentNorm']}")
    if not np.allclose(selected_axis, EXPECTED_AXIS, rtol=0.0, atol=IDENTITY_ATOL):
        raise RuntimeError(f"DAR1 frozen axis identity drift: {selected_axis.tolist()}")

    return {
        "hierarchy": hierarchy,
        "changedDiagnosticAxisRoles": changed,
        "changedDiagnosticAxisRoleCount": len(changed),
        "allNonTailRootAxesExactInherited": True,
        "selectedTangentMatchesFrozenIdentity": True,
        "selectedAxisMatchesFrozenIdentity": True,
        "roles": rows,
    }


def _control_snapshot(controls) -> list[dict]:
    return [
        {
            "role": c.role,
            "parent": c.parent,
            "domain": c.domain,
            "positionR10": list(c.position),
            "provenance": c.provenance,
            "derivation": c.derivation,
        }
        for c in controls
    ]


def run_identity_only(source_glb: Path, geometry_dir: Path, out_file: Path):
    r12 = load_r12(geometry_dir)
    inherited = r12.run_identity_only(source_glb, geometry_dir, out_file)
    result = {
        "version": VERSION,
        "variant": VARIANT,
        "decisionToken": DECISION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "preflightToken": PREFLIGHT_TOKEN,
        "r12AdapterSha256": EXPECTED_R12_SHA256,
        "r12AdapterGitBlobSha1": EXPECTED_R12_GIT_BLOB_SHA1,
        "inheritedR12Identity": inherited,
    }
    out_file.write_bytes(stable_json(result))
    return result


def run_stage0_audit(source_glb: Path, geometry_dir: Path, out_file: Path):
    r12 = load_r12(geometry_dir)
    r11 = r12.load_r11(geometry_dir)

    v, f, identity = r11.reproduce_v3125(source_glb, geometry_dir)
    if identity.get("meshArraySha256") != EXPECTED_V3125_SHA256:
        raise RuntimeError("DAR1 V3125 identity drift")
    frame = r11.frame_sign_audit(v, geometry_dir)

    skel, transform, pitch = r11.voxel_skeleton(v, f)
    raw_graph = r11.graph_from_skeleton(skel)
    graph, _snapped, nodes, paths = r11.derive_semantic_graph(v, raw_graph, transform, pitch)
    r11_controls, path_worlds = r11.make_controls(transform, nodes, paths)
    aliases = r12.derive_surface_terminal_aliases(v, r11)
    r12_controls = r12.replace_paw_bind_controls(r11, r11_controls, aliases)
    r12_delta = r12.delta_audit(r11, r11_controls, r12_controls, path_worlds, aliases)

    controls_before = _control_snapshot(r12_controls)
    controls_before_bytes = stable_json(controls_before)
    domains, interfaces, _domain_info, _polylines = r11.derive_domains(v, path_worlds, pitch)
    indices, weights = r11.build_weights(v, r12_controls, domains, interfaces, pitch)
    weight_report = r11.weight_audit(indices, weights, domains, interfaces)
    weight_bytes = r11.serialize_weights(indices, weights)

    axis_audit = axis_isolation_audit(r11, r12_controls)

    controls_after = _control_snapshot(r12_controls)
    controls_after_bytes = stable_json(controls_after)
    if controls_before_bytes != controls_after_bytes:
        raise RuntimeError("DAR1 axis audit mutated control scaffold")

    indices_after, weights_after = r11.build_weights(v, r12_controls, domains, interfaces, pitch)
    if not np.array_equal(indices, indices_after) or not np.array_equal(weights, weights_after):
        raise RuntimeError("DAR1 axis audit mutated or destabilized frozen weights")

    rest = r11.rest_lbs(v, r12_controls, indices, weights)
    delta = np.linalg.norm(rest - v, axis=1)
    h = float(r11.body_metrics(v)["height"])
    rest_max = float(delta.max() / h)
    rest_rms = float(math.sqrt(float(np.mean(delta * delta))) / h)
    if rest_max > r11.REST_MAX_NORMALIZED or rest_rms > r11.REST_RMS_NORMALIZED:
        raise RuntimeError("DAR1 neutral rest identity drift")

    report = {
        "version": VERSION,
        "variant": VARIANT,
        "decisionToken": DECISION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "preflightToken": PREFLIGHT_TOKEN,
        "structuralStage1EvidenceExecuted": False,
        "jacobianDerivativeExecuted": False,
        "rasterEvidenceExecuted": False,
        "r12AdapterSha256": EXPECTED_R12_SHA256,
        "r12AdapterGitBlobSha1": EXPECTED_R12_GIT_BLOB_SHA1,
        "identity": identity,
        "frame": frame,
        "pitch": float(pitch),
        "controlCount": len(r12_controls),
        "controlSnapshotSha256Before": hashlib.sha256(controls_before_bytes).hexdigest(),
        "controlSnapshotSha256After": hashlib.sha256(controls_after_bytes).hexdigest(),
        "controlSnapshotByteIdenticalBeforeAfter": controls_before_bytes == controls_after_bytes,
        "r12DeltaAudit": r12_delta,
        "weightSha256Before": hashlib.sha256(weight_bytes).hexdigest(),
        "weightSha256After": hashlib.sha256(r11.serialize_weights(indices_after, weights_after)).hexdigest(),
        "weightByteIdenticalBeforeAfter": bool(
            r11.serialize_weights(indices_after, weights_after) == weight_bytes
        ),
        "weightAudit": weight_report,
        "axisIsolation": axis_audit,
        "rest": {"maxNormalized": rest_max, "rmsNormalized": rest_rms},
        "prunedSkeletonNodeCount": len(graph),
    }
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(stable_json(report))
    return report


def run_stage1(source_glb: Path, geometry_dir: Path, out: Path):
    r12 = load_r12(geometry_dir)
    original_loader = r12.load_r11
    r11 = original_loader(geometry_dir)
    inherited_axis = r11.diagnostic_axis

    def revised_axis(role, controls_by_role_map):
        return diagnostic_axis_dar1(r11, inherited_axis, role, controls_by_role_map)

    original_axis = r11.diagnostic_axis
    r11.diagnostic_axis = revised_axis
    r12.load_r11 = lambda _geometry_dir: r11
    try:
        return r12.run_stage1(source_glb, geometry_dir, out)
    finally:
        r12.load_r11 = original_loader
        r11.diagnostic_axis = original_axis


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_glb", type=Path)
    ap.add_argument("--geometry-dir", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--out", type=Path, required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--identity-only", action="store_true")
    mode.add_argument("--stage0-audit", action="store_true")
    mode.add_argument("--stage1", action="store_true")
    a = ap.parse_args()
    if a.identity_only:
        result = run_identity_only(a.source_glb, a.geometry_dir, a.out)
    elif a.stage0_audit:
        result = run_stage0_audit(a.source_glb, a.geometry_dir, a.out)
    else:
        result = run_stage1(a.source_glb, a.geometry_dir, a.out)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
