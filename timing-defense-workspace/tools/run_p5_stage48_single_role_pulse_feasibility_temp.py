#!/usr/bin/env python3
"""TEMP P5 Stage48 single protected-role-pulse feasibility diagnostic.

Removes the repeated 4.9 s stress-cycle only for this bounded test and asks whether one
real-monster escort pulse can make SIEGER's role readable at all under current class/shop
power. All physical spawns remain x=0.92; monster/class/shop stats are unchanged.
No Stage48 content/cadence adoption or production authority.
"""
from __future__ import annotations

import copy
import inspect
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def row(typ,band,t,ref=0.0):
    # build_integrated_schedule: t = warmup(12) + ref - lead
    return {"type":typ,"band":int(band),"referenceOffset":float(ref),"spawnLeadSeconds":float(12.0+ref-t)}
def make(direction,name,escort_rows):
    d=copy.deepcopy(direction); s=d["stageDirection"]["48"]
    s["pressureCycleSecondsCandidate"]=999.0
    s["diagnosticPacket"]=list(escort_rows)+[row("SIEGER",2,8.0,2.0)]
    s["note"]=f"TEMP_SINGLE_ROLE_PULSE_FEASIBILITY:{name}"
    integ.validate_right_edge_contract(d)
    return d

def caller_now():
    f=inspect.currentframe()
    try:
        f=f.f_back
        while f:
            v=f.f_locals.get("now")
            if isinstance(v,(int,float)): return round(float(v),4)
            f=f.f_back
    finally: del f
    return None

def main():
    base=load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal=load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49=load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction=load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop=load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    integration=load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    integ.validate_right_edge_contract(direction); base=integ.inject_diagnostic_monsters(base,stage49); settled.install_fixed_schedule_hook()

    escorts=[
        row("SHIELD",-2,0.0), row("BRUTE",-1,1.0),
        row("SHIELD",-2,2.0), row("BRUTE",-1,3.0),
        row("SHIELD",-2,4.0), row("BRUTE",-1,5.0),
        row("SHIELD",-2,6.0), row("BRUTE",-1,7.0),
    ]
    variants={
        "SINGLE_ESCORT4":make(direction,"SINGLE_ESCORT4",escorts[:4]),
        "SINGLE_ESCORT6":make(direction,"SINGLE_ESCORT6",escorts[:6]),
        "SINGLE_ESCORT8":make(direction,"SINGLE_ESCORT8",escorts[:8]),
    }
    scale=float(integration["shopEffectScale"]); profile_name="BALANCED"
    starts=v2.pre_stage48_states(base,temporal,direction,shop,integration,[profile_name],scale)

    glb=integ.SIMULATE.__globals__; oh=glb["hit"]; on=glb["nearest"]; om=glb["make_mob"]
    trace=None
    def mw(mon,cfg,typ,band,idx):
        m=om(mon,cfg,typ,band,idx)
        if trace is not None and typ=="SIEGER": trace["s"]={"spawnAt":caller_now(),"firstDamageAt":None,"firstPrimaryAt":None,"deathAt":None,"deathX":None}
        return m
    def nw(mobs):
        p=on(mobs)
        if trace is not None and p is not None and p.typ=="SIEGER" and trace.get("s") and trace["s"]["firstPrimaryAt"] is None: trace["s"]["firstPrimaryAt"]=caller_now()
        return p
    def hw(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=False):
        t=caller_now(); iss=target is not None and getattr(target,"typ",None)=="SIEGER"; alive=bool(getattr(target,"alive",False)) if target else False; bx=float(getattr(target,"x",0.0)) if target else None
        if iss and trace is not None and trace.get("s") and trace["s"]["firstDamageAt"] is None: trace["s"]["firstDamageAt"]=t
        res=oh(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=armor_ignore)
        if iss and trace is not None and trace.get("s") and alive and not bool(getattr(target,"alive",False)) and trace["s"]["deathAt"] is None:
            trace["s"]["deathAt"]=t; trace["s"]["deathX"]=round(bx,4)
        return res
    glb["hit"]=hw; glb["nearest"]=nw; glb["make_mob"]=mw

    out={"version":"p5-stage48-single-role-pulse-feasibility-temp-v0.1","authority":"TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY","rows":[]}
    try:
        for name,d in variants.items():
            for cls in integ.CLASSES:
                st=starts[(profile_name,cls)]; trace={}
                sim,_=settled.simulate_stage(base,temporal,d,integration,cls,st["profile"],scale,48,st["startStage48Wall"],0.25 if cls=="Tank" else None,120.0)
                s=trace.get("s") or {}; sp=s.get("spawnAt"); fp=s.get("firstPrimaryAt"); fd=s.get("firstDamageAt"); de=s.get("deathAt")
                out["rows"].append({
                    "variant":name,"escortCount":int(name[-1]),"class":cls,
                    "windups":int(sim.get("siegerWindups") or 0),"shots":int(sim.get("siegerShots") or 0),"repositions":int(sim.get("siegerRepositions") or 0),
                    "wallHits":int(sim.get("wallHits") or 0),"endWall":sim.get("endWall"),"endActive":sim.get("endActive"),"burialTime":sim.get("burialTime"),
                    "firstDamageAfterSpawn":round(fd-sp,4) if fd is not None and sp is not None else None,
                    "firstPrimaryAfterSpawn":round(fp-sp,4) if fp is not None and sp is not None else None,
                    "deathAfterSpawn":round(de-sp,4) if de is not None and sp is not None else None,
                    "deathX":s.get("deathX"),
                    "diedBeforePrimary":bool(de is not None and (fp is None or de<fp-1e-9)),
                })
                trace=None
    finally:
        glb["hit"]=oh; glb["nearest"]=on; glb["make_mob"]=om
    text=json.dumps(out,indent=2,sort_keys=True); Path("p5_stage48_single_role_pulse_feasibility_temp.json").write_text(text+"\n",encoding="utf-8"); print(text)
if __name__=="__main__": main()
