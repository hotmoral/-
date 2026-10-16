from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import bpy
import numpy as np

VERSION = "P1_C_POST_R10_RIGGED_CAT_MOTION_REFERENCE_AUDIT_V1"


def parse_args() -> argparse.Namespace:
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    return ap.parse_args(argv)


def sha_topology(mesh) -> str:
    h = hashlib.sha256()
    h.update(int(len(mesh.vertices)).to_bytes(8, "little", signed=False))
    h.update(int(len(mesh.polygons)).to_bytes(8, "little", signed=False))
    for poly in mesh.polygons:
        verts = tuple(int(v) for v in poly.vertices)
        h.update(len(verts).to_bytes(4, "little", signed=False))
        for v in verts:
            h.update(v.to_bytes(4, "little", signed=False))
    return h.hexdigest()


def mesh_coords(mesh) -> np.ndarray:
    arr = np.empty((len(mesh.vertices), 3), dtype=np.float64)
    for i, v in enumerate(mesh.vertices):
        arr[i, :] = (float(v.co.x), float(v.co.y), float(v.co.z))
    return arr


def bbox_diag(points: np.ndarray) -> float:
    if len(points) == 0:
        return 0.0
    ext = points.max(axis=0) - points.min(axis=0)
    return float(np.linalg.norm(ext))


def best_fit_similarity(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, dict]:
    if source.shape != target.shape or source.ndim != 2 or source.shape[1] != 3:
        raise ValueError("shape mismatch for similarity alignment")
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
        "sourceCentroid": [float(x) for x in xs],
        "targetCentroid": [float(x) for x in yt],
    }


def displacement_summary(source: np.ndarray, target: np.ndarray) -> dict:
    aligned, transform = best_fit_similarity(source, target)
    d = np.linalg.norm(aligned - target, axis=1)
    diag = bbox_diag(target)
    n = d / diag if diag > 1e-30 else d
    return {
        "alignment": transform,
        "targetBBoxDiagonal": diag,
        "normalized": {
            "p50": float(np.percentile(n, 50)),
            "p90": float(np.percentile(n, 90)),
            "p95": float(np.percentile(n, 95)),
            "p99": float(np.percentile(n, 99)),
            "max": float(np.max(n)),
            "rms": float(np.sqrt(np.mean(n * n))),
        },
    }


def armature_modifier_target(obj):
    for mod in obj.modifiers:
        if mod.type == "ARMATURE" and getattr(mod, "object", None) is not None:
            return mod.object
    if obj.parent is not None and obj.parent.type == "ARMATURE":
        return obj.parent
    return None


def choose_primary_mesh() -> tuple[object | None, object | None, list[dict]]:
    candidates = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        arm = armature_modifier_target(obj)
        candidates.append({
            "object": obj,
            "armature": arm,
            "vertexCount": len(obj.data.vertices),
            "polygonCount": len(obj.data.polygons),
            "vertexGroupCount": len(obj.vertex_groups),
            "hasArmature": arm is not None,
        })
    ranked = sorted(
        candidates,
        key=lambda x: (x["hasArmature"], x["polygonCount"], x["vertexCount"]),
        reverse=True,
    )
    chosen = ranked[0] if ranked else None
    report = [
        {
            "name": x["object"].name,
            "dataName": x["object"].data.name,
            "vertexCount": x["vertexCount"],
            "polygonCount": x["polygonCount"],
            "vertexGroupCount": x["vertexGroupCount"],
            "armatureObject": x["armature"].name if x["armature"] else None,
            "modifiers": [
                {
                    "name": m.name,
                    "type": m.type,
                    "object": getattr(getattr(m, "object", None), "name", None),
                }
                for m in x["object"].modifiers
            ],
        }
        for x in ranked
    ]
    if chosen is None:
        return None, None, report
    return chosen["object"], chosen["armature"], report


def vertex_group_summary(obj) -> list[dict]:
    index_to_name = {g.index: g.name for g in obj.vertex_groups}
    weights: dict[int, list[float]] = defaultdict(list)
    for v in obj.data.vertices:
        for g in v.groups:
            if float(g.weight) > 0.0:
                weights[int(g.group)].append(float(g.weight))
    out = []
    for idx, name in sorted(index_to_name.items(), key=lambda kv: kv[1].lower()):
        ws = np.asarray(weights.get(idx, []), dtype=np.float64)
        out.append({
            "index": idx,
            "name": name,
            "weightedVertexCount": int(len(ws)),
            "weightSum": float(ws.sum()) if len(ws) else 0.0,
            "weightP50": float(np.percentile(ws, 50)) if len(ws) else None,
            "weightP90": float(np.percentile(ws, 90)) if len(ws) else None,
            "weightMax": float(ws.max()) if len(ws) else None,
        })
    return out


def armature_summary(arm_obj) -> dict | None:
    if arm_obj is None or arm_obj.type != "ARMATURE":
        return None
    bones = []
    for b in arm_obj.data.bones:
        bones.append({
            "name": b.name,
            "parent": b.parent.name if b.parent else None,
            "useDeform": bool(b.use_deform),
            "headLocal": [float(x) for x in b.head_local],
            "tailLocal": [float(x) for x in b.tail_local],
            "length": float(b.length),
        })
    return {
        "objectName": arm_obj.name,
        "dataName": arm_obj.data.name,
        "boneCount": len(bones),
        "bones": bones,
    }


def action_summary(action) -> dict:
    frame_range = [float(action.frame_range[0]), float(action.frame_range[1])]
    fcurves = list(getattr(action, "fcurves", []))
    groups = sorted({getattr(fc.group, "name", None) for fc in fcurves if getattr(fc, "group", None)})
    paths = sorted({str(fc.data_path) for fc in fcurves})
    return {
        "name": action.name,
        "frameRange": frame_range,
        "fCurveCount": len(fcurves),
        "groups": groups,
        "sampleDataPaths": paths[:40],
    }


def sampled_frames(action) -> list[int]:
    start = int(math.floor(float(action.frame_range[0])))
    end = int(math.ceil(float(action.frame_range[1])))
    if end <= start:
        return [start]
    vals = [start, round(start + 0.25 * (end - start)), round(start + 0.5 * (end - start)), round(start + 0.75 * (end - start)), end]
    return sorted(set(int(v) for v in vals))


def evaluated_mesh_state(obj, depsgraph) -> tuple[dict, np.ndarray]:
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
    try:
        state = {
            "vertexCount": len(mesh.vertices),
            "polygonCount": len(mesh.polygons),
            "topologySha256": sha_topology(mesh),
        }
        coords = mesh_coords(mesh)
    finally:
        eval_obj.to_mesh_clear()
    return state, coords


def audit_action(scene, obj, arm_obj, action) -> dict:
    arm_obj.animation_data_create()
    old_action = arm_obj.animation_data.action
    old_frame = int(scene.frame_current)
    arm_obj.animation_data.action = action
    frames = sampled_frames(action)
    states = []
    coords = []
    try:
        for frame in frames:
            scene.frame_set(frame)
            depsgraph = bpy.context.evaluated_depsgraph_get()
            depsgraph.update()
            state, c = evaluated_mesh_state(obj, depsgraph)
            state["frame"] = frame
            states.append(state)
            coords.append(c)
    finally:
        arm_obj.animation_data.action = old_action
        scene.frame_set(old_frame)

    topo_set = {(s["vertexCount"], s["polygonCount"], s["topologySha256"]) for s in states}
    exact_correspondence = len(topo_set) == 1 and len(coords) >= 2
    displacement = []
    if exact_correspondence:
        ref = coords[0]
        for i in range(1, len(coords)):
            d = displacement_summary(ref, coords[i])
            d["fromFrame"] = frames[0]
            d["toFrame"] = frames[i]
            displacement.append(d)
    return {
        "action": action_summary(action),
        "frames": frames,
        "evaluatedStates": states,
        "topologyInvariantAcrossSampledFrames": len(topo_set) == 1,
        "directVertexCorrespondenceAcrossSampledFrames": exact_correspondence,
        "displacementFromFirstSample": displacement,
    }


def main() -> None:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    primary, armature, meshes = choose_primary_mesh()
    actions = sorted(bpy.data.actions, key=lambda a: a.name.lower())
    action_reports = [action_summary(a) for a in actions]
    motion_actions = [a for a in actions if any(k in a.name.lower() for k in ("walk", "run"))]

    report = {
        "version": VERSION,
        "blenderVersion": bpy.app.version_string,
        "filePath": bpy.data.filepath,
        "objects": {
            "meshCount": sum(1 for o in bpy.data.objects if o.type == "MESH"),
            "armatureCount": sum(1 for o in bpy.data.objects if o.type == "ARMATURE"),
            "allMeshCandidates": meshes,
        },
        "primaryMesh": None,
        "armature": armature_summary(armature),
        "actions": action_reports,
        "motionActionAudits": [],
        "firewall": [
            "this source is motion-structure evidence only",
            "its morphology is not adopted as Mobi morphology",
            "no bone positions or weights are transferred to Mobi in this audit",
        ],
    }

    if primary is None:
        report["auditConclusion"] = "NO_MESH_OBJECT_FOUND"
    else:
        report["primaryMesh"] = {
            "objectName": primary.name,
            "dataName": primary.data.name,
            "baseVertexCount": len(primary.data.vertices),
            "basePolygonCount": len(primary.data.polygons),
            "baseTopologySha256": sha_topology(primary.data),
            "vertexGroupCount": len(primary.vertex_groups),
            "armatureObject": armature.name if armature else None,
            "vertexGroups": vertex_group_summary(primary),
        }
        if armature is None:
            report["auditConclusion"] = "PRIMARY_MESH_HAS_NO_ARMATURE_BINDING"
        elif not motion_actions:
            report["auditConclusion"] = "NO_WALK_OR_RUN_ACTION_FOUND"
        else:
            for action in motion_actions:
                report["motionActionAudits"].append(
                    audit_action(bpy.context.scene, primary, armature, action)
                )
            clean = [
                a for a in report["motionActionAudits"]
                if a["directVertexCorrespondenceAcrossSampledFrames"]
            ]
            report["auditConclusion"] = (
                "FIXED_TOPOLOGY_RIGGED_MOTION_REFERENCE_AVAILABLE"
                if clean
                else "RIGGED_ACTIONS_PRESENT_BUT_EVALUATED_TOPOLOGY_NOT_FIXED"
            )

    (args.out / "rigged_cat_motion_reference_summary.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
