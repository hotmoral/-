"""Invented four-cell and asymmetric examples; no private geometry copied."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generic_training_geometry import normalize,rotate,mirror,orbit,distinct_shapes,placements,first_moves,guard_unscored

# Public synthetic 4-cell hooked board; not an authoritative private problem.
BOARD=[(0,0),(1,0),(2,0),(0,1)]
FIRST=[(0,0),(1,0)]
SECOND=[(0,0),(0,1)]

class TrainingMathChecks(unittest.TestCase):
    def test_translate_not_distinct(self):
        self.assertEqual(orbit(BOARD),orbit([(x+5,y-9) for x,y in BOARD]))
    def test_rotate_not_distinct(self):
        self.assertEqual(orbit(BOARD),orbit(rotate(BOARD)))
    def test_reflect_not_distinct(self):
        self.assertEqual(orbit(BOARD),orbit(mirror(BOARD)))
    def test_distinct_check_rejects_rotated_repeat(self):
        with self.assertRaises(ValueError):
            distinct_shapes([BOARD,rotate(BOARD)])
    def test_distinct_different_count(self):
        self.assertEqual(distinct_shapes([BOARD,[(0,0),(1,0),(2,0)]]),2)
    def test_toy_first_placement_has_yes_and_no(self):
        cases=first_moves(BOARD,FIRST,SECOND)
        self.assertEqual(sorted(label for cells,label in cases),["NO","YES"])
    def test_solved_remainder_verified(self):
        possibilities=first_moves(BOARD,FIRST,SECOND)
        self.assertTrue(any(state=="YES" for _,state in possibilities))
    def test_disconnected_remainder_is_blocked(self):
        possibilities=first_moves(BOARD,FIRST,SECOND)
        self.assertTrue(any(state=="NO" for _,state in possibilities))
    def test_learning_scene_cannot_submit(self):
        for event in ("SCORE","EVIDENCE","SUBMIT"):
            with self.subTest(event=event),self.assertRaises(ValueError):
                guard_unscored(role="TRAIN_A",event=event,assigned=False)
    def test_assessment_requires_assignment(self):
        with self.assertRaises(ValueError):
            guard_unscored(role="ASSESS",event="SUBMIT",assigned=False)
    def test_unscored_undo_allowed(self):
        self.assertTrue(guard_unscored(role="TRAIN_B",event="UNDO",assigned=False))
    def test_bad_cells_rejected(self):
        with self.assertRaises(ValueError):
            normalize([(0,0),(0,0)])

if __name__=="__main__":
    unittest.main()
