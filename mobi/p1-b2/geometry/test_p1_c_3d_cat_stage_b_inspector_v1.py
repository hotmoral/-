import json, struct, tempfile, unittest
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("inspector", HERE/"p1_c_3d_cat_stage_b_inspector_v1.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def pad4(b,pad=b" "):
    return b + pad*((4-len(b)%4)%4)

def make_glb(path):
    positions=[(0.,0.,0.),(1.,0.,0.),(1.,2.,0.),(0.,2.,0.)]
    indices=[0,1,2,0,2,3]
    pbytes=b"".join(struct.pack("<fff",*p) for p in positions)
    ibytes=b"".join(struct.pack("<H",i) for i in indices)
    binb=pad4(pbytes+ibytes,b"\x00")
    doc={
      "asset":{"version":"2.0","generator":"unit"},
      "scene":0,
      "scenes":[{"nodes":[0]}],
      "nodes":[{"mesh":0,"translation":[10,20,30],"name":"cat"}],
      "meshes":[{"name":"body","primitives":[{"attributes":{"POSITION":0},"indices":1,"mode":4}]}],
      "buffers":[{"byteLength":len(binb)}],
      "bufferViews":[
        {"buffer":0,"byteOffset":0,"byteLength":len(pbytes)},
        {"buffer":0,"byteOffset":len(pbytes),"byteLength":len(ibytes)}
      ],
      "accessors":[
        {"bufferView":0,"componentType":5126,"count":4,"type":"VEC3","min":[0,0,0],"max":[1,2,0]},
        {"bufferView":1,"componentType":5123,"count":6,"type":"SCALAR"}
      ]
    }
    js=pad4(json.dumps(doc,separators=(",",":")).encode())
    chunks=struct.pack("<II",len(js),0x4E4F534A)+js+struct.pack("<II",len(binb),0x004E4942)+binb
    data=struct.pack("<4sII",b"glTF",2,12+len(chunks))+chunks
    path.write_bytes(data)

class InspectorTests(unittest.TestCase):
    def test_basic_inspection(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.glb"; make_glb(p)
            r=m.inspect(p)
            self.assertEqual(r["file"]["glbVersion"],2)
            self.assertEqual(r["structure"]["meshCount"],1)
            self.assertEqual(r["structure"]["primitiveCount"],1)
            self.assertEqual(r["geometry"]["totalTriangleCount"],2)
            self.assertEqual(r["geometry"]["primitiveConnectedComponentCounts"],[1])
            self.assertEqual(r["geometry"]["worldBoundsMin"],[10.0,20.0,30.0])
            self.assertEqual(r["geometry"]["worldBoundsMax"],[11.0,22.0,30.0])
            self.assertEqual(r["geometry"]["worldExtents"],[1.0,2.0,0.0])
            self.assertEqual(r["geometry"]["nonFinitePositionScalars"],0)
    def test_bad_magic(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.glb"; p.write_bytes(b"bad")
            with self.assertRaises(ValueError): m.inspect(p)

if __name__=="__main__": unittest.main()
