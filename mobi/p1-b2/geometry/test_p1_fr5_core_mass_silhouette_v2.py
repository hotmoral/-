from __future__ import annotations

import p1_fr5_core_mass_silhouette_v1 as v1
import p1_fr5_core_mass_silhouette_v2 as v2
import test_p1_fr5_core_mass_silhouette_v1 as v1_tests


# Reuse the complete V1 invariant suite against the V2 candidate. The inherited
# methods resolve their geometry module through this module-global replacement.
v1_tests.fr5 = v2


class P1FR5CoreMassSilhouetteV2Tests(v1_tests.P1FR5CoreMassSilhouetteV1Tests):
    def test_contract_coefficients_and_influence_topology_are_exact(self):
        self.assertEqual(
            v2.VIEW_SCALES,
            {
                "CRANIUM_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.14, "FRONT": 1.20},
                "CERVICAL_BRIDGE": {"PROFILE": 1.00, "THREE_QUARTER": 0.88, "FRONT": 0.80},
                "THORAX_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.08, "FRONT": 1.12},
            },
        )
        self.assertEqual(v2.LAYER_IDS, v1.LAYER_IDS)
        self.assertEqual(v2.INFLUENCE_WEIGHTS, v1.INFLUENCE_WEIGHTS)
        for layer_id, scales in v2.VIEW_SCALES.items():
            self.assertEqual(scales["PROFILE"], 1.0)
            if layer_id == "CRANIUM_MASS":
                self.assertLessEqual(scales["THREE_QUARTER"], 1.20)
                self.assertLessEqual(scales["FRONT"], 1.20)
            elif layer_id == "CERVICAL_BRIDGE":
                self.assertGreaterEqual(scales["THREE_QUARTER"], 0.80)
                self.assertGreaterEqual(scales["FRONT"], 0.80)
            elif layer_id == "THORAX_MASS":
                self.assertLessEqual(scales["THREE_QUARTER"], 1.12)
                self.assertLessEqual(scales["FRONT"], 1.12)


if __name__ == "__main__":
    import unittest
    unittest.main()
