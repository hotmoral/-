import importlib.util, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("render", HERE/"p1_c_3d_cat_stage_d_projection_v1.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class ProjectionTests(unittest.TestCase):
    def test_frozen_center_and_ground_mapping(self):
        x,y=m.project_point((m.CENTER_X,m.GROUND_Y,m.CENTER_Z),0.0)
        self.assertAlmostEqual(x,48.0,places=12)
        self.assertAlmostEqual(y,91.0,places=12)
        x2,y2=m.project_point((m.CENTER_X,m.GROUND_Y,m.CENTER_Z),90.0)
        self.assertAlmostEqual(x2,48.0,places=12)
        self.assertAlmostEqual(y2,91.0,places=12)
    def test_profile_front_maps_screen_right(self):
        # +Z anatomical front must point screen-right at 90 deg profile.
        a=m.project_point((m.CENTER_X,m.GROUND_Y,m.CENTER_Z),90.0)[0]
        b=m.project_point((m.CENTER_X,m.GROUND_Y,m.CENTER_Z+0.1),90.0)[0]
        self.assertGreater(b,a)
    def test_triangle_raster_and_metrics(self):
        pts=[(1.0,1.0),(5.0,1.0),(1.0,5.0)]
        mask=m.rasterize(pts,[(0,1,2)],width=8,height=8)
        r=m.mask_metrics(mask,width=8,height=8)
        self.assertGreater(r['occupiedPixels'],0)
        self.assertEqual(r['components8'],1)
        self.assertEqual(r['bbox'],[1,1,4,4])
    def test_png_deterministic(self):
        gray=bytes([0,255,255,0])
        a=m.png_gray(2,2,gray); b=m.png_gray(2,2,gray)
        self.assertEqual(a,b)
        self.assertTrue(a.startswith(b'\x89PNG\r\n\x1a\n'))
    def test_nearest_upscale_exact(self):
        w,h,p=m.upscale_nearest(bytes([0,255,128,64]),2,2,2)
        self.assertEqual((w,h),(4,4))
        self.assertEqual(p,bytes([0,0,255,255,0,0,255,255,128,128,64,64,128,128,64,64]))

if __name__=='__main__': unittest.main()
