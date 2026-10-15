from __future__ import annotations

# Reuse the accepted C3 matrix/scorecard machinery while replacing only the
# renderer entry point with the minimal-correction v3 adapter.
import run_c3_matrix as _base
from c3_renderer_minimal_v3 import MINIMAL_CORRECTION_VERSION, render_fixture

_base.render_fixture = render_fixture

canonical_bytes = _base.canonical_bytes
render_payload = _base.render_payload
run_c3_matrix = _base.run_c3_matrix
render_scorecard = _base.render_scorecard
write_scorecards = _base.write_scorecards


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    parser.add_argument("--sample-count", type=int, default=17)
    args = parser.parse_args()

    records, summary = run_c3_matrix(sample_count=args.sample_count)
    summary["rendererValidityAdapter"] = "P1_C3_RENDERER_VALIDITY_V2"
    summary["minimalCorrectionVersion"] = MINIMAL_CORRECTION_VERSION
    print(json.dumps(summary, indent=2, sort_keys=True))

    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "results.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
        (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
        scorecards = write_scorecards(out / "scorecards")
        print(f"scorecards={len(scorecards)}")
