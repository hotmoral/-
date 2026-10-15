from __future__ import annotations

import hashlib
import json
from typing import Dict, List, Tuple

import p1_fr1_mesh_probe as fr1
import p1_fr1_mesh_probe_v2 as fr1_v2
import p1_fr2_layered_view_prototype as fr2_base
import p1_fr2_layered_view_prototype_v5 as fr2_v5


PROTOTYPE_VERSION = "P1_FR3_FELINE_CORE_TOPOLOGY_V1_24PT"

CORE_VERTEX_IDS = (
    "C00_NOSE_TOP", "C01_BRIDGE", "C02_FOREHEAD", "C03_CROWN_FRONT",
    "C04_CROWN_REAR", "C05_NECK_DORSAL_HEAD", "C06_NECK_DORSAL_BASE",
    "C07_SHOULDER_FRONT", "C08_SHOULDER_DORSAL", "C09_BACK_FRONT",
    "C10_BACK_REAR", "C11_HAUNCH_DORSAL", "C12_RUMP", "C13_HAUNCH_VENTRAL",
    "C14_BELLY_REAR", "C15_BELLY_MID", "C16_BELLY_FRONT", "C17_STERNUM",
    "C18_CHEST_FRONT", "C19_NECK_VENTRAL_BASE", "C20_THROAT", "C21_JAW_REAR",
    "C22_MUZZLE_BOTTOM", "C23_NOSE_BOTTOM",
)
CORE_BOUNDARY_EDGES = tuple((CORE_VERTEX_IDS[i], CORE_VERTEX_IDS[(i + 1) % len(CORE_VERTEX_IDS)]) for i in range(len(CORE_VERTEX_IDS)))
PROFILE_SHAPE = ((1.08,-0.16),(1.02,-0.28),(0.92,-0.43),(0.82,-0.56),(0.66,-0.56),(0.54,-0.46),(0.42,-0.33),(0.28,-0.35),(0.12,-0.45),(-0.13,-0.48),(-0.40,-0.49),(-0.70,-0.54),(-0.96,-0.26),(-0.87,0.28),(-0.62,0.31),(-0.36,0.27),(-0.10,0.17),(0.08,0.21),(0.25,0.30),(0.36,0.15),(0.46,0.05),(0.60,0.01),(0.86,0.05),(1.08,-0.05))
THREE_QUARTER_SHAPE = ((0.75,-0.16),(0.70,-0.28),(0.62,-0.42),(0.52,-0.55),(0.37,-0.57),(0.24,-0.46),(0.12,-0.31),(-0.02,-0.32),(-0.18,-0.40),(-0.38,-0.43),(-0.57,-0.42),(-0.72,-0.36),(-0.80,-0.08),(-0.70,0.33),(-0.51,0.39),(-0.31,0.36),(-0.08,0.27),(0.09,0.30),(0.28,0.34),(0.36,0.17),(0.43,0.05),(0.51,0.00),(0.66,0.02),(0.76,-0.06))
FRONT_SHAPE = ((0.20,-0.22),(0.29,-0.32),(0.38,-0.46),(0.40,-0.59),(0.12,-0.64),(-0.14,-0.56),(-0.27,-0.39),(-0.48,-0.29),(-0.57,-0.13),(-0.61,0.07),(-0.60,0.26),(-0.51,0.45),(-0.31,0.56),(-0.12,0.59),(0.05,0.58),(0.22,0.56),(0.39,0.49),(0.53,0.35),(0.59,0.14),(0.34,-0.29),(0.28,-0.32),(0.21,-0.25),(0.20,-0.16),(0.21,-0.18))
CANONICAL_SHAPES = {"PROFILE":PROFILE_SHAPE,"THREE_QUARTER":THREE_QUARTER_SHAPE,"FRONT":FRONT_SHAPE}
CORE_SKIN_WEIGHTS = {
"C00_NOSE_TOP":{"HEAD":1.0},"C01_BRIDGE":{"HEAD":1.0},"C02_FOREHEAD":{"HEAD":1.0},"C03_CROWN_FRONT":{"HEAD":1.0},"C04_CROWN_REAR":{"HEAD":0.98,"FORE":0.02},"C05_NECK_DORSAL_HEAD":{"HEAD":0.85,"FORE":0.15},"C06_NECK_DORSAL_BASE":{"HEAD":0.55,"FORE":0.45},"C07_SHOULDER_FRONT":{"HEAD":0.20,"FORE":0.75,"BODY":0.05},"C08_SHOULDER_DORSAL":{"FORE":0.82,"BODY":0.18},"C09_BACK_FRONT":{"FORE":0.35,"BODY":0.60,"PELVIS":0.05},"C10_BACK_REAR":{"FORE":0.10,"BODY":0.68,"PELVIS":0.22},"C11_HAUNCH_DORSAL":{"BODY":0.20,"PELVIS":0.80},"C12_RUMP":{"PELVIS":1.0},"C13_HAUNCH_VENTRAL":{"BODY":0.10,"PELVIS":0.90},"C14_BELLY_REAR":{"BODY":0.38,"PELVIS":0.62},"C15_BELLY_MID":{"FORE":0.05,"BODY":0.72,"PELVIS":0.23},"C16_BELLY_FRONT":{"FORE":0.22,"BODY":0.70,"PELVIS":0.08},"C17_STERNUM":{"HEAD":0.02,"FORE":0.60,"BODY":0.38},"C18_CHEST_FRONT":{"HEAD":0.03,"FORE":0.82,"BODY":0.15},"C19_NECK_VENTRAL_BASE":{"HEAD":0.20,"FORE":0.78,"BODY":0.02},"C20_THROAT":{"HEAD":0.48,"FORE":0.52},"C21_JAW_REAR":{"HEAD":0.82,"FORE":0.18},"C22_MUZZLE_BOTTOM":{"HEAD":0.98,"FORE":0.02},"C23_NOSE_BOTTOM":{"HEAD":1.0}}
CANONICAL_ANCHOR_REFS = {view:dict(refs) for view,refs in fr1_v2.CANONICAL_ANCHOR_REFS.items()}
def _canonical_bytes(v): return json.dumps(v,sort_keys=True,separators=(",",":")).encode()
def _hash_json(v): return hashlib.sha256(_canonical_bytes(v)).hexdigest()
def canonical_view_weights(yaw_rad): return fr1.canonical_view_weights(yaw_rad)
def _shape_blend(weights):
    return [(sum(CANONICAL_SHAPES[n][i][0]*w for n,w in weights.items()),sum(CANONICAL_SHAPES[n][i][1]*w for n,w in weights.items())) for i in range(len(CORE_VERTEX_IDS))]
def _blended_reference_anchor(view_weights,skin):
    x=y=0.0
    for vn,vw in view_weights.items():
        refs=CANONICAL_ANCHOR_REFS[vn]; x+=vw*sum(refs[n][0]*w for n,w in skin.items()); y+=vw*sum(refs[n][1]*w for n,w in skin.items())
    return x,y
def build_core_vertices(fixture):
    state=fixture.state; yaw=float(fixture.payload.get("orientation",{}).get("yawRad",0.0)); vw=canonical_view_weights(yaw); shape=_shape_blend(vw); sx,sy=fr1._screen_scale(fixture,vw); out=[]
    for vid,(px,py) in zip(CORE_VERTEX_IDS,shape):
        skin=CORE_SKIN_WEIGHTS[vid]
        if abs(sum(skin.values())-1.0)>1e-12: raise RuntimeError((vid,skin))
        actual=fr1_v2._weighted_actual_anchor(state,skin); rx,ry=_blended_reference_anchor(vw,skin); out.append((vid,actual.x+(px-rx)*sx,actual.y+(py-ry)*sy))
    return tuple(out)
def topology_signature():
    return _hash_json({"coreVertexIds":CORE_VERTEX_IDS,"coreBoundaryEdges":CORE_BOUNDARY_EDGES,"skinWeightKeys":{v:tuple(sorted(CORE_SKIN_WEIGHTS[v])) for v in CORE_VERTEX_IDS},"coreAccessory":"EAR_PAIR_TRIANGLES_ATTACHED_TO_CORE","meshDomains":("CORE","FORE_L","FORE_R","HIND_L","HIND_R","TAIL")})
def build_probe(fixture,direction=+1):
    state=fixture.state; before=fr1._hash_json(fr1._anchor_payload(state)); yaw=float(fixture.payload.get("orientation",{}).get("yawRad",0.0)); core=build_core_vertices(fixture); ears=fr2_v5.build_ear_shapes(fixture); limbs=fr2_v5.build_limb_meshes(fixture); tail=fr2_v5.build_tail_mesh(fixture); after=fr1._hash_json(fr1._anchor_payload(state))
    return fr2_base.FR2ProbeResult(semantic_hash=fixture.semantic_hash,morphology_id=fixture.morphology_id,case_id=fixture.case_id,size_dp=int(fixture.size_dp),t=float(fixture.t),direction=int(direction),yaw_rad=yaw,view_weights=tuple(sorted(canonical_view_weights(yaw).items())),core_vertices=core,ear_shapes=ears,limb_meshes=limbs,tail_mesh=tail,topology_signature=topology_signature(),semantic_anchor_hash_before=before,semantic_anchor_hash_after=after,paw_pin_error_max=max(m["pawPinError"] for m in limbs),core_self_intersections=fr1.count_self_intersections(core),correction_families=tuple())
def result_dict(result):
    p=fr2_base.result_dict(result); p["version"]=PROTOTYPE_VERSION; return p
build_ear_shapes=fr2_v5.build_ear_shapes
build_limb_meshes=fr2_v5.build_limb_meshes
build_tail_mesh=fr2_v5.build_tail_mesh
limb_crossing_count=fr2_v5.limb_crossing_count
FR2ProbeResult=fr2_base.FR2ProbeResult
