#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, math, statistics
from pathlib import Path

CLASSES = ["knight","rogue","tank","archer","mage"]
SEEDS = [101,211,307]
LEGACY_XP = {
    "NORMAL":8,"GOOD":12,"PERFECT":18,
    "HEAVY":10,"HEAVY+":14,"GREAT":18,"SUPER":23,"CRITICAL":28
}
MILESTONES=[6,11,16,21,26,31]

def q(vals,p):
    vals=sorted(vals)
    if not vals: return None
    if len(vals)==1: return vals[0]
    x=(len(vals)-1)*p
    lo=math.floor(x); hi=math.ceil(x)
    if lo==hi: return vals[lo]
    return vals[lo]*(hi-x)+vals[hi]*(x-lo)

def load_runner(path:Path):
    spec=importlib.util.spec_from_file_location("p3_runner",path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def legacy_threshold(level:int)->int:
    return sum(60+12*(l-1) for l in range(1,level))

def xp_by_stage(run):
    out={s:0 for s in range(1,11)}
    for rec in run["ledger"]:
        if rec.get("recordType")!="PowerAttribution" or rec.get("effectId")!="PLAYER_BASE_ATTACK":
            continue
        tier=rec.get("actionTransforms",{}).get("timingTier")
        if tier in LEGACY_XP:
            out[int(rec["stage"])]+=LEGACY_XP[tier]
    return out

def event_by_stage(run):
    out={}
    for row in run["stageSummaries"]:
        out[int(row["stage"])]=int(row["expEligibleEventsEnd"])-int(row["expEligibleEventsStart"])
    return out

def heavy_tier(a,b):
    if a=="P" and b=="P": return "CRITICAL"
    w=(2 if a=="P" else 1 if a=="G" else 0)+(2 if b=="P" else 1 if b=="G" else 0)
    if w>=3: return "SUPER"
    if w==2: return "GREAT"
    if w==1: return "HEAVY+"
    return "HEAVY"

def expected_turn_xp_current_central():
    states=["F","B"]
    pi={"F":.4,"B":.6}
    emit={"F":{"P":1.0,"G":0.0,"N":0.0},
          "B":{"P":.5,"G":1/3,"N":1/6}}
    trans={"F":{"F":.98,"B":.02},
           "B":{"F":1/75,"B":74/75}}
    joint={(a,b):0.0 for a in "PGN" for b in "PGN"}
    for s in states:
        for a,pa in emit[s].items():
            for s2,pt in trans[s].items():
                for b,pb in emit[s2].items():
                    joint[(a,b)]+=pi[s]*pa*pt*pb
    en=.1*8+.2*12+.7*18
    eh=sum(prob*LEGACY_XP[heavy_tier(a,b)] for (a,b),prob in joint.items())
    return .75*en+.25*eh

def expected_turn_xp_iid(m):
    en=sum(m[j]*{"N":8,"G":12,"P":18}[j] for j in "NGP")
    eh=0.0
    for a in "NGP":
        for b in "NGP":
            eh+=m[a]*m[b]*LEGACY_XP[heavy_tier(a,b)]
    return .75*en+.25*eh

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("runner",type=Path)
    ap.add_argument("fixture",type=Path)
    args=ap.parse_args()
    runner=load_runner(args.runner)
    fx=json.loads(args.fixture.read_text(encoding="utf-8"))

    lv1=[]; forced=[]
    for cls in CLASSES:
        for seed in SEEDS:
            r0,_=runner.primary_run(fx,cls,seed,"LV1_CONTINUITY")
            r1,_=runner.primary_run(fx,cls,seed,"FORCED_LV6_TRANSITION")
            lv1.append((cls,seed,r0)); forced.append((cls,seed,r1))

    cum_by_stage={s:[] for s in range(1,11)}
    unlocks={lv:[] for lv in MILESTONES}
    thresholds={str(lv):legacy_threshold(lv) for lv in MILESTONES}
    for cls,seed,run in lv1:
        sxp=xp_by_stage(run); cum=0; seen={}
        for s in range(1,11):
            cum+=sxp[s]; cum_by_stage[s].append(cum)
            for lv in MILESTONES:
                if lv not in seen and cum>=legacy_threshold(lv): seen[lv]=s
        for lv in MILESTONES: unlocks[lv].append(seen.get(lv))

    cum_stats={str(s):{"P25":q(v,.25),"P50":q(v,.5),"P75":q(v,.75)} for s,v in cum_by_stage.items()}
    unlock_stats={}
    for lv,vals in unlocks.items():
        present=[x for x in vals if x is not None]
        unlock_stats[str(lv)]={
            "reachedWithinP3":len(present),"runs":len(vals),
            "P25":q(present,.25) if present else None,
            "P50":q(present,.5) if present else None,
            "P75":q(present,.75) if present else None,
        }

    feedback={}
    for cls in CLASSES:
        ev0=[]; ev1=[]; xp0=[]; xp1=[]
        for c,seed,r in lv1:
            if c==cls: ev0.append(sum(event_by_stage(r).values())); xp0.append(sum(xp_by_stage(r).values()))
        for c,seed,r in forced:
            if c==cls: ev1.append(sum(event_by_stage(r).values())); xp1.append(sum(xp_by_stage(r).values()))
        m0=statistics.mean(ev0); m1=statistics.mean(ev1); x0=statistics.mean(xp0); x1=statistics.mean(xp1)
        feedback[cls]={
            "lv1EventMean":m0,"forcedLv6EventMean":m1,"eventDeltaPct":(m1/m0-1)*100 if m0 else None,
            "lv1LegacyCreditMean":x0,"forcedLv6LegacyCreditMean":x1,"legacyCreditDeltaPct":(x1/x0-1)*100 if x0 else None,
        }

    current=expected_turn_xp_current_central()
    avg=expected_turn_xp_iid({"N":.25,"G":.55,"P":.20})
    oldsk=expected_turn_xp_iid({"N":.10,"G":.50,"P":.40})
    perfect=expected_turn_xp_iid({"N":0.0,"G":0.0,"P":1.0})

    out={
        "version":"p4-exp-preproposal-diagnostics-v0.1",
        "status":"DERIVED_DIAGNOSTIC_NOT_DESIGN_AUTHORITY",
        "sourceBoundary":{"runner":"P3 canonical runner","fixture":"P3 canonical synthetic first-10 fixture","important":"P3 fixture is not exact launch authoring."},
        "legacyPrototype":{"grantByCompletedTurn":LEGACY_XP,"cumulativeMilestoneThresholds":thresholds,"p3First10CumulativeCreditQuantiles":cum_stats,"legacyThresholdUnlockStageInsideP3":unlock_stats},
        "lv6EventOpportunityFeedback":feedback,
        "legacyShapeExpectedGrantPerCompletedTurn":{"oldAverage_iid":avg,"oldSkilled_iid":oldsk,"currentCentral_markov":current,"perfect":perfect,"currentCentralVsOldAveragePct":(current/avg-1)*100,"perfectVsCurrentCentralPct":(perfect/current-1)*100},
        "interpretation":[
            "Legacy absolute level thresholds are structurally too fast for the current 50-Stage target.",
            "Legacy relative quality-reward shape remains separable from absolute threshold scale and can be tested independently.",
            "Forced Lv6 offensive power materially reduces later timing-event opportunity for Rogue/Archer/Mage in the P3 fixture.",
            "No class-specific EXP compensation is authorized by this diagnostic.",
            "No P4 EXP formula or threshold is frozen by this diagnostic."
        ]
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
