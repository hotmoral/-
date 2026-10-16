from __future__ import annotations
import argparse, binascii, hashlib, importlib.util, json, math, struct, zlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location("stage_b_inspector", HERE/"p1_c_3d_cat_stage_b_inspector_v1.py")
_ins=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_ins)

VERSION="P1_C_3D_CAT_STAGE_D_PROJECTION_V1"
EXPECTED_SOURCE_SHA256="6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5"
STRUCTURAL_NODE_NAME="Cat continuous body"
CANVAS=96
SCALE=111.37388017614773
CENTER_X=2.7641654014587402e-06
CENTER_Z=-0.018680110573768616
GROUND_Y=0.0055554211139678955
SCREEN_CENTER_X=48.0
GROUND_SCREEN_Y=91.0
EPSILON=1e-9
VIEWS=[
    ("EXACT_FRONT",0.0),
    ("NEAR_FRONT",22.5),
    ("STRONG_3Q",45.0),
    ("NEAR_PROFILE",67.5),
    ("EXACT_PROFILE",90.0),
]

def _chunk(kind: bytes, payload: bytes)->bytes:
    return struct.pack(">I",len(payload))+kind+payload+struct.pack(">I",binascii.crc32(kind+payload)&0xffffffff)

def png_gray(width:int,height:int,pixels:bytes)->bytes:
    if len(pixels)!=width*height: raise ValueError("pixel length mismatch")
    raw=b"".join(b"\x00"+pixels[y*width:(y+1)*width] for y in range(height))
    ihdr=struct.pack(">IIBBBBB",width,height,8,0,0,0,0)
    return b"\x89PNG\r\n\x1a\n"+_chunk(b"IHDR",ihdr)+_chunk(b"IDAT",zlib.compress(raw,9))+_chunk(b"IEND",b"")

def mask_to_gray(mask: bytearray|bytes)->bytes:
    return bytes(0 if v else 255 for v in mask)

def upscale_nearest(gray:bytes,w:int,h:int,factor:int)->tuple[int,int,bytes]:
    rows=[]
    for y in range(h):
        row=gray[y*w:(y+1)*w]
        big=b"".join(bytes([v])*factor for v in row)
        rows.extend([big]*factor)
    return w*factor,h*factor,b"".join(rows)

def combine_horizontal(grays:list[bytes],w:int,h:int)->tuple[int,int,bytes]:
    return w*len(grays),h,b"".join(b"".join(g[y*w:(y+1)*w] for g in grays) for y in range(h))

def project_point(p,deg:float):
    x,y,z=p; th=math.radians(deg); c=math.cos(th); s=math.sin(th)
    screen_x=SCREEN_CENTER_X+SCALE*((x-CENTER_X)*c+(z-CENTER_Z)*s)
    screen_y=GROUND_SCREEN_Y-SCALE*(y-GROUND_Y)
    return (screen_x,screen_y)

def rasterize(projected:list[tuple[float,float]],triangles:list[tuple[int,int,int]],width:int=CANVAS,height:int=CANVAS)->bytearray:
    mask=bytearray(width*height)
    for ia,ib,ic in triangles:
        ax,ay=projected[ia]; bx,by=projected[ib]; cx,cy=projected[ic]
        minx=min(ax,bx,cx); maxx=max(ax,bx,cx); miny=min(ay,by,cy); maxy=max(ay,by,cy)
        ix0=max(0,math.ceil(minx-0.5)); ix1=min(width-1,math.floor(maxx-0.5))
        iy0=max(0,math.ceil(miny-0.5)); iy1=min(height-1,math.floor(maxy-0.5))
        if ix0>ix1 or iy0>iy1: continue
        area=(bx-ax)*(cy-ay)-(by-ay)*(cx-ax)
        if abs(area)<1e-14: continue
        for iy in range(iy0,iy1+1):
            py=iy+0.5; row=iy*width
            for ix in range(ix0,ix1+1):
                if mask[row+ix]: continue
                px=ix+0.5
                e0=(bx-ax)*(py-ay)-(by-ay)*(px-ax)
                e1=(cx-bx)*(py-by)-(cy-by)*(px-bx)
                e2=(ax-cx)*(py-cy)-(ay-cy)*(px-cx)
                if ((e0>=-EPSILON and e1>=-EPSILON and e2>=-EPSILON) or
                    (e0<=EPSILON and e1<=EPSILON and e2<=EPSILON)):
                    mask[row+ix]=1
    return mask

def mask_metrics(mask:bytearray|bytes,width:int=CANVAS,height:int=CANVAS):
    occupied=[i for i,v in enumerate(mask) if v]
    if not occupied: return {"occupiedPixels":0,"bbox":None,"centroid":None,"components8":0}
    xs=[i%width for i in occupied]; ys=[i//width for i in occupied]
    live=set(occupied); components=0
    while live:
        components+=1; start=live.pop(); stack=[start]
        while stack:
            q=stack.pop(); x=q%width; y=q//width
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    if dx==0 and dy==0: continue
                    nx=x+dx; ny=y+dy
                    if 0<=nx<width and 0<=ny<height:
                        ni=ny*width+nx
                        if ni in live: live.remove(ni); stack.append(ni)
    n=len(occupied)
    return {"occupiedPixels":n,"bbox":[min(xs),min(ys),max(xs),max(ys)],"centroid":[sum(xs)/n,sum(ys)/n],"components8":components}

def load_structural_mesh(glb:Path):
    data,version,doc,bin_chunk,_=_ins.load_glb(glb)
    sha=hashlib.sha256(data).hexdigest()
    if sha!=EXPECTED_SOURCE_SHA256: raise ValueError(f"source hash drift: {sha}")
    matches=[n for n in doc.get("nodes",[]) if n.get("name")==STRUCTURAL_NODE_NAME]
    if len(matches)!=1: raise ValueError(f"expected one structural node, got {len(matches)}")
    node=matches[0]; mesh=doc["meshes"][node["mesh"]]; prims=mesh.get("primitives",[])
    if len(prims)!=1: raise ValueError("structural mesh primitive count drift")
    p=prims[0]; pos_idx=p["attributes"]["POSITION"]
    local=_ins.accessor_values(doc,bin_chunk,pos_idx)
    # Frozen source currently uses translation only on the structural node. Use inspector TRS helper for safety.
    wm=_ins._trs(node.get("translation"),node.get("rotation"),node.get("scale")) if "matrix" not in node else [float(x) for x in node["matrix"]]
    verts=[_ins._transform_point(wm,v[:3]) for v in local]
    tris,_,mode=_ins.primitive_triangles(doc,bin_chunk,p)
    if mode!=4: raise ValueError("structural primitive mode drift")
    if len(verts)!=99642 or len(tris)!=199280: raise ValueError("structural count drift")
    return verts,tris,sha

def render(glb:Path,out:Path):
    verts,tris,sha=load_structural_mesh(glb); out.mkdir(parents=True,exist_ok=True)
    reports=[]; natives=[]
    for name,deg in VIEWS:
        projected=[project_point(p,deg) for p in verts]
        mask=rasterize(projected,tris)
        gray=mask_to_gray(mask); natives.append(gray)
        native_name=f"P1C_3D_CAT_{name}_96.png"; enlarged_name=f"P1C_3D_CAT_{name}_96_8X.png"
        (out/native_name).write_bytes(png_gray(CANVAS,CANVAS,gray))
        bw,bh,bgray=upscale_nearest(gray,CANVAS,CANVAS,8)
        (out/enlarged_name).write_bytes(png_gray(bw,bh,bgray))
        r=mask_metrics(mask); r.update({"name":name,"yawDeg":deg,"nativePng":native_name,"enlargedPng":enlarged_name})
        reports.append(r)
    sw,sh,sgray=combine_horizontal(natives,CANVAS,CANVAS)
    (out/"P1C_3D_CAT_VIEW_STRIP_96.png").write_bytes(png_gray(sw,sh,sgray))
    ew,eh,egray=upscale_nearest(sgray,sw,sh,8)
    (out/"P1C_3D_CAT_VIEW_STRIP_96_8X.png").write_bytes(png_gray(ew,eh,egray))
    summary={
        "version":VERSION,"sourceSha256":sha,"structuralNodeName":STRUCTURAL_NODE_NAME,
        "canvas":[CANVAS,CANVAS],"projection":"orthographic","pixelRule":"projected triangle union at native pixel centers",
        "scalePxPerMeter":SCALE,"centerXZ":[CENTER_X,CENTER_Z],"groundY":GROUND_Y,
        "screenCenterX":SCREEN_CENTER_X,"groundScreenY":GROUND_SCREEN_Y,"epsilon":EPSILON,
        "vertexCount":len(verts),"triangleCount":len(tris),"views":reports,
        "stripNative":"P1C_3D_CAT_VIEW_STRIP_96.png","stripEnlarged":"P1C_3D_CAT_VIEW_STRIP_96_8X.png",
    }
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return summary

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("glb",type=Path); ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args(); print(json.dumps(render(a.glb,a.out),indent=2,sort_keys=True))
if __name__=="__main__": main()
