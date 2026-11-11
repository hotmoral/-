"""Public, fully synthetic classroom-flow regression tests."""
from dataclasses import replace
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generic_teaching_flow import verify,example

class FlowRules(unittest.TestCase):
    def reject(self,mutate):
        x=example();mutate(x)
        with self.assertRaises(ValueError):verify(x)
    def test_valid(self):self.assertEqual(verify(example()),"PASS_SYNTHETIC_ONLY")
    def test_stale_intro(self):self.reject(lambda x:x.__setitem__(1,replace(x[1],stimulus="z")))
    def test_fading_not_new(self):self.reject(lambda x:x.__setitem__(3,replace(x[3],stimulus="a")))
    def test_assessment_reuses_intro(self):self.reject(lambda x:x.__setitem__(4,replace(x[4],stimulus="a")))
    def test_assessment_reuses_faded(self):self.reject(lambda x:x.__setitem__(4,replace(x[4],stimulus="b")))
    def test_training_scored(self):self.reject(lambda x:x.__setitem__(1,replace(x[1],role="SCORE")))
    def test_answer_leak(self):self.reject(lambda x:x.__setitem__(4,replace(x[4],answer_revealed=True)))
    def test_unreleased(self):
        with self.assertRaises(ValueError):verify(example(),released=False)
    def test_assisted_not_independent(self):
        with self.assertRaises(ValueError):verify(example(),assisted=True)
    def test_debrief_not_rescore(self):self.reject(lambda x:x.__setitem__(5,replace(x[5],role="SCORE")))

if __name__=="__main__":unittest.main()
