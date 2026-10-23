#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'; DATA=ROOT/'legacy-game-structure'/'data'
sys.path.insert(0,str(TOOLS))
import run_p4a_marker_inverse_design_v0_1 as p4a
import run_p6_b2_p4b_reconstruction_preflight_temp as static_probe
import run_skilled_v2_central_role_probe as materializer

CORPUS=DATA/'p4a_marker_opportunity_corpus_v0_1.json'
P4A_SUM=DATA/'p4a_marker_inverse_design_summary_v0_1.json'
P4B=DATA/'p4b_combat_feedback_divergence_v0_1.json'
BASE=DATA/'model_a_representative_recipes_v0_1.yaml'
KIN=DATA/'model_a_kinematic_anchor_v0_1.yaml'
COMBAT=DATA/'model_a_combat_sensitivity_anchor_v0_1.yaml'
OVERLAYS=[DATA/'model_a_critical_role_expression_candidates_v0_1.yaml',DATA/'model_a_additional10_role_expression_candidates_v0_1.yaml']
LEVELS=(6,11,16,21,26,31); ACTIVE=(6,11,16,21)
CLASSES=('knight','rogue','tank','archer','mage'); TIERS=('T1','T2','T3','T4')
GATE={'within1StageRateMin':.90,'meanAbsStageErrorMax':.75,'maxAbsStageErrorMax':3.0}

def load_yaml(p): return yaml.safe_load(p.read_text()) or {}

def highest(cum,thr):
    lv=1
    for x in LEVELS:
        if cum>=thr[x]:lv=x
        else:break
    return lv

def active_lv(lv): return max((x for x in ACTIVE if x<=min(lv,21)),default=1)

def rank_calibrate(raw_by_id,target_min,target_med,target_max):
    ordered=sorted(raw_by_id.items(),key=lambda kv:(kv[1],kv[0])); n=len(ordered); out={}
    for rank,(rid,_) in enumerate(ordered):
        q=rank/(n-1) if n>1 else .5
        if q<=.5: val=target_min+(target_med-target_min)*(q/.5)
        else: val=target_med+(target_max-target_med)*((q-.5)/.5)
        out[rid]=val
    return out

def build_recipe_maps(hist):
    base=load_yaml(BASE); kin=load_yaml(KIN); combat=load_yaml(COMBAT)
    recipes=materializer.materialize_all20(base,kin,[load_yaml(p) for p in OVERLAYS])
    maps={c:{} for c in CLASSES}
    for cls in CLASSES:
        baseline={r['id']:static_probe.simulate(r,combat,cls,1) for r in recipes}
        for lv in ACTIVE:
            raw={r['id']:static_probe.simulate(r,combat,cls,lv)/baseline[r['id']] for r in recipes}
            tr=hist['all20ActionRatioRanges'][cls][f'Lv{lv}']; med=float(hist['all20ActionRatioVsLv1Median'][cls][f'Lv{lv}'])
            maps[cls][lv]=rank_calibrate(raw,float(tr[0]),med,float(tr[1]))
    return maps

def response_global(cls,lv,hist,stage):
    al=active_lv(lv)
    return 1.0 if al==1 else float(hist['all20ActionRatioVsLv1Median'][cls][f'Lv{al}'])

def response_recipe(cls,lv,hist,stage,maps):
    al=active_lv(lv)
    if al==1:return 1.0
    bundle=stage['recipeBundle']; vals=[]; weights=[]
    for rid in bundle:
        vals.append(float(maps[cls][al][rid])); weights.append(float(p4a.WORK[rid]))
    return sum(v*w for v,w in zip(vals,weights))/sum(weights) if weights else float(hist['all20ActionRatioVsLv1Median'][cls][f'Lv{al}'])

def simulate(stages,tier,seed_i,credit,cls,thr,hist,mode,maps):
    p=p4a.Central(p4a.derived_seed(tier,'CENTRAL',seed_i)); action_no=1; cum=0.; rows=[]
    dn={'N':100.,'G':140.,'P':200.}; dh={'HEAVY':180.,'HEAVY+':230.,'GREAT':300.,'SUPER':400.,'CRITICAL':600.}
    cn={'N':credit['NORMAL'],'G':credit['GOOD'],'P':credit['PERFECT']}; ch={k:credit[k] for k in ('HEAVY','HEAVY+','GREAT','SUPER','CRITICAL')}
    use_recipe=mode.startswith('recipe_'); stage_boundary=mode.endswith('_stage_boundary')
    for st in stages:
        workload=float(st['workloadEhp']); stage_start_lv=highest(cum,thr)
        while workload>0:
            lv=stage_start_lv if stage_boundary else highest(cum,thr)
            r=response_recipe(cls,lv,hist,st,maps) if use_recipe else response_global(cls,lv,hist,st)
            if action_no%4==0:
                a=p.judge();b=p.judge();q=p4a.heavy_tier(a,b);base=dh[q];gain=ch[q]
            else:
                q=p.judge();base=dn[q];gain=cn[q]
            workload-=base/r;cum+=gain;action_no+=1
        rows.append({'stage':int(st['stage']),'cumCredit':cum})
    return rows

def unlock(rows,thr):
    for r in rows:
        if r['cumCredit']>=thr:return int(r['stage'])
    return 51

def evaluate(mode,corpus,p4a_sum,hist,maps):
    thr={int(k):float(v) for k,v in p4a_sum['firstPassMidpointAnchorCandidates'].items()}; fx={(f['tier'],f['envelope']):f for f in corpus['fixtures']}; credit=corpus['qualityCredit']
    total=exact=within1=0; ae=0.;mx=0.; outliers=[]
    for cls in CLASSES:
        for tier in TIERS:
            runs=[simulate(fx[(tier,'CENTRAL')]['stages'],tier,i,credit,cls,thr,hist,mode,maps) for i in range(1,101)]
            pred=[float(p4a.quant([unlock(r,thr[lv]) for r in runs],.5)) for lv in LEVELS]
            target=[float(x) for x in hist['p4aMidpointFeedbackPropagationP50Examples'][cls][tier]]
            for lv,a,b in zip(LEVELS,pred,target):
                e=abs(a-b);total+=1;exact+=e<1e-9;within1+=e<=1.;ae+=e;mx=max(mx,e)
                if e>1:outliers.append({'class':cls,'tier':tier,'level':lv,'predicted':a,'historical':b,'absError':e})
    s={'points':total,'exactPoints':exact,'exactRate':round(exact/total,6),'within1StagePoints':within1,'within1StageRate':round(within1/total,6),'meanAbsStageError':round(ae/total,6),'maxAbsStageError':round(mx,6),'outliersGt1':outliers}
    s['gatePass']=s['within1StageRate']>=GATE['within1StageRateMin'] and s['meanAbsStageError']<=GATE['meanAbsStageErrorMax'] and s['maxAbsStageError']<=GATE['maxAbsStageErrorMax']
    return s

def main():
    corpus=p4a.normalize_corpus(json.loads(CORPUS.read_text())); p4a_sum=json.loads(P4A_SUM.read_text());hist=json.loads(P4B.read_text());maps=build_recipe_maps(hist)
    modes=('global_immediate','global_stage_boundary','recipe_immediate','recipe_stage_boundary')
    results={m:evaluate(m,corpus,p4a_sum,hist,maps) for m in modes}
    best=min(modes,key=lambda m:(not results[m]['gatePass'],-results[m]['within1StageRate'],results[m]['meanAbsStageError'],results[m]['maxAbsStageError']))
    out={'version':'p6-b2-p4b-propagation-semantics-matrix-temp-v0.1','authority':'TEMP_RECOVERED_EQUIVALENCE_DIAGNOSTIC_ONLY','recipeMapConstruction':'rank-calibrated per class/level using archived min/median/max; rank signal from materialized-all20 v0.16 reconstruction; milestone results held out for validation','gate':GATE,'results':results,'bestMode':best,'anyGatePass':any(v['gatePass'] for v in results.values()),'shopInjected':False,'productionAuthority':False}
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()
