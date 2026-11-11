"""Synthetic-only course activity cases; no private project fixtures."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))

from generic_lesson_flow import ToyActivity, check_play, classify, positive_process

DIRECT=ToyActivity("DIRECT",("TURN","UNDO"))
MIRROR=ToyActivity("DIRECT",("MIRROR","UNDO"))
MENTAL=ToyActivity("PREDICT",("CHOOSE","COMMIT"),True,True)
LESSON=ToyActivity("TRAINING",("TURN","UNDO"))
DRAFT=ToyActivity("EXTENSION",("PLACE","UNDO"),False,False,False)


class GenericLessonFlowTests(unittest.TestCase):
    def test_direct_rotation(self):
        self.assertEqual(check_play(DIRECT,["TURN","UNDO","TURN","SUBMIT"])["submitCount"],1)

    def test_direct_mirror(self):
        self.assertEqual(check_play(MIRROR,["MIRROR","SUBMIT"])["submitCount"],1)

    def test_mental_choice_and_after_commit_replay(self):
        self.assertEqual(check_play(MENTAL,["CHOOSE","COMMIT","REPLAY","SUBMIT"]),
                         {"submitCount":1,"firstChoiceRetained":True,"committed":True})

    def test_no_rotate_before_mental_commit(self):
        with self.assertRaises(ValueError):
            check_play(MENTAL,["TURN","CHOOSE","COMMIT"])

    def test_no_replay_or_solution_before_commit(self):
        for trace in (["REPLAY","CHOOSE","COMMIT"],["SHOW_SOLUTION","CHOOSE","COMMIT"]):
            with self.subTest(trace=trace),self.assertRaises(ValueError):
                check_play(MENTAL,trace)

    def test_unauthorized_hint_or_undo(self):
        for trace in (["HINT"],["UNDO","CHOOSE","COMMIT"]):
            with self.subTest(trace=trace),self.assertRaises(ValueError):
                check_play(MENTAL,trace)

    def test_teaching_does_not_submit(self):
        with self.assertRaises(ValueError):
            check_play(LESSON,["TURN","SUBMIT"])

    def test_unapproved_extension_not_submit(self):
        with self.assertRaises(ValueError):
            check_play(DRAFT,["PLACE","SUBMIT"])

    def test_score_cannot_be_submitted_twice(self):
        with self.assertRaises(ValueError):
            check_play(DIRECT,["TURN","SUBMIT","SUBMIT"])

    def test_assistance_prevents_independent(self):
        self.assertEqual(classify(solved=True,helped=True,corrected=False),
                         "ASSISTED_SUCCESS")

    def test_undo_without_error_not_self_correction(self):
        self.assertEqual(classify(solved=True,helped=False,corrected=False),
                         "INDEPENDENT_SUCCESS")

    def test_technical_abort_not_learner_failure(self):
        self.assertEqual(classify(solved=False,helped=False,corrected=False,technical_abort=True),
                         "UNSCORED_TECHNICAL")

    def test_unknown_or_illegal_not_positive_process(self):
        self.assertTrue(positive_process(legal=True,future="YES",actual_move=True))
        self.assertFalse(positive_process(legal=True,future="UNKNOWN",actual_move=True))
        self.assertFalse(positive_process(legal=True,future="NO",actual_move=True))
        self.assertFalse(positive_process(legal=False,future="YES",actual_move=True))
        self.assertFalse(positive_process(legal=True,future="YES",actual_move=False))


if __name__=="__main__":
    unittest.main()
