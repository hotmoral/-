#!/usr/bin/env python3
"""Public synthetic-only learning transfer validator; no private project imports.

The tool can validate a PUBLIC or SANITIZED equivalent plan. A passing result
DOES NOT prove private bank integrity, educational effect, or canonical parity.
"""
import json
from pathlib import Path
import sys


def verify(data):
    if data.get("schemaVersion") != "synthetic-transfer-rules-v1":
        raise ValueError("Invalid public synthetic schema")
    policy = data["requirements"]
    if policy["minDistinctStimuli"] < 2 or policy["minRepresentationFamilies"] < 2:
        raise ValueError("Reference policy must check transfer diversity")
    if policy["minHeldoutPerSkill"] < 1:
        raise ValueError("Held-out evaluation must be reserved")
    summary = {}
    if not data.get("domains"):
        raise ValueError("Missing synthetic domains")
    for skill, group in sorted(data["domains"].items()):
        if not isinstance(skill, str) or not skill:
            raise ValueError("Unnamed skill")
        seen_ids, seen_stimuli = set(), set()
        practice = group["existing"] + group["planned"]
        heldout = group["heldout"]
        for row in practice + heldout:
            if set(row) != {"id", "stimulus", "representation", "stageUpdateEligible"}:
                raise ValueError("Unexpected untrusted record fields")
            if not row["id"] or not row["stimulus"] or not row["representation"]:
                raise ValueError("Empty identifier")
            if row["stageUpdateEligible"] is not False:
                raise ValueError("Transfer evidence may not promote Core stage")
            if row["id"] in seen_ids or row["stimulus"] in seen_stimuli:
                raise ValueError("Duplicate ID or stimulus contaminates evaluation")
            seen_ids.add(row["id"])
            seen_stimuli.add(row["stimulus"])
        if len(practice) < policy["minDistinctStimuli"]:
            raise ValueError("Insufficient independent practice stimuli")
        reps = {row["representation"] for row in practice}
        if len(reps) < policy["minRepresentationFamilies"]:
            raise ValueError("Insufficient genuine representation families")
        if len(heldout) < policy["minHeldoutPerSkill"]:
            raise ValueError("Missing unseen evaluation probe")
        summary[skill] = {
            "practiceCount": len(practice),
            "representationCount": len(reps),
            "heldoutCount": len(heldout)
        }
    return {"status": "PASS_PUBLIC_SYNTHETIC_RULES_ONLY", "domains": summary,
            "warning": "No private source or actual learner competence validated"}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 validate.py <public synthetic fixture>")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(verify(data), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
