#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

def load_runner(path:Path):
    spec=importlib.util.spec_from_file_location("p3runner",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    ap=argparse.ArgumentParser()
    root=Path(__file__).resolve().parents[1]
    ap.add_argument("--fixture",type=Path,default=root/"legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json")
    ap.add_argument("--runner",type=Path,default=root/"tools/run_p3_persistent_kernel_v0_1.py")
    args=ap.parse_args()
    fx=json.loads(args.fixture.read_text(encoding="utf-8"))
    errors=[]
    if fx.get("status")!="USER_APPROVED_TEST_FIXTURE_NOT_PRODUCTION_AUTHORING":
        errors.append("fixture status must remain test-only")
    tc=fx.get("testControls",{})
    if tc.get("classes")!=["knight","rogue","tank","archer","mage"]: errors.append("class matrix mismatch")
    if tc.get("baseSeeds")!=[101,211,307]: errors.append("seed matrix mismatch")
    if tc.get("lanes")!=["LV1_CONTINUITY","FORCED_LV6_TRANSITION"]: errors.append("lane matrix mismatch")
    if tc.get("forcedLv6Stage")!=6: errors.append("forced Lv6 Stage must be 6 for approved P3 fixture")
    stages=fx.get("stages",[])
    if len(stages)!=10 or [x.get("stage") for x in stages]!=list(range(1,11)):
        errors.append("exactly 10 ordered fixture stages required")
    recipe_ids={p["recipeId"] for s in stages for p in s.get("phases",[])}
    if recipe_ids-{"T1_E01_M","T1_E02_M"}: errors.append(f"unapproved main-lane recipes: {sorted(recipe_ids)}")
    monster_types={x["type"] for r in fx.get("recipes",{}).values() for x in r.get("spawns",[])}
    if monster_types-{"GRUNT","RUNNER"}: errors.append(f"unapproved first-10 monster types: {sorted(monster_types)}")
    if "BRUTE" in monster_types: errors.append("BRUTE must not appear in P3 main fixture")
    if tc.get("shopPolicy")!="OFF_NEUTRAL": errors.append("shop policy must remain OFF_NEUTRAL")
    if errors:
        print(json.dumps({"recordType":"P3_VALIDATION","result":"FAIL","errors":errors},separators=(",",":")))
        return 2
    runner=load_runner(args.runner)
    primary,fixtures,summary=runner.execute(fx)
    if len(primary)!=30: errors.append(f"expected 30 primary runs, got {len(primary)}")
    if len(fixtures)<7: errors.append(f"expected >=7 targeted fixtures, got {len(fixtures)}")
    if summary.get("classification")!="P3_STRUCTURAL_PASS": errors.append("runner did not classify structural PASS")
    if not all(r.get("playerStreamContinuous") for r in primary): errors.append("player sequence continuity failed")
    if not all(r.get("deterministic") for r in primary): errors.append("deterministic replay failed")
    if not all(r.get("stagesCompleted")==10 for r in primary): errors.append("one or more primary runs did not settle 10 stages")
    forced=[r for r in primary if r["lane"]=="FORCED_LV6_TRANSITION"]
    lv1=[r for r in primary if r["lane"]=="LV1_CONTINUITY"]
    if len(forced)!=15 or len(lv1)!=15: errors.append("lane population mismatch")
    by_class={c:sum(r.get("lv6AttributionEntries",0) for r in forced if r["classId"]==c) for c in tc["classes"]}
    if any(v<=0 for v in by_class.values()): errors.append(f"missing forced Lv6 attribution: {by_class}")
    if any(r.get("lv6AttributionEntries",0)!=0 for r in lv1): errors.append("Lv1 lane contains Lv6 attribution")
    if not all(f.get("pass") for f in fixtures): errors.append("targeted fixture failure")
    attr=[f for f in fixtures if f["fixture"]=="F8_BASE_HP_ATTRITION_CONTINUITY"]
    if not attr or not attr[0]["pass"] or not (attr[0]["afterStage1"]<attr[0]["startHp"] and attr[0]["afterStage2"]<=attr[0]["afterStage1"]):
        errors.append("base HP attrition continuity evidence missing")
    out={"recordType":"P3_VALIDATION","result":"PASS" if not errors else "FAIL","errors":errors,
         "primaryRuns":len(primary),"targetedFixtures":len(fixtures),"lv6AttributionByClass":by_class,
         "combo40ObservedRuns":summary.get("combo40ObservedRuns"),"warning":"Structural test only; no balance number frozen."}
    print(json.dumps(out,ensure_ascii=False,separators=(",",":")))
    return 0 if not errors else 2

if __name__=="__main__":
    raise SystemExit(main())
