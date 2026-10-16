from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location("stage_b_inspector", HERE/"p1_c_3d_cat_stage_b_inspector_v1.py")
_ins=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_ins)

STRUCTURAL_NODE_NAME="Cat continuous body"
EXPECTED_SOURCE_SHA256="6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5"

def topology_metrics(vertex_count, triangles):
    edge_counts=Counter(); directed=Counter(); tri_keys=Counter()
    degenerate=0
    for a,b,c in triangles:
        tri_keys[tuple(sorted((a,b,c)))] += 1
        if len({a,b,c}) < 3: degenerate += 1
        for u,v in ((a,b),(b,c),(c,a)):
            edge_counts[(min(u,v),max(u,v))] += 1
            directed[(u,v)] += 1
    boundary=sum(1 for n in edge_counts.values() if n==1)
    nonmanifold=sum(1 for n in edge_counts.values() if n>2)
    orientation_bad=0
    for (u,v),n in edge_counts.items():
        if n==2 and not (directed[(u,v)]==1 and directed[(v,u)]==1):
            orientation_bad += 1
    duplicate=sum(n-1 for n in tri_keys.values() if n>1)
    e=len(edge_counts); f=len(triangles); chi=vertex_count-e+f
    return {
        "vertexCount":vertex_count,"uniqueEdgeCount":e,"triangleCount":f,
        "eulerCharacteristic":chi,
        "edgeMultiplicityHistogram":{str(k):v for k,v in sorted(Counter(edge_counts.values()).items())},
        "boundaryEdgeCount":boundary,"nonManifoldEdgeCount":nonmanifold,
        "orientationMismatchEdgeCount":orientation_bad,
        "degenerateIndexTriangleCount":degenerate,"duplicateTriangleCount":duplicate,
        "closedTwoManifoldByIndexTopology": boundary==0 and nonmanifold==0 and orientation_bad==0 and degenerate==0,
        "genusIfConnectedClosedOrientable": (2-chi)/2,
    }

def diagnose(glb: Path):
    data,version,doc,bin_chunk,chunks=_ins.load_glb(glb)
    import hashlib
    sha=hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SOURCE_SHA256:
        raise ValueError(f"source hash drift: {sha}")
    matches=[(i,n) for i,n in enumerate(doc.get("nodes",[])) if n.get("name")==STRUCTURAL_NODE_NAME]
    if len(matches)!=1: raise ValueError(f"expected exactly one {STRUCTURAL_NODE_NAME!r}, got {len(matches)}")
    ni,node=matches[0]; mi=node.get("mesh")
    if mi is None: raise ValueError("structural node has no mesh")
    prims=doc["meshes"][mi].get("primitives",[])
    if len(prims)!=1: raise ValueError(f"expected one structural primitive, got {len(prims)}")
    p=prims[0]; pos_idx=p.get("attributes",{}).get("POSITION")
    if pos_idx is None: raise ValueError("missing POSITION")
    vertex_count=doc["accessors"][pos_idx]["count"]
    triangles,_,mode=_ins.primitive_triangles(doc,bin_chunk,p)
    if mode != 4: raise ValueError(f"expected TRIANGLES mode 4, got {mode}")
    metrics=topology_metrics(vertex_count,triangles)
    metrics.update({"version":"P1_C_3D_CAT_STAGE_B_TOPOLOGY_DIAGNOSTIC_V1","sourceSha256":sha,"structuralNodeName":STRUCTURAL_NODE_NAME,"nodeIndex":ni,"meshIndex":mi})
    return metrics

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("glb",type=Path); ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args(); r=diagnose(a.glb); a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n"); print(json.dumps(r,indent=2,sort_keys=True))
if __name__=="__main__": main()
