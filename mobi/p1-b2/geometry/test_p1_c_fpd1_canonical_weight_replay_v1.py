from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TARGET = HERE / "p1_c_fpd1_canonical_weight_replay_v1.py"
spec = importlib.util.spec_from_file_location("fpd1_replay_under_test", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load FPD1 canonical replay adapter")
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class FPD1CanonicalWeightReplayTests(unittest.TestCase):
    def test_contract_identity_exact(self):
        self.assertEqual(replay.VERSION, "P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_V1")
        self.assertEqual(replay.SELECTION_TOKEN, "P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_SELECTED")
        self.assertEqual(replay.CONTRACT_TOKEN, "P1_C_FPD1_CANONICAL_WEIGHT_REPLAY_CONTRACT_FROZEN")
        self.assertEqual(replay.POSE_ID, "FPD1_FOREQUARTER_PIVOT_NECK_HEAD_YAW_LEFT_8DEG")

    def test_canonical_weight_identity_constants_exact(self):
        self.assertEqual(replay.CANONICAL_WEIGHTS_BYTES, 112532)
        self.assertEqual(replay.CANONICAL_PREFIX, b"MOBI_R11_WEIGHTS_V1\0")
        self.assertEqual(replay.CANONICAL_VERTEX_COUNT, 3125)
        self.assertEqual(replay.CANONICAL_ROLE_COUNT, 30)
        self.assertEqual(replay.CANONICAL_MAX_INFLUENCES, 4)
        self.assertEqual(replay.CANONICAL_SERIALIZED_SHA256, "171653287d416ce2fdb30db3e51356b241f0507614de8316ec0ed4ec0588b12c")
        self.assertEqual(replay.CANONICAL_INDICES_SHA256, "1907a206446b8da3497cb1e6adba4f59120f3af41bd5b003fabe513db64f871b")
        self.assertEqual(replay.CANONICAL_WEIGHT_FLOATS_SHA256, "aa3569c6d2c3350bf21493d8c4fc8acc8d15db366cdcf51c8c81c7cdafa57411")

    def test_source_artifact_identity_exact(self):
        self.assertEqual(replay.CANONICAL_SOURCE_ARTIFACT_ID, 12088123879)
        self.assertEqual(replay.CANONICAL_SOURCE_ARTIFACT_DIGEST, "sha256:a395cf71206d3459c9ed052c37ff51ad1c0be097bc66fb5ebb02f7e208b97c84")
        self.assertEqual(replay.CANONICAL_SOURCE_MEMBER, "neutral_stage1_regression/weights.bin")

    def test_frozen_fpd1_loader_identity(self):
        fpd1 = replay.load_fpd1(HERE)
        self.assertEqual(fpd1.VERSION, replay.EXPECTED_FPD1_VERSION)
        self.assertEqual(fpd1.POSE_ID, replay.POSE_ID)
        self.assertEqual(tuple(fpd1.SELECTED_ROLES), ("NECK_BASE_CTRL", "HEAD_CTRL"))
        self.assertEqual(fpd1.PIVOT_ROLE, "FOREQUARTER_CTRL")
        self.assertEqual(float(fpd1.ANGLE_DEG), 8.0)
        self.assertTrue(np.array_equal(fpd1.AXIS_R10, np.asarray([0.0, 1.0, 0.0], dtype=np.float64)))

    def test_parse_rejects_noncanonical_payload(self):
        with self.assertRaisesRegex(RuntimeError, "byte length drift"):
            replay.parse_canonical_weights_bytes(b"not canonical")

    def test_ulp_drift_stats_exact_identity(self):
        a = np.asarray([[0.25, 0.75], [0.5, 0.5]], dtype=np.float64)
        r = replay.ulp_drift_stats(a, a.copy())
        self.assertEqual(r["bitwiseDifferentSlots"], 0)
        self.assertEqual(r["verticesWithAnyDifference"], 0)
        self.assertEqual(r["maxAbsoluteDifference"], 0.0)
        self.assertEqual(r["maxUlp"], 0)

    def test_ulp_drift_stats_detects_one_ulp_without_semantic_change(self):
        a = np.asarray([[0.25, 0.75], [0.5, 0.5]], dtype=np.float64)
        b = a.copy()
        b[0, 0] = np.nextafter(b[0, 0], np.inf)
        r = replay.ulp_drift_stats(a, b)
        self.assertEqual(r["bitwiseDifferentSlots"], 1)
        self.assertEqual(r["verticesWithAnyDifference"], 1)
        self.assertEqual(r["maxUlp"], 1)
        self.assertGreater(r["maxAbsoluteDifference"], 0.0)


if __name__ == "__main__":
    unittest.main()
