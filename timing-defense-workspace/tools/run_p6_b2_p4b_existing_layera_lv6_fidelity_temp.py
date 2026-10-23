#!/usr/bin/env python3
from __future__ import annotations
import json, statistics, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import simulate_class_aware_layer_a as sim

DATA=ROOT/'legacy-game-structure'/'data'
RECIPES=DATA/'model_a_representative_recipes_v0_1.yaml'
KIN=DATA/'model_a_kinematic_anchor_v0_1.yaml'
COMBAT=DATA/'model_a_combat_sensitivity_anchor_v0_1.yaml'
TRACE=DATA/'model_a_class_action_trace_bracket_v0_1.yaml'
HIST=DATA/'p4b_combat_feedback_divergence_v0_1.json'
CLASSES=('knight','rogue','tank','archer','mage')

def main():
    recipes=yaml.safe_load(RECIPES.read_text())['recipes']
    kin=yaml.safe_load(KIN.read_text())
    combat=yaml.safe_load(COMBAT.read_text())
    trace_doc=yaml.safe_load(TRACE.read_text())
    trace=trace_doc['profiles']['TRACE_BRACKET_CENTRAL']
    pm1=trace_doc['powerModes']['CURRENT_AUTHORITY_LV1']
    pm6=trace_doc['powerModes']['CURRENT_AUTHORITY_LV6']
    hist=json.loads(HIST.read_text())
    out={'version':'p6-b2-existing-layera-lv6-fidelity-temp-v0.1','recipeCount':len(recipes),'perClass':{},'productionAuthority':False}
    max_med=max_edge=0.0
    for cls in CLASSES:
        a1=[];a6=[]
        for r in recipes:
            a1.append(sim.simulate(r,kin,combat,trace,cls,pm1)['actions'])
            a6.append(sim.simulate(r,kin,combat,trace,cls,pm6)['actions'])
        ratios=[x/y if y else 1.0 for x,y in zip(a6,a1)]
        med=statistics.median(ratios); lo=min(ratios); hi=max(ratios)
        target=float(hist['all20ActionRatioVsLv1Median'][cls]['Lv6'])
        tr=hist['all20ActionRatioRanges'][cls]['Lv6']
        md=abs(med-target);ed=max(abs(lo-float(tr[0])),abs(hi-float(tr[1])))
        max_med=max(max_med,md);max_edge=max(max_edge,ed)
        out['perClass'][cls]={'lv1Actions':a1,'lv6Actions':a6,'ratios':[round(x,6) for x in ratios],'median':round(med,6),'range':[round(lo,6),round(hi,6)],'historicalMedian':target,'historicalRange':tr,'medianAbsDiff':round(md,6),'maxRangeEdgeAbsDiff':round(ed,6)}
    out['summary']={'maxMedianAbsDiff':round(max_med,6),'maxRangeEdgeAbsDiff':round(max_edge,6),'exactAt3Decimals':max_med<0.0005 and max_edge<0.0005}
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()
