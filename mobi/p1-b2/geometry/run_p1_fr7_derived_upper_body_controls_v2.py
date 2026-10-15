from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import p1_fr7_derived_upper_body_controls_v2 as v2
import run_p1_fr4_internal_core_scaffold as fr4_render
import run_p1_fr7_derived_upper_body_controls_v1 as v1_run


RUN_VERSION = "P1_FR7_DERIVED_UPPER_BODY_CONTROLS_EVIDENCE_V2_FINAL"
FROZEN_V1 = {
    "publicRepository": "hotmoral/-",
    "publicHead": "db4e82744a24ca55bdb29129f1a71705033c6e1e",
    "runId": 38821827010,
    "jobId": 116719964867,
    "artifactId": 12012962615,
    "artifactDigest": "sha256:944ffc4db7fad9acd76ddef932d76ad20ca5d2f833939cdaec24740488ae7570",
    "recordContentSha256": "af4b4b2666b30ad0d927d03fe069bfd01d54a9deb727ddae8529734b97ece4a6",
}


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def run_matrix():
    old = v1_run.fr7
    old_version = v1_run.RUN_VERSION
    try:
        v1_run.fr7 = v2
        v1_run.RUN_VERSION = RUN_VERSION
        records, summary = v1_run.run_matrix()
    finally:
        v1_run.fr7 = old
        v1_run.RUN_VERSION = old_version
    summary["version"] = RUN_VERSION
    summary["prototypeVersion"] = v2.PROTOTYPE_VERSION
    return records, summary


def generate_debug_svgs(output_dir: Path):
    old = v1_run.fr7
    try:
        v1_run.fr7 = v2
        files = v1_run.generate_debug_svgs(output_dir)
    finally:
        v1_run.fr7 = old
    for path in files:
        text = path.read_text(encoding="utf-8").replace("FR7 V1", "FR7 V2")
        path.write_text(text, encoding="utf-8")
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    records, summary = run_matrix()
    (out / "records.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    baseline_dir = out / "frozen_p1f_baseline"
    baseline_manifest = fr4_render.generate_frozen_p1f_baseline(baseline_dir)
    debug_dir = out / "debug"
    svg_files = generate_debug_svgs(debug_dir)
    manifest = {
        "version": RUN_VERSION,
        "summary": summary,
        "frozenFr7V1": FROZEN_V1,
        "frozenP1FBaselineVersion": baseline_manifest["version"],
        "debugSvgs": [
            {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(svg_files)
        ],
    }
    manifest["manifestContentSha256"] = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if not summary["structuralPass"]:
        raise SystemExit("P1-FR7 V2 structural invariant lane failed")


if __name__ == "__main__":
    main()
