#!/usr/bin/env python3
from __future__ import annotations
import json, statistics, subprocess, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'
DATA=ROOT/'legacy-game-structure'/'data'
sys.path.insert(0,str(TOOLS))
import simulate_class_aware_layer_a as sim

BASE=DATA/'model_a_representative_recipes_v0_1.yaml'
KIN=DATA/'model_a_kinematic_anchor_v0_1.yaml'
COMBAT=DATA/'model_a_combat_sensitivity_anchor_v0_1.yaml'
TRACE=DATA/'model_a_class_action_trace_bracket_v0_1.yaml'
HIST=DATA/'p4b_combat_feedback_divergence_v0_1.json'
CRIT=DATA/'model_a_critical_role_expression_candidates_v0_1.yaml'
ADD=DATA/'model_a_additional10_role_expression_candidates_v0_1.yaml'
MAT=TOOLS/'materialize_critical_role_candidates.py'
CLASSES=('knight','rogue','tank','archer','mage')

def materialize(overlay:Path):
    s=subprocess.check_output([sys.executable,str(MAT),str(BASE),str(KIN),str(overlay)],text=True)
    return yaml.safe_load(s)['recipes']

def main():
    recipes=materialize(CRIT)+materialize(ADD)
    byid={r['id']:r for r in recipes}
    if len(byid)!=20: raise AssertionError(f'expected 20 unique materialized recipes, got {len(byid)}')
    recipes=[byid[k] for k in sorted(byid)]
    kin=yaml.safe_load(KIN.read_text())
    combat=yaml.safe_load(COMBAT.read_text())
    tdoc=yaml.safe_load(TRACE.read_text())
    trace=tdoc['profiles']['TRACE_BRACKET_CENTRAL']
    pm1=tdoc['powerModes']['CURRENT_AUTHORITY_LV1']
    pm6=tdoc['powerModes']['CURRENT_AUTHORITY_LV6']
    hist=json.loads(HIST.read_text())
    out={'version':'p6-b2-materialized-all20-lv6-fidelity-temp-v0.1','recipeCount':20,'perClass':{},'productionAuthority':False,'shopInjected':False}
    max_med=max_edge=0.0
    for cls in CLASSES:
        a1=[]; a6=[]
        for r in recipes:
            a1.append(sim.simulate(r,kin,combat,trace,cls,pm1)['actions'])
            a6.append(sim.simulate(r,kin,combat,trace,cls,pm6)['actions'])
        ratios=[x/y if y else 1.0 for x,y in zip(a6,a1)]
        med=statistics.median(ratios); lo=min(ratios); hi=max(ratios)
        target=float(hist['all20ActionRatioVsLv1Median'][cls]['Lv6'])
        tr=hist['all20ActionRatioRanges'][cls]['Lv6']
        md=abs(med-target); ed=max(abs(lo-float(tr[0])),abs(hi-float(tr[1])))
        max_med=max(max_med,md); max_edge=max(max_edge,ed)
        out['perClass'][cls]={'median':round(med,6),'range':[round(lo,6),round(hi,6)],'historicalMedian':target,'historicalRange':tr,'medianAbsDiff':round(md,6),'maxRangeEdgeAbsDiff':round(ed,6),'ratios':[round(x,6) for x in ratios]}
    out['summary']={'maxMedianAbsDiff':round(max_med,6),'maxRangeEdgeAbsDiff':round(max_edge,6),'exactAt3Decimals':max_med<0.0005 and max_edge<0.0005}
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__': main()
