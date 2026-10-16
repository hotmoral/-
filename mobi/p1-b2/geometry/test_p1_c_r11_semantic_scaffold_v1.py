import hashlib, unittest
import numpy as np
import p1_c_r11_semantic_scaffold_v1 as r

class R11Stage0Tests(unittest.TestCase):
    def test_role_contract_exact(self):
        self.assertEqual(len(r.ROLE_ORDER),30); self.assertEqual(len(set(r.ROLE_ORDER)),30)
        self.assertEqual(sum(r.ROLE_DOMAIN[x]=="CORE" for x in r.ROLE_ORDER),6)
        self.assertEqual(sum(r.ROLE_DOMAIN[x]=="FORE_L" for x in r.ROLE_ORDER),5)
        self.assertEqual(sum(r.ROLE_DOMAIN[x]=="FORE_R" for x in r.ROLE_ORDER),5)
        self.assertEqual(sum(r.ROLE_DOMAIN[x]=="HIND_L" for x in r.ROLE_ORDER),4)
        self.assertEqual(sum(r.ROLE_DOMAIN[x]=="HIND_R" for x in r.ROLE_ORDER),4)
        self.assertEqual(sum(r.ROLE_DOMAIN[x]=="TAIL" for x in r.ROLE_ORDER),6)
        self.assertIsNone(r.PARENT["BODY_ROOT_CTRL"])
        self.assertEqual(set(r.PARENT),set(r.ROLE_ORDER))
        roots=[x for x in r.ROLE_ORDER if r.PARENT[x] is None]; self.assertEqual(roots,["BODY_ROOT_CTRL"])
        for role in r.ROLE_ORDER:
            seen=set(); cur=role
            while cur is not None:
                self.assertNotIn(cur,seen); seen.add(cur); cur=r.PARENT[cur]

    def test_mesh_hash_is_order_sensitive_and_stable(self):
        v=np.array([[0,0,0],[1,0,0],[0,1,0]],float); f=np.array([[0,1,2]],np.int32)
        a=r.mesh_array_sha256(v,f); b=r.mesh_array_sha256(v.copy(),f.copy())
        self.assertEqual(a,b); self.assertNotEqual(a,r.mesh_array_sha256(v[[1,0,2]],f))
        self.assertEqual(len(a),64)

    def test_graph_shortest_path_tie_is_deterministic(self):
        a=(0,0,0); b=(1,0,0); c=(0,1,0); d=(1,1,0)
        g={a:{b,c},b:{a,d},c:{a,d},d:{b,c}}
        p1,_=r.shortest_path(g,a,d,1.0); p2,_=r.shortest_path(g,a,d,1.0)
        self.assertEqual(p1,p2); self.assertEqual(p1,[a,c,d] if c<b else [a,b,d])

    def test_terminal_pruning_protects_anchor(self):
        g={(0,0,0):{(1,0,0)},(1,0,0):{(0,0,0),(2,0,0),(1,1,0)},(2,0,0):{(1,0,0)},(1,1,0):{(1,0,0)}}
        out=r.prune_graph(g,{(2,0,0)},0.01,1.0)
        self.assertIn((2,0,0),out)

    def test_curvature_fallback_is_predeclared(self):
        p=np.stack([np.linspace(0,1,10),np.zeros(10),np.zeros(10)],axis=1)
        x=r.select_internal_points(p,3,(0.2,0.5,0.8))
        self.assertEqual([z[2] for z in x],["FALLBACK_ARC_QUANTILE"]*3)
        self.assertEqual([round(z[0],2) for z in x],[0.2,0.5,0.8])

    def test_domain_gating_and_weights_no_cross_side(self):
        controls=[]
        # Synthetic positions preserve exact 30-role vocabulary; domains separated in x.
        for i,role in enumerate(r.ROLE_ORDER):
            dom=r.ROLE_DOMAIN[role]; x={"FORE_L":2,"HIND_L":2,"FORE_R":-2,"HIND_R":-2,"CORE":0,"TAIL":0}[dom]
            z={"FORE_L":2,"FORE_R":2,"HIND_L":-2,"HIND_R":-2,"CORE":0,"TAIL":-3}[dom]
            controls.append(r.Control(role,r.PARENT[role],dom,(x+0.01*i,0,z),r.PROVENANCE[role],"TEST"))
        verts=np.array([[2,0,2],[-2,0,2],[2,0,-2],[-2,0,-2],[0,0,0],[0,0,-3]],float)
        domains=np.array(["FORE_L","FORE_R","HIND_L","HIND_R","CORE","TAIL"]); interfaces=np.zeros(6,bool)
        idx,w=r.build_weights(verts,controls,domains,interfaces,0.1)
        self.assertTrue(np.allclose(w.sum(axis=1),1.0,atol=1e-12))
        for i,d in enumerate(domains):
            roles=[r.ROLE_ORDER[int(q)] for q in idx[i] if int(q)!=255]
            self.assertTrue(all(r.ROLE_DOMAIN[x]==d for x in roles))

    def test_weight_serialization_stable(self):
        idx=np.array([[0,1,255,255]],dtype=np.uint8); w=np.array([[0.75,0.25,0,0]],float)
        a=r.serialize_weights(idx,w); b=r.serialize_weights(idx.copy(),w.copy())
        self.assertEqual(a,b); self.assertTrue(a.startswith(r.WEIGHT_HASH_PREFIX)); self.assertEqual(hashlib.sha256(a).hexdigest(),hashlib.sha256(b).hexdigest())

    def test_rest_lbs_identity(self):
        controls=[r.Control(role,r.PARENT[role],r.ROLE_DOMAIN[role],(0,0,0),r.PROVENANCE[role],"TEST") for role in r.ROLE_ORDER]
        v=np.array([[1.2,-0.3,0.7]],float); idx=np.array([[0,1,2,3]],dtype=np.uint8); w=np.array([[0.1,0.2,0.3,0.4]],float)
        out=r.rest_lbs(v,controls,idx,w); self.assertTrue(np.allclose(out,v,rtol=0,atol=2e-16))

if __name__=="__main__": unittest.main()
