from __future__ import annotations

import p1_fr1_mesh_probe as v1
import p1_fr1_mesh_probe_v2 as v2


PROBE_VERSION = "P1_FR1_LAYERED_VIEW_MESH_FEASIBILITY_V3_DIRECTION_CONVENTION"


def build_core_vertices(fixture):
    """V2 smooth skinning with the accepted H6N screen-space mirror convention.

    H6N negative turns mirror paw identity/order and yaw sign, but structural
    core anchors with z=0 project to the same screen-x coordinates for +/- yaw.
    V1/V2 additionally mirrored the canonical core contour by yaw sign, which
    double-applied a direction mirror and folded the contour only on the
    negative-turn half of the matrix. V3 removes that extra screen-x mirror.

    This does not alter semantic orientation or anatomical L/R identity. It only
    aligns visible core deformation with the already accepted projection model.
    """
    state = fixture.state
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    view_weights = v1.canonical_view_weights(yaw)
    shape = v1._shape_blend(view_weights)
    sx, sy = v1._screen_scale(fixture, view_weights)

    vertices = []
    for vertex_id, (shape_x, shape_y) in zip(v1.CORE_VERTEX_IDS, shape):
        skin = v2.CORE_SKIN_WEIGHTS[vertex_id]
        if abs(sum(skin.values()) - 1.0) > 1e-12:
            raise RuntimeError((vertex_id, skin))
        actual = v2._weighted_actual_anchor(state, skin)
        ref_x, ref_y = v2._blended_reference_anchor(view_weights, skin)
        local_x = (shape_x - ref_x) * sx
        local_y = (shape_y - ref_y) * sy
        vertices.append((vertex_id, actual.x + local_x, actual.y + local_y))
    return tuple(vertices)


def build_probe(fixture, direction: int = +1):
    state = fixture.state
    before_hash = v1._hash_json(v1._anchor_payload(state))
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    core = build_core_vertices(fixture)
    limbs = v1.build_limb_meshes(fixture)
    tail = v1.build_tail_mesh(fixture)
    after_hash = v1._hash_json(v1._anchor_payload(state))

    return v1.MeshProbeResult(
        semantic_hash=fixture.semantic_hash,
        morphology_id=fixture.morphology_id,
        case_id=fixture.case_id,
        size_dp=int(fixture.size_dp),
        t=float(fixture.t),
        direction=int(direction),
        yaw_rad=yaw,
        view_weights=tuple(sorted(v1.canonical_view_weights(yaw).items())),
        core_vertices=core,
        limb_meshes=limbs,
        tail_mesh=tail,
        topology_signature=v1.topology_signature(),
        semantic_anchor_hash_before=before_hash,
        semantic_anchor_hash_after=after_hash,
        paw_pin_error_max=max(mesh["pawPinError"] for mesh in limbs),
        core_self_intersections=v1.count_self_intersections(core),
        correction_families=tuple(),
    )


def result_dict(result):
    payload = v1.result_dict(result)
    payload["version"] = PROBE_VERSION
    return payload


CORE_VERTEX_IDS = v1.CORE_VERTEX_IDS
canonical_view_weights = v1.canonical_view_weights
topology_signature = v1.topology_signature
