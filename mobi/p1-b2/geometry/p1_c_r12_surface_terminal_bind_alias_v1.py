from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

VERSION = "P1_C_R12_SURFACE_TERMINAL_BIND_ALIAS_V1"
FREEZE_TOKEN = "R12_STAGE0_IMPLEMENTATION_FREEZE"
DECISION_TOKEN = "R12_RF_M_SURFACE_TERMINAL_BIND_ALIAS_SELECTED_FOR_FEASIBILITY"
CONTRACT_TOKEN = "R12_SURFACE_TERMINAL_BIND_ALIAS_FEASIBILITY_CONTRACT_FROZEN"

EXPECTED_R11_IMPLEMENTATION_SHA256 = "af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87"
EXPECTED_R11_VERSION = "P1_C_R11_SEMANTIC_SCAFFOLD_V1"
EXPECTED_R11_FREEZE_TOKEN = "R11_STAGE0_IMPLEMENTATION_FREEZE"
EXPECTED_V3125_MESH_SHA256 = "839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77"

PAW_ROLE_TO_ANCHOR = {
    "FORE_L_PAW_CTRL": "FORE_L_PAW",
    "FORE_R_PAW_CTRL": "FORE_R_PAW",
    "HIND_L_PAW_CTRL": "HIND_L_PAW",
    "HIND_R_PAW_CTRL": "HIND_R_PAW",
}
PAW_ROLE_TO_PATH = {
    "FORE_L_PAW_CTRL": "FORE_L",
    "FORE_R_PAW_CTRL": "FORE_R",
    "HIND_L_PAW_CTRL": "HIND_L",
    "HIND_R_PAW_CTRL": "HIND_R",
}
PAW_ROLE_TO_DOMAIN = {
    "FORE_L_PAW_CTRL": "FORE_L",
    "FORE_R_PAW_CTRL": "FORE_R",
    "HIND_L_PAW_CTRL": "HIND_L",
    "HIND_R_PAW_CTRL": "HIND_R",
}
PAW_ROLES = tuple(PAW_ROLE_TO_ANCHOR)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_json(obj) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, separators=(",", ": ")) + "\n").encode("utf-8")


def load_r11(geometry_dir: Path):
    path = geometry_dir / "p1_c_r11_semantic_scaffold_v1.py"
    if not path.is_file():
        raise RuntimeError("assembled frozen R11 implementation is missing")
    actual_sha = sha256_file(path)
    if actual_sha != EXPECTED_R11_IMPLEMENTATION_SHA256:
        raise RuntimeError(f"R11 implementation SHA drift: {actual_sha}")
    spec = importlib.util.spec_from_file_location("mobi_r11_frozen_for_r12", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen R11 implementation")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    checks = {
        "version": getattr(mod, "VERSION", None),
        "freezeToken": getattr(mod, "FREEZE_TOKEN", None),
        "roleCount": len(getattr(mod, "ROLE_ORDER", ())),
        "domains": tuple(getattr(mod, "DOMAIN_ORDER", ())),
        "pawSupportRadiusPitches": getattr(mod, "PAW_SUPPORT_RADIUS_PITCHES", None),
        "maxInfluences": getattr(mod, "MAX_INFLUENCES", None),
    }
    expected = {
        "version": EXPECTED_R11_VERSION,
        "freezeToken": EXPECTED_R11_FREEZE_TOKEN,
        "roleCount": 30,
        "domains": ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        "pawSupportRadiusPitches": 4.0,
        "maxInfluences": 4,
    }
    if checks != expected:
        raise RuntimeError(f"R11 structural identity drift: {checks}")
    return mod


def _quadrant_masks(vertices: np.ndarray, xmid: float, zmid: float) -> dict[str, np.ndarray]:
    return {
        "FORE_L_PAW": (vertices[:, 0] >= xmid) & (vertices[:, 2] >= zmid),
        "FORE_R_PAW": (vertices[:, 0] < xmid) & (vertices[:, 2] >= zmid),
        "HIND_L_PAW": (vertices[:, 0] >= xmid) & (vertices[:, 2] < zmid),
        "HIND_R_PAW": (vertices[:, 0] < xmid) & (vertices[:, 2] < zmid),
    }


def derive_surface_terminal_aliases(vertices: np.ndarray, r11) -> dict[str, dict]:
    v = np.asarray(vertices, dtype=np.float64, order="C")
    b = r11.body_metrics(v)
    h = float(b["height"])
    xmid = float(b["center"][0])
    zmid = float(b["center"][2])
    aliases: dict[str, dict] = {}
    for anchor, mask in _quadrant_masks(v, xmid, zmid).items():
        quadrant_indices = np.flatnonzero(mask)
        if len(quadrant_indices) == 0:
            raise RuntimeError(f"empty R12 paw quadrant {anchor}")
        q_ymin = float(v[quadrant_indices, 1].min())
        threshold = q_ymin + 0.035 * h
        candidate_indices = quadrant_indices[v[quadrant_indices, 1] <= threshold]
        if len(candidate_indices) == 0:
            raise RuntimeError(f"empty R12 paw sole candidate set {anchor}")
        sole = v[candidate_indices]
        sole_mean = np.asarray(sole.mean(axis=0), dtype=np.float64)
        ranked = []
        for index in candidate_indices.tolist():
            d = v[int(index)] - sole_mean
            ranked.append((float(np.dot(d, d)), int(index)))
        squared_distance, selected_index = min(ranked)
        selected = np.asarray(v[selected_index], dtype=np.float64)
        aliases[anchor] = {
            "quadrantVertexCount": int(len(quadrant_indices)),
            "candidateCount": int(len(candidate_indices)),
            "quadrantYMin": q_ymin,
            "soleThresholdY": float(threshold),
            "soleMeanR10": sole_mean.tolist(),
            "surfaceBindIndex": selected_index,
            "surfaceBindPositionR10": selected.tolist(),
            "squaredDistanceToSoleMean": squared_distance,
            "derivation": "FROZEN_SOLE_CANDIDATE_ARGMIN_DISTANCE_THEN_GLOBAL_VERTEX_INDEX",
        }
    return aliases


def replace_paw_bind_controls(r11, r11_controls, aliases: dict[str, dict]):
    out = []
    for c in r11_controls:
        if c.role not in PAW_ROLE_TO_ANCHOR:
            out.append(c)
            continue
        alias = aliases[PAW_ROLE_TO_ANCHOR[c.role]]
        out.append(r11.Control(
            c.role,
            c.parent,
            c.domain,
            tuple(map(float, alias["surfaceBindPositionR10"])),
            c.provenance,
            "R12_SURFACE_TERMINAL_ALIAS_EXISTING_V3125_VERTEX",
        ))
    return out


def delta_audit(r11, r11_controls, r12_controls, path_worlds, aliases: dict[str, dict]) -> dict:
    old = {c.role: c for c in r11_controls}
    new = {c.role: c for c in r12_controls}
    if tuple(old) != tuple(new) or tuple(old) != tuple(r11.ROLE_ORDER):
        raise RuntimeError("control role/order drift")
    changed = []
    medial = {}
    for role in r11.ROLE_ORDER:
        a, b = old[role], new[role]
        if (a.parent, a.domain, a.provenance) != (b.parent, b.domain, b.provenance):
            raise RuntimeError(f"non-coordinate control metadata drift {role}")
        if tuple(a.position) != tuple(b.position):
            changed.append(role)
        if role in PAW_ROLES:
            endpoint = np.asarray(path_worlds[PAW_ROLE_TO_PATH[role]][-1], dtype=np.float64)
            if not np.array_equal(np.asarray(a.position, dtype=np.float64), endpoint):
                raise RuntimeError(f"R11 medial paw endpoint no longer matches semantic path {role}")
            medial[role] = {
                "medialEndpointR10": endpoint.tolist(),
                "r12SurfaceBindIndex": int(aliases[PAW_ROLE_TO_ANCHOR[role]]["surfaceBindIndex"]),
                "r12SurfaceBindPositionR10": list(aliases[PAW_ROLE_TO_ANCHOR[role]]["surfaceBindPositionR10"]),
                "distanceMedialToSurfaceBind": float(np.linalg.norm(
                    endpoint - np.asarray(aliases[PAW_ROLE_TO_ANCHOR[role]]["surfaceBindPositionR10"], dtype=np.float64)
                )),
            }
    if tuple(changed) != PAW_ROLES:
        raise RuntimeError(f"R12 causal delta is not exactly the four paw binds: {changed}")
    return {
        "changedRoles": changed,
        "changedRoleCount": len(changed),
        "unchangedNonPawRoleCount": 26,
        "roleCount": len(r12_controls),
        "parentDomainProvenanceUnchanged": True,
        "medialPawEndpointsRetained": medial,
    }


def alias_semantic_weight_gate(r11, vertices, aliases, domains, indices, weights) -> dict:
    reports = {}
    for role in PAW_ROLES:
        anchor = PAW_ROLE_TO_ANCHOR[role]
        expected_domain = PAW_ROLE_TO_DOMAIN[role]
        alias = aliases[anchor]
        index = int(alias["surfaceBindIndex"])
        if not (0 <= index < len(vertices)):
            raise RuntimeError(f"alias vertex index out of range {role}")
        expected_position = np.asarray(alias["surfaceBindPositionR10"], dtype=np.float64)
        if not np.array_equal(np.asarray(vertices[index], dtype=np.float64), expected_position):
            raise RuntimeError(f"alias position is not exact V3125 vertex {role}")
        actual_domain = str(domains[index])
        if actual_domain != expected_domain:
            raise RuntimeError(f"alias vertex domain mismatch {role}: {actual_domain} != {expected_domain}")
        role_index = int(r11.ROLE_INDEX[role])
        slots = np.where(indices[index] == role_index)[0]
        own_weight = float(weights[index, int(slots[0])]) if len(slots) else 0.0
        if not own_weight > 0.0:
            raise RuntimeError(f"paw role has no positive weight at its surface bind alias {role}")
        reports[role] = {
            "surfaceBindIndex": index,
            "expectedDomain": expected_domain,
            "actualDomain": actual_domain,
            "ownRoleNormalizedWeightAtAlias": own_weight,
            "positionMatchesExactV3125Vertex": True,
        }
    return reports


def run_identity_only(source_glb: Path, geometry_dir: Path, out_file: Path):
    r11 = load_r11(geometry_dir)
    _v, _f, identity = r11.reproduce_v3125(source_glb, geometry_dir)
    mesh_sha = str(identity.get("meshArraySha256", ""))
    if mesh_sha != EXPECTED_V3125_MESH_SHA256:
        raise RuntimeError(f"V3125 mesh identity drift: {mesh_sha}")
    result = {
        "version": VERSION,
        "freezeTokenRequired": FREEZE_TOKEN,
        "r11ImplementationSha256": EXPECTED_R11_IMPLEMENTATION_SHA256,
        "v3125": identity,
    }
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(stable_json(result))
    return result


def run_stage1(source_glb: Path, geometry_dir: Path, out: Path):
    r11 = load_r11(geometry_dir)
    out.mkdir(parents=True, exist_ok=True)

    v, f, identity = r11.reproduce_v3125(source_glb, geometry_dir)
    if str(identity.get("meshArraySha256", "")) != EXPECTED_V3125_MESH_SHA256:
        raise RuntimeError("V3125 mesh identity drift")
    frame = r11.frame_sign_audit(v, geometry_dir)
    if frame.get("anatomicalLeftSign") != "+X_R10":
        raise RuntimeError("R12 frame/sign drift")

    skel, transform, pitch = r11.voxel_skeleton(v, f)
    raw_graph = r11.graph_from_skeleton(skel)
    graph, snapped, nodes, paths = r11.derive_semantic_graph(v, raw_graph, transform, pitch)
    r11_controls, path_worlds = r11.make_controls(transform, nodes, paths)

    aliases = derive_surface_terminal_aliases(v, r11)
    r12_controls = replace_paw_bind_controls(r11, r11_controls, aliases)
    delta = delta_audit(r11, r11_controls, r12_controls, path_worlds, aliases)

    (out / "medial_graph.json").write_bytes(stable_json(r11.graph_diagnostic(graph)))
    (out / "semantic_paths.json").write_bytes(stable_json(r11.semantic_paths_diagnostic(paths, transform)))
    (out / "r11_medial_paw_endpoints.json").write_bytes(stable_json(delta["medialPawEndpointsRetained"]))
    (out / "r12_surface_terminal_aliases.json").write_bytes(stable_json(aliases))
    (out / "r12_delta_audit.json").write_bytes(stable_json(delta))

    domains, interfaces, domain_info, _polylines = r11.derive_domains(v, path_worlds, pitch)
    domains_check, interfaces_check, _domain_info_check, _polylines_check = r11.derive_domains(v, path_worlds, pitch)
    if not np.array_equal(domains, domains_check) or not np.array_equal(interfaces, interfaces_check):
        raise RuntimeError("inherited six-domain derivation is not deterministic")

    indices, weights = r11.build_weights(v, r12_controls, domains, interfaces, pitch)
    weight_report = r11.weight_audit(indices, weights, domains, interfaces)
    alias_gate = alias_semantic_weight_gate(r11, v, aliases, domains, indices, weights)

    rest = r11.rest_lbs(v, r12_controls, indices, weights)
    delta_rest = np.linalg.norm(rest - v, axis=1)
    h = float(r11.body_metrics(v)["height"])
    rest_report = {
        "maxNormalized": float(delta_rest.max() / h),
        "rmsNormalized": float(math.sqrt(float(np.mean(delta_rest * delta_rest))) / h),
    }
    if rest_report["maxNormalized"] > r11.REST_MAX_NORMALIZED or rest_report["rmsNormalized"] > r11.REST_RMS_NORMALIZED:
        raise RuntimeError(f"rest drift fail {rest_report}")

    paw_positions = {
        role: np.asarray(next(c.position for c in r12_controls if c.role == role), dtype=np.float64)
        for role in PAW_ROLES
    }
    jacobian = r11.jacobian_audit(
        v, r12_controls, indices, weights, domains, pitch, domain_info["TAIL"], paw_positions
    )

    stage_d = r11._load_module(
        geometry_dir / "p1_c_3d_cat_stage_d_projection_v1.py",
        "r12_inherited_stage_d",
    )
    primary_raster = r11.write_primary_raster_evidence(stage_d, v, rest, f, out)
    raster = []
    triangles = [tuple(map(int, t)) for t in f.tolist()]
    for deg in np.arange(0.0, 90.0 + 1e-9, 2.5):
        base = stage_d.rasterize([stage_d.project_point(p, float(deg)) for p in v.tolist()], triangles)
        neutral = stage_d.rasterize([stage_d.project_point(p, float(deg)) for p in rest.tolist()], triangles)
        same = bytes(base) == bytes(neutral)
        raster.append({
            "yawDeg": float(deg),
            "byteIdentical": same,
            "sha256": hashlib.sha256(bytes(base)).hexdigest(),
        })
        if not same:
            raise RuntimeError(f"neutral raster drift at {deg}")

    scaffold = []
    for c in r12_controls:
        entry = {
            "ordinal": int(r11.ROLE_INDEX[c.role] + 1),
            "role": c.role,
            "parent": c.parent,
            "domain": c.domain,
            "positionR10": list(c.position),
            "provenance": c.provenance,
            "derivation": c.derivation,
        }
        if c.role in PAW_ROLES:
            entry["medialSemanticPathEndpointR10"] = delta["medialPawEndpointsRetained"][c.role]["medialEndpointR10"]
            entry["surfaceBindVertexIndex"] = aliases[PAW_ROLE_TO_ANCHOR[c.role]]["surfaceBindIndex"]
        scaffold.append(entry)

    weight_bytes = r11.serialize_weights(indices, weights)
    (out / "weights.bin").write_bytes(weight_bytes)
    (out / "scaffold.json").write_bytes(stable_json(scaffold))
    (out / "frame_sign_audit.json").write_bytes(stable_json(frame))
    (out / "domains.json").write_bytes(stable_json({
        "domains": domains.tolist(),
        "rootInterface": interfaces.tolist(),
    }))
    (out / "weight_audit.json").write_bytes(stable_json(weight_report))
    (out / "alias_semantic_weight_gate.json").write_bytes(stable_json(alias_gate))
    (out / "jacobian.json").write_bytes(stable_json(jacobian))
    (out / "raster_identity.json").write_bytes(stable_json(raster))

    summary = {
        "version": VERSION,
        "freezeTokenRequired": FREEZE_TOKEN,
        "decisionToken": DECISION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "r11ImplementationSha256": EXPECTED_R11_IMPLEMENTATION_SHA256,
        "identity": identity,
        "topologyIdentity": {
            "vertexCount": len(v),
            "faceCount": len(f),
            "faceIndexSha256": r11.face_index_sha256(f),
        },
        "pitch": float(pitch),
        "pawSupportRadiusPitches": float(r11.PAW_SUPPORT_RADIUS_PITCHES),
        "rawSkeletonNodes": len(raw_graph),
        "prunedSkeletonNodes": len(graph),
        "controlCount": len(r12_controls),
        "causalDelta": delta,
        "aliasSemanticWeightGate": alias_gate,
        "weightSha256": hashlib.sha256(weight_bytes).hexdigest(),
        "weightAudit": weight_report,
        "rest": rest_report,
        "primaryRaster": primary_raster,
        "rasterAll37ByteIdentical": all(x["byteIdentical"] for x in raster),
        "exactFront": raster[0],
    }
    (out / "summary.json").write_bytes(stable_json(summary))
    files = sorted(p for p in out.iterdir() if p.is_file() and p.name != "EVIDENCE_SHA256SUMS.txt")
    (out / "EVIDENCE_SHA256SUMS.txt").write_text(
        "".join(f"{sha256_file(p)}  {p.name}\n" for p in files),
        encoding="utf-8",
    )
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_glb", type=Path)
    ap.add_argument("--geometry-dir", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--identity-only", action="store_true")
    args = ap.parse_args()
    result = (
        run_identity_only(args.source_glb, args.geometry_dir, args.out)
        if args.identity_only
        else run_stage1(args.source_glb, args.geometry_dir, args.out)
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
