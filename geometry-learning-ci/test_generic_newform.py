"""Generic synthetic-only checks, deliberately unrelated to private content."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generic_newform import Attempt, summarize


def training():
    return [Attempt("sample-a", "dots", "FIRST_TRY"),
            Attempt("sample-b", "edges", "FIRST_TRY"),
            Attempt("sample-c", "dots", "FIRST_TRY")]


class GenericFreshExampleChecks(unittest.TestCase):
    def test_guided_does_not_prove_independent(self):
        seq=[Attempt("a","dots","GUIDED"),Attempt("b","edges","GUIDED"),Attempt("c","dots","GUIDED")]
        self.assertEqual(summarize(seq)[0],"INSUFFICIENT")

    def test_self_corrected_is_not_first_try(self):
        seq=[Attempt("a","dots","CORRECTED"),Attempt("b","edges","CORRECTED"),Attempt("c","dots","CORRECTED")]
        self.assertEqual(summarize(seq)[0],"INSUFFICIENT")

    def test_diverse_training_enough_but_not_novel_assessment(self):
        self.assertEqual(summarize(training()),("PREPARED","NOT_ASSESSED","NOT_ASSESSED"))

    def test_one_presentation_family_does_not_count_as_diverse(self):
        self.assertEqual(summarize([Attempt(f"x{i}","dots","FIRST_TRY") for i in range(3)])[0],"INSUFFICIENT")

    def test_training_example_reuse_is_not_fresh_assessment(self):
        seq=training()+[Attempt("sample-a","dots","FIRST_TRY","NEW_PROBE")]
        self.assertEqual(summarize(seq)[1],"INCONCLUSIVE")

    def test_new_probe_requires_independent_first_try(self):
        seq=training()+[Attempt("new","faces","CORRECTED","NEW_PROBE")]
        self.assertEqual(summarize(seq)[1],"INCONCLUSIVE")

    def test_new_probe_enables_generalization_evidence_not_retention(self):
        seq=training()+[Attempt("new","faces","FIRST_TRY","NEW_PROBE")]
        self.assertEqual(summarize(seq),("PREPARED","SUPPORTED","PENDING"))

    def test_delayed_evidence_must_be_new_and_verified(self):
        seq=training()+[Attempt("new","faces","FIRST_TRY","NEW_PROBE")]
        self.assertEqual(summarize(seq+[Attempt("later","boundary","FIRST_TRY","LATE_PROBE",True)])[2],"SUPPORTED")
        self.assertEqual(summarize(seq+[Attempt("later","boundary","FIRST_TRY","LATE_PROBE",False)])[2],"INCONCLUSIVE")

    def test_retest_after_failure_not_fresh_training(self):
        seq=[Attempt("a","dots","FIRST_TRY"),Attempt("b","edges","FIRST_TRY"),
             Attempt("c","dots","UNRESOLVED"),Attempt("c","dots","FIRST_TRY")]
        self.assertEqual(summarize(seq)[0],"INSUFFICIENT")

    def test_new_unresolved_prompts_review(self):
        seq=training()+[Attempt("bad","faces","UNRESOLVED","NEW_PROBE")]
        self.assertEqual(summarize(seq),("RECHECK","RECHECK","RECHECK"))


if __name__=="__main__":
    unittest.main()
