from __future__ import annotations

import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from e_v0_fixture_adapter import H4, H6N, H7, MORPHOLOGIES
from run_p1f_perceptual_evidence import (
    EVIDENCE_VERSION,
    FILMSTRIP_SAMPLES,
    PRIMARY_SIZE_DP,
    generate,
    render_filmstrip,
)


class P1FPerceptualEvidenceTests(unittest.TestCase):
    def test_sampling_contract_is_exact(self):
        self.assertEqual(80, PRIMARY_SIZE_DP)
        self.assertEqual(9, len(FILMSTRIP_SAMPLES[H4]))
        self.assertEqual(11, len(FILMSTRIP_SAMPLES[H6N]))
        self.assertEqual(9, len(FILMSTRIP_SAMPLES[H7]))
        self.assertEqual(0.0, FILMSTRIP_SAMPLES[H4][0])
        self.assertEqual(1.0, FILMSTRIP_SAMPLES[H4][-1])
        self.assertEqual(0.0, FILMSTRIP_SAMPLES[H6N][0])
        self.assertEqual(1.0, FILMSTRIP_SAMPLES[H6N][-1])

    def test_h6n_both_directions_generate_without_geometry_mutation(self):
        for morphology in MORPHOLOGIES:
            positive, pos_hashes = render_filmstrip(morphology, H6N, +1)
            negative, neg_hashes = render_filmstrip(morphology, H6N, -1)
            self.assertEqual(11, len(pos_hashes))
            self.assertEqual(11, len(neg_hashes))
            self.assertIn("dir=+1", positive)
            self.assertIn("dir=-1", negative)

    def test_full_evidence_bundle_dimensions_and_xml(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = generate(tmp)
            self.assertEqual(EVIDENCE_VERSION, manifest["version"])
            self.assertEqual(22, manifest["fileCount"])
            # 5*(9 H4 + 11*2 H6N + 9 H7)=200, plus 20 morph overview + 12 scale overview.
            self.assertEqual(232, manifest["totalRenderedFrames"])
            paths = sorted(Path(tmp).glob("*.svg"))
            self.assertEqual(22, len(paths))
            for path in paths:
                ET.parse(path)

    def test_manifest_is_byte_deterministic(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            left = generate(a)
            right = generate(b)
            self.assertEqual(left, right)
            self.assertEqual(
                Path(a, "manifest.json").read_bytes(),
                Path(b, "manifest.json").read_bytes(),
            )
            for entry in left["files"]:
                self.assertEqual(
                    Path(a, entry["file"]).read_bytes(),
                    Path(b, entry["file"]).read_bytes(),
                )

    def test_manifest_contains_only_expected_evidence_kinds(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = generate(tmp)
            kinds = [entry["kind"] for entry in manifest["files"]]
            self.assertEqual(20, kinds.count("filmstrip"))
            self.assertEqual(1, kinds.count("morphology_overview"))
            self.assertEqual(1, kinds.count("scale_overview"))
            parsed = json.loads(Path(tmp, "manifest.json").read_text())
            self.assertEqual(manifest, parsed)


if __name__ == "__main__":
    unittest.main()
