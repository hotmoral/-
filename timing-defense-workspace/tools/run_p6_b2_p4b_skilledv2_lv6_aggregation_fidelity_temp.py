#!/usr/bin/env python3
from __future__ import annotations
import json, statistics, sys
from collections import defaultdict
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'; DATA=ROOT/'legacy-game-structure'/'data'
sys.path.insert(0,str(TOOLS))
import simulate_class_aware_role_metrics_v0_2 as sim
import run_skilled_v2_central_role_probe as central_runner

BASE=DATA/'model_a_representative_recipes_v0_1.yaml'
KIN=DATA/'model_a_kinematic_anchor_v0_1.yaml'
COMBAT=DATA/'model_a_combat_sensitivity_anchor_v0_1.yaml'
LEGACY=DATA/'model_a_class_action_trace_bracket_v0_1.yaml'
CENTRAL=DATA/'skilled_v2_central_sequence_candidate_v0_1.yaml'
HIST=DATA/'p4b_combat_feedback_divergence_v0_1.json'
OVERLAYS=[DATA/'model_a_critical_role_expression_candidates_v0_1.yaml',DATA/'model_a_additional10_role_expression_candidates_v0_1.yaml']
SEEDS=(101,211,307)
CLASSES=tuple(sim.CLASSES)

def load(p): return yaml.safe_load(p.read_text()) or {}

def one(recipe,kin,combat,central,pm,cls,seed):
    consumed=[]; rs=central_runner.row_seed(seed,str(recipe['id']),cls)
    old=sim.judge_stream
    try:
        def seeded(_ps,_bj): return central_runner.central_judge_stream(central,rs,consumed)
        sim.judge_stream=seeded
        tc={'perfectStreakJudges':1,'breakJudge':'GOOD','actionIntervalMs':1100,'targetReacquireDelayMs':0}
        return int(sim.simulate(recipe,kin,combat,tc,cls,pm).get('actions') or 0)
    finally: sim.judge_stream=old

def stats(vals): return {'median':round(statistics.median(vals),6),'range':[round(min(vals),6),round(max(vals),6)]}

def main():
    base=load(BASE); kin=load(KIN); combat=load(COMBAT); legacy=load(LEGACY); central=load(CENTRAL); hist=json.loads(HIST.read_text())
    recipes=central_runner.materialize_all20(base,kin,[load(p) for p in OVERLAYS])
    pm1=legacy['powerModes']['CURRENT_AUTHORITY_LV1']; pm6=legacy['powerModes']['CURRENT_AUTHORITY_LV6']
    out={'version':'p6-b2-p4b-skilledv2-lv6-aggregation-fidelity-temp-v0.1','perClass':{},'shopInjected':False,'productionAuthority':False}
    for cls in CLASSES:
        rows=[]; per_recipe=defaultdict(list); counts=defaultdict(lambda:{'lv1':[],'lv6':[]})
        for r in recipes:
            for seed in SEEDS:
                a1=one(r,kin,combat,central,pm1,cls,seed); a6=one(r,kin,combat,central,pm6,cls,seed)
                ratio=a6/a1 if a1 else 1.0
                rows.append(ratio); per_recipe[str(r['id'])].append(ratio); counts[str(r['id'])]['lv1'].append(a1); counts[str(r['id'])]['lv6'].append(a6)
        recipe_ratio_medians=[statistics.median(v) for v in per_recipe.values()]
        ratio_of_recipe_action_medians=[]
        for rid in sorted(counts):
            a1=statistics.median(counts[rid]['lv1']); a6=statistics.median(counts[rid]['lv6']); ratio_of_recipe_action_medians.append(a6/a1 if a1 else 1.0)
        target={'median':float(hist['all20ActionRatioVsLv1Median'][cls]['Lv6']),'range':[float(x) for x in hist['all20ActionRatioRanges'][cls]['Lv6']]}
        modes={'all60RowRatios':stats(rows),'recipeMedianOfRatios':stats(recipe_ratio_medians),'ratioOfRecipeActionMedians':stats(ratio_of_recipe_action_medians)}
        for m in modes.values():
            m['medianAbsDiff']=round(abs(m['median']-target['median']),6)
            m['maxRangeEdgeAbsDiff']=round(max(abs(m['range'][0]-target['range'][0]),abs(m['range'][1]-target['range'][1])),6)
        best=min(modes,key=lambda k:(modes[k]['medianAbsDiff'],modes[k]['maxRangeEdgeAbsDiff']))
        out['perClass'][cls]={'historical':target,'modes':modes,'bestByMedianThenRange':best}
    scores={m:{'maxMedianAbsDiff':0.0,'maxRangeEdgeAbsDiff':0.0,'sumMedianAbsDiff':0.0} for m in ('all60RowRatios','recipeMedianOfRatios','ratioOfRecipeActionMedians')}
    for rec in out['perClass'].values():
        for mode,st in rec['modes'].items():
            scores[mode]['maxMedianAbsDiff']=max(scores[mode]['maxMedianAbsDiff'],st['medianAbsDiff'])
            scores[mode]['maxRangeEdgeAbsDiff']=max(scores[mode]['maxRangeEdgeAbsDiff'],st['maxRangeEdgeAbsDiff'])
            scores[mode]['sumMedianAbsDiff']+=st['medianAbsDiff']
    for s in scores.values():
        for k in s:s[k]=round(s[k],6)
    out['aggregationScores']=scores
    out['bestAggregation']=min(scores,key=lambda k:(scores[k]['sumMedianAbsDiff'],scores[k]['maxMedianAbsDiff'],scores[k]['maxRangeEdgeAbsDiff']))
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__': main()
