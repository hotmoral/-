"""Only invented example labels are used; no private project data."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))

from generic_curriculum_graph import verify_graph

NODES=("pattern_intro","pattern_reason","view_intro","view_reason","space_intro","space_reason")
OBS=("view_observe",)
HARD=(
    ("pattern_intro","pattern_reason"),
    ("view_intro","view_reason"),
    ("space_intro","space_reason"),
    ("view_observe","view_intro"),
)
SOFT=(
    ("pattern_intro","space_intro"),
    ("pattern_reason","view_reason"),
    ("view_intro","space_reason"),
)

def check(hard=HARD,advice=SOFT,source=HARD, nodes=NODES):
    return verify_graph(
        nodes=nodes,observation_nodes=OBS,
        actual_mandatory=source,proposed_mandatory=hard,optional_bridges=advice)


class GenericLearningDAGTests(unittest.TestCase):
    def test_valid_synthetic_curriculum(self):
        self.assertEqual(check()["status"],"PASS_PUBLIC_SYNTHETIC_DAG_RULES_ONLY")

    def test_mandatory_edge_missing_is_not_permitted(self):
        with self.assertRaises(ValueError):
            check(hard=HARD[:-1])

    def test_invented_mandatory_gate_rejected(self):
        with self.assertRaises(ValueError):
            check(hard=HARD+(("pattern_intro","view_intro"),))

    def test_observation_dependency_is_mandatory(self):
        with self.assertRaises(ValueError):
            check(hard=HARD[:-1])

    def test_soft_bridge_does_not_become_hard_gate(self):
        with self.assertRaises(ValueError):
            check(hard=HARD+SOFT)

    def test_advisory_cycle_detected(self):
        with self.assertRaises(ValueError):
            check(advice=SOFT+(("space_reason","pattern_intro"),))

    def test_no_fabricated_node(self):
        with self.assertRaises(ValueError):
            check(advice=SOFT+(("not_in_training","view_reason"),))

    def test_no_self_dependency(self):
        with self.assertRaises(ValueError):
            check(advice=SOFT+(("view_intro","view_intro"),))

    def test_duplicate_advisory_edge_rejected(self):
        with self.assertRaises(ValueError):
            check(advice=SOFT+(SOFT[0],))


if __name__=="__main__":
    unittest.main()
