from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from c5_runtime_cost_proxy import build_cost_report, canonical_json_bytes
from c5_source_cost_audit import build_source_audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    report_a = build_cost_report()
    report_b = build_cost_report()
    bytes_a = canonical_json_bytes(report_a)
    bytes_b = canonical_json_bytes(report_b)
    if bytes_a != bytes_b:
        raise RuntimeError("C5 deterministic cost report mismatch across repeated run")

    audit = build_source_audit()
    audit_bytes = canonical_json_bytes(audit)

    report_path = out_dir / "c5_runtime_cost_report.json"
    audit_path = out_dir / "c5_source_cost_audit.json"
    report_path.write_bytes(bytes_a + b"\n")
    audit_path.write_bytes(audit_bytes + b"\n")

    report_sha = hashlib.sha256(bytes_a).hexdigest()
    audit_sha = hashlib.sha256(audit_bytes).hexdigest()

    manifest = {
        "runtimeCostReportSha256": report_sha,
        "sourceCostAuditSha256": audit_sha,
        "deterministicRepeatExact": True,
        "fixtureSampleCount": report_a["fixtureSampleCount"],
        "renderSampleCount": report_a["renderSampleCount"],
        "decisionProxies": report_a["decisionProxies"],
        "sourceAudit": audit,
    }
    manifest_bytes = canonical_json_bytes(manifest)
    (out_dir / "summary.json").write_bytes(manifest_bytes + b"\n")

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
