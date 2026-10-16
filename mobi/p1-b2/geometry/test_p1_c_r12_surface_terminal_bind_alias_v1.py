from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TARGET = HERE / "p1_c_r12_surface_terminal_bind_alias_v1.py"
spec = importlib.util.spec_from_file_location("r12_under_test", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load R12 adapter")
r12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r12)


class R12SurfaceTerminalBindAliasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r11 = r12.load_r11(HERE)

    def test_alias_derivation_uses_frozen_quadrants_and_sole_region(self):
        v = np.asarray([
            [1.0, 0.0, 1.0], [1.0, 0.0, 2.0], [2.0, 0.0, 1.0],
            [-1.0, 0.0, 1.0], [-1.0, 0.0, 2.0], [-2.0, 0.0, 1.0],
            [1.0, 0.0, -1.0], [1.0, 0.0, -2.0], [2.0, 0.0, -1.0],
            [-1.0, 0.0, -1.0], [-1.0, 0.0, -2.0], [-2.0, 0.0, -1.0],
            [2.0, 1.0, 2.0], [-2.0, 1.0, 2.0], [2.0, 1.0, -2.0], [-2.0, 1.0, -2.0],
        ], dtype=np.float64)
        aliases = r12.derive_surface_terminal_aliases(v, self.r11)
        self.assertEqual(aliases["FORE_L_PAW"]["surfaceBindIndex"], 0)
        self.assertEqual(aliases["FORE_R_PAW"]["surfaceBindIndex"], 3)
        self.assertEqual(aliases["HIND_L_PAW"]["surfaceBindIndex"], 6)
        self.assertEqual(aliases["HIND_R_PAW"]["surfaceBindIndex"], 9)
        for x in aliases.values():
            self.assertEqual(x["candidateCount"], 3)
            self.assertEqual(x["derivation"], "FROZEN_SOLE_CANDIDATE_ARGMIN_DISTANCE_THEN_GLOBAL_VERTEX_INDEX")

    def test_alias_exact_distance_tie_breaks_by_global_vertex_index(self):
        v = np.asarray([
            [1.0, 0.0, 1.0], [2.0, 0.0, 1.0],
            [-1.0, 0.0, 1.0],
            [1.0, 0.0, -1.0],
            [-1.0, 0.0, -1.0],
            [2.0, 1.0, 2.0], [-2.0, 1.0, 2.0], [2.0, 1.0, -2.0], [-2.0, 1.0, -2.0],
        ], dtype=np.float64)
        aliases = r12.derive_surface_terminal_aliases(v, self.r11)
        self.assertEqual(aliases["FORE_L_PAW"]["candidateCount"], 2)
        self.assertEqual(aliases["FORE_L_PAW"]["surfaceBindIndex"], 0)

    def test_replacement_and_delta_audit_change_exactly_four_paw_roles(self):
        controls = []
        path_worlds = {}
        paw_old = {
            "FORE_L_PAW_CTRL": np.array([10.0, 0.0, 1.0]),
            "FORE_R_PAW_CTRL": np.array([-10.0, 0.0, 1.0]),
            "HIND_L_PAW_CTRL": np.array([10.0, 0.0, -1.0]),
            "HIND_R_PAW_CTRL": np.array([-10.0, 0.0, -1.0]),
        }
        for i, role in enumerate(self.r11.ROLE_ORDER):
            pos = paw_old.get(role, np.array([float(i), float(i + 1), float(i + 2)]))
            controls.append(self.r11.Control(
                role, self.r11.PARENT[role], self.r11.ROLE_DOMAIN[role],
                tuple(map(float, pos)), self.r11.PROVENANCE[role], "TEST_BASELINE",
            ))
        for role, path_name in r12.PAW_ROLE_TO_PATH.items():
            end = paw_old[role]
            path_worlds[path_name] = np.vstack([end + np.array([0.0, 1.0, 0.0]), end])

        aliases = {}
        for j, (role, anchor) in enumerate(r12.PAW_ROLE_TO_ANCHOR.items()):
            aliases[anchor] = {
                "surfaceBindIndex": j,
                "surfaceBindPositionR10": [100.0 + j, 0.0, 0.0],
            }
        changed = r12.replace_paw_bind_controls(self.r11, controls, aliases)
        report = r12.delta_audit(self.r11, controls, changed, path_worlds, aliases)
        self.assertEqual(tuple(report["changedRoles"]), r12.PAW_ROLES)
        self.assertEqual(report["changedRoleCount"], 4)
        self.assertEqual(report["unchangedNonPawRoleCount"], 26)

    def test_alias_semantic_weight_gate_requires_own_positive_weight(self):
        v = np.asarray([
            [1.0, 0.0, 1.0], [-1.0, 0.0, 1.0],
            [1.0, 0.0, -1.0], [-1.0, 0.0, -1.0],
        ], dtype=np.float64)
        anchors = ["FORE_L_PAW", "FORE_R_PAW", "HIND_L_PAW", "HIND_R_PAW"]
        aliases = {
            anchor: {"surfaceBindIndex": i, "surfaceBindPositionR10": v[i].tolist()}
            for i, anchor in enumerate(anchors)
        }
        domains = np.asarray(["FORE_L", "FORE_R", "HIND_L", "HIND_R"], dtype="U7")
        indices = np.full((4, self.r11.MAX_INFLUENCES), 255, dtype=np.uint8)
        weights = np.zeros((4, self.r11.MAX_INFLUENCES), dtype=np.float64)
        for i, role in enumerate(r12.PAW_ROLES):
            indices[i, 0] = self.r11.ROLE_INDEX[role]
            weights[i, 0] = 1.0
        report = r12.alias_semantic_weight_gate(self.r11, v, aliases, domains, indices, weights)
        self.assertEqual(set(report), set(r12.PAW_ROLES))
        self.assertTrue(all(x["ownRoleNormalizedWeightAtAlias"] == 1.0 for x in report.values()))

        weights[0, 0] = 0.0
        with self.assertRaisesRegex(RuntimeError, "no positive weight"):
            r12.alias_semantic_weight_gate(self.r11, v, aliases, domains, indices, weights)


if __name__ == "__main__":
    unittest.main()
