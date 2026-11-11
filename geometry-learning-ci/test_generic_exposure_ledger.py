"""Synthetic event ledger regression tests; no private cases or IDs."""
import copy
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generic_exposure_ledger import ToyLedger,Event

def item(seq,kind,episode="sample",**payload):
    return Event(f"evt-{seq}",seq,kind,episode,payload)

def show(ledger,episode="sample",key="new",role="TEST",verified=True,approved=True,assigned=True):
    return ledger.push(item(len(ledger.events),"SHOW",episode,role=role,
        equivalence_key=key,verified_identity=verified,approved=approved,assigned=assigned))

def complete(ledger,episode="sample"):
    n=len(ledger.events)
    ledger.push(item(n,"CHOOSE",episode,choice="A"))
    ledger.push(item(n+1,"COMMIT",episode))
    ledger.push(item(n+2,"RESULT",episode,correct=True))

class ExposureLedgerChecks(unittest.TestCase):
    def test_first_time_success_is_candidate(self):
        l=ToyLedger();show(l);complete(l)
        self.assertTrue(l.summary("sample")["independentFreshCandidate"])

    def test_reuse_of_training_a_not_fresh(self):
        l=ToyLedger();show(l,"a","shape","TRAIN_A");show(l,"sample","shape");complete(l)
        self.assertFalse(l.fresh_independent("sample"))

    def test_reuse_of_faded_example_not_fresh(self):
        l=ToyLedger();show(l,"b","shape2","TRAIN_B");show(l,"sample","shape2");complete(l)
        self.assertEqual(l.summary("sample")["freshness"],"EXPOSED")

    def test_same_identity_changed_title_not_new(self):
        l=ToyLedger();show(l,"a","equivalent","TRAIN_A")
        show(l,"sample","equivalent");complete(l)
        self.assertFalse(l.fresh_independent("sample"))

    def test_missing_exposure_history_fail_closed(self):
        l=ToyLedger(history_complete=False);show(l);complete(l)
        self.assertEqual(l.summary("sample")["freshness"],"UNKNOWN")
        self.assertFalse(l.fresh_independent("sample"))

    def test_unverified_fingerprint_fail_closed(self):
        l=ToyLedger();show(l,verified=False);complete(l)
        self.assertFalse(l.fresh_independent("sample"))

    def test_help_request_not_same_as_help_delivered(self):
        l=ToyLedger();show(l);l.push(item(1,"HELP_REQUESTED"));l.push(item(2,"CHOOSE",choice="A"))
        l.push(item(3,"COMMIT"));l.push(item(4,"RESULT",correct=True))
        self.assertTrue(l.fresh_independent("sample"))

    def test_help_before_commit_not_independent(self):
        l=ToyLedger();show(l);l.push(item(1,"HELP_SHOWN"));complete(l)
        self.assertFalse(l.fresh_independent("sample"))

    def test_postcommit_replay_does_not_change_first_choice(self):
        l=ToyLedger();show(l);l.push(item(1,"CHOOSE",choice="A"));l.push(item(2,"COMMIT"))
        l.push(item(3,"REPLAY"));l.push(item(4,"RESULT",correct=True))
        self.assertEqual(l.summary("sample")["first"],"A")
        self.assertTrue(l.fresh_independent("sample"))

    def test_first_clicked_choice_immutable(self):
        l=ToyLedger();show(l);l.push(item(1,"CHOOSE",choice="A"));l.push(item(2,"CHOOSE",choice="B"))
        l.push(item(3,"COMMIT"));l.push(item(4,"RESULT",correct=True))
        self.assertEqual((l.summary("sample")["first"],l.summary("sample")["committed"]),("A","B"))
        self.assertFalse(l.fresh_independent("sample"))

    def test_answer_reveal_before_commit_rejected(self):
        l=ToyLedger();show(l)
        with self.assertRaises(ValueError):l.push(item(1,"REVEAL"))

    def test_unapproved_test_may_not_score(self):
        l=ToyLedger();show(l,approved=False);l.push(item(1,"CHOOSE",choice="A"));l.push(item(2,"COMMIT"))
        with self.assertRaises(ValueError):l.push(item(3,"RESULT",correct=True))

    def test_unassigned_test_may_not_score(self):
        l=ToyLedger();show(l,assigned=False);l.push(item(1,"CHOOSE",choice="A"));l.push(item(2,"COMMIT"))
        with self.assertRaises(ValueError):l.push(item(3,"RESULT",correct=True))

    def test_second_result_rejected(self):
        l=ToyLedger();show(l);complete(l)
        with self.assertRaises(ValueError):l.push(item(4,"RESULT",correct=True))

    def test_retry_same_id_is_idempotent(self):
        l=ToyLedger();show(l);complete(l)
        receipt=copy.deepcopy(l.events[-1])
        l.push(receipt)
        self.assertEqual(len(l.events),4)
        self.assertEqual(l.summary("sample")["submitted"],1)

    def test_conflicting_retry_rejected(self):
        l=ToyLedger();show(l);complete(l)
        with self.assertRaises(ValueError):l.push(Event("evt-3",3,"RESULT","sample",{"correct":False}))

    def test_suspend_resume_preserves_first_click(self):
        l=ToyLedger();show(l);l.push(item(1,"CHOOSE",choice="A"))
        l.push(item(2,"SUSPEND"));r=copy.deepcopy(l)
        r.push(item(3,"RESUME"));r.push(item(4,"CHOOSE",choice="B"))
        self.assertEqual(r.summary("sample")["first"],"A")

    def test_technical_abort_retains_exposure_but_no_score(self):
        l=ToyLedger();show(l);l.push(item(1,"TECH_ABORT"))
        self.assertTrue(l.summary("sample")["technicallyAbortedNotScored"])
        show(l,"new_episode","new");self.assertEqual(l.summary("new_episode")["freshness"],"EXPOSED")

    def test_invalid_order_rejected(self):
        l=ToyLedger();show(l)
        with self.assertRaises(ValueError):l.push(item(3,"HELP_REQUESTED"))

    def test_training_result_cannot_score(self):
        l=ToyLedger();show(l,role="TRAIN_A")
        with self.assertRaises(ValueError):l.push(item(1,"RESULT",correct=True))

if __name__=="__main__":
    unittest.main()
