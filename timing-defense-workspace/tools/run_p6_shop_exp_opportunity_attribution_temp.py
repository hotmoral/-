#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge

OUT = Path("p6_shop_exp_opportunity_attribution_temp.json")
SEEDS = list(range(1, 21))
CLASSES = list(bridge.CLASSES)
ENTRY_CHARGE = 0
PROFILE = bridge.PROFILE

# P4-approved methodology candidate quality weights. Numerical values remain provisional.
XP_CREDIT = {
    "NORMAL": 1.000,
    "GOOD": 1.500,
    "PERFECT": 2.250,
    "HEAVY": 1.250,
    "HEAVY+": 1.750,
    "GREAT": 2.250,
    "SUPER": 2.875,
    "CRITICAL": 3.500,
}

VARIANTS = ("ATK_OFF", "ATK_ON")


def mean(values):
    return sum(values) / len(values) if values else None


def r6(value):
    return None if value is None else round(float(value), 6)


def install_judgment_trace():
    original = bridge.bridge_next_judgment

    def traced_next_judgment():
        judgment = original()
        rs = bridge.BRIDGE_CTX["runState"]
        rs.setdefault("_traceJudgments", []).append(judgment)
        return judgment

    bridge.bridge_next_judgment = traced_next_judgment
    return original


def reconstruct_stage_awards(trace, stages, entry_charge):
    idx = 0
    charge = int(entry_charge)
    out = []
    total_tiers = Counter()
    total_xp = 0.0

    for stage in stages:
        before_idx = idx
        tiers = Counter()
        xp = 0.0
        for _ in range(int(stage["rootActions"])):
            if charge >= 3:
                if idx + 1 >= len(trace):
                    raise RuntimeError("trace exhausted inside Heavy action")
                x = trace[idx]
                y = trace[idx + 1]
                idx += 2
                tier = bridge.p3.strong(x, y)
                charge = 0
            else:
                if idx >= len(trace):
                    raise RuntimeError("trace exhausted inside ordinary action")
                tier = trace[idx]
                idx += 1
                charge = min(3, charge + 1)

            if tier not in XP_CREDIT:
                raise RuntimeError(f"unknown XP tier: {tier}")
            tiers[tier] += 1
            xp += XP_CREDIT[tier]

        consumed = idx - before_idx
        if consumed != int(stage["judgmentsConsumed"]):
            raise RuntimeError(
                f"Stage{stage['stage']} judgment reconstruction mismatch: "
                f"trace={consumed} recorded={stage['judgmentsConsumed']}"
            )
        if sum(tiers.values()) != int(stage["rootActions"]):
            raise RuntimeError(f"Stage{stage['stage']} action-tier count mismatch")

        total_tiers.update(tiers)
        total_xp += xp
        out.append({
            "stage": int(stage["stage"]),
            "settled": bool(stage["settled"]),
            "buried": bool(stage["buried"]),
            "rootActions": int(stage["rootActions"]),
            "judgmentsConsumed": int(stage["judgmentsConsumed"]),
            "heavyActions": int(stage["heavyActions"]),
            "actionTierCounts": dict(sorted(tiers.items())),
            "xpCredit": round(xp, 6),
        })

    if idx != len(trace):
        raise RuntimeError(f"unused judgment trace entries: used={idx} total={len(trace)}")

    return {
        "stages": out,
        "totalActionTierCounts": dict(sorted(total_tiers.items())),
        "totalXpCredit": round(total_xp, 6),
        "traceJudgments": len(trace),
        "endingChargeReconstructed": int(charge),
    }


def run_variant(sim_fn, inputs, original_profile_for, cls, mode, seed, variant):
    base, temporal, direction, shop, integration, central = inputs
    base_profile = original_profile_for(shop, cls, PROFILE)
    effective_profile = dict(base_profile)
    if variant == "ATK_OFF":
        effective_profile["atk"] = 0
    elif variant != "ATK_ON":
        raise ValueError(variant)

    def variant_profile_for(shop_arg, cls_arg, name_arg):
        profile = dict(original_profile_for(shop_arg, cls_arg, name_arg))
        if name_arg == PROFILE and variant == "ATK_OFF":
            profile["atk"] = 0
        return profile

    bridge.integ.profile_for = variant_profile_for
    try:
        row = bridge.run_chain(
            sim_fn,
            base,
            temporal,
            direction,
            shop,
            integration,
            central,
            cls,
            mode,
            seed,
            ENTRY_CHARGE,
        )
    finally:
        bridge.integ.profile_for = original_profile_for

    rs = bridge.BRIDGE_CTX.get("runState") or {}
    trace = list(rs.get("_traceJudgments", []))
    awards = reconstruct_stage_awards(trace, row["stages"], ENTRY_CHARGE)

    recorded_actions = int(row["totalRootActions"])
    reconstructed_actions = sum(x["rootActions"] for x in awards["stages"])
    if recorded_actions != reconstructed_actions:
        raise RuntimeError(
            f"root action mismatch {cls} {mode} {seed} {variant}: "
            f"recorded={recorded_actions} reconstructed={reconstructed_actions}"
        )
    if awards["endingChargeReconstructed"] != int(row["chargeEnd"]):
        raise RuntimeError(
            f"ending charge mismatch {cls} {mode} {seed} {variant}: "
            f"reconstructed={awards['endingChargeReconstructed']} recorded={row['chargeEnd']}"
        )

    scale = float(integration["shopEffectScale"])
    row.update({
        "shopAttackVariant": variant,
        "effectiveShopRanks": effective_profile,
        "effectiveShopAtkPct": round(float(effective_profile["atk"]) * 0.08 * scale, 6),
        "xpCreditWeights": XP_CREDIT,
        "xpAwards": awards,
    })
    return row


def stage_map(row):
    return {int(x["stage"]): x for x in row["xpAwards"]["stages"]}


def pair_delta(off, on):
    off_stages = stage_map(off)
    on_stages = stage_map(on)
    common = sorted(set(off_stages) & set(on_stages))
    stage_rows = []
    for stage_no in common:
        a = off_stages[stage_no]
        b = on_stages[stage_no]
        both_settled = bool(a["settled"] and b["settled"])
        stage_rows.append({
            "stage": stage_no,
            "bothReached": True,
            "bothSettled": both_settled,
            "atkOffRootActions": a["rootActions"],
            "atkOnRootActions": b["rootActions"],
            "rootActionDeltaOnMinusOff": b["rootActions"] - a["rootActions"],
            "atkOffXpCredit": a["xpCredit"],
            "atkOnXpCredit": b["xpCredit"],
            "xpCreditDeltaOnMinusOff": round(b["xpCredit"] - a["xpCredit"], 6),
        })

    return {
        "class": off["class"],
        "mode": off["mode"],
        "baseSeed": off["baseSeed"],
        "atkOffThrough49": bool(off["settledThroughStage49"]),
        "atkOnThrough49": bool(on["settledThroughStage49"]),
        "survivalPromotion": bool((not off["settledThroughStage49"]) and on["settledThroughStage49"]),
        "survivalRegression": bool(off["settledThroughStage49"] and (not on["settledThroughStage49"])),
        "atkOffFailureStage": off["failureStage"],
        "atkOnFailureStage": on["failureStage"],
        "atkOffTotalRootActions": int(off["totalRootActions"]),
        "atkOnTotalRootActions": int(on["totalRootActions"]),
        "atkOffTotalXpCredit": off["xpAwards"]["totalXpCredit"],
        "atkOnTotalXpCredit": on["xpAwards"]["totalXpCredit"],
        "commonStageDeltas": stage_rows,
    }


def aggregate_pairs(pairs):
    result = {"overall": {}, "perClass": {}}
    groups = {"overall": pairs}
    for cls in CLASSES:
        groups[cls] = [p for p in pairs if p["class"] == cls]

    for label, rows in groups.items():
        stage_summary = {}
        for stage_no in bridge.STAGES:
            both_reached = []
            both_settled = []
            for pair in rows:
                sr = next((x for x in pair["commonStageDeltas"] if x["stage"] == stage_no), None)
                if sr is None:
                    continue
                both_reached.append(sr)
                if sr["bothSettled"]:
                    both_settled.append(sr)

            off_actions = [x["atkOffRootActions"] for x in both_settled]
            on_actions = [x["atkOnRootActions"] for x in both_settled]
            off_xp = [x["atkOffXpCredit"] for x in both_settled]
            on_xp = [x["atkOnXpCredit"] for x in both_settled]
            mean_off_actions = mean(off_actions)
            mean_on_actions = mean(on_actions)
            mean_off_xp = mean(off_xp)
            mean_on_xp = mean(on_xp)
            stage_summary[str(stage_no)] = {
                "pairedBothReached": len(both_reached),
                "pairedBothSettled": len(both_settled),
                "meanRootActionsAtkOff": r6(mean_off_actions),
                "meanRootActionsAtkOn": r6(mean_on_actions),
                "meanRootActionDeltaOnMinusOff": r6(
                    None if mean_off_actions is None else mean_on_actions - mean_off_actions
                ),
                "meanRootActionCompressionPct": r6(
                    None if not mean_off_actions else (mean_off_actions - mean_on_actions) / mean_off_actions
                ),
                "meanXpCreditAtkOff": r6(mean_off_xp),
                "meanXpCreditAtkOn": r6(mean_on_xp),
                "meanXpCreditDeltaOnMinusOff": r6(
                    None if mean_off_xp is None else mean_on_xp - mean_off_xp
                ),
                "meanXpCreditCompressionPct": r6(
                    None if not mean_off_xp else (mean_off_xp - mean_on_xp) / mean_off_xp
                ),
            }

        block = {
            "pairs": len(rows),
            "atkOffThrough49": sum(1 for p in rows if p["atkOffThrough49"]),
            "atkOnThrough49": sum(1 for p in rows if p["atkOnThrough49"]),
            "survivalPromotions": sum(1 for p in rows if p["survivalPromotion"]),
            "survivalRegressions": sum(1 for p in rows if p["survivalRegression"]),
            "stagePairedOpportunity": stage_summary,
        }
        if label == "overall":
            result["overall"] = block
        else:
            result["perClass"][label] = block
    return result


def main():
    original_next = install_judgment_trace()
    original_profile_for = bridge.integ.profile_for
    try:
        inputs = bridge.load_inputs()
        base, temporal, direction, shop, integration, central = inputs
        if float(integration["referenceWarmupSeconds"]) != 12.0:
            raise RuntimeError("bridge warmup contract changed")
        sim_fn = bridge.build_bridge_simulate()

        rows = []
        # Central-skilled lane: 20 paired seeds x five classes.
        for seed in SEEDS:
            for cls in CLASSES:
                for variant in VARIANTS:
                    rows.append(
                        run_variant(
                            sim_fn,
                            inputs,
                            original_profile_for,
                            cls,
                            "SKILLED_V2_CENTRAL",
                            seed,
                            variant,
                        )
                    )

        # All-perfect ceiling control: one deterministic case per class and variant.
        for cls in CLASSES:
            for variant in VARIANTS:
                rows.append(
                    run_variant(
                        sim_fn,
                        inputs,
                        original_profile_for,
                        cls,
                        "ALL_PERFECT",
                        1,
                        variant,
                    )
                )
    finally:
        bridge.bridge_next_judgment = original_next
        bridge.integ.profile_for = original_profile_for

    by_key = {
        (r["mode"], int(r["baseSeed"]), r["class"], r["shopAttackVariant"]): r
        for r in rows
    }
    pairs = []
    for mode in ("SKILLED_V2_CENTRAL", "ALL_PERFECT"):
        seeds = SEEDS if mode == "SKILLED_V2_CENTRAL" else [1]
        for seed in seeds:
            for cls in CLASSES:
                off = by_key[(mode, seed, cls, "ATK_OFF")]
                on = by_key[(mode, seed, cls, "ATK_ON")]
                pairs.append(pair_delta(off, on))

    skilled_pairs = [p for p in pairs if p["mode"] == "SKILLED_V2_CENTRAL"]
    perfect_pairs = [p for p in pairs if p["mode"] == "ALL_PERFECT"]

    sample_profile = bridge.integ.profile_for(inputs[3], "Knight", PROFILE)
    output = {
        "version": "p6-shop-exp-opportunity-attribution-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "purpose": (
            "Measure the incremental late-run shop ATK -> kill-speed/chronology -> valid timing-action "
            "opportunity -> provisional XP_CREDIT feedback on the admitted P5-P6 persistent-state bridge."
        ),
        "sourceBridge": {
            "branchBase": "timing-defense-workspace-temp-p5p6-fidelity@0c334efed0af8ddcdef4eb93c34146ecfa7dadf5",
            "runner": "tools/run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1.py",
        },
        "fixed": {
            "mode": "SKILLED_V2_CENTRAL plus ALL_PERFECT ceiling control",
            "seeds": SEEDS,
            "classes": CLASSES,
            "entryCharge": ENTRY_CHARGE,
            "entryComboBoundary": 0,
            "shopProfile": PROFILE,
            "shopEffectScale": float(inputs[4]["shopEffectScale"]),
            "fortAndDefRanksHeldIdenticalBetweenVariants": True,
            "currentBalancedProfileExample": sample_profile,
            "xpCreditWeights": XP_CREDIT,
            "heavyXpAwardSemantics": "ONE_ROOT_ACTION_ONE_XP_AWARD_DESPITE_TWO_JUDGMENTS",
        },
        "variants": {
            "ATK_OFF": "same BALANCED FORT/DEF ranks; ATK rank forced to zero",
            "ATK_ON": "existing BALANCED ATK/FORT/DEF diagnostic ranks",
        },
        "interpretationBoundary": [
            "This isolates the ATK component only; CRIT/CRITDMG/KNOCK are not included in this cross-class bridge.",
            "Stage46-49 already assumes Lv31 is acquired, so this run measures late XP-opportunity compression, not exact Lv31 reach timing.",
            "Only paired stages where both variants settle are used for clean opportunity-compression means; survival changes are reported separately.",
            "The current Stage48 armored/proxy center remains diagnostic and is not adopted.",
            "Fixed late-segment shop ranks are not actual Stage1-45 purchase history.",
            "P4 XP_CREDIT values remain provisional and are used here only for relative attribution.",
            "No EXP semantic, shop coefficient, class coefficient, encounter packet, or production value is frozen by this run.",
        ],
        "rows": rows,
        "pairs": pairs,
        "aggregate": {
            "skilled": aggregate_pairs(skilled_pairs),
            "allPerfect": aggregate_pairs(perfect_pairs),
        },
    }

    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    print(text)
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
