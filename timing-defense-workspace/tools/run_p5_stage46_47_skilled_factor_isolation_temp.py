#!/usr/bin/env python3
"""TEMP P5 Stage46-47 skilled timing-quality factor isolation.

Separates two effects exposed by SKILLED_V2_CENTRAL:
A) lower ordinary judgment tiers;
B) reduced P×P / Lv31-final frequency.

Modes:
- ALL_PERFECT: existing idealized P5 control.
- CENTRAL_FULL: central ordinary + central Heavy pair.
- CENTRAL_NORMAL_ONLY: central ordinary judgments, but Heavy forced P×P/CRITICAL.
- CENTRAL_HEAVY_ONLY: ordinary forced PERFECT, Heavy pair follows central model.

All central modes still consume the same underlying judgment stream so Markov state
chronology stays comparable. Diagnostic only; no adoption/freeze/production authority.
"""
from __future__ import annotations

import inspect
import json
from collections import Counter
from pathlib import Path

import yaml

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46
import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_armored_standoff_hybrid_temp as hybrid
from simulate_class_aware_layer_a import BASE_DAMAGE, strong_tier
from validate_skilled_v2_central_sequence import RNG, choose

SEEDS = list(range(1, 21))
PROFILE = "BALANCED"
DRAIN_SECONDS = 240.0
MODES = ("CENTRAL_FULL", "CENTRAL_NORMAL_ONLY", "CENTRAL_HEAVY_ONLY")


def load_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def load_yaml(path): return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def row_seed(base_seed, cls):
    h=2166136261
    for b in f"{base_seed}|P5_STAGE46_47_FACTOR|{cls}".encode():
        h ^= b; h=(h*16777619)&0xffffffff
    return h or 0x6D2B79F5


def stream(cfg, seed):
    model=cfg["model"]; rng=RNG(seed); state=choose(model["initialState"],rng.unit())
    while True:
        s=model["states"][state]
        j=choose(s["judgmentDistribution"],rng.unit())
        yield j
        state=choose(s["transitionAfterJudgment"],rng.unit())


def build_mode_sim(ctx):
    src=inspect.getsource(stage46.simulate)
    old='''            attack_no += 1\n            heavy = attack_no % heavy_every == 0\n            if heavy:\n                heavy_index += 1\n            is_miss = heavy and heavy_index in missed_heavy_indices\n            tier = "SUPER" if is_miss else ("CRITICAL" if heavy else "PERFECT")\n            base_damage = 400 if is_miss else (600 if heavy else 200)\n            if heavy and not is_miss:\n                stats["pxpCount"] += 1\n            if is_miss:\n                stats["heavyMissCount"] += 1\n            primary = nearest(mobs)\n            final = has_lv31 and heavy and not is_miss\n'''
    new='''            attack_no += 1\n            heavy = attack_no % heavy_every == 0\n            if heavy:\n                heavy_index += 1\n            is_miss = False\n            if heavy:\n                _sx = next(_factor_ctx["stream"])\n                _sy = next(_factor_ctx["stream"])\n                _observed = _strong_tier(_sx, _sy)\n                tier = "CRITICAL" if _factor_ctx["mode"] == "CENTRAL_NORMAL_ONLY" else _observed\n                _factor_ctx["judgments"].extend((_sx, _sy))\n                _factor_ctx["observedHeavyTiers"][_observed] = _factor_ctx["observedHeavyTiers"].get(_observed, 0) + 1\n            else:\n                _sx = next(_factor_ctx["stream"])\n                _sy = None\n                tier = "PERFECT" if _factor_ctx["mode"] == "CENTRAL_HEAVY_ONLY" else _sx\n                _factor_ctx["judgments"].append(_sx)\n            base_damage = float(_base_damage_map[tier])\n            if heavy and tier == "CRITICAL":\n                stats["pxpCount"] += 1\n            if heavy and tier != "CRITICAL":\n                stats["heavyMissCount"] += 1\n            primary = nearest(mobs)\n            final = has_lv31 and heavy and tier == "CRITICAL"\n'''
    if src.count(old)!=1: raise RuntimeError("timing block changed")
    skilled_src=src.replace(old,new,1)
    stage46._factor_ctx=ctx; stage46._strong_tier=strong_tier; stage46._base_damage_map=BASE_DAMAGE
    original=integ.inspect.getsource
    def gs(obj): return skilled_src if obj is stage46.simulate else original(obj)
    integ.inspect.getsource=gs
    try: fn=integ.build_identity_aware_simulate()
    finally: integ.inspect.getsource=original
    return hybrid.install_fixed_schedule_hook_on(fn)


def inputs():
    base=load_json("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal=load_json("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49=load_json("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction=load_json("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop=load_json("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement=load_json("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration=load_json("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    central=load_yaml("legacy-game-structure/data/skilled_v2_central_sequence_candidate_v0_1.yaml")
    base=integ.inject_diagnostic_monsters(base,stage49)
    base["monsterAnchors"]["ARMORED_DURABLE_PROXY"]=dict(refinement["knightRobustPair"]["anchor"])
    return base,temporal,direction,shop,integration,central


def chain(sim_fn,base,temporal,direction,shop,integration,cls,ctx=None):
    scale=float(integration["shopEffectScale"]); profile=integ.profile_for(shop,cls,PROFILE)
    wall_max=float(integration["startingBaseWallHp"])+float(profile["fort"])*100.0*scale
    current=wall_max; stages=[]
    for stage_no in (46,47):
        cfg,schedule=settled.fixed_stage_cfg(temporal,direction,integration,stage_no,cls,DRAIN_SECONDS)
        row=sim_fn(base,cfg,cls,True,(),overrides={"shockwaveCoefficient":0.25} if cls=="Tank" else None,shop_profile=profile,effect_scale=scale,start_wall_current=current)
        current=float(row["endWall"])
        stages.append({"stage":stage_no,"settled":row.get("burialTime") is None and int(row.get("endActive") or 0)==0,"buried":row.get("burialTime") is not None,"endWall":round(current,3),"pxp":int(row.get("pxpCount") or 0),"nonPxpHeavy":int(row.get("heavyMissCount") or 0),"siegerShots":int(row.get("siegerShots") or 0)})
        if row.get("burialTime") is not None or int(row.get("endActive") or 0)!=0: break
    return {"class":cls,"through47":len(stages)==2 and all(s["settled"] for s in stages),"finalWall":round(current,3),"stages":stages}


def main():
    base,temporal,direction,shop,integration,central=inputs()
    # Fidelity compatibility: authoritative HEAVY+ knockback equals GOOD/GREAT = 0.013.
    old_bk=stage46.basic_knock
    def bk(tier): return 0.013 if tier=="HEAVY+" else old_bk(tier)
    stage46.basic_knock=bk

    original=hybrid.install_fixed_schedule_hook_on(integ.SIMULATE)
    ctx={"stream":None,"mode":None,"judgments":[],"observedHeavyTiers":{}}
    mode_sim=build_mode_sim(ctx)
    out={"version":"p5-stage46-47-skilled-factor-isolation-temp-v0.1","authority":"TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE","seeds":SEEDS,"rows":[]}

    for cls in integ.CLASSES:
        r=chain(original,base,temporal,direction,shop,integration,cls)
        r.update({"mode":"ALL_PERFECT","seed":None}); out["rows"].append(r)

    for mode in MODES:
        for seed in SEEDS:
            for cls in integ.CLASSES:
                ctx["stream"]=stream(central,row_seed(seed,cls)); ctx["mode"]=mode; ctx["judgments"]=[]; ctx["observedHeavyTiers"]={}
                r=chain(mode_sim,base,temporal,direction,shop,integration,cls,ctx)
                r.update({"mode":mode,"seed":seed,"judgments":dict(Counter(ctx["judgments"])),"observedHeavyTiers":dict(sorted(ctx["observedHeavyTiers"].items()))})
                out["rows"].append(r)

    agg={}
    for mode in ("ALL_PERFECT",)+MODES:
        rows=[r for r in out["rows"] if r["mode"]==mode]
        per={}
        for cls in integ.CLASSES:
            rr=[r for r in rows if r["class"]==cls]
            per[cls]={"through47":sum(1 for r in rr if r["through47"]),"cases":len(rr),"stage46Fails":sum(1 for r in rr if r["stages"] and r["stages"][-1]["stage"]==46 and not r["through47"]),"finalWalls":[r["finalWall"] for r in rr]}
        agg[mode]={"through47":sum(1 for r in rows if r["through47"]),"cases":len(rows),"perClass":per}
    out["aggregate"]=agg
    text=json.dumps(out,indent=2,sort_keys=True); Path("p5_stage46_47_skilled_factor_isolation_temp.json").write_text(text+"\n",encoding="utf-8"); print(text)

if __name__=="__main__": main()
