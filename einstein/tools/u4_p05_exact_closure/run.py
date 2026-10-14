from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "harness" / "u4_p05_exact_closure"
FIXTURE = ROOT / "fixtures" / "u4_p05_exact_closure" / "control_manifest.json"
OUTPUT = ROOT / "output" / "u4_p05_exact_closure"

sys.path.insert(0, str(HARNESS))

from mutation_suite import run_all  # noqa: E402


def file_sha256(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    manifest = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = run_all()

    expected_by_id = {item["id"]: item["expected"] for item in manifest["controls"]}
    result_by_id = {item["id"]: item for item in results}

    manifest_ok = (
        len(expected_by_id) == 25
        and set(expected_by_id) == set(result_by_id)
        and all(result_by_id[cid]["expected"] == expected_by_id[cid] for cid in expected_by_id)
    )

    for item in results:
        status = "PASS" if item["pass"] else "FAIL"
        print(
            f'{item["id"]}: {status} '
            f'expected={item["expected"]} actual='
            f'{{"admissibility":"{item["actual"]["admissibility"]}",'
            f'"closure":"{item["actual"]["closure"]}",'
            f'"absence":"{item["actual"]["absence"]}"}}'
        )

    bundle_files = [
        HARNESS / "model.py",
        HARNESS / "mutation_suite.py",
        HARNESS / "README.md",
        FIXTURE,
        Path(__file__).resolve(),
    ]
    hashes = {str(path.relative_to(ROOT)): file_sha256(path) for path in bundle_files}

    passed = manifest_ok and all(item["pass"] for item in results)
    report = {
        "schemaVersion": "1.0.0",
        "suite": "einstein-u4-p05-exact-closure-public-model",
        "controlCount": len(results),
        "manifestParity": manifest_ok,
        "passed": passed,
        "controls": results,
        "sourceHashes": hashes,
        "limitations": [
            "This is a standalone public-safe synthetic abstract model.",
            "It does not contain or compile private EinsteinGame production Java.",
            "PASS here is not private production integration evidence."
        ]
    }

    OUTPUT.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT / "report.json"
    report_path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    manifest_path = OUTPUT / "sha256.txt"
    manifest_path.write_text(
        "\n".join(f"{value}  {key}" for key, value in sorted(hashes.items())) + "\n",
        encoding="utf-8"
    )

    print(f"CONTROL_COUNT={len(results)}")
    print(f"MANIFEST_PARITY={'PASS' if manifest_ok else 'FAIL'}")
    print(f"SUITE_RESULT={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
