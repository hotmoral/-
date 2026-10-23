#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

SRC = Path("p6_shop_exp_opportunity_attribution_temp.json")


def mean(values):
    return sum(values) / len(values) if values else None


def r6(value):
    return None if value is None else round(float(value), 6)


def summarize(rows):
    def cohort(block):
        if not block:
            return {
                "pairs": 0,
                "meanAtkOffRootActions": None,
                "meanAtkOnRootActions": None,
                "meanRootActionDeltaOnMinusOff": None,
                "meanAtkOffXpCredit": None,
                "meanAtkOnXpCredit": None,
                "meanXpCreditDeltaOnMinusOff": None,
            }
        off_a = mean([p["atkOffTotalRootActions"] for p in block])
        on_a = mean([p["atkOnTotalRootActions"] for p in block])
        off_x = mean([p["atkOffTotalXpCredit"] for p in block])
        on_x = mean([p["atkOnTotalXpCredit"] for p in block])
        return {
            "pairs": len(block),
            "meanAtkOffRootActions": r6(off_a),
            "meanAtkOnRootActions": r6(on_a),
            "meanRootActionDeltaOnMinusOff": r6(on_a - off_a),
            "meanRootActionNetChangePct": r6((on_a - off_a) / off_a if off_a else None),
            "meanAtkOffXpCredit": r6(off_x),
            "meanAtkOnXpCredit": r6(on_x),
            "meanXpCreditDeltaOnMinusOff": r6(on_x - off_x),
            "meanXpCreditNetChangePct": r6((on_x - off_x) / off_x if off_x else None),
        }

    return {
        "allPairsIncludingSurvivalExtension": cohort(rows),
        "bothThrough49": cohort([p for p in rows if p["atkOffThrough49"] and p["atkOnThrough49"]]),
        "survivalPromotionsOnly": cohort([p for p in rows if p["survivalPromotion"]]),
        "survivalRegressionsOnly": cohort([p for p in rows if p["survivalRegression"]]),
    }


def grouped(pairs):
    out = {"overall": summarize(pairs), "perClass": {}}
    classes = sorted({p["class"] for p in pairs})
    for cls in classes:
        out["perClass"][cls] = summarize([p for p in pairs if p["class"] == cls])
    return out


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    pairs = data["pairs"]
    skilled = [p for p in pairs if p["mode"] == "SKILLED_V2_CENTRAL"]
    perfect = [p for p in pairs if p["mode"] == "ALL_PERFECT"]
    out = {
        "version": "p6-shop-exp-opportunity-cumulative-summary-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_DERIVED_FROM_EXISTING_B1_OUTPUT",
        "skilled": grouped(skilled),
        "allPerfect": grouped(perfect),
        "interpretationBoundary": [
            "allPairs includes survival-extension exposure and must not be interpreted as pure within-stage compression",
            "bothThrough49 isolates cumulative late-chain opportunity among pairs that settle both variants through Stage49",
            "survivalPromotionsOnly shows the competing path where shop ATK creates additional future-stage opportunity by preventing failure",
        ],
    }
    print("P6_SHOP_EXP_CUMULATIVE=" + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
