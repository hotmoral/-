#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "legacy-game-structure" / "data" / "p5_shop_economy_spend_capacity_fixture_v0_1.json"

CATEGORY_ORDER = ["atk", "crit", "critdmg", "fort", "def", "knock"]


def js_round_positive(value: float) -> int:
    return math.floor(value + 0.5)


def build_costs(fixture):
    base = fixture["rankBaseCosts"]
    mult = fixture["categoryMultipliers"]
    costs = {
        category: [js_round_positive(x * mult[category]) for x in base]
        for category in CATEGORY_ORDER
    }
    total = sum(sum(v) for v in costs.values())
    if total != fixture["fullShopReferenceCost"]:
        raise AssertionError(f"full-shop reference mismatch: {total} != {fixture['fullShopReferenceCost']}")
    return costs, total


def buy_priority(wallet, ranks, costs, priority):
    purchases = []
    while True:
        bought = False
        for category in priority:
            rank = ranks[category]
            if rank >= len(costs[category]):
                continue
            price = costs[category][rank]
            if wallet + 1e-9 >= price:
                wallet -= price
                ranks[category] += 1
                purchases.append({"category": category, "newRank": ranks[category], "cost": price})
                bought = True
                break
        if not bought:
            return wallet, purchases


def buy_balanced(wallet, ranks, costs):
    purchases = []
    while True:
        options = []
        for idx, category in enumerate(CATEGORY_ORDER):
            rank = ranks[category]
            if rank >= len(costs[category]):
                continue
            price = costs[category][rank]
            if wallet + 1e-9 >= price:
                options.append((rank, price, idx, category))
        if not options:
            return wallet, purchases
        _, price, _, category = min(options)
        wallet -= price
        ranks[category] += 1
        purchases.append({"category": category, "newRank": ranks[category], "cost": price})


def run_policy(fixture, costs, total_reference, spend_ratio, policy_name, role_class=None):
    total_budget = total_reference * spend_ratio
    first_stage = fixture["stageIncomeWeight"]["firstStage"]
    last_stage = fixture["stageIncomeWeight"]["lastShopStage"]
    weights = {stage: 55 + 12 * stage for stage in range(first_stage, last_stage + 1)}
    weight_total = sum(weights.values())
    ranks = {category: 0 for category in CATEGORY_ORDER}
    wallet = 0.0
    spent = 0
    snapshots = {}
    max_events = []

    policies = fixture["policies"]
    for stage in range(first_stage, last_stage + 1):
        wallet += total_budget * weights[stage] / weight_total
        purchases = []
        if policy_name == "BALANCED":
            wallet, purchases = buy_balanced(wallet, ranks, costs)
        elif policy_name == "SAVE_DELAY":
            if stage >= policies["SAVE_DELAY"]["spendStartStage"]:
                wallet, purchases = buy_balanced(wallet, ranks, costs)
        elif policy_name == "ROLE_AWARE":
            wallet, purchases = buy_priority(wallet, ranks, costs, policies["ROLE_AWARE"][role_class])
        else:
            wallet, purchases = buy_priority(wallet, ranks, costs, policies[policy_name])

        for purchase in purchases:
            spent += purchase["cost"]
            if purchase["newRank"] == len(costs[purchase["category"]]):
                max_events.append({"stage": stage, "category": purchase["category"]})

        if stage in fixture["snapshotStages"]:
            snapshots[str(stage)] = {
                "ranks": dict(ranks),
                "wallet": round(wallet, 6),
                "spent": spent,
                "spendRatioOfFullShop": round(spent / total_reference, 6),
            }

    all_max = all(ranks[c] == len(costs[c]) for c in CATEGORY_ORDER)
    return {
        "policy": policy_name if role_class is None else f"ROLE_AWARE:{role_class}",
        "inputSpendCapacityRatio": spend_ratio,
        "nominalTotalBudget": round(total_budget, 6),
        "snapshots": snapshots,
        "finalRanks": dict(ranks),
        "finalWallet": round(wallet, 6),
        "spent": spent,
        "spentRatioOfFullShop": round(spent / total_reference, 6),
        "maxEvents": max_events,
        "allSixMaxed": all_max,
    }


def main():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    costs, total_reference = build_costs(fixture)

    result = {
        "schemaVersion": "p5-shop-economy-spend-capacity-probe-output-v0.1",
        "fixtureSchemaVersion": fixture["schemaVersion"],
        "classification": "ECONOMY_ONLY_PREFLIGHT_NO_COMBAT_AUTHORITY",
        "referenceCosts": costs,
        "fullShopReferenceCost": total_reference,
        "ratioRuns": {},
        "centerKillSharePerturbationBalanced": {},
    }

    base_policies = ["ATTACK_HEAVY", "CRIT_HEAVY", "DEFENSE_HEAVY", "BALANCED", "SAVE_DELAY"]
    role_classes = list(fixture["policies"]["ROLE_AWARE"].keys())

    for ratio in fixture["spendCapacityRatios"]:
        key = f"{ratio:.2f}"
        runs = [run_policy(fixture, costs, total_reference, ratio, p) for p in base_policies]
        runs.extend(run_policy(fixture, costs, total_reference, ratio, "ROLE_AWARE", c) for c in role_classes)
        result["ratioRuns"][key] = runs

    for ratio in fixture["centerKillShareWalletPerturbationRatios"]:
        result["centerKillSharePerturbationBalanced"][f"{ratio:.2f}"] = run_policy(
            fixture, costs, total_reference, ratio, "BALANCED"
        )

    result["checks"] = {
        "noAllSixMaxoutInTestedRuns": all(
            not run["allSixMaxed"]
            for runs in result["ratioRuns"].values()
            for run in runs
        ),
        "balancedCenterRetainsLateChoice": not result["ratioRuns"]["0.50"][3]["allSixMaxed"],
        "productionValuesFrozen": False,
        "combatBalanceClaimAllowed": False,
    }

    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
