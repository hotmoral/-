#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result", type=Path)
    args = ap.parse_args()
    x = json.loads(args.result.read_text(encoding="utf-8"))
    c = x["checks"]
    errors = []

    if x["authority"].get("survivalClaim") is not False:
        errors.append("survivalClaim must remain false")
    if c.get("invariantFailures"):
        errors.append(f"invariantFailures={len(c['invariantFailures'])}")
    if not c.get("earlyLv6DirectionalPass"):
        errors.append("earlyLv6DirectionalPass=false")

    rows = c["isolatedSameStageAtkDirection"]
    pairs = [p for r in rows for p in r["pairs"]]
    total_off = sum(int(p["off"]) for p in pairs)
    total_on = sum(int(p["on"]) for p in pairs)
    global_pass = total_on <= total_off

    listed = c.get("isolatedSameStageAtkPairViolations", [])
    derived = []
    for r in rows:
        for p in r["pairs"]:
            if int(p["on"]) > int(p["off"]):
                derived.append({
                    "fixture": r["fixture"], "class": r["class"], "stage": r["stage"],
                    "level": r["level"], "seed": p["seed"], "off": p["off"], "on": p["on"],
                })
    key = lambda z: (z["fixture"], z["class"], z["stage"], z["level"], z["seed"], z["off"], z["on"])
    if sorted(derived, key=key) != sorted(listed, key=key):
        errors.append("reported isolated ATK exceptions do not match derived exceptions")
    if not global_pass:
        errors.append(f"isolated same-stage ATK global direction failed: on={total_on} > off={total_off}")

    print("classification=", x["classification"])
    print("survivalClaim=", x["authority"]["survivalClaim"])
    print("invariantFailures=", len(c["invariantFailures"]))
    print("earlyLv6DirectionalPass=", c["earlyLv6DirectionalPass"])
    for r in c["earlyLv6Directional"]:
        print("EARLY", r["class"], r["deltaPct"], r["expected"], r["pass"])
    print("isolatedSameStageAtkGlobalDirectionPass=", global_pass)
    print("isolatedSameStageAtkTotalPairs=", len(pairs))
    print("isolatedSameStageAtkTotalOff=", total_off)
    print("isolatedSameStageAtkTotalOn=", total_on)
    print("isolatedSameStageAtkDeltaPct=", round((total_on / total_off - 1) * 100, 4) if total_off else None)
    print("isolatedSameStageAtkReportedExceptionCount=", len(listed))
    for v in listed:
        print("ATK_EXCEPTION", v)
    print("isolatedSameStageAtkPerGroupStrictPass=", c["isolatedSameStageAtkAggregatePass"],
          "(diagnostic only; contract allows reported discrete chronology exceptions)")
    print("cumulativePathStageRootActionIncreaseCount=", c["cumulativePathStageRootActionIncreaseCount"],
          "(report-only; cumulative paths diverge progression/judgment phase)")
    print("--- LV31 SUMMARY ---")
    for r in x["summary"]:
        print(r["fixture"], r["class"], "ATK_ON" if r["shopOn"] else "ATK_OFF",
              "reach", r["lv31ReachCount"], "meanStage", r["lv31ReachStageMean"],
              "range", r["lv31ReachStageMin"], r["lv31ReachStageMax"], "roots", r["rootActionsMean"])

    if errors:
        for e in errors:
            print("ERROR", e, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
