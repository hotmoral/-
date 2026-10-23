#!/usr/bin/env python3
"""TEMP P5 Stage48 real-monster overtake-handoff diagnostic.

Question: can faster real monsters spawned after SIEGER physically overtake it and take over
frontmost screening late enough to create readable SIEGER role opportunity?

No monster/class/shop stat changes. Stage48 cycle remains 4.9 s. All physical spawns remain
at x=0.92. Band separation is diagnostic only. No candidate adoption or production authority.
"""
from __future__ import annotations

import copy
import inspect
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2

REAL = {"BRUTE", "CHARGER", "FLYER", "GRUNT", "RUNNER", "SHIELD", "SIEGER", "SPLITTER", "SUPPORTER"}


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def e(typ, band, ref, lead):
    assert typ in REAL
    return {"type":typ,"band":int(band),"referenceOffset":float(ref),"spawnLeadSeconds":float(lead)}

def first_time(row): return 12.0 + float(row["referenceOffset"]) - float(row["spawnLeadSeconds"])

def make_variant(direction, name, screens, sieger):
    d=copy.deepcopy(direction)
    s48=d["stageDirection"]["48"]
    assert abs(float(s48["pressureCycleSecondsCandidate"])-4.9)<1e-9
    packet=list(screens)+[sieger,e("RUNNER",-1,3.6,0.0),e("CHARGER",1,4.1,0.0)]
    s48["diagnosticPacket"]=packet
    s48["note"]=f"TEMP_OVERTAKE_HANDOFF:{name}"
    integ.validate_right_edge_contract(d)
    return d

def caller_now():
    f=inspect.currentframe()
    try:
        f=f.f_back
        while f is not None:
            v=f.f_locals.get("now")
            if isinstance(v,(int,float)): return round(float(v),4)
            f=f.f_back
    finally:
        del f
    return None

def main():
    base=load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal=load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49=load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction=load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop=load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    integration=load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    integ.validate_right_edge_contract(direction)
    base=integ.inject_diagnostic_monsters(base,stage49)
    settled.install_fixed_schedule_hook()

    sieger=e("SIEGER",2,2.0,6.0)  # first authored SIEGER t=8.0
    variants={
        # Geometry-isolated four-BRUTE baseline from prior diagnostic.
        "ISO_BRUTE4_BASELINE": make_variant(direction,"ISO_BRUTE4_BASELINE",[
            e("BRUTE",-2,0.0,11.0), e("BRUTE",-1,0.5,10.0),
            e("BRUTE",-2,1.0,9.0), e("BRUTE",-1,1.5,8.0),
        ],sieger),
        # Preserve four total escort bodies: two early BRUTEs, then two SHIELDs spawned after SIEGER.
        # SHIELD speed .057 vs SIEGER .045: +1.3s spawn delay catches ~6.18s after SIEGER;
        # +2.3s delay catches ~10.93s after SIEGER (straight-line no-knock/no-kill derivation).
        "BRUTE2_SHIELD2_HANDOFF": make_variant(direction,"BRUTE2_SHIELD2_HANDOFF",[
            e("BRUTE",-2,0.0,11.0),      # t=1.0
            e("BRUTE",-1,0.5,9.5),       # t=3.0
            e("SHIELD",-2,2.5,5.2),      # t=9.3
            e("SHIELD",-1,3.0,4.7),      # t=10.3
        ],sieger),
        # Earlier first handoff / later second handoff.
        "BRUTE2_SHIELD2_WIDE_HANDOFF": make_variant(direction,"BRUTE2_SHIELD2_WIDE_HANDOFF",[
            e("BRUTE",-2,0.0,11.0),      # t=1.0
            e("BRUTE",-1,0.5,9.5),       # t=3.0
            e("SHIELD",-2,2.4,5.4),      # t=9.0  (+1.0)
            e("SHIELD",-1,3.1,4.6),      # t=10.5 (+2.5)
        ],sieger),
        # One late SPLITTER replaces the second SHIELD; if killed ahead of SIEGER, its children create a real handoff.
        "BRUTE2_SHIELD_SPLITTER_HANDOFF": make_variant(direction,"BRUTE2_SHIELD_SPLITTER_HANDOFF",[
            e("BRUTE",-2,0.0,11.0),
            e("BRUTE",-1,0.5,9.5),
            e("SHIELD",-2,2.4,5.4),      # t=9.0
            e("SPLITTER",-1,3.0,3.2),    # t=11.8 (+3.8; catch near late travel window)
        ],sieger),
    }

    scale=float(integration["shopEffectScale"]); profile_name="BALANCED"
    starts=v2.pre_stage48_states(base,temporal,direction,shop,integration,[profile_name],scale)

    glb=integ.SIMULATE.__globals__
    original_hit=glb["hit"]; original_nearest=glb["nearest"]; original_make=glb["make_mob"]
    trace=None

    def make_wrap(mon,cfg,typ,band,idx):
        m=original_make(mon,cfg,typ,band,idx)
        if trace is not None and typ=="SIEGER":
            trace["siegers"][m.id]={"id":m.id,"spawnAt":caller_now(),"band":int(m.band),"firstDamageAt":None,"firstPrimaryAt":None,"deathAt":None,"deathX":None}
        return m
    def nearest_wrap(mobs):
        p=original_nearest(mobs)
        if trace is not None and p is not None and p.typ=="SIEGER":
            x=trace["siegers"].get(p.id)
            if x is not None and x["firstPrimaryAt"] is None: x["firstPrimaryAt"]=caller_now()
        return p
    def hit_wrap(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=False):
        t=caller_now(); is_s=target is not None and getattr(target,"typ",None)=="SIEGER"
        alive=bool(getattr(target,"alive",False)) if target is not None else False
        bx=float(getattr(target,"x",0.0)) if target is not None else None
        if is_s and trace is not None:
            it=trace["siegers"].get(str(target.id))
            if it is not None and it["firstDamageAt"] is None: it["firstDamageAt"]=t
        result=original_hit(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=armor_ignore)
        if is_s and trace is not None:
            it=trace["siegers"].get(str(target.id)); after=bool(getattr(target,"alive",False))
            if it is not None and alive and not after and it["deathAt"] is None:
                it["deathAt"]=t; it["deathX"]=round(bx,4)
        return result
    glb["make_mob"]=make_wrap; glb["nearest"]=nearest_wrap; glb["hit"]=hit_wrap

    out={"version":"p5-stage48-overtake-handoff-temp-v0.1","authority":"TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY","variants":{}}
    try:
        for name,d in variants.items():
            packet=d["stageDirection"]["48"]["diagnosticPacket"]
            rows=[]
            for cls in integ.CLASSES:
                st=starts[(profile_name,cls)]; trace={"siegers":{}}
                row,_=settled.simulate_stage(base,temporal,d,integration,cls,st["profile"],scale,48,st["startStage48Wall"],0.25 if cls=="Tank" else None,120.0)
                items=list(trace["siegers"].values())
                for it in items:
                    sp=it.get("spawnAt"); fd=it.get("firstDamageAt"); fp=it.get("firstPrimaryAt"); de=it.get("deathAt")
                    it["damagedBeforePrimary"]=bool(fd is not None and (fp is None or fd<fp-1e-9))
                    it["diedBeforePrimary"]=bool(de is not None and (fp is None or de<fp-1e-9))
                    it["secondsToPrimary"]=round(fp-sp,4) if fp is not None and sp is not None else None
                    it["lifeSeconds"]=round(de-sp,4) if de is not None and sp is not None else None
                rows.append({
                    "class":cls,"windups":int(row.get("siegerWindups") or 0),"shots":int(row.get("siegerShots") or 0),"repositions":int(row.get("siegerRepositions") or 0),
                    "wallHits":int(row.get("wallHits") or 0),"endWall":row.get("endWall"),
                    "damagedBeforePrimary":sum(x["damagedBeforePrimary"] for x in items),"diedBeforePrimary":sum(x["diedBeforePrimary"] for x in items),"everPrimary":sum(x["firstPrimaryAt"] is not None for x in items),
                    "maxSecondsToPrimary":max((x["secondsToPrimary"] for x in items if x["secondsToPrimary"] is not None),default=None),
                    "minDeathX":min((x["deathX"] for x in items if x["deathX"] is not None),default=None),
                    "siegers":items,
                })
                trace=None
            out["variants"][name]={
                "firstCycleSchedule":[{"type":x["type"],"band":x["band"],"time":round(first_time(x),3)} for x in packet],
                "rows":rows,
                "aggregate":{"windupCases":sum(r["windups"]>0 for r in rows),"totalWindups":sum(r["windups"] for r in rows),"shotCases":sum(r["shots"]>0 for r in rows),"totalShots":sum(r["shots"] for r in rows)},
            }
    finally:
        glb["make_mob"]=original_make; glb["nearest"]=original_nearest; glb["hit"]=original_hit

    text=json.dumps(out,indent=2,sort_keys=True)
    Path("p5_stage48_overtake_handoff_temp.json").write_text(text+"\n",encoding="utf-8")
    print(text)

if __name__=="__main__": main()
