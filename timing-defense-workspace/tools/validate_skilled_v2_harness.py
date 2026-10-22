#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

EXPECTED_HARNESS_IDS = ["H0", "H1", "H2", "H3", "H4", "H5"]
EXPECTED_CONTEXTS = {
    "H0": "BASELINE",
    "H1": "TEMPO",
    "H2": "DURABLE",
    "H3": "TURNOVER",
    "H4": "STATEFUL",
    "H5": "MIXED",
}
EXPECTED_PROFILES = {
    "SKILLED_V2_CONSERVATIVE",
    "SKILLED_V2_CENTRAL",
    "SKILLED_V2_STRONG",
    "HIGH_MASTERY_STRESS",
}
FORBIDDEN_LANE_TRUE = [
    "campaignAttempt",
    "affectsStars",
    "affectsTierRecords",
    "affectsPermanentProgression",
    "affectsAchievements",
    "affectsTitles",
    "affectsRunShopEconomy",
    "persistsCampaignExp",
    "persistsCampaignCoin",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("harness_yaml", type=Path)
    args = p.parse_args()

    data = yaml.safe_load(args.harness_yaml.read_text(encoding="utf-8")) or {}
    errors: list[str] = []
    warnings: list[str] = []

    if data.get("status") != "CALIBRATION_SPEC_NOT_FITTED":
        fail(errors, "status must remain CALIBRATION_SPEC_NOT_FITTED before observed trace fitting")

    lane = data.get("lane") or {}
    if lane.get("id") != "HARNESS_ONLY":
        fail(errors, "lane.id must be HARNESS_ONLY")
    for key in FORBIDDEN_LANE_TRUE:
        if lane.get(key) is not False:
            fail(errors, f"lane.{key} must be false")
    if lane.get("preserveGameInputJudgmentSemantics") is not True:
        fail(errors, "harness must preserve game input/judgment semantics for measured variables")

    harnesses = data.get("harnesses") or []
    ids = [str(x.get("id")) for x in harnesses]
    if ids != EXPECTED_HARNESS_IDS:
        fail(errors, f"harness IDs/order must be exactly {EXPECTED_HARNESS_IDS}, got {ids}")

    by_id = {str(x.get("id")): x for x in harnesses}
    for hid in EXPECTED_HARNESS_IDS:
        h = by_id.get(hid) or {}
        if h.get("pressureContext") != EXPECTED_CONTEXTS[hid]:
            fail(errors, f"{hid}.pressureContext must be {EXPECTED_CONTEXTS[hid]}")
        if not h.get("purpose"):
            fail(errors, f"{hid} must declare purpose")
        if not h.get("requiredMetrics"):
            fail(errors, f"{hid} must declare requiredMetrics")
        controls = h.get("controls") or {}
        if controls.get("progressionEffects") != "DISABLED":
            fail(errors, f"{hid} controls.progressionEffects must be DISABLED")

    h0 = by_id.get("H0") or {}
    h0_controls = h0.get("controls") or {}
    if h0_controls.get("longEnoughForCombo40Opportunity") is not True:
        fail(errors, "H0 must provide a real combo40 opportunity")
    if h0_controls.get("statefulMechanics") != "DISABLED":
        fail(errors, "H0 stateful mechanics must be disabled")

    h3 = by_id.get("H3") or {}
    if (h3.get("controls") or {}).get("targetTurnover") != "HIGH_AND_INTENTIONAL":
        fail(errors, "H3 must intentionally isolate target turnover")

    h4 = by_id.get("H4") or {}
    dep = h4.get("roleExpressionDependency") or {}
    if dep.get("contractMonster") != "CHARGER" or dep.get("requireReadableWindup") is not True:
        fail(errors, "H4 must depend on a readable CHARGER windup contract")
    if not dep.get("sourceEvidence"):
        fail(errors, "H4 must cite role-expression evidence")

    h5 = by_id.get("H5") or {}
    if int(h5.get("minimumDistinctPressureFamilies") or 0) < 2:
        fail(errors, "H5 must combine at least two pressure families")
    if (h5.get("controls") or {}).get("brandNewMechanic") != "FORBIDDEN":
        fail(errors, "H5 must not introduce a brand-new mechanic")

    user_anchors = data.get("userAnchors") or {}
    if user_anchors.get("oldSkilledTooWeak") is not True:
        fail(errors, "old-skilled-too-weak user anchor must be preserved")
    if user_anchors.get("combo40OrdinarySkilledAchievable") is not True:
        fail(errors, "combo40 ordinary-skilled anchor must be preserved")
    if float(user_anchors.get("nonT1CentralFullTierClearUpperBound", -1)) != 0.60:
        fail(errors, "non-T1 CENTRAL full-Tier clear upper bound must remain 0.60")

    fitting = data.get("fitting") or {}
    if fitting.get("methodClass") != "SEQUENCE_AWARE_CONTEXT_CONDITIONED":
        fail(errors, "fitting must be sequence-aware/context-conditioned")
    profiles = set(fitting.get("profiles") or [])
    if profiles != EXPECTED_PROFILES:
        fail(errors, f"profile family mismatch: {sorted(profiles)}")
    if fitting.get("highMasterySeparateFromOrdinarySkilled") is not True:
        fail(errors, "HIGH_MASTERY_STRESS must remain separate from ordinary skilled")

    forbidden = set(fitting.get("forbidden") or [])
    required_forbidden = {
        "single_global_iid_judgment_vector_as_complete_model",
        "reverse_fit_player_weakness_to_hit_clear_rate_target",
        "classify_combo40_as_high_mastery_only",
        "fit_from_single_trace_only",
    }
    missing_forbidden = required_forbidden - forbidden
    if missing_forbidden:
        fail(errors, f"missing anti-pattern guards: {sorted(missing_forbidden)}")

    post = data.get("postFitGates") or {}
    diff = post.get("difficulty") or {}
    if diff.get("evaluatedOnlyAfterFit") is not True:
        fail(errors, "difficulty clear-rate gate must be evaluated only after player fitting")
    if float(diff.get("nonT1CentralFullTierClearUpperBound", -1)) != 0.60:
        fail(errors, "post-fit difficulty gate must remain 0.60")
    if (post.get("lv31") or {}).get("centralTargetUnlockStageBand") != [41, 45]:
        fail(errors, "Lv31 CENTRAL target band must remain [41,45]")

    numeric = data.get("numericFitValues") or {}
    if numeric.get("status") != "OPEN_UNTIL_OBSERVED_TRACES":
        fail(errors, "numeric fit values must remain open until observed traces")

    trace = data.get("traceSchema") or {}
    for key in ("sessionRequiredFields", "actionRequiredFields", "stateEventRequiredFields"):
        if not trace.get(key):
            fail(errors, f"traceSchema.{key} must not be empty")

    if len(harnesses) == 6 and not errors:
        warnings.append("Harness structure is valid, but this does not constitute observed-player fitting.")

    print(f"VALIDATION=SKILLED_V2_HARNESS errors={len(errors)} warnings={len(warnings)}")
    for x in errors:
        print(f"ERROR {x}")
    for x in warnings:
        print(f"WARN {x}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
