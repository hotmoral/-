#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "legacy-game-structure" / "data" / "t1_representative_transition_slice_recipes_v0_1.yaml"
EXPECTED_STAGES = {5, 18, 20, 21, 22, 23, *range(39, 51)}


def max_density(times: list[int], window_ms: int) -> int:
    if not times:
        return 0
    return max(sum(1 for other in times if start <= other < start + window_ms) for start in times)


def main() -> int:
    doc = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    guards = doc["guards"]
    allowed_monsters = set(guards["allowedMonsters"])
    allowed_archetypes = set(guards["allowedArchetypes"])
    allowed_formations = set(guards["allowedFormations"])
    allowed_cadences = set(guards["allowedCadences"])
    physical_x = float(guards["physicalSpawnX"])
    normal4 = int(guards["authored4sNormalMax"])
    watch4 = int(guards["authored4sWatchMax"])

    errors: list[str] = []
    warnings: list[str] = []
    rows: list[tuple[int, str, int, int, int]] = []

    if doc.get("tier") != "T1":
        errors.append("tier must be T1")
    if guards.get("stageBoundary") != "STAGE_SETTLED":
        errors.append("stageBoundary must be STAGE_SETTLED")
    if guards.get("midfieldPopIn") is not False:
        errors.append("midfieldPopIn must remain false")

    recipes = doc.get("recipes", [])
    ids = [r.get("id") for r in recipes]
    stages = [int(r.get("stage")) for r in recipes]
    if len(ids) != len(set(ids)):
        errors.append("duplicate recipe id")
    if len(stages) != len(set(stages)):
        errors.append("duplicate recipe stage")
    if set(stages) != EXPECTED_STAGES:
        errors.append(f"stage set mismatch: got={sorted(stages)} expected={sorted(EXPECTED_STAGES)}")

    by_id = {r["id"]: r for r in recipes}
    by_stage = {int(r["stage"]): r for r in recipes}

    for r in sorted(recipes, key=lambda x: int(x["stage"])):
        stage = int(r["stage"])
        rid = r["id"]
        if r["archetype"] not in allowed_archetypes:
            errors.append(f"{rid}: illegal primary archetype {r['archetype']}")
        for a in r.get("componentArchetypes", []):
            if a not in allowed_archetypes:
                errors.append(f"{rid}: illegal component archetype {a}")
        if r["formation"] not in allowed_formations:
            errors.append(f"{rid}: illegal primary formation {r['formation']}")
        for f in r.get("formationSet", []):
            if f not in allowed_formations:
                errors.append(f"{rid}: illegal formationSet entry {f}")
        if r["cadence"] not in allowed_cadences:
            errors.append(f"{rid}: illegal cadence {r['cadence']}")
        if abs(float(r["entryBaseX"]) - physical_x) > 1e-9:
            errors.append(f"{rid}: entryBaseX {r['entryBaseX']} != physicalSpawnX {physical_x}")

        spawns = r.get("spawns", [])
        times = [int(s["tMs"]) for s in spawns]
        if times != sorted(times):
            errors.append(f"{rid}: spawn times are not monotone")
        for spawn in spawns:
            if spawn["type"] not in allowed_monsters:
                errors.append(f"{rid}: illegal monster {spawn['type']}")
            y = float(spawn["y"])
            if not 0.0 <= y <= 1.0:
                errors.append(f"{rid}: y out of range {y}")

        max4 = max_density(times, 4000)
        max6 = max_density(times, 6000)
        if max4 > watch4:
            errors.append(f"{rid}: authored4s density {max4} exceeds watch max {watch4}")
        elif max4 > normal4:
            warnings.append(f"{rid}: authored4s density {max4} is in WATCH range")
        rows.append((stage, rid, len(spawns), max4, max6))

    for pair in doc.get("pairedDiagnostics", []):
        rid = pair.get("recipe")
        if rid not in by_id:
            errors.append(f"paired diagnostic {pair.get('id')}: missing recipe {rid}")
            continue
        if int(by_id[rid]["stage"]) != int(pair["stage"]):
            errors.append(f"paired diagnostic {pair.get('id')}: recipe/stage mismatch")
        if pair.get("variantRule") != "IDENTICAL_RECIPE_ONLY_SKILL_STATE_DIFFERS":
            errors.append(f"paired diagnostic {pair.get('id')}: invalid paired-variant rule")

    for seq in doc.get("sequentialSlices", []):
        if seq.get("boundary") != "STAGE_SETTLED":
            errors.append(f"{seq.get('id')}: sequential boundary must be STAGE_SETTLED")
        if set(seq.get("persistentState", [])) != {"wallDeficit", "combo", "charge"}:
            errors.append(f"{seq.get('id')}: persistent state set mismatch")
        for stage in seq.get("stages", []):
            if int(stage) not in by_stage:
                errors.append(f"{seq.get('id')}: missing stage recipe {stage}")

    if 40 in by_stage and 41 in by_stage:
        s40 = max_density([int(s["tMs"]) for s in by_stage[40]["spawns"]], 4000)
        s41 = max_density([int(s["tMs"]) for s in by_stage[41]["spawns"]], 4000)
        if not s41 < s40:
            errors.append(f"Stage41 relief not expressed in authored4s density: S40={s40} S41={s41}")

    print("stage recipe authored max4s max6s")
    for stage, rid, authored, max4, max6 in rows:
        print(f"{stage:>2} {rid:<36} {authored:>2} {max4:>2} {max6:>2}")
    for msg in warnings:
        print(f"WARNING: {msg}")
    for msg in errors:
        print(f"ERROR: {msg}")
    print(f"RESULT={'PASS' if not errors else 'FAIL'} errors={len(errors)} warnings={len(warnings)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
