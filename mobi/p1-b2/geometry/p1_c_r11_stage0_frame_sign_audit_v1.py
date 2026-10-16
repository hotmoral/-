from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5"
EXPECTED_STRUCTURAL_COUNT = 99642
EXPECTED_STAGE_D_BLOB = "5c8820fb7270e7727ececb1bb37d3a24331b24ab"
FACE_NODE_NAMES = (
    "Eye", "Eye.001", "Muzzle pad", "Muzzle pad.001",
    "Nose", "Vertical pupil", "Vertical pupil.001",
)


def parse_glb(path: Path):
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"source hash drift: {sha}")
    magic, version, total = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total != len(data):
        raise RuntimeError("GLB header drift")
    offset = 12
    chunks = []
    while offset < len(data):
        size, kind = struct.unpack_from("<II", data, offset)
        offset += 8
        chunks.append((kind, data[offset:offset + size]))
        offset += size
    doc = json.loads(chunks[0][1].decode("utf-8").rstrip("\x00 "))
    bin_chunk = chunks[1][1]
    return data, doc, bin_chunk


def structural_positions(doc, bin_chunk):
    nodes = [n for n in doc["nodes"] if n.get("name") == "Cat continuous body"]
    if len(nodes) != 1:
        raise RuntimeError(f"structural node count drift: {len(nodes)}")
    node = nodes[0]
    primitive = doc["meshes"][node["mesh"]]["primitives"][0]
    accessor = doc["accessors"][primitive["attributes"]["POSITION"]]
    view = doc["bufferViews"][accessor["bufferView"]]
    if accessor["componentType"] != 5126 or accessor["type"] != "VEC3":
        raise RuntimeError("POSITION accessor drift")
    base = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    stride = view.get("byteStride", 12)
    t = node.get("translation", [0.0, 0.0, 0.0])
    out = []
    for i in range(accessor["count"]):
        x, y, z = struct.unpack_from("<fff", bin_chunk, base + i * stride)
        out.append((x + t[0], y + t[1], z + t[2]))
    if len(out) != EXPECTED_STRUCTURAL_COUNT:
        raise RuntimeError(f"structural vertex count drift: {len(out)}")
    return out


def run(path: Path):
    data, doc, bin_chunk = parse_glb(path)
    points = structural_positions(doc, bin_chunk)
    mins = [min(p[k] for p in points) for k in range(3)]
    maxs = [max(p[k] for p in points) for k in range(3)]
    nodes = {n.get("name"): n for n in doc["nodes"]}
    face = {name: nodes[name].get("translation") for name in FACE_NODE_NAMES}

    # Geometry hard-gate: facial semantic parts occupy the positive-Z face region,
    # while paired eyes/muzzle/pupils are mirrored across X.
    if not all(face[name][2] > 0.0 for name in FACE_NODE_NAMES):
        raise RuntimeError("face/front +Z audit failed")
    for a, b in (("Eye", "Eye.001"), ("Muzzle pad", "Muzzle pad.001"), ("Vertical pupil", "Vertical pupil.001")):
        pa, pb = face[a], face[b]
        if not (pa[0] < 0.0 < pb[0] and abs(pa[0] + pb[0]) <= 1e-9):
            raise RuntimeError(f"bilateral X mirror audit failed: {a}/{b}")

    # Frozen Stage-C/Stage-D view convention.
    def screen_right(deg: float):
        th = math.radians(deg)
        return (math.cos(th), 0.0, math.sin(th))

    def camera_forward_toward_target(deg: float):
        th = math.radians(deg)
        return (math.sin(th), 0.0, -math.cos(th))

    r0 = screen_right(0.0)
    f0 = camera_forward_toward_target(0.0)
    r90 = screen_right(90.0)
    if not (abs(r0[0] - 1.0) <= 1e-15 and abs(f0[2] + 1.0) <= 1e-15 and abs(r90[2] - 1.0) <= 1e-15):
        raise RuntimeError("frozen view-vector audit failed")

    # +Z is the animal's front. At yaw 0 the camera is on +Z and looks -Z,
    # so the animal faces the viewer. Viewer screen-right is +X; for a facing
    # subject viewer-right is the subject's anatomical-left.
    anatomical_left_sign = "+X_R10"
    result = {
        "version": "P1_C_R11_STAGE0_FRAME_SIGN_AUDIT_V1",
        "sourceSha256": hashlib.sha256(data).hexdigest(),
        "sourceBytes": len(data),
        "stageDProjectionBlobReferenced": EXPECTED_STAGE_D_BLOB,
        "structuralVertexCount": len(points),
        "structuralAabbMin": mins,
        "structuralAabbMax": maxs,
        "faceNodeTranslations": face,
        "sourceFrame": {"up": "+Y_R10", "front": "+Z_R10", "bilateral": "X_R10"},
        "yaw0": {"screenRight": r0, "cameraForwardTowardTarget": f0},
        "yaw90": {"screenRight": r90},
        "anatomicalLeftSign": anatomical_left_sign,
        "mapping": {"x_B3": "z_R10", "y_B3": "y_R10", "z_B3": "x_R10"},
        "decision": "PASS_PLUS_X_R10_IS_ANATOMICAL_LEFT",
        "failurePolicy": "STOP_CHANGE_CONTROL_NO_SILENT_FLIP",
    }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_glb", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    result = run(a.source_glb)
    a.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
