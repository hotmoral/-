from __future__ import annotations
import argparse, json, math, struct, hashlib
from pathlib import Path
from collections import defaultdict

COMPONENT_FORMAT = {
    5120: ("b", 1),
    5121: ("B", 1),
    5122: ("h", 2),
    5123: ("H", 2),
    5125: ("I", 4),
    5126: ("f", 4),
}
TYPE_COMPONENTS = {"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4,"MAT2":4,"MAT3":9,"MAT4":16}

def _identity():
    return [1.0,0.0,0.0,0.0, 0.0,1.0,0.0,0.0, 0.0,0.0,1.0,0.0, 0.0,0.0,0.0,1.0]

def _matmul(a,b):
    out=[0.0]*16
    for r in range(4):
        for c in range(4):
            out[c*4+r]=sum(a[k*4+r]*b[c*4+k] for k in range(4))
    return out

def _trs(t=None,r=None,s=None):
    tx,ty,tz=(t or [0,0,0])
    qx,qy,qz,qw=(r or [0,0,0,1])
    sx,sy,sz=(s or [1,1,1])
    xx,yy,zz=qx*qx,qy*qy,qz*qz
    xy,xz,yz=qx*qy,qx*qz,qy*qz
    wx,wy,wz=qw*qx,qw*qy,qw*qz
    rot=[
        1-2*(yy+zz), 2*(xy+wz), 2*(xz-wy), 0,
        2*(xy-wz), 1-2*(xx+zz), 2*(yz+wx), 0,
        2*(xz+wy), 2*(yz-wx), 1-2*(xx+yy), 0,
        0,0,0,1
    ]
    scale=[sx,0,0,0, 0,sy,0,0, 0,0,sz,0, 0,0,0,1]
    trans=_identity(); trans[12],trans[13],trans[14]=tx,ty,tz
    return _matmul(trans,_matmul(rot,scale))

def _transform_point(m,p):
    x,y,z=p
    return (
        m[0]*x+m[4]*y+m[8]*z+m[12],
        m[1]*x+m[5]*y+m[9]*z+m[13],
        m[2]*x+m[6]*y+m[10]*z+m[14],
    )

def load_glb(path: Path):
    data=path.read_bytes()
    if len(data)<20: raise ValueError("too short for GLB")
    magic,version,length=struct.unpack_from("<4sII",data,0)
    if magic != b"glTF": raise ValueError(f"bad magic {magic!r}")
    if length != len(data): raise ValueError(f"header length {length} != file size {len(data)}")
    off=12; js=None; bins=[]; chunks=[]
    while off < len(data):
        if off+8>len(data): raise ValueError("truncated chunk header")
        clen,ctype=struct.unpack_from("<II",data,off); off+=8
        if off+clen>len(data): raise ValueError("truncated chunk")
        payload=data[off:off+clen]; off+=clen
        chunks.append({"type":ctype,"length":clen})
        if ctype == 0x4E4F534A:
            if js is not None: raise ValueError("multiple JSON chunks")
            js=json.loads(payload.rstrip(b" \t\r\n\x00").decode("utf-8"))
        elif ctype == 0x004E4942:
            bins.append(payload)
    if js is None: raise ValueError("missing JSON chunk")
    if len(bins)>1: raise ValueError("multiple BIN chunks unsupported for bounded inspector")
    return data,version,js,(bins[0] if bins else b""),chunks

def accessor_values(doc,bin_chunk,index):
    a=doc["accessors"][index]
    if "sparse" in a: raise ValueError(f"sparse accessor unsupported: {index}")
    if "bufferView" not in a: raise ValueError(f"accessor without bufferView unsupported: {index}")
    bv=doc["bufferViews"][a["bufferView"]]
    if bv.get("buffer",0) != 0: raise ValueError("external/multiple buffers unsupported in GLB inspector")
    ctype=a["componentType"]; fmt,size=COMPONENT_FORMAT[ctype]
    ncomp=TYPE_COMPONENTS[a["type"]]
    elem_size=size*ncomp
    stride=bv.get("byteStride",elem_size)
    if stride < elem_size: raise ValueError("invalid byteStride")
    base=bv.get("byteOffset",0)+a.get("byteOffset",0)
    count=a["count"]; out=[]; unpack="<"+fmt*ncomp
    for i in range(count):
        pos=base+i*stride
        if pos+elem_size>len(bin_chunk): raise ValueError(f"accessor {index} out of BIN bounds")
        vals=struct.unpack_from(unpack,bin_chunk,pos)
        out.append(vals[0] if ncomp==1 else vals)
    return out

def primitive_triangles(doc,bin_chunk,p):
    mode=p.get("mode",4)
    pos_idx=p.get("attributes",{}).get("POSITION")
    if pos_idx is None: return [],0,None
    vcount=doc["accessors"][pos_idx]["count"]
    seq=[int(x) for x in accessor_values(doc,bin_chunk,p["indices"])] if "indices" in p else list(range(vcount))
    tris=[]
    if mode==4:
        tris=[tuple(seq[i:i+3]) for i in range(0,len(seq)-2,3)]
    elif mode==5:
        for i in range(len(seq)-2):
            a,b,c=seq[i],seq[i+1],seq[i+2]
            tris.append((b,a,c) if i%2 else (a,b,c))
    elif mode==6:
        if seq: tris=[(seq[0],seq[i],seq[i+1]) for i in range(1,len(seq)-1)]
    return tris,len(seq),mode

def component_count(vertex_count,tris):
    if vertex_count==0: return 0
    used=set(); adj=defaultdict(set)
    for tri in tris:
        if len(set(tri))<3: continue
        for v in tri: used.add(v)
        a,b,c=tri
        adj[a].update((b,c)); adj[b].update((a,c)); adj[c].update((a,b))
    seen=set(); comps=0
    for start in sorted(used):
        if start in seen: continue
        comps+=1; stack=[start]; seen.add(start)
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); stack.append(v)
    if not tris and vertex_count: return vertex_count
    return comps

def inspect(path: Path):
    data,glb_version,doc,bin_chunk,chunks=load_glb(path)
    nodes=doc.get("nodes",[]); meshes=doc.get("meshes",[]); scenes=doc.get("scenes",[])
    default_scene=doc.get("scene",0 if scenes else None)
    primitive_reports=[]; local_positions={}
    total_vertex_refs=0; total_index_refs=0; total_triangles=0; morph_target_sets=0; nonfinite=0; primitive_connected=[]

    for mi,m in enumerate(meshes):
        for pi,p in enumerate(m.get("primitives",[])):
            pos_idx=p.get("attributes",{}).get("POSITION"); vcount=0
            if pos_idx is not None:
                vals=accessor_values(doc,bin_chunk,pos_idx); local_positions[pos_idx]=vals
                vcount=len(vals); total_vertex_refs += vcount
                for vv in vals:
                    if not all(math.isfinite(float(x)) for x in vv[:3]): nonfinite += 1
            tris,icount,mode=primitive_triangles(doc,bin_chunk,p)
            total_index_refs += icount; total_triangles += len(tris)
            cc=component_count(vcount,tris) if mode in (4,5,6) else None
            if cc is not None: primitive_connected.append(cc)
            morph=len(p.get("targets",[])); morph_target_sets += morph
            mats=doc.get("materials",[]); mat_idx=p.get("material")
            primitive_reports.append({
                "meshIndex":mi,"meshName":m.get("name"),"primitiveIndex":pi,
                "mode":mode,"positionAccessor":pos_idx,"vertexCount":vcount,
                "indexCount":icount,"triangleCount":len(tris),
                "connectedComponentsByIndexGraph":cc,"materialIndex":mat_idx,
                "materialName":mats[mat_idx].get("name") if mat_idx is not None and mat_idx < len(mats) else None,
                "morphTargetCount":morph,"attributes":sorted(p.get("attributes",{}).keys()),
            })

    def node_local(n):
        if "matrix" in n:
            if len(n["matrix"])!=16: raise ValueError("bad node matrix")
            return [float(x) for x in n["matrix"]]
        return _trs(n.get("translation"),n.get("rotation"),n.get("scale"))

    world_min=[math.inf]*3; world_max=[-math.inf]*3; scene_mesh_nodes=[]
    def visit(ni,parent,ancestry):
        if ni in ancestry: raise ValueError("cycle in node graph")
        n=nodes[ni]; wm=_matmul(parent,node_local(n))
        if "mesh" in n:
            mi=n["mesh"]
            scene_mesh_nodes.append({"nodeIndex":ni,"nodeName":n.get("name"),"meshIndex":mi,"meshName":meshes[mi].get("name")})
            for p in meshes[mi].get("primitives",[]):
                pos_idx=p.get("attributes",{}).get("POSITION")
                if pos_idx is None: continue
                vals=local_positions.get(pos_idx) or accessor_values(doc,bin_chunk,pos_idx)
                for v in vals:
                    q=_transform_point(wm,v[:3])
                    for k in range(3):
                        world_min[k]=min(world_min[k],q[k]); world_max[k]=max(world_max[k],q[k])
        ancestry=ancestry|{ni}
        for ci in n.get("children",[]): visit(ci,wm,ancestry)

    if scenes and default_scene is not None:
        for root in scenes[default_scene].get("nodes",[]): visit(root,_identity(),set())
    elif nodes:
        childset={c for n in nodes for c in n.get("children",[])}
        for root in [i for i in range(len(nodes)) if i not in childset]: visit(root,_identity(),set())

    finite_bounds=all(math.isfinite(x) for x in world_min+world_max)
    if finite_bounds: ext=[world_max[i]-world_min[i] for i in range(3)]
    else: world_min=world_max=ext=None

    mats=doc.get("materials",[])
    return {
        "version":"P1_C_3D_CAT_STAGE_B_INSPECTOR_V1",
        "file":{"name":path.name,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"glbVersion":glb_version,"declaredAssetVersion":doc.get("asset",{}).get("version"),"generator":doc.get("asset",{}).get("generator"),"chunks":chunks},
        "structure":{"sceneCount":len(scenes),"defaultScene":default_scene,"nodeCount":len(nodes),"meshCount":len(meshes),"meshNodeCountInDefaultScene":len(scene_mesh_nodes),"primitiveCount":len(primitive_reports),"materialCount":len(mats),"skinCount":len(doc.get("skins",[])),"animationCount":len(doc.get("animations",[])),"cameraCount":len(doc.get("cameras",[])),"textureCount":len(doc.get("textures",[])),"imageCount":len(doc.get("images",[])),"samplerCount":len(doc.get("samplers",[])),"morphTargetSetCount":morph_target_sets,"accessorCount":len(doc.get("accessors",[])),"bufferViewCount":len(doc.get("bufferViews",[])),"bufferCount":len(doc.get("buffers",[]))},
        "geometry":{"totalPrimitiveVertexReferences":total_vertex_refs,"totalPrimitiveIndexReferences":total_index_refs,"totalTriangleCount":total_triangles,"primitiveConnectedComponentCounts":primitive_connected,"nonFinitePositionScalars":nonfinite,"worldBoundsMin":world_min,"worldBoundsMax":world_max,"worldExtents":ext},
        "materials":[{"index":i,"name":m.get("name"),"doubleSided":m.get("doubleSided",False),"alphaMode":m.get("alphaMode","OPAQUE")} for i,m in enumerate(mats)],
        "meshNodes":scene_mesh_nodes,"primitives":primitive_reports,
        "extensionsUsed":doc.get("extensionsUsed",[]),"extensionsRequired":doc.get("extensionsRequired",[]),
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("glb",type=Path); ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args(); report=inspect(args.glb); args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=="__main__": main()
