#!/usr/bin/env python3
"""TEMP P5 Stage48 armored + fodder + SUPPORTER mix screen.

Tests whether existing SUPPORTER speed aura can complement the user-approved limited armored front
and fodder-target layer, improving both protection time and SIEGER travel without touching global
SIEGER speed/standoff or any monster stat. Diagnostic only; no composition/timing is adopted/frozen.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2
import run_p5_stage48_armored_low_density_front_temp as low


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def caller_now():
    f=inspect.currentframe()
    try:
        f=f.f_back
        while f:
            v=f.f_locals.get("now")
            if isinstance(v,(int,float)): return round(float(v),4)
            f=f.f_back
    finally:
        del f
    return None

def r(typ,band,t): return low.row(typ,band,t)

def make(direction,name,rows): return low.make(direction,name,list(rows)+[low.row("SIEGER",2,8.0,2.0)])

def main():
    base=load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal=load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49=load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction=load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop=load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement=load("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration=load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    integ.validate_right_edge_contract(direction)
    base=integ.inject_diagnostic_monsters(base,stage49)
    base["monsterAnchors"]["ARMORED_DURABLE_PROXY"]=dict(refinement["knightRobustPair"]["anchor"])
    settled.install_fixed_schedule_hook()

    p3=[r("ARMORED_DURABLE_PROXY",-2,5.25),r("ARMORED_DURABLE_PROXY",0,6.25),r("ARMORED_DURABLE_PROXY",-1,7.25)]
    p2=[r("ARMORED_DURABLE_PROXY",-2,5.25),r("ARMORED_DURABLE_PROXY",-1,7.25)]
    grunt2=[r("GRUNT",1,5.85),r("GRUNT",0,6.98)]
    grunt3=[r("GRUNT",1,5.55),r("GRUNT",0,6.35),r("GRUNT",-2,6.98)]
    brute_grunt=[r("BRUTE",1,5.85),r("GRUNT",0,6.98)]
    support=[r("SUPPORTER",1,7.80)]

    variants={
        "P3_GRUNT2":make(direction,"P3_GRUNT2",p3+grunt2),
        "P3_GRUNT2_SUPPORT":make(direction,"P3_GRUNT2_SUPPORT",p3+grunt2+support),
        "P3_BRUTE_GRUNT":make(direction,"P3_BRUTE_GRUNT",p3+brute_grunt),
        "P3_BRUTE_GRUNT_SUPPORT":make(direction,"P3_BRUTE_GRUNT_SUPPORT",p3+brute_grunt+support),
        "P2_GRUNT3":make(direction,"P2_GRUNT3",p2+grunt3),
        "P2_GRUNT3_SUPPORT":make(direction,"P2_GRUNT3_SUPPORT",p2+grunt3+support),
        "P2_BRUTE_GRUNT_SUPPORT":make(direction,"P2_BRUTE_GRUNT_SUPPORT",p2+brute_grunt+support),
    }

    scale=float(integration["shopEffectScale"]); profile="BALANCED"
    starts=v2.pre_stage48_states(base,temporal,direction,shop,integration,[profile],scale)
    glb=integ.SIMULATE.__globals__; old_hit,old_make=glb["hit"],glb["make_mob"]; trace=None

    def make_wrap(mon,cfg,typ,band,idx):
        m=old_make(mon,cfg,typ,band,idx)
        if trace is not None and typ=="SIEGER": trace["s"]={"spawn":caller_now(),"first":None,"death":None,"deathX":None,"minX":float(m.x)}
        return m

    def hit_wrap(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=False):
        t=caller_now(); typ=getattr(target,"typ",None) if target is not None else None; alive=bool(getattr(target,"alive",False)) if target is not None else False; x=float(getattr(target,"x",0.0)) if target is not None else None
        if trace is not None and typ=="SIEGER":
            s=trace.get("s")
            if s and s["first"] is None: s["first"]=t; s["firstRaw"]=round(float(raw),3)
        res=old_hit(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=armor_ignore)
        if trace is not None and typ=="SIEGER" and alive and not bool(getattr(target,"alive",False)):
            s=trace.get("s")
            if s and s["death"] is None: s["death"]=t; s["deathX"]=round(x,4)
        return res

    glb["hit"],glb["make_mob"]=hit_wrap,make_wrap
    out={"version":"p5-stage48-armored-fodder-support-mix-temp-v0.1","authority":"TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY","rows":[],"schedules":{}}
    try:
        for name,d in variants.items():
            cfg=integ.stage_temporal(temporal,d,integration,48,"Mage")
            out["schedules"][name]=[{"t":round(t,3),"type":typ,"band":band} for t,typ,band in integ.build_integrated_schedule(cfg)]
            for cls in integ.CLASSES:
                st=starts[(profile,cls)]; trace={}
                sim,_=settled.simulate_stage(base,temporal,d,integration,cls,st["profile"],scale,48,st["startStage48Wall"],0.25 if cls=="Tank" else None,120.0)
                s=trace.get("s") or {}; sp,first,death=s.get("spawn"),s.get("first"),s.get("death")
                out["rows"].append({"variant":name,"class":cls,"firstDamageAfterSpawn":round(first-sp,4) if first is not None and sp is not None else None,"firstDamageRaw":s.get("firstRaw"),"deathAfterSpawn":round(death-sp,4) if death is not None and sp is not None else None,"deathX":s.get("deathX"),"siegerWindups":int(sim.get("siegerWindups") or 0),"siegerShots":int(sim.get("siegerShots") or 0),"siegerRepositions":int(sim.get("siegerRepositions") or 0),"wallLoss":round(float(st["startStage48Wall"])-float(sim.get("endWall") or 0.0),3),"burialTime":sim.get("burialTime")})
                trace=None
    finally:
        glb["hit"],glb["make_mob"]=old_hit,old_make
    text=json.dumps(out,indent=2,sort_keys=True); Path("p5_stage48_armored_fodder_support_mix_temp.json").write_text(text+"\n",encoding="utf-8"); print(text)

if __name__=="__main__": main()
