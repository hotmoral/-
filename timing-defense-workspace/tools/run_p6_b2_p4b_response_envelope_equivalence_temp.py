#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'
DATA=ROOT/'legacy-game-structure'/'data'
sys.path.insert(0,str(TOOLS))
import run_p4a_marker_inverse_design_v0_1 as p4a

CORPUS=DATA/'p4a_marker_opportunity_corpus_v0_1.json'
P4A_SUM=DATA/'p4a_marker_inverse_design_summary_v0_1.json'
P4B=DATA/'p4b_combat_feedback_divergence_v0_1.json'
LEVELS=(6,11,16,21,26,31)
ACTIVE_POWER_LEVELS=(6,11,16,21)
CLASSES=('knight','rogue','tank','archer','mage')
TIERS=('T1','T2','T3','T4')


def highest_unlocked(cum,thr):
    lv=1
    for x in LEVELS:
        if cum>=thr[x]: lv=x
        else: break
    return lv


def response_for(cls,lv,hist):
    if lv<6:return 1.0
    active=max(x for x in ACTIVE_POWER_LEVELS if x<=min(lv,21))
    return float(hist['all20ActionRatioVsLv1Median'][cls][f'Lv{active}'])


def simulate(stages,tier,seed_i,credit,cls,thr,hist):
    p=p4a.Central(p4a.derived_seed(tier,'CENTRAL',seed_i))
    action_no=1; cum=0.0; rows=[]
    dmg_n={'N':100.0,'G':140.0,'P':200.0}
    dmg_h={'HEAVY':180.0,'HEAVY+':230.0,'GREAT':300.0,'SUPER':400.0,'CRITICAL':600.0}
    c_n={'N':credit['NORMAL'],'G':credit['GOOD'],'P':credit['PERFECT']}
    c_h={k:credit[k] for k in ('HEAVY','HEAVY+','GREAT','SUPER','CRITICAL')}
    for st in stages:
        workload=float(st['workloadEhp']); turns=0; stage_credit=0.0
        while workload>0:
            lv=highest_unlocked(cum,thr)
            r=response_for(cls,lv,hist)
            if action_no%4==0:
                a=p.judge(); b=p.judge(); q=p4a.heavy_tier(a,b); base=dmg_h[q]; gain=c_h[q]
            else:
                q=p.judge(); base=dmg_n[q]; gain=c_n[q]
            # Archived action-opportunity response is represented as an equivalent workload-clearance multiplier.
            # r < 1 means fewer root actions than Lv1; therefore each surviving action clears 1/r baseline workload.
            workload-=base/r
            cum+=gain; stage_credit+=gain; turns+=1; action_no+=1
        rows.append({'stage':int(st['stage']),'turns':turns,'stageCredit':stage_credit,'cumCredit':cum})
    return rows


def unlock(rows,threshold):
    for r in rows:
        if r['cumCredit']>=threshold:return int(r['stage'])
    return 51


def main():
    corpus=p4a.normalize_corpus(json.loads(CORPUS.read_text()))
    p4a_sum=json.loads(P4A_SUM.read_text())
    hist=json.loads(P4B.read_text())
    thr={int(k):float(v) for k,v in p4a_sum['firstPassMidpointAnchorCandidates'].items()}
    fixtures={(f['tier'],f['envelope']):f for f in corpus['fixtures']}
    credit=corpus['qualityCredit']
    out={'version':'p6-b2-p4b-response-envelope-equivalence-temp-v0.1','authority':'TEMP_RECOVERED_EQUIVALENCE_PROBE_ONLY','shopInjected':False,'thresholds':thr,'perClass':{},'mismatch':{},'productionAuthority':False}
    exact=0; within1=0; total=0; abs_err=0; max_err=0
    for cls in CLASSES:
        out['perClass'][cls]={}
        target_cls=hist['p4aMidpointFeedbackPropagationP50Examples'][cls]
        for tier in TIERS:
            runs=[simulate(fixtures[(tier,'CENTRAL')]['stages'],tier,i,credit,cls,thr,hist) for i in range(1,101)]
            pred=[]
            for lv in LEVELS:
                vals=[unlock(r,thr[lv]) for r in runs]
                pred.append(float(p4a.quant(vals,.5)))
            target=[float(x) for x in target_cls[tier]]
            errs=[abs(a-b) for a,b in zip(pred,target)]
            exact+=sum(e<1e-9 for e in errs); within1+=sum(e<=1.0 for e in errs); total+=len(errs); abs_err+=sum(errs); max_err=max(max_err,max(errs))
            out['perClass'][cls][tier]={'predictedP50':pred,'historicalP50':target,'absError':errs}
    out['mismatch']={'points':total,'exactPoints':exact,'exactRate':round(exact/total,6),'within1StagePoints':within1,'within1StageRate':round(within1/total,6),'meanAbsStageError':round(abs_err/total,6),'maxAbsStageError':round(max_err,6)}
    # Gate intentionally strict enough to reject a merely qualitative lookalike while allowing lost-runner equivalence.
    out['recoveredEquivalenceGate']={'pass':(within1/total>=0.90 and abs_err/total<=0.75 and max_err<=3.0),'requirements':{'within1StageRateMin':0.90,'meanAbsStageErrorMax':0.75,'maxAbsStageErrorMax':3.0}}
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()
